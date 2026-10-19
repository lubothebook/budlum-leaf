#!/usr/bin/env python3
"""tiers.py - question 1: the energy tiers Bare, Buffer and Full.

For every hand-over gap (0.1 s .. 30 min) and every load of hw/energy/04 it finds:
  Buffer  the least number of the 128 micro cells that ride the gap, by a time-stepped
          constant-power discharge with the cell DCIR, the 3.40 V seat floor and a C-rate cap;
  Full    the time all 128 cells carry the load;
  Bare    the least volume of a capacitor store (EDLC, lithium-ion capacitor, thin solid-state cell),
          by a constant-power discharge through the ESR and a converter, and whether it fits
          in the 0.24 mm routing margin of the tile stack.

Run:  python3 hw/hostpower/powerpath/tiers.py
Out:  out/tiers.json, out/tiers.txt, out/tiers_buffer.png, out/tiers_bare.png
"""
import math

import numpy as np

import common as C

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


# ------------------------------------------------------------------ assumptions
CMAX = 3.0            # C, discharge cap of the micro cell. The pack charges at 2.9 to 3.5 C (hw/energy/04) [H]
V_FLOOR = 3.40        # V, seat floor for the display classes [D] hw/energy/03
SOC_FLOOR = 0.10      # reserve kept for the safe end of a session and the island [D] this team
SOC_FLOAT = 0.60      # top of the 40 to 60 % storage float [D] this team
ETA_CONV = 0.90       # supercapacitor backup converter [H]


# ------------------------------------------------------------------ Buffer: cells
def cell_run(n, P, E_cell_Wh, dcir, soc0, t_goal, soc_floor=SOC_FLOOR, vfloor=V_FLOOR, cmax=None):
    cmax = CMAX if cmax is None else cmax
    """Constant power P (W at VBUS) from n parallel cells. Returns (seconds_carried, stop_reason).
    Stops at t_goal. The stop reasons are: ok, energy (soc floor), voltage (seat floor), current (C-rate)."""
    q_ah = n * C.cell_q_Ah(E_cell_Wh)
    soc, t = soc0, 0.0
    dt = max(1e-3, min(t_goal / 3000.0, 1.0))
    while t < t_goal:
        v0 = float(C.ocv(soc))
        r = dcir * C.r_factor(soc) / n
        disc = v0 * v0 - 4.0 * r * P
        if disc < 0:
            return t, "voltage"
        i = (v0 - math.sqrt(disc)) / (2.0 * r)
        vt = v0 - i * r
        if vt < vfloor:
            return t, "voltage"
        if i / q_ah > cmax:
            return t, "current"
        if soc <= soc_floor:
            return t, "energy"
        step = min(dt, t_goal - t)
        soc -= i * step / (3600.0 * q_ah)
        t += step
    return t_goal, "ok"


def min_cells(P, t, E_cell_Wh, dcir, soc0, vfloor):
    for n in range(1, C.N_TILES + 1):
        sec, why = cell_run(n, P, E_cell_Wh, dcir, soc0, t, vfloor=vfloor)
        if why == "ok":
            if n == 1:
                return n, "none"
            _, why_prev = cell_run(n - 1, P, E_cell_Wh, dcir, soc0, t, vfloor=vfloor)
            return n, why_prev
    return None, "more than 128"


def full_hours(P, E_cell_Wh, dcir, soc0, vfloor):
    sec, _ = cell_run(C.N_TILES, P, E_cell_Wh, dcir, soc0, 40 * 3600.0, vfloor=vfloor)
    return sec / 3600.0


# ------------------------------------------------------------------ Bare: capacitor stores
# Published inputs, each derived from a datasheet figure. C_cm3 in F/cm3 of the package, k in ohm.cm3
# (ESR times package volume, so a store of V cm3 has ESR k / V). rho in g/cm3 [H].
TECH = {
    "EDLC, large cell (Maxwell BCAP3000)": dict(
        C_cm3=3000.0 / 476.0, vmax=2.7, vmin=1.35, k=0.23e-3 * 476.0, rho=1.0, t_min_mm=60.4,
        tag="[PUBLICATION] Maxwell BCAP3000 P270 datasheet 3003279-EN.3: 3000 F min, 2.7 V, 0.23 mOhm max, 475 g, "
            "diameter 60.4 mm by about 166 mm, volume 0.476 L from the product matrix. Vmin 1.35 V is the converter cut [HYPOTHESIS]"),
    "EDLC, thin chip (Seiko CPH3225A)": dict(
        C_cm3=0.011 / (3.2 * 2.5 * 0.9e-3), vmax=3.3, vmin=1.65, k=160.0 * (3.2 * 2.5 * 0.9e-3), rho=1.2, t_min_mm=0.9,
        tag="[PUBLICATION] Seiko CPH3225A: 11 mF, 3.3 V, 3.2 x 2.5 x 0.9 mm. The 160 ohm ESR comes from a distributor "
            "listing and is unconfirmed [HYPOTHESIS]"),
    "lithium-ion capacitor (Taiyo Yuden LIC1030RS3R8206)": dict(
        C_cm3=20.0 / (math.pi * 5.0 ** 2 * 30.0 / 1000.0), vmax=3.8, vmin=2.2,
        k=4.0 * (math.pi * 5.0 ** 2 * 30.0 / 1000.0), rho=1.6, t_min_mm=10.0,
        tag="[PUBLICATION] Taiyo Yuden LIC1030RS3R8206: 20 F, 3.8 V upper limit, 2.2 V lower limit, 10 mm diameter by 30 mm, "
            "internal resistance 4000 mOhm max (device sheet, non-preferred status)"),
    "thin solid-state cell (ST EFL700A39)": dict(
        C_cm3=(0.7e-3 * 3600.0 / (4.2 - 3.6)) / (25.4 * 25.4 * 0.2e-3), vmax=4.2, vmin=3.6,
        k=120.0 * (25.4 * 25.4 * 0.2e-3), rho=2.0, t_min_mm=0.2,
        tag="[PUBLICATION] ST EnFilm EFL700A39 (DocID 17370): 0.7 mAh, 3.9 V nominal, 3.6 to 4.2 V, 25.4 x 25.4 x 0.2 mm, "
            "Rint 100 to 120 ohm, 10 mA pulse (100 ms on, 900 ms off), 5 mA continuous. The cell is treated as a "
            "linear capacitor over 3.6 to 4.2 V [HYPOTHESIS]"),
}
for _k, _t in TECH.items():
    _t["wh_l_usable"] = 0.5 * _t["C_cm3"] * (_t["vmax"] ** 2 - _t["vmin"] ** 2) / 3600.0 * 1000.0
    _t["wh_l_full"] = 0.5 * _t["C_cm3"] * _t["vmax"] ** 2 / 3600.0 * 1000.0


def cap_run(vol, t, P, eta=ETA_CONV, t_goal=None):
    """Constant power P (W out of the converter) from a store of vol cm3. Seconds carried."""
    c = t["C_cm3"] * vol
    esr = t["k"] / vol
    pin = P / eta
    v = t["vmax"]
    tt = 0.0
    t_goal = t_goal if t_goal is not None else 1e9
    while tt < t_goal:
        disc = v * v - 4.0 * esr * pin
        if disc < 0:
            return tt
        i = (v - math.sqrt(disc)) / (2.0 * esr)
        vt = v - i * esr
        if vt < t["vmin"]:
            return tt
        # adaptive step: 0.2 % of the energy-limited time or the RC time constant
        dt = max(1e-4, min(0.002 * 0.5 * c * v * v / max(pin, 1e-9), 2.0, esr * c * 0.2 if esr * c > 0 else 1.0))
        dt = min(dt, t_goal - tt)
        v -= i * dt / c
        tt += dt
    return t_goal


def cap_min_volume(t, P, gap):
    lo, hi = 1e-6, 1e5
    if cap_run(hi, t, P, t_goal=gap) < gap:
        return None
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if cap_run(mid, t, P, t_goal=gap) >= gap:
            hi = mid
        else:
            lo = mid
    return hi


def margin_volume(t_margin_mm, fill):
    return C.BODY_AREA_MM2 * fill * t_margin_mm / 1000.0       # cm3


def main():
    global CMAX
    res = {"assumptions": dict(CMAX=CMAX, V_FLOOR=V_FLOOR, SOC_FLOOR=SOC_FLOOR, SOC_FLOAT=SOC_FLOAT,
                               ETA_CONV=ETA_CONV, note="loads are W at the cells (VBUS)"),
           "buffer": {}, "bare": {}, "full": {}, "tech": {}, "saving": {}}
    p("POWER-PATH · question 1 · tiers Bare, Buffer, Full")
    p("loads (W at VBUS): " + ", ".join("%s %.3f" % kv for kv in C.LOADS.items()))
    p("assumptions: C-rate cap %.1f C [H], seat floor %.2f V [D], SOC reserve %.0f %%, storage float top %.0f %%, converter %.2f [H]"
      % (CMAX, V_FLOOR, 100 * SOC_FLOOR, 100 * SOC_FLOAT, ETA_CONV))
    p("")

    # ------------------------------------------------ the cell numbers
    for v in ("G", "S"):
        c = C.CELLS[v]
        swing = C.e_frac(SOC_FLOOR, SOC_FLOAT)
        swing100 = C.e_frac(SOC_FLOOR, 1.0)
        p("cell %s at the target density: %.4f Wh, %.2f mAh, DCIR %.2f ohm, %.3f g. Usable swing: float %.0f to %.0f %% = %.3f of the energy, "
          "topped 100 to %.0f %% = %.3f" % (v, c["E_target_Wh"], 1000 * C.cell_q_Ah(c["E_target_Wh"]), c["dcir"],
                                            c["mass_g"], 100 * SOC_FLOAT, 100 * SOC_FLOOR, swing, 100 * SOC_FLOOR, swing100))
        res["buffer"].setdefault("cell_" + v, dict(E_Wh=c["E_target_Wh"], swing_float=swing, swing_topped=swing100))
    p("")

    # ------------------------------------------------ Buffer and Full
    p("BUFFER: least number n of the 128 cells, by time-stepped discharge (S cell, 750 Wh/L target)")
    for tag, soc0 in (("floated at 60 %", SOC_FLOAT), ("topped to 100 %", 1.0)):
        for v in ("S", "G"):
            c = C.CELLS[v]
            hdr = "  %-4s %-16s" % (v, tag) + "".join("%9s" % g for g, _ in C.GAPS)
            p(hdr)
            tbl = {}
            for ln, P in C.LOADS.items():
                row = []
                vf = V_FLOOR if P > 0.1 else 3.0
                for gn, gs in C.GAPS:
                    n, why = min_cells(P, gs, c["E_target_Wh"], c["dcir"], soc0, vf)
                    row.append((n, why))
                    tbl.setdefault(ln, {})[gn] = dict(n=n, limit=why,
                                                      E_need_Wh=P * gs / 3600.0,
                                                      E_cells_nominal_Wh=None if n is None else n * c["E_target_Wh"],
                                                      mass_g=None if n is None else n * c["mass_g"])
                p("  %-21s" % ln + "".join("%9s" % ("-" if n is None else "%d%s" % (n, {"energy": "e", "current": "i", "voltage": "v", "none": "", "more than 128": "x"}.get(w, ""))) for n, w in row))
            res["buffer"].setdefault("tables", {})["%s %s" % (v, tag)] = tbl
            p("  (e energy limit, i C-rate limit, v voltage or seat floor limit, x more than 128 cells)")
            p("")

    # quadrant-swap-safe count: the other three quadrants must carry the load
    p("BUFFER with the quadrant swap: cells spread over four quadrants, one removed, three carry the 3 s swap")
    swap = {}
    for ln, P in C.LOADS.items():
        c = C.CELLS["S"]
        vf = V_FLOOR if P > 0.1 else 3.0
        n3, why = min_cells(P, 3.0, c["E_target_Wh"], c["dcir"], SOC_FLOAT, vf)
        tot = None if n3 is None else int(4 * math.ceil(n3 * 4.0 / 3.0 / 4.0))
        swap[ln] = dict(n_three_quadrants=n3, n_total=tot)
        p("  %-14s 3 s on three quadrants needs %s cells, so %s cells in total (a multiple of 4)" % (ln, n3, tot))
    res["buffer"]["swap_3s"] = swap
    p("")

    # Buffer sizes of the BRIEF
    for e in (0.3, 1.5):
        for v in ("G", "S"):
            n = math.ceil(e / C.CELLS[v]["E_target_Wh"])
            p("BRIEF Buffer %.1f Wh nominal is %d %s cells, %.1f g, %.0f %% of the 128" % (e, n, v, n * C.CELLS[v]["mass_g"], 100 * n / 128))
            res["buffer"].setdefault("brief_range", {})["%.1f Wh %s" % (e, v)] = dict(n=n, mass_g=n * C.CELLS[v]["mass_g"])
    p("")

    p("FULL: hours that all 128 cells carry each load, S target and G target (from 100 % to the 10 % reserve; from the 60 % float)")
    for ln, P in C.LOADS.items():
        vf = V_FLOOR if P > 0.1 else 3.0
        row = {}
        for v in ("G", "S"):
            c = C.CELLS[v]
            row[v + "_100"] = full_hours(P, c["E_target_Wh"], c["dcir"], 1.0, vf)
            row[v + "_60"] = full_hours(P, c["E_target_Wh"], c["dcir"], SOC_FLOAT, vf)
        res["full"][ln] = row
        p("  %-14s G %6.2f h (%5.2f h from 60 %%)   S %6.2f h (%5.2f h from 60 %%)" % (ln, row["G_100"], row["G_60"], row["S_100"], row["S_60"]))
    p("")

    # ------------------------------------------------ Bare
    p("BARE: capacitor technologies from published figures")
    for k, t in TECH.items():
        p("  %-52s %6.1f Wh/L usable, %6.1f Wh/L at full voltage, ESR x volume %.3g ohm.cm3, thinnest part %.2f mm" %
          (k, t["wh_l_usable"], t["wh_l_full"], t["k"], t["t_min_mm"]))
        p("      " + t["tag"])
        res["tech"][k] = {kk: vv for kk, vv in t.items()}
    p("  micro cell at 750 Wh/L and 850 Wh/L for scale: the capacitor store is 40 to 130 times less dense")
    p("")

    margins = {"0.24 mm, all of the margin": 0.24, "0.12 mm, half": 0.12, "0.04 mm, after the 0.20 mm coil (FINAL/21 21.2.6 item 4)": 0.04}
    fill = 0.5
    p("room for a Bare store: %.0f %% of the %.0f mm2 of the body (hinge corners, magnets and coil keep the rest) [H]" % (100 * fill, C.BODY_AREA_MM2))
    for mk, mm in margins.items():
        p("  margin %-62s %.3f cm3" % (mk, margin_volume(mm, fill)))
    p("")

    p("BARE minimum volume in cm3 (store behind a %.2f converter). 'x' means no volume carries the load, because the ESR limits the power" % ETA_CONV)
    bare = {}
    for k, t in TECH.items():
        p("  %s" % k)
        p("    %-14s" % "load" + "".join("%11s" % g for g, _ in C.GAPS))
        bare[k] = {}
        for ln, P in C.LOADS.items():
            row = []
            for gn, gs in C.GAPS:
                v = cap_min_volume(t, P, gs)
                row.append(v)
                bare[k].setdefault(ln, {})[gn] = dict(
                    vol_cm3=v, E_stored_full_Wh=None if v is None else v * t["wh_l_full"] / 1000.0,
                    mass_g=None if v is None else v * t["rho"])
            p("    %-14s" % ln + "".join("%11s" % ("x" if v is None else ("%.3g" % v)) for v in row))
    res["bare"]["min_volume"] = bare
    p("")

    p("BARE reach: the longest time a store that fills the margin carries a load (s). Thin parts must also be thin enough")
    reach = {}
    for mk, mm in margins.items():
        vol = margin_volume(mm, fill)
        p("  store volume %.3f cm3 (%s)" % (vol, mk))
        reach[mk] = {}
        for k, t in TECH.items():
            fits_thick = t["t_min_mm"] <= mm
            row = {}
            for ln, P in C.LOADS.items():
                row[ln] = cap_run(vol, t, P, t_goal=36000.0)
            reach[mk][k] = dict(vol_cm3=vol, thick_ok=fits_thick, seconds=row)
            p("    %-52s thickness %s: " % (k, "ok " if fits_thick else "NO ") +
              " ".join("%s %.3g s" % (ln.split()[0], s) for ln, s in row.items()))
    res["bare"]["reach"] = reach
    p("")

    # fit verdict per gap at the safe-screen and the peak load
    fit = {}
    p("BARE verdict: does a store of the 0.24 mm margin (half the body area) carry the gap, thickness included")
    vol_all = margin_volume(0.24, fill)
    for k, t in TECH.items():
        fit[k] = {}
        for ln in ("standby", "safe screen", "delta session", "peak"):
            row = []
            for gn, gs in C.GAPS:
                v = bare[k][ln][gn]["vol_cm3"]
                ok = v is not None and v <= vol_all and t["t_min_mm"] <= 0.24
                row.append("%s" % ("yes" if ok else "no"))
                fit[k].setdefault(ln, {})[gn] = ok
            p("  %-52s %-14s %s" % (k, ln, " ".join("%s=%s" % (g[0], r) for g, r in zip(C.GAPS, row))))
    res["bare"]["fit_0p24_mm"] = fit
    p("")

    # a capacitor store held in the cell layer instead of the margin: tiles of cell volume
    p("BARE in the cell layer: the cell layer is 0.90 mm, so a 0.9 mm chip EDLC fits it. Tiles of cell volume (%.4f cm3 each) the store needs" % (C.CELL_VOL_MM3 / 1000.0))
    tiles = {}
    for k, t in TECH.items():
        tiles[k] = {}
        for ln in ("safe screen", "delta session", "peak"):
            row = []
            for gn, gs in C.GAPS[:4]:
                v = bare[k][ln][gn]["vol_cm3"]
                nt = None if v is None else int(math.ceil(v / (C.CELL_VOL_MM3 / 1000.0)))
                tiles[k].setdefault(ln, {})[gn] = nt
                row.append("%s=%s" % (gn, nt))
            p("  %-52s %-14s %s" % (k, ln, " ".join(row)))
    res["bare"]["tiles_of_cell_volume"] = tiles
    p("  The same loads on micro cells need 2 cells (safe screen) and 14 to 53 cells (delta to peak), see the Buffer table. Cells are 40 to 400 times denser.")
    p("")
    # ceramic bulk capacitance for the 0.1 s and 1 s peak gaps
    mlcc_c, mlcc_v, mlcc_mm3 = 100e-6, 6.3, 2.0 * 1.25 * 1.25     # 0805 100 uF 6.3 V class [H], 50 % DC-bias loss at 4.4 V
    for gn, gs in C.GAPS[:2]:
        e_j = C.LOADS["peak"] * gs
        c_need = 2.0 * e_j / (4.48 ** 2 - 3.40 ** 2)
        n = c_need / (mlcc_c * 0.5)
        p("CERAMIC: %s at the 8.7 W peak needs %.3g F on VBUS between 4.48 and 3.40 V, so %.0f of a 100 uF 0805 part (%.1f cm3) at 50 %% bias loss [HYPOTHESIS]"
          % (gn, c_need, n, n * mlcc_mm3 / 1000.0))
        res["bare"].setdefault("ceramic", {})[gn] = dict(F=c_need, parts=n, cm3=n * mlcc_mm3 / 1000.0)
    p("")
    # sensitivity of the Buffer count to the C-rate cap
    sens = {}
    p("BUFFER sensitivity to the C-rate cap, S cell floated at 60 %, 3 s gap")
    keep = CMAX
    for cm in (2.0, 3.0, 5.0, 10.0):
        CMAX = cm
        row = {}
        for ln in ("safe screen", "delta session", "video", "peak"):
            P = C.LOADS[ln]
            c = C.CELLS["S"]
            n, why = min_cells(P, 3.0, c["E_target_Wh"], c["dcir"], SOC_FLOAT, V_FLOOR)
            row[ln] = n
        sens["%.0f C" % cm] = row
        p("  %4.0f C: " % cm + ", ".join("%s %s" % kv for kv in row.items()))
    CMAX = keep
    res["buffer"]["cmax_sensitivity_3s"] = sens
    p("")

    # ------------------------------------------------ the savings against Full
    p("SAVINGS against Full (128 cells, S at 750 Wh/L: %.2f Wh, %.1f g of cells)" % (128 * C.CELLS["S"]["E_target_Wh"], 128 * C.CELLS["S"]["mass_g"]))
    full_mass = 128 * C.CELLS["S"]["mass_g"]
    sv = {}
    for name, n in (("Bare", 0), ("Buffer 14 cells", 14), ("Buffer 23 cells", 23), ("Buffer 52 cells", 52), ("Full", 128)):
        m = n * C.CELLS["S"]["mass_g"]
        th_flat = 2.00 if n else 2.00 - C.STACK["cell"]
        sv[name] = dict(n=n, cell_mass_g=m, saved_g=full_mass - m, saved_pct=100 * (full_mass - m) / full_mass,
                        thickness_empty_tile_mm=2.00 - C.STACK["cell"],
                        thickness_flat_body_mm=th_flat,
                        thickness_saved_flat_mm=2.00 - th_flat, E_Wh=n * C.CELLS["S"]["E_target_Wh"])
        p("  %-16s %3d cells, %.2f Wh, %.1f g of cells, saves %.1f g (%.0f %%). A tile with no cell is %.2f mm thick. A flat body is %.2f mm thick, "
          "so it saves %.2f mm"
          % (name, n, sv[name]["E_Wh"], m, sv[name]["saved_g"], sv[name]["saved_pct"], 2.00 - C.STACK["cell"], th_flat, sv[name]["thickness_saved_flat_mm"]))
    res["saving"] = sv
    p("  A Buffer body is flat at 2.00 mm only if the cells sit in tiles of the full stack. Cells held outside the body (the B module) leave a 1.10 mm body.")
    p("")

    C.dump("tiers", res, LINES)
    plots(res)


def plots(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    tbl = res["buffer"]["tables"]["S floated at 60 %"]
    gx = [g for g, _ in C.GAPS]
    xs = np.arange(len(gx))
    for i, (ln, row) in enumerate(tbl.items()):
        ys = [np.nan if row[g]["n"] is None else row[g]["n"] for g in gx]
        ax[0].plot(xs, ys, "-o", color=C.PAL[i % len(C.PAL)], lw=1.6, ms=4, label=ln)
    ax[0].axhline(128, color="#444", lw=1, ls=":")
    ax[0].text(5.0, 130, "all 128 cells; no point means more", fontsize=8, ha="right")
    ax[0].set_xticks(xs)
    ax[0].set_xticklabels(gx)
    ax[0].set_ylim(0, 140)
    C.style(ax[0], "hand-over gap", "cells needed (of 128)", "Buffer: S cell floated at 60 %, reserve 10 %")
    ax[0].legend(fontsize=7, loc="center left", bbox_to_anchor=(0.0, 0.62), ncol=2, frameon=False)
    # right: volume of a Bare store against the margin, EDLC large and thin film
    for i, (k, t) in enumerate(TECH.items()):
        ys = [np.nan if res["bare"]["min_volume"][k]["delta session"][g]["vol_cm3"] is None
              else res["bare"]["min_volume"][k]["delta session"][g]["vol_cm3"] for g in gx]
        ax[1].plot(xs, ys, "-o", color=C.PAL[i], lw=1.6, ms=4, label=k.split(" (")[0])
    ax[1].set_yscale("log")
    ax[1].axhline(margin_volume(0.24, 0.5), color="#444", lw=1, ls=":")
    ax[1].text(0.02, margin_volume(0.24, 0.5) * 1.15, "0.24 mm margin, half the body area", fontsize=8)
    ax[1].set_xticks(xs)
    ax[1].set_xticklabels(gx)
    C.style(ax[1], "hand-over gap", "store volume, cm3", "Bare: store volume at the delta session, 2.24 W")
    ax[1].legend(fontsize=7, loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(C.OUT + "/tiers_buffer.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    names = []
    vals = []
    for k, t in TECH.items():
        names.append(k.split(" (")[0])
        vals.append(t["wh_l_usable"])
    names += ["micro cell G model", "micro cell S model"]
    vals += [694.0, 850.0]
    colors = [C.PAL[0]] * 4 + [C.PAL[6]] * 2
    ax.barh(names, vals, color=colors, height=0.6)
    ax.set_xscale("log")
    for i, v in enumerate(vals):
        ax.text(v * 1.08, i, "%.3g" % v, va="center", fontsize=8)
    C.style(ax, "usable Wh/L", "", "Energy density, usable window")
    ax.set_xlim(1, 3000)
    fig.tight_layout()
    fig.savefig(C.OUT + "/tiers_bare.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
