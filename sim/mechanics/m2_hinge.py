"""(2) The edge-on polyimide hinge: strain, copper, fatigue and the R 25.5 mm wrap.

Part A. In-plane hinge turn 2*theta, bending through the 12.5 um thickness.
  free chord : the lattice lets the chord relax, pure arc, eps = t*phi/(2L)
  pinned     : the tiles turn about the ideal corner pivot, so the chord is
               L*cos(phi/2). Solved as an Euler elastica (scipy solve_bvp).
Part B. Copper in the ribbon: composite neutral axis, Cu strain vs offset.
Part C. Fatigue: Cu by Coffin-Manson (Manson universal slopes), PI by
  Basquin with a Goodman mean-stress fix. Gates MEC-42 and MEC-39.
Part D. Out-of-plane wrap of the body to R 25.5 mm (16 rows -> 22.5 deg per
  row). The as-specified edge-on ribbon, at every in-plane orientation, and
  the proposed universal hinge.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq

from common import (DEG, E_CU, E_PI, H_RIBBON, L_RIBBON, NY, PLOTS, SU_CU, T_BODY,
                    T_CU, T_PI, UTS_PI, YIELD_STRAIN_PI, A_TILE, mm, um, save, verdict)

PHI_GATE = {"25 % (2theta=35 deg)": 35 * DEG, "41 % (2theta=90 deg)": 90 * DEG}
CYCLES = {"25 % (2theta=35 deg)": 10_000, "41 % (2theta=90 deg)": 1_000}
LIFE_FACTOR = 10.0
NX_COLS = 8             # hinges across one row boundary for a pull along y      # [DECISION of this team] the predicted life must be 10x the gate cycles

# ------------------------------------------------------------------ Part A


def eps_free(phi, t=T_PI, L=L_RIBBON):
    return t * phi / (2 * L)


def kappa_pinned(phi):
    """Max non-dimensional curvature kappa*L of the elastica with chord cos(phi/2)."""
    c = np.cos(phi / 2)
    s = np.linspace(0, 1, 201)

    def f(s, y, p):
        return np.vstack([y[1], -p[0] * np.sin(y[0]), np.cos(y[0])])

    def bc(ya, yb, p):
        return np.array([ya[0] + phi / 2, yb[0] - phi / 2, ya[2], yb[2] - c])
    y0 = np.vstack([-phi / 2 + phi * s, phi * np.ones_like(s), np.sinc(phi / 2 / np.pi) * s])
    sol = solve_bvp(f, bc, s, y0, p=[1.0], tol=1e-8, max_nodes=20000)
    assert sol.success, sol.message
    return np.abs(sol.sol(np.linspace(0, 1, 2001))[1]).max(), sol.p[0]


def elastica_tension(phi, T, t=T_PI, L=L_RIBBON, h=H_RIBBON[0]):
    """Free-chord ribbon with end tension T [N] and end angles -phi/2, +phi/2.

    Returns (max PI strain, chord / L). Tension pulls the ribbon straight and
    puts the turn into two end kinks of length sqrt(EI/T).
    """
    EI = E_PI * h * t ** 3 / 12
    p = -T * L ** 2 / EI
    s = np.linspace(0, 1, 401)
    y = np.vstack([-phi / 2 + phi * s, phi * np.ones_like(s), np.sinc(phi / 2 / np.pi) * s])
    for pk in np.linspace(0, p, 2 + int(abs(p) // 5)):
        sol = solve_bvp(lambda s, y: np.vstack([y[1], -pk * np.sin(y[0]), np.cos(y[0])]),
                        lambda ya, yb: np.array([ya[0] + phi / 2, yb[0] - phi / 2, ya[2]]),
                        s, y, tol=1e-7, max_nodes=50000)
        s, y = sol.x, sol.y
    k = np.abs(y[1]).max()
    return t / 2 * k / L, y[2, -1]


def t_allow(phi, eps_lim, **kw):
    """Largest hinge tension that keeps the PI strain at eps_lim."""
    if elastica_tension(phi, 0.0, **kw)[0] >= eps_lim:
        return 0.0
    hi = 1e-3
    while elastica_tension(phi, hi, **kw)[0] < eps_lim:
        hi *= 2
    return brentq(lambda T: elastica_tension(phi, T, **kw)[0] - eps_lim, 0.0, hi, xtol=1e-7)


def eps_pinned(phi, t=T_PI, L=L_RIBBON):
    k, _ = kappa_pinned(phi)
    return t / 2 * k / L

# ------------------------------------------------------------------ Part B


def copper_strain(kappa, offset, f_cu=0.5, t=T_PI, tcu=T_CU):
    """Strain at the Cu fibre and at the PI skin for a Cu layer at `offset`.

    The section per unit height: PI of thickness t with an embedded Cu strip
    of thickness tcu covering a fraction f_cu of the ribbon height.
    """
    ea_pi = E_PI * (t - f_cu * tcu)
    ea_cu = E_CU * f_cu * tcu
    y_na = ea_cu * offset / (ea_pi + ea_cu)       # PI centroid stays near 0
    eps_cu = (abs(offset - y_na) + tcu / 2) * kappa
    eps_pi = (t / 2 + abs(y_na)) * kappa
    return eps_cu, eps_pi, y_na

# ------------------------------------------------------------------ Part C


def n_cu(d_eps, su=SU_CU, e=E_CU, duct=0.05):
    """Manson universal slopes: d_eps = 3.5 Su/E N^-0.12 + D^0.6 N^-0.6.

    duct = true fracture ductility D. 0.05 is a thin-film value [HYPOTHESIS];
    rolled annealed foil reaches 0.3 to 0.6 [GENERAL].
    """
    g = lambda lg: 3.5 * su / e * (10 ** lg) ** -0.12 + duct ** 0.6 * (10 ** lg) ** -0.6 - d_eps
    if g(12) > 0:
        return 1e12
    return 10 ** brentq(g, 0, 12)


def n_pi(eps_max, sf=UTS_PI, b=-0.085):
    """Basquin S-N with Goodman for a 0 -> eps_max cycle. b is [HYPOTHESIS]."""
    sa = sm = E_PI * eps_max / 2
    sar = sa / (1 - sm / UTS_PI)
    return 0.5 * (sar / sf) ** (1 / b)

# ------------------------------------------------------------------ Part D


def wrap_analysis(R=25.5 * mm):
    phi = A_TILE / R                      # row-to-row turn
    out = dict(R_mm=R / mm, phi_row_deg=phi / DEG, rows=NY, total_deg=NY * phi / DEG)
    h = H_RIBBON[0]
    # (i) as specified, ribbon crossing the row line (axis along y): bend about its height
    out["stiff_mode_strain"] = h / 2 * phi / L_RIBBON
    # largest row turn the stiff mode can take at 1 % strain, and the radius it gives
    phi_ok = 0.01 * L_RIBBON / (h / 2)
    out["stiff_mode_R_limit_mm"] = A_TILE / phi_ok / mm
    # (ii) orientation sweep: ribbon axis at angle alpha to the wrap axis
    alpha = np.linspace(0, 90, 91) * DEG
    tw = phi * np.cos(alpha) / L_RIBBON            # twist rate
    stiff = h / 2 * phi * np.sin(alpha) / L_RIBBON
    wagner_free = tw ** 2 * h ** 2 / 12            # edge fibre, free axial end
    wagner_fixed = tw ** 2 * h ** 2 / 8            # edge fibre, ends held apart
    shear = T_PI * tw                              # torsional shear strain
    # pivot offset: the tiles touch at a face line, the ribbon centre sits ~1.0 mm away
    d_off = 1.0 * mm
    sbend = 3 * T_PI * d_off * phi / L_RIBBON ** 2  # clamped-guided S-bend through thickness
    out["parallel_twist_edge_strain_free"] = float(wagner_free[0])
    out["parallel_twist_edge_strain_fixed"] = float(wagner_fixed[0])
    out["parallel_torsion_shear"] = float(shear[0])
    out["parallel_offset_sbend_strain"] = float(sbend)
    out["min_over_alpha_strain"] = float(np.min(np.maximum(stiff, wagner_free) + sbend * np.cos(alpha)))
    # seam opening at the face: rigid tiles turn about a contact line
    out["face_open_if_pivot_at_back_mm"] = T_BODY * phi / mm
    # (iii) the universal hinge fix: flat CPI segment in series, at pivot depth d_f
    d_f = 0.125 * mm
    L_f, w_f = 0.8 * mm, 0.5 * mm
    out["fix"] = dict(
        flat_len_mm=L_f / mm, flat_width_mm=w_f / mm, flat_t_um=T_PI / um, pivot_depth_mm=d_f / mm,
        flat_strain=T_PI * phi / (2 * L_f),
        # in-plane moment of the edge-on segment at 90 deg, carried by the flat segment edgewise
        flat_inplane_strain_at_90=(E_PI * h * T_PI ** 3 / 12 * (90 * DEG) / L_RIBBON)
        * (w_f / 2) / (E_PI * T_PI * w_f ** 3 / 12),
        face_kerf_close_um=d_f * phi / um,
        cap_top_bevel_um=max(0.0, (d_f * phi - 10 * um) / 2) / um,
        back_open_mm=(T_BODY - d_f) * phi / mm,
        R70_flat_strain=T_PI * (A_TILE / (70 * mm)) / (2 * L_f),
        face_out_R_limit_m=A_TILE / (10 * um / (T_BODY - d_f)),
    )
    # variant B: ball pivot and flat segment in the back tray, at depth 1.85 mm
    d_b = 1.85 * mm
    out["fix_back_pivot"] = dict(
        pivot_depth_mm=d_b / mm, wrap_direction="face out (screen outside)",
        face_seam_open_mm=d_b * phi / mm, back_skin_strain=0.0,
        face_in_R_limit_m=A_TILE / (10 * um / d_b))
    return out, alpha, stiff, wagner_free, sbend


def main():
    res = {}
    # ---- Part A: options
    phis = np.linspace(1, 90, 90) * DEG
    tlist = [7.5 * um, 12.5 * um, 25 * um]
    llist = [0.5 * mm, 0.8 * mm, 1.0 * mm, 1.2 * mm, 1.6 * mm]
    table = []
    for t in tlist:
        for L in llist:
            row = dict(t_um=t / um, L_mm=L / mm)
            for name, ph in PHI_GATE.items():
                row[name + " free"] = eps_free(ph, t, L)
                row[name + " pinned"] = eps_pinned(ph, t, L)
            table.append(row)
    res["options"] = table
    base = {name: dict(free=eps_free(ph), pinned=eps_pinned(ph),
                       pinned_axial_load=kappa_pinned(ph)[1]) for name, ph in PHI_GATE.items()}
    res["baseline"] = base
    res["final21_claims"] = {"25 %": 0.0048, "41 %": 0.0123}

    # ---- Part B + C
    fat = {}
    for mode in ("free", "pinned"):
        for off in (0.0, 0.5 * um, 1.0 * um, 2.0 * um):
            key = f"{mode}, Cu offset {off/um:.1f} um"
            D_cu = D_pi = 0.0
            rec = {}
            for name, ph in PHI_GATE.items():
                eps = base[name][mode]
                kap = 2 * eps / T_PI
                ec, ep, yna = copper_strain(kap, off)
                Nc, Np = n_cu(ec), n_pi(ep)
                D_cu += CYCLES[name] / Nc
                D_pi += CYCLES[name] / Np
                rec[name] = dict(eps_cu=ec, eps_pi=ep, N_cu=Nc, N_pi=Np,
                                 pi_below_half_yield=ep < YIELD_STRAIN_PI / 2)
            rec["miner_cu"] = D_cu; rec["miner_pi"] = D_pi
            rec["pass"] = bool(D_cu * LIFE_FACTOR <= 1 and D_pi * LIFE_FACTOR <= 1
                               and all(rec[n]["eps_pi"] < YIELD_STRAIN_PI / 2 for n in PHI_GATE))
            fat[key] = rec
    res["fatigue"] = fat
    # tolerance search: the largest Cu offset that still passes in the pinned bound
    offs = np.linspace(0, 4, 81) * um
    ok = []
    for off in offs:
        d = 0.0
        for name, ph in PHI_GATE.items():
            ec, _, _ = copper_strain(2 * base[name]["pinned"] / T_PI, off)
            d += CYCLES[name] / n_cu(ec)
        ok.append(d * LIFE_FACTOR <= 1)
    ok = np.array(ok)
    res["max_cu_offset_um_pinned"] = float(offs[ok].max() / um) if ok.any() else 0.0
    okf = []
    for off in offs:
        d, pi_ok = 0.0, True
        for name, ph in PHI_GATE.items():
            ec, ep, _ = copper_strain(2 * base[name]["free"] / T_PI, off)
            d += CYCLES[name] / n_cu(ec)
            pi_ok &= ep < YIELD_STRAIN_PI / 2
        okf.append(d * LIFE_FACTOR <= 1 and pi_ok)
    okf = np.array(okf)
    res["max_cu_offset_um_free"] = float(offs[okf].max() / um) if okf.any() else 0.0

    # ---- tension sensitivity: the allowed hinge tension per gate angle
    # limit: PI at half its yield (1.5 %) and Cu (1 um offset) inside the x10 fatigue life
    tens = {}
    for name, ph in PHI_GATE.items():
        # Cu strain limit from the fatigue curve at x10 cycles
        ecu_lim = brentq(lambda e: n_cu(e) - LIFE_FACTOR * CYCLES[name] * 2, 1e-4, 0.05)
        # Cu strain ~ (1 um + 1 um)/ (t/2) of the PI strain for a 1 um offset
        ratio = copper_strain(1.0, 1 * um)[0] / copper_strain(1.0, 1 * um)[1]
        lim = min(YIELD_STRAIN_PI / 2, ecu_lim / ratio)
        tens[name] = dict(eps_limit=lim, T_allow_N=t_allow(ph, lim),
                          chord_T0=elastica_tension(ph, 0.0)[1])
    res["tension"] = tens
    TT = np.logspace(-5, 0, 26)
    res["tension_curve_90"] = [[T, *elastica_tension(90 * DEG, T)] for T in TT]
    # ductility sensitivity at the baseline (free, centred)
    res["cu_life_vs_ductility_90deg"] = {
        str(D): n_cu(copper_strain(2 * base["41 % (2theta=90 deg)"]["pinned"] / T_PI, 0)[0], duct=D)
        for D in (0.02, 0.05, 0.1, 0.3)}

    # ---- Part E: the fix for tension. A load-bearing ball pivot at each corner
    # carries the tension, so the ribbon turns about a fixed point (pinned case).
    # Find the shortest ribbon that passes in the pinned case.
    piv = {}
    for t in (12.5 * um, 7.5 * um):
        def ok(L):
            D = 0.0
            good = True
            for name, ph in PHI_GATE.items():
                ep = eps_pinned(ph, t, L)
                ec, epi, _ = copper_strain(2 * ep / t, 1 * um, t=t)
                D += CYCLES[name] / n_cu(ec)
                good &= epi < YIELD_STRAIN_PI / 2
            return good and D * LIFE_FACTOR <= 1, D
        Ls = np.arange(0.8, 3.01, 0.05) * mm
        Lmin = next((L for L in Ls if ok(L)[0]), None)
        piv[f"t {t/um:g} um"] = dict(L_min_mm=None if Lmin is None else Lmin / mm,
                                     eps_pi_90=eps_pinned(90 * DEG, t, Lmin),
                                     miner_cu=ok(Lmin)[1])
    # ball pivot: Si3N4 ball in a conforming Ti-6Al-4V seat (R_seat = 1.05 R_ball)
    Rb = 0.15 * mm
    Rs = 1.05 * Rb
    Reff = Rb * Rs / (Rs - Rb)
    Estar = 1 / ((1 - 0.27 ** 2) / 310e9 + (1 - 0.34 ** 2) / 114e9)
    p0 = 1.6 * 880e6
    F_yield = np.pi ** 3 * p0 ** 3 * Reff ** 2 / (6 * Estar ** 2)
    F_user = 50.0       # [DECISION of this team] two-hand pull at full stretch, design overload
    piv["ball"] = dict(ball_d_mm=2 * Rb / mm, R_eff_mm=Reff / mm, F_first_yield_N=F_yield,
                       F_per_hinge_pull_y_N=F_user / NX_COLS, F_per_hinge_pull_x_N=F_user / NY,
                       margin=F_yield / (F_user / NX_COLS))
    # flat segment for the wrap in the pinned case (pivot plane = flat segment plane)
    piv["flat_pinned_strain_22p5"] = eps_pinned(A_TILE / (25.5 * mm), T_PI, 0.8 * mm)
    res["pivot_fix"] = piv

    # ---- Part D
    wrap, alpha, stiff, wag, sbend = wrap_analysis()
    res["wrap_R25p5"] = wrap
    res["wrap_R70"] = wrap_analysis(70 * mm)[0]
    res["gates"] = {
        "MEC-42 hinge PI, free chord, tension-free": verdict(fat["free, Cu offset 1.0 um"]["pass"]),
        "MEC-39 Cu trace, free chord, offset <= 1 um": verdict(fat["free, Cu offset 1.0 um"]["pass"]),
        "MEC-42 if the hinge is pinned (corner pivot), L 0.8": verdict(fat["pinned, Cu offset 0.0 um"]["pass"]),
        "MEC-42/39 ball pivot + longer ribbon (fix)": verdict(piv["t 12.5 um"]["L_min_mm"] is not None
                                                             and piv["ball"]["margin"] >= 2),
        "R 25.5 wrap, as-specified ribbon": verdict(wrap["min_over_alpha_strain"] < 0.01),
        "R 25.5 wrap, universal hinge fix": verdict(wrap["fix"]["flat_strain"] < 0.01
                                                    and wrap["fix"]["flat_inplane_strain_at_90"] < 0.01),
    }
    save("m2_hinge", res)

    # ---- plots
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for t in tlist:
        for L in (0.8 * mm, 1.6 * mm):
            ax[0].plot(phis / DEG, 100 * eps_free(phis, t, L), label=f"t {t/um:g} um, L {L/mm:g} mm")
    pin = [eps_pinned(p) for p in phis[::5]]
    ax[0].plot(phis[::5] / DEG, 100 * np.array(pin), "k--", label="t 12.5, L 0.8, pinned")
    ax[0].axhline(100 * YIELD_STRAIN_PI, color="r", ls=":", label="PI yield 3 %")
    ax[0].axvline(35, color="gray", ls=":"); ax[0].axvline(90, color="gray", ls=":")
    ax[0].set_xlabel("hinge turn 2theta deg"); ax[0].set_ylabel("PI outer strain %")
    ax[0].legend(fontsize=7); ax[0].grid(alpha=.3); ax[0].set_title("edge-on ribbon bending strain")
    ax[1].plot(alpha / DEG, 100 * (stiff), label="height-wise bending (stiff mode)")
    ax[1].plot(alpha / DEG, 100 * wag, label="twist edge fibre")
    ax[1].axhline(100 * sbend, color="g", ls="--", label="pivot-offset S-bend")
    ax[1].axhline(100 * wrap["fix"]["flat_strain"], color="k", lw=2, label="universal hinge, flat segment")
    ax[1].set_yscale("log"); ax[1].set_xlabel("ribbon axis angle to the wrap axis, deg")
    ax[1].set_ylabel("strain %"); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
    ax[1].set_title("R 25.5 mm wrap: 22.5 deg per row")
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m2_hinge.png", dpi=130); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    eps = np.logspace(-3.5, -1.3, 100)
    ax.loglog([n_cu(e) for e in eps], 100 * eps, label="Cu film, D=0.05")
    ax.loglog([n_cu(e, duct=0.3) for e in eps], 100 * eps, label="Cu RA foil, D=0.3")
    ax.loglog([n_pi(e) for e in eps], 100 * eps, label="PI, 0->max, Goodman")
    for name, ph in PHI_GATE.items():
        e = copper_strain(2 * base[name]["pinned"] / T_PI, 1 * um)[0]
        ax.plot(CYCLES[name] * LIFE_FACTOR, 100 * e, "ko")
        ax.annotate(name + "\nCu, 1 um offset, x10 life", (CYCLES[name] * LIFE_FACTOR, 100 * e), fontsize=7)
    ax.set_xlabel("cycles to failure"); ax.set_ylabel("strain range %"); ax.grid(alpha=.3, which="both")
    ax.legend(fontsize=8); ax.set_title("strain-life of the hinge materials")
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m2_fatigue.png", dpi=130); plt.close(fig)
    return res


if __name__ == "__main__":
    r = main()
    import json
    print(json.dumps(r["baseline"], indent=1, default=float))
    for k, v in r["fatigue"].items():
        print(k, {n: (round(v[n]["eps_cu"]*100, 3), round(v[n]["eps_pi"]*100, 3), f"{v[n]['N_cu']:.2e}", f"{v[n]['N_pi']:.2e}") for n in PHI_GATE}, "pass", v["pass"])
    print("tension", r["tension"])
    print("pivot", r["pivot_fix"])
    print("max offset", r["max_cu_offset_um_free"], r["max_cu_offset_um_pinned"], r["cu_life_vs_ductility_90deg"])
    print(json.dumps(r["wrap_R25p5"], indent=1, default=float))
    print(r["gates"])
