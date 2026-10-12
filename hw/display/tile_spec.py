#!/usr/bin/env python3
"""tile_spec.py - the numbers of one 508 ppi micro-LED tile.

Budlum Leaf L.6.0, Display team, hw/display/.

Sections
  A. the drive scheme: LTPS TFT pixel circuits against CMOS micro-ICs (uIC),
     transistor count per pixel and the area fit in a 50 um pixel
  B. the PWM: bit depth, LSB time, sub-frame split, flicker fundamental
  C. the TGV set: count, pitch, diameter, resistance, power-grid IR drop
  D. the power of one tile at 500 and 1 000 nits, full white, both emitter
     options (direct RGB and blue + quantum-dot conversion)

Every input that is not a decision of Part 21 is tagged in the comment.
Run:  python3 tile_spec.py
"""
import numpy as np

PITCH = 50.0e-6          # m                                  [DECISION]
N = 200                  # px per edge                        [DECISION]
FPS = 240                # Hz                                 [DECISION]
TILE_A = (N * PITCH) ** 2
H, C, Q = 6.626e-34, 2.998e8, 1.602e-19

print("=" * 72)
print("A. THE DRIVE SCHEME: does the pixel circuit fit in 50 x 50 um?")
print("=" * 72)
pix_area = (PITCH * 1e6) ** 2                       # 2 500 um2
# --- LTPS TFT on glass ---------------------------------------------------
# a TFT with its contacts at a 2.0-2.5 um rule: 50-110 um2 (shipping OLED
# phones at ~500 ppi fit 7T1C x 3 sub-pixels).                [GENERAL]
tft_area = np.array([50.0, 80.0, 110.0])
cap_area = 80.0          # um2 for ~0.1 pF at 1.24 fF/um2 (50 nm SiNx)
route_frac = 0.40        # area taken by scan, emit, sweep, data and power lines
circuits = {
    "7T1C PAM (OLED class)": (7, 1),
    "8T2C sweep PWM (uLED, minimum)": (8, 2),
    "13T3C PWM + PAM + Vth comp. (uLED)": (13, 3),
}
usable = pix_area * (1 - route_frac)
print(f"pixel area {pix_area:.0f} um2, usable after routing {usable:.0f} um2")
for name, (t, c) in circuits.items():
    need = 3 * (t * tft_area + c * cap_area)
    fits = ["fits" if n <= usable else "NO" for n in need]
    print(f"  {name:38s} {3*t:3d}T{3*c}C per pixel  area {need[0]:5.0f}/{need[1]:5.0f}/{need[2]:5.0f} um2  -> {fits}")
print("  verdict: a uLED-grade PWM pixel (13T3C x 3) does not fit an LTPS pixel at 50 um.")
print()
# --- CMOS micro-IC, one per 2 x 2 pixel cell (12 sub-pixels) --------------
bits = 12                  # PWM bits per sub-pixel
sub = 12                   # sub-pixels served (4 px x RGB); the S sites are repair spares
uic = {
    "bus receiver + address match (7 b row addr + strobe)": 400,
    "back buffer: 144 b shift/load register, 20T DFF": sub * bits * 20,
    "front buffer: 144 b latch, 8T":                     sub * bits * 8,
    "12 b equality comparators, 12 x (12 XNOR + tree)":  sub * (bits * 10 + 30),
    "set/reset output latches":                          sub * 12,
    "12 b PWM counter + 4-segment bit-split logic":      600,
    "current sinks, 2-level PAM, 16 outputs incl. S":    16 * 8,
    "bias, reference trim DAC, POR, test":               600,
}
t_uic = sum(uic.values())
for k, v in uic.items():
    print(f"  uIC  {k:52s} {v:6d} T")
print(f"  uIC total {t_uic} T  ->  {t_uic/4:.0f} T per pixel ({t_uic/12:.0f} T per sub-pixel)")
for node, dens in (("40 nm HV, 2.0 MT/mm2 effective", 2.0), ("28 nm HV (DDI class), 5.0 MT/mm2", 5.0)):
    area = t_uic / dens          # um2, since 1 MT/mm2 = 1 T/um2
    print(f"  {node:34s} die {area:6.0f} um2")
street = PITCH * 1e6 - 12.0      # clear street between quad clusters: 50 - (7+5) = 38 um
uic_w, uic_l = 20.0, 85.0
print(f"  street between pixel clusters {street:.0f} um. uIC 20 x 85 um = {uic_w*uic_l:.0f} um2 in the "
      f"horizontal street, {(street-uic_w)/2:.0f} um clear each side")
print(f"  uIC share of the 100 x 100 um cell: {uic_w*uic_l/1e4*100:.1f} %; uICs per tile {(N//2)**2}, "
      f"per device {(N//2)**2*128}")
print("  verdict: the 28 nm HV uIC (1 541 um2) fits the 1 700 um2 street slot. The 40 nm uIC (3 852 um2) does not.")
print()

print("=" * 72)
print("B. THE PWM")
print("=" * 72)
frame = 1 / FPS
segments = 4
lsb = frame / 2 ** bits
print(f"frame {frame*1e3:.3f} ms, {bits}-bit PWM, LSB {lsb*1e6:.3f} us, counter clock {1/lsb/1e6:.3f} MHz")
print(f"bit-split into {segments} segments -> flicker fundamental {FPS*segments} Hz")
pam_lo = 1 / 16
print(f"2-level PAM (low = 1/{int(1/pam_lo)}) -> {bits + 4} bit effective range, "
      f"smallest step at 1 000 nits = {1000/2**bits*pam_lo*1e3:.1f} mnit")
print(f"uLED rise and fall ~10-50 ns [GENERAL], so the {lsb*1e6:.2f} us LSB is {lsb/50e-9:.0f}x the edge")
print(f"data per uIC per frame: {sub*bits} b; per tile per frame {(N//2)**2*sub*bits/1e6:.2f} Mb; "
      f"raw per tile {(N//2)**2*sub*bits*FPS/1e6:.1f} Mb/s")
print()

print("=" * 72)
print("C. THE TGV SET of the carrier glass")
print("=" * 72)
glass_t = 150e-6          # m, carrier glass (of the 0.25 mm glass-LED-glass)
d_tgv = 12e-6             # m, via diameter, Cu filled (LIDE class, 10:1)  [PUBLICATION] LPKF
rho = 1.72e-8
r_tgv = rho * glass_t / (np.pi * d_tgv ** 2 / 4)
rows_uic = N // 2
tgv = {
    "row-bus data, 2 per uIC row (redundant pair)": 2 * rows_uic,
    "clock (H-tree roots), 4 per tile x 2": 8,
    "latch / frame strobe x 2": 4,
    "VLED_GB (3.3 V) power": 16,
    "VLED_R (2.8 V) power": 16,
    "VDD core (0.9 V)": 8,
    "GND": 32,
    "test, thermistor and seam sense": 4,
}
n_tgv = sum(tgv.values())
for k, v in tgv.items():
    print(f"  {k:46s} {v:4d}")
print(f"  total TGVs per tile {n_tgv}; per device {n_tgv*128}")
print(f"  via d {d_tgv*1e6:.0f} um in {glass_t*1e6:.0f} um glass (AR {glass_t/d_tgv:.1f}:1), R = {r_tgv*1e3:.1f} mOhm")
print("  data vias: one column at the tile centre line, 100 um pitch (one per uIC row), in the street")
print("  intersections at (50, 50) um mod 100 um; power vias on a 2.5 mm grid; minimum pitch 100 um = 8.3 d")
print()
# IR drop of the front power mesh from 16 feed vias, at 1 000 nits (current from part D)
rs_mesh = rho / 3e-6 / 0.30          # 3 um Cu, 30 % of the area as mesh  [HYPOTHESIS]


def ir_drop(I_tile, n_feed):
    # each feed serves a disc of area A/n; drop of a uniformly loaded disc fed at its centre:
    # dV = I_cell * Rs / (4 pi) * (2 ln(R/r) - 1)
    Rcell = np.sqrt(TILE_A / n_feed / np.pi)
    Icell = I_tile / n_feed
    return Icell * rs_mesh / (4 * np.pi) * (2 * np.log(Rcell / (d_tgv / 2)) - 1)


print("=" * 72)
print("D. THE POWER OF ONE TILE, FULL WHITE, D65")
print("=" * 72)


def g(x, mu, s1, s2):
    s = np.where(x < mu, s1, s2)
    return np.exp(-0.5 * ((x - mu) / s) ** 2)


def cmf(lam):  # Wyman, Sloan, Shirley 2013 multi-lobe fit of CIE 1931 2 deg  [PUBLICATION]
    x = 1.056 * g(lam, 599.8, 37.9, 31.0) + 0.362 * g(lam, 442.0, 16.0, 26.7) - 0.065 * g(lam, 501.1, 20.4, 26.2)
    y = 0.821 * g(lam, 568.8, 46.9, 40.5) + 0.286 * g(lam, 530.9, 16.3, 31.1)
    z = 1.217 * g(lam, 437.0, 11.8, 36.0) + 0.681 * g(lam, 459.0, 26.0, 13.8)
    return x, y, z


lam = np.arange(380.0, 781.0, 0.5)
X_, Y_, Z_ = cmf(lam)


def primary(peak, fwhm):
    s = fwhm / 2.3548
    sp = np.exp(-0.5 * ((lam - peak) / s) ** 2)
    sp /= np.trapezoid(sp, lam)               # 1 W of radiation
    XYZ = np.array([np.trapezoid(sp * f, lam) for f in (X_, Y_, Z_)]) * 683.0
    mean_l = np.trapezoid(sp * lam, lam)
    return XYZ, mean_l                        # lm-scaled XYZ per W, mean wavelength


options = {
    # name: [(peak, fwhm, EQE at the operating point, rail V)] for R, G, B
    # EQE at 5 um with ALD sidewall passivation, low current density.      [HYPOTHESIS]
    "direct RGB, InGaN R/G/B 5 um": [(625, 45, 0.05, 2.8), (528, 30, 0.12, 3.3), (462, 20, 0.20, 3.3)],
    "blue 5 um + QD R/G (2 red sites)": [(630, 25, None, 3.3), (530, 25, None, 3.3), (462, 20, 0.20, 3.3)],
}
# QD conversion: QY 0.90, absorption with a blue-cut DBR 0.95, out-coupling of the
# converter 0.60, Stokes ratio from the photon energies.                  [HYPOTHESIS]
QD_QY, QD_ABS, QD_OUT = 0.90, 0.95, 0.60
xw, yw = 0.3127, 0.3290                        # D65
Wxyz = np.array([xw / yw, 1.0, (1 - xw - yw) / yw])
T_STACK = 0.85        # top glass 0.92 x OCA 0.99 x PC cap with AgNW 0.93   [HYPOTHESIS]
DRV = 0.90            # current-sink efficiency share left after headroom is in the rail V
OVERHEAD = {"uIC counters and latches (10 000 x 0.16 uW)": 1.6e-3,
            "uIC bias and leakage (10 000 x 0.05 uW)": 0.5e-3,
            "row buses (346 Mb/s x 0.8 pJ/b)": 0.28e-3,
            "tile hub: DSC decode, demura, 4 retimed ports (avg)": 3.0e-3}
ov = sum(OVERHEAD.values())
results = {}
for name, prim in options.items():
    XYZs, mls = zip(*(primary(p, f) for p, f, *_ in prim))
    M = np.column_stack(XYZs)                  # columns: XYZ per W of R, G, B radiation
    for nits in (500, 1000):
        flux = np.pi * nits * TILE_A / T_STACK      # lm leaving the emitters (Lambertian)
        w = np.linalg.solve(M, Wxyz * flux)         # W of radiation per primary
        P = 0.0
        detail = []
        for (peak, fwhm, eqe, vr), wr, ml in zip(prim, w, mls):
            ephot = H * C / (ml * 1e-9)
            if eqe is None:                        # QD converted colour, pumped by blue
                eqe_b = prim[2][2]
                stokes = 462.0 / ml
                eqe = eqe_b * QD_QY * QD_ABS * QD_OUT * stokes * (ml / 462.0)  # photons out per electron
            I = wr / ephot / eqe * Q
            nchip = 2 if (peak >= 620 and "QD" in name) else 1
            Pe = I * vr / DRV
            P += Pe
            detail.append((peak, wr * 1e3, I * 1e3, Pe * 1e3, nchip))
        results[(name, nits)] = P
        print(f"{name} @ {nits} nits: flux at emitters {flux*1e3:.1f} mlm, radiation "
              f"{sum(w)*1e3:.3f} mW, LER {flux/sum(w):.0f} lm/W")
        for peak, wr, I, Pe, nc in detail:
            print(f"     {peak} nm: {wr:6.3f} mW optical, {I:6.3f} mA, {Pe:6.2f} mW electric "
                  f"({I/(N*N)/nc*1e6:.2f} uA per chip, J = {I/(N*N)/nc/(5e-4**2):.0f} A/cm2 at 100 % duty)")
        print(f"     LED power {P*1e3:.1f} mW + overhead {ov*1e3:.1f} mW = {(P+ov)*1e3:.1f} mW per tile, "
              f"{(P+ov)*128:.2f} W per device full white")
print()
for k, v in OVERHEAD.items():
    print(f"  overhead: {k:52s} {v*1e3:.2f} mW")
I1000 = results[("direct RGB, InGaN R/G/B 5 um", 1000)] / 3.3
print(f"  front-mesh IR drop at 1 000 nits, 16 feeds per rail: {ir_drop(I1000, 16)*1e3:.2f} mV "
      f"(mesh {rs_mesh*1e3:.1f} mOhm/sq)")
print(f"  stretched view: to hold the mean luminance at 25 % stretch the pixels run x{1.2544**2:.2f}, "
      f"at 41 % x2.00")
