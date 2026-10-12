#!/usr/bin/env python3
"""sim_privacy.py: can colluding validators link the probes of a Leaf to its wallet?

FINAL/21 Section 21.5.4. Gate SW-24 (probes) and the privacy rules of
SPEC.md Section 7.

The serving validator (P) and the shadow (S) learn the wallet of a session.
That is inherent: the session is the wallet's chain state. The question is
what the probes add. The other 2 to 3 candidates of the probe set see probes
only. A probe is linked when the adversary can map the identifier it sees
to a wallet it learned in some session that a colluding P or S served.

The adversary
  * a share f of the validators, chosen at random, colluding and logging;
  * it links retroactively inside the lifetime of an identifier.

The identifiers a probe can carry
  * a device or wallet field, or a QUIC resumption ticket (variant V0 only);
  * a clock field: the Leaf clock in PathProbe.t_send_us. A clock offset is
    a stable device fingerprint [PUBLICATION] Kohno, Broido, Claffy, "Remote
    physical device fingerprinting", IEEE S&P 2005;
  * the network address: a 5G IPv6 /64 prefix per PDU session, a home Wi-Fi
    public address per household, a venue address shared by several Leafs.

The variants
  V0  naive: a stable device field in every probe;
  V1  fresh QUIC keys and connection IDs per session, no tickets, no device
      field, but the clock field stays and the 5G prefix lives for a day;
  V2  V1 with no clock field (the Leaf matches the probe_id itself);
  V3  V2 plus a fresh 5G prefix per Leaf session (a new PDU session);
  V4  V3 plus the room validator at home (L0), so home probes stay in the room.

Output: results/privacy.json.
    python3 sim_privacy.py
"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

N_USERS = 20000
N_VAL = 24
N_CAND = 5             # P, S and 3 probe-only candidates
SESS_PER_DAY = 6       # [HYPOTHESIS]
P_5G = 0.55
P_HOME = 0.30          # the rest is venue Wi-Fi
VENUE_SET = 6          # mean Leafs behind one venue address [HYPOTHESIS]
HOUSEHOLD = 1.3        # mean Leafs per household [HYPOTHESIS]


def simulate(variant, f, seed=11):
    r = random.Random(seed)
    colluders = set(r.sample(range(N_VAL), max(1, round(f * N_VAL))))
    # identifiers
    home_of = {}
    hh = 0
    u = 0
    while u < N_USERS:
        size = 1 + (1 if r.random() < HOUSEHOLD - 1 else 0)
        for _ in range(size):
            if u < N_USERS:
                home_of[u] = hh
                u += 1
        hh += 1
    sessions = []          # (user, ident, cands, P, S, at_home)
    for u in range(N_USERS):
        day_prefix = ("5g", u, 0)
        for k in range(SESS_PER_DAY):
            x = r.random()
            if x < P_5G:
                ident = ("5g", u, k) if variant in ("V3", "V4") else day_prefix
                home = False
            elif x < P_5G + P_HOME:
                ident = ("home", home_of[u])
                home = True
            else:
                ident = ("venue", r.randrange(N_USERS // VENUE_SET))
                home = False
            cands = r.sample(range(N_VAL), N_CAND)
            sessions.append((u, ident, cands, cands[0], cands[1], home))
    # what the adversary learns: identifier -> wallets, from P or S sessions
    learned = {}
    device_known = set()
    for (u, ident, cands, P, S, home) in sessions:
        if P in colluders or S in colluders:
            learned.setdefault(ident, set()).add(u)
            device_known.add(u)
    # members of each identifier (the anonymity set the adversary faces)
    members = {}
    for (u, ident, *_rest) in sessions:
        members.setdefault(ident, set()).add(u)
    probes_seen = linked = 0
    exposed_sessions = baseline_sessions = 0
    for (u, ident, cands, P, S, home) in sessions:
        served = P in colluders or S in colluders
        baseline_sessions += served
        if variant == "V4" and home:
            # the room validator serves at home, the Leaf sends no metro probes
            exposed_sessions += served
            continue
        probe_only = [c for c in cands[2:] if c in colluders]
        if not probe_only:
            exposed_sessions += served
            continue
        probes_seen += 1
        if variant == "V0":
            ok = u in device_known
        elif variant == "V1":
            ok = u in device_known          # the clock offset is a device fingerprint
        else:
            ok = u in learned.get(ident, ()) and len(members[ident]) == 1
        linked += ok
        exposed_sessions += served or ok
    n = len(sessions)
    return dict(probe_sessions_seen=probes_seen,
                linked_share=round(linked / max(1, probes_seen), 4),
                exposure=round(exposed_sessions / n, 4),
                baseline=round(baseline_sessions / n, 4),
                added_by_probes=round((exposed_sessions - baseline_sessions) / n, 4))


def main():
    out = {}
    for f in (0.05, 0.10, 0.20, 0.33):
        for v in ("V0", "V1", "V2", "V3", "V4"):
            out[f"f={f}|{v}"] = simulate(v, f)
            print(f, v, out[f"f={f}|{v}"])
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "privacy.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
