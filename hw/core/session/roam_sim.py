#!/usr/bin/env python3
"""roam_sim.py - a Skin picked up from Core A and attached to Core B.

Session seat of hw/core, block HP-2. The Skin carries no state. The session
follows through RG-19: Core A pauses (or lapses), Core B resumes as a second
writer. The question: time to first pixel, to the live frame and to the full
session, for three Skin stores (none, seconds, minutes), two tethers and three
Core B states.

Read only: hw/hostpower/continuity (powersm, handover_sim) and the delay model of
net/discovery through it. The tether rates and delays follow hw/core/link/out
(links.txt, latency.txt): DSC at 3:1, 19.4 Gb/s net on contact leaves, 5 Gb/s on
60 GHz. The attach and relink times are an ASSUMPTION of this seat, because the
link seat gives none. Replace them when it does.

Times run from the moment the Skin touches Core B (a cable seats, or a 60 GHz
link answers). Every stage time is [HYPOTHESIS] except the FINAL/21 Section
21.5.7 rows that netmodel reproduces.

Run: python3 roam_sim.py      writes out/roam.md and out/roam.json
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
import netmodel as nm  # noqa: E402  (on the path through handover_sim)
import skinsession as K  # noqa: E402

OUT = os.path.join(HERE, "out")
FRAME_MS = 1000.0 / 240.0
RAW_FRAME_BITS = 1600 * 3200 * 30          # 10 bit, 4:4:4: 36.9 Gbit/s at 240 Hz [Lead, BRIEF]

# --------------------------------------------------------- the tethers (assumed) ---
TETHERS = {
    # attach_ms: seat or beam training and link key; ratio: compression of the pixel stream;
    # powered: the tether carries power to the Skin
    "cable": dict(attach_ms=150.0, rate_gbps=19.4, ratio=3.0, one_way_ms=0.047, powered=True,
                  relink_ms=100.0),
    "mmwave": dict(attach_ms=250.0, rate_gbps=5.0, ratio=3.0, one_way_ms=0.48, powered=False,
                   relink_ms=60.0),
}
A = {
    "skin_boot_ms": 25.0,        # the Skin ROM and the panel driver wake                 [HYPOTHESIS]
    "skin_rom_screen_ms": 6.5,   # compose 2 ms, scan 4.17 ms, panel                      [TREE] bootsm
    "pair_ms": 30.0,             # U7 challenge of the Skin identity, registry cache hit  [HYPOTHESIS]
    "core_proc_ms": 3.0,         # Core decode of the intra frame and the light transcode [HYPOTHESIS]
    "skin_decode_ms": 0.5,       # the minimal decoder in the Skin                        [HYPOTHESIS]
    "a_pause_ms": 50.0,          # Core A sees the Skin gone, signs and submits the pause  [HYPOTHESIS]
    "lapse_after_s": 2.0,        # RG-19 rule R3: a lapse needs 2 s of silence
}


def frame_tx_ms(t):
    return RAW_FRAME_BITS / t["ratio"] / (t["rate_gbps"] * 1e9) * 1000.0


class Scen:
    def __init__(self, name, short, link_b, core_b, tether, carry_s, prewarm, a_alive, dl_mbps, takeover=False):
        self.name, self.short, self.link_b, self.core_b = name, short, link_b, core_b
        self.tether, self.carry_s, self.prewarm = tether, carry_s, prewarm
        self.a_alive, self.dl_mbps, self.takeover = a_alive, dl_mbps, takeover

    def with_(self, **kw):
        d = dict(self.__dict__)
        d.update(kw)
        s = Scen(d["name"], d["short"], d["link_b"], d["core_b"], d["tether"], d["carry_s"],
                 d["prewarm"], d["a_alive"], d["dl_mbps"], d["takeover"])
        return s


SCENARIOS = [
    Scen("R1 desk Core to a vehicle Core, standby, 5G", "R1", "cell_warm", "standby", "cable",
         30.0, False, True, 150.0),
    Scen("R2 desk Core to a second desk Core, awake, Wi-Fi, proximity hint", "R2", "wifi", "awake",
         "cable", 10.0, True, True, 2000.0),
    Scen("R3 desk Core to a vehicle Core, just started, cold modem", "R3", "cell_cold", "cold",
         "cable", 30.0, False, True, 150.0),
    Scen("R4 desk Core dies, the Skin goes to the vehicle Core", "R4", "cell_warm", "standby",
         "cable", 30.0, False, False, 150.0),
    Scen("R5 desk Core dies, the Skin reaches the vehicle Core in 1 s, by pause and lapse", "R5",
         "cell_warm", "standby", "cable", 1.0, False, False, 150.0),
    Scen("R6 the same, by TakeOver", "R6", "cell_warm", "standby", "cable", 1.0, False, False, 150.0,
         takeover=True),
]


def core_ready_ms(sc, bt):
    """Core B: when its U7 and hub answer, and when its network link is up."""
    if sc.core_b == "awake":
        return 0.0, 0.0
    return bt["t_safe"], bt["t_link"]


def one(sc, store, r, bt_cache):
    t = TETHERS[sc.tether]
    bt = bt_cache[sc.link_b if sc.core_b != "awake" else "both"]
    rtt = H.rtt_ms(r, "wifi" if sc.link_b == "wifi" else "cell")
    store_s = K.rom_screen_s(K.SKIN_STORES[store])
    skin_alive = store_s >= sc.carry_s
    # a wireless Skin with an empty store cannot even attach
    if not skin_alive and not t["powered"]:
        return dict(outcome="NO_POWER", t_pixel=float("nan"), t_live=float("nan"),
                    t_full=float("nan"), frames=float("nan"), rom_s=store_s)
    core_safe, core_net = core_ready_ms(sc, bt)
    skin_boot = 0.0 if skin_alive else A["skin_boot_ms"]
    t_link = max(core_safe, t["attach_ms"], skin_boot)
    t_pixel = t_link + A["skin_rom_screen_ms"]
    t_paired = t_link + A["pair_ms"]
    # the pause of Core A, or the lapse, must come first
    if sc.takeover:
        wait = 0.0                    # RG-19A rule R13: a granted writer needs no pause and no lapse
    elif sc.a_alive:
        wait = max(0.0, A["a_pause_ms"] - sc.carry_s * 1000.0)
    else:
        wait = max(0.0, (A["lapse_after_s"] - sc.carry_s) * 1000.0)
    start = max(t_paired, core_net, wait)
    first = H.first_live_frame_ms(r, H.Scen("x", "x", 0, "dock", "x", sc.link_b, sc.dl_mbps, False, 1.0), rtt)
    if sc.prewarm:
        # B fetched the snapshot, checked the pause record and rendered the frozen frame
        crit = H.A["u7_sign_ms"] + rtt + A["core_proc_ms"]
        enc = 0.0
        full_extra = 2 * rtt
    else:
        crit = (H.A["u7_sign_ms"] + rtt / 2 + H.A["verify_pause_ms"] + H.A["sync_ms"] + first
                + rtt / 2 + A["core_proc_ms"])
        full_extra = H.A["sync_ms"] + 2 * rtt
    t_live = (start + crit + frame_tx_ms(t) + t["one_way_ms"] + A["skin_decode_ms"]
              + r.uniform(0.0, FRAME_MS) + 0.3)
    t_full = t_live + full_extra
    frames = max(0, math.ceil((t_live - t_pixel) / FRAME_MS))
    return dict(outcome="ROAMED", t_pixel=t_pixel, t_live=t_live, t_full=t_full,
                frames=frames, rom_s=store_s)


def pct(xs, p):
    xs = sorted(x for x in xs if x == x)
    if not xs:
        return float("nan")
    return xs[min(len(xs) - 1, max(0, int(round(p / 100.0 * (len(xs) - 1)))))]


def run(sc, store, n=2000, seed=21):
    r = random.Random(seed * 131 + len(sc.short) * 17 + len(store) + int(sc.carry_s))
    bt_cache = {k: P.boot_times(k) for k in ("both", "wifi", "cell_warm", "cell_cold")}
    rows = [one(sc, store, r, bt_cache) for _ in range(n)]
    out = rows[0]["outcome"]
    return dict(scenario=sc.short, store=store, tether=sc.tether, carry_s=sc.carry_s,
                outcome=out, rom_s=rows[0]["rom_s"],
                t_pixel_p50=pct([x["t_pixel"] for x in rows], 50),
                t_live_p50=pct([x["t_live"] for x in rows], 50),
                t_live_p99=pct([x["t_live"] for x in rows], 99),
                t_full_p50=pct([x["t_full"] for x in rows], 50),
                frames_p50=pct([x["frames"] for x in rows], 50))


# ------------------------------------------------- the input path with a Skin ---
def i2p(kind, tether, skin=True, n=100000, seed=5, predicted=False):
    """Mean and p99 input to photon, with the Skin hop added. Baseline is FINAL/21 21.5.7."""
    r = random.Random(seed)
    t = TETHERS[tether]
    if kind == "wifi":
        wired = nm.wired_ow_ms(0.0, 0.0, hops=2)
        k = nm.WIFI
    else:
        wired = nm.wired_ow_ms(0.0, 3.0, hops=2, fixed=nm.UPF_MS)
        k = nm.CELL
    extra = (2 * t["one_way_ms"] + frame_tx_ms(t) * 0.0625 + A["core_proc_ms"] / 3.0
             + A["skin_decode_ms"]) if skin else 0.0     # one slice, not the frame
    xs = []
    for _ in range(n):
        if predicted:
            v = nm.touch_ms(r) + 0.2 + nm.scanout_ms(r) + extra
        else:
            v = nm.input_to_photon(r, k, wired) + extra
        xs.append(v)
    xs.sort()
    return sum(xs) / n, xs[int(0.99 * (n - 1))]


# --------------------------------------------- the distance classes: C0, C1, C2 ---
# C0 contact or tether to 2 m, C1 a room to about 30 m, C2 far, up to kilometres
# (hw/core/BRIEF.md Section 8). At C0 and C1 the device is a Skin: the Core sends pixels.
# At C2 the device is the L.6.0 Leaf: the Core is a validator, the Leaf decodes slices
# and holds the frame store and the compositor, and its own U7 signs. [DECISION] Ayaz.
LAT = json.load(open(os.path.join(ROOT, "sim", "latency", "results", "results.json")))["paths"]


def c2_stage_rtt(path):
    sm = LAT[path]["stages_mean"]
    return sm["air_up"] + sm["net"] + sm["air_down"]


C2_PATHS = {
    # name: (the link kind of handover_sim, extra wired round trip in ms, the sim/latency path, dl_mbps)
    "C2 km, 5G cell-site, large Core antenna": ("cell", 0.0, "nr_cell", 150.0),
    "C2 far, far validator": ("cell", 80.0, "far", 150.0),
}
LEAF_VARIANTS = {
    "asleep": "silicon asleep in Skin mode, modem cold",
    "awake": "silicon and modem awake, decoder idle",
    "hot": "decoding a C2 shadow in parallel while tethered",
}


def c2_rtt(r, path):
    kind, extra, _, _ = C2_PATHS[path]
    return H.rtt_ms(r, kind) + extra * r.uniform(0.97, 1.03)


def leaf_out(variant, path, r, bt):
    """C0 or C1 Core to a C2 Core. The tether is lost at t = 0. The Leaf is the new writer."""
    kind, extra, _, dl = C2_PATHS[path]
    rtt = c2_rtt(r, path)
    sc = H.Scen("c2", "C2", 0, "dock", "x", kind, dl, False, 1.0)
    first = H.first_live_frame_ms(r, sc, rtt)
    scan = r.uniform(0.0, FRAME_MS) + 0.3
    sign = H.A["u7_sign_ms"]
    if variant == "asleep":
        t_pixel = bt["cell_cold"]["t_safe"]
        t_link = bt["cell_cold"]["t_link"]
        hs = 1.5 * rtt + H.A["se_check_ms"]
        t_live = (t_link + hs + sign + rtt / 2 + H.A["sync_ms"] + first + rtt / 2 + scan)
        not_live, covered = math.ceil((t_live - t_pixel) / FRAME_MS), 0
    elif variant == "awake":
        t_pixel = R_DETECT + A["skin_rom_screen_ms"]
        t_live = sign + rtt / 2 + H.A["sync_ms"] + first + rtt / 2 + scan
        not_live, covered = math.ceil((t_live - t_pixel) / FRAME_MS), 0
    else:
        t_pixel = 0.0                       # the Leaf frame store is current
        t_live = sign + rtt + FRAME_MS + scan
        not_live, covered = 0, math.ceil((sign + rtt) / FRAME_MS)
    return dict(t_pixel=t_pixel, t_live=t_live, not_live=not_live, covered=covered, rtt=rtt)


R_DETECT = 2 * FRAME_MS


def leaf_back(tether, path, r):
    """C2 back to a C0 or C1 Core. The Leaf stays live on C2 while the tether trains."""
    t = TETHERS[tether]
    rtt = c2_rtt(r, path)
    core_rtt = H.rtt_ms(r, "wifi")           # the Core on its own network, a room validator
    attach = t["attach_ms"] + A["pair_ms"]
    # the Core starts its sync at contact, in parallel with the tether
    ready = H.A["sync_ms"] + H.A["verify_pause_ms"]
    start = max(attach, ready)
    takeover = H.A["u7_sign_ms"] + core_rtt
    render = H.A["render_ms"] + A["core_proc_ms"] + frame_tx_ms(t) + t["one_way_ms"] + A["skin_decode_ms"]
    t_switch = start + takeover + render + r.uniform(0.0, FRAME_MS) + 0.3
    covered = math.ceil((takeover + render) / FRAME_MS)
    return dict(t_switch=t_switch, covered=covered, not_live=0, rtt=rtt)


def leaf_roundtrip(n=2000, seed=33):
    r = random.Random(seed)
    bt = {k: P.boot_times(k) for k in ("cell_cold", "cell_warm")}
    out = {"out": [], "back": [], "lat": []}
    for path in C2_PATHS:
        for v in LEAF_VARIANTS:
            rows = [leaf_out(v, path, r, bt) for _ in range(n)]
            out["out"].append(dict(path=path, variant=v,
                                   t_pixel=pct([x["t_pixel"] for x in rows], 50),
                                   t_live_p50=pct([x["t_live"] for x in rows], 50),
                                   t_live_p99=pct([x["t_live"] for x in rows], 99),
                                   not_live=pct([x["not_live"] for x in rows], 50),
                                   covered=pct([x["covered"] for x in rows], 50),
                                   rtt=pct([x["rtt"] for x in rows], 50)))
        for tether in ("cable", "mmwave"):
            rows = [leaf_back(tether, path, r) for _ in range(n)]
            out["back"].append(dict(path=path, tether=tether,
                                    t_switch_p50=pct([x["t_switch"] for x in rows], 50),
                                    t_switch_p99=pct([x["t_switch"] for x in rows], 99),
                                    covered=pct([x["covered"] for x in rows], 50)))
    for path, (_, _, key, _) in C2_PATHS.items():
        out["lat"].append(dict(path=path, rtt_stage_mean=c2_stage_rtt(key),
                               mean=LAT[key]["mean"], p99=LAT[key]["p99"]))
    return out


def fmt(ms):
    if ms != ms:
        return "n/a"
    return f"{ms:.0f} ms" if ms < 1000 else f"{ms/1000:.2f} s"


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"roam": [], "i2p": []}
    L = ["# The Skin that roams (generated by roam_sim.py)\n",
         "Times run from the moment the Skin touches Core B. `2 000` draws per cell. "
         "The tether numbers are an assumption of this seat. `[HYPOTHESIS]` every stage time.\n"]
    p = L.append
    for sc in SCENARIOS:
        p(f"\n## {sc.name}\n")
        p(f"Carry `{sc.carry_s:g} s`, tether {sc.tether}, Core B {sc.core_b}, "
          f"prewarm {'yes' if sc.prewarm else 'no'}, Core A {'alive' if sc.a_alive else 'dead'}, "
          f"{'TakeOver' if sc.takeover else 'pause and resume'}.\n")
        p("| Skin store | ROM screen lasts | outcome | first pixel p50 | live frame p50 | live frame p99 | full session p50 | frames not live |")
        p("|---|---|---|---|---|---|---|---|")
        for store in ("none", "seconds", "minutes"):
            c = run(sc, store)
            res["roam"].append(c)
            p(f"| {store} | {c['rom_s']:.0f} s | {c['outcome']} | {fmt(c['t_pixel_p50'])} | "
              f"{fmt(c['t_live_p50'])} | {fmt(c['t_live_p99'])} | {fmt(c['t_full_p50'])} | "
              f"{c['frames_p50']:.0f} |")
    p("\n## Tether and carry, scenario R1\n")
    p("| tether | carry | outcome | first pixel p50 | live frame p50 | full session p50 |")
    p("|---|---|---|---|---|---|")
    sc1 = SCENARIOS[0]
    for tether in ("cable", "mmwave"):
        for carry in (1.0, 5.0, 30.0, 300.0, 3600.0):
            for store in ("none", "minutes", "cell"):
                if store == "none" and carry != 30.0:
                    continue
                if store == "cell" and tether == "cable":
                    continue
                c = run(sc1.with_(tether=tether, carry_s=carry), store, n=800)
                res["roam"].append(dict(c, sweep=True))
                p(f"| {tether}, {store} | {carry:g} s | {c['outcome']} | {fmt(c['t_pixel_p50'])} | "
                  f"{fmt(c['t_live_p50'])} | {fmt(c['t_full_p50'])} |")
    p("\n## The input to photon, with and without the Skin hop\n")
    p("| path | a new action, mean | p99 | a predicted action, mean | p99 |")
    p("|---|---|---|---|---|")
    for kind, tether, name in (("wifi", "cable", "Wi-Fi, room validator"), ("cell", "cable", "5G, cell-site validator")):
        for skin in (False, True):
            m, q = i2p(kind, tether, skin=skin)
            pm, pq = i2p(kind, tether, skin=skin, predicted=True)
            res["i2p"].append(dict(path=name, skin=skin, mean=m, p99=q, pmean=pm, pp99=pq))
            p(f"| {name}, {'Skin on a cable' if skin else 'Leaf, no Skin'} | {m:.1f} ms | {q:.1f} ms | {pm:.1f} ms | {pq:.1f} ms |")
    cls = leaf_roundtrip()
    res["classes"] = cls
    p("\n## The distance classes: a Leaf from a C0 or C1 Core to a C2 Core, and back\n")
    p("At C2 the device is the L.6.0 Leaf. It renders locally with its slice decoder. Its own U7 signs. "
      "The session moves by one TakeOver transaction. The round trips come from `sim/latency`.\n")
    p("| class | the path | round trip, stage mean | input to photon, mean | p99 |")
    p("|---|---|---|---|---|")
    for m, n_ in (("cable", "C0, a Skin on a cable"), ("mmwave", "C1, a Skin on a 60 GHz link")):
        a, b = i2p("wifi", m)
        p(f"| {n_} | the Core in the room, Wi-Fi validator | `{2*TETHERS[m]['one_way_ms']:.2f} ms` | {a:.1f} ms | {b:.1f} ms |")
    for x in cls["lat"]:
        p(f"| {x['path'].split(',')[0]} | {x['path'].split(', ',1)[1]} | `{x['rtt_stage_mean']:.1f} ms` | {x['mean']:.1f} ms | {x['p99']:.1f} ms |")
    p("\n### Out: the tether is lost, the Leaf becomes the writer at C2\n")
    p("| path | the Leaf before | first pixel p50 | live frame p50 | live frame p99 | frames not live | frames covered by U1 | inside the 40 ms reprojection limit |")
    p("|---|---|---|---|---|---|---|---|")
    for x in cls["out"]:
        inside = "n/a" if x["covered"] == 0 else ("yes" if x["covered"] * FRAME_MS <= 40.0 else "NO")
        p(f"| {x['path']} | {x['variant']} | {fmt(x['t_pixel'])} | {fmt(x['t_live_p50'])} | {fmt(x['t_live_p99'])} | {x['not_live']:.0f} | {x['covered']:.0f} | {inside} |")
    p("\n### Back: the Leaf reaches a Core, the Core becomes the writer\n")
    p("The Leaf stays live on its C2 stream while the tether trains. It is a make before break. The time does not depend on the C2 path, because the TakeOver goes through the Core network.\n")
    p("| from | tether | switch complete p50 | switch complete p99 | frames not live | frames covered by U1 |")
    p("|---|---|---|---|---|---|")
    for x in cls["back"]:
        p(f"| {x['path']} | {x['tether']} | {fmt(x['t_switch_p50'])} | {fmt(x['t_switch_p99'])} | 0 | {x['covered']:.0f} |")
    open(os.path.join(OUT, "roam.md"), "w").write("\n".join(L) + "\n")
    json.dump(res, open(os.path.join(OUT, "roam.json"), "w"), indent=1)
    print("\n".join(L))


if __name__ == "__main__":
    main()
