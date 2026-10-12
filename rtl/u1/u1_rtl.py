#!/usr/bin/env python3
"""U1 RTL (Amaranth 0.5): one warp lane of the U1 TCON and compositor.

The lane renders one 200x200 tile per job:
  LOAD    read the tile's registers from the 128-entry parameter file
  SETUP   fold the 1/16-px seam shift into b; find the source window origin
  FILL    stream a 208x208 source window from the frame store through the
          layer compositor (frame pick, scroll, glyph echo, cursor) into a
          2x2 parity-banked window buffer (one bilinear quad per clock)
  WARP    DDA over the tile, bilinear resample, one RGB pixel per clock

The production lane ping-pongs two window buffers so FILL(t+1) overlaps
WARP(t). This RTL runs them in sequence; the datapath is the same.
The golden reference is golden.py; the two must agree bit for bit.
"""
from amaranth import *
from amaranth.lib import data, memory

import golden as G

PARAM = data.StructLayout({
    "acx": signed(G.A_BITS), "acy": signed(G.A_BITS),
    "arx": signed(G.A_BITS), "ary": signed(G.A_BITS),
    "bx": signed(G.B_BITS), "by": signed(G.B_BITS),
    "dx": signed(G.SH_BITS), "dy": signed(G.SH_BITS),
})

CW = 14  # coordinate width (signed), covers -8192..8191


def clamp(v, lo, hi):
    return Mux(v < lo, lo, Mux(v > hi, hi, v))


def ext9(v):
    """Unsigned 8-bit to signed 10-bit."""
    return Cat(v, C(0, 2)).as_signed()


def blend_ch(m, base, col, w, name):
    """base + ((col-base)*w + 128) >> 8, w in 0..256 (unsigned 9)."""
    d = Signal(signed(10), name=f"{name}_d")
    p = Signal(signed(20), name=f"{name}_p")
    o = Signal(8, name=f"{name}_o")
    m.d.comb += [d.eq(ext9(col) - ext9(base)),
                 p.eq(d * Cat(w, C(0, 1)).as_signed()),
                 o.eq(base + ((p + 128) >> 8))]
    return o


class U1Lane(Elaboratable):
    def __init__(self, atlas_init=(), cursor_init=()):
        self.atlas_init = list(atlas_init)
        self.cursor_init = list(cursor_init)
        # ---- per-tile parameter file write port
        self.prm_we = Signal()
        self.prm_waddr = Signal(7)
        self.prm_wdata = Signal(PARAM)
        # ---- compositor registers (latched per tile slot by the sequencer)
        self.frame_sel = Signal(2)
        self.rx0, self.rx1 = Signal(11), Signal(11)
        self.ry0, self.ry1 = Signal(12), Signal(12)
        self.sx, self.sy = Signal(11), Signal(13)
        self.cx, self.cy = Signal(signed(CW)), Signal(signed(CW))
        self.glyph_rgb = Signal(24)
        self.g_valid = Signal(G.NGLYPH)
        self.g_x = [Signal(signed(CW), name=f"g_x{k}") for k in range(G.NGLYPH)]
        self.g_y = [Signal(signed(CW), name=f"g_y{k}") for k in range(G.NGLYPH)]
        self.g_idx = [Signal(6, name=f"g_idx{k}") for k in range(G.NGLYPH)]
        # ---- atlas and cursor sprite write ports
        self.atlas_we = Signal()
        self.atlas_waddr = Signal(15)
        self.atlas_wdata = Signal(4)
        self.cur_we = Signal()
        self.cur_waddr = Signal(10)
        self.cur_wdata = Signal(32)
        # ---- control
        self.start = Signal()
        self.tile = Signal(7)
        self.busy = Signal()
        self.done = Signal()
        self.oob = Signal()
        # ---- frame store read interface (sync, 1-cycle latency)
        self.fs_req = Signal()
        self.fs_layer = Signal()
        self.fs_frame = Signal(2)
        self.fs_x = Signal(11)
        self.fs_y = Signal(13)
        self.fs_data = Signal(24)
        # ---- tile pixel output
        self.o_valid = Signal()
        self.o_u = Signal(8)
        self.o_v = Signal(8)
        self.o_rgb = Signal(24)

    def ports(self):
        p = [self.prm_we, self.prm_waddr, self.prm_wdata.as_value(), self.frame_sel,
             self.rx0, self.rx1, self.ry0, self.ry1, self.sx, self.sy, self.cx, self.cy,
             self.glyph_rgb, self.g_valid, *self.g_x, *self.g_y, *self.g_idx,
             self.atlas_we, self.atlas_waddr, self.atlas_wdata,
             self.cur_we, self.cur_waddr, self.cur_wdata,
             self.start, self.tile, self.busy, self.done, self.oob,
             self.fs_req, self.fs_layer, self.fs_frame, self.fs_x, self.fs_y, self.fs_data,
             self.o_valid, self.o_u, self.o_v, self.o_rgb]
        return p

    def elaborate(self, platform):
        m = Module()
        FA, WB, WW, WH, T = G.FA, G.WB, G.WW, G.WH, G.TILE

        # ================================================== memories
        m.submodules.prm = prm = memory.Memory(shape=PARAM, depth=128, init=[])
        prm_w = prm.write_port()
        prm_r = prm.read_port()
        m.d.comb += [prm_w.en.eq(self.prm_we), prm_w.addr.eq(self.prm_waddr),
                     prm_w.data.eq(self.prm_wdata)]

        m.submodules.atlas = atlas = memory.Memory(
            shape=4, depth=G.NATLAS * G.GH * G.GW, init=self.atlas_init)
        at_w = atlas.write_port()
        at_r = atlas.read_port()
        m.d.comb += [at_w.en.eq(self.atlas_we), at_w.addr.eq(self.atlas_waddr),
                     at_w.data.eq(self.atlas_wdata)]

        m.submodules.cursor = cursor = memory.Memory(
            shape=32, depth=G.CUR * G.CUR, init=self.cursor_init)
        cu_w = cursor.write_port()
        cu_r = cursor.read_port()
        m.d.comb += [cu_w.en.eq(self.cur_we), cu_w.addr.eq(self.cur_waddr),
                     cu_w.data.eq(self.cur_wdata)]

        bank_w, bank_r = {}, {}
        for py in range(2):
            for px in range(2):
                mem = memory.Memory(shape=24, depth=WH * WH, init=[])
                m.submodules[f"bank{px}{py}"] = mem
                bank_w[px, py] = mem.write_port()
                bank_r[px, py] = mem.read_port()

        # ================================================== tile registers
        acx, acy = Signal(signed(G.A_BITS)), Signal(signed(G.A_BITS))
        arx, ary = Signal(signed(G.A_BITS)), Signal(signed(G.A_BITS))
        bx, by = Signal(signed(G.B_BITS)), Signal(signed(G.B_BITS))
        dx, dy = Signal(signed(G.SH_BITS)), Signal(signed(G.SH_BITS))
        wx0, wy0 = Signal(signed(CW)), Signal(signed(CW))

        # seam shift folded into b (SETUP1)
        bx_eff = Signal(signed(G.B_BITS))
        by_eff = Signal(signed(G.B_BITS))
        sh_x = (dx * acx + dy * arx) >> G.SEAM_FB
        sh_y = (dx * acy + dy * ary) >> G.SEAM_FB

        # window origin from the four corners (SETUP2)
        L = T - 1

        def min4(a, b, c, d):
            ab = Mux(a < b, a, b)
            cd = Mux(c < d, c, d)
            return Mux(ab < cd, ab, cd)
        kx = [Signal(signed(G.B_BITS + 2), name=f"kx{n}") for n in range(4)]
        ky = [Signal(signed(G.B_BITS + 2), name=f"ky{n}") for n in range(4)]
        m.d.comb += [kx[0].eq(bx_eff), kx[1].eq(bx_eff + acx * L),
                     kx[2].eq(bx_eff + arx * L), kx[3].eq(bx_eff + acx * L + arx * L),
                     ky[0].eq(by_eff), ky[1].eq(by_eff + acy * L),
                     ky[2].eq(by_eff + ary * L), ky[3].eq(by_eff + acy * L + ary * L)]
        mnx = Signal(signed(G.B_BITS + 2))
        mny = Signal(signed(G.B_BITS + 2))
        m.d.comb += [mnx.eq(min4(*kx)), mny.eq(min4(*ky))]
        tx = Signal(signed(CW + 1))
        ty = Signal(signed(CW + 1))
        m.d.comb += [tx.eq((mnx >> FA) - 1), ty.eq((mny >> FA) - 1)]

        # ================================================== fill pipeline
        fi, fj = Signal(8), Signal(8)          # window counters
        f_go = Signal()                        # issue enable (comb, from FSM)
        # F0 -> registered absolute coords and window index
        f1_v = Signal()
        f1_x, f1_y = Signal(11), Signal(12)
        f1_i, f1_j = Signal(8), Signal(8)
        ax = Signal(signed(CW + 1))
        ay = Signal(signed(CW + 1))
        m.d.comb += [ax.eq(wx0 + fi), ay.eq(wy0 + fj)]
        m.d.sync += [f1_v.eq(f_go),
                     f1_x.eq(clamp(ax, 0, G.W - 1)), f1_y.eq(clamp(ay, 0, G.H - 1)),
                     f1_i.eq(fi), f1_j.eq(fj)]

        # F1: compositor addressing
        sx1 = Signal(signed(CW + 2))
        sy1 = Signal(signed(CW + 2))
        inside = Signal()
        m.d.comb += [
            inside.eq((f1_x >= self.rx0) & (f1_x < self.rx1) &
                      (f1_y >= self.ry0) & (f1_y < self.ry1)),
            sx1.eq(f1_x - self.rx0 + self.sx),
            sy1.eq(f1_y - self.ry0 + self.sy),
            self.fs_req.eq(f1_v),
            self.fs_layer.eq(inside),
            self.fs_frame.eq(self.frame_sel),
            self.fs_x.eq(Mux(inside, clamp(sx1, 0, G.WL - 1), f1_x)),
            self.fs_y.eq(Mux(inside, clamp(sy1, 0, G.HL - 1), f1_y)),
        ]
        # glyph slots, first hit wins
        ghit = Signal()
        gaddr = Signal(15)
        glx = [Signal(signed(CW + 1), name=f"glx{k}") for k in range(G.NGLYPH)]
        gly = [Signal(signed(CW + 1), name=f"gly{k}") for k in range(G.NGLYPH)]
        hits = []
        for k in range(G.NGLYPH):
            m.d.comb += [glx[k].eq(f1_x - self.g_x[k]), gly[k].eq(f1_y - self.g_y[k])]
            hits.append(self.g_valid[k] & (glx[k] >= 0) & (glx[k] < G.GW) &
                        (gly[k] >= 0) & (gly[k] < G.GH))
        for k in range(G.NGLYPH):
            cond = m.If if k == 0 else m.Elif
            with cond(hits[k]):
                m.d.comb += [ghit.eq(1),
                             gaddr.eq(Cat(glx[k][:4], gly[k][:5], self.g_idx[k]))]
        m.d.comb += [at_r.addr.eq(gaddr), at_r.en.eq(1)]
        # cursor
        clx = Signal(signed(CW + 1))
        cly = Signal(signed(CW + 1))
        m.d.comb += [clx.eq(f1_x - self.cx), cly.eq(f1_y - self.cy)]
        chit = (clx >= 0) & (clx < G.CUR) & (cly >= 0) & (cly < G.CUR)
        m.d.comb += [cu_r.addr.eq(Cat(clx[:5], cly[:5])), cu_r.en.eq(1)]

        f2_v, f2_g, f2_c = Signal(), Signal(), Signal()
        f2_i, f2_j = Signal(8), Signal(8)
        m.d.sync += [f2_v.eq(f1_v), f2_g.eq(ghit), f2_c.eq(chit),
                     f2_i.eq(f1_i), f2_j.eq(f1_j)]

        # F2: blend glyph then cursor
        a4 = Signal(4)
        m.d.comb += a4.eq(Mux(f2_g, at_r.data, 0))
        wg = Signal(9)
        m.d.comb += wg.eq(Cat(a4, a4) + (a4 >> 3))
        spr = cu_r.data
        a8 = Signal(8)
        m.d.comb += a8.eq(Mux(f2_c, spr[24:32], 0))
        wc = Signal(9)
        m.d.comb += wc.eq(a8 + (a8 >> 7))
        comp = []
        for ch in range(3):
            base = self.fs_data[8 * ch:8 * ch + 8]
            g1 = blend_ch(m, base, self.glyph_rgb[8 * ch:8 * ch + 8], wg, f"g{ch}")
            c1 = blend_ch(m, g1, spr[8 * ch:8 * ch + 8], wc, f"c{ch}")
            comp.append(c1)
        f3_v = Signal()
        f3_i, f3_j = Signal(8), Signal(8)
        f3_px = Signal(24)
        m.d.sync += [f3_v.eq(f2_v), f3_i.eq(f2_i), f3_j.eq(f2_j), f3_px.eq(Cat(*comp))]
        # F3: write the parity bank
        f3_addr = Signal(14)
        m.d.comb += f3_addr.eq((f3_j >> 1) * WH + (f3_i >> 1))
        for (px, py), wp in bank_w.items():
            m.d.comb += [wp.en.eq(f3_v & (f3_i[0] == px) & (f3_j[0] == py)),
                         wp.addr.eq(f3_addr), wp.data.eq(f3_px)]

        # ================================================== warp pipeline
        accx, accy = Signal(signed(G.B_BITS)), Signal(signed(G.B_BITS))
        rowx, rowy = Signal(signed(G.B_BITS)), Signal(signed(G.B_BITS))
        wu, wv = Signal(8), Signal(8)
        w_go = Signal()
        ix = Signal(signed(CW + 2))
        iy = Signal(signed(CW + 2))
        m.d.comb += [ix.eq((accx >> FA) - wx0), iy.eq((accy >> FA) - wy0)]
        x0 = Signal(8)
        y0 = Signal(8)
        m.d.comb += [x0.eq(clamp(ix, 0, WW - 2)), y0.eq(clamp(iy, 0, WW - 2))]
        with m.If(w_go & ((ix < 0) | (ix > WW - 2) | (iy < 0) | (iy > WW - 2))):
            m.d.sync += self.oob.eq(1)
        for (px, py), rp in bank_r.items():
            xi = (x0 + (x0[0] ^ px)) >> 1
            yi = (y0 + (y0[0] ^ py)) >> 1
            m.d.comb += [rp.addr.eq(yi * WH + xi), rp.en.eq(1)]
        w1_v = Signal()
        w1_u, w1_v_ = Signal(8), Signal(8)
        w1_xp, w1_yp = Signal(), Signal()
        w1_fx, w1_fy = Signal(WB), Signal(WB)
        m.d.sync += [w1_v.eq(w_go), w1_u.eq(wu), w1_v_.eq(wv),
                     w1_xp.eq(x0[0]), w1_yp.eq(y0[0]),
                     w1_fx.eq(accx[FA - WB:FA]), w1_fy.eq(accy[FA - WB:FA])]
        # W1: route banks to taps, horizontal lerp
        one = 1 << WB

        def tap(xo, yo):
            sel = Signal(24, name=f"tap{xo}{yo}")
            cases = []
            for (px, py), rp in bank_r.items():
                cases.append(((px, py), rp.data))
            with m.Switch(Cat(w1_xp ^ xo, w1_yp ^ yo)):
                for (px, py), dat in cases:
                    with m.Case(px | (py << 1)):
                        m.d.comb += sel.eq(dat)
            return sel
        p00, p10, p01, p11 = tap(0, 0), tap(1, 0), tap(0, 1), tap(1, 1)
        w2_v = Signal()
        w2_u, w2_vv = Signal(8), Signal(8)
        w2_fy = Signal(WB)
        top = [Signal(14, name=f"top{c}") for c in range(3)]
        bot = [Signal(14, name=f"bot{c}") for c in range(3)]
        fxc = Signal(WB + 1)
        m.d.comb += fxc.eq(one - w1_fx)
        for c in range(3):
            s = slice(8 * c, 8 * c + 8)
            m.d.sync += [top[c].eq(p00[s] * fxc + p10[s] * w1_fx),
                         bot[c].eq(p01[s] * fxc + p11[s] * w1_fx)]
        m.d.sync += [w2_v.eq(w1_v), w2_u.eq(w1_u), w2_vv.eq(w1_v_), w2_fy.eq(w1_fy)]
        # W2: vertical lerp and round
        fyc = Signal(WB + 1)
        m.d.comb += fyc.eq(one - w2_fy)
        outs = [((top[c] * fyc + bot[c] * w2_fy + (1 << (2 * WB - 1))) >> (2 * WB))[:8]
                for c in range(3)]
        m.d.sync += [self.o_valid.eq(w2_v), self.o_u.eq(w2_u), self.o_v.eq(w2_vv),
                     self.o_rgb.eq(Cat(*outs))]

        # ================================================== sequencer
        drain = Signal(3)
        m.d.comb += [prm_r.en.eq(1), prm_r.addr.eq(self.tile)]
        m.d.sync += self.done.eq(0)
        with m.FSM():
            with m.State("IDLE"):
                with m.If(self.start):
                    m.d.sync += [self.busy.eq(1), self.oob.eq(0)]
                    m.next = "LOAD"
            with m.State("LOAD"):
                d = prm_r.data
                m.d.sync += [acx.eq(d.acx), acy.eq(d.acy), arx.eq(d.arx), ary.eq(d.ary),
                             bx.eq(d.bx), by.eq(d.by), dx.eq(d.dx), dy.eq(d.dy)]
                m.next = "SETUP1"
            with m.State("SETUP1"):
                m.d.sync += [bx_eff.eq(bx - sh_x), by_eff.eq(by - sh_y)]
                m.next = "SETUP2"
            with m.State("SETUP2"):
                m.d.sync += [wx0.eq((tx >> 1) << 1), wy0.eq((ty >> 1) << 1),
                             fi.eq(0), fj.eq(0)]
                m.next = "FILL"
            with m.State("FILL"):
                m.d.comb += f_go.eq(1)
                with m.If(fi == WW - 1):
                    m.d.sync += [fi.eq(0), fj.eq(fj + 1)]
                    with m.If(fj == WW - 1):
                        m.d.sync += drain.eq(4)
                        m.next = "FDRAIN"
                with m.Else():
                    m.d.sync += fi.eq(fi + 1)
            with m.State("FDRAIN"):
                m.d.sync += drain.eq(drain - 1)
                with m.If(drain == 1):
                    m.d.sync += [accx.eq(bx_eff), accy.eq(by_eff),
                                 rowx.eq(bx_eff), rowy.eq(by_eff), wu.eq(0), wv.eq(0)]
                    m.next = "WARP"
            with m.State("WARP"):
                m.d.comb += w_go.eq(1)
                with m.If(wu == T - 1):
                    m.d.sync += [wu.eq(0), wv.eq(wv + 1),
                                 rowx.eq(rowx + arx), rowy.eq(rowy + ary),
                                 accx.eq(rowx + arx), accy.eq(rowy + ary)]
                    with m.If(wv == T - 1):
                        m.d.sync += drain.eq(4)
                        m.next = "WDRAIN"
                with m.Else():
                    m.d.sync += [wu.eq(wu + 1), accx.eq(accx + acx), accy.eq(accy + acy)]
            with m.State("WDRAIN"):
                m.d.sync += drain.eq(drain - 1)
                with m.If(drain == 1):
                    m.d.sync += [self.busy.eq(0), self.done.eq(1)]
                    m.next = "IDLE"
        return m
