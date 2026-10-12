#!/usr/bin/env python3
"""netmodel.py: the shared delay model of the discovery team.

FINAL/21 Section 21.5.4 and 21.5.7. Gates SW-24, DST-11, DST-12.

All times are milliseconds and all distances are kilometres. Every parameter
is [HYPOTHESIS] unless its comment names a [DECISION] or a [PUBLICATION].
The stage means match the table of FINAL/21 Section 21.5.7, so the
simulations of this directory start from the same budget as the decision.

Run it alone to print the check against the 21.5.7 table:
    python3 netmodel.py
"""
import math
import random

# --------------------------------------------------------------- physics ---
# [PUBLICATION] ITU-T G.652 fibre: group index about 1.468, so light moves
# 299792.458 / 1.468 = 204.2 km per ms, about 4.9 us per km.
C_FIBRE_KM_PER_MS = 299792.458 / 1.468 / 1000.0
# Free space, for UWB and any radio relay leg.
C_AIR_M_PER_NS = 0.299792458

FRAME_HZ = 240.0                      # [DECISION] 240 Hz scan-out
FRAME_MS = 1000.0 / FRAME_HZ          # 4.1667 ms
TOUCH_HZ = 480.0                      # [DECISION] touch scan


def fibre_ms(km, stretch=1.5):
    """One-way fibre delay for a straight-line distance and a route stretch.

    A metro fibre route is 1.3 to 2.0 times the straight line [HYPOTHESIS].
    """
    return km * stretch / C_FIBRE_KM_PER_MS


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


# --------------------------------------------------- the fixed stages ---
# Means match FINAL/21 Section 21.5.7: touch 1.8, render 4.3, encode 1.5,
# decode 1.5, scan-out 2.4. Shapes are [HYPOTHESIS].

def touch_ms(r):
    return r.uniform(0.0, 1000.0 / TOUCH_HZ) + 0.758


def render_ms(r):
    return r.gammavariate(100.0, 4.3 / 100.0)      # cv 0.10


def encode_ms(r):
    return r.gammavariate(100.0, 1.5 / 100.0)


def decode_ms(r):
    return r.gammavariate(100.0, 1.5 / 100.0)


def scanout_ms(r):
    return r.uniform(0.0, FRAME_MS) + 0.317


# ----------------------------------------------------------- the air ---
# Wi-Fi 7 MLO: mean 1.0 ms each way (21.5.7). Gamma with cv 0.6.
# 5G SA with configured grant on a 2.5 ms TDD pattern: uplink waits for a
# slot, uniform on 2.5 ms, plus 1.05 ms of processing, mean 2.3 ms. The
# downlink mean is 1.3 ms. A block error at 10 % adds one HARQ round of 3 ms
# [PUBLICATION] 3GPP TS 38.211 and TS 38.214 numerology; values [HYPOTHESIS].

WIFI = "wifi"
CELL = "cell"


def air_up_ms(r, kind):
    if kind == WIFI:
        return r.gammavariate(2.78, 1.0 / 2.78)
    t = r.uniform(0.0, 2.5) + 0.75
    if r.random() < 0.10:
        t += 3.0
    return t


def air_dl_ms(r, kind):
    if kind == WIFI:
        return r.gammavariate(2.78, 1.0 / 2.78)
    t = r.uniform(0.0, 1.0) + 0.5
    if r.random() < 0.10:
        t += 3.0
    return t


AIR_UP_MEAN = {WIFI: 1.0, CELL: 2.3}
AIR_DL_MEAN = {WIFI: 1.0, CELL: 1.3}

# ------------------------------------------------------- the wired part ---
HOP_MS = 0.02          # one router or switch hop, one way [HYPOTHESIS]
OLT_MS = 0.15          # GPON OLT and home gateway, one way [HYPOTHESIS]
UPF_MS = 0.10          # 5G UPF and local breakout, one way [HYPOTHESIS]


def wired_ow_ms(km_access, km_core, stretch_access=1.6, stretch_core=1.5,
                hops=4, fixed=0.0):
    """One-way wired delay: access leg to the breakout, then core to the validator."""
    return (fibre_ms(km_access, stretch_access) + fibre_ms(km_core, stretch_core)
            + hops * HOP_MS + fixed)


def queue_ms(r, mean):
    """Queueing at the validator ingress and egress, exponential [HYPOTHESIS]."""
    return r.expovariate(1.0 / mean) if mean > 0 else 0.0


# ------------------------------------------------ the check of 21.5.7 ---

def input_to_photon(r, kind, wired_ow, q_mean=0.03):
    """One new action, end to end, for one access kind and one wired leg."""
    t = touch_ms(r) + air_up_ms(r, kind) + wired_ow + queue_ms(r, q_mean)
    t += render_ms(r) + encode_ms(r)
    t += wired_ow + queue_ms(r, q_mean) + air_dl_ms(r, kind)
    t += decode_ms(r) + scanout_ms(r)
    return t


def _pct(xs, p):
    xs = sorted(xs)
    k = min(len(xs) - 1, max(0, int(round(p / 100.0 * (len(xs) - 1)))))
    return xs[k]


def check_table(n=200_000, seed=7):
    r = random.Random(seed)
    cases = {
        # name: (kind, one-way wired, the mean of 21.5.7)
        "wifi_room (AP to dock, 0.05 ms)": (WIFI, 0.05, 13.6),
        "wifi_city (10 km, PoP, 0.6 ms)": (WIFI, wired_ow_ms(3, 10, fixed=OLT_MS), 14.7),
        "5g_cellsite (0.15 ms)": (CELL, UPF_MS + 0.05, 15.4),
    }
    out = {}
    for name, (kind, ow, ref) in cases.items():
        xs = [input_to_photon(r, kind, ow) for _ in range(n)]
        out[name] = dict(wired_ow_ms=round(ow, 3), mean=round(sum(xs) / n, 2),
                         p50=round(_pct(xs, 50), 2), p99=round(_pct(xs, 99), 2),
                         ref_mean_21_5_7=ref)
    return out


if __name__ == "__main__":
    import json
    print("fibre: %.1f km per ms one way, 20 km straight at stretch 2.0 = %.3f ms"
          % (C_FIBRE_KM_PER_MS, fibre_ms(20, 2.0)))
    print(json.dumps(check_table(), indent=2))
