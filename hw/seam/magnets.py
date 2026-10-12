#!/usr/bin/env python3
"""magnets.py - N52H preload magnets of the quadrant seat.

1. Force between two cuboid magnets: the analytic Akoun-Yonnet solution
   [PUBLICATION] G. Akoun, J.-P. Yonnet, IEEE Trans. Magn. 20(5) 1962-1964, 1984.
   It is checked against a brute-force surface-charge integral.
2. The demagnetising factor of a prism: Aharoni [PUBLICATION]
   A. Aharoni, J. Appl. Phys. 83, 3432 (1998). Checked: a cube gives 1/3.
3. The sizing: the magnet length per tile type that gives the ball preload at
   +50 C, the force at -10 C, and the demagnetisation margin of a loose quadrant.
"""
import itertools
import json
import math
import os
import numpy as np
import seam_params as P


def akoun_yonnet(J1, J2, d1, d2, offset):
    """Force on magnet 2 from magnet 1, both magnetised along +z.

    d1, d2: full dimensions (x, y, z) in m. offset: centre of 2 minus centre of 1.
    Returns (Fx, Fy, Fz) in N.
    """
    a, b, c = (d / 2.0 for d in d1)
    A, B, C = (d / 2.0 for d in d2)
    al, be, ga = offset
    F = np.zeros(3)
    for i, j, k, l, p, q in itertools.product((0, 1), repeat=6):
        u = al + (-1) ** j * A - (-1) ** i * a
        v = be + (-1) ** l * B - (-1) ** k * b
        w = ga + (-1) ** q * C - (-1) ** p * c
        r = math.sqrt(u * u + v * v + w * w)
        sgn = (-1) ** (i + j + k + l + p + q)
        lru = math.log(max(r - u, 1e-30))
        lrv = math.log(max(r - v, 1e-30))
        at = math.atan2(u * v, r * w) if abs(w) > 0 else 0.0
        fx = 0.5 * (v * v - w * w) * lru + u * v * lrv + v * w * at + 0.5 * r * u
        fy = 0.5 * (u * u - w * w) * lrv + u * v * lru + u * w * at + 0.5 * r * v
        fz = -u * w * lru - v * w * lrv + u * v * at - r * w
        F += sgn * np.array([fx, fy, fz])
    return J1 * J2 / (4 * math.pi * P.MU0) * F


def charge_model(J1, J2, d1, d2, offset, n=14):
    """Brute-force check: Coulomb force between the four pole sheets."""
    g, wts = np.polynomial.legendre.leggauss(n)

    def sheet(d, ctr, zsign):
        X, Y = np.meshgrid(g * d[0] / 2, g * d[1] / 2, indexing="ij")
        W = np.outer(wts, wts) * d[0] * d[1] / 4
        pts = np.stack([X.ravel() + ctr[0], Y.ravel() + ctr[1],
                        np.full(X.size, ctr[2] + zsign * d[2] / 2)], 1)
        return pts, W.ravel()

    F = np.zeros(3)
    for s1 in (1, -1):
        p1, w1 = sheet(d1, (0, 0, 0), s1)
        for s2 in (1, -1):
            p2, w2 = sheet(d2, offset, s2)
            R = p2[None, :, :] - p1[:, None, :]
            r3 = np.linalg.norm(R, axis=2) ** 3
            F += s1 * s2 * np.einsum("ij,ijk->k", (w1[:, None] * w2[None, :]) / r3, R)
    return J1 * J2 / (4 * math.pi * P.MU0) * F


def aharoni_dz(a, b, c):
    """Magnetometric demag factor along c of a 2a x 2b x 2c prism."""
    r = math.sqrt(a * a + b * b + c * c)
    ab, bc, ac = math.hypot(a, b), math.hypot(b, c), math.hypot(a, c)
    t = ((b * b - c * c) / (2 * b * c) * math.log((r - a) / (r + a))
         + (a * a - c * c) / (2 * a * c) * math.log((r - b) / (r + b))
         + b / (2 * c) * math.log((ab + a) / (ab - a))
         + a / (2 * c) * math.log((ab + b) / (ab - b))
         + c / (2 * a) * math.log((bc - b) / (bc + b))
         + c / (2 * b) * math.log((ac - a) / (ac + a))
         + 2 * math.atan(a * b / (c * r))
         + (a ** 3 + b ** 3 - 2 * c ** 3) / (3 * a * b * c)
         + (a * a + b * b - 2 * c * c) / (3 * a * b * c) * r
         + c / (a * b) * (ac + bc)
         - (ab ** 3 + bc ** 3 + ac ** 3) / (3 * a * b * c))
    return t / math.pi


def br_at(T):
    return P.N52H["Br"] * (1 + P.N52H["Br_tc"] * (T - 20.0))


def hcj_at(T):
    return P.N52H["Hcj"] * (1 + P.N52H["Hcj_tc"] * (T - 20.0))


def pair_force(L_mm, T=23.0, gap_um=None, dy_mm=0.0, dz_mm=0.0):
    """Attractive force of a facing pair (seam normal = local z of the formula)."""
    gap = (gap_um if gap_um is not None else P.MAG_GAP_um) * 1e-6
    d = (L_mm * 1e-3, P.MAG_H_mm * 1e-3, P.MAG_T_mm * 1e-3)
    J = br_at(T)
    off = (dy_mm * 1e-3, dz_mm * 1e-3, P.MAG_T_mm * 1e-3 + gap)
    F = akoun_yonnet(J, J, d, d, off)
    return -F[2], F[0], F[1]           # normal (attractive +), along-seam, z


def size_length(target_N, T=50.0):
    """Shortest magnet length (0.05 mm steps) that gives target_N at temperature T."""
    L = 0.5
    while L < 9.0:
        if pair_force(L, T)[0] >= target_N:
            return round(L, 2)
        L += 0.05
    return None


def collar_force():
    c = P.COLLAR
    area = math.pi / 4 * (c["OD_mm"] ** 2 - c["ID_mm"] ** 2)
    free = math.pi * (c["OD_mm"] + c["ID_mm"]) * c["h_mm"]
    S = area / free
    sigma = c["E"] * c["squeeze"] * (1 + 2 * S * S)
    return sigma * area * 1e-6, sigma, S


def main():
    res = {}
    # ---- validation of the force model
    d = (2e-3, 1e-3, 0.5e-3)
    off = (0.1e-3, 0.05e-3, 0.5e-3 + 0.3e-3)
    fa = akoun_yonnet(1.4, 1.4, d, d, off)
    fn = charge_model(1.4, 1.4, d, d, off, n=16)
    err = float(np.max(np.abs(fa - fn)) / np.max(np.abs(fn)))
    res["validation_force_rel_err"] = err
    print(f"Akoun-Yonnet vs charge model at 0.3 mm gap: {fa*1e3} mN vs {fn*1e3} mN, err {err:.2e}")
    # dipole limit far away
    m = 1.4 / P.MU0 * np.prod(d)
    z = 20e-3
    f_dip = 3 * P.MU0 * m * m / (2 * math.pi * z ** 4)
    f_ay = -akoun_yonnet(1.4, 1.4, d, d, (0, 0, z))[2]
    res["validation_dipole_ratio"] = f_ay / f_dip
    print(f"far field, AY / dipole = {f_ay/f_dip:.4f}")
    cube = aharoni_dz(1, 1, 1)
    res["validation_cube_demag"] = cube
    print(f"Aharoni cube demag factor {cube:.5f} (exact 1/3)")

    # ---- loads to be carried by each tile type at +50 C (worst, weakest magnet)
    pre = P.PRELOAD_PER_BALL_N
    Fc, sig_c, S = collar_force()
    leaf = 2 * (P.LEAF_FORCE_N + Fc)
    ribbon_misfit = 0.05              # coupler ribbon misfit allowance, from split_coupler.py
    hot = 1 + 2 * P.N52H["Br_tc"] * (P.T_MAX_C - P.T_REF_C)
    types = {
        "two-ball tile": 2 * pre + ribbon_misfit,
        "one-ball hub tile (short half-axis)": 1 * pre + ribbon_misfit,
        "leaf magnet (cancels two sealed leaves at z = 1.55 mm)": leaf,
    }
    sizing = {}
    for name, need23 in types.items():
        need50 = need23            # the preload target is a +50 C floor
        L = size_length(need50, P.T_MAX_C)
        F_cold = pair_force(L, P.T_MIN_C)[0]
        F_ref = pair_force(L, P.T_REF_C)[0]
        F_hot = pair_force(L, P.T_MAX_C)[0]
        sizing[name] = dict(need_N=need50, L_mm=L, F_m10=F_cold, F_23=F_ref, F_50=F_hot)
        print(f"{name:55s} need {need50:.3f} N at +50 C -> L = {L:.2f} mm; "
              f"F = {F_cold:.3f} / {F_ref:.3f} / {F_hot:.3f} N at -10 / 23 / 50 C")
    res["sizing"] = sizing
    res["collar"] = dict(force_N=Fc, stress_MPa=sig_c / 1e6, shape_factor=S)
    res["hot_factor"] = hot

    # ---- gap sensitivity and lateral (along-seam) stiffness of a 2-ball pair
    L2 = sizing["two-ball tile"]["L_mm"]
    gaps = [20, 49, 100, 250, 500, 1000, 2000]
    res["force_vs_gap"] = {g: pair_force(L2, 23.0, g)[0] for g in gaps}
    f0 = pair_force(L2, 23.0)[0]
    f1 = pair_force(L2, 23.0, P.MAG_GAP_um + 1.0)[0]
    res["k_normal_N_per_um"] = f1 - f0           # negative stiffness of the pair
    fy = pair_force(L2, 23.0, dy_mm=0.005)[1]
    res["k_along_N_per_um"] = -fy / 5.0
    fz = pair_force(L2, 23.0, dz_mm=0.002)[2]
    res["k_z_N_per_um"] = -fz / 2.0
    print(f"pair stiffness: normal {res['k_normal_N_per_um']*1e3:.2f} mN/um (negative), "
          f"along {res['k_along_N_per_um']*1e3:.2f} mN/um, z {res['k_z_N_per_um']*1e3:.2f} mN/um")

    # ---- demagnetisation margin of a loose (unseated) quadrant
    a, b, c = L2 / 2, P.MAG_H_mm / 2, P.MAG_T_mm / 2
    Nd = aharoni_dz(a, b, c)
    out = {}
    for T in (P.T_MAX_C, 60.0, 80.0):
        Hd = 1.2 * Nd * br_at(T) / P.MU0         # 1.2 = edge and corner local excess
        Hk = P.N52H["knee"] * hcj_at(T)
        out[T] = dict(Hd_kA_m=Hd / 1e3, Hknee_kA_m=Hk / 1e3, margin=Hk / Hd)
        print(f"loose magnet at {T:4.0f} C: Nd {Nd:.3f}, H_d {Hd/1e3:.0f} kA/m, "
              f"knee {Hk/1e3:.0f} kA/m, margin {Hk/Hd:.2f}")
    res["demag"] = dict(Nd=Nd, cases=out)

    # removal force of one quadrant: 8 long-edge tiles + 4 short-edge tiles
    q = sizing
    F_long = 7 * q["two-ball tile"]["F_23"] + q["two-ball tile"]["F_23"]
    F_short = 3 * q["two-ball tile"]["F_23"] + q["one-ball hub tile (short half-axis)"]["F_23"]
    res["removal"] = dict(long_edge_N=F_long, short_edge_N=F_short,
                          diagonal_pull_N=math.hypot(F_long, F_short))
    print(f"quadrant pull-off at 23 C: long edge {F_long:.2f} N, short edge {F_short:.2f} N, "
          f"diagonal pull {math.hypot(F_long, F_short):.2f} N (no peel credit)")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/magnets.json", "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    main()
