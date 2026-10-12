#!/usr/bin/env python3
"""params.py - the single parameter set of the L.6.0 Leaf Dock.

Dock team, hw/dock/. Gate SW-20 (FINAL/21, Section 21.4.4 and 21.8).
Every other script in this directory imports this file. Tags follow the
team brief: D = [DECISION], H = [HYPOTHESIS], P = [PUBLICATION], T = [TREE].
"""

# ------------------------------------------------------------------ the Leaf
LEAF_W, LEAF_L, LEAF_T = 80.0, 160.0, 2.00      # mm, D FINAL/21
LEAF_R_PLAN = 6.35                              # mm plan corner, D brief s4
QI_COIL_D = 46.0                                # mm, Rx sector coils, D FINAL/21

# ------------------------------------------------------------------ soft edges
EDGE_R = 0.50          # mm, every dock outer edge, D brief s4 (Ayaz 2026-10-12)
WINDOW_BREAK = 0.10    # mm, the pad window edge break, D brief s4 "windows"
FILLET_SEGMENTS = 8    # facets per 90 deg of fillet in the STL

# ------------------------------------------------------------------ enclosure
DOCK_W = 162.0         # mm, X: pad zone + electronics bay, H
DOCK_L = 200.0         # mm, Y: fence + pad + exhaust, H
DOCK_H = 24.0          # mm, Z: deck top above the floor, H (stack below)
DOCK_R_PLAN = 10.0     # mm plan corner of the deck, H
WALL = 1.6             # mm side wall, PC-GF10 top cover, H
FLOOR = 1.2            # mm, 6061-T6 floor tub, H
CEIL = 1.6             # mm top cover over the electronics bay, H

PAD_W, PAD_L = LEAF_W + 4.0, LEAF_L + 4.0       # mm AlN window, 2 mm margin
PAD_R = LEAF_R_PLAN + 2.0
PAD_T = 0.80           # mm AlN window, k = 170 W/mK, H
PAD_CX = 6.0 + PAD_W / 2.0                      # mm from the -X outer face
PAD_CY = 14.0 + PAD_L / 2.0                     # mm from the -Y outer face
APERTURE_INSET = 3.0   # mm ledge that holds the window, H

FENCE_W, FENCE_D, FENCE_H = 40.0, 6.0, 3.0      # mm, the pin fence, H
FENCE_Y0 = 14.0 - 1.0 - FENCE_D                 # mm, its -Y face; 1 mm gap to pad
PIN_COUNT, PIN_PITCH = 12, 0.80                 # D FINAL/21 21.3.2, hw/energy
PIN_SLOT_W, PIN_SLOT_H, PIN_SLOT_DEPTH = 10.4, 1.2, 3.0

FOOT_D, FOOT_H = 14.0, 4.0                      # mm silicone feet, 40 Shore A, H
USBC_W, USBC_H = 9.0, 3.4                        # mm opening, H
ETH_W, ETH_H = 0.0, 0.0                          # no RJ45: 2.5 GbE over USB-C alt, H

# the vertical stack under the pad, top down, mm, H
PAD_STACK = [
    ("AlN window", 0.80),
    ("Tx coil and ferrite in a cold-plate pocket", 3.00),   # copper vapour chamber
    ("TEC module, 127 couples", 3.40),
    ("heat-sink base", 2.50),
    ("fins, 0.15 mm Cu at 1.2 mm pitch", 9.00),
    ("air plenum", 2.10),
    ("floor", FLOOR),
]

# ------------------------------------------------------------------ the charge paths
QI_P_RX = 25.0           # W after the Leaf rectifier, D FINAL/21
CONTACT_P_RX = 25.0      # W at the VHV leaves, D FINAL/20, hw/energy
CONTACT_V = 12.0         # V on VHV (leaves 5 and 8), hw/energy/out/bar_pins.txt
PAD_SETPOINT = 22.0      # deg C, the regulated pad, sim/thermal F5
PAD_FLOOR = 22.0         # deg C, the lowest setpoint, lithium plating rule, sim/thermal
ETA_TX_COIL = 0.95       # Tx coil + ferrite, H
ETA_INVERTER = 0.97      # GaN full bridge, H
ETA_TX_FRONT = 0.97      # the buck that feeds the bridge, H
ETA_CONTACT_BB = 0.96    # the 12 V buck-boost for the leaves, H
F_DEVICE_HEAT_TO_PAD = 0.87   # share of Leaf heat that leaves through the back, H
UA_PAD_LEAK = 0.15       # W/K, the cold plate to the room, through 3 mm foam, H
R_COLD = 0.15            # K/W, AlN + TIM + vapour chamber to the TEC cold face, H
R_SINK_TEC = 0.30        # K/W, the TEC fin section at the blower flow, H

# a 127-couple 40 x 40 x 3.4 mm module, rated at Th = 50 deg C, H
TEC = dict(n_modules=2, Imax=6.0, Vmax=15.7, dTmax=70.0, Qmax=58.0, Th_rated=50.0)

# ------------------------------------------------------------------ the pack
PACK_S, PACK_P = 2, 1
CELL_V_NOM, CELL_AH = 3.70, 2.75     # LiPo 605080 class, H
PACK_USABLE = 0.95                    # 3.0 V to 4.2 V window, H
PACK_CHARGE_W = 20.0                  # W, 1 C, H

# ------------------------------------------------------------------ the loads, W
# (name, idle, typical, peak, tag)
LOADS = {
    "Wi-Fi 7 AP (SoC + 2x2 5 GHz + 2x2 6 GHz)": (3.0, 6.5, 9.0, "H"),
    "60 GHz 802.11ay radio + 32-element array": (0.4, 2.5, 4.0, "H"),
    "UWB anchor, secure ranging (STS)": (0.05, 0.15, 0.30, "H"),
    "secure element + 1-wire dock identity": (0.01, 0.02, 0.05, "H"),
    "PD sink, charger, housekeeping MCU": (0.20, 0.40, 0.60, "H"),
    "blower, 60 mm class": (0.0, 0.8, 1.6, "H"),
    "status light bar": (0.02, 0.05, 0.10, "H"),
}
VALIDATOR = {
    "compute module (Orin NX 16 GB class)": (5.0, 18.0, 25.0, "H"),
    "NVMe 1 TB, M.2 2242": (0.05, 1.5, 3.5, "H"),
    "2.5 GbE PHY": (0.3, 0.8, 1.0, "H"),
    "PKCS#11 signer (TEE + SE)": (0.02, 0.05, 0.10, "H"),
}

WALL_FEED_W = 140.0    # USB-C PD 3.1 EPR, 28 V 5 A, H
