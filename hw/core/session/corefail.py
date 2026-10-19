#!/usr/bin/env python3
"""corefail.py - the Core as a single point, and the Skin on a link loss.

Session seat of hw/core, block HP-2.

Part A. One Core serves N Skins. What does each failure cost, and how does the
joint failure of N Skins on one Core compare with N Leafs, a Core in each?
Part B. A Skin has no frame store. What does it show on a link loss, and how long
does it take to come back?

Read only: hw/hostpower/continuity (powersm, handover_sim), proto/model/handover.py
(through dockpair), net/discovery results (the validator crash rates), and
roam_sim.py of this directory. Every rate is [HYPOTHESIS] except the validator
crash and outage figures of net/discovery.

Run: python3 corefail.py      writes out/corefail.md and out/corefail.json
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
sys.path.insert(0, os.path.join(ROOT, "hw", "hostpower", "continuity"))
import powersm as P  # noqa: E402
import handover_sim as H  # noqa: E402
import handover as proto_handover  # noqa: E402  proto/model/handover.py
import roam_sim as R  # noqa: E402
import skinsession as K  # noqa: E402

OUT = os.path.join(HERE, "out")
FLEET = json.load(open(os.path.join(ROOT, "net", "discovery", "results", "handover.json")))["params"]
HOURS_YEAR = 8760.0

# ------------------------------------------------------------------ the rates ---
RATES = {
    "core_box": (1 / 20000.0, 600.0),      # per hour, seconds until a screen is back: a new Core
    "skin_panel": (1 / 50000.0, 3600.0),   # a Skin panel fails: swap a Skin
    "cable_link": (1 / 50000.0, 60.0),     # a connector or a cable fails
    "mmwave_link": (2.0, 1.0),             # blockage events per hour and their length
    "host_power": (1 / 100.0, None),       # a host power loss event; the gap is drawn below
    "validator_crash": (FLEET["crash_per_h"], FLEET["crash_down_s"]),
}
P_SHADOW_ABSENT = 0.05                     # no shadow in another power domain      [HYPOTHESIS]


def gap_exceeds(t_s):
    """P(a host power gap lasts longer than t). A short mode and a parked mode."""
    return 0.98 * math.exp(-t_s / 60.0) + 0.02 * math.exp(-t_s / 14400.0)


# ------------------------------------------------- the load of N Skins on a Core ---
ETA_BODY, ETA_B = 0.92, 0.90                 # hw/energy runtime.py                        [TREE]
SKIN_DELTA_W, SKIN_VIDEO_W = 0.80, 1.35      # the surface load, body column                [TREE]
CORE_DELTA = dict(hub=0.70, radio=0.40, auth=0.12)    # the ring column of the delta row   [TREE]


def core_power_w(n, mode="mirror", profile="delta"):
    """Watts at the cells for N Skins on one Core. Mirror shares the decode; extend and split do not."""
    skin = SKIN_DELTA_W if profile == "delta" else SKIN_VIDEO_W
    hub = CORE_DELTA["hub"]
    if mode == "mirror":
        hub = hub + 0.10 * (n - 1)               # one scaler per extra Skin               [HYPOTHESIS]
    else:
        hub = hub * n
    ring = hub + CORE_DELTA["radio"] + CORE_DELTA["auth"]
    return n * skin / ETA_BODY + ring / ETA_B


def core_bridge_s(n, store_wh, mode="mirror"):
    """Seconds the lit session lasts on a store that all N Skins share, then the B cell hold."""
    e = 5.0 + store_wh * 3600.0 * P.USABLE
    hold = P.tier_times(P.BARE)["hold_s"]
    return e / core_power_w(n, mode), hold


# ----------------------------------------------------------- availability ---
BETA = 0.02        # share of Core and Leaf box failures with a common cause: one firmware
                   # fault, one dock, one batch of parts. The beta-factor model.   [HYPOTHESIS]


def u_of(rate_per_h, dur_s):
    """Share of time a component is down, for Poisson failures of fixed length."""
    return 1.0 - math.exp(-rate_per_h * dur_s / 3600.0)


def unavailability(n, design, tether="cable", beta=BETA):
    """Fraction of time. design: 'split' (one Core, N Skins) or 'leafs' (N Leafs)."""
    box, panel = RATES["core_box"], RATES["skin_panel"]
    link = RATES["cable_link"] if tether == "cable" else RATES["mmwave_link"]
    u_box, u_panel, u_link = u_of(*box), u_of(*panel), u_of(*link)
    if design == "split":
        u_skin = 1 - (1 - u_panel) * (1 - u_link)
        all_dark = 1 - (1 - u_box) * (1 - u_skin ** n)
        return dict(core=u_box, skin=u_skin, all_dark=all_dark,
                    mean_dark_screens=n * (1 - (1 - u_box) * (1 - u_skin)),
                    events_per_h=box[0] + n * (panel[0] + link[0]))
    u_ind = u_of(box[0] * (1 - beta), box[1])
    u_cc = u_of(box[0] * beta, box[1])
    u_leaf = 1 - (1 - u_ind) * (1 - u_panel)
    all_dark = 1 - (1 - u_cc) * (1 - u_leaf ** n)
    return dict(core=u_box, skin=u_panel, leaf=u_leaf, all_dark=all_dark,
                mean_dark_screens=n * (1 - (1 - u_box) * (1 - u_panel)),
                events_per_h=n * (box[0] + panel[0]))


def simulate_all_dark(n, design, scale=1.0, hours=2.0e5, seed=3, tether="cable"):
    """Interval simulation that checks the closed form, with the rates times `scale`."""
    r = random.Random(seed)
    box, panel = RATES["core_box"], RATES["skin_panel"]
    link = RATES["cable_link"] if tether == "cable" else RATES["mmwave_link"]

    def intervals(rate, dur_s):
        out, t = [], 0.0
        lam = rate * scale
        while True:
            t += r.expovariate(lam)
            if t > hours:
                return out
            out.append((t, t + dur_s / 3600.0))

    def union(ivs):
        ivs = sorted(ivs)
        out = []
        for a, b in ivs:
            if out and a <= out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], b))
            else:
                out.append((a, b))
        return out

    def intersect(xs, ys):
        out, i, j = [], 0, 0
        while i < len(xs) and j < len(ys):
            a, b = max(xs[i][0], ys[j][0]), min(xs[i][1], ys[j][1])
            if a < b:
                out.append((a, b))
            if xs[i][1] < ys[j][1]:
                i += 1
            else:
                j += 1
        return out

    if design == "split":
        core = union(intervals(*box))
        dark = None
        for _ in range(n):
            sk = union(intervals(*panel) + intervals(*link))
            dark = sk if dark is None else intersect(dark, sk)
        allv = union(core + dark)
    else:
        allv = None
        for _ in range(n):                       # beta = 0 here: the check has no common cause
            lf = union(intervals(*box) + intervals(*panel))
            allv = lf if allv is None else intersect(allv, lf)
    return sum(b - a for a, b in allv) / hours


# ----------------------------------------------------------- the case table ---
def failover_numbers():
    r = random.Random(3)
    warm = [proto_handover.unplanned_gap_frames(H.rtt_ms(r, "cell")) for _ in range(5000)]
    return H.pct(warm, 50), H.pct(warm, 99)


def roam_live_ms(short):
    sc = next(s for s in R.SCENARIOS if s.short == short)
    return R.run(sc, "minutes", n=800)["t_live_p50"]


def case_table(n=3):
    w50, w99 = failover_numbers()
    pw = core_power_w(n, "mirror")
    lit, hold = core_bridge_s(n, 0.9)
    lit1, _ = core_bridge_s(1, 0.9)
    rows = [
        dict(case="C1 host power lost, the Core store carries",
             cost=f"all {n} Skins keep the session for {lit/60:.0f} min lit (one Skin: {lit1/60:.0f} min), "
                  f"then {hold/60:.0f} min dark; one store, {n} loads",
             back="on a host: the live frame in 0.3 s (Wi-Fi) to 2.4 s (cold 5G)",
             state="none finalized; the flush rule holds"),
        dict(case="C2 one Skin link lost",
             cost="that Skin shows the ROM screen in 15 ms; the other Skins and the session are untouched",
             back=f"relink and the last frame in {R.TETHERS['cable']['relink_ms'] + R.frame_tx_ms(R.TETHERS['cable']) + 6:.0f} ms (cable), "
                  f"{R.TETHERS['mmwave']['relink_ms'] + R.frame_tx_ms(R.TETHERS['mmwave']) + 6:.0f} ms (60 GHz)",
             state="none; touches on a dark Skin are lost"),
        dict(case="C3 the Core box dies",
             cost=f"all {n} Skins go dark at once; the session lapses after 2 s",
             back=f"Skins on another Core: the live frame in {roam_live_ms('R1')/1000:.2f} s; "
                  f"the Core must be reached by hand",
             state="none finalized; up to 7 s if the Core had no other radio path and no flush"),
        dict(case="C4 the validator role fails on the Core",
             cost=f"a shadow in another power domain takes over: {w50:.0f} to {w99:.0f} frames covered by the Core compositor; "
                  f"the Skins see no break",
             back="at once; a cold start without a shadow takes about 130 ms",
             state="none"),
        dict(case="C5 a Skin dies",
             cost="that screen only; the Core and the session are untouched",
             back="a new Skin pairs: a wallet action, then the live frame in 0.3 s",
             state="none"),
    ]
    return rows, dict(w50=w50, w99=w99, power_w=pw)


# ------------------------------------------- the distance class and the single point ---
FLEETS = {"stress fleet of net/discovery": FLEET["crash_per_h"],
          "healthy fleet, one tenth of the crash rate": FLEET["crash_per_h"] / 10.0}
N_USERS_PER_CORE = 100        # users on one large C2 Core, the fleet seat decides [HYPOTHESIS]


def validator_unavailability(k, crash_per_h, beta=BETA):
    """Share of time with no reachable validator, k replicas. Beta is a regional common cause."""
    u = u_of(crash_per_h, FLEET["crash_down_s"])
    return 1 - (1 - beta * u) * (1 - (u * (1 - beta)) ** k)


def spof_by_class():
    r = random.Random(4)
    rows = []
    for path, (kind, extra, key, dl) in R.C2_PATHS.items():
        rtts = [R.c2_rtt(r, path) for _ in range(3000)]
        warm = [proto_handover.unplanned_gap_frames(x) for x in rtts]
        cold = []
        for x in rtts:
            first = H.A["render_ms"] + H.A["encode_first_ms"] + 15 * H.A["encode_slice_ms"] + H.A["decode_ms"]
            cold.append(2 * x + 20.0 + 1.5 * x + H.A["se_check_ms"] + H.A["sync_ms"] + x + first + 4.2)
        rows.append(dict(path=path, rtt=H.pct(rtts, 50), warm50=H.pct(warm, 50), warm99=H.pct(warm, 99),
                         cold50=H.pct(cold, 50), cold99=H.pct(cold, 99)))
    return rows


# ------------------------------------------------------- part B: a link loss ---
DETECT_MS = 2 * 1000.0 / 240.0          # two scan frames with no stream               [HYPOTHESIS]


def link_loss(r, tether, store, outage_s, kind):
    """What the Skin shows and how long it takes to come back.

    kind: 'glitch' (the link retrains, the Skin stays powered),
          'unplug' (cable pulled: no link and no power from the Core).
    """
    t = R.TETHERS[tether]
    store_s = K.rom_screen_s(K.SKIN_STORES[store])
    own_power = store_s > 0
    if kind == "glitch":
        powered_s = outage_s if (t["powered"] or own_power) else 0.0
        if not t["powered"] and own_power:
            powered_s = min(outage_s, store_s)
        elif t["powered"]:
            powered_s = outage_s
    else:
        powered_s = min(outage_s, store_s)
    rom_start = DETECT_MS + R.A["skin_rom_screen_ms"] if powered_s > 0 else None
    shows = "black" if powered_s == 0 else ("the ROM screen" if powered_s >= outage_s else "the ROM screen, then black")
    dark_at_back = (kind == "unplug" and store_s < outage_s) or (kind == "glitch" and powered_s < outage_s)
    relink = t["relink_ms"] if kind == "glitch" else t["attach_ms"]
    boot = R.A["skin_boot_ms"] if dark_at_back else 0.0
    back = max(relink, boot) + R.frame_tx_ms(t) + t["one_way_ms"] + R.A["skin_decode_ms"] \
        + r.uniform(0.0, R.FRAME_MS) + 0.3
    return dict(shows=shows, rom_ms=rom_start, back_ms=back, missed_frames=int(outage_s * 240),
                stale_frame_shown=False)


def link_table():
    rows = []
    r = random.Random(8)
    for tether in ("cable", "mmwave"):
        for kind in ("glitch", "unplug"):
            if tether == "mmwave" and kind == "unplug":
                continue
            for outage in (0.05, 1.0, 10.0, 60.0, 900.0):
                for store in ("none", "seconds", "minutes"):
                    if tether == "mmwave" and store == "none":
                        continue                     # a wireless Skin needs its own cell
                    xs = [link_loss(r, tether, store, outage, kind) for _ in range(300)]
                    back = H.pct([x["back_ms"] for x in xs], 50)
                    rows.append(dict(tether=tether, kind=kind, outage_s=outage, store=store,
                                     shows=xs[0]["shows"], rom_ms=xs[0]["rom_ms"], back_ms=back,
                                     missed=xs[0]["missed_frames"]))
    return rows


def fmt_s(s):
    if s < 1:
        return f"{s*1000:.0f} ms"
    if s < 120:
        return f"{s:g} s"
    return f"{s/60:g} min"


def main():
    os.makedirs(OUT, exist_ok=True)
    L = []
    p = L.append
    p("# The Core as a single point, and the Skin on a link loss (generated by corefail.py)\n")
    p("## The load of N Skins on one Core, delta session\n")
    p("| N | mirror, watts | extend or split, watts | mirror, lit time on `0.9 Wh` | extend, lit time on `0.9 Wh` | N Leafs, lit time each |")
    p("|---|---|---|---|---|---|")
    p_leaf = core_power_w(1, "mirror")
    for n in (1, 2, 3, 4, 6):
        lm, _ = core_bridge_s(n, 0.9, "mirror")
        le, _ = core_bridge_s(n, 0.9, "extend")
        p(f"| {n} | {core_power_w(n,'mirror'):.2f} | {core_power_w(n,'extend'):.2f} | {lm/60:.1f} min | {le/60:.1f} min | {core_bridge_s(1,0.9)[0]/60:.1f} min |")
    p("\nAll `N` Skins share one store, so each Skin gets `1/N` of the lit time. "
      "N Leafs hold `N` stores. `[HYPOTHESIS]` the hub scaling.\n")
    rows, fo = case_table(3)
    p("## The failure cases, N = 3 Skins on one Core, a `0.9 Wh` store\n")
    p("| case | what the user sees | how long to come back | state lost |")
    p("|---|---|---|---|")
    for x in rows:
        p(f"| {x['case']} | {x['cost']} | {x['back']} | {x['state']} |")
    p("\n## Joint failure: N Skins on one Core against N Leafs\n")
    p("Rates per hour and repair times in seconds, all `[HYPOTHESIS]`: "
      + ", ".join(f"{k} {v[0]:.2e} per h and {v[1]} s" for k, v in RATES.items() if v[1] is not None and k != "validator_crash")
      + ". A Leaf is a Core and a panel in one body. The common-cause share is `{BETA}`.\n")
    res = {"avail": [], "power": [], "case": rows, "link": None, "rates": {k: list(v) for k, v in RATES.items()}}
    p("| N | design | no screen at all, minutes per year | dark screen-minutes per year | events per year |")
    p("|---|---|---|---|---|")
    for n in (1, 2, 3, 4, 6):
        for design in ("split", "leafs"):
            u = unavailability(n, design)
            res["avail"].append(dict(n=n, design=design, **u))
            p(f"| {n} | {'one Core, N Skins' if design=='split' else 'N Leafs'} | "
              f"{u['all_dark']*HOURS_YEAR*60:.3g} | {u['mean_dark_screens']*HOURS_YEAR*60:.3g} | "
              f"{u['events_per_h']*HOURS_YEAR:.3g} |")
    p("\nWith the 60 GHz link in place of the cable, `N = 3`:\n")
    p("| design | no screen at all, minutes per year | dark screen-minutes per year |")
    p("|---|---|---|")
    for design in ("split", "leafs"):
        u = unavailability(3, design, tether="mmwave")
        res["avail"].append(dict(n=3, design=design, tether="mmwave", **u))
        p(f"| {design} | {u['all_dark']*HOURS_YEAR*60:.3g} | {u['mean_dark_screens']*HOURS_YEAR*60:.3g} |")
    u3s, u3l = unavailability(3, "split"), unavailability(3, "leafs")
    ratio = u3s["all_dark"] / u3l["all_dark"]
    res["ratio_all_dark_n3"] = ratio
    p(f"\nFor `N = 3` the chance that no screen works is `{ratio:.2g}` times higher with one Core. "
      f"The dark screen-minutes per year differ by `{u3s['mean_dark_screens']/u3l['mean_dark_screens']:.2f}` times, "
      "so the Split moves the risk into one event. It does not add risk of the same kind.\n")
    p("### Check of the closed form by simulation, rates times 1500\n")
    p("| N | design | closed form | simulated |")
    p("|---|---|---|---|")
    for n in (2, 3):
        for design in ("split", "leafs"):
            sc = 1500.0
            saved = dict(RATES)
            try:
                for k in ("core_box", "skin_panel", "cable_link"):
                    RATES[k] = (saved[k][0] * sc, saved[k][1])
                cf = unavailability(n, design, beta=0.0)["all_dark"]
                RATES.update(saved)
                sim = simulate_all_dark(n, design, scale=sc, hours=1.0e5)
            finally:
                RATES.update(saved)
            res.setdefault("check", []).append(dict(n=n, design=design, closed=cf, sim=sim))
            p(f"| {n} | {design} | {cf:.3e} | {sim:.3e} |")
    p("\n### The host power loss, restarts per year\n")
    p("A host power gap longer than the store ends in a pause and a restart. "
      "The gap law is a short mode (mean `60 s`) and a parked mode (`2 %`, mean `4 h`). `[HYPOTHESIS]`\n")
    p("| design | lit time | restarts per year | what restarts |")
    p("|---|---|---|---|")
    lam = RATES["host_power"][0]
    for n in (1, 3, 6):
        lit, hold = core_bridge_s(n, 0.9)
        pr = gap_exceeds(lit + hold)
        res["power"].append(dict(n=n, design="split", lit_s=lit, restarts_year=lam * HOURS_YEAR * pr))
        p(f"| one Core, {n} Skins, `0.9 Wh` | {lit/60:.1f} min | {lam*HOURS_YEAR*pr:.2f} | all {n} Skins at once |")
        lit1, hold1 = core_bridge_s(1, 0.9)
        pr1 = gap_exceeds(lit1 + hold1)
        p(f"| {n} Leafs, one host, `0.9 Wh` each | {lit1/60:.1f} min | {lam*HOURS_YEAR*pr1:.2f} | all {n} Leafs at once, on a common host |")
    p("\nThe store is the same in both. The restart count rises a little with N. "
      "The common host, not the Split, is what restarts everything at once.\n")
    p("## The Core as a single point, by distance class\n")
    p("At C0 and C1 the Core is the device and the screens depend on it. At C2 the Leaf keeps its own silicon, "
      "frame store, compositor and U7, and the Core is a validator with replicas.\n")
    sp = spof_by_class()
    res["spof"] = sp
    p("| class | the Core box dies | what the user sees | how long |")
    p("|---|---|---|---|")
    p(f"| C0 or C1, one Core, N Skins | all N screens | dark, then the ROM screen while the store lasts | until another Core: `{RATES['core_box'][1]:.0f} s` assumed, then the live frame in `0.3 s` |")
    for x in sp:
        warm_ms = x["warm50"] * R.FRAME_MS
        within = "inside" if warm_ms <= 40.0 else "outside"
        p(f"| {x['path']}, a shadow in another power domain | none of the Leafs go dark | the Leaf frame store and compositor cover `{x['warm50']:.0f}` to `{x['warm99']:.0f}` frames, {within} the `40 ms` limit | `{warm_ms:.0f} ms` |")
        p(f"| {x['path']}, no shadow | none of the Leafs go dark | a cold start on the next validator | `{x['cold50']:.0f} ms` p50, `{x['cold99']:.0f} ms` p99 |")
    p(f"\n**The blast radius grows.** A large C2 Core serves about `{N_USERS_PER_CORE}` users. One box death touches all of them in the same instant. "
      f"A hot shadow costs `76 Mbit/s` per session. A warm shadow costs `0.26 Mbit/s`. "
      f"A cold start of `{N_USERS_PER_CORE}` sessions needs `{N_USERS_PER_CORE*256/1000:.1f} MB` of intra frames in about `0.15 s`.\n")
    p("Share of time with no reachable validator, `k` replicas, with the common-cause share "
      f"`{BETA}`. This is the real single point at C2.\n")
    p("| fleet | k = 1 | k = 2 | k = 3 | k = 4 |")
    p("|---|---|---|---|---|")
    res["valav"] = []
    for name, lam in FLEETS.items():
        cells = []
        for k in (1, 2, 3, 4):
            u = validator_unavailability(k, lam)
            res["valav"].append(dict(fleet=name, k=k, minutes_year=u * HOURS_YEAR * 60))
            cells.append(f"{u*HOURS_YEAR*60:.3g} min per year")
        p(f"| {name} | " + " | ".join(cells) + " |")
    p("\nThe table counts a validator outage, not a dark screen. At C2 the screen lives on, "
      "and the Leaf shows the last frame and the compositor result. The beta term sets the floor: "
      "more replicas stop helping when a common cause takes them all.\n")
    p("## Part B: the Skin on a link loss\n")
    p(f"Detection takes `{DETECT_MS:.1f} ms` (two scan frames without a stream). The ROM screen follows in "
      f"`{R.A['skin_rom_screen_ms']} ms`. The Skin never shows a stale frame: it has no frame store, and a stale frame looks live.\n")
    p("| tether | cause | outage | store | the Skin shows | ROM screen at | back after the link returns | frames missed |")
    p("|---|---|---|---|---|---|---|---|")
    lt = link_table()
    res["link"] = lt
    for x in lt:
        if x["outage_s"] in (1.0, 60.0) or (x["store"] == "seconds" and x["outage_s"] != 10.0):
            continue
        p(f"| {x['tether']} | {x['kind']} | {fmt_s(x['outage_s'])} | {x['store']} | {x['shows']} | "
          f"{'none' if x['rom_ms'] is None else f'{x['rom_ms']:.0f} ms'} | {x['back_ms']:.0f} ms | {x['missed']} |")
    open(os.path.join(OUT, "corefail.md"), "w").write("\n".join(L) + "\n")
    json.dump(res, open(os.path.join(OUT, "corefail.json"), "w"), indent=1, default=str)
    print("\n".join(L))


if __name__ == "__main__":
    main()
