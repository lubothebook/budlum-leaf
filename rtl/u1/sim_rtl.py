#!/usr/bin/env python3
"""Simulate the U1 lane RTL with amaranth.sim against the golden model.

For every case it loads the 128 tile registers into the RTL parameter file,
renders a set of tiles in the RTL (the testbench plays the frame store) and
compares every output pixel with golden.render_tile. Result: results/rtl_vs_golden.json

    python3 sim_rtl.py            # the standard set (about 6 min on 4 cores)
    python3 sim_rtl.py --quick    # one tile per case
"""
import json
import os
import sys
import time

import numpy as np
from amaranth.sim import Simulator

import golden as G
from u1_rtl import U1Lane

HERE = os.path.dirname(os.path.abspath(__file__))


def seam_table():
    """Seam shifts in 1/16 px on the quadrant lines (column 3/4, row 7/8)."""
    s = [[(0, 0) for _ in range(G.NX)] for _ in range(G.NY)]
    for j in range(G.NY):
        s[j][3] = (5, 0)
        s[j][4] = (-3, 0)
    for i in range(G.NX):
        a, b = s[7][i]
        s[7][i] = (a, 7)
        a, b = s[8][i]
        s[8][i] = (a, -16)
    return s


def pack_param(r):
    """Pack a register dict into the PARAM struct bit layout."""
    fields = [("acx", G.A_BITS), ("acy", G.A_BITS), ("arx", G.A_BITS), ("ary", G.A_BITS),
              ("bx", G.B_BITS), ("by", G.B_BITS), ("dx", G.SH_BITS), ("dy", G.SH_BITS)]
    v, sh = 0, 0
    for name, w in fields:
        v |= (r[name] & ((1 << w) - 1)) << sh
        sh += w
    return v


def run_case(st, regs, tiles):
    atlas = st['atlas'].reshape(-1).astype(int).tolist()
    cur = st['cursor'].astype(np.int64)
    cur_words = (cur[..., 0] | (cur[..., 1] << 8) | (cur[..., 2] << 16) | (cur[..., 3] << 24))
    dut = U1Lane(atlas_init=atlas, cursor_init=cur_words.reshape(-1).tolist())
    frames = st['frames'].astype(np.int64)
    fw = frames[..., 0] | (frames[..., 1] << 8) | (frames[..., 2] << 16)
    lay = st['layer'].astype(np.int64)
    lw = lay[..., 0] | (lay[..., 1] << 8) | (lay[..., 2] << 16)
    r = st['r']
    out = {}
    stats = {}

    async def tb(ctx):
        # registers
        ctx.set(dut.frame_sel, r['frame_sel'])
        for k in ('rx0', 'rx1', 'ry0', 'ry1', 'sx', 'sy', 'cx', 'cy'):
            ctx.set(getattr(dut, k), r[k])
        ctx.set(dut.glyph_rgb, r['glyph_rgb'][0] | (r['glyph_rgb'][1] << 8) | (r['glyph_rgb'][2] << 16))
        gv = 0
        for k, g in enumerate(r['glyphs']):
            gv |= (g['valid'] & 1) << k
            ctx.set(dut.g_x[k], g['x'])
            ctx.set(dut.g_y[k], g['y'])
            ctx.set(dut.g_idx[k], g['idx'])
        ctx.set(dut.g_valid, gv)
        # parameter file
        ctx.set(dut.prm_we, 1)
        for t, rg in enumerate(regs):
            ctx.set(dut.prm_waddr, t)
            ctx.set(dut.prm_wdata.as_value(), pack_param(rg))
            await ctx.tick()
        ctx.set(dut.prm_we, 0)
        await ctx.tick()
        for t in tiles:
            img = np.full((G.TILE, G.TILE, 3), -1, dtype=np.int64)
            ctx.set(dut.tile, t)
            ctx.set(dut.start, 1)
            await ctx.tick()
            ctx.set(dut.start, 0)
            prev = None
            cycles = 0
            t0 = time.time()
            while True:
                req, layer, frm, x, y = ctx.get(dut.fs_req), ctx.get(dut.fs_layer), \
                    ctx.get(dut.fs_frame), ctx.get(dut.fs_x), ctx.get(dut.fs_y)
                if prev is not None:
                    ctx.set(dut.fs_data, prev)
                prev = (int(lw[y, x]) if layer else int(fw[frm, y, x])) if req else None
                if ctx.get(dut.o_valid):
                    v = ctx.get(dut.o_rgb)
                    img[ctx.get(dut.o_v), ctx.get(dut.o_u)] = (v & 255, (v >> 8) & 255, v >> 16)
                if ctx.get(dut.done):
                    break
                await ctx.tick()
                cycles += 1
            out[t] = img
            stats[t] = dict(cycles=cycles, oob=int(ctx.get(dut.oob)), wall_s=round(time.time() - t0, 1))

    sim = Simulator(dut)
    sim.add_clock(5e-9)
    sim.add_testbench(tb)
    sim.run()
    return out, stats


def build_case(k, quick=False):
    """Case k of 7: circle and grid at 0, 17.5 and 45 deg, then the compositor scene."""
    seam = seam_table()
    tl = [60] if quick else [0, 27, 59, 60, 127]  # corner, interior, seam pair, last
    if k < 6:
        kind, th = ('circle', 'grid')[k // 3], (0.0, 17.5, 45.0)[k % 3]
        st = G.empty_store()
        st['frames'][0] = G.raster(kind)
        regs = G.tile_regs(G.pose_unit(G.uniform_phi(th)), seam)
        return f"{kind}@{th}", st, regs, tl
    st = G.compositor_scene()
    regs = G.tile_regs(G.pose_unit(G.uniform_phi(17.5)), seam)
    return "compositor@17.5", st, regs, ([1] if quick else [0, 1, 8, 9])


def work(arg):
    k, quick = arg
    name, st, regs, tiles = build_case(k, quick)
    rtl, stats = run_case(st, regs, tiles)
    rows = []
    for t in tiles:
        gold = G.render_tile(t, regs, st)
        diff = int(np.count_nonzero(rtl[t] != gold))
        ok = diff == 0 and stats[t]['oob'] == 0
        rows.append(dict(case=name, tile=t, pixels=G.TILE * G.TILE * 3, mismatches=diff,
                         bit_exact=ok, **stats[t]))
        print(rows[-1], flush=True)
    return rows


def main():
    from multiprocessing import Pool
    quick = '--quick' in sys.argv
    res = dict(cases=[], all_bit_exact=True)
    with Pool(4) as pool:
        for rows in pool.map(work, [(k, quick) for k in range(7)]):
            for row in rows:
                res['all_bit_exact'] &= row['bit_exact']
                res['cases'].append(row)
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    fn = 'rtl_vs_golden_quick.json' if quick else 'rtl_vs_golden.json'
    with open(os.path.join(HERE, 'results', fn), 'w') as f:
        json.dump(res, f, indent=1)
    print("ALL BIT EXACT:", res['all_bit_exact'])
    return 0 if res['all_bit_exact'] else 1


if __name__ == '__main__':
    sys.exit(main())
