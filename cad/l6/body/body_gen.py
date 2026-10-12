#!/usr/bin/env python3
"""body_gen.py - the parametric generator of the L.6.0 rotating-square body.

Source: FINAL/21-stretch-stem-and-projection.md, Sections 21.2.1, 21.2.2,
21.2.4 and 21.2.6. Units are millimetres. The body centre is the origin.

The model
---------
* 8 x 16 = 128 rigid tiles of 10 x 10 x 2.00 mm, with chamfered corners.
* Tile (i, j) turns by s * theta, s = (-1)^(i+j). The tile pitch is
  L = a (cos theta + sin theta). Neighbours share one corner pivot.
* Each neighbour pair carries one edge-on polyimide ribbon. The ribbon is a
  fixed-length arc (0.80 mm) between the two chamfer-face midpoints. It
  bulges toward the pivot, and its ends sink 30 um into the two tiles.
* The hinges that cross a quadrant seam are split couplers: the ribbon is
  cut at its middle, so the quadrant lifts out.
* Six Si3N4 kinematic seat balls sit at split-coupler pivots, below the
  ribbon layer. Each quadrant sees three of them (a Maxwell seat).
* The Qi2.2 sector coil zone is an annulus at the "+" crossing, clipped to
  each tile at rest and carried by the tile in every state.

Run:  python3 body_gen.py            (writes STL, SVG, PNG and JSON here)
"""
import json
import math
import os
from dataclasses import dataclass, asdict, field

import numpy as np
import trimesh
from scipy.optimize import brentq
from shapely.geometry import Polygon, Point
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class BodyParams:
    a: float = 10.0               # tile cell pitch at rest [DECISION] 21.2.1
    kerf: float = 0.010           # cut between tiles, <= 10 um [DECISION] 21.2.4
    nx: int = 8                   # columns [DECISION]
    ny: int = 16                  # rows [DECISION]
    t: float = 2.00               # tile thickness [DECISION] 21.2.7
    chamfer: float = 0.55         # chamfer leg; set by the ribbon length rule
    rib_len: float = 0.80         # ribbon free length [DECISION] 21.2.2
    rib_thk: float = 0.0125       # 12.5 um polyimide [DECISION]
    rib_z0: float = 0.68          # ribbon bottom, above the seat balls
    rib_h: float = 1.20           # ribbon height, inside 1.2-1.5 mm [DECISION]
    rib_embed: float = 0.03       # bond length into each chamfer face
    rib_seg: int = 6              # arc segments
    split_gap: float = 0.02       # cut of a split coupler
    ball_d: float = 0.60          # Si3N4 seat ball [HYPOTHESIS]
    ball_zc: float = 0.36         # ball centre height, below the ribbons
    # edge softening, order of Ayaz 2026-10-12, HARDWARE/06 doctrine
    r_perim: float = 0.65         # outer perimeter front and back face edges
    R_corner: float = 6.35        # the four outer plan corners
    r_break: float = 0.03         # cap top edge, back edge and chamfer corners
    n_perim: int = 6              # segments of a 0.65 mm quarter fillet
    n_break: int = 2              # segments of a 0.03 mm edge break
    n_corner: int = 8             # segments of the R 6.35 mm plan corner
    run_out: float = 2.0          # run-out of r_perim to r_break at a hinge chamfer
    n_run: int = 6                # samples of the run-out
    qi_od: float = 45.0           # Qi coil outer diameter 44-46 mm [DECISION]
    qi_id: float = 20.0           # Qi coil inner diameter [HYPOTHESIS]
    # seat ball sites: target positions at rest, snapped to split couplers
    seat_targets: list = field(default_factory=lambda: [
        ("Q1|Q2", (0.0, 15.0)), ("Q1|Q2", (0.0, 65.0)),
        ("Q3|Q4", (0.0, -15.0)), ("Q3|Q4", (0.0, -65.0)),
        ("Q1|Q4", (25.0, 0.0)), ("Q2|Q3", (-25.0, 0.0)),
    ])


STATES = [("rest", 0.0), ("default", 17.5), ("max", 45.0)]


def rot(phi):
    c, s = math.cos(phi), math.sin(phi)
    return np.array([[c, -s], [s, c]])


def quadrant(p, i, j):
    right = i >= p.nx // 2
    top = j >= p.ny // 2
    return {(True, True): "Q1", (False, True): "Q2",
            (False, False): "Q3", (True, False): "Q4"}[(right, top)]


class Body:
    """The body at one turn angle theta (degrees)."""

    def __init__(self, p: BodyParams, theta_deg: float):
        self.p = p
        self.theta_deg = theta_deg
        th = math.radians(theta_deg)
        self.th = th
        self.L = p.a * (math.cos(th) + math.sin(th))
        h = p.a / 2
        self.local_corners = np.array([[h, h], [-h, h], [-h, -h], [h, -h]])
        self.tiles = []
        for j in range(p.ny):
            for i in range(p.nx):
                s = 1 if (i + j) % 2 == 0 else -1
                c = np.array([(i - (p.nx - 1) / 2) * self.L,
                              (j - (p.ny - 1) / 2) * self.L])
                c0 = np.array([(i - (p.nx - 1) / 2) * p.a,
                               (j - (p.ny - 1) / 2) * p.a])
                R = rot(s * th)
                self.tiles.append(dict(i=i, j=j, s=s, c=c, c0=c0, R=R,
                                       q=quadrant(p, i, j)))
        self.index = {(t["i"], t["j"]): k for k, t in enumerate(self.tiles)}
        self._hinges()

    # -- geometry of one tile -------------------------------------------
    def corners(self, k):
        t = self.tiles[k]
        return self.local_corners @ t["R"].T + t["c"]

    def plan_local(self, k):
        """The plan outline of tile k in its own frame, CCW.

        Returns (vertices, radii). radii[m] is the front and back edge
        fillet radius at vertex m:
        * r_perim on an outer perimeter face and on the R 6.35 mm corner,
        * r_break on every interior face, chamfer and chamfer round,
        * a smoothstep run-out from r_perim to r_break over run_out mm
          where a perimeter face meets a hinge chamfer.
        """
        p = self.p
        t = self.tiles[k]
        c = p.chamfer
        perim = {0: t["j"] == p.ny - 1, 1: t["i"] == 0,
                 2: t["j"] == 0, 3: t["i"] == p.nx - 1}   # sides top, left, bottom, right
        # the physical tile is the 10 mm cell less the kerf: 9.990 mm
        C = self.local_corners * (p.a - p.kerf) / p.a

        def rounded(V, din, dout, r, n):
            turn = math.atan2(din[0] * dout[1] - din[1] * dout[0], np.dot(din, dout))
            tl = r * math.tan(turn / 2)
            A = V - tl * din
            O = A + r * np.array([-din[1], din[0]])
            a0 = math.atan2(A[1] - O[1], A[0] - O[0])
            return [O + r * np.array([math.cos(a0 + turn * m / n), math.sin(a0 + turn * m / n)])
                    for m in range(n + 1)]

        feats = []          # per corner: (points, radius, kind)
        for kc in range(4):
            V = C[kc]
            din = (C[kc] - C[(kc - 1) % 4]) / (p.a - p.kerf)
            dout = (C[(kc + 1) % 4] - C[kc]) / (p.a - p.kerf)
            if perim[(kc - 1) % 4] and perim[kc]:
                feats.append((rounded(V, din, dout, p.R_corner, p.n_corner), p.r_perim, "R"))
            else:
                A, B = V - c * din, V + c * dout
                dch = (B - A) / np.linalg.norm(B - A)
                pts = rounded(A, din, dch, p.r_break, p.n_break) + \
                    rounded(B, dch, dout, p.r_break, p.n_break)
                feats.append((pts, p.r_break, "C"))
        verts, radii = [], []

        def smooth(u):
            u = min(max(u, 0.0), 1.0)
            return u * u * (3 - 2 * u)

        for kc in range(4):
            pts, r, kind = feats[kc]
            verts += pts
            radii += [r] * len(pts)
            if not perim[kc]:
                continue
            S = np.array(pts[-1])
            nxt = feats[(kc + 1) % 4]
            E = np.array(nxt[0][0])
            Ls = np.linalg.norm(E - S)
            u = (E - S) / Ls
            ss = []
            if kind == "C":
                ss += [p.run_out * m / p.n_run for m in range(1, p.n_run + 1)]
            if nxt[2] == "C":
                ss += [Ls - p.run_out * m / p.n_run for m in range(p.n_run, 0, -1)]
            for sv in sorted(set(np.round(ss, 9))):
                if 1e-6 < sv < Ls - 1e-6:
                    w = 1.0
                    if kind == "C":
                        w = min(w, smooth(sv / p.run_out))
                    if nxt[2] == "C":
                        w = min(w, smooth((Ls - sv) / p.run_out))
                    verts.append(S + sv * u)
                    radii.append(p.r_break + (p.r_perim - p.r_break) * w)
        return np.array(verts), np.array(radii)

    def tile_poly2d(self, k):
        t = self.tiles[k]
        return self.plan_local(k)[0] @ t["R"].T + t["c"]

    def chamfer_mid_dist(self):
        return (self.p.chamfer + self.p.kerf) / math.sqrt(2)

    def to_state(self, k, xy_rest):
        """Carry a rest-state point of tile k into this state."""
        t = self.tiles[k]
        return (np.asarray(xy_rest) - t["c0"]) @ t["R"].T + t["c"]

    # -- hinges ----------------------------------------------------------
    def _hinges(self):
        """Find the shared corner of each neighbour pair.

        The corner pairing is read at a small probe angle, because at
        theta = 0 two corner pairs coincide along the shared edge.
        """
        probe = Body.__new__(Body)
        probe.p = self.p
        probe.local_corners = self.local_corners
        pt = math.radians(1.0)
        probe.tiles = [dict(t, R=rot(t["s"] * pt),
                            c=t["c0"] * (math.cos(pt) + math.sin(pt)) / 1.0)
                       for t in self.tiles]
        self.hinges = []
        for k, t in enumerate(self.tiles):
            for di, dj in ((1, 0), (0, 1)):
                n = self.index.get((t["i"] + di, t["j"] + dj))
                if n is None:
                    continue
                ca, cb = probe.corners(k), probe.corners(n)
                d = np.linalg.norm(ca[:, None, :] - cb[None, :, :], axis=2)
                ia, ib = np.unravel_index(np.argmin(d), d.shape)
                srt = np.sort(d.ravel())
                assert srt[0] < 1e-9 and srt[1] > 1e-3, "pivot not unique"
                P = self.corners(k)[ia]
                Pb = self.corners(n)[ib]
                split = t["q"] != self.tiles[n]["q"]
                self.hinges.append(dict(a=k, b=n, ca=int(ia), cb=int(ib),
                                        P=(P + Pb) / 2,
                                        gap=float(np.linalg.norm(P - Pb)),
                                        split=split,
                                        seam="|".join(sorted([t["q"], self.tiles[n]["q"]]))
                                        if split else ""))

    def ribbon_paths(self, h):
        """The centre line of the ribbon of hinge h, as one or two polylines."""
        p = self.p
        A, B = self.tiles[h["a"]], self.tiles[h["b"]]
        P = h["P"]
        r_m = (p.chamfer + p.kerf) / math.sqrt(2)   # pivot to chamfer midpoint
        uA = (A["c"] - P) / np.linalg.norm(A["c"] - P)
        uB = (B["c"] - P) / np.linalg.norm(B["c"] - P)
        MA, MB = P + r_m * uA, P + r_m * uB
        d = np.linalg.norm(MB - MA)
        assert d < p.rib_len, f"ribbon too short: chord {d:.4f}"
        u = (MB - MA) / d
        mid = (MA + MB) / 2
        away = P - (A["c"] + B["c"]) / 2
        n = np.array([-u[1], u[0]])
        if np.dot(n, away) < 0:
            n = -n
        alpha = brentq(lambda x: math.sin(x) / x - d / p.rib_len, 1e-9, math.pi - 1e-9)
        R = p.rib_len / (2 * alpha)
        Cc = mid - R * math.cos(alpha) * n

        def arc(t0, t1, m):
            ts = np.linspace(t0, t1, m + 1)
            return np.array([Cc + R * (math.sin(t) * u + math.cos(t) * n) for t in ts])

        eA = MA + p.rib_embed * uA
        eB = MB + p.rib_embed * uB
        if not h["split"]:
            pts = arc(-alpha, alpha, p.rib_seg)
            return [np.vstack([eA, pts, eB])]
        dl = p.split_gap / 2 / R
        m = max(p.rib_seg // 2, 2)
        return [np.vstack([eA, arc(-alpha, -dl, m)]),
                np.vstack([arc(dl, alpha, m), eB])]

    def ribbon_sag(self, h):
        """Chord and sagitta of the ribbon arc of hinge h."""
        p = self.p
        A, B = self.tiles[h["a"]], self.tiles[h["b"]]
        P = h["P"]
        r_m = (p.chamfer + p.kerf) / math.sqrt(2)   # pivot to chamfer midpoint
        MA = P + r_m * (A["c"] - P) / np.linalg.norm(A["c"] - P)
        MB = P + r_m * (B["c"] - P) / np.linalg.norm(B["c"] - P)
        d = float(np.linalg.norm(MB - MA))
        alpha = brentq(lambda x: math.sin(x) / x - d / p.rib_len, 1e-9, math.pi - 1e-9)
        R = p.rib_len / (2 * alpha)
        return d, R * (1 - math.cos(alpha))

    # -- seat balls ------------------------------------------------------
    def seat_hinges(self):
        """Snap each seat target (rest coordinates) to a split coupler."""
        rest = self if self.theta_deg == 0 else Body(self.p, 0.0)
        out = []
        for seam, xy in self.p.seat_targets:
            best, bd = None, 1e9
            for hi, h in enumerate(rest.hinges):
                if h["seam"] != seam:
                    continue
                # skip the "+" crossing itself
                if np.linalg.norm(h["P"]) < 1e-6:
                    continue
                dd = np.linalg.norm(h["P"] - np.array(xy))
                if dd < bd:
                    best, bd = hi, dd
            out.append(best)
        return out

    # -- qi zone ---------------------------------------------------------
    def qi_pieces(self):
        """The coil annulus cut per tile at rest, carried into this state."""
        p = self.p
        ring = Point(0, 0).buffer(p.qi_od / 2, 256).difference(
            Point(0, 0).buffer(p.qi_id / 2, 256))
        rest = Body(p, 0.0)
        pieces = []
        for k in range(len(self.tiles)):
            tp = Polygon(rest.tile_poly2d(k))
            g = ring.intersection(tp)
            if g.is_empty or g.area < 1e-6:
                continue
            geoms = getattr(g, "geoms", [g])
            for gg in geoms:
                if gg.geom_type != "Polygon":
                    continue
                ext = np.array(gg.exterior.coords)
                pieces.append(dict(k=k, q=self.tiles[k]["q"],
                                   xy=self.to_state(k, ext), area=gg.area))
        return pieces

    def seam_edges(self):
        """The seam-facing edge of every tile on a quadrant line."""
        edges = []
        mx, my = self.p.nx // 2, self.p.ny // 2
        for k, t in enumerate(self.tiles):
            i, j = t["i"], t["j"]
            h = self.p.a / 2
            loc = []
            if i == mx - 1:
                loc.append(((h, -h), (h, h)))
            if i == mx:
                loc.append(((-h, -h), (-h, h)))
            if j == my - 1:
                loc.append(((-h, h), (h, h)))
            if j == my:
                loc.append(((-h, -h), (h, -h)))
            for e in loc:
                edges.append(np.array(e) @ t["R"].T + t["c"])
        return edges


# ---------------------------------------------------------------------------
# meshing, with no triangulation engine (convex fans and strips only)
# ---------------------------------------------------------------------------
def prism_convex(poly, z0, z1):
    poly = np.asarray(poly, float)
    n = len(poly)
    area = 0.5 * np.sum(poly[:, 0] * np.roll(poly[:, 1], -1) - np.roll(poly[:, 0], -1) * poly[:, 1])
    if area < 0:
        poly = poly[::-1]
    v = np.vstack([np.c_[poly, np.full(n, z0)], np.c_[poly, np.full(n, z1)]])
    f = []
    for k in range(1, n - 1):
        f.append([0, k + 1, k])               # bottom, facing -z
        f.append([n, n + k, n + k + 1])       # top, facing +z
    for k in range(n):
        k2 = (k + 1) % n
        f.append([k, k2, n + k2])
        f.append([k, n + k2, n + k])
    return trimesh.Trimesh(v, np.array(f), process=False)


def fillet_levels(r, n, t):
    """z levels of a quarter fillet of radius r at the bottom and the top."""
    phi = np.linspace(0, math.pi / 2, n + 1)
    zb = r - r * np.sin(phi)
    return np.concatenate([zb, t - zb])


def fillet_inset(r, z, t):
    """Inset of a face with radius r fillets on its front and back edges."""
    zz = np.minimum(z, t - z)
    if zz >= r:
        return 0.0
    return r - math.sqrt(max(r * r - (r - zz) ** 2, 0.0))


def tile_layers(verts, radii, p):
    """The z levels and the plan loops of a softened tile.

    Each plan vertex moves inward along its miter vector by the inset of
    its own quarter fillet, so every vertex column traces an exact
    quarter circle of its radius at the front and at the back.
    """
    n = len(verts)
    e = np.roll(verts, -1, axis=0) - verts
    e /= np.linalg.norm(e, axis=1)[:, None]
    nrm = np.c_[e[:, 1], -e[:, 0]]                 # outward normals of CCW edges
    n1, n2 = np.roll(nrm, 1, axis=0), nrm
    miter = (n1 + n2) / (1 + np.einsum("ij,ij->i", n1, n2))[:, None]
    zs = set(np.round(fillet_levels(p.r_break, p.n_break, p.t), 9))
    for r in set(np.round(radii, 9)):
        if r > p.r_break + 1e-9:
            zs |= set(np.round(fillet_levels(p.r_perim, p.n_perim, p.t), 9))
            break
    zs = sorted(zs)
    loops = []
    for z in zs:
        d = np.array([fillet_inset(r, z, p.t) for r in radii])
        loops.append(verts - d[:, None] * miter)
    return np.array(zs), loops


def loop_at(verts, radii, p, z):
    """The plan loop of a softened tile at one height z."""
    zs, loops = tile_layers(verts, radii, p)
    e = np.roll(verts, -1, axis=0) - verts
    e /= np.linalg.norm(e, axis=1)[:, None]
    nrm = np.c_[e[:, 1], -e[:, 0]]
    n1 = np.roll(nrm, 1, axis=0)
    miter = (n1 + nrm) / (1 + np.einsum("ij,ij->i", n1, nrm))[:, None]
    d = np.array([fillet_inset(r, z, p.t) for r in radii])
    return verts - d[:, None] * miter


def softened_tile(verts, radii, p):
    zs, loops = tile_layers(verts, radii, p)
    n, m = len(verts), len(zs)
    V = [np.c_[lp, np.full(n, z)] for lp, z in zip(loops, zs)]
    cen = verts.mean(axis=0)
    V.append([[cen[0], cen[1], zs[0]], [cen[0], cen[1], zs[-1]]])
    V = np.vstack(V)
    cb, ct = m * n, m * n + 1
    top = (m - 1) * n
    F = []
    for k in range(n):
        k2 = (k + 1) % n
        F.append([cb, k2, k])
        F.append([ct, top + k, top + k2])
    for L in range(m - 1):
        a0, b0 = L * n, (L + 1) * n
        for k in range(n):
            k2 = (k + 1) % n
            F.append([a0 + k, a0 + k2, b0 + k2])
            F.append([a0 + k, b0 + k2, b0 + k])
    mesh = trimesh.Trimesh(V, np.array(F), process=False)
    mesh.merge_vertices()
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    return mesh


def tile_mesh(body, k):
    verts, radii = body.plan_local(k)
    m = softened_tile(verts, radii, body.p)
    t = body.tiles[k]
    T = np.eye(4)
    T[:2, :2] = t["R"]
    T[:2, 3] = t["c"]
    m.apply_transform(T)
    return m


def strip_offsets(path, w):
    """Left and right offset lines of a polyline, with mitred joints."""
    path = np.asarray(path, float)
    seg = np.diff(path, axis=0)
    seg /= np.linalg.norm(seg, axis=1)[:, None]
    nrm = np.c_[-seg[:, 1], seg[:, 0]]
    vn = np.zeros_like(path)
    vn[0], vn[-1] = nrm[0], nrm[-1]
    for k in range(1, len(path) - 1):
        m = nrm[k - 1] + nrm[k]
        m /= np.linalg.norm(m)
        vn[k] = m / max(np.dot(m, nrm[k]), 0.2)
    return path + vn * w / 2, path - vn * w / 2


def extrude_strip(path, w, z0, z1):
    Lf, Rt = strip_offsets(path, w)
    n = len(path)
    # vertex blocks: L bottom, R bottom, L top, R top
    v = np.vstack([np.c_[Lf, np.full(n, z0)], np.c_[Rt, np.full(n, z0)],
                   np.c_[Lf, np.full(n, z1)], np.c_[Rt, np.full(n, z1)]])
    LB, RB, LT, RT = 0, n, 2 * n, 3 * n
    f = []
    for k in range(n - 1):
        a, b = k, k + 1
        f += [[LB + a, LB + b, RB + b], [LB + a, RB + b, RB + a]]   # bottom
        f += [[LT + a, RT + b, LT + b], [LT + a, RT + a, RT + b]]   # top
        f += [[LB + a, LT + b, LB + b], [LB + a, LT + a, LT + b]]   # left wall
        f += [[RB + a, RB + b, RT + b], [RB + a, RT + b, RT + a]]   # right wall
    f += [[LB, RB, RT], [LB, RT, LT]]                               # start cap
    e = n - 1
    f += [[LB + e, RT + e, RB + e], [LB + e, LT + e, RT + e]]       # end cap
    m = trimesh.Trimesh(v, np.array(f), process=False)
    if m.volume < 0:
        m.invert()
    return m


def build_mesh(body: Body):
    p = body.p
    parts = {"tiles": [], "ribbons": [], "balls": []}
    for k in range(len(body.tiles)):
        parts["tiles"].append(tile_mesh(body, k))
    for h in body.hinges:
        for path in body.ribbon_paths(h):
            parts["ribbons"].append(extrude_strip(path, p.rib_thk, p.rib_z0, p.rib_z0 + p.rib_h))
    for hi in body.seat_hinges():
        P = body.hinges[hi]["P"]
        s = trimesh.creation.icosphere(subdivisions=1, radius=p.ball_d / 2)
        s.apply_translation([P[0], P[1], p.ball_zc])
        parts["balls"].append(s)
    return parts


# ---------------------------------------------------------------------------
# plans
# ---------------------------------------------------------------------------
QCOL = {"Q1": "#cfe3f5", "Q2": "#d8efd4", "Q3": "#f6e3c6", "Q4": "#ead7f0"}


def draw_plan(ax, body: Body, title=True):
    from matplotlib.patches import Polygon as MPoly, Circle
    p = body.p
    for k, t in enumerate(body.tiles):
        ax.add_patch(MPoly(body.tile_poly2d(k), closed=True, fc=QCOL[t["q"]],
                           ec="#334", lw=0.25))
    for pc in body.qi_pieces():
        ax.add_patch(MPoly(pc["xy"], closed=True, fc="#e8a33d", ec="#a8641a",
                           lw=0.3, alpha=0.55))
    for h in body.hinges:
        for path in body.ribbon_paths(h):
            ax.plot(path[:, 0], path[:, 1], color="#b02020" if h["split"] else "#555",
                    lw=0.35)
    for e in body.seam_edges():
        ax.plot(e[:, 0], e[:, 1], color="#d01818", lw=0.9)
    for hi in body.seat_hinges():
        P = body.hinges[hi]["P"]
        ax.add_patch(Circle(P, 1.3, fc="#1b4d9e", ec="white", lw=0.4, zorder=5))
    ext = body.L * np.array([p.nx, p.ny]) / 2
    ax.plot([-ext[0], ext[0], ext[0], -ext[0], -ext[0]],
            [-ext[1], -ext[1], ext[1], ext[1], -ext[1]], ls="--", lw=0.4, color="#888")
    for q, (sx, sy) in {"Q1": (1, 1), "Q2": (-1, 1), "Q3": (-1, -1), "Q4": (1, -1)}.items():
        ax.text(sx * ext[0] * 0.5, sy * ext[1] * 0.5, q, ha="center", va="center",
                fontsize=11, color="#223", weight="bold", alpha=0.55, zorder=6)
    ax.set_aspect("equal")
    ax.set_xlim(-60, 60)
    ax.set_ylim(-118, 118)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(f"θ = {body.theta_deg:g}°\n{2*ext[0]:.1f} x {2*ext[1]:.1f} mm lattice",
                     fontsize=9)


def write_plans(p, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    files = []
    for name, th in STATES:
        b = Body(p, th)
        fig, ax = plt.subplots(figsize=(4.2, 7.6))
        draw_plan(ax, b)
        fig.text(0.5, 0.012, "red: quadrant split lines and split couplers · blue: seat balls · "
                 "orange: Qi sector coil zone", ha="center", fontsize=5.5)
        fig.tight_layout(rect=(0, 0.02, 1, 1))
        for ext in ("svg", "png"):
            fn = os.path.join(outdir, f"plan-{name}.{ext}")
            fig.savefig(fn, dpi=220)
            files.append(fn)
        plt.close(fig)
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 7.4))
    for ax, (name, th) in zip(axs, STATES):
        draw_plan(ax, Body(p, th))
    fig.suptitle("Budlum Leaf L.6.0 rotating-square body, top view, same scale", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fn = os.path.join(outdir, "plan-three-states.png")
    fig.savefig(fn, dpi=200)
    files.append(fn)
    plt.close(fig)
    # hinge detail: a seam node with a seat ball, and a plain node
    from matplotlib.patches import Polygon as MPoly, Circle
    fig, axs = plt.subplots(2, 3, figsize=(10.5, 7.2))
    for col, (name, th) in enumerate(STATES):
        b = Body(p, th)
        seat = b.seat_hinges()[0]
        plain = next(hi for hi, h in enumerate(b.hinges)
                     if b.tiles[h["a"]]["i"] == 2 and b.tiles[h["a"]]["j"] == 3)
        for row, hi in enumerate((seat, plain)):
            ax = axs[row, col]
            P0 = b.hinges[hi]["P"]
            for k in range(len(b.tiles)):
                poly = b.tile_poly2d(k)
                if np.min(np.linalg.norm(poly - P0, axis=1)) < 4:
                    ax.add_patch(MPoly(poly, closed=True, fc=QCOL[b.tiles[k]["q"]], ec="#334", lw=0.5))
            for h in b.hinges:
                if np.linalg.norm(h["P"] - P0) < 3:
                    for path in b.ribbon_paths(h):
                        ax.plot(path[:, 0], path[:, 1], color="#b02020" if h["split"] else "#222", lw=1.2)
                    ax.plot(*h["P"], "k+", ms=5, mew=0.6)
            if row == 0:
                ax.add_patch(Circle(P0, p.ball_d / 2, fc="#1b4d9e", ec="none", alpha=0.45))
            ax.set_xlim(P0[0] - 1.6, P0[0] + 1.6)
            ax.set_ylim(P0[1] - 1.6, P0[1] + 1.6)
            ax.set_aspect("equal")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f"θ = {th:g}°, " + ("seam split coupler + seat ball" if row == 0 else "plain hinge"),
                         fontsize=8)
    fig.suptitle("Hinge detail, 3.2 x 3.2 mm windows: 0.80 mm PI ribbon on chamfer midpoints, + = pivot",
                 fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fn = os.path.join(outdir, "plan-hinge-detail.png")
    fig.savefig(fn, dpi=200)
    files.append(fn)
    plt.close(fig)
    return files


def main():
    p = BodyParams()
    out = {"params": asdict(p), "states": {}}
    names = {"rest": "body-rest.stl", "default": "body-default.stl", "max": "body-max.stl"}
    for name, th in STATES:
        b = Body(p, th)
        parts = build_mesh(b)
        allm = parts["tiles"] + parts["ribbons"] + parts["balls"]
        mesh = trimesh.util.concatenate(allm)
        fn = os.path.join(HERE, names[name])
        mesh.export(fn)
        seats = b.seat_hinges()
        out["states"][name] = dict(
            theta_deg=th, file=names[name], n_tiles=len(parts["tiles"]),
            n_ribbon_bodies=len(parts["ribbons"]), n_balls=len(parts["balls"]),
            n_faces=int(len(mesh.faces)), bytes=os.path.getsize(fn),
            seat_balls=[dict(seam=b.hinges[hi]["seam"],
                             xy=[round(float(v), 4) for v in b.hinges[hi]["P"]],
                             z=p.ball_zc) for hi in seats])
        print(f"{name:8s} θ={th:5.1f}°  {fn}  faces={len(mesh.faces)}  "
              f"{os.path.getsize(fn)/1e6:.2f} MB")
    out["plans"] = [os.path.basename(f) for f in write_plans(p, HERE)]
    with open(os.path.join(HERE, "body-geometry.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("plans:", ", ".join(out["plans"]))


if __name__ == "__main__":
    main()
