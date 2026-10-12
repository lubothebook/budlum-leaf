#!/usr/bin/env python3
"""budget.py - the NRE and unit cost estimate of the Budlum Leaf L.6.0 build.

The Program Office. Every input is a [HYPOTHESIS] of the Program Office
unless its comment names a source. Each line carries a low, a base and a
high value. The script sums the non-recurring engineering (NRE), adds the
contingency, models the unit cost at three volumes, and writes budget.json.

The unit cost model is parametric for the display and the cells, because
those two dominate. The other parts are quoted per unit at each volume.

Run: python3 budget.py
"""
import json
import os

LMH = ("low", "base", "high")

# ----------------------------------------------------------------- NRE (M USD)
NRE = [
    # (work package, owner, low, base, high, the basis)
    ("508 ppi micro-LED tile: partner NRE, masks, transfer and repair tooling",
     "hw/display", 25.0, 38.0, 60.0, "two partner programmes in parallel, 3 tile spins"),
    ("pixel uIC, 28 nm: design, IP, 2 mask sets",
     "hw/display", 8.0, 12.0, 18.0, "28 nm mask set about 1.5-3 M USD each"),
    ("TGV glass carrier and black cut process",
     "hw/display", 3.0, 5.0, 8.0, "glass partner development and laser cells"),
    ("hermetic micro cell: can, feedthrough, Si-C, formation line pilot",
     "hw/energy", 12.0, 18.0, 30.0, "custom can line and 3 sample generations"),
    ("TCM protection IC per tile, custom",
     "hw/energy", 4.0, 6.0, 9.0, "mixed-signal derivative of a shipping protection IC"),
    ("U1 TCON and compositor ASIC",
     "rtl/u1", 18.0, 28.0, 40.0, "one spin plus a metal fix, 12 nm class"),
    ("U6 slice decoder and frame store ASIC, AV1 and HEVC IP",
     "rtl/u6", 14.0, 22.0, 32.0, "decoder IP licence plus one spin"),
    ("5G modem SiP, 10.0 x 8.0 x 0.80 mm, RF front end",
     "hw/rf", 6.0, 9.0, 15.0, "OSAT SiP NRE and modem vendor engineering"),
    ("body mechanics: hinge, skin, caps, kinematic seats, rigs",
     "sim/mechanics", 4.0, 6.0, 10.0, "coupons, cycle rigs, 3 body iterations"),
    ("B module: LCP-GF40 moulds, LDS, gaskets, jack",
     "hw/rf", 3.0, 4.5, 7.0, "4 mould tools x 2 iterations"),
    ("50 MP camera column with sapphire L1",
     "hw/camera", 4.0, 6.0, 10.0, "custom 5-element lens and module line set-up"),
    ("Leaf Dock and Leaf pad, regulated 22 C",
     "hw/dock", 1.5, 2.5, 4.0, "the pad holds the 25 W sustained case"),
    ("firmware integrity, U7 applet, boot chain",
     "fw/boot, fw/u7", 3.0, 5.0, 8.0, "secure element applet and evaluation"),
    ("validator Leaf duty RG-18, protocol, discovery",
     "validator/leaf-duty", 15.0, 24.0, 35.0, "40 engineers over 3 years"),
    ("hardware, system and program staff",
     "program", 55.0, 75.0, 100.0, "120 engineers over 4.5 years at 140 k USD loaded"),
    ("prototype builds: EVT 200, DVT 500, PVT 2 000",
     "program", 6.0, 9.5, 16.0, "see BUILDS below"),
    ("certification: Qi2.2, GCF, PTCRB, radio, safety, battery, SAR",
     "program", 2.5, 4.0, 6.0, "laboratory quotes of the class"),
    ("factory: test line, fixtures, calibration stations",
     "program", 15.0, 25.0, 40.0, "one line in Turkey, one in Asia"),
]
CONTINGENCY = {"low": 0.15, "base": 0.25, "high": 0.35}

BUILDS = {  # units, unit cost low/base/high in USD
    "EVT": (200, 9000, 15000, 25000),
    "DVT": (500, 4000, 6000, 10000),
    "PVT": (2000, 900, 1400, 2200),
}

# ------------------------------------------------------- unit cost (USD/unit)
VOLUMES = (100_000, 1_000_000, 5_000_000)  # units per year

# display: parametric
PIX_PER_TILE = 200 * 200
SUBPIX = 4            # RGBS quad, hw/display/README.md
TILES = 128
UIC_PER_TILE = PIX_PER_TILE // 4   # one uIC per 2 x 2 pixels, hw/display
# cost per million emitters: epitaxy, chip, mass transfer, inspection, laser repair
CHIP_USD_PER_M = {100_000: (60.0, 100.0, 160.0), 1_000_000: (25.0, 45.0, 75.0), 5_000_000: (12.0, 22.0, 38.0)}
# one uIC: a 28 nm die of about 30 x 30 um plus its own transfer and test, per million
UIC_USD_PER_M = {100_000: (40.0, 70.0, 120.0), 1_000_000: (20.0, 35.0, 60.0), 5_000_000: (10.0, 18.0, 30.0)}
GLASS_TGV_PER_TILE = {100_000: (0.60, 0.90, 1.40), 1_000_000: (0.30, 0.45, 0.70), 5_000_000: (0.18, 0.28, 0.45)}
TILE_YIELD = {100_000: (0.80, 0.70, 0.55), 1_000_000: (0.90, 0.85, 0.75), 5_000_000: (0.95, 0.92, 0.85)}

# cells: parametric, cost per Wh of a hermetic micro cell
CELL_WH = 7.2 / 128    # the 750 Wh/L target, FINAL/21
CELL_USD_PER_WH = {100_000: (9.0, 14.0, 22.0), 1_000_000: (4.0, 6.5, 10.0), 5_000_000: (2.5, 4.0, 6.5)}
CELL_FIXED = {100_000: (0.20, 0.30, 0.45), 1_000_000: (0.10, 0.15, 0.25), 5_000_000: (0.07, 0.10, 0.16)}  # can, feedthrough, fuse

# other blocks: (low, base, high) at each volume
OTHER = {
    "tile mechanics: PC caps, hinges, skin, seats, magnets, 128 tiles": {100_000: (40, 60, 90), 1_000_000: (22, 32, 48), 5_000_000: (15, 22, 34)},
    "TCM protection IC x 128": {100_000: (13, 19, 26), 1_000_000: (6.4, 9.6, 14), 5_000_000: (4.5, 6.4, 9.6)},
    "Qi2.2 sector coils, shield, rectifier": {100_000: (6, 9, 13), 1_000_000: (3.5, 5, 7.5), 5_000_000: (2.5, 3.5, 5)},
    "touch grid, AgNW, on the caps": {100_000: (8, 12, 18), 1_000_000: (4, 6, 9), 5_000_000: (3, 4.5, 7)},
    "U1 and U6 ASICs with 16 MB store": {100_000: (30, 45, 65), 1_000_000: (14, 20, 30), 5_000_000: (9, 13, 20)},
    "U5 5G modem SiP with RF front end and eSIM": {100_000: (48, 60, 80), 1_000_000: (34, 42, 55), 5_000_000: (27, 34, 44)},
    "U2A Wi-Fi 7 and BT 6.0, U2B 60 GHz and UWB": {100_000: (14, 18, 24), 1_000_000: (9, 12, 16), 5_000_000: (7, 9.5, 13)},
    "U7 secure element, U8 IMU, U3 audio, U4 power, NOR": {100_000: (9, 12, 16), 1_000_000: (5.5, 7.5, 10), 5_000_000: (4.2, 5.8, 8)},
    "50 MP camera column with sapphire L1": {100_000: (22, 30, 42), 1_000_000: (13, 18, 25), 5_000_000: (10, 14, 19)},
    "B module mechanics: LCP shells, LDS, windows, jack, speaker, mics": {100_000: (22, 30, 42), 1_000_000: (12, 17, 24), 5_000_000: (9, 13, 18)},
    "rear round AMOLED": {100_000: (6, 8, 12), 1_000_000: (3.5, 5, 7), 5_000_000: (2.8, 4, 5.5)},
    "ring PCBA, 8-layer HDI, assembly": {100_000: (10, 14, 20), 1_000_000: (6, 8.5, 12), 5_000_000: (4.5, 6.5, 9)},
    "B cell 0.14 Wh": {100_000: (1.5, 2.2, 3), 1_000_000: (0.9, 1.3, 1.8), 5_000_000: (0.7, 1.0, 1.4)},
    "final assembly, calibration, test, provisioning": {100_000: (60, 85, 120), 1_000_000: (28, 40, 58), 5_000_000: (18, 26, 38)},
    "packaging, logistics, warranty reserve 3 %": {100_000: (25, 35, 50), 1_000_000: (14, 20, 28), 5_000_000: (10, 14, 20)},
}
ROYALTY_PCT = (0.030, 0.040, 0.050)   # cellular SEP royalties, share of unit cost


def nre():
    out = {}
    for k, key in enumerate(LMH):
        base = sum(row[2 + k] for row in NRE)
        out[key] = dict(lines=base, contingency=base * CONTINGENCY[key],
                        total=base * (1 + CONTINGENCY[key]))
    return out


def builds_check():
    return {k: sum(v[0] * v[1 + i] for v in BUILDS.values()) / 1e6 for i, k in enumerate(LMH)}


def display_cost(vol, i):
    emitters = PIX_PER_TILE * SUBPIX
    chips = emitters / 1e6 * CHIP_USD_PER_M[vol][i]
    uics = UIC_PER_TILE / 1e6 * UIC_USD_PER_M[vol][i]
    glass = GLASS_TGV_PER_TILE[vol][i]
    good_tile = (chips + uics + glass) / TILE_YIELD[vol][i]
    return dict(per_tile=good_tile, chips=chips, uics=uics, glass=glass, device=good_tile * TILES)


def cell_cost(vol, i):
    per_cell = CELL_WH * CELL_USD_PER_WH[vol][i] + CELL_FIXED[vol][i]
    return dict(per_cell=per_cell, device=per_cell * TILES)


def unit_cost():
    res = {}
    for vol in VOLUMES:
        res[vol] = {}
        for i, key in enumerate(LMH):
            d = display_cost(vol, i)
            c = cell_cost(vol, i)
            lines = {"micro-LED tiles x 128": d["device"], "micro cells x 128": c["device"]}
            for name, tbl in OTHER.items():
                lines[name] = tbl[vol][i]
            sub = sum(lines.values())
            lines["cellular SEP royalties"] = sub * ROYALTY_PCT[i]
            total = sum(lines.values())
            res[vol][key] = dict(lines=lines, total=total, display=d, cell=c)
    return res


def main():
    n = nre()
    b = builds_check()
    u = unit_cost()
    print("== NRE, M USD")
    print(f"{'':60s} {'low':>7s} {'base':>7s} {'high':>7s}")
    for row in NRE:
        print(f"{row[0][:60]:60s} {row[2]:7.1f} {row[3]:7.1f} {row[4]:7.1f}")
    for key in ("lines", "contingency", "total"):
        print(f"{key.upper():60s} " + " ".join(f"{n[k][key]:7.1f}" for k in LMH))
    print("prototype builds check, M USD: " + ", ".join(f"{k} {b[k]:.2f}" for k in LMH))
    print("\n== unit cost, USD per Leaf (body plus B module)")
    for vol in VOLUMES:
        t = u[vol]
        print(f"volume {vol:>9,d}/yr: low {t['low']['total']:7.0f}  base {t['base']['total']:7.0f}  high {t['high']['total']:7.0f}")
        bd = t["base"]
        print(f"   base display {bd['lines']['micro-LED tiles x 128']:.0f} "
              f"({bd['display']['per_tile']:.2f}/tile: chips {bd['display']['chips']:.2f}, "
              f"uIC {bd['display']['uics']:.2f}, glass {bd['display']['glass']:.2f}), "
              f"cells {bd['lines']['micro cells x 128']:.0f} ({bd['cell']['per_cell']:.3f}/cell), "
              f"display share {100 * bd['lines']['micro-LED tiles x 128'] / bd['total']:.0f} %")
    out = dict(nre=n, nre_lines=[dict(item=r[0], owner=r[1], low=r[2], base=r[3], high=r[4], basis=r[5]) for r in NRE],
               builds=b, unit={str(v): {k: dict(total=u[v][k]["total"], lines=u[v][k]["lines"]) for k in LMH} for v in VOLUMES})
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
