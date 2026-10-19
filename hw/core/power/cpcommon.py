#!/usr/bin/env python3
"""cpcommon.py - shared inputs of the POWER seat of hw/core (block HP-2, Core and Skin).

Reads, read only and without writing bytecode: hw/hostpower/powerpath (common, tiers, hosts, celllife),
hw/energy/out (through that package) and hw/seam/kinematic_seat for the tile stack.
Tags: D = [DECISION], H = [HYPOTHESIS], P = [PUBLICATION], G = [GENERAL], T = [TREE].
Run the scripts with numpy, scipy and matplotlib on the path (install them in user space).
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
PP = os.path.join(ROOT, "hw", "hostpower", "powerpath")
sys.path.insert(0, PP)
import common as HC      # noqa: E402  hostpower common: loads, cells, OCV
import tiers as TI       # noqa: E402  Bare and Buffer sizing, read only
import hosts as HO       # noqa: E402  host classes, read only
import celllife as CL    # noqa: E402  aging model, read only

import numpy as np       # noqa: E402

PAL = HC.PAL
style = HC.style

# ------------------------------------------------------------------ the use cases of hw/energy/04 (T)
CASES = {c["name"]: c for c in HC.BUDGET["cases"]}
CASE_NAMES = [c["name"] for c in HC.BUDGET["cases"]]
# session refresh rate of the pixel stream, Hz [H]. 0 means no pixel link. None means the Skin is dark.
FPS = {
    "wallet standby, screen off, Wi-Fi TWT": None,
    "rear display glance, body dark": None,
    "safe screen, no link": 0,
    "static page at 10 Hz": 10,
    "music on the 3.5 mm jack, screen off": None,
    "voice call on 5G, screen off": None,
    "delta session, 250 nits, Wi-Fi": 60,
    "delta session at 41 % stretch": 60,
    "50 MP camera, viewfinder and upload": 60,
    "video session, Wi-Fi": 120,
    "video outdoors, 800 nits, 5G": 120,
}
WIRE_AT_240HZ = 13.43      # Gb/s, DSC 10 bpp 3:1 on the wire, hw/display/out/interface.txt [T]

# ------------------------------------------------------------------ the Skin add-ons, low / nominal / high [H]
ADD = {
    "link_static_W": (0.015, 0.030, 0.060),     # lanes locked, clock recovery, when the link is on
    "e_rx_pJ_bit": (3.0, 5.0, 10.0),            # SerDes receiver energy per bit [G]
    "backchannel_W": (0.005, 0.010, 0.020),     # 400 Mb/s back channel, enumeration, tile telemetry
    "edge_router_W": (0.010, 0.030, 0.060),     # seat controller, route table, seam sense, display on
    "touch_W": (0.020, 0.050, 0.100),           # AgNW touch scan at 480 Hz, display on
    "identity_W": (0.002, 0.005, 0.010),        # part record chip, always on when powered
    "camera_W": (0.35, 0.35, 0.35),             # sensor and AF and OIS stay with the lens, hw/energy/04 [T]
}
ETA_TILE = 0.92        # tile drivers from VBUS, hw/energy/04 [T]
ETA_LOCAL = 0.88       # the local 1.0 and 1.8 V bucks of the Skin [H]
ETA_CAM = 0.90
LEVELS = {"low": 0, "nom": 1, "high": 2}

# the thermal ceilings of the L.6.0 body in free air, hw/hostpower/thermal [H]
LIMIT_STILL_W = 1.73
LIMIT_WIND_W = 2.37


def skin_load(case, level="nom"):
    """The Skin load of a Leaf 160 for a use case of hw/energy/04: dict of W at the Skin VBUS grid."""
    c = CASES[case]
    k = LEVELS[level]
    body = c["body_W"]
    fps = FPS[case]
    cam = 0.35 if case.startswith("50 MP") else 0.0
    d = dict(body_load_W=body, body_vbus_W=body / ETA_TILE)
    if fps is None:               # the Skin is dark but powered: only the identity chip
        link = bc = router = touch = 0.0
        rate = 0.0
        ident = ADD["identity_W"][k]
    else:
        ident = ADD["identity_W"][k]
        display_on = body > 0
        rate = WIRE_AT_240HZ * fps / 240.0
        link = (ADD["link_static_W"][k] + ADD["e_rx_pJ_bit"][k] * 1e-12 * rate * 1e9) if fps > 0 else 0.0
        bc = ADD["backchannel_W"][k] if fps > 0 else 0.0
        router = ADD["edge_router_W"][k] if display_on else 0.003
        touch = ADD["touch_W"][k] if display_on else 0.0
    addons = link + bc + router + touch + ident
    d.update(link_W=link, backchannel_W=bc, router_W=router, touch_W=touch, identity_W=ident, camera_load_W=cam,
             rate_Gbps=rate, addons_load_W=addons)
    d["addons_vbus_W"] = addons / ETA_LOCAL
    d["camera_vbus_W"] = cam / ETA_CAM
    d["skin_vbus_W"] = d["body_vbus_W"] + d["addons_vbus_W"] + d["camera_vbus_W"]
    return d


def dump(name, obj, lines):
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)
    with open(os.path.join(OUT, name + ".txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
