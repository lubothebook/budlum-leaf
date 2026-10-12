#!/usr/bin/env python3
"""warp.py - the stretched view: what U1 must warp, and how well.

Budlum Leaf L.6.0, Display team, hw/display/.

Model (rotating squares, Part 21.2.1)
  tile (i, j) turns by phi = (-1)^(i+j) * theta about its centre;
  the tile centres stay on a square lattice of pitch a * (cos theta + sin theta).
  The script checks this from the hinge geometry first.

Then, for a circle and a grid drawn on the canvas, at 25.4 % and 41.4 %:
  - no warp (each tile shows its rest image)         -> the shape error
  - the U1 per-tile affine warp, perfect angles      -> the shape error
  - the warp with a per-tile angle error of 0.1 deg, 0.5 deg and 1 deg
Gate DSP-17: the shape error under 1 %.

Run:  python3 warp.py      (writes out/stretched_view.png)
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
A = 10.0          # mm tile
NX, NY = 8, 16
NPX = 200
P = A / NPX
rng = np.random.default_rng(7)


def R(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s], [s, c]])


# --- 1. kinematics check: the hinge points meet
def check_hinges(theta):
    s = np.cos(theta) + np.sin(theta)
    err = 0.0
    for i in range(NX - 1):
        for j in range(NY):
            pa, pb = (-1) ** (i + j) * theta, (-1) ** (i + 1 + j) * theta
            ca, cb = np.array([i, j]) * A * s, np.array([i + 1, j]) * A * s
            # the hinge corner pair: the right corners of A and the left corners of B
            best = min(np.linalg.norm(ca + R(pa) @ np.array([A / 2, sy * A / 2])
                                      - cb - R(pb) @ np.array([-A / 2, sy * A / 2]))
                       for sy in (-1, 1))
            err = max(err, best)
    return err


print("== the rotating-square kinematics ==")
for deg in (0, 17.5, 30, 45):
    th = np.radians(deg)
    s = np.cos(th) + np.sin(th)
    print(f"theta {deg:5.1f} deg: stretch {100*(s-1):5.1f} %, area x{s*s:.3f}, "
          f"pixel coverage {100/s/s:5.1f} %, hinge closure error {check_hinges(th)*1e3:.2e} um, "
          f"body {80*s:.1f} x {160*s:.1f} mm")
print("note: Part 21.2.3 quotes 61 % and 47.5 % coverage. Full-square pixel glass gives 63.5 % and 50.0 %.")
print()

# local pixel coordinates (centres) relative to the tile centre
u = (np.arange(NPX) - (NPX - 1) / 2) * P
UX, UY = np.meshgrid(u, u)
U = np.stack([UX.ravel(), UY.ravel()])            # 2 x 40 000


def physical(theta_k):
    """Physical positions of every pixel, per tile. theta_k: NX x NY true angles.
    Centres follow the mean stretch (one degree of freedom)."""
    th = theta_k.mean()
    s = np.cos(th) + np.sin(th)
    pos = {}
    for i in range(NX):
        for j in range(NY):
            phi = (-1) ** (i + j) * theta_k[i, j]
            c = (np.array([i, j]) - np.array([(NX - 1) / 2, (NY - 1) / 2])) * A * s
            pos[(i, j)] = c[:, None] + R(phi) @ U
    return pos, s


def shape_error(theta, sigma_deg, warp=True, trials=1):
    """Draw a circle of radius 25 mm (canvas units) and a grid line; return the
    worst relative radial error of the lit physical pixels."""
    worst_c, worst_g = 0.0, 0.0
    for _ in range(trials):
        theta_true = np.full((NX, NY), theta)
        pos, s = physical(theta_true)
        est = theta_true + np.radians(sigma_deg) * rng.standard_normal((NX, NY))
        pos_est, s_est = physical(est) if warp else physical(np.zeros((NX, NY)))
        r0 = 25.0
        rad, gl = [], []
        for k in pos:
            X = pos[k]                    # where the light is
            Xe = pos_est[k]               # where U1 thinks it is
            if warp:
                canvas = Xe / s_est       # canvas sample shown by that pixel (zoom mode)
            else:
                canvas = Xe               # rest image, no warp
            dist = np.hypot(canvas[0], canvas[1])
            lit = np.abs(dist - r0) < P / 2
            if lit.any():
                rad.append(np.hypot(X[0, lit], X[1, lit]))
            litg = np.abs(canvas[1] - 12.51) < P / 2          # a horizontal grid line
            if litg.any():
                gl.append(X[:, litg])
        rad = np.concatenate(rad)
        r_fit = rad.mean()
        worst_c = max(worst_c, np.abs(rad - r_fit).max() / r_fit)
        g = np.concatenate(gl, axis=1)
        coef = np.polyfit(g[0], g[1], 1)
        resid = g[1] - np.polyval(coef, g[0])
        worst_g = max(worst_g, np.abs(resid).max() / (80 * s) )
    return worst_c, worst_g, r_fit / r0


print("== DSP-17: the shape error of a 25 mm circle and a grid line ==")
print("(error = largest radial deviation of the lit pixels / radius; line = deviation / body width)")
ok = True
for deg in (17.5, 45.0):
    th = np.radians(deg)
    for label, sig, warp in (("no warp", 0.0, False), ("U1 warp, exact angles", 0.0, True),
                             ("U1 warp, 0.1 deg rms", 0.1, True), ("U1 warp, 0.5 deg rms", 0.5, True),
                             ("U1 warp, 1.0 deg rms", 1.0, True)):
        ec, eg, scale = shape_error(th, sig, warp, trials=3 if sig else 1)
        floor = (P / 2) / 25.0
        mark = "PASS" if ec < 0.01 else "fail"
        print(f"  theta {deg:4.1f}: {label:24s} circle {100*ec:6.2f} %  line {100*eg:6.3f} %  "
              f"scale {scale:.3f}  {mark}")
        if warp and sig <= 0.5:
            ok &= ec < 0.01
print(f"  the sampling floor of a 50 um pixel on a 25 mm circle is {100*(P/2)/25:.2f} %")
print()

print("== the U1 warp requirement, derived ==")
px = 1600 * 3200
print(f"  output: {px/1e6:.2f} Mpx per frame, x240 = {px*240/1e9:.2f} Gpx/s, bilinear = {4*px*240/1e9:.2f} Gtap/s")
for deg in (17.5, 45.0):
    th = np.radians(deg)
    s = np.cos(th) + np.sin(th)
    bb = s  # bounding box of a turned tile, in tile edges
    print(f"  theta {deg}: source window per tile {200*bb:.0f} x {200*bb:.0f} px (zoom mode reads "
          f"{200*bb/s:.0f} x {200*bb/s:.0f} canvas px), canvas for the 'more room' mode "
          f"{1600*s:.0f} x {3200*s:.0f} = {1600*3200*s*s*3/1e6:.1f} MB raw at 24 b")
lever = 141.4                     # px from tile centre to corner
for err in (0.1, 0.5):
    print(f"  angle error {err} deg moves a tile corner by {lever*np.radians(err):.2f} px")
print("  coordinate format: 13 b integer + 4 b fraction (1/16 px = 3.125 um, the seam shift step)")
print("  angle input: per tile, 16 b, from the hinge sensors via the back channel, at 480 Hz")
print("  warp latency: applied at scan-out, angles at most one frame (4.2 ms) old -> SW-21 under 10 ms")
print()


def plot(theta_deg, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    th = np.radians(theta_deg)
    pos, s = physical(np.full((NX, NY), th))
    fig, axes = plt.subplots(1, 2, figsize=(10, 9))
    for ax, warp in zip(axes, (False, True)):
        for (i, j), X in pos.items():
            phi = (-1) ** (i + j) * th
            c = (np.array([i, j]) - np.array([(NX - 1) / 2, (NY - 1) / 2])) * A * s
            corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * A / 2
            poly = (R(phi) @ corners.T).T + c
            ax.add_patch(Polygon(poly, closed=True, facecolor="#1b1f24", edgecolor="#555", lw=0.4))
            rest_c = (np.array([[i], [j]]) - np.array([[(NX - 1) / 2], [(NY - 1) / 2]])) * A
            canvas = X / s if warp else rest_c + U
            d = np.hypot(canvas[0], canvas[1])
            lit = (np.abs(d - 25.0) < 0.6) | (np.abs(np.mod(canvas[0] + 5, 20) - 10) < 0.25) \
                | (np.abs(np.mod(canvas[1] + 5, 20) - 10) < 0.25)
            ax.plot(X[0, lit], X[1, lit], ",", color="#7fdcff")
        ax.set_aspect("equal")
        ax.set_xlim(-60, 60)
        ax.set_ylim(-60, 60)
        ax.set_facecolor("black")
        ax.set_title(("U1 per-tile warp" if warp else "no warp") + f", theta {theta_deg} deg", fontsize=10)
    fig.suptitle("The stretched view: a 25 mm circle and a 20 mm grid at 25.4 % stretch (centre detail)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


plot(17.5, os.path.join(OUT, "stretched_view.png"))
print("wrote out/stretched_view.png")
print("DSP-17 (model):", "PASS at 0.5 deg rms angle error or better" if ok else "FAIL")
