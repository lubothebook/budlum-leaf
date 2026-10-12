#!/usr/bin/env python3
"""Gate DSP-17: the shape error of the per-tile warp, full frame, all 128 tiles.

The golden model (bit-exact with the RTL, see sim_rtl.py) renders every tile.
Each tile pixel is then placed at its true physical position (float pose of the
rotating-square lattice). The edge pixels (picked by the true geometry, |sdf| < 0.5 px)
give a sub-pixel edge estimate from the 4-px anti-aliased ramp: sdf_hat = (0.5 - I) * RAMP. We compare it with the true shape.

  circle: radius estimate of each edge pixel, r_hat = |p - c| - sdf_hat
          shape error = max |r_hat - R| / R, over all circles
  grid:   line-edge position error, max |sdf_hat - sdf| / pitch

The baseline is the same body with no warp (each tile shows its rest square).
Writes results/shape_error.json and results/warp_*.png.
"""
import json
import os

import numpy as np

import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
PITCH_UM = 50.0
# Edge pixels are picked by the TRUE geometry: |sdf| < EDGE. Then all four bilinear
# taps (within sqrt(2) px) sit on the linear part of the ramp, so the estimate
# sdf_hat = (0.5 - I) * RAMP has no clipping bias.
EDGE = G.RAMP / 2 - 1.5


def true_src_positions(phi):
    tp = G.true_pose(phi)
    v, u = np.mgrid[0:G.TILE, 0:G.TILE].astype(np.float64)
    pu, pv = u - (G.TILE - 1) / 2, v - (G.TILE - 1) / 2
    world = np.zeros((G.NY * G.NX, G.TILE, G.TILE, 2))
    for j in range(G.NY):
        for i in range(G.NX):
            a = tp['ang'][j, i]
            c, s = np.cos(a), np.sin(a)
            t = j * G.NX + i
            world[t, ..., 0] = tp['C'][j, i, 0] + c * pu - s * pv
            world[t, ..., 1] = tp['C'][j, i, 1] + s * pu + c * pv
    src = (world - tp['mean']) / tp['s'] + np.array([G.W / 2 - 0.5, G.H / 2 - 0.5])
    return world, src, tp['s']


def measure(kind, img, src, s):
    I = img[..., 0].astype(np.float64) / 255.0
    X, Y = src[..., 0], src[..., 1]
    sdf_hat = (0.5 - I) * G.RAMP
    if kind == 'circle':
        worst, n = 0.0, 0
        per = []
        for (cx, cy, R) in G.CIRCLES:
            d_this = np.hypot(X - cx, Y - cy) - R
            d_all = G.sdf_circles(X, Y, G.CIRCLES)
            m = (np.abs(d_this - d_all) < 1e-9) & (np.abs(d_this) < EDGE)
            r_hat = np.hypot(X[m] - cx, Y[m] - cy) - sdf_hat[m]
            err = np.abs(r_hat - R)
            e = float(err.max() / R) if err.size else 0.0
            per.append(dict(R=R, edge_pixels=int(m.sum()), max_err_px=float(err.max()),
                            rms_err_px=float(np.sqrt((err ** 2).mean())),
                            shape_error_pct=100 * e,
                            size_error_pct=float(100 * abs(r_hat.mean() - R) / R)))
            worst = max(worst, e)
            n += int(m.sum())
        return dict(shape_error_pct=100 * worst, edge_pixels=n, circles=per,
                    max_edge_err_um=max(p['max_err_px'] for p in per) * s * PITCH_UM)
    g = G.GRID
    dx = np.abs(((X - g['x0'] + g['pitch'] / 2) % g['pitch']) - g['pitch'] / 2)
    dy = np.abs(((Y - g['y0'] + g['pitch'] / 2) % g['pitch']) - g['pitch'] / 2)
    lim = g['hw'] + G.RAMP + 1.5
    sdf = G.sdf_grid(X, Y, **g)
    m = (np.abs(sdf) < EDGE) & ~((dx < lim) & (dy < lim))  # skip the line crossings
    err = np.abs(sdf_hat[m] - sdf[m])
    return dict(shape_error_pct=float(100 * err.max() / g['pitch']), edge_pixels=int(m.sum()),
                max_err_px=float(err.max()), rms_err_px=float(np.sqrt((err ** 2).mean())),
                max_edge_err_um=float(err.max() * s * PITCH_UM))


def geometry_error(regs, src):
    """Source point used by the fixed-point DDA versus the true source point, px."""
    v, u = np.mgrid[0:G.TILE, 0:G.TILE].astype(np.int64)
    worst = 0.0
    for t, r in enumerate(regs):
        bx, by, _, _, _ = G.tile_setup(r)
        X = (bx + u * r['acx'] + v * r['arx']) / G.ONE
        Y = (by + u * r['acy'] + v * r['ary']) / G.ONE
        worst = max(worst, float(np.hypot(X - src[t, ..., 0], Y - src[t, ..., 1]).max()))
    return worst


def splat(world, img, s, path):
    """Forward-place every tile pixel at its physical position (a picture of the face)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    k = 0.25  # canvas px per tile px
    wpx = world.reshape(-1, 2)
    lo = wpx.min(0)
    sz = np.ceil((wpx.max(0) - lo) * k).astype(int) + 2
    can = np.full((sz[1], sz[0]), 40, dtype=np.uint8)  # dark diamonds
    q = np.round((wpx - lo) * k).astype(int)
    can[q[:, 1], q[:, 0]] = img[..., 0].reshape(-1)
    plt.imsave(path, can, cmap='gray', vmin=0, vmax=255)


def seam_shift_check():
    """1/16-px seam steps: a vertical edge moves by dx/16 px on the tile."""
    st = G.empty_store()
    Y, X = np.mgrid[0:G.H, 0:G.W].astype(np.float64)
    d = (X - 100.3)  # one vertical edge inside tile 0
    st['frames'][0] = np.repeat(np.round(np.clip(0.5 - d / G.RAMP, 0, 1) * 255)
                                .astype(np.uint8)[..., None], 3, axis=2)
    base = G.identity_regs()
    rows = []
    ref = None
    for k in range(0, 17):
        regs = [dict(r) for r in base]
        regs[0]['dx'] = k
        img = G.render_tile(0, regs, st)[..., 0].astype(np.float64) / 255
        row = img[100]
        idx = np.where((row[:-1] >= 0.5) & (row[1:] < 0.5))[0][0]
        pos = idx + (row[idx] - 0.5) / (row[idx] - row[idx + 1])
        ref = pos if ref is None else ref
        rows.append(dict(step=k, expected_px=k / 16, measured_px=float(pos - ref)))
    err = max(abs(r['measured_px'] - r['expected_px']) for r in rows)
    return dict(steps=rows, max_step_error_px=err, max_step_error_um=err * PITCH_UM)


def main():
    os.makedirs(OUT, exist_ok=True)
    res = dict(gate='DSP-17', pass_limit_pct=1.0, runs=[])
    frames = {k: G.raster(k) for k in ('circle', 'grid')}
    for th, label in ((0.0, '0%'), (17.5, '25.4%'), (45.0, '41.4%')):
        phi = G.uniform_phi(th)
        regs = G.tile_regs(G.pose_unit(phi))
        world, src, s = true_src_positions(phi)
        geo = geometry_error(regs, src)
        print(th, 'DDA geometry error px', geo)
        for kind in ('circle', 'grid'):
            st = G.empty_store()
            st['frames'][0] = frames[kind]
            img = G.render_all(regs, st)
            mw = measure(kind, img, src, s)
            base = G.render_all(G.identity_regs(), st)
            mb = measure(kind, base, src, s)
            mb['displacement_px'] = geometry_error(G.identity_regs(), src)
            row = dict(theta_deg=th, stretch=label, image=kind, warped=mw,
                       dda_geometry_error_px=geo,
                       baseline_no_warp=dict(shape_error_pct=mb['shape_error_pct'],
                                             displacement_px=mb['displacement_px']),
                       passes=bool(mw['shape_error_pct'] < 1.0))
            res['runs'].append(row)
            print(th, kind, 'warp %.4f %%' % mw['shape_error_pct'],
                  'no-warp %.2f %% (saturated), displacement %.1f px' % (
                      mb['shape_error_pct'], mb['displacement_px']), flush=True)
            if th > 0:
                splat(world, img, s, os.path.join(OUT, f'warp_{kind}_{th:g}.png'))
                if kind == 'circle':
                    splat(world, base, s, os.path.join(OUT, f'nowarp_{kind}_{th:g}.png'))
    res['seam_shift'] = seam_shift_check()
    print('seam step error px', res['seam_shift']['max_step_error_px'])
    res['all_pass'] = all(r['passes'] for r in res['runs'])
    with open(os.path.join(OUT, 'shape_error.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print('DSP-17 all pass:', res['all_pass'])


if __name__ == '__main__':
    main()
