"""geom_body.py - wire models of the Leaf body ground and the bar antennas.

Used by a1_ifa.py, seats_stretch.py and mimo.py with mom_wire.Wires.

Frames: the body lies in z = 0 (the mid plane of the can metal), x along the
80 mm edge, y along the 160 mm edge. The top edge is y = 160 mm. The front
face is +z. The bar copper sits 1.15 mm out from the can edge (0.375 inset +
0.775 to the middle of the antenna layer) and 2.36 mm towards the front over
the overhang band (cs2d.py case "A1_overhang").
"""
import numpy as np
from rf_common import surface_resistance, SIGMA, TILE, NX, NY

MM = 1e-3
EDGE_A = 0.28 * MM        # the 1.1 mm tall can edge as a wire (a = t / 4)
GRID_A = 0.25 * MM
ARM_A = 0.40 * MM         # a 1.6 mm strip as a wire (a = w / 4)
ARM_DY = 1.15 * MM        # can edge to the antenna layer
ARM_DZ = 2.36 * MM        # metal mid plane to the overhang strip centre


def ground_rprime(f, metal="SS304", spacing=TILE / 2):
    """Series loss per metre of a grid wire that stands for a plate.

    A grid of pitch d carries K d per wire; equating I^2 R' per cell to
    Rs |K|^2 / 2 per face pair gives R' = Rs / (2 d) [GENERAL].
    """
    return surface_resistance(f, SIGMA[metal]) / (2 * spacing)


EDGE_W = 2.2 * MM     # the edge current spreads over the can wall and the coil layer [HYPOTHESIS]


def edge_rprime(f, metal="SS304"):
    """Series loss per metre of the ground edge under the bar (same as the TL model)."""
    return surface_resistance(f, SIGMA[metal]) / EDGE_W


def strip_rprime(f, width=1.6 * MM, metal="Cu_LDS"):
    # current on both faces of a thin strip, with edge crowding factor 1.5 [GENERAL]
    return 1.5 * surface_resistance(f, SIGMA[metal]) / (2 * width)


def plate(W, f, xs=None, ys=None, metal="SS304", dx_edge=2 * MM,
          fine_x=(28 * MM, 52 * MM), dx_fine=1 * MM):
    """A solid ground as a wire grid with a refined top edge."""
    if xs is None:
        xs = np.arange(0, 80.01, 4.0) * MM
    if ys is None:
        ys = np.concatenate([np.arange(0, 136, 8.0), np.arange(136, 160.01, 4.0)]) * MM
    rg = ground_rprime(f, metal, spacing=4 * MM)
    re = edge_rprime(f, metal)
    for y in ys:
        top = abs(y - ys[-1]) < 1e-9
        for x0, x1 in zip(xs[:-1], xs[1:]):
            fine = top and fine_x is not None and fine_x[0] - 1e-9 <= x0 and x1 <= fine_x[1] + 1e-9
            n = max(1, int(round((x1 - x0) / (dx_fine if fine else dx_edge)))) if top else 1
            W.line((x0, y, 0), (x1, y, 0), n, EDGE_A if top else GRID_A, re if top else rg)
    for x in xs:
        for y0, y1 in zip(ys[:-1], ys[1:]):
            W.line((x, y0, 0), (x, y1, 0), 1, GRID_A, rg)
    return ys[-1]


def tile_corners(theta, i, j):
    """Corner points (4 x 2) of tile (i, j) in the rotating-square lattice."""
    s = TILE
    sgn = 1 if (i + j) % 2 == 0 else -1
    th = sgn * theta
    D = s * (np.cos(theta) + np.sin(theta))
    c = np.array([(i + 0.5) * D, (j + 0.5) * D])
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    v = 0.5 * s * np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    return c + v @ R.T


def mosaic(W, f, theta, metal="SS304", fine_tiles=(), nfine=5, cross=True):
    """The 128-tile body as rotated square outlines joined at the corners.

    Tiles in fine_tiles are cut into nfine segments per side (near the bar).
    The corner hinges are modelled as shared nodes (an EGaIn or 2 um Cu link).
    """
    rg = ground_rprime(f, metal, spacing=TILE / 2)
    tiles = {}
    for i in range(NX):
        for j in range(NY):
            P = tile_corners(theta, i, j)
            n = nfine if (i, j) in fine_tiles else 2
            a = EDGE_A if j == NY - 1 else GRID_A
            for k in range(4):
                p0, p1 = P[k], P[(k + 1) % 4]
                W.line((*p0, 0), (*p1, 0), n, a, rg)
            if cross:
                mids = [(P[k] + P[(k + 1) % 4]) / 2 for k in range(4)]
                c = P.mean(0)
                for m in mids:
                    W.line((*m, 0), (*c, 0), 1, GRID_A, rg)
            tiles[(i, j)] = P
    return tiles


def top_profile(tiles, x):
    """Highest metal point y under x, from the top-row tile polygons."""
    ymax = -np.inf
    for (i, j), P in tiles.items():
        if j != NY - 1:
            continue
        for k in range(4):
            p0, p1 = P[k], P[(k + 1) % 4]
            lo, hi = sorted((p0[0], p1[0]))
            if lo - 1e-12 <= x <= hi + 1e-12 and hi > lo:
                t = (x - p0[0]) / (p1[0] - p0[0])
                ymax = max(ymax, p0[1] + t * (p1[1] - p0[1]))
    return ymax


def nearest_ground(W, p, ymin):
    """Nearest existing node in the plane z = 0 with y >= ymin."""
    N = np.array(W.nodes)
    m = (np.abs(N[:, 2]) < 1e-9) & (N[:, 1] >= ymin)
    idx = np.where(m)[0]
    d = np.linalg.norm(N[idx, :2] - np.asarray(p)[:2], axis=1)
    return N[idx[np.argmin(d)]]


def ifa(W, f, x_short, x_feed, x_tune, x_open, y_arm, ymin_ground,
        cload_per_m=0.0, dx=1.0 * MM, dz=ARM_DZ, cap_step=2.0 * MM):
    """Add the A1 inverted-F over the top ground edge; return the leg nodes.

    The arm runs along x from x_short to x_open at y = y_arm, z = dz.
    Each leg runs from the arm to the nearest ground node of the top edge.
    The port and the tuner are the middle node of their legs.
    cload_per_m adds capacitor legs every cap_step that stand for the extra
    capacitance of the LCP over air (the dielectric of the bar).
    """
    rl = strip_rprime(f)
    keys = [x_short, x_feed, x_open] + ([x_tune] if x_tune is not None else [])
    caps = []
    if cload_per_m > 0:
        for x in np.arange(x_short + cap_step, x_open + 1e-9, cap_step):
            if min(abs(x - v) for v in keys) > 0.4 * MM:
                caps.append(x)
    xs = sorted(set(keys + caps))
    W.polyline([(x, y_arm, dz) for x in xs], dx, ARM_A, rl, tag="arm")
    nodes = {}
    legs = [("short", x_short), ("feed", x_feed)]
    if x_tune is not None:
        legs.append(("tune", x_tune))
    for name, x in legs + [("cap", x) for x in caps]:
        top = np.array((x, y_arm, dz))
        tgt = nearest_ground(W, top, ymin_ground)
        mid = 0.5 * (top + tgt)
        a = ARM_A / 2 if name != "cap" else ARM_A / 4
        W.line(top, mid, 1, a, rl if name != "cap" else 0.0, tag=name)
        ids = W.line(mid, tgt, 1, a, rl if name != "cap" else 0.0, tag=name)
        if name == "cap":
            C = cload_per_m * cap_step
            W.loads[ids[0]] = (lambda C: (lambda ff: 1.0 / (1j * 2 * np.pi * ff * C)))(C)
        else:
            nodes[name] = ids[0]
    return nodes
