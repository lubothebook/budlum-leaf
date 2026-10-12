#!/usr/bin/env python3
"""U1 golden model: bit-exact fixed-point reference of the U1 TCON/compositor.

Every function here uses integer arithmetic only (numpy int64, Python int).
The Amaranth RTL in u1_rtl.py must match it bit for bit.

Four jobs, no program:
  1. cursor overlay     (32x32 RGBA8888 sprite, alpha blend)
  2. scroll offset      (a rectangle of the frame reads from a taller layer)
  3. glyph echo         (8 glyph slots, 4-bit coverage atlas sent by the validator)
  4. stretch warp       (per-tile affine map, bilinear resample, 1/16-px seam shift)
plus the "pick" of one of 4 speculative frames (frame_sel).

Coordinate rule: source pixel (x, y) has its centre at the integer point (x, y).
Tile pixel (u, v), u, v in 0..199, reads source point  X = b + u*ac + v*ar.
"""
import math
import numpy as np

# ---------------------------------------------------------------- constants
TILE = 200                 # pixels per tile side
NX, NY = 8, 16             # tiles across, tiles down
W, H = NX * TILE, NY * TILE  # 1600 x 3200 frame
FA = 18                    # fractional bits of A and of b / the DDA accumulator
WB = 6                     # bilinear weight bits (1/64 px)
SEAM_FB = 4                # seam shift is in 1/16 px of the tile (output) lattice
WW = 208                   # tile source window side (even, parity banked 2x2)
WH = WW // 2               # bank side (104)
A_BITS = 20                # signed S1.18
B_BITS = 34                # signed S15.18
SH_BITS = 6                # signed seam shift, -32..31 sixteenths
TRIG_STEPS = 4096          # hinge-angle code: 4096 steps per 90 degrees
NGLYPH = 8                 # glyph echo slots
GW, GH = 16, 32            # glyph cell
NATLAS = 64                # glyphs in the atlas
CUR = 32                   # cursor sprite side
WL, HL = 1600, 6400        # scroll layer size
NFRAMES = 4                # speculative frames in the store

ONE = 1 << FA


def rnd_shift(x, s):
    """Round-half-up arithmetic right shift (works for int and int64 arrays)."""
    return (x + (1 << (s - 1))) >> s


# ------------------------------------------------------------- pose unit
def trig_lut(code):
    """cos and sin ROM, S1.18, code in 1/4096 of 90 degrees (signed)."""
    a = code * (math.pi / 2) / TRIG_STEPS
    return int(round(math.cos(a) * ONE)), int(round(math.sin(a) * ONE))


def hinge_corners(sign):
    """Local hinge corners (right, down) in px from the tile centre.

    Rotating squares: tiles with sign +1 turn +theta, tiles with -1 turn -theta.
    Returns (h_right, h_left, h_down, h_up) as (x, y) tuples of half-sides.
    """
    if sign > 0:
        return (1, -1), (-1, 1), (1, 1), (-1, -1)
    return (1, 1), (-1, -1), (-1, 1), (1, -1)


def rotq(c, s, hx, hy, half=TILE // 2):
    """R(phi) * (hx, hy) * half, Q18 px."""
    return (c * hx - s * hy) * half, (s * hx + c * hy) * half


def pose_unit(phi_code):
    """Fixed-function pose unit: hinge angles -> per-tile registers.

    phi_code: int array (NY, NX), signed turn of each tile in 1/4096 of 90 deg.
    Returns dict with ac, ar, b (Q18 ints, shape (NY, NX, 2)) and diagnostics.
    The chain is integrated down column 0, then along every row.
    """
    cs = np.zeros((NY, NX, 2), dtype=object)
    for j in range(NY):
        for i in range(NX):
            cs[j, i] = trig_lut(int(phi_code[j, i]))
    C = np.zeros((NY, NX, 2), dtype=object)  # Q18 px, tile 0,0 at 0
    C[0, 0] = (0, 0)
    for j in range(NY):
        if j > 0:  # step down from (j-1, 0)
            sa = 1 if ((j - 1) % 2 == 0) else -1
            sb = -sa
            ca, sna = cs[j - 1, 0]
            cb, snb = cs[j, 0]
            ha = hinge_corners(sa)[2]
            hb = hinge_corners(sb)[3]
            ax, ay = rotq(ca, sna, *ha)
            bx, by = rotq(cb, snb, *hb)
            C[j, 0] = (C[j - 1, 0][0] + ax - bx, C[j - 1, 0][1] + ay - by)
        for i in range(1, NX):
            sa = 1 if ((i - 1 + j) % 2 == 0) else -1
            sb = -sa
            ca, sna = cs[j, i - 1]
            cb, snb = cs[j, i]
            ha = hinge_corners(sa)[0]
            hb = hinge_corners(sb)[1]
            ax, ay = rotq(ca, sna, *ha)
            bx, by = rotq(cb, snb, *hb)
            C[j, i] = (C[j, i - 1][0] + ax - bx, C[j, i - 1][1] + ay - by)
    # face scale from the chain extent (integer divider, once per update)
    dx = sum(C[j, NX - 1][0] - C[j, 0][0] for j in range(NY))
    dy = sum(C[NY - 1, i][1] - C[0, i][1] for i in range(NX))
    s_q = (dx // (NY * (NX - 1) * TILE) + dy // (NX * (NY - 1) * TILE)) // 2
    inv_s = ((1 << (2 * FA)) + s_q // 2) // s_q
    mx = sum(C[j, i][0] for j in range(NY) for i in range(NX))
    my = sum(C[j, i][1] for j in range(NY) for i in range(NX))
    mx = mx // (NX * NY)
    my = my // (NX * NY)
    ac = np.zeros((NY, NX, 2), dtype=np.int64)
    ar = np.zeros((NY, NX, 2), dtype=np.int64)
    b = np.zeros((NY, NX, 2), dtype=np.int64)
    half = (TILE - 1) / 2  # 99.5, pixel-centre offset
    for j in range(NY):
        for i in range(NX):
            c, s = cs[j, i]
            acx, acy = rnd_shift(c * inv_s, FA), rnd_shift(s * inv_s, FA)
            arx, ary = -acy, acx
            # world of pixel (0,0) relative to the face mean, Q18
            p0x = C[j, i][0] - mx - (c * 199 - s * 199) // 2
            p0y = C[j, i][1] - my - (s * 199 + c * 199) // 2
            bx = rnd_shift(p0x * inv_s, FA) + (W // 2) * ONE - ONE // 2
            by = rnd_shift(p0y * inv_s, FA) + (H // 2) * ONE - ONE // 2
            ac[j, i] = (acx, acy)
            ar[j, i] = (arx, ary)
            b[j, i] = (bx, by)
    return dict(ac=ac, ar=ar, b=b, inv_s=inv_s, s_q=s_q, C=C, mean=(mx, my))


def uniform_phi(theta_deg):
    """Hinge codes of a uniform stretch: checkerboard +theta / -theta."""
    code = int(round(theta_deg / 90.0 * TRIG_STEPS))
    phi = np.zeros((NY, NX), dtype=np.int64)
    for j in range(NY):
        for i in range(NX):
            phi[j, i] = code if (i + j) % 2 == 0 else -code
    return phi


def true_pose(phi_code):
    """Float pose (the physical truth) for the shape-error measurement."""
    ang = phi_code * (math.pi / 2) / TRIG_STEPS
    C = np.zeros((NY, NX, 2))
    for j in range(NY):
        if j > 0:
            sa = 1 if ((j - 1) % 2 == 0) else -1
            ha, hb = hinge_corners(sa)[2], hinge_corners(-sa)[3]
            C[j, 0] = C[j - 1, 0] + _rf(ang[j - 1, 0], ha) - _rf(ang[j, 0], hb)
        for i in range(1, NX):
            sa = 1 if ((i - 1 + j) % 2 == 0) else -1
            ha, hb = hinge_corners(sa)[0], hinge_corners(-sa)[1]
            C[j, i] = C[j, i - 1] + _rf(ang[j, i - 1], ha) - _rf(ang[j, i], hb)
    sx = (C[:, -1, 0] - C[:, 0, 0]).mean() / ((NX - 1) * TILE)
    sy = (C[-1, :, 1] - C[0, :, 1]).mean() / ((NY - 1) * TILE)
    return dict(ang=ang, C=C, s=(sx + sy) / 2, mean=C.reshape(-1, 2).mean(0))


def _rf(a, h):
    c, s = math.cos(a), math.sin(a)
    hx, hy = h[0] * TILE / 2, h[1] * TILE / 2
    return np.array([c * hx - s * hy, s * hx + c * hy])


def tile_regs(pose, seam=None):
    """Pack per-tile registers: list of 128 dicts in tile order t = j*NX + i."""
    regs = []
    for j in range(NY):
        for i in range(NX):
            dx, dy = (0, 0) if seam is None else seam[j][i]
            regs.append(dict(acx=int(pose['ac'][j, i, 0]), acy=int(pose['ac'][j, i, 1]),
                             arx=int(pose['ar'][j, i, 0]), ary=int(pose['ar'][j, i, 1]),
                             bx=int(pose['b'][j, i, 0]), by=int(pose['b'][j, i, 1]),
                             dx=int(dx), dy=int(dy)))
    return regs


def identity_regs():
    """No warp: every tile shows its rest square (the baseline of DSP-17)."""
    regs = []
    for j in range(NY):
        for i in range(NX):
            regs.append(dict(acx=ONE, acy=0, arx=0, ary=ONE,
                             bx=i * TILE * ONE, by=j * TILE * ONE, dx=0, dy=0))
    return regs


# --------------------------------------------------------- tile setup unit
def tile_setup(r):
    """Seam shift folded into b, and the source window origin (even)."""
    bx = r['bx'] - ((r['dx'] * r['acx'] + r['dy'] * r['arx']) >> SEAM_FB)
    by = r['by'] - ((r['dx'] * r['acy'] + r['dy'] * r['ary']) >> SEAM_FB)
    last = TILE - 1
    xs = [bx, bx + last * r['acx'], bx + last * r['arx'], bx + last * r['acx'] + last * r['arx']]
    ys = [by, by + last * r['acy'], by + last * r['ary'], by + last * r['acy'] + last * r['ary']]
    wx0 = (((min(xs) >> FA) - 1) >> 1) << 1
    wy0 = (((min(ys) >> FA) - 1) >> 1) << 1
    fits = ((max(xs) >> FA) + 1 - wx0 <= WW - 1) and ((max(ys) >> FA) + 1 - wy0 <= WW - 1)
    return bx, by, wx0, wy0, fits


# ------------------------------------------------------------ compositor
def blend(base, col, w):
    """base + round((col-base)*w/256), w in 0..256, per channel int64 arrays."""
    return base + (((col - base) * w + 128) >> 8)


def compose(xs, ys, st):
    """Compose frame pixels at absolute coords (any shape int arrays).

    st: dict with frames (NFRAMES,H,W,3), layer (HL,WL,3), atlas (NATLAS,GH,GW),
        cursor (CUR,CUR,4), and the register dict 'r'.
    """
    r = st['r']
    x = np.clip(xs, 0, W - 1)
    y = np.clip(ys, 0, H - 1)
    inside = (x >= r['rx0']) & (x < r['rx1']) & (y >= r['ry0']) & (y < r['ry1'])
    lx = np.clip(x - r['rx0'] + r['sx'], 0, WL - 1)
    ly = np.clip(y - r['ry0'] + r['sy'], 0, HL - 1)
    base = np.where(inside[..., None], st['layer'][ly, lx],
                    st['frames'][r['frame_sel']][y, x]).astype(np.int64)
    # glyph echo: first valid slot that covers the pixel wins
    a4 = np.zeros(x.shape, dtype=np.int64)
    done = np.zeros(x.shape, dtype=bool)
    for k in range(NGLYPH):
        g = r['glyphs'][k]
        if not g['valid']:
            continue
        gx, gy = x - g['x'], y - g['y']
        hit = (gx >= 0) & (gx < GW) & (gy >= 0) & (gy < GH) & ~done
        a = st['atlas'][g['idx'], np.clip(gy, 0, GH - 1), np.clip(gx, 0, GW - 1)]
        a4 = np.where(hit, a, a4)
        done |= hit
    wg = ((a4 << 4) | a4) + (a4 >> 3)
    out = blend(base, np.array(r['glyph_rgb'], dtype=np.int64), wg[..., None])
    # cursor
    cx, cy = x - r['cx'], y - r['cy']
    hit = (cx >= 0) & (cx < CUR) & (cy >= 0) & (cy < CUR)
    spr = st['cursor'][np.clip(cy, 0, CUR - 1), np.clip(cx, 0, CUR - 1)].astype(np.int64)
    a8 = np.where(hit, spr[..., 3], 0)
    wc = a8 + (a8 >> 7)
    out = blend(out, spr[..., :3], wc[..., None])
    return out


def fill_window(wx0, wy0, st):
    jj, ii = np.mgrid[0:WW, 0:WW]
    return compose(wx0 + ii, wy0 + jj, st)  # (WW, WW, 3)


# ------------------------------------------------------------------ warp
def warp_tile(r, win, wx0, wy0, bx, by):
    v, u = np.mgrid[0:TILE, 0:TILE].astype(np.int64)
    X = bx + u * r['acx'] + v * r['arx']
    Y = by + u * r['acy'] + v * r['ary']
    x0 = np.clip((X >> FA) - wx0, 0, WW - 2)
    y0 = np.clip((Y >> FA) - wy0, 0, WW - 2)
    fx = ((X >> (FA - WB)) & ((1 << WB) - 1))[..., None]
    fy = ((Y >> (FA - WB)) & ((1 << WB) - 1))[..., None]
    one = 1 << WB
    p00, p10 = win[y0, x0], win[y0, x0 + 1]
    p01, p11 = win[y0 + 1, x0], win[y0 + 1, x0 + 1]
    top = p00 * (one - fx) + p10 * fx
    bot = p01 * (one - fx) + p11 * fx
    return (top * (one - fy) + bot * fy + (1 << (2 * WB - 1))) >> (2 * WB)


def render_tile(t, regs, st):
    r = regs[t]
    bx, by, wx0, wy0, fits = tile_setup(r)
    assert fits, f"tile {t}: footprint exceeds the {WW}-px window"
    win = fill_window(wx0, wy0, st)
    return warp_tile(r, win, wx0, wy0, bx, by)


def render_all(regs, st):
    return np.stack([render_tile(t, regs, st) for t in range(NX * NY)])


# --------------------------------------------------------------- scenes
def default_regs():
    return dict(frame_sel=0, rx0=0, rx1=0, ry0=0, ry1=0, sx=0, sy=0,
                cx=-100, cy=-100, glyph_rgb=(255, 255, 255),
                glyphs=[dict(valid=0, x=0, y=0, idx=0) for _ in range(NGLYPH)])


def empty_store():
    return dict(frames=np.zeros((NFRAMES, H, W, 3), dtype=np.uint8),
                layer=np.zeros((HL, WL, 3), dtype=np.uint8),
                atlas=np.zeros((NATLAS, GH, GW), dtype=np.uint8),
                cursor=np.zeros((CUR, CUR, 4), dtype=np.uint8),
                r=default_regs())


RAMP = 4.0  # anti-aliased edge width in source px (wide enough for a clean edge estimate)


def sdf_circles(X, Y, circles):
    d = np.full(np.shape(X), np.inf)
    for (cx, cy, R) in circles:
        d = np.minimum(d, np.hypot(X - cx, Y - cy) - R)
    return d


def sdf_grid(X, Y, pitch=100.0, hw=3.0, x0=0.0, y0=0.0):
    dx = np.abs(((X - x0 + pitch / 2) % pitch) - pitch / 2)
    dy = np.abs(((Y - y0 + pitch / 2) % pitch) - pitch / 2)
    return np.minimum(dx, dy) - hw


CIRCLES = [(800.0, 1600.0, 700.0), (400.0, 400.0, 150.0), (1200.0, 2800.0, 150.0),
           (700.0, 2500.0, 40.0)]  # the last one sits inside one tile, clear of the others
GRID = dict(pitch=100.0, hw=3.0, x0=0.3, y0=0.7)


def sdf_scene(kind, X, Y):
    if kind == 'circle':
        return sdf_circles(X, Y, CIRCLES)
    return sdf_grid(X, Y, **GRID)


def raster(kind):
    Y, X = np.mgrid[0:H, 0:W].astype(np.float64)
    d = sdf_scene(kind, X, Y)
    g = np.clip(0.5 - d / RAMP, 0.0, 1.0)
    v = np.round(g * 255).astype(np.uint8)
    return np.repeat(v[..., None], 3, axis=2)


def compositor_scene(seed=7):
    """A scene that exercises scroll, glyph echo, cursor and frame pick."""
    rng = np.random.default_rng(seed)
    st = empty_store()
    Y, X = np.mgrid[0:H, 0:W]
    for k in range(NFRAMES):
        st['frames'][k, ..., 0] = (X * 255 // (W - 1)).astype(np.uint8)
        st['frames'][k, ..., 1] = (Y * 255 // (H - 1)).astype(np.uint8)
        st['frames'][k, ..., 2] = ((X // 50 + Y // 50 + k) % 2 * 200).astype(np.uint8)
    Yl, Xl = np.mgrid[0:HL, 0:WL]
    st['layer'][..., 0] = ((Xl ^ Yl) & 255).astype(np.uint8)
    st['layer'][..., 1] = ((Yl // 3) & 255).astype(np.uint8)
    st['layer'][..., 2] = (((Xl // 7) * 13) & 255).astype(np.uint8)
    st['atlas'][:] = rng.integers(0, 16, size=st['atlas'].shape, dtype=np.uint8)
    st['cursor'][:] = rng.integers(0, 256, size=st['cursor'].shape, dtype=np.uint8)
    st['cursor'][..., 3][:8, :8] = 255
    st['cursor'][..., 3][-8:, -8:] = 0
    r = st['r']
    r.update(frame_sel=2, rx0=210, rx1=590, ry0=150, ry1=370, sx=1234, sy=4321,
             cx=383, cy=187, glyph_rgb=(250, 40, 90))
    for k in range(NGLYPH):
        r['glyphs'][k] = dict(valid=int(k != 5), x=230 + 14 * k, y=300 + (k % 3) * 9,
                              idx=int(rng.integers(0, NATLAS)))
    return st
