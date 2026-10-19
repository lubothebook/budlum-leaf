#!/usr/bin/env python3
"""common.py - shared inputs of the POWER-PATH team, hw/hostpower/powerpath/.

Reads (read only) hw/energy/out/cell_spec.json and hw/energy/out/budget.json.
Every other script of this directory imports this file.

Tags: D = [DECISION], H = [HYPOTHESIS], P = [PUBLICATION], G = [GENERAL], T = [TREE].
Run the scripts with numpy, scipy and matplotlib on the path.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return json.load(f)


CELLSPEC = load("hw/energy/out/cell_spec.json")      # T
BUDGET = load("hw/energy/out/budget.json")           # T

# ------------------------------------------------------------------ the loads, W at the cells (T)
# Names of hw/energy/04 Section 3. The 8.7 W peak is the BRIEF Section 5 worst case [D].
def _case(prefix):
    for c in BUDGET["cases"]:
        if c["name"].startswith(prefix):
            return c["battery_W"]
    raise KeyError(prefix)


LOADS = {
    "standby": _case("wallet standby"),          # 0.061
    "safe screen": _case("safe screen"),         # 0.219
    "delta session": _case("delta session, 250"),  # 2.242
    "video": _case("video session"),             # 3.646
    "outdoor": _case("video outdoors"),          # 7.482
    "peak": 8.7,                                 # BRIEF s5 [D]
}
GAPS = [("0.1 s", 0.1), ("1 s", 1.0), ("3 s", 3.0), ("30 s", 30.0),
        ("5 min", 300.0), ("30 min", 1800.0)]

# ------------------------------------------------------------------ the micro cell (T, read from cell_spec.json)
N_TILES = 128
TILE_MM = 10.0
BODY_AREA_MM2 = 80.0 * 160.0
CELL_VOL_MM3 = CELLSPEC["geometry"]["cell_volume_mm3"]       # 76.88
STACK = {  # thickness of the 2.00 mm tile stack, FINAL/21 21.2.7, mm
    "cap": 0.25, "adhesive": 0.05, "glass_led": 0.25, "oca": 0.03, "coil": 0.20,
    "cell": 0.90, "skin": 0.08, "routing_margin": 0.24,
}
CELLS = {}
for _v in ("G", "S"):
    _s = CELLSPEC["variants"][_v]
    CELLS[_v] = dict(
        E_target_Wh=CELL_VOL_MM3 * 1e-6 * _s["target_whl"],   # 600 and 750 Wh/L
        E_model_Wh=_s["energy_Wh"],
        dcir=_s["dcir_ohm"], mass_g=_s["mass_g"], vmax=_s["v_max"], vmin=_s["v_min"],
        vnom=_s["v_nom"], q_model_mAh=_s["capacity_mAh"])

# B cell and island numbers (T, hw/energy/04 and 05)
B_CELL_WH = BUDGET["b_cell_Wh"] if "b_cell_Wh" in BUDGET else 20.0 * 8.0 * 1.5 * 1e-6 * 600.0
USABLE_B = 0.96 * 0.95            # usable fraction through U4, runtime.py
P_ISLAND = 0.025                  # W: U7 secure element 0.020 + U4 housekeeping 0.005 [H]
P_RING_CAP = 0.40                 # W: U4 cap on the islanded ring, hw/energy/03 s1.2 [D]

# ------------------------------------------------------------------ open-circuit voltage of the cell
# LiCoO2 / graphite at 4.45 V. A generic curve [H]. The energy is scaled to the cell energy.
_SOC = np.array([0, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0])
_OCV = np.array([3.20, 3.50, 3.62, 3.70, 3.75, 3.80, 3.86, 3.93, 4.02, 4.12, 4.26, 4.45])


def ocv(soc):
    return np.interp(soc, _SOC, _OCV)


_grid = np.linspace(0, 1, 2001)
_E_INT = np.trapezoid(ocv(_grid), _grid)      # V (mean voltage over the SOC range)


def e_frac(a, b):
    """Fraction of the full (0..100 %) cell energy between SOC a and SOC b (a < b)."""
    g = np.linspace(a, b, 400)
    return float(np.trapezoid(ocv(g), g) / _E_INT)


def r_factor(soc):
    """DCIR against SOC: 1.0 above 40 %, rising to 2.0 at 10 % and below [H]."""
    return float(np.interp(soc, [0.0, 0.1, 0.4, 1.0], [2.0, 2.0, 1.0, 1.0]))


def cell_q_Ah(E_Wh):
    return E_Wh / _E_INT


# ------------------------------------------------------------------ plotting style (colour-blind safe, thin marks)
PAL = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#6b6b6b"]


def style(ax, xlabel="", ylabel="", title=""):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    ax.grid(True, color="#dddddd", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def dump(name, obj, text_lines):
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)
    with open(os.path.join(OUT, name + ".txt"), "w") as f:
        f.write("\n".join(text_lines) + "\n")
