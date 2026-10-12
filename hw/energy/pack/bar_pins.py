#!/usr/bin/env python3
"""bar_pins.py - the 12 gold leaves of the seat field: map, current per pin,
mirror symmetry and the dead-pad leakage. Energy and BMS team.

Gates MON-16, MON-21, MON-23, ENR-19 (dead pad), SW-20.

Run:  python3 hw/energy/pack/bar_pins.py
Out:  hw/energy/out/bar_pins.json, hw/energy/out/bar_pins.txt
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)

R_LEAF = 0.018        # ohm per leaf  [DECISION] HARDWARE/08
I_RATED = 1.5         # A per leaf, continuous  [HYPOTHESIS], gate MON-16
PITCH = 0.80          # mm: 12 leaves in the 9.6 mm field  [DECISION] FINAL/21 21.3.2

PINS = {
    1: ("GND", "ground, long leaf, mates first and breaks last"),
    2: ("VBUS", "body bus 3.40-4.48 V, B supply"),
    3: ("L0+", "high-speed lane 0, positive"),
    4: ("L0-", "high-speed lane 0, negative"),
    5: ("VHV", "charge rail 5-20 V from a port part or the dock"),
    6: ("SBA", "sideband A: dead-pad handshake, identity, cell telemetry"),
    7: ("SBB", "sideband B: tile control, hinge angles, Qi status"),
    8: ("VHV", "charge rail 5-20 V"),
    9: ("L1-", "high-speed lane 1, negative"),
    10: ("L1+", "high-speed lane 1, positive"),
    11: ("VBUS", "body bus 3.40-4.48 V"),
    12: ("GND", "ground, long leaf"),
}


def mirror_ok():
    """the bar seats on the front or the back face: pin k lands on 13-k."""
    same = {"GND", "VBUS", "VHV"}
    swap = {("L0+", "L1+"), ("L0-", "L1-"), ("SBA", "SBB")}
    bad = []
    for k in range(1, 7):
        a, b = PINS[k][0], PINS[13 - k][0]
        if a == b and a in same:
            continue
        if (a, b) in swap or (b, a) in swap:
            continue
        bad.append((k, a, b))
    return bad


def per_pin(name, net_currents):
    rows = []
    for k, (net, _) in PINS.items():
        n_same = sum(1 for v in PINS.values() if v[0] == net)
        i = net_currents.get(net, 0.0) / n_same
        rows.append((k, net, i, i * i * R_LEAF))
    return rows


def main():
    L = []
    p = L.append
    res = {"pins": PINS, "mirror_faults": mirror_ok(), "cases": {}}
    p("seat field: 12 leaves at %.2f mm pitch = %.1f mm" % (PITCH, 12 * PITCH))
    p("mirror check (front/back seat): %s" % ("pass" if not res["mirror_faults"] else res["mirror_faults"]))
    # cases: the net currents in A, worst case
    v_min = 3.40
    cases = {
        "B module, video 1.92 W": {"VBUS": 1.92 / 0.90 / 3.78, "GND": 1.92 / 0.90 / 3.78},
        "B module, peak 4.50 W at 3.40 V": {"VBUS": 4.50 / 0.90 / v_min, "GND": 4.50 / 0.90 / v_min},
        "B module, B cell charge 1C plus video": {"VBUS": (1.92 / 0.90 + 0.037 * 4.4) / 3.78,
                                                   "GND": (1.92 / 0.90 + 0.037 * 4.4) / 3.78},
        "port part, 27 W at 9 V (PD fixed)": {"VHV": 27 / 9.0, "GND": 27 / 9.0},
        "port part, 27 W at 15 V": {"VHV": 27 / 15.0, "GND": 27 / 15.0},
        "dock pads, 25 W at 12 V": {"VHV": 25 / 12.0, "GND": 25 / 12.0},
    }
    for name, nets in cases.items():
        rows = per_pin(name, nets)
        worst = max(r[2] for r in rows)
        loss = sum(r[3] for r in rows)
        res["cases"][name] = dict(rows=rows, worst_A=worst, loss_mW=1e3 * loss,
                                  ok=worst <= I_RATED)
        p("%-40s worst leaf %.2f A (%s), leaf loss %.1f mW, %s"
          % (name, worst, ", ".join("%d:%s %.2f" % (k, n, i) for k, n, i, _ in rows if i > 0),
             1e3 * loss, "PASS" if worst <= I_RATED else "OVER %.1f A" % I_RATED))
    # dead-pad probe leakage in salt water
    v_probe, r_probe, t_on, period = 1.8, 1.0e6, 200e-6, 0.250
    i_avg = v_probe / r_probe * t_on / period
    res["dead_pad_probe_avg_uA"] = i_avg * 1e6
    p("dead-pad probe on SBA/SBB: %.1f V through %.1f MOhm, %.0f us every %.0f ms: average %.4f uA (MON-16 limit 1 uA)"
      % (v_probe, r_probe / 1e6, t_on * 1e6, period * 1e3, i_avg * 1e6))
    p("power leaves at rest: 0 V, 1 MOhm to GND, so no DC across wet pads")
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(OUT, "bar_pins.json"), "w") as f:
        json.dump(res, f, indent=1)
    with open(os.path.join(OUT, "bar_pins.txt"), "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
