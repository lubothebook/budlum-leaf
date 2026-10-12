#!/usr/bin/env python3
"""verify_body.py - the checks of the L.6.0 rotating-square body.

Run after body_gen.py. Reads the exported STL files and the generator.
Writes verify-results.json and exits 1 when any check fails.

Checks (gate in brackets, FINAL/21 Section 21.8):
  C1  tile count 128, 32 per quadrant                       [MEC-39]
  C2  lattice envelope = (cos t + sin t) x 80 x 160          [MEC-39, DSP-17]
  C3  STL bounding box = mid-plane plan bounding box         [MEC-39]
  C4  no tile overlap, no ribbon or ball clash (shapely)     [MEC-39, MEC-42]
  C5  hinge corner coincidence, 232 hinges, 1 per corner     [MEC-42]
  C6  watertight STL bodies, positive volumes                [MEC-39]
  C7  ribbon chord <= ribbon length at every state           [MEC-42]
  C8  void diagonal 2 a sin t (6.0 mm at 17.5 deg)           [MEC-41]
  C9  edge softening: facet audit and measured radii         [MEC-41]
  C10 cell volume inside the softened tile                   [ENR-22]
  C11 kinematic seat: 3 balls per quadrant, vee axes         [MEC-40]
  I1  tile coverage of the stretched face (information)      [DSP-17]
"""
import json
import math
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import Polygon, Point, box
from shapely.strtree import STRtree

import body_gen as g

HERE = os.path.dirname(os.path.abspath(__file__))
P = g.BodyParams()
RES = {"checks": {}, "states": {}}
FAILS = []


def check(name, ok, **info):
    RES["checks"].setdefault(name, []).append(dict(ok=bool(ok), **info))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: " +
          ", ".join(f"{k}={v}" for k, v in info.items()))
    if not ok:
        FAILS.append(name)


def fit_circle(pts):
    """Least-squares circle (Kasa) through 2D points. Returns (centre, r, rms)."""
    pts = np.asarray(pts, float)
    A = np.c_[2 * pts, np.ones(len(pts))]
    b = (pts ** 2).sum(1)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    c = sol[:2]
    r = math.sqrt(sol[2] + c @ c)
    rms = float(np.sqrt(np.mean((np.linalg.norm(pts - c, axis=1) - r) ** 2)))
    return c, r, rms


def ribbon_polys(body):
    out = []
    for hi, h in enumerate(body.hinges):
        for path in body.ribbon_paths(h):
            Lf, Rt = g.strip_offsets(path, P.rib_thk)
            out.append((hi, Polygon(np.vstack([Lf, Rt[::-1]]))))
    return out


def state_checks(name, th, stl):
    print(f"\n== {name}: theta = {th} deg ==")
    b = g.Body(P, th)
    S = {}
    k = math.cos(math.radians(th)) + math.sin(math.radians(th))
    # C1
    qs = [t["q"] for t in b.tiles]
    counts = {q: qs.count(q) for q in ("Q1", "Q2", "Q3", "Q4")}
    check("C1 tile count", len(b.tiles) == 128 and all(v == 32 for v in counts.values()),
          tiles=len(b.tiles), per_quadrant=counts)
    # C2 lattice envelope from the hinge-pivot lattice (sharp corners)
    allc = np.vstack([b.corners(i) for i in range(len(b.tiles))])
    env = allc.max(0) - allc.min(0)
    exp = np.array([80.0, 160.0]) * k
    check("C2 lattice envelope", np.allclose(env, exp, atol=1e-9),
          stretch_factor=round(k, 5), envelope_mm=[round(float(v), 3) for v in env],
          expected_mm=[round(float(v), 3) for v in exp], area_ratio=round(k * k, 4))
    S.update(stretch=k, envelope=env.tolist())
    # C3 STL bbox vs plan bbox
    mesh = trimesh.load(stl, process=True)
    bb = mesh.bounds[1] - mesh.bounds[0]
    plans = [Polygon(b.tile_poly2d(i)) for i in range(len(b.tiles))]
    ub = np.array([min(p.bounds[0] for p in plans), min(p.bounds[1] for p in plans),
                   max(p.bounds[2] for p in plans), max(p.bounds[3] for p in plans)])
    pb = ub[2:] - ub[:2]
    check("C3 STL bounding box", np.allclose(bb[:2], pb, atol=1e-4) and abs(bb[2] - P.t) < 1e-6,
          stl_mm=[round(float(v), 3) for v in bb], chamfer_loss_mm=[round(float(v), 3) for v in env - bb[:2]])
    S.update(stl_bbox=bb.tolist())
    # C4 overlaps
    tree = STRtree(plans)
    worst = 0.0
    for i, p in enumerate(plans):
        for j in tree.query(p):
            if j > i:
                worst = max(worst, p.intersection(plans[j]).area)
    check("C4 tile overlap", worst < 1e-9, max_overlap_mm2=f"{worst:.2e}")
    rp = ribbon_polys(b)
    clash = 0
    for hi, poly in rp:
        h = b.hinges[hi]
        for j in tree.query(poly):
            if j in (h["a"], h["b"]):
                continue
            if poly.intersection(plans[j]).area > 1e-12:
                clash += 1
    rtree = STRtree([q for _, q in rp])
    rr = 0
    for a_, (hi, poly) in enumerate(rp):
        for c_ in rtree.query(poly):
            if c_ > a_ and rp[c_][0] != hi and poly.intersects(rp[c_][1]):
                rr += 1
    seats = b.seat_hinges()
    bc = 0
    for hi in seats:
        circ = Point(b.hinges[hi]["P"]).buffer(P.ball_d / 2, 64)
        for j in tree.query(circ):
            if circ.intersection(plans[j]).area > 1e-12:
                bc += 1
    zgap = P.rib_z0 - (P.ball_zc + P.ball_d / 2)
    check("C4 ribbon and ball clash", clash == 0 and rr == 0 and bc == 0 and zgap > 0,
          ribbon_vs_foreign_tile=clash, ribbon_vs_ribbon=rr, ball_vs_tile=bc,
          ball_to_ribbon_z_gap_mm=round(zgap, 3))
    # C5 hinges
    gaps = [h["gap"] for h in b.hinges]
    used = {}
    for h in b.hinges:
        for t_, c_ in ((h["a"], h["ca"]), (h["b"], h["cb"])):
            used[(t_, c_)] = used.get((t_, c_), 0) + 1
    nsplit = sum(h["split"] for h in b.hinges)
    check("C5 hinge corner coincidence",
          len(b.hinges) == 232 and max(gaps) < 1e-9 and max(used.values()) == 1,
          hinges=len(b.hinges), max_pivot_gap_mm=f"{max(gaps):.1e}",
          max_uses_per_corner=max(used.values()), split_couplers=nsplit)
    # C6 watertight bodies
    bodies = mesh.split(only_watertight=False, repair=False)
    nexp = 128 + (232 - nsplit) + 2 * nsplit + len(seats)
    wt = all(x.is_watertight for x in bodies)
    vol = min(x.volume for x in bodies)
    check("C6 watertight STL", mesh.is_watertight and wt and vol > 0 and len(bodies) == nexp,
          bodies=len(bodies), expected=nexp, all_watertight=wt,
          min_body_volume_mm3=f"{vol:.2e}", faces=len(mesh.faces),
          size_MB=round(os.path.getsize(stl) / 1e6, 2))
    # C7 ribbon chord
    chords = [b.ribbon_sag(h) for h in b.hinges]
    dmax = max(c[0] for c in chords)
    check("C7 ribbon chord", dmax < P.rib_len, max_chord_mm=round(dmax, 4),
          ribbon_len_mm=P.rib_len, sagitta_mm=round(chords[0][1], 4))
    # C8 void diagonal: void enclosed by tiles (0,0),(1,0),(0,1),(1,1)
    if th > 0:
        quad = {b.index[(0, 0)], b.index[(1, 0)], b.index[(0, 1)], b.index[(1, 1)]}
        piv = np.array([h["P"] for h in b.hinges if h["a"] in quad and h["b"] in quad])
        dd = np.linalg.norm(piv[:, None] - piv[None], axis=2)
        # the rhombus diagonals are the two largest distinct pair distances
        dl = sorted(dd[np.triu_indices(4, 1)])
        diag = [x for x in dl if abs(x - P.a) > 1e-6] or dl[-2:]
        if len(diag) == 0:
            diag = dl[-2:]
        sd, ld = (diag[0], diag[-1]) if len(diag) == 2 else (dl[-2], dl[-1])
        exp_s = 2 * P.a * math.sin(math.radians(th))
        exp_l = 2 * P.a * math.cos(math.radians(th))
        check("C8 void diagonal", abs(sd - min(exp_s, exp_l)) < 1e-6 and abs(ld - max(exp_s, exp_l)) < 1e-6,
              short_mm=round(sd, 3), long_mm=round(ld, 3),
              expected=[round(min(exp_s, exp_l), 3), round(max(exp_s, exp_l), 3)])
    # I1 coverage
    cov = sum(p.area for p in plans) / (env[0] * env[1])
    cov_sharp = 128 * P.a ** 2 / (env[0] * env[1])
    print(f"  [INFO] I1 coverage: tiles {cov*100:.1f} % (unchamfered {cov_sharp*100:.1f} %)")
    S.update(coverage=cov, coverage_unchamfered=cov_sharp)
    # C11 seat
    if th == 0:
        quad_balls = {q: [] for q in ("Q1", "Q2", "Q3", "Q4")}
        for hi in seats:
            h = b.hinges[hi]
            for t_ in (h["a"], h["b"]):
                quad_balls[b.tiles[t_]["q"]].append(h["P"])
        vee = {}
        ok = True
        for q, pts in quad_balls.items():
            pts = np.array(pts)
            cen = pts.mean(0)
            ang = [math.degrees(math.atan2(*(pp - cen)[::-1])) for pp in pts]
            spread = sorted(((ang[i] - ang[j]) % 360) for i in range(3) for j in range(3) if i != j)
            u_, w_ = pts[1] - pts[0], pts[2] - pts[0]
            area = 0.5 * abs(u_[0] * w_[1] - u_[1] * w_[0])
            ok &= len(pts) == 3 and area > 50
            vee[q] = dict(balls=[[round(v, 2) for v in pp] for pp in pts],
                          vee_axis_deg=[round(a, 1) for a in ang], triangle_mm2=round(area, 1))
        check("C11 kinematic seat", ok and len(seats) == 6, balls=len(seats),
              per_quadrant={q: len(v) for q, v in quad_balls.items()})
        RES["seat"] = vee
    RES["states"][name] = S
    return b, mesh


def edge_checks(b_rest, mesh_rest):
    print("\n== C9 edge softening ==")
    # facet audit: no crease sharper than one fillet facet step
    worst, nbad = 0.0, 0
    lim = 47.0
    for k in range(len(b_rest.tiles)):
        m = g.tile_mesh(b_rest, k)
        a = np.degrees(m.face_adjacency_angles)
        worst = max(worst, a.max())
        nbad += int((a > lim).sum())
    check("C9 facet audit", nbad == 0, max_facet_turn_deg=round(worst, 2),
          limit_deg=lim, creases_over_limit=nbad,
          note="a 90 deg edge split into 2 or more facets turns 45 deg or less")
    # independent fits on the vertices of the exported rest STL.
    # A plane section would cut the triangle diagonals and read chords, so the
    # fits use the true vertices, projected on the face normal.
    sec = {}
    V = mesh_rest.vertices
    hk = P.kerf / 2
    xmin, ymin = -P.nx * P.a / 2, -P.ny * P.a / 2
    yc = (5 - (P.ny - 1) / 2) * P.a            # tile (0,5), mid left side
    xo = xmin + hk                              # its outer face
    sel = V[(np.abs(V[:, 1] - yc) < 2.5) & (V[:, 0] < xo + P.r_perim + 1e-6)]
    top = sel[sel[:, 2] >= P.t - P.r_perim - 1e-6]
    bot = sel[sel[:, 2] <= P.r_perim + 1e-6]
    _, sec["perimeter_front"], _ = fit_circle(top[:, [0, 2]])
    _, sec["perimeter_back"], _ = fit_circle(bot[:, [0, 2]])
    xs = xmin + 2 * P.a - hk                    # right face of tile (1,5)
    lim = (P.a - P.kerf) / 2 - P.chamfer - P.r_break * math.tan(math.pi / 8) + 1e-6
    sel = V[(np.abs(V[:, 1] - yc) < lim) & (V[:, 0] <= xs + 1e-5) & (V[:, 0] > xs - P.r_break - 1e-5)]
    top = sel[sel[:, 2] >= P.t - P.r_break - 1e-5]
    bot = sel[sel[:, 2] <= P.r_break + 1e-5]
    _, sec["cap_top_break"], _ = fit_circle(top[:, [0, 2]])
    _, sec["back_break"], _ = fit_circle(bot[:, [0, 2]])
    # plan rounds: vertices on the flat wall at z = t - r_perim (zero inset)
    zw = P.t - P.r_perim
    W = V[np.abs(V[:, 2] - zw) < 1e-5][:, :2]
    sel = W[(W[:, 0] < xmin + hk + P.R_corner - 1e-6) & (W[:, 1] < ymin + hk + P.R_corner - 1e-6)]
    _, sec["plan_corner_R"], _ = fit_circle(sel)
    W2 = V[np.abs(V[:, 2] - (P.t - P.r_break)) < 1e-5][:, :2]
    vx = np.array([xmin + P.a - hk, ymin + P.a - hk - P.chamfer])   # tile (0,0) corner (h,h)
    near = W2[(np.linalg.norm(W2 - vx, axis=1) < 0.03) & (W2[:, 0] <= vx[0] + 1e-5)]
    _, sec["chamfer_corner_round"], _ = fit_circle(near)
    sec = {k_: round(v_, 4) for k_, v_ in sec.items()}
    spec = {"perimeter_front": P.r_perim, "perimeter_back": P.r_perim,
            "cap_top_break": P.r_break, "back_break": P.r_break,
            "plan_corner_R": P.R_corner, "chamfer_corner_round": P.r_break}
    # each radius equals its order within 1 %: not sharper, and not a whole face
    ok = all(abs(sec[k_] - spec[k_]) <= 0.01 * spec[k_] for k_ in spec)
    check("C9 measured radii (STL vertices)", ok, **sec)
    RES["edge_radii_measured"] = sec
    # run-out: the minimum radius on any perimeter face vertex
    v, r = b_rest.plan_local(b_rest.index[(0, 5)])
    check("C9 run-out", r.min() >= P.r_break - 1e-12 and r.max() <= P.r_perim + 1e-12,
          perimeter_tile_radius_range_mm=[round(float(r.min()), 3), round(float(r.max()), 3)],
          run_out_mm=P.run_out)
    # kerf and edge pixel: the mid-plane footprint is the sharp 10 mm tile
    mid = np.array(g.loop_at(v, r, P, 1.0))
    ext = mid.max(0) - mid.min(0)
    glass_z = (P.t - 0.25 - 0.05 - 0.25, P.t - 0.30)
    dz = max(g.fillet_inset(P.r_break, z, P.t) for z in np.linspace(*glass_z, 11))
    check("C9 kerf and edge pixel untouched", abs(ext[0] - (P.a - P.kerf)) < 1e-9 and dz == 0.0,
          footprint_at_midplane_mm=[round(float(e), 4) for e in ext],
          break_inset_at_glass_layer_mm=dz,
          glass_layer_z_mm=[round(z, 2) for z in glass_z])


def cell_check(b):
    print("\n== C10 cell envelope ==")
    cz = (0.32, 1.22)
    hc = 9.25 / 2
    cell = box(-hc, -hc, hc, hc)
    bad = []
    for k in range(len(b.tiles)):
        v, r = b.plan_local(k)
        worst = 0.0
        for z in cz:
            lp = Polygon(g.loop_at(v, r, P, z))
            worst = max(worst, cell.difference(lp).area)
        if worst > 1e-9:
            t = b.tiles[k]
            bad.append(dict(tile=[t["i"], t["j"]], cell_outside_mm2=round(worst, 3)))
    loss = sum(x["cell_outside_mm2"] for x in bad)
    frac = loss / (128 * 9.25 ** 2)
    ok = all(x["tile"] in ([0, 0], [P.nx - 1, 0], [0, P.ny - 1], [P.nx - 1, P.ny - 1]) for x in bad)
    check("C10 cell inside tile", ok, tiles_with_cell_outside=len(bad),
          corner_cell_notch_mm2=bad[0]["cell_outside_mm2"] if bad else 0,
          body_cell_area_loss_pct=round(100 * frac, 3),
          note="only the four R 6.35 corner tiles clip the cell")
    RES["cell_notch"] = dict(tiles=bad, loss_fraction=frac)


def main():
    files = {"rest": "body-rest.stl", "default": "body-default.stl", "max": "body-max.stl"}
    keep = {}
    for name, th in g.STATES:
        keep[name] = state_checks(name, th, os.path.join(HERE, files[name]))
    edge_checks(*keep["rest"])
    cell_check(keep["rest"][0])
    tot = sum(os.path.getsize(os.path.join(HERE, f)) for f in files.values())
    check("STL total size", tot < 15e6, total_MB=round(tot / 1e6, 2))
    RES["fails"] = FAILS
    with open(os.path.join(HERE, "verify-results.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print(f"\n{'ALL PASS' if not FAILS else 'FAILED: ' + ', '.join(sorted(set(FAILS)))}")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
