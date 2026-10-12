#!/usr/bin/env python3
"""schedule.py - the program network of the Budlum Leaf L.6.0 build.

The Program Office. A critical path method (CPM) solve over the work
packages of program/PLAN.md. Month 0 is 2026-11-01. Each duration is a
[HYPOTHESIS] of the Program Office, set from the lead times of the
technology class. The script prints the early start, the late start, the
float and the critical path, and writes schedule.json.

Run: python3 schedule.py
"""
import json
import os
from datetime import date

START = date(2026, 11, 1)

# id: (name, months, predecessors, owner team, gate)
TASKS = {
    "T00": ("concept freeze, partner short list, NDAs, sample orders", 3, [], "program", "PRG"),
    # display, 508 ppi micro-LED on glass
    "D1": ("508 ppi test tile on glass, 5 um chips, 50.0 um pitch", 12, ["T00"], "hw/display", "DSP-19"),
    "D2": ("pixel uIC, 28 nm, one per 2 x 2 pixels, tape-out and silicon", 14, ["T00"], "hw/display", "DSP-19"),
    "D3": ("integrated tile: uIC, TGV glass, black cut face, seam coupon", 9, ["D1", "D2"], "hw/display", "DSP-19"),
    "D4": ("128-tile EVT set, known-good tiles, laser repair", 6, ["D3"], "hw/display", "DSP-19"),
    "D5": ("DVT tile lot, yield learning, edge margin 16 um", 6, ["EVT"], "hw/display", "DSP-19"),
    "D6": ("micro-LED tile line qualification at rate", 8, ["D5"], "hw/display", "DSP-19"),
    # cells
    "C1": ("Si-C coin-cell dilatometry, scaffold swell 22 %", 4, ["T00"], "hw/energy", "ENR-22"),
    "C2": ("30 um welded can, alumina-Pt feedthrough supplier", 10, ["T00"], "hw/energy", "ENR-22"),
    "C3": ("micro cell A-sample, 9.25 x 9.25 x 0.90 mm", 6, ["C1", "C2"], "hw/energy", "ENR-22"),
    "C4": ("micro cell B-sample, fuse test, 128-cell body set", 8, ["C3"], "hw/energy", "ENR-23"),
    "C5": ("C-sample, IEC 62133-2, UN 38.3 file", 7, ["C4", "EVT"], "hw/energy", "ENR-22"),
    # body mechanics and seam
    "H1": ("4 x 4 tile coupon: edge-on hinge, skin, caps", 8, ["T00"], "sim/mechanics", "MEC-42"),
    "H2": ("full 128-tile body with ribbons and kinematic seats", 6, ["H1"], "cad/l6", "MEC-39"),
    # Qi2.2
    "Q1": ("four sector coil coupon, 25 W, regulated Leaf pad", 6, ["T00"], "hw/energy", "ENR-24"),
    "Q2": ("Qi2.2 pre-test on the EVT body", 3, ["EVT", "Q1"], "hw/energy", "ENR-24"),
    "Q3": ("Qi2.2 25 W certification at a WPC test lab", 4, ["DVT", "Q2"], "program", "ENR-24"),
    # silicon U1 and U6
    "S1": ("U1 and U6 RTL to sign-off", 12, ["T00"], "rtl/u1, rtl/u6", "SW-21"),
    "S2": ("U1 and U6 tape-out and first silicon", 6, ["S1"], "rtl/u1, rtl/u6", "SW-21"),
    "S3": ("U1 and U6 bring-up on the bench", 4, ["S2"], "rtl/u1, rtl/u6", "SW-21"),
    # 5G modem
    "M1": ("modem vendor selection, hostless SA modem, Rel-17 or later", 4, ["T00"], "program", "RF-17"),
    "M2": ("10.0 x 8.0 x 0.80 mm modem and RF front-end SiP design", 10, ["M1"], "hw/rf", "RF-17"),
    "M3": ("SiP samples, RF-17, desense in the ring", 6, ["M2"], "hw/rf", "RF-17"),
    "M4": ("GCF, PTCRB and operator certification", 6, ["DVT", "M3"], "program", "DST-11"),
    # B module
    "B1": ("LCP-GF40 moulds, LDS antennas, soft-edge radii", 8, ["T00"], "hw/rf", "MON-23"),
    "B2": ("50 MP column, sapphire L1, 3.90 mm", 12, ["T00"], "hw/camera", "CAM-21"),
    "B3": ("B module rev A with ring PCBA", 4, ["B1", "B2", "S3", "M3"], "hw/electronics", "MON-21"),
    # validator RG-18
    "V1": ("RG-18 alpha: fixed-point render, frame hash chain", 9, ["T00"], "validator/leaf-duty", "RG-18"),
    "V2": ("RG-18 beta: re-execution, hot shadow, receipts, slashing", 9, ["V1"], "validator/leaf-duty", "RG-18"),
    "V3": ("testnet with cell-site validators and one operator", 9, ["V2"], "net/discovery", "DST-11"),
    "V4": ("mainnet activation of the Leaf duty", 3, ["V3", "DVT"], "validator/leaf-duty", "RG-18"),
    # integration builds
    "EVT": ("EVT build, 200 units, gates on a working Leaf", 4, ["D4", "C4", "H2", "B3"], "program", "MEC-39"),
    "DVT": ("DVT build, 500 units, full gate list", 6, ["EVT", "D5", "C5"], "program", "all"),
    "PVT": ("PVT build, 2 000 units at line rate, pilot in Turkey", 4, ["DVT", "D6", "Q3", "M4", "V4"], "program", "all"),
    "MP": ("mass production start (SOP)", 0, ["PVT"], "program", "PRG"),
}


def solve(tasks):
    order, seen = [], set()

    def visit(t):
        if t in seen:
            return
        for p in tasks[t][2]:
            visit(p)
        seen.add(t)
        order.append(t)

    for t in tasks:
        visit(t)
    es, ef = {}, {}
    for t in order:
        es[t] = max((ef[p] for p in tasks[t][2]), default=0)
        ef[t] = es[t] + tasks[t][1]
    end = max(ef.values())
    succ = {t: [] for t in tasks}
    for t, v in tasks.items():
        for p in v[2]:
            succ[p].append(t)
    ls, lf = {}, {}
    for t in reversed(order):
        lf[t] = min((ls[s] for s in succ[t]), default=end)
        ls[t] = lf[t] - tasks[t][1]
    return order, es, ef, ls, lf, end


def month_to_date(m):
    y = START.year + (START.month - 1 + m) // 12
    mo = (START.month - 1 + m) % 12 + 1
    return date(y, mo, 1).isoformat()[:7]


def main():
    order, es, ef, ls, lf, end = solve(TASKS)
    crit = [t for t in order if ls[t] - es[t] == 0]
    rows = []
    print(f"{'id':5s} {'start':8s} {'end':8s} {'float':>5s}  name")
    for t in order:
        fl = ls[t] - es[t]
        rows.append(dict(id=t, name=TASKS[t][0], months=TASKS[t][1], owner=TASKS[t][3],
                         gate=TASKS[t][4], start=month_to_date(es[t]), end=month_to_date(ef[t]),
                         es=es[t], ef=ef[t], float=fl, critical=fl == 0))
        print(f"{t:5s} {month_to_date(es[t]):8s} {month_to_date(ef[t]):8s} {fl:5d}  {'*' if fl == 0 else ' '} {TASKS[t][0]}")
    print(f"\nthe program length: {end} months, SOP {month_to_date(end)}")
    print("the critical path: " + " -> ".join(crit))
    out = dict(start=START.isoformat(), months=end, sop=month_to_date(end), critical=crit, tasks=rows)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
