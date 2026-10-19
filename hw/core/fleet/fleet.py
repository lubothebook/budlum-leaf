#!/usr/bin/env python3
"""fleet.py - how many Leafs does one Core serve? The capacity model of seat FLEET, block HP-3.

Question 1 of the order of Ayaz (hw/core/BRIEF.md Section 8): the Core can be kilometres from
the Leaf, with a large antenna, and one Core serves many screens. The Leaf keeps its antennas.
This file counts the Leafs per Core as the minimum over three limits:

  radio             the sector: beamforming, MU-MIMO layers, the slice stream down, the uplink
                    under SAR, the scheduling grants and the connected-user table
  compute           render, hash and re-execution of every session (hw/dock/validator_sizing.py,
                    validator/leaf-duty), the frame engine, the codec, the DRAM
  memory + network  session state, the frame ring, the NIC and the backhaul, the receipts

It is a model, not a measurement. Every number that no source gives is a [HYPOTHESIS] with a
range, and the Monte Carlo of main() draws all of them. The reads are read only.

Distance classes of BRIEF Section 8: C0 contact or tether up to 2 m, C1 room up to about 30 m,
C2 far, up to kilometres. They are not the link classes C0 to C4 of FINAL/05 Section 5.4.
The activities of this file are named idle, delta and video, never C1 or C2.

Run:   python3 fleet.py            (about 40 s)
Out:   out/fleet.txt, out/fleet.json
"""
import importlib.util
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


# ===================================================================== read only inputs
def load_module(name, path, extra_path=None):
    """Import a file of another seat without writing anything beside it."""
    if extra_path:
        sys.path.insert(0, extra_path)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        if extra_path:
            sys.path.remove(extra_path)
            sys.modules.pop("common", None)
    return mod


VS = load_module("dock_validator_sizing", os.path.join(ROOT, "hw", "dock", "validator_sizing.py"))
try:
    BENCH = json.load(open(os.path.join(ROOT, "hw", "dock", "out", "validator_sizing.json")))["bench"]
    BENCH_SRC = "hw/dock/out/validator_sizing.json"
except (OSError, ValueError, KeyError):
    BENCH = dict(ms_per_frame=57.3, hash_ms_per_frame=18.5, overdraw=2.254)
    BENCH_SRC = "recorded run of 2026-10-12 (hw/dock fallback)"

W, H = 1600, 3200
PIX = W * H                                   # 5.12 MP, the Leaf 160 face [TREE] FINAL/21 21.5.1
FRAME_BYTES = PIX * 4                         # RGBA8, 20.48 MB [TREE] validator/leaf-duty
HZ = 240
SLICES = 16
RASTER_MS_FULL = BENCH["ms_per_frame"] - BENCH["hash_ms_per_frame"]   # one reference core, full frame [TREE]
OVERDRAW = BENCH["overdraw"]                  # [TREE]
SIMD = VS.SIMD_SPEEDUP                        # [HYPOTHESIS] of the dock team
CHAIN_CORES, NET_CORES, CHAIN_RAM_GB = VS.CHAIN_CORES, VS.NET_CORES, VS.CHAIN_RAM_GB   # [HYPOTHESIS] dock team
SHA_LUT, PX_LUT, INFRA_LUT = VS.SHA_LUT, VS.PX_ENGINE_LUT, VS.INFRA_LUT                # [HYPOTHESIS] dock team
SHA_GBPS_FPGA = 64.0 / (64.0 / VS.SHA_ROUNDS_PER_CLK) * VS.FE_CLK_MHZ * 1e6 / 1e9      # 0.6 GB/s per core
PX_GPX_FPGA = VS.PX_PER_CLK * VS.FE_CLK_MHZ * 1e6 * 0.8 / 1e9                          # 3.84 Gpx/s per engine
LUT_PER_GBPS = SHA_LUT / SHA_GBPS_FPGA
LUT_PER_GPX = PX_LUT / PX_GPX_FPGA

# signature and key sizes [PUBLICATION] FIPS 204: ML-DSA-65 sig 3309 B, ML-DSA-87 sig 4627 B, pk 2592 B
SIG65, SIG87, PK87 = 3309, 4627, 2592
# frame header of validator/leaf-duty/src/frame.rs, session id elided: 8 + 32 + 32 + 32 + 16 x 32 + 10 [TREE]
HDR_FIXED = 8 + 32 + 32 + 32 + SLICES * 32 + 10

# ===================================================================== the parameters
# Every entry: base value. RANGES holds the (low, high) the Monte Carlo draws between.
BASE = dict(
    # --- radio, NR at C2 (3GPP TR 38.901 path loss, [PUBLICATION]; the rest [HYPOTHESIS])
    fc_ghz=3.5, bw_mhz=100.0, scs_khz=30.0, n_prb=273,
    dl_frac=0.743, ul_frac=0.229,        # DDDSU with S 10:2:2 [TREE] sim/latency
    ovh_dl=0.75, ovh_ul=0.80,            # reference signals, PDCCH, DMRS
    n_elem=256, g_elem=6.0,              # the large Core array
    p_tot_dbm=50.0,                      # 100 W conducted over the array; a 64T64R AAU is 200 W [PUBLICATION]
    nf_bs=3.0, nf_ue=7.0,
    leaf_gain_db=-2.5 + 3.0,             # A1 at -2.5 dB (RF-22) [TREE], two-branch combining +3 dB
    body_db=3.0,                         # the hand
    env_db=8.0,                          # light indoor or vehicle, outdoor is 0
    p_ue_dbm=20.0,                       # class 3 is 23 dBm, SAR back-off of 3 dB (RF-16)
    kappa=0.75, se_max_dl=5.5, se_max_ul=4.0, sinr_min_db=-6.5,
    k_max=16, k_ul_max=8,
    csi_q=0.6,                           # share of the post-array pilot SNR that the beam can use
    srs_prb=4, srs_accum=8,
    rho_cap=0.7,                         # utilisation cap that keeps the 30 ms p99 of sim/latency
    conn_active=1000, conn_inactive=8000,
    slots_per_s=2000, users_per_slot=8, cg_ul_grant_share=0.1,
    sectors=1, h_bs=25.0, urban=1,
    # --- radio, Wi-Fi 7 at C0 and C1
    wf_fc_ghz=6.5, wf_bw_mhz=320.0, wf_ap_eirp_dbm=23.0, wf_nf=6.0, wf_p_ue_dbm=20.0,
    wf_mac_eff=0.65, wf_avail=0.70, wf_mu=3.0, wf_t_ovh_us=100.0, wf_assoc=256,
    wf_room_radius_m=15.0, c0_radius_m=1.5, c0_ports=1,
    # --- activity (see ACTS)
    batches_delta=10.0, batches_video=1.0, ack_share=0.015,
    ul_mode=3,   # 3 the ruled split (wallet signer in the Core), 0 key inline, 1 key by reference, 2 MAC per batch: wallet in the Leaf
    ident_sig=2420, sign_ms=1.0,   # the identity element attests once per second: ML-DSA-44 signature 2420 B [PUBLICATION] FIPS 204
    dirty_delta=0.35, fps_delta=30.0, fps_video=60.0, spec_delta=2,
    shadow_share=0.10, sample_share=1.0 / 16.0,     # density.py C state-hot shadow, leaf-duty sample rate
    # --- compute
    sha_x=1.0, lut_x=1.0, codec_x=1.0, asic_lut_eq=10.0e6,
    # --- memory and network
    mem_x=1.0, rho_net=0.7,
)
RANGES = dict(
    n_elem=None,
    csi_q=(0.25, 1.0), env_db=None, body_db=(0.0, 6.0), p_ue_dbm=(17.0, 23.0), nf_ue=(6.0, 9.0),
    kappa=(0.55, 0.85), rho_cap=(0.5, 0.8), conn_active=(600, 1500), conn_inactive=(3000, 15000),
    users_per_slot=(4, 16), k_max=(8, 24),
    wf_mac_eff=(0.5, 0.75), wf_avail=(0.5, 0.9), wf_mu=(1.5, 4.0), wf_t_ovh_us=(60, 200),
    batches_delta=(2.0, 30.0), ack_share=(0.005, 0.03), ul_mode=None, ident_sig=(64, 2420), sign_ms=(0.5, 2.0),
    dirty_delta=(0.12, 0.6), fps_delta=(10.0, 60.0), fps_video=(30.0, 60.0),
    sha_x=(0.6, 1.6), lut_x=(0.5, 2.0), codec_x=(0.5, 1.5), asic_lut_eq=(4.0e6, 20.0e6),
    mem_x=(0.7, 1.6),
)

# the day mix of registered Leafs at the peak hour: 15 % in a session [TREE] net/discovery/density.py PEAK_CONC
MIX = dict(idle=0.85, delta=0.12, video=0.03)               # [HYPOTHESIS] the split of the 15 %


def activity(p, name, px_factor=1.0):
    """Per-session demands, the slice stream and the uplink, from the protocol sizes. [HYPOTHESIS]"""
    a = dict(name=name)
    if name == "idle":
        a.update(payload_mbps=0.0, fps=0.2, dirty=1.0 / 16, spec=0, rscale=1.0, batches=0.0,
                 receipts_per_s=0.1, root_per_s=0.1, ack_share=0.0, txop=0.2, src_in_mbps=0.001,
                 dec_mpix=0.0, enc_streams=1, ring_extra=0, state_mb=5.0, hdr_fps=0.0)
    elif name == "delta":
        a.update(payload_mbps=1.8, fps=p["fps_delta"], dirty=p["dirty_delta"], spec=p["spec_delta"], rscale=1.0,
                 batches=p["batches_delta"], receipts_per_s=1.0, root_per_s=1.0, ack_share=p["ack_share"],
                 txop=40.0, src_in_mbps=0.5, dec_mpix=0.0, enc_streams=1 + p["spec_delta"], ring_extra=0,
                 state_mb=2.0, hdr_fps=p["fps_delta"])
    elif name == "full240":
        # the worst case of hw/dock/validator_sizing.py: every pixel of every frame at 240 Hz, 2 speculative frames, not a session class
        a.update(payload_mbps=80.0, fps=240.0, dirty=1.0, spec=2, rscale=1.0, batches=10.0, receipts_per_s=1.0,
                 root_per_s=1.0, ack_share=p["ack_share"], txop=240.0, src_in_mbps=1.0, dec_mpix=0.0, enc_streams=3,
                 ring_extra=0, state_mb=2.0, hdr_fps=240.0)
    elif name == "camera":
        # the sensor stays in the B module, the image processing is in the Core, so the raw stream goes up:
        # 12.5 MP binned at 30 fps and 0.1 bit per pixel is 37.5 Mbit/s [TREE] FINAL/21 12.5 MP binned stream; bit rate [HYPOTHESIS]
        a.update(payload_mbps=2.5, fps=30.0, dirty=0.5, spec=0, rscale=0.6, batches=1.0, receipts_per_s=1.0,
                 root_per_s=1.0, ack_share=p["ack_share"], txop=60.0, src_in_mbps=0.1, dec_mpix=0.0, enc_streams=1,
                 ring_extra=0, state_mb=40.0, hdr_fps=30.0, ul_payload_mbps=37.5, isp_gops=12.5 * 30 * 60 / 1000.0)
    elif name in ("video", "video80", "video150"):
        rate = dict(video=30.0, video80=80.0, video150=150.0)[name] * px_factor
        a.update(payload_mbps=rate, fps=p["fps_video"], dirty=1.0, spec=0, rscale=0.4,
                 batches=p["batches_video"], receipts_per_s=1.0, root_per_s=1.0, ack_share=p["ack_share"],
                 txop=2.0 * p["fps_video"], src_in_mbps=rate * 0.8, dec_mpix=250.0 * px_factor,
                 enc_streams=1, ring_extra=3, state_mb=2.0, hdr_fps=p["fps_video"])
    else:
        raise KeyError(name)
    a["px_factor"] = px_factor
    a.setdefault("ul_payload_mbps", 0.0)
    a.setdefault("isp_gops", 0.0)
    shared = p["shadow_share"] + p["sample_share"]
    a["renders"] = 1 + a["spec"] + (shared if name != "idle" else shared * 0.0)
    # the wire: slice stream down, signed things up
    hdr_bytes = a["hdr_fps"] * (HDR_FIXED + 32 * (1 + a["spec"]))
    root_bytes = a["root_per_s"] * (SIG65 + 200)
    a["dl_mbps"] = a["payload_mbps"] + 8e-6 * (hdr_bytes + root_bytes)
    if p["ul_mode"] == 3:      # the ruled split: inputs under a pairing MAC, the identity element attests each second
        tx_bytes = a["batches"] * (16 + 40) + a["receipts_per_s"] * (p["ident_sig"] + 100) + 64
    elif p["ul_mode"] == 2:    # a session MAC per batch, one ML-DSA-87 signature per second over the batch chain
        tx_bytes = a["batches"] * (16 + 40) + a["receipts_per_s"] * (SIG87 + 300) + 64
    else:
        pk = PK87 if p["ul_mode"] == 0 else 0
        tx_bytes = a["batches"] * (SIG87 + pk + 200) + a["receipts_per_s"] * (SIG87 + pk + 300) + 64
    a["ul_mbps"] = 8e-6 * tx_bytes + a["ack_share"] * a["payload_mbps"] + a["ul_payload_mbps"]
    # the signatures made by the Core: the validator root each second, and under the ruled split every input batch
    # and every receipt too, because the wallet signer sits in the Core
    a["signs_per_s"] = a["root_per_s"] + ((a["batches"] + a["receipts_per_s"]) if p["ul_mode"] == 3 else 0.0)
    # compute demand of one session
    a["enc_mpix"] = a["fps"] * a["dirty"] * PIX * px_factor / 1e6 * a["enc_streams"] * (0.0 if name == "idle" else 1.0)
    a["hash_gbps"] = a["fps"] * a["dirty"] * FRAME_BYTES * px_factor * a["renders"] / 1e9
    a["touched_gpx"] = a["fps"] * a["dirty"] * OVERDRAW * a["rscale"] * PIX * px_factor * a["renders"] / 1e9
    a["raster_ref_core_s"] = a["fps"] * a["dirty"] * RASTER_MS_FULL * 1e-3 * a["rscale"] * px_factor * a["renders"]
    a["mem_mb"] = a["state_mb"] if name == "idle" else (
        (a["renders"] + 2 + a["ring_extra"]) * FRAME_BYTES * px_factor / 1e6 + a["state_mb"])
    a["mem_mb"] *= p["mem_x"]
    return a


# ===================================================================== the Cores
# One reference build per distance class. cpu: cores, speed against the reference core, SHA-256 GB/s per core,
# DRAM GB/s. Sources: hw/dock/validator_sizing.py CANDIDATES [PUBLICATION datasheets, as the dock team tags them]
# for C0 and C1. The C2 server is [HYPOTHESIS]. The MA35D row is [PUBLICATION] AMD: 8 x 4Kp60 per card,
# 35 W typical, USD 1595 at launch (a 4Kp60 stream is 498 Mpix/s).
KU15P = dict(lut=522720, w=18.0, usd=2600.0)                    # [TREE] hw/dock/validator_sizing.py FPGAS
MA35D = dict(enc=8 * 3840 * 2160 * 60 / 1e6, dec=8 * 3840 * 2160 * 60 / 1e6, w=35.0, usd=1595.0)

CORES = {
    "C0": dict(label="dock Core", cpu=dict(big=8, vs_ref=0.85, sha=1.3, membw=102.4, w=18.0, usd=700.0),
               ram_gb=16, engine=dict(kind="fpga", n=1, **KU15P),
               codec=dict(enc=500.0, dec=500.0, w=0.0, usd=0.0, n=1),     # the Orin NX encoder [HYPOTHESIS] 1 x 4Kp60
               nic=2.5, wan=1.0, radius_m=2.0, sign_per_s=600.0, isp_gops=400.0),
    "C1": dict(label="room Core", cpu=dict(big=8, vs_ref=0.95, sha=1.4, membw=204.8, w=25.0, usd=1000.0),
               ram_gb=32, engine=dict(kind="fpga", n=1, **KU15P),
               codec=dict(enc=1000.0, dec=1000.0, w=0.0, usd=0.0, n=1),   # the AGX Orin, 2 x 4Kp60 [HYPOTHESIS]
               nic=2.5, wan=1.0, radius_m=30.0, sign_per_s=1000.0, isp_gops=1000.0),
    "C2": dict(label="site Core", cpu=dict(big=192, vs_ref=1.8, sha=2.2, membw=600.0, w=900.0, usd=45000.0),
               ram_gb=1024, engine=dict(kind="fpga", n=4, **KU15P),
               codec=dict(enc=MA35D["enc"] * 4, dec=MA35D["dec"] * 4, w=MA35D["w"] * 4, usd=MA35D["usd"] * 4, n=4),
               nic=100.0, wan=100.0, radius_m=2000.0, sign_per_s=4000.0, isp_gops=100000.0),
}


def core_variant(core, kind):
    """C2 compute tiers: 'cpu' (hash and raster on the CPU), 'fpga' (the frame engine), 'asic' (the engine as a die)."""
    c = json.loads(json.dumps(CORES[core]))
    if kind == "cpu":
        c["engine"] = None
    elif kind == "asic":
        c["engine"] = dict(kind="asic", n=4, w=25.0, usd=1500.0, lut=None)
    return c


# ===================================================================== propagation, 3GPP TR 38.901
def _log10(x):
    return np.log10(x)


def pl_uma(d2d, p, hut=1.5):
    """UMa path loss in dB, LOS and NLOS, plus P(LOS). [PUBLICATION] 3GPP TR 38.901 Table 7.4.1-1."""
    fc = p["fc_ghz"]
    hbs = p["h_bs"]
    d3 = np.sqrt(d2d ** 2 + (hbs - hut) ** 2)
    dbp = 4.0 * (hbs - 1.0) * (hut - 1.0) * fc * 1e9 / 3e8
    pl1 = 28.0 + 22.0 * _log10(d3) + 20.0 * math.log10(fc)
    pl2 = 28.0 + 40.0 * _log10(d3) + 20.0 * math.log10(fc) - 9.0 * _log10(dbp ** 2 + (hbs - hut) ** 2)
    los = np.where(d2d <= dbp, pl1, pl2)
    nl = 13.54 + 39.08 * _log10(d3) + 20.0 * math.log10(fc) - 0.6 * (hut - 1.5)
    nlos = np.maximum(los, nl)
    plos = np.minimum(18.0 / d2d, 1.0) * (1 - np.exp(-d2d / 63.0)) + np.exp(-d2d / 63.0)
    return los, nlos, plos


def pl_rma(d2d, p, hut=1.5, h=5.0, w=20.0):
    """RMa path loss in dB. [PUBLICATION] 3GPP TR 38.901, recalled, to be checked by the far seat."""
    fc = p["fc_ghz"]
    hbs = 35.0
    d3 = np.sqrt(d2d ** 2 + (hbs - hut) ** 2)
    dbp = 2 * math.pi * hbs * hut * fc * 1e9 / 3e8

    def pl1(d):
        return (20 * _log10(40 * math.pi * d * fc / 3.0) + min(0.03 * h ** 1.72, 10.0) * _log10(d)
                - min(0.044 * h ** 1.72, 14.77) + 0.002 * math.log10(h) * d)
    p1 = pl1(d3)
    d3b = math.sqrt(dbp ** 2 + (hbs - hut) ** 2)
    p2 = pl1(d3b) + 40 * _log10(d3 / d3b)
    los = np.where(d2d <= dbp, p1, p2)
    nl = (161.04 - 7.1 * math.log10(w) + 7.5 * math.log10(h)
          - (24.37 - 3.7 * (h / hbs) ** 2) * math.log10(hbs)
          + (43.42 - 3.1 * math.log10(hbs)) * (_log10(d3) - 3.0) + 20 * math.log10(fc)
          - (3.2 * math.log10(11.75 * hut) ** 2 - 4.97))
    nlos = np.maximum(los, nl)
    plos = np.where(d2d <= 10, 1.0, np.exp(-(d2d - 10.0) / 1000.0))
    return los, nlos, plos


def pl_inh(d2d, p):
    """Indoor office, mixed. [PUBLICATION] 3GPP TR 38.901 InH-Office, LOS probability from the mixed model."""
    fc = p["wf_fc_ghz"]
    d3 = np.sqrt(d2d ** 2 + 1.0)
    los = 32.4 + 17.3 * _log10(d3) + 20 * math.log10(fc)
    nl = 38.3 * _log10(d3) + 17.30 + 24.9 * math.log10(fc)
    plos = np.where(d2d <= 1.2, 1.0, np.where(d2d < 6.5, np.exp(-(d2d - 1.2) / 4.7),
                                              np.exp(-(d2d - 6.5) / 32.6) * 0.32))
    return los, np.maximum(los, nl), plos


def ring_distances(radius_m, n=40, dmin=35.0):
    """Equal-area rings of a disc: each ring is one user of a uniform fleet."""
    r = radius_m * np.sqrt((np.arange(n) + 0.5) / n)
    return np.maximum(r, dmin)


# ===================================================================== the radio at C2, NR massive MIMO
def pick_config(cands, max_outage=0.10):
    """The layer count with most served Leafs among those that leave at most 10 % of the disc without a link;
    when none qualifies, the one with the least outage."""
    good = [c for c in cands if c["outage"] <= max_outage]
    if good:
        return max(good, key=lambda c: c["n"])
    return min(cands, key=lambda c: (c["outage"], -c["n"]))


def nr_capacity(p, a, d_m):
    """Leafs that one sector serves for activity `a` when the Leafs sit at the ground distances d_m
    (equal weights). Returns the limits, the layers used and the outage share. All [HYPOTHESIS]."""
    d_m = np.atleast_1d(np.asarray(d_m, dtype=float))
    n = p["n_elem"]
    pl = pl_uma if p["urban"] else pl_rma
    los, nlos, plos = pl(d_m, p)
    pls = np.stack([los, nlos])                                    # 2 x D
    wts = np.stack([plos, 1 - plos]) / d_m.size                    # 2 x D, sums to 1
    env = p["env_db"] + p["body_db"]
    bw = p["bw_mhz"] * 1e6
    noise_ue = -174 + 10 * math.log10(bw) + p["nf_ue"]
    pr1 = p["p_tot_dbm"] + p["g_elem"] + 10 * math.log10(n) - pls - env + p["leaf_gain_db"]
    s1 = 10 ** ((pr1 - noise_ue) / 10)                             # single-user array-gain SNR, 2 x D
    # the pilot: UL SRS over a few PRBs with accumulation, post-array SNR
    scs = p["scs_khz"] * 1e3
    rb_hz = 12 * scs
    noise_srs = -174 + 10 * math.log10(p["srs_prb"] * rb_hz) + p["nf_bs"]
    rho_p = 10 ** ((p["p_ue_dbm"] + p["leaf_gain_db"] - p["body_db"] + p["g_elem"] + 10 * math.log10(n)
                    - pls - p["env_db"] - noise_srs) / 10) * p["srs_accum"] * p["csi_q"]
    eps2 = 1.0 / (1.0 + rho_p)
    smin = 10 ** (p["sinr_min_db"] / 10)
    # downlink: pick the layer count K that serves the most users with at most 10 % outage
    cands = []
    for k in sorted({1, 2, 4, 6, 8, 12, 16, 24, 32}):
        if k > p["k_max"] or k > n // 4:
            continue
        sk = s1 / k * (n - k + 1) / n
        sinr = (1 - eps2) * sk / (1 + (k - 1) * eps2 * sk / n)
        ok = sinr >= smin
        wok = float((wts * ok).sum())
        if wok <= 0:
            cands.append(dict(n=0.0, k=k, outage=1.0))
            continue
        se = np.where(ok, np.minimum(p["se_max_dl"], p["kappa"] * np.log2(1 + sinr)), 0.0)
        rate_layer = bw * p["dl_frac"] * p["ovh_dl"] * se / 1e6    # Mbit/s if the Leaf had the whole layer
        f = np.where(ok, a["dl_mbps"] / np.maximum(rate_layer, 1e-9), 0.0)
        ef = float((wts * f).sum()) / wok                          # mean share of one layer, served Leafs only
        cands.append(dict(n=p["rho_cap"] * k / ef, k=k, outage=1.0 - wok))
    best = pick_config(cands)
    n_dl = best["n"]
    # uplink: the smallest PRB count that carries the rate, power concentrated on few PRBs
    nrb = np.arange(1, p["n_prb"] + 1)
    need = a["ul_mbps"] * 1.1 * 1e6
    cands_u = []
    for ku in (1, 2, 4, 8):
        if ku > p["k_ul_max"]:
            continue
        pr = (p["p_ue_dbm"] + p["leaf_gain_db"] - p["body_db"] + p["g_elem"] + 10 * math.log10(n)
              - pls - p["env_db"])                                  # 2 x D
        noise = -174 + 10 * np.log10(nrb * rb_hz) + p["nf_bs"]      # R
        snr = 10 ** ((pr[:, :, None] - noise[None, None, :]) / 10) * (n - ku + 1) / n   # 2 x D x R
        e2 = eps2[:, :, None]
        sinr = (1 - e2) * snr / (1 + (ku - 1) * e2 * snr / n)
        se = np.minimum(p["se_max_ul"], p["kappa"] * np.log2(1 + sinr))
        se = np.where(sinr >= 10 ** (-9.0 / 10), se, 0.0)           # repetition lets the UL go lower than the DL
        rate = nrb[None, None, :] * rb_hz * se * p["ul_frac"] * p["ovh_ul"]
        okr = rate >= need
        first = np.where(okr.any(axis=2), okr.argmax(axis=2) + 1, 0).astype(float)   # 2 x D
        feas = first > 0
        r1 = rate[:, :, 0]                                          # one PRB, all UL slots
        first = np.where(feas & (r1 >= need), need / np.maximum(r1, 1e-9), first)   # a share of one PRB
        wok = float((wts * feas).sum())
        if wok <= 0:
            cands_u.append(dict(n=0.0, k=ku, outage=1.0))
            continue
        en = float((wts * first).sum()) / wok
        cands_u.append(dict(n=p["rho_cap"] * ku * p["n_prb"] / en, k=ku, outage=1.0 - wok))
    best_u = pick_config(cands_u)
    n_ul = best_u["n"] if a["ul_mbps"] > 0 else float("inf")
    # control: grants per second
    g = a["txop"] * (1 + p["cg_ul_grant_share"]) + 1.0
    n_ctrl = p["rho_cap"] * p["slots_per_s"] * p["users_per_slot"] / g
    n_conn = p["conn_inactive"] if a["name"] == "idle" else p["conn_active"]
    return {
        "radio.dl": n_dl * p["sectors"], "radio.ul": n_ul * p["sectors"],
        "radio.ctrl": n_ctrl * p["sectors"], "radio.conn": n_conn * p["sectors"],
        "_k_dl": best["k"], "_k_ul": best_u["k"], "_outage_dl": best["outage"],
        "_outage_ul": best_u["outage"],
    }


# ===================================================================== the radio at C0 and C1, Wi-Fi 7
def wifi_capacity(p, a, d_m):
    d_m = np.atleast_1d(np.asarray(d_m, dtype=float))
    los, nlos, plos = pl_inh(d_m, p)
    pls = np.stack([los, nlos])
    wts = np.stack([plos, 1 - plos]) / d_m.size
    bw = p["wf_bw_mhz"] * 1e6
    noise_dl = -174 + 10 * math.log10(bw) + p["wf_nf"]
    g_ue = p["leaf_gain_db"] - p["body_db"]
    mu = p["wf_mu"]
    snr_dl = p["wf_ap_eirp_dbm"] - 10 * math.log10(mu) + g_ue - pls - noise_dl      # EIRP limit shared by MU users
    snr_dl_lin = 10 ** (snr_dl / 10)
    # two spatial streams of the Leaf when the SNR allows
    r1 = bw * 0.93 * np.minimum(10.0, np.log2(1 + snr_dl_lin / 2.0)) * 0.8 * 0.83
    streams = np.where(snr_dl > 12, 2, 1)
    rphy_dl = r1 * np.where(streams == 2, 1.8, 1.0)
    noise_ul = -174 + 10 * math.log10(bw) + 5.0
    snr_ul = p["wf_p_ue_dbm"] + g_ue + 6.0 - pls - noise_ul
    rphy_ul = bw * 0.93 * np.minimum(10.0, np.log2(1 + 10 ** (snr_ul / 10) / 2.0)) * 0.8 * 0.83
    eff = p["wf_mac_eff"]
    t_ovh = p["wf_t_ovh_us"] * 1e-6
    txop = a["txop"]
    bits_dl = a["dl_mbps"] * 1e6 / txop
    bits_ul = a["ul_mbps"] * 1e6 / txop
    air = txop * ((t_ovh / mu) + bits_dl / (rphy_dl * eff) + (t_ovh * 1.2) + bits_ul / (rphy_ul * eff))
    if a["name"] == "idle":
        air = np.full_like(air, a["txop"] * 2 * t_ovh)
    ea = float((wts * air).sum())
    n_air = p["wf_avail"] * p["rho_cap"] / ea
    n_assoc = p["wf_assoc"]
    return {"radio.dl": n_air, "radio.ul": float("inf"), "radio.ctrl": float("inf"), "radio.conn": n_assoc,
            "_airtime_per_leaf": ea}


def radio_limits(p, a, cls):
    if cls == "C2":
        return nr_capacity(p, a, ring_distances(p.get("c2_radius_m", 2000.0)))
    if cls == "C1":
        return wifi_capacity(p, a, ring_distances(p["wf_room_radius_m"], dmin=1.0))
    out = wifi_capacity(p, a, ring_distances(p["c0_radius_m"], dmin=0.3))
    out["radio.ports"] = float(p["c0_ports"])
    return out


# ===================================================================== compute, memory, network
def compute_limits(p, a, core):
    c = core
    cpu = c["cpu"]
    cores_free = 0.85 * cpu["big"] - CHAIN_CORES - NET_CORES
    lim = {}
    sha = cpu["sha"] * p["sha_x"]
    scene = 0.25 * (a["fps"] * a["renders"] / (HZ * 3.0))          # the scene build and the GPU feed [HYPOTHESIS] dock
    netc = 0.5 * (a["dl_mbps"] + a["ul_mbps"] + a["src_in_mbps"]) / 1000.0   # QUIC, 0.5 core per Gbit/s [HYPOTHESIS]
    sigc = (a["batches"] + a["receipts_per_s"]) * 150e-6 + a["signs_per_s"] * p["sign_ms"] * 1e-3   # verify 0.15 ms, sign
    eng = c["engine"]
    if eng is None:
        cores = a["hash_gbps"] / sha + a["raster_ref_core_s"] / (cpu["vs_ref"] * SIMD) + netc + sigc
        mem_bw = a["touched_gpx"] * 8.0 + a["hash_gbps"] + 0.1
        lim["compute.cpu"] = cores_free / max(cores, 1e-12)
    else:
        cores = scene + netc + sigc
        lim["compute.cpu"] = cores_free / max(cores, 1e-12)
        lut_s = (LUT_PER_GBPS * a["hash_gbps"] + LUT_PER_GPX * a["touched_gpx"]) / p["lut_x"]
        if eng["kind"] == "fpga":
            avail = eng["n"] * (0.8 * eng["lut"] - INFRA_LUT)
        else:
            avail = eng["n"] * p["asic_lut_eq"]
        lim["compute.engine"] = avail / max(lut_s, 1e-9)
        mem_bw = 0.6 * (a["touched_gpx"] / 8.31) + 0.002 + (a["dl_mbps"] + a["src_in_mbps"]) / 8000.0
    lim["compute.dram"] = 0.6 * cpu["membw"] / max(mem_bw, 1e-12)
    lim["compute.sign"] = c["sign_per_s"] * 0.8 / max(a["signs_per_s"], 1e-9)
    lim["compute.isp"] = c["isp_gops"] * 0.8 / a["isp_gops"] if a["isp_gops"] > 0 else float("inf")
    cod = c["codec"]
    lim["compute.enc"] = 0.8 * cod["enc"] * p["codec_x"] / a["enc_mpix"] if a["enc_mpix"] > 0 else float("inf")
    lim["compute.dec"] = 0.8 * cod["dec"] * p["codec_x"] / a["dec_mpix"] if a["dec_mpix"] > 0 else float("inf")
    return lim


def memnet_limits(p, a, core):
    c = core
    ram_mb = 0.8 * c["ram_gb"] * 1000.0 - (CHAIN_RAM_GB + 2.0) * 1000.0
    lim = {"memnet.ram": ram_mb / a["mem_mb"]}
    nic_per = a["dl_mbps"] + a["ul_mbps"] + a["src_in_mbps"]
    wan_per = a["src_in_mbps"] + a["ul_mbps"] + 0.05
    lim["memnet.nic"] = p["rho_net"] * c["nic"] * 1000.0 / nic_per
    lim["memnet.wan"] = p["rho_net"] * c["wan"] * 1000.0 / wan_per
    return lim


def limits(p, act, cls, core=None, px_factor=1.0):
    a = activity(p, act, px_factor)
    core = core or CORES[cls]
    d = {}
    d.update({k: v for k, v in radio_limits(p, a, cls).items()})
    d.update(compute_limits(p, a, core))
    d.update(memnet_limits(p, a, core))
    rl = {k: v for k, v in d.items() if k.startswith("radio.")}
    d["_bind_radio"] = min(rl, key=rl.get)
    return a, d


def reduce_limits(d):
    """The minimum over the three groups and the sub-limit that binds."""
    groups = {}
    for k, v in d.items():
        if k.startswith("_"):
            continue
        g = k.split(".")[0]
        if g not in groups or v < groups[g][1]:
            groups[g] = (k, v)
    top = min(groups.values(), key=lambda kv: kv[1])
    return top[1], top[0], {g: v[1] for g, v in groups.items()}, {g: v[0] for g, v in groups.items()}


def n_for(p, act, cls, core=None, px_factor=1.0):
    a, d = limits(p, act, cls, core, px_factor)
    n, bind, groups, gbind = reduce_limits(d)
    return dict(n=n, bind=bind, groups=groups, group_bind=gbind, detail=d, act=a)


def mix_by_limit(p, cls, core=None, mix=MIX, px_factor=1.0):
    """Registered Leafs per Core on each sub-limit at the peak mix. Every limit is linear in the sessions, so the
    cost of one registered Leaf on a limit is the mix-weighted sum of 1/N."""
    per = {act: limits(p, act, cls, core, px_factor)[1] for act in mix}
    keys = [k for k in per["idle"] if not k.startswith("_")]
    cost = {}
    for k in keys:
        cost[k] = sum(mix[a] / max(per[a][k], 1e-12) for a in mix if np.isfinite(per[a][k]))
    return {k: (1.0 / v if v > 0 else float("inf")) for k, v in cost.items()}


def n_mix(p, cls, core=None, mix=MIX, px_factor=1.0):
    """Registered Leafs per Core at the peak hour: the minimum over the three groups of the sub-limits."""
    nmix = mix_by_limit(p, cls, core, mix, px_factor)
    groups = {}
    for k, v in nmix.items():
        g = k.split(".")[0]
        if g not in groups or v < groups[g][1]:
            groups[g] = (k, v)
    top = min(groups.values(), key=lambda kv: kv[1])
    return dict(n=top[1], bind=top[0], groups={g: v[1] for g, v in groups.items()},
                group_bind={g: v[0] for g, v in groups.items()}, by_limit=nmix)


# ===================================================================== the Skin, for the contrast of Section 5
PIXEL_GBPS = {"raw": 36.9, "3:1": 12.3, "4:1": 9.2, "6:1": 6.1}       # [TREE] BRIEF Section 3


def skin_mode(p):
    """Skins per Core when the link carries pixels (BRIEF Section 3). A Skin has no frame store and no
    compositor, so the Core renders every pixel at 240 Hz: one render, no speculative frames."""
    out = {}
    # one Skin: full frame at 240 Hz
    hash_gbps = HZ * FRAME_BYTES / 1e9
    touched = HZ * OVERDRAW * PIX / 1e9
    lut = LUT_PER_GBPS * hash_gbps + LUT_PER_GPX * touched
    out["per_skin"] = dict(hash_gbps=hash_gbps, touched_gpx=touched, lut_k=lut / 1e3,
                           enc_mpix=HZ * PIX / 1e6)
    for cls, cd in (("C0", CORES["C0"]), ("C1", CORES["C1"])):
        eng = cd["engine"]
        avail = eng["n"] * (0.8 * eng["lut"] - INFRA_LUT)
        n_comp = avail / lut
        row = dict(compute=n_comp)
        if cls == "C0":
            # a tether per Skin: USB4 class cable, 40 Gbit/s [GENERAL]; the dock has p ports
            row["link"] = float(p["c0_ports"] * 2)
            row["link_note"] = "tether ports of the dock, 2 per dock [HYPOTHESIS], one Skin per tether"
        else:
            # 60 GHz 802.11ay: 4 channels of 2.16 GHz, 6 Gbit/s PHY each, MAC 0.7 [HYPOTHESIS]
            agg = 4 * 6.0 * 0.7
            row["link"] = {k: agg / v for k, v in PIXEL_GBPS.items() if k != "raw"}
            row["link_note"] = "60 GHz room link, 16.8 Gbit/s aggregate per Core [HYPOTHESIS]"
        out[cls] = row
    out["C2"] = dict(compute=float("nan"), link=0.0,
                     link_note="6 Gbit/s does not cross a kilometre to a Leaf antenna: BRIEF Section 8.2")
    return out


# ===================================================================== the Monte Carlo
def draw(rng, base):
    p = dict(base)
    for k, r in RANGES.items():
        if r is None:
            continue
        lo, hi = r
        v = rng.uniform(lo, hi)
        p[k] = int(round(v)) if isinstance(base[k], int) else v
    p["env_db"] = float(rng.choice([0.0, 8.0, 15.0, 25.0], p=[0.35, 0.35, 0.2, 0.1]))
    p["ul_mode"] = 3
    p["ident_sig"] = int(rng.choice([64, 666, 2420]))
    return p


def monte_carlo(n=400, seed=7, cls_list=("C0", "C1", "C2"), acts=("idle", "delta", "video", "camera"), c2_radius_m=2000.0):
    rng = np.random.default_rng(seed)
    res = {(c, a): [] for c in cls_list for a in acts}
    res.update({(c, "mix"): [] for c in cls_list})
    binds = {(c, a): {} for c in cls_list for a in list(acts) + ["mix"]}
    for _ in range(n):
        p = draw(rng, BASE)
        p["c2_radius_m"] = c2_radius_m
        for c in cls_list:
            for a in acts:
                r = n_for(p, a, c)
                res[(c, a)].append(r["n"])
                g = r["group_bind"][r["bind"].split(".")[0]]
                binds[(c, a)][g] = binds[(c, a)].get(g, 0) + 1
            m = n_mix(p, c)
            res[(c, "mix")].append(m["n"])
            binds[(c, "mix")][m["bind"]] = binds[(c, "mix")].get(m["bind"], 0) + 1
    summ = {}
    for k, v in res.items():
        v = np.array(v, dtype=float)
        v = np.where(np.isfinite(v), v, 1e9)
        summ["%s/%s" % k] = dict(p10=float(np.percentile(v, 10)), p50=float(np.percentile(v, 50)),
                                 p90=float(np.percentile(v, 90)),
                                 bind={b: round(c / n, 3) for b, c in sorted(binds[k].items(), key=lambda kv: -kv[1])})
    return summ


# ===================================================================== reach
def reach_m(p, act, env_db=None, urban=1, p_ue=None, ul_mode=None, max_outage=0.10, ack=None):
    """The largest ground distance at which one Leaf (all Leafs at that distance) still has a DL and a UL link
    with the sector idle. The Leaf uplink under SAR sets it. Bisection on the distance."""
    q = dict(p)
    q["urban"] = urban
    if env_db is not None:
        q["env_db"] = env_db
    if p_ue is not None:
        q["p_ue_dbm"] = p_ue
    if ul_mode is not None:
        q["ul_mode"] = ul_mode
    if ack is not None:
        q["ack_share"] = ack
    a = activity(q, act)
    out = {}
    for which in ("dl", "ul"):
        lo, hi = 50.0, 40000.0
        for _ in range(26):
            mid = math.sqrt(lo * hi)
            r = nr_capacity(q, a, np.array([mid]))
            ok = r["_outage_" + which] <= max_outage and (r["radio.dl"] if which == "dl" else r["radio.ul"]) > 0
            if ok:
                lo = mid
            else:
                hi = mid
        out[which] = lo
    out["reach"] = min(out["dl"], out["ul"])
    return out


# ===================================================================== the report
def fmt_n(x):
    if not np.isfinite(x) or x > 1e8:
        return "inf"
    if x >= 100:
        return "%.0f" % x
    if x >= 10:
        return "%.1f" % x
    return "%.2f" % x


def covered(d):
    return 1.0 - max(d.get("_outage_dl", 0.0), d.get("_outage_ul", 0.0))


def main(quick=False):
    L = []

    def pr(s=""):
        L.append(s)
        print(s)

    p = dict(BASE)
    p["c2_radius_m"] = 2000.0
    res = {}
    pr("FLEET seat, block HP-3 · Leafs per Core · the capacity model")
    pr("Inputs read only: %s, hw/dock/validator_sizing.py constants, validator/leaf-duty, net/discovery." % BENCH_SRC)
    pr("Every result is a [HYPOTHESIS]. The base case is one set of numbers. The Monte Carlo draws all ranges.")
    pr("")
    pr("0 · what one session costs, per activity (Leaf 160, 1600 x 3200, 240 Hz scan-out)")
    pr("  %-9s %8s %8s %7s %6s %7s %7s %7s %7s %7s" % (
        "activity", "DL Mbit", "UL kbit", "fps", "dirty", "renders", "hashGBs", "Gpx/s", "encMpix", "mem MB"))
    for act in ("idle", "delta", "video", "video80", "video150", "camera"):
        a = activity(p, act)
        pr("  %-9s %8.3f %8.1f %7.1f %6.2f %7.2f %7.3f %7.3f %7.1f %7.0f" % (
            act, a["dl_mbps"], a["ul_mbps"] * 1000, a["fps"], a["dirty"], a["renders"],
            a["hash_gbps"], a["touched_gpx"], a["enc_mpix"], a["mem_mb"]))
    pr("  THE RULING (Ayaz, 2026-10-19): the B module keeps the camera, the transducers, the antennas and the radio front end, and at C1 and C2")
    pr("  the link PHY, slice decoder, frame store, compositor and a hardened identity element. The wallet signer, the session, the AI, the image")
    pr("  processing, the validator role and the energy host sit in the Core. So the Core signs each input batch and each receipt.")
    pr("  The uplink of the ruled split is a pairing MAC per batch and one attestation per second by the identity element (ML-DSA-44, %d B)." % p["ident_sig"])
    pr("  The delta uplink: ruled %.0f kbit/s; wallet in the Leaf (L.6.0): %.0f with the key inline, %.0f by reference, %.0f with a MAC per batch."
       % tuple(activity(dict(p, ul_mode=m), "delta")["ul_mbps"] * 1000 for m in (3, 0, 1, 2)))
    pr("  Under the ruling the camera stream goes up, because the image processing is in the Core: %.1f Mbit/s of 12.5 MP binned frames." % (
        activity(p, "camera")["ul_payload_mbps"]))
    pr("")

    # ------------------------------------------------------------ the main table
    pr("1 · LEAFS PER CORE, base case. Minimum over radio, compute and memory+network.")
    pr("  C0 dock Core: Orin NX + KU15P frame engine, Wi-Fi 7 at 1.5 m, one contact pad. C1 room Core: AGX Orin + KU15P,")
    pr("  Wi-Fi 7, room radius 15 m. C2 site Core: one sector of 256 elements, 100 W, 3.5 GHz, 100 MHz TDD, Leafs in a")
    pr("  disc of 2 km, 8 dB of wall or vehicle loss, 192 cores, 4 frame engines, 4 MA35D encoders.")
    pr("  %-3s %-8s %9s  %-8s %9s %9s %9s %7s  %s" % ("cls", "activity", "Leafs", "binds", "radio", "compute", "mem+net", "covered", "sub-limit"))
    table = {}
    for cls in ("C0", "C1", "C2"):
        for act in ("idle", "delta", "video", "camera"):
            r = n_for(p, act, cls)
            table["%s/%s" % (cls, act)] = r
            cv = covered(r["detail"]) if cls == "C2" else 1.0
            pr("  %-3s %-8s %9s  %-8s %9s %9s %9s %6.0f%%  %s" % (
                cls, act, fmt_n(r["n"]), r["bind"].split(".")[0], fmt_n(r["groups"]["radio"]),
                fmt_n(r["groups"]["compute"]), fmt_n(r["groups"]["memnet"]), 100 * cv, r["bind"]))
        m = n_mix(p, cls)
        table["%s/mix" % cls] = m
        pr("  %-3s %-8s %9s  %-8s %9s %9s %9s %7s  %s" % (
            cls, "peak mix", fmt_n(m["n"]), m["bind"].split(".")[0], fmt_n(m["groups"]["radio"]),
            fmt_n(m["groups"]["compute"]), fmt_n(m["groups"]["memnet"]), "", m["bind"]))
    pr("  peak mix: %s of the registered Leafs, so one number is the registered Leafs one Core carries." % MIX)
    pr("  covered: the share of the 2 km disc that has a link. Leafs counted are those in the covered part.")
    pr("  C0 counts the Wi-Fi 7 AP of the dock. The contact pads of a dock carry one Leaf each (radio.ports = %d)." % p["c0_ports"])
    res["table"] = {k: dict(n=v["n"], bind=v["bind"], groups=v["groups"], group_bind=v["group_bind"]) for k, v in table.items()}
    pr("")

    # ------------------------------------------------------------ the detail of every sub-limit at C2
    pr("2 · every sub-limit, C2 base case (Leafs, one Core)")
    keys = [k for k in table["C2/delta"]["detail"] if not k.startswith("_")]
    pr("  %-16s " % "limit" + " ".join("%10s" % a for a in ("idle", "delta", "video", "camera")))
    for k in keys:
        pr("  %-16s " % k + " ".join("%10s" % fmt_n(table["C2/%s" % a]["detail"][k]) for a in ("idle", "delta", "video", "camera")))
    for a in ("idle", "delta", "video", "camera"):
        d = table["C2/%s" % a]["detail"]
        pr("  %s: DL layers K=%d, UL layers %d, DL outage %.1f %%, UL outage %.1f %%" % (
            a, d["_k_dl"], d["_k_ul"], 100 * d["_outage_dl"], 100 * d["_outage_ul"]))
    res["c2_sublimits"] = {a: {k: table["C2/%s" % a]["detail"][k] for k in keys} for a in ("idle", "delta", "video", "camera")}
    pr("")

    # ------------------------------------------------------------ the reach of the Leaf under SAR
    pr("3 · the REACH of a Leaf from the Core, km, with 10 % outage allowed (the sector empty). Downlink and uplink apart.")
    pr("  %-34s %8s %8s %8s %8s" % ("case", "DL km", "UL km", "reach", "model"))
    pr("  (the camera row needs 37.5 Mbit/s up: a stream beyond what a SAR-limited Leaf sends; see the photograph table of twohosts.py)")
    reach = {}
    cases = []
    for act in ("delta", "video"):
        for mode, lab in ((3, "RULED split"), (0, "L.6.0 key inline"), (2, "L.6.0 MAC + 1 sig/s")):
            cases.append((act, mode, lab, 8.0, 1, 20.0, None))
    for urban in (1, 0):
        for env in (0.0, 8.0, 15.0):
            cases.append(("delta", 3, "ruled, env %d dB" % env, env, urban, 20.0, None))
    for pu in (17.0, 23.0):
        cases.append(("delta", 3, "ruled, P_ue %d dBm" % pu, 8.0, 1, pu, None))
    cases.append(("video", 3, "ruled, ACK 0.3 %", 8.0, 1, 20.0, 0.003))
    cases.append(("camera", 3, "ruled, camera upload", 8.0, 1, 20.0, None))
    for act, mode, lab, env, urban, pu, ack in cases:
        r = reach_m(p, act, env_db=env, urban=urban, p_ue=pu, ul_mode=mode, ack=ack)
        key = "%s | %s | env %d | %s | %d dBm" % (act, lab, env, "UMa" if urban else "RMa", pu)
        reach[key] = r
        pr("  %-34s %8.2f %8.2f %8.2f %8s" % ("%s, %s" % (act, lab), r["dl"] / 1e3, r["ul"] / 1e3, r["reach"] / 1e3,
                                              ("UMa" if urban else "RMa") + " env%d" % env))
    pr("  base: 256 elements, 100 W, 3.5 GHz, 100 MHz, 3 dB hand, Leaf at 20 dBm. The far seat owns the link budget proper.")
    res["reach"] = reach
    pr("")

    # ------------------------------------------------------------ sweeps at C2
    pr("4 · C2 sweeps, Leafs per Core. Radio limit, then the minimum over all three. Covered is the share of the disc with a link.")
    pr("  The compute box of the base case holds 79 delta or 41 video sessions, so the minimum stops there. The README, Section 5, right-sizes the compute.")
    pr("  4a · the radius of the Leaf disc, km. UMa is the city, RMa is open country.")
    pr("  %6s | %-44s | %-44s" % ("radius", "urban: radio delta, radio video, covered", "rural: radio delta, radio video, covered"))
    sw = {}
    for rkm in (0.3, 0.5, 1, 2, 3, 5, 8, 10):
        row = {}
        cells = []
        for urb in (1, 0):
            q = dict(p, c2_radius_m=rkm * 1000.0, urban=urb)
            rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
            row["urban" if urb else "rural"] = dict(
                delta=rd["n"], video=rv["n"], delta_radio=rd["groups"]["radio"], video_radio=rv["groups"]["radio"],
                delta_bind=rd["bind"], video_bind=rv["bind"], delta_cov=covered(rd["detail"]), video_cov=covered(rv["detail"]))
            cells.append("%9s %-9s %9s %-9s %4.0f%% %4.0f%%" % (
                fmt_n(rd["groups"]["radio"]), rd["detail"]["_bind_radio"], fmt_n(rv["groups"]["radio"]),
                rv["detail"]["_bind_radio"], 100 * covered(rd["detail"]), 100 * covered(rv["detail"])))
        sw["radius_%s" % rkm] = row
        pr("  %6.1f | %s | %s" % (rkm, cells[0], cells[1]))
    p1 = dict(p, c2_radius_m=1000.0)
    pr("  The sweeps 4b to 4d use a disc of 1 km, where the base case covers the whole disc.")
    pr("  4b · the array size, elements (100 W total power held), radio side")
    pr("  %8s %12s %12s   %s" % ("elements", "delta radio", "video radio", "covered delta / video"))
    for ne in (16, 64, 128, 256, 512, 1024):
        q = dict(p1, n_elem=ne)
        rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
        sw["elem_%d" % ne] = dict(delta_radio=rd["groups"]["radio"], video_radio=rv["groups"]["radio"],
                                  delta_bind=rd["detail"]["_bind_radio"], video_bind=rv["detail"]["_bind_radio"],
                                  delta_cov=covered(rd["detail"]), video_cov=covered(rv["detail"]))
        pr("  %8d %12s %12s   %s / %s   %.0f%% / %.0f%%" % (ne, fmt_n(rd["groups"]["radio"]), fmt_n(rv["groups"]["radio"]),
                                                          rd["detail"]["_bind_radio"], rv["detail"]["_bind_radio"],
                                                          100 * covered(rd["detail"]), 100 * covered(rv["detail"])))
    pr("  4c · the Leaf uplink power under SAR, dBm (class 3 is 23)")
    pr("  %8s %12s %12s   %s" % ("P_ue", "delta radio", "video radio", "covered delta / video"))
    for pu in (14, 17, 20, 23):
        q = dict(p1, p_ue_dbm=float(pu))
        rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
        sw["pue_%d" % pu] = dict(delta_radio=rd["groups"]["radio"], video_radio=rv["groups"]["radio"],
                                 delta_bind=rd["detail"]["_bind_radio"], video_bind=rv["detail"]["_bind_radio"],
                                 delta_cov=covered(rd["detail"]), video_cov=covered(rv["detail"]))
        pr("  %8d %12s %12s   %s / %s   %.0f%% / %.0f%%" % (pu, fmt_n(rd["groups"]["radio"]), fmt_n(rv["groups"]["radio"]),
                                                          rd["detail"]["_bind_radio"], rv["detail"]["_bind_radio"],
                                                          100 * covered(rd["detail"]), 100 * covered(rv["detail"])))
    pr("  4d · the wall or vehicle loss between the Core and the Leaf, dB")
    pr("  %8s %12s %12s   %s" % ("env", "delta radio", "video radio", "covered delta / video"))
    for ev in (0, 8, 15, 25):
        q = dict(p1, env_db=float(ev))
        rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
        sw["env_%d" % ev] = dict(delta_radio=rd["groups"]["radio"], video_radio=rv["groups"]["radio"],
                                 delta_bind=rd["detail"]["_bind_radio"], video_bind=rv["detail"]["_bind_radio"],
                                 delta_cov=covered(rd["detail"]), video_cov=covered(rv["detail"]))
        pr("  %8d %12s %12s   %s / %s   %.0f%% / %.0f%%" % (
            ev, fmt_n(rd["groups"]["radio"]), fmt_n(rv["groups"]["radio"]), rd["detail"]["_bind_radio"],
            rv["detail"]["_bind_radio"], 100 * covered(rd["detail"]), 100 * covered(rv["detail"])))
    pr("  4e · the sectors of one mast (radio times the sectors, compute pooled in one box)")
    for sec in (1, 3):
        q = dict(p, sectors=sec)
        rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
        sw["sectors_%d" % sec] = dict(delta=rd["n"], video=rv["n"], delta_bind=rd["bind"], video_bind=rv["bind"])
        pr("  sectors %d: delta %s (%s), video %s (%s)" % (sec, fmt_n(rd["n"]), rd["bind"], fmt_n(rv["n"]), rv["bind"]))
    pr("  4f · the stream rate: video at 30, 80 and 150 Mbit/s")
    for act in ("video", "video80", "video150"):
        r = n_for(p, act, "C2")
        sw["rate_%s" % act] = dict(n=r["n"], radio=r["groups"]["radio"], bind=r["bind"])
        pr("  %-9s DL %6.1f Mbit/s: radio %s, compute %s, mem+net %s, binds %s" % (
            act, r["act"]["dl_mbps"], fmt_n(r["groups"]["radio"]), fmt_n(r["groups"]["compute"]),
            fmt_n(r["groups"]["memnet"]), r["bind"]))
    pr("  4g · the uplink design: the ruled split, then the wallet in the Leaf: key inline (validator/leaf-duty), key by reference, MAC + 1 signature per second")
    for mode, lab in ((3, "RULED split"), (0, "key inline"), (1, "key by ref"), (2, "MAC + 1 sig/s")):
        q = dict(p, ul_mode=mode)
        rd, rv = n_for(q, "delta", "C2"), n_for(q, "video", "C2")
        sw["ul_mode_%d" % mode] = dict(delta=rd["n"], video=rv["n"], ul_delta=rd["act"]["ul_mbps"], ul_video=rv["act"]["ul_mbps"],
                                       delta_bind=rd["bind"], video_bind=rv["bind"],
                                       delta_cov=covered(rd["detail"]), video_cov=covered(rv["detail"]))
        pr("  %-14s delta UL %4.0f kbit/s -> %s Leafs (%s, covered %.0f%%); video UL %4.0f kbit/s -> %s (%s, covered %.0f%%)" % (
            lab, rd["act"]["ul_mbps"] * 1e3, fmt_n(rd["n"]), rd["bind"], 100 * covered(rd["detail"]),
            rv["act"]["ul_mbps"] * 1e3, fmt_n(rv["n"]), rv["bind"], 100 * covered(rv["detail"])))
    res["sweeps"] = sw
    pr("")

    # ------------------------------------------------------------ the compute tiers
    pr("5 · the compute tier of the box (the radio held at its base case): where does the compute wall stand?")
    pr("  %-3s %-28s %9s %9s %9s %9s %9s   %s" % ("cls", "tier", "idle", "delta", "video", "mix", "full240", "wall: delta, video, full240"))
    tiers = {}
    ma = lambda c, n: dict(c, codec=dict(c["codec"], enc=c["codec"]["enc"] + n * MA35D["enc"],
                                         dec=c["codec"]["dec"] + n * MA35D["dec"]))
    variants = [("C2", "cpu", "CPU only, MA35D encoders", core_variant("C2", "cpu")),
                ("C2", "fpga", "4 FPGA frame engines", core_variant("C2", "fpga")),
                ("C2", "asic", "4 ASIC frame engines", core_variant("C2", "asic")),
                ("C1", "base", "AGX Orin + KU15P (base)", core_variant("C1", "fpga")),
                ("C1", "ma35d", "base + 1 MA35D", ma(core_variant("C1", "fpga"), 1)),
                ("C0", "base", "Orin NX + KU15P (base)", core_variant("C0", "fpga")),
                ("C0", "ma35d", "base + 1 MA35D", ma(core_variant("C0", "fpga"), 1))]
    for cls, kind, label, core in variants:
        row = {}
        for act in ("idle", "delta", "video", "full240"):
            a, d = limits(p, act, cls, core)
            row[act] = min(v for k, v in d.items() if k.startswith("compute."))
            row[act + "_bind"] = min((k for k in d if k.startswith("compute.")), key=lambda k: d[k])
            rk = [k for k in d if k.startswith("compute.") and k not in ("compute.enc", "compute.dec", "compute.isp")]
            row[act + "_render"] = min(d[k] for k in rk)
            row[act + "_render_bind"] = min(rk, key=lambda k: d[k])
        mm = n_mix(p, cls, core)
        row["mix_compute"] = mm["groups"]["compute"]
        row["mix"] = mm["n"]
        row["mix_bind"] = mm["bind"]
        tiers["%s/%s" % (cls, kind)] = row
        pr("  %-3s %-28s %9s %9s %9s %9s %9s   %s, %s, %s" % (
            cls, label, fmt_n(row["idle"]), fmt_n(row["delta"]), fmt_n(row["video"]), fmt_n(row["mix_compute"]),
            fmt_n(row["full240"]), row["delta_bind"], row["video_bind"], row["full240_bind"]))
    pr("  the render side alone (CPU, frame engine, DRAM, signer; the encoder left out), sessions per box:")
    pr("  %-3s %-28s %9s %9s %9s   %s" % ("cls", "tier", "delta", "video", "full240", "wall"))
    for cls, kind, label, core in variants:
        row = tiers["%s/%s" % (cls, kind)]
        pr("  %-3s %-28s %9s %9s %9s   %s, %s, %s" % (cls, label, fmt_n(row["delta_render"]), fmt_n(row["video_render"]),
                                                  fmt_n(row["full240_render"]), row["delta_render_bind"], row["video_render_bind"],
                                                  row["full240_render_bind"]))
    pr("  full240 is the worst case of hw/dock/validator_sizing.py: every pixel at 240 Hz with 2 speculative frames. It is not a session class.")
    pr("  (compute limit only, one box. A site buys devices to match the radio: econ.py right-sizes them.)")
    res["compute_tiers"] = tiers
    pr("")

    # ------------------------------------------------------------ the family
    pr("6 · one Core for the whole family: the pixel count scales the compute and the video rate")
    fam = {"Leaf 80": 0.5, "Leaf 160": 1.0, "Leaf 480": 72 * 240 * 240 / PIX}
    famres = {}
    for name, f in fam.items():
        r = n_for(p, "video", "C2", px_factor=f)
        d = n_for(p, "delta", "C2", px_factor=f)
        famres[name] = dict(px_factor=f, video=r["n"], delta=d["n"], video_bind=r["bind"], delta_bind=d["bind"],
                            video_compute=r["groups"]["compute"], delta_compute=d["groups"]["compute"])
        pr("  %-9s pixels x%.2f  delta %s (%s, compute %s)  video %s (%s, compute %s)" % (
            name, f, fmt_n(d["n"]), d["bind"], fmt_n(d["groups"]["compute"]), fmt_n(r["n"]), r["bind"], fmt_n(r["groups"]["compute"])))
    res["family"] = famres
    pr("")

    # ------------------------------------------------------------ the Skin
    pr("7 · the Skin, a pixel link (BRIEF Section 3), for the contrast only. The ruling keeps the slice decoder in the B module at C1 and C2.")
    sk = skin_mode(p)
    pr("  one Skin needs: hash %.1f GB/s, %.2f Gpx/s touched, %.0f k LUT, %.0f Mpix/s of link coding" % (
        sk["per_skin"]["hash_gbps"], sk["per_skin"]["touched_gpx"], sk["per_skin"]["lut_k"], sk["per_skin"]["enc_mpix"]))
    pr("  C0: compute %.1f Skins per KU15P, link %.0f (%s)" % (sk["C0"]["compute"], sk["C0"]["link"], sk["C0"]["link_note"]))
    pr("  C1: compute %.1f Skins per KU15P, link %s (%s)" % (
        sk["C1"]["compute"], {k: round(v, 1) for k, v in sk["C1"]["link"].items()}, sk["C1"]["link_note"]))
    pr("  C2: 0 (%s)" % sk["C2"]["link_note"])
    res["skin"] = sk
    pr("")

    # ------------------------------------------------------------ the Monte Carlo
    nmc = 120 if quick else 400
    pr("8 · the Monte Carlo of %d draws over every range (design held: array, boxes). Leafs per Core, p10 / p50 / p90." % nmc)
    mc = monte_carlo(nmc)
    pr("  %-12s %12s %12s %12s   %s" % ("case", "p10", "p50", "p90", "binding share"))
    for k, v in mc.items():
        pr("  %-12s %12s %12s %12s   %s" % (k, fmt_n(v["p10"]), fmt_n(v["p50"]), fmt_n(v["p90"]),
                                           ", ".join("%s %.0f%%" % (b, 100 * s) for b, s in list(v["bind"].items())[:3])))
    res["monte_carlo"] = mc
    res["base_params"] = BASE
    res["mix"] = MIX
    with open(os.path.join(OUT, "fleet.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    with open(os.path.join(OUT, "fleet.txt"), "w") as f:
        f.write("\n".join(L) + "\n")
    return res


if __name__ == "__main__":
    main(quick="--quick" in sys.argv)
