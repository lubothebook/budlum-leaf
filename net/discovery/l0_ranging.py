#!/usr/bin/env python3
"""l0_ranging.py: the L0 distance bound. Can a relay make a far validator look near?

FINAL/21 Section 21.5.4, layer L0. Gate SW-24: "a relayed validator fails
the distance proof".

The model
  * IEEE 802.15.4z HRP UWB with STS, double-sided two-way ranging (DS-TWR)
    [PUBLICATION] IEEE 802.15.4z-2020; the DS-TWR formula is the
    asymmetric one of Neirynck, Luk, McLoughlin, IEEE WPNC 2016;
  * clock offsets of +-20 ppm on each side, reply times of 200 to 400 us;
  * first-path timing noise of 0.25 ns rms (about 7.5 cm), so the 1 sigma
    distance error is near the +-10 cm of the decision;
  * a relay adds its own latency plus the cable or air path it bridges;
  * the distance-reduction attack on the STS receiver: Ghost Peak succeeds
    in about 4 % of attempts and moves the result by up to 12 m
    [PUBLICATION] Leu, Camurati, Heinrich, Roeschlin, Anliker, Hollick,
    Capkun, Classen, "Ghost Peak", USENIX Security 2022.

The rule under test (SPEC.md Section 2.3)
  * N = 8 DS-TWR rounds with fresh STS from one ML-KEM session;
  * pass when the median is <= 10 m AND the spread (max - min) is <= 0.6 m;
  * and the QUIC round trip of the session is <= 2 ms (the L0 class).

Output: results/l0_ranging.json.
    python3 l0_ranging.py
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
C = 0.299792458        # m per ns
BOUND_M = 10.0
SPREAD_M = 0.6
N_ROUNDS = 8
SIGMA_NS = 0.25
GHOST_P = 0.04
GHOST_MAX_M = 12.0


def ds_twr(rng, tof_ns, n, ppm_i, ppm_r):
    """Measured ToF of n DS-TWR rounds, with clock offsets and first-path noise."""
    reply1 = rng.uniform(200e3, 400e3, n)       # ns, responder
    reply2 = rng.uniform(200e3, 400e3, n)       # ns, initiator
    ki, kr = 1 + ppm_i * 1e-6, 1 + ppm_r * 1e-6
    noise = lambda: rng.normal(0, SIGMA_NS, n)
    round1 = (2 * tof_ns + reply1) * ki + noise()      # initiator clock
    round2 = (2 * tof_ns + reply2) * kr + noise()      # responder clock
    treply1 = reply1 * kr + noise()
    treply2 = reply2 * ki + noise()
    return (round1 * round2 - treply1 * treply2) / (round1 + round2 + treply1 + treply2)


def verdict(d):
    return (np.median(d) <= BOUND_M) and (d.max() - d.min() <= SPREAD_M)


def main():
    rng = np.random.default_rng(21)
    out = dict(params=dict(N_ROUNDS=N_ROUNDS, BOUND_M=BOUND_M, SPREAD_M=SPREAD_M,
                           SIGMA_NS=SIGMA_NS))
    # 1. honest error at 3 m, the clocks at +-20 ppm
    err = []
    for _ in range(5000):
        d = ds_twr(rng, 3.0 / C, 1, rng.uniform(-20, 20), rng.uniform(-20, 20)) * C
        err.append(d[0] - 3.0)
    err = np.array(err)
    out["honest_error_cm"] = dict(mean=round(100 * err.mean(), 2), sd=round(100 * err.std(), 2),
                                  p99_abs=round(100 * np.quantile(abs(err), 0.99), 2))
    # 2. honest pass rate at 1, 5, 9.5 m
    out["honest_pass"] = {}
    for true_m in (1.0, 5.0, 9.5):
        ok = sum(verdict(ds_twr(rng, true_m / C, N_ROUNDS, rng.uniform(-20, 20),
                                rng.uniform(-20, 20)) * C) for _ in range(2000))
        out["honest_pass"][true_m] = ok / 2000
    # 3. relays: (name, extra one-way ns). A relay sits 2 m from the Leaf.
    relays = {
        "analog RF relay, 5 m cable": 5 / (0.7 * C),
        "analog RF relay, 30 m cable": 30 / (0.7 * C),
        "digital relay, 100 ns": 100.0,
        "digital relay, 1 us": 1000.0,
        "Wi-Fi bridge to next flat, 50 us": 50e3,
        "fibre to a validator 10 km away": 10e3 * 1.468 / C,
    }
    out["relay"] = {}
    for name, extra_ns in relays.items():
        tof = 2.0 / C + extra_ns
        d = ds_twr(rng, tof, N_ROUNDS, 5, -5) * C
        out["relay"][name] = dict(measured_m=round(float(np.median(d)), 2), passes=bool(verdict(d)))
    # 4. Ghost Peak on a validator at 25 m: every round must be pulled the same
    #    way and stay inside the spread, so the attempts must all succeed.
    out["ghost_peak"] = {}
    for n in (1, 2, 4, 8):
        trials = 200_000
        hits = rng.random((trials, n)) < GHOST_P
        out["ghost_peak"][n] = dict(success=float(hits.all(axis=1).mean()),
                                    analytic=GHOST_P ** n)
    out["ghost_peak_note"] = "N = 8 gives 0.04^8 = 6.6e-12 per session when rounds are independent"
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "l0_ranging.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
