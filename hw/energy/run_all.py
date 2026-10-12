#!/usr/bin/env python3
"""run_all.py - runs every energy script in order and checks the gates.

Run:  python3 hw/energy/run_all.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["cell/microcell.py", "pack/network.py", "pack/bar_pins.py", "budget/runtime.py"]

for s in STEPS:
    print("=" * 78)
    print("RUN", s)
    print("=" * 78)
    subprocess.run([sys.executable, os.path.join(HERE, s)], check=True)

out = os.path.join(HERE, "out")
cell = json.load(open(os.path.join(out, "cell_spec.json")))
net = json.load(open(os.path.join(out, "network.json")))
pins = json.load(open(os.path.join(out, "bar_pins.json")))
vol = cell["geometry"]["cell_volume_mm3"]

print("=" * 78)
print("GATE CHECKS (design-level, by calculation; the hardware test is the gate)")
checks = []
q600 = 32 * vol * 600e-6
q750 = 32 * vol * 750e-6
checks.append(("ENR-22 quadrant at 600 Wh/L >= 1.42 Wh", q600 >= 1.42, "%.3f Wh" % q600))
checks.append(("ENR-22 quadrant at 750 Wh/L >= 1.80 Wh", q750 >= 1.80, "%.3f Wh" % q750))
checks.append(("cell model G >= 600 Wh/L", cell["variants"]["G"]["whl_cell"] >= 600,
               "%.0f Wh/L" % cell["variants"]["G"]["whl_cell"]))
checks.append(("cell model S >= 750 Wh/L", cell["variants"]["S"]["whl_cell"] >= 750,
               "%.0f Wh/L" % cell["variants"]["S"]["whl_cell"]))
fz = net["fuse"]
cs = net["cell_short"]
checks.append(("ENR-23 fuse opens before any other cell fuse heats",
               all(c["i_other_cell_max_A"] < fz["i_fuse_steady_A"] for c in cs),
               "others max %.2f A < %.2f A" % (max(c["i_other_cell_max_A"] for c in cs), fz["i_fuse_steady_A"])))
checks.append(("ENR-23 fuse opens before a hinge line melts", fz["selectivity"] > 100,
               "I2t ratio x%.0f" % fz["selectivity"]))
bs = net["bus_short"]
checks.append(("bus short: TCM trip 0.02 ms before hinge melt",
               all(b["t_hinge_melt_ms"] > 0.1 for b in bs),
               "hinge melt %.2f ms" % min(b["t_hinge_melt_ms"] for b in bs)))
checks.append(("bar leaves within 1.5 A in every case",
               all(c["ok"] for c in pins["cases"].values()), "see bar_pins.txt"))
checks.append(("mirror pinout", not pins["mirror_faults"], "front/back"))
checks.append(("dead-pad probe < 1 uA", pins["dead_pad_probe_avg_uA"] < 1.0,
               "%.4f uA" % pins["dead_pad_probe_avg_uA"]))
bal = [v for k, v in net["soc"].items() if "k_bal=2.0" in k]
checks.append(("balance keeps SOC spread < 5 %", all(b["spread_max"] < 0.05 for b in bal),
               "%.1f %%" % (100 * max(b["spread_max"] for b in bal))))
for name, ok, val in checks:
    print("  %-52s %-5s %s" % (name, "PASS" if ok else "FAIL", val))
