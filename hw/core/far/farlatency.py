#!/usr/bin/env python3
"""farlatency.py - input to photon at 100 m to 10 km, with the Core at the radio and behind a backhaul.

It reuses sim/latency/model.py by import, read only. What the far link adds to that model:
  1. propagation: 3.336 us per km in air, each way (2 d / c on the whole path);
  2. Wi-Fi: the slot time grows with the distance (coverage class: aAirPropagationTime), so AIFS and the
     backoff grow, and hidden stations collide more beyond 500 m [HYPOTHESIS];
  3. the serialisation of the first slice (60 kbit) and of the input packet at the rate the link budget gives;
  4. HARQ: the first-transmission BLER rises when the SNR margin falls under 3 dB [HYPOTHESIS];
  5. the backhaul: fibre at 4.9 us per km on a route 1.5 x the straight line, plus 0.3 ms of equipment.
The gate is the 30 ms p99 of Part 21 Section 21.5.7. Run: python3 farlatency.py  (about 2 minutes)
Out: out/latency.json, out/latency.txt
"""
import copy
import json
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "sim", "latency"))
import numpy as np  # noqa: E402
import model as M  # noqa: E402  (sim/latency/model.py, read only)
import farlink as F  # noqa: E402

OUT = os.path.join(HERE, "out")
N = 200_000
C_KM_MS = 299792.458 / 1000.0          # km per ms
SLICE_BITS = 60e3                      # first slice, the sim README: about 60 kbit
IN_SMALL_BITS = 200 * 8                # the input packet of the sim (under 200 B)
IN_SIGNED_BITS = (64 + 3309) * 8       # a touch batch with an ML-DSA-65 signature
FIBRE_MS_PER_KM = 4.9e-3               # 1.468 index: 4.9 us per km
ROUTE = 1.5                            # fibre route over the straight line (density.py uses 1.5 to 2.0)
EQUIP_MS = 0.3                         # the UPF and switching, as the sim's cell-site path
BACKHAUL = [("Core at the radio", 0.0), ("metro, 20 km of fibre", 20.0), ("regional, 100 km", 100.0),
            ("national, 500 km", 500.0)]
DIST = F.DIST_M

CONFIGS = [  # name, tech, scenario, Core gain
    ("5G 3.5 GHz, urban NLOS, Core 18 dBi", "nr35", "UMa-NLOS", 18),
    ("5G 3.5 GHz, LOS, Core 25 dBi", "nr35", "UMa-LOS", 25),
    ("5G 700 MHz, urban NLOS, Core 18 dBi", "nr07", "UMa-NLOS", 18),
    ("5G 700 MHz, LOS, Core 25 dBi", "nr07", "UMa-LOS", 25),
    ("Wi-Fi 5 GHz, LOS, Core 25 dBi", "wifi5", "UMa-LOS", 25),
    ("Wi-Fi 2.4 GHz, LOS, Core 25 dBi", "wifi24", "UMa-LOS", 25),
]


def bler_from_margin(m):
    """First-transmission BLER. 10 % with link adaptation while the margin is 3 dB or more. [HYPOTHESIS]"""
    if m >= 3.0:
        return 0.10
    return min(0.9, 0.10 * 10 ** ((3.0 - m) / 2.0))


def make_path(tech, d_m, link, net_rtt_ms, net_kind, ul_bits):
    """A sim Path for this radio, distance and link state, plus the post-hoc add-on in ms."""
    t = F.TECH[tech]
    d_km = d_m / 1000.0
    prop_ms = 2 * d_km / C_KM_MS
    r_dl = link["dl_bps"] / t["duty_dl"]            # the rate while transmitting
    r_ul = link["ul_bps"] / t["duty_ul"]
    add = prop_ms
    net = M.Net(net_kind, net_rtt_ms, 0.3, tail_ms=0.1 if net_kind != "far" else 2.0)
    if t["band"] == "ism":
        slot = 0.009 + 2 * d_km / C_KM_MS            # coverage class: slot grows with the round trip
        aifs = 0.016 + 2 * slot
        hid = d_m > 500
        links = tuple(M.WifiLink(busy=b, slot_ms=slot, aifs_ms=aifs, coll=0.12 if hid else 0.05,
                                 refreeze=0.25 if hid else 0.10) for b in (0.30, 0.15))
        if t["f"] < 3:                                # one link only on 2.4 GHz
            links = links[:1]
        ul_ppdu = 0.04 + ul_bits / max(r_ul, 1.0) * 1e3
        dl_ppdu = 0.04 + SLICE_BITS / max(r_dl, 1.0) * 1e3
        w = M.Wifi(links=links, mlo=len(links) > 1, ul_ppdu_ms=ul_ppdu, dl_ppdu_ms=dl_ppdu)
        nr = M.Nr()
        air = "wifi"
    else:
        # 5G: the air stages of the sim carry one slot. More slots add time.
        slot_ms = 0.5
        n_dl = math.ceil(SLICE_BITS / max(r_dl * slot_ms * 1e-3, 1.0))
        n_ul = math.ceil(ul_bits / max(r_ul * slot_ms * 1e-3, 1.0))
        add += (n_dl - 1) * slot_ms + ((n_dl - 1) // 3) * 1.0
        add += (n_ul - 1) * 2.5                      # one UL slot per 2.5 ms period
        b_dl = bler_from_margin(link["margin_dl"])
        b_ul = bler_from_margin(link["margin_ul"])
        nr = M.Nr(bler_ul=b_ul, bler_dl=b_dl)
        w = M.Wifi()
        air = "nr"
    return M.Path("far", air, net, wifi=w, nr=nr), add


def run_case(tech, d_m, link, backhaul_km, ul_bits, far80=False, n=N, seed=7):
    if far80:
        kind, rtt = "far", 80.0
    else:
        base = 0.1 if F.TECH[tech]["band"] == "ism" else 0.3
        rtt = base if backhaul_km == 0 else EQUIP_MS + 2 * backhaul_km * ROUTE * FIBRE_MS_PER_KM
        kind = "lan" if F.TECH[tech]["band"] == "ism" else "upf"
    path, add = make_path(tech, d_m, link, rtt, kind, ul_bits)
    tot, st = M.simulate(path, n, seed)
    tot = tot + add
    return M.stats(tot), add, rtt


def feasible(link):
    """The link carries the slice stream lower bound down and the 0.4 Mbit/s tag uplink up."""
    return link["dl_bps"] >= F.SLICE_LO_BPS and link["ul_bps"] >= F.UL_CORE_MAC_BPS


def max_rtt_for_gate(tech, d_m, link, ul_bits, gate=30.0):
    lo, hi = 0.0, 40.0
    s0, _, _ = run_case(tech, d_m, link, 0, ul_bits, n=60_000)
    if s0["p99"] > gate:
        return None
    for _ in range(9):
        mid = (lo + hi) / 2
        path, add = make_path(tech, d_m, link, mid, "lan" if F.TECH[tech]["band"] == "ism" else "upf", ul_bits)
        tot, _ = M.simulate(path, 60_000, 11)
        if np.percentile(tot + add, 99) <= gate:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    lines = []

    def p(s=""):
        lines.append(s)
        print(s)

    res = {}
    p("FAR LINK LATENCY · input to photon p99 (ms), gate 30 ms · sim/latency/model.py + the far link terms")
    p("link from farlink.py, 90 %% shadow margin, BTK rules, Leaf as designed. N = %d actions per cell." % N)
    p("'--' = the link does not carry 25 Mbit/s down and 0.41 Mbit/s up at that distance (no stream).")
    p("")
    for ul_name, ul_bits in (("input 200 B (the sim packet)", IN_SMALL_BITS),
                             ("input 3.4 kB (touch batch with an ML-DSA-65 signature)", IN_SIGNED_BITS)):
        p("input packet: %s" % ul_name)
        p("  %-40s %-26s " % ("radio", "Core position") + " ".join("%8s" % ("%g m" % d if d < 1000 else "%g km" % (d / 1000)) for d in DIST))
        for name, tech, scen, g in CONFIGS:
            links = {d: F.link(tech, scen, d, g, "TR") for d in DIST}
            for bname, bkm in BACKHAUL + [("far validator 80 ms", None)]:
                cells = []
                for d in DIST:
                    lk = links[d]
                    if not feasible(lk):
                        cells.append("--")
                        continue
                    s, add, rtt = run_case(tech, d, lk, bkm or 0, ul_bits, far80=(bkm is None), n=N // 2)
                    cells.append("%.1f" % s["p99"])
                    res.setdefault(ul_name, {}).setdefault(name, {}).setdefault(bname, {})[str(d)] = dict(
                        p99=s["p99"], mean=s["mean"], p999=s["p999"], frac_over_30=s["frac_over_30"], add_ms=add, rtt_ms=rtt,
                        dl_mbps=lk["dl_bps"] / 1e6, ul_mbps=lk["ul_bps"] / 1e6)
                p("  %-40s %-26s " % (name[:40], bname) + " ".join("%8s" % c for c in cells))
            p("")
        p("")
    # the backhaul budget
    p("the backhaul round trip the 30 ms p99 leaves (ms, between the radio and the Core), input 200 B")
    p("  %-40s " % "radio" + " ".join("%8s" % ("%g m" % d if d < 1000 else "%g km" % (d / 1000)) for d in DIST))
    bud = {}
    for name, tech, scen, g in CONFIGS:
        cells = []
        for d in DIST:
            lk = F.link(tech, scen, d, g, "TR")
            if not feasible(lk):
                cells.append("--")
                continue
            m = max_rtt_for_gate(tech, d, lk, IN_SMALL_BITS)
            cells.append("fail" if m is None else "%.1f" % m)
            bud.setdefault(name, {})[str(d)] = m
        p("  %-40s " % name[:40] + " ".join("%8s" % c for c in cells))
    f20, f100, f500 = (2 * k * ROUTE * FIBRE_MS_PER_KM for k in (20, 100, 500))
    p("  fibre RTT: 20 km at route 1.5 = %.2f ms, 100 km = %.2f ms, 500 km = %.2f ms (plus %.1f ms of equipment)"
      % (f20, f100, f500, EQUIP_MS))
    p("  propagation in air, whole path: %.2f us per km each way, %.1f us per km on the round trip" % (1e3 / C_KM_MS, 2e3 / C_KM_MS))
    res["backhaul_budget_ms"] = bud
    with open(os.path.join(OUT, "latency.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(OUT, "latency.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
