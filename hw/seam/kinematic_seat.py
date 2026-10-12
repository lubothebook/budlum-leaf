#!/usr/bin/env python3
"""kinematic_seat.py - the quadrant seat: Si3N4 balls in WC vees, N52H preload.

Deliverable 1 of the seam team. It proves:
  1. the constraint count: the + seat leaves exactly the global rigid motion
     free in plane, and one benign rz loop redundancy (rank analysis);
  2. one seat cell (two vees on a tile edge) leaves only the fold and the
     along-seam slide free, so the seat never fights the body bend;
  3. the Hertz contact of a straight vee and of the gothic-arch vee, with the
     ring-crack check of both ceramics;
  4. the stiffness of a ball, a tile and the tile natural frequency;
  5. the repeatability by Monte Carlo over 10 000 swaps, with wear;
  6. the thermal shift of the seat from the preload change -10..+50 C.
Gate: MEC-40 (repeat under 1 um over 10 000 swaps).
"""
import json
import math
import os
import numpy as np
import seam_params as P

R_BALL = P.BALL_D_mm / 2 * 1e-3


def e_star(m1="Si3N4", m2="WC-Ni"):
    E1, n1 = P.MAT[m1][:2]
    E2, n2 = P.MAT[m2][:2]
    return 1.0 / ((1 - n1 ** 2) / E1 + (1 - n2 ** 2) / E2)


def g_star(m1="Si3N4", m2="WC-Ni"):
    E1, n1 = P.MAT[m1][:2]
    E2, n2 = P.MAT[m2][:2]
    G1, G2 = E1 / (2 * (1 + n1)), E2 / (2 * (1 + n2))
    return 1.0 / ((2 - n1) / G1 + (2 - n2) / G2)


def hertz(W, Rx, Ry=None):
    """Elliptical Hertz contact, Hamrock-Brewe closed forms [PUBLICATION].

    Rx, Ry: effective radii in the two principal planes (Ry >= Rx).
    Returns semi-axes a (along the larger radius), b, p0, approach, k_normal.
    """
    Ry = Rx if Ry is None else Ry
    Ep = 2 * e_star()
    Rp = 1.0 / (1.0 / Rx + 1.0 / Ry)
    kk = 1.0339 * (Ry / Rx) ** 0.636
    eps = 1.0003 + 0.5968 * Rx / Ry
    zeta = 1.5277 + 0.6023 * math.log(Ry / Rx)
    a = (6 * kk ** 2 * eps * W * Rp / (math.pi * Ep)) ** (1 / 3)
    b = (6 * eps * W * Rp / (math.pi * kk * Ep)) ** (1 / 3)
    d = zeta * ((9 / (2 * eps * Rp)) * (W / (math.pi * kk * Ep)) ** 2) ** (1 / 3)
    p0 = 3 * W / (2 * math.pi * a * b)
    return dict(a=a, b=b, p0=p0, delta=d, k_n=1.5 * W / d, k_t=8 * g_star() * math.sqrt(a * b))


def flank_load(F_ball, kind="vee"):
    """Normal load on each contact for a ball pressed with F_ball along the seat axis."""
    if kind == "vee":
        half = math.radians(P.VEE_INCLUDED_deg / 2)
        return F_ball / (2 * math.sin(half)), 2      # normals at (90 - half) deg to the axis
    beta = math.radians(P.TRIHEDRAL_NORMAL_deg)
    return F_ball / (3 * math.cos(beta)), 3


def contact_set(F_ball, gothic=True, kind="vee"):
    N, n = flank_load(F_ball, kind)
    if gothic and kind == "vee":
        rg = P.GOTHIC_CONFORMITY * P.BALL_D_mm * 1e-3
        Ry = 1.0 / (1.0 / R_BALL - 1.0 / rg)
        h = hertz(N, R_BALL, Ry)
    else:
        h = hertz(N, R_BALL)
    h["N"] = N
    h["n_contacts"] = n
    # Hertz ring crack: radial tension at the contact edge, (1 - 2 nu) / 3 * p0
    h["ring_tension_Si3N4"] = (1 - 2 * P.MAT["Si3N4"][1]) / 3 * h["p0"]
    h["ring_tension_WC"] = (1 - 2 * P.MAT["WC-Ni"][1]) / 3 * h["p0"]
    h["tau_max"] = 0.31 * h["p0"]
    return h


def ball_stiffness(F_ball, gothic=True):
    """3x3 stiffness of one ball in a vee: frame x = seat axis, y = groove, z = up."""
    h = contact_set(F_ball, gothic)
    half = math.radians(P.VEE_INCLUDED_deg / 2)
    K_kin, K_stick = np.zeros((3, 3)), np.zeros((3, 3))
    for s in (1, -1):
        n = np.array([math.sin(half), 0.0, s * math.cos(half)])
        nn = np.outer(n, n)
        K_kin += h["k_n"] * nn
        K_stick += h["k_n"] * nn + h["k_t"] * (np.eye(3) - nn)
    return K_kin, K_stick, h


# --------------------------------------------------------------------------
# constraint rank analysis
# --------------------------------------------------------------------------
def rank_inplane():
    """Quadrants as in-plane rigid bodies (x, y, rz). Rows = constraint directions."""
    order = ["Q1", "Q2", "Q3", "Q4"]
    rows = []
    for c in P.seat_contacts():
        nvec = np.array(c["normal"])
        dirs = [nvec]
        if c["kind"] == "trihedral":
            dirs.append(np.array(c["along"]))
        p = np.array([c["x"], c["y"]])
        for d in dirs:
            r = np.zeros(12)
            jb, jr = order.index(c["ball"]), order.index(c["recv"])
            mom = p[0] * d[1] - p[1] * d[0]
            r[3 * jb:3 * jb + 3] = [d[0], d[1], mom]
            r[3 * jr:3 * jr + 3] = [-d[0], -d[1], -mom]
            rows.append(r)
    A = np.array(rows)
    rk = np.linalg.matrix_rank(A, tol=1e-9)
    # rank of each seam alone: the sum minus the system rank is the loop redundancy
    per = {}
    idx = 0
    for c in P.seat_contacts():
        n = 2 if c["kind"] == "trihedral" else 1
        per.setdefault(c["ha"], []).extend(range(idx, idx + n))
        idx += n
    per_rank = {k: int(np.linalg.matrix_rank(A[v], tol=1e-9)) for k, v in per.items()}
    return dict(rows=len(rows), rank=int(rk), dof=12, mobility=12 - int(rk),
                per_seam_rank=per_rank,
                loop_redundancy=int(sum(per_rank.values()) - rk))


def rank_tile(kind="two-vee"):
    """One seat cell: ball tile against a fixed receiver tile, 6 DOF."""
    pts = [(0.0, s, 0.0) for s in P.BALL_S_mm]
    rows = []
    for (x, y, z) in pts:
        for d in (np.array([1.0, 0, 0]), np.array([0, 0, 1.0])):   # vee: normal and z
            p = np.array([x, y, z])
            rows.append(np.concatenate([d, np.cross(p, d)]))
    A = np.array(rows)
    rk = np.linalg.matrix_rank(A)
    # free motions: null space
    _, s, vt = np.linalg.svd(A)
    null = vt[rk:]
    return dict(rank=int(rk), free=null.round(3).tolist())


def rank_hub():
    """The hub tile of Q1: two balls on x = 0 (trihedral + vee), one Q4 ball in its vee."""
    rows = []
    def add(p, d):
        p = np.array(p, float)
        d = np.array(d, float)
        rows.append(np.concatenate([d, np.cross(p, d)]))
    s1, s2 = P.BALL_S_mm
    add((0, s1, 0), (1, 0, 0)); add((0, s1, 0), (0, 1, 0)); add((0, s1, 0), (0, 0, 1))
    add((0, s2, 0), (1, 0, 0)); add((0, s2, 0), (0, 0, 1))
    add((P.SINGLE_BALL_S_mm, 0, 0), (0, 1, 0)); add((P.SINGLE_BALL_S_mm, 0, 0), (0, 0, 1))
    A = np.array(rows)
    return dict(rows=len(rows), rank=int(np.linalg.matrix_rank(A)))


# --------------------------------------------------------------------------
# repeatability Monte Carlo
# --------------------------------------------------------------------------
def repeat_mc(n_swaps=10000, seed=7, K_wear=1e-6):
    """Edge-pixel position error of one tile pair per swap (dx across, dz step)."""
    rng = np.random.default_rng(seed)
    F_ball = P.PRELOAD_PER_BALL_N
    K_kin, K_st, h = ball_stiffness(F_ball)
    kx, kz, kt = K_kin[0, 0], K_kin[2, 2], h["k_t"]
    mu, N = P.MU_SI3N4_WC, h["N"]
    rq = math.hypot(0.010, 0.012) * 1e-6        # ball G3 and lapped WC, Rq [GENERAL]
    out = np.zeros((n_swaps, 2))
    wear = np.zeros(n_swaps)
    vol = 0.0
    for i in range(n_swaps):
        dx_b, dz_b = [], []
        for _ in range(2):                      # two balls of the tile
            ft = rng.uniform(-mu * N, mu * N, 2)  # friction residual on each flank, tangential
            # tangential residuals on the +45 and -45 flanks map to (x, z)
            half = math.radians(45)
            t1 = np.array([-math.cos(half), 0, math.sin(half)])
            t2 = np.array([-math.cos(half), 0, -math.sin(half)])
            dpos = (ft[0] * t1 + ft[1] * t2) / kt * 0.5   # half: the two flanks share
            rough = rng.normal(0, 0.5 * rq, 2)
            misfit = rng.normal(0, 0.01) / (2 * kx)       # coupler misfit change, 10 mN rms
            dx_b.append(dpos[0] + rough[0] + misfit)
            dz_b.append(dpos[2] + rough[1])
        # Archard micro-slip wear: 2 um slip per swap per flank
        vol += K_wear * 1e-9 * N * 2e-6                   # m^3, K in mm^3/(N m)
        depth = vol / (math.pi * h["a"] * h["b"] * 4)     # spread as the spot widens x4
        wear[i] = depth / math.cos(math.radians(45))
        out[i] = [np.mean(dx_b) + wear[i], np.mean(dz_b)]
    swap_to_swap = np.diff(out, axis=0)
    return dict(
        sigma_dx_um=float(np.std(swap_to_swap[:, 0]) * 1e6 / math.sqrt(2)),
        sigma_dz_um=float(np.std(swap_to_swap[:, 1]) * 1e6 / math.sqrt(2)),
        p999_dx_um=float(np.percentile(np.abs(swap_to_swap[:, 0]), 99.9) * 1e6),
        p999_dz_um=float(np.percentile(np.abs(swap_to_swap[:, 1]) * 1e6, 99.9)),
        wear_drift_x_um=float(wear[-1] * 1e6),
        trace=out,
    )


def tile_mass_g():
    dens = {"PC cap + AgNW": 1.2, "OCA": 1.0, "glass-LED-glass": 2.45, "slip OCA": 1.0,
            "Qi coil / spreader": 4.0, "micro cell": 2.6, "hinge routing + tolerance": 1.5,
            "floating back skin": 1.1}
    m = 0.0
    for name, t in P.STACK:
        area = P.CELL_mm ** 2 if name == "micro cell" else P.TILE_mm ** 2
        m += t * area * dens[name] * 1e-3
    return m


def main():
    res = {}
    F = P.PRELOAD_PER_BALL_N
    hot = 1.0
    cold = (1 + P.N52H["Br_tc"] * (P.T_MIN_C - 20)) ** 2 / (1 + P.N52H["Br_tc"] * (P.T_MAX_C - 20)) ** 2
    print("== Hertz contact per ball, Si3N4 D0.50 mm in WC-Ni, 90 deg vee ==")
    for label, Fb in (("+50 C floor", F), ("-10 C", F * cold), ("overload stop", P.OVERLOAD_RELEASE_N)):
        for gothic in (False, True):
            h = contact_set(Fb, gothic)
            key = f"{label} {'gothic' if gothic else 'straight'}"
            res[key] = {k: float(v) for k, v in h.items()}
            print(f"{key:28s} N {h['N']*1e3:6.1f} mN  a {h['a']*1e6:5.2f} b {h['b']*1e6:5.2f} um  "
                  f"p0 {h['p0']/1e9:4.2f} GPa  ring Si3N4 {h['ring_tension_Si3N4']/1e6:4.0f} MPa  "
                  f"k_n {h['k_n']/1e6:5.2f} N/um")
    tri = contact_set(F, gothic=False, kind="trihedral")
    res["trihedral +50 C"] = {k: float(v) for k, v in tri.items()}
    print(f"trihedral, 3 flat faces: N {tri['N']*1e3:.1f} mN, p0 {tri['p0']/1e9:.2f} GPa")

    K_kin, K_st, h = ball_stiffness(F)
    mass = tile_mass_g()
    k_tile_x = 2 * K_kin[0, 0]
    k_tile_z = 2 * K_kin[2, 2]
    f_z = 1 / (2 * math.pi) * math.sqrt(k_tile_z / (mass * 1e-3))
    res["stiffness"] = dict(ball_x_N_per_um=K_kin[0, 0] / 1e6, ball_z_N_per_um=K_kin[2, 2] / 1e6,
                            ball_y_stick_N_per_um=K_st[1, 1] / 1e6, tile_x_N_per_um=k_tile_x / 1e6,
                            tile_z_N_per_um=k_tile_z / 1e6, tile_mass_g=mass,
                            tile_f_z_kHz=f_z / 1e3, z_capacity_per_tile_N=2 * F)
    print(f"stiffness: ball x {K_kin[0,0]/1e6:.2f}, z {K_kin[2,2]/1e6:.2f} N/um (kinematic), "
          f"y stick {K_st[1,1]/1e6:.2f} N/um; tile x {k_tile_x/1e6:.2f}, z {k_tile_z/1e6:.2f} N/um")
    print(f"tile mass {mass:.3f} g, tile-on-seat mode {f_z/1e3:.1f} kHz; z load before a flank unloads "
          f"{2*F:.2f} N per tile = {2*F/(mass*1e-3*9.81):.0f} g")

    # thermal seat shift from preload change -10..+50 C (gothic, per flank)
    h50 = contact_set(F, True)
    hm10 = contact_set(F * cold, True)
    d_shift = (hm10["delta"] - h50["delta"]) / math.sin(math.radians(45))
    res["preload_thermal_shift_um"] = d_shift * 1e6
    print(f"seat shift from preload change over -10..+50 C: {d_shift*1e6*1e3:.1f} nm along the seat axis, 0 in z (symmetric)")

    res["rank_inplane"] = rank_inplane()
    res["rank_tile"] = rank_tile()
    res["rank_hub"] = rank_hub()
    print("in-plane rank:", res["rank_inplane"])
    print("seat cell rank:", res["rank_tile"]["rank"], "free motions:", res["rank_tile"]["free"])
    print("hub tile rank:", res["rank_hub"])

    # redundancy loads: lattice hinges absorb seat misfit
    rb = P.RIBBON
    A = rb["t_um"] * 1e-6 * rb["h_mm"] * 1e-3
    k_axial = rb["E"] * A / (rb["L_mm"] * 1e-3)
    I = rb["t_um"] * 1e-6 * (rb["h_mm"] * 1e-3) ** 3 / 12
    k_bend = 12 * rb["E"] * I / (rb["L_mm"] * 1e-3) ** 3
    k_shear = rb["G"] * A / (rb["L_mm"] * 1e-3) * 5 / 6
    k_z = 1 / (1 / k_bend + 1 / k_shear)
    rz_loop = 2e-6 / 75e-3
    res["redundancy"] = dict(ribbon_axial_N_per_um=k_axial / 1e6, ribbon_z_N_per_um=k_z / 1e6,
                             misfit_1um_axial_N=k_axial * 1e-6, misfit_1um_z_N=k_z * 1e-6,
                             rz_loop_misclosure_urad=rz_loop * 1e6)
    print(f"ribbon: axial {k_axial/1e6*1e3:.1f} mN/um, z-shear {k_z/1e6*1e3:.1f} mN/um; "
          f"1 um misfit costs {k_axial*1e-6*1e3:.0f} mN axial, {k_z*1e-6*1e3:.0f} mN in z")

    mc = repeat_mc()
    for k in ("sigma_dx_um", "sigma_dz_um", "p999_dx_um", "p999_dz_um", "wear_drift_x_um"):
        res.setdefault("repeat", {})[k] = mc[k]
    mc6 = repeat_mc(K_wear=1e-5)
    res["repeat"]["wear_drift_x_um_K1e-5"] = mc6["wear_drift_x_um"]
    print(f"repeat per swap: sigma dx {mc['sigma_dx_um']*1e3:.1f} nm, dz {mc['sigma_dz_um']*1e3:.1f} nm; "
          f"99.9 % |dx| {mc['p999_dx_um']*1e3:.0f} nm, |dz| {mc['p999_dz_um']*1e3:.0f} nm")
    print(f"wear drift after 10 000 swaps: {mc['wear_drift_x_um']*1e3:.1f} nm (K = 1e-6), "
          f"{mc6['wear_drift_x_um']*1e3:.1f} nm (K = 1e-5), along the seat axis, none in z")
    res["gate_MEC40_repeat_pass"] = bool(mc["p999_dx_um"] < 1.0 and mc["p999_dz_um"] < 1.0
                                         and mc6["wear_drift_x_um"] < 1.0)
    print("MEC-40 repeat < 1 um over 10 000 swaps:", "PASS" if res["gate_MEC40_repeat_pass"] else "FAIL")
    os.makedirs("results", exist_ok=True)
    np.save("results/repeat_trace.npy", mc["trace"])
    json.dump(res, open("results/kinematic_seat.json", "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    main()
