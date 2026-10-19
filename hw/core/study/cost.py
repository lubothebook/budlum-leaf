#!/usr/bin/env python3
"""cost.py - the BOM model of the Split: an L.6.0 Leaf against a Skin plus a Core.

Study seat, block HP-2. It imports program/budget.py read only and reuses its
tables (display, cells, other blocks, royalty). It changes none of them. Every
number that budget.py does not hold is a [HYPOTHESIS] with a low, base and high
value in PARAMS below, and the sweep samples all of them.

Run:   python3 cost.py            (about 20 s)
Out:   out/cost_table.txt, out/sweep.txt, out/tornado.txt, out/cost.json,
       out/breakeven.png

Terms. "aio" is the all-in-one L.6.0 Leaf of program/budget.py (body plus B
module). "Skin" is the surface. "Core" is the hardware. Cost is BOM USD per
unit, at a volume per year, before margin. The model never prices the margin.
"""
import json
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True          # write nothing outside this directory
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "program"))
import budget as B                      # noqa: E402  read only

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

VOLS = B.VOLUMES                       # 100 000, 1 000 000, 5 000 000 per year
VOLF = {100_000: 1.5, 1_000_000: 1.0, 5_000_000: 0.8}   # [HYPOTHESIS] Core parts scale

# --------------------------------------------------------------------- sizes
# (pixel factor, tile factor, label). The reference is the Leaf 160, 128 tiles.
# [TREE] FINAL/01 Section 1.2. Leaf 480 uses T40 B tiles at 152 ppi: 72 tiles of
# 240 x 240 px. Its emitter cost per million is [HYPOTHESIS] the same as P160.
SIZES = {
    "Leaf 80":   (0.50, 0.50),
    "Leaf 160":  (1.00, 1.00),
    "Leaf 160x2": (2.00, 2.00),    # Leaf 160 squared, 160 x 160 mm
    "Leaf 480":  (72 * 240 * 240 / (3200 * 1600), 72 / 128.0),
}

# Block names of program/budget.py OTHER. They are the keys, not copies.
K_MECH = "tile mechanics: PC caps, hinges, skin, seats, magnets, 128 tiles"
K_TCM = "TCM protection IC x 128"
K_QI = "Qi2.2 sector coils, shield, rectifier"
K_TOUCH = "touch grid, AgNW, on the caps"
K_ASIC = "U1 and U6 ASICs with 16 MB store"
K_MODEM = "U5 5G modem SiP with RF front end and eSIM"
K_WIFI = "U2A Wi-Fi 7 and BT 6.0, U2B 60 GHz and UWB"
K_MISC = "U7 secure element, U8 IMU, U3 audio, U4 power, NOR"
K_CAM = "50 MP camera column with sapphire L1"
K_BMECH = "B module mechanics: LCP shells, LDS, windows, jack, speaker, mics"
K_AMOLED = "rear round AMOLED"
K_RING = "ring PCBA, 8-layer HDI, assembly"
K_BCELL = "B cell 0.14 Wh"
K_ASM = "final assembly, calibration, test, provisioning"
K_PACK = "packaging, logistics, warranty reserve 3 %"

# --------------------------------------------------------------- parameters
# name: (low, base, high, unit, note). All [HYPOTHESIS] of the study seat.
PARAMS = {
    "f_dec_skin":   (0.40, 0.60, 0.85, "share", "share of U1 and U6 cost that stays in the Skin (minimal decoder)"),
    "lane_extra":   (0.10, 0.25, 0.45, "share", "extra Core silicon per added Skin, as a share of U1 and U6"),
    "misc_core":    (0.60, 0.70, 0.85, "share", "share of the U7, U8, U3, U4 bundle that moves to the Core"),
    "ident_usd":    (0.60, 1.00, 2.00, "USD", "identity chip in each Skin, at 1 M per year"),
    "bmech_skin":   (0.30, 0.50, 0.80, "share", "share of B module mechanics that stays on the Skin with the camera"),
    "core_pcb_x":   (1.20, 1.60, 2.50, "x ring PCBA", "Core board against the L.6.0 ring PCBA"),
    "core_encl":    (6.0, 12.0, 22.0, "USD", "Core enclosure and seals, at 1 M per year"),
    "core_hours":   (2.5, 3.0, 4.0, "h", "session the Core energy must carry"),
    "core_w_skin":  (0.20, 0.40, 0.80, "W", "added Core silicon power per Skin (encode and link)"),
    "core_cell_wh": (0.35, 0.70, 1.30, "USD/Wh", "conventional Core cell with its pack, at 1 M per year"),
    "core_bms":     (1.5, 2.5, 4.0, "USD", "Core protection and gauge"),
    "asm_x":        (0.50, 0.60, 0.80, "x", "assembly and test of a Skin or a Core against the L.6.0 unit"),
    "cable_usd":    (3.0, 6.0, 12.0, "USD", "tether cable and connector pair, at 1 M per year"),
    "phy_usd":      (3.0, 5.0, 9.0, "USD", "wired link chip at one end, at 1 M per year"),
    "radio_usd":    (10.0, 18.0, 32.0, "USD", "60 GHz radio with antenna at one end, at 1 M per year"),
    "skin_wh":      (1.5, 2.5, 4.0, "Wh", "Skin cell for a wireless Skin"),
    "radio_gbps":   (10.0, 14.0, 20.0, "Gb/s", "usable rate of one 60 GHz link"),
    "pixel_gbps":   (6.1, 9.2, 13.43, "Gb/s", "pixel stream of a Leaf 160 after compression"),
    "nre_extra":    (25.0, 40.0, 70.0, "M USD", "extra NRE of the Split: Skin ASIC, link, Core board"),
    "cell_wh_kg":   (200.0, 250.0, 300.0, "Wh/kg", "Core pack energy per kilogram"),
    "wifi_skin":    (0.50, 0.60, 0.75, "share", "C1: share of the Wi-Fi 7, BT, UWB bundle that stays in the Skin"),
    "enc_base":     (0.20, 0.30, 0.50, "share", "C1: Core slice encoder as a share of U1 and U6, for one Skin"),
    "c1_gbps":      (0.15, 0.40, 1.00, "Gb/s", "C1: slice stream per Skin (Part 21 design, tens to about 150 Mbit/s plus margin)"),
    "ap_gbps":      (2.0, 3.0, 4.0, "Gb/s", "C1: usable rate of one Wi-Fi 7 access radio in the Core"),
    "skin_wh_c1":   (2.0, 3.5, 5.5, "Wh", "C1: Skin cell, since the Skin runs its own decoder and radio"),
}
RADIO_W = (1.0, 2.0, 3.5)       # W per 60 GHz end, [HYPOTHESIS], used in the heat note only
PHY_W = (0.2, 0.4, 0.8)         # W per wired link end, [HYPOTHESIS]
WIFI_DEC_W = (0.6, 1.0, 1.6)    # W for Wi-Fi 7, decoder and frame store in a C1 Skin, [HYPOTHESIS]
SKIN_VIDEO_W = 1.35             # [TREE] hw/energy/04, body column, video session
SKIN_DELTA_W = 0.80             # [TREE] same, delta session
FREE_AIR_W = (1.73, 2.37)       # [TREE] BRIEF Section 3, hw/hostpower/thermal: still, light wind


def lmh(t, u):
    """Piecewise linear value of a (low, base, high) triple. u in [0, 1]."""
    lo, ba, hi = t[0], t[1], t[2]
    return lo + (ba - lo) * (u / 0.5) if u <= 0.5 else ba + (hi - ba) * ((u - 0.5) / 0.5)


def tri(vol, tbl, u):
    return lmh(tbl[vol], u)


class Draw:
    """One draw of every uncertain term. u in [0, 1]: 0 low, 0.5 base, 1 high."""

    def __init__(self, rng=None):
        keys = ["disp", "cell", "sil", "cam", "mech", "asm", "roy"]
        self.u = {k: (0.5 if rng is None else rng.random()) for k in keys}
        self.p = {k: (v[1] if rng is None else v[0] + rng.random() * (v[2] - v[0]))
                  for k, v in PARAMS.items()}
        self.tile_x = 1.0           # multiplier on the micro-LED tile cost, for the what-if sweep


# ------------------------------------------------------------ budget lines
def blocks(vol, d):
    """The L.6.0 unit cost lines at the draw d, with display and cells per unit."""
    u = d.u
    emitters = B.PIX_PER_TILE * B.SUBPIX
    chips = emitters / 1e6 * tri(vol, B.CHIP_USD_PER_M, u["disp"])
    uics = B.UIC_PER_TILE / 1e6 * tri(vol, B.UIC_USD_PER_M, u["disp"])
    glass = tri(vol, B.GLASS_TGV_PER_TILE, u["disp"])
    # tile yield runs high to low as the draw runs low to high
    y = tri(vol, B.TILE_YIELD, u["disp"])
    tile = (chips + uics + glass) / y * d.tile_x
    cell1 = B.CELL_WH * tri(vol, B.CELL_USD_PER_WH, u["cell"]) + tri(vol, B.CELL_FIXED, u["cell"])
    g = {"u_sil": u["sil"], "u_cam": u["cam"], "u_mech": u["mech"], "u_asm": u["asm"]}
    O = B.OTHER
    line = {
        "tile": tile,                       # per tile
        "cell1": cell1,                     # per micro cell
        K_MECH: tri(vol, O[K_MECH], g["u_mech"]),
        K_TCM: tri(vol, O[K_TCM], g["u_mech"]),
        K_QI: tri(vol, O[K_QI], g["u_mech"]),
        K_TOUCH: tri(vol, O[K_TOUCH], g["u_mech"]),
        K_ASIC: tri(vol, O[K_ASIC], g["u_sil"]),
        K_MODEM: tri(vol, O[K_MODEM], g["u_sil"]),
        K_WIFI: tri(vol, O[K_WIFI], g["u_sil"]),
        K_MISC: tri(vol, O[K_MISC], g["u_sil"]),
        K_CAM: tri(vol, O[K_CAM], g["u_cam"]),
        K_BMECH: tri(vol, O[K_BMECH], g["u_mech"]),
        K_AMOLED: tri(vol, O[K_AMOLED], g["u_mech"]),
        K_RING: tri(vol, O[K_RING], g["u_mech"]),
        K_BCELL: tri(vol, O[K_BCELL], g["u_cell"] if "u_cell" in g else u["cell"]),
        K_ASM: tri(vol, O[K_ASM], g["u_asm"]),
        K_PACK: tri(vol, O[K_PACK], g["u_asm"]),
    }
    line["roy_pct"] = lmh(B.ROYALTY_PCT, u["roy"])
    return line


def aio(vol, d, size="Leaf 160"):
    """The all-in-one L.6.0 Leaf of a size. Sub-total and total with royalties."""
    px, tl = SIZES[size]
    L = blocks(vol, d)
    lines = {
        "micro-LED tiles": L["tile"] * 128 * px,
        "micro cells": L["cell1"] * 128 * (1.0 if size == "Leaf 480" else tl),
        K_MECH: L[K_MECH] * tl, K_TCM: L[K_TCM] * tl, K_TOUCH: L[K_TOUCH] * tl,
        K_QI: L[K_QI], K_ASIC: L[K_ASIC], K_MODEM: L[K_MODEM], K_WIFI: L[K_WIFI],
        K_MISC: L[K_MISC], K_CAM: L[K_CAM], K_BMECH: L[K_BMECH], K_AMOLED: L[K_AMOLED],
        K_RING: L[K_RING], K_BCELL: L[K_BCELL], K_ASM: L[K_ASM], K_PACK: L[K_PACK],
    }
    sub = sum(lines.values())
    lines["royalties"] = sub * L["roy_pct"]
    return dict(lines=lines, sub=sub, total=sub + lines["royalties"])


# ------------------------------------------------------------------- the Skin
def skin(vol, d, size="Leaf 160", link="wired", camera=True):
    """BOM of one Skin. Returns the lines, the sub-total and the royalty-free total."""
    px, tl = SIZES[size]
    p, L = d.p, blocks(vol, d)
    vf = VOLF[vol]
    dec_share = 1.0 if link == "wifi" else p["f_dec_skin"]
    lines = {
        "micro-LED tiles": L["tile"] * 128 * px,
        K_MECH: L[K_MECH] * tl, K_TOUCH: L[K_TOUCH] * tl,
        "decoder and TCON, Skin share": (L[K_ASIC]) * dec_share,
        "identity chip": p["ident_usd"] * vf,
        "IMU and Skin misc": L[K_MISC] * (1 - p["misc_core"]),
    }
    if camera:
        lines[K_CAM] = L[K_CAM]
        lines["B stub mechanics"] = L[K_BMECH] * p["bmech_skin"]
    if link == "wired":
        lines["tether cable"] = p["cable_usd"] * vf
        lines["link chip, Skin end"] = p["phy_usd"] * vf
    elif link == "wifi":
        lines["Wi-Fi 7, BT, UWB, Skin share"] = L[K_WIFI] * p["wifi_skin"]
        n_cell = max(1, math.ceil(p["skin_wh_c1"] / B.CELL_WH))
        lines["Skin cells"] = n_cell * L["cell1"]
        lines["Skin TCM"] = L[K_TCM] * n_cell / 128.0
        lines["Skin Qi coil"] = L[K_QI]
    else:
        lines["60 GHz radio, Skin end"] = p["radio_usd"] * vf
        n_cell = max(1, math.ceil(p["skin_wh"] / B.CELL_WH))
        lines["Skin cells"] = n_cell * L["cell1"]
        lines["Skin TCM"] = L[K_TCM] * n_cell / 128.0
        lines["Skin Qi coil"] = L[K_QI]
    lines["assembly and pack"] = (L[K_ASM] + L[K_PACK]) * p["asm_x"]
    sub = sum(lines.values())
    return dict(lines=lines, sub=sub)


# -------------------------------------------------------------------- the Core
def core_watts(d, n):
    return 1.92 + p_skin_w() * n + d.p["core_w_skin"] * n


def p_skin_w():
    return 1.35        # [TREE] hw/energy/04 body column, video session


def core(vol, d, n, link="wired"):
    """BOM of one Core that serves n Skins of a Leaf 160 class. Sub-total only."""
    p, L = d.p, blocks(vol, d)
    vf = VOLF[vol]
    asic = L[K_ASIC]
    if link == "wifi":
        core_dec = asic * p["enc_base"]
        n_ap = max(1, math.ceil(n * p["c1_gbps"] / p["ap_gbps"]))
        core_wifi = L[K_WIFI] + L[K_WIFI] * p["wifi_skin"] * (n_ap - 1)
    else:
        core_dec = asic * (1 - p["f_dec_skin"])
        core_wifi = L[K_WIFI]
    lines = {
        "decoder and compositor, Core share": core_dec,
        "extra Skin lanes": asic * p["lane_extra"] * (n - 1),
        "5G modem SiP": L[K_MODEM],
        "Wi-Fi 7, BT, UWB": core_wifi,
        "secure element and misc, Core share": L[K_MISC] * p["misc_core"],
        "Core board": L[K_RING] * p["core_pcb_x"],
        "Core enclosure": p["core_encl"] * vf,
        "rear status display": L[K_AMOLED],
        "Qi2.2 coil for the Core": L[K_QI],
    }
    if link == "wired":
        wh = p["core_hours"] * core_watts(d, n)
        lines["link chip, Core end"] = p["phy_usd"] * vf * n
    elif link == "wifi":
        wh = p["core_hours"] * (1.92 + p["core_w_skin"] * n)
    else:
        wh = p["core_hours"] * (1.92 + p["core_w_skin"] * n)
        n_rad = math.ceil(n * p["pixel_gbps"] / p["radio_gbps"])
        lines["60 GHz radios, Core"] = p["radio_usd"] * vf * max(n, n_rad)
    lines["Core energy"] = wh * p["core_cell_wh"] * vf + p["core_bms"]
    lines["assembly and pack"] = (L[K_ASM] + L[K_PACK]) * p["asm_x"]
    sub = sum(lines.values())
    return dict(lines=lines, sub=sub, wh=wh)


def system(vol, d, skins, link="wired", royalty="system", camera=True):
    """Split cost of a Core plus a list of Skins against the same Leaves all-in-one."""
    n = len(skins)
    c = core(vol, d, n, link)
    s_list = [skin(vol, d, z, link, camera) for z in skins]
    pct = blocks(vol, d)["roy_pct"]
    base = c["sub"] + sum(s["sub"] for s in s_list) if royalty == "system" else c["sub"]
    roy = base * pct
    split = c["sub"] + sum(s["sub"] for s in s_list) + roy
    a_list = [aio(vol, d, z) for z in skins]
    all_in = sum(a["total"] for a in a_list)
    return dict(core=c, skins=s_list, aio=a_list, split=split, all_in=all_in,
                saving=all_in - split, roy=roy)


def breakeven(vol, d, link="wired", royalty="system", size="Leaf 160", nmax=16):
    for n in range(1, nmax + 1):
        r = system(vol, d, [size] * n, link, royalty)
        if r["saving"] > 0:
            return n
    return None


# ---------------------------------------------------------- mass and thickness
def mass_and_stack(d):
    """Skin mass and thickness against the L.6.0 body. [HYPOTHESIS] densities."""
    p = d.p
    body_g = 68.0                              # [TREE] FINAL/00 answer 19
    cell_vol_cm3 = 9.25 * 9.25 * 0.90 / 1000.0
    cells_g = 128 * cell_vol_cm3 * 2.5         # [GENERAL] cell density 2.3 to 3.0 g/cm3
    qi_g = 3.0                                 # [HYPOTHESIS] sector coils and shield
    skin_g = body_g - cells_g - qi_g
    stack_mm = 2.00 - 0.90 - 0.20              # [TREE] FINAL/21 stack: cell 0.90, coil 0.20
    return dict(body_g=body_g, cells_g=cells_g, skin_g=skin_g, stack_mm=stack_mm)


def core_mass(d, n):
    wh = core(1_000_000, d, n)["wh"]
    return wh / d.p["cell_wh_kg"] * 1000.0 + 25.0 + 45.0   # cells, board, enclosure [HYPOTHESIS]


# ------------------------------------------------------------------- reports
def fmt_lines(lines, total=None, w=64):
    out = []
    for k, v in lines.items():
        out.append("   %-*s %9.2f" % (w, k[:w], v))
    return "\n".join(out)


def tables():
    d = Draw()
    t = []
    P = t.append
    P("COST OF THE SPLIT, base draw. BOM USD per unit, no margin. All [HYPOTHESIS].")
    P("L.6.0 numbers come from program/budget.py, read only.\n")
    for vol in VOLS:
        a = aio(vol, d)
        P("== volume %s per year" % format(vol, ","))
        P("all-in-one Leaf 160, L.6.0: %.0f USD (budget.py base: %.0f)" % (
            a["total"], B.unit_cost()[vol]["base"]["total"]))
        a_lines = a["lines"]
        disp = a_lines["micro-LED tiles"]
        P("   micro-LED tiles %.0f USD = %.0f %% of the unit; cells %.0f USD = %.0f %%" % (
            disp, 100 * disp / a["total"], a_lines["micro cells"], 100 * a_lines["micro cells"] / a["total"]))
        for link in ("wired", "wireless"):
            s = skin(vol, d, "Leaf 160", link)
            sn = skin(vol, d, "Leaf 160", link, camera=False)
            P(" -- link %s" % link)
            P("   Skin Leaf 160 with camera: %.0f USD sub-total; without camera: %.0f USD" % (s["sub"], sn["sub"]))
            P(fmt_lines(s["lines"]))
            for n in (1, 2, 4, 8):
                c = core(vol, d, n, link)
                r = system(vol, d, ["Leaf 160"] * n, link, "system")
                r2 = system(vol, d, ["Leaf 160"] * n, link, "core")
                P("   N=%d Core %.0f USD (%.1f Wh) | split %.0f vs all-in-one %.0f | saving %.0f USD (%.1f %%) | royalty on Core only: saving %.0f USD" % (
                    n, c["sub"], c["wh"], r["split"], r["all_in"], r["saving"], 100 * r["saving"] / r["all_in"], r2["saving"]))
            P("   break-even Skins per Core: royalty on system %s, on Core only %s" % (
                breakeven(vol, d, link, "system"), breakeven(vol, d, link, "core")))
        P("")
    vol = 1_000_000
    P("== Core lines, N=4, wired, 1 M per year")
    P(fmt_lines(core(vol, d, 4, "wired")["lines"]))
    P("\n== mixed sizes, 1 M per year, base draw")
    mixes = {
        "1 x Leaf 160": ["Leaf 160"],
        "2 x Leaf 80 + 1 x Leaf 160": ["Leaf 80", "Leaf 80", "Leaf 160"],
        "Leaf 80 + Leaf 160 + Leaf 160x2": ["Leaf 80", "Leaf 160", "Leaf 160x2"],
        "Leaf 80 + Leaf 160 + Leaf 160x2 + Leaf 480": ["Leaf 80", "Leaf 160", "Leaf 160x2", "Leaf 480"],
        "2 x Leaf 160 + 1 x Leaf 480": ["Leaf 160", "Leaf 160", "Leaf 480"],
        "4 x Leaf 160": ["Leaf 160"] * 4,
        "8 x Leaf 80": ["Leaf 80"] * 8,
    }
    for name, z in mixes.items():
        for link in ("wired", "wireless"):
            r = system(vol, d, z, link, "system")
            P("   %-46s %-8s split %7.0f  all-in-one %7.0f  saving %6.0f (%5.1f %%)  Core %5.0f" % (
                name, link, r["split"], r["all_in"], r["saving"], 100 * r["saving"] / r["all_in"], r["core"]["sub"]))
    P("\n== Skin cost by size, 1 M per year, wired, with camera")
    for z in SIZES:
        s = skin(vol, d, z, "wired")
        a = aio(vol, d, z)
        P("   %-12s Skin %7.0f  all-in-one %7.0f  Skin share %5.1f %%  tiles in Skin %5.1f %%" % (
            z, s["sub"], a["total"], 100 * s["sub"] / a["total"], 100 * s["lines"]["micro-LED tiles"] / s["sub"]))
    m = mass_and_stack(d)
    P("\n== mass and thickness of the Skin (L.6.0 body %.1f g, 2.00 mm)" % m["body_g"])
    P("   cells %.1f g, Qi layer 3 g, Skin about %.1f g (%.0f %% lighter), stack %.2f mm" % (
        m["cells_g"], m["skin_g"], 100 * (m["body_g"] - m["skin_g"]) / m["body_g"], m["stack_mm"]))
    for n in (1, 2, 4, 8):
        P("   Core N=%d: %.1f Wh, about %.0f g" % (n, core(vol, d, n)["wh"], core_mass(d, n)))
    P("")
    P(class_report(vol))
    P("")
    P(delta_table(vol, d))
    P("")
    P(heat_note())
    P("")
    P(tile_sweep(vol))
    P("")
    P(size_break_even(vol))
    # the extra NRE
    nre_extra = PARAMS["nre_extra"][1]
    P("\n== the extra NRE of the Split, base %.0f M USD" % nre_extra)
    for n in (2, 4, 8):
        r = system(vol, d, ["Leaf 160"] * n, "wired", "system")
        if r["saving"] > 0:
            P("   N=%d: saving %.0f USD per system, extra NRE repaid after %.0f systems" % (
                n, r["saving"], nre_extra * 1e6 / r["saving"]))
        else:
            P("   N=%d: no saving per system, the extra NRE is never repaid by BOM" % n)
    return "\n".join(t)


CLASSES = {"C0": "wired", "C0r": "wireless", "C1": "wifi"}


def leaving_fraction(vol, d, link, size="Leaf 160"):
    """Share of the all-in-one sub-total that does not stay in one Skin."""
    a = aio(vol, d, size)["sub"]
    s = skin(vol, d, size, link)["sub"]
    return 1.0 - s / a


def class_report(vol=1_000_000):
    d = Draw()
    out = ["== the distance classes: what BOM leaves the Leaf (Leaf 160, 1 M per year, base draw)",
           "   C0 tether to 2 m, C0r 60 GHz to about 10 m with a clear path, C1 room to about 30 m, C2 far to km",
           "   %-6s %-9s %9s %9s %9s %9s %9s %9s" % ("class", "link", "Skin USD", "aio USD", "leaves %", "Core N=1", "Core N=4", "Core N=8")]
    a = aio(vol, d)
    for c, link in CLASSES.items():
        s = skin(vol, d, "Leaf 160", link)["sub"]
        out.append("   %-6s %-9s %9.0f %9.0f %8.1f%% %9.0f %9.0f %9.0f" % (
            c, link, s, a["sub"], 100 * leaving_fraction(vol, d, link),
            core(vol, d, 1, link)["sub"], core(vol, d, 4, link)["sub"], core(vol, d, 8, link)["sub"]))
    out.append("   %-6s %-9s %9.0f %9.0f %8.1f%% %9s %9s %9s" % (
        "C2", "5G", a["sub"], a["sub"], 0.0, "n/a", "n/a", "n/a"))
    out.append("   C2 note: the Skin keeps the modem, decoder, store, radio, camera and cells, so it is the L.6.0 Leaf.")
    out.append("   The far Core is a validator and a network service. It is no BOM of the Leaf and no saving.")
    out.append("")
    out.append("   saving of the Split against all-in-one, USD per system (percent), royalty on the system")
    out.append("   %-6s %-9s %18s %18s %18s %18s  %s" % ("class", "link", "N=1", "N=2", "N=4", "N=8", "break-even"))
    for c, link in CLASSES.items():
        row = []
        for n in (1, 2, 4, 8):
            r = system(vol, d, ["Leaf 160"] * n, link, "system")
            row.append("%7.0f (%5.1f%%)" % (r["saving"], 100 * r["saving"] / r["all_in"]))
        out.append("   %-6s %-9s %18s %18s %18s %18s  %s" % (c, link, *row, breakeven(vol, d, link, "system")))
    out.append("   C2     5G                      0 (  0.0%)         0 (  0.0%)         0 (  0.0%)         0 (  0.0%)  not applicable")
    return "\n".join(out)


def delta_table(vol, d):
    """What leaves the Leaf 160 and where it goes, at N = 4, wired. USD per Skin."""
    a = aio(vol, d)["lines"]
    s = skin(vol, d, "Leaf 160", "wired")["lines"]
    c = core(vol, d, 4, "wired")["lines"]
    out = ["== what leaves the all-in-one Leaf 160, 1 M per year, base draw (USD per unit)",
           "   %-62s %8s %8s" % ("line", "all-in-one", "Skin")]
    for k, v in a.items():
        sk = s.get(k, 0.0)
        out.append("   %-62s %8.1f %8.1f" % (k[:62], v, sk))
    for k, v in s.items():
        if k not in a:
            out.append("   %-62s %8s %8.1f   (new Skin line)" % (k[:62], "", v))
    out.append("   Core, N=4, per Skin: %.1f USD" % (sum(c.values()) / 4.0))
    return "\n".join(out)


def heat_note():
    out = ["== the Skin load against the free-air limit, W (heat note, [HYPOTHESIS] for the link terms)",
           "   free-air sustained limit of the L.6.0 body: %.2f W still, %.2f W light wind [TREE]" % FREE_AIR_W]
    for lab, w in (("delta session", SKIN_DELTA_W), ("video session", SKIN_VIDEO_W)):
        for link, extra in (("wired C0", PHY_W), ("60 GHz C0r", RADIO_W), ("Wi-Fi 7 C1", WIFI_DEC_W)):
            lo, ba, hi = (w + extra[0], w + extra[1], w + extra[2])
            verdict = "inside" if ba <= FREE_AIR_W[0] else ("inside with wind" if ba <= FREE_AIR_W[1] else "over")
            out.append("   %-14s %-16s %.2f / %.2f / %.2f W  base is %s" % (lab, link, lo, ba, hi, verdict))
    out.append("   C2: the Skin is the L.6.0 Leaf, so the load is the L.6.0 load [TREE] and no heat moves out")
    return "\n".join(out)


def tile_sweep(vol=1_000_000):
    out = ["== what if the micro-LED tile gets cheaper (tile_x multiplier), N=4 wired, royalty on system"]
    out.append("   %-8s %12s %10s %12s %14s" % ("tile_x", "all-in-one", "Skin", "Skin/aio", "saving %"))
    for x in (1.0, 0.5, 0.25, 0.10, 0.05):
        d = Draw()
        d.tile_x = x
        a = aio(vol, d)["total"]
        s = skin(vol, d, "Leaf 160", "wired")["sub"]
        r = system(vol, d, ["Leaf 160"] * 4, "wired", "system")
        out.append("   %-8.2f %12.0f %10.0f %11.0f %% %13.1f %%" % (x, a, s, 100 * s / a, 100 * r["saving"] / r["all_in"]))
    # the tile cost at which a Skin costs 500 USD
    d = Draw()
    base_tile = aio(vol, d)["lines"]["micro-LED tiles"]
    rest = skin(vol, d, "Leaf 160", "wired")["sub"] - base_tile
    out.append("   a Skin of 500 USD needs the tile cost of the 128 tiles at %.0f USD (now %.0f USD): a factor %.2f" % (
        500 - rest, base_tile, (500 - rest) / base_tile))
    return "\n".join(out)


def size_break_even(vol=1_000_000):
    out = ["== break-even by Skin size, base draw, 1 M per year, wired, royalty on system"]
    d = Draw()
    for z in SIZES:
        row = []
        for n in (1, 2, 3, 4):
            r = system(vol, d, [z] * n, "wired", "system")
            row.append("N=%d %6.0f (%4.1f %%)" % (n, r["saving"], 100 * r["saving"] / r["all_in"]))
        out.append("   %-12s %s  break-even %s" % (z, " | ".join(row), breakeven(vol, d, "wired", "system", z)))
    return "\n".join(out)


def sweep(nsamp=6000, seed=7):
    rng = np.random.default_rng(seed)
    vol = 1_000_000
    rows = {"wired": [], "wireless": [], "wifi": []}
    for _ in range(nsamp):
        d = Draw(rng)
        for link in rows:
            rec = {"skin": skin(vol, d, "Leaf 160", link)["sub"],
                   "aio": aio(vol, d)["total"],
                   "disp_share": aio(vol, d)["lines"]["micro-LED tiles"] / aio(vol, d)["total"],
                   "be_sys": breakeven(vol, d, link, "system"),
                   "be_core": breakeven(vol, d, link, "core")}
            for n in (1, 2, 4, 8):
                r = system(vol, d, ["Leaf 160"] * n, link, "system")
                rec["core%d" % n] = core(vol, d, n, link)["sub"]
                rec["sav%d" % n] = r["saving"]
                rec["pct%d" % n] = 100 * r["saving"] / r["all_in"]
            rows[link].append(rec)
    res = {}
    out = ["SWEEP: %d draws at 1 M per year. Every budget group and every PARAMS term is sampled." % nsamp,
           "P10, P50, P90 in USD per unit unless said. All [HYPOTHESIS].\n"]
    for link, R in rows.items():
        out.append("== link %s" % link)

        def q(key):
            v = np.array([r[key] for r in R], dtype=float)
            return np.percentile(v, [10, 50, 90])

        for key, lab in (("aio", "all-in-one Leaf 160"), ("skin", "Skin Leaf 160 with camera"),
                         ("core1", "Core, N=1"), ("core2", "Core, N=2"), ("core4", "Core, N=4"), ("core8", "Core, N=8")):
            a = q(key)
            out.append("   %-28s P10 %7.0f  P50 %7.0f  P90 %7.0f" % (lab, *a))
            res[link + "_" + key] = [float(x) for x in a]
        a = q("disp_share")
        out.append("   micro-LED share of the all-in-one P10 %.2f P50 %.2f P90 %.2f" % tuple(a))
        for n in (1, 2, 4, 8):
            sv = np.array([r["sav%d" % n] for r in R])
            pc = np.array([r["pct%d" % n] for r in R])
            out.append("   N=%d saving USD P10 %7.0f P50 %7.0f P90 %7.0f | percent P50 %5.1f | P(split cheaper) %.2f" % (
                n, *np.percentile(sv, [10, 50, 90]), np.percentile(pc, 50), float((sv > 0).mean())))
            res["%s_sav%d" % (link, n)] = [float(x) for x in np.percentile(sv, [10, 50, 90])]
            res["%s_p%d" % (link, n)] = float((sv > 0).mean())
        for key, lab in (("be_sys", "royalty on the system"), ("be_core", "royalty on the Core only")):
            v = [r[key] if r[key] is not None else 99 for r in R]
            c = {k: int(sum(1 for x in v if x == k)) for k in (1, 2, 3, 4, 99)}
            out.append("   break-even Skins per Core, %s: 1:%d 2:%d 3:%d 4:%d never:%d of %d" % (
                lab, c[1], c[2], c[3], c[4], c[99], len(v)))
            res["%s_%s" % (link, key)] = {str(k): c[k] for k in c}
        out.append("")
    return "\n".join(out), res


def tornado():
    """One at a time swing of the N=4 wired saving, all else at base."""
    vol = 1_000_000
    base = system(vol, Draw(), ["Leaf 160"] * 4, "wired", "system")["saving"]
    rows = []
    for k, v in PARAMS.items():
        vals = []
        for pos in (0, 2):
            d = Draw()
            d.p[k] = v[pos]
            vals.append(system(vol, d, ["Leaf 160"] * 4, "wired", "system")["saving"])
        rows.append((abs(vals[1] - vals[0]), k, vals))
    for g in ("disp", "cell", "sil", "cam", "mech", "asm", "roy"):
        vals = []
        for pos in (0.0, 1.0):
            d = Draw()
            d.u[g] = pos
            vals.append(system(vol, d, ["Leaf 160"] * 4, "wired", "system")["saving"])
        rows.append((abs(vals[1] - vals[0]), "budget group: " + g, vals))
    rows.sort(reverse=True)
    out = ["TORNADO: N=4, wired, 1 M per year. Saving of the Split in USD per system.",
           "base saving %.0f USD. Each row moves one term from low to high.\n" % base]
    for sw, k, v in rows:
        out.append("   %-26s low %8.0f  high %8.0f  swing %7.0f" % (k, v[0], v[1], sw))
    return "\n".join(out)


def plot(res_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    vol = 1_000_000
    d = Draw()
    ns = list(range(1, 13))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for link, ls in (("wired", "-"), ("wireless", "--"), ("wifi", ":")):
        for roy, col in (("system", "#1f5f8b"), ("core", "#c0612b")):
            y = [system(vol, d, ["Leaf 160"] * n, link, roy)["saving"] for n in ns]
            ax.plot(ns, y, ls, color=col, label="%s, royalty on %s" % (link, roy))
    ax.axhline(0, color="#555", lw=0.8)
    ax.set_xlabel("Skins per Core, Leaf 160 class")
    ax.set_ylabel("BOM saving against all-in-one, USD")
    ax.set_title("Split saving, base draw, 1 M per year")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(res_path, dpi=140)


def main():
    txt = tables()
    open(os.path.join(OUT, "cost_table.txt"), "w").write(txt + "\n")
    print(txt)
    sw, res = sweep()
    open(os.path.join(OUT, "sweep.txt"), "w").write(sw + "\n")
    print("\n" + sw)
    tn = tornado()
    open(os.path.join(OUT, "tornado.txt"), "w").write(tn + "\n")
    print("\n" + tn)
    json.dump(res, open(os.path.join(OUT, "cost.json"), "w"), indent=1)
    plot(os.path.join(OUT, "breakeven.png"))


if __name__ == "__main__":
    main()
