#!/usr/bin/env python3
"""jack_sideload.py - side load on the 0.20 mm jack walls under plug leverage.

Three steps:
  1. Lever model. The plug is a rigid pin. A side force F acts at `arm` past the
     shoulder. The bore reacts at the blind end (a triangular line load over
     the closed bore) and at the mouth support. This gives the peak line load q
     (N/mm) on the wall at the blind end.
  2. Hand beam. The 0.20 mm crown as a fixed-fixed strip, uniform and with the
     true variable thickness of a bore in a 4.00 mm plate. These bound the stress.
  3. Plane-strain FE of the ring cross-section at the closed end (x = 0) and in
     the captured trough (x = 6.0). Linear triangles, scipy sparse solve. It
     gives the stress per 1 N/mm of wall load, for LCP alone and for a sleeve
     of PEEK, PEEK-GF30 or Y-TZP in the 0.20 mm wall band.

Run:  python3 jack_sideload.py         (about 20 s)  -> out/sideload.json
"""
import json
import math
import os
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.spatial import Delaunay

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

D_CH, RB, T_W, T = P.CHORD_D, P.BORE_D / 2, P.WALL_T, P.RING_T
CLOSED_BORE = 4.84          # from jack_geometry.py
S_SHOULDER = P.PLUG_L       # tip datum
# mouth support centroid s (mm from blind end) and how it is built, per direction
MOUTH = {
    "+y outboard": dict(s=9.6, how="C-clip sleeve contact and LCP lips, x 3.6..9.9"),
    "-y inboard": dict(s=11.5, how="solid saddle and cradle floor with the rim boss"),
    "+z face": dict(s=10.5, how="cradle side walls and the C-clip"),
}
# where the deep reaction lands, as the direction the plug pushes the wall
DEEP_DIR = {"+y outboard": "-y", "-y inboard": "+y", "+z face": "-z"}


# ----------------------------------------------------------------- 1 lever
# V0: the groove as drawn, LCP walls, mouth support inside the plain trough.
# V1: the team design. A C-clip sleeve contact in the captured zone and a
#     closed collar in the rim boss move the mouth support out, and a stiff
#     cup spreads the blind-end load (trapezoid in place of a triangle).
VARIANTS = {
    "V0": {"+y outboard": 9.6, "-y inboard": 11.5, "+z face": 10.5},
    "V1": {"+y outboard": 11.25, "-y inboard": 13.0, "+z face": 12.5},
}
STIFF = {"Y-TZP"}          # a sleeve stiff enough to spread the load


def lever(F, arm, s_m, stiff=False):
    s_load = S_SHOULDER + arm
    if stiff:                                    # trapezoid 1.3 : 0.7
        k_peak, s_d = 1.3, 0.433 * CLOSED_BORE
    else:                                        # triangle
        k_peak, s_d = 2.0, CLOSED_BORE / 3.0
    R_deep = F * (s_load - s_m) / (s_m - s_d)
    R_mouth = F + R_deep
    q_peak = k_peak * R_deep / CLOSED_BORE       # N/mm
    return R_deep, R_mouth, q_peak


# ----------------------------------------------------------------- 2 hand beam
def beam_uniform(q, t=T_W, span=P.BORE_D):
    """Fixed-fixed strip, unit width, central load q (N per mm of bore)."""
    M = q * span / 8.0
    return 6 * M / t**2


def beam_variable(q, n=4001):
    """Fixed-fixed strip with h(u) = T/2 - sqrt(RB^2 - u^2), central load.

    Solves the redundant end moment by the unit-load method: the slope at
    the centre is zero by symmetry (half beam, fixed at u = RB).
    """
    u = np.linspace(0, RB, n)
    h = T / 2 - np.sqrt(np.maximum(RB**2 - u**2, 0))
    EI = h**3 / 12.0                              # E cancels
    # half beam, cantilever from the wall (u=RB) to the centre (u=0),
    # central half-load q/2 at u=0 and unknown moment M0 at u=0.
    # M(u) = M0 - (q/2) * u ; slope at centre = int M/EI du = 0
    a = np.trapezoid(1 / EI, u)
    b = np.trapezoid(u / EI, u)
    M0 = (q / 2) * b / a
    M = M0 - (q / 2) * u
    sig = 6 * np.abs(M) / h**2
    return float(sig.max()), float(u[sig.argmax()])


# ----------------------------------------------------------------- 3 FE
def mesh(x_station, y_in=10.8, h=0.025):
    y_max = min(math.sqrt(P.RING_RO**2 - x_station**2), D_CH + RB + T_W + 1.0)
    ys = np.arange(y_in, y_max + 1e-9, h)
    zs = np.arange(-T / 2, T / 2 + 1e-9, h)
    Y, Z = np.meshgrid(ys, zs)
    pts = np.c_[Y.ravel(), Z.ravel()]
    keep = pts[:, 0] <= y_max - 0.5 * h
    pts = pts[keep]
    # circle points: the bore and the sleeve interface
    circ = []
    for r in (RB, RB + T_W):
        n = int(math.ceil(2 * math.pi * r / (0.7 * h)))
        th = np.linspace(0, 2 * math.pi, n, endpoint=False)
        c = np.c_[D_CH + r * np.cos(th), r * np.sin(th)]
        c = c[(c[:, 0] <= y_max) & (np.abs(c[:, 1]) <= T / 2)]
        circ.append(c)
    rr = np.hypot(pts[:, 0] - D_CH, pts[:, 1])
    far = (np.abs(rr - RB) > 0.45 * h) & (np.abs(rr - RB - T_W) > 0.45 * h) & (rr > RB)
    pts = pts[far]
    # rim edge points
    ze = zs.copy()
    edge = np.c_[np.full_like(ze, y_max), ze]
    re = np.hypot(edge[:, 0] - D_CH, edge[:, 1])
    edge = edge[re > RB + 0.3 * h]
    pts = np.vstack([pts, circ[0], circ[1], edge])
    pts = np.unique(np.round(pts, 6), axis=0)
    tri = Delaunay(pts).simplices
    cen = pts[tri].mean(axis=1)
    rc = np.hypot(cen[:, 0] - D_CH, cen[:, 1])
    e1 = pts[tri[:, 1]] - pts[tri[:, 0]]
    e2 = pts[tri[:, 2]] - pts[tri[:, 0]]
    a = 0.5 * np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0])
    ok = (rc > RB) & (cen[:, 0] < y_max) & (a > 1e-10)
    return pts, tri[ok], y_in, y_max


def solve(x_station, load_dir, sleeve=None, theta_c=45.0, h=0.025):
    pts, tri, y_in, y_max = mesh(x_station, h=h)
    n = len(pts)
    cen = pts[tri].mean(axis=1)
    rc = np.hypot(cen[:, 0] - D_CH, cen[:, 1])
    # the sleeve is D-flat: it fills the knife-edge wedges at the faces up to
    # a 0.15 mm land, so no LCP sliver sits over the crown.
    in_sleeve = (rc < RB + T_W) | ((np.abs(cen[:, 1]) > T / 2 - 0.15) &
                                   (np.abs(cen[:, 0] - D_CH) < 1.0))
    E = np.where(in_sleeve & (sleeve is not None),
                 P.MATERIALS[sleeve]["E"] if sleeve else 0,
                 P.MATERIALS["LCP-GF40"]["E"])
    nu = np.where(in_sleeve & (sleeve is not None),
                  P.MATERIALS[sleeve]["nu"] if sleeve else 0,
                  P.MATERIALS["LCP-GF40"]["nu"])
    # CST plane strain
    p0, p1, p2 = pts[tri[:, 0]], pts[tri[:, 1]], pts[tri[:, 2]]
    b = np.c_[p1[:, 1] - p2[:, 1], p2[:, 1] - p0[:, 1], p0[:, 1] - p1[:, 1]]
    c = np.c_[p2[:, 0] - p1[:, 0], p0[:, 0] - p2[:, 0], p1[:, 0] - p0[:, 0]]
    A = 0.5 * (b[:, 0] * c[:, 1] - b[:, 1] * c[:, 0])
    sgn = np.sign(A)
    A = np.abs(A)
    b *= sgn[:, None]
    c *= sgn[:, None]
    B = np.zeros((len(tri), 3, 6))
    B[:, 0, 0::2] = b
    B[:, 1, 1::2] = c
    B[:, 2, 0::2] = c
    B[:, 2, 1::2] = b
    B /= (2 * A)[:, None, None]
    f = E / ((1 + nu) * (1 - 2 * nu))
    Dm = np.zeros((len(tri), 3, 3))
    Dm[:, 0, 0] = Dm[:, 1, 1] = f * (1 - nu)
    Dm[:, 0, 1] = Dm[:, 1, 0] = f * nu
    Dm[:, 2, 2] = f * (1 - 2 * nu) / 2
    Ke = np.einsum("eki,ekl,elj->eij", B, Dm, B) * A[:, None, None]
    dof = np.c_[2 * tri[:, 0], 2 * tri[:, 0] + 1, 2 * tri[:, 1], 2 * tri[:, 1] + 1,
                2 * tri[:, 2], 2 * tri[:, 2] + 1]
    I = np.repeat(dof, 6, axis=1).ravel()
    J = np.tile(dof, 6).ravel()
    K = coo_matrix((Ke.ravel(), (I, J)), shape=(2 * n, 2 * n)).tocsr()
    # load on the bore edges
    dvec = {"+y": (1, 0), "-y": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[load_dir]
    rn = np.hypot(pts[:, 0] - D_CH, pts[:, 1])
    on_bore = np.abs(rn - RB) < 1e-4
    edges = set()
    for e in tri:
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if on_bore[e[i]] and on_bore[e[j]]:
                edges.add((min(e[i], e[j]), max(e[i], e[j])))
    Fv = np.zeros(2 * n)
    tot = 0.0
    loads = []
    for i, j in edges:
        m = 0.5 * (pts[i] + pts[j])
        nv = (m - [D_CH, 0]) / np.linalg.norm(m - [D_CH, 0])
        rel = math.degrees(math.acos(np.clip(nv @ dvec, -1, 1)))
        if rel >= theta_c:
            continue
        L = np.linalg.norm(pts[i] - pts[j])
        p = math.cos(math.pi / 2 * rel / theta_c)
        loads.append((i, j, nv, p * L))
        tot += p * L * (nv @ dvec)
    for i, j, nv, w in loads:
        fe = nv * w / tot / 2
        Fv[2 * i:2 * i + 2] += fe
        Fv[2 * j:2 * j + 2] += fe
    # fix the saddle root, y = y_in
    fixed = np.where(np.abs(pts[:, 0] - y_in) < 1e-6)[0]
    fd = np.r_[2 * fixed, 2 * fixed + 1]
    free = np.setdiff1d(np.arange(2 * n), fd)
    u = np.zeros(2 * n)
    u[free] = spsolve(K[free][:, free].tocsc(), Fv[free])
    ue = u[dof]
    eps = np.einsum("eij,ej->ei", B, ue)
    sig = np.einsum("eij,ej->ei", Dm, eps)
    sx, sy, txy = sig[:, 0], sig[:, 1], sig[:, 2]
    s1 = (sx + sy) / 2 + np.sqrt(((sx - sy) / 2) ** 2 + txy**2)
    # leave out the elements on the fixed root (BC singularity)
    away = cen[:, 0] > y_in + 0.15
    out = {}
    for name, mask in (("wall", in_sleeve & away), ("body", ~in_sleeve & away)):
        if mask.any():
            k = np.argmax(np.where(mask, s1, -1e9))
            out[name] = dict(s1_per_Npmm=float(s1[k]),
                             at=[round(float(cen[k, 0]), 3), round(float(cen[k, 1]), 3)])
    out["max_disp_um_per_Npmm"] = float(np.abs(u).max() * 1000)
    out["nodes"] = int(n)
    return out


def main():
    res = {"lever": {}, "beam": {}, "fe": {}, "verdict": []}
    print("SIDE LOAD ON THE JACK WALLS (MON-22)")
    print(" 1 lever model, plug as a rigid pin, tip datum, shoulder s = 14.0")
    for vname, ms in VARIANTS.items():
        for case, L in P.SIDE_LOADS.items():
            for dname, s_m in ms.items():
                for stiff in (False, True):
                    Rd, Rm, q = lever(L["F"], L["arm"], s_m, stiff)
                    res["lever"][f"{vname} {case} {dname} {'stiff' if stiff else 'soft'}"] = dict(
                        s_mouth=s_m, R_deep=Rd, R_mouth=Rm, q_peak=q, deep_wall=DEEP_DIR[dname])
                    if case == "service":
                        print(f"   {vname} {case:7s} {dname:12s} {'stiff' if stiff else 'soft '} s_m {s_m:5.2f}"
                              f"  R_deep {Rd:5.1f} N  R_mouth {Rm:5.1f} N  q_peak {q:5.2f} N/mm")
    M = P.SIDE_LOADS["service"]["F"] * P.SIDE_LOADS["service"]["arm"]
    sp = 32 * M / (math.pi * P.PLUG_D**3)
    print(f"   plug shank bending at the shoulder {sp:.0f} MPa (brass yields near 300)")
    res["plug_bending_MPa"] = sp

    print(" 2 hand beam on the 0.20 mm crown, per 1 N/mm")
    bu = beam_uniform(1.0)
    bv, ub = beam_variable(1.0)
    res["beam"] = dict(uniform=bu, variable=bv, variable_at_u=ub)
    print(f"   uniform 0.20 strip over 3.6 mm: {bu:.0f} MPa per N/mm")
    print(f"   true thickness h(u):            {bv:.0f} MPa per N/mm at u = {ub:.2f}")

    print(" 3 plane-strain FE, max principal stress per 1 N/mm of wall load")
    stations = [(0.0, "+y", 45), (0.0, "-y", 45), (0.0, "+z", 45), (6.0, "+y", 85), (6.0, "+z", 45)]
    for xs, ld, tc in stations:
        for sl in (None, "PEEK", "PEEK-GF30", "Y-TZP"):
            r = solve(xs, ld, sleeve=sl, theta_c=tc)
            key = f"x={xs} {ld} {sl or 'LCP only'}"
            res["fe"][key] = r
            w = r.get("wall", {}); bd = r.get("body", {})
            print(f"   {key:26s} band {w.get('s1_per_Npmm', 0):5.1f} at {w.get('at')}  "
                  f"LCP {bd.get('s1_per_Npmm', 0):5.1f} at {bd.get('at')}  disp {r['max_disp_um_per_Npmm']:.2f} um")

    print(" 4 verdict at the blind end (x = 0). Allowables: service = design, abuse = 0.9 nominal")
    print("   (LCP abuse = 0.45 nominal: weld line). ±z is the free module, not backed by the face.")
    for vname, ms in VARIANTS.items():
        for case in P.SIDE_LOADS:
            for dname in ms:
                ld = DEEP_DIR[dname].replace("-z", "+z")   # symmetric section
                for sl in (None, "PEEK", "PEEK-GF30", "Y-TZP"):
                    lv = res["lever"][f"{vname} {case} {dname} {'stiff' if sl in STIFF else 'soft'}"]
                    fe = res["fe"][f"x=0.0 {ld} {sl or 'LCP only'}"]
                    mat = sl or "LCP-GF40"
                    if sl is None:   # one material: the band split is bookkeeping
                        k = max(fe["wall"]["s1_per_Npmm"], fe["body"]["s1_per_Npmm"])
                        s_wall = s_body = k * lv["q_peak"]
                    else:
                        s_wall = fe["wall"]["s1_per_Npmm"] * lv["q_peak"]
                        s_body = fe["body"]["s1_per_Npmm"] * lv["q_peak"]
                    if case == "service":
                        aw, ab = P.MATERIALS[mat]["S_allow"], P.MATERIALS["LCP-GF40"]["S_allow"]
                    else:
                        aw = P.MATERIALS[mat]["S_nom"] * (0.45 if mat == "LCP-GF40" else 0.9)
                        ab = P.MATERIALS["LCP-GF40"]["S_nom"] * 0.45
                    ok = s_wall <= aw and s_body <= ab
                    res["verdict"].append(dict(variant=vname, case=case, dir=dname, wall=mat,
                                               q_peak=lv["q_peak"], s_wall=s_wall, allow_wall=aw,
                                               s_lcp=s_body, allow_lcp=ab, ok=bool(ok)))
                    print(f"   {vname} {case:7s} {dname:12s} {mat:9s} q {lv['q_peak']:5.2f}  "
                          f"band {s_wall:5.0f}/{aw:4.0f}  LCP {s_body:5.0f}/{ab:4.0f}  "
                          f"{'PASS' if ok else 'FAIL'}")
    print(" 6 capacity: largest F at 15 mm past the shoulder, V1 supports")
    print("   blind end at x = 0 and the captured trough at x = 6 (lips). Metals use the")
    print("   stiff-band FE factors of Y-TZP (E within a factor of two).")
    L_cap = {"+y outboard": 6.35, "-y inboard": None, "+z face": 7.1}
    cap = {}
    for mat in ("LCP-GF40", "PEEK", "PEEK-GF30", "Y-TZP", "Ti-6Al-4V", "17-4PH H900", "Zr-BMG"):
        sl = None if mat == "LCP-GF40" else (mat if mat in ("PEEK", "PEEK-GF30", "Y-TZP") else "Y-TZP")
        stiff = mat not in ("LCP-GF40", "PEEK", "PEEK-GF30")
        row = {}
        for dname, s_m in VARIANTS["V1"].items():
            _, Rm1, q1 = lever(1.0, P.SIDE_LOADS["service"]["arm"], s_m, stiff)
            ld0 = DEEP_DIR[dname].replace("-z", "+z")
            fe0 = res["fe"][f"x=0.0 {ld0} {sl or 'LCP only'}"]
            k0 = max(fe0["wall"]["s1_per_Npmm"], fe0["body"]["s1_per_Npmm"]) if sl is None \
                else fe0["wall"]["s1_per_Npmm"]
            S = P.MATERIALS[mat]["S_allow"]
            f_end = S / (k0 * q1) if k0 * q1 > 0 else float("inf")
            if L_cap[dname]:
                ld6 = dname.split()[0]
                fe6 = res["fe"][f"x=6.0 {ld6} {sl or 'LCP only'}"]
                k6 = fe6["wall"]["s1_per_Npmm"]
                q6 = 2 * Rm1 / L_cap[dname]
                f_mouth = S / (k6 * q6)
            else:
                f_mouth = float("inf")
            row[dname] = dict(F_blind_end=round(f_end, 2), F_trough=round(min(f_mouth, 999), 2),
                              F_max=round(min(f_end, f_mouth), 2))
        cap[mat] = row
        print(f"   {mat:12s} " + "  ".join(f"{d.split()[0]} {v['F_max']:5.2f} N" for d, v in row.items()))
    res["capacity_N_at_15mm"] = cap
    # ------------------------------------------------------------- 7
    print(" 7 rigid pin on an elastic bed (linear pressure), the best spread")
    print("   the wall can give. Baseline chord 13.8 against change request CR-AUD-1,")
    print("   chord 13.2: the closed tube grows from 4.84 to 9.78 mm.")
    k_stiff = {"+y": res["fe"]["x=0.0 +y Y-TZP"]["wall"]["s1_per_Npmm"],
               "z": max(res["fe"]["x=0.0 +z Y-TZP"]["wall"]["s1_per_Npmm"],
                        res["fe"]["x=6.0 +z Y-TZP"]["wall"]["s1_per_Npmm"])}
    k_lcp = {"+y": max(res["fe"]["x=0.0 +y LCP only"]["wall"]["s1_per_Npmm"],
                       res["fe"]["x=0.0 +y LCP only"]["body"]["s1_per_Npmm"]),
             "z": max(res["fe"]["x=0.0 +z LCP only"]["wall"]["s1_per_Npmm"],
                      res["fe"]["x=6.0 +z LCP only"]["wall"]["s1_per_Npmm"])}
    k_soft = {m: {"+y": res["fe"][f"x=0.0 +y {m}"]["wall"]["s1_per_Npmm"],
                  "z": max(res["fe"][f"x=0.0 +z {m}"]["wall"]["s1_per_Npmm"],
                           res["fe"][f"x=6.0 +z {m}"]["wall"]["s1_per_Npmm"])}
              for m in ("PEEK", "PEEK-GF30")}

    def q_bed(F, L, s_load):
        a11, a12, a22 = L, L**2 / 2, L**3 / 3
        det = a11 * a22 - a12 * a12
        A = (F * a22 - F * s_load * a12) / det
        B = (a11 * F * s_load - a12 * F) / det
        return max(abs(A), abs(A + B * L))

    s_load = P.PLUG_L + P.SIDE_LOADS["service"]["arm"]
    layouts = {"13.8 (as decided)": {"+y": 4.84, "z": 14.0},
               "13.2 (CR-AUD-1)": {"+y": 9.78, "z": 14.0}}
    bed = {}
    for lay, Ls in layouts.items():
        bed[lay] = {}
        for mat in ("LCP-GF40", "PEEK", "PEEK-GF30", "Y-TZP", "Ti-6Al-4V", "17-4PH H900", "Zr-BMG"):
            if mat == "LCP-GF40":
                kk = k_lcp
            elif mat in k_soft:
                kk = k_soft[mat]
            else:
                kk = k_stiff
            row = {}
            for dd in ("+y", "z"):
                q1 = q_bed(1.0, Ls[dd], s_load)
                row[dd] = round(P.MATERIALS[mat]["S_allow"] / (kk[dd] * q1), 2)
            row["min"] = min(row["+y"], row["z"])
            bed[lay][mat] = row
            print(f"   chord {lay:18s} {mat:12s} +y {row['+y']:5.2f} N   z {row['z']:5.2f} N")
    res["elastic_bed_capacity_N"] = bed
    F_req = P.SIDE_LOADS["service"]["F"]
    passing = {lay: [m for m, r in v.items() if r["min"] >= F_req] for lay, v in bed.items()}
    res["passing_10N"] = passing
    print(" RESULT")
    for lay, ms in passing.items():
        print(f"   chord {lay}: materials that hold {F_req:.0f} N at 15 mm in every direction: "
              f"{ms if ms else 'none'}")
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "sideload.json"), "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
