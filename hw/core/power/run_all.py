#!/usr/bin/env python3
"""run_all.py - runs the scripts of the POWER seat of hw/core in order. About 40 s.

Run:  python3 hw/core/power/run_all.py
numpy, scipy and matplotlib must be importable.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
for name in ("skin_tree.py", "link_power.py", "core_energy.py", "mass.py", "distance.py", "damage.py"):
    print("=== %s" % name)
    r = subprocess.run([sys.executable, os.path.join(HERE, name)], cwd=HERE, env=env, stdout=subprocess.DEVNULL)
    if r.returncode:
        sys.exit("%s failed" % name)
print("done: see out/")
