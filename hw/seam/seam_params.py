#!/usr/bin/env python3
"""seam_params.py - the single source of numbers of the seam and quadrant-swap team.

Budlum Leaf L.6.0, hw/seam. Every other script imports this file, so a number
changes in one place only. Units: SI unless the name ends in _mm or _um.

Source of the fixed inputs: FINAL/21 Sections 21.2.1 to 21.2.7 and the team brief.
Tags follow the repo: [DECISION] fixed by FINAL/21, [HYPOTHESIS] our design value
to be proven by gate MEC-40, [GENERAL] handbook value, [PUBLICATION] cited.
"""
import math

MU0 = 4e-7 * math.pi
EPS0 = 8.8541878128e-12

# --------------------------------------------------------------------------
# body and lattice  [DECISION] FINAL/21 21.2.1
# --------------------------------------------------------------------------
BODY_W_mm, BODY_H_mm, BODY_T_mm = 80.0, 160.0, 2.00
TILE_mm = 10.0
TILES_X, TILES_Y = 8, 16
QUAD_TILES_X, QUAD_TILES_Y = 4, 8          # 32 tiles per quadrant
T_MIN_C, T_MAX_C, T_REF_C = -10.0, 50.0, 23.0

# tile stack, top (z = 0) downwards  [DECISION] FINAL/21 21.2.7
STACK = [  # name, thickness mm
    ("PC cap + AgNW", 0.25),
    ("OCA", 0.05),
    ("glass-LED-glass", 0.25),
    ("slip OCA", 0.03),
    ("Qi coil / spreader", 0.20),
    ("micro cell", 0.90),
    ("hinge routing + tolerance", 0.24),
    ("floating back skin", 0.08),
]
CELL_mm = 9.25                              # cell footprint, so the rim is 0.375 mm
RIM_mm = (TILE_mm - CELL_mm) / 2.0          # 0.375 mm per side
CHAMFER_LEG_mm = 0.90                       # corner chamfer for the hinge [HYPOTHESIS]

# seam optics  [DECISION] FINAL/21 21.2.4
PIXEL_PITCH_um = 50.0
EDGE_PIXEL_um = 20.0
CUT_MAX_um = 10.0
GLASS_GAP_NOM_um = 9.0                      # seat-set glass gap, so pitch 49.0 um [HYPOTHESIS]
GLASS_GAP_TOL_um = 0.8
SHIFT_STEP_um = PIXEL_PITCH_um / 16.0       # 3.125 um, U1 sub-pixel step [DECISION]

# --------------------------------------------------------------------------
# materials  [GENERAL] handbook values
# --------------------------------------------------------------------------
MAT = {
    #            E (Pa), nu,   alpha (1/K), density
    "Si3N4":    (310e9, 0.27, 3.2e-6, 3200),
    "WC-Ni":    (600e9, 0.22, 5.2e-6, 14800),   # binderless or Ni-bound, no Co (corrosion)
    "glass":    (73e9,  0.22, 3.2e-6, 2380),    # display carrier, alkali-free, 3.2 ppm/K
    "PC":       (2.4e9, 0.38, 65e-6, 1200),     # hard-coated polycarbonate cap
    "LEDlayer": (15e9,  0.30, 30e-6, 3000),     # micro-LED + planarisation + metal, effective
    "Ti64":     (114e9, 0.34, 8.6e-6, 4430),
    "PI":       (2.5e9, 0.34, 20e-6, 1420),     # polyimide ribbon
    "NdFeB":    (160e9, 0.24, 5.0e-6, 7500),
}
SIL_OCA_G = 0.06e6          # silicone OCA shear modulus, flat over -40..+80 C [GENERAL]
SIL_OCA_ALPHA = 300e-6
MU_SI3N4_WC = 0.15          # dry sliding friction [GENERAL]

# --------------------------------------------------------------------------
# kinematic seat  [HYPOTHESIS] our design, gate MEC-40
# --------------------------------------------------------------------------
BALL_D_mm = 0.50            # Si3N4 grade G3, sphericity 0.08 um
BALL_GRADE_SPHERICITY_um = 0.08
BALL_Z_mm = 0.85            # ball centre below the cap top, inside the coil/cell rim band
BALL_INSET_um = 40.0        # ball centre lies 40 um inside the ball-side tile face
VEE_INCLUDED_deg = 90.0     # contact angle 45 deg on each flank
GOTHIC_CONFORMITY = 0.54    # flank radius / ball DIAMETER (bearing convention), gothic-arch vee
TRIHEDRAL_NORMAL_deg = 45.0 # trihedral face normals at 45 deg to the seat axis
BALL_S_mm = (1.8, 8.2)      # ball positions along a tile edge, from the hub-side corner
SINGLE_BALL_S_mm = 6.0      # the one ball of a corner tile on a short half-axis
OVERLOAD_RELEASE_N = 1.0    # each vee insert sits on a 1.0 N preloaded stop [HYPOTHESIS]
PRELOAD_PER_BALL_N = 0.25   # preload floor per ball at +50 C (the weakest magnet state)

# magnets  N52H  [DECISION] grade; size [HYPOTHESIS]
N52H = dict(Br=1.44, Br_tc=-0.0012, Hcj=1353e3, Hcj_tc=-0.0060, knee=0.90, Tmax=120.0)
MAG_T_mm = 0.30             # along the seam normal (magnetisation)
MAG_H_mm = 0.50             # z height, 0.60..1.10 mm, centred on the ball line
MAG_Z_mm = 0.85             # centre depth, level with the balls
MAG_RECESS_um = 20.0        # each face recessed and covered, so the magnetic gap is
MAG_GAP_um = GLASS_GAP_NOM_um + 2 * MAG_RECESS_um   # 49 um

# contacts crossing the seat  [DECISION] FINAL/21 21.2.6: two Qi series links per seam
QI_LEAF_TILE = 2            # tile index on each half-axis that carries the two leaves
LEAF_FORCE_N = 0.05         # gold leaf normal force
LEAF_Z_mm = 1.55            # leaf and collar centre depth; a leaf magnet at the same depth cancels them
LEAF_S_mm = (4.0, 6.0)      # leaf positions along the Qi-leaf tile edge
COLLAR = dict(OD_mm=0.24, ID_mm=0.12, h_mm=0.05, squeeze=0.15, E=7e6)  # FFKM collar

# --------------------------------------------------------------------------
# split coupler  [HYPOTHESIS]
# --------------------------------------------------------------------------
RIBBON = dict(t_um=12.5, h_mm=1.2, L_mm=0.8, E=2.5e9, G=0.93e9, sigma_u=231e6)
KEY = dict(w_mm=0.30, l_mm=0.40, h_mm=1.10, flange_mm=0.10)
GATE_PIN_D_mm = 0.12
GATE_PIN_TAU = 550e6        # Ti-6Al-4V shear strength
GATE_LIFT_mm = 0.15
GATE_SPRING_N = 0.04
SMA = dict(d_um=25.0, L_mm=6.0, rho_e=1.425e3, I_hold=0.045, I_pulse=0.150,
           strain=0.030, force_N=0.087, cp=837.0, latent=20e3, dens=6450.0,
           Af_C=90.0, cool_s=0.18)   # Flexinol HT class, 25 um  [GENERAL]


def half_axes():
    """The four seam half-axes of the + crossing.

    Each entry: name, seam line, ball-side quadrant, receiver quadrant,
    tile count, unit vector along the seam (away from the hub), and the
    seam normal pointing from the receiver into the ball side.
    """
    return [
        dict(name="HA1", line="x=0, y>0", ball="Q1", recv="Q2", n=8,
             along=(0.0, 1.0), normal=(1.0, 0.0)),
        dict(name="HA2", line="y=0, x<0", ball="Q2", recv="Q3", n=4,
             along=(-1.0, 0.0), normal=(0.0, 1.0)),
        dict(name="HA3", line="x=0, y<0", ball="Q3", recv="Q4", n=8,
             along=(0.0, -1.0), normal=(-1.0, 0.0)),
        dict(name="HA4", line="y=0, x>0", ball="Q4", recv="Q1", n=4,
             along=(1.0, 0.0), normal=(0.0, -1.0)),
    ]


def seat_contacts():
    """Every ball of the + seat: half-axis, tile, s along the seam, kind, xy (mm).

    Rule: a non-corner tile gets two vees, so it keeps the fold free.
    The hub tile of a long half-axis gets two balls; the hub tile of a short
    half-axis gets one. HA1 hub ball 1 sits in a trihedral (y across x = 0).
    HA2 hub ball sits in a trihedral (x across y = 0). All others are vees.
    """
    out = []
    for ha in half_axes():
        ax, ay = ha["along"]
        for k in range(ha["n"]):
            if k == 0 and ha["n"] == 4:
                s_list = [SINGLE_BALL_S_mm]
            else:
                s_list = list(BALL_S_mm)
            for j, s in enumerate(s_list):
                kind = "vee"
                if ha["name"] == "HA1" and k == 0 and j == 0:
                    kind = "trihedral"
                if ha["name"] == "HA2" and k == 0:
                    kind = "trihedral"
                d = k * TILE_mm + s
                out.append(dict(ha=ha["name"], tile=k, s=s, kind=kind,
                                x=ax * d, y=ay * d, normal=ha["normal"],
                                along=ha["along"], ball=ha["ball"], recv=ha["recv"]))
    return out


def coupler_nodes():
    """The 24 split couplers of the + crossing, at the lattice nodes.

    In the rotating-square lattice each tile pair across an edge shares one
    hinge, at one end of the edge, alternating along the seam. Along x = 0 the
    crossing hinges sit at |y| = 0, 20, 20, 40, 40, 60, 60, 80 mm. Along y = 0
    they sit at |x| = 10, 10, 30, 30 mm.
    """
    nodes = []
    for sgn, ha in ((1, "HA1"), (-1, "HA3")):
        for row in range(8):
            yy = 10 * row if row % 2 == 0 else 10 * (row + 1)
            nodes.append(dict(ha=ha, x=0.0, y=sgn * yy, row=row))
    for sgn, ha in ((-1, "HA2"), (1, "HA4")):
        for col in range(4):
            xx = 10 * (col + 1) if col % 2 == 0 else 10 * col
            nodes.append(dict(ha=ha, x=sgn * xx, y=0.0, row=col))
    return nodes


def stack_z():
    """Return [(name, z_top, z_bottom)] in mm from the cap top."""
    z, out = 0.0, []
    for name, t in STACK:
        out.append((name, z, z + t))
        z += t
    return out


if __name__ == "__main__":
    c = seat_contacts()
    print(f"stack total {sum(t for _, t in STACK):.2f} mm, rim {RIM_mm:.3f} mm")
    print(f"balls {len(c)}: trihedral {sum(1 for q in c if q['kind']=='trihedral')}, "
          f"vee {sum(1 for q in c if q['kind']=='vee')}")
    print(f"couplers {len(coupler_nodes())}")
    for ha in half_axes():
        n = sum(1 for q in c if q["ha"] == ha["name"])
        print(f"  {ha['name']} {ha['line']:10s} {ha['ball']}->{ha['recv']}  balls {n}")
