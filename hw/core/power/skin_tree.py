#!/usr/bin/env python3
"""skin_tree.py - question 1 of the POWER seat: the Skin power tree, the Skin loads, the tier question.

Run:  python3 hw/core/power/skin_tree.py
Out:  out/skin_tree.json, out/skin_tree.txt, out/skin_loads.png, out/skin_bare.png
"""
import math

import numpy as np

import cpcommon as K

HC, TI = K.HC, K.TI
LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


def main():
    res = {}
    p("POWER seat · question 1 · the Skin power tree and the tier question")
    p("")
    # ------------------------------------------------------------ what stays and what moves
    stay = [
        ("micro-LED drivers, 200 x 200 px per tile", "VBUS 3.40 V floor", "stays: the emitters"),
        ("row and column address drivers, local 1.0 V buck per four tiles", "VBUS", "stays: the tile drivers"),
        ("tile hub: DSC decode, demura, 4 retimed ports (3 mW per tile)", "1.0 and 1.8 V", "stays: the minimal decoder, already in the tile [T] hw/display tile_spec.py"),
        ("AgNW touch front end", "1.8 V", "stays: touch"),
        ("hinge-angle sensor, seam strip, thermistor", "1.8 V", "stays"),
        ("seat controller SC, link receiver on D0 and D1, back channel", "VBUS or the sideband", "stays: the link PHY"),
        ("identity chip with the part record (law L9), no signing key", "1.8 V", "stays: identity, replaces U7 [H]"),
        ("U_Q x4 with the 3:1 SC stage", "VHV to VBUS", "stays only if the Skin takes VHV. Not needed if the Core regulates VBUS"),
        ("TCM per tile and the 128 cells", "VBUS", "LEAVE: the cells go to the Core, Buffer and Bare are options"),
        ("U1 TCON and compositor, U6 decoder and 16 MB store", "ring", "MOVE to the Core"),
        ("U2A, U2B, U5, U7, U8", "ring", "MOVE to the Core"),
        ("50 MP sensor, AF, OIS", "ring", "STAYS with the lens (BRIEF 4.3). Its processing moves"),
        ("rear AMOLED, flash, speaker, jack, microphones", "ring", "MOVE to the Core [H]"),
        ("B cell 0.144 Wh and U4", "ring", "MOVE to the Core. The Skin has no island rail"),
    ]
    p("WHAT STAYS ON THE SKIN AND WHAT MOVES (rows of hw/energy/03 section 1.1)")
    for a, b, c in stay:
        p("  %-66s %-22s %s" % (a, b, c))
    res["moves"] = stay
    p("")
    p("THE SKIN POWER TREE, rebuilt from hw/energy/03 for the Skin alone")
    for t in (
        "  CORE --- power ---> seat field leaves 2, 11 VBUS (or 5, 8 VHV) --- S_SEAT, dead-pad law of 03 section 3 ---+",
        "                                                                                                             v",
        "  VBUS grid, 3.40 to 4.48 V, regulated by the Core, no cell on it (a Bare store or a few cells are options)",
        "     |-- tile nodes: micro-LED drivers, row and column address (1.0 V buck per four tiles), AgNW touch, hinge sensor",
        "     |-- tile hub: DSC decode and 4 retimed ports (the minimal decoder, 3 mW per tile)",
        "     '-- seat tile: seat controller, link RX on D0 and D1, back channel BC, identity chip, edge router",
        "  CORE <--- pixels, D0 and D1, 2 pairs at 10 Gb/s ---> seat tile <--- touch, hinge angles, telemetry, BC ---> CORE",
        "  Gone from the Skin: U1 U6 U2A U2B U5 U7 U8 U3 U4, the B cell, the rear panel, the audio, the 128 cells (by default).",
    ):
        p(t)
    p("")

    # ------------------------------------------------------------ the loads
    p("THE SKIN LOAD PER USE CASE, W. Body column of hw/energy/04, plus the link and decoder assumed here. Low / nominal / high.")
    p("  assumptions: link RX 3 / 5 / 10 pJ/bit and 15 / 30 / 60 mW static; edge router 10 / 30 / 60 mW; touch 20 / 50 / 100 mW;")
    p("  identity 2 / 5 / 10 mW; back channel 5 / 10 / 20 mW; tile drivers at 0.92, local bucks at 0.88. All [HYPOTHESIS], the link seat refines them.")
    p("  %-42s %7s %7s | %7s %7s %7s | %6s | %s" % ("use case", "body", "addons", "low", "nom", "high", "Gb/s", "heat headroom still / wind (nom)"))
    table = {}
    for n in K.CASE_NAMES:
        lo, no, hi = K.skin_load(n, "low"), K.skin_load(n, "nom"), K.skin_load(n, "high")
        hd_s = K.LIMIT_STILL_W - no["skin_vbus_W"]
        hd_w = K.LIMIT_WIND_W - no["skin_vbus_W"]
        table[n] = dict(body_load_W=no["body_load_W"], addons_load_W=no["addons_load_W"], low=lo["skin_vbus_W"],
                        nom=no["skin_vbus_W"], high=hi["skin_vbus_W"], rate_Gbps=no["rate_Gbps"],
                        headroom_still=hd_s, headroom_wind=hd_w, detail=no)
        p("  %-42s %7.3f %7.3f | %7.3f %7.3f %7.3f | %6.2f | %+.2f / %+.2f" % (
            n, no["body_load_W"], no["addons_load_W"], lo["skin_vbus_W"], no["skin_vbus_W"], hi["skin_vbus_W"], no["rate_Gbps"], hd_s, hd_w))
    res["loads"] = table
    p("  Skin load is at the VBUS grid. It includes the 1/0.92 of the tile drivers. All of it is heat on the Skin.")
    v = table["video session, Wi-Fi"]
    d = table["delta session, 250 nits, Wi-Fi"]
    p("  Against the free-air ceiling of 1.73 W still and 2.37 W in a light wind [H] hw/hostpower/thermal:")
    p("    delta: %.2f W nominal, %.2f W high: passes still air by %.2f W (nominal) and %.2f W (high)" % (
        d["nom"], d["high"], K.LIMIT_STILL_W - d["nom"], K.LIMIT_STILL_W - d["high"]))
    p("    video: %.2f W nominal, %.2f W high: still air margin %+.2f W nominal and %+.2f W high; wind margin %+.2f and %+.2f W" % (
        v["nom"], v["high"], K.LIMIT_STILL_W - v["nom"], K.LIMIT_STILL_W - v["high"], K.LIMIT_WIND_W - v["nom"], K.LIMIT_WIND_W - v["high"]))
    body_v = 1.35 / K.ETA_TILE
    p("    the video body alone is %.2f W at VBUS, so the link, the decoder, the touch and the interface share %.2f W in still air" % (
        body_v, K.LIMIT_STILL_W - body_v))
    res["video_addon_budget_still_W"] = K.LIMIT_STILL_W - body_v
    p("")

    # ------------------------------------------------------------ the tier question
    loads = {
        "Lead delta body 0.80": 0.80,
        "Lead video body 1.35": 1.35,
        "Skin delta nominal": d["nom"],
        "Skin video nominal": v["nom"],
        "Skin safe screen nominal": table["safe screen, no link"]["nom"],
        "Skin outdoor video nominal": table["video outdoors, 800 nits, 5G"]["nom"],
    }
    res["tier_loads"] = loads
    gaps = HC.GAPS[:5]    # 0.1 s .. 5 min
    fill = 0.5
    margins = {"0.24 mm": 0.24, "0.04 mm": 0.04}
    vol_m = {k: TI.margin_volume(m, fill) for k, m in margins.items()}
    p("BARE STORE for the Skin loads: least volume in cm3, behind a 0.90 converter. 'x' means the ESR limits the power")
    p("  room: %.3f cm3 in the 0.24 mm margin, %.3f cm3 in the 0.04 mm margin (half of the 12 800 mm2 body); the cell layer, if freed, holds %.2f cm3 (128 tiles x %.4f cm3)" % (
        vol_m["0.24 mm"], vol_m["0.04 mm"], 128 * HC.CELL_VOL_MM3 / 1000.0, HC.CELL_VOL_MM3 / 1000.0))
    bare = {}
    for tk, t in TI.TECH.items():
        p("  %s" % tk)
        p("    %-28s" % "load" + "".join("%11s" % g for g, _ in gaps))
        bare[tk] = {}
        for ln, P in loads.items():
            row = []
            for gn, gs in gaps:
                vol = TI.cap_min_volume(t, P, gs)
                row.append(vol)
                bare[tk].setdefault(ln, {})[gn] = dict(
                    vol_cm3=vol,
                    tiles_cell_layer=None if vol is None else int(math.ceil(vol / (HC.CELL_VOL_MM3 / 1000.0))),
                    fits_0p24=bool(vol is not None and vol <= vol_m["0.24 mm"] and t["t_min_mm"] <= 0.24),
                    fits_0p04=bool(vol is not None and vol <= vol_m["0.04 mm"] and t["t_min_mm"] <= 0.04))
            p("    %-28s" % ln + "".join("%11s" % ("x" if x is None else "%.3g" % x) for x in row))
    res["bare"] = bare
    p("")
    p("DOES A CAPACITOR STORE FIT A MARGIN? (volume and thickness both)")
    ans = {}
    for tk, t in TI.TECH.items():
        for ln in ("Lead delta body 0.80", "Lead video body 1.35", "Skin video nominal"):
            for gn in ("0.1 s", "1 s", "3 s"):
                c = bare[tk][ln][gn]
                ans[(tk, ln, gn)] = c
    for ln in ("Lead delta body 0.80", "Lead video body 1.35", "Skin video nominal"):
        for gn in ("0.1 s", "1 s", "3 s"):
            f24 = [tk.split(" (")[0] for tk in TI.TECH if bare[tk][ln][gn]["fits_0p24"]]
            f04 = [tk.split(" (")[0] for tk in TI.TECH if bare[tk][ln][gn]["fits_0p04"]]
            v_edlc = bare["EDLC, large cell (Maxwell BCAP3000)"][ln][gn]
            v_chip = bare["EDLC, thin chip (Seiko CPH3225A)"][ln][gn]
            p("  %-24s %-5s: fits 0.24 mm: %-6s fits 0.04 mm: %-6s | volume only, large-cell density: 0.24 mm %s, 0.04 mm %s | cell layer tiles: large-cell %d, chip %d" % (
                ln, gn, ", ".join(f24) if f24 else "none", ", ".join(f04) if f04 else "none",
                "yes" if v_edlc["vol_cm3"] <= vol_m["0.24 mm"] else "no", "yes" if v_edlc["vol_cm3"] <= vol_m["0.04 mm"] else "no",
                v_edlc["tiles_cell_layer"], v_chip["tiles_cell_layer"]))
    p("")
    p("  The thinnest published EDLC is 0.9 mm and the thin solid-state cell cannot carry 0.8 W (100 ohm). So neither margin holds the store.")
    p("  The answer does not need the choice between 0.24 and 0.04 mm. It needs the cell layer (0.90 mm) to be free, and it is, with no cell.")
    p("  The one number the answer needs from FINAL/21 is the cell layer of 0.90 mm in 21.2.7, and the tile area of 10 x 10 mm.")
    p("")

    # ------------------------------------------------------------ the Buffer count for the Skin loads
    p("BUFFER for the Skin loads: least micro cells of the 128 (S cell, floated at 60 %, 3 C cap), gaps 3 s, 5 min, 30 min")
    buf = {}
    c = HC.CELLS["S"]
    for ln, P in loads.items():
        row = {}
        for gn, gs in (("3 s", 3.0), ("5 min", 300.0), ("30 min", 1800.0)):
            vf = TI.V_FLOOR if P > 0.1 else 3.0
            n, why = TI.min_cells(P, gs, c["E_target_Wh"], c["dcir"], TI.SOC_FLOAT, vf)
            row[gn] = dict(n=n, limit=why, Wh=None if n is None else n * c["E_target_Wh"])
        buf[ln] = row
        p("  %-28s " % ln + "   ".join("%s: %s cells (%s)" % (g, r["n"], r["limit"]) for g, r in row.items()))
    res["buffer"] = buf
    p("  Part 22 had 14 / 22 / 53 cells for 2.24 / 3.65 / 8.7 W at 3 s. The Skin needs 5 to 10 cells at the same gap (0.80 to 1.65 W).")
    p("")
    p("THE TIER VERDICT FOR A SKIN [HYPOTHESIS]")
    p("  1. Full: never. The Skin holds no energy of its own. No state lives on it, so a power gap loses no chain state.")
    p("  2. Buffer: not needed for continuity. A Skin without a Core shows nothing, because the pixels come from the Core.")
    p("  3. Buffer as an option: 5 cells (0.29 Wh) hold the safe screen for 30 min with no link. That is the 'never empty' Skin of BRIEF 4.1.")
    p("  4. Bare: yes, a store of 0.1 to 1 s rides a contact bounce or a cable re-seat. It needs the cell layer, not the margin.")
    p("  5. No cell at all: the default. The Skin goes dark in a gap and re-syncs when the link returns.")
    res["verdict"] = dict(full="never", buffer="option: 5 cells for a 30 min safe screen", bare="1 s store in the cell layer", default="no cell")
    K.dump("skin_tree", res, LINES)
    plots(table, bare, loads)


def plots(table, bare, loads):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = [n for n in K.CASE_NAMES if table[n]["nom"] > 0.05]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ys = np.arange(len(names))
    body = [table[n]["detail"]["body_vbus_W"] for n in names]
    add = [table[n]["detail"]["addons_vbus_W"] for n in names]
    cam = [table[n]["detail"]["camera_vbus_W"] for n in names]
    ax.barh(ys, body, color=K.PAL[0], height=0.6, label="tile drivers and emitters at VBUS")
    ax.barh(ys, add, left=body, color=K.PAL[1], height=0.6, label="link, router, touch, identity")
    ax.barh(ys, cam, left=[b + a for b, a in zip(body, add)], color=K.PAL[2], height=0.6, label="camera sensor")
    ax.axvline(K.LIMIT_STILL_W, color="#444", lw=1, ls=":")
    ax.axvline(K.LIMIT_WIND_W, color="#444", lw=1, ls="--")
    ax.text(K.LIMIT_STILL_W, -0.8, "1.73 W still", fontsize=8, ha="right")
    ax.text(K.LIMIT_WIND_W, -0.8, "2.37 W wind", fontsize=8, ha="left")
    ax.set_yticks(ys)
    ax.set_yticklabels([n.split(",")[0] for n in names], fontsize=8)
    ax.invert_yaxis()
    K.style(ax, "Skin load at the VBUS grid, W", "", "Skin load per use case, Leaf 160")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(K.OUT + "/skin_loads.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    gx = [g for g, _ in HC.GAPS[:5]]
    xs = np.arange(len(gx))
    tk = "EDLC, large cell (Maxwell BCAP3000)"
    for i, ln in enumerate(("Lead delta body 0.80", "Lead video body 1.35", "Skin video nominal", "Skin safe screen nominal")):
        ys = [bare[tk][ln][g]["vol_cm3"] for g in gx]
        ax.plot(xs, ys, "-o", color=K.PAL[i], lw=1.6, ms=4, label=ln)
    ax.set_yscale("log")
    for lab, m in (("0.24 mm margin", 0.24), ("0.04 mm margin", 0.04)):
        v = TI.margin_volume(m, 0.5)
        ax.axhline(v, color="#444", lw=1, ls=":")
        ax.text(0.0, v * 1.1, lab + " (volume only, EDLC is 0.9 mm thick)", fontsize=7)
    ax.set_xticks(xs)
    ax.set_xticklabels(gx)
    K.style(ax, "gap", "store volume, cm3", "Bare store for the Skin, large-cell EDLC")
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(K.OUT + "/skin_bare.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
