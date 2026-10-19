#!/usr/bin/env python3
"""handover_sim.py - host A to host B: the time to first pixel, the time to
a full session and the frames lost, for the three energy tiers.

Continuity team of hw/hostpower, L.6.1 (proposed). Gates HST-1, HST-2, HST-3.

What it composes (all read only, by import or by file):
  powersm.py               the tiers, the phase times, the bootsm boot times
  fw/boot/bootsm.py        the boot path of a dead Leaf (through powersm)
  net/discovery/netmodel   the air and wired delays of FINAL/21 Section 21.5.7
  net/discovery/results    the zero-frame share of the validator handover
  proto/model/handover.py  the lead and the gap of the shadow handover

The model of one handover
  Phase A, before host B: the tier decides what the Leaf is at host B.
    LIVE    the gap is shorter than the live ride-through of the store.
            The face never goes dark. The session never stops.
    HOLD    the body store is empty, the B cell holds the radios at 0.40 W.
            The face is dark. The frame store and the link live. Bare reaches
            this phase for about 16 minutes.
    RESUME  the store is at its floor. A SessionPause is on record, or, with
            no link at that moment, the validator pauses by lapse. The Leaf
            at host B boots from the chain record.
  Phase B, after host B: the host handshake, then the path that the phase gave.

Honest limits. Every stage time is [HYPOTHESIS] except the FINAL/21 budget
rows that netmodel reproduces. DST-11 and DST-12 measure the real values.

Run: python3 handover_sim.py            writes out/handover.md and out/handover.json
"""
import json
import math
import os
import random
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "net", "discovery"))
sys.path.insert(0, os.path.join(ROOT, "proto", "model"))
import powersm as P  # noqa: E402
import netmodel as nm  # noqa: E402
import handover as proto_handover  # noqa: E402  proto/model/handover.py

OUT = os.path.join(HERE, "out")
FRAME_MS = 1000.0 / 240.0

# ------------------------------------------------ the assumptions, tagged ---
A = {
    "pad_close_ms": 12.0,      # the seat quadrant closes at 12 ms          [TREE] STATE-MACHINE 5
    "rail_ms": 5.0,            # tile rails ramp after a pad closes          [TREE] bootsm
    "u7_sign_ms": 8.0,         # one ML-DSA-44 session-key signature in U7   [HYPOTHESIS]
    "verify_pause_ms": 15.0,   # the validator checks a finality proof        [HYPOTHESIS]
    "sync_ms": 60.0,           # a validator takes a session state            [TREE] net/discovery
    "se_check_ms": 20.0,       # U7 checks a new validator key                [TREE] net/discovery
    "render_ms": 4.3,          # execute and render                           [DECISION] FINAL/21
    "encode_first_ms": 1.5,    # first-slice encode                           [DECISION] FINAL/21
    "encode_slice_ms": 0.35,   # each further intra slice, 16 slices          [HYPOTHESIS]
    "decode_ms": 1.5,          # first-slice decode                           [DECISION] FINAL/21
    "intra_bpp": 0.4,          # a full intra frame of a UI page              [HYPOTHESIS]
    "px": 1600 * 3200,
    "aon_ramp_ms": 3.0,        # host AON feed starts U4 on a dead Leaf       [HYPOTHESIS]
    "shadow_cache_s": 60.0,    # a validator keeps a session state hot        [HYPOTHESIS]
    "grant_term_s": 86400.0,   # the session grant term                       [HYPOTHESIS]
    "anchor_window_s": 14 * 86400.0,  # weak-subjectivity window              [GENERAL] unknown for Budlum
    "detect_lapse_s": 1.0,     # the validator pauses by lapse after 1 s      [HYPOTHESIS]
    "p_pre_warm": 0.90,        # shadow ready at host B when radios were alive [HYPOTHESIS]
}
HOST_AUTH_MS = {"dock": 20.0, "qi": 250.0, "pd": 350.0}   # trust team owns the true values [HYPOTHESIS]


class Scen:
    def __init__(self, name, short, gap_s, host_b, val_b, link_b, dl_mbps,
                 cached_state, p_link_ok):
        self.name, self.short, self.gap_s = name, short, gap_s
        self.host_b, self.val_b, self.link_b = host_b, val_b, link_b
        self.dl_mbps, self.cached_state, self.p_link_ok = dl_mbps, cached_state, p_link_ok


SCENARIOS = [
    # The walk: 100 m at 1.4 m/s is 71 s, and a door adds a few seconds.
    Scen("S1 desk dock, a walk, a vehicle", "S1", 75.0, "pd", "cell-site 5G",
         "cell_cold", 150.0, False, 0.90),
    # Lift off the dock, cross the hall, set on a Qi puck. No room validator.
    Scen("S2 dock validator, then a cell-site validator", "S2", 8.0, "qi",
         "cell-site 5G", "cell_cold", 600.0, False, 0.97),
    # Two docks, 40 cm apart. The same room, the same LAN.
    Scen("S3 two docks side by side", "S3", 1.5, "dock", "room Wi-Fi",
         "wifi", 2000.0, True, 0.99),
]

# the zero-frame handover stats of net/discovery, policy C and policy A
_h = json.load(open(os.path.join(ROOT, "net", "discovery", "results", "handover.json")))
_s = _h["scenarios"]["stress"]["policies"]
P_PLANNED = _s["C"]["zero_loss_handover_share"]
FAILOVER_FRAMES_C = _s["C"]["frames_lost_per_failover"]
FAILOVER_FRAMES_A = _s["A"]["frames_lost_per_failover"]


# ----------------------------------------------------------- the draws ---
def rtt_ms(r, link):
    """Round trip Leaf to validator. Same stage models as FINAL/21 Section 21.5.7."""
    if link == "wifi":
        wired = nm.wired_ow_ms(0.0, 0.0, hops=2)
        up, dn = nm.air_up_ms(r, nm.WIFI), nm.air_dl_ms(r, nm.WIFI)
    else:
        wired = nm.wired_ow_ms(0.0, 3.0, hops=2, fixed=nm.UPF_MS)
        up, dn = nm.air_up_ms(r, nm.CELL), nm.air_dl_ms(r, nm.CELL)
    return up + dn + 2 * wired + nm.queue_ms(r, 0.03) + nm.queue_ms(r, 0.03)


def host_auth_ms(r, host):
    return HOST_AUTH_MS[host] * math.exp(r.gauss(0.0, 0.25))


def intra_tx_ms(sc):
    bits = A["px"] * A["intra_bpp"]
    return bits / (sc.dl_mbps * 1e6) * 1000.0


def first_live_frame_ms(r, sc, rtt):
    """From the moment the validator starts, to a decoded intra frame on the Leaf."""
    enc = A["encode_first_ms"] + 15 * A["encode_slice_ms"]
    return A["render_ms"] + enc + intra_tx_ms(sc) + A["decode_ms"]


def scan_ms(r):
    return r.uniform(0.0, FRAME_MS) + 0.317


# --------------------------------------------------------- one timeline ---
def phase_a(tier, sc, gap_s, h_ms):
    """What the Leaf is at host B. The handshake time counts as gap."""
    tt = P.tier_times(tier)
    g = gap_s + h_ms / 1000.0
    if g <= tt["live_s"]:
        return "LIVE", tt
    if tier.bcell and g <= tt["bridge_s"]:
        return "HOLD", tt
    return "RESUME", tt


def timeline(tier, sc, gap_s, r, boot_cache):
    tt = P.tier_times(tier)
    H = host_auth_ms(r, sc.host_b)
    rtt = rtt_ms(r, "wifi" if sc.link_b == "wifi" else "cell")
    phase, tt = phase_a(tier, sc, gap_s, H)
    face_dark_a_s = max(0.0, gap_s - tt["live_s"]) if phase != "LIVE" else 0.0
    res = dict(phase=phase, outcome=phase, H=H, rtt=rtt,
               dark_before_s=face_dark_a_s, unseen_ticks=0, inflight_lost=0,
               note="")
    if phase == "LIVE":
        planned = r.random() < P_PLANNED
        res.update(t_pixel=0.0, t_live=0.0, t_full=0.0,
                   frames_lost=0.0 if planned else FAILOVER_FRAMES_C)
        res["note"] = "shadow at host B was warm" if planned else "unplanned cut to the shadow"
        return res
    first = first_live_frame_ms(r, sc, rtt)
    if phase == "HOLD":
        warm = r.random() < A["p_pre_warm"]
        t_pixel = H + A["pad_close_ms"] + A["rail_ms"] + scan_ms(r)
        t_stream = rtt + first + (0.0 if warm else A["se_check_ms"] + A["sync_ms"] + rtt)
        t_live = max(t_stream, H + A["pad_close_ms"] + A["rail_ms"]) + scan_ms(r)
        t_full = t_live + (0.0 if warm else A["sync_ms"] + 2 * rtt)
        res.update(t_pixel=t_pixel, t_live=t_live, t_full=t_full,
                   frames_lost=max(0, math.ceil((t_live - t_pixel) / FRAME_MS)))
        res["note"] = "the frame store showed the last frame until the first live slice"
        return res
    # RESUME: the Leaf boots from the chain record
    link_ok = r.random() < sc.p_link_ok
    cold_dark = gap_s > tt["bridge_s"] + tt["suspended_max_s"]
    bt = boot_cache[sc.link_b]
    wake = H + (A["aon_ramp_ms"] if (cold_dark or not tier.bcell) else 0.0)
    t_pixel = wake + bt["t_safe"]
    t_rear = (A["aon_ramp_ms"] if (cold_dark or not tier.bcell) else 0.0) + bt["t_rear"]
    t_offer = wake + bt["t_session"]
    sync = 0.0 if (sc.cached_state and gap_s <= A["shadow_cache_s"]) else A["sync_ms"]
    verify = A["verify_pause_ms"] * (1.0 if link_ok else 1.8)
    t_live = (t_offer + A["u7_sign_ms"] + rtt / 2 + verify + sync + first
              + rtt / 2 + scan_ms(r))
    t_full = t_live + A["sync_ms"] + 2 * rtt
    # the in-flight input at the instant of power loss: one batch per 2.08 ms
    inflight = math.ceil(480.0 * (rtt / 2) / 1000.0)
    res.update(t_pixel=t_pixel, t_live=t_live, t_full=t_full, t_rear=t_rear,
               t_offer=t_offer,
               frames_lost=max(0, math.ceil((t_live - t_pixel) / FRAME_MS)),
               inflight_lost=inflight)
    # long gaps end in a stated refusal, never a silent loss
    if gap_s > A["anchor_window_s"]:
        res["outcome"] = "STATED_ANCHOR"
        res["note"] = "the anchor is older than the window: re-anchor by a second channel"
    elif gap_s > A["grant_term_s"]:
        res["outcome"] = "STATED_GRANT"
        res["note"] = "the grant expired: one wallet action, the state is intact"
    elif not link_ok:
        res["outcome"] = "RESUME_LAPSE"
        res["unseen_ticks"] = int(A["detect_lapse_s"] * 240)
        res["note"] = "no link at the pause: the validator paused by lapse"
    else:
        res["outcome"] = "RESUME_CLEAN"
        res["note"] = "SessionPause on record"
    return res


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    return xs[min(len(xs) - 1, max(0, int(round(p / 100.0 * (len(xs) - 1)))))]


def run_cell(tier, sc, gap_s, n=3000, seed=11):
    r = random.Random(seed * 1009 + int(gap_s * 10) + len(tier.name))
    boot_cache = {k: P.boot_times(k if k != "wifi" else "wifi") for k in ("wifi", "cell_cold", "cell_warm")}
    rows = [timeline(tier, sc, gap_s, r, boot_cache) for _ in range(n)]
    outcomes = {}
    for x in rows:
        outcomes[x["outcome"]] = outcomes.get(x["outcome"], 0) + 1
    main = max(outcomes, key=outcomes.get)
    sel = [x for x in rows if x["outcome"] == main]
    return dict(
        tier=tier.name, scenario=sc.short, gap_s=gap_s, n=n, outcome=main,
        share={k: v / n for k, v in outcomes.items()},
        dark_before_s=sel[0]["dark_before_s"],
        t_pixel_p50=pct([x["t_pixel"] for x in sel], 50),
        t_pixel_p99=pct([x["t_pixel"] for x in sel], 99),
        t_live_p50=pct([x["t_live"] for x in sel], 50),
        t_live_p99=pct([x["t_live"] for x in sel], 99),
        t_full_p50=pct([x["t_full"] for x in sel], 50),
        t_full_p99=pct([x["t_full"] for x in sel], 99),
        frames_p50=pct([x["frames_lost"] for x in sel], 50),
        frames_p99=pct([x["frames_lost"] for x in sel], 99),
        frames_mean=sum(x["frames_lost"] for x in rows) / n,
        t_rear_p50=pct([x.get("t_rear", float("nan")) for x in sel if "t_rear" in x], 50),
        t_offer_p50=pct([x.get("t_offer", float("nan")) for x in sel if "t_offer" in x], 50),
        inflight=max(x["inflight_lost"] for x in rows),
        unseen=max(x["unseen_ticks"] for x in rows),
    )


# --------------------------------------------------------------- tables ---
GAPS = [0.05, 0.3, 0.57, 1.5, 3.0, 8.0, 75.0, 300.0, 900.0, 1800.0, 3600.0,
        7200.0, 21600.0, 86400.0, 2 * 86400.0, 30 * 86400.0]


def fmt_t(ms):
    if ms != ms:
        return "n/a"
    if ms < 1000:
        return f"{ms:.0f} ms"
    return f"{ms/1000:.2f} s"


def fmt_gap(s):
    if s < 60:
        return f"{s:.3g} s"
    if s < 3600:
        return f"{s/60:.3g} min"
    if s < 86400:
        return f"{s/3600:.3g} h"
    return f"{s/86400:.3g} d"


def cond4_rows():
    """BRIEF Section 5, condition 4: E_buffer >= P_peak x t_handover."""
    rows = []
    for t in (P.BARE, P.BUFFER_LO, P.BUFFER, P.BUFFER_HI, P.FULL):
        e = t.body_j
        pr = P.bridge_profile(t)
        rows.append(dict(tier=t.name, e_j=e,
                         t_peak_s=e / P.W["peak"], t_live_s=e / P.W["live"],
                         t_policy_s=pr["live_s"], b_hold_s=pr["hold_s"],
                         t_bridge_s=pr["bridge_s"]))
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    tiers = [P.BARE0, P.BARE_S, P.BARE, P.BUFFER, P.FULL]
    results = {"scenarios": [], "sweep": [], "cond4": cond4_rows(),
               "assumptions": A, "p_planned": P_PLANNED,
               "failover_frames_C": FAILOVER_FRAMES_C,
               "failover_frames_A": FAILOVER_FRAMES_A}
    L = []
    p = L.append
    p("# Host A to host B timelines (generated by handover_sim.py)\n")
    p("Each cell is `3 000` draws. A time runs from the moment host B touches the Leaf. "
      "Frames lost counts `240 Hz` scan-outs that show the stored or safe frame and not a live frame.\n")
    for sc in SCENARIOS:
        p(f"\n## {sc.name}: gap {fmt_gap(sc.gap_s)}, host {sc.host_b}, validator {sc.val_b}\n")
        p("| tier | outcome at host B | face dark before B | first pixel p50 | live frame p50 | live frame p99 | full session p50 | frames lost p50 | frames lost p99 |")
        p("|---|---|---|---|---|---|---|---|---|")
        for t in tiers:
            c = run_cell(t, sc, sc.gap_s)
            results["scenarios"].append(c)
            p(f"| {t.name} | {c['outcome']} | {fmt_gap(c['dark_before_s']) if c['dark_before_s'] else '0 s'} | "
              f"{fmt_t(c['t_pixel_p50'])} | {fmt_t(c['t_live_p50'])} | {fmt_t(c['t_live_p99'])} | "
              f"{fmt_t(c['t_full_p50'])} | {c['frames_p50']:.0f} | {c['frames_p99']:.0f} |")
    p("\n## The gap sweep, scenario S1 (vehicle, 5G cell-site)\n")
    p("| gap | " + " | ".join(t.name for t in tiers) + " |")
    p("|---|" + "---|" * len(tiers))
    sc1 = SCENARIOS[0]
    for g in GAPS:
        cells = []
        for t in tiers:
            c = run_cell(t, sc1, g, n=1200)
            results["sweep"].append(c)
            cells.append(f"{c['outcome']}, live {fmt_t(c['t_live_p50'])}, {c['frames_p50']:.0f} fr")
        p(f"| {fmt_gap(g)} | " + " | ".join(cells) + " |")
    p("\n## The restart from the chain record, by link (Bare-0, a forced resume)\n")
    p("The boot path is bootsm.py. The live frame adds the resume exchange of RG-19.\n")
    p("| link | rear glance | safe screen | session offered | live frame p50 | live frame p99 | full session p50 | frames not live |")
    p("|---|---|---|---|---|---|---|---|")
    cold = [
        ("Wi-Fi, a known dock", Scen("c1", "C1", 3600.0, "dock", "room", "wifi", 2000.0, False, 1.0)),
        ("5G, modem attached in idle", Scen("c2", "C2", 3600.0, "qi", "cell", "cell_warm", 600.0, False, 1.0)),
        ("5G, modem cold (the default)", Scen("c3", "C3", 3600.0, "qi", "cell", "cell_cold", 600.0, False, 1.0)),
        ("5G loaded cell, modem cold", Scen("c4", "C4", 3600.0, "pd", "cell", "cell_cold", 150.0, False, 1.0)),
    ]
    results["cold"] = []
    for name, sc in cold:
        c = run_cell(P.BARE0, sc, sc.gap_s, n=2000)
        results["cold"].append(dict(c, link=name))
        p(f"| {name} | {fmt_t(c['t_rear_p50'])} | {fmt_t(c['t_pixel_p50'])} | {fmt_t(c['t_offer_p50'])} | "
          f"{fmt_t(c['t_live_p50'])} | {fmt_t(c['t_live_p99'])} | {fmt_t(c['t_full_p50'])} | {c['frames_p50']:.0f} |")
    pw = P.W
    p(f"\nThe price of an attached modem in SUSPENDED: the draw rises from {pw['suspended']*1000:.0f} mW to "
      f"{pw['suspended_warm']*1000:.0f} mW. The guaranteed SUSPENDED life falls from "
      f"{(P.B_FLOOR_J-P.E_PAUSE_J)/pw['suspended']/60:.0f} to {(P.B_FLOOR_J-P.E_PAUSE_J)/pw['suspended_warm']/60:.0f} min.")
    p("\n## Condition 4 of the BRIEF, `E_buffer >= P_peak x t_handover`\n")
    p("The body store only. The B cell never carries a peak.\n")
    p("| tier | body store | longest gap at 8.7 W | longest gap at the 2.24 W session | face lit under the policy | B cell hold after that | all the way to the pause |")
    p("|---|---|---|---|---|---|---|")
    for x in results["cond4"]:
        p(f"| {x['tier']} | {x['e_j']:.0f} J | {fmt_gap(x['t_peak_s'])} | {fmt_gap(x['t_live_s'])} | "
          f"{fmt_gap(x['t_policy_s'])} | {fmt_gap(x['b_hold_s']) if x['b_hold_s'] else 'none'} | "
          f"{fmt_gap(x['t_bridge_s'])} |")
    open(os.path.join(OUT, "handover.md"), "w").write("\n".join(L) + "\n")
    json.dump(results, open(os.path.join(OUT, "handover.json"), "w"), indent=1)
    print("\n".join(L))


if __name__ == "__main__":
    main()
