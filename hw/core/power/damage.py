#!/usr/bin/env python3
"""damage.py - question 5 of the POWER seat: which Part 22 findings the Split strengthens or weakens.

Reads out/*.json of this seat and the out/*.json of hw/hostpower/powerpath (read only). Every number is loaded, none typed.

Run:  python3 hw/core/power/damage.py   (after the other scripts)
Out:  out/damage.json, out/damage.txt
"""
import json
import os

import cpcommon as K

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


def rd(name, base=None):
    with open(os.path.join(base or K.OUT, name + ".json")) as f:
        return json.load(f)


def main():
    ST, LP, CE, MA, DI = rd("skin_tree"), rd("link_power"), rd("core_energy"), rd("mass"), rd("distance")
    T22 = rd("tiers", K.PP + "/out")
    CL22 = rd("celllife", K.PP + "/out")
    rows = []

    def row(topic, verdict, c0, c1, c2):
        rows.append(dict(topic=topic, verdict=verdict, C0=c0, C1=c1, C2=c2))
        p("%s: %s" % (topic, verdict))
        p("   C0: %s" % c0)
        p("   C1: %s" % c1)
        p("   C2: %s" % c2)
        p("")

    p("POWER seat · question 5 · the damage report on the Part 22 findings")
    p("")
    # ------------------------------------------------ Bare
    b22_d = T22["bare"]["min_volume"]["EDLC, large cell (Maxwell BCAP3000)"]["delta session"]["3 s"]["vol_cm3"]
    b22_v = T22["bare"]["min_volume"]["EDLC, large cell (Maxwell BCAP3000)"]["video"]["3 s"]["vol_cm3"]
    bs = ST["bare"]["EDLC, large cell (Maxwell BCAP3000)"]
    s_d, s_v = bs["Lead delta body 0.80"]["3 s"], bs["Lead video body 1.35"]["3 s"]
    row("BARE STORE (Part 22: no store fits the 0.24 mm margin, 3 s of the safe screen needs 3 tiles)",
        "STRENGTHENED at C0, unchanged at C2",
        "the 3 s store shrinks %.1f times (%.2f against %.2f cm3 at the delta class, %.2f against %.2f at video). It fits the vacated cell layer in %d to %d tiles at large-cell density, %d to %d tiles of chip EDLC. It misses both margins on thickness."
        % (b22_d / s_d["vol_cm3"], s_d["vol_cm3"], b22_d, s_v["vol_cm3"], b22_v, s_d["tiles_cell_layer"], s_v["tiles_cell_layer"],
           ST["bare"]["EDLC, thin chip (Seiko CPH3225A)"]["Lead delta body 0.80"]["3 s"]["tiles_cell_layer"],
           ST["bare"]["EDLC, thin chip (Seiko CPH3225A)"]["Lead video body 1.35"]["3 s"]["tiles_cell_layer"]),
        "the C1a Skin load is %.2f W at delta, so the store is %.2f cm3 for 3 s: the gain is gone, and the Skin needs a near host or a cell."
        % (DI["skin_load"]["C1a"]["delta"], DI["tier"]["C1a delta"]["bare_3s_cm3"]),
        "none. The Skin is the L.6.0 Leaf, the Part 22 answer stands: no fit in the margin.")
    # ------------------------------------------------ Buffer
    n22 = {k: T22["buffer"]["tables"]["S floated at 60 %"][k]["3 s"]["n"] for k in ("delta session", "video", "peak")}
    nsk = ST["buffer"]
    core_lim = CE["power_limit_Wh"]
    row("BUFFER POWER LIMIT (Part 22: the 3 C cap sets the cell count, peak 8.7 W needs %d cells)" % n22["peak"],
        "WEAKENED for the Skin, STRENGTHENED for the Core",
        "the Skin needs %s to %s cells at 3 s (0.80 to 1.65 W) against %d and %d. It needs no Buffer. The limit moves to the Core, which needs %.1f Wh of cells at 3 C for 4 Skins at peak and %.1f Wh for 8."
        % (nsk["Lead delta body 0.80"]["3 s"]["n"], nsk["Skin video nominal"]["3 s"]["n"], n22["delta session"], n22["video"],
           core_lim["N4 peak"]["3 C"], core_lim["N8 peak"]["3 C"]),
        "the C1a Skin on a near host is power limited as at C0, with %d to %d cells at 3 s."
        % (DI["tier"]["C1a delta"]["buffer"]["3 s"]["n"], DI["tier"]["C1a video"]["buffer"]["3 s"]["n"]),
        "unchanged: %d, %d and %d cells at 3 s for the delta, video and peak classes." % (n22["delta session"], n22["video"], n22["peak"]))
    # ------------------------------------------------ host peak
    sp = CE["split_price"]
    cr = CE["carry"]
    h0 = cr["H0"]["max_n"]
    h5 = cr["H5"]["max_n"]
    row("HOST PEAK (Part 22: a host carries 8.7 W, 9.0 W on VHV; a 5 W pad does not)",
        "WEAKENED",
        "the Split costs %+.0f percent at the delta class, %+.0f percent at video and %+.0f percent at peak for one Skin and its Core (%.2f W against 2.24 W at delta). "
        "With the 0.2 C top-up, H0 carries at most %d Skins at every class, H5 at most %d at peak, H6a none. 8 Skins need %.1f W at delta on the host."
        % (100 * sp["delta"], 100 * sp["video"], 100 * sp["peak"], CE["sets"]["N1 delta"]["bus_W"], h0["peak"], h5["peak"], CE["sets"]["N8 delta"]["p_in_W"]),
        "the Core carries a radio array (%.1f W) and the Skin sits on its own host. The system at N = 1 takes %.2f W against 2.24 W." % (
            DI["core"]["N1"]["c1a_delta"] - CE["sets"]["N1 delta"]["bus_W"] + 0.0 if False else DI["system_N1_delta_W"]["C1a"] - DI["skin_load"]["C1a"]["delta"], DI["system_N1_delta_W"]["C1a"]),
        "the energy host of the Leaf is the Part 22 host and its numbers stand. The Core runs on mains: %.1f W per validator, %.1f W per Leaf at N = 8." % (
            18.0, DI["core"]["N8"]["c2_core_share_per_leaf_W"]))
    # ------------------------------------------------ cell life
    life = CE["life"]["4"]
    ratio = CL22["ratio"]
    row("CELL LIFE (Part 22: host-fed Full %.1f years against %.1f cycled; a small Buffer works hard)" % (ratio["hostfed_full_years"], ratio["cycled_years"]),
        "STRENGTHENED",
        "no cell on the Skin, so no cell aging in a surface at the skin limit. The Core cell sits in a part the user can swap. A Core Buffer of 5 min lives %.1f years, 30 min %.1f years, a 4 h cell %.1f years (4 Skins, host-fed, float 50 percent)."
        % (life["Buffer 5 min"]["years"], life["Buffer 30 min"]["years"], life["Core 4 h"]["years"]),
        "unchanged where the Skin has no cell. A roaming C1a Skin with a cell ages as Part 22 says.",
        "unchanged: the Leaf cell is the energy host, so %.1f years host-fed and %.1f years cycled stand." % (ratio["hostfed_full_years"], ratio["cycled_years"]))
    # ------------------------------------------------ heat
    sl = ST["loads"]
    d, v = sl["delta session, 250 nits, Wi-Fi"], sl["video session, Wi-Fi"]
    row("HEAT of the Skin against the free-air ceiling (Part 22 thermal: the L.6.0 Leaf fails everywhere)",
        "STRENGTHENED at C0 only",
        "the Skin takes %.2f W at delta (margin %+.2f W to 1.73 W still) and %.2f W at video (margin %+.2f W, and %+.2f W with the high add-ons). The pad interface adds %.0f mW at video."
        % (d["nom"], d["headroom_still"], v["nom"], v["headroom_still"], K.LIMIT_STILL_W - v["high"], 1000 * LP["worn P1 pads, VBUS direct video"]["skin_heat_interface_W"]),
        "C1a: %.2f W at delta, %.2f W at video. It passes delta by %+.2f W and fails video." % (
            DI["skin_load"]["C1a"]["delta"], DI["skin_load"]["C1a"]["heavy"], K.LIMIT_STILL_W - DI["skin_load"]["C1a"]["delta"]),
        "the Skin is the L.6.0 Leaf: %.2f W and %.2f W, over the ceiling by %.2f and %.2f W." % (
            2.24, 3.65, 2.24 - K.LIMIT_STILL_W, 3.65 - K.LIMIT_STILL_W))
    # ------------------------------------------------ the mass and the energy price in the Split
    s1 = MA["skin"]["S1 no cell, no coil (pads power)"]
    s0 = MA["skin"]["S0 no cell, Qi coil kept"]
    row("MASS AND ENERGY OF THE SPLIT (Part 22 gave capacity moving, not vanishing)",
        "MIXED",
        "the Skin weighs %.1f g (coil kept) or %.1f g (pads power), %.1f to %.1f g lighter than the 78.8 g device. The Core takes %.0f g for 3 h and the pair is %+.0f percent against one Leaf at N = 1 (S1). Break-even on mass is N = %s."
        % (s0["g"], s1["g"], s0["saved_g"], s1["saved_g"], MA["core"]["N1"]["3 h"]["total_g"] if False else MA["core"]["N1"]["3 h"]["total_g"],
           100 * (MA["system"]["N1"]["system_S1_g"] / MA["system"]["N1"]["leaves_g"] - 1), MA["break_even_N"]),
        "the energy costs more: %+.0f percent at N = 1 because of the Core radio array."
        % (100 * (DI["system_N1_delta_W"]["C1a"] / 2.242 - 1)),
        "the Split buys nothing on energy: the Leaf keeps its 2.24 W and the validator adds its share.")
    p("THE SENTENCE FOR THE STUDY")
    p("  The Split pays on mass and on the Skin heat at C0. It costs energy at every distance. It does not pay at C2.")
    K.dump("damage", dict(rows=rows), LINES)


if __name__ == "__main__":
    main()
