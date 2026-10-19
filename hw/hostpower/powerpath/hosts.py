#!/usr/bin/env python3
"""hosts.py - question 4: the host classes H0 to H6 and where the capacity goes.

For every host class: the offered power, the interface, the conversion chain, the clamp, whether it carries the
8.7 W peak and the 25 W port-part case, the host energy per hour of Leaf at four loads, and the run time of a
host battery (H1, H5) on the Leaf.

Chain efficiencies are [HYPOTHESIS] unless a file of hw/ gives them. The Leaf side is: leaves (I2R), then U_Q (3:1 SC, 0.97).

Run:  python3 hw/hostpower/powerpath/hosts.py
Out:  out/hosts.json, out/hosts.txt, out/hosts.png
"""
import math

import numpy as np

import common as C

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


ETA_UQ = 0.97                  # U_Q at its ratio [H]
R_LEAVES = 0.018 / 2           # ohm: two VHV leaves of 18 mOhm in parallel, one way; the return is the same [T] bar_pins.py
P_UQ_TOTAL = 25.0              # W: four U_Q of 6.25 W [T] hw/energy/03
LOAD_NAMES = ["standby", "delta session", "video", "peak"]
DOCK_OVERHEAD_AP_OFF = 0.20 + 0.02 + 0.01      # W, hw/dock/params.py idle: PD sink 0.20, light bar 0.02, secure element 0.01
DOCK_OVERHEAD_AP_ON = 3.0 + 0.4 + 0.05 + 0.2 + 0.02 + 0.01   # W, idle values with the Wi-Fi AP and the 60 GHz radio on


def leaf_side(p_vbus, v_vhv):
    """Power the host must put on VHV for p_vbus on the bus, with the leaves I2R."""
    p_uq_in = p_vbus / ETA_UQ
    i = p_uq_in / v_vhv
    loss_leaves = 2.0 * i * i * R_LEAVES        # out and back
    return p_uq_in + loss_leaves, loss_leaves


def load_dump_energy(us, ri, td, vclamp):
    """Joules into a clamp for the ISO 16750-2 load dump pulse: exponential decay with a half time td [GENERAL]."""
    tau = td / math.log(2.0)
    t = np.linspace(0, 8 * tau, 20000)
    v = us * np.exp(-t / tau)
    i = np.clip((v - vclamp) / ri, 0, None)
    return float(np.trapezoid(i * vclamp, t))


HOSTS = [
    dict(id="H0", name="wall dock", v_vhv=12.0, offered_vhv=25.0, offered_note="25 W at the VHV leaves [D] FINAL/20, hw/dock",
         interface="the 12 bar pads: leaves 5 and 8 VHV at 12 V, 1.04 A each at 25 W; or Qi2.2 25 W in the same dock",
         chain=[("wall adapter, USB-C PD EPR 28 V", 0.93), ("dock 12 V buck-boost (hw/dock/params.py)", 0.96)],
         clamp="the adapter and the dock take the mains and the clamp. The Leaf sees 12 V only, after the dead-pad proof",
         overhead_w=DOCK_OVERHEAD_AP_OFF, overhead_note="dock AP off: PD sink, light bar, secure element"),
    dict(id="H1", name="dock pack, 20 Wh", v_vhv=12.0, offered_vhv=25.0, offered_note="25 W for the Leaf is 1.35 C of the 20 Wh pack [T] hw/energy/05",
         interface="the 12 bar pads from the dock slot, as H0",
         chain=[("pack usable 3.0 to 4.2 V window", 0.95), ("pack protector and cell DCIR", 0.97), ("dock 12 V buck-boost", 0.96)],
         clamp="the pack is a floating cell: no transient. Pack under-voltage cut at 3.0 V per cell",
         overhead_w=DOCK_OVERHEAD_AP_OFF, overhead_note="dock AP off", pack_wh=20.0),
    dict(id="H2", name="desk USB-C PD", v_vhv=15.0, offered_vhv=45.0, offered_note="7.5 W (5 V 1.5 A) to 100 W; 15 V 3 A is 45 W [PUBLICATION] USB PD 3.0 fixed PDOs 5, 9, 15, 20 V",
         interface="the port part on a seat: VHV leaves 5 and 8 at 9 V (27 W, 1.50 A per leaf, no margin) or 15 V (0.90 A per leaf)",
         chain=[("wall adapter or hub PD source", 0.90), ("port part PD sink and its switch", 0.98)],
         clamp="the port part holds a 20 V rated input, an OVP switch and a back-flow block. VBUS of a bad cable is cut at 22 V [H]",
         overhead_w=0.0, overhead_note="none"),
    dict(id="H3a", name="vehicle 12 V", v_vhv=15.0, offered_vhv=45.0, offered_note="a PD car adapter of 30 to 100 W; 15 V 3 A is 45 W [GENERAL]",
         interface="a PD car adapter into the port part, or a cradle with the 12 pads and its own 12 V stage",
         chain=[("vehicle adapter, wide-input buck", 0.90), ("port part PD sink and its switch", 0.98)],
         clamp="adapter side: OVP switch for the load dump, TVS, cranking hold. The Leaf sees the PD output only",
         overhead_w=0.0, overhead_note="none", bus_window="9 to 16 V run; 6 to 10.5 V cranking minimum by severity code A to D; 35 V suppressed load dump; 79 to 101 V unsuppressed"),
    dict(id="H3b", name="vehicle 24 V", v_vhv=15.0, offered_vhv=45.0, offered_note="a PD adapter for 24 V systems of 30 to 100 W [GENERAL]",
         interface="as H3a, with an 80 V class input stage",
         chain=[("vehicle adapter, wide-input buck", 0.89), ("port part PD sink and its switch", 0.98)],
         clamp="adapter side: OVP switch for 58 V suppressed and 151 to 202 V unsuppressed load dump",
         overhead_w=0.0, overhead_note="none", bus_window="16 to 32 V run; 10 to 22 V cranking minimum by severity code E to H; 58 V typical suppressed clamp; 151 to 202 V unsuppressed"),
    dict(id="H4a", name="industrial 24 V", v_vhv=12.0, offered_vhv=25.0, offered_note="24 V rail (IEC 61131-2 class 19.2 to 28.8 V) through a 25 to 60 W isolated DC-DC [GENERAL]",
         interface="a cradle with the 12 pads, or an isolated DC-DC into a USB-C port part",
         chain=[("isolated 24 V to 12 V DC-DC", 0.92)],
         clamp="DC-DC input: reverse and surge clamp to the plant rule. Isolation 1.5 kV [H]",
         overhead_w=0.0, overhead_note="none", bus_window="19.2 to 28.8 V run (24 V -20 % / +25 %)"),
    dict(id="H4b", name="PoE type 2 (802.3at)", v_vhv=12.0, offered_vhv=25.5 * 0.90, offered_note="PD input 25.5 W [PUBLICATION] IEEE 802.3at Type 2, then 0.90 for the splitter [H]",
         interface="a PoE splitter into the port part (USB-C PD 9 V or 12 V), isolation 1.5 kVrms of the standard",
         chain=[("PoE splitter and its DC-DC", 0.90), ("cable and PSE share", 0.97)],
         clamp="the PD controller of the splitter holds 37 to 57 V and the isolation",
         overhead_w=0.0, overhead_note="none", bus_window="PD input 37 to 57 V"),
    dict(id="H4c", name="PoE type 3 (802.3bt)", v_vhv=15.0, offered_vhv=51.0 * 0.90, offered_note="PD input 51 W [PUBLICATION] IEEE 802.3bt Type 3, then 0.90 [H]",
         interface="as H4b",
         chain=[("PoE splitter and its DC-DC", 0.90), ("cable and PSE share", 0.97)],
         clamp="as H4b", overhead_w=0.0, overhead_note="none", bus_window="PD input 42.5 to 57 V"),
    dict(id="H5", name="worn power bank or belt pack", v_vhv=9.0, offered_vhv=18.0, offered_note="5000 mAh bank, 9 V 2 A is 18 W [GENERAL]; 5 V 3 A is 15 W",
         interface="the port part on a seat, by a short USB-C lead; or pads on a belt dock",
         chain=[("bank cell, boost, protection", 0.88), ("port part PD sink and its switch", 0.98)],
         clamp="a floating cell: no transient. Auto shut-off below 50 to 100 mA is common [H]",
         overhead_w=0.0, overhead_note="none", pack_wh=18.5),
    dict(id="H6a", name="low-power Qi pad, 5 W", v_vhv=5.0, offered_vhv=5.0, offered_note="Qi BPP 5 W at the rectifier [GENERAL]",
         interface="Qi coil: four sector coils in series and the Q1 rectifier",
         chain=[("pad supply, inverter and coil", 0.89), ("coupling, shield and rectifier", 0.90)],
         clamp="the rectifier clamp. Foreign object detection of the pad",
         overhead_w=0.0, overhead_note="none"),
    dict(id="H6b", name="Qi2 pad, 15 W", v_vhv=9.0, offered_vhv=15.0, offered_note="Qi EPP and Qi2 15 W at the rectifier [GENERAL]",
         interface="as H6a", chain=[("pad supply, inverter and coil", 0.89), ("coupling, shield and rectifier", 0.90)],
         clamp="as H6a", overhead_w=0.0, overhead_note="none"),
    dict(id="H6c", name="Qi2.2 pad, 25 W", v_vhv=12.0, offered_vhv=25.0, offered_note="Qi2.2 25 W at the rectifier [D] FINAL/21 21.2.6",
         interface="as H6a", chain=[("pad supply, inverter and coil", 0.89), ("coupling, shield and rectifier", 0.90)],
         clamp="as H6a", overhead_w=0.0, overhead_note="none"),
]


def main():
    p("POWER-PATH · question 4 · host classes")
    p("loads at VBUS: " + ", ".join("%s %.3f W" % (k, C.LOADS[k]) for k in LOAD_NAMES))
    p("the Leaf side: leaves 2 x 9 mOhm each way, U_Q 3:1 at %.2f, four U_Q give %.1f W at most" % (ETA_UQ, P_UQ_TOTAL))
    p("")
    res = {"hosts": {}}
    for h in HOSTS:
        eta_host = float(np.prod([e for _, e in h["chain"]]))
        v = h["v_vhv"]
        out = dict(name=h["name"], interface=h["interface"], clamp=h["clamp"], offered_vhv_W=h["offered_vhv"],
                   offered_note=h["offered_note"], eta_host=eta_host, chain=h["chain"])
        # can it carry the 8.7 W peak
        need_peak, _ = leaf_side(8.7, v)
        out["need_at_vhv_peak_W"] = need_peak
        out["carries_peak"] = h["offered_vhv"] >= need_peak
        out["margin_peak_W"] = h["offered_vhv"] - need_peak
        # the 25 W case is defined at the VHV leaves in hw/energy/03 and hw/dock (25 W, or 27 W at 9 V)
        need_25 = 25.0
        out["need_at_vhv_25W_case_W"] = need_25
        out["carries_25W_case"] = h["offered_vhv"] >= need_25
        # 5 V class: a 5 V input has no 3:1 ratio. A bypass or linear mode loses (1 - VBUS/5)
        out["five_volt_class"] = v <= 5.0
        if v <= 5.0:
            out["bypass_eta"] = 3.86 / 4.9
        # host energy per hour of Leaf
        e = {}
        for ln in LOAD_NAMES:
            pv = C.LOADS[ln]
            pin, _ = leaf_side(pv, v)
            if v <= 5.0:
                pin = pv / (3.86 / 4.9)
            e[ln] = pin / eta_host + h["overhead_w"]
        out["host_Wh_per_h"] = e
        out["overhead_w"] = h["overhead_w"]
        out["bus_window"] = h.get("bus_window")
        # host battery run time
        if "pack_wh" in h:
            wh = h["pack_wh"]
            if h["id"] == "H1":
                usable_to_leaf = wh * 0.95 * 0.97 * 0.96
                ap_on = DOCK_OVERHEAD_AP_ON
            else:
                usable_to_leaf = wh * 0.88 * 0.98 * 0.95        # bank boost and the 5 % end margin
                ap_on = None
            rt = {}
            for ln in LOAD_NAMES:
                pin, _ = leaf_side(C.LOADS[ln], v)
                rt[ln] = usable_to_leaf / (pin + (h["overhead_w"] if h["id"] == "H1" else 0.0))
            out["pack_hours"] = rt
            out["pack_Wh_at_vhv"] = usable_to_leaf
            if ap_on is not None:
                out["pack_hours_ap_on_delta"] = usable_to_leaf / (leaf_side(C.LOADS["delta session"], v)[0] + ap_on)
        # interface heat in the Leaf at the 8.7 W peak (a first estimate, the thermal team owns the number)
        if h["id"].startswith("H6"):
            prx = 8.7 / ETA_UQ
            heat = 2.062 * (prx / 25.0) ** 2 + 0.641 * (prx / 25.0) + prx * (1 / ETA_UQ - 1) * ETA_UQ
            out["leaf_heat_at_peak_W"] = heat
        else:
            i = need_peak / v
            leaf = 2.0 * i * i * R_LEAVES
            out["leaf_heat_at_peak_W"] = leaf + 8.7 / ETA_UQ * (1 - ETA_UQ)
        res["hosts"][h["id"]] = out

    # --------------------------------------------------------------- the table
    p("%-5s %-26s %8s %7s | %6s %6s | %7s %7s %7s %7s | heat at 8.7 W" % (
        "id", "host", "offer W", "eta", "8.7 W", "25 W", "stby", "delta", "video", "peak"))
    for h in HOSTS:
        o = res["hosts"][h["id"]]
        p("%-5s %-26s %8.1f %7.3f | %6s %6s | %7.2f %7.2f %7.2f %7.2f | %.2f W%s" % (
            h["id"], h["name"], o["offered_vhv_W"], o["eta_host"], "yes" if o["carries_peak"] else "NO",
            "yes" if o["carries_25W_case"] else "NO",
            o["host_Wh_per_h"]["standby"], o["host_Wh_per_h"]["delta session"], o["host_Wh_per_h"]["video"],
            o["host_Wh_per_h"]["peak"], o["leaf_heat_at_peak_W"], "  [5 V class, bypass loss]" if o["five_volt_class"] else ""))
    p("  columns: offered power on VHV, host-side chain efficiency, carries the 8.7 W peak, carries the 25 W port part case,")
    p("  host energy in Wh per hour of Leaf at each load (the standby of H0 and H1 includes the dock overhead), Leaf heat from the interface at the peak")
    p("")
    for h in HOSTS:
        o = res["hosts"][h["id"]]
        p("%s %s" % (h["id"], h["name"]))
        p("    offered: %s" % o["offered_note"])
        p("    interface: %s" % o["interface"])
        p("    chain: " + ", ".join("%s %.2f" % c for c in o["chain"]))
        p("    clamp: %s" % o["clamp"])
        if o["bus_window"]:
            p("    input window: %s" % o["bus_window"])
        p("    need on VHV: peak %.1f W, 25 W case %.1f W; margin at the peak %.1f W" % (o["need_at_vhv_peak_W"], o["need_at_vhv_25W_case_W"], o["margin_peak_W"]))
        if "pack_hours" in o:
            p("    the host battery delivers %.1f Wh to the VHV leaves; hours on the Leaf: " % o["pack_Wh_at_vhv"] +
              ", ".join("%s %.1f h" % kv for kv in o["pack_hours"].items()))
            if "pack_hours_ap_on_delta" in o:
                p("    with the dock Wi-Fi AP and 60 GHz radio on, the delta session runs %.1f h" % o["pack_hours_ap_on_delta"])
    p("")

    # --------------------------------------------------------------- the vehicle transients
    p("VEHICLE INPUT WINDOW, load dump energy into a clamp [GENERAL] by the ISO 16750-2 pulse (exponential, half time td)")
    ld = {}
    for name, us, ri, td, vc in (("12 V test A unsuppressed, 101 V, 4 ohm, 400 ms, clamp 36 V", 101.0, 4.0, 0.400, 36.0),
                                 ("12 V test A, 79 V, 0.5 ohm, 40 ms, clamp 36 V", 79.0, 0.5, 0.040, 36.0),
                                 ("24 V test A unsuppressed, 202 V, 8 ohm, 350 ms, clamp 70 V", 202.0, 8.0, 0.350, 70.0),
                                 ("24 V test A, 151 V, 1 ohm, 100 ms, clamp 70 V", 151.0, 1.0, 0.100, 70.0)):
        e = load_dump_energy(us, ri, td, vc)
        ld[name] = e
        p("  %-62s %7.1f J  (a 600 W, 1 ms TVS takes about 0.6 J, so a series OVP switch must take it)" % (name, e))
    res["load_dump_J"] = ld
    p("  The Leaf has no part in this. The PD adapter or the cradle stage owns the clamp. The Leaf sees a PD output that can drop out for 0.1 to 1 s.")
    p("  A cranking dropout becomes a hand-over gap of 0.1 to 3 s. The cell bridges it: see powerpath.py S1.")
    p("")

    # --------------------------------------------------------------- where the capacity goes
    p("WHERE THE CAPACITY GOES: nominal host energy, step by step, to the Leaf bus")
    wh = {}
    for hid, start in (("H1", 20.0), ("H5", 18.5)):
        o = res["hosts"][hid]
        steps = []
        if hid == "H1":
            seq = [("nominal", 1.0), ("usable window", 0.95), ("pack out", 0.97), ("dock 12 V stage", 0.96), ("leaves and U_Q", ETA_UQ * 0.999)]
        else:
            seq = [("nominal 3.7 V", 1.0), ("boost, protection", 0.88), ("port part", 0.98), ("end margin", 0.95), ("leaves and U_Q", ETA_UQ * 0.999)]
        e = start
        for nm, f in seq:
            e *= f
            steps.append((nm, e))
        wh[hid] = steps
        p("  %s: " % hid + " -> ".join("%s %.1f Wh" % s for s in steps))
        own = res["hosts"][hid]["pack_hours"]["delta session"]
        own_leaf = 7.38 * 0.96 / C.LOADS["delta session"]
        p("     delta session: %.1f h on the host battery against %.1f h on the Leaf Full cell (7.38 Wh at 750 Wh/L)" % (own, own_leaf))
    res["capacity_chain"] = wh
    p("")
    C.dump("hosts", res, LINES)
    plots(res)


def plots(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    ids = [h["id"] for h in HOSTS]
    names = ["%s %s" % (h["id"], h["name"]) for h in HOSTS]
    ys = np.arange(len(ids))
    for j, ln in enumerate(("delta session", "peak")):
        vals = [res["hosts"][i]["host_Wh_per_h"][ln] for i in ids]
        ax[0].barh(ys + (j - 0.5) * 0.36, vals, height=0.34, color=C.PAL[j], label=ln + " (%.1f W at the bus)" % C.LOADS[ln])
    ax[0].set_yticks(ys)
    ax[0].set_yticklabels(names, fontsize=8)
    ax[0].invert_yaxis()
    C.style(ax[0], "host energy per hour of Leaf, Wh", "", "Host energy per hour")
    ax[0].legend(fontsize=8, frameon=False, loc="lower right")
    # right: offered power against the two needs
    offered = [res["hosts"][i]["offered_vhv_W"] for i in ids]
    ax[1].barh(ys, offered, height=0.55, color=C.PAL[5])
    ax[1].axvline(res["hosts"]["H0"]["need_at_vhv_peak_W"], color=C.PAL[1], lw=1.5)
    ax[1].axvline(res["hosts"]["H0"]["need_at_vhv_25W_case_W"], color=C.PAL[0], lw=1.5)
    ax[1].text(res["hosts"]["H0"]["need_at_vhv_peak_W"] + 0.4, len(ids) - 0.3, "8.7 W peak", fontsize=8, color=C.PAL[1])
    ax[1].text(res["hosts"]["H0"]["need_at_vhv_25W_case_W"] + 0.4, len(ids) - 0.9, "25 W case", fontsize=8, color=C.PAL[0])
    ax[1].set_yticks(ys)
    ax[1].set_yticklabels([""] * len(ids))
    ax[1].invert_yaxis()
    C.style(ax[1], "offered power on VHV, W", "", "Offered power against the two needs")
    fig.tight_layout()
    fig.savefig(C.OUT + "/hosts.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
