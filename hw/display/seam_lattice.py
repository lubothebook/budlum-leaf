#!/usr/bin/env python3
"""seam_lattice.py - the 508 ppi pixel lattice of one tile, a 2x2 block and the
whole Leaf 160 face, and the proof of gate DSP-19 (the seam gap).

Budlum Leaf L.6.0, Display team, hw/display/.

What it does
  1. Builds the pixel-centre lattice of one 10 mm tile (200 x 200 px).
  2. Builds the four-colour emitter lattice (R, G, B, S quad) of each pixel.
  3. Places 2 x 2 tiles at the tile pitch of 10.000 mm with a glass kerf k.
  4. Measures every adjacent-pixel gap and every same-colour emitter gap,
     inside the tiles, across the straight seams and across the 4-tile corner.
  5. Measures the largest empty circle (Delaunay) near the corner against
     the interior, so a hole at the corner cannot hide.
  6. Sweeps the kerf from 0 to 10 um and repeats the check.
  7. Checks the whole 1600 x 3200 face (8 x 16 tiles) along both axes.
  8. Writes the lattices (.npz) and a zoomed PNG of the seam corner.

Run:  python3 seam_lattice.py        (about 10 s)
Exit code 0 when gate DSP-19 (geometry part) passes.
"""
import os
import sys
import numpy as np
from scipy.spatial import Delaunay, cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- decisions
PITCH = 50.0            # um, 508 ppi           [DECISION] Part 21.2.3
N = 200                 # px per tile edge      [DECISION]
TILE_PITCH = N * PITCH  # 10 000 um, the tile pitch at rest
KERF_NOM = 6.0          # um, glass-to-glass gap at rest, nominal (display team)
KERF_MAX = 10.0         # um, the limit of Part 21.2.4
CHIP = 5.0              # um, square micro-LED chip            (display team)
SUB = 7.0               # um, sub-pitch of the 2 x 2 quad      (display team)
CHIPPING = 10.0         # um, worst edge chipping of an ultrafast-laser cut
MARGIN_RULE = 16.0      # um, Part 21.2.4 chip-to-cut margin
# quad offsets from the pixel centre: R top-left, G top-right, B bottom-left,
# S (the red twin, a second red chip) bottom-right.
QUAD = {"R": (-SUB / 2, +SUB / 2), "G": (+SUB / 2, +SUB / 2),
        "B": (-SUB / 2, -SUB / 2), "S": (+SUB / 2, -SUB / 2)}
TOL = 1e-9


def tile_pixels(kerf):
    """Pixel centres of one tile in its own frame, origin at the glass corner.

    The glass is TILE_PITCH - kerf wide. The first centre sits at
    (PITCH - kerf) / 2 from the glass edge, so the cut-to-centre distance is
    the same on all four edges.
    """
    m = (PITCH - kerf) / 2.0
    c = m + PITCH * np.arange(N)
    X, Y = np.meshgrid(c, c, indexing="xy")
    return X, Y, m, TILE_PITCH - kerf


def block(kerf, nx=2, ny=2):
    """Pixel centres of an nx x ny tile block: arrays (ny*N, nx*N)."""
    X, Y, m, w = tile_pixels(kerf)
    xs = np.concatenate([X[0] + i * TILE_PITCH for i in range(nx)])
    ys = np.concatenate([Y[:, 0] + j * TILE_PITCH for j in range(ny)])
    BX, BY = np.meshgrid(xs, ys, indexing="xy")
    return BX, BY, m, w


def gaps(BX, BY):
    """Horizontal and vertical neighbour distances of a grid of centres."""
    dx = np.hypot(np.diff(BX, axis=1), np.diff(BY, axis=1))
    dy = np.hypot(np.diff(BX, axis=0), np.diff(BY, axis=0))
    dd1 = np.hypot(BX[1:, 1:] - BX[:-1, :-1], BY[1:, 1:] - BY[:-1, :-1])
    dd2 = np.hypot(BX[1:, :-1] - BX[:-1, 1:], BY[1:, :-1] - BY[:-1, 1:])
    return dx, dy, dd1, dd2


def check_kerf(kerf, verbose=False):
    BX, BY, m, w = block(kerf)
    dx, dy, dd1, dd2 = gaps(BX, BY)
    seam_c = N - 1                       # index of the gap that crosses the seam
    r = {}
    r["kerf"] = kerf
    r["edge_centre_um"] = m
    r["glass_mm"] = w / 1000.0
    r["interior_max"] = max(dx[:, :seam_c].max(), dy[:seam_c, :].max())
    r["seam_v_max"] = dx[:, seam_c].max()          # gap across the vertical seam
    r["seam_v_min"] = dx[:, seam_c].min()
    r["seam_h_max"] = dy[seam_c, :].max()          # across the horizontal seam
    r["seam_h_min"] = dy[seam_c, :].min()
    r["corner_diag"] = max(dd1[seam_c, seam_c], dd2[seam_c, seam_c])
    r["all_max"] = max(dx.max(), dy.max())
    r["all_min"] = min(dx.min(), dy.min())
    r["diag_max"] = max(dd1.max(), dd2.max())
    # chip edge margin to the cut, worst chip of the quad, worst edge
    half = SUB / 2 + CHIP / 2
    r["chip_margin_um"] = m - half
    r["chip_gap_um"] = SUB - CHIP
    # same-colour emitter lattices across the seams
    col = {}
    for name, (ox, oy) in QUAD.items():
        ex, ey = BX + ox, BY + oy
        gx, gy, _, _ = gaps(ex, ey)
        col[name] = (gx.max(), gy.max(), gx[:, seam_c].max(), gy[seam_c, :].max())
    r["colour"] = col
    r["colour_max"] = max(max(v) for v in col.values())
    # neighbour emitters of different colour across a seam: the smallest clear
    # space between two chips on either side of the cut
    r["chip_to_chip_across_seam"] = 2 * r["chip_margin_um"] + kerf
    return r, BX, BY


def empty_circle_corner(BX, BY, half_win=12):
    """Largest Delaunay circumradius near the 4-tile corner and in the interior."""
    c = N
    def max_circ(xs, ys):
        P = np.column_stack([xs.ravel(), ys.ravel()])
        tri = Delaunay(P)
        A, B, C = P[tri.simplices[:, 0]], P[tri.simplices[:, 1]], P[tri.simplices[:, 2]]
        a = np.linalg.norm(B - C, axis=1)
        b = np.linalg.norm(A - C, axis=1)
        cc = np.linalg.norm(A - B, axis=1)
        area = 0.5 * np.abs((B[:, 0] - A[:, 0]) * (C[:, 1] - A[:, 1])
                            - (C[:, 0] - A[:, 0]) * (B[:, 1] - A[:, 1]))
        ok = area > 1e-6
        R = a[ok] * b[ok] * cc[ok] / (4 * area[ok])
        return R.max()
    sl = slice(c - half_win, c + half_win)
    corner = max_circ(BX[sl, sl], BY[sl, sl])
    inner = slice(N // 2 - half_win, N // 2 + half_win)
    interior = max_circ(BX[inner, inner], BY[inner, inner])
    return corner, interior


def full_face(kerf):
    """The whole 1600 x 3200 face: the lattice is separable, so check x and y."""
    _, _, m, _ = tile_pixels(kerf)
    loc = m + PITCH * np.arange(N)
    xs = np.concatenate([loc + i * TILE_PITCH for i in range(8)])
    ys = np.concatenate([loc + j * TILE_PITCH for j in range(16)])
    gx, gy = np.diff(xs), np.diff(ys)
    return len(xs), len(ys), gx.max(), gx.min(), gy.max(), gy.min()


def pitch_error_sweep():
    """Seam gap against the rest tile pitch error. The gap is pitch - 9 950 um."""
    errs = np.array([-4, -2, -1, 0, +1, +2])
    return [(e, TILE_PITCH + e - (N - 1) * PITCH) for e in errs]


def plot_corner(results, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    colours = {"R": "#d62728", "G": "#2ca02c", "B": "#1f77b4", "S": "#9e9e9e"}
    fig, axes = plt.subplots(1, 2, figsize=(14, 7.2))
    for ax, (kerf, title) in zip(axes, results):
        BX, BY, m, w = block(kerf)
        cx = cy = TILE_PITCH - kerf / 2.0          # centre of the corner gap
        span = 3 * PITCH + 10
        # glass of the four tiles
        for i in range(2):
            for j in range(2):
                x0, y0 = i * TILE_PITCH, j * TILE_PITCH
                ax.add_patch(Rectangle((x0, y0), w, w, facecolor="#101418",
                                       edgecolor="#f0c040", lw=1.2, zorder=0))
        # chips
        sel = (np.abs(BX - cx) < span + PITCH) & (np.abs(BY - cy) < span + PITCH)
        for x, y in zip(BX[sel], BY[sel]):
            for name, (ox, oy) in QUAD.items():
                ax.add_patch(Rectangle((x + ox - CHIP / 2, y + oy - CHIP / 2), CHIP, CHIP,
                                       facecolor=colours[name], edgecolor="none", zorder=2))
            ax.plot(x, y, "+", color="white", ms=5, mew=0.6, zorder=3)
        # chipping zone and margin
        for i in range(2):
            for j in range(2):
                x0, y0 = i * TILE_PITCH, j * TILE_PITCH
                ax.add_patch(Rectangle((x0 + CHIPPING, y0 + CHIPPING), w - 2 * CHIPPING,
                                       w - 2 * CHIPPING, fill=False, ls=":",
                                       edgecolor="#ff7f0e", lw=0.8, zorder=1))
        # dimension across the vertical seam on the row just below the corner
        yrow = BY[N - 1, 0]
        xa, xb = BX[0, N - 1], BX[0, N]
        ax.annotate("", xy=(xa, yrow - 14), xytext=(xb, yrow - 14),
                    arrowprops=dict(arrowstyle="<->", color="cyan", lw=1.0))
        ax.text((xa + xb) / 2, yrow - 22,
                f"{m:.1f} + {kerf:.1f} + {m:.1f} = {xb - xa:.1f} um",
                color="cyan", ha="center", va="top", fontsize=9)
        r, _, _ = check_kerf(kerf)
        ax.set_xlabel(
                f"x (um)\nkerf {kerf:.1f} um   glass {w/1000:.3f} mm\n"
                f"seam gap max {r['all_max']:.3f} um   corner diag {r['corner_diag']:.2f} um\n"
                f"chip-to-cut margin {r['chip_margin_um']:.1f} um (chipping {CHIPPING:.0f} um)",
                fontsize=8.5)
        ax.set_xlim(cx - span, cx + span)
        ax.set_ylim(cy - span, cy + span)
        ax.set_aspect("equal")
        ax.set_facecolor("#05070a")
        ax.set_title(title, fontsize=10)
        ax.set_ylabel("y (um)")
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in colours.values()]
    fig.legend(handles, ["R", "G", "B", "S (red twin)"], loc="lower center", ncol=4)
    fig.suptitle("Budlum Leaf L.6.0 - the 4-tile seam corner, 508 ppi (50.0 um), "
                 "5 um chips in a 7 um RGBS quad", fontsize=11)
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    ok = True
    print("== DSP-19 geometry: the lattice-continuous seam ==")
    print(f"pitch {PITCH} um ({25400/PITCH:.1f} ppi), {N} x {N} px, tile pitch {TILE_PITCH/1000:.3f} mm")
    print(f"chip {CHIP} um, quad sub-pitch {SUB} um, chip gap {SUB-CHIP} um")
    X, Y, m, w = tile_pixels(KERF_NOM)
    np.savez_compressed(os.path.join(OUT, "tile_lattice_kerf6.npz"), x=X, y=Y,
                        quad=np.array([QUAD[k] for k in "RGBS"]))
    BX, BY, m, w = block(KERF_MAX)
    np.savez_compressed(os.path.join(OUT, "block2x2_lattice_kerf10.npz"), x=BX, y=BY)
    BXn, BYn, _, _ = block(KERF_NOM)
    np.savez_compressed(os.path.join(OUT, "block2x2_lattice_kerf6.npz"), x=BXn, y=BYn)
    print(f"tile lattice: {X.size} centres; 2x2 block: {BX.size} centres; "
          f"emitters per 2x2 block: {BX.size*4}")
    print()
    print(f"{'kerf':>5} {'edge c':>7} {'glass mm':>9} {'int max':>8} {'seam V':>15} {'seam H':>15} "
          f"{'corner':>7} {'colour':>7} {'margin':>7}")
    for k in np.arange(0.0, KERF_MAX + 0.001, 1.0):
        r, _, _ = check_kerf(k)
        print(f"{k:5.1f} {r['edge_centre_um']:7.2f} {r['glass_mm']:9.4f} {r['interior_max']:8.3f} "
              f"{r['seam_v_min']:7.3f}-{r['seam_v_max']:7.3f} {r['seam_h_min']:7.3f}-{r['seam_h_max']:7.3f} "
              f"{r['corner_diag']:7.3f} {r['colour_max']:7.3f} {r['chip_margin_um']:7.2f}")
        good = (abs(r["all_max"] - PITCH) < TOL and abs(r["all_min"] - PITCH) < TOL
                and abs(r["colour_max"] - PITCH) < TOL
                and abs(r["corner_diag"] - PITCH * np.sqrt(2)) < TOL)
        ok &= good
    print()
    for k in (KERF_NOM, KERF_MAX):
        r, BX, BY = check_kerf(k)
        cmax, imax = empty_circle_corner(BX, BY)
        print(f"kerf {k:4.1f} um: largest empty circle radius, corner {cmax:.3f} um, "
              f"interior {imax:.3f} um (ideal {PITCH/np.sqrt(2):.3f})")
        ok &= abs(cmax - imax) < 1e-6
        print(f"   chip-to-cut margin {r['chip_margin_um']:.2f} um  "
              f"(rule {MARGIN_RULE} um: {'met' if r['chip_margin_um'] >= MARGIN_RULE - 1e-9 else 'below'}; "
              f"chipping {CHIPPING} um: {'clear' if r['chip_margin_um'] > CHIPPING else 'HIT'})")
        print(f"   clear space chip to chip across the seam {r['chip_to_chip_across_seam']:.1f} um")
        for name, v in r["colour"].items():
            print(f"   colour {name}: max same-colour gap {max(v):.3f} um "
                  f"(across V seam {v[2]:.3f}, across H seam {v[3]:.3f})")
        ok &= r["chip_margin_um"] > CHIPPING
    print()
    for k in (KERF_NOM, KERF_MAX):
        nx, ny, gxmax, gxmin, gymax, gymin = full_face(k)
        print(f"full face kerf {k:4.1f}: {nx} x {ny} px, x gaps {gxmin:.3f}..{gxmax:.3f}, "
              f"y gaps {gymin:.3f}..{gymax:.3f} um")
        ok &= (nx, ny) == (1600, 3200) and abs(max(gxmax, gymax) - PITCH) < TOL
    print()
    print("seam gap against the rest error of the tile pitch (kerf has no effect):")
    for e, g in pitch_error_sweep():
        print(f"   pitch error {e:+.0f} um -> seam gap {g:.1f} um  "
              f"{'pass' if g <= PITCH + TOL else 'FAIL DSP-19'}")
    plot_corner([(KERF_NOM, f"nominal kerf {KERF_NOM:.0f} um (glass {(TILE_PITCH-KERF_NOM)/1000:.3f} mm)"),
                 (KERF_MAX, f"limit kerf {KERF_MAX:.0f} um (glass {(TILE_PITCH-KERF_MAX)/1000:.3f} mm)")],
                os.path.join(OUT, "seam_corner_zoom.png"))
    print()
    print("wrote out/seam_corner_zoom.png, out/tile_lattice_kerf6.npz, out/block2x2_lattice_kerf*.npz")
    print("DSP-19 geometry:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
