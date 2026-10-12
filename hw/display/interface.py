#!/usr/bin/env python3
"""interface.py - the display data path: U1 -> 12 bar leaves -> seat tile ->
hinge mesh -> 128 tile hubs -> 10 000 uICs per tile.

Budlum Leaf L.6.0, Display team, hw/display/.

Sections
  A. the bandwidth of 1600 x 3200 at 240 Hz, raw and compressed
  B. the 12 leaves: the display share and the symmetric pin map
  C. the hinge mesh: the worst hinge load for each of the four seat tiles,
     by an optimal flow (LP) and by the XY routing the hub runs, and with
     one root hinge broken
  D. the lanes per hinge, the lines per hinge, and the fit in the hinge
     copper (strain, resistance, reflection)
  E. the per-tile addressing and the latency of the mesh

Run:  python3 interface.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog

W, Hh, FPS = 1600, 3200, 240
NX, NY = 8, 16
TILES = NX * NY
PX_T = 200 * 200

print("=" * 72)
print("A. BANDWIDTH")
print("=" * 72)
raw24 = W * Hh * FPS * 24
raw30 = W * Hh * FPS * 30
print(f"raw 24 b/px {raw24/1e9:.2f} Gb/s, raw 30 b/px {raw30/1e9:.2f} Gb/s")
modes = {"DSC 1.2b, 8 bpp (24 b in, 3:1)": 8, "DSC 1.2b, 10 bpp (30 b in, 3:1)": 10,
         "VDC-M 1.2, 6 bpp (30 b in, 5:1)": 6}
PKT = 1.06      # packet header, CRC, sync and idle share   [HYPOTHESIS]
LINE = 132 / 128
for k, bpp in modes.items():
    bw = W * Hh * FPS * bpp
    print(f"  {k:34s} {bw/1e9:6.2f} Gb/s payload, {bw*PKT*LINE/1e9:6.2f} Gb/s on the wire, "
          f"{bw/TILES/1e6:6.1f} Mb/s per tile")
DESIGN_BPP = 10
total = W * Hh * FPS * DESIGN_BPP * PKT * LINE
per_tile = total / TILES
print(f"design case: DSC 10 bpp, one 200 x 200 slice per tile -> {total/1e9:.2f} Gb/s total, "
      f"{per_tile/1e6:.1f} Mb/s per tile")
print("the stream size does not change with stretch: U1 sends the warped 200 x 200 tile images.")
print()

print("=" * 72)
print("B. THE 12 BAR LEAVES")
print("=" * 72)
LEAF_RATE = 10.0e9     # per pair, USB 3.2 Gen 2 class over a short leaf  [HYPOTHESIS] gate MON-23
pins = ["VSYS", "GND", "D0+", "D0-", "GND", "BC+", "BC-", "GND", "D1-", "D1+", "GND", "VSYS"]
mir = {"D0+": "D1+", "D0-": "D1-", "D1+": "D0+", "D1-": "D0-", "BC+": "BC-", "BC-": "BC+"}
sym = all(pins[11 - i] == mir.get(pins[i], pins[i]) for i in range(12))
print("leaf  1..12 at 0.8 mm pitch:", " ".join(pins))
print(f"mirror (front/back flip, 180 deg turn) maps the map onto itself, up to lane and polarity swap: {sym}")
cap = 2 * LEAF_RATE * 128 / 132
print(f"two display pairs at {LEAF_RATE/1e9:.0f} Gb/s: {cap/1e9:.2f} Gb/s payload capacity, "
      f"need {total*132/128/1e9:.2f} -> margin {(cap/(total*132/128)-1)*100:.0f} %")
one = LEAF_RATE * 128 / 132
vdcm = W * Hh * FPS * 6 * PKT
print(f"one pair lost: VDC-M 6 bpp needs {vdcm/1e9:.2f} Gb/s on {one/1e9:.2f} -> "
      f"{'fits' if vdcm < one else 'does not fit'}")
print("display uses 4 leaves (D0, D1) + the shared GND; BC is the 400 Mb/s back channel")
print("(touch at 480 Hz, hinge angles, seam sense, tile telemetry, enumeration).")
print()

print("=" * 72)
print("C. THE HINGE MESH")
print("=" * 72)
nodes = [(x, y) for y in range(NY) for x in range(NX)]
idx = {n: i for i, n in enumerate(nodes)}
und = []
for x, y in nodes:
    if x + 1 < NX:
        und.append(((x, y), (x + 1, y)))
    if y + 1 < NY:
        und.append(((x, y), (x, y + 1)))
print(f"{TILES} tiles, {len(und)} hinges (each tile joins its 4 edge neighbours at its 4 corners)")
SEATS = {"top edge (3,0)": (3, 0), "bottom edge (4,15)": (4, 15),
         "left edge (0,7)": (0, 7), "right edge (7,8)": (7, 8)}


def lp_min_max(root, broken=()):
    arcs = []
    for a, b in und:
        if (a, b) in broken or (b, a) in broken:
            continue
        arcs += [(a, b), (b, a)]
    nA = len(arcs)
    c = np.zeros(nA + 1)
    c[-1] = 1.0
    Aeq = np.zeros((TILES, nA + 1))
    beq = np.full(TILES, -per_tile)
    beq[idx[root]] = per_tile * (TILES - 1)
    for j, (a, b) in enumerate(arcs):
        Aeq[idx[a], j] += 1.0
        Aeq[idx[b], j] -= 1.0
    # load of a hinge = flow both ways; bound by t
    Aub, bub = [], []
    seen = {}
    for j, (a, b) in enumerate(arcs):
        key = frozenset((a, b))
        seen.setdefault(key, []).append(j)
    for key, js in seen.items():
        row = np.zeros(nA + 1)
        for j in js:
            row[j] = 1.0
        row[-1] = -1.0
        Aub.append(row)
        bub.append(0.0)
    res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * (nA + 1), method="highs")
    return res.x[-1], res


def xy_routing(root):
    """Dimension-order routing: along the root row first, then along columns."""
    load = {frozenset(e): 0.0 for e in und}
    rx, ry = root
    for (x, y) in nodes:
        if (x, y) == root:
            continue
        path = []
        cx, cy = rx, ry
        while cy != y:
            ny = cy + (1 if y > cy else -1)
            path.append(((cx, cy), (cx, ny)))
            cy = ny
        while cx != x:
            nx = cx + (1 if x > cx else -1)
            path.append(((cx, cy), (nx, cy)))
            cx = nx
        for a, b in path:
            load[frozenset((a, b))] += per_tile
    return max(load.values()), load


def yx_split(root):
    """The hub table: the root row and root column carry the trunks; each tile picks
    the shorter of XY and YX, ties split. A table, not an LP: what the hub firmware loads."""
    load = {frozenset(e): 0.0 for e in und}
    rx, ry = root

    def walk(order, x, y, w):
        cx, cy = rx, ry
        for axis in order:
            if axis == "x":
                while cx != x:
                    nx = cx + (1 if x > cx else -1)
                    load[frozenset(((cx, cy), (nx, cy)))] += w
                    cx = nx
            else:
                while cy != y:
                    ny = cy + (1 if y > cy else -1)
                    load[frozenset(((cx, cy), (cx, ny)))] += w
                    cy = ny
    for (x, y) in nodes:
        if (x, y) != root:
            walk("xy", x, y, per_tile / 2)
            walk("yx", x, y, per_tile / 2)
    return max(load.values())


worst = 0.0
for name, r in SEATS.items():
    t_lp, _ = lp_min_max(r)
    t_xy, _ = xy_routing(r)
    t_sp = yx_split(r)
    deg = sum(1 for e in und if r in e)
    # one root hinge broken
    root_edges = [e for e in und if r in e]
    t_brk = max(lp_min_max(r, broken=(e,))[0] for e in root_edges)
    worst = max(worst, t_lp, t_brk)
    print(f"  seat {name:20s} degree {deg}: LP optimum {t_lp/1e9:5.2f} Gb/s, XY {t_xy/1e9:5.2f}, "
          f"XY/YX split {t_sp/1e9:5.2f}, LP with one root hinge broken {t_brk/1e9:5.2f} Gb/s")
print("  verdict: plain XY routing overloads the root row; the hub runs a route table from the LP.")
print("  the validators compute the tables (no CPU on the device); U1 loads them at enumeration.")
print(f"  bound: total / degree = {total*(TILES-1)/TILES/3/1e9:.2f} Gb/s for a degree-3 seat")
print()

print("=" * 72)
print("D. LANES AND LINES PER HINGE, AND THE COPPER FIT")
print("=" * 72)
LANE = 3.2e9          # per differential lane, retimed every hop, bidirectional-capable
for lanes in (1, 2, 3):
    capl = lanes * LANE * 128 / 132
    print(f"  {lanes} lane(s) x {LANE/1e9:.1f} Gb/s = {capl/1e9:.2f} Gb/s payload: "
          f"worst load {worst/1e9:.2f} -> {'fits' if capl >= worst*132/128 else 'no'} "
          f"({worst*132/128/capl*100:.0f} % used)")
LANES = 3
line_map = ["G", "D0+", "D0-", "G", "D1+", "D1-", "G", "D2+", "D2-", "G", "BC+", "BC-", "G"]
print(f"  chosen: {LANES} lanes + 1 back-channel pair + 5 guard grounds = {len(line_map)} lines:",
      " ".join(line_map))
h_rib = 1.2e-3        # the low end of the 1.2-1.5 mm ribbon height     [DECISION]
keep = 0.10e-3
wl, sl = 15e-6, 15e-6
n_lines = int((h_rib - 2 * keep + sl) // (wl + sl))
print(f"  ribbon {h_rib*1e3:.1f} mm tall, {keep*1e3:.1f} mm keep-out each end, w/s {wl*1e6:.0f}/{sl*1e6:.0f} um:"
      f" {n_lines} lines on one neutral-plane copper layer")
print(f"  display share {len(line_map)}/{n_lines} = {len(line_map)/n_lines*100:.0f} % of the ribbon; "
      f"{n_lines-len(line_map)} lines left for power, balance and Qi strands")
t_pi, t_cu = 12.5e-6, 2.0e-6
for stretch, eps_s in (("25 %", 0.0048), ("41 %", 0.0123)):
    eps_cu = eps_s * (t_cu / 2) / (t_pi / 2)
    print(f"  strain at {stretch}: ribbon surface {eps_s*100:.2f} %, centred 2 um Cu {eps_cu*100:.3f} % "
          f"(Cu thin-film endurance ~0.2-0.3 % [GENERAL])")
rho = 1.72e-8
L_h = 0.8e-3
R_line = rho * L_h / (wl * t_cu)
skin = np.sqrt(rho / (np.pi * LANE / 2 * 4e-7 * np.pi))
print(f"  line R over the 0.8 mm hinge {R_line:.2f} Ohm; skin depth at {LANE/2e9:.1f} GHz {skin*1e6:.2f} um")
# coplanar strips impedance, thin strips, eps_eff of a thin PI film in air
from scipy.special import ellipk
k = sl / (sl + 2 * wl)
kp = np.sqrt(1 - k * k)
eeff = 1.6                 # [HYPOTHESIS] 12.5 um PI in air
Zcps = 120 * np.pi / np.sqrt(eeff) * ellipk(k * k) / ellipk(kp * kp)
lam = 3e8 / (LANE / 2) / np.sqrt(eeff)
beta_l = 2 * np.pi * L_h / lam
Z0 = 100.0
# ABCD of a line section between two Z0 ports
A = np.cos(beta_l); B = 1j * Zcps * np.sin(beta_l); Cc = 1j * np.sin(beta_l) / Zcps; D = A
S11 = (A + B / Z0 - Cc * Z0 - D) / (A + B / Z0 + Cc * Z0 + D)
print(f"  hinge pair impedance ~{Zcps:.0f} Ohm diff., electrical length {np.degrees(beta_l):.1f} deg at Nyquist,"
      f" |S11| {abs(S11):.3f} ({20*np.log10(abs(S11)):.1f} dB): a lumped step, harmless")
print()

print("=" * 72)
print("E. ADDRESSING AND LATENCY")
print("=" * 72)
hops = []
for name, r in SEATS.items():
    hmax = max(abs(x - r[0]) + abs(y - r[1]) for x, y in nodes)
    hops.append(hmax)
    print(f"  seat {name:20s} farthest tile {hmax} hops")
HOP = 25e-9
print(f"  retime per hop ~{HOP*1e9:.0f} ns -> worst {max(hops)*HOP*1e6:.2f} us")
slice_t = 1 / FPS / NY
print(f"  rolling tile latch: one tile row of the frame arrives in {slice_t*1e3:.3f} ms; "
      f"emission centroid of a 4-segment PWM {1/FPS/4/2*1e3:.2f} ms later")
print("  packet: [dest x 3 b | dest y 4 b | type 4 b | line 8 b | len 12 b | payload | CRC-32]")
print("  broadcast type for frame sync; the sync carries a hop count so every hub")
print("  latches at the same instant to within 1 us.")
