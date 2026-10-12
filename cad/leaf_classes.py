#!/usr/bin/env python3
# BUDLUM LEAF · cad/leaf_classes.py · revision L.4.1 · 2026-10-07
#
# Builds the three family classes (Leaf 80, Leaf 160, Leaf 480) under the single
# 12-edge softened rectangular prism form law defined in cad/leaf_geom.py:
#   - Plan is an upright rectangle W x H
#   - 4 vertical corner edges rounded at small corner radius R = 3.20 * (short / 80)^0.25 mm
#   - 8 horizontal face-to-wall edges filleted at r = 0.80 mm (0.70 mm on Leaf 80)

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from leaf_geom import main as build_all

if __name__ == "__main__":
    build_all()
