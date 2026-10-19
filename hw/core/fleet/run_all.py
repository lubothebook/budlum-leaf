#!/usr/bin/env python3
"""run_all.py - runs the five scripts of seat FLEET in order. About 3 minutes. Writes only to out/."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for name in ("fleet.py", "twohosts.py", "econ.py", "roam.py"):
    print("=== %s" % name, flush=True)
    r = subprocess.run([sys.executable, "-B", os.path.join(HERE, name)], cwd=HERE, stdout=subprocess.DEVNULL)
    if r.returncode:
        sys.exit("%s failed" % name)
print("done: see out/")
