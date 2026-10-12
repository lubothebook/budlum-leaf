"""(1) Rotating-square kinematics of the 8 x 16 tile body.

Builds the real 128-tile lattice with shapely at each angle, checks that no
tiles overlap, and measures the stretch, the area, the pixel fill, the gap
diamond and the Poisson ratio. Tile (i, j) turns by (-1)^(i+j) * theta and its
centre sits at pitch p = a (cos theta + sin theta).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

from common import A_TILE, NX, NY, DEG, PLOTS, mm, save

CHAMFER = 0.6 * mm   # [DECISION of this team] 45 deg corner chamfer leg for the hinge pocket


def tile_poly(cx, cy, rot, a=A_TILE, c=CHAMFER):
    h = a / 2
    # octagon: square with 45 deg chamfers of leg c at the corners
    pts = [(-h + c, -h), (h - c, -h), (h, -h + c), (h, h - c),
           (h - c, h), (-h + c, h), (-h, h - c), (-h, -h + c)]
    cr, sr = np.cos(rot), np.sin(rot)
    return Polygon([(cx + x * cr - y * sr, cy + x * sr + y * cr) for x, y in pts])


def lattice(theta, a=A_TILE, c=CHAMFER):
    p = a * (np.cos(theta) + np.sin(theta))
    return [tile_poly(i * p, j * p, (-1) ** (i + j) * theta, a, c)
            for j in range(NY) for i in range(NX)], p


def hinge_points(theta, a=A_TILE):
    """Return list of (tile_k, tile_l, xy) with the ideal corner pivots."""
    p = a * (np.cos(theta) + np.sin(theta))
    out = []

    def corner(i, j, sx, sy):
        r = (-1) ** (i + j) * theta
        x, y = sx * a / 2, sy * a / 2
        return np.array([i * p + x * np.cos(r) - y * np.sin(r),
                         j * p + x * np.sin(r) + y * np.cos(r)])
    for j in range(NY):
        for i in range(NX):
            s = (-1) ** (i + j)
            if i + 1 < NX:   # horizontal neighbour: shared corner below (s=+1) or above
                sy = -1 if s > 0 else 1
                out.append(((i, j), (i + 1, j), corner(i, j, 1, sy), corner(i + 1, j, -1, sy)))
            if j + 1 < NY:   # vertical neighbour
                sx = 1 if s > 0 else -1
                out.append(((i, j), (i, j + 1), corner(i, j, sx, 1), corner(i, j + 1, sx, -1)))
    return out


def analyse(theta):
    tiles, p = lattice(theta)
    # overlap check on neighbours only (the lattice is local)
    over = 0.0
    for j in range(NY):
        for i in range(NX):
            k = j * NX + i
            for di, dj in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < NX and 0 <= jj < NY:
                    over += tiles[k].intersection(tiles[jj * NX + ii]).area
    xmin, ymin, xmax, ymax = unary_union(tiles).bounds
    W, H = xmax - xmin, ymax - ymin
    tile_area = sum(t.area for t in tiles)
    s = np.cos(theta) + np.sin(theta)
    return dict(theta_deg=theta / DEG, two_theta_deg=2 * theta / DEG, stretch=s - 1,
                W_mm=W / mm, H_mm=H / mm, area_ratio=s ** 2,
                fill_ideal=1 / s ** 2,                      # infinite lattice, sharp squares
                fill_pixels=tile_area / (len(tiles) * (A_TILE * s) ** 2),
                diamond_short_mm=2 * A_TILE * np.sin(theta) / mm,
                diamond_long_mm=2 * A_TILE * np.cos(theta) / mm,
                diamond_area_mm2=A_TILE ** 2 * np.sin(2 * theta) / mm ** 2,
                overlap_mm2=over / mm ** 2)


def hinge_check(theta):
    """Max mismatch of the two corner points of each hinge (must be ~0)."""
    return max(np.linalg.norm(b - c) for _, _, b, c in hinge_points(theta))


def main():
    thetas = np.linspace(0, 45, 91) * DEG
    rows = [analyse(t) for t in thetas]
    W = np.array([r["W_mm"] for r in rows]); H = np.array([r["H_mm"] for r in rows])
    # Poisson ratio from the real finite lattice: nu = -(dW/W)/(dH/H)
    nu = -(np.gradient(W) / W) / (np.gradient(H) / H)
    for r, n in zip(rows, nu):
        r["poisson"] = n
    key = {k: analyse(k * DEG) for k in (17.5, 45.0)}
    for k in key:
        # at 45 deg dW and dH both vanish (the lattice locks), so read nu just below it
        kk = min(k, 44.0)
        key[k]["poisson"] = float(np.interp(kk, [r["theta_deg"] for r in rows], nu))
        key[k]["hinge_closure_um"] = hinge_check(k * DEG) / 1e-6
    res = dict(chamfer_mm=CHAMFER / mm, n_tiles=NX * NY,
               default=key[17.5], maximum=key[45.0],
               max_overlap_mm2=max(r["overlap_mm2"] for r in rows),
               poisson_range=[float(nu[2:-2].min()), float(nu[2:-2].max())],
               final21_claims=dict(stretch_17p5=0.254, stretch_45=0.414,
                                   fill_25=0.61, fill_41=0.475, gap_6mm=6.0,
                                   body_45=[113, 226]))
    save("m1_kinematics", res)

    # ---- plots
    fig, ax = plt.subplots(1, 3, figsize=(12, 7.5))
    for a_, th in zip(ax, (0.0, 17.5, 45.0)):
        tiles, _ = lattice(th * DEG)
        for t in tiles:
            x, y = t.exterior.xy
            a_.fill(np.array(x) / mm, np.array(y) / mm, fc="#4a7bd0", ec="#1b2a4a", lw=0.4)
        for _, _, b, _ in hinge_points(th * DEG):
            a_.plot(b[0] / mm, b[1] / mm, ".", color="#d9480f", ms=1.5)
        a_.set_aspect("equal"); a_.set_title(f"theta = {th:.1f} deg, stretch {np.cos(th*DEG)+np.sin(th*DEG)-1:.1%}")
        a_.set_xlim(-10, 120); a_.set_ylim(-10, 235)
    fig.suptitle("8 x 16 rotating-square body (hinge pivots in orange)")
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m1_lattice.png", dpi=130); plt.close(fig)

    th = [r["theta_deg"] for r in rows]
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    ax[0, 0].plot(th, [100 * r["stretch"] for r in rows]); ax[0, 0].set_ylabel("linear stretch %")
    ax[0, 1].plot(th, [r["area_ratio"] for r in rows]); ax[0, 1].set_ylabel("area ratio")
    ax[1, 0].plot(th, [100 * r["fill_ideal"] for r in rows], label="sharp squares")
    ax[1, 0].plot(th, [100 * r["fill_pixels"] for r in rows], label="chamfered, 8x16 bbox")
    ax[1, 0].set_ylabel("pixel fill %"); ax[1, 0].legend()
    ax[1, 1].plot(th, [r["diamond_short_mm"] for r in rows], label="short diagonal")
    ax[1, 1].plot(th, [r["diamond_long_mm"] for r in rows], label="long diagonal")
    ax[1, 1].set_ylabel("gap diamond mm"); ax[1, 1].legend()
    for a_ in ax.flat:
        a_.set_xlabel("theta deg"); a_.grid(alpha=.3)
        a_.axvline(17.5, color="k", ls=":"); a_.axvline(45, color="k", ls=":")
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m1_kinematics.png", dpi=130); plt.close(fig)
    return res


if __name__ == "__main__":
    r = main()
    for k in ("default", "maximum"):
        print(k, {kk: round(v, 4) if isinstance(v, float) else v for kk, v in r[k].items()})
    print("max overlap mm2", r["max_overlap_mm2"], "poisson", r["poisson_range"])
