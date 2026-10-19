#!/usr/bin/env python3
"""twohosts.py - the energy host and the compute host. Question 2 of the order of Ayaz.

Power does not travel kilometres, so at C2 the Leaf energy is local (its own cell, or a near host
of Part 22) and the compute is a remote Core. This file puts numbers on it:

  1. the radio duty that a long link needs (the Leaf antennas are as designed), by distance;
  2. the Leaf load at C2 with the loads of hw/energy/04, the radio term replaced;
  3. the run time on the cell alone, and the energy a near host gives per hour;
  4. the heat against the free-air limit of Part 22.5;
  5. a free sweep of the radio duty, so the table does not depend on the link model.

Read only: hw/energy/out/budget.json, hw/hostpower/powerpath/hosts.py, fleet.py of this seat.
Run:   python3 twohosts.py        Out: out/twohosts.txt, out/twohosts.json
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fleet as F  # noqa: E402

ROOT, OUT = F.ROOT, F.OUT
HOSTS = F.load_module("hostpower_hosts", os.path.join(ROOT, "hw", "hostpower", "powerpath", "hosts.py"),
                      os.path.join(ROOT, "hw", "hostpower", "powerpath"))
EN = json.load(open(os.path.join(ROOT, "hw", "energy", "out", "budget.json")))

# --------------------------------------------------------------------------- the Leaf loads, hw/energy/04 [TREE]
ETA_BODY, ETA_B, R_PATH, V_BUS = 0.92, 0.90, 0.050, 3.80
USABLE, ETA_BCELL = 0.96, 0.95
# W at the load. body = display + address. ring_other = hub + authority. radio_wifi is the Wi-Fi radio of the table.
# THE RULING (Ayaz, 2026-10-19): the B module keeps the camera, the transducers, the antennas, the radio front end and, at C1
# and C2, the link PHY, slice decoder, frame store, compositor and a hardened identity element. The wallet signer, the session,
# the AI, the image processing and the energy host are in the Core. So the B module loses the secure element signing,
# and the authority domain (U7, U8, U4: 0.12 W in the delta row) falls to the identity element, the IMU and U4.
AUTH_L60 = 0.12
AUTH_RULED = 0.07        # [HYPOTHESIS] identity element 0.015, IMU and sensors 0.03, U4 housekeeping 0.005, pairing crypto 0.02
AUTH_IDLE_L60, AUTH_IDLE_RULED = 0.020, 0.012
LOADS_L60 = {
    "idle":  dict(body=0.000, ring_other=0.005 + AUTH_IDLE_L60, radio_wifi=0.030, radio_5g_near=0.050),
    "delta": dict(body=0.800, ring_other=0.700 + AUTH_L60, radio_wifi=0.400, radio_5g_near=0.600),
    "video": dict(body=1.350, ring_other=1.200 + AUTH_L60, radio_wifi=0.600, radio_5g_near=1.100),
}
LOADS = {
    "idle":  dict(body=0.000, ring_other=0.005 + AUTH_IDLE_RULED, radio_wifi=0.030, radio_5g_near=0.050),
    "delta": dict(body=0.800, ring_other=0.700 + AUTH_RULED, radio_wifi=0.400, radio_5g_near=0.600),
    "video": dict(body=1.350, ring_other=1.200 + AUTH_RULED, radio_wifi=0.600, radio_5g_near=1.100),
}
# radio_5g_near: delta [HYPOTHESIS] (the 5G voice call of the table is 0.55 W with little data), video 1.10 W
# [TREE] hw/energy/04, "video outdoors, 5G" radio column; idle [HYPOTHESIS] a 5G inactive state.
STORES = {   # Wh nominal [TREE] hw/energy/04 Section 2
    "Full S 750 Wh/L": 7.38, "Full G 600 Wh/L": 5.90,
    "Buffer 20 cells S": 20 * 7.38 / 128, "Buffer 20 cells G": 20 * 5.90 / 128,
}
B_CELL_WH = 20.0 * 8.0 * 1.5 * 1e-6 * 600.0       # 0.144 Wh [TREE]
LIMIT_STILL, LIMIT_WIND, PLATE_W = 1.73, 2.37, 5.7   # W, [TREE] Part 22.5, hw/hostpower/thermal
K_PER_W = 10.0                                    # K per W above the limit load [HYPOTHESIS], from 41.3 vs 36.2 C at 2.24 W
CELL_W_PER_CELL = 0.164                           # W per cell at 3 C, S variant [TREE] hw/hostpower/powerpath/tiers.py


def battery_w(load, radio_w):
    pb = load["body"]
    pB = load["ring_other"] + radio_w
    p = pb / ETA_BODY + pB / ETA_B
    i = p / V_BUS
    return p + i * i * R_PATH


def hours(wh_nominal, p_w, with_b=True):
    e = wh_nominal * USABLE + (B_CELL_WH * USABLE * ETA_BCELL if with_b else 0.0)
    return e / p_w


# --------------------------------------------------------------------------- the radio state of the Leaf at C2
RX_FLOOR, RX_ACTIVE, TX_CHAIN = 0.12, 1.10, 0.30      # W, a sub-6 5G modem at 100 MHz, 2 branches [HYPOTHESIS]
PA_ETA_MAX = 0.35                                      # at 23 dBm [HYPOTHESIS]


def pa_dc_w(p_rf_dbm, p_max_dbm=23.0):
    p_rf = 10 ** (p_rf_dbm / 10) / 1000.0
    eta = max(0.04, PA_ETA_MAX * math.sqrt(p_rf / (10 ** (p_max_dbm / 10) / 1000.0)))
    return p_rf / eta


def link_state(p, a, d_m, k_load=2):
    """Receive duty, transmit duty and transmit power of one Leaf at the ground distance d_m, with k_load layers
    running in the sector. LOS and NLOS are weighted by the LOS probability. Returns None when no link closes."""
    d = np.array([d_m], dtype=float)
    pl = F.pl_uma if p["urban"] else F.pl_rma
    los, nlos, plos = pl(d, p)
    pls = np.array([los[0], nlos[0]])
    wts = np.array([plos[0], 1 - plos[0]])
    n = p["n_elem"]
    env = p["env_db"] + p["body_db"]
    bw = p["bw_mhz"] * 1e6
    rb_hz = 12 * p["scs_khz"] * 1e3
    noise_ue = -174 + 10 * math.log10(bw) + p["nf_ue"]
    pr1 = p["p_tot_dbm"] + p["g_elem"] + 10 * math.log10(n) - pls - env + p["leaf_gain_db"]
    s1 = 10 ** ((pr1 - noise_ue) / 10)
    noise_srs = -174 + 10 * math.log10(p["srs_prb"] * rb_hz) + p["nf_bs"]
    rho_p = 10 ** ((p["p_ue_dbm"] + p["leaf_gain_db"] - p["body_db"] + p["g_elem"] + 10 * math.log10(n)
                    - pls - p["env_db"] - noise_srs) / 10) * p["srs_accum"] * p["csi_q"]
    eps2 = 1 / (1 + rho_p)
    k = min(k_load, n // 4)
    sk = s1 / k * (n - k + 1) / n
    sinr = (1 - eps2) * sk / (1 + (k - 1) * eps2 * sk / n)
    ok = sinr >= 10 ** (p["sinr_min_db"] / 10)
    se = np.where(ok, np.minimum(p["se_max_dl"], p["kappa"] * np.log2(1 + sinr)), 0)
    rate_layer = bw * p["dl_frac"] * p["ovh_dl"] * se / 1e6
    with np.errstate(divide="ignore"):
        f = np.where(se > 0, a["dl_mbps"] / np.maximum(rate_layer, 1e-9), np.inf)
    duty_dl = float((wts * f).sum())
    # uplink: open-loop power control to a receive SNR of 12 dB over the allocation, capped at the SAR power;
    # the allocation starts at 8 PRBs and widens until the rate fits. A floor: one UL slot per transmit opportunity.
    need = a["ul_mbps"] * 1.1 * 1e6
    g_up = p["leaf_gain_db"] - p["body_db"] + p["g_elem"] + 10 * math.log10(n)
    res = []
    for w, plv in zip(wts, pls):
        got = None
        for nrb in (8, 16, 32, 64, 128, 273):
            noise = -174 + 10 * math.log10(nrb * rb_hz) + p["nf_bs"]
            p_tx = min(p["p_ue_dbm"], noise + 12.0 - g_up + plv + p["env_db"])
            snr = 10 ** ((p_tx + g_up - plv - p["env_db"] - noise) / 10)
            se_u = min(p["se_max_ul"], p["kappa"] * math.log2(1 + snr)) if snr >= 10 ** (-0.9) else 0.0
            rate = nrb * rb_hz * se_u * p["ul_frac"] * p["ovh_ul"]
            if rate >= need:
                share = need / rate
                duty = max(p["ul_frac"] * share, a["txop"] * 0.0005)
                got = (p_tx, duty)
                break
        res.append((w, got))
    ok_w = sum(w for w, r in res if r is not None)
    if ok_w < 0.9:
        return dict(fail="UL", ul_cover=ok_w, duty_dl=duty_dl)
    ptx = sum(w * r[0] for w, r in res if r is not None) / ok_w
    duty_ul = sum(w * r[1] for w, r in res if r is not None) / ok_w
    if not np.isfinite(duty_dl) or duty_dl > p["dl_frac"]:
        return dict(fail="DL", ul_cover=ok_w, duty_dl=duty_dl)
    return dict(duty_dl=duty_dl, duty_ul=duty_ul, ptx=ptx, ul_cover=ok_w)


def radio_model_w(duty_dl, duty_ul, ptx_dbm):
    return (RX_FLOOR + min(duty_dl, 1.0) * (RX_ACTIVE - RX_FLOOR)
            + duty_ul * (TX_CHAIN + pa_dc_w(ptx_dbm)))


def radio_w_at(p, act, d_m, k_load=2):
    """The Leaf radio power at C2: the near-cell figure of hw/energy plus the model increment over 300 m outdoors."""
    a = F.activity(p, act)
    near = link_state(dict(p, env_db=0.0, urban=1), a, 300.0, k_load)
    st = link_state(p, a, d_m, k_load)
    if st is None or near is None or "fail" in st or "fail" in near:
        return st if st is not None else None
    base = radio_model_w(near["duty_dl"], near["duty_ul"], near["ptx"])
    here = radio_model_w(st["duty_dl"], st["duty_ul"], st["ptx"])
    w = LOADS[act]["radio_5g_near"] + (here - base)
    return dict(radio_w=w, **st, near_model=base, here_model=here)



def ul_max_rate_mbps(p, d_m, pue=None):
    """The most that a SAR-limited Leaf can send up at the ground distance d_m: full power, the best PRB count, all UL slots,
    one Leaf alone in the sector. LOS and NLOS weighted. [HYPOTHESIS]"""
    d = np.array([d_m], dtype=float)
    pl = F.pl_uma if p["urban"] else F.pl_rma
    los, nlos, plos = pl(d, p)
    pls = [float(los[0]), float(nlos[0])]
    wts = [float(plos[0]), 1 - float(plos[0])]
    n = p["n_elem"]
    rb_hz = 12 * p["scs_khz"] * 1e3
    g_up = p["leaf_gain_db"] - p["body_db"] + p["g_elem"] + 10 * math.log10(n)
    tot = 0.0
    for w, plv in zip(wts, pls):
        best = 0.0
        for nrb in (1, 2, 4, 8, 16, 32, 64, 128, 273):
            noise = -174 + 10 * math.log10(nrb * rb_hz) + p["nf_bs"]
            snr = 10 ** (((pue if pue is not None else p["p_ue_dbm"]) + g_up - plv - p["env_db"] - noise) / 10)
            se = min(p["se_max_ul"], p["kappa"] * math.log2(1 + snr)) if snr >= 10 ** (-0.9) else 0.0
            best = max(best, nrb * rb_hz * se * p["ul_frac"] * p["ovh_ul"])
        tot += w * best
    return tot / 1e6


def friis_uw(d_m, eirp_dbm=36.0, f_hz=915e6, g_rx_dbi=2.0, eta=0.5):
    lam = 3e8 / f_hz
    pr_w = 10 ** (eirp_dbm / 10) / 1000.0 * 10 ** (g_rx_dbi / 10) * (lam / (4 * math.pi * d_m)) ** 2
    return pr_w * eta * 1e6


# --------------------------------------------------------------------------- the report
def host_wh_per_h(hid, p_load_vbus):
    """Host energy per hour of Leaf for the VBUS load, by the chain of hw/hostpower/powerpath/hosts.py."""
    h = next(x for x in HOSTS.HOSTS if x["id"] == hid)
    eta = float(np.prod([e for _, e in h["chain"]]))
    pin, _ = HOSTS.leaf_side(p_load_vbus, h["v_vhv"])
    return pin / eta + h["overhead_w"], h


def main():
    L = []

    def pr(s=""):
        L.append(s)
        print(s)

    p = dict(F.BASE)
    out = {}
    pr("FLEET seat · the two hosts · energy and heat of a Leaf at C2 (the B module as ruled, the compute remote)")
    pr("Loads: hw/energy/04 with the authority domain cut by the ruling. At C2 the Wi-Fi radio is replaced by a 5G radio. Near-cell 5G radio: idle %.3f, delta %.2f, video %.2f W."
       % tuple(LOADS[a]["radio_5g_near"] for a in ("idle", "delta", "video")))
    pr("The model adds the increment of the radio duty over a Leaf at 300 m outdoors. Heat limit: free air %.2f W still, %.2f W light wind, dock plate %.1f W."
       % (LIMIT_STILL, LIMIT_WIND, PLATE_W))
    pr("")
    pr("1 · the Leaf at C0 and C1, Wi-Fi radio, under the ruling (W at the cells, hours on the cell alone)")
    pr("  The ruling cuts the authority domain from %.2f to %.2f W. The L.6.0 value is in the last column." % (AUTH_L60, AUTH_RULED))
    pr("  %-8s %8s %9s %9s %9s %9s %9s" % ("activity", "W", "Full S h", "Full G h", "Buf S min", "B cell min", "L.6.0 W"))
    base = {}
    for act in ("idle", "delta", "video"):
        w = battery_w(LOADS[act], LOADS[act]["radio_wifi"])
        base[act] = dict(W=w, full_s=hours(STORES["Full S 750 Wh/L"], w), full_g=hours(STORES["Full G 600 Wh/L"], w),
                         buf_s_min=60 * hours(STORES["Buffer 20 cells S"], w, with_b=True),
                         b_min=60 * B_CELL_WH * USABLE * ETA_BCELL / (LOADS[act]["ring_other"] + LOADS[act]["radio_wifi"]))
        b = base[act]
        b["W_l60"] = battery_w(LOADS_L60[act], LOADS_L60[act]["radio_wifi"])
        pr("  %-8s %8.3f %9.2f %9.2f %9.1f %9.1f %9.3f" % (act, b["W"], b["full_s"], b["full_g"], b["buf_s_min"], b["b_min"], b["W_l60"]))
    pr("  check: hw/energy/04 gives delta 2.242 W, video 3.646 W, Full S 3.2 h and 2.0 h, for the L.6.0 split (last column).")
    out["base_wifi"] = base
    pr("")

    configs = [("l60", "L.6.0 split: the wallet in the Leaf, key inline, ACK 1.5 %, 8 dB", dict(ul_mode=0, ack_share=0.015, env_db=8.0)),
               ("ruled8", "the RULED split: wallet signer in the Core, ACK 1.5 %, 8 dB", dict(ul_mode=3, ack_share=0.015, env_db=8.0)),
               ("lean8", "the ruled split with ACK 0.3 %, 8 dB", dict(ul_mode=3, ack_share=0.003, env_db=8.0)),
               ("lean0", "the ruled split with ACK 0.3 %, outdoors 0 dB", dict(ul_mode=3, ack_share=0.003, env_db=0.0))]
    for tag, lab, over in configs:
        pr("2 · the Leaf at C2 (loads of the %s), %s; sector loaded with 2 layers, Leaf at 20 dBm" % ("L.6.0 split" if tag == "l60" else "ruled split", lab))
        pr("  %6s %-6s %7s %7s %7s %8s %8s | %7s %8s %9s %9s %8s" % (
            "km", "act", "dutyDL", "dutyUL", "Ptx dBm", "radio W", "Leaf W", "heat", "Full S h", "Buf S min", "B cell m", "cells pk"))
        rows = {}
        for dkm in (0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0):
            for act in ("delta", "video"):
                q = dict(p, **over)
                if dkm >= 5.0:
                    q["urban"] = 0
                r = radio_w_at(q, act, dkm * 1000.0)
                key = "%s_%s_%.1f" % (tag, act, dkm)
                if r is None or "fail" in r:
                    why = (r or {}).get("fail", "?")
                    pr("  %6.1f %-6s   no link: the %s does not close (%s)" % (
                        dkm, act, why, "receive duty over the DL share of 0.74" if why == "DL" else "the SAR uplink is too weak for the signed traffic"))
                    rows[key] = dict(km=dkm, act=act, fail=why)
                    continue
                ld = LOADS_L60 if tag == "l60" else LOADS
                w = battery_w(ld[act], r["radio_w"])
                heat = "ok" if w <= LIMIT_STILL else ("wind" if w <= LIMIT_WIND else ("plate" if w <= PLATE_W else "FAIL"))
                cells = math.ceil((8.7 + (r["radio_w"] - ld[act]["radio_5g_near"])) / CELL_W_PER_CELL)
                rows[key] = dict(km=dkm, act=act, duty_dl=r["duty_dl"], duty_ul=r["duty_ul"], ptx=r["ptx"], radio_w=r["radio_w"],
                                 leaf_w=w, heat=heat, full_s_h=hours(STORES["Full S 750 Wh/L"], w),
                                 full_g_h=hours(STORES["Full G 600 Wh/L"], w),
                                 buf_s_min=60 * hours(STORES["Buffer 20 cells S"], w),
                                 b_min=60 * B_CELL_WH * USABLE * ETA_BCELL / (ld[act]["ring_other"] + r["radio_w"]),
                                 cells_peak=cells, ul_cover=r["ul_cover"])
                x = rows[key]
                pr("  %6.1f %-6s %7.3f %7.3f %7.1f %8.3f %8.3f | %7s %8.2f %9.1f %9.1f %8d" % (
                    dkm, act, x["duty_dl"], x["duty_ul"], x["ptx"], x["radio_w"], x["leaf_w"], x["heat"], x["full_s_h"],
                    x["buf_s_min"], x["b_min"], x["cells_peak"]))
        out["c2_" + tag] = rows
        pr("  heat: ok at or under %.2f W free air still; wind at or under %.2f W; plate at or under %.1f W (dock or cradle); FAIL beyond." % (
            LIMIT_STILL, LIMIT_WIND, PLATE_W))
        pr("")

    pr("3 · the radio duty as a free parameter. Leaf W and Full S hours, delta session, radio = near figure plus the duty terms")
    pr("  duty is the share of the time that the receiver decodes data. The UL duty is the share that the PA transmits.")
    pr("  %7s %7s %8s | %8s %8s %8s" % ("dutyDL", "dutyUL", "Ptx dBm", "radio W", "Leaf W", "Full S h"))
    near_w = radio_model_w(0.10, 0.01, 0.0)
    sweep = []
    for ddl in (0.1, 0.25, 0.5, 0.75, 1.0):
        for dul, ptx in ((0.02, 0.0), (0.10, 10.0), (0.20, 20.0)):
            rw = LOADS["delta"]["radio_5g_near"] + radio_model_w(ddl, dul, ptx) - near_w
            w = battery_w(LOADS["delta"], rw)
            sweep.append(dict(duty_dl=ddl, duty_ul=dul, ptx=ptx, radio_w=rw, leaf_w=w, full_s_h=hours(STORES["Full S 750 Wh/L"], w)))
            pr("  %7.2f %7.2f %8.0f | %8.3f %8.3f %8.2f" % (ddl, dul, ptx, rw, w, hours(STORES["Full S 750 Wh/L"], w)))
    out["duty_sweep"] = sweep
    pr("")

    pr("4 · the near host: energy per hour of Leaf at the host input, and the run time of a host store")
    pr("  Leaf at C2, 1 km, 8 dB, the ruled split, ACK 0.3 %. The host feeds the load. The cell floats (Part 22.4).")
    pr("  The ruling puts the energy host in the Core. At C0 that is the pad or the tether. At C2 power does not travel, so the host below is a near host.")
    r1 = {act: radio_w_at(dict(p, env_db=8.0, ul_mode=3, ack_share=0.003), act, 1000.0) for act in ("delta", "video")}
    assert all("fail" not in v for v in r1.values())
    w1 = {act: battery_w(LOADS[act], r1[act]["radio_w"]) for act in r1}
    pr("  Leaf load at 1 km: delta %.2f W, video %.2f W (Wi-Fi: %.2f, %.2f W)" % (
        w1["delta"], w1["video"], base["delta"]["W"], base["video"]["W"]))
    pr("  %-5s %-22s %10s %10s %10s %10s" % ("host", "name", "delta Wh/h", "video Wh/h", "wifi delta", "store h dlt"))
    hostrows = {}
    for hid in ("H0", "H1", "H2", "H3a", "H4a", "H5"):
        wd, h = host_wh_per_h(hid, w1["delta"])
        wv, _ = host_wh_per_h(hid, w1["video"])
        ww, _ = host_wh_per_h(hid, base["delta"]["W"])
        store = None
        if "pack_wh" in h:
            if hid == "H1":
                usable = h["pack_wh"] * 0.95 * 0.97 * 0.96
            else:
                usable = h["pack_wh"] * 0.88 * 0.98 * 0.95
            pin, _ = HOSTS.leaf_side(w1["delta"], h["v_vhv"])
            store = usable / (pin + (h["overhead_w"] if hid == "H1" else 0.0))
        hostrows[hid] = dict(name=h["name"], delta_wh_h=wd, video_wh_h=wv, wifi_delta_wh_h=ww, store_h_delta=store)
        pr("  %-5s %-22s %10.2f %10.2f %10.2f %10s" % (hid, h["name"], wd, wv, ww, "-" if store is None else "%.1f" % store))
    out["near_host"] = hostrows
    pr("  H1 and H5 hours count the host store only. The dock radios are off: at C2 the Leaf uses its own 5G.")
    pr("")

    pr("5 · what the Leaf needs when the energy host and the compute host are different places")
    pr("  numbers from hw/hostpower/continuity (Part 22.9) and hw/dock, read only")
    needs = [
        ("a compute gap, energy host alive: the Core dies, a shadow takes over", "4 to 5 frames covered by U1; cold start 133 ms p50, 152 ms p99", "hw/dock dockpair"),
        ("a compute gap, no shadow, no other Core in reach", "the local safe screen in 15 ms; the Leaf own radio finds a far validator, mean 93 ms RTT", "FINAL/21 21.5.7, session seat"),
        ("an energy gap, compute alive: host swap on a 75 s walk", "Buffer and Full: 0 frames lost in 95 % of draws, 3 at p99", "Part 22.9.1"),
        ("both at once: a vehicle stops and the cell site is cold", "live frame 0.48 s warm 5G, 2.4 s cold 5G, after the host pass", "Part 22.9.1"),
        ("a power gap longer than the store at far radio load", "Buffer 20 cells: about %.0f min of delta at 1 km, then pause on chain; Full S: %.1f h" % (
            60 * hours(STORES["Buffer 20 cells S"], w1["delta"]), hours(STORES["Full S 750 Wh/L"], w1["delta"])), "this file"),
        ("the peak at far radio: cells for 3 C", "8.7 W peak plus the radio increment needs %d cells of 128 at 1 km (8 dB), %d at 3 km outdoors" % (
            math.ceil((8.7 + r1["video"]["radio_w"] - 1.10) / CELL_W_PER_CELL),
            math.ceil((8.7 + radio_w_at(dict(p, env_db=0.0, ul_mode=3, ack_share=0.003), "video", 3000.0).get("radio_w", r1["video"]["radio_w"]) - 1.10) / CELL_W_PER_CELL)), "this file, tiers.py"),
    ]
    for a_, b_, c_ in needs:
        pr("  - %s: %s [%s]" % (a_, b_, c_))
    out["needs"] = needs
    pr("")
    pr("6 · power does not travel: what a far-field RF energy host could give a Leaf. 915 MHz, 36 dBm EIRP [PUBLICATION] FCC 15.247, 2 dBi, 50 % rectifier")
    pr("  %8s %12s %14s" % ("metres", "harvest uW", "short by"))
    need_w = base["delta"]["W"]
    harvest = {}
    for dm in (0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 1000.0):
        u = friis_uw(dm)
        harvest[str(dm)] = dict(uw=u, short=need_w * 1e6 / u)
        pr("  %8.1f %12.3f %14.0f" % (dm, u, need_w * 1e6 / u))
    pr("  The Leaf needs %.2f W in a delta session. Near-field contact or a pad at 0 to 2 m is the only energy host that closes (Part 22)." % need_w)
    pr("  So the energy host sits in the Core at C0 only. At C1 and C2 the energy is in a near host or the cell: the rule of necessity.")
    out["friis"] = harvest
    pr("")
    pr("7 · the photograph at C2: the image processing is in the Core, so the burst goes up the SAR-limited link (a deferred job, Part 10)")
    pr("  two payloads [HYPOTHESIS]: a fusion burst of 8 frames of 12.5 MP at 0.5 bit per pixel is 6.3 MB; one finished 50 MP frame is 12 MB.")
    pr("  %6s %6s %12s %10s %10s %10s" % ("km", "env", "max UL Mbit", "6.3 MB s", "12 MB s", "energy J"))
    ph = {}
    for env in (0.0, 8.0):
        for dkm in (0.1, 0.3, 0.5, 1.0, 2.0, 3.0):
            q = dict(p, env_db=env)
            rate = ul_max_rate_mbps(q, dkm * 1000.0)
            if rate < 0.01:
                pr("  %6.1f %6.0f %12.3f %10s %10s %10s" % (dkm, env, rate, "no link", "no link", "-"))
                continue
            t1, t2 = 6.3 * 8 / rate, 12.0 * 8 / rate
            e_j = t2 * (RX_FLOOR + TX_CHAIN + pa_dc_w(20.0))
            ph["%s_%s" % (env, dkm)] = dict(rate=rate, t_burst=t1, t_single=t2, energy_j=e_j)
            pr("  %6.1f %6.0f %12.3f %10.1f %10.1f %10.1f" % (dkm, env, rate, t1, t2, e_j))
    pr("  The live camera stream of the capacity model needs 37.5 Mbit/s up. The link carries it only where the table shows 40 Mbit/s or more.")
    pr("  The energy is small against a cell of 26 kJ (Full S). The time is the cost: seconds at 1 km, minutes beyond 2 km.")
    out["photo"] = ph
    with open(os.path.join(OUT, "twohosts.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    with open(os.path.join(OUT, "twohosts.txt"), "w") as f:
        f.write("\n".join(L) + "\n")
    return out


if __name__ == "__main__":
    main()
