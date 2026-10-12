#!/usr/bin/env python3
"""common.py - the shared decisions and the counted quantities of the mfg team.

Budlum Leaf L.6.0, Manufacturing and Test team, mfg/.
Every number here is tagged. The counts are computed, not typed.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PLOTS = os.path.join(HERE, "plots")
REPO = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)
os.makedirs(PLOTS, exist_ok=True)

# ------------------------------------------------------------ decisions, Part 21
NX, NY = 8, 16                 # tiles across and along          [DECISION] 21.2.1
TILE = 10.0                    # mm, tile pitch at rest           [DECISION] 21.2.1
QX, QY = 4, 8                  # tiles per quadrant, x and y      [DECISION] 32 per quadrant
PX_TILE = 200 * 200            # pixels per tile                  [DECISION] 21.2.3
EMIT_PX = 4                    # R, G, B and the red twin S       display team, tile_spec
UIC_TILE = 100 * 100           # uICs per tile                    display team, tile_spec
TGV_TILE = 288                 # through-glass vias per tile      display team, tile_spec
PITCH_UM = 50.0                # pixel pitch                      [DECISION] 21.2.3
KERF_MAX_UM = 10.0             # glass cut, upper limit           [DECISION] 21.2.4
KERF_NOM_UM = 6.0              # glass kerf nominal at rest       display team, seam_lattice
EDGE_MARGIN_RULE_UM = 16.0     # chip to cut                      [DECISION] 21.2.4
CHIPPING_MAX_UM = 10.0         # ultrafast-laser chipping limit   [DECISION] 21.2.4
CAP_KERF_HOT_UM = 10.0         # PC cap kerf at +50 C             [DECISION] 21.2.4
CAP_GROW_UM_40K = 27.0         # 10 mm cap growth over 40 K       [DECISION] 21.2.4
BAR_T, BAR_TOL = 1.00, 0.05    # mm                               [DECISION] MON-23
MOD_T, MOD_TOL = 4.00, 0.05    # mm                               [DECISION] MON-23
SEAT_REPEAT_UM = 1.0           # quadrant seat repeat             [DECISION] MEC-40
SWAPS = 10_000                 # swaps of MEC-40                  [DECISION]

# the soft edges of the team brief, section 4, Ayaz 2026-10-12      [DECISION]
SOFT_EDGES = [
    # name, nominal mm, where, how it is made
    ("body perimeter, front and back face edges", 0.65, "44 perimeter tiles", "moulded PC edge cap"),
    ("tile PC-cap top edges and chamfer corners", 0.03, "128 caps", "tilted-beam laser bevel"),
    ("B ring outer top and bottom edges", 0.40, "ring shell", "LCP mould, steel radius"),
    ("B ring inner bore edges", 0.25, "ring shell", "LCP mould, steel radius"),
    ("B bar long edges", 0.20, "bar skin shot", "LCP mould, steel radius"),
    ("B moulded 90 deg corner, outside edge", 0.30, "bar to ring corner", "LCP mould, steel radius"),
    ("jack mouth", 0.20, "ring rim", "LCP mould, core-pin radius"),
    ("windows", 0.10, "sapphire L1 and rear cover", "CNC edge grind and polish"),
]


def lattice_counts():
    """Count the hinges of the rotating-square lattice from the grid.

    Each tile joins each edge neighbour through one corner hinge.
    A hinge whose two tiles lie in different quadrants is a split coupler.
    """
    def quad(i, j):
        return (i // QX, j // QY)

    hinges, split = 0, 0
    for i in range(NX):
        for j in range(NY):
            for di, dj in ((1, 0), (0, 1)):
                a, b = i + di, j + dj
                if a < NX and b < NY:
                    hinges += 1
                    if quad(i, j) != quad(a, b):
                        split += 1
    fixed = hinges - split
    ribbons = fixed + 2 * split          # a split coupler is two half ribbons
    bonds = 2 * fixed + 2 * split        # a half ribbon has one tile bond and one coupler pad
    perim = 2 * NX + 2 * NY - 4
    per_q_ribbons = ribbons // 4
    # internal straight cut length, for the seam metrology
    seam_mm = (NX - 1) * NY * TILE + (NY - 1) * NX * TILE
    return {
        "tiles": NX * NY,
        "tiles_per_quadrant": QX * QY,
        "hinges": hinges,
        "split_couplers": split,
        "fixed_hinges": fixed,
        "ribbon_bodies": ribbons,
        "ribbons_per_quadrant": per_q_ribbons,
        "ribbon_bonds": bonds,
        "bonds_per_quadrant": bonds // 4,
        "perimeter_tiles": perim,
        "interior_tiles": NX * NY - perim,
        "tile_pairs": hinges,
        "seam_length_mm": seam_mm,
        "pixels": NX * NY * PX_TILE,
        "emitters": NX * NY * PX_TILE * EMIT_PX,
        "uics": NX * NY * UIC_TILE,
        "tgvs": NX * NY * TGV_TILE,
    }


def save_json(name, obj):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=float)
    return path


if __name__ == "__main__":
    c = lattice_counts()
    for k, v in c.items():
        print(f"{k:22s} {v}")
    # cross-check with the CAD team's body: 256 ribbon bodies
    cad = os.path.join(REPO, "cad", "l6", "body", "body-geometry.json")
    if os.path.exists(cad):
        n = json.load(open(cad))["states"]["rest"]["n_ribbon_bodies"]
        print(f"CAD n_ribbon_bodies {n}: {'match' if n == c['ribbon_bodies'] else 'MISMATCH'}")
