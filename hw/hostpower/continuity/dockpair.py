#!/usr/bin/env python3
"""dockpair.py - the dock validator pair: power and compute in one box.

Continuity team of hw/hostpower, L.6.1 (proposed). Gate HST-6.

When the dock holds both the power host and the validator (hw/dock), one box
is the failure domain of two jobs. This file counts what each failure costs the
Leaf in each energy tier, and asks if the pair helps or hurts the Host Life Law.

The failure cases
  F1  the box dies: power and compute together (PSU, mains loss on a flat pack)
  F2  the link dies: the dock uplink is down, power and compute live
  F3  power dies and the link lives: the contact or the Qi path fails
  F4  compute dies and power lives: the validator crashes
  F5  thermal overload: the dock sheds load by its priority list
  F6  a hostile pair: it cuts power at a chosen instant and serves old state

Read only: powersm (tiers), handover_sim (the delay draws), proto/model/handover
(the shadow gap), hw/dock/params (the box loads and the pack), net/discovery
results (the crash and brownout rates of the validator fleet).

Run: python3 dockpair.py      writes out/dockpair.md and out/dockpair.json
"""
import importlib.util
import json
import math
import os
import random
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import powersm as P  # noqa: E402
import handover_sim as H  # noqa: E402
import handover as proto_handover  # noqa: E402  proto/model/handover.py


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DOCK = _load("dock_params_ro", os.path.join(ROOT, "hw", "dock", "params.py"))
FLEET = json.load(open(os.path.join(ROOT, "net", "discovery", "results", "handover.json")))["params"]
OUT = os.path.join(HERE, "out")
FRAME_MS = 1000.0 / 240.0

# ---------------------------------------------------------- the box power ---
def box_w(with_validator):
    typ = sum(v[1] for v in DOCK.LOADS.values())
    if with_validator:
        typ += sum(v[1] for v in DOCK.VALIDATOR.values())
        typ += 10.0        # the FPGA frame engine of hw/dock/validator_sizing.py [HYPOTHESIS]
    return typ


PACK_WH = 2 * DOCK.CELL_V_NOM * DOCK.CELL_AH * DOCK.PACK_USABLE * 1.0   # 2S1P, usable


def pack_minutes(with_validator, leaf_w=0.0):
    return PACK_WH / (box_w(with_validator) + leaf_w) * 60.0


# -------------------------------------------------- failure-rate assumptions ---
RATES = {
    "mains_outage_per_h": 1 / 2000.0,   # a mains outage that outlasts the pack [HYPOTHESIS]
    "psu_per_h": 1 / 100000.0,          # the dock supply or its buck fails     [HYPOTHESIS]
    "thermal_per_h": 1 / 20000.0,       # a thermal trip of the whole box       [HYPOTHESIS]
    "validator_crash_per_h": FLEET["crash_per_h"],      # net/discovery stress fleet
    "validator_down_s": FLEET["crash_down_s"],
    "validator_brownout_per_h": FLEET["brownout_per_h"],
}


def joint_rates():
    r = RATES
    box = r["mains_outage_per_h"] + r["psu_per_h"] + r["thermal_per_h"]
    # split design: power host and validator are two boxes in two power domains.
    # A joint loss needs a power failure and a validator crash inside one outage.
    window_h = r["validator_down_s"] / 3600.0
    split = box * (r["validator_crash_per_h"] * window_h)
    return dict(pair=box, split=split, ratio=box / split)


# ------------------------------------------------------------- the draws ---
def failover_frames(r, warm, rtt_ms):
    """Frames the Leaf covers (WARM) or loses (HOT) when the primary goes silent."""
    if not warm:
        return 0
    return proto_handover.unplanned_gap_frames(rtt_ms)


def cold_validator_start_ms(r, link):
    """A cold session on a new validator, on the store: discover, hello, sync, intra frame."""
    rtt = H.rtt_ms(r, link)
    first = H.A["render_ms"] + H.A["encode_first_ms"] + 15 * H.A["encode_slice_ms"] + H.A["decode_ms"]
    discover = 2 * rtt + 20.0          # an anycast bootstrap and one probe burst [HYPOTHESIS]
    return discover + 1.5 * rtt + H.A["se_check_ms"] + H.A["sync_ms"] + rtt + first + 4.2


def run_failover(n=20000, seed=3):
    r = random.Random(seed)
    out = {"warm": [], "hot": [], "cold_ms": []}
    for _ in range(n):
        rtt = H.rtt_ms(r, "cell")
        out["warm"].append(failover_frames(r, True, rtt))
        out["hot"].append(0)
        out["cold_ms"].append(cold_validator_start_ms(r, "cell"))
    return out


def pct(xs, p):
    return H.pct(xs, p)


# ---------------------------------------------------------- the case table ---
def cases():
    """One row per failure case. The three tier columns hold what differs by tier."""
    fo = run_failover()
    warm50, warm99 = pct(fo["warm"], 50), pct(fo["warm"], 99)
    cold50, cold99 = pct(fo["cold_ms"], 50), pct(fo["cold_ms"], 99)
    tiers = (P.BARE, P.BUFFER, P.FULL)
    tt = {t.name: P.tier_times(t) for t in tiers}

    def per_tier(fn):
        return [fn(tt[t.name]) for t in tiers]

    live = per_tier(lambda x: f"live {_fmt(x['live_s'])}, hold {_fmt(x['hold_s'])}")
    fits = all(cold99 / 1000.0 < tt[t.name]["live_s"] for t in tiers)
    rows = [
        dict(case="F1 box dies, a shadow in another power domain",
             frames=f"{warm50:.0f} to {warm99:.0f} covered by U1",
             tiers=live, state="none finalized, at most the in-flight inputs",
             verdict="holds while a host arrives in time"),
        dict(case="F1 box dies, no shadow",
             frames=f"cold start {cold50:.0f} ms p50, {cold99:.0f} ms p99",
             tiers=live, state="none finalized, at most the in-flight inputs",
             verdict="holds, the cold start fits in every live time" if fits else "FAILS in a tier"),
        dict(case="F2 uplink dies, the Leaf has its own 5G",
             frames="0, the Leaf dual-sends over its own radio",
             tiers=["live"] * 3, state="none", verdict="holds"),
        dict(case="F2 uplink dies, the Leaf has no other path",
             frames="0 seen, the session is local only",
             tiers=["live, unfinalized"] * 3,
             state="all inputs since the last finality if the box then dies, up to 7 s",
             verdict="LOSS: stated as LOCAL on the class line"),
        dict(case="F3 power path dies, link lives",
             frames="0, the same validator keeps serving",
             tiers=per_tier(lambda x: f"live {_fmt(x['live_s'])}, hold {_fmt(x['hold_s'])}, then a pause to the same box"),
             state="none", verdict="holds"),
        dict(case="F4 validator dies, power lives",
             frames=f"{warm50:.0f} to {warm99:.0f} covered by U1 from WARM, 0 from HOT",
             tiers=["live on the host, no store used"] * 3, state="none", verdict="holds"),
        dict(case="F5 thermal overload",
             frames="as F4: the dock sheds the validator before the Leaf charge",
             tiers=["live on the host"] * 3, state="none",
             verdict="holds by the priority list of hw/dock"),
        dict(case="F6 a hostile pair cuts power, then serves old state",
             frames="the Leaf resumes only a root that matches the chain",
             tiers=["pause, then a refused resume"] * 3, state="none, the resume is refused",
             verdict="holds by RG-19 rules 4 and 5"),
    ]
    return rows, dict(warm50=warm50, warm99=warm99, cold50=cold50, cold99=cold99)


def _fmt(s):
    return H.fmt_gap(s) if s > 0 else "0 s"


def main():
    os.makedirs(OUT, exist_ok=True)
    rows, fo = cases()
    jr = joint_rates()
    L = []
    p = L.append
    p("# The dock validator pair (generated by dockpair.py)\n")
    p("## The box and its pack\n")
    p("| item | value |")
    p("|---|---|")
    p(f"| a dock with no validator, typical draw | {box_w(False):.1f} W |")
    p(f"| a dock with the validator and the frame engine, typical draw | {box_w(True):.1f} W |")
    p(f"| usable pack energy | {PACK_WH:.1f} Wh |")
    p(f"| a mains outage, plain dock, no Leaf charge | {pack_minutes(False):.0f} min |")
    p(f"| a mains outage, dock with the validator | {pack_minutes(True):.0f} min |")
    p(f"| the same, with the Leaf at the 2.24 W session | {pack_minutes(True, 2.24):.0f} min |")
    p("\n## The joint loss of power and primary validator, events per hour\n")
    p("| design | rate | meaning |")
    p("|---|---|---|")
    p(f"| the pair, one box | {jr['pair']:.2e} | one box event takes both |")
    p(f"| a split design, two power domains | {jr['split']:.2e} | a power loss inside a validator outage |")
    p(f"| ratio | {jr['ratio']:.0f} | the pair makes the joint loss this many times more frequent |")
    p("\nThe rates are `[HYPOTHESIS]` except the validator crash and outage figures, which come from "
      "`net/discovery`.\n")
    p("\n## The cases, by tier\n")
    p("| case | frames at the face | Bare | Buffer | Full | state lost | verdict |")
    p("|---|---|---|---|---|---|---|")
    for r in rows:
        p(f"| {r['case']} | {r['frames']} | {r['tiers'][0]} | {r['tiers'][1]} | {r['tiers'][2]} | "
          f"{r['state']} | {r['verdict']} |")
    p("\n## The shadow takeover\n")
    p(f"The unplanned gap from WARM is `{fo['warm50']:.0f}` frames at p50 and `{fo['warm99']:.0f}` at p99. "
      f"A cold start on a new validator takes `{fo['cold50']:.0f} ms` at p50 and `{fo['cold99']:.0f} ms` at p99.")
    open(os.path.join(OUT, "dockpair.md"), "w").write("\n".join(L) + "\n")
    json.dump(dict(rows=rows, joint=jr, failover=fo, rates=RATES, pack_wh=PACK_WH,
                   box_w_plain=box_w(False), box_w_validator=box_w(True)),
              open(os.path.join(OUT, "dockpair.json"), "w"), indent=1)
    print("\n".join(L))


if __name__ == "__main__":
    main()
