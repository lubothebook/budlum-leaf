#!/usr/bin/env python3
"""run_all.py - runs the five scripts of the POWER-PATH team in order.

Run:  python3 hw/hostpower/powerpath/run_all.py
(numpy, scipy and matplotlib must be installed.)
Takes about one minute.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for name in ("tiers.py", "powerpath.py", "celllife.py", "hosts.py", "thesis_check.py"):
    print("=== %s" % name)
    r = subprocess.run([sys.executable, os.path.join(HERE, name)], cwd=HERE, stdout=subprocess.DEVNULL)
    if r.returncode:
        sys.exit("%s failed" % name)
print("done: see out/")
