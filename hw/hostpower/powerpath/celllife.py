#!/usr/bin/env python3
"""celllife.py - question 3: cell life, cycled daily against host-fed at a storage SOC.

MODEL  Schmalstieg, Kaebitz, Ecker and Sauer, J. Power Sources 257 (2014) 325-334, a semi-empirical holistic
aging model fitted to the Sanyo UR18650E (NMC / graphite, 2.05 Ah). [PUBLICATION] The constants and the
equations below are taken from the table and Eq. 3 to 6 of Lee, Bjurek, Hagman, Li and Zou, "Vehicle-to-grid
optimization considering battery aging", IFAC-PapersOnLine 56(2) (2023) 6624-6629, doi 10.1016/j.ifacol.2023.10.362
(open full text at research.chalmers.se/publication/539723). The original paper was not open for reading here.

  C_lost = alpha(Vmean, theta) * T**0.75 + beta(Vrms, dDoD) * sqrt(Q)        (fraction of the first capacity)
  alpha  = (7.543e6 * Vmean - 23.75e6) * exp(-6976 / theta)                 T in days, theta in K
  beta   = 7.348e-3 * (Vrms - 3.667)**2 + 7.600e-4 + 4.081e-3 * dDoD         Q in Ah of throughput
  OCV(z) = 3.3324 + 2.1021 z - 5.8485 z**2 + 8.0326 z**3 - 3.4599 z**4       z = SOC, cell of 2.05 Ah

TRANSFER to the Leaf cell [HYPOTHESIS]: the micro cell is LiCoO2 at 4.45 V with a Si-C or graphite anode, not NMC at 4.2 V.
The model is applied by state of charge (the OCV polynomial above), and the throughput Q is the number of
equivalent full cycles times 2.05 Ah, so one cycle of the micro cell ages as one cycle of the 18650. Two uncertainties
are carried: a lognormal factor on alpha and on beta with a 10th to 90th percentile band of 2 times and 1/2, and an
extra high-voltage factor on the daily 100 % dwell of 1.0 to 2.0 times (4.45 V against 4.2 V).

Run:  python3 hw/hostpower/powerpath/celllife.py
Out:  out/celllife.json, out/celllife.txt, out/celllife.png
"""
import math

import numpy as np
from scipy.optimize import brentq

import common as C

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


E0, E1, E2 = 7.543e6, 23.75e6, 6976.0
Z0, Z1, Z2, Z3 = 7.348e-3, 3.667, 7.600e-4, 4.081e-3
G = [3.3324, 2.1021, -5.8485, 8.0326, -3.4599]
Q18650 = 2.05


def ocv_m(z):
    z = np.asarray(z, float)
    return G[0] + G[1] * z + G[2] * z ** 2 + G[3] * z ** 3 + G[4] * z ** 4


def alpha(v, th):
    return (E0 * v - E1) * math.exp(-E2 / th)


def beta(vrms, dod):
    return Z0 * (vrms - Z1) ** 2 + Z2 + Z3 * dod


def closs(T_days, efc_per_day, vmean, vrms, dod, th, fa=1.0, fb=1.0):
    q = efc_per_day * Q18650 * T_days
    return fa * alpha(vmean, th) * T_days ** 0.75 + fb * beta(vrms, dod) * math.sqrt(max(q, 0.0))


def years_to(frac, efc_per_day, vmean, vrms, dod, th, fa=1.0, fb=1.0):
    f = lambda T: closs(T, efc_per_day, vmean, vrms, dod, th, fa, fb) - frac
    if f(1e5) < 0:
        return float("inf"), float("inf")
    d = brentq(f, 1.0, 1e5)
    return d / 365.25, efc_per_day * d


def profile_stats(segments):
    """segments: list of (hours, z_start, z_end). Returns time-weighted mean V and rms V, with the model OCV."""
    tv, tv2, tt = 0.0, 0.0, 0.0
    for h, a, b in segments:
        z = np.linspace(a, b, 200)
        v = ocv_m(z)
        tv += h * v.mean()
        tv2 += h * (v ** 2).mean()
        tt += h
    return tv / tt, math.sqrt(tv2 / tt)


def main():
    p("POWER-PATH · question 3 · cell life, Schmalstieg 2014 model with the constants of Lee et al. 2023")
    p("alpha(3.7 V, 25 C) = %.3e per day^0.75 ; 365 d of storage at 3.7 V and 25 C loses %.2f %%"
      % (alpha(3.7, 298.15), 100 * alpha(3.7, 298.15) * 365 ** 0.75))
    p("model OCV at SOC 0, 0.5, 1: %.2f, %.2f, %.2f V (a 4.2 V cell)" % tuple(ocv_m([0, 0.5, 1.0])))
    p("")
    res = {"model": dict(E=[E0, E1, E2], Z=[Z0, Z1, Z2, Z3], ocv_poly=G, q18650_Ah=Q18650), "cases": {}}

    # ---------------------------------------------------------------- the profiles
    # A: cycled daily 100 -> 20: 6 h at 100 % overnight, 16 h discharge, 2 h charge
    prof_A = [(6, 1.0, 1.0), (16, 1.0, 0.2), (2, 0.2, 1.0)]
    # A2: cycled daily 100 -> 20, charged just before use: no dwell at 100 %
    prof_A2 = [(1, 1.0, 1.0), (21, 1.0, 0.2), (2, 0.2, 1.0)]
    # B: host-fed float at 50 % with shallow bridging
    prof_B = [(24, 0.5, 0.5)]
    cases = {}

    def add(name, prof, efc, dod, note):
        vm, vr = profile_stats(prof)
        cases[name] = dict(vmean=vm, vrms=vr, efc=efc, dod=dod, note=note)

    add("A  cycled daily 100 to 20 %, 6 h at 100 % overnight", prof_A, 0.8, 0.8, "0.8 equivalent cycles a day, depth 0.8")
    add("A2 cycled daily 100 to 20 %, no dwell at 100 %", prof_A2, 0.8, 0.8, "0.8 cycles a day, depth 0.8")

    # host-fed: bridging work per day. h hand-overs of tb minutes at P watts, shared by n cells.
    def bridging(n_cells, h, tb_min, P):
        e = h * P * tb_min / 60.0
        e_cells = n_cells * C.CELLS["S"]["E_target_Wh"]
        efc = e / e_cells
        dod = min(1.0, (P * tb_min / 60.0) / e_cells)
        return efc, dod

    for label, n, h, tb, P in (("B1 host-fed Full 128 cells, 6 hand-overs a day of 4 min at 2.24 W", 128, 6, 4, 2.242),
                               ("B2 host-fed Buffer 20 cells, 6 hand-overs a day of 4 min at 2.24 W", 20, 6, 4, 2.242),
                               ("B3 host-fed Buffer 20 cells, 2 hand-overs a day of 2 min at 2.24 W", 20, 2, 2, 2.242),
                               ("B4 host-fed Buffer 40 cells, 6 hand-overs a day of 4 min at 2.24 W", 40, 6, 4, 2.242)):
        efc, dod = bridging(n, h, tb, P)
        add(label, prof_B, efc, dod, "%.2f cycles a day at depth %.2f" % (efc, dod))
    # B at the top of the float band, 60 %, and at 40 %
    for z in (0.4, 0.6):
        efc, dod = bridging(128, 6, 4, 2.242)
        add("B1z%02d host-fed Full, float at %d %%" % (z * 100, z * 100), [(24, z, z)], efc, dod, "same bridging as B1")
    # C: the bad host-fed case: a host that holds the cell at 100 %
    efc, dod = bridging(128, 6, 4, 2.242)
    add("C  host-fed Full but charger holds 100 % (no float policy)", [(24, 1.0, 1.0)], efc, dod, "same bridging as B1")

    p("%-86s %6s %6s %6s %6s" % ("case", "Vmean", "Vrms", "EFC/d", "dDoD"))
    for k, c in cases.items():
        p("%-86s %6.3f %6.3f %6.3f %6.2f" % (k, c["vmean"], c["vrms"], c["efc"], c["dod"]))
    p("")

    # ---------------------------------------------------------------- years to 80 % capacity
    rng = np.random.default_rng(20261019)
    sig = math.log(2.0) / 1.2816
    N = 4000
    fa = np.exp(rng.normal(0, sig, N))
    fb = np.exp(rng.normal(0, sig, N))
    fhv = rng.uniform(1.0, 2.0, N)          # high-voltage factor on the 100 % dwell (4.45 V cell)
    ths = {"25 C": 298.15, "33 C": 306.15}
    p("YEARS to 80 %% capacity, base values and a Monte Carlo of %d draws (P10 / P50 / P90)" % N)
    p("%-86s %10s %10s | %24s" % ("case", "25 C", "33 C", "25 C P10 / P50 / P90"))
    table = {}
    for k, c in cases.items():
        row = {}
        for tn, th in ths.items():
            y, efc_end = years_to(0.2, c["efc"], c["vmean"], c["vrms"], c["dod"], th)
            row[tn] = dict(years=y, efc_at_end=efc_end)
        ys = []
        hv_case = k.startswith("A ") or k.startswith("C ")
        for i in range(N):
            f_a = fa[i] * (fhv[i] if hv_case else 1.0)
            f_b = fb[i] * (fhv[i] if hv_case else 1.0)
            y, _ = years_to(0.2, c["efc"], c["vmean"], c["vrms"], c["dod"], 298.15, f_a, f_b)
            ys.append(min(y, 99.0))
        q = np.percentile(ys, [10, 50, 90])
        row["mc25"] = dict(p10=q[0], p50=q[1], p90=q[2])
        table[k] = row
        p("%-86s %8.1f y %8.1f y | %6.1f %6.1f %6.1f" % (k, row["25 C"]["years"], row["33 C"]["years"], q[0], q[1], q[2]))
    res["cases"] = {k: dict(cases[k], **table[k]) for k in cases}
    p("  The high-voltage factor (1 to 2 times) applies to the cases A and C only. The 4000 draws use a fixed seed.")
    p("")

    # ---------------------------------------------------------------- ratio and the EU story
    a = table["A  cycled daily 100 to 20 %, 6 h at 100 % overnight"]["25 C"]["years"]
    b1 = table["B1 host-fed Full 128 cells, 6 hand-overs a day of 4 min at 2.24 W"]["25 C"]["years"]
    b2 = table["B2 host-fed Buffer 20 cells, 6 hand-overs a day of 4 min at 2.24 W"]["25 C"]["years"]
    p("RATIO at 25 C: host-fed Full lives %.1f times as long as the cycled cell (%.1f against %.1f years); host-fed Buffer 20 cells %.1f times (%.1f years)"
      % (b1 / a, b1, a, b2 / a, b2))
    res["ratio"] = dict(cycled_years=a, hostfed_full_years=b1, hostfed_buffer20_years=b2,
                        ratio_full=b1 / a, ratio_buffer20=b2 / a)
    # cycles to 80 % at full depth cycling, back to back, 2 and 6 cycles a day: the label of 2023/1670 counts these
    p("")
    p("CYCLES to 80 percent at depth 1.0 (the unit of Regulation (EU) 2023/1670: 800 cycles and 80 percent), model value, 25 C")
    eu = {}
    for per_day in (2.0, 6.0):
        vm, vr = profile_stats([(1, 1.0, 0.0), (1, 0.0, 1.0)])
        y, efc = years_to(0.2, per_day, vm, vr, 1.0, 298.15)
        eu["%g per day" % per_day] = dict(cycles=efc, years=y)
        p("  %4.1f cycles a day: %5.0f full cycles to 80 %% (%.1f years); against the 800 cycles of 2023/1670: %s"
          % (per_day, efc, y, "meets" if efc >= 800 else "misses"))
    res["eu_cycles"] = eu
    p("  The model is fitted to a 2013 NMC cell. A micro cell result of 800 cycles needs its own test, gate HST-5.")
    p("  The Leaf is not named a phone or a tablet. Whether 2023/1670 applies is a legal reading of hw/energy/06. [HYPOTHESIS]")
    p("")

    # ---------------------------------------------------------------- the lithium and cobalt mass
    F = 96485.0
    M_LI, M_CO, LCE = 6.94, 58.93, 5.323
    util = 0.66       # fraction of the LiCoO2 lithium that cycles at a 4.45 V cut-off, 180 of 274 mAh/g [GENERAL]
    p("LITHIUM AND COBALT in the cells, by stoichiometry [GENERAL]: Faraday's law, %.0f %% of the LiCoO2 lithium cycles at 4.45 V" % (100 * util))
    li_cell, co_cell = {}, {}
    for v in ("G", "S"):
        e = C.CELLS[v]["E_target_Wh"]
        q_ah = C.cell_q_Ah(e)
        n_li = q_ah * 3600.0 / F / util
        li_mg = n_li * M_LI * 1000.0 + 0.07          # plus 0.07 mg of LiPF6 lithium in the electrolyte [H]
        co_mg = n_li * M_CO * 1000.0
        li_cell[v], co_cell[v] = li_mg, co_mg
        p("  cell %s: %.1f mAh -> %.2f mg Li (%.0f mg Li2CO3 equivalent) and %.0f mg Co in the cathode" % (v, 1000 * q_ah, li_mg, li_mg * LCE, co_mg))
    li = {}
    for name, n in (("Full 128", 128), ("Buffer 20", 20), ("Buffer 40", 40), ("Buffer 52", 52), ("Bare 0", 0)):
        li[name] = dict(n=n, Li_g=n * li_cell["S"] / 1000.0, LCE_g=n * li_cell["S"] * LCE / 1000.0, Co_g=n * co_cell["S"] / 1000.0,
                        Li_saved_g=(128 - n) * li_cell["S"] / 1000.0, LCE_saved_g=(128 - n) * li_cell["S"] * LCE / 1000.0,
                        Co_saved_g=(128 - n) * co_cell["S"] / 1000.0)
        p("  %-10s Li %.3f g, Li2CO3 equivalent %.2f g, Co %.2f g | saved against Full: Li %.3f g, Li2CO3 %.2f g, Co %.2f g"
          % (name, li[name]["Li_g"], li[name]["LCE_g"], li[name]["Co_g"], li[name]["Li_saved_g"], li[name]["LCE_saved_g"], li[name]["Co_saved_g"]))
    res["lithium"] = li
    p("  per million units, Buffer 20 saves %.0f kg of Li (%.1f t of Li2CO3) and %.1f t of cobalt"
      % (li["Buffer 20"]["Li_saved_g"] * 1e3, li["Buffer 20"]["LCE_saved_g"], li["Buffer 20"]["Co_saved_g"]))
    p("")
    C.dump("celllife", res, LINES)
    plots(cases)


def plots(cases):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    days = np.linspace(1, 365.25 * 15, 600)
    pick = [("A  cycled daily 100 to 20 %, 6 h at 100 % overnight", "cycled daily 100 to 20 %"),
            ("B1 host-fed Full 128 cells, 6 hand-overs a day of 4 min at 2.24 W", "host-fed, Full tier"),
            ("B2 host-fed Buffer 20 cells, 6 hand-overs a day of 4 min at 2.24 W", "host-fed, Buffer 20 cells"),
            ("C  host-fed Full but charger holds 100 % (no float policy)", "host-fed, held at 100 %")]
    for i, (k, lab) in enumerate(pick):
        c = cases[k]
        y = [100 * (1 - closs(d, c["efc"], c["vmean"], c["vrms"], c["dod"], 298.15)) for d in days]
        ax[0].plot(days / 365.25, y, color=C.PAL[i], lw=1.8, label=lab)
    ax[0].axhline(80, color="#444", lw=1, ls=":")
    ax[0].set_ylim(50, 100)
    C.style(ax[0], "years", "capacity, %", "Schmalstieg model at 25 C")
    ax[0].legend(fontsize=8, frameon=False)
    # right: years to 80 % against temperature for A and B1
    ths = np.arange(15, 41, 1.0)
    for i, (k, lab) in enumerate(pick[:2]):
        c = cases[k]
        ys = [min(years_to(0.2, c["efc"], c["vmean"], c["vrms"], c["dod"], 273.15 + t)[0], 60) for t in ths]
        ax[1].plot(ths, ys, color=C.PAL[i], lw=1.8, label=lab)
    ax[1].set_yscale("log")
    ax[1].axvline(36.2, color="#444", lw=1, ls=":")
    ax[1].text(36.0, 1.2, "skin limit 36.2 C", rotation=90, fontsize=8, ha="right")
    C.style(ax[1], "cell temperature, C", "years to 80 %", "Life against temperature")
    ax[1].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(C.OUT + "/celllife.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
