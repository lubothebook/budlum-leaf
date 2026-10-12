#!/usr/bin/env python3
"""lens_design.py: the five-element column lens of the Budlum Leaf B module.

Targets (FINAL/21 section 21.3.5, gate CAM-21):
  f = 3.30 mm, f/2.0, about 88 deg diagonal view, TTL 3.30 mm (L1 front vertex
  to the image at infinity focus), L1 = sapphire window insert, 50 MP sensor
  with 0.61-0.64 um pixels (half diagonal 3.27 mm for the 0.64 um class).

Run:  python3 lens_design.py [--quick]
Writes ../out/lens_start.json, ../out/lens_final.json, ../out/optimize_log.json
The optimiser is scipy.optimize.least_squares (trust region reflective) in
three stages, then perturbed restarts. The merit is the polychromatic RMS
spot about the polychromatic centroid at seven fields, plus hinge penalties
for EFL, thicknesses, edges, gaps, back focus, chief ray angle, distortion,
surface slope and clear aperture.
"""
import json
import os
import sys
import time
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raytrace import (Lens, trace, paraxial, rays_for_field, rays_batch, hexapolar,
                      WAVES, WEIGHTS, WL_D, n_of)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

EFL = 3.30
FNUM = 2.0
TTL = 3.30
IMGH = 3.27            # half diagonal, 8160 x 6144 at 0.64 um
THMAX = np.degrees(np.arctan(IMGH / EFL))
NA = 7                 # asphere terms A4..A16
FIELDS = np.array([0.0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0])
FWEIGHT = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.6])
MATS = ["SAPPHIRE", "AIR", "EP-9000", "AIR", "APEL5514ML", "AIR",
        "APEL5514ML", "AIR", "APEL5514ML", "AIR"]
NAMES = ["L1 front (window face)", "L1 rear (stop)", "L2 front", "L2 rear",
         "L3 front", "L3 rear", "L4 front", "L4 rear", "L5 front", "L5 rear"]
STOP = 1
RN = np.array([0.85, 0.85, 0.90, 1.00, 1.15, 1.35, 1.65, 2.00, 2.40, 2.80])

# limits
T_MIN_PLASTIC = 0.20
EDGE_MIN = 0.10
GAP_MIN = 0.025
BFL_MIN = 0.22
BFL_EDGE_MIN = 0.10
CRA_MAX = 37.0
DIST_MAX = 0.015
SLOPE_MAX = 52.0
CA_MAX = 2.95
FIELD_FRAC_TAN = True


def start_lens():
    c = np.array([0.0, -1 / 2.6, 1 / 4.0, 1 / 2.6, 1 / 12.0, -1 / 25.0,
                  -1 / 4.0, -1 / 1.6, 1 / 4.0, 1 / 1.8])
    c[1:] *= 0.85
    k = np.array([0, 0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -3.0, -4.0])
    a = np.zeros((10, NA))
    t = np.array([0.35, 0.04, 0.22, 0.30, 0.33, 0.30, 0.50, 0.30, 0.36, 0.0])
    t[-1] = TTL - t[:-1].sum()
    return Lens(c, k, a, RN, t, MATS, STOP, EFL / FNUM, NAMES)


# ---------------------------------------------------------------- packing
ASPH_SURF = [2, 3, 4, 5, 6, 7, 8, 9]   # polymer surfaces
SPH_SURF = [1]                         # sapphire rear; front is flat
THK = list(range(9))                   # t[0..8], t[9] = TTL - sum


def pack(L, n_asph):
    x = [L.c[i] for i in SPH_SURF]
    x += [L.c[i] for i in ASPH_SURF]
    x += [L.k[i] for i in ASPH_SURF]
    for i in ASPH_SURF:
        x += list(L.a[i, :n_asph])
    x += [L.t[i] for i in THK]
    return np.array(x)


def unpack(x, L0, n_asph):
    L = L0.copy()
    p = 0
    for i in SPH_SURF:
        L.c[i] = x[p]; p += 1
    for i in ASPH_SURF:
        L.c[i] = x[p]; p += 1
    for i in ASPH_SURF:
        L.k[i] = x[p]; p += 1
    for i in ASPH_SURF:
        L.a[i, :n_asph] = x[p:p + n_asph]; p += n_asph
    for i in THK:
        L.t[i] = x[p]; p += 1
    L.t[9] = TTL - L.t[:9].sum()
    return L


def bounds(n_asph):
    lo, hi = [], []
    for _ in SPH_SURF:
        lo.append(-1.5); hi.append(0.3)
    for _ in ASPH_SURF:
        lo.append(-2.5); hi.append(2.5)
    for _ in ASPH_SURF:
        lo.append(-80.0); hi.append(-1.0)  # k <= -1 keeps every sag real
    for _ in ASPH_SURF:
        lo += [-1.0] * n_asph; hi += [1.0] * n_asph
    tl = [0.30, 0.02, 0.20, 0.02, 0.20, 0.02, 0.20, 0.02, 0.20]
    th = [0.50, 0.60, 0.50, 0.80, 0.70, 0.80, 0.80, 0.80, 0.70]
    lo += tl; hi += th
    return np.array(lo), np.array(hi)


# ---------------------------------------------------------------- merit
PUPIL = hexapolar(3)


FIELD_SCALE = [1.0]
FOCUS_W = [0.0]   # paraxial focus residual weight, used in the first stages


def field_angles():
    if FIELD_FRAC_TAN:
        return np.degrees(np.arctan(FIELD_SCALE[0] * FIELDS * np.tan(np.radians(THMAX))))
    return FIELDS * THMAX


def evaluate(L, full=False):
    """Return residual vector (micrometre-like units) and a report dict."""
    res = []
    rep = dict(spots=[], cra=[], dist=[], fail=0)
    angs = field_angles()
    P, D, wl, Fi, Wi, Pi = rays_batch(L, angs, PUPIL, WAVES)
    o = trace(L, P, D, wl, keep=True)
    V = o["valid"] & np.all(np.isfinite(o["P"]), 1)
    rep["fail"] = int((~V).sum())
    hits_r = np.array([h["r"][V].max() if V.any() else 9.0 for h in o["hits"]])
    W = WEIGHTS[Wi]
    X = o["P"][:, 0]; Y = o["P"][:, 1]
    iD = int(np.argmin(np.abs(WAVES - WL_D)))
    rep_efl = paraxial(L)["efl"]
    for fi, (th, fw) in enumerate(zip(angs, FWEIGHT)):
        m = Fi == fi
        v = V[m]
        x, y, w = X[m], Y[m], W[m]
        ch = np.where(m & (Wi == iD) & (Pi == 0))[0][0]
        cy = Y[ch]
        cra = np.degrees(np.arccos(np.clip(o["D"][ch, 2], -1, 1))) if V[ch] else 90.0
        ideal = rep_efl * np.tan(np.radians(th))
        dist = (cy - ideal) / ideal if th > 0 else 0.0
        if not V[ch]:
            dist = 1.0
        if v.sum() < 3:
            res.append(np.full(2 * len(x), 50.0)); rep["spots"].append(np.inf)
            rep["cra"].append(90.0); rep["dist"].append(1.0)
            continue
        xc = np.average(x[v], weights=w[v]); yc = np.average(y[v], weights=w[v])
        ex = np.where(v, x - xc, 0.05) * 1e3
        ey = np.where(v, y - yc, 0.05) * 1e3
        sw = np.sqrt(w / w.sum()) * fw
        res.append(ex * sw); res.append(ey * sw)
        rep["spots"].append(float(np.sqrt(np.average(ex[v] ** 2 + ey[v] ** 2, weights=w[v]))))
        rep["cra"].append(float(cra)); rep["dist"].append(float(dist))
    rep["ca"] = hits_r
    par = paraxial(L)
    rep["efl"] = par["efl"]; rep["bfl_par"] = par["bfl"]
    pen = []
    pen.append(3.0 * (par["efl"] - EFL) * 1e3)
    pen.append(FOCUS_W[0] * (par["bfl"] - L.t[-1]) * 1e3)
    # thickness / edge / gap constraints
    ca = hits_r + 0.03
    zv = L.z_vertex()
    edge = []
    gaps = []
    slopes = []
    for i in range(L.S - 1):
        rr = np.linspace(0, max(ca[i], ca[i + 1]), 25)
        d = L.t[i] + L.sag(i + 1, rr) - L.sag(i, rr)
        if L.mat[i] == "AIR":
            gaps.append(d.min())
            pen.append(30.0 * max(0, GAP_MIN - d.min()) * 1e3)
        else:
            re = max(ca[i], ca[i + 1]) + 0.05
            de = L.t[i] + L.sag(i + 1, re) - L.sag(i, re)
            edge.append(float(de))
            pen.append(30.0 * max(0, EDGE_MIN - de) * 1e3)
            pen.append(30.0 * max(0, (T_MIN_PLASTIC if L.mat[i] != "SAPPHIRE" else 0.30) - L.t[i]) * 1e3)
    # back focus and L5 edge to image
    bfl = L.t[-1]
    rr = np.linspace(0, ca[-1], 25)
    dimg = bfl - L.sag(L.S - 1, rr)
    pen.append(30.0 * max(0, BFL_MIN - bfl) * 1e3)
    pen.append(30.0 * max(0, BFL_EDGE_MIN - dimg.min()) * 1e3)
    for i in range(L.S):
        sl = np.degrees(np.arctan(np.abs(L.dsag_dr(i, np.linspace(0, ca[i], 25))))).max()
        slopes.append(sl)
        pen.append(2.0 * max(0, sl - SLOPE_MAX) * 10)
        pen.append(20.0 * max(0, ca[i] - CA_MAX) * 1e3)
    for c_, d_ in zip(rep["cra"], rep["dist"]):
        pen.append(1.0 * max(0, c_ - CRA_MAX) * 5)
        pen.append(1.0 * max(0, abs(d_) - DIST_MAX) * 1e3)
    rep.update(edge=edge, gaps=gaps, slopes=slopes, bfl=bfl, img_edge_gap=float(dimg.min()))
    r = np.concatenate(res + [np.array(pen)])
    r = np.where(np.isfinite(r), r, 1e3)
    return r, rep


def merit(L):
    r, rep = evaluate(L)
    return float(np.sqrt(np.mean(r ** 2))), rep


def optimise(L0, n_asph, nfev, log, tag):
    x0 = pack(L0, n_asph)
    lo, hi = bounds(n_asph)
    x0 = np.clip(x0, lo + 1e-9, hi - 1e-9)

    def f(x):
        return evaluate(unpack(x, L0, n_asph))[0]
    t0 = time.time()
    sol = least_squares(f, x0, bounds=(lo, hi), method="trf", x_scale="jac",
                        max_nfev=nfev, diff_step=1e-6, ftol=1e-10, xtol=1e-10)
    L = unpack(sol.x, L0, n_asph)
    m, rep = merit(L)
    log.append(dict(stage=tag, n_asph=n_asph, nfev=int(sol.nfev), merit=m,
                    spots_um=[float(s) for s in rep["spots"]], efl=float(rep["efl"]),
                    seconds=round(time.time() - t0, 1)))
    print(f"[{tag}] merit {m:9.3f}  spots um {np.round(rep['spots'], 2)}  efl {rep['efl']:.4f}  "
          f"cra {np.round(rep['cra'][-1], 1)}  dist {np.round(100 * np.array(rep['dist'][-1]), 2)}%  "
          f"({time.time() - t0:.0f}s)", flush=True)
    return L, m


def main():
    quick = "--quick" in sys.argv
    scale = 0.3 if quick else 1.0
    log = []
    L = start_lens()
    # first get the EFL near target by scaling curvatures of L4
    m, rep = merit(L)
    print("start merit", m, "efl", rep["efl"], "spots", np.round(rep["spots"], 2))
    L.save(os.path.join(OUT, "lens_start.json"), dict(merit=m))
    log.append(dict(stage="start", merit=m, spots_um=[float(s) for s in rep["spots"]], efl=float(rep["efl"])))
    for fs in (0.5, 0.75, 0.9):
        FIELD_SCALE[0] = fs
        L, m = optimise(L, 1, int(200 * scale), log, f"A0: field {fs:.2f}, c, k, A4, t")
    FIELD_SCALE[0] = 1.0
    L, m = optimise(L, 1, int(400 * scale), log, "A: c, k, A4, t")
    L, m = optimise(L, 3, int(800 * scale), log, "B: + A6, A8")
    L, m = optimise(L, NA, int(1500 * scale), log, "C: + A10..A16")
    best, bm = L, m
    rng = np.random.default_rng(7)
    for rs in range(0 if quick else 4):
        x = pack(best, NA)
        lo, hi = bounds(NA)
        x = np.clip(x + rng.normal(0, 0.02, x.size) * (hi - lo) * 0.05, lo + 1e-9, hi - 1e-9)
        Lp = unpack(x, best, NA)
        Lp, mp = optimise(Lp, NA, int(1200 * scale), log, f"D{rs}: perturbed restart")
        if mp < bm:
            best, bm = Lp, mp
    m, rep = merit(best)
    best.save(os.path.join(OUT, "lens_final.json"), dict(merit=m))
    with open(os.path.join(OUT, "optimize_log.json"), "w") as f:
        json.dump(log, f, indent=1)
    print("final merit", m)


if __name__ == "__main__":
    main()
