#!/usr/bin/env python3
"""cs2d.py - 2-D quasi-static cross-section of the bar line (A1, A2).

The A1 inverted-F arm and the body edge ground form a transmission line.
This script solves Laplace's equation on the bar cross-section with the
real layers (FINAL/21 21.2.7 tile stack, 21.3.2 bar stack) by finite
differences, and returns Z0 and eps_eff of the arm line.

Coordinates of the section: y points out of the body edge, z across the
body thickness. The front face is z = +1.00 mm, the edge face is y = 0.
The bar spans y = 0..1.00 mm and z = -1.00..+3.00 mm (it overhangs the
face by 2.00 mm on the ring side, because the bar is 4.0 mm across).

The ground is the metal of every tile: the cell can (z = -0.68..+0.22 mm)
and the coil or spreader layer (z = +0.22..+0.42 mm), inset 0.375 mm from
the tile edge. Run: python3 cs2d.py
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from rf_common import C0, EPS0, EPS_LCP_GF40, EPS_LCP_FILM, CAN_INSET

MM = 1e-3


def build_eps(Y, Z, with_diel=True):
    """Cell permittivity map on the cell centres Y, Z (in mm)."""
    e = np.ones_like(Y)
    if not with_diel:
        return e
    body = Y < 0
    # body dielectrics by the tile stack
    e[body & (Z > 0.42) & (Z <= 0.47)] = 3.0              # slip OCA + OCA
    e[body & (Z > 0.47) & (Z <= 0.75)] = 5.8              # glass / LED / glass
    e[body & (Z > 0.75) & (Z <= 1.00)] = 2.9              # PC cap
    e[body & (Z >= -1.0) & (Z < -0.68)] = 3.1             # skin + routing
    e[body & (Z >= -0.68) & (Z <= 0.42)] = 3.0            # inset rim round the can
    bar = (Y >= 0) & (Y <= 1.0) & (Z >= -1.0) & (Z <= 3.0)
    e[bar] = EPS_LCP_GF40
    e[bar & (Y >= 0.25) & (Y < 0.35)] = EPS_LCP_FILM      # mmWave flex layer
    return e


def solve(strip_z=(1.3, 2.9), strip_y=(0.75, 0.80), h=0.05, box=15.0,
          with_diel=True, edge_inset=CAN_INSET / MM, extra_ground=None):
    """Return the capacitance per metre of the strip to the ground."""
    ys = np.arange(-box, box + h / 2, h)
    zs = np.arange(-box, box + h / 2, h)
    ny, nz = len(ys), len(zs)
    YN, ZN = np.meshgrid(ys, zs, indexing="ij")
    yc = 0.5 * (ys[1:] + ys[:-1]); zc = 0.5 * (zs[1:] + zs[:-1])
    YC, ZC = np.meshgrid(yc, zc, indexing="ij")
    eps = build_eps(YC, ZC, with_diel)
    fixed = np.zeros((ny, nz), bool)
    V = np.zeros((ny, nz))
    ground = (YN <= -edge_inset + 1e-9) & (ZN >= -0.68 - 1e-9) & (ZN <= 0.42 + 1e-9)
    if extra_ground is not None:
        ground |= extra_ground(YN, ZN)
    strip = (YN >= strip_y[0] - 1e-9) & (YN <= strip_y[1] + 1e-9) & \
            (ZN >= strip_z[0] - 1e-9) & (ZN <= strip_z[1] + 1e-9)
    border = np.zeros_like(fixed); border[0, :] = border[-1, :] = True
    border[:, 0] = border[:, -1] = True
    fixed |= ground | strip | border
    V[strip] = 1.0
    # edge permittivities: an edge between nodes (i,j)-(i+1,j) borders cells (i,j-1),(i,j)
    epad = np.pad(eps, 1, mode="edge")      # (ny+1, nz+1)
    ey = 0.5 * (epad[1:-1, :-1] + epad[1:-1, 1:])   # y-edges: (ny-1, nz)
    ez = 0.5 * (epad[:-1, 1:-1] + epad[1:, 1:-1])   # z-edges: (ny, nz-1)
    idx = -np.ones((ny, nz), int)
    free = ~fixed
    idx[free] = np.arange(free.sum())
    n = free.sum()
    rows, cols, vals = [], [], []
    rhs = np.zeros(n)
    diag = np.zeros(n)

    def couple(i0, j0, i1, j1, w):
        # add edge between node arrays (i0,j0) and (i1,j1) of weight w
        a, b = idx[i0, j0], idx[i1, j1]
        fa, fb = free[i0, j0], free[i1, j1]
        m = fa
        np.add.at(diag, a[m], w[m])
        mm = fa & fb
        rows.append(a[mm]); cols.append(b[mm]); vals.append(-w[mm])
        mf = fa & ~fb
        np.add.at(rhs, a[mf], w[mf] * V[i1, j1][mf])
    I, J = np.meshgrid(np.arange(ny - 1), np.arange(nz), indexing="ij")
    couple(I, J, I + 1, J, ey); couple(I + 1, J, I, J, ey)
    I, J = np.meshgrid(np.arange(ny), np.arange(nz - 1), indexing="ij")
    couple(I, J, I, J + 1, ez); couple(I, J + 1, I, J, ez)
    rows.append(np.arange(n)); cols.append(np.arange(n)); vals.append(diag)
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    x = spl.spsolve(A.tocsc(), rhs)
    V[free] = x
    # energy W = 1/2 sum eps |grad V|^2 over edges (the h^2 cell area cancels the 1/h^2)
    dVy = V[1:, :] - V[:-1, :]
    dVz = V[:, 1:] - V[:, :-1]
    W = 0.5 * EPS0 * ((ey * dVy ** 2).sum() + (ez * dVz ** 2).sum())
    return 2 * W   # C per metre for V = 1


def line(strip_z=(1.3, 2.9), **kw):
    C = solve(strip_z=strip_z, with_diel=True, **kw)
    Ca = solve(strip_z=strip_z, with_diel=False, **kw)
    ee = C / Ca
    Z0 = 1.0 / (C0 * np.sqrt(C * Ca))
    return Z0, ee, C, Ca


if __name__ == "__main__":
    print("cs2d: the A1 / A2 arm line over the body edge ground")
    print(f"  grid 0.05 mm, box +/-15 mm. Ground inset {CAN_INSET*1e3:.3f} mm (can of 9.25 mm in a 10 mm tile)")
    cases = [("A1 over the overhang, z = 1.3..2.9 (1.6 mm wide)", (1.3, 2.9)),
             ("A1 over the edge, z = -0.8..0.8 (1.6 mm)", (-0.8, 0.8)),
             ("A2 over the edge, z = -0.9..0.9 (1.8 mm)", (-0.9, 0.9)),
             ("A1 full width, z = -0.9..2.9 (3.8 mm)", (-0.9, 2.9))]
    for name, z in cases:
        Z0, ee, C, Ca = line(z)
        print(f"  {name:52s} Z0 = {Z0:6.1f} Ohm  eps_eff = {ee:4.2f}  C = {C*1e12:5.1f} pF/m")
    Z0b, eeb, _, _ = line((1.3, 2.9), box=22.0)
    print(f"  box check (+/-22 mm), overhang strip: Z0 = {Z0b:6.1f} Ohm, eps_eff = {eeb:4.2f}")
    # the user's 1.00 mm reference height: copper 1.00 mm over a flush edge ground
    Z0r, eer, _, _ = line((-0.8, 0.8), edge_inset=0.25)
    print(f"  reference, copper 1.00 mm over the ground face (inset 0.25): Z0 = {Z0r:6.1f} Ohm, eps_eff = {eer:4.2f}")
    import json, os
    out = {}
    for key, z in (("A1_overhang", (1.3, 2.9)), ("A1_edge", (-0.8, 0.8)), ("A2_edge", (-0.9, 0.9))):
        Z0, ee, C, Ca = line(z)
        out[key] = dict(Z0=Z0, eps_eff=ee, C=C, Ca=Ca, Z0_air=1.0 / (C0 * Ca), strip_z_mm=z)
    os.makedirs("out", exist_ok=True)
    json.dump(out, open("out/cs2d.json", "w"), indent=1)
    print("  wrote out/cs2d.json")
