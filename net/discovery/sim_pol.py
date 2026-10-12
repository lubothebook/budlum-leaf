#!/usr/bin/env python3
"""sim_pol.py: coverage rewards and latency proof of location under attack.

FINAL/21 Section 21.5.4 ("the density, by the protocol"). Gate SW-24, and
research order RG-18 for the slashing side.

The mechanism under test (SPEC.md Section 6)
  * a validator claims a cell X. Challengers measure the min-filtered round
    trip to it. Physics forbids a reply faster than the fibre allows, so a
    prover can only look farther, never closer;
  * the chain holds a calibrated route stretch per region (the latency map),
    so each challenger has an expected round trip e_c for the claim;
  * a challenger reports "consistent" when m_c <= e_c (1 + tau) + delta;
  * the claim fails when R_REJ or more of the K challengers report
    inconsistent. An honest prover meets only Byzantine "inconsistent"
    reports; a spoofer meets every honest challenger on the far side of X.

The attacks
  G1  spoof: the GPU sits at Y in a city, the claim is X at distance D;
  G1b spoof with Byzantine challengers (a stake share f) that vouch for it;
  G2  relay hotspot: a cheap keyed box at X, the GPU at Y;
  G3  framing: Byzantine challengers try to fail an honest validator;
  G4  fake demand: Sybil Leafs that farm session-minute emission.

The challenger selection rules compared
  D0  the 24 nearest challengers by claimed position (the witness model of
      early location networks);
  D1  24 by VRF, stake weighted, 4 in each 60 degree sector, inside 400 km;
  D2  16 by VRF in the sectors (round-robin) plus 8 from the tenure pool
      (1 year of consistent latency-map history), where the attacker holds
      a share f/2;
  D3  D2, and a challenger must pass its own claim, weighted by served
      session minutes. Only the attacker boxes that sit near X (PHYS = 10 %)
      stay in the pool.

Output: results/pol.json and results/pol_spoof.png.
    python3 sim_pol.py [--quick]
"""
import argparse
import json
import math
import os

import numpy as np

import netmodel as nm

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

REGION_KM = 1000.0
N_CITIES = 40
N_HONEST = 400
RURAL_SHARE = 0.15
K = 24
SECTORS = 6
R_SEL_KM = 400.0
R_REJ = 6            # a claim fails when 6 or more of the 24 report inconsistent
CELL_KM = 100.0      # the coverage-bonus cell, matched to the PoL resolution
TAU = 0.10           # relative tolerance (see tau_sweep)
DELTA_MS = 0.30      # absolute tolerance
SIGMA_CAL = 0.06     # error of the calibrated stretch, relative [HYPOTHESIS]
RULES = ("D0", "D1", "D2", "D3")
SLASH_SHARE = 0.05   # stake slashed on a failed claim [DECISION proposal]


def make_region(rng):
    cities = rng.uniform(0, REGION_KM, size=(N_CITIES, 2))
    pop = 1.0 / np.arange(1, N_CITIES + 1)          # Zipf
    pop /= pop.sum()
    n_city = int(N_HONEST * (1 - RURAL_SHARE))
    which = rng.choice(N_CITIES, size=n_city, p=pop)
    spread = 5 + 25 * np.sqrt(pop[which] / pop.max())
    urban = cities[which] + rng.normal(0, 1, size=(n_city, 2)) * spread[:, None]
    rural = rng.uniform(0, REGION_KM, size=(N_HONEST - n_city, 2))
    H = np.clip(np.vstack([urban, rural]), 0, REGION_KM)
    return cities, pop, H


def stretch(rng, n):
    """Route stretch of a pair: 1.2 plus an exponential of mean 0.35, cap 3 [HYPOTHESIS]."""
    return np.minimum(3.0, 1.2 + rng.exponential(0.35, n))


def rtt_ms(d_km, s):
    """Min-filtered round trip: fibre both ways, 6 hops each way, 0.1 ms access."""
    return 2 * d_km * s / nm.C_FIBRE_KM_PER_MS + 2 * 6 * nm.HOP_MS + 0.1


def select(rng, X, H, att_pos, rule, f_tenure):
    """Return (positions, is_byzantine) of the K challengers for a claim at X."""
    pool = np.vstack([H, att_pos]) if len(att_pos) else H
    byz = np.r_[np.zeros(len(H), bool), np.ones(len(att_pos), bool)]
    d = np.hypot(*(pool - X).T)
    if rule == "D0":
        idx = np.argsort(d)[:K]
        return pool[idx], byz[idx]
    ang = np.arctan2(pool[:, 1] - X[1], pool[:, 0] - X[0])
    sec = ((ang + math.pi) / (2 * math.pi) * SECTORS).astype(int) % SECTORS
    ok = (d < R_SEL_KM) & (d > 1.0)
    picks = []
    n_sector = 4 if rule == "D1" else 3                 # D2, D3: 16 in sectors + ...
    for s in range(SECTORS):
        cand = np.flatnonzero(ok & (sec == s))
        if len(cand) == 0:
            continue
        picks.extend(rng.choice(cand, size=min(n_sector, len(cand)), replace=False))
    if rule in ("D2", "D3"):
        picks = picks[:16]
    P, B = list(pool[picks]), list(byz[picks])
    if rule in ("D2", "D3"):                            # ... the tenure pool
        need = K - len(P)
        hon = np.flatnonzero(ok & ~byz)
        for _ in range(need):
            if rng.random() < f_tenure or len(hon) == 0:
                P.append(X + rng.normal(0, 20, 2))      # an aged Byzantine identity
                B.append(True)
            else:
                P.append(pool[rng.choice(hon)])
                B.append(False)
    else:
        need = K - len(P)                               # empty sectors: fill at random
        rest = np.setdiff1d(np.flatnonzero(ok), picks)
        if need > 0 and len(rest):
            extra = rng.choice(rest, size=min(need, len(rest)), replace=False)
            P += list(pool[extra])
            B += list(byz[extra])
    return np.array(P), np.array(B, bool)


def verifiable(X, H, min_per_sector=2, min_sectors=5):
    """A cell is verifiable when tenured (honest) validators surround it.

    The chain computes this per epoch from the latency map: at least
    min_per_sector tenured validators inside R_SEL_KM in min_sectors of
    the 6 sectors. Only verifiable cells earn the coverage bonus.
    """
    d = np.hypot(*(H - X).T)
    ok = (d < R_SEL_KM) & (d > 1.0)
    ang = np.arctan2(H[ok, 1] - X[1], H[ok, 0] - X[0])
    sec = ((ang + math.pi) / (2 * math.pi) * SECTORS).astype(int) % SECTORS
    counts = np.bincount(sec, minlength=SECTORS)
    return int((counts >= min_per_sector).sum()) >= min_sectors


PHYS = 0.10   # D3: share of attacker challenger identities physically near X [HYPOTHESIS]


def attacker_layout(rng, X, n_att):
    """Byzantine identities claim positions round X, 2 per sector, 15-60 km out."""
    if n_att == 0:
        return np.zeros((0, 2))
    ang = rng.uniform(0, 2 * math.pi, n_att)
    r = rng.uniform(15, 60, n_att)
    return X + np.c_[r * np.cos(ang), r * np.sin(ang)]


def trial(rng, H, X, Y, att_pos, rule, f_tenure, honest_prover, frame):
    """One claim at X by a prover truly at Y. Returns True when the claim passes."""
    if rule == "D3" and len(att_pos):
        # a challenger must pass its own claim: only boxes really near X stay
        att_pos = att_pos[: int(round(PHYS * len(att_pos)))]
    C, B = select(rng, X, H, att_pos, rule, f_tenure)
    if len(C) == 0:
        return False
    n = len(C)
    dX = np.hypot(*(C - X).T)
    dY = np.hypot(*(C - Y).T)
    s_true = stretch(rng, n)
    s_cal = s_true * (1 + rng.normal(0, SIGMA_CAL, n))   # the latency map's estimate
    e = rtt_ms(dX, s_cal)
    true = rtt_ms(dY, s_true)
    # the prover adds delay to any challenger that sees it too close: m = max(true, e)
    m = np.maximum(true, e) if not honest_prover else true
    consistent = m <= e * (1 + TAU) + DELTA_MS
    if frame:                       # Byzantine challengers report a fail
        consistent = np.where(B, False, consistent)
    else:                           # Byzantine challengers vouch for their prover
        consistent = np.where(B, True, consistent)
    return (n - consistent.sum()) < R_REJ


def spoof_grid(rng, H, cities, pop, trials):
    out = {}
    n_h = len(H)
    for rule in RULES:
        for f in (0.0, 0.1, 0.2, 0.33, 0.5):
            n_att = int(round(f / (1 - f) * n_h)) if f < 1 else 0
            # the attacker spreads its identities over 10 regions it targets
            n_local = n_att // 10
            for D in (10, 25, 50, 100, 200, 400):
                ok = n_ok = 0
                for _ in range(trials * 3):
                    if n_ok >= trials:
                        break
                    Y = cities[rng.choice(len(cities), p=pop)] + rng.normal(0, 5, 2)
                    a = rng.uniform(0, 2 * math.pi)
                    X = np.clip(Y + D * np.array([math.cos(a), math.sin(a)]), 0, REGION_KM)
                    if not verifiable(X, H):
                        continue             # an unverifiable cell earns no bonus
                    n_ok += 1
                    att = attacker_layout(rng, X, n_local)
                    ok += trial(rng, H, X, Y, att, rule, f / 2, False, False)
                out[f"{rule}|f={f}|D={D}"] = ok / max(1, n_ok)
    return out


def frame_grid(rng, H, trials):
    out = {}
    n_h = len(H)
    for rule in RULES:
        for f in (0.0, 0.1, 0.2, 0.33, 0.5):
            n_att = int(round(f / (1 - f) * n_h))
            n_local = n_att // 10
            for kind in ("urban", "rural"):
                fails = 0
                for _ in range(trials):
                    X = H[rng.integers(0, int(len(H) * (1 - RURAL_SHARE)))] if kind == "urban" \
                        else H[rng.integers(int(len(H) * (1 - RURAL_SHARE)), len(H))]
                    att = attacker_layout(rng, X, n_local)
                    fails += not trial(rng, H, X, X, att, rule, f / 2, True, True)
                out[f"{rule}|f={f}|{kind}"] = fails / trials
    return out


def bonus_capture(rng, H, cities, pop, trials):
    """Share of the coverage bonus pool the attacker captures.

    The pool pays each verified cell of CELL_KM equally, split among the
    validators in it. The attacker keeps its GPUs in the 5 largest cities and
    claims every empty cell from the nearest of them. It claims a cell only
    when the expected bonus beats the expected slash. One identity per cell.
    """
    n = int(REGION_KM // CELL_KM)
    occ = set(map(tuple, (H // CELL_KM).astype(int).tolist()))
    empty = [(i, j) for i in range(n) for j in range(n) if (i, j) not in occ]
    big = cities[np.argsort(-pop)[:5]]
    n_ver = sum(verifiable(np.array([(i + 0.5) * CELL_KM, (j + 0.5) * CELL_KM]), H)
                for i in range(n) for j in range(n))
    out = dict(cells=n * n, honest_cells=len(occ), empty_cells=len(empty),
               verifiable_cells=n_ver)
    for rule in RULES:
        for f in (0.1, 0.2, 0.33):
            n_att = int(round(f / (1 - f) * N_HONEST))
            n_local = n_att // 10
            gains = []
            for (i, j) in empty:
                X = np.array([(i + 0.5) * CELL_KM, (j + 0.5) * CELL_KM])
                if not verifiable(X, H):
                    continue
                Y = big[np.argmin(np.hypot(*(big - X).T))]
                ok = sum(trial(rng, H, X, Y, attacker_layout(rng, X, n_local), rule,
                               f / 2, False, False) for _ in range(trials))
                p = ok / trials
                bonus = 1.0 / (len(occ) + 1)
                if p * bonus - (1 - p) * SLASH_SHARE * bonus * 20 > 0:   # slash = 20 cell-epochs x 5 %
                    gains.append(p)
            gains = sorted(gains, reverse=True)[:n_att]
            won = sum(gains)
            out[f"{rule}|f={f}"] = dict(share=round(won / (len(occ) + won), 4),
                                        cells_claimed=len(gains), expected_cells_won=round(won, 2))
    return out


def tau_sweep(rng, H, cities, pop, trials):
    """Resolution against honest false fails, f = 0, for three tolerances."""
    global TAU
    keep = TAU
    out = {}
    for tau in (0.05, 0.10, 0.15):
        TAU = tau
        row = {}
        for D in (25, 50, 100):
            ok = n = 0
            while n < trials:
                Y = cities[rng.choice(len(cities), p=pop)] + rng.normal(0, 5, 2)
                a = rng.uniform(0, 2 * math.pi)
                X = np.clip(Y + D * np.array([math.cos(a), math.sin(a)]), 0, REGION_KM)
                if not verifiable(X, H):
                    continue
                n += 1
                ok += trial(rng, H, X, Y, np.zeros((0, 2)), "D1", 0, False, False)
            row[f"spoof_D={D}"] = ok / trials
        ff = sum(not trial(rng, H, X, X, np.zeros((0, 2)), "D1", 0, True, True)
                 for X in H[rng.integers(0, len(H), trials)] if verifiable(X, H))
        row["honest_false_fail"] = ff / trials
        out[tau] = row
    TAU = keep
    return out


def sigma_sweep(rng, H, cities, pop, trials):
    """The calibration error of the latency map is the key unknown."""
    global SIGMA_CAL
    keep = SIGMA_CAL
    out = {}
    for sig in (0.06, 0.15, 0.25):
        SIGMA_CAL = sig
        ok = n = 0
        while n < trials:
            Y = cities[rng.choice(len(cities), p=pop)] + rng.normal(0, 5, 2)
            a = rng.uniform(0, 2 * math.pi)
            X = np.clip(Y + 100 * np.array([math.cos(a), math.sin(a)]), 0, REGION_KM)
            if not verifiable(X, H):
                continue
            n += 1
            ok += trial(rng, H, X, Y, np.zeros((0, 2)), "D1", 0, False, False)
        Xs = [X for X in H[rng.integers(0, len(H), trials)] if verifiable(X, H)]
        ff = sum(not trial(rng, H, X, X, np.zeros((0, 2)), "D1", 0, True, True) for X in Xs)
        out[sig] = dict(spoof_D100=ok / trials, honest_false_fail=ff / max(1, len(Xs)))
    SIGMA_CAL = keep
    return out


def relay_detect(rng, trials=20000, n_samples=20):
    """G2: a keyed relay box at X, the GPU at Y. A render-in-the-loop challenge
    sends a session frame request; its round trip minus the ping is the render
    plus encode time plus any relay leg. The check passes when the min over
    n_samples of that excess is under render_min + guard."""
    out = {}
    guard = 0.6  # ms
    render_min = 4.3 * 0.75 + 1.5 * 0.75   # the floor of the render model
    for D in (0, 5, 10, 25, 50, 100, 200):
        leg = 2 * D * 1.5 / nm.C_FIBRE_KM_PER_MS
        rend = rng.gamma(100, 4.3 / 100, (trials, n_samples)) + rng.gamma(100, 1.5 / 100, (trials, n_samples))
        jitter = rng.exponential(0.05, (trials, n_samples))
        ex = (rend + jitter + leg).min(axis=1)
        floor = np.quantile((rng.gamma(100, 4.3 / 100, (trials, n_samples))
                             + rng.gamma(100, 1.5 / 100, (trials, n_samples))).min(axis=1), 0.999)
        out[D] = dict(added_rtt_ms=round(leg, 3),
                      detected=float(np.mean(ex > floor + guard)),
                      false_alarm_at_0=None)
    out[0]["false_alarm_at_0"] = out[0]["detected"]
    return out


def fake_demand():
    """G4: the economics of Sybil Leafs farming session-minute emission.

    Units are a session minute's fee F = 1. The attacker owns the validator,
    so the fee it pays itself is free unless a share b of it burns.
    """
    rows = []
    device_cost_min = 400.0 / (2 * 365 * 600)   # a 400-fee-unit device, 2 years, 600 min a day
    for E in (0.5, 1.0, 2.0):                    # emission per minute, in fees
        for b in (0.0, 0.5, 1.0):                # burned share of the fee
            for cap in (600, 120):               # eligible minutes per device per day
                profit_min = E - b * 1.0 - device_cost_min * 600 / cap
                rows.append(dict(emission=E, burn=b, cap_min_day=cap,
                                 profit_per_min=round(profit_min, 3),
                                 profitable=profit_min > 0))
    rule = "emission per minute <= burned fee per minute, so self-dealing never profits"
    return dict(rows=rows, rule=rule)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    rng = np.random.default_rng(2026)
    cities, pop, H = make_region(rng)
    trials = 60 if a.quick else 600
    spoof = spoof_grid(rng, H, cities, pop, trials)
    frame = frame_grid(rng, H, trials)
    out = dict(params=dict(K=K, R_REJ=R_REJ, CELL_KM=CELL_KM, TAU=TAU, DELTA_MS=DELTA_MS, SIGMA_CAL=SIGMA_CAL,
                           R_SEL_KM=R_SEL_KM, N_HONEST=N_HONEST, trials=trials),
               spoof_success=spoof, honest_false_fail=frame,
               bonus_capture=bonus_capture(rng, H, cities, pop, max(20, trials // 10)),
               tau_sweep=tau_sweep(rng, H, cities, pop, trials),
               sigma_sweep=sigma_sweep(rng, H, cities, pop, trials),
               relay_hotspot=relay_detect(rng),
               fake_demand=fake_demand())
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "pol.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    for rule in RULES:
        print(rule, "spoof success, rows f, cols D=10..400 km")
        for f in (0.0, 0.1, 0.2, 0.33, 0.5):
            print("  f=%.2f " % f + " ".join("%.3f" % spoof[f"{rule}|f={f}|D={D}"]
                                           for D in (10, 25, 50, 100, 200, 400)))
        print("  framing (urban, rural):", [(f, frame[f"{rule}|f={f}|urban"], frame[f"{rule}|f={f}|rural"])
                                          for f in (0.0, 0.1, 0.2, 0.33, 0.5)])
    print("bonus capture", out["bonus_capture"])
    print("tau sweep", out["tau_sweep"])
    print("sigma sweep", out["sigma_sweep"])
    print("relay", {k: v["detected"] for k, v in out["relay_hotspot"].items()})
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 4, figsize=(14, 3.5), sharey=True)
        Ds = (10, 25, 50, 100, 200, 400)
        for ax, rule in zip(axs, RULES):
            for f in (0.0, 0.1, 0.2, 0.33, 0.5):
                ax.plot(Ds, [spoof[f"{rule}|f={f}|D={D}"] for D in Ds], marker="o", label=f"f={f}")
            ax.set_xscale("log")
            ax.set_title(rule)
            ax.set_xlabel("spoof distance D, km")
        axs[0].set_ylabel("claim passes")
        axs[0].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(RES, "pol_spoof.png"), dpi=120)
    except Exception as e:
        print("plot skipped:", e)


if __name__ == "__main__":
    main()
