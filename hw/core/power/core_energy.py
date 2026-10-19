#!/usr/bin/env python3
"""core_energy.py - question 3 of the POWER seat: size the Core for 1, 2, 4 and 8 Skins.

The Skin catalogue: Leaf 80, Leaf 160, Leaf 480 and the Frame. Skin loads from skin_tree.py (cpcommon.skin_load).
The Core holds the silicon, the radios, the secure element, the energy and the processing (BRIEF Section 2).

Core load at its rails  = radio + authority + hub fixed + sum over Skins of (hub variable + link TX)
Core load at its cell   = that / 0.90 (U4 class converters, hw/energy/04)
Skin supply             = each Skin at VBUS / 0.93 (the Core output stage regulating VBUS) [H]
The hub model is a fit of the rows of FINAL/04 section 4.6: fixed 0.50 W (delta) and 1.00 W (video), plus 0.10 W per
2.56 Mpx of pixels. It reproduces Leaf 80 delta 0.60 W, Leaf 160 delta 0.70 W, Leaf 160 video 1.20 W, Leaf 160 squared video 1.40 W.

Run:  python3 hw/core/power/core_energy.py
Out:  out/core_energy.json, out/core_energy.txt, out/core_energy.png
"""
import math

import numpy as np

import cpcommon as K

HC, HO, CL = K.HC, K.HO, K.CL
LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


ETA_RING = 0.90        # Core converters [T]
ETA_OUT = 0.93         # Core output stage for the Skin VBUS [H]
ETA_IN = 0.95          # host input path of the Core [H]
UNIT_PX = 1600 * 1600  # 2.56 Mpx, one P80 [T]
E_TX_PJ = 8.0          # link transmitter, pJ per bit [G] [H]
TX_STATIC = 0.030      # W per link [H]

SKINS = {
    # px, area mm2, body W delta-class, body W heavy-class, fps delta, fps heavy, touch
    "Leaf 80": dict(px=1600 * 1600, area=6400.0, body=(0.45, 0.45 * 1.35 / 0.80), fps=(60, 120), touch=True,
                    src="FINAL/04 4.6 Leaf 80 delta 0.35 + 0.10 W; heavy scaled by 1.35/0.80 [H]"),
    "Leaf 160": dict(px=1600 * 3200, area=12800.0, body=(0.80, 1.35), fps=(60, 120), touch=True,
                     src="hw/energy/04 delta 0.80 W, video 1.35 W [T]"),
    "Leaf 480": dict(px=2872 * 1436, area=115200.0, body=(5.80, 5.80 * 1.35 / 0.80), fps=(10, 60), touch=True,
                     src="FINAL/04 4.6 static work session 5.00 + 0.80 W; heavy scaled [H]"),
    "Frame": dict(px=2 * 3840 * 2160, area=2400.0, body=(0.80, 1.20), fps=(60, 90), touch=False,
                  src="FINAL/07 7.5: 0.4 to 1.2 W with the display on, 0.8 W nominal [D]"),
}
MIXES = {
    1: ["Leaf 160"],
    2: ["Leaf 160", "Leaf 80"],
    4: ["Leaf 160", "Leaf 160", "Leaf 80", "Frame"],
    8: ["Leaf 480", "Leaf 160", "Leaf 160", "Leaf 160", "Leaf 80", "Leaf 80", "Frame", "Frame"],
}
RING_PEAK_SURPLUS = 4.50 - 2.42      # W: the ring peak of hw/energy/03 against the outdoor ring of 04 [T]


def wire_gbps(px, fps):
    return px * fps * 30.0 / 3.0 * (13.43 / 12.29) / 1e9


def skin_power(name, cls, level="nom"):
    """Skin at VBUS, W. cls: 'delta' or 'heavy' or 'outdoor' (only the Leaf 160 has an outdoor value)."""
    s = SKINS[name]
    k = K.LEVELS[level]
    if cls == "outdoor":
        assert name == "Leaf 160"
        return K.skin_load("video outdoors, 800 nits, 5G", level)["skin_vbus_W"]
    i = 0 if cls == "delta" else 1
    body = s["body"][i]
    fps = s["fps"][i]
    rate = wire_gbps(s["px"], fps)
    ar = s["area"] / 12800.0
    link = K.ADD["link_static_W"][k] + K.ADD["e_rx_pJ_bit"][k] * rate * 1e-3
    bc = K.ADD["backchannel_W"][k]
    router = K.ADD["edge_router_W"][k] * math.sqrt(ar)
    touch = K.ADD["touch_W"][k] * ar if s["touch"] else 0.0
    ident = K.ADD["identity_W"][k]
    return body / K.ETA_TILE + (link + bc + router + touch + ident) / K.ETA_LOCAL, rate


def core_power(mix, cls, level="nom"):
    """Return dict with the Core and Skin powers for a mix of Skins in a class ('delta', 'heavy' or 'peak')."""
    delta = cls == "delta"
    radio = 0.40 if delta else 0.60
    auth = 0.12
    hub_fixed = 0.50 if delta else 1.00
    load = radio + auth + hub_fixed
    skins = []
    outdoor_used = False
    for nm in mix:
        c = "delta" if delta else "heavy"
        if cls == "peak" and nm == "Leaf 160" and not outdoor_used:
            sp = skin_power(nm, "outdoor", level)
            rate = wire_gbps(SKINS[nm]["px"], 120)
            outdoor_used = True
        else:
            sp, rate = skin_power(nm, c, level)
        hub_var = 0.10 * SKINS[nm]["px"] / UNIT_PX
        tx = TX_STATIC + E_TX_PJ * rate * 1e-3
        load += hub_var + tx
        skins.append(dict(name=nm, skin_vbus_W=sp, rate_Gbps=rate, hub_var_W=hub_var, link_tx_W=tx))
    if cls == "peak":
        load += RING_PEAK_SURPLUS
    skin_sum = sum(s["skin_vbus_W"] for s in skins)
    core_cell = load / ETA_RING
    skin_supply = skin_sum / ETA_OUT
    bus = core_cell + skin_supply
    p_in = bus / ETA_IN
    heat = p_in - skin_sum          # everything the Core takes that does not leave as Skin power
    return dict(core_load_W=load, core_cell_W=core_cell, skin_vbus_sum_W=skin_sum, skin_supply_W=skin_supply, bus_W=bus,
                p_in_W=p_in, core_heat_W=heat, skins=skins)


def main():
    p("POWER seat · question 3 · the Core for 1, 2, 4 and 8 Skins")
    p("model: Core load = radio + authority + hub fixed + per Skin (hub variable + link TX). Core at its cell /%.2f, Skin supply /%.2f, host input /%.2f" % (ETA_RING, ETA_OUT, ETA_IN))
    p("check of the hub fit against FINAL/04 4.6: Leaf 80 delta %.2f W (table 0.60), Leaf 160 delta %.2f W (0.70), Leaf 160 video %.2f W (1.20), Leaf 160 squared video %.2f W (1.40)" % (
        0.50 + 0.10, 0.50 + 0.20, 1.00 + 0.20, 1.00 + 0.40))
    p("")
    res = {"skins": {k: {kk: vv for kk, vv in v.items() if kk != "src"} for k, v in SKINS.items()}, "mixes": MIXES, "sets": {}}
    p("THE SKIN CATALOGUE (loads at VBUS, nominal, delta-class and heavy-class)")
    for nm, s in SKINS.items():
        d, rd = skin_power(nm, "delta")
        h, rh = skin_power(nm, "heavy")
        p("  %-9s %5.1f Mpx, body %.2f / %.2f W -> Skin %.2f / %.2f W at VBUS, link %.2f / %.2f Gb/s   [%s]" % (
            nm, s["px"] / 1e6, s["body"][0], s["body"][1], d, h, rd, rh, s["src"]))
    p("")

    # ------------------------------------------------------------ the sets
    p("THE CORE FOR N SKINS, W")
    p("  %-3s %-38s %-6s | %8s %8s %8s %8s %8s %8s" % ("N", "mix", "class", "core load", "core cell", "Skins", "bus", "host in", "core heat"))
    for n, mix in MIXES.items():
        for cls in ("delta", "heavy", "peak"):
            r = core_power(mix, cls)
            lo = core_power(mix, cls, "low")
            hi = core_power(mix, cls, "high")
            r["p_in_low_W"], r["p_in_high_W"] = lo["p_in_W"], hi["p_in_W"]
            res["sets"]["N%d %s" % (n, cls)] = r
            p("  %-3d %-38s %-6s | %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f   (host in low %.2f high %.2f)" % (
                n, ",".join(m.replace("Leaf ", "L") for m in mix), cls, r["core_load_W"], r["core_cell_W"], r["skin_vbus_sum_W"],
                r["bus_W"], r["p_in_W"], r["core_heat_W"], lo["p_in_W"], hi["p_in_W"]))
    p("")
    # the cost of the split at N = 1
    one_d = res["sets"]["N1 delta"]["bus_W"]
    one_h = res["sets"]["N1 heavy"]["bus_W"]
    one_p = res["sets"]["N1 peak"]["bus_W"]
    l60 = {"delta": HC.LOADS["delta session"], "video": HC.LOADS["video"], "peak": 8.7}
    p("THE PRICE OF THE SPLIT at N = 1 (Leaf 160 plus its Core), bus power against the L.6.0 battery power of hw/energy/04")
    p("  delta: %.2f W against %.2f W, %+.0f %%" % (one_d, l60["delta"], 100 * (one_d / l60["delta"] - 1)))
    p("  video: %.2f W against %.2f W, %+.0f %%" % (one_h, l60["video"], 100 * (one_h / l60["video"] - 1)))
    p("  peak:  %.2f W against %.2f W, %+.0f %%" % (one_p, l60["peak"], 100 * (one_p / l60["peak"] - 1)))
    res["split_price"] = dict(delta=one_d / l60["delta"] - 1, video=one_h / l60["video"] - 1, peak=one_p / l60["peak"] - 1)
    p("  The extra is the second conversion of the Skin supply (%.2f), the link transmitter and the link receiver." % ETA_OUT)
    p("")

    # ------------------------------------------------------------ the Core energy
    p("THE CORE ENERGY: nominal Wh of cells for a session on the Core alone (no host), delta class, usable 0.96 and path 0.97")
    cell_whkg = 574.0
    en = {}
    for n in MIXES:
        r = res["sets"]["N%d delta" % n]
        row = {}
        for h in (1.0, 4.0, 8.0):
            wh = r["bus_W"] * h / (0.96 * 0.97)
            row["%g h" % h] = dict(Wh=wh, cells_g=wh / cell_whkg * 1000.0, volume_cm3=wh / 0.750 )
        en["N%d" % n] = row
        p("  N=%d: %s" % (n, "   ".join("%s: %.1f Wh, %.0f g of cells, %.0f cm3 at 750 Wh/L" % (k, v["Wh"], v["cells_g"], v["volume_cm3"]) for k, v in row.items())))
    res["energy"] = en
    p("  Cells are at the S model of 574 Wh/kg and 750 Wh/L. A pack adds structure, about 1.3 times the mass [H].")
    p("")
    p("THE CORE POWER LIMIT OF THE CELL: the least Wh of cells that carry the heavy and the peak power at a C-rate")
    lim = {}
    for n in MIXES:
        for cls in ("heavy", "peak"):
            r = res["sets"]["N%d %s" % (n, cls)]
            row = {"%g C" % c: r["bus_W"] / c for c in (3.0, 5.0, 10.0)}
            lim["N%d %s" % (n, cls)] = row
            p("  N=%d %-5s %6.2f W on the cell: " % (n, cls, r["bus_W"]) + ", ".join("%s: %.1f Wh" % kv for kv in row.items()))
    res["power_limit_Wh"] = lim
    p("  Part 22: the 128 micro cells carry 8.7 W at 3 C with 53 cells, 3.1 Wh. The Core with 4 Skins at peak needs a cell that carries the table above.")
    p("")

    # ------------------------------------------------------------ cell life of the Core
    p("CELL LIFE OF A HOST-FED CORE CELL, Schmalstieg model of hw/hostpower/powerpath/celllife.py, float at 50 %, 25 C, 6 hand-overs a day of 4 min at the delta class")
    vm, vr = CL.profile_stats([(24, 0.5, 0.5)])
    life = {}
    for n in (1, 4, 8):
        P = res["sets"]["N%d delta" % n]["bus_W"]
        row = {}
        for tag, minutes in (("Buffer 5 min", 5.0), ("Buffer 30 min", 30.0), ("Core 4 h", 240.0), ("Core 8 h", 480.0)):
            e_nom = P * minutes / 60.0 / (0.485 * 0.93)           # floated 60 to 10 %, path
            e_day = 6 * P * 4.0 / 60.0
            efc = e_day / e_nom
            dod = min(1.0, (P * 4.0 / 60.0) / e_nom)
            y, _ = CL.years_to(0.2, efc, vm, vr, dod, 298.15)
            row[tag] = dict(E_nom_Wh=e_nom, efc_per_day=efc, dod=dod, years=y)
        life[n] = row
        p("  N=%d (%.1f W): " % (n, P) + "   ".join("%s %.1f Wh %.2f cycles/day %.1f y" % (k, v["E_nom_Wh"], v["efc_per_day"], v["years"]) for k, v in row.items()))
    res["life"] = life
    p("  A Core cell sized for minutes cycles hard and ages fast. The Core cell wants hours of energy, or the host is the life.")
    p("")

    # ------------------------------------------------------------ the host classes
    p("WHAT N SKINS COST THE HOST CLASSES OF PART 22 SECTION 22.6")
    p("  need on VHV = Core host input power of the class + top-up at 0.2 C of a 4 h Core cell; offered power of hosts.py")
    hosts = {h["id"]: h for h in HO.HOSTS}
    carry = {}
    names = [h["id"] for h in HO.HOSTS]
    p("  %-5s %-26s %7s | " % ("id", "host", "offer W") + " ".join("N%d d/h/p" % n for n in MIXES))
    for h in HO.HOSTS:
        v = h["v_vhv"]
        row = {}
        cells = []
        for n in MIXES:
            ok = []
            for cls in ("delta", "heavy", "peak"):
                r = res["sets"]["N%d %s" % (n, cls)]
                topup = 0.2 * res["energy"]["N%d" % n]["4 h"]["Wh"]
                need = r["p_in_W"] + topup
                if v <= 5.0:
                    need = need / (3.86 / 4.9)
                else:
                    # leaves I2R at the host voltage, 18 mohm loop
                    need += (need / v) ** 2 * 0.018
                row[cls] = dict(need_W=need, ok=h["offered_vhv"] >= need)
                ok.append("y" if h["offered_vhv"] >= need else "-")
            cells.append("/".join(ok))
            row["N%d" % n] = "/".join(ok)
        carry[h["id"]] = row
        p("  %-5s %-26s %7.1f | " % (h["id"], h["name"], h["offered_vhv"]) + " ".join("%8s" % c for c in cells))
    res["carry"] = carry
    p("  d is the delta class, h the heavy (video) class, p the peak class. y carries it, - does not.")
    p("")
    p("  Largest of the four sets each host carries, at the delta, heavy and peak class:")
    for h in HO.HOSTS:
        row = carry[h["id"]]
        best = {}
        for cls in ("delta", "heavy", "peak"):
            ns = [n for n in MIXES if row["N%d" % n].split("/")[("delta", "heavy", "peak").index(cls)] == "y"]
            best[cls] = max(ns) if ns else 0
        p("    %-5s %-26s delta N<=%d  heavy N<=%d  peak N<=%d" % (h["id"], h["name"], best["delta"], best["heavy"], best["peak"]))
        row["max_n"] = best
    p("")
    p("  Host energy per hour of Core at 8 Skins (delta class), Wh per hour, and the run time of the host batteries H1 and H5:")
    r8 = res["sets"]["N8 delta"]
    for h in HO.HOSTS:
        eta = float(np.prod([e for _, e in h["chain"]]))
        e = r8["p_in_W"] / eta + h["overhead_w"]
        extra = ""
        if h["id"] == "H1":
            extra = "  battery 17.7 Wh runs %.1f h" % (17.7 / (r8["p_in_W"] + h["overhead_w"]))
        if h["id"] == "H5":
            extra = "  battery 15.2 Wh runs %.1f h" % (15.2 / r8["p_in_W"])
        p("    %-5s %-26s %6.1f Wh per hour%s" % (h["id"], h["name"], e, extra))
        carry[h["id"]]["Wh_per_h_N8_delta"] = e
    res["h1_h5_hours_N8"] = dict(H1=17.7 / (r8["p_in_W"] + 0.23), H5=15.2 / r8["p_in_W"])
    K.dump("core_energy", res, LINES)
    plots(res, carry)


def plots(res, carry):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ns = list(MIXES)
    for j, cls in enumerate(("delta", "heavy", "peak")):
        ys = [res["sets"]["N%d %s" % (n, cls)]["p_in_W"] for n in ns]
        ax.plot(ns, ys, "-o", color=K.PAL[j], lw=1.8, ms=5, label="Core host input, %s class" % cls)
    for hid, col, ls in (("H0", "#444", ":"), ("H5", K.PAL[3], "--"), ("H6b", K.PAL[4], "-."), ("H4b", K.PAL[5], "--")):
        o = [h for h in HO.HOSTS if h["id"] == hid][0]
        ax.axhline(o["offered_vhv"], color=col, lw=1, ls=ls)
        ax.text(8.1, o["offered_vhv"], "%s %.0f W" % (hid, o["offered_vhv"]), fontsize=8, va="center")
    ax.set_xticks(ns)
    ax.set_xlim(0.7, 9.0)
    K.style(ax, "number of Skins on one Core", "W on the host", "Core host input against the host classes")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(K.OUT + "/core_energy.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
