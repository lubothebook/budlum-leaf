#!/usr/bin/env python3
"""placement.py - ring PCBA placement study of the Budlum Leaf B module (L.6.0).

The question: do U1..U9, U_BMS, the cell, the camera column, the jack, the
speaker, the microphones, the flash, the tuners, the inductors and the clocks
fit on a Ø30.0 x 0.55 mm 8-layer HDI board around a 7 x 6 mm camera hole?

The method: a 2D packing check.
  * board    = disk r 15.0 minus a 0.25 mm edge keep-out
  * cut-outs = the camera hole 7.0 x 6.0 (+0.25), the jack notch on a 13.8 mm
               chord, the bar-flex landing, and (scenario) eight magnet pockets
  * every IC carries a 0.40 mm skirt for 01005 decoupling and a 0.15 mm
    courtyard. An RF chip under a shield can carries 0.30 mm more.
  * a raster contact packer (0.1 mm grid, 12 orientations, FFT overlap test)
    places the parts largest first, at the pose with the most contact.
  * shapely then checks every placed polygon exactly: inside the board, out
    of every cut-out, and clear of every other part.

The scenarios:
  S0  HARDWARE/13 as written: one flat 20.0 x 8.0 mm cell on the board,
      magnets cut through the board.
  S1  S0 with the cell split into two 10.0 x 8.0 x 1.50 mm cells (same volume).
  S2  S1 with the magnets 0.80 mm thick, below the board in the rim pad.
  S3  S2 with both cells stacked over cold parts no taller than 0.70 mm.
  S4  S3 with the bottom face of the rim band (r 12.2..14.75) used for parts
      no taller than 0.55 mm.
  S5  S4 with U1 and U6 merged into one 7.5 x 7.5 mm die.

Run:  python3 placement.py      (writes placement_S*.svg and placement_results.txt)
"""
import math
import os
import sys

import numpy as np
from scipy.signal import fftconvolve
from shapely.geometry import Point, box
from shapely.affinity import rotate, translate
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))

R_BOARD = 15.0          # Ø30.0 ring PCBA, HARDWARE/13 part 15
EDGE_KO = 0.25
HOLE_W, HOLE_H, HOLE_KO = 7.0, 6.0, 0.25
SKIRT_IC, COURT, CAN = 0.40, 0.15, 0.30
CELL_Z_MAX_UNDER = 0.70  # 2.30 above board - 1.50 cell - 0.10 insulating film
BOTTOM_Z_MAX = 0.55      # rim band below the board: 0.85 - 0.25 shell - 0.05 gap
RIM_IN, RIM_OUT = 12.2, R_BOARD - EDGE_KO

STACK = dict(module=4.00, front_window=0.30, rear_window=0.30, amoled=0.40,
             shield=0.15, pcba=0.55, spreader=0.80)   # [HYPOTHESIS]

GRID = 0.05
N = int(round(2 * 15.6 / GRID)) + 1
XS = (np.arange(N) - (N - 1) / 2) * GRID
XX, YY = np.meshgrid(XS, XS[::-1])   # row 0 = top (y max)


def height_above_board():
    s = STACK
    return round(s["module"] - s["front_window"] - s["rear_window"] - s["amoled"] - s["shield"] - s["pcba"], 3)


# ---------------------------------------------------------------- parts
# name, w, h, z (height above its face), kind, hot, rmin, rmax
def parts(scenario):
    P = []
    def add(n, w, h, z, kind, hot=False, rmin=0.0, rmax=99.0):
        P.append(dict(name=n, w=w, h=h, z=z, kind=kind, hot=hot, rmin=rmin, rmax=rmax))
    add("U5 5G modem",            10.0, 8.0, 0.80, "rf", hot=True)
    if scenario == "S5":
        add("U16 TCON+codec",      7.5, 7.5, 0.70, "ic", hot=True)
    else:
        add("U6 codec+store",      6.0, 6.0, 0.70, "ic", hot=True)
        add("U1 TCON",             5.2, 5.2, 0.45, "ic", hot=True)
    add("U2A WiFi7/BT6",           5.0, 5.0, 0.60, "rf", hot=True)
    add("U2B 60G/UWB",             5.0, 4.5, 0.60, "rf", hot=True)
    add("U4 PMIC",                 3.2, 3.2, 0.40, "ic", hot=True)
    add("U3 audio",                3.2, 3.2, 0.40, "ic")
    add("U_BMS mux",               3.0, 3.0, 0.40, "ic")
    add("U9 NOR",                  2.0, 3.0, 0.55, "ic")
    add("U4B bias/flash",          2.0, 2.0, 0.40, "ic")
    add("U7 SE",                   2.0, 2.0, 0.40, "ic")
    add("U8 IMU",                  2.0, 2.0, 0.70, "ic")
    add("Y1 TCXO",                 2.0, 1.6, 0.70, "ic")
    add("SPK speaker",             9.0, 3.2, 2.20, "mech", rmin=10.5)
    add("MK1 mic",                 2.7, 1.8, 0.90, "mech", rmin=11.5)
    add("MK2 mic",                 2.7, 1.8, 0.90, "mech", rmin=11.5)
    add("D1 flash",                2.4, 1.6, 0.65, "mech", rmax=11.0)
    add("CAMFLEX",                 3.0, 1.6, 0.50, "mech", rmax=7.5)
    add("DISPFLEX",                4.0, 1.6, 0.50, "mech")
    for i in range(1, 4):
        add("TUN%d tuner" % i,     1.5, 1.0, 0.40, "mech")
    add("Y2 32k",                  1.6, 1.0, 0.45, "mech")
    for i in range(1, 8):
        add("L%d" % i,             2.0, 1.25, 0.65, "mech")
    if scenario == "S0":
        add("BT1 cell 20x8",      20.0, 8.0, 1.50, "cell")
    else:
        add("BT1a cell",          10.0, 8.0, 1.50, "cell")
        add("BT1b cell",          10.0, 8.0, 1.50, "cell")
    return P


def inflate(p):
    return {"ic": SKIRT_IC + COURT, "rf": SKIRT_IC + COURT + CAN}.get(p["kind"], COURT)


# ---------------------------------------------------------------- board
def board(scenario):
    disk = Point(0, 0).buffer(R_BOARD - EDGE_KO, resolution=180)
    hole = box(-HOLE_W / 2 - HOLE_KO, -HOLE_H / 2 - HOLE_KO, HOLE_W / 2 + HOLE_KO, HOLE_H / 2 + HOLE_KO)
    jack = box(-7.0, -15.8, 7.0, -11.8).buffer(0.2, join_style=2)       # chord 13.8, bore Ø4.0
    flex = box(-2.5, 11.6, 2.5, 16.0)                                     # moulded corner flex
    cuts = [hole, jack, flex]
    if scenario in ("S0", "S1"):
        for k in range(8):                       # 8 N52H 3.2x1.6, lower 140°, away from A1
            ang = 200 + k * (140 / 7)
            m = box(-1.75, -0.95, 1.75, 0.95)
            m = rotate(m, ang + 90, origin=(0, 0))
            cuts.append(translate(m, 13.6 * math.cos(math.radians(ang)), 13.6 * math.sin(math.radians(ang))))
    return disk, cuts


def raster(geom):
    from matplotlib.path import Path
    m = np.zeros((N, N), bool)
    pts = np.c_[XX.ravel(), YY.ravel()]
    for g in getattr(geom, "geoms", [geom]):
        if g.is_empty:
            continue
        inside = Path(np.asarray(g.exterior.coords)).contains_points(pts).reshape(N, N)
        for it in g.interiors:
            inside &= ~Path(np.asarray(it.coords)).contains_points(pts).reshape(N, N)
        m |= inside
    return m


def rect_mask(w, h, ang):
    """Conservative raster of a w x h rectangle rotated by ang, centred."""
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    hw, hh = w / 2, h / 2
    R = int(math.ceil(math.hypot(hw, hh) / GRID)) + 1
    k = (np.arange(2 * R + 1) - R) * GRID
    X, Y = np.meshgrid(k, k[::-1])
    u = X * c + Y * s
    v = -X * s + Y * c
    return (np.abs(u) <= hw) & (np.abs(v) <= hh)


RING = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], float)


def place(forbid, p, extra_allow=None, exact=None, topk=400):
    """Return the verified (x, y, ang) pose with most contact, or None.

    The raster ranks the poses. shapely then checks the best poses exactly
    against `exact` (the free region of that face) and keeps the first valid.
    """
    g = inflate(p)
    w, h = p["w"] + 2 * g, p["h"] + 2 * g
    r = np.hypot(XX, YY)
    allow = ~forbid & (r >= p["rmin"]) & (r <= p["rmax"])
    if extra_allow is not None:
        allow &= extra_allow
    blocked = (~allow).astype(float)
    cands = []
    for ang in range(0, 180, 15):
        m = rect_mask(w, h, ang)
        ov = fftconvolve(blocked, m[::-1, ::-1].astype(float), mode="same")
        feas = ov < 0.5
        if not feas.any():
            continue
        ring = fftconvolve(m.astype(float), RING, mode="full")[1:-1, 1:-1] > 0.5
        ring &= ~m
        contact = fftconvolve(blocked, ring[::-1, ::-1].astype(float), mode="same")
        score = np.where(feas, contact + 1e-3 * r, -1.0)
        flat = score.ravel()
        k = min(topk, int((flat >= 0).sum()))
        idx = np.argpartition(-flat, k - 1)[:k]
        for i in idx:
            cands.append((flat[i], XX.ravel()[i], YY.ravel()[i], ang))
    cands.sort(key=lambda c: -c[0])
    for sc, x, y, ang in cands:
        pose = (float(x), float(y), ang)
        if exact is None or exact.contains(poly_of(p, pose)):
            return pose
    return None


def poly_of(p, pose):
    g = inflate(p)
    s = box(-p["w"] / 2 - g, -p["h"] / 2 - g, p["w"] / 2 + g, p["h"] / 2 + g)
    return translate(rotate(s, pose[2], origin=(0, 0)), pose[0], pose[1])


# ---------------------------------------------------------------- scenarios
def run(scenario):
    disk, cuts = board(scenario)
    stacked = scenario in ("S3", "S4", "S5")
    bottom = scenario in ("S4", "S5")
    region = disk.difference(unary_union(cuts))
    forbid_top = ~raster(region)
    rim_bottom = Point(0, 0).buffer(RIM_OUT, resolution=180).difference(
        Point(0, 0).buffer(RIM_IN, resolution=180)).difference(unary_union(cuts))
    forbid_bot = ~raster(rim_bottom)

    ps = parts(scenario)
    placed, failed = [], []           # (p, poly, face)
    first = ("U5 ", "SPK", "CAMFLEX", "D1 ", "MK1", "MK2")
    head = [p for f in first for p in ps if p["name"].startswith(f)]
    cells = [p for p in ps if p["kind"] == "cell"]
    tail = sorted([p for p in ps if p not in head and p not in cells],
                  key=lambda p: -(p["w"] + 2 * inflate(p)) * (p["h"] + 2 * inflate(p)))
    sequence = head + cells + tail
    cold_zone = np.zeros((N, N), bool)
    cell_region = Point(0, 0).buffer(15.4, resolution=180).difference(unary_union(cuts))
    forbid_cell = ~raster(cell_region)
    free_top, free_bot, free_cell = region, rim_bottom, cell_region
    cell_union = Point(0, 0).buffer(0)

    def is_cold(p):
        zz = p["z"] + (0.15 if p["kind"] == "rf" else 0)
        return (not p["hot"]) and zz <= CELL_Z_MAX_UNDER and not p["name"].startswith("D1")

    for p in sequence:
        if p["kind"] == "cell" and stacked:
            # a stacked cell floats 0.10 mm over cold parts. It may overhang the
            # board edge to r 15.4, inside the shell wall.
            pose = place(forbid_cell, p, exact=free_cell)
            if pose is None:
                failed.append((p, "cell layer"))
                continue
            pg = poly_of(p, pose)
            placed.append((p, pg, "cell"))
            free_cell = free_cell.difference(pg)
            cell_union = cell_union.union(pg)
            m = raster(pg)
            forbid_cell |= m
            cold_zone |= m
            continue
        allow = None if (is_cold(p) or p["kind"] == "cell") else ~cold_zone
        ex = free_top if allow is None else free_top.difference(cell_union)
        pose = place(forbid_top, p, allow, exact=ex)
        face = "top"
        if pose is None and bottom and p["z"] <= BOTTOM_Z_MAX and p["kind"] != "cell":
            pose = place(forbid_bot, p, exact=free_bot)
            face = "bottom"
        if pose is None:
            failed.append((p, "no room"))
            continue
        pg = poly_of(p, pose)
        placed.append((p, pg, face))
        m = raster(pg)
        if face == "top":
            forbid_top |= m
            free_top = free_top.difference(pg)
            if not is_cold(p):
                forbid_cell |= m
                free_cell = free_cell.difference(pg)
        else:
            forbid_bot |= m
            free_bot = free_bot.difference(pg)

    # ------------- exact shapely verification
    errors = []
    for face, reg in (("top", region), ("bottom", rim_bottom)):
        polys = [(p, g) for p, g, f in placed if f == face]
        for p, g in polys:
            if not reg.buffer(1e-6).contains(g):
                errors.append("%s leaves the %s region" % (p["name"], face))
        for i in range(len(polys)):
            for j in range(i + 1, len(polys)):
                if polys[i][1].intersection(polys[j][1]).area > 1e-6:
                    errors.append("%s overlaps %s" % (polys[i][0]["name"], polys[j][0]["name"]))
    if stacked:
        cellpolys = [g for p, g, f in placed if f == "cell"]
        for cg in cellpolys:
            for p, g, f in placed:
                if f != "top":
                    continue
                if g.intersection(cg).area > 1e-6:
                    zz = p["z"] + (0.15 if p["kind"] == "rf" else 0)
                    if p["hot"] or zz > CELL_Z_MAX_UNDER or p["name"].startswith("D1"):
                        errors.append("%s is hot or tall under a cell" % p["name"])
        if len(cellpolys) == 2 and cellpolys[0].intersection(cellpolys[1]).area > 1e-6:
            errors.append("cells overlap")

    a_top = region.area
    a_bot = rim_bottom.area if bottom else 0.0
    used_top = sum(g.area for p, g, f in placed if f == "top")
    used_bot = sum(g.area for p, g, f in placed if f == "bottom")
    demand = sum((p["w"] + 2 * inflate(p)) * (p["h"] + 2 * inflate(p)) for p in ps
                 if not (stacked and p["kind"] == "cell"))
    return dict(scenario=scenario, disk=disk, cuts=cuts, placed=placed, failed=failed,
                errors=errors, a_top=a_top, a_bot=a_bot, used_top=used_top,
                used_bot=used_bot, demand=demand)


# ---------------------------------------------------------------- output
def svg(res, path):
    S = 13.0
    W = int(2 * 16.5 * S)
    def tr(x, y):
        return (x + 16.5) * S, (16.5 - y) * S
    def poly(g, fill, op=1.0, dash=False):
        out = []
        for gg in getattr(g, "geoms", [g]):
            if gg.is_empty:
                continue
            pts = " ".join("%.1f,%.1f" % tr(x, y) for x, y in gg.exterior.coords)
            out.append('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="#222" stroke-width="0.8"%s/>'
                       % (pts, fill, op, ' stroke-dasharray="4 3"' if dash else ""))
        return "\n".join(out)
    col = dict(ic="#6c8ebf", rf="#b85450", mech="#82b366", cell="#d6b656")
    b = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Helvetica,Arial,sans-serif">' % (W, W + 70, W, W + 70),
         '<rect width="100%" height="100%" fill="#ffffff"/>',
         poly(Point(0, 0).buffer(16.0, resolution=128).difference(Point(0, 0).buffer(15.0, resolution=128)), "#cccccc", 0.6),
         poly(res["disk"], "#f4f1e8")]
    for c in res["cuts"]:
        b.append(poly(c, "#8c8c8c", 0.85))
    for p, g, f in res["placed"]:
        if f == "cell":
            continue
        b.append(poly(g, col[p["kind"]], 0.75 if f == "top" else 0.30, dash=(f == "bottom")))
        c = g.centroid
        x, y = tr(c.x, c.y)
        b.append('<text x="%.1f" y="%.1f" font-size="7" text-anchor="middle">%s</text>' % (x, y + 2, p["name"].split(" ")[0]))
    for p, g, f in res["placed"]:
        if f == "cell":
            b.append(poly(g, col["cell"], 0.25, dash=True))
            c = g.centroid
            x, y = tr(c.x, c.y)
            b.append('<text x="%.1f" y="%.1f" font-size="9" font-weight="bold" text-anchor="middle">%s (stacked)</text>' % (x, y - 18, p["name"].split(" ")[0]))
    t = "%s: placed %d, failed %d" % (res["scenario"], len(res["placed"]), len(res["failed"]))
    if res["failed"]:
        t += " (" + ", ".join(p["name"].split(" ")[0] for p, _ in res["failed"]) + ")"
    b.append('<text x="10" y="%d" font-size="12">%s</text>' % (W + 18, t))
    b.append('<text x="10" y="%d" font-size="10">grey: camera hole, jack notch, bar flex, magnet pockets. blue IC+skirt, red RF+can, green mechanical.</text>' % (W + 36))
    b.append('<text x="10" y="%d" font-size="10">dashed pale: bottom face of the rim band. dashed yellow: cell stacked 0.10 mm over cold parts.</text>' % (W + 52))
    b.append("</svg>")
    open(path, "w").write("\n".join(b))


def main():
    lines = []
    def out(s=""):
        print(s)
        lines.append(s)
    hz = height_above_board()
    out("vertical budget above the board: %.2f mm; spreader %.2f mm over parts up to %.2f mm" % (hz, STACK["spreader"], hz - STACK["spreader"]))
    out("parts taller than %.2f mm take a spreader cut-out: speaker 2.20 mm (fits %.2f), cell 1.50 mm" % (hz - STACK["spreader"], hz))
    d_min = HOLE_H / 2 + HOLE_KO + COURT
    r_corner = math.hypot(10.0 + COURT, d_min + 8.0 + COURT)
    out("analytic: a flat 20x8 cell beside the hole puts a corner at r %.2f mm against the edge r %.2f mm: %s"
        % (r_corner, R_BOARD - EDGE_KO, "fits" if r_corner <= R_BOARD - EDGE_KO else "DOES NOT FIT"))
    out()
    out("%-3s %7s %7s %8s %8s %7s %8s %7s  %s" % ("sc", "placed", "failed", "demand", "top", "fill", "bottom", "errors", "failed parts"))
    results = {}
    for sc in ("S0", "S1", "S2", "S3", "S4", "S5"):
        r = run(sc)
        results[sc] = r
        fill = (r["used_top"] + r["used_bot"]) / (r["a_top"] + r["a_bot"])
        out("%-3s %7d %7d %8.1f %8.1f %6.0f%% %8.1f %7d  %s" % (
            sc, len(r["placed"]), len(r["failed"]), r["demand"], r["a_top"], 100 * fill,
            r["a_bot"], len(r["errors"]), ", ".join(p["name"] for p, _ in r["failed"]) or "-"))
        for e in r["errors"]:
            out("      ERROR " + e)
        svg(r, os.path.join(HERE, "placement_%s.svg" % sc))
    out()
    out("demand = sum of part areas with skirt, courtyard and can (cells left out when stacked).")
    out("top/bottom = board area free of cut-outs, mm^2. fill = placed area / available area.")
    for sc in ("S4", "S5"):
        bots = [p["name"] for p, g, f in results[sc]["placed"] if f == "bottom"]
        out("%s bottom-face parts: %s" % (sc, ", ".join(bots) or "-"))
    open(os.path.join(HERE, "placement_results.txt"), "w").write("\n".join(lines) + "\n")
    ok = not results["S4"]["failed"] and not results["S4"]["errors"]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
