#!/usr/bin/env python3
"""mass.py - question 4 of the POWER seat: the mass of a Skin against the 68 g body plus the 10.8 g B module.

Sources: the L.6.0 B module bill of materials, HARDWARE/13 (10.80 g, [HYPOTHESIS] until weighed); the micro cell mass
0.114 g (hw/energy/01); the tile stack and its densities of hw/seam/kinematic_seat.py; the body figure 68 g of FINAL/21 and
HARDWARE/17 (stated). Every added part has its assumption in the code.

Run:  python3 hw/core/power/mass.py   (after core_energy.py)
Out:  out/mass.json, out/mass.txt, out/mass.png
"""
import math

import numpy as np

import cpcommon as K
import core_energy as CE

HC = K.HC
LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


# the B module bill of materials of HARDWARE/13 section 2: (no, name, g, where it goes in the Split)
BOM = [
    (1, "bar shell", 0.20, "core"), (2, "A1 and A2 antennas", 0.02, "core"), (3, "A4 60 GHz array", 0.05, "core"),
    (4, "body-link leaves", 0.08, "core"), (5, "corner flex", 0.10, "core"), (6, "ring shell", 2.20, "core"),
    (7, "front sapphire window", 0.54, "lens"), (8, "rear sapphire window", 0.54, "core"), (9, "rear AMOLED", 0.25, "core"),
    (10, "Cu-graphite shield", 0.15, "core"), (11, "camera column", 0.45, "lens"), (12, "LED flash", 0.10, "core"),
    (13, "micro-speaker", 0.60, "core"), (14, "two microphones", 0.06, "core"), (15, "ring PCBA", 1.40, "core"),
    (16, "U1 TCON and compositor", 0.10, "core"), (17, "U2A Wi-Fi 7", 0.10, "core"), (18, "U2B 60 GHz and UWB", 0.10, "core"),
    (19, "U5 5G modem", 0.50, "core"), (20, "U6 decoder and frame store", 0.15, "core"), (21, "U7 secure element", 0.02, "core"),
    (22, "U8 IMU", 0.02, "core"), (23, "U3 codec and U4 power chip", 0.10, "core"), (24, "A3 ring loop", 0.02, "core"),
    (25, "aperture tuners", 0.03, "core"), (26, "3.5 mm jack", 0.30, "core"), (27, "cell multiplexer", 0.03, "gone"),
    (28, "seat magnets", 0.34, "core"), (29, "B cell", 0.60, "gone"), (30, "gaskets", 0.25, "core"),
    (31, "spreader and latent buffer", 1.10, "core"), (32, "shield cans", 0.30, "core"),
]
BOM_TOTAL = sum(b[2] for b in BOM)
CELL_G = HC.CELLS["S"]["mass_g"]          # 0.114 g
N_CELL = 128
DENS = {"PC cap + AgNW": 1.2, "OCA": 1.0, "glass-LED-glass": 2.45, "slip OCA": 1.0, "Qi coil / spreader": 4.0,
        "micro cell": 2.6, "hinge routing + tolerance": 1.5, "floating back skin": 1.1}   # g/cm3, hw/seam/kinematic_seat.py [H]
STACK = [("PC cap + AgNW", 0.25), ("OCA", 0.05), ("glass-LED-glass", 0.25), ("slip OCA", 0.03),
         ("Qi coil / spreader", 0.20), ("micro cell", 0.90), ("hinge routing + tolerance", 0.24), ("floating back skin", 0.08)]


def tile_layers():
    out = {}
    for nm, t in STACK:
        area = 9.25 ** 2 if nm == "micro cell" else 100.0
        out[nm] = t * area * DENS[nm] * 1e-3
    return out


def main():
    p("POWER seat · question 4 · the mass of a Skin")
    L60_BODY, L60_B = 68.0, 10.8
    L60 = L60_BODY + L60_B
    p("L.6.0 device: body %.1f g (stated, FINAL/21) + B module %.2f g (HARDWARE/13 BOM, summed %.2f g) = %.1f g" % (L60_BODY, L60_B, BOM_TOTAL, L60))
    tl = tile_layers()
    tile_seam = sum(tl.values())
    tile_fix = tile_seam - tl["micro cell"] + CELL_G
    p("bottom-up check of the body from the tile stack: seam team densities give %.3f g per tile, %.1f g for 128; with the cell at 0.114 g (hw/energy/01) %.3f g per tile, %.1f g" % (
        tile_seam, 128 * tile_seam, tile_fix, 128 * tile_fix))
    p("  so the stated 68 g leaves %.1f g for hinges, seam lips, 16 magnets, U_Q, TCM, ribbons and edges. The 68 g is a carry-over of the L.5.0 body [H], not a L.6.0 weighing." % (L60_BODY - 128 * tile_fix))
    res = {"L60_g": L60, "tile_g": tile_fix, "tile_layers_g": tl, "bom_total_g": BOM_TOTAL}
    p("")
    # ------------------------------------------------------------ what leaves the body and the module
    cells_g = N_CELL * CELL_G
    tcm_g = 128 * 0.0005         # TCM and fuse neck per tile, WLCSP 0.9 x 0.7 x 0.15 mm plus the neck [H]
    coil_g = 128 * tl["Qi coil / spreader"]
    spreader_g = 128 * (100.0 * 0.10 * 2.2 * 1e-3)       # a 0.10 mm graphite spreader keeps the heat path [H]
    p("WHAT LEAVES")
    p("  the 128 cells: %.1f g (%.4f g each, %.2f Wh at 750 Wh/L)" % (cells_g, CELL_G, 128 * HC.CELLS["S"]["E_target_Wh"]))
    p("  TCM and fuse necks: %.2f g [H]" % tcm_g)
    p("  the B module: %.1f g. Of it the lens parts (camera column, one window) %.2f g can stay on the Skin as a camera pod" % (
        L60_B, sum(b[2] for b in BOM if b[3] == "lens")))
    p("  the Qi coil and shield layer: %.1f g by the seam stack. A 0.10 mm graphite spreader replaces it: %.1f g, so %.1f g saved if power comes by pads" % (
        coil_g, spreader_g, coil_g - spreader_g))
    p("")
    # ------------------------------------------------------------ the Skin variants
    add_core_iface = 0.15          # identity chip, link PHY, edge router, seat pads [H]
    bare_g = 0.20                  # a chip EDLC store of 0.1 to 1 s: 0.1 to 0.2 cm3 at 1.0 g/cm3 [H]
    buf5_g = 5 * CELL_G
    camera_pod = 0.45 + 0.54 + 0.05 + 0.20     # sensor column, one window, flex, shell [H]
    variants = {
        "S0 no cell, Qi coil kept": L60_BODY - cells_g - tcm_g + add_core_iface,
        "S1 no cell, no coil (pads power)": L60_BODY - cells_g - tcm_g + add_core_iface - (coil_g - spreader_g),
    }
    variants["S2 S1 + Bare store (1 s)"] = variants["S1 no cell, no coil (pads power)"] + bare_g
    variants["S3 S1 + 5 cell Buffer (safe screen 30 min)"] = variants["S1 no cell, no coil (pads power)"] + buf5_g
    variants["S4 S1 + camera pod"] = variants["S1 no cell, no coil (pads power)"] + camera_pod
    variants["S5 S0 + camera pod + 5 cell Buffer"] = variants["S0 no cell, Qi coil kept"] + camera_pod + buf5_g
    p("THE SKIN, g (stated 68 g body basis), against the L.6.0 device of %.1f g" % L60)
    out = {}
    for k, m in variants.items():
        out[k] = dict(g=m, saved_g=L60 - m, saved_pct=100 * (L60 - m) / L60,
                      thickness_mm=2.00 - 0.90 - (0.20 - 0.10 if "no coil" in k or "S2" in k or "S3" in k or "S4" in k else 0.0))
        p("  %-46s %6.1f g   saves %5.1f g (%4.1f %%)   body thickness %.2f mm" % (k, m, out[k]["saved_g"], out[k]["saved_pct"], out[k]["thickness_mm"]))
    res["skin"] = out
    p("  The bottom-up basis gives the same saving. The saving is the parts that leave, %.1f g of cells and TCM, %.1f g of B module, %.1f g of coil, less %.2f g added." % (
        cells_g + tcm_g, L60_B, coil_g - spreader_g, add_core_iface))
    p("  The Skin is lighter by 25 to 33 g, that is 32 to 41 percent. The cells leave the Skin by default. The camera pod costs %.1f g." % camera_pod)
    p("")
    # ------------------------------------------------------------ the Core
    core_elec = sum(b[2] for b in BOM if b[3] == "core" and b[0] not in (1, 2, 3, 4, 5, 6, 28, 30))   # parts that carry over, without the old shell
    p("THE CORE, g. Electronics, radios, audio, rear panel, spreader that carry over from the B module: %.2f g (BOM rows, shell and magnets not counted)" % core_elec)
    p("  the Core adds a housing, a large antenna set and the energy. Assumptions [H]: housing 0.35 x (electronics + cells), pack structure 1.3 x cell mass at 574 Wh/kg")
    core = {}
    for n in (1, 2, 4, 8):
        mix = ["Leaf 160"] * n
        r = CE.core_power(mix, "delta")
        for hrs in (3.0, 8.0):
            wh = r["bus_W"] * hrs / (0.96 * 0.97)
            cells = wh / 574.0 * 1000.0 * 1.3
            elec = core_elec + 0.30 * (n - 1)          # one more hub and link TX share per Skin [H]
            housing = max(8.0, 0.35 * (elec + cells))
            total = elec + cells + housing
            core.setdefault("N%d" % n, {})["%g h" % hrs] = dict(Wh=wh, cells_g=cells, elec_g=elec, housing_g=housing, total_g=total)
    for n in (1, 2, 4, 8):
        p("  N=%d: " % n + "   ".join("%s: %.1f Wh, cells %.0f g, electronics %.1f g, housing %.0f g, total %.0f g" % (
            h, v["Wh"], v["cells_g"], v["elec_g"], v["housing_g"], v["total_g"]) for h, v in core["N%d" % n].items()))
    res["core"] = core
    p("")
    p("THE SYSTEM, Leaf 160 Skins on one Core (Core sized for 3 h at the delta class, the runtime of the Leaf Full cell), against N L.6.0 devices")
    sysm = {}
    s1 = variants["S1 no cell, no coil (pads power)"]
    s0 = variants["S0 no cell, Qi coil kept"]
    for n in (1, 2, 4, 8):
        c = core["N%d" % n]["3 h"]["total_g"]
        sysm["N%d" % n] = dict(system_S1_g=n * s1 + c, system_S0_g=n * s0 + c, leaves_g=n * L60, core_g=c)
        p("  N=%d: %d Skins S1 %.0f g + Core %.0f g = %.0f g (S0: %.0f g) against %d Leaves %.0f g; %+.0f %%" % (
            n, n, n * s1, c, n * s1 + c, n * s0 + c, n, n * L60, 100 * ((n * s1 + c) / (n * L60) - 1)))
    res["system"] = sysm
    # break-even N
    ne = None
    for n in range(1, 30):
        mix = ["Leaf 160"] * n
        r = CE.core_power(mix, "delta")
        wh = r["bus_W"] * 3.0 / (0.96 * 0.97)
        cells = wh / 574.0 * 1000.0 * 1.3
        elec = core_elec + 0.30 * (n - 1)
        c = elec + cells + max(8.0, 0.35 * (elec + cells))
        if n * s1 + c < n * L60 and ne is None:
            ne = n
    p("  break-even on mass: the Split system is lighter than N Leaves from N = %s Skins on one Core" % ne)
    res["break_even_N"] = ne
    n1 = sysm["N1"]
    p("  At N = 1 the pair is %+.0f percent (S1) or %+.0f percent (S0) against one Leaf: the energy and the electronics sit in the Core." % (
        100 * (n1["system_S1_g"] / n1["leaves_g"] - 1), 100 * (n1["system_S0_g"] / n1["leaves_g"] - 1)))
    p("  A Skin worn alone is lighter by 25 to 33 g. The mass gain of the system starts at N = %s." % ne)
    K.dump("mass", res, LINES)
    plots(out, L60)


def plots(out, L60):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    names = ["L.6.0 device"] + list(out.keys())
    vals = [L60] + [v["g"] for v in out.values()]
    ys = np.arange(len(names))
    ax.barh(ys, vals, color=[K.PAL[6]] + [K.PAL[0]] * len(out), height=0.6)
    for i, v in enumerate(vals):
        ax.text(v + 0.6, i, "%.1f g" % v, va="center", fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 95)
    K.style(ax, "mass, g", "", "Skin mass against the L.6.0 device (body 68 g plus B module 10.8 g)")
    fig.tight_layout()
    fig.savefig(K.OUT + "/mass.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
