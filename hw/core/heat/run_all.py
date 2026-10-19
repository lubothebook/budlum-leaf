#!/usr/bin/env python3
"""run_all.py - seat HEAT of hw/core, block HP-2: the heat of the Split.

    python3 run_all.py            # about 1 minute

Out: out/selfcheck.txt, out/skin_cases.{json,txt}, out/skin_sustained.{json,txt},
     out/core_box.{json,txt}, out/tether.{json,txt}, out/frame.{json,txt},
     out/damage.{json,txt}, out/summary.json, out/plots/01..06
"""
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import coreheat as C
import eyewear as EW
H = C.H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PLOTS = os.path.join(OUT, "plots")
os.makedirs(PLOTS, exist_ok=True)
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
CRIT, INK, INK2, GRID = "#d03b3b", "#0b0b0b", "#52514e", "#e1e0d9"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 2.0, "font.size": 9, "legend.frameon": False,
})
SHORTL = {"delta_energy": "d0.8", "delta_thermal": "d1.25", "video": "video", "5g_like": "5G", "outdoor_800nit": "out800"}
LIM = C.LIM
AMBS = (20.0, 25.0, 30.0, 35.0)
SUMMARY = {}
T0 = time.time()


def W(name, lines):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("\n".join(lines) + "\n")


def J(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def rd(x, n=2):
    return round(float(x), n)


def dew_point(t, rh):
    """Magnus formula [GENERAL]."""
    a, b = 17.62, 243.12
    g = math.log(rh / 100.0) + a * t / (b + t)
    return b * g / (a - g)


# ==========================================================================
def selfcheck():
    L = ["SELF CHECK of the Skin build against the L.6.0 numbers", ""]
    ok = True
    # 1. the library with a ring reproduces 41.3 C: use the hostthermal point
    r = H.point("delta", "battery", "float", 25.0, False, False)
    good = abs(r["T_gate"] - 41.3) < 0.1
    ok &= good
    L.append("L.6.0 delta 2.5 W, 25 C, free air, battery: %.2f C (reference 41.3)  %s" % (r["T_gate"], "ok" if good else "DIFF"))
    # 2. the Skin build puts no heat in the ring nodes and has no ring cover
    q, i = C.skin_q("delta_thermal")
    ring_heat = q[H.I_PCB] + q[H.I_SHELL] + q[H.I_BAR]
    good = ring_heat == 0.0
    ok &= good
    L.append("heat in the ring nodes of the Skin build: %.3f W  %s" % (ring_heat, "ok" if good else "DIFF"))
    e = C.env(25.0, False)
    good = float(e.net.disc.max()) == 0.0
    ok &= good
    L.append("ring cover on the face tiles, largest fraction: %.3f  %s" % (float(e.net.disc.max()), "ok" if good else "DIFF"))
    # 3. the heat balance: heat in equals heat to the boundary
    T = C.solve_T(e, q)
    bal = float((e.net.Gb * (T - 25.0)).sum() - q.sum())
    good = abs(bal) < 1e-6
    ok &= good
    L.append("heat balance residual: %.2e W  %s" % (bal, "ok" if good else "DIFF"))
    # 4. the Skin with the L.6.0 load and the ring load put back on the tiles equals map (a) heat in total
    d, a = C.LOADS["delta_thermal"]
    L.append("map (a) tiles %.2f W, ring %.2f W, total %.2f W" % (d + a, 1.25, d + a + 1.25))
    # 5. box model sanity: a 5 W load on a 140x90x30 box in still air
    t = C.box_T(5.0, C.BOXES["M 140x90x30"], 25.0)
    L.append("box M, 5 W, 25 C, still air, mean surface %.1f C (a plausible 35 to 45 C)" % t)
    ok &= 33.0 < t < 47.0
    L.append("")
    L.append("all checks pass: %s" % ok)
    W("selfcheck.txt", L)
    print("\n".join(L))
    SUMMARY["selfcheck_pass"] = bool(ok)


# ==========================================================================
def item1_2():
    res = {}
    L = ["ITEM 1 and 2 - THE SKIN ALONE: steady hottest face point (C), no B ring, no bar load",
         "Loads are display + address. PHY = link PHY and minimal decoder, swept 0.15, 0.25, 0.35 W.",
         "dist = PHY spread over all tiles. seat = PHY on the seat tile (worst of the two is marked).",
         "cells = own cells, no host. f.10, f.34 = contact feed with 0.10 or 0.34 W loss, the cell floats or is absent.",
         "A value over 36.2 C fails (marked X).", ""]
    for wind in (False, True):
        for amb in AMBS:
            L.append("=== ambient %.0f C, %s ===" % (amb, "light wind" if wind else "still air"))
            L.append("%-24s %-6s %-8s %7s %7s %7s %7s  %-18s" % ("load", "feed", "PHY W", "dist", "seat", "worst", "margin", "hot spot (dist)"))
            for load in C.LOADS:
                for feed in ("cells", "feed010", "feed034"):
                    for phy in C.PHY_SWEEP:
                        qd, _ = C.skin_q(load, 1.0, phy, "dist", feed)
                        qs, _ = C.skin_q(load, 1.0, phy, "seat", feed)
                        hd = C.skin_T(qd, amb, wind)
                        hs = C.skin_T(qs, amb, wind)
                        worst = max(hd["T"], hs["T"])
                        key = f"{amb:.0f}C|{'wind' if wind else 'still'}|{load}|{feed}|{phy}"
                        res[key] = dict(T_dist=rd(hd["T"]), T_seat=rd(hs["T"]), T_worst=rd(worst),
                                        margin=rd(LIM - worst), passes=bool(worst <= LIM),
                                        hot_layer=hd["layer"], hot_tile=hd["tile"],
                                        hot_tile_seat=hs["tile"], hot_layer_seat=hs["layer"],
                                        Q_W=rd(_["Q"], 3), P_disp_addr=rd(_["P_disp"], 3))
                        if feed == "cells" or phy == 0.25:
                            L.append("%-24s %-6s %-8.2f %7.1f %7.1f %7.1f %+7.1f  %s (%d,%d)%s" % (
                                C.LABEL[load], feed, phy, hd["T"], hs["T"], worst, LIM - worst,
                                hd["layer"], hd["tile"][0], hd["tile"][1], "  X" if worst > LIM else ""))
            L.append("")
    # the L.6.0 reference: the same map (a) with the ring, at the same ambients
    L.append("=== reference L.6.0 body with the ring, delta 2.5 W (map a), battery ===")
    ref = {}
    for wind in (False, True):
        for amb in AMBS:
            r = H.point("delta", "battery", "float", amb, wind, False)
            ref[f"{amb:.0f}C|{'wind' if wind else 'still'}"] = dict(T=rd(r["T_gate"]), where=r["where"])
            L.append("%.0f C %-6s %.1f C (%s)" % (amb, "wind" if wind else "still", r["T_gate"], r["where"]))
    res["L60_reference_delta"] = ref
    # pass counts
    keys = [k for k in res if "|" in k and k[0].isdigit()]
    npass = sum(res[k]["passes"] for k in keys)
    L.append("")
    L.append("pass count over the whole grid (%d runs): %d pass, %d fail" % (len(keys), npass, len(keys) - npass))
    # the hot spot summary
    tiles = {}
    for k in keys:
        t = (res[k]["hot_layer"], tuple(res[k]["hot_tile"]))
        tiles[t] = tiles.get(t, 0) + 1
    L.append("hot spot of the distributed runs (layer, tile column, tile row): " +
             ", ".join("%s %s x%d" % (a, b, n) for (a, b), n in sorted(tiles.items(), key=lambda x: -x[1])[:4]))
    seat_tiles = {}
    for k in keys:
        t = (res[k]["hot_layer_seat"], tuple(res[k]["hot_tile_seat"]))
        seat_tiles[t] = seat_tiles.get(t, 0) + 1
    L.append("hot spot of the seat-PHY runs: " + ", ".join("%s %s x%d" % (a, b, n) for (a, b), n in
                                                          sorted(seat_tiles.items(), key=lambda x: -x[1])[:4]))
    res["_hot"] = dict(dist={str(k): v for k, v in tiles.items()}, seat={str(k): v for k, v in seat_tiles.items()})
    J("skin_cases.json", res)
    W("skin_cases.txt", L)
    SUMMARY["skin_pass_count"] = dict(runs=len(keys), pass_=int(npass))

    # ---- the sustained table
    sus = {}
    L2 = ["SUSTAINED DISPLAY AND ADDRESS POWER of the Skin that holds 36.2 C (W)",
          "The tiles carry the display and address load uniformly, so the sustained power does not depend on the session shape.",
          "Value = PHY 0.25 W spread over the tiles. Range = PHY 0.15 to 0.35 W, spread or on the seat tile, worst and best.",
          "P_display is the display part of the sustained power in the delta shape (0.60 of 0.80 W).",
          "nits35 = luminance at a 35 % picture level; white = luminance of a full white field (100 % picture level).",
          "FINAL/17 Section 17.13: P_display = 0.60 W x (nits / 250) x (APL / 35 %).", ""]
    for feed in ("cells", "feed010", "feed034"):
        for wind in (False, True):
            L2.append("=== %s, %s ===" % (C.FEEDS[feed], "light wind" if wind else "still air"))
            L2.append("%-9s %-24s %-9s %-9s %-9s %-11s %-11s" % ("ambient", "sustained W (range)", "P_disp W", "nits35", "white", "APL@800", "holds"))
            for amb in AMBS:
                vals = []
                for phy in C.PHY_SWEEP:
                    for place in ("dist", "seat"):
                        vals.append(C.sustained_skin("delta_energy", amb, wind, phy, place, feed)["P_disp_addr"])
                nom = C.sustained_skin("delta_energy", amb, wind, 0.25, "dist", feed)
                pic = C.picture(nom["P_display"])
                holds = [C.LABEL[k].split(" ")[0] + ("" if k not in ("delta_thermal",) else "(a)") for k in C.LOADS
                         if min(vals) >= sum(C.LOADS[k])]
                # which sessions hold at the nominal PHY
                holds_nom = [k for k in C.LOADS if nom["P_disp_addr"] >= sum(C.LOADS[k])]
                holds_all = [k for k in C.LOADS if min(vals) >= sum(C.LOADS[k])]
                sus[f"{feed}|{'wind' if wind else 'still'}|{amb:.0f}C"] = dict(
                    P_nominal=rd(nom["P_disp_addr"], 3), P_min=rd(min(vals), 3), P_max=rd(max(vals), 3),
                    P_display=rd(nom["P_display"], 3), nits_at_apl35=rd(pic["nits_at_apl35"], 0),
                    nits_full_white=rd(pic["nits_full_white"], 0), apl_at_800nits=rd(pic["apl_at_800"], 1),
                    holds_nominal_phy=holds_nom, holds_all_phy=holds_all)
                L2.append("%-9s %-24s %-9.2f %-9.0f %-9.0f %-11.0f %s" % (
                    "%.0f C" % amb, "%.2f (%.2f to %.2f)" % (nom["P_disp_addr"], min(vals), max(vals)),
                    nom["P_display"], pic["nits_at_apl35"], pic["nits_full_white"], pic["apl_at_800"],
                    "/".join(SHORTL[k] for k in holds_nom) or "none"))
            L2.append("")
    L2.append("holds = the sessions of the table of Item 1 whose display and address load stays under the sustained power, nominal PHY.")
    J("skin_sustained.json", sus)
    W("skin_sustained.txt", L2)

    # ---- plots
    # 01 field: L.6.0 against Skin, delta, 25 C
    fig, axs = plt.subplots(1, 2, figsize=(8, 5.6))
    e0 = H.env(25.0, False, "free")
    q0, _ = H.heat("delta", "battery", "float", cfg=H.FIX)
    T0v = e0.solve(q0, dict(P_rx=0.0))
    e1 = C.env(25.0, False)
    q1, _ = C.skin_q("delta_thermal", 1.0, 0.25, "dist", "cells")
    T1v = C.solve_T(e1, q1)
    f0 = np.array([T0v[e0.net.nid(t, "FS")] for t in range(H.NT)]).reshape(16, 8)
    f1 = np.array([T1v[e1.net.nid(t, "FS")] for t in range(H.NT)]).reshape(16, 8)
    vmax = f0.max()
    for ax, f, ttl in ((axs[0], f0, "L.6.0 body with the ring\n2.5 W, hottest %.1f C" % f0.max()),
                       (axs[1], f1, "Skin alone, 1.25 W + 0.25 W PHY\nhottest %.1f C" % f1.max())):
        im = ax.imshow(f, cmap="Blues", vmin=25, vmax=vmax, extent=(0, 80, 160, 0))
        ax.set_title(ttl, fontsize=9, color=INK)
        ax.grid(False)
        ax.contour(np.linspace(5, 75, 8), np.linspace(5, 155, 16), f, levels=[LIM], colors=[CRIT], linewidths=1.5)
    cb = fig.colorbar(im, ax=axs, shrink=0.75)
    cb.set_label("front cap, C (red line = 36.2 C)")
    fig.suptitle("The hot spot under the ring disappears, 25 C still air", color=INK)
    fig.savefig(os.path.join(PLOTS, "01_skin_fields.png"), dpi=130)
    plt.close(fig)
    # 02 sustained against ambient
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.0), sharey=True)
    amb_f = np.arange(15, 36, 2.5)
    for ax, wind in zip(axs, (False, True)):
        for k, (load, col) in enumerate((("delta_energy", S[0]), ("video", S[1]), ("5g_like", S[2]))):
            ys = [C.sustained_skin(load, a, wind, 0.25, "dist", "cells")["P_disp_addr"] for a in amb_f]
            ax.plot(amb_f, ys, color=col, label="Skin, shape of " + C.LABEL[load].split(" ")[0])
            d, a_ = C.LOADS[load]
            ax.axhline(d + a_, color=col, lw=0.8, ls=":")
        l60 = [H.sustained("delta", "battery", "float", a, wind, False)["P_adm"] for a in amb_f]
        ax.plot(amb_f, l60, color=INK2, ls="--", label="L.6.0 body with ring, total load")
        ax.set_xlabel("ambient, C")
        ax.set_title("light wind" if wind else "still air", fontsize=9, color=INK)
    axs[0].set_ylabel("sustained display + address power, W")
    axs[0].legend(fontsize=7)
    fig.suptitle("Skin sustained power under 36.2 C (dotted = the nominal load of that session)", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "02_skin_sustained.png"), dpi=130)
    plt.close(fig)
    return res, sus


# ==========================================================================
def item3():
    res = {}
    L = ["ITEM 3 - THE CORE ALONE: a sealed box with the silicon and the radio",
         "Assumptions [HYPOTHESIS]: aluminium case, matte, emissivity 0.90, the heat spreads to a mean case rise;",
         "the peak case rise is 1.25 times the mean rise. Natural convection and radiation from textbook simple forms [GENERAL].",
         "free = still air on a desk (bottom half blocked). fan = 2 m/s over a plain case. fan+fins = the same with 3x area.",
         "plate = the footprint on a 22 C plate (h = 400 W/m2K), the rest in still air.",
         "Core heat = rails / 0.90 + Skin supply loss (6 %) + 0.25 W of link PHY per Skin. Radio and authority run once (shared).",
         "'unshared' puts the whole ring load of the Leaf (1.22 / 1.92 W) on every Skin.",
         "5G modem = 1.20 W (U5 of map c). Validator option = hw/dock/params.py: idle %.1f, typical %.1f, peak %.1f W." % (
             C.VALIDATOR_IDLE, C.VALIDATOR_TYP, C.VALIDATOR_PEAK), ""]
    # heat table
    L.append("--- Core heat in W ---")
    L.append("%-34s %6s %6s %6s %6s" % ("case", "N=1", "N=2", "N=4", "N=8"))
    heat = {}
    for sess in ("delta", "video"):
        for shared in (True, False):
            for modem in (False, True):
                for val in (None, "typ"):
                    row = [C.core_heat(n, sess, shared, modem, val) for n in (1, 2, 4, 8)]
                    name = "%s, %s%s%s" % (sess, "shared" if shared else "unshared", ", 5G" if modem else "",
                                          ", validator typ" if val else "")
                    heat[name] = row
                    L.append("%-34s %6.1f %6.1f %6.1f %6.1f" % ((name,) + tuple(row)))
    res["heat_W"] = heat
    # surface temperature for sizes, N=1,2,4,8 delta shared, no modem; and a few more
    L.append("")
    L.append("--- mean case temperature, C, at 25 C ambient (peak in brackets) ---")
    surf = {}
    for case_name, kw in (("delta shared", dict(session="delta")),
                          ("video shared", dict(session="video")),
                          ("video shared + 5G", dict(session="video", modem=True)),
                          ("video shared + 5G + validator typ", dict(session="video", modem=True, validator="typ"))):
        L.append("[%s]" % case_name)
        L.append("%-16s %-3s %-7s %-14s %-14s %-14s %-14s" % ("box", "N", "Q W", "free", "fan", "fan+fins", "plate 22 C"))
        for b, dims in C.BOXES.items():
            for n in (1, 2, 4, 8):
                Q = C.core_heat(n, **kw)
                cells = []
                for mode, extra in (("free", {}), ("fan", {}), ("fan", dict(fins=3.0)), ("plate", {})):
                    tm = C.box_T(Q, dims, 25.0, mode=mode, **extra)
                    cells.append((tm, C.peak_T(tm, 25.0, mode)))
                    surf[f"{case_name}|{b}|N{n}|{mode}{'_fins' if extra else ''}"] = dict(Q=rd(Q), T_mean=rd(tm), T_peak=rd(cells[-1][1]))
                L.append("%-16s %-3d %-7.1f " % (b, n, Q) + "".join("%-14s" % ("%.1f (%.1f)" % c) for c in cells))
        L.append("")
    res["surface"] = surf
    # N max under touch limits
    L.append("--- the largest number of Skins a Core holds, peak case temperature at or under the touch limit ---")
    L.append("Touch limits [HYPOTHESIS, recalled, not read from the standard]: 41 C a worn or pocket Core;")
    L.append("43 C a Core that is held or rests on skin; 48 C IEC 62368-1 TS1 style limit for a part touched or held for over a minute.")
    L.append("The limits are absolute, as at 25 C ambient. Radio and authority run once. 'cap' means 64 Skins reached.")
    L.append("The plate rows stop where the dock TEC reaches its pumping limit (hw/dock; the search stops at 32 W, the TEC limit is 27 W at 35 C).")
    nmax = {}
    for b, dims in C.BOXES.items():
        L.append("[box %s]" % b)
        L.append("%-12s %-24s %s" % ("limit", "mode", "  ".join("%6s" % ("%.0f C" % a) for a in AMBS)))
        for tl in (41.0, 43.0, 48.0):
            for mode, kw in (("free", {}), ("fan", {}), ("fan+fins", dict(fins=3.0)), ("plate", {})):
                mm = "fan" if mode.startswith("fan") else mode
                row = []
                for amb in AMBS:
                    best = 0
                    for n in range(1, 65):
                        Q = C.core_heat(n, "delta", True, False, None)
                        tm = C.box_T(Q, dims, amb, mode=mm, **kw)
                        tp = C.peak_T(tm, amb, mm)
                        tec_ok = (mm != "plate") or (Q + 0.15 * (amb - 22.0) <= H.tec_qmax(amb))
                        if tp <= tl and tec_ok:
                            best = n
                        else:
                            break
                    row.append(best)
                    nmax[f"{b}|{tl:.0f}|{mode}|{amb:.0f}C|delta"] = best
                L.append("%-12s %-24s %s" % ("%.0f C" % tl, "delta, " + mode, "  ".join("%6s" % ("cap" if v >= 64 else v) for v in row)))
        L.append("")
    # the same for video, 43 C, free
    L.append("--- video, 43 C, free air and fan+fins ---")
    for b, dims in C.BOXES.items():
        for mode, kw in (("free", {}), ("fan", dict(fins=3.0))):
            row = []
            for amb in AMBS:
                best = 0
                for n in range(1, 65):
                    Q = C.core_heat(n, "video", True, False, None)
                    tm = C.box_T(Q, dims, amb, mode=("fan" if mode == "fan" else "free"), **kw)
                    if C.peak_T(tm, amb, "fan" if mode == "fan" else "free") <= 43.0:
                        best = n
                    else:
                        break
                row.append(best)
                nmax[f"{b}|43|{mode}|video|" + "|".join("%.0f" % a for a in AMBS)] = row
            L.append("%-16s %-9s %s" % (b, mode, "  ".join("%6s" % v for v in row)))
    res["N_max"] = nmax
    # unshared and the options
    L.append("")
    L.append("--- the heat each box holds at 43 C peak, 25 C ambient ---")
    opts = {}
    for b, dims in C.BOXES.items():
        def qlim(mode, **kw):
            lo, hi = 0.0, 600.0
            for _ in range(60):
                m = 0.5 * (lo + hi)
                tm = C.box_T(m, dims, 25.0, mode=mode, **kw)
                if C.peak_T(tm, 25.0, mode) <= 43.0:
                    lo = m
                else:
                    hi = m
            return lo
        qf, qfan, qplate = qlim("free"), qlim("fan", fins=3.0), min(qlim("plate"), H.tec_qmax(25.0))
        opts[b] = dict(free=qf, fan_fins=qfan, plate=qplate)
        L.append("%-16s passive %.1f W, fan+fins %.1f W, plate %.1f W (the TEC limit binds; peak at 43 C, 25 C ambient)" % (b, qf, qfan, qplate))
    L.append("Validator typical %.1f W, idle %.1f W, peak %.1f W. The dock plate TEC pumps %.0f W at least (hw/dock)." % (
        C.VALIDATOR_TYP, C.VALIDATOR_IDLE, C.VALIDATOR_PEAK, min(H.tec_qmax(a) for a in AMBS)))
    res["Q_limit_43C_25C"] = opts
    J("core_box.json", res)
    W("core_box.txt", L)

    # plot: case temperature against Q for the four boxes
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
    Qs = np.linspace(0.5, 40, 60)
    for ax, (mode, kw, ttl) in zip(axs, (("free", {}, "free air, still"), ("fan", dict(fins=3.0), "fan 2 m/s, 3x fins"),
                                          ("plate", {}, "on a 22 C plate"))):
        for (b, dims), col in zip(C.BOXES.items(), S):
            ax.plot(Qs, [C.peak_T(C.box_T(q, dims, 25.0, mode=mode, **kw), 25.0, mode) for q in Qs],
                    color=col, label=b)
        for lv, ls_ in ((41, ":"), (43, "--"), (48, "-")):
            ax.axhline(lv, color=INK2, lw=0.9, ls=ls_)
        ax.set_ylim(20, 80)
        ax.set_xlabel("Core heat, W")
        ax.set_title(ttl + ", 25 C", fontsize=9, color=INK)
        ax.text(0.8, 48.8, "48 C", fontsize=7.5, color=INK2)
        ax.text(0.8, 43.8, "43 C", fontsize=7.5, color=INK2)
        ax.text(0.8, 41.8 - 3.2, "41 C", fontsize=7.5, color=INK2)
    for x, lab in ((C.core_heat(1, "delta"), "N=1"), (C.core_heat(4, "delta"), "N=4"),
                   (C.core_heat(8, "delta"), "N=8"), (C.VALIDATOR_TYP + C.core_heat(1, "delta"), "+validator")):
        axs[0].axvline(x, color=GRID, lw=1.0)
        axs[0].text(x + 0.2, 77, lab, fontsize=7, color=INK2, rotation=90, va="top")
    axs[0].set_ylabel("peak case temperature, C")
    axs[0].legend(fontsize=7, loc="lower right")
    fig.suptitle("Core box: peak case temperature against heat. Lines are the assumed touch limits", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "03_core_box.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
def item4():
    res = {}
    L = ["ITEM 4 - THE TETHER HEAT at the Skin end",
         "hw/core/power/ and hw/core/link/ held no files when this run was made, so the options below are sweeps",
         "and named hypotheses. Tether heat = link PHY + decoder + the power path loss at the Skin end.", ""]
    # sweep A: extra loss at the seat tile
    L.append("--- sweep A: extra Skin-end loss, W, on the seat tile, on top of a 0.25 W PHY and decoder ---")
    L.append("%-18s %-8s %9s %9s %9s %9s %9s %9s" % ("load", "amb", "0.0", "0.1", "0.25", "0.5", "0.75", "1.0"))
    sweepA = {}
    for load in ("delta_energy", "video", "5g_like"):
        for amb in (25.0, 30.0):
            sus_row, T_row = [], []
            for ex in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
                s = C.sustained_skin(load, amb, False, 0.25, "dist", "none", extra=ex)
                sus_row.append(s["P_disp_addr"])
                q, _ = C.skin_q(load, 1.0, 0.25, "dist", "none", extra=ex)
                T_row.append(C.skin_T(q, amb, False)["T"])
            sweepA[f"{load}|{amb:.0f}"] = dict(P_sustained=[rd(x, 3) for x in sus_row], T_nominal=[rd(x) for x in T_row])
            L.append("%-18s %-8s " % (C.LABEL[load][:18], "%.0f C" % amb) + " ".join("%9.2f" % x for x in sus_row) + "  W sustained")
            L.append("%-18s %-8s " % ("", "") + " ".join("%9.1f" % x for x in T_row) + "  C at nominal")
    res["sweepA"] = sweepA
    # cost per watt
    s0 = C.sustained_skin("video", 25.0, False, 0.25, "dist", "none", extra=0.0)["P_disp_addr"]
    s1 = C.sustained_skin("video", 25.0, False, 0.25, "dist", "none", extra=1.0)["P_disp_addr"]
    res["video_25C_loss_per_W"] = s0 - s1
    L.append("")
    s1d = C.sustained_skin("video", 25.0, False, 0.25, "dist", "none", extra=1.0, extra_place="dist")["P_disp_addr"]
    res["video_25C_loss_per_W_spread"] = s0 - s1d
    L.append("Each watt of Skin-end loss on the seat tile costs %.2f W of sustained display power at 25 C, still air." % (s0 - s1))
    L.append("The same watt spread over all tiles costs %.2f W. Where the loss sits matters by a factor of %.1f." % (s0 - s1d, (s0 - s1) / (s0 - s1d)))
    L.append("'sust seat' puts the path loss on the seat tile. 'sust spread' puts it in regulators spread over the tiles.")
    # sweep B: PHY power
    L.append("")
    L.append("--- sweep B: link PHY and decoder power, W, spread over the tiles, own cell-less Skin ---")
    sweepB = {}
    for load in ("video", "5g_like"):
        row = []
        for phy in (0.1, 0.25, 0.5, 0.75, 1.0):
            row.append(C.sustained_skin(load, 25.0, False, phy, "dist", "none")["P_disp_addr"])
        sweepB[load] = [rd(x, 3) for x in row]
        L.append("%-18s 25 C still: " % C.LABEL[load][:18] + " ".join("%6.2f" % x for x in row) + "  W display+address for PHY 0.1 0.25 0.5 0.75 1.0")
    res["sweepB"] = sweepB
    # options
    L.append("")
    L.append("--- named options [HYPOTHESIS], the Skin draws display + address of the video load, 1.35 W ---")
    L.append("%-44s %6s %6s %6s %8s %8s %9s %9s" % ("option", "PHY+dec", "path", "heat", "T 25 C", "T 35 C", "sust seat", "sust spread"))
    ccfg = H.FIX.copy(V_rect=12.0)
    P_el0 = 1.35
    def qi_chain(Prx):
        Lc = H.charge_losses(ccfg, Prx)
        return Lc["coil"] + Lc["shield_eddy"] + Lc["ac_lead"] + Lc["rectifier"] + Lc["charger"]
    options = {
        "wired, short copper, VBUS 3.85 V, 12 pads": (0.15 + 0.10, lambda P: 0.10 + 0.006 * P * P),
        "wired, 12 V in, 3:1 charger at the Skin": (0.15 + 0.10, lambda P: 0.10 + 0.05 * P),
        "wired, 48 V EPR in, buck at the Skin": (0.15 + 0.10, lambda P: 0.10 + 0.10 * P),
        "optical fibre + 12 V power, 3:1 at the Skin": (0.25 + 0.10, lambda P: 0.10 + 0.05 * P),
        "cable 10 Gbit/s PHY, 12 V power": (0.30 + 0.10, lambda P: 0.10 + 0.05 * P),
        "60 GHz link + Qi-class wireless power": (0.80 + 0.10, lambda P: qi_chain(P)),
        "60 GHz link + own cells (no power cable)": (0.80 + 0.10, lambda P: 0.0),
    }
    opt_res = {}
    for name, (phy, path) in options.items():
        P_total = P_el0 + phy
        loss = path(P_total)
        row = {}
        for amb in (25.0, 35.0):
            q, _ = C.skin_q("video", 1.0, phy, "dist", "cells" if "own cells" in name else "none", extra=loss)
            row[amb] = C.skin_T(q, amb, False)["T"]
        fd = "cells" if "own cells" in name else "none"
        s = C.sustained_skin("video", 25.0, False, phy, "dist", fd, extra=loss)
        s2 = C.sustained_skin("video", 25.0, False, phy, "dist", fd, extra=loss, extra_place="dist")
        opt_res[name] = dict(PHY_decoder=phy, path_loss=rd(loss, 3), tether_heat=rd(phy + loss, 3),
                             T25=rd(row[25.0]), T35=rd(row[35.0]), sustained25=rd(s["P_disp_addr"], 3),
                             sustained25_spread=rd(s2["P_disp_addr"], 3))
        L.append("%-44s %6.2f %6.2f %6.2f %8.1f %8.1f %9.2f %9.2f" % (name, phy, loss, phy + loss, row[25.0], row[35.0],
                                                                    s["P_disp_addr"], s2["P_disp_addr"]))
    res["options"] = opt_res
    L.append("")
    L.append("--- the largest PHY and decoder power (spread, own cells) that holds 36.2 C for the nominal Skin load, W ---")
    maxphy = {}
    for load in ("delta_energy", "video", "5g_like"):
        row = []
        for amb in (20.0, 25.0, 30.0, 35.0):
            def ok(phy, load=load, amb=amb):
                q, _ = C.skin_q(load, 1.0, phy, "dist", "cells")
                return C.skin_T(q, amb, False)["T"] <= LIM
            if not ok(0.0):
                row.append(0.0)
                continue
            lo, hi = 0.0, 8.0
            for _ in range(40):
                m = 0.5 * (lo + hi)
                if ok(m):
                    lo = m
                else:
                    hi = m
            row.append(lo)
        maxphy[load] = [rd(x, 3) for x in row]
        L.append("%-18s 20, 25, 30, 35 C still: " % C.LABEL[load][:18] + "  ".join("%.2f" % x for x in row))
    res["max_phy"] = maxphy
    L.append("")
    L.append("Core end: the supply loses 6 % of the Skin power and the PHY takes 0.25 W per Skin, already in item 3.")
    J("tether.json", res)
    W("tether.txt", L)
    # plot
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.0))
    ex = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)
    for load, col in (("delta_energy", S[0]), ("video", S[1]), ("5g_like", S[2])):
        axs[0].plot(ex, sweepA[f"{load}|25"]["P_sustained"], color=col, marker="o", ms=4, label=C.LABEL[load])
    axs[0].set_xlabel("extra Skin-end loss, W")
    axs[0].set_ylabel("sustained display + address power, W")
    axs[0].set_title("25 C still air, PHY 0.25 W", fontsize=9, color=INK)
    axs[0].legend(fontsize=7)
    names = list(opt_res)
    axs[1].barh(range(len(names)), [opt_res[n]["tether_heat"] for n in names], color=S[0], height=0.6)
    for i, n in enumerate(names):
        axs[1].text(opt_res[n]["tether_heat"] + 0.02, i, "%.2f W" % opt_res[n]["tether_heat"], va="center", fontsize=7.5, color=INK)
    axs[1].set_yticks(range(len(names)))
    axs[1].set_yticklabels([n[:34] for n in names], fontsize=7)
    axs[1].invert_yaxis()
    axs[1].set_xlabel("tether heat at the Skin end, W")
    axs[1].grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "04_tether.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
def item5():
    res = {}
    L = ["ITEM 5 - THE FRAME: the face-worn Skin",
         "Model: the two-node face model of hw/hostpower/thermal/eyewear.py (skin 34 C, 100 cm2 exposed, 8 cm2 contact).",
         "The Split moves the silicon and the radio to a Core. The Frame keeps the microdisplay, the link PHY, the decoder and the connector.",
         "P_display spreads over the lens and the rim. P_temple (PHY, decoder, connector) sits in the temple behind 3 K/W.",
         "Before the Split the whole load sat in the Frame with 60 % in a temple hot spot (eyewear.py): 1.05 W at 25 C still air.", ""]
    L.append("--- the heat limit in W of display power for a given temple load (PHY + decoder + connector) ---")
    L.append("%-30s %-8s %8s %8s %8s %8s" % ("temple load", "wind", "20 C", "25 C", "30 C", "35 C"))
    fr = {}
    for temple in (0.25, 0.45, 0.59, 0.69):
        for wind in (False, True):
            row = [C.frame_pmax(temple, a, wind) for a in AMBS]
            fr[f"{temple}|{'wind' if wind else 'still'}"] = [rd(x, 3) for x in row]
            L.append("%-30s %-8s %8.2f %8.2f %8.2f %8.2f" % ("%.2f W" % temple, "wind" if wind else "still", *row))
    res["display_limit"] = fr
    L.append("   0.25 W = PHY and decoder 0.15 + connector 0.10. 0.45 = 0.25 + 0.20. 0.59 = 0.25 + 0.34. 0.69 = 0.35 + 0.34.")
    L.append("")
    L.append("--- total heat limit in the Frame, W (display + temple), against the 1.05 W of the unsplit Frame ---")
    tot = {}
    for temple in (0.25, 0.59, 0.69):
        row = [(C.frame_pmax(temple, a, False) + temple) if C.frame_temps(0.0, temple, a, False)["T_peak"] <= LIM else 0.0
               for a in AMBS]
        tot[str(temple)] = [rd(x, 3) for x in row]
        L.append("temple %.2f W: " % temple + "  ".join("%.2f" % x for x in row) + "   (20, 25, 30, 35 C)")
    base = [EW.p_max(a, False) for a in AMBS]
    L.append("0.00 means the temple load alone is over the limit with the display off.")
    L.append("unsplit (eyewear.py): " + "  ".join("%.2f" % x for x in base))
    res["total_limit"] = tot
    res["unsplit"] = [rd(x, 3) for x in base]
    L.append("")
    L.append("--- Split Frame verdict at 25 C, still air: display power D, temple load T ---")
    verd = {}
    for D in (0.20, 0.35, 0.50):
        for T in (0.25, 0.59, 0.69):
            t = C.frame_temps(D, T, 25.0, False)
            verd[f"D{D}|T{T}"] = dict(T_peak=rd(t["T_peak"]), margin=rd(LIM - t["T_peak"]))
            L.append("D %.2f W, temple %.2f W: peak %.1f C, margin %+.1f K" % (D, T, t["T_peak"], LIM - t["T_peak"]))
    res["verdict_25C"] = verd
    # the ambient limit of the 0.8 W frame, before and after
    def amb_limit(fn):
        for ta in np.arange(10, 45.01, 0.05):
            if fn(ta):
                return float(ta) - 0.05
        return None
    before = amb_limit(lambda ta: EW.temps(0.8 + 0.34, ta, False)["T_peak"] > LIM)
    after = amb_limit(lambda ta: C.frame_temps(0.35, 0.59, ta, False)["T_peak"] > LIM)
    after2 = amb_limit(lambda ta: C.frame_temps(0.35, 0.25, ta, False)["T_peak"] > LIM)
    res["ambient_limit"] = dict(before_0p8W_conn034=before, after_D035_T059=after, after_D035_T025=after2)
    L.append("")
    L.append("Ambient up to which the Frame holds 36.2 C in still air: unsplit 0.8 W + 0.34 W loss: %.1f C;" % before)
    L.append("Split, display 0.35 W, temple 0.59 W: %.1f C; Split, display 0.35 W, temple 0.25 W: %.1f C." % (after, after2))
    t_c1 = C.frame_temps(0.35, 0.90 + 0.10, 25.0, False)
    res["C1_frame_25C"] = dict(T_peak=rd(t_c1["T_peak"]), margin=rd(LIM - t_c1["T_peak"]))
    L.append("A C1 Frame with a 0.90 W PHY and decoder and a 0.10 W connector, display 0.35 W, 25 C: peak %.1f C (margin %+.1f K)." % (
        t_c1["T_peak"], LIM - t_c1["T_peak"]))
    J("frame.json", res)
    W("frame.txt", L)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ta = np.arange(15, 38.1, 1.0)
    ax.plot(ta, [EW.p_max(t, False) for t in ta], color=INK2, ls="--", label="unsplit Frame, total heat")
    for temple, col in ((0.25, S[0]), (0.59, S[1])):
        ax.plot(ta, [C.frame_pmax(temple, t, False) + temple for t in ta], color=col,
                label="Split, total heat, temple %.2f W" % temple)
        ax.plot(ta, [C.frame_pmax(temple, t, False) for t in ta], color=col, ls=":",
                label="Split, display only, temple %.2f W" % temple)
    ax.axhspan(0.2, 0.5, color=S[2], alpha=0.12)
    ax.text(15.3, 0.52, "assumed microdisplay 0.2 to 0.5 W", color=INK2, fontsize=8)
    ax.set_xlabel("ambient, C")
    ax.set_ylabel("heat held under 36.2 C, W")
    ax.legend(fontsize=7)
    ax.set_title("Frame face-side limit, before and after the Split (still air)", fontsize=9, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "05_frame.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
def item6():
    res = {}
    L = ["ITEM 6 - DAMAGE REPORT numbers: dock plate, dew point, TEC, throttle", ""]
    # dew point: the warmest plate that holds the Skin under 36.2 C
    L.append("--- the warmest dock plate set-point that holds the Skin at 36.2 C (PHY 0.25 W, own cells) ---")
    L.append("%-8s %-24s %12s %14s %14s %14s %14s" % ("ambient", "load", "plate max C", "dew 60 % RH", "margin", "dew 80 % RH", "margin"))
    for amb in (25.0, 30.0, 35.0):
        for load in ("delta_energy", "video", "5g_like"):
            q, _ = C.skin_q(load, 1.0, 0.25, "dist", "cells")
            e = C.env(amb, False, "dock")
            lo, hi = 10.0, 60.0
            if C.skin_T(q, amb, False, "dock", lo)["T"] > LIM:
                tp = None
            else:
                for _ in range(40):
                    m = 0.5 * (lo + hi)
                    if C.skin_T(q, amb, False, "dock", m)["T"] <= LIM:
                        lo = m
                    else:
                        hi = m
                tp = lo
            dp = dew_point(amb, 60.0)
            dp8 = dew_point(amb, 80.0)
            res[f"plate|{amb:.0f}C|{load}"] = dict(plate_max=None if tp is None else rd(tp), dew60=rd(dp), dew80=rd(dp8),
                                                   margin60=None if tp is None else rd(tp - dp),
                                                   margin80=None if tp is None else rd(tp - dp8))
            L.append("%-8s %-24s %12s %14.1f %14s %14.1f %14s" % ("%.0f C" % amb, C.LABEL[load], "none" if tp is None else "%.1f" % tp,
                                                      dp, "n.a." if tp is None else "%+.1f" % (tp - dp), dp8,
                                                      "n.a." if tp is None else "%+.1f" % (tp - dp8)))
    # L.6.0 body for comparison: the plate max of the delta session with the ring
    L.append("")
    L.append("--- the same plate limit for the L.6.0 body with the ring (delta 2.5 W, battery) ---")
    for amb in (25.0, 35.0):
        e = H.env(amb, False, "dock")
        q, info = H.heat("delta", "battery", "float", cfg=H.FIX)
        lo, hi = 10.0, 60.0
        for _ in range(40):
            m = 0.5 * (lo + hi)
            T = e.solve(q, dict(P_rx=0.0)) if False else None
            rhs = q + e.net.q_fixed + e.net.GbT + (m - 20.0) * e.gpad
            Tv = e.lu.solve(rhs)
            if e.net.readout(Tv)["T_surface_max"] <= LIM:
                lo = m
            else:
                hi = m
        res[f"plate_L60|{amb:.0f}C"] = rd(lo)
        L.append("%.0f C: plate max %.1f C, dew point %.1f C at 60 %% RH, %.1f C at 80 %% RH" % (
            amb, lo, dew_point(amb, 60.0), dew_point(amb, 80.0)))
    # TEC load
    L.append("")
    L.append("--- the TEC electric power for the plate at 22 C, W (hw/dock/budget.py solve_tec) ---")
    L.append("%-8s %-26s %8s %8s" % ("ambient", "case", "q_need", "P_tec"))
    for amb in (25.0, 35.0):
        for name, Qleaf in (("L.6.0 delta, battery", H.heat("delta", "battery", "float")[1]["Q_leaf"]),
                            ("Skin video 1.35 W + PHY", C.skin_q("video", 1.0, 0.25, "dist", "cells")[1]["Q"]),
                            ("Skin delta 0.80 W + PHY", C.skin_q("delta_energy", 1.0, 0.25, "dist", "cells")[1]["Q"])):
            qn = Qleaf * H.DP.F_DEVICE_HEAT_TO_PAD + H.DP.UA_PAD_LEAK * (amb - H.DP.PAD_SETPOINT)
            sol = H.DB.solve_tec(amb, max(qn, 0.01))
            res[f"tec|{amb:.0f}C|{name}"] = dict(q_need=rd(qn), P_tec=None if not sol else rd(sol["P_tec"]))
            L.append("%-8s %-26s %8.2f %8.2f" % ("%.0f C" % amb, name, qn, sol["P_tec"] if sol else float("nan")))
    # TEC power at a higher set-point
    L.append("")
    L.append("--- TEC electric power at 35 C ambient for a warmer plate set-point, Skin video 1.35 W + PHY, W ---")
    Qs = C.skin_q("video", 1.0, 0.25, "dist", "cells")[1]["Q"]
    old = H.DP.PAD_SETPOINT
    for sp in (22.0, 26.0, 28.0, 30.0):
        H.DP.PAD_SETPOINT = sp
        qn = Qs * H.DP.F_DEVICE_HEAT_TO_PAD + H.DP.UA_PAD_LEAK * (35.0 - sp)
        sol = H.DB.solve_tec(35.0, max(qn, 0.01))
        res[f"tec_setpoint|{sp:.0f}"] = None if not sol else rd(sol["P_tec"])
        L.append("set-point %.0f C: q_need %.2f W, TEC %s W" % (sp, qn, "n.a." if not sol else "%.2f" % sol["P_tec"]))
    H.DP.PAD_SETPOINT = old
    # throttle law at 30 C
    L.append("")
    L.append("--- the throttle law on the Skin at 30 C: the steady display scale (PHY fixed 0.25 W) ---")
    for wind in (False, True):
        for load in ("delta_thermal", "video", "5g_like", "outdoor_800nit"):
            def holds(s):
                q, _ = C.skin_q(load, s, 0.25, "dist", "cells")
                return s <= H.derate(C.skin_T(q, 30.0, wind)["T"], LIM) + 1e-12
            if holds(1.0):
                s = 1.0
            else:
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    m = 0.5 * (lo + hi)
                    if holds(m):
                        lo = m
                    else:
                        hi = m
                s = lo
            res[f"throttle|30C|{'wind' if wind else 'still'}|{load}"] = rd(s, 3)
            L.append("%-8s %-24s display scale %.2f" % ("wind" if wind else "still", C.LABEL[load], s))
    J("damage.json", res)
    W("damage.txt", L)
    return res


# ==========================================================================
def item_c2():
    res = {}
    L = ["CLASS C2 - the Leaf keeps the radio, the 5G modem, the decoder and the compositor (BRIEF Section 8)",
         "The body is the L.6.0 fixed body with the B ring. The ring carries hub + authority + radio.",
         "hub (decoder, compositor, frame store): delta 0.70 W, video 1.20 W. authority 0.12 W. Radio domain swept 0.4 to 1.6 W.",
         "Tiles carry display + address: delta 0.60 + 0.20 W, video 1.10 + 0.25 W (hw/energy body column).",
         "Energy is local: the Leaf cells (cells), or a near contact host (f.10, f.34).", ""]
    for wind in (False, True):
        for amb in AMBS:
            L.append("=== ambient %.0f C, %s ===" % (amb, "light wind" if wind else "still air"))
            L.append("%-8s %-7s %6s %7s %7s %7s %-12s %9s" % ("session", "feed", "radio", "P_L W", "T hot", "margin", "hot spot", "ring only"))
            for sess in ("delta", "video"):
                for feed in ("cells", "feed034"):
                    for rad in C.R_SWEEP:
                        q, i = C.c2_q(sess, rad, 1.0, feed)
                        t = C.c2_T(q, amb, wind)
                        q0, _ = C.c2_q(sess, rad, 0.0, feed)
                        t0 = C.c2_T(q0, amb, wind)
                        key = f"{amb:.0f}C|{'wind' if wind else 'still'}|{sess}|{feed}|{rad}"
                        res[key] = dict(T=rd(t["T"]), where=t["where"], margin=rd(LIM - t["T"]), P_L=rd(i["P_L"], 3),
                                        T_ring_only=rd(t0["T"]), passes=bool(t["T"] <= LIM), Q=rd(i["Q"], 3))
                        if feed == "cells" or rad == 0.4:
                            L.append("%-8s %-7s %6.1f %7.2f %7.1f %+7.1f %-12s %9.1f%s" % (
                                sess, feed, rad, i["P_L"], t["T"], LIM - t["T"], t["where"], t0["T"],
                                "" if t["T"] <= LIM else "  X"))
            L.append("")
    # sustained
    L.append("--- sustained display + address power at C2, ring fixed (W; 0.00 = the ring alone is over 36.2 C) ---")
    L.append("%-8s %-8s %-7s %6s %7s %7s %7s %7s" % ("session", "wind", "radio", "", "20 C", "25 C", "30 C", "35 C"))
    for sess in ("delta", "video"):
        for wind in (False, True):
            for rad in C.R_SWEEP:
                vals = []
                for amb in AMBS:
                    s = C.c2_sustained(sess, rad, amb, wind)
                    d, a = C.C2_TILES[sess]
                    vals.append(s * (d + a))
                    res[f"sus|{amb:.0f}C|{'wind' if wind else 'still'}|{sess}|{rad}"] = rd(s * (d + a), 3)
                L.append("%-8s %-8s %-7.1f %6s %7.2f %7.2f %7.2f %7.2f" % (sess, "wind" if wind else "still", rad, "", *vals))
    # the ring alone, picture off, floor
    L.append("")
    L.append("--- the ring alone (display off): the highest ambient where it holds 36.2 C, still air ---")
    for sess in ("delta", "video"):
        for rad in C.R_SWEEP:
            amb_hi = None
            for a in np.arange(10.0, 40.0, 0.25):
                q0, _ = C.c2_q(sess, rad, 0.0, "cells")
                if C.c2_T(q0, a, False)["T"] > LIM:
                    amb_hi = a - 0.25
                    break
            res[f"ring_only_amb|{sess}|{rad}"] = amb_hi
            L.append("%-6s radio %.1f W: the ring alone holds up to %.1f C ambient" % (sess, rad, amb_hi if amb_hi else 40.0))
    # C2 on the dock plate for reference
    L.append("")
    L.append("--- C2 on the dock plate at 22 C (reference: the ring has a heat path again), 35 C ambient, still air ---")
    for sess in ("delta", "video"):
        for rad in C.R_SWEEP:
            q, i = C.c2_q(sess, rad, 1.0, "cells")
            t = C.c2_T(q, 35.0, False, "dock", 22.0)
            res[f"dock|35C|{sess}|{rad}"] = rd(t["T"])
            L.append("%-6s radio %.1f W: hottest %.1f C (%s)" % (sess, rad, t["T"], t["where"]))
    J("c2.json", res)
    W("c2.txt", L)
    # plot
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.0))
    rr = np.linspace(0.4, 1.6, 7)
    for sess, col in (("delta", S[0]), ("video", S[1])):
        for amb, ls_ in ((25.0, "-"), (30.0, "--")):
            ys = [C.c2_T(C.c2_q(sess, x, 1.0, "cells")[0], amb, False)["T"] for x in rr]
            axs[0].plot(rr, ys, color=col, ls=ls_, label="%s, %.0f C" % (sess, amb))
    axs[0].axhline(LIM, color=CRIT, lw=1.3)
    axs[0].text(0.42, LIM + 0.8, "36.2 C", color=CRIT, fontsize=8)
    axs[0].set_xlabel("radio domain at the Leaf, W")
    axs[0].set_ylabel("hottest face point, C (still air)")
    axs[0].set_title("C2: the L.6.0 body with the ring", fontsize=9, color=INK)
    axs[0].legend(fontsize=7)
    # right: Skin (C0/C1) against C2 across ambient, delta
    amb_f = np.arange(15, 36, 2.5)
    c0 = [C.skin_T(C.skin_q("delta_energy", 1.0, 0.25, "dist", "cells")[0], a, False)["T"] for a in amb_f]
    c2a = [C.c2_T(C.c2_q("delta", 0.4, 1.0, "cells")[0], a, False)["T"] for a in amb_f]
    c2b = [C.c2_T(C.c2_q("delta", 1.6, 1.0, "cells")[0], a, False)["T"] for a in amb_f]
    axs[1].plot(amb_f, c0, color=S[2], label="C0 and C1: Skin alone, delta 0.80 W + 0.25 W PHY")
    axs[1].plot(amb_f, c2a, color=S[0], label="C2: Leaf with ring, radio 0.4 W")
    axs[1].plot(amb_f, c2b, color=S[1], label="C2: Leaf with ring, radio 1.6 W")
    axs[1].axhline(LIM, color=CRIT, lw=1.3)
    axs[1].set_xlabel("ambient, C")
    axs[1].set_title("delta session, still air", fontsize=9, color=INK)
    axs[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "06_c2.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
if __name__ == "__main__":
    selfcheck()
    for f in (item1_2, item3, item4, item5, item6, item_c2):
        t = time.time()
        print("running", f.__name__, flush=True)
        f()
        print("   %.1f s" % (time.time() - t), flush=True)
    SUMMARY["runtime_s"] = round(time.time() - T0, 1)
    J("summary.json", SUMMARY)
    print("done in %.1f s" % SUMMARY["runtime_s"])
