#!/usr/bin/env python3
"""yield_repair.py - the defect, repair and known-good-tile math of the face.

Budlum Leaf L.6.0, Display team, hw/display/.
Gate DSP-19, second half: under 5 dead pixels per device.

Flow
  1. transfer the blue (or RGB) chips and the uICs onto the carrier glass
  2. inspect: photoluminescence of every chip, then electroluminescence of
     the tile through its own hub
  3. repair pass 1 and pass 2: laser lift-off of the bad chip, re-place a
     good chip in the same site, re-inspect
  4. in the QD option, pattern the quantum dots only after the blue array
     is clean, so one chip type is repaired
  5. bin each tile by its residual dead pixels: known-good tiles only
  6. assemble 32 tiles per quadrant, test again (assembly damage)

Run:  python3 yield_repair.py
"""
import numpy as np
from scipy.stats import poisson

TILES = 128
PX = 200 * 200
CHIPS_PX = 4                 # R, G, B and the red twin (S site)
UIC_T = 100 * 100
TGV_T = 288
REP_S = 2.0                  # s per repair, laser lift-off + place + re-check [HYPOTHESIS]
F_SHORT = 0.10               # share of chip faults that are shorts or stuck-on  [HYPOTHESIS]
ESC = 0.002                 # share of faults the inspection misses             [HYPOTHESIS]
P_ASM = 0.2                  # expected dead pixels per device from assembly   [HYPOTHESIS]

print(f"chips per device {TILES*PX*CHIPS_PX/1e6:.2f} M, uICs {TILES*UIC_T/1e6:.2f} M, TGVs {TILES*TGV_T}")
print()
hdr = (f"{'p_chip':>8} {'p_uIC':>7} {'r':>6} | {'chip faults':>11} {'uIC faults':>10} {'repairs':>8} "
       f"{'repair min':>10} | {'resid/tile':>10} {'P(<5) no sort':>13} {'KGT yield':>9} {'P(<5) KGT':>9}")
print(hdr)
print("-" * len(hdr))
rows = []
for p_chip in (1e-4, 1e-5, 1e-6):
    for p_uic in (1e-4, 1e-5):
        for r in (0.95, 0.99):
            chips_t = PX * CHIPS_PX
            # a red fault with a live twin is not a dead pixel unless it shorts:
            # 1/4 of chips are red, 1/4 are the twin -> half the chip faults are red-side
            red_side = 0.5 * chips_t * p_chip
            red_need = red_side * F_SHORT            # shorts must be cut and replaced
            red_twin_ok = red_side * (1 - F_SHORT)   # carried by the twin, calibrated
            gb_need = 0.5 * chips_t * p_chip         # G and B faults: all repaired
            uic_need = UIC_T * p_uic
            need_t = red_need + gb_need + uic_need
            resid_t = need_t * ((1 - r) ** 2 + ESC)  # two repair passes + inspection escapes
            resid_t_dev = resid_t * TILES
            p_no_sort = poisson.cdf(4, resid_t_dev + P_ASM)
            kgt = np.exp(-resid_t)                   # tile with zero residual dead pixels
            p_kgt = poisson.cdf(4, P_ASM)
            rep_min = (red_need + gb_need + uic_need) * TILES * REP_S / 60 * (1 + (1 - r))
            rows.append((p_chip, p_uic, r, resid_t, kgt))
            print(f"{p_chip:8.0e} {p_uic:7.0e} {r:6.3f} | {TILES*(red_side*2):11.0f} {TILES*uic_need:10.1f} "
                  f"{TILES*need_t:8.0f} {rep_min:10.1f} | {resid_t:10.2e} {p_no_sort:13.4f} {kgt:9.4f} {p_kgt:9.4f}")
print()
print("reading the table")
print(" - 'chip faults' counts every bad chip; the red twin absorbs 90 % of the red ones.")
print(" - 'repairs' are the laser re-place events per device; 'repair min' is the line time.")
print(" - 'KGT yield' is the share of tiles that leave repair with zero dead pixels.")
print(" - with known-good tiles the device count is set by assembly damage only.")
print()
# the mass-transfer target that keeps repair time under 10 min per device and KGT yield > 99 %
for p_chip in np.logspace(-6, -4, 9):
    need_dev = TILES * (PX * CHIPS_PX * p_chip * (0.5 * F_SHORT + 0.5) + UIC_T * 1e-5)
    minutes = need_dev * REP_S / 60
    print(f"  p_chip {p_chip:7.1e}: repairs/device {need_dev:7.0f}, {minutes:6.1f} min")
print()
# TGV loss: data vias are doubled, so a row bus fails only if both fail
for p_v in (1e-5, 1e-4):
    dev_rows = TILES * 100 * p_v ** 2
    print(f"  TGV p {p_v:.0e}: expected dead uIC rows per device {dev_rows:.1e} (doubled data vias)")
# the seam rule: no dead pixel within 2 px of a cut, so the seam never shows a gap
print()
print("seam rule: the edge band (2 px each side of a cut) has 1 596 px per tile edge pair;")
print("a dead pixel there doubles the local gap to 100 um, so the KGT bin rejects any edge-band dead pixel.")
