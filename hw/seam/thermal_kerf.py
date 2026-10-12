#!/usr/bin/env python3
"""thermal_kerf.py - the thermal budget of the seam, -10..+50 C.  Gate MEC-40.

Deliverable 3 of the seam team.
  1. A general n-layer laminate solver (classical lamination, equi-biaxial). It
     is validated against the Timoshenko bimetal formula [PUBLICATION]
     S. Timoshenko, J. Opt. Soc. Am. 11, 233 (1925).
  2. The curl of the symmetric glass / micro-LED / glass stack, nominal and at
     its thickness tolerance.
  3. The curl of the PC cap on the glass stack: a rigid bond (Timoshenko), and
     the real bond through a soft OCA (Suhir shear-lag model [PUBLICATION]
     E. Suhir, J. Appl. Mech. 53, 657 (1986)), for a silicone and an acrylic OCA.
  4. The PC cap kerf and the glass carrier gap from -10 to +50 C.
  5. The Z-step budget at a uniform temperature, and its sensitivity to a
     temperature difference across the seam.
"""
import json
import math
import os
import numpy as np
import seam_params as P


def Ep(mat):
    E, nu = P.MAT[mat][:2]
    return E / (1 - nu)


def laminate(layers, dT):
    """layers: [(mat, t_m, alpha_override or None)] from the top. Returns kappa (1/m), eps0, D."""
    z = 0.0
    A = B = Dm = NT = MT = 0.0
    for mat, t, a in layers:
        E = Ep(mat)
        al = P.MAT[mat][2] if a is None else a
        z1, z2 = z, z + t
        A += E * t
        B += E * (z2 ** 2 - z1 ** 2) / 2
        Dm += E * (z2 ** 3 - z1 ** 3) / 3
        NT += E * al * dT * t
        MT += E * al * dT * (z2 ** 2 - z1 ** 2) / 2
        z = z2
    M = np.array([[A, B], [B, Dm]])
    eps0, kap = np.linalg.solve(M, [NT, MT])
    D_eff = Dm - B * B / A
    return kap, eps0, D_eff, A, NT / (A * dT) if dT else 0.0


def timoshenko(t1, t2, E1, E2, da, dT):
    m, n = t1 / t2, E1 / E2
    h = t1 + t2
    return 6 * da * dT * (1 + m) ** 2 / (h * (3 * (1 + m) ** 2 + (1 + m * n) * (m * m + 1 / (m * n))))


def glg(top=0.10e-3, led=0.05e-3, bot=0.10e-3):
    return [("glass", top, None), ("LEDlayer", led, None), ("glass", bot, None)]


def suhir(G, dT, half=P.TILE_mm / 2 * 1e-3, h0=0.05e-3, nx=400):
    """PC cap on the glass stack through an OCA of shear modulus G (per unit width)."""
    t1 = 0.25e-3
    E1 = Ep("PC")
    kap2, _, D2, A2, a2 = laminate(glg(), 1.0)
    t2 = 0.25e-3
    E2t2 = A2
    D1 = E1 * t1 ** 3 / 12
    D = D1 + D2
    d = t1 / 2 + h0 + t2 / 2
    lam = 1 / (E1 * t1) + 1 / E2t2 + d * d / D
    G1 = P.MAT["PC"][0] / (2 * (1 + P.MAT["PC"][1]))
    kap_i = h0 / G + t1 / (3 * G1) + t2 / (3 * 30e9)
    k = math.sqrt(lam / kap_i)
    da = P.MAT["PC"][2] - a2
    x = np.linspace(0, half, nx)
    T = da * dT / lam * (1 - np.cosh(k * x) / np.cosh(k * half))
    curv = d * T / D
    slope = np.concatenate([[0], np.cumsum((curv[1:] + curv[:-1]) / 2 * np.diff(x))])
    w = np.concatenate([[0], np.cumsum((slope[1:] + slope[:-1]) / 2 * np.diff(x))])
    u_rel = da * dT * math.tanh(k * half) / k
    rigid_k = d * da * dT / (lam * D)
    return dict(k_per_mm=k * 1e-3, kl=k * half, edge_slope=slope[-1], edge_lift=w[-1],
                u_rel=u_rel, curv_centre=curv[0], curv_rigid=rigid_k, x=x, w=w)


def g_acrylic(T):
    return max(0.03e6, 0.10e6 * 10 ** ((P.T_REF_C - T) / 25.0))


def main():
    res = {}
    dT40 = 40.0
    # ---- 1. validation: 2-layer laminate equals Timoshenko
    lay = [("PC", 0.25e-3, None), ("glass", 0.25e-3, None)]
    k_clt = laminate(lay, dT40)[0]
    k_tim = timoshenko(0.25e-3, 0.25e-3, Ep("PC"), Ep("glass"),
                       P.MAT["PC"][2] - P.MAT["glass"][2], dT40)
    res["validation"] = dict(clt=abs(k_clt), timoshenko=k_tim, rel_err=abs(abs(k_clt) - k_tim) / k_tim)
    print(f"validation, PC 0.25 on glass 0.25, 40 K: CLT {abs(k_clt):.4f} 1/m, Timoshenko {k_tim:.4f} 1/m")
    L40 = 40e-3
    cant = abs(k_clt) * L40 ** 2 / 2
    res["final21_claim_40mm"] = dict(cantilever_mm=cant * 1e3, centre_sag_mm=abs(k_clt) * L40 ** 2 / 8 * 1e3)
    print(f"rigid PC on glass over 40 mm: {cant*1e3:.2f} mm end lift as a cantilever "
          f"(FINAL/21 says about 1.8 mm), {abs(k_clt)*L40**2/8*1e3:.2f} mm centre sag")

    # ---- 2. symmetric glass / LED / glass
    rows = {}
    for name, (tt, ll, bb) in {"nominal 0.100/0.050/0.100": (0.100, 0.05, 0.100),
                               "tolerance 0.095/0.050/0.105": (0.095, 0.05, 0.105),
                               "tolerance 0.105/0.050/0.095": (0.105, 0.05, 0.095)}.items():
        for dT in (P.T_MIN_C - P.T_REF_C, P.T_MAX_C - P.T_REF_C):
            k = laminate(glg(tt * 1e-3, ll * 1e-3, bb * 1e-3), dT)[0]
            lift = k * (P.TILE_mm / 2 * 1e-3) ** 2 / 2
            rows[f"{name} dT {dT:+.0f}"] = dict(kappa=k, edge_lift_nm=lift * 1e9,
                                                 edge_slope_urad=k * P.TILE_mm / 2 * 1e-3 * 1e6)
            print(f"GLG {name:28s} dT {dT:+5.0f} K: kappa {k:+.2e} 1/m, tile edge lift {lift*1e9:+7.2f} nm, "
                  f"edge slope {k*5e-3*1e6:+6.2f} urad")
    res["glg"] = rows

    # ---- 3. PC cap on the glass stack through the OCA
    oca = {}
    for label, Gfun in (("silicone OCA", lambda T: P.SIL_OCA_G), ("acrylic OCA", g_acrylic)):
        for T in (P.T_MIN_C, P.T_MAX_C):
            dT = T - P.T_REF_C
            s = suhir(Gfun(T), dT)
            oca[f"{label} {T:+.0f} C"] = dict(G_MPa=Gfun(T) / 1e6, kl=s["kl"],
                                               edge_slope_urad=s["edge_slope"] * 1e6,
                                               edge_lift_nm=s["edge_lift"] * 1e9,
                                               u_rel_um=s["u_rel"] * 1e6,
                                               curl_ratio=s["curv_centre"] / s["curv_rigid"])
            print(f"{label:13s} {T:+4.0f} C: G {Gfun(T)/1e6:5.2f} MPa, k*l {s['kl']:5.2f}, cap edge slip "
                  f"{s['u_rel']*1e6:+6.2f} um, tile edge lift {s['edge_lift']*1e9:+8.1f} nm, "
                  f"edge slope {s['edge_slope']*1e6:+7.1f} urad, curl {s['curv_centre']/s['curv_rigid']*100:4.1f} % of rigid")
    res["cap_on_glass"] = oca

    # ---- 4. kerf of the PC cap and the glass gap
    kerf = {}
    for label, Gfun in (("silicone OCA", lambda T: P.SIL_OCA_G), ("acrylic OCA", g_acrylic),
                        ("free cap (bound)", None)):
        def urel(T):
            dT = T - P.T_REF_C
            if Gfun is None:
                return (P.MAT["PC"][2] - P.MAT["glass"][2]) * dT * P.TILE_mm / 2 * 1e-3
            return suhir(Gfun(T), dT)["u_rel"]
        k_ref = 10e-6 + 2 * urel(P.T_MAX_C)            # 10 um at +50 C
        k_m10 = k_ref - 2 * urel(P.T_MIN_C)
        kerf[label] = dict(kerf_ref_um=k_ref * 1e6, kerf_50_um=10.0, kerf_m10_um=k_m10 * 1e6)
        print(f"cap kerf, {label:16s}: {10.0:.1f} um at +50 C, {k_ref*1e6:.1f} um at 23 C, {k_m10*1e6:.1f} um at -10 C")
    res["kerf"] = kerf
    res["final21_kerf_note"] = ("FINAL/21 gives 37 um at -10 C. Over 60 K the cap grows 37 um against "
                                "the glass, so the kerf is 10 + 37 = 47 um when the cap is free.")
    # glass gap: the chain edge pixel - glass - insert - ball - vee - insert - glass - edge pixel
    chain = [("glass", 0.30e-3), ("WC-Ni", 0.35e-3), ("Si3N4", 0.25e-3)]
    dgap = sum((P.MAT[m][2] - P.MAT["glass"][2]) * L for m, L in chain) * 2 * (P.T_MAX_C - P.T_MIN_C)
    res["glass_gap_change_um"] = dgap * 1e6
    print(f"glass carrier gap change -10..+50 C across the seat chain: {dgap*1e6:.3f} um "
          f"(pitch {40+P.GLASS_GAP_NOM_um:.1f} um stays inside 50.0 um)")

    # ---- 5. Z-step budget at uniform temperature, and the cross-seam gradient
    def aeff(mat, constrained=True):
        a, nu = P.MAT[mat][2], P.MAT[mat][1]
        return a * (1 + nu) / (1 - nu) if constrained else a
    seg = [("PC", 0.25e-3, 0.38), ("OCA", 0.05e-3, 0.49), ("glass", 0.25e-3, 0.22),
           ("slipOCA", 0.03e-3, 0.49), ("coil", 0.27e-3, 0.34)]
    alpha = {"PC": 65e-6, "OCA": P.SIL_OCA_ALPHA, "glass": 3.2e-6, "slipOCA": P.SIL_OCA_ALPHA, "coil": 20e-6}
    dz_per_K = sum(t * alpha[m] * (1 + nu) / (1 - nu) for m, t, nu in seg)
    res["z_per_K_nm"] = dz_per_K * 1e9
    gradient_limit = 1e-6 / dz_per_K
    # tolerance-driven differential at uniform temperature
    tol = {"PC": 5e-6, "OCA": 3e-6, "glass": 3e-6, "slipOCA": 2e-6, "coil": 3e-6}
    dT_max = max(P.T_MAX_C - P.T_REF_C, P.T_REF_C - P.T_MIN_C)
    thick_tol = sum(tol[m] * alpha[m] * (1 + nu) / (1 - nu) for m, t, nu in seg) * dT_max
    rep = json.load(open("results/kinematic_seat.json"))["repeat"]["p999_dz_um"] * 1e-6
    budget = {
        "seat repeat, 99.9 % [kinematic_seat.py]": rep,
        "face-referenced ball and vee setting, two sides RSS": math.hypot(0.14e-6, 0.14e-6),
        "layer thickness tolerance x CTE, worst case": thick_tol,
        "bond line +-2 um x 60 ppm/K": 2e-6 * 60e-6 * dT_max * 2,
        "tile-to-tile curl difference at the edge pixel (20 um lever)":
            abs(rows["tolerance 0.095/0.050/0.105 dT -33"]["edge_slope_urad"]) * 1e-6 * 20e-6 * 2,
        "preload change and wear (symmetric vee, zero in z)": 0.0,
    }
    total_wc = sum(budget.values())
    total_rss = math.sqrt(sum(v * v for v in budget.values()))
    res["zstep_budget_um"] = {k: v * 1e6 for k, v in budget.items()}
    res["zstep_total_worst_um"] = total_wc * 1e6
    res["zstep_total_rss_um"] = total_rss * 1e6
    res["zstep_gradient_nm_per_K"] = dz_per_K * 1e9
    res["zstep_gradient_limit_K"] = gradient_limit
    print("Z-step budget at a uniform temperature, -10..+50 C:")
    for k, v in budget.items():
        print(f"   {v*1e6:7.3f} um  {k}")
    print(f"   total {total_wc*1e6:.3f} um worst case, {total_rss*1e6:.3f} um RSS -> MEC-40 step < 1 um: "
          f"{'PASS' if total_wc < 1e-6 else 'FAIL'}")
    print(f"cross-seam gradient: {dz_per_K*1e9:.0f} nm/K, so a step of 1 um needs {gradient_limit:.1f} K across the seam")
    res["gate_MEC40_step_pass"] = bool(total_wc < 1e-6)

    # ---- plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        Ts = np.linspace(P.T_MIN_C, P.T_MAX_C, 61)
        fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
        for label, Gfun, c in (("silicone OCA", lambda T: P.SIL_OCA_G, "#2a6fdb"),
                               ("acrylic OCA", g_acrylic, "#d9822b")):
            k_ref = 10 + 2 * suhir(Gfun(P.T_MAX_C), P.T_MAX_C - P.T_REF_C)["u_rel"] * 1e6
            kerfs = [k_ref - 2 * suhir(Gfun(T), T - P.T_REF_C)["u_rel"] * 1e6 for T in Ts]
            slopes = [suhir(Gfun(T), T - P.T_REF_C)["edge_slope"] * 2e6 for T in Ts]
            ax[0].plot(Ts, kerfs, color=c, label=label)
            ax[1].plot(Ts, slopes, color=c, label=label)
        ax[0].axhline(50, color="#888", ls="--", lw=1)
        ax[0].text(-9, 51, "50 um: the dark-line limit", fontsize=8, color="#555")
        ax[0].set_xlabel("temperature (C)"); ax[0].set_ylabel("PC cap kerf (um)")
        ax[0].set_title("cap kerf, 10 um at +50 C"); ax[0].legend(fontsize=8, frameon=False)
        ax[1].set_xlabel("temperature (C)"); ax[1].set_ylabel("slope kink at a seam (urad)")
        ax[1].set_title("curl kink, two tiles"); ax[1].legend(fontsize=8, frameon=False)
        names = list(budget.keys())
        short = ["seat repeat", "ball/vee setting", "thickness x CTE", "bond line", "curl diff", "preload, wear"]
        ax[2].barh(short, [budget[n] * 1e6 for n in names], color="#2a6fdb")
        ax[2].axvline(1.0, color="#c0392b", ls="--", lw=1)
        ax[2].set_xlabel("Z-step contribution (um)"); ax[2].set_title(f"MEC-40 step: {total_wc*1e6:.2f} um of 1 um")
        for a in ax:
            for s in ("top", "right"):
                a.spines[s].set_visible(False)
        fig.tight_layout()
        fig.savefig("drawings/S04-thermal-kerf-curl-zstep.svg")
        plt.close(fig)
    except ImportError:
        pass
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/thermal_kerf.json", "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    main()
