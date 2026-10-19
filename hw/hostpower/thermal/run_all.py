#!/usr/bin/env python3
"""run_all.py - the THERMAL team study of hw/hostpower.

Question: when the host feeds the Leaf, is always-on possible under the 36.2 C skin
limit, and through which interface?

    python3 run_all.py            # about 1 to 3 minutes

Out: out/selfcheck.txt, out/item1_cases.{json,txt}, out/item2_admission.{json,txt},
     out/item3_feed_vs_charge.{json,txt}, out/eyewear.{json,txt},
     out/item5_throttle.{json,txt}, out/thesis_check.{json,txt}, out/summary.json,
     out/plots 01..06 (PNG)
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import hostthermal as H
import eyewear

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PLOTS = os.path.join(OUT, "plots")
os.makedirs(PLOTS, exist_ok=True)

# validated default palette (dataviz skill, references/palette.md), fixed slot order
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
CRIT, INK, INK2, GRID = "#d03b3b", "#0b0b0b", "#52514e", "#e1e0d9"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 2.0, "font.size": 9, "legend.frameon": False,
})

SESSIONS = ("delta", "video_wifi", "5g_outdoor")
SLABEL = {"delta": "delta 2.5 W", "video_wifi": "video Wi-Fi 3.3 W", "5g_outdoor": "5G outdoor 4.2 W"}
IF_ORDER = ("battery", "contact_lo", "contact_hi", "contact_i2r", "qi_bpp", "qi_epp", "qi_mpp")
ADM_IFACES = ("battery", "contact_lo", "contact_hi", "qi_bpp", "qi_epp", "qi_mpp")
ICOL = {"battery": S[0], "battery_table": INK2, "contact_lo": S[1], "contact_hi": S[1], "contact_i2r": S[5],
        "qi_bpp": S[2], "qi_epp": S[3], "qi_mpp": S[4]}
ILS = {"contact_hi": "--"}
LIM = H.T_LIM
AMBS = (20.0, 25.0, 30.0, 35.0)

T0 = time.time()
SUMMARY = {}
W = lambda path, lines: open(os.path.join(OUT, path), "w").write("\n".join(lines) + "\n")


def J(path, obj):
    with open(os.path.join(OUT, path), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def wind_of(sess):
    return H.SESS_WIND[sess]


def rd(x, n=2):
    return round(float(x), n)


def mlabel(iface, mode):
    return H.IFACES[iface]["label"] + ("" if mode == "float" or iface in ("battery",) else
                                       {"topup": ", cell +0.2 C", "charge": ", cell charges at cap"}
                                       .get(mode, ", cell +%s C" % mode[1:]))


# ==========================================================================
# 0. self check against sim/thermal
# ==========================================================================
def selfcheck():
    L = ["SELF CHECK against sim/thermal/README.md (L.6.0), fixed body, 25 C", ""]
    chk = {}
    r = H.point("delta", "battery", "float", 25.0, False, False)
    chk["delta battery 25C hottest"] = (r["T_gate"], 41.3, 0.1)
    n = H.Network(H.FIX)
    q_up = H.LT.session_q(n, "video")
    chk["battery heat vs session_q, W"] = (r["Q_leaf"], float(q_up.sum()), 1e-9)
    sus = H.sustained("delta", "battery", "float", 25.0, False, False)
    chk["delta battery sustained, W"] = (sus["P_thermal"], 1.73, 0.03)
    r5 = H.point("5g_outdoor", "battery", "float", 25.0, True, False)
    chk["5G battery 25C hottest"] = (r5["T_gate"], 44.9, 0.1)
    # the Qi 25 W received charge on the puck, no session load, cell charging
    ccfg = H.FIX.copy(V_rect=15.0)
    Lc = H.charge_losses(ccfg, 25.0)
    chk["Qi 25 W device heat total, W"] = (
        sum(v for k, v in Lc.items() if not k.startswith("_")), 6.93, 0.02)
    ok = True
    for k, (a, b, tol) in chk.items():
        good = abs(a - b) <= tol
        ok &= good
        L.append("%-40s model %8.3f  reference %8.3f  tol %.3f  %s" % (k, a, b, tol, "ok" if good else "DIFF"))
    L.append("")
    L.append("all checks pass: %s" % ok)
    W("selfcheck.txt", L)
    print("\n".join(L))
    SUMMARY["selfcheck_pass"] = bool(ok)
    return ok


# ==========================================================================
# 1. the cases
# ==========================================================================
CASE_MODES = (("battery", "float"), ("battery_table", "float"), ("contact_lo", "float"), ("contact_hi", "float"),
              ("contact_i2r", "float"),
              ("qi_bpp", "float"), ("qi_bpp", "topup"),
              ("qi_epp", "float"), ("qi_epp", "topup"),
              ("qi_mpp", "float"), ("qi_mpp", "topup"))


def item1():
    res = {}
    L = ["ITEM 1 - CASES: steady hottest point of the fixed body for session x interface",
         "T_skin = hottest touchable surface (front cap, ring shell, bar, back skin). T_cap = hottest front cap tile.",
         "margin = 36.2 C minus T_skin. A negative margin fails condition 2 of BRIEF Section 5.",
         "Free-air rows: battery and contact hang in still air (5G: light wind). Qi rows lie on a passive puck.",
         "Dock rows: the Leaf lies on the 22 C regulated cold plate of hw/dock.",
         "Cell float: zero cell current. topup: the cell gains 0.2 C (1.14 W) in addition.", ""]
    for amb in (25.0, 30.0):
        for plate in (False, True):
            L.append("--- ambient %.0f C, %s ---" % (amb, "dock cold plate" if plate else "no cold plate"))
            L.append("%-34s %-17s %7s %7s %7s %-14s %7s %7s %6s" % (
                "case", "session", "T_skin", "T_cap", "margin", "hottest", "Q_leaf", "P_rx", "host"))
            for sess in SESSIONS:
                wind = wind_of(sess)
                for iface, mode in CASE_MODES:
                    r = H.point(sess, iface, mode, amb, wind, plate)
                    key = f"{amb:.0f}C|{'dock' if plate else 'open'}|{sess}|{iface}|{mode}"
                    res[key] = dict(T_skin=rd(r["T_gate"]), T_cap=rd(r["T_front_max"]),
                                    margin=rd(LIM - r["T_gate"]), where=r["where"],
                                    Q_leaf_W=rd(r["Q_leaf"], 3), P_rx_W=rd(r["P_rx"], 3),
                                    P_cell_net_W=rd(r["P_net"], 3), P_load_W=rd(r["P_L"], 3),
                                    host_limited=bool(r["host_limited"]), tec_ok=bool(r["tec_ok"]),
                                    T_cell_max=rd(r["T_cell_max"]), T_pad=rd(r["T_pad"]))
                    L.append("%-34s %-17s %7.1f %7.1f %+7.1f %-14s %7.2f %7.2f %6s" % (
                        mlabel(iface, mode), SLABEL[sess], r["T_gate"], r["T_front_max"],
                        LIM - r["T_gate"], r["where"], r["Q_leaf"], r["P_rx"],
                        "LIMIT" if r["host_limited"] else "ok"))
                L.append("")
    # the unfixed baseline body, for the record
    L.append("--- reference: the unfixed L.6.0 baseline body, battery only, 25 C free air ---")
    for sess in SESSIONS:
        r = H.point(sess, "battery", "float", 25.0, wind_of(sess), False, body="baseline")
        res[f"baseline_body|25C|{sess}"] = dict(T_skin=rd(r["T_gate"]), T_cap=rd(r["T_front_max"]),
                                                where=r["where"])
        L.append("%-20s T_skin %.1f C (%s)" % (SLABEL[sess], r["T_gate"], r["where"]))
    J("item1_cases.json", res)
    W("item1_cases.txt", L)
    SUMMARY["item1_file"] = "out/item1_cases.txt"
    # plot: 25 C open, bars per session
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)
    modes = [m for m in CASE_MODES if m[1] == "float"]
    for ax, sess in zip(axs, SESSIONS):
        vals = [res[f"25C|open|{sess}|{i}|{m}"]["T_skin"] for i, m in modes]
        xs = np.arange(len(modes))
        ax.bar(xs, [v - 20 for v in vals], bottom=20, color=[ICOL[i] for i, _ in modes], width=0.65)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.5, "%.1f" % v, ha="center", fontsize=7.5, color=INK)
        ax.axhline(LIM, color=CRIT, lw=1.4)
        ax.set_xticks(xs)
        ax.set_xticklabels(["battery\nin air", "battery\non table", "contact\n0.10 W", "contact\n0.34 W", "contact\nI2R", "Qi BPP\n5 W",
                            "Qi EPP\n15 W", "Qi MPP\n25 W"], fontsize=7)
        ax.set_title(SLABEL[sess], fontsize=9, color=INK)
        ax.set_ylim(20, 62)
        ax.grid(axis="x", visible=False)
    axs[0].set_ylabel("steady hottest skin point, C (25 C ambient, fixed body)")
    axs[0].text(-0.4, 59.0, "red line: the 36.2 C limit", color=CRIT, fontsize=8.5)
    fig.suptitle("Item 1: every interface fails the 36.2 C limit in free air at 25 C", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "01_cases_25C.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
# 2. the admission table
# ==========================================================================
QI3 = ("qi_bpp", "qi_epp", "qi_mpp")
ADM_ENTRIES = [("battery", "float"), ("battery_table", "float"), ("contact_lo", "float"), ("contact_hi", "float")] + \
              [(i, "float") for i in QI3] + [(i, "topup") for i in QI3] + [(i, "charge") for i in QI3]
SHORT = {"battery": "bat", "battery_table": "tbl", "contact_lo": "ct.10", "contact_hi": "ct.34",
         "qi_bpp": "BPP", "qi_epp": "EPP", "qi_mpp": "MPP"}


def col_name(i, m):
    return SHORT[i] + {"float": "", "topup": "+t", "charge": "+chg"}[m]


def item2():
    res = {}
    L = ["ITEM 2 - ADMISSION TABLE: highest sustained session power at the loads that holds 36.2 C",
         "Value in W at the loads, for the shape of each session. ON = the full session is always-on. C = the host cap binds.",
         "Columns: bat battery only in air; tbl battery lying on a table; ct.10, ct.34 contact with 0.10 or 0.34 W loss; BPP, EPP, MPP = Qi class 5, 15, 25 W.",
         "float = the host feeds the load. +t = the cell also gains 0.2 C. +chg = the host input sits at its class cap and the cell takes the rest.",
         "Nominal powers: delta 2.50 W, video Wi-Fi 3.27 W, 5G outdoor 4.18 W.",
         "Entries: host feeds the load with the cell floating (float), or the cell also gains 0.2 C (topup).",
         "limit: T = thermal, C = host cap (the Qi class cannot carry the load).", ""]
    for plate in (False, True):
        for wind in (False, True):
            for sess in SESSIONS:
                L.append("=== %s | %s | %s ===" % ("dock cold plate" if plate else "no cold plate",
                                                  "light wind" if wind else "still air", SLABEL[sess]))
                hdr = "%-7s" % "T_amb" + "".join("%-11s" % col_name(i, m) for i, m in ADM_ENTRIES)
                L.append(hdr)
                for amb in AMBS:
                    row = "%-7s" % ("%d C" % amb)
                    for iface, mode in ADM_ENTRIES:
                        s = H.sustained(sess, iface, mode, amb, wind, plate)
                        key = f"{'dock' if plate else 'open'}|{'wind' if wind else 'still'}|{amb:.0f}C|{sess}|{iface}|{mode}"
                        res[key] = dict(P_adm_W=rd(s["P_adm"], 3), P_thermal_W=rd(s["P_thermal"], 3),
                                        P_cap_W=rd(s["P_cap"], 3), limit=s["limit"],
                                        always_on=s["always_on"])
                        tag = "ON" if s["always_on"] else ("C" if s["limit"] == "host cap" else "")
                        row += "%-11s" % ("%.2f %s" % (s["P_adm"], tag))
                    L.append(row)
                L.append("")
    # the largest Qi class for each session
    L.append("=== the Qi classes that allow an always-on session. Rule A: cell floats. Rule B: host charges the cell at its cap ===")
    L.append("%-6s %-6s %-8s %-6s %-14s %-14s %-14s" % ("plate", "wind", "T_amb", "rule", SLABEL["delta"][:13],
                                                           SLABEL["video_wifi"][:13], SLABEL["5g_outdoor"][:13]))
    big = {}
    for plate in (False, True):
        for wind in (False, True):
            for amb in AMBS:
                for rule, mode in (("A", "float"), ("B", "charge")):
                    row = []
                    for sess in SESSIONS:
                        ok = [i for i in QI3 if res[f"{'dock' if plate else 'open'}|{'wind' if wind else 'still'}|{amb:.0f}C|{sess}|{i}|{mode}"]["always_on"]]
                        row.append("/".join(SHORT[i] for i in ok) if ok else "none")
                        big[f"{'dock' if plate else 'open'}|{'wind' if wind else 'still'}|{amb:.0f}C|{sess}|{rule}"] = ok
                    L.append("%-6s %-6s %-8s %-6s %-14s %-14s %-14s" % (
                        "dock" if plate else "none", "wind" if wind else "still", "%d C" % amb, rule, *row))
    res["always_on_qi_classes"] = big
    J("item2_admission.json", res)
    W("item2_admission.txt", L)
    # plot: delta shape and video shape, still air, versus ambient
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.6), sharey="row")
    for ri, sess in enumerate(("delta", "video_wifi")):
        for ci, plate in enumerate((False, True)):
            ax = axs[ri, ci]
            for iface, mode in ADM_ENTRIES:
                if mode != "float":
                    continue
                ys = [res[f"{'dock' if plate else 'open'}|still|{a:.0f}C|{sess}|{iface}|{mode}"]["P_adm_W"]
                      for a in AMBS]
                ax.plot(AMBS, ys, color=ICOL[iface], ls=ILS.get(iface, "-"), marker="o", ms=4,
                        label=H.IFACES[iface]["label"])
            ax.axhline(H.sess_total(sess), color=INK2, lw=1.0, ls=":")
            ax.text(20.1, H.sess_total(sess) + 0.1, "session %.2f W" % H.sess_total(sess), color=INK2, fontsize=8)
            ax.set_title("%s, %s, still air" % (SLABEL[sess], "dock cold plate" if plate else "no cold plate"),
                         fontsize=9, color=INK)
            ax.set_xlabel("ambient, C")
            ax.set_xticks(AMBS)
            if ci == 0:
                ax.set_ylabel("admitted load power, W")
    axs[0, 0].legend(fontsize=7, loc="upper right")
    fig.suptitle("Item 2: sustained load power that holds 36.2 C. Dotted line = the session power", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "02_admission.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
# 3. the feed-the-load rule
# ==========================================================================
def item3():
    res = {}
    L = ["ITEM 3 - FEED-THE-LOAD RULE: the host feeds the load and the cell floats,",
         "against the host that also charges the cell during the session.",
         "Q_leaf is the heat inside the Leaf. saved = Q_leaf(charge) - Q_leaf(float). wall = DC draw of the host side.",
         "modes: float, +0.2 C (1.14 W), 1 C (5.7 W), cap (host input at the class cap, the cell takes the rest).",
         ""]
    modes = (("float", "float"), ("topup", "+0.2 C"), ("c1.0", "1 C"), ("charge", "cap"))
    for amb, plate in ((25.0, False), (25.0, True), (30.0, False)):
        L.append("--- ambient %.0f C, %s ---" % (amb, "dock cold plate" if plate else "Qi puck / free air"))
        L.append("%-26s %-16s %-7s %7s %7s %7s %7s %7s %6s" % (
            "interface", "session", "mode", "Q_leaf", "saved", "T_skin", "dT", "wall W", "cellW"))
        for iface in ("contact_lo", "qi_bpp", "qi_epp", "qi_mpp"):
            for sess in SESSIONS:
                base = None
                for mode, mlabel_ in modes:
                    r = H.point(sess, iface, mode, amb, wind_of(sess), plate)
                    if base is None:
                        base = r
                    key = f"{amb:.0f}C|{'dock' if plate else 'open'}|{iface}|{sess}|{mode}"
                    res[key] = dict(Q_leaf=rd(r["Q_leaf"], 3), saved_vs_float=rd(r["Q_leaf"] - base["Q_leaf"], 3),
                                    T_skin=rd(r["T_gate"]), dT_vs_float=rd(r["T_gate"] - base["T_gate"]),
                                    P_wall=rd(r["P_wall"], 3), P_cell_net=rd(r["P_net"], 3),
                                    P_rx=rd(r["P_rx"], 3), host_limited=bool(r["host_limited"]))
                    L.append("%-26s %-16s %-7s %7.2f %7.2f %7.1f %+7.1f %7.2f %6.2f%s" % (
                        H.IFACES[iface]["label"][:26], SLABEL[sess], mlabel_, r["Q_leaf"],
                        r["Q_leaf"] - base["Q_leaf"], r["T_gate"], r["T_gate"] - base["T_gate"],
                        r["P_wall"], r["P_net"], "  host-limited" if r["host_limited"] else ""))
                L.append("")
    # what the rule is worth in admitted power, Qi puck at 25 C, delta shape
    L.append("--- sustained delta-shape load, Qi puck, 25 C still air (W at the loads) ---")
    adm = {}
    for iface in QI3:
        row = {}
        for mode, ml in modes:
            s = H.sustained("delta", iface, mode, 25.0, False, False)
            row[mode] = rd(s["P_adm"], 3)
        adm[iface] = row
        L.append("%-18s float %.2f W, +0.2 C %.2f W, 1 C %.2f W, cap %.2f W" % (
            H.IFACES[iface]["label"], row["float"], row["topup"], row["c1.0"], row["charge"]))
    res["sustained_delta_puck_25C"] = adm
    # wall energy per hour
    J("item3_feed_vs_charge.json", res)
    W("item3_feed_vs_charge.txt", L)
    # plot: Qi MPP, three sessions, heat by mode, 25 C puck
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, iface in zip(axs[:2], ("qi_mpp", "qi_epp")):
        xs = np.arange(len(SESSIONS))
        wd = 0.2
        for k, (mode, ml) in enumerate(modes):
            vals = [res[f"25C|open|{iface}|{s}|{mode}"]["Q_leaf"] for s in SESSIONS]
            ax.bar(xs + (k - 1.5) * wd, vals, width=wd - 0.02, color=S[k], label="cell: " + ml)
            for x, v in zip(xs, vals):
                ax.text(x + (k - 1.5) * wd, v + 0.1, "%.1f" % v, ha="center", fontsize=7, color=INK)
        ax.set_xticks(xs)
        ax.set_xticklabels([SLABEL[s] for s in SESSIONS], fontsize=8)
        ax.set_ylabel("heat inside the Leaf, W")
        ax.set_title(H.IFACES[iface]["label"] + ", 25 C", fontsize=9, color=INK)
        ax.grid(axis="x", visible=False)
    axs[0].legend(fontsize=7.5, loc="upper left")
    ax = axs[2]
    xs = np.arange(3)
    for k, (mode, ml) in enumerate(modes):
        vals = [adm[i][mode] for i in QI3]
        ax.bar(xs + (k - 1.5) * 0.2, vals, width=0.18, color=S[k], label="cell: " + ml)
        for x, v in zip(xs, vals):
            ax.text(x + (k - 1.5) * 0.2, v + 0.05, "%.1f" % v, ha="center", fontsize=7, color=INK)
    ax.axhline(2.5, color=INK2, lw=1.0, ls=":")
    ax.text(-0.45, 2.6, "delta session 2.5 W", color=INK2, fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels(["Qi BPP 5 W", "Qi EPP 15 W", "Qi MPP 25 W"], fontsize=8)
    ax.set_ylabel("admitted load, W (delta shape)")
    ax.set_title("sustained load under 36.2 C, puck, 25 C still air", fontsize=9, color=INK)
    ax.grid(axis="x", visible=False)
    fig.suptitle("Item 3: heat of feeding the load against charging the cell during the session", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "03_feed_vs_charge.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
# 4. eyewear
# ==========================================================================
def item4():
    res, lines = eyewear.run()
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    tas = np.arange(15, 38.1, 1.0)
    for wind, col, lab in ((False, S[0], "still air"), (True, S[1], "light wind")):
        ax.plot(tas, [eyewear.p_max(t, wind) for t in tas], color=col, label=lab)
    ax.axhspan(0.4, 1.2, color=S[2], alpha=0.15)
    ax.text(15.3, 1.22, "Frame loads, display on, 0.4 to 1.2 W", color=INK2, fontsize=8)
    ax.set_xlabel("ambient, C")
    ax.set_ylabel("heat the Frame holds under 36.2 C, W")
    ax.set_title("Item 4: face-side limit, two-node model, skin 34 C", fontsize=9, color=INK)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "04_eyewear.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
# 5. the throttle
# ==========================================================================
def item5():
    res = {}
    L = ["ITEM 5 - THROTTLE: steady state of the law of sim/thermal (derate on the hottest skin point)",
         "law: full to 34.2 C, 20 % at 36.0 C, off at 36.2 C. The floor of the existing run is 30 %.",
         "s_whole: display, stream and radio scale together (the run of sim/thermal). disp W = s_whole x the display term.",
         "s_disp: only the tiles scale and the ring chips keep their power. 0.00 means the ring alone is too hot.",
         "nits35 = display power held converted by FINAL/17 Section 17.13: 250 nits at 0.60 W and 35 % picture level.",
         "apl250 = the same power as a picture level at 250 nits. state: full, throttle, or BELOW the 30 % floor (the law cuts off).",
         ""]
    for amb in (30.0, 25.0):
        L.append("=== ambient %.0f C ===" % amb)
        L.append("%-26s %-17s %-6s %7s %7s %-8s %7s %7s %7s" % (
            "interface", "session", "plate", "s_whole", "s_disp", "state", "disp W", "nits35", "apl250"))
        for plate in (False, True):
            for sess in SESSIONS:
                for iface in ADM_IFACES:
                    w = wind_of(sess)
                    a = H.throttle_steady(sess, iface, "float", amb, w, plate, display_only=False)
                    b = H.throttle_steady(sess, iface, "float", amb, w, plate, display_only=True)
                    pd = a["s"] * H.DISPLAY_W[sess]
                    st = ("full" if a["state"] == "full" else "throttle" if a["state"] == "throttled" else "BELOW")
                    key = f"{amb:.0f}C|{'dock' if plate else 'open'}|{sess}|{iface}"
                    res[key] = dict(s_whole=rd(a["s"], 3), state=st, T_whole=rd(a["T"]),
                                    s_display_only=rd(b["s"], 3), display_W_held=rd(pd, 3),
                                    nits_at_apl35=rd(H.nits_at_apl35(pd), 0),
                                    apl_at_250nits=rd(H.apl_at_250nits(pd), 1))
                    L.append("%-26s %-17s %-6s %7.2f %7.2f %-8s %7.2f %7.0f %7.1f" % (
                        H.IFACES[iface]["label"][:26], SLABEL[sess], "dock" if plate else "none", a["s"], b["s"],
                        st, pd, H.nits_at_apl35(pd), H.apl_at_250nits(pd)))
                L.append("")
    J("item5_throttle.json", res)
    W("item5_throttle.txt", L)
    # plot: the held fraction of the session at 30 C, no cold plate (the dock holds 100 %)
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ifs = ADM_IFACES
    xs = np.arange(len(SESSIONS))
    wd = 0.13
    for k, iface in enumerate(ifs):
        vals = [res[f"30C|open|{s}|{iface}"]["s_whole"] * 100 for s in SESSIONS]
        ax.bar(xs + (k - 2.5) * wd, vals, width=wd - 0.015, color=ICOL[iface],
               label=H.IFACES[iface]["label"], alpha=1.0 if iface != "contact_hi" else 0.6)
    ax.axhline(30, color=CRIT, lw=1.2)
    ax.text(2.45, 33.0, "30 % floor of the law", color=CRIT, fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels([SLABEL[s] for s in SESSIONS], fontsize=8)
    ax.set_ylim(0, 108)
    ax.set_ylabel("session power held, % of the nominal")
    ax.set_title("Item 5: steady state of the throttle law at 30 C, no cold plate. The dock holds 100 %",
                 fontsize=9, color=INK)
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "05_throttle.png"), dpi=130)
    plt.close(fig)
    return res


# ==========================================================================
# the dock TEC check
# ==========================================================================
def dock_tec():
    L = ["DOCK TEC CHECK: the 22 C cold plate of hw/dock holds the set-point for every case of Item 2?",
         "q_need = 0.87 x Leaf heat + Tx coil loss (Qi) + 0.15 W/K x (T_amb - 22). Solved with hw/dock/budget.py solve_tec.", "",
         "%-8s %-17s %-30s %7s %7s %7s %7s %6s" % ("T_amb", "session", "case", "q_need", "P_tec", "Q_hot", "T_hot", "COP")]
    res = {}
    for amb in (25.0, 35.0):
        for sess in SESSIONS:
            for iface, mode in (("battery", "float"), ("contact_hi", "float"), ("qi_mpp", "float"), ("qi_mpp", "charge")):
                r = H.point(sess, iface, mode, amb, wind_of(sess), True)
                q_need = (r["Q_leaf"] * H.DP.F_DEVICE_HEAT_TO_PAD + r["tx_coil_loss"]
                          + H.DP.UA_PAD_LEAK * (amb - H.DP.PAD_SETPOINT))
                sol = H.DB.solve_tec(amb, max(q_need, 0.01))
                key = f"{amb:.0f}C|{sess}|{iface}|{mode}"
                if sol:
                    res[key] = dict(q_need=rd(q_need), P_tec=rd(sol["P_tec"]), Q_hot=rd(sol["Q_hot"]),
                                    T_hot=rd(sol["T_hot"]), COP=rd(sol["COP"]))
                    L.append("%-8s %-17s %-30s %7.2f %7.2f %7.2f %7.1f %6.2f" % (
                        "%d C" % amb, SLABEL[sess], mlabel(iface, mode)[:30], q_need, sol["P_tec"],
                        sol["Q_hot"], sol["T_hot"], sol["COP"]))
                else:
                    res[key] = dict(q_need=rd(q_need), feasible=False)
                    L.append("%-8s %-17s %-30s %7.2f   NO CURRENT HOLDS 22 C" % ("%d C" % amb, SLABEL[sess],
                                                                                mlabel(iface, mode)[:30], q_need))
    res["qmax_W"] = {f"{a:.0f}C": rd(H.tec_qmax(a)) for a in AMBS}
    L.append("")
    L.append("the TEC pumps at least %.0f W at the set-point from 20 to 35 C (check cap 32 W). Item 2 needs at most 12 W." %
             min(res["qmax_W"].values()))
    L.append("dew point: at 35 C and 60 percent relative humidity it is about 26 C, above the 22 C plate. Open issue.")
    J("dock_tec.json", res)
    W("dock_tec.txt", [l.replace("%%", "%") for l in L])
    return res


# ==========================================================================
# the thesis check
# ==========================================================================
def thesis():
    res = {}
    L = ["THESIS CHECK - condition 2 of BRIEF Section 5 for the nominal session, margin in K (36.2 C minus T_skin)",
         "A negative number fails by that many degrees. Cell floats. 5G has the light wind.", ""]
    for plate in (False, True):
        L.append("--- %s ---" % ("dock cold plate" if plate else "no cold plate (Qi: passive puck)"))
        L.append("%-12s %-18s " % ("T_amb", "session") + "".join("%-13s" % H.IFACES[i]["label"].split(",")[0][:12] for i in ADM_IFACES))
        for amb in (20.0, 25.0, 30.0, 35.0):
            for sess in SESSIONS:
                row = "%-12s %-18s " % ("%d C" % amb, SLABEL[sess])
                for iface in ADM_IFACES:
                    r = H.point(sess, iface, "float", amb, wind_of(sess), plate)
                    m = LIM - r["T_gate"]
                    res[f"{'dock' if plate else 'open'}|{amb:.0f}C|{sess}|{iface}"] = dict(
                        margin=rd(m), T_skin=rd(r["T_gate"]), passes=bool(m >= 0 and r["tec_ok"] and r["cell_ok"]))
                    row += "%-13s" % ("%+.1f" % m)
                L.append(row)
        L.append("")
    # counts
    npass = sum(1 for k, v in res.items() if v["passes"] and k.startswith("open"))
    ntot = sum(1 for k in res if k.startswith("open"))
    dpass = sum(1 for k, v in res.items() if v["passes"] and k.startswith("dock"))
    dtot = sum(1 for k in res if k.startswith("dock"))
    res["_counts"] = dict(open_pass=npass, open_total=ntot, dock_pass=dpass, dock_total=dtot)
    L.append("passing combinations: no cold plate %d of %d, dock cold plate %d of %d" % (npass, ntot, dpass, dtot))
    J("thesis_check.json", res)
    W("thesis_check.txt", L)
    print("\n".join(L))
    SUMMARY["thesis_counts"] = res["_counts"]
    return res


# ==========================================================================
if __name__ == "__main__":
    ok = selfcheck()
    for f in (item1, item2, item3, item4, item5, dock_tec, thesis):
        t = time.time()
        print("running", f.__name__, flush=True)
        f()
        print("   %.1f s" % (time.time() - t), flush=True)
    SUMMARY["runtime_s"] = round(time.time() - T0, 1)
    J("summary.json", SUMMARY)
    print("done in %.1f s" % SUMMARY["runtime_s"])
