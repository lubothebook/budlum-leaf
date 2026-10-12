"""Shared constants of the Budlum Leaf L.6.0 mechanics simulations.

Every geometric value comes from FINAL/21 (Section 21.2) unless tagged.
Every material value carries its tag in the comment.
SI units inside the code: metres, newtons, pascals, kilograms, seconds.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PLOTS = os.path.join(HERE, "plots")
RESULTS = os.path.join(HERE, "results")
os.makedirs(PLOTS, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

mm = 1e-3
um = 1e-6
DEG = np.pi / 180.0
G0 = 9.80665
MU0 = 4e-7 * np.pi

# ---------------------------------------------------------------- geometry [DECISION] FINAL/21
A_TILE = 10.0 * mm            # tile side
NX, NY = 8, 16                # tiles across x (80 mm) and y (160 mm)
T_BODY = 2.00 * mm
THETA_DEFAULT = 17.5 * DEG    # 25.4 % stretch
THETA_MAX = 45.0 * DEG        # 41.4 % stretch
N_HINGE = (NX - 1) * NY + NX * (NY - 1)   # 112 + 120 = 232 hinges

# hinge ribbon [DECISION] FINAL/21 21.2.2
T_PI = 12.5 * um
H_RIBBON = (1.2 * mm, 1.5 * mm)
L_RIBBON = 0.8 * mm
T_CU = 2.0 * um

# tile stack, top to bottom [DECISION] FINAL/21 21.2.7
STACK = [  # name, thickness m, density kg/m3 (density is [GENERAL])
    ("PC cap + AgNW", 0.25 * mm, 1200.0),
    ("OCA", 0.05 * mm, 1050.0),
    ("glass-LED-glass", 0.25 * mm, 2450.0),
    ("slip OCA", 0.03 * mm, 1050.0),
    ("Qi coil+shield / spreader", 0.20 * mm, 4000.0),
    ("micro cell (9.25 sq)", 0.90 * mm, 2600.0),
    ("back skin", 0.08 * mm, 1200.0),
    ("hinge routing + tolerance", 0.24 * mm, 0.0),
]
CELL_SIDE = 9.25 * mm

# ---------------------------------------------------------------- materials
E_PI = 2.5e9        # Kapton HN tensile modulus [PUBLICATION] DuPont Kapton HN datasheet
UTS_PI = 231e6      # [PUBLICATION] DuPont Kapton HN datasheet, 25 um film
YIELD_STRAIN_PI = 0.03   # [PUBLICATION] DuPont, 3 % yield point
E_CU = 117e9        # bulk Cu [GENERAL]; thin ED film 100-120 GPa
SU_CU = 300e6       # ED / sputtered Cu film tensile strength [GENERAL]
E_PC = 2.4e9        # polycarbonate [GENERAL]
NU_PC = 0.37
Y_PC = 62e6         # PC tensile yield [GENERAL]
E_GLASS = 70e9      # alkali-free display glass [GENERAL]
NU_GLASS = 0.22
E_STEEL = 200e9
NU_STEEL = 0.30

# design allowables for the glass layer [HYPOTHESIS]
SIG_GLASS_PLAIN = 100e6      # unstrengthened, laser-cut display glass, design tensile
SIG_GLASS_UTG = 400e6        # chemically strengthened ultra-thin glass, design tensile


def tile_mass():
    """Return (total kg, list of (layer, kg)) for one 10 mm tile."""
    out = []
    for name, t, rho in STACK:
        area = CELL_SIDE ** 2 if name.startswith("micro cell") else A_TILE ** 2
        out.append((name, area * t * rho))
    out.append(("hinge share (2 ribbons + Cu)", 2 * 1.35 * mm * 0.8 * mm * T_PI * 1420.0))
    return sum(m for _, m in out), out


def save(name, data):
    """Write a result dict to results/<name>.json."""
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (bool, np.bool_)):
            return bool(o)
        raise TypeError(type(o))
    with open(os.path.join(RESULTS, name + ".json"), "w") as f:
        json.dump(data, f, indent=2, default=conv)


def load(name):
    with open(os.path.join(RESULTS, name + ".json")) as f:
        return json.load(f)


def verdict(ok):
    return "PASS" if ok else "FAIL"
