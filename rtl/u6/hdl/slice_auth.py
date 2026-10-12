"""U6 inline slice authentication checker. Amaranth 0.5.

One Keccak-f[1600] core, one round per clock, does two jobs per slice:
  1. d   = SHA3-256(sid || canon(header) || payload)   (rate 136 B, keyless)
  2. tag = KMAC128(K, d, 128, "BLF-SLICE-v1")          (one block from a
     prefix state that U7 computed and loaded; rate 168 B)
Then a constant-time 128-bit compare, and a strict seq > last_seq check.

The wire slice is 64-bit words, little-endian:
  w0 = version[15:0] | flags[31:16] | slice_index[63:32]
  w1 = seq    w2 = frame_no    w3 = payload_len[31:0] | y0[47:32] | layer[63:48]
  w4 .. w3+m = payload, zero padded, m = ceil(payload_len / 8)
  w4+m, w5+m = the 128-bit tag
The checker never forwards bytes; the ingress buffer holds the slice and
releases it to the decoder only on res_valid with res_err == OK.
"""
from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
       [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]

OK, BAD_TAG, REPLAY, NO_KEY, LENGTH, BAD_VERSION = range(6)
MAX_PAYLOAD = 65536
VERSION = 1
SLOT_BIT = 16          # flags bit 0 sits at bit 16 of w0


def keccak_round(a, rc):
    """Combinational Keccak round on 25 lane Values, a[x + 5*y]."""
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ c[(x + 1) % 5].rotate_left(1) for x in range(5)]
    t = [a[i] ^ d[i % 5] for i in range(25)]
    b = [None] * 25
    for x in range(5):
        for y in range(5):
            b[y + 5 * ((2 * x + 3 * y) % 5)] = t[x + 5 * y].rotate_left(ROT[x][y])
    out = [None] * 25
    for x in range(5):
        for y in range(5):
            out[x + 5 * y] = b[x + 5 * y] ^ (~b[(x + 1) % 5 + 5 * y] & b[(x + 2) % 5 + 5 * y])
    out[0] = out[0] ^ rc
    return out


class SliceAuth(wiring.Component):
    # configuration port, written only by U7 over its private bus
    cfg_we: In(1)
    cfg_addr: In(6)       # [5] slot; [4:0] 0..24 prefix lane, 25 sid_lo, 26 sid_hi,
    cfg_data: In(64)      # 27 slot valid (data[0]), 28 session reset (last_seq := 0)
    # the slice word stream from the ingress parser
    in_data: In(64)
    in_valid: In(1)
    in_last: In(1)
    in_ready: Out(1)
    # one verdict per slice
    res_valid: Out(1)
    res_err: Out(3)
    res_digest: Out(256)
    res_seq: Out(64)
    res_frame: Out(64)
    res_flags: Out(16)
    res_slice: Out(32)
    busy: Out(1)

    def elaborate(self, platform):
        m = Module()

        st = [Signal(64, name=f"st{i}") for i in range(25)]
        pre = [[Signal(64, name=f"pre{s}_{i}") for i in range(25)] for s in range(2)]
        kvalid = Signal(2)
        sid = [Signal(64, name="sid_lo"), Signal(64, name="sid_hi")]
        last_seq = Signal(64)

        widx = Signal(15)          # word index in the wire slice
        lane = Signal(5)           # absorb lane, 0..16
        rnd = Signal(5)
        ret = Signal(2)            # where a permutation returns to
        R_ABSORB, R_PADBLK, R_KMAC, R_TAG = range(4)
        mreg = Signal(14)
        err_len = Signal()
        version = Signal(16)
        flags = Signal(16)
        sidx = Signal(32)
        seq = Signal(64)
        frame = Signal(64)
        digest = Signal(256)
        tag = Signal(128)
        tagw = Signal()            # which tag word comes next

        # ---- configuration ---------------------------------------------------
        cslot = self.cfg_addr[5]
        caddr = self.cfg_addr[0:5]
        with m.If(self.cfg_we):
            for s in range(2):
                for i in range(25):
                    with m.If((cslot == s) & (caddr == i)):
                        m.d.sync += pre[s][i].eq(self.cfg_data)
                with m.If((cslot == s) & (caddr == 27)):
                    m.d.sync += kvalid[s].eq(self.cfg_data[0])
            with m.If(caddr == 25):
                m.d.sync += sid[0].eq(self.cfg_data)
            with m.If(caddr == 26):
                m.d.sync += sid[1].eq(self.cfg_data)
            with m.If(caddr == 28):
                m.d.sync += last_seq.eq(0)

        # ---- the round function ------------------------------------------------
        rc = Array([C(v, 64) for v in RC])[rnd]
        rnext = keccak_round(st, rc)

        def init_state():
            # lanes 0 and 1 take the sid when the first word arrives
            stmts = [st[i].eq(0) for i in range(25)]
            stmts += [lane.eq(2), widx.eq(0),
                      err_len.eq(0), tagw.eq(0)]
            return stmts

        m.d.sync += self.res_valid.eq(0)
        w = self.in_data
        plen = w[0:32]
        m_now = Mux(widx == 3, (plen + 7) >> 3, mreg)

        with m.FSM(init="BOOT"):
            with m.State("BOOT"):
                m.d.sync += init_state()
                m.next = "ABSORB"

            with m.State("ABSORB"):
                m.d.comb += self.in_ready.eq(1)
                with m.If(self.in_valid):
                    m.d.sync += widx.eq(widx + 1)
                    wh = Mux(widx == 0, w & ~C(1 << SLOT_BIT, 64), w)
                    with m.Switch(widx):
                        with m.Case(0):
                            m.d.sync += [version.eq(w[0:16]), flags.eq(w[16:32]), sidx.eq(w[32:64])]
                        with m.Case(1):
                            m.d.sync += seq.eq(w)
                        with m.Case(2):
                            m.d.sync += frame.eq(w)
                        with m.Case(3):
                            m.d.sync += mreg.eq((plen + 7) >> 3)
                    too_big = (widx == 3) & (plen > MAX_PAYLOAD)
                    end_hash = (widx >= 3) & (widx == 3 + m_now)
                    with m.If(self.in_last):
                        # a last word inside the hashed part is always early
                        m.d.sync += err_len.eq(1)
                        m.next = "REPORT"
                    with m.Elif(too_big):
                        m.d.sync += err_len.eq(1)
                        m.next = "DRAIN"
                    with m.Else():
                        for i in range(25):
                            x = Mux(widx == 0, sid[i], st[i]) if i < 2 else st[i]
                            if i < 17:
                                x = x ^ Mux(lane == i, wh, 0)
                            if 1 <= i < 17:
                                x = x ^ Mux(end_hash & (lane + 1 == i), C(0x06, 64), 0)
                            if i == 16:
                                x = x ^ Mux(end_hash & (lane < 16), C(0x80 << 56, 64), 0)
                            m.d.sync += st[i].eq(x)
                        with m.If(lane == 16):
                            m.d.sync += [lane.eq(0), rnd.eq(0),
                                         ret.eq(Mux(end_hash, R_PADBLK, R_ABSORB))]
                            m.next = "PERM"
                        with m.Else():
                            m.d.sync += lane.eq(lane + 1)
                            with m.If(end_hash):
                                m.d.sync += [rnd.eq(0), ret.eq(R_KMAC)]
                                m.next = "PERM"

            with m.State("PERM"):
                m.d.sync += [st[i].eq(rnext[i]) for i in range(25)]
                m.d.sync += rnd.eq(rnd + 1)
                with m.If(rnd == 23):
                    with m.Switch(ret):
                        with m.Case(R_ABSORB):
                            m.next = "ABSORB"
                        with m.Case(R_PADBLK):
                            m.next = "PADBLK"
                        with m.Case(R_KMAC):
                            m.next = "KMAC"
                        with m.Case(R_TAG):
                            m.next = "TAGRX"

            with m.State("PADBLK"):
                m.d.sync += [st[0].eq(st[0] ^ 0x06), st[16].eq(st[16] ^ (0x80 << 56)),
                             rnd.eq(0), ret.eq(R_KMAC)]
                m.next = "PERM"

            with m.State("KMAC"):
                # digest = lanes 0..3; load the slot's prefix and XOR the one block
                slot = flags[0]
                m.d.sync += digest.eq(Cat(st[0], st[1], st[2], st[3]))
                for i in range(25):
                    p = Mux(slot, pre[1][i], pre[0][i])
                    if i < 4:
                        p = p ^ st[i]
                    if i == 4:
                        p = p ^ C(0x040180, 64)     # right_encode(128) = 80 01, pad 04
                    if i == 20:
                        p = p ^ C(0x80 << 56, 64)   # byte 167 of the 168-byte rate
                    m.d.sync += st[i].eq(p)
                m.d.sync += [rnd.eq(0), ret.eq(R_TAG)]
                m.next = "PERM"

            with m.State("TAGRX"):
                m.d.comb += self.in_ready.eq(1)
                with m.If(self.in_valid):
                    m.d.sync += tagw.eq(1)
                    with m.If(~tagw):
                        m.d.sync += tag[0:64].eq(w ^ st[0])
                        with m.If(self.in_last):
                            m.d.sync += err_len.eq(1)
                            m.next = "REPORT"
                    with m.Else():
                        m.d.sync += tag[64:128].eq(w ^ st[1])
                        with m.If(self.in_last):
                            m.next = "REPORT"
                        with m.Else():
                            m.d.sync += err_len.eq(1)
                            m.next = "DRAIN"

            with m.State("DRAIN"):
                m.d.comb += self.in_ready.eq(1)
                with m.If(self.in_valid & self.in_last):
                    m.next = "REPORT"

            with m.State("REPORT"):
                slot = flags[0]
                key_ok = Mux(slot, kvalid[1], kvalid[0])
                tag_ok = tag == 0                      # XOR-accumulated: no early exit
                fresh = seq > last_seq
                err = Signal(3)
                with m.If(err_len):
                    m.d.comb += err.eq(LENGTH)
                with m.Elif(version != VERSION):
                    m.d.comb += err.eq(BAD_VERSION)
                with m.Elif(~key_ok):
                    m.d.comb += err.eq(NO_KEY)
                with m.Elif(~tag_ok):
                    m.d.comb += err.eq(BAD_TAG)
                with m.Elif(~fresh):
                    m.d.comb += err.eq(REPLAY)
                with m.Else():
                    m.d.comb += err.eq(OK)
                with m.If(err == OK):
                    m.d.sync += last_seq.eq(seq)
                m.d.sync += [self.res_valid.eq(1), self.res_err.eq(err),
                             self.res_digest.eq(digest), self.res_seq.eq(seq),
                             self.res_frame.eq(frame), self.res_flags.eq(flags),
                             self.res_slice.eq(sidx)]
                m.d.sync += init_state()
                m.next = "ABSORB"

        m.d.comb += self.busy.eq(widx != 0)
        return m
