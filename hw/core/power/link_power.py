#!/usr/bin/env python3
"""link_power.py - question 2 of the POWER seat: power over the link, four ways.

Options  P1 the 12 gold pads with the Core regulating VBUS (no stage on the Skin)
         P2 the 12 gold pads at VHV 12 V with the U_Q 3:1 stage on the Skin (the L.6.0 host path)
         P3 a flex tether with its own power conductors, at 12 V with U_Q on the Skin
         P4 a Qi-class coupling (the four sector coils), with and without a radio for the pixels
         P5 one hybrid cable for power and pixels, at 12 V with U_Q on the Skin

Run:  python3 hw/core/power/link_power.py
Out:  out/link_power.json, out/link_power.txt, out/link_power.png
"""
import numpy as np

import cpcommon as K

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


R_LEAF = 0.018            # ohm per leaf, hw/energy/03 [T]
WORN = 3.97               # worn pad factor, hw/hostpower/thermal [H]
ETA_UQ = 0.97             # U_Q 3:1 at its ratio [H]
V_SKIN = 3.90             # VBUS on the Skin at the float, the cells are gone so the Core sets it [D] proposed
RHO_CU = 1.72e-8
QI_CHAIN = 0.89 * 0.90    # pad supply, inverter and coil; coupling, shield and rectifier. hosts.py [H]
LEAF_RATING_A = 1.5       # per leaf [H] MON-16


def flex_r_per_m(w_mm=3.0, t_um=35.0):
    return RHO_CU / (w_mm * 1e-3 * t_um * 1e-6)


def qi_skin_heat(p_rx):
    """Heat in the Skin from coil, shield, lead and rectifier at p_rx W received. The 25 W chain of sim/thermal [H]."""
    return 2.062 * (p_rx / 25.0) ** 2 + 0.641 * (p_rx / 25.0)


def option(name, p_skin, extra_load=0.0, worn=False):
    """Returns the row for a Skin load p_skin W at VBUS."""
    wf = WORN if worn else 1.0
    P = p_skin + extra_load
    r = dict(option=name, load_W=P)
    if name == "P1 pads, VBUS direct":
        v = V_SKIN
        R = 2 * (R_LEAF / 2) * wf
        i = P / v
        loss = i * i * R
        r.update(V=v, I=i, R_loop_ohm=R, path_loss_W=loss, skin_heat_interface_W=loss, drop_V=i * R,
                 per_leaf_A=i / 2, ok_rating=i / 2 <= LEAF_RATING_A, conv_loss_skin_W=0.0,
                 data="2 pairs at 10 Gb/s, 19.4 Gb/s payload, need 13.9 [T] hw/display interface.txt")
    elif name == "P2 pads, VHV 12 V + U_Q":
        v = 12.0
        R = 2 * (R_LEAF / 2) * wf
        pin = P / ETA_UQ
        i = pin / v
        loss = i * i * R
        conv = pin - P
        r.update(V=v, I=i, R_loop_ohm=R, path_loss_W=loss + conv, skin_heat_interface_W=loss + conv, drop_V=i * R,
                 per_leaf_A=i / 2, ok_rating=i / 2 <= LEAF_RATING_A, conv_loss_skin_W=conv,
                 data="as P1")
    elif name.startswith("P3 flex tether"):
        L = 0.5 if "0.5" in name else 2.0
        v = 12.0
        R = 2 * flex_r_per_m() * L + 4 * 0.020
        pin = P / ETA_UQ
        i = pin / v
        loss = i * i * R
        conv = pin - P
        skin_conn = i * i * 0.040      # the Skin-end connector pair, 2 contacts of 20 mohm
        r.update(V=v, I=i, R_loop_ohm=R, path_loss_W=loss + conv, skin_heat_interface_W=skin_conn + conv, drop_V=i * R,
                 conv_loss_skin_W=conv, per_leaf_A=None, ok_rating=True,
                 data="as many pairs as the flex carries. 3 mm x 35 um Cu: %.3f ohm/m per conductor" % flex_r_per_m())
    elif name.startswith("P4 Qi"):
        radio = 0.6 if "radio" in name else 0.0
        P2 = P + radio / 0.88
        prx = P2 / ETA_UQ
        heat = qi_skin_heat(prx)
        conv = prx - P2
        total_loss = prx / QI_CHAIN - P2
        r.update(load_W=P2, V=12.0, I=prx / 12.0, R_loop_ohm=None, path_loss_W=total_loss, skin_heat_interface_W=heat + conv,
                 drop_V=None, conv_loss_skin_W=conv, per_leaf_A=None, ok_rating=prx <= 25.0,
                 data=("none for pixels: Qi load modulation is kb/s. A 60 GHz radio adds %.2f W on the Skin" % (radio / 0.88)) if radio else
                 "none for pixels: Qi load modulation carries kb/s, a second path is needed")
    elif name == "P5 hybrid cable":
        v = 12.0
        extra = 0.17 / 0.88          # USB4 class PHY at 15 pJ/bit plus the PD sink and retimer [H]
        P2 = P + extra
        pin = P2 / ETA_UQ
        i = pin / v
        R = 2 * 0.084 * 1.0 + 2 * 0.0125
        loss = i * i * R
        conv = pin - P2
        skin_conn = i * i * 0.0125
        r.update(load_W=P2, V=v, I=i, R_loop_ohm=R, path_loss_W=loss + conv, skin_heat_interface_W=skin_conn + conv, drop_V=i * R,
                 conv_loss_skin_W=conv, per_leaf_A=None, ok_rating=True,
                 data="40 Gb/s class [G] USB4. 1 m of 24 AWG, 0.084 ohm/m; Type-C contacts 25 mohm, 4 in parallel")
    r["skin_total_heat_W"] = r["load_W"] + r["skin_heat_interface_W"]
    r["eff_core_to_skin"] = r["load_W"] / (r["load_W"] + r["path_loss_W"])
    return r


def main():
    p("POWER seat · question 2 · power over the link, at the Skin load")
    loads = {
        "delta": K.skin_load("delta session, 250 nits, Wi-Fi")["skin_vbus_W"],
        "camera": K.skin_load("50 MP camera, viewfinder and upload")["skin_vbus_W"],
        "video": K.skin_load("video session, Wi-Fi")["skin_vbus_W"],
        "outdoor": K.skin_load("video outdoors, 800 nits, 5G")["skin_vbus_W"],
    }
    p("Skin load at VBUS, nominal: " + ", ".join("%s %.2f W" % kv for kv in loads.items()))
    p("limits: free-air still %.2f W, light wind %.2f W for the whole Skin [H]; the pad leaf rating is %.1f A [H]" % (K.LIMIT_STILL_W, K.LIMIT_WIND_W, LEAF_RATING_A))
    p("")
    names = ["P1 pads, VBUS direct", "P2 pads, VHV 12 V + U_Q", "P3 flex tether 0.5 m, 12 V + U_Q", "P3 flex tether 2.0 m, 12 V + U_Q",
             "P4 Qi, power only", "P4 Qi + 60 GHz radio for the pixels", "P5 hybrid cable"]
    res = {}
    for worn in (False, True):
        p("%s PADS" % ("WORN" if worn else "NEW"))
        p("  %-36s %-8s %6s %6s %8s %9s %9s %9s %7s | %s" % ("option", "load", "V", "I,A", "R,mohm", "path,mW", "iface,mW", "skinW", "eff", "verdict vs 1.73 / 2.37 W"))
        for ln, P in loads.items():
            for nm in names:
                r = option(nm, P, worn=worn)
                key = "%s %s %s" % ("worn" if worn else "new", nm, ln)
                res[key] = r
                st = "pass" if r["skin_total_heat_W"] <= K.LIMIT_STILL_W else ("wind only" if r["skin_total_heat_W"] <= K.LIMIT_WIND_W else "FAIL")
                p("  %-36s %-8s %6.1f %6.2f %8s %9.1f %9.1f %9.3f %6.1f%% | %s" % (
                    nm, ln, r["V"], r["I"], "-" if r["R_loop_ohm"] is None else "%.0f" % (1000 * r["R_loop_ohm"]),
                    1000 * r["path_loss_W"], 1000 * r["skin_heat_interface_W"], r["skin_total_heat_W"], 100 * r["eff_core_to_skin"], st))
            p("")
    p("READING (worn pads shown, the worst case)")
    d = {k: v for k, v in res.items() if k.startswith("worn")}
    for ln in loads:
        row = {nm: d["worn %s %s" % (nm, ln)] for nm in names}
        best = min(row.items(), key=lambda kv: kv[1]["skin_heat_interface_W"])
        worst = max(row.items(), key=lambda kv: kv[1]["skin_heat_interface_W"])
        p("  %-8s interface heat on the Skin: lowest %s %.0f mW, highest %s %.0f mW" % (
            ln, best[0], 1000 * best[1]["skin_heat_interface_W"], worst[0], 1000 * worst[1]["skin_heat_interface_W"]))
    p("")
    v1 = res["new P1 pads, VBUS direct video"]
    w1 = res["worn P1 pads, VBUS direct video"]
    q = res["new P4 Qi, power only video"]
    qr = res["new P4 Qi + 60 GHz radio for the pixels video"]
    h = res["new P5 hybrid cable video"]
    p("  P1 at the video load: %.2f A, %.1f mW new and %.1f mW worn, drop %.0f mV worn, %.2f A per leaf of 1.5 A" % (
        v1["I"], 1000 * v1["skin_heat_interface_W"], 1000 * w1["skin_heat_interface_W"], 1000 * w1["drop_V"], v1["per_leaf_A"]))
    p("  Qi at the video load: %.0f mW of interface heat on the Skin, %.1f times the pads. With a pixel radio the Skin total is %.2f W" % (
        1000 * q["skin_heat_interface_W"], q["skin_heat_interface_W"] / max(v1["skin_heat_interface_W"], 1e-9), qr["skin_total_heat_W"]))
    p("  hybrid cable at the video load: Skin total %.2f W, the PHY and PD sink add %.2f W to the Skin" % (h["skin_total_heat_W"], h["load_W"] - loads["video"]))
    p("")
    p("THE RULING FOR THE STUDY [HYPOTHESIS]")
    n1 = res["new P1 pads, VBUS direct video"]
    p2 = res["worn P2 pads, VHV 12 V + U_Q video"]
    f2 = res["worn P3 flex tether 2.0 m, 12 V + U_Q video"]
    p("  1. The pads win. The Core regulates VBUS and the Skin has no stage. Interface heat at the video load is %.0f mW new and %.0f mW worn." % (
        1000 * n1["skin_heat_interface_W"], 1000 * w1["skin_heat_interface_W"]))
    p("  2. The Core must sense the VBUS leaves through the back channel BC and hold %.2f V at the tiles. The worn drop is %.0f mV at the video load." % (
        V_SKIN, 1000 * w1["drop_V"]))
    p("  3. The U_Q stage costs the Skin %.0f mW more than the direct feed at the video load. It buys a lower current for a long cable." % (
        1000 * (p2["skin_heat_interface_W"] - w1["skin_heat_interface_W"])))
    p("  4. A 2 m flex tether at 12 V adds %.0f mW to the cable over the pads and nothing on the Skin beyond the stage." % (
        1000 * (f2["path_loss_W"] - p2["path_loss_W"])))
    p("  5. Qi-class power puts %.0f mW on the Skin, %.1f times the 12 V pads, and gives no pixels. The pixel radio adds %.2f W to the Skin." % (
        1000 * q["skin_heat_interface_W"], q["skin_heat_interface_W"] / p2["skin_heat_interface_W"], qr["load_W"] - q["load_W"]))
    p("  6. The hybrid cable shares a connector with the pixels. It is the best product shape and it costs the Skin the PHY: +%.2f W." % (h["load_W"] - loads["video"]))
    p("  7. Every option fails the 1.73 W ceiling at the outdoor video load of %.2f W. The load, not the interface, causes that." % loads["outdoor"])
    K.dump("link_power", res, LINES)
    plots(res, loads, names)


def plots(res, loads, names):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    short = ["P1 pads VBUS", "P2 pads 12 V", "P3 flex 0.5 m", "P3 flex 2 m", "P4 Qi", "P4 Qi + radio", "P5 hybrid"]
    for j, ln in enumerate(("delta", "video")):
        vals = [1000 * res["worn %s %s" % (nm, ln)]["skin_heat_interface_W"] for nm in names]
        ax[0].bar(np.arange(len(names)) + (j - 0.5) * 0.36, vals, width=0.34, color=K.PAL[j], label=ln + " (%.2f W)" % loads[ln])
    ax[0].set_yscale("log")
    ax[0].set_xticks(range(len(names)))
    ax[0].set_xticklabels(short, rotation=30, ha="right", fontsize=8)
    K.style(ax[0], "", "interface heat on the Skin, mW", "Interface heat, worn pads")
    ax[0].legend(fontsize=8, frameon=False)
    for j, nm in enumerate(names):
        ys = [res["worn %s %s" % (nm, ln)]["skin_total_heat_W"] for ln in ("delta", "camera", "video")]
        ax[1].plot(["delta", "camera", "video"], ys, "-o", color=K.PAL[j % len(K.PAL)], lw=1.4, ms=4, label=short[j])
    ax[1].axhline(K.LIMIT_STILL_W, color="#444", lw=1, ls=":")
    ax[1].axhline(K.LIMIT_WIND_W, color="#444", lw=1, ls="--")
    K.style(ax[1], "", "Skin heat total, W", "Skin heat: load plus interface")
    ax[1].legend(fontsize=7, frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(K.OUT + "/link_power.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
