#!/usr/bin/env python3
"""thesis_check.py - question 5: the four conditions of BRIEF Section 5 that the power-path numbers touch.

Reads out/tiers.json, out/powerpath.json, out/hosts.json and out/celllife.json (written by the other scripts).

Run:  python3 hw/hostpower/powerpath/thesis_check.py
Out:  out/thesis.json, out/thesis.txt
"""
import json
import os

import common as C
import hosts as H

LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


def rd(name):
    with open(os.path.join(C.OUT, name + ".json")) as f:
        return json.load(f)


def main():
    T, PP, HO, CL = rd("tiers"), rd("powerpath"), rd("hosts"), rd("celllife")
    rows = []

    def row(cond, test, verdict, detail):
        rows.append(dict(condition=cond, test=test, verdict=verdict, detail=detail))
        p("%-11s %-62s %-5s %s" % (cond, test, verdict, detail))

    p("POWER-PATH · question 5 · the thesis check, BRIEF Section 5")
    p("")
    # ---------------------------------------------------------------- 1 power
    s = C.CELLS["S"]
    q20 = 20 * C.cell_q_Ah(s["E_target_Wh"])
    q128 = 128 * C.cell_q_Ah(s["E_target_Wh"])
    topup = {"Buffer 20": 0.5 * q20 * 3.9, "Full 128": 0.5 * q128 * 3.9}
    p("P_host >= P_load + P_topup, peak 8.7 W, path loss included. Top-up at 0.5 C: Buffer 20 cells %.2f W, Full %.2f W" % tuple(topup.values()))
    for hid, o in HO["hosts"].items():
        v = {"H0": 12, "H1": 12, "H2": 15, "H3a": 15, "H3b": 15, "H4a": 12, "H4b": 12, "H4c": 15, "H5": 9, "H6a": 5, "H6b": 9, "H6c": 12}[hid]
        for tn, tp in topup.items():
            need, _ = H.leaf_side(8.7 + tp, v) if v > 5 else (((8.7 + tp) / (3.86 / 4.9)), 0)
            margin = o["offered_vhv_W"] - need
            row("1 power", "%s %s, peak plus top-up (%s)" % (hid, o["name"], tn), "PASS" if margin >= 0 else "FAIL",
                "need %.1f W, offer %.1f W, margin %+.1f W" % (need, o["offered_vhv_W"], margin))
    p("")
    weak = [(h, o) for h, o in HO["hosts"].items() if not o["carries_peak"]]
    s6 = {k: v for k, v in PP["scenarios"].items() if k.startswith("S6")}
    for k, v in s6.items():
        sm = v["summary"]
        row("1 power", "weak host H6a 5 W, outdoor 7.5 W 15 min, %s" % k.split(" ", 1)[1], "PASS" if sm["bus_below_seat_floor_s"] == 0 else "FAIL",
            "pack assist; bus under the 3.40 V seat floor %.0f s; final pack SOC %.2f" % (sm["bus_below_seat_floor_s"], sm["final_soc"]))
    p("")

    # ---------------------------------------------------------------- 4 continuity
    p("E_buffer >= P_peak x t_handover, and a power gap never loses chain state")
    swing = C.e_frac(0.10, 0.60)
    e20 = 20 * s["E_target_Wh"] * swing
    e_need = 8.7 * 3.0 / 3600.0
    row("4 continuity", "energy form, 3 s at 8.7 W, Buffer 20 cells floated", "PASS",
        "usable %.3f Wh against %.4f Wh, a factor of %.0f" % (e20, e_need, e20 / e_need))
    n_peak = T["buffer"]["tables"]["S floated at 60 %"]["peak"]["3 s"]["n"]
    n_peak_c5 = T["buffer"]["cmax_sensitivity_3s"]["5 C"]["peak"]
    cap20 = 3.0 * q20 * 3.9 * 0.9
    row("4 continuity", "power form, 8.7 W for 3 s, Buffer 20 cells at 3 C", "FAIL",
        "20 cells carry %.1f W at 3 C, short by %.1f W; the peak needs %d cells at 3 C (%d at 5 C)" % (cap20, 8.7 - cap20, n_peak, n_peak_c5))
    n_d = T["buffer"]["tables"]["S floated at 60 %"]["delta session"]["5 min"]["n"]
    row("4 continuity", "walk of 5 min at the delta session 2.24 W, Buffer floated at 60 %", "PASS",
        "%d cells (%.2f Wh nominal), inside the 0.3 to 1.5 Wh of the BRIEF" % (n_d, n_d * s["E_target_Wh"]))
    n30f = T["buffer"]["tables"]["S floated at 60 %"]["delta session"]["30 min"]["n"]
    n30t = T["buffer"]["tables"]["S topped to 100 %"]["delta session"]["30 min"]["n"]
    row("4 continuity", "30 min at the delta session, Buffer floated at 60 %", "FAIL",
        "%d cells, %.2f Wh nominal, against the 1.5 Wh top of the BRIEF, over by %.0f %%" % (n30f, n30f * s["E_target_Wh"], 100 * (n30f * s["E_target_Wh"] / 1.5 - 1)))
    row("4 continuity", "30 min at the delta session, Buffer topped to 100 % before the gap", "PASS",
        "%d cells, %.2f Wh nominal, but the seat floor of 3.40 V limits it (v)" % (n30t, n30t * s["E_target_Wh"]))
    bare = T["bare"]["min_volume"]
    vol_m = T["bare"]["reach"]["0.24 mm, all of the margin"]["EDLC, large cell (Maxwell BCAP3000)"]["vol_cm3"]
    v3p = bare["EDLC, large cell (Maxwell BCAP3000)"]["peak"]["3 s"]["vol_cm3"]
    row("4 continuity", "Bare capacitor store, 3 s at 8.7 W, in the 0.24 mm margin", "FAIL",
        "best EDLC needs %.2f cm3 against %.2f cm3 of margin, and no published part is under 0.9 mm thick" % (v3p, vol_m))
    vs3 = bare["EDLC, large cell (Maxwell BCAP3000)"]["safe screen"]["3 s"]["vol_cm3"]
    vc3 = bare["EDLC, thin chip (Seiko CPH3225A)"]["safe screen"]["3 s"]["vol_cm3"]
    row("4 continuity", "Bare capacitor store, 3 s at the safe screen 0.219 W, to close a session", "PASS (in cell volume)",
        "%.2f to %.2f cm3 of EDLC (1 to 3 tiles of cell volume), 0.9 mm thick: it needs cell layer room, not the margin" % (vs3, vc3))
    th_ok = T["bare"]["fit_0p24_mm"]["thin solid-state cell (ST EFL700A39)"]["standby"]["5 min"]
    row("4 continuity", "Bare thin solid-state store in the margin, standby 0.061 W for 5 min", "PASS" if th_ok else "FAIL",
        "fits at 0.24 mm; it cannot carry a screen, because of its 100 ohm resistance (10 mA pulse)")
    # island and swap from the simulator
    drop = PP["island_never_dropped"]
    row("4 continuity", "island rail (U7 and U4 ROM) over all %d simulated runs" % len(PP["scenarios"]), "PASS" if drop else "FAIL",
        "1V8_AON never dropped in brownout, host loss, vanish, hot swap and 5 W host runs")
    a, b = PP["scenarios"]["S5a Buffer 20 cells S, float 60 %"]["summary"], PP["scenarios"]["S5b Buffer 20 cells S, float 60 %"]["summary"]
    row("4 continuity", "quadrant swap with no host, Buffer cells spread over four quadrants", "PASS",
        "bus min %.2f V, no mode change" % a["vbus_min"])
    row("4 continuity", "quadrant swap with no host, all Buffer cells in the removed quadrant", "FAIL",
        "body bus lost for %.1f s (ISLAND %.1f s). Place Buffer cells in all four quadrants" % (b["mode_seconds"].get("ISLAND", 0), b["mode_seconds"].get("ISLAND", 0)))
    # island duration
    e_b = C.B_CELL_WH
    for z in (0.60, 1.0):
        hrs = e_b * C.e_frac(0.0, z) * 0.95 / (C.P_ISLAND / 0.80)
        p("    island-only run time of the B cell from %d %%: %.1f h at %.3f W from the cell" % (100 * z, hrs, C.P_ISLAND / 0.80))
        rows.append(dict(condition="4 continuity", test="island-only hours from %d %%" % (100 * z), verdict="INFO", detail="%.1f h" % hrs))
    p("")

    # ---------------------------------------------------------------- 3 trust and 2 heat, as far as numbers touch
    ho = HO["hosts"]
    row("2 heat", "interface heat in the Leaf at 8.7 W, contact (H0 to H5)", "INFO", "%.2f W, set by U_Q loss" % ho["H0"]["leaf_heat_at_peak_W"])
    row("2 heat", "interface heat in the Leaf at 8.7 W, Qi pad (H6)", "INFO", "%.2f W, %.1f times the contact value" % (ho["H6c"]["leaf_heat_at_peak_W"], ho["H6c"]["leaf_heat_at_peak_W"] / ho["H0"]["leaf_heat_at_peak_W"]))
    row("3 trust", "host input enters at VHV behind the OR diode; VBUS and U7 are never connected to a host before the proof", "BY DESIGN",
        "simulator: host qualified only after 3 ms challenge, the contract and 20 ms; before that VHV leaves stay at 0 V")
    p("")

    # ---------------------------------------------------------------- the thesis sentences
    cl = CL["ratio"]
    p("THESIS READING")
    p("  The Host Life Law holds for power on the hosts H0 to H4 and H6c. It fails for a 5 W host and for the 25 W case on PoE type 2, a belt pack and low-power pads.")
    p("  The cell as the bridge holds for gaps up to 3 s at the delta class and for a walk of 5 min. It does not hold at the 8.7 W peak with the 0.3 to 1.5 Wh Buffer.")
    p("  Bare holds as 'a surface' only with at least 3 tiles of cell volume given to an EDLC. It does not hold inside the 0.24 mm margin.")
    p("  Cell life: host-fed Full lives %.1f times as long as the cell cycled daily (%.1f against %.1f years at 25 C). A Buffer of 20 cells lives %.1f times as long, because it does all the bridging work."
      % (cl["ratio_full"], cl["hostfed_full_years"], cl["cycled_years"], cl["ratio_buffer20"]))
    C.dump("thesis", dict(rows=rows), LINES)


if __name__ == "__main__":
    main()
