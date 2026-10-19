#!/usr/bin/env python3
"""explore.py - the search for a Leaf with an unlimited battery.

Block HP-4, the Program Lead's own lab notebook (no sub-agent). Ayaz, 2026-10-19:
the battery may sit in the Leaf, but it must be very small, and the whole event
lives in the hardware, so the energy is unlimited. The Lead tests every door that
physics offers, writes down the failures, and keeps the doors that stay open.

Every probe prints a row: the door, the energy that arrives (W), the need (W) and
the verdict. Tags: D = [DECISION], H = [HYPOTHESIS], P = [PUBLICATION] (source in
LAB-NOTEBOOK.md), G = [GENERAL], T = [TREE] (a number read from this repository).

Run:  python3 explore.py        (numpy only; it writes out/results.json and out/results.txt)
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- the Leaf, T
FACE_M2 = 0.080 * 0.160            # m2, the 80 x 160 mm face, T FINAL/21
FACE_CM2 = FACE_M2 * 1e4
LOADS = {                           # W at the battery or bus, T hw/energy/04, link seat
    "wallet standby today": 0.061,  # T hw/energy/04, wallet standby, battery draw
    "Skin delta": 0.95,             # T hw/core/link
    "Skin video": 1.57,             # T hw/core/link
    "Leaf delta": 2.24,             # T hw/energy/04
    "Leaf video": 3.65,             # T hw/energy/04
}
HEAT_LIMIT_STILL = 1.73             # W, sustained free air, 25 C, T hw/hostpower/thermal
HEAT_LIMIT_WIND = 2.37              # W, light wind, T hw/hostpower/thermal
HEAT_LIMIT_SKIN = 2.93              # W, Skin alone, sustained display and address, T hw/core/heat
B_CELL_WH = 0.144                   # Wh, T hw/energy
CELL_USABLE = 0.90                  # H usable fraction of the B cell
IDLE_TARGET_W = 50e-6               # W, the target of this study, D

rows = []


def row(door, arrives, need, verdict, note, tag="H"):
    rows.append(dict(door=door, arrives_W=arrives, need_W=need, verdict=verdict,
                     note=note, tag=tag))


def fmt_w(x):
    if x is None:
        return "n.a."
    a = abs(x)
    if a >= 1:
        return f"{x:.2f} W"
    if a >= 1e-3:
        return f"{x*1e3:.1f} mW"
    return f"{x*1e6:.1f} uW"


# ============================================================ door 1: RF beam
# Exposure caps the power density anywhere a person can stand: 10 W/m2 above
# 2 GHz (ICNIRP 2020 general public, FCC 1 mW/cm2). P] The Leaf is held by a person.
def rf_beam():
    out = {}
    for label, S in (("10 W/m2 (ICNIRP, FCC)", 10.0), ("40 W/m2 (FCC localised, >6 GHz, optimistic)", 40.0)):
        for eta in (0.2, 0.5):
            p = S * FACE_M2 * eta
            out[(label, eta)] = p
            row(f"RF beam at the exposure cap, {label}, rectenna {int(eta*100)} %",
                p, LOADS["Skin delta"],
                "FAIL" if p < LOADS["Skin delta"] else "PASS",
                "the whole face as an ideal rectenna; the cap is on the person, not on the room", "P")
    # the EIRP route: power density from a legal transmitter
    for eirp_w, name in ((0.1, "Wi-Fi 20 dBm EIRP"), (4.0, "Wi-Fi 36 dBm EIRP (FCC 2.4 GHz)"), (100.0, "licensed 50 dBm EIRP")):
        for d in (1.0, 3.0, 10.0):
            S = min(eirp_w / (4 * math.pi * d * d), 10.0)
            p = S * FACE_M2 * 0.3
            row(f"RF beam from {name} at {d:g} m, rectenna 30 %", p, LOADS["wallet standby today"],
                "FAIL" if p < 1e-3 else ("EDGE" if p < LOADS["wallet standby today"] else "PASS"),
                "free space, no wall, no hand; S capped at 10 W/m2", "G")
    return out


# ============================================================ door 2: IR beam
# Wi-Charge class: 3 W optical over 4.6 m, Class 1, line of sight (P, see notebook).
# Every optical watt absorbed in the Leaf ends as heat, so the heat limit caps the
# electrical power at eta * limit.
def ir_beam():
    for eta in (0.40, 0.55, 0.65, 0.689):
        for lim_name, lim in (("still", HEAT_LIMIT_STILL), ("light wind", HEAT_LIMIT_WIND),
                              ("Skin alone, still", HEAT_LIMIT_SKIN)):
            p_el = eta * lim
            row(f"IR beam into a back PV panel, receiver {eta*100:.0f} %, free air {lim_name}",
                p_el, LOADS["Skin delta"],
                "PASS" if p_el >= LOADS["Skin delta"] else "FAIL",
                f"optical input at the heat cap = {lim:.2f} W; electrical = eta x cap; Skin video needs {LOADS['Skin video']} W: "
                f"{'PASS' if p_el >= LOADS['Skin video'] else 'FAIL'}", "P")
    # what a 3 W beam gives at the receiver
    for eta in (0.40, 0.55, 0.689):
        row(f"IR beam 3 W optical, geometry 0.85, receiver {eta*100:.0f} %", 3.0 * 0.85 * eta,
            LOADS["Skin video"], "n.a.", "the beam power is not the limit; the heat is", "P")
    # receiver area at 100 mW/cm2 (about one sun) on the receiver
    row("IR receiver area for 2 W optical at 100 mW/cm2", 2.0 / 0.1, None, "INFO",
        "cm2; fits the 128 cm2 back, does not fit the 8 cm2 ring", "G")


# ============================================================ door 3: magnetic
def ellip_k_e(m):
    """complete elliptic integrals K(m), E(m) by the AGM (m = k^2)."""
    a, b = 1.0, math.sqrt(1.0 - m)
    c2 = m
    s = 0.5 * c2
    pw = 0.5
    while abs(a - b) > 1e-15:
        an = 0.5 * (a + b)
        bn = math.sqrt(a * b)
        pw *= 2
        c = 0.5 * (a - b)
        s += pw * 0.5 * c * c
        a, b = an, bn
    K = math.pi / (2 * a)
    E = K * (1 - s)
    return K, E


def mutual_loops(r1, r2, d):
    mu0 = 4e-7 * math.pi
    m = 4 * r1 * r2 / ((r1 + r2) ** 2 + d * d)
    K, E = ellip_k_e(m)
    k = math.sqrt(m)
    return mu0 * math.sqrt(r1 * r2) * ((2 / k - k) * K - (2 / k) * E)


def loop_self(r, a, n=1):
    mu0 = 4e-7 * math.pi
    return mu0 * n * n * r * (math.log(8 * r / a) - 2)


def magnetic():
    r_rx, n_rx, a_rx = 0.020, 12, 0.3e-3          # H the sector coil acting as a round coil
    q_rx, q_tx = 60.0, 200.0                       # H
    L_rx = loop_self(r_rx, a_rx, n_rx)
    out = {}
    for tx_name, r_tx, n_tx in (("pad 150 mm", 0.075, 8), ("desk mat 400 mm", 0.20, 5), ("ceiling loop 1 m", 0.50, 3)):
        L_tx = loop_self(r_tx, 1e-3, n_tx)
        for d in (0.01, 0.05, 0.10, 0.30, 0.50, 1.0, 2.0):
            M = n_tx * n_rx * mutual_loops(r_tx, r_rx, d)
            k = M / math.sqrt(L_tx * L_rx)
            x = k * k * q_tx * q_rx
            eta = x / (1 + math.sqrt(1 + x)) ** 2
            out[(tx_name, d)] = (k, eta)
            row(f"magnetic resonance, Tx {tx_name}, Rx coil 46 mm, coaxial, {d*100:.0f} cm",
                None, LOADS["Skin delta"], "EDGE" if eta >= 0.5 else ("WEAK" if eta >= 0.1 else "FAIL"),
                f"k = {k:.2e}, best link efficiency {eta*100:.2f} %", "G")
    return out


# ============================================================ door 4: the body
def body_coupled():
    for v, i, name in ((60.0, 0.5e-3, "SELV 60 V, 0.5 mA"), (60.0, 2e-3, "SELV 60 V, 2 mA (DC)")):
        p = v * i * 0.8
        row(f"galvanic path through the body, {name}", p, LOADS["Skin delta"], "FAIL",
            "touch-current limits recalled from IEC 60990; skin irritation; two contacts needed", "H")


# ============================================================ door 5: harvest
def harvest():
    # 1000 lux of LED light carries about 315 uW/cm2 (Nature Energy consensus), GaAs 29 % -> 92 uW/cm2 (P)
    for lux in (100, 300, 1000):
        inc = 315.5e-6 * lux / 1000.0                 # W/cm2 incident
        for part, area, eta, geom in (
            ("back PV, GaAs 25 %, back faces the light", FACE_CM2 * 0.8, 0.25, 1.0),
            ("back PV, the Leaf lies face up", FACE_CM2 * 0.8, 0.25, 0.0),
            ("face as photodiode, micro-LED 1 %", FACE_CM2 * 0.9, 0.01, 0.5),
        ):
            p = inc * area * eta * geom
            row(f"indoor light {lux} lux, {part}", p, IDLE_TARGET_W,
                "PASS" if p >= IDLE_TARGET_W else "FAIL", f"{inc*1e6:.0f} uW/cm2 incident", "P" if "back" in part else "H")
    # outdoors, one sun, 100 mW/cm2
    for part, area, eta, geom in (("back PV, GaAs 25 %, faces the sun", FACE_CM2 * 0.8, 0.25, 1.0),
                                  ("face as photodiode, micro-LED 1 %", FACE_CM2 * 0.9, 0.01, 0.5)):
        p = 0.1 * area * eta * geom
        row(f"outdoors, one sun, {part}", p, LOADS["Skin delta"],
            "PASS" if p >= LOADS["Skin delta"] else "FAIL", "the heat of the absorbed sun is not counted here", "H")
    # body heat: wearable TEG about 20 uW/cm2 at 5 K (recalled), half the area in contact
    p = 20e-6 * FACE_CM2 * 0.5
    row("pocket body heat, TEG 20 uW/cm2, half the face", p, IDLE_TARGET_W, "PASS" if p >= IDLE_TARGET_W else "FAIL",
        "the pocket is dark, so heat is the harvest there", "H")
    # kinetic: a handheld harvester, 10 to 100 uW (recalled)
    row("walking, kinetic harvester", 50e-6, IDLE_TARGET_W, "EDGE", "recalled range 10 to 100 uW; not sourced", "H")


# ============================================================ door 6: the stretch
def stretch():
    E_tpu, eps, t_skin = 20e6, 0.25, 80e-6         # Pa, strain, m, H
    vol = FACE_M2 * t_skin
    e_cycle = 0.5 * E_tpu * eps ** 2 * vol         # J stored per full stretch
    for eta in (0.05, 0.30):
        life = e_cycle * eta * 10_000 / 3600.0     # Wh over the MEC-39 cycle life
        row(f"stretch harvest, dielectric elastomer {int(eta*100)} %, 10 000 cycles", None, None,
            "FAIL", f"{life:.2f} Wh over the whole hinge life (one video hour is 3.65 Wh); one stretch stores {e_cycle:.2f} J", "H")


# ============================================================ door 7: NFC
def nfc():
    for p_mw, t_s in ((15, 1.0), (20, 2.0)):
        e = p_mw * 1e-3 * t_s
        row(f"NFC tap, {p_mw} mW for {t_s:g} s", e, None, "INFO",
            f"{e*1e3:.0f} mJ per tap; the trust seat puts one signature at 1 to 20 mJ; an e-paper update is 15 to 40 mJ", "P")


# ============================================================ door 8: one beam, power and pixels
# SLIPT demonstrations: 3.8 Gbit/s with a multi-segment GaAs converter at 39.7 %, and
# gigabit rates with multi-junction InGaAsP above 55 % at 1530 nm over 3 m (P, notebook).
def slipt():
    need_gbps = 13.1                                   # T hw/core/link, DSC 10 bpp, 240 Hz
    for name, got in (("GaAs multi-segment converter, 3.8 Gbit/s", 3.8), ("InGaAsP multi-junction, about 1 Gbit/s", 1.0)):
        row(f"one beam for power and pixels, {name}", None, None, "FAIL",
            f"carries {got} Gbit/s; the Skin pixel stream needs {need_gbps} Gbit/s ({need_gbps/got:.1f} times more)", "P")
    # a separate data photodiode at 5 to 10 pJ/bit, scaled from published receiver front ends (H)
    for pj in (5.0, 10.0):
        p_rx = need_gbps * 1e9 * pj * 1e-12
        load = LOADS["Skin delta"] + p_rx
        for lim_name, lim in (("L.6.0 body cap 1.73 W", HEAT_LIMIT_STILL), ("Skin alone cap 2.93 W", HEAT_LIMIT_SKIN)):
            eta_min = load / lim
            row(f"separate data diode {pj:g} pJ/bit, Skin delta + receiver {p_rx*1e3:.0f} mW, {lim_name}",
                None, load, "PASS" if eta_min <= 0.689 else "FAIL",
                f"the power converter must reach {eta_min*100:.0f} % (lab record 68.9 %)", "H")


# ============================================================ door 9: the Sheet, light from the hardware
def sheet():
    area = FACE_M2
    for L in (100.0, 250.0, 800.0):
        for G, name in ((1.0, "diffuse white, rho 0.8"), (10.0, "retroreflective, gain 10"), (50.0, "retroreflective, gain 50")):
            lm = math.pi * L * area / (0.8 * G)
            watt = lm / 20.0                              # H 20 lm/W wall plug of a pico projector
            row(f"Sheet at {L:g} nits, {name}: flux on the Leaf", watt, None, "INFO",
                f"{lm:.2f} lm at the screen, about {watt:.2f} W at the Core (20 lm/W)", "G")
    # ambient wash on a diffuse sheet versus the image
    for lux, place in ((500, "office"), (10_000, "shade"), (100_000, "direct sun")):
        wash = 0.8 * lux / math.pi                       # nits, diffuse white
        row(f"Sheet ambient wash on a diffuse white sheet, {place} {lux} lux", None, None,
            "FAIL" if wash > 250 else "PASS", f"{wash:,.0f} nits of ambient against a 250 nit image", "G")
    # angular size and the pixels needed at 60 ppd (the sharpness law)
    for dist in (0.4, 3.0):
        ang_w = 2 * math.degrees(math.atan(0.040 / dist))
        ang_h = 2 * math.degrees(math.atan(0.080 / dist))
        row(f"Sheet at {dist:g} m: pixels the viewer resolves at 60 ppd", None, None, "INFO",
            f"{ang_w*60:.0f} x {ang_h*60:.0f} px on the sheet ({ang_w:.1f} x {ang_h:.1f} deg)", "G")
    # laser scanning line rate for 60 ppd at 0.4 m
    for hz in (60, 120, 240):
        rate = 1356 * hz / 1e3
        row(f"Sheet, laser scanning, 1356 lines at {hz} Hz", None, None, "FAIL" if rate > 60 else "PASS",
            f"line rate {rate:.0f} kHz against about 60 kHz for a fast MEMS mirror (recalled)", "H")


# ============================================================ door 10: Paper, the bistable layer
# A bistable reflective layer holds an image at 0 W and costs energy only per update.
# Small panel: 27.6 x 27.6 mm (7.6 cm2) active area, 15 to 75 mJ per full refresh (H, from the
# NFC e-paper sources and recalled panel data). The cost scales with the area.
def paper():
    small_cm2 = 7.6
    scale = FACE_CM2 / small_cm2
    for e_small_mj in (15.0, 75.0):
        e_full = e_small_mj * 1e-3 * scale
        for frac, name in ((1.0, "full refresh"), (1/3, "partial refresh")):
            e = e_full * frac
            for src, p in (("RF at the 10 W/m2 cap, 25 mW", 25e-3), ("RF at the cap, 64 mW", 64e-3),
                           ("indoor light 1000 lux, back PV, 8 mW", 8e-3), ("pocket heat TEG, 1.3 mW", 1.3e-3)):
                row(f"Paper layer {name} ({e:.2f} J) fed by {src}", p, None, "INFO",
                    f"one update every {e/p:,.0f} s", "H")
    for tap_mj in (15.0, 40.0):
        row(f"Paper layer from one NFC tap, {tap_mj:g} mJ", None, None, "INFO",
            f"covers {tap_mj / (15.0 * scale) * 100:.1f} to {tap_mj / (75.0 * scale) * 100:.1f} % of a full face: a badge, not a page", "H")


# ============================================================ the day of a tiny-cell Leaf
# A day away from any host, with only the 0.144 Wh B cell. Hours of heartbeat, the Paper updates and
# a few minutes of active use. Every figure is H (see notebook); the floor and the update energies are ranges.
def day():
    usable_wh = B_CELL_WH * CELL_USABLE
    out = []
    for floor_name, floor_w in (("floor low 9.6 uW", 9.6e-6), ("floor high 42 uW", 42e-6)):
        for upd, e_upd in ((100, 0.08), (300, 0.42)):               # updates per day, J per partial update
            for act_min in (0, 5, 15):
                e_idle = floor_w * 24 * 3600
                e_paper = upd * e_upd
                e_act = LOADS["Skin delta"] * act_min * 60
                total_j = e_idle + e_paper + e_act
                days = usable_wh * 3600 / total_j
                out.append((floor_name, upd, e_upd, act_min, total_j / 3.6, days))
                row(f"day away from a host: {floor_name}, {upd} Paper updates of {e_upd} J, {act_min} min active",
                    None, None, "INFO", f"{total_j/3.6:.1f} mWh a day, the B cell lasts {days:.1f} days", "H")
    return out


# ============================================================ the idle floor
def idle_floor():
    parts = [  # name, low W, high W, tag
        ("secure element in deep sleep", 1e-6, 5e-6, "H"),
        ("wake-up receiver, sub-uW to 3 uW class", 0.3e-6, 3e-6, "P"),
        ("power chip quiescent current", 2e-6, 8e-6, "H"),
        ("real-time clock", 0.3e-6, 1e-6, "H"),
        ("touch or motion wake", 5e-6, 20e-6, "H"),
        ("near-field tag mode listen", 1e-6, 5e-6, "H"),
        ("bistable glance layer, holding", 0.0, 0.0, "G"),
    ]
    lo = sum(p[1] for p in parts)
    hi = sum(p[2] for p in parts)
    return parts, lo, hi


def autonomy(p_w):
    return B_CELL_WH * CELL_USABLE / p_w          # hours


def main():
    rf_beam()
    ir_beam()
    mag = magnetic()
    body_coupled()
    harvest()
    stretch()
    nfc()
    slipt()
    sheet()
    paper()
    day()
    parts, lo, hi = idle_floor()

    lines = []
    lines.append("THE SEARCH FOR AN UNLIMITED BATTERY - the probes")
    lines.append(f"face {FACE_CM2:.0f} cm2; Skin delta {LOADS['Skin delta']} W; heat cap still air {HEAT_LIMIT_STILL} W\n")
    for r in rows:
        lines.append(f"[{r['verdict']:<4}] {r['door'][:84]:<84} arrives {fmt_w(r['arrives_W']):>9} | need {fmt_w(r['need_W']):>9} | {r['note']}")
    lines.append("\nTHE IDLE FLOOR (the heartbeat)")
    for name, a, b, tag in parts:
        lines.append(f"  {name:<46} {a*1e6:5.1f} to {b*1e6:5.1f} uW  [{tag}]")
    lines.append(f"  {'sum':<46} {lo*1e6:5.1f} to {hi*1e6:5.1f} uW   (today: {LOADS['wallet standby today']*1e3:.0f} mW, {LOADS['wallet standby today']/hi:,.0f} to {LOADS['wallet standby today']/lo:,.0f} times more)")
    lines.append("\nAUTONOMY OF THE B CELL AT THE FLOOR")
    for label, p in (("today, 61 mW", LOADS["wallet standby today"]), ("floor high", hi), ("floor low", lo), ("target 50 uW", IDLE_TARGET_W)):
        h = autonomy(p)
        lines.append(f"  {label:<14} {h:12,.1f} h = {h/24:10,.1f} days")
    # wakes: one wake of 1 s at the Skin delta load
    wake_wh = LOADS["Skin delta"] * 1.0 / 3600.0
    lines.append(f"  one 1 s wake at the Skin delta load costs {wake_wh*1e3:.3f} mWh; the B cell holds {B_CELL_WH*CELL_USABLE/wake_wh:,.0f} wakes")
    # the cost of energy
    kwh = LOADS["Leaf video"] * 8 * 365 / 1000
    lines.append(f"\nENERGY COST: video 3.65 W for 8 h a day is {kwh:.1f} kWh a year, {kwh*0.2:.1f} EUR at 0.20 EUR/kWh")
    text = "\n".join(lines)
    open(os.path.join(OUT, "results.txt"), "w", encoding="utf-8").write(text + "\n")
    json.dump(dict(rows=rows, idle_floor_W=[lo, hi], autonomy_h=dict(today=autonomy(0.061), floor_high=autonomy(hi),
              floor_low=autonomy(lo), target=autonomy(IDLE_TARGET_W)), energy_cost_kwh_year=kwh),
              open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)
    print(text)


if __name__ == "__main__":
    main()
