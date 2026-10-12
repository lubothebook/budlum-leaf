"""rf_common.py - shared constants, geometry and materials of the RF team.

Every number carries its tag in the comment. The geometry comes from
FINAL/21 (sections 21.2, 21.3, 21.4) and HARDWARE/13.
"""
import numpy as np

C0 = 299792458.0
MU0 = 4e-7 * np.pi
EPS0 = 1.0 / (MU0 * C0 ** 2)
ETA0 = MU0 * C0
KB = 1.380649e-23
T0 = 290.0

# ------------------------------------------------------------------ body
BODY_W = 80.0e-3          # [DECISION] FINAL/21 21.2.1, short edge (x)
BODY_L = 160.0e-3         # [DECISION] long edge (y)
BODY_T = 2.00e-3          # [DECISION] tile stack
TILE = 10.0e-3            # [DECISION] 8 x 16 tiles
NX, NY = 8, 16
THETA_DEFAULT = np.radians(17.5)   # [DECISION] 25.4 % stretch
THETA_MAX = np.radians(45.0)       # [DECISION] 41.4 % stretch

# tile stack, from the front face (z = +1.00 mm) down, FINAL/21 21.2.7 [DECISION]
STACK = [("PC cap + AgNW touch", 0.25e-3, 2.9, 0.010),
         ("OCA", 0.05e-3, 3.0, 0.020),
         ("glass / micro-LED / glass", 0.25e-3, 5.8, 0.005),
         ("slip OCA", 0.03e-3, 3.0, 0.020),
         ("Qi coil or graphite spreader", 0.20e-3, None, None),   # conductor
         ("micro cell can", 0.90e-3, None, None),                 # conductor
         ("back skin TPU", 0.08e-3, 2.8, 0.020),
         ("hinge routing", 0.24e-3, 3.3, 0.005)]
CELL = 9.25e-3            # [DECISION] can footprint, so 0.375 mm inset from the tile edge
CAN_INSET = (TILE - CELL) / 2

# conductor of the body ground [GENERAL] handbook conductivities
SIGMA = {"Cu": 5.8e7, "Cu_LDS": 3.5e7, "SS304": 1.4e6, "Ti": 2.4e6,
         "graphite_PGS": 1.0e6, "EGaIn": 3.4e6, "Au": 4.1e7}

# ------------------------------------------------------------------ bar
BAR_L, BAR_W, BAR_T = 32.0e-3, 4.0e-3, 1.00e-3     # [DECISION] FINAL/21 21.3.1
# bar layers from the edge outward (y), FINAL/21 21.3.2 [DECISION]
BAR_STACK = [("contact layer LCP + 12 gold leaves", 0.25e-3),
             ("mmWave layer, two-layer LCP flex", 0.10e-3),
             ("core LCP-GF40", 0.40e-3),
             ("antenna layer LDS copper", 0.05e-3),
             ("top skin LCP-GF40", 0.20e-3)]
EPS_LCP_GF40, TAN_LCP_GF40 = 3.9, 0.005    # [HYPOTHESIS] glass-filled LCP class, 2-6 GHz
EPS_LCP_FILM, TAN_LCP_FILM = 3.0, 0.002    # [PUBLICATION] Rogers ULTRALAM 3850HT class, Dk 2.9-3.14
H_ANT = 0.75e-3           # copper bottom over the bar bottom [DECISION] from BAR_STACK
H_EDGE = 1.00e-3          # the radiator height of FINAL/21 21.4.1 item 2 [DECISION]

# ------------------------------------------------------------------ ring
RING_RO, RING_RI, RING_T = 16.0e-3, 12.0e-3, 4.00e-3   # [DECISION]
PCBA_R = 15.0e-3          # Ring PCBA d 30.0 [DECISION] HARDWARE/13
JACK_CHORD = 13.8e-3      # bore axis from the ring centre [DECISION] 21.3.6
JACK_BORE = 4.0e-3        # outside of the bore with walls
JACK_TROUGH = 9.0e-3      # the open trough in the rim
JACK_CLOSED = 5.0e-3      # the closed blind end


def db(x):
    return 10 * np.log10(x)


def undb(x):
    return 10 ** (x / 10)


def surface_resistance(f, sigma, mur=1.0):
    return np.sqrt(np.pi * f * MU0 * mur / sigma)


def stretch_factor(theta):
    return np.cos(theta) + np.sin(theta)


def fspl_db(d, f):
    return 20 * np.log10(4 * np.pi * d * f / C0)


def noise_floor_dbm(bw_hz, nf_db):
    return 10 * np.log10(KB * T0 * bw_hz * 1e3) + nf_db
