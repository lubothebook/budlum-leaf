#!/usr/bin/env python3
"""farlink.py - the far link budget of the Core and the Leaf, 100 m to 10 km.

Block HP-3, seat far link. Study only. Every number is [HYPOTHESIS] unless the
tag says otherwise. Distance classes of hw/core/BRIEF.md Section 8: C0 contact,
C1 room, C2 far. This model covers C1 (100 m) and C2 (300 m to 10 km).

Run:  python3 farlink.py      writes out/budget.json, out/range.json, out/arch.json,
                              out/antenna.json, out/summary.txt

Method (all by script)
 1. Path loss: FSPL, 3GPP TR 38.901 UMa, UMi, RMa, O2I, ITU-R P.1238, P.676 (pathloss.py).
 2. Link: Core EIRP (PA and regulator), Core gain G, path loss plus a 90 % shadow margin
    (1.28 sigma), Leaf antenna gain as the designs and hw/rf give it, noise and margins.
 3. Rate: Shannon with an implementation gap, capped by the highest modulation, times the
    MAC efficiency and the duplex share, rank 1 or 2.
 4. Architectures: the rate each one needs, and the distance where it stops.
 5. The big antenna trade: range per Core gain, aperture area, beams, what it does not buy.
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import pathloss as PL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

DIST_M = [100, 300, 1000, 3000, 5000, 10000]
CORE_G = [6, 12, 18, 25]            # dBi, the order of Ayaz
C0 = 299792458.0
K_DBM_HZ = -174.0                   # kT at 290 K

# ------------------------------------------------------------------ the Leaf, as designed
# D = directivity, EFF = efficiency in dB. Sources:
#  A1 D+2.6 dBi HARDWARE/19 (L.5.0 peak gain, read as directivity), EFF -2.5 dB FINAL/21 21.4.1 [HYPOTHESIS gate RF-22]
#  A2 D+3.6 dBi HARDWARE/19, EFF -3 dB [HYPOTHESIS, the A3 target applied]
#  A3 loop -3 dB FINAL/21 21.4.1 [HYPOTHESIS]
#  A4 +8.8 dBi array gain, HARDWARE/19, RF-19 [HYPOTHESIS]
#  A5/A6 +1.8 dBi HARDWARE/19, EFF -3 dB at 3.5 GHz; 0.7 GHz is electrically small, EFF -6 dB [HYPOTHESIS]
# RF_GAP: hw/rf/out/a1_ifa.txt MoM check of the design: eta_rad 0.108 = -9.7 dB (the TL model says
# -15.3 dB). The gate target is -2.5 dB, so the gap is 7.2 dB. The stress case applies this gap to
# every Leaf antenna, because no other antenna has a hw/rf result.
RF_GAP_DB = 9.7 - 2.5
HAND_DB = 6.0                       # [HYPOTHESIS] hand grip loss on a body-worn phone-class antenna, 3 to 10 dB [GENERAL]

TECH = {
    "wifi24": dict(label="Wi-Fi 7 2.4 GHz (A1)", f=2.44, bw_dl=40e6, bw_ul=40e6, leaf_g=2.6 - 2.5, nf_leaf=6.0,
                   nf_core=5.0, p_leaf=20.0, pa_core=30.0, se_dl=7.5, se_ul=7.5, mac=0.80, duty_dl=0.75,
                   duty_ul=0.25, gap=4.0, floor=4.0, rmax_dl=2, rmax_ul=2, div=3.0, band="ism", min_bw=20e6),
    "wifi5": dict(label="Wi-Fi 7 5 GHz (A2/A3)", f=5.60, bw_dl=80e6, bw_ul=80e6, leaf_g=3.6 - 3.0, nf_leaf=6.0,
                  nf_core=5.0, p_leaf=20.0, pa_core=30.0, se_dl=7.5, se_ul=7.5, mac=0.80, duty_dl=0.75,
                  duty_ul=0.25, gap=4.0, floor=4.0, rmax_dl=2, rmax_ul=2, div=3.0, band="ism", min_bw=20e6),
    "wifi6": dict(label="Wi-Fi 7 6 GHz (A2/A3)", f=6.20, bw_dl=160e6, bw_ul=160e6, leaf_g=3.6 - 3.0, nf_leaf=6.0,
                  nf_core=5.0, p_leaf=20.0, pa_core=30.0, se_dl=7.5, se_ul=7.5, mac=0.80, duty_dl=0.75,
                  duty_ul=0.25, gap=4.0, floor=4.0, rmax_dl=2, rmax_ul=2, div=3.0, band="ism", min_bw=20e6),
    "nr35": dict(label="5G SA 3.5 GHz TDD, 80 MHz (A5/A6, U5)", f=3.60, bw_dl=80e6, bw_ul=80e6, leaf_g=1.8 - 3.0,
                 nf_leaf=7.0, nf_core=3.5, p_leaf=23.0, pa_core=49.0, se_dl=7.4, se_ul=5.5, mac=0.86,
                 duty_dl=0.74, duty_ul=0.23, gap=3.0, floor=-6.0, rmax_dl=2, rmax_ul=1, div=3.0, band="lic", min_bw=2.16e6),
    "nr07": dict(label="5G SA 700 MHz FDD, 2 x 10 MHz (A5/A6, U5)", f=0.73, bw_dl=10e6, bw_ul=10e6, leaf_g=2.0 - 6.0,
                 nf_leaf=7.0, nf_core=3.5, p_leaf=23.0, pa_core=43.0, se_dl=7.4, se_ul=5.5, mac=0.86,
                 duty_dl=1.0, duty_ul=1.0, gap=3.0, floor=-6.0, rmax_dl=2, rmax_ul=1, div=3.0, band="lic", min_bw=1.08e6),
    "v60": dict(label="60 GHz 802.11ay, 2.16 GHz (A4)", f=62.0, bw_dl=2.16e9, bw_ul=2.16e9, leaf_g=8.8,
                nf_leaf=9.0, nf_core=7.0, p_leaf=10.0, pa_core=20.0, se_dl=3.0, se_ul=3.0, mac=0.70,
                duty_dl=0.75, duty_ul=0.25, gap=4.0, floor=-1.0, rmax_dl=1, rmax_ul=1, div=0.0, band="mm", min_bw=None),
    "v60w": dict(label="60 GHz 802.11ay, 8.64 GHz bonded (A4)", f=62.0, bw_dl=8.64e9, bw_ul=8.64e9, leaf_g=8.8,
                 nf_leaf=9.0, nf_core=7.0, p_leaf=10.0, pa_core=20.0, se_dl=3.0, se_ul=3.0, mac=0.70,
                 duty_dl=0.75, duty_ul=0.25, gap=4.0, floor=-1.0, rmax_dl=1, rmax_ul=1, div=0.0, band="mm", min_bw=None),
}

# ------------------------------------------------------------------ regulator EIRP caps, dBm
# None = licensed band, no EIRP cap in the model (the PA and the licence set it).
# [PUBLICATION] BTK "Frekans Tahsisinden Muaf Telsiz Cihaz ve Sistemlerine Iliskin Teknik Olculer",
#   btk.gov.tr, Table of wideband data transmission: 2400-2483.5 MHz 100 mW e.i.r.p. (TS EN 300 328);
#   5150-5350 MHz 200 mW, indoor only; 5470-5725 MHz 1 W e.i.r.p., indoor and outdoor (TS EN 301 893);
#   57-66 GHz 40 dBm e.i.r.p., 13 dBm/MHz, not fixed outdoors (TS EN 302 567). Read 2026-10-19.
#   The extracted edition has no 5925-6425 MHz row: the 6 GHz Turkey value is [HYPOTHESIS].
# [PUBLICATION] 47 CFR 15.247(b)(3),(b)(4),(c): 1 W conducted, minus 1 dB per dB of gain over 6 dBi
#   for point-to-multipoint, so 36 dBm EIRP; fixed point-to-point 2.4 GHz minus 1 dB per 3 dB over 6 dBi;
#   5725-5850 MHz fixed point-to-point no reduction. Read from the eCFR 2026-10-19.
# [PUBLICATION] FCC 6 GHz (47 CFR 15.407, FCC fact sheet of 2021-09-09): standard power AFC access point
#   36 dBm EIRP, 23 dBm/MHz; client of it 30 dBm; low power indoor 30 dBm, client 24 dBm.
# ETSI EN 303 687 6 GHz: LPI 23 dBm EIRP indoor, VLP 14 dBm EIRP: the numbers come from a secondary
#   source (a wireless-regdb post quoting ICASA); the PDF was not readable here [HYPOTHESIS].
# FCC 15.255 60 GHz 40 dBm average EIRP: from memory [HYPOTHESIS].
REG_CORE = {
    "TR":   dict(wifi24=20.0, wifi5=30.0, wifi6=14.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
    "ETSI": dict(wifi24=20.0, wifi5=30.0, wifi6=14.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
    "FCC":  dict(wifi24=36.0, wifi5=36.0, wifi6=36.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
}
REG_LEAF = {
    "TR":   dict(wifi24=20.0, wifi5=30.0, wifi6=14.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
    "ETSI": dict(wifi24=20.0, wifi5=30.0, wifi6=14.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
    "FCC":  dict(wifi24=36.0, wifi5=36.0, wifi6=30.0, nr35=None, nr07=None, v60=40.0, v60w=40.0),
}
CORE_MISC_DB = 1.0       # feeder, radome, pointing [HYPOTHESIS]
LEAF_MISC_DB = 1.0       # polarisation and implementation [HYPOTHESIS]
NOISE_RISE_DB = 3.0      # interference and noise rise, both ways [HYPOTHESIS]
MU_SINR_CAP_DB = 22.0    # leakage between simultaneous beams [HYPOTHESIS]
ETA_AP = 0.60            # aperture efficiency of a panel or dish [GENERAL]
G_EL_ARRAY = 5.0         # patch element gain of the beamforming array, dBi [GENERAL]
SECTOR_AZ_DEG = 120.0
N_RF_MAX = 16            # hybrid array, simultaneous beams [HYPOTHESIS]

SCEN_KEYS = ["FS", "UMa-LOS", "UMa-NLOS", "UMa-NLOS+O2I-low", "UMa-NLOS+O2I-high", "RMa-LOS", "RMa-NLOS"]
LOS_LIKE = {"FS", "UMa-LOS", "RMa-LOS"}


def lg(x):
    return math.log10(x)


def leaf_gain(tech, case):
    g = TECH[tech]["leaf_g"]
    if case == "stress":
        g -= RF_GAP_DB
    return g


def cap_for(reg, tech, leaf=False):
    return (REG_LEAF if leaf else REG_CORE)[reg][tech]


def shannon_rate(snr_db, bw, se_max, gap_db, floor_db, mac, duty, rmax, pen2_db, div_db, ul=False, min_bw=None):
    """Rate in bit/s: Shannon with a gap, capped, rank 1 or 2, times MAC efficiency and duplex share.

    snr_db is the SNR over the whole bandwidth bw. When the link is power limited the scheduler
    narrows the allocation: the SNR over the allocation b is snr + 10 log10(bw / b). The best allocation
    with SNR over the floor is taken (halving steps down to min_bw). Zero if none reaches the floor."""
    best = 0.0
    b = bw
    while True:
        s_all = snr_db + 10 * math.log10(bw / b)
        if s_all >= floor_db:
            for r in range(1, rmax + 1):
                if r == 1:
                    s_db = s_all + (0.0 if ul else div_db) - gap_db
                else:
                    s_db = s_all - (3.0 if ul else 0.0) - pen2_db - gap_db
                se = r * min(se_max, math.log2(1 + 10 ** (s_db / 10)))
                best = max(best, b * se * mac * duty)
        if min_bw is None or b / 2 < min_bw:
            break
        b /= 2
    return best


def link(tech, scen, d, g_core, reg="TR", leaf_case="design", body_db=0.0, tx_backoff_db=0.0,
         shadow=True, nbeams=1):
    """One link: returns a dict with the powers, SNRs and rates (bit/s) both ways."""
    t = TECH[tech]
    fn, (lo, hi) = PL.scenarios(t["f"])[scen]
    pl, sig = fn(d, t["f"])
    sh = 1.28 * sig if shadow else 0.0
    pen2 = 8.0 if scen in LOS_LIKE else 3.0
    mu = 10 * lg(nbeams)
    # Core side
    cap = cap_for(reg, tech)
    cap_leaf_over = None
    if scen.startswith("IN") and tech == "wifi6":      # indoors the 6 GHz low power indoor class applies
        cap = {"TR": 23.0, "ETSI": 23.0, "FCC": 30.0}[reg]
        cap_leaf_over = {"TR": 23.0, "ETSI": 23.0, "FCC": 24.0}[reg]
    p_core = t["pa_core"] if cap is None else min(t["pa_core"], cap - g_core)
    p_core_beam = p_core - mu
    eirp_core = p_core_beam + g_core - CORE_MISC_DB
    g_leaf = leaf_gain(tech, leaf_case) - body_db
    # the effective Leaf antenna gain also holds the leaf efficiency loss on transmit
    rx_dl = eirp_core - pl - sh + g_leaf - LEAF_MISC_DB
    noise_dl = K_DBM_HZ + 10 * lg(t["bw_dl"]) + t["nf_leaf"]
    snr_dl = rx_dl - noise_dl - NOISE_RISE_DB
    if nbeams > 1:
        snr_dl = min(snr_dl, MU_SINR_CAP_DB)
    # Leaf side: conducted power bounded by class, SAR stress backoff and the EIRP cap
    capl = cap_for(reg, tech, leaf=True) if cap_leaf_over is None else cap_leaf_over
    p_leaf = t["p_leaf"] - tx_backoff_db
    if capl is not None:
        p_leaf = min(p_leaf, capl - g_leaf)
    eirp_leaf = p_leaf + g_leaf
    rx_ul = eirp_leaf - LEAF_MISC_DB - pl - sh + g_core - CORE_MISC_DB
    noise_ul = K_DBM_HZ + 10 * lg(t["bw_ul"]) + t["nf_core"]
    snr_ul = rx_ul - noise_ul - NOISE_RISE_DB
    if nbeams > 1:
        snr_ul = min(snr_ul, MU_SINR_CAP_DB)
    r_dl = shannon_rate(snr_dl, t["bw_dl"], t["se_dl"], t["gap"], t["floor"], t["mac"], t["duty_dl"],
                        t["rmax_dl"], pen2, t["div"], min_bw=t["min_bw"])
    r_ul = shannon_rate(snr_ul, t["bw_ul"], t["se_ul"], t["gap"], t["floor"], t["mac"], t["duty_ul"],
                        t["rmax_ul"], pen2, t["div"], ul=True, min_bw=t["min_bw"])
    return dict(tech=tech, scen=scen, d=d, g_core=g_core, reg=reg, leaf_case=leaf_case, pl=pl, sigma=sig,
                shadow_margin=sh, valid=(lo <= d <= hi), eirp_core=eirp_core, eirp_leaf=eirp_leaf,
                p_core=p_core, p_leaf=p_leaf, rx_dl=rx_dl, rx_ul=rx_ul, snr_dl=snr_dl, snr_ul=snr_ul,
                margin_dl=snr_dl + (10 * lg(t["bw_dl"] / t["min_bw"]) if t["min_bw"] else 0) - t["floor"],
                margin_ul=snr_ul + (10 * lg(t["bw_ul"] / t["min_bw"]) if t["min_bw"] else 0) - t["floor"], dl_bps=r_dl, ul_bps=r_ul,
                eirp_capped=(cap is not None and p_core >= cap - g_core - 1e-9))


# ------------------------------------------------------------------ the required rates
W, H, HZ, BITS = 1600, 3200, 240, 10
RAW_BPS = W * H * HZ * BITS * 3                      # 36.864 Gbit/s
PIX_PER_S_60 = W * H * 60                            # content at 60 Hz
# The slice stream, Part 21 with the local compositor. [HYPOTHESIS]
#  A full-screen, visually transparent 10-bit stream at 60 Hz needs 0.16 bit per pixel
#  (HEVC class HDR streams run 0.1 to 0.3 bpp [GENERAL]): 0.163 * 307 Mpx/s = 50 Mbit/s.
#  Part 21 adds two speculative frames per frame (hw/dock/validator_sizing.py SPEC_COUNT = 2): x3 = 150.
#  A video class stream (Part 5 Section 5.4, C2 and C3: 10 to 80 Mbit/s) gives the low end, 25 Mbit/s,
#  and a delta (UI) stream is far under it (C1: 10 kbit/s to 2 Mbit/s).
BPP_TRANSPARENT = 0.163
SLICE_FULL_BPS = BPP_TRANSPARENT * PIX_PER_S_60
SLICE_HI_BPS = SLICE_FULL_BPS * 3
SLICE_LO_BPS = 25e6
# the uplink: touch 480 Hz x 64 B, IMU 1 kHz x 16 B, voice Opus 32 kbit/s, and a signed batch
# (ML-DSA-65 signature 3309 B, 60 batches/s). [HYPOTHESIS]
UL_CORE_BPS = 480 * 64 * 8 + 1000 * 16 * 8 + 32e3 + 60 * 3309 * 8
UL_CORE_MAC_BPS = 480 * 64 * 8 + 1000 * 16 * 8 + 32e3 + 60 * 16 * 8   # session MAC tag instead of a signature
UL_CAM_HEVC_BPS = 40e6                               # Part 5 C4 class: 5 to 130 Mbit/s
UL_CAM_RAW_BPS = 50e6 * 10 * 30                      # 50 MP, 10 bit, 30 fps: 15 Gbit/s
ARCH = [
    ("raw pixel stream", RAW_BPS, UL_CORE_BPS),
    ("compressed pixel stream 3:1", RAW_BPS / 3, UL_CORE_BPS),
    ("compressed pixel stream 6:1", RAW_BPS / 6, UL_CORE_BPS),
    ("slice stream, upper (full screen, 2 speculative frames)", SLICE_HI_BPS, UL_CORE_BPS),
    ("slice stream, lower (video class)", SLICE_LO_BPS, UL_CORE_BPS),
]


# ------------------------------------------------------------------ range solver
def grid(lo=3.0, hi=64000.0, n=500):
    a, b = lg(lo), lg(hi)
    return [10 ** (a + (b - a) * i / (n - 1)) for i in range(n)]


def reach(fn_rate, req, lo=3.0, hi=64000.0):
    """Largest d with rate >= req, assuming the rate falls with distance. Metres. 0 = not even at 3 m."""
    g = grid(lo, hi)
    if fn_rate(g[0]) < req:
        return 0.0
    last = g[0]
    for d in g[1:]:
        if fn_rate(d) < req:
            return last
        last = d
    return hi


def fmt_d(d):
    if d <= 0:
        return "<3 m"
    if d >= 63000:
        return ">64 km"
    return "%d m" % round(d, -1) if d < 1000 else "%.1f km" % (d / 1000)


def mbps(x):
    return x / 1e6


def table_rows():
    """The full budget for the JSON file."""
    rows = []
    for tech in TECH:
        scens = ["IN", "FS", "UMa-LOS", "UMa-NLOS", "UMa-NLOS+O2I-low", "RMa-NLOS"] if tech not in ("v60", "v60w") \
            else ["IN", "FS", "UMa-NLOS+O2I-low"]
        for scen in scens:
            for reg in (("TR", "FCC") if TECH[tech]["band"] != "lic" else ("TR",)):
                for g in CORE_G:
                    for case in ("design", "stress"):
                        for d in DIST_M:
                            r = link(tech, scen, d, g, reg, case)
                            rows.append({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    return rows


def main():
    lines = []

    def p(s=""):
        lines.append(s)
        print(s)

    p("BUDLUM LEAF · THE FAR LINK · block HP-3 seat far link · study, all [HYPOTHESIS] unless tagged")
    p("")
    p("0 · the self test of the path loss models (known values)")
    for k, v in PL.selftest().items():
        p("  %-28s %s" % (k, v))
    p("")
    p("1 · the Leaf antenna gains used (realised gain = directivity + efficiency)")
    for tech, t in TECH.items():
        p("  %-46s design %+5.1f dBi   stress %+5.1f dBi   Tx class %4.1f dBm   NF %.0f dB"
          % (t["label"], leaf_gain(tech, "design"), leaf_gain(tech, "stress"), t["p_leaf"], t["nf_leaf"]))
    p("  stress = the A1 gap of hw/rf (MoM %.1f dB against the %.1f dB gate) applied to every antenna: %.1f dB"
      % (-9.7, -2.5, RF_GAP_DB))
    p("")

    # ---------------- the required rates
    p("2 · the rates the architectures need")
    for name, dl, ul in ARCH:
        p("  %-58s DL %9.1f Mbit/s   UL %6.2f Mbit/s" % (name, mbps(dl), mbps(ul)))
    p("  uplink with a 16 B session tag in place of the signature: %.2f Mbit/s" % mbps(UL_CORE_MAC_BPS))
    p("  uplink camera: HEVC class %.0f Mbit/s, raw 50 MP 10 bit 30 fps %.1f Gbit/s"
      % (mbps(UL_CAM_HEVC_BPS), UL_CAM_RAW_BPS / 1e9))
    p("  slice: %.3f bit/px x %.0f Mpx/s = %.0f Mbit/s full screen; x3 with two speculative frames = %.0f Mbit/s"
      % (BPP_TRANSPARENT, PIX_PER_S_60 / 1e6, mbps(SLICE_FULL_BPS), mbps(SLICE_HI_BPS)))
    p("")

    p("2b · the ceiling of each Leaf radio, best case, no path loss (bit/s: bandwidth x streams x top spectral efficiency x MAC)")
    ceil = {}
    for lab, bw, st, se, mac, duty in (("Wi-Fi 7 320 MHz 2x2 (6 GHz)", 320e6, 2, 7.5, 0.80, 0.75),
                                       ("5G n78 80 MHz 2 layers", 80e6, 2, 7.4, 0.86, 0.74),
                                       ("5G n28 2 x 10 MHz 2 layers", 10e6, 2, 7.4, 0.86, 1.0),
                                       ("802.11ay 8.64 GHz, 1 stream (A4)", 8.64e9, 1, 3.0, 0.70, 0.75),
                                       ("802.11ay 2.16 GHz, 1 stream (A4)", 2.16e9, 1, 3.0, 0.70, 0.75)):
        full, shared = bw * st * se * mac, bw * st * se * mac * duty
        ceil[lab] = dict(full_bps=full, shared_bps=shared)
        p("  %-36s all air time %8.2f Gbit/s   with the duplex share %8.2f Gbit/s   raw needs x%.1f   6:1 needs x%.2f"
          % (lab, full / 1e9, shared / 1e9, RAW_BPS / shared, RAW_BPS / 6 / shared))
    p("")
    # ---------------- the headline tables, G = 18 dBi, Turkey rules, design Leaf
    p("3 · the link per Leaf, Core 18 dBi, BTK rules, Leaf as designed, 90 % shadow margin, Mbit/s (DL / UL)")
    for scen in ["IN", "IN-1F", "FS", "UMa-LOS", "UMa-NLOS", "UMa-NLOS+O2I-low", "RMa-LOS", "RMa-NLOS"]:
        p("  scenario %s" % scen)
        p("  %-46s " % "radio" + " ".join("%14s" % ("%g m" % d if d < 1000 else "%g km" % (d / 1000)) for d in DIST_M))
        for tech in TECH:
            if tech in ("v60", "v60w") and scen not in ("IN", "FS", "UMa-NLOS+O2I-low"):
                continue
            cells = []
            for d in DIST_M:
                r = link(tech, scen, d, 18, "TR", "design")
                if scen.startswith("IN") and d > 100:
                    cells.append("n/a")
                    continue
                cells.append("%6.0f /%6.1f" % (mbps(r["dl_bps"]), mbps(r["ul_bps"])) + ("*" if not r["valid"] else " "))
            p("  %-46s " % TECH[tech]["label"][:46] + " ".join("%14s" % c for c in cells))
    p("  * outside the validity range of the 38.901 formula (an extrapolation)")
    p("")

    # ---------------- where each side is the limit
    p("4 · which side limits the link (margin over the SNR floor, dB; the smaller one limits). Core 18 dBi, urban NLOS, BTK")
    p("  %-46s " % "radio" + " ".join("%16s" % ("%g m" % d if d < 1000 else "%g km" % (d / 1000)) for d in DIST_M))
    limit_rows = {}
    for tech in TECH:
        cells = []
        for d in DIST_M:
            r = link(tech, "UMa-NLOS", d, 18, "TR", "design")
            side = "UL" if r["margin_ul"] < r["margin_dl"] else "DL"
            cells.append("%s %+5.0f/%+5.0f" % (side, r["margin_dl"], r["margin_ul"]))
        limit_rows[tech] = cells
        p("  %-46s " % TECH[tech]["label"][:46] + " ".join("%16s" % c for c in cells))
    p("  format: limiting side, DL margin / UL margin in dB over the floor. Negative = no link.")
    p("")

    # ---------------- range per architecture
    p("5 · the distance at which each architecture stops (best radio, Core gain 25 dBi, BTK rules, Leaf as designed)")
    arch_out = {}
    for scen in ["FS", "UMa-LOS", "RMa-LOS", "UMa-NLOS", "UMa-NLOS+O2I-low", "RMa-NLOS"]:
        p("  scenario %s" % scen)
        for name, dl, ul in ARCH:
            best = (0.0, "none")
            for tech in TECH:
                if tech in ("v60", "v60w") and scen not in ("FS",):
                    continue
                # both directions must hold: the slice rate down and the control rate up
                def f(d, tech=tech):
                    r = link(tech, scen, d, 25, "TR", "design")
                    return min(r["dl_bps"] / dl, r["ul_bps"] / ul) if True else 0
                d_ok = reach(f, 1.0)
                if d_ok > best[0]:
                    best = (d_ok, tech)
            arch_out.setdefault(scen, {})[name] = dict(range_m=best[0], radio=best[1])
            p("    %-58s %9s  (%s)" % (name, fmt_d(best[0]), TECH[best[1]]["label"] if best[1] != "none" else "no radio"))
    p("  The 60 GHz row is a free space LOS line. The other scenarios drop it (no NLOS at 60 GHz).")
    p("")

    # ---------------- per radio ranges for the slice stream, per Core gain
    p("6 · the range extension per Core gain, slice stream (DL 25 Mbit/s and 150 Mbit/s, UL 2.1 Mbit/s), Leaf as designed")
    range_out = {}
    for scen in ["UMa-LOS", "RMa-LOS", "UMa-NLOS", "UMa-NLOS+O2I-low", "RMa-NLOS"]:
        p("  scenario %s, BTK rules, km" % scen)
        p("  %-46s %-8s " % ("radio", "need") + " ".join("%9s" % ("%g dBi" % g) for g in CORE_G))
        for tech in ["wifi24", "wifi5", "wifi6", "nr35", "nr07"]:
            for label, req_dl in (("DL25", SLICE_LO_BPS), ("DL150", SLICE_HI_BPS), ("UL2.1", None)):
                cells = []
                for g in CORE_G:
                    if req_dl is None:
                        f = lambda d, g=g, tech=tech: link(tech, scen, d, g, "TR")["ul_bps"]
                        dd = reach(f, UL_CORE_BPS)
                    else:
                        f = lambda d, g=g, tech=tech: link(tech, scen, d, g, "TR")["dl_bps"]
                        dd = reach(f, req_dl)
                    cells.append(dd)
                range_out.setdefault(scen, {}).setdefault(tech, {})[label] = dict(zip([str(g) for g in CORE_G], cells))
                p("  %-46s %-8s " % (TECH[tech]["label"][:46], label) + " ".join("%9s" % fmt_d(c) for c in cells))
    p("")

    # ---------------- regulator effect on the Wi-Fi downlink
    p("7 · the regulator: the Wi-Fi downlink range (150 Mbit/s) in urban NLOS for each rule set, Core 25 dBi")
    reg_out = {}
    for tech in ["wifi24", "wifi5", "wifi6"]:
        row = []
        for reg in ("TR", "ETSI", "FCC"):
            f = lambda d, tech=tech, reg=reg: link(tech, "UMa-NLOS", d, 25, reg)["dl_bps"]
            f25 = lambda d, tech=tech, reg=reg: link(tech, "UMa-NLOS", d, 25, reg)["dl_bps"]
            r150 = reach(f, SLICE_HI_BPS)
            r25 = reach(f25, SLICE_LO_BPS)
            fu = lambda d, tech=tech, reg=reg: link(tech, "UMa-NLOS", d, 25, reg)["ul_bps"]
            ru = reach(fu, UL_CORE_BPS)
            row.append((reg, r150, r25, ru))
            reg_out.setdefault(tech, {})[reg] = dict(dl150_m=r150, dl25_m=r25, ul_m=ru,
                                                      eirp_core_dbm=link(tech, "UMa-NLOS", 1000, 25, reg)["eirp_core"])
        p("  %-28s " % TECH[tech]["label"][:28] + "   ".join(
            "%s: DL150 %s DL25 %s UL %s (EIRP %.0f dBm)" % (r, fmt_d(a), fmt_d(b), fmt_d(c),
                                                           reg_out[tech][r]["eirp_core_dbm"]) for r, a, b, c in row))
    p("")

    # ---------------- the big antenna: size
    p("8 · the Core antenna as an object: aperture for each gain (eta %.2f, square aperture, HPBW = 70 lambda / D)" % ETA_AP)
    ant = {}
    p("  %-8s %-8s %-10s %-12s %-18s %-12s %-10s" % ("band", "G dBi", "A_eff m2", "A_phys m2", "square side", "HPBW deg", "elements"))
    for tech, fgz in (("nr07", 0.73), ("wifi24", 2.44), ("nr35", 3.6), ("wifi5", 5.6), ("wifi6", 6.2), ("v60", 62.0)):
        lam = C0 / (fgz * 1e9)
        for g in CORE_G:
            gl = 10 ** (g / 10)
            ae = gl * lam ** 2 / (4 * math.pi)
            ap = ae / ETA_AP
            side = math.sqrt(ap)
            hp = min(180.0, 70 * lam / side)
            n_el = max(1, round(10 ** ((g - G_EL_ARRAY) / 10)))
            ant.setdefault(tech, {})[str(g)] = dict(f_ghz=fgz, a_eff_m2=ae, a_phys_m2=ap, side_m=side, hpbw_deg=hp,
                                                    array_elements=n_el, lambda_m=lam)
            p("  %-8s %-8d %-10.3f %-12.3f %-18s %-12.1f %-10d" % (tech, g, ae, ap, "%.2f x %.2f m" % (side, side), hp, n_el))
    p("")

    # ---------------- beams
    p("9 · beamforming: Leafs served per Core (3 sectors, 120 deg each), slice stream 150 Mbit/s, all Leafs at the range shown,")
    p("    urban NLOS, BTK rules, hybrid array with up to %d simultaneous beams, element gain %.0f dBi" % (N_RF_MAX, G_EL_ARRAY))
    beams_out = {}
    for tech in ["nr35", "nr07", "wifi5"]:
        for g in (12, 18, 25):
            lam = C0 / (TECH[tech]["f"] * 1e9)
            side = math.sqrt(10 ** (g / 10) * lam ** 2 / (4 * math.pi) / ETA_AP)
            hp = min(120.0, 70 * lam / side)
            cells_az = max(1, int(SECTOR_AZ_DEG // hp))
            n_el = max(1, round(10 ** ((g - G_EL_ARRAY) / 10)))
            nb = max(1, min(N_RF_MAX, cells_az, n_el))
            for d in (300, 1000, 3000):
                r = link(tech, "UMa-NLOS", d, g, "TR", nbeams=nb)
                per_beam = r["dl_bps"]
                agg = nb * per_beam
                n_leaf = int(agg // SLICE_HI_BPS) * 3
                n_leaf_lo = int(agg // SLICE_LO_BPS) * 3
                r1 = link(tech, "UMa-NLOS", d, g, "TR", nbeams=1)
                beams_out.setdefault(tech, {}).setdefault(str(g), {})[str(d)] = dict(
                    hpbw_deg=hp, beams=nb, per_leaf_rate_mbps=mbps(per_beam), single_beam_rate_mbps=mbps(r1["dl_bps"]),
                    leafs_150=n_leaf, leafs_25=n_leaf_lo)
                p("  %-6s G %2d dBi HPBW %5.1f deg, %2d beams, d %5d m: single beam %7.1f Mbit/s, per Leaf with %2d beams %7.1f, Leafs at 150: %3d, at 25: %3d"
                  % (tech, g, hp, nb, d, mbps(r1["dl_bps"]), nb, mbps(per_beam), n_leaf, n_leaf_lo))
    p("")

    # ---------------- what the big antenna does not buy
    p("10 · what the big Core antenna does not buy: slice stream DL 25 Mbit/s and UL 2.1 Mbit/s, urban NLOS, BTK rules, Core 25 dBi")
    nb_out = {}
    cases = [("Leaf as designed, free hand", dict(leaf_case="design", body_db=0.0, tx_backoff_db=0.0)),
             ("hand grip -6 dB", dict(leaf_case="design", body_db=HAND_DB, tx_backoff_db=0.0)),
             ("SAR stress, Tx -10 dB", dict(leaf_case="design", body_db=0.0, tx_backoff_db=10.0)),
             ("hw/rf A1 gap -7.2 dB", dict(leaf_case="stress", body_db=0.0, tx_backoff_db=0.0)),
             ("hw/rf gap + hand + SAR -10 dB", dict(leaf_case="stress", body_db=HAND_DB, tx_backoff_db=10.0))]
    for tech in ["wifi24", "wifi5", "nr35", "nr07"]:
        for scen in ("UMa-NLOS", "UMa-NLOS+O2I-low"):
            for name, kw in cases:
                fd = lambda d, tech=tech, scen=scen, kw=kw: link(tech, scen, d, 25, "TR", **kw)["dl_bps"]
                fu = lambda d, tech=tech, scen=scen, kw=kw: link(tech, scen, d, 25, "TR", **kw)["ul_bps"]
                rd, ru = reach(fd, SLICE_LO_BPS), reach(fu, UL_CORE_BPS)
                nb_out.setdefault(tech, {}).setdefault(scen, {})[name] = dict(dl25_m=rd, ul_m=ru)
                p("  %-8s %-18s %-32s DL25 %8s   UL2.1 %8s" % (tech, scen, name, fmt_d(rd), fmt_d(ru)))
    p("")

    # ---------------- the 60 GHz detail
    p("11 · 60 GHz, line of sight, A4 +8.8 dBi, Core 25 dBi, 40 dBm EIRP cap: rate per Leaf (Gbit/s, DL)")
    v60_out = {}
    for tech in ("v60", "v60w"):
        for case in ("design", "stress"):
            cells = []
            for d in (3, 10, 30, 100, 300, 1000):
                r = link(tech, "FS", d, 25, "TR", case)
                cells.append("%7.2f" % (r["dl_bps"] / 1e9))
                v60_out.setdefault(tech, {}).setdefault(case, {})[str(d)] = dict(dl_gbps=r["dl_bps"] / 1e9, ul_mbps=r["ul_bps"] / 1e6,
                                                                              snr_dl=r["snr_dl"])
            p("  %-40s %-7s d = 3, 10, 30, 100, 300, 1000 m: %s" % (TECH[tech]["label"][:40], case, " ".join(cells)))
    p("  raw stream needs %.1f Gbit/s; 6:1 needs %.1f; 3:1 needs %.1f" % (RAW_BPS / 1e9, RAW_BPS / 6e9, RAW_BPS / 3e9))
    p("  the A4 array is 1 x 4 and one polarisation, so one stream: the 802.11ay ceiling is the bandwidth times %.1f bit/s/Hz"
      % TECH["v60w"]["se_dl"])
    p("")

    # ---------------- 60 GHz reach of the pixel streams, from 1 m
    p("12 · 60 GHz reach of the pixel streams, line of sight (free space and oxygen), search from 1 m")
    v60r = {}
    for tech in ("v60", "v60w"):
        for case in ("design", "stress"):
            for g in (12, 18, 25):
                row = {}
                for nm, rate in (("raw 36.9 Gbit/s", RAW_BPS), ("3:1 12.3 Gbit/s", RAW_BPS / 3), ("6:1 6.1 Gbit/s", RAW_BPS / 6)):
                    fdl = lambda d, tech=tech, g=g, case=case: link(tech, "FS", d, g, "TR", case)["dl_bps"]
                    fb = lambda d, tech=tech, g=g, case=case: link(tech, "FS", d, g, "TR", case)["ul_bps"]
                    row[nm] = dict(dl_m=reach(fdl, rate, lo=1.0, hi=5000.0), ul2_m=reach(fb, UL_CORE_BPS, lo=1.0, hi=5000.0))
                v60r.setdefault(tech, {}).setdefault(case, {})[str(g)] = row
                p("  %-40s %-7s Core %2d dBi: " % (TECH[tech]["label"][:40], case, g) + "; ".join(
                    "%s DL to %s, UL 2 Mbit/s to %s" % (k, ("%.0f m" % v["dl_m"]) if v["dl_m"] else "never", ("%.0f m" % v["ul2_m"]) if v["ul2_m"] else "never")
                    for k, v in row.items()))
    p("")

    out = dict(
        inputs=dict(dist_m=DIST_M, core_g=CORE_G, rf_gap_db=RF_GAP_DB, hand_db=HAND_DB, core_misc_db=CORE_MISC_DB,
                    leaf_misc_db=LEAF_MISC_DB, noise_rise_db=NOISE_RISE_DB, eta_ap=ETA_AP,
                    required=dict(raw_bps=RAW_BPS, slice_hi_bps=SLICE_HI_BPS, slice_lo_bps=SLICE_LO_BPS,
                                  slice_full_bps=SLICE_FULL_BPS, ul_core_bps=UL_CORE_BPS,
                                  ul_cam_hevc_bps=UL_CAM_HEVC_BPS, ul_cam_raw_bps=UL_CAM_RAW_BPS),
                    tech={k: {kk: vv for kk, vv in v.items()} for k, v in TECH.items()},
                    reg_core=REG_CORE, reg_leaf=REG_LEAF),
        selftest=PL.selftest(), ceilings=ceil)
    with open(os.path.join(OUT, "budget.json"), "w") as fh:
        json.dump(dict(out, rows=table_rows()), fh, indent=0)
    with open(os.path.join(OUT, "range.json"), "w") as fh:
        json.dump(dict(range_m=range_out, regulator=reg_out, not_bought=nb_out), fh, indent=1)
    with open(os.path.join(OUT, "arch.json"), "w") as fh:
        json.dump(dict(reach_m=arch_out, limit_side=limit_rows, v60=v60_out, v60_reach=v60r), fh, indent=1)
    with open(os.path.join(OUT, "antenna.json"), "w") as fh:
        json.dump(dict(aperture=ant, beams=beams_out), fh, indent=1)
    with open(os.path.join(OUT, "summary.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
