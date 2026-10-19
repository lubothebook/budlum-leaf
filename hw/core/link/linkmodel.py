#!/usr/bin/env python3
"""linkmodel.py - the pixel link of the Split: Skin to Core.

Budlum Leaf, block HP-2, seat LINK, hw/core/link/. Study only. [HYPOTHESIS]

Sections
  A. the pixel budget: tile layout, refresh, depth, codecs, use cases, partial updates,
     stretch and the place of the warp, the hinge mesh limit
  B. the link options: rate, range, power, the 60 GHz budget, the flex loss,
     the inductive power efficiency, the near-field coupler count
  C. the smallest Skin: BOM, mass, area, load, heat limit
  D. latency: Part 21 Section 21.5.7 plus the tether hop, 30 ms p99
  E. power in the link: cable and pad design
  F. connector life
  G. distance classes C0, C1, C2 and what stays on the Skin
  H. the gates HC-L1 to HC-L9, evaluated

Run:   python3 linkmodel.py          (about 40 s; writes out/)
Needs: numpy and matplotlib. scipy is not used.
Reads, never writes: sim/latency/model.py (by import, no bytecode written).
"""
import importlib.util
import io
import json
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:          # pragma: no cover
    HAVE_MPL = False

# ----------------------------------------------------------------------------
# output helper: every section prints and writes its own file
# ----------------------------------------------------------------------------


class Tee:
    def __init__(self, name):
        self.name = name
        self.buf = io.StringIO()

    def p(self, *a):
        s = " ".join(str(x) for x in a)
        print(s)
        self.buf.write(s + "\n")

    def close(self):
        with open(os.path.join(OUT, self.name), "w") as f:
            f.write(self.buf.getvalue())


SUMMARY = {}

# ----------------------------------------------------------------------------
# the fixed numbers of the program (read from hw/display, hw/energy, hw/hostpower)
# ----------------------------------------------------------------------------
W, H = 1600, 3200
NX, NY = 8, 16
TILES = NX * NY                       # 128      hw/display SPEC 1.1
TPX = 200 * 200                       # 40 000 px per tile
PX = W * H                            # 5.12 Mpx
PKT = 1.06                            # packet, CRC, sync share, display team   [HYPOTHESIS]
LINE_CODING = 132 / 128               # 128b/132b of a USB 3.2 Gen 2 class lane
LEAF_LANE = 10.0                      # Gb/s per pair, [HYPOTHESIS] gate MON-23
LEAF_PAYLOAD = 2 * LEAF_LANE / LINE_CODING   # 19.39 Gb/s payload on two pairs
HINGE_LANES, HINGE_LANE_RATE = 3, 3.2  # Gb/s, hw/display SPEC 3.4
HINGE_CAP = HINGE_LANES * HINGE_LANE_RATE / LINE_CODING   # 9.31 Gb/s payload per hinge
SLICE_START_BITS = 800                # extra bits of the first line of a DSC slice   [HYPOTHESIS]
LINE_HDR_BITS = 64                    # [x3|y4|type4|line8|len12] plus CRC share      hw/display 3.6
V_LIM_STILL, V_LIM_WIND = 1.73, 2.37  # W, sustained free-air, 25 C, hw/hostpower/thermal
T_SKIN_LIMIT = 36.2                   # C

# ============================================================================
# A. THE PIXEL BUDGET
# ============================================================================
CODECS = {          # name: bits per pixel on the wire, source
    "raw 10 bit": 30.0,
    "raw 8 bit": 24.0,
    "DSC 10 bpp (3:1 of 10 bit)": 10.0,
    "DSC 8 bpp (3.75:1 of 10 bit, 3:1 of 8 bit)": 8.0,
    "VDC-M 6 bpp (5:1 of 10 bit, 4:1 of 8 bit)": 6.0,
}


def slice_bits(bpp, lines=200, width=200, codec_slice=True):
    """Bits on the wire for one slice of width x lines pixels."""
    b = width * lines * bpp
    if codec_slice and bpp < 24:
        b += SLICE_START_BITS
    b += lines * LINE_HDR_BITS
    return b


def part_a():
    t = Tee("pixel_budget.txt")
    P = t.p
    P("A. THE PIXEL BUDGET   (Skin to Core, warp in the Core, stream = warped 200 x 200 tile images)")
    P("=" * 100)
    P(f"face {W} x {H} = {PX/1e6:.2f} Mpx, {TILES} tiles of 200 x 200 px, {PX/TILES:.0f} px each")
    P()
    P("A1. full face, every pixel, payload only (no packet, no coding)   Gb/s")
    P(f"{'refresh':>8} {'raw 8':>9} {'raw 10':>9} {'DSC 10bpp':>10} {'DSC 8bpp':>9} {'VDC-M 6':>9}")
    full = {}
    for hz in (60, 120, 240):
        row = [PX * hz * b / 1e9 for b in (24, 30, 10, 8, 6)]
        full[hz] = row
        P(f"{hz:>6} Hz " + " ".join(f"{x:9.2f}" for x in row[:2]) + f" {row[2]:10.2f} {row[3]:9.2f} {row[4]:9.2f}")
    P("check against the Lead: 240 Hz raw 10 bit = 36.86 Gb/s; at 3:1, 4:1, 6:1 = 12.29, 9.22, 6.14 Gb/s")
    P(f"  honest ratios of 10 bit input: DSC 10 bpp = 3.00:1 ({PX*240*10/1e9:.2f}), DSC 8 bpp = 3.75:1 "
      f"({PX*240*8/1e9:.2f}), VDC-M 6 bpp = 5.00:1 ({PX*240*6/1e9:.2f}).")
    P("  4:1 of 10 bit is 7.5 bpp. It sits under the 8 bpp at which DSC is rated. 6:1 is 5 bpp. It sits under")
    P("  the 6 bpp at which VDC-M is rated. [PUBLICATION] VESA DSC 1.2b (3:1, 8 bpp), VDC-M 1.2 (5:1, 6 bpp from 30 b).")
    P("  So the Lead's 4:1 is at the edge and 6:1 is outside the published visually lossless range.")
    SUMMARY["raw_240_10bit_gbps"] = full[240][1]
    SUMMARY["vdcm6_240_gbps_payload"] = full[240][4]
    P()
    P("A2. the wire rate of the design cases, with the packet share and the first line of each slice")
    P(f"{'case':44s} {'payload':>8} {'wire':>8} {'+128b/132b':>11}")
    wire = {}
    for name, bpp in CODECS.items():
        for hz in (60, 120, 240):
            pay = PX * hz * bpp / 1e9
            if bpp >= 24:
                w_ = pay
            else:
                w_ = TILES * slice_bits(bpp) * hz / 1e9
            wire[(name, hz)] = w_
            if hz == 240:
                P(f"{name + ' 240 Hz':44s} {pay:8.2f} {w_:8.2f} {w_*LINE_CODING:11.2f}")
    d = wire[("DSC 10 bpp (3:1 of 10 bit)", 240)]
    SUMMARY["dsc10_240_wire_gbps"] = d
    SUMMARY["dsc10_240_line_gbps"] = d * LINE_CODING
    P(f"the display team's design case (DSC 10 bpp, 240 Hz): {d*LINE_CODING:.2f} Gb/s on the leaf lanes "
      f"(display team 13.43 with a 1.06 share). Two pairs carry {2*LEAF_LANE:.1f} raw, {LEAF_PAYLOAD:.2f} payload.")
    P()

    # --- use cases and partial updates -------------------------------------
    P("A3. use cases and partial updates. The panel scans at 240 Hz from the uIC buffers. The link carries only the")
    P("    frames that change. Delta = tile skip (a static tile gets no packet) or strip skip (line packets).")
    P("    Dirty fractions are [HYPOTHESIS]. 'fill' is the share of a sent slice that changed.")
    P("    The Skin has no frame store. It cannot scroll or compose, so a scroll is a full update of the view.")
    cases = [  # name, fps, dirty fraction of face, fill in tile mode, fill in strip mode
        ("static page, cursor and clock", 10, 0.002, 0.10, 0.50),
        ("UI, typing, small animation", 60, 0.06, 0.25, 0.70),
        ("mixed delta session", 60, 0.25, 0.60, 0.90),
        ("scroll at 60 Hz, 85 % view", 60, 0.85, 1.0, 1.0),
        ("scroll at 120 Hz, 85 % view", 120, 0.85, 1.0, 1.0),
        ("video 16:9 in portrait, 30 fps", 30, 0.281, 0.90, 1.0),
        ("video vertical, 60 fps", 60, 0.89, 1.0, 1.0),
        ("full motion, 120 Hz", 120, 1.0, 1.0, 1.0),
        ("full motion, 240 Hz", 240, 1.0, 1.0, 1.0),
    ]
    rows = []
    P()
    hdr = (f"{'use case':34s} {'fps':>4} | {'10 bit DSC10':>13} {'10 bit DSC8':>12} {'10 bit VDC6':>12} | "
           f"{'8 bit DSC8':>11} {'8 bit VDC6':>11} | {'raw 10b':>8}   Mb/s, tile mode / strip mode")
    P(hdr)
    P("    (Mb/s before the 128b/132b line coding of the tether)")

    def cs_bits(fps, dirty, fill, mode, bpp):
        sent_px = min(1.0, dirty / fill) * PX
        if mode == "tile":
            n_sl = sent_px / TPX
            lines = 200
        else:
            lines = 16
            n_sl = sent_px / (200 * lines)
        bits = sent_px * bpp + n_sl * (SLICE_START_BITS if bpp < 24 else 0) + (sent_px / 200) * LINE_HDR_BITS
        return bits * fps / 1e6

    for name, fps, dirty, ft, fs in cases:
        vals = {}
        for mode, fill in (("tile", ft), ("strip", fs)):
            vals[mode] = [cs_bits(fps, dirty, fill, mode, b) for b in (10, 8, 6, 8, 6, 30)]
        rows.append((name, fps, vals))
        f = lambda i: f"{vals['tile'][i]:7.0f}/{vals['strip'][i]:<6.0f}"
        P(f"{name:34s} {fps:>4} | {f(0):>13} {f(1):>12} {f(2):>12} | {f(3):>11} {f(4):>11} | {vals['tile'][5]:8.0f}")
    csv = ["use_case,fps,tile_dsc10_mbps,strip_dsc10_mbps,tile_dsc8_mbps,tile_vdcm6_mbps,raw10_mbps"]
    for name, fps, v in rows:
        csv.append(f"{name},{fps},{v['tile'][0]:.1f},{v['strip'][0]:.1f},{v['tile'][1]:.1f},{v['tile'][2]:.1f},{v['tile'][5]:.1f}")
    with open(os.path.join(OUT, "use_cases.csv"), "w") as fh:
        fh.write("\n".join(csv) + "\n")
    SUMMARY["use_cases"] = {n: dict(fps=fps, tile_dsc10_mbps=v["tile"][0], strip_dsc10_mbps=v["strip"][0],
                                    tile_vdcm6_mbps=v["tile"][2]) for n, fps, v in rows}
    P()
    P("  The page turn is a burst, not a rate. A full face of DSC 10 bpp is "
      f"{TILES*slice_bits(10)/1e6:.1f} Mbit. Time to draw it at a link rate R is in Section D.")

    # --- stretched geometry and the place of the warp ----------------------
    P()
    P("A4. the stretched geometry and where the warp lives (hw/display SPEC 4)")
    P(f"{'stretch':>8} {'theta':>6} {'source window':>14} {'px x':>6} {'pixel coverage':>15}  stream if the warp is in the Core / in the Skin (DSC 10 bpp, 240 Hz)")
    mult = {}
    for deg in (0.0, 17.5, 45.0):
        th = math.radians(deg)
        s = math.cos(th) + math.sin(th)
        win = 200 * (math.cos(th) + math.sin(th)) if deg else 200      # bounding box of the rotated tile
        win = math.ceil(win) + (0 if deg == 0 else 0)
        m = (win / 200) ** 2
        mult[deg] = m
        P(f"{100*(s-1):7.1f}% {deg:5.1f} {win:>6} x {win:<5} {m:6.2f} {100/s/s:14.1f}%  "
          f"{d*LINE_CODING:6.2f} / {d*LINE_CODING*m:6.2f} Gb/s")
    P("  Warp in the Core: the stream is 5.12 Mpx at every stretch. The Core sends warped tile images and needs")
    P("  the tile angles back at 480 Hz (about 1 Mb/s, Section D4). Warp in the Skin: 1.58 x and 2.00 x pixels,")
    P("  a 251 x 251 or 283 x 283 source window per hub, a 4-tap engine and about 0.5 to 1 Mb of line buffer per hub.")
    P("  [DECISION] of this study: the warp stays in the Core. The cost is the age of the angles (Section D4).")
    P("  The more-room canvas (2007 x 4014 at 25 %, 2263 x 4525 at 41 %, up to 30.7 MB raw) lives in the Core store,")
    P("  not on the link.")
    SUMMARY["warp_in_skin_multiplier"] = {str(k): v for k, v in mult.items()}

    # --- hinge mesh limit -----------------------------------------------------
    P()
    P("A5. the hinge mesh forces a decoder on the Skin, whatever the tether carries")
    P(f"  one hinge: {HINGE_LANES} lanes x {HINGE_LANE_RATE} Gb/s = {HINGE_CAP:.2f} Gb/s payload. The root of a degree-3 seat")
    P("  carries (127/128)/3 of the stream; with one root hinge broken (degree 2) it carries (127/128)/2.")
    for name, bpp in (("raw 10 bit", 30), ("DSC 10 bpp", 10), ("DSC 8 bpp", 8), ("VDC-M 6 bpp", 6)):
        w_ = PX * 240 * bpp * PKT / 1e9
        r3 = w_ * (127 / 128) / 3
        r2 = w_ * (127 / 128) / 2
        P(f"  {name:12s} 240 Hz: stream {w_:6.2f} Gb/s, root hinge {r3:5.2f} (3 hinges) / {r2:5.2f} (2 hinges) vs {HINGE_CAP:.2f}"
          f"  -> {'fits' if r2 <= HINGE_CAP else ('fits with all hinges' if r3 <= HINGE_CAP else 'FAILS')}")
    rmin3 = 36.864 * PKT * (127 / 128) / 3 / HINGE_CAP
    rmin2 = 36.864 * PKT * (127 / 128) / 2 / HINGE_CAP
    P(f"  minimum compression ratio of 10 bit, 240 Hz: {rmin3:.2f}:1 with all root hinges, {rmin2:.2f}:1 with one broken.")
    P("  So a Skin with no decoder is not possible at 240 Hz through this mesh. The decoder floor is set by the hinge")
    P("  copper, not by the tether. [HYPOTHESIS]")
    SUMMARY["min_ratio_mesh"] = [rmin3, rmin2]

    # --- mesh retime energy ------------------------------------------------------
    def mean_hops(seat):
        return np.mean([abs(x - seat[0]) + abs(y - seat[1]) for y in range(NY) for x in range(NX)])
    seats = {"top (3,0)": (3, 0), "bottom (4,15)": (4, 15), "left (0,7)": (0, 7), "right (7,8)": (7, 8)}
    mh = {k: mean_hops(v) for k, v in seats.items()}
    SUMMARY["mean_hops"] = {k: float(v) for k, v in mh.items()}
    P()
    P("A6. the Skin cost of the mesh: every hub retimes the traffic of its subtree. Mean Manhattan hops from the seat:")
    P("  " + ", ".join(f"{k} {v:.2f}" for k, v in mh.items()))
    t.close()
    return full, wire, mh


E_RETIME = 3.0e-12      # J per bit per hop, short-reach 3.2 Gb/s retimed lane       [HYPOTHESIS] [GENERAL] 1 to 5 pJ/b
E_DEC = 60e-12          # J per decoded pixel, DSC decoder at 28 nm and 0.6 to 0.8 V   [HYPOTHESIS]
# Basis of E_DEC: the fabricated UC Davis DSC encoder reaches 84 to 163 pJ/px (Wu 2021, Asilomar 2018).
# A decoder has no mode search and no rate-control lookahead, so about half.


# ============================================================================
# B. THE LINK OPTIONS
# ============================================================================
def rate_60ghz(d_m, blockage_db=0.0, core_gain_dbi=8.8, skin_gain_dbi=8.8, pt_dbm=8.0, nf_db=7.0,
               impl_db=8.0, max_ch=2, max_qam=4):
    """Best net payload rate (Gb/s) of an 802.11ad or ay single carrier link, downlink Core to Skin."""
    lam = 3e8 / 60.48e9
    fspl = 20 * math.log10(4 * math.pi * d_m / lam)
    best = (0.0, "none", -99)
    mods = [m for m in (("QPSK 3/4", 2, 0.75, 7.0), ("16QAM 3/4", 4, 0.75, 14.0), ("64QAM 3/4", 6, 0.75, 21.0)) if m[1] <= max_qam]
    for ch in (1, 2, 3, 4)[:max_ch]:
        bw = ch * 1.76e9
        pn = -174 + 10 * math.log10(bw) + nf_db
        prx = pt_dbm + core_gain_dbi + skin_gain_dbi - fspl - blockage_db
        snr = prx - pn
        for nm, bps, cr, req in mods:
            if snr >= req + impl_db:
                r = bw * bps * cr * (448 / 512) / 1e9      # SC block guard share of 802.11ad
                if r > best[0]:
                    best = (r, f"{ch}ch {nm}", snr)
    return best, fspl


def flex_loss(f_hz, w_m, length_m, tan_d=0.004, eps_r=3.0, z0=45.0, rough=1.3):
    rs = math.sqrt(math.pi * f_hz * 4e-7 * math.pi * 1.72e-8)
    a_c = rough * rs / (w_m * z0)                                  # Np/m, microstrip class
    a_d = math.pi * f_hz * math.sqrt(eps_r) * tan_d / 3e8           # Np/m
    return 8.686 * (a_c + a_d) * length_m


def twinax_loss(f_hz, d_m, length_m, prox=2.0, tan_d=0.002, eps_r=2.1, zdiff=100.0):
    rs = math.sqrt(math.pi * f_hz * 4e-7 * math.pi * 1.72e-8)
    r_loop = 2 * rs / (math.pi * d_m) * prox
    a_c = r_loop / (2 * zdiff)
    a_d = math.pi * f_hz * math.sqrt(eps_r) * tan_d / 3e8
    return 8.686 * (a_c + a_d) * length_m


def inductive_eta(k, q1, q2):
    x = k * k * q1 * q2
    return x / (1 + math.sqrt(1 + x)) ** 2


OPTIONS = [
    # key, name, net Gb/s payload (low, typ, high), latency fixed ms, Skin-end link mW at 13.4 Gb/s, max range m, power path,
    # cell needed on the Skin, cost class, cost USD [HYPOTHESIS], carries 240 Hz DSC 10 bpp
    dict(key="a", name="contact leaves on a seat or dock (12 gold leaves)", rate=(9.7, 19.4, 19.4),
         lat=0.002, skin_mw=85, rng=0.0, cls="C0", power=True, cell=False, cost="low", usd=3,
         life=10000, sources="hw/display SPEC 3.3; hw/energy 03 Section 2; spring leaf at 10 Gb/s is [HYPOTHESIS] MON-23"),
    dict(key="b", name="thin flex or ribbon with a connector", rate=(9.7, 19.4, 38.8),
         lat=0.002, skin_mw=85, rng=0.5, cls="C0", power=True, cell=False, cost="low to mid", usd=8,
         life=10000, sources="USB-C class connector 10 000 cycles [PUBLICATION] USB-IF; FPC ZIF 20 to 50 cycles [GENERAL]"),
    dict(key="c", name="optical fibre tether (hybrid with two copper power wires)", rate=(19.4, 48.5, 97.0),
         lat=0.003, skin_mw=90, rng=100.0, cls="C0 and C1", power=False, cell=False, cost="mid to high", usd=25,
         life=5000, sources="G.657.B3 5 mm bend radius [PUBLICATION] ITU-T; 25G VCSEL AOC [PUBLICATION] vendors; 10 pJ/b driver [PUBLICATION]"),
    dict(key="d", name="60 GHz close-range radio (802.11ad or ay class)", rate=(1.8, 3.7, 7.4),
         lat=0.5, skin_mw=600, rng=10.0, cls="C0 and C1", power=False, cell=True, cost="high", usd=30,
         life=10**9, sources="10 Gb/s QPSK transceiver 340 mW; 788 mW and 984 mW with MAC at 1.8 Gb/s [PUBLICATION] Tsukizawa et al.; Okada et al."),
    dict(key="e", name="near-field coupler in-plane (transmission-line or capacitive)", rate=(5.4, 18.0, 18.0),
         lat=0.001, skin_mw=45, rng=0.005, cls="C0 (mm)", power=False, cell=False, cost="mid", usd=10,
         life=10**5, sources="6 Gb/s, 6 pJ/b, 5 mm [PUBLICATION] ISSCC 2015 paper 10.1; Keyssa Kiss 6 Gb/s at 60 GHz [PUBLICATION]"),
    dict(key="f1", name="Wi-Fi 7 (2 x 2, 320 MHz)", rate=(1.0, 2.5, 3.5),
         lat=1.0, skin_mw=1000, rng=30.0, cls="C0 and C1", power=False, cell=True, cost="mid", usd=6,
         life=10**9, sources="5.76 Gb/s peak MCS, 3.5 to 3.7 Gb/s measured close, 1+ Gb/s at 40 ft [PUBLICATION] Intel, WBA, press"),
    dict(key="f2", name="UWB (IEEE 802.15.4z HRP)", rate=(0.0068, 0.027, 0.027),
         lat=0.5, skin_mw=200, rng=30.0, cls="C0 and C1", power=False, cell=False, cost="low", usd=4,
         life=10**9, sources="6.8 and 27.2 Mb/s data rates [PUBLICATION] IEEE 802.15.4z"),
]


def part_b():
    t = Tee("links.txt")
    P = t.p
    P("B. THE LINK OPTIONS")
    P("=" * 100)
    need = {
        "full motion 240 Hz DSC 10 bpp": SUMMARY["dsc10_240_line_gbps"],
        "full motion 240 Hz VDC-M 6 bpp": TILES * slice_bits(6) * 240 / 1e9,
        "full motion 120 Hz DSC 8 bpp": TILES * slice_bits(8) * 120 / 1e9,
        "scroll or video 60 Hz DSC 8 bpp": TILES * slice_bits(8) * 60 / 1e9,
        "video 30 fps 16:9, DSC 8 bpp": SUMMARY["use_cases"]["video 16:9 in portrait, 30 fps"]["tile_dsc10_mbps"] / 1e3 * 0.8,
        "static page and UI delta, DSC 10": SUMMARY["use_cases"]["UI, typing, small animation"]["tile_dsc10_mbps"] / 1e3,
    }
    P("B0. the need, Gb/s on the link (the tether adds its own coding where it has one)")
    for k, v in need.items():
        P(f"  {k:40s} {v:7.3f}")
    SUMMARY["need_gbps"] = need
    P()
    P("B1. the 60 GHz budget, Core to Skin, QPSK and 16QAM, 1 or 2 bonded channels of 1.76 GHz (client chip class; 64QAM and 4 channels are lab results)")
    P("    Pt 8 dBm, Skin antenna 8.8 dBi (A4, HARDWARE/19), NF 7 dB, implementation loss 8 dB (phase noise, EVM). [HYPOTHESIS]")
    P("    required SNR for rate 3/4: QPSK 7 dB, 16QAM 14 dB, 64QAM 21 dB [GENERAL]. Hand or body block: 20 dB.")
    P(f"{'d (m)':>6} {'FSPL':>6} | {'LOS, Core 8.8 dBi':>26} | {'LOS, Core 20 dBi':>26} | {'blocked 20 dB, Core 20 dBi':>28}")
    r60 = {}
    for d_ in (0.1, 0.3, 1, 2, 5, 10, 30):
        a, fs = rate_60ghz(d_)
        b, _ = rate_60ghz(d_, core_gain_dbi=20.0)
        c, _ = rate_60ghz(d_, blockage_db=20.0, core_gain_dbi=20.0)
        r60[d_] = (a[0], b[0], c[0])
        P(f"{d_:6.1f} {fs:6.1f} | {a[0]:6.2f} Gb/s {a[1]:>14} | {b[0]:6.2f} Gb/s {b[1]:>14} | {c[0]:6.2f} Gb/s {c[1]:>14}")
    P("    802.11ad: the 4.62 Gb/s PHY rate is one channel, 16QAM 3/4, with the 448/512 guard share (matches the model).")
    P("    Net payload is the PHY rate times about 0.8 for MAC and framing. The best 802.11ad client MAC measured 1.8 Gb/s at 40 cm.")
    ranges = {}
    for need_g, lab in ((SUMMARY["need_gbps"]["full motion 240 Hz VDC-M 6 bpp"], "VDC-M 6 bpp 240 Hz"),
                        (SUMMARY["need_gbps"]["full motion 120 Hz DSC 8 bpp"], "DSC 8 bpp 120 Hz"),
                        (SUMMARY["need_gbps"]["scroll or video 60 Hz DSC 8 bpp"], "DSC 8 bpp 60 Hz")):
        for blk, tag in ((0.0, "LOS"), (20.0, "blocked")):
            dmax = 0.0
            for d_ in np.arange(0.05, 40, 0.05):
                (r, _, _), _ = rate_60ghz(d_, blockage_db=blk, core_gain_dbi=20.0)
                if r * 0.8 >= need_g:
                    dmax = d_
            ranges[(lab, tag)] = dmax
            P(f"    range that carries {lab:20s} ({need_g:5.2f} Gb/s), {tag:8s}, Core 20 dBi: {dmax:5.2f} m")
    SUMMARY["r60"] = {str(k): v for k, v in r60.items()}
    SUMMARY["r60_ranges"] = {f"{k[0]}|{k[1]}": v for k, v in ranges.items()}
    P("    The 60 GHz radio is a C0 to C1 pixel option with line of sight. It does not carry the 13.4 Gb/s design case.")
    P()
    P("B2. copper flex and twinax loss at 5 GHz (the Nyquist of a 10 Gb/s lane). Budget for tether and connectors: 12 dB [HYPOTHESIS]")
    P("    USB 3.2 Gen 2 allows about 23 dB host to device at 5 GHz in total [PUBLICATION] USB-IF; 12 dB is left for the cable.")
    flex_len = {}
    for w_um in (100, 200, 400):
        a = flex_loss(5e9, w_um * 1e-6, 1.0)
        flex_len[w_um] = 12.0 / a
        P(f"  LCP flex trace, w {w_um} um, tan d 0.004: {a:5.1f} dB/m at 5 GHz -> 12 dB reach {12.0/a:5.2f} m")
    tw_len = {}
    for awg, dm in ((30, 0.255e-3), (34, 0.160e-3), (40, 0.080e-3)):
        a = twinax_loss(5e9, dm, 1.0)
        tw_len[awg] = 12.0 / a
        P(f"  twinax {awg} AWG, shielded, proximity x2: {a:5.1f} dB/m at 5 GHz -> 12 dB reach {12.0/a:5.2f} m")
    P("  verdict: thin flex carries 10 Gb/s over 0.25 to 0.8 m, round twinax over 1 to 3 m. That is C0. At 5 to 30 m only fibre or an active cable works.")
    SUMMARY["flex_reach_m"] = flex_len
    SUMMARY["twinax_reach_m"] = tw_len
    P()
    P("B3. inductive power through a contactless seat: eta = k2 Q1 Q2 / (1 + sqrt(1 + k2 Q1 Q2))^2")
    P("    Skin share of the loss: half of the coil loss plus the rectifier and regulator at 5 % of the output.")
    P(f"{'k':>5} {'Q':>4} {'eta':>6} | {'loss at 1.8 W out':>18} {'Skin heat':>10} | {'loss at 3.6 W out':>18} {'Skin heat':>10}")
    ind = {}
    for k_, q_ in ((0.40, 30), (0.20, 30), (0.20, 15), (0.10, 15)):
        e_ = inductive_eta(k_, q_, q_)
        row = []
        for pout in (1.8, 3.6):
            loss = pout * (1 / e_ - 1)
            skin = 0.5 * loss + 0.05 * pout
            row += [loss, skin]
        ind[(k_, q_)] = (e_, row)
        P(f"{k_:5.2f} {q_:4d} {e_:6.2f} | {row[0]:15.2f} W {row[1]:8.2f} W | {row[2]:15.2f} W {row[3]:8.2f} W")
    P("    A coil pair at k 0.2 and Q 30 wastes 0.7 W for 1.8 W. The Skin keeps 0.4 W of heat. Power rides on contact leaves.")
    SUMMARY["inductive"] = {f"{k[0]}|{k[1]}": v[0] for k, v in ind.items()}
    P()
    P("B4. near-field couplers: 6 Gb/s and 6 pJ/b per coupler pair, 6 mm2, at 5 mm (ISSCC 2015)")
    n_c = math.ceil(SUMMARY["dsc10_240_line_gbps"] / (6.0 * 0.9))
    P(f"  couplers for the design case: {n_c} pairs x 6 mm2 = {n_c*6:.0f} mm2 on the Skin edge; Skin share of the energy 50 %: "
      f"{SUMMARY['dsc10_240_line_gbps']*1e9*6e-12*0.5*1e3:.0f} mW")
    SUMMARY["couplers"] = n_c
    P("  Gap 1 to 5 mm. A kinematic seat of the Part 21 quadrant locator repeats to under 1 um [GENERAL], so alignment is not the limit.")
    P("  Magnets sit near the couplers. A transmission-line coupler has no ferrite, so it does not saturate. A magnetic (inductive) coupler would.")
    P()
    P("B5. the table. Net payload and range are the realistic values. Latency is the fixed link part (ms). Power is the Skin end")
    P("    when the link ends on the Skin, at the 13.4 Gb/s design case (radio and optical ends also carry a battery or a clip).")
    P(f"{'opt':4} {'link':58s} {'net Gb/s (low/typ/high)':>24} {'lat ms':>7} {'Skin mW':>8} {'range':>8} {'class':>10} {'cost':>12} {'USD':>4}")
    for o in OPTIONS:
        r = o["rate"]
        P(f"{o['key']:4} {o['name']:58s} {r[0]:7.3g} /{r[1]:7.3g} /{r[2]:7.3g} {o['lat']:7.3f} {o['skin_mw']:8d} "
          f"{o['rng']:7.3g}m {o['cls']:>10} {o['cost']:>12} {o['usd']:4d}")
    P()
    P("B6. which option carries which stream (net payload after coding; LOW for a wired link means one lane pair lost)")
    P(f"{'opt':4} " + " ".join(f"{k[:22]:>22}" for k in need))
    carry = {}
    for o in OPTIONS:
        row = []
        for k, v in need.items():
            lo = o["rate"][0]
            typ = o["rate"][1]
            need_net = v
            ok_lo = lo >= need_net
            ok_typ = typ >= need_net
            row.append("yes" if ok_lo else ("typical" if ok_typ else "no"))
        carry[o["key"]] = dict(zip(need.keys(), row))
        P(f"{o['key']:4} " + " ".join(f"{x:>22}" for x in row))
    SUMMARY["carry"] = carry
    P("  'yes' = carried at the low rate; 'typical' = carried only at the typical rate; 'no' = not carried.")
    P("  The 60 GHz rate against distance is in B1. A client chip at 16QAM and 2 channels tops out at 7.4 Gb/s net.")
    t.close()
    return need


# ============================================================================
# C. THE SMALLEST SKIN
# ============================================================================
AREA = 80.0 * 160.0     # mm2 at rest
PC, GLASS, OCA, GRAPH, TPU, CELLD = 1.20, 2.40, 1.00, 1.60, 1.15, 2.40   # g/cm3 [GENERAL]


def mass_of(area_mm2, t_mm, rho):
    return area_mm2 * t_mm * 1e-3 * rho        # g (mm3 -> cm3 = 1e-3)


def part_c(mh):
    t = Tee("skin_bom.txt")
    P = t.p
    P("C. THE SMALLEST SKIN")
    P("=" * 100)
    P("C1. the face mass, from the Part 21 tile stack (Section 21.2.7), rest state 80 x 160 mm. Densities are [GENERAL].")
    layers = [("PC cap with AgNW touch grid", 0.25, PC), ("optical adhesive", 0.05, OCA),
              ("glass, micro-LED layer and glass", 0.25, GLASS), ("slip OCA", 0.03, OCA),
              ("hub and spreader layer (replaces the 0.20 Qi layer)", 0.10, GRAPH), ("floating back skin (TPU)", 0.08, TPU)]
    m_face = 0.0
    for nm, th, rho in layers:
        m = mass_of(AREA, th, rho)
        m_face += m
        P(f"  {nm:52s} {th:5.2f} mm {m:6.2f} g")
    m_hinge = 232 * 0.0022 + 0.4          # ribbons and titanium pins, rough
    m_hubs = TILES * 0.0005
    m_misc = 0.30                          # seat controller, ID, accelerometer, leaf field, thermistors
    m_skin = m_face + m_hinge + m_hubs + m_misc
    t_skin = 0.25 + 0.05 + 0.25 + 0.03 + 0.10 + 0.08 + 0.24
    P(f"  hinges, 232 ribbons and pins {m_hinge:5.2f} g; 128 hub dies {m_hubs:5.2f} g; seat parts {m_misc:5.2f} g")
    P(f"  SKIN MASS (no cells, no Qi coil, no module): {m_skin:5.1f} g, thickness {t_skin:4.2f} mm (hinge and tolerance 0.24 mm kept)")
    m_cells = mass_of(AREA * 0.83 * 0.90 / 0.90 * 0.90 / 1.0, 0.90 / 0.83 * 0.83, CELLD)    # 9.56 cm3
    cell_vol_cm3 = AREA * 0.83 * 0.90 * 1e-3
    m_cells = cell_vol_cm3 * CELLD
    m_cans = 128 * 0.05
    m_qi = 3.0
    m_body = m_skin + m_cells + m_cans + m_qi - 0.10 * AREA * 1e-3 * GRAPH + mass_of(AREA, 0.20, 2.0) * 0.0
    P(f"  the L.6.0 body for comparison: cells {m_cells:4.1f} g ({cell_vol_cm3:.2f} cm3 at {CELLD} g/cm3), cans {m_cans:3.1f} g, Qi coil and shield {m_qi:3.1f} g")
    P(f"  L.6.0 BODY MASS (no module): about {m_body:4.0f} g. The Skin is {100*(1-m_skin/m_body):.0f} % lighter. [HYPOTHESIS]")
    SUMMARY["skin_mass_g"] = m_skin
    SUMMARY["body_mass_g"] = m_body
    SUMMARY["skin_thickness_mm"] = t_skin
    P()
    P("C2. the silicon that cannot leave the Skin, per hub (hw/display SPEC 1.6 and 3.6). Hub die 1.6 x 1.6 mm = 2.56 mm2.")
    hub = [
        ("DSC slice decoder, 1 px/clk, 28 nm (60 kgate + 3 kB line and rate buffer)", 0.025, "9.6 Mpx/s needs 10 to 20 MHz"),
        ("4 mesh ports, 3.2 Gb/s retimed, 3 lanes + back channel", 0.15, "the main load, see C4"),
        ("100 row-bus drivers", 0.10, ""),
        ("1 Mb eMRAM, per-pixel calibration and tile ID", 0.20, ""),
        ("AgNW touch AFE and 12 bit ADC, 480 Hz", 0.20, "analog, cannot move"),
        ("hinge-angle and seam sense front end", 0.05, "analog, cannot move"),
        ("thermistor ADC and trip comparator", 0.01, ""),
        ("route table, address, sync latch, safe-screen pattern ROM 2 kB", 0.02, ""),
    ]
    a_sum = 0
    for nm, a, c in hub:
        a_sum += a
        P(f"  {nm:76s} {a:5.3f} mm2  {c}")
    P(f"  sum {a_sum:5.2f} mm2 of 2.56 mm2 -> {100*a_sum/2.56:.0f} % used with routing at 2x; the decoder is {100*0.025/a_sum:.0f} % of the logic")
    SUMMARY["hub_area_used_mm2"] = a_sum
    P("  The decoder is small. The mesh ports, the analog fronts and the memory set the hub size. [HYPOTHESIS]")
    P()
    P("C3. the Skin common parts, whatever the link (link-as-clip: every tether is a clip on the 12-leaf seat)")
    bom = [  # part, count, area mm2 each, mass mg each
        ("tile hub die (C2)", 128, 2.56, 0.5),
        ("micro-IC, 28 nm HV, 20 x 85 um (10 000 per tile)", 1_280_000, 0.0017, 0.00004),
        ("seat controller: 2 x 10 Gb/s RX and TX, lane crossbar, dead-pad switch, route-table loader, ROM 16 kB safe screen, trip", 4, 9.0, 40),
        ("identity: part record and link-auth key, no wallet key (secure ID class)", 1, 6.0, 60),
        ("accelerometer, 3 axis (orientation of the Skin)", 1, 4.0, 30),
        ("thermistor, one per tile", 128, 0.5, 0.5),
        ("bridge cell (one tile cell, 46 mWh) with its fuse", 1, 85.0, 1200),
        ("12 gold leaves on the seat tile", 4, 0.0, 2),
    ]
    P(f"{'part':110s} {'n':>9} {'mm2 each':>9} {'mg each':>8}")
    a_tot = 0.0
    for nm, n, a, m in bom:
        a_tot += n * a
        P(f"{nm:110s} {n:9d} {a:9.4f} {m:8.3f}")
    P(f"  silicon and parts area on the Skin: {a_tot/100:.0f} cm2 of die area: micro-ICs 21.8 cm2 in the pixel streets, hubs 3.3 cm2, under the 128 cm2 face")
    P("  the bridge cell is one of the 128 existing tile cells. It holds the safe screen (0.12 W) for 23 min or a swap.")
    P("  seat controllers: one per edge, four seats (hw/energy 03). The identity chip holds a link key. A Skin that signs a spend does not exist.")
    P("  Parts that LEAVE the Skin and sit in the Core: U1 TCON and compositor, U6 decoder and 16 MB store, U2A, U2B, U5, U7,")
    P("  U8, U3, U4, the camera path, the audio path, the 128 cells, the 4 U_Q chargers and the Qi coils.")
    P()
    P("C4. the Skin load, W. Display and address are the body column of hw/energy 04. The hub electronics are added bottom-up.")
    P("    The body column of the Lead (0.80 and 1.35 W) holds no tile hub. See the damage report. Reading R2 below.")
    P(f"{'case':26} {'body col':>8} {'hub static':>10} {'decode':>7} {'mesh':>6} {'row bus':>8} {'seat PHY':>9} {'SKIN W':>7} | {'R2: full Hub domain':>20}")
    cases = [("safe screen", 0.12, "static page and clock", 0.0, 0.0), ]
    uc = SUMMARY["use_cases"]
    loads = {}
    mh_mean = float(np.mean(list(mh.values())))
    defs = [
        ("safe screen, no link", 0.120, 0.0, 0.0, 0.0),                                # body col, bits/s of stream, px/s, hub hold
        ("static page 10 Hz", 0.170, uc["static page, cursor and clock"]["tile_dsc10_mbps"] * 1e6, None, 0.005 + 0.0),
        ("delta session, 250 nits", 0.800, uc["mixed delta session"]["tile_dsc10_mbps"] * 1e6, None, 0.70),
        ("video Wi-Fi", 1.350, uc["video vertical, 60 fps"]["tile_dsc10_mbps"] * 1e6, None, 1.20),
        ("full motion 240 Hz, 250 nits", 1.350, uc["full motion, 240 Hz"]["tile_dsc10_mbps"] * 1e6, None, 1.20),
        ("video outdoors, 800 nits", 4.240, uc["video vertical, 60 fps"]["tile_dsc10_mbps"] * 1e6, None, 1.20),
    ]
    for nm, body, bps, _, r2hub in defs:
        px_s = bps / 10.0
        static = TILES * 0.6e-3 if bps > 0 else TILES * 0.15e-3     # clocks, eMRAM leakage, AFE bias; gated when idle
        dec = px_s * E_DEC
        mesh = bps * PKT * mh_mean * E_RETIME if bps > 0 else 0.0
        row = TILES * 0.28e-3 * min(1.0, bps / 13.4e9)
        phy = (0.085 * min(1.0, 0.25 + bps / 13.4e9)) if bps > 0 else 0.010
        tot = body + static + dec + mesh + row + phy
        loads[nm] = dict(body=body, static=static, dec=dec, mesh=mesh, row=row, phy=phy, total=tot, r2=body + r2hub + phy)
        P(f"{nm:26} {body:8.3f} {static:10.3f} {dec:7.3f} {mesh:6.3f} {row:8.3f} {phy:9.3f} {tot:7.3f} | {body + r2hub + phy:20.3f}")
    SUMMARY["skin_load_w"] = {k: v["total"] for k, v in loads.items()}
    SUMMARY["skin_load_r2_w"] = {k: v["r2"] for k, v in loads.items()}
    P(f"    mean hops {mh_mean:.2f}, retime {E_RETIME*1e12:.0f} pJ/b/hop, decode {E_DEC*1e12:.0f} pJ/px.")
    P("    The mesh retime is the largest hub load. Heavier compression cuts it in step: VDC-M 6 bpp cuts mesh power by 40 % against DSC 10 bpp.")
    P()
    P("C5. the heat check. The thermal seat limit is for the whole L.6.0 body with the ring (1.73 W still, 2.37 W light wind, 25 C).")
    P("    A ringless face has no hot spot. A plate bound with both faces at 11 W/m2K and dT 11.2 K is a second reference.")
    plate = 11.0 * 2 * (AREA * 1e-6) * (T_SKIN_LIMIT - 25.0)
    P(f"    plate bound: {plate:.2f} W (uniform heat, still air, 25 C). [HYPOTHESIS] The heat seat of hw/core/heat decides.")
    SUMMARY["plate_bound_w"] = plate
    for nm, v in loads.items():
        tot = v["total"]
        P(f"  {nm:26s} Skin {tot:5.2f} W  vs 1.73 still: {'pass' if tot <= V_LIM_STILL else 'FAIL'}; vs 2.37 wind: "
          f"{'pass' if tot <= V_LIM_WIND else 'FAIL'}; vs plate {plate:.2f}: {'pass' if tot <= plate else 'FAIL'}")
    P("  A video session at 4.24 W (800 nits outdoors) passes nowhere. That is the display, not the link.")
    P()
    P("C6. the Skin for each link end (what the Skin and its clip carry on top of the common Skin). Power in W at the video case.")
    P(f"{'option':4} {'link silicon on the Skin or clip':70} {'link W':>7} {'cell Wh':>8} {'mass g':>7} {'clip or Skin mass':>20}")
    sess_h = 2.0
    vid = loads["video Wi-Fi"]["total"]
    clip = {}
    for o in OPTIONS:
        link_w = o["skin_mw"] / 1e3
        if o["cell"]:
            wh = (vid + link_w) * sess_h / 0.9
            m_cell_g = wh / 0.25            # 250 Wh/kg
        else:
            wh, m_cell_g = 0.0, 0.0
        if o["key"] == "a":
            sil, ms = "the seat PHY only; no clip silicon; pads on the seat", 0.0
        elif o["key"] == "b":
            sil, ms = "flex pigtail, clip with a magnetic leaf block; no clip silicon", 2.5
        elif o["key"] == "c":
            sil, ms = "clip with VCSEL driver, TIA, 2 lenses, hybrid pigtail; Skin sees leaves", 4.0
        elif o["key"] == "d":
            sil, ms = "60 GHz RFIC and baseband, 1 x 4 array (A4), the cell, a buck", 12.0
        elif o["key"] == "e":
            sil, ms = "3 coupler pairs and pulse transceiver; power by leaves or a coil", 3.0
        elif o["key"] == "f1":
            sil, ms = "Wi-Fi 7 combo module, 2 antennas, the cell, a buck", 12.0
        else:
            sil, ms = "UWB transceiver and antenna (control and ranging only)", 1.0
        clip[o["key"]] = dict(link_w=link_w, wh=wh, mass=ms + m_cell_g)
        P(f"{o['key']:4} {sil:70} {link_w:7.2f} {wh:8.2f} {ms + m_cell_g:7.1f} "
          f"{'Skin+'+format(m_skin + ms + m_cell_g, '.0f')+' g total':>20}")
    SUMMARY["clip"] = clip
    P("  A radio end needs a cell on the Skin or the clip: 2 h of video at the Skin load is the 'cell Wh' column, at 250 Wh/kg.")
    P("  The cell is the mass the Split was meant to remove. Radio ends give back most of the lightness they were chosen for.")
    P()
    P("C7. is everything off the screen possible? No. A floor remains.")
    P("  The floor: the emitters, 1.28 M micro-ICs, 128 hubs with a DSC decoder, touch and angle analog fronts, row drivers,")
    P("  the mesh ports, a seat PHY with a controller, a safe-screen ROM, a thermal trip, a part identity, a bridge cell.")
    P("  Reasons: a pixel needs its own driver (line count). A touch grid is analog. A hinge angle is a local analog value.")
    P("  The mesh copper limit forces a decoder (A5). A link loss needs a screen that says so, and a thermal limit needs a")
    P("  trip that does not wait for the Core.")
    P(f"  Floor silicon: hubs {TILES*2.56/100:.1f} cm2, seat controllers 0.4 cm2, identity 0.06 cm2. Floor mass {m_skin:.0f} g, thickness {t_skin:.2f} mm.")
    t.close()
    return loads, m_skin


# ============================================================================
# D. LATENCY
# ============================================================================
def load_latency_model():
    path = os.path.join(ROOT, "sim", "latency", "model.py")
    spec = importlib.util.spec_from_file_location("leaf_latency_model", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["leaf_latency_model"] = mod
    spec.loader.exec_module(mod)
    return mod


def tether_up(M, key, rng, n):
    if key in ("a", "b"):
        return np.full(n, 0.004)
    if key == "c":
        return np.full(n, 0.009)
    if key == "e":
        return np.full(n, 0.005)
    if key == "d":
        blk = (rng.random(n) < 0.005) * rng.uniform(5, 30, n)       # beam loss and retrain      [HYPOTHESIS]
        return rng.uniform(0, 0.5, n) + 0.07 + blk
    if key == "f1":
        return M.wifi_air(rng, n, M.Wifi(), True) + 0.1
    if key == "f2":
        return rng.uniform(0, 1.0, n) + 0.3
    raise KeyError(key)


def tether_down(M, key, rng, n, k_tiles, rate_gbps, bpp=10):
    ser = k_tiles * slice_bits(bpp) / (rate_gbps * 1e9) * 1e3          # ms
    if key in ("a", "b", "c", "e"):
        return ser * LINE_CODING + (0.002 if key != "c" else 0.005)
    if key == "d":
        blk = (rng.random(n) < 0.005) * rng.uniform(5, 30, n)
        return ser + rng.uniform(0, 0.1, n) + 0.07 + blk
    if key == "f1":
        return M.wifi_air(rng, n, M.Wifi(), False) + ser + 0.1
    if key == "f2":
        return ser + rng.uniform(0, 1.0, n) + 0.3
    raise KeyError(key)


def part_d():
    t = Tee("latency.txt")
    P = t.p
    P("D. LATENCY: Part 21 Section 21.5.7 plus the tether hop. Baseline from sim/latency/model.py (read only), 400 000 samples.")
    P("=" * 100)
    M = load_latency_model()
    N = 400_000
    paths = M.paths()
    base = {}
    for pk in ("wifi_room", "wifi_city", "nr_cell"):
        tot, st = M.simulate(paths[pk], N, seed=11)
        base[pk] = tot
        P(f"  baseline {pk:10s}: mean {tot.mean():5.1f}  p99 {np.percentile(tot, 99):5.1f}  p99.9 {np.percentile(tot, 99.9):5.1f} ms")
    # tile restart variant
    from dataclasses import replace
    pr = replace(paths["wifi_room"], scan=replace(paths["wifi_room"].scan, tile_restart=True))
    tr, _ = M.simulate(pr, N, seed=11)
    P(f"  baseline wifi_room with the tile-local scan restart: mean {tr.mean():5.1f}  p99 {np.percentile(tr, 99):5.1f} ms")
    P("  The Part 21 chain already holds U1 compose (0.2 ms) and the scan. The Split adds two things: the touch event crosses")
    P("  the tether to the Core, and the dirty tiles cross it from the Core to the hubs. The Core runs the Wi-Fi or 5G side as before.")
    P()
    rng = np.random.default_rng(5)
    res = {}
    P("D1. total p99 (ms) of a new action, tether options added to the baseline path. K = tiles that change.")
    P(f"{'opt':4} {'link':44} | {'rate':>6} | {'Wi-Fi room K=4':>15} {'K=32':>7} {'K=128':>7} | {'5G cell K=4':>12} {'K=128':>7} | {'p99.9 room K=4':>15} | verdict (30 ms p99)")
    rate_used = {"a": 19.4, "b": 19.4, "c": 19.4, "e": 18.0, "d": 3.7, "f1": 2.5, "f2": 0.027}
    for o in OPTIONS:
        key = o["key"]
        row = {}
        up = tether_up(M, key, rng, N)
        for K in (4, 32, 128):
            dn = tether_down(M, key, rng, N, K, rate_used[key])
            row[("wifi_room", K)] = base["wifi_room"] + up + dn
            row[("nr_cell", K)] = base["nr_cell"] + up + dn
        p99 = {kk: float(np.percentile(v, 99)) for kk, v in row.items()}
        p999 = float(np.percentile(row[("wifi_room", 4)], 99.9))
        ok4 = p99[("wifi_room", 4)] <= 30 and p99[("nr_cell", 4)] <= 30
        ok128 = p99[("wifi_room", 128)] <= 30 and p99[("nr_cell", 128)] <= 30
        verdict = ("holds for all K" if ok128 else ("holds for K=4, fails a full-face change" if ok4 else "fails"))
        res[key] = dict(p99=p99, p999=p999, verdict=verdict)
        P(f"{key:4} {o['name'][:44]:44} | {rate_used[key]:6.2f} | {p99[('wifi_room',4)]:15.1f} {p99[('wifi_room',32)]:7.1f} "
          f"{p99[('wifi_room',128)]:7.1f} | {p99[('nr_cell',4)]:12.1f} {p99[('nr_cell',128)]:7.1f} | {p999:15.1f} | {verdict}")
    P("  UWB at 27 Mb/s needs 15 ms per tile at DSC 10 bpp. It cannot carry pixels. It carries touch, angles and heartbeat.")
    SUMMARY["latency_res"] = {k: dict(p99={f"{a[0]}|{a[1]}": b for a, b in v["p99"].items()}, p999=v["p999"], verdict=v["verdict"])
                             for k, v in res.items()}
    SUMMARY["baseline_p99"] = {k: float(np.percentile(v, 99)) for k, v in base.items()}
    P()
    P("D2. the time to draw a full face (a page turn, K = 128 tiles) at the link rate, DSC 10 bpp and VDC-M 6 bpp")
    for o in OPTIONS:
        key = o["key"]
        r = rate_used[key]
        for nm, bpp in (("DSC 10", 10), ("VDC-M 6", 6)):
            ms = TILES * slice_bits(bpp) / (r * 1e9) * 1e3 * (LINE_CODING if key in "abce" else 1)
            P(f"  {key:3} {o['name'][:46]:46s} {nm:8s} {ms:9.2f} ms")
    P()
    P("D3. the tether's own share, mean and p99 of the added delay for K = 4 tiles (ms)")
    for o in OPTIONS:
        key = o["key"]
        dd = tether_up(M, key, rng, N) + tether_down(M, key, rng, N, 4, rate_used[key])
        P(f"  {key:3} mean {dd.mean():7.3f}  p99 {np.percentile(dd, 99):7.3f}  p99.9 {np.percentile(dd, 99.9):7.3f}")
        res[key]["add_mean"] = float(dd.mean())
        res[key]["add_p99"] = float(np.percentile(dd, 99))
    SUMMARY["tether_add"] = {k: dict(mean=v["add_mean"], p99=v["add_p99"]) for k, v in res.items()}
    P()
    P("D4. the warp reads angles. The Core warps from angles that are old when the frame lights.")
    P("    age = angle sample U(0, 2.08 ms) + uplink + warp 0.2 ms + encode 0.1 ms + downlink of one tile + tile scan U(0, 0.26 ms) + LED 0.05 ms")
    P("    error = rate x age. DSP-17 limit 1.0 deg rms; target 0.1 deg (hw/display SPEC 4). With a linear predictor only the jitter remains.")
    P(f"{'opt':4} {'mean age ms':>11} {'rms age':>8} {'jitter sd':>9} | {'35 deg/s':>9} {'100 deg/s':>10} {'300 deg/s':>10}  no predictor | {'100 deg/s':>10} {'300 deg/s':>10}  predictor")
    warp = {}
    for o in OPTIONS:
        key = o["key"]
        if key == "f2":
            continue
        age = (rng.uniform(0, 2.083, N) + tether_up(M, key, rng, N) + 0.2 + 0.1
               + tether_down(M, key, rng, N, 1, rate_used[key]) + rng.uniform(0, 0.26, N) + 0.05)
        ms_ = age.mean()
        rms = math.sqrt(np.mean(age ** 2))
        sd = age.std()
        e = lambda w, a: w * a / 1e3
        warp[key] = dict(mean=ms_, rms=rms, sd=sd, e35=e(35, rms), e100=e(100, rms), e300=e(300, rms),
                         p100=e(100, sd), p300=e(300, sd))
        P(f"{key:4} {ms_:11.2f} {rms:8.2f} {sd:9.2f} | {e(35, rms):9.2f} {e(100, rms):10.2f} {e(300, rms):10.2f}               | "
          f"{e(100, sd):10.3f} {e(300, sd):10.3f}")
    SUMMARY["warp_age"] = warp
    P(f"  The 480 Hz angle sample (mean 1.04 ms) dominates the age. The wired tether adds 0.1 ms.")
    P(f"  Wired: {warp['a']['e100']:.2f} deg rms at 100 deg/s and {warp['a']['e300']:.2f} at 300 deg/s, no predictor. 100 deg/s is a 17.5 deg pull in 0.17 s.")
    P(f"  Wi-Fi 7: {warp['f1']['e100']:.2f} and {warp['f1']['e300']:.2f}; the 300 deg/s case sits at the 1.0 deg limit. 60 GHz jitter (blockage) gives {warp['d']['p300']:.2f} deg with a predictor at 300 deg/s.")
    P(f"  The 0.1 deg target holds only for a wired tether with a predictor at 100 deg/s ({warp['a']['p100']:.3f} deg). [HYPOTHESIS]")
    P()
    P("D5. the touch and angle uplink (the back channel, BC)")
    bc = TILES * 16 * 480 / 1e6 + 800 * 12 * 480 / 1e6
    P(f"  angles: 128 x 16 bit x 480 Hz = {TILES*16*480/1e6:.2f} Mb/s. Raw touch image 800 nodes x 12 bit x 480 Hz = {800*12*480/1e6:.2f} Mb/s.")
    P(f"  total {bc:.2f} Mb/s against the 400 Mb/s of the BC pair. UWB (27 Mb/s) could carry it. Heartbeat 100 us on the sideband.")
    SUMMARY["bc_mbps"] = bc
    # plot
    if HAVE_MPL:
        C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
        fig, ax = plt.subplots(figsize=(8, 4.2))
        keys = [o["key"] for o in OPTIONS if o["key"] != "f2"]
        xs = np.arange(len(keys))
        for i, (K, c) in enumerate(((4, C[0]), (128, C[1]))):
            vals = [res[k]["p99"][("wifi_room", K)] for k in keys]
            ax.bar(xs + (i - 0.5) * 0.38, vals, 0.34, color=c, label=f"K = {K} tiles change")
        ax.axhline(30, color="#5f5e58", lw=1.2)
        ax.text(len(keys) - 0.5, 30.8, "30 ms gate", ha="right", color="#5f5e58", fontsize=9)
        ax.set_xticks(xs)
        ax.set_xticklabels([f"({k[0]})" if k != "f1" else "(f) Wi-Fi 7" for k in keys])
        ax.set_ylabel("p99 input to photon, ms (Wi-Fi room path)")
        ax.set_title("Tether option against the 30 ms gate")
        ax.legend(frameon=False)
        ax.grid(axis="y", color="#e4e3dd", lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.savefig(os.path.join(OUT, "latency_p99.png"), dpi=130, bbox_inches="tight")
        plt.close(fig)
    t.close()
    return rate_used


# ============================================================================
# E. POWER IN THE LINK
# ============================================================================
def const_power_current(v0, r_loop, p_load):
    disc = v0 * v0 - 4 * r_loop * p_load
    if disc < 0:
        return float("nan")
    return (v0 - math.sqrt(disc)) / (2 * r_loop)


def part_e():
    t = Tee("power_link.txt")
    P = t.p
    P("E. POWER IN THE LINK: can the tether carry the Skin power with the data?")
    P("=" * 100)
    skin = SUMMARY["skin_load_w"]
    loads = {"delta": skin["delta session, 250 nits"], "video": skin["video Wi-Fi"], "peak": 3.10 + 0.55 + 0.1}
    P(f"  Skin loads at the connector, W: delta {loads['delta']:.2f}, video {loads['video']:.2f}, peak (full white, 1000 nits, QD) {loads['peak']:.2f}")
    P("  The sinks need 3.40 V (green) at the tile node, so the Skin end must stay above 3.60 V under the peak. [DECISION] hw/energy 03.")
    P()
    rho = 1.72e-8
    awg_d = {24: 0.511e-3, 28: 0.321e-3, 30: 0.255e-3, 34: 0.160e-3}
    P("E1. copper per metre")
    for a, dm in awg_d.items():
        P(f"  {a} AWG: {rho/(math.pi*dm*dm/4):.3f} ohm/m")
    P("  LCP flex strip 0.5 mm x 35 um: " + f"{rho/(0.5e-3*35e-6):.2f} ohm/m")
    P()
    P("E2. designs. VBUS from the Core at v0; the Skin takes constant power. Parallel conductors: n on VBUS, n on GND.")
    P(f"{'design':44} {'v0':>5} {'R loop':>7} | {'I delta':>7} {'loss':>6} | {'I video':>7} {'loss':>6} | {'I peak':>6} {'V at Skin':>9} {'loss':>6} | verdict")
    designs = [
        ("12 leaves only (dock pads), 18 mohm, 2+2 leaves", 4.2, 4 * 0.018 / 4 * 2 / 2, "C0"),
        ("flex 0.3 m, 2 x 0.5 mm strips per side + leaves", 5.0, 2 * (0.98 * 0.3 / 2) + 0.018, "C0"),
        ("flex 0.5 m, 3 strips per side + leaves", 5.0, 2 * (0.98 * 0.5 / 3) + 0.018, "C0"),
        ("round 28 AWG, 2 m, 2+2 wires, at 5 V", 5.0, 2 * (rho / (math.pi * 0.321e-3**2 / 4) * 2 / 2) + 0.018, "C0 edge"),
        ("round 28 AWG, 2 m, 2+2 wires, 12 V, clip buck 93 %", 12.0, 2 * (rho / (math.pi * 0.321e-3**2 / 4) * 2 / 2) + 0.018, "C0"),
        ("hybrid fibre, 28 AWG, 10 m, 20 V, clip buck 93 %", 20.0, 2 * (rho / (math.pi * 0.321e-3**2 / 4) * 10), "C1"),
        ("hybrid fibre, 24 AWG, 30 m, 20 V, clip buck 93 %", 20.0, 2 * (rho / (math.pi * 0.511e-3**2 / 4) * 30), "C1"),
    ]
    out = {}
    for nm, v0, r, cl in designs:
        buck = "buck" in nm
        eff = 0.93 if buck else 1.0
        row = []
        okp = True
        for case in ("delta", "video", "peak"):
            p_ = loads[case] / eff
            i = const_power_current(v0, r, p_)
            loss = i * i * r
            vs = v0 - i * r
            row.append((i, loss, vs))
        # peak voltage at the Skin end: for buck designs the clip regulates, so use the clip input margin (9 V)
        vmin_ok = (row[2][2] >= 3.6) if not buck else (row[2][2] >= 8.0)
        verdict = "pass" if vmin_ok and not math.isnan(row[2][0]) else "FAIL"
        out[nm] = dict(v0=v0, r=r, rows=row, verdict=verdict, cls=cl)
        P(f"{nm:44} {v0:5.1f} {r:7.3f} | {row[0][0]:7.3f} {row[0][1]:6.3f} | {row[1][0]:7.3f} {row[1][1]:6.3f} | "
          f"{row[2][0]:6.3f} {row[2][2]:9.2f} {row[2][1]:6.3f} | {verdict} ({cl})")
    SUMMARY["power_designs"] = {k: dict(v0=v["v0"], r=v["r"], i_peak=v["rows"][2][0], v_peak=v["rows"][2][2],
                                        loss_video=v["rows"][1][1], loss_peak=v["rows"][2][1], verdict=v["verdict"])
                                for k, v in out.items()}
    P("  Losses are heat in the cable, not on the Skin. The buck sits in the clip, so its 7 % loss (0.13 W at video) is clip heat.")
    P()
    P("E3. the leaves as a power path (hw/energy 03 Section 2.1: 18 mohm, 1.5 A per leaf, continuous)")
    for case, w_ in loads.items():
        i = w_ / 4.2
        P(f"  {case:6s} {w_:5.2f} W at 4.2 V: {i:5.2f} A over 2 VBUS leaves = {i/2:4.2f} A each ({100*i/2/1.5:3.0f} % of rating), "
          f"leaf loss {4*0.018*(i/2)**2*1e3:6.1f} mW")
    P("  the leaves carry the Skin power with margin. The pins that matter are the data lanes.")
    P()
    P("E4. the conductor count of the tether that carries both")
    P("  data: 2 lanes x 2 wires (D0, D1) + BC pair + 1 sideband + guard grounds = 8 lines of 100 ohm class")
    P("  power: 2 VBUS + 2 GND (flex or round) at 5 V up to 0.5 m; 2 VHV + 2 GND at 12 to 20 V beyond 1 m with a clip buck")
    P("  flex 0.3 m with 12 conductors: mass 1.3 g, 6 mm wide at 0.5 mm pitch; round 28 AWG micro bundle, 2 m: 8 g")
    P()
    P("E5. radios and the cell. No power rides on a radio. The Skin then holds a cell.")
    P(f"  video at {loads['video']:.2f} W plus a 60 GHz end (0.6 W) for 2 h: {(loads['video']+0.6)*2/0.9:.1f} Wh = {(loads['video']+0.6)*2/0.9/0.25:.0f} g of cell at 250 Wh/kg")
    P(f"  video at {loads['video']:.2f} W plus a Wi-Fi 7 end (1.0 W) for 2 h: {(loads['video']+1.0)*2/0.9:.1f} Wh = {(loads['video']+1.0)*2/0.9/0.25:.0f} g")
    P(f"  that is 81 to 97 % of the 5.9 Wh L.6.0 body battery. A radio end gives the Split no mass gain.")
    P()
    P("E6. a Skin with no cell and a hot-unplug: the safe screen needs 0.12 W for 60 s = 7.2 J = 2 mWh. One tile cell holds 46 mWh.")
    t.close()
    return loads


# ============================================================================
# F. CONNECTOR LIFE
# ============================================================================
def part_f():
    t = Tee("connector_life.txt")
    P = t.p
    P("F. CONNECTOR AND CABLE LIFE. A tether is a product. [GENERAL] unless marked.")
    P("=" * 100)
    cls = [("FPC ZIF or board-to-board", 30), ("USB-C receptacle, rated [PUBLICATION] USB-IF", 10000),
           ("pogo or gold leaf, consumer wearable class", 30000), ("expanded-beam optical, dust tolerant", 5000),
           ("near-field coupler on a kinematic seat", 100000), ("flex, RA copper, r = 5 mm, bends", 200000)]
    P(f"{'part':56} {'cycles':>8} | years at 1, 4, 20 mates (or bends) a day")
    life = {}
    for nm, c in cls:
        yrs = [c / (r * 365) for r in (1, 4, 20)]
        life[nm] = yrs
        P(f"{nm:56} {c:8d} | {yrs[0]:8.1f} {yrs[1]:8.1f} {yrs[2]:8.1f}")
    P("  A ZIF connector gives 30 cycles: one month at one mate a day. It is not a user connector.")
    P("  Gold wear: a 0.5 to 3 um gold layer on a leaf wears to the nickel at 5 000 to 50 000 cycles; contact resistance then climbs. [GENERAL]")
    P("  A seat that mates 4 times a day on 12 leaves needs 10 000 cycles for 7 years. Pass HC-L7.")
    SUMMARY["life_years"] = {k: v for k, v in life.items()}
    t.close()


# ============================================================================
# G. DISTANCE CLASSES
# ============================================================================
def part_g():
    t = Tee("distance_classes.txt")
    P = t.p
    P("G. DISTANCE CLASSES (hw/core/BRIEF.md Section 8): C0 up to 2 m, C1 up to about 30 m, C2 kilometres")
    P("=" * 100)
    P("G1. which option exists at which class")
    P(f"{'opt':4} {'link':58} {'C0':>5} {'C1':>5} {'C2':>5}   note")
    tab = [
        ("a", "contact leaves on a seat or dock", "yes", "no", "no", "touching; 0 m"),
        ("b", "thin flex or ribbon", "yes", "no", "no", "0.25 to 0.8 m by loss (B2); twinax 1 to 3 m"),
        ("b2", "active copper or round cable (USB4 class)", "yes", "no", "no", "2 m passive, to 5 m active; not a Leaf part"),
        ("c", "optical fibre tether", "yes", "yes", "no", "to 100 m by loss; power by copper pair or local"),
        ("d", "60 GHz close-range radio", "yes", "LOS only", "no", "to 18 m LOS at 2.6 Gb/s, 8 m at 5.1 Gb/s (B1); a hand blocks it"),
        ("e", "near-field coupler in-plane", "mm only", "no", "no", "a seat, not a tether"),
        ("f1", "Wi-Fi 7", "yes", "yes", "no", "outdoors 100 m to 1 km only at low rate (far seat)"),
        ("f2", "UWB", "yes", "yes", "no", "control, ranging, no pixels"),
        ("g", "the Leaf radios: 5G modem U5, Wi-Fi 7 U2A, bar and ring antennas", "yes", "yes", "yes", "slice streams only, tens to 150 Mb/s"),
    ]
    for r in tab:
        P(f"{r[0]:4} {r[1]:58} {r[2]:>5} {r[3]:>5} {r[4]:>5}   {r[5]}")
    P()
    P("G2. the stream that crosses each class")
    uc = SUMMARY["use_cases"]
    P("  C0 and C1 wired or fibre: DSC slices, 0.004 to 13.1 Gb/s (use cases, Section A3).")
    P("  C1 radio: DSC or VDC-M slices of the changed tiles, 0.2 to 3 Gb/s at 60 Hz. 60 GHz carries up to about 4 Gb/s net in line of sight.")
    P("  C2: only the Leaf radios. The stream is an AV1 or HEVC slice stream. The bitrate model below uses bits per pixel of coded video.")
    P(f"{'content':36} {'fps':>4} {'bpp (coded)':>11} {'dirty':>6} {'Mb/s':>8}   [HYPOTHESIS] AV1 low-latency slices, screen content costs more per changed pixel")
    c2 = [
        ("static page, cursor and clock", 10, 0.80, 0.002),
        ("UI, typing, small animation", 60, 0.50, 0.06),
        ("scroll at 60 Hz", 60, 0.12, 0.85),
        ("video 16:9, 30 fps", 30, 0.09, 0.28),
        ("video vertical, 60 fps", 60, 0.04, 0.89),
        ("full motion, 240 Hz game", 240, 0.025, 1.0),
    ]
    c2r = {}
    for nm, fps, bpp, dirty in c2:
        mbps = PX * dirty * fps * bpp / 1e6
        c2r[nm] = (mbps, mbps * 4)
        P(f"{nm:36} {fps:4d} {bpp:11.3f} {dirty:6.3f} {mbps:8.1f}  (high estimate, bpp x 4: {mbps*4:.1f})")
    P("  Range of C2 stream: 0.1 Mb/s (static) to about 150 Mb/s (full motion at 240 Hz), the figure of the brief. The compressed")
    P("  rate is 40 to 100 times under the DSC rate: DSC is intra-only at 3:1 to 5:1. AV1 and HEVC use motion search and inter frames.")
    SUMMARY["c2_mbps"] = c2r
    P("  The ratio DSC 10 bpp / AV1 for full motion at 240 Hz: "
      f"{SUMMARY['dsc10_240_line_gbps']*1e3/c2r['full motion, 240 Hz game'][0]:.0f}:1 (low) to {SUMMARY['dsc10_240_line_gbps']*1e3/c2r['full motion, 240 Hz game'][1]:.0f}:1 (high).")
    P()
    P("G3. what stays on the Skin at each class")
    P(f"  C0 and C1 wired: the common Skin of Section C (hubs with DSC decoders, no frame store, no compositor). {SUMMARY['skin_mass_g']:.0f} g, {SUMMARY['skin_thickness_mm']:.2f} mm.")
    P("  C1 radio (Wi-Fi 7, 60 GHz): the common Skin + a radio end + a cell + a small link MAC core. Decoder stays the DSC hub.")
    P("  C2: the Skin is the L.6.0 Leaf. It needs, because the slice stream is 100 times thinner and the path is long:")
    fs_raw = W * H * 3 / 1e6
    fs_10 = W * H * 30 / 8 / 1e6
    P(f"    U6 AV1 and HEVC slice decoder; the frame store: {fs_raw:.2f} MB (8 bit RGB), {fs_10:.1f} MB (10 bit), 30.7 MB for the more-room canvas;")
    P("    U1 compositor: cursor, scroll offset, typed-glyph echo, stretch warp (4.92 Gtap/s); U2A, U2B, U5; U7; the cell 5.9 Wh.")
    P("  Why the compositor and the store cannot leave: at C2 the round trip is 1 to 20+ ms by air alone plus the fibre (0.005 ms per km each way,")
    P("  0.1 ms at 20 km). The predicted-action path of Part 21 (4.4 ms mean) needs the store on the Leaf.")
    l2 = fs_raw
    P("  The C2 Skin is the Leaf: the smallest Skin is a C0 and C1 result. [HYPOTHESIS]")
    P()
    P("G4. mass and load of the Skin by class (video session, Wi-Fi)")
    sk = SUMMARY["skin_mass_g"]
    P(f"  C0 wired: Skin {sk:.0f} g, load {SUMMARY['skin_load_w']['video Wi-Fi']:.2f} W, no cell (bridge only)")
    P(f"  C1 fibre with clip: Skin {sk:.0f} g plus a 4 g clip, load {SUMMARY['skin_load_w']['video Wi-Fi']:.2f} W")
    cl_d = SUMMARY["clip"]["d"]
    cl_f = SUMMARY["clip"]["f1"]
    P(f"  C1 60 GHz: Skin {sk + cl_d['mass']:.0f} g with its cell ({cl_d['wh']:.1f} Wh), load {SUMMARY['skin_load_w']['video Wi-Fi'] + 0.6:.2f} W")
    P(f"  C1 Wi-Fi 7: Skin {sk + cl_f['mass']:.0f} g with its cell ({cl_f['wh']:.1f} Wh), load {SUMMARY['skin_load_w']['video Wi-Fi'] + 1.0:.2f} W")
    P(f"  C2: the Leaf body {SUMMARY['body_mass_g']:.0f} g plus the module of 20 g; load 2.02 W (delta) and 3.27 W (video), hw/energy 04 body plus ring")
    t.close()


# ============================================================================
# H. GATES
# ============================================================================
def part_h():
    t = Tee("gates.txt")
    P = t.p
    P("H. THE PROPOSED GATES HC-L1 TO HC-L11, evaluated by the model. A PASS here is a model result, not a measurement.")
    P("=" * 100)
    res = []

    def gate(name, text, ok, val):
        res.append((name, ok))
        P(f"  {name:6s} {'PASS' if ok else 'FAIL':5s} {text}   [{val}]")

    d = SUMMARY["dsc10_240_line_gbps"]
    gate("HC-L1", "design case DSC 10 bpp 240 Hz fits the wired tether with 25 % margin (need x 1.25 <= 19.4 Gb/s)",
         d * 1.25 <= LEAF_PAYLOAD, f"{d*1.25:.2f} vs {LEAF_PAYLOAD:.2f}")
    gate("HC-L1b", "same case on one lane pair with VDC-M 6 bpp (the one-pair fallback)",
         TILES * slice_bits(6) * 240 / 1e9 * LINE_CODING <= LEAF_PAYLOAD / 2, f"{TILES*slice_bits(6)*240/1e9*LINE_CODING:.2f} vs {LEAF_PAYLOAD/2:.2f}")
    gate("HC-L2", "compression within the published visually lossless range (ratio <= 3.75:1 DSC, 5:1 VDC-M, from 10 bit)",
         True, "design 3:1; the Lead's 6:1 is outside and is withdrawn")
    sk = SUMMARY["skin_load_w"]
    gate("HC-L3a", "Skin load, delta session, under 1.73 W still-air limit",
         sk["delta session, 250 nits"] <= V_LIM_STILL, f"{sk['delta session, 250 nits']:.2f} W")
    gate("HC-L3b", "Skin load, video, under 2.37 W light-wind limit",
         sk["video Wi-Fi"] <= V_LIM_WIND, f"{sk['video Wi-Fi']:.2f} W")
    gate("HC-L3c", "Skin load, video, under 1.73 W still-air limit",
         sk["video Wi-Fi"] <= V_LIM_STILL, f"{sk['video Wi-Fi']:.2f} W")
    gate("HC-L3d", "Skin load, full motion 240 Hz, under 1.73 W still-air limit",
         sk["full motion 240 Hz, 250 nits"] <= V_LIM_STILL, f"{sk['full motion 240 Hz, 250 nits']:.2f} W")
    r2 = SUMMARY["skin_load_r2_w"]["video Wi-Fi"]
    gate("HC-L3e", "reading R2 (the whole Hub domain sits on the Skin): video under 2.37 W light-wind limit",
         r2 <= V_LIM_WIND, f"{r2:.2f} W")
    pw = SUMMARY["power_designs"]
    nm = "flex 0.3 m, 2 x 0.5 mm strips per side + leaves"
    gate("HC-L4", "tether power from 5.0 V: peak 3.75 W, Skin end at or above 3.60 V, loop at or under 0.35 ohm, cable loss under 0.25 W",
         pw[nm]["v_peak"] >= 3.6 and pw[nm]["r"] <= 0.35 and pw[nm]["loss_peak"] <= 0.25,
         f"{pw[nm]['v_peak']:.2f} V, {pw[nm]['r']:.3f} ohm, {pw[nm]['loss_peak']:.2f} W")
    la = SUMMARY["latency_res"]
    gate("HC-L5a", "wired tether (a): p99 at or under 30 ms on Wi-Fi room and 5G cell paths, K = 128",
         la["a"]["verdict"] == "holds for all K", f"{la['a']['p99']['wifi_room|128']:.1f} ms")
    gate("HC-L5b", "tether adds under 0.1 ms mean and 0.5 ms p99 at K = 4 (wired)",
         SUMMARY["tether_add"]["a"]["p99"] <= 0.5, f"{SUMMARY['tether_add']['a']['p99']:.3f} ms")
    gate("HC-L5c", "Wi-Fi 7 tether (f): p99 at or under 30 ms for a full-face change",
         la["f1"]["verdict"] == "holds for all K", f"{la['f1']['p99']['wifi_room|128']:.1f} ms")
    gate("HC-L5d", "60 GHz tether (d): p99.9 at or under 30 ms (blockage)",
         la["d"]["p999"] <= 30, f"{la['d']['p999']:.1f} ms")
    wa = SUMMARY["warp_age"]
    gate("HC-L6", "angle age: rms error at 100 deg/s at or under 1.0 deg without a predictor (wired)",
         wa["a"]["e100"] <= 1.0, f"{wa['a']['e100']:.2f} deg")
    gate("HC-L6b", "angle age: rms error at 100 deg/s at or under 1.0 deg without a predictor (Wi-Fi 7)",
         wa["f1"]["e100"] <= 1.0, f"{wa['f1']['e100']:.2f} deg")
    gate("HC-L8", "Skin mass without cells at or under 20 g and thickness under 1.2 mm",
         SUMMARY["skin_mass_g"] <= 20 and SUMMARY["skin_thickness_mm"] < 1.2,
         f"{SUMMARY['skin_mass_g']:.1f} g, {SUMMARY['skin_thickness_mm']:.2f} mm")
    nlife = SUMMARY["life_years"]["pogo or gold leaf, consumer wearable class"][1]
    gate("HC-L7", "seat life at 4 mates a day at or above 7 years (needs 10 400 cycles)", nlife >= 7, f"{nlife:.1f} years at 30 000 cycles")
    gate("HC-L10", "the mesh forces the decoder: the stream needs at least 2.08:1 with one root hinge broken (DSC 10 bpp gives 3:1)",
         SUMMARY["min_ratio_mesh"][1] <= 3.0, f"{SUMMARY['min_ratio_mesh'][1]:.2f}:1 needed")
    gate("HC-L11", "C2 slice stream at or under 150 Mb/s for every use case (high estimate)",
         max(v[1] for v in SUMMARY["c2_mbps"].values()) <= 150, f"{max(v[1] for v in SUMMARY['c2_mbps'].values()):.0f} Mb/s")
    P("  HC-L9  TEST  safe screen within 100 ms of heartbeat loss, thermal trip independent of the Core, no key on the Skin that signs a spend (bench test, no model)")
    P()
    n_ok = sum(1 for _, ok in res if ok)
    P(f"  {n_ok} of {len(res)} model checks pass. The FAIL lines are the damage to the Split on the link alone.")
    SUMMARY["gates"] = {n: ok for n, ok in res}
    t.close()


def pixel_plot(full):
    if not HAVE_MPL:
        return
    C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
    uc = SUMMARY["use_cases"]
    names = list(uc.keys())
    tile = [uc[n]["tile_dsc10_mbps"] / 1e3 for n in names]
    strip = [uc[n]["strip_dsc10_mbps"] / 1e3 for n in names]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ys = np.arange(len(names))
    ax.barh(ys - 0.19, tile, 0.34, color=C[0], label="tile skip")
    ax.barh(ys + 0.19, strip, 0.34, color=C[1], label="strip skip (16 lines)")
    ax.set_xscale("log")
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    for x, lab in ((19.4, "two leaf pairs 19.4"), (2.5, "Wi-Fi 7 typical 2.5"), (0.027, "UWB 0.027")):
        ax.axvline(x, color="#5f5e58", lw=1)
        ax.text(x * 1.05, 0.99, lab, fontsize=8, color="#5f5e58", rotation=90, va="top", transform=ax.get_xaxis_transform())
    ax.set_xlabel("stream, Gb/s, DSC 10 bpp (log)")
    ax.set_title("Pixel stream by use case, with link capacity")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
    ax.grid(axis="x", color="#e4e3dd", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(os.path.join(OUT, "pixel_budget.png"), dpi=130, bbox_inches="tight")
    plt.close(fig)
    # 60 GHz
    fig, ax = plt.subplots(figsize=(7, 4))
    ds = np.arange(0.1, 30, 0.1)
    for (blk, gc, lab, c) in ((0.0, 8.8, "line of sight, Core 8.8 dBi", C[2]), (0.0, 20.0, "line of sight, Core 20 dBi", C[0]),
                              (20.0, 20.0, "blocked 20 dB, Core 20 dBi", C[1])):
        r = [rate_60ghz(d_, blockage_db=blk, core_gain_dbi=gc)[0][0] * 0.8 for d_ in ds]
        ax.plot(ds, r, color=c, label=lab)
    ax.set_xscale("log")
    ax.set_xlabel("distance, m")
    ax.set_ylabel("net payload, Gb/s")
    ax.set_title("60 GHz Skin link, net rate against distance")
    ax.axhline(13.43, color="#5f5e58", lw=1)
    ax.text(0.11, 13.8, "design case 13.4", fontsize=8, color="#5f5e58")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(color="#e4e3dd", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(os.path.join(OUT, "rate60.png"), dpi=130, bbox_inches="tight")
    plt.close(fig)


def main():
    full, wire, mh = part_a()
    part_b()
    part_c(mh)
    part_d()
    part_e()
    part_f()
    part_g()
    part_h()
    pixel_plot(full)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(SUMMARY, f, indent=1, default=float)


if __name__ == "__main__":
    main()
