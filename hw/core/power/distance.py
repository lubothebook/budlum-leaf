#!/usr/bin/env python3
"""distance.py - the distance column of the POWER seat (BRIEF Section 8): C0, C1 and C2.

C0  a contact or a tether, up to 2 m. The minimal Skin of skin_tree.py, power by pads, pixels by wire.
C1  a room, up to about 30 m. Power cannot cross it, so the Skin sits on a near energy host (a Part 22 host)
    or carries its own cell. Pixels come by radio. Two bounds:
      C1a  a wireless pixel link at Gb/s, minimal Skin plus a radio client and a stream decoder
      C1b  a slice stream with the local compositor: the Skin is the L.6.0 Leaf (same as C2)
C2  far, kilometres. The Skin keeps the radio, the decoder, the frame store and the compositor of L.6.0. The Core is a validator.
    Power does not travel, so the two hosts law holds: the energy host is local and the compute host is remote.

Run:  python3 hw/core/power/distance.py     (after core_energy.py)
Out:  out/distance.json, out/distance.txt
"""
import math
import os
import sys

import numpy as np

import cpcommon as K
import core_energy as CE

HC, TI, HO = K.HC, K.TI, K.HO
sys.path.insert(0, os.path.join(K.ROOT, "hw", "dock"))
import params as DP      # noqa: E402  read only

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


RADIO = {"delta": 0.40, "heavy": 0.60}       # Skin radio client, the radio column of hw/energy/04 [T]
DECODER = {"delta": 0.25, "heavy": 0.45}     # slice decoder for a Leaf 160, a share of the hub of FINAL/04 [H], scaled by pixels
AP_FIRST, AP_EXTRA = DP.LOADS["60 GHz 802.11ay radio + 32-element array"][1], 0.30   # W: Core radio, 2.5 W typ [T] hw/dock/params.py, +0.3 W per Skin [H]
VALIDATOR_W = 18.0                           # W typ of one validator module [T] hw/dock/params.py
L60 = {"delta": HC.LOADS["delta session"], "heavy": HC.LOADS["video"]}


def link_part(name, cls, level="nom"):
    s = CE.SKINS[name]
    k = K.LEVELS[level]
    i = 0 if cls == "delta" else 1
    rate = CE.wire_gbps(s["px"], s["fps"][i])
    return (K.ADD["link_static_W"][k] + K.ADD["e_rx_pJ_bit"][k] * rate * 1e-3 + K.ADD["backchannel_W"][k]) / K.ETA_LOCAL


def skin_c1a(name, cls):
    """Skin at VBUS for C1a: C0 Skin without the wired PHY, plus a radio client and a stream decoder."""
    c0, _ = CE.skin_power(name, cls)
    dec = max(0.10, DECODER[cls] * CE.SKINS[name]["px"] / (1600 * 3200))
    return c0 - link_part(name, cls) + (RADIO[cls] + dec) / K.ETA_LOCAL


def core_c1a(mix, cls):
    """Core for C1a: no wired link TX, one radio array shared, a stream encoder in the hub."""
    delta = cls == "delta"
    load = 0.12 + (0.50 if delta else 1.00)
    n = len(mix)
    load += AP_FIRST + AP_EXTRA * (n - 1)
    skin_sum = 0.0
    for nm in mix:
        load += 0.10 * CE.SKINS[nm]["px"] / CE.UNIT_PX
        skin_sum += skin_c1a(nm, cls)
    # at C1 the Skins are not fed by the Core: each Skin sits on its own energy host
    core_cell = load / CE.ETA_RING
    p_in = core_cell / CE.ETA_IN
    return dict(core_load_W=load, p_in_W=p_in, skin_sum_W=skin_sum)


def main():
    p("POWER seat · the distance column: C0 contact or tether (2 m), C1 room (30 m), C2 far (kilometres)")
    p("")
    res = {}
    # ------------------------------------------------------------ the Skin load per class
    p("THE SKIN LOAD at VBUS, Leaf 160, nominal, W and the margin to the free-air ceilings (1.73 still, 2.37 wind) [H]")
    p("  %-34s %8s %8s | %s" % ("class", "delta", "video", "reading"))
    rows = {}
    c0 = {c: CE.skin_power("Leaf 160", c)[0] for c in ("delta", "heavy")}
    c1 = {c: skin_c1a("Leaf 160", c) for c in ("delta", "heavy")}
    c2 = {c: L60[c] for c in ("delta", "heavy")}
    rows["C0"] = c0
    rows["C1a"] = c1
    rows["C1b"] = c2
    rows["C2"] = c2
    for k, v in rows.items():
        note = "%+.2f / %+.2f W margin to 1.73 W still; %+.2f / %+.2f to 2.37 W wind" % (
            K.LIMIT_STILL_W - v["delta"], K.LIMIT_STILL_W - v["heavy"], K.LIMIT_WIND_W - v["delta"], K.LIMIT_WIND_W - v["heavy"])
        p("  %-34s %8.2f %8.2f | %s" % (
            {"C0": "C0 minimal Skin", "C1a": "C1a radio client + stream decoder", "C1b": "C1b slice stream, L.6.0 Leaf", "C2": "C2 L.6.0 Leaf, at the cells"}[k],
            v["delta"], v["heavy"], note))
    res["skin_load"] = rows
    p("  C2 and C1b are the battery power of hw/energy/04: delta 2.24 W, video 3.65 W. They hold radio, decoder, frame store, compositor and authority.")
    p("  The Split buys nothing on energy there: the Skin is the L.6.0 Leaf, and the remote Core adds its own load on top.")
    p("")

    # ------------------------------------------------------------ the power tree per class
    p("THE SKIN POWER TREE PER CLASS")
    tree = {
        "C0": "the tree of skin_tree.py: pads or tether into VBUS, no cell, no ring. Energy comes with the pixels from the Core.",
        "C1a": "the C0 tree plus a radio client and a stream decoder on the Skin. Power cannot cross a room: the VBUS grid is fed by a near energy host (a Part 22 host H0 to H6) or by a cell.",
        "C1b": "the L.6.0 tree of hw/energy/03 in full: body, ring, U4, B cell, U7. The near host or the Leaf cells feed it.",
        "C2": "the L.6.0 tree of hw/energy/03 in full. The energy host is local to the Leaf. The compute host is the remote Core. Two hosts, two laws.",
    }
    for k, t in tree.items():
        p("  %-4s %s" % (k, t))
    res["tree"] = tree
    p("")

    # ------------------------------------------------------------ the tier answer per class
    p("THE TIER ANSWER FOR THE SKIN PER CLASS")
    c = HC.CELLS["S"]
    ans = {}
    loads_c1 = {"C1a delta": c1["delta"], "C1a video": c1["heavy"]}
    for nm, P in loads_c1.items():
        row = {}
        for gn, gs in (("3 s", 3.0), ("5 min", 300.0), ("30 min", 1800.0)):
            n, why = TI.min_cells(P, gs, c["E_target_Wh"], c["dcir"], TI.SOC_FLOAT, TI.V_FLOOR)
            row[gn] = dict(n=n, limit=why)
        vol3 = TI.cap_min_volume(TI.TECH["EDLC, large cell (Maxwell BCAP3000)"], P, 3.0)
        vol1 = TI.cap_min_volume(TI.TECH["EDLC, large cell (Maxwell BCAP3000)"], P, 1.0)
        ans[nm] = dict(buffer=row, bare_1s_cm3=vol1, bare_3s_cm3=vol3)
        p("  %-10s %.2f W: Buffer %s | Bare EDLC %.2f cm3 for 1 s, %.2f cm3 for 3 s" % (
            nm, P, ", ".join("%s %s cells (%s)" % (g, r["n"], r["limit"]) for g, r in row.items()), vol1, vol3))
    p("  C0:  no cell is the default. Bare 1 s in the cell layer (2 to 3 tiles). Buffer only as the safe-screen option, 5 cells. (skin_tree.py)")
    p("  C1a: the Skin has no tether, so it needs an energy host nearby or a cell. With a Part 22 host on contact, the C0 answer holds. A free-roaming Skin is Full.")
    p("  C1b and C2: the Part 22 answer holds unchanged. Buffer 14 cells at 3 s for the delta class, 53 for the peak. Bare does not fit the margin. Full for roaming.")
    res["tier"] = ans
    p("")

    # ------------------------------------------------------------ the Core per class
    p("THE CORE SIZING PER CLASS: host input in W for 1, 2, 4 and 8 Skins, delta class and heavy class")
    p("  %-3s | %-24s | %-30s | %s" % ("N", "C0 wired Core", "C1a radio Core (no Skin power)", "C2: N full Leaves, each on its own host; Core = validator"))
    core = {}
    for n, mix in CE.MIXES.items():
        c0d, c0h = CE.core_power(mix, "delta")["p_in_W"], CE.core_power(mix, "heavy")["p_in_W"]
        c1d, c1h = core_c1a(mix, "delta")["p_in_W"], core_c1a(mix, "heavy")["p_in_W"]
        # C2: each Leaf takes 2.24 / 3.65 W from its own host; the Core is a validator module, 18 W typ, shared by n Leaves
        c2_leaf_d, c2_leaf_h = L60["delta"], L60["heavy"]
        c2_core = VALIDATOR_W
        core["N%d" % n] = dict(c0_delta=c0d, c0_heavy=c0h, c1a_delta=c1d, c1a_heavy=c1h, c2_core_W=c2_core,
                               c2_leaf_delta_W=c2_leaf_d, c2_leaf_heavy_W=c2_leaf_h,
                               c2_system_delta_W=n * c2_leaf_d + c2_core, c2_core_share_per_leaf_W=c2_core / n)
        p("  %-3d | %5.2f / %5.2f W        | %5.2f / %5.2f W Core, %5.2f / %5.2f W Skins | %d x %.2f W Leaves + 18 W validator = %.1f W, %.1f W of Core per Leaf" % (
            n, c0d, c0h, c1d, c1h, core_c1a(mix, "delta")["skin_sum_W"], core_c1a(mix, "heavy")["skin_sum_W"],
            n, c2_leaf_d, n * c2_leaf_d + c2_core, c2_core / n))
    res["core"] = core
    p("")
    p("  The C0 column carries the Skin supply, so it holds the whole system. The C1a column is the Core alone, the Skins sit on their own hosts.")
    p("  Total energy of the system at N = 1, delta class:")
    sys_c0 = CE.core_power(["Leaf 160"], "delta")["bus_W"]
    c1a_total = core_c1a(["Leaf 160"], "delta")["p_in_W"] + c1["delta"]
    c2_total = L60["delta"] + 0.12
    p("    C0  %.2f W  (%+.0f %% against the 2.24 W Leaf)" % (sys_c0, 100 * (sys_c0 / L60["delta"] - 1)))
    p("    C1a %.2f W  (%+.0f %%): Core with its radio array %.2f W plus the Skin %.2f W" % (c1a_total, 100 * (c1a_total / L60["delta"] - 1), core_c1a(["Leaf 160"], "delta")["p_in_W"], c1["delta"]))
    p("    C2  %.2f W at the Leaf, plus a validator share. With 1 Leaf per 18 W validator the system takes %.1f W" % (L60["delta"], L60["delta"] + VALIDATOR_W))
    p("        The Core share per Leaf falls as 18 W / N: 18.0, 9.0, 4.5, 2.25 W for N = 1, 2, 4, 8. The Leaf keeps its 2.24 W in every case.")
    res["system_N1_delta_W"] = dict(C0=sys_c0, C1a=c1a_total, C2_leaf=L60["delta"], C2_with_validator=L60["delta"] + VALIDATOR_W)
    p("")

    # ------------------------------------------------------------ host classes per class
    p("WHICH PART 22 HOST CLASSES CARRY WHAT, per distance class (offered power on VHV; heavy class; 8.7 W peak for C2)")
    carry = {}
    for h in HO.HOSTS:
        v = h["v_vhv"]
        def ok(w):
            need = w / (3.86 / 4.9) if v <= 5.0 else w + (w / v) ** 2 * 0.018
            return h["offered_vhv"] >= need
        c0s = ok(CE.core_power(["Leaf 160"], "heavy")["p_in_W"])         # a Core with one Leaf 160 on the host (C0)
        c1s = ok(c1["heavy"] / CE.ETA_IN)                                  # the C1a Skin on its host
        c1c = ok(core_c1a(["Leaf 160"], "heavy")["p_in_W"])                # the C1a Core on its host
        c2s = ok(9.0)                                                      # the Leaf, 9.0 W on VHV as in Part 22
        carry[h["id"]] = dict(C0_core_N1=c0s, C1a_skin=c1s, C1a_core=c1c, C2_leaf_peak=c2s)
        p("  %-5s %-26s C0 Core+Skin %-3s | C1a Skin %-3s, C1a Core %-3s | C2 Leaf peak %-3s" % (
            h["id"], h["name"], "yes" if c0s else "NO", "yes" if c1s else "NO", "yes" if c1c else "NO", "yes" if c2s else "NO"))
    res["carry"] = carry
    p("")
    p("WHICH RESULTS HOLD AT C0, C1 AND C2")
    p("  Skin power tree and no cell:       C0 yes. C1a only on a near host. C1b and C2 no, the Skin is the L.6.0 Leaf.")
    p("  Bare store in the cell layer:      C0 yes. C1 and C2 as Part 22: no fit in the margin, 3 tiles of cell layer for a safe screen.")
    p("  Buffer power limit:                the 3 C rule holds at every class. C0 needs 5 to 10 cells, C1b and C2 need 14 to 53.")
    p("  Core energy and the host classes:  C0 and C1a. At C2 the Core is on mains and the Part 22 host classes govern the Leaf alone.")
    p("  Energy price of the Split:         C0 +10 to +13 %. C1a more. C2: no gain, plus the validator share.")
    K.dump("distance", res, LINES)


if __name__ == "__main__":
    main()
