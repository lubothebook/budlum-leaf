#!/usr/bin/env python3
# BUDLUM LEAF · cad/edge_audit.py · revision L.6.0 · 2026-10-12
#
# The soft-edge audit of every STL in cad/models (TEAM-BRIEF section 4).
#
# For each STL it reports:
#   watertight   every edge is shared by exactly two faces
#   bbox         the bounding box in mm
#   sharp        the exposed convex edges whose normal turn is above 30 deg
#                (a raw 90 deg edge turns 90 deg; a fillet of n segments turns 90/n per edge)
#   max_turn     the largest normal turn over the exposed convex edges, in deg
#   len_sharp    the summed length of the sharp exposed edges, in mm
# An edge is exposed when a point 0.03 mm outside it lies in no other part of the same STL.
#
# Then it measures the named touch-edge radii by slicing the meshes and fitting circles.
#
# Usage:
#   python3 cad/edge_audit.py                 # audit cad/models, print the table
#   python3 cad/edge_audit.py DIR out.json    # audit DIR, also write the numbers as JSON

import json
import math
import os
import sys

import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
SHARP_DEG = 30.0
PROBE = 0.03


def winding(tris, pts):
    """Generalised winding number of each point against a closed triangle set (about 1 inside, 0 outside)."""
    w = np.zeros(len(pts))
    for s in range(0, len(pts), 256):
        p = pts[s:s + 256][:, None, :]
        a = tris[None, :, 0, :] - p
        b = tris[None, :, 1, :] - p
        c = tris[None, :, 2, :] - p
        la, lb, lc = (np.linalg.norm(x, axis=2) for x in (a, b, c))
        det = np.einsum("ijk,ijk->ij", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("ijk,ijk->ij", a, b) * lc + np.einsum("ijk,ijk->ij", b, c) * la + np.einsum("ijk,ijk->ij", c, a) * lb
        w[s:s + 256] = np.arctan2(det, den).sum(axis=1) / (2.0 * np.pi)
    return np.abs(w)


def exposed_mask(mesh, comps, face_comp, edges_idx, mids, nrm):
    """True where the probe point outside the edge lies in no other component."""
    probe = mids + PROBE * nrm
    keep = np.ones(len(edges_idx), dtype=bool)
    owner = face_comp[mesh.face_adjacency[edges_idx][:, 0]]
    for ci, c in enumerate(comps):
        if len(c.faces) < 4:
            continue
        lo, hi = c.bounds
        cand = np.where((owner != ci) & np.all(probe >= lo - 1e-6, axis=1) & np.all(probe <= hi + 1e-6, axis=1) & keep)[0]
        if len(cand) == 0:
            continue
        inside = winding(c.triangles, probe[cand]) > 0.5
        keep[cand[inside]] = False
    return keep


def audit(path):
    mesh = trimesh.load(path, force="mesh", process=True)
    labels = trimesh.graph.connected_component_labels(mesh.face_adjacency, node_count=len(mesh.faces))
    comps = []
    face_comp = labels
    for li in range(labels.max() + 1):
        idx = np.where(labels == li)[0]
        comps.append(mesh.submesh([idx], append=True))
    ang = np.degrees(mesh.face_adjacency_angles)
    convex = mesh.face_adjacency_convex
    sel = np.where(convex & (ang > SHARP_DEG))[0]
    ev = mesh.vertices[mesh.face_adjacency_edges[sel]]
    mids = ev.mean(axis=1)
    lens = np.linalg.norm(ev[:, 1] - ev[:, 0], axis=1)
    n2 = mesh.face_normals[mesh.face_adjacency[sel]]
    nrm = n2.sum(axis=1)
    nrm /= np.linalg.norm(nrm, axis=1)[:, None] + 1e-12
    keep = exposed_mask(mesh, comps, face_comp, sel, mids, nrm) if len(sel) else np.zeros(0, bool)
    # max turn over all exposed convex edges (tested on the sharpest 4000 to bound the cost)
    allc = np.where(convex & (ang > 1.0))[0]
    order = allc[np.argsort(-ang[allc])][:4000]
    if len(order):
        ev2 = mesh.vertices[mesh.face_adjacency_edges[order]]
        n22 = mesh.face_normals[mesh.face_adjacency[order]].sum(axis=1)
        n22 /= np.linalg.norm(n22, axis=1)[:, None] + 1e-12
        k2 = exposed_mask(mesh, comps, face_comp, order, ev2.mean(axis=1), n22)
        max_turn = float(ang[order][k2].max()) if k2.any() else 0.0
    else:
        max_turn = 0.0
    sharp_mids = mids[keep]
    sharp_ang = ang[sel][keep]
    # group the sharp exposed edges by component for the report
    groups = {}
    owner = face_comp[mesh.face_adjacency[sel][keep][:, 0]] if keep.any() else np.zeros(0, int)
    for ci in np.unique(owner):
        m = owner == ci
        b = comps[ci].bounds
        groups[int(ci)] = {
            "n": int(m.sum()),
            "len_mm": float(lens[keep][m].sum()),
            "max_deg": float(sharp_ang[m].max()),
            "part_bbox": [[round(float(x), 2) for x in b[0]], [round(float(x), 2) for x in b[1]]],
        }
    return {
        "file": os.path.basename(path),
        "bytes": os.path.getsize(path),
        "tris": int(len(mesh.faces)),
        "watertight": bool(mesh.is_watertight),
        "parts": len(comps),
        "bbox": [[round(float(x), 4) for x in mesh.bounds[0]], [round(float(x), 4) for x in mesh.bounds[1]]],
        "sharp": int(keep.sum()),
        "len_sharp_mm": round(float(lens[keep].sum()), 2),
        "max_turn_deg": round(max_turn, 2),
        "groups": groups,
    }


# ── Named radius checks: slice a mesh with a plane and fit a circle to the corner points ──
def fit_circle(pts):
    A = np.c_[2 * pts[:, 0], 2 * pts[:, 1], np.ones(len(pts))]
    b = (pts ** 2).sum(axis=1)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = sol[0], sol[1]
    r = math.sqrt(max(sol[2] + cx * cx + cy * cy, 0.0))
    return r


def section_pts(mesh, origin, normal, axes):
    seg = trimesh.intersections.mesh_plane(mesh, plane_normal=normal, plane_origin=origin)
    if len(seg) == 0:
        return np.zeros((0, 2))
    p = seg.reshape(-1, 3)
    return np.c_[p[:, axes[0]], p[:, axes[1]]]


def corner_radius(pts2, corner, quad, r_nom):
    """Fit a circle to the section points in the corner box of side 0.98 r_nom.
    corner: (a, b) the sharp corner position; quad: (sa, sb) the direction into the material."""
    a0, b0 = corner
    sa, sb = quad
    box = 0.98 * r_nom
    da = (pts2[:, 0] - a0) * sa
    db = (pts2[:, 1] - b0) * sb
    m = (da >= -1e-6) & (da <= box) & (db >= -1e-6) & (db <= box)
    # drop the points that sit on the flat faces
    m &= (da > 0.02 * r_nom) & (db > 0.02 * r_nom)
    q = np.unique(np.round(pts2[m], 6), axis=0)
    if len(q) < 3:
        return None, len(q)
    return fit_circle(q), len(q)


def named_checks(d):
    out = []

    def load(n):
        return trimesh.load(os.path.join(d, n), force="mesh")

    # 1. body perimeter face edges, r 0.65: section at y = 0 through the long side
    for n, w in (("leaf80-body.stl", 40.0), ("leaf160-body.stl", 80.0), ("leaf480-body.stl", 320.0)):
        m = load(n)
        p = section_pts(m, [0, 0, 1.0], [0, 1, 0], (0, 2))
        r_top, k1 = corner_radius(p, (w / 2, 2.0), (-1, -1), 0.65)
        r_bot, k2 = corner_radius(p, (w / 2, 0.0), (-1, +1), 0.65)
        out.append((n, "body side, front face edge", 0.65, r_top, k1))
        out.append((n, "body side, back face edge", 0.65, r_bot, k2))
    # 2. B module (ring centre (16, 16), z 0 .. 2): section at y = 16 through the ring
    for n in ("monogram-module.stl", "monogram-ring.stl", "monogram-letter.stl"):
        m = load(n)
        p = section_pts(m, [16.0, 16.0, 1.0], [0, 1, 0], (0, 2))
        r1, k1 = corner_radius(p, (32.0, 2.0), (-1, -1), 0.40)
        r2, k2 = corner_radius(p, (32.0, 0.0), (-1, +1), 0.40)
        out.append((n, "B ring outer edge, front", 0.40, r1, k1))
        out.append((n, "B ring outer edge, back", 0.40, r2, k2))
        if n == "monogram-ring.stl":
            r3, k3 = corner_radius(p, (28.0, 2.0), (+1, -1), 0.25)
            r4, k4 = corner_radius(p, (28.0, 0.0), (+1, +1), 0.25)
            out.append((n, "B bore edge, front", 0.25, r3, k3))
            out.append((n, "B bore edge, back", 0.25, r4, k4))
            # 3. bar long edges, section at x = 16 (plane normal x), axes (z, y)
            q = section_pts(m, [16.0, 36.5, -0.5], [1, 0, 0], (2, 1))
            r5, k5 = corner_radius(q, (-2.0, 37.0), (+1, -1), 0.20)
            r6, k6 = corner_radius(q, (-2.0, 36.0), (+1, +1), 0.20)
            out.append((n, "B bar long edge, top", 0.20, r5, k5))
            out.append((n, "B bar long edge, bottom", 0.20, r6, k6))
    # 4. rail parts r 0.50 (clamped to 0.45 x the part thickness): x-arm section at x = 30
    m = load("rail-receiver.stl")
    p = section_pts(m, [30.0, 0.0, -5.5], [1, 0, 0], (1, 2))
    if len(p):
        top = p[:, 1].max()
        rr, kk = corner_radius(p, (1.2, top), (-1, -1), 0.40)
        out.append(("rail-receiver.stl", "Ti cruciform arm long edge", 0.40, rr, kk))
    return out


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "models")
    res = []
    only_named = os.environ.get("NAMED_ONLY") == "1"
    for n in sorted(os.listdir(d)):
        if n.endswith(".stl") and not only_named:
            r = audit(os.path.join(d, n))
            res.append(r)
            print("%-26s %9d B %7d tris wt=%-5s parts=%4d sharp=%6d len=%9.1f mm max_turn=%6.2f deg bbox=%s"
                  % (r["file"], r["bytes"], r["tris"], r["watertight"], r["parts"], r["sharp"], r["len_sharp_mm"], r["max_turn_deg"], r["bbox"]))
    chk = named_checks(d)
    print("\nNamed radius checks (section + circle fit):")
    for (n, what, nom, r, k) in chk:
        print("  %-22s %-30s nominal r %.2f  measured %s  (%d pts)" % (n, what, nom, "%.3f" % r if r else "none", k))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            json.dump({"files": res, "named": [list(c) for c in chk]}, f, indent=1)


if __name__ == "__main__":
    main()
