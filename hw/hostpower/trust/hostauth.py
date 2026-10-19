#!/usr/bin/env python3
"""hostauth.py - the trust model of host power for the Budlum Leaf.

TRUST team of hw/hostpower, revision L.6.1 (proposed). The executable model
behind 01-THREAT-MODEL.md, 02-DESIGN-RULES.md and 03-GATE-MAP.md.

The thesis condition 3 of BRIEF Section 5: a host that feeds the Leaf never
gains authority over it. This file models:

  1. the classes of host power and the policy table (who gets which class)
  2. the HostRecord, its bounded parser and its authentication by U7 with
     ed25519 strict verification (the primitive of fw/u7 session.rs)
  3. the atomic commit of counters, signatures and updates across a power loss
  4. the island rail: a bridge capacitor, a brownout detector and a glitch
     simulation of the rail that U7 lives on
  5. the sizing of the island store and the leakage of the host line

Everything physical is [HYPOTHESIS] until the bench measures it. The wallet
key of the real U7 is ML-DSA-87; this model signs with ed25519 as a stand-in,
because the model proves the control flow, not the lattice maths.

Run: python3 hostauth.py        the policy table and the key numbers
     python3 -m unittest discover -s tests
"""
import functools
import hashlib
import json
import math
import os
import struct
import sys
from dataclasses import dataclass, field

# ===================================================== ed25519, RFC 8032 ===
# A reference implementation for the model. verify_strict follows the rule of
# ed25519-dalek verify_strict (fw/u7 session.rs): S below the group order,
# canonical point encodings, and no small-order key or nonce point.
_P = 2 ** 255 - 19
_Q = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_SQRT_M1 = pow(2, (_P - 1) // 4, _P)


def _inv(x):
    return pow(x, _P - 2, _P)


def _add(a, b):
    aa = (a[1] - a[0]) * (b[1] - b[0]) % _P
    bb = (a[1] + a[0]) * (b[1] + b[0]) % _P
    cc = 2 * a[3] * b[3] * _D % _P
    dd = 2 * a[2] * b[2] % _P
    e, f, g, h = bb - aa, dd - cc, dd + cc, bb + aa
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _mul(s, pt):
    r = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            r = _add(r, pt)
        pt = _add(pt, pt)
        s >>= 1
    return r


def _eq(a, b):
    return ((a[0] * b[2] - b[0] * a[2]) % _P == 0 and
            (a[1] * b[2] - b[1] * a[2]) % _P == 0)


def _recover_x(y, sign):
    if y >= _P:
        return None
    x2 = (y * y - 1) * _inv(_D * y * y + 1) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P != 0:
        x = x * _SQRT_M1 % _P
    if (x * x - x2) % _P != 0:
        return None
    if (x & 1) != sign:
        x = _P - x
    return x


_GY = 4 * _inv(5) % _P
_GX = _recover_x(_GY, 0)
_G = (_GX, _GY, 1, _GX * _GY % _P)
_ID = (0, 1, 1, 0)


def _compress(pt):
    zi = _inv(pt[2])
    x, y = pt[0] * zi % _P, pt[1] * zi % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _decompress(s):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _P)


def _h512(b):
    return hashlib.sha512(b).digest()


def _expand(secret):
    h = _h512(secret)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def ed_public(secret):
    return _compress(_mul(_expand(secret)[0], _G))


def ed_sign(secret, msg):
    a, prefix = _expand(secret)
    pub = _compress(_mul(a, _G))
    r = int.from_bytes(_h512(prefix + msg), "little") % _Q
    rs = _compress(_mul(r, _G))
    h = int.from_bytes(_h512(rs + pub + msg), "little") % _Q
    return rs + int.to_bytes((r + h * a) % _Q, 32, "little")


def _small_order(pt):
    return _eq(_mul(8, pt), _ID)


@functools.lru_cache(maxsize=4096)
def ed_verify_strict(pub, msg, sig):
    if len(pub) != 32 or len(sig) != 64:
        return False
    a_pt = _decompress(pub)
    r_pt = _decompress(sig[:32])
    if a_pt is None or r_pt is None:
        return False
    s = int.from_bytes(sig[32:], "little")
    if s >= _Q or _small_order(a_pt) or _small_order(r_pt):
        return False
    h = int.from_bytes(_h512(sig[:32] + pub + msg), "little") % _Q
    return _eq(_mul(s, _G), _add(r_pt, _mul(h, a_pt)))


# ============================================ the classes and the policy ===
# Class: (name, v_min mV, v_max mV, max power mW). [HYPOTHESIS] window values.
# P1 is the power-only low class of an unauthenticated host. 0.5 W covers the
# islanded ring of hw/energy/03 Section 1.2 item 5 (0.40 W).
CLASSES = {
    0: ("P0", 0, 0, 0),
    1: ("P1", 4750, 5500, 500),
    2: ("P2", 8100, 9900, 15000),
    3: ("P3", 13500, 16500, 27000),
}
LEAF_RATING_A = 1.5          # per leaf, hw/energy/03 Section 2, MON-16
VHV_LEAVES = 2               # leaves 5 and 8
HOST_ABS_MAX_MV = 24000      # the Leaf-side S_SEAT survives this, [HYPOTHESIS]
BINDING_TOL = 0.05           # host-reported against locally measured volts
REAUTH_S = 30.0              # a grant dies after this without a fresh record
MAX_ANCHOR_AGE_S = 6 * 3600  # an older anchor is a stale clock, [HYPOTHESIS]
FAULT_LIMIT = 3              # detected faults per attachment before lockout

KIND_HOST, KIND_VOUCH = 0, 1     # a host signs for itself; an adapter vouches
ROLE_NONE, ROLE_VALIDATOR = 0, 1

TAG_HOST = b"BDLM_LEAF_HOST_RECORD_V1"   # a sixth tag, joins U7-3

_REC = ">BQ32sBBIHHBBQQ32sHH"
REC_LEN = struct.calcsize(_REC)
FRAME_LEN = REC_LEN + 64


class ParseError(ValueError):
    pass


@dataclass(frozen=True)
class HostRecord:
    chain_id: int
    host_key: bytes
    kind: int
    cls: int
    max_power_mw: int
    v_min_mv: int
    v_max_mv: int
    role: int
    lanes: int
    expiry: int            # anchor height, the chain clock of the light client
    counter: int
    nonce: bytes
    meas_mv: int           # what the host says it measures at its output
    meas_ma: int
    version: int = 1

    def pack(self):
        return struct.pack(_REC, self.version, self.chain_id, self.host_key,
                           self.kind, self.cls, self.max_power_mw,
                           self.v_min_mv, self.v_max_mv, self.role, self.lanes,
                           self.expiry, self.counter, self.nonce,
                           self.meas_mv, self.meas_ma)

    def signing_bytes(self):
        return TAG_HOST + self.pack()


def parse_frame(frame):
    """The bounded parser. Fixed length, no allocation by input, no loops.
    Returns (HostRecord, signature) or raises ParseError."""
    if not isinstance(frame, (bytes, bytearray)) or len(frame) != FRAME_LEN:
        raise ParseError("length")
    f = struct.unpack(_REC, bytes(frame[:REC_LEN]))
    (ver, chain, key, kind, cls, pw, vmin, vmax, role, lanes, exp, ctr,
     nonce, mv, ma) = f
    if ver != 1:
        raise ParseError("version")
    if kind not in (KIND_HOST, KIND_VOUCH) or role not in (0, 1) or lanes not in (0, 1):
        raise ParseError("enum")
    if cls not in (1, 2, 3):
        raise ParseError("class")
    if vmin > vmax:
        raise ParseError("window")
    return (HostRecord(chain, key, kind, cls, pw, vmin, vmax, role, lanes, exp,
                       ctr, nonce, mv, ma, ver), bytes(frame[REC_LEN:]))


def sign_record(secret, rec):
    return rec.pack() + ed_sign(secret, rec.signing_bytes())


def record_inside_class(rec):
    """The record must claim a window and a power inside its class row."""
    _, vmin, vmax, pw = CLASSES[rec.cls]
    return (rec.v_min_mv >= vmin and rec.v_max_mv <= vmax and
            0 < rec.max_power_mw <= pw)


def leaf_current_ok(cls):
    """The class row never loads a VHV leaf above its rating at the low edge."""
    _, vmin, _, pw = CLASSES[cls]
    if cls == 0:
        return True
    amps = pw / vmin               # mW / mV = A
    return amps / VHV_LEAVES <= LEAF_RATING_A


# =================================================== the persistent store ===
class PowerLoss(Exception):
    pass


class NVM:
    """Two slots, a sequence number and a checksum. The checksum is the commit
    point. A torn write fails the checksum, so the older slot still reads.
    cut_at: the step at which power ends. Steps: 0 erase, 1 write half,
    2 write the rest and the checksum. [HYPOTHESIS] single-word atomic write."""

    def __init__(self):
        self.slots = [None, None]
        self.steps = 0

    @staticmethod
    def _crc(seq, data):
        return hashlib.sha256(struct.pack(">Q", seq) + data).digest()[:8]

    def _valid(self, s):
        return s is not None and s[2] == self._crc(s[0], s[1])

    def read(self):
        good = [s for s in self.slots if self._valid(s)]
        if not good:
            return None
        return json.loads(max(good, key=lambda s: s[0])[1].decode())

    def seq(self):
        good = [s[0] for s in self.slots if self._valid(s)]
        return max(good) if good else 0

    def commit(self, obj, cut_at=None):
        data = json.dumps(obj, sort_keys=True).encode()
        seq = self.seq() + 1
        v0, v1 = self._valid(self.slots[0]), self._valid(self.slots[1])
        if v0 and v1:
            target = 0 if self.slots[0][0] < self.slots[1][0] else 1   # the older
        elif v0:
            target = 1
        else:
            target = 0
        if cut_at == 0:
            raise PowerLoss("before erase")
        self.slots[target] = None                       # step 0, erase
        if cut_at == 1:
            raise PowerLoss("after erase")
        half = len(data) // 2
        self.slots[target] = (seq, data[:half], b"torn")   # step 1, torn
        if cut_at == 2:
            raise PowerLoss("torn write")
        self.slots[target] = (seq, data, self._crc(seq, data))  # step 2
        if cut_at == 3:
            raise PowerLoss("after commit")


NVM_COMMIT_STEPS = 4      # cut points 0 to 3 of NVM.commit


def _fresh_state():
    return {"trust": {}, "ctr": {}, "faults": 0, "floor": 0, "lastsign": 0}


# ===================================================== the secure element ===
@dataclass(frozen=True)
class Grant:
    cls: int
    row: str
    reason: str
    lanes: bool = False
    role_claim_ok: bool = False
    deadline_s: float = 0.0

    @property
    def name(self):
        return CLASSES[self.cls][0]

    @property
    def v_window_mv(self):
        return CLASSES[self.cls][1:3]

    @property
    def max_power_mw(self):
        return CLASSES[self.cls][3]


# the policy table, row id -> (class rule, lanes, render rule)
POLICY_ROWS = {
    "R1": "no attach, or the adapter fails ENR-19: P0, lanes dead, no render from the host",
    "R2": "adapter passes, host unknown or any check fails: P1, lanes dead",
    "R3": "adapter vouch for a dumb source: at most P2, lanes dead",
    "R4": "host record valid, key paired by the owner: its class, at most the ceiling",
    "R5": "any row with role validator: same class, render only after SW-22 and admission",
    "R6": "a fresh check fails later: the grant falls to R2 within the deadline",
}


class U7:
    """The part of U7 that judges a host. State in NVM survives a power cycle.
    ram_counters=True models the hole: counters kept in RAM only."""

    def __init__(self, nvm=None, rng=os.urandom, chain_id=1, anchor_height=1000,
                 active_validators=(), ram_counters=False):
        self.nvm = nvm if nvm is not None else NVM()
        if self.nvm.read() is None:
            self.nvm.commit(_fresh_state())
        self.rng = rng
        self.chain_id = chain_id
        self.anchor_height = anchor_height
        self.active = set(active_validators)
        self.ram_counters = ram_counters
        self.power_cycle()

    # ------------------------------------------------------------ RAM ---
    def power_cycle(self):
        """A host that cuts power resets everything in RAM."""
        self._pending = None
        self.grant = Grant(0, "R1", "powered down")
        self.uptime_s = 0.0
        self.anchor_seen_s = 0.0
        self.attach_faults = 0
        self._ram_ctr = {}
        self._host_v = 0

    @property
    def state(self):
        return self.nvm.read()

    def _ctr_get(self, hk):
        if self.ram_counters:
            return self._ram_ctr.get(hk, 0)
        return self.state["ctr"].get(hk, 0)

    def _ctr_put(self, hk, v, cut_at=None):
        if self.ram_counters:
            self._ram_ctr[hk] = v
            return
        s = self.state
        s["ctr"][hk] = v
        self.nvm.commit(s, cut_at)

    # ------------------------------------------------ owner pairing ---
    def pair(self, key, ceiling, lanes_ok=False, presence=False, origin="OWNER",
             cut_at=None):
        """Add a host key to the trust store. Needs the owner's physical press."""
        if not presence:
            raise PermissionError("pairing needs the owner's button press")
        if ceiling not in (1, 2, 3):
            raise ValueError("ceiling")
        s = self.state
        s["trust"][key.hex()] = [ceiling, bool(lanes_ok), origin]
        self.nvm.commit(s, cut_at)

    def unpair(self, key, presence=False):
        if not presence:
            raise PermissionError("unpairing needs the owner's button press")
        s = self.state
        s["trust"].pop(key.hex(), None)
        self.nvm.commit(s)

    # ---------------------------------------------------- the anchor ---
    def advance_anchor(self, height):
        if height > self.anchor_height:
            self.anchor_height = height
        self.anchor_seen_s = self.uptime_s

    def anchor_fresh(self):
        return (self.uptime_s - self.anchor_seen_s) <= MAX_ANCHOR_AGE_S

    def tick(self, seconds):
        """Time passes. A grant that is not renewed falls to the base class."""
        self.uptime_s += seconds
        if self.grant.cls > 1 and self.uptime_s > self.grant.deadline_s:
            self.grant = Grant(self._base_cls(), "R6", "re-authentication missed")
        return self.grant

    # -------------------------------------------------- the handshake ---
    def _base_cls(self):
        lo, hi = CLASSES[1][1:3]
        return 1 if (self._adapter_ok and lo <= self._host_v <= hi) else 0

    def attach(self, adapter_ok, host_mv):
        """ENR-19 has run. adapter_ok: the adapter passed its pad handshake.
        host_mv: the volts the Leaf measures at the pad."""
        self._adapter_ok = adapter_ok
        self._host_v = host_mv
        self.attach_faults = 0
        if not adapter_ok:
            self.grant = Grant(0, "R1", "adapter refused: pads stay at 0 V")
        else:
            self.grant = Grant(self._base_cls(), "R2", "unauthenticated host",
                               deadline_s=self.uptime_s)
        return self.grant

    def challenge(self):
        """A fresh single-use nonce. Nothing else leaves U7 before the host
        proves itself: no wallet address, no version, no session id."""
        nonce = self.rng(32)
        self._pending = nonce
        return nonce

    def _fail(self, reason):
        self.grant = Grant(self._base_cls(), "R2", reason, deadline_s=self.uptime_s)
        return self.grant

    def respond(self, frame, local_mv=None, cut_at=None):
        """Judge a host answer. Every failure falls to the base class."""
        pending, self._pending = self._pending, None     # single use, always
        if local_mv is None:
            local_mv = self._host_v
        if not self._adapter_ok:
            return self._fail("adapter refused")
        if pending is None:
            return self._fail("no open challenge")
        try:
            rec, sig = parse_frame(frame)
        except ParseError as e:
            return self._fail(f"parse: {e}")
        if rec.nonce != pending:
            return self._fail("nonce mismatch")
        if rec.chain_id != self.chain_id:
            return self._fail("wrong chain")
        if not ed_verify_strict(rec.host_key, rec.signing_bytes(), sig):
            return self._fail("bad signature")
        entry = self.state["trust"].get(rec.host_key.hex())
        if entry is None:
            return self._fail("unknown host key")
        ceiling, lanes_ok, _origin = entry
        if rec.counter <= self._ctr_get(rec.host_key.hex()):
            return self._fail("replayed counter")
        if rec.expiry <= self.anchor_height or not self.anchor_fresh():
            return self._fail("expired or stale clock")
        if rec.cls > ceiling:
            return self._fail("over-class request")
        if not record_inside_class(rec):
            return self._fail("record outside its class row")
        if rec.kind == KIND_VOUCH and rec.cls > 2:
            return self._fail("a vouch never exceeds P2")
        if abs(rec.meas_mv - local_mv) > BINDING_TOL * max(local_mv, 1):
            return self._fail("power channel binding mismatch")
        if self._base_cls() != 1:
            return self._fail("pad volts outside the handshake window")
        # the handshake runs at P1 volts; the class window binds after the
        # grant, when the sink asks for the contract (see bridge_state)
        # burn the counter before the grant takes effect
        self._ctr_put(rec.host_key.hex(), rec.counter, cut_at)
        role_ok = rec.role == ROLE_VALIDATOR and rec.host_key in self.active
        lanes = bool(rec.lanes and lanes_ok and rec.kind == KIND_HOST and rec.cls >= 2)
        row = "R3" if rec.kind == KIND_VOUCH else "R4"
        if role_ok:
            row = "R5"
        self.grant = Grant(rec.cls, row, "record accepted", lanes, role_ok,
                           self.uptime_s + REAUTH_S)
        return self.grant

    # -------------------------------------------------- the render ---
    def render(self, stream_key):
        """What the display path shows. Independent of the power class. SW-22,
        plus the stale clock rule. A role claim never opens the stream."""
        if not self.anchor_fresh():
            return "SAFE_SCREEN"
        if stream_key not in self.active:
            return "SAFE_SCREEN"
        return "STREAM"


# ============================================ the island and its glitches ===
@dataclass
class RailResult:
    v_island_min: float
    v_island_max: float
    bod_trip_us: float
    bod_margin_us: float
    in_window: bool


def simulate_rail(host_v, t_end_us, c_uF=100.0, i_load_mA=20.0, r_src_ohm=1.0,
                  i_lim_A=0.2, v_clamp=3.6, v_nom=3.3, v_bod=2.4, v_ldo=1.8,
                  dropout=0.2, psrr_db=40.0, dt_us=0.5):
    """The bridge rail: host, ideal diode, current limit, bridge capacitor,
    clamp, brownout detector, and a 1.8 V LDO for U7. host_v(t_us) is the
    host waveform in volts. Returns the island rail extremes and the margin
    between the brownout trip and the island rail leaving its window.
    [HYPOTHESIS] every parameter."""
    c = c_uF * 1e-6
    i_load = i_load_mA * 1e-3
    vc = v_nom
    atten = 10 ** (-psrr_db / 20)
    vmin, vmax = 9.9, 0.0
    bod_t = None
    out_t = None
    edge = v_ldo + dropout
    t = 0.0
    while t < t_end_us:
        vh = host_v(t)
        # a hysteretic pre-regulator: it charges the bridge capacitor to v_nom
        # and stops. The clamp is the backstop if the regulator ever fails.
        i_in = 0.0 if vc >= v_nom else min(max(0.0, (vh - vc)) / r_src_ohm, i_lim_A)
        vc += (i_in - i_load) * dt_us * 1e-6 / c
        if vc > v_clamp:
            vc = v_clamp
        if vc < 0:
            vc = 0.0
        if vc >= edge:
            vi = v_ldo + (vc - v_nom) * atten
        else:
            vi = max(vc - dropout, 0.0)
        vmin, vmax = min(vmin, vi), max(vmax, vi)
        if bod_t is None and vc < v_bod:
            bod_t = t
        if out_t is None and (vi < v_ldo * 0.95 or vi > v_ldo * 1.05):
            out_t = t
        t += dt_us
    ok = out_t is None
    margin = (out_t - bod_t) if (out_t is not None and bod_t is not None) else float("inf")
    if bod_t is None:
        bod_t = float("inf")
    return RailResult(vmin, vmax, bod_t, margin, ok)


def drop_wave(t_start, t_len, v_before=5.0, v_during=0.0):
    return lambda t: v_during if t_start <= t < t_start + t_len else v_before


def spike_wave(t_start, t_len, v_before=5.0, v_during=20.0):
    return lambda t: v_during if t_start <= t < t_start + t_len else v_before


def ride_through_ms(c_uF=100.0, i_load_mA=20.0, v_nom=3.3, v_bod=2.4):
    """The time from a host loss to the brownout trip. A simple C dV / I."""
    return c_uF * 1e-6 * (v_nom - v_bod) / (i_load_mA * 1e-3) * 1e3


def bridge_state(grant, v_mv, p_mw):
    """The S_HOST switch and the hardware limiter. No firmware in this path:
    a comparator and a current limit. Authentication only moves the class. The
    envelope below holds for every class, true or false. [HYPOTHESIS] 10 us."""
    name, lo, hi, cap = CLASSES[grant.cls]
    if grant.cls == 0:
        return "OPEN", "class P0, the pads stay at 0 V"
    if v_mv > HOST_ABS_MAX_MV:
        return "OPEN", "above the absolute maximum, the clamp takes the surge"
    if not lo <= v_mv <= hi:
        return "OPEN", "outside the class window"
    if p_mw > cap:
        return "LIMIT", "the current limit holds the class power"
    return "CLOSED", "inside the class"


# ================================================ the atomic signature ===
@dataclass
class SignOutcome:
    released: bytes
    reason: str
    counter: int
    faults: int


def sign_atomic(u7, wallet_secret, msg, *, design="island", store_mJ=10.0,
                e_chunk_mJ=1.0, host_cut_at=None, glitch_phase=None,
                glitch_hits_verify=False, attached=True):
    """One wallet signature under the atomic-commit rule.

    design island: the rules R-A1 to R-A4 of 02-DESIGN-RULES.md. The host switch
      opens for the compute, the counter burns before release, the signature is
      verified before it leaves.
    design naive: U7 on the host rail, signature released first, counter
      committed after. It is the foil that shows what the rules prevent.

    host_cut_at: phase at which the host withdraws power. Phases: 0 token,
      1 isolate, 2 burn the counter, 3 compute, 4 self-verify, 5 release,
      6 commit (naive only).
    glitch_phase: 3 flips a bit during compute. glitch_hits_verify models a
      second glitch that skips the self-verify. [HYPOTHESIS] the silicon adds
      redundancy to the check, see the open issues.
    """
    s = u7.state
    ctr = s["lastsign"]
    pub = ed_public(wallet_secret)
    host_up = attached

    def cut(phase):
        nonlocal host_up
        if host_cut_at == phase:
            host_up = False

    if design == "island":
        if s["faults"] >= FAULT_LIMIT and attached:
            return SignOutcome(b"", "LOCKOUT: detach the host to sign", ctr, s["faults"])
        cut(0)
        if store_mJ < 1.5 * e_chunk_mJ:
            return SignOutcome(b"", "REFUSED: the island store is too low", ctr, s["faults"])
        cut(1)                                  # the host switch is open now
        cut(2)
        s["lastsign"] = ctr + 1
        u7.nvm.commit(s)                        # burn before use
        cut(3)
        body = struct.pack(">Q", ctr + 1) + msg
        sig = ed_sign(wallet_secret, body)
        if glitch_phase == 3:
            sig = sig[:-1] + bytes([sig[-1] ^ 0x01])
        cut(4)
        ok = ed_verify_strict(pub, body, sig)
        if glitch_hits_verify:
            ok = True                           # the second glitch skips it
        if not ok:
            s = u7.state
            s["faults"] += 1
            u7.nvm.commit(s)
            return SignOutcome(b"", "FAULT: self-verify failed, nothing released",
                               ctr + 1, s["faults"])
        cut(5)
        if not attached and u7.state["faults"] > 0:
            s = u7.state
            s["faults"] = 0                     # a clean signature with no host
            u7.nvm.commit(s)
        return SignOutcome(sig, "RELEASED", ctr + 1, u7.state["faults"])

    # the naive design: the host rail feeds U7
    if host_cut_at in (0, 1, 2, 3, 4):
        return SignOutcome(b"", "LOST: host power ended during compute", ctr, s["faults"])
    body = struct.pack(">Q", ctr + 1) + msg
    sig = ed_sign(wallet_secret, body)
    if host_cut_at == 6:
        # the signature already left, the counter never committed
        return SignOutcome(sig, "RELEASED then counter lost", ctr, s["faults"])
    s["lastsign"] = ctr + 1
    u7.nvm.commit(s)
    return SignOutcome(sig, "RELEASED", ctr + 1, s["faults"])


# ================================================== the atomic update ===
PROGRAM_SECRET_LABEL = b"model program key"


@dataclass
class Release:
    seq: int
    chunks: list
    manifest_sig: bytes = b""

    @property
    def digest(self):
        return hashlib.sha256(b"".join(self.chunks)).digest()

    def manifest(self):
        return b"BDLM_LEAF_MANIFEST_MODEL" + struct.pack(">Q", self.seq) + self.digest


def make_release(program_secret, seq, nchunks=6):
    r = Release(seq, [hashlib.sha256(f"{seq}:{i}".encode()).digest() for i in range(nchunks)])
    r.manifest_sig = ed_sign(program_secret, r.manifest())
    return r


TRIAL_LIMIT = 3


class Device:
    """Two flash slots, one NVM blob. A power cut can land on any tick."""

    def __init__(self, program_pub, first):
        self.pub = program_pub
        self.nvm = NVM()
        self.flash = {"A": first, "B": None}
        self.nvm.commit({"active": "A", "floor": first.seq, "next": 0,
                         "target": None, "pending": None, "trials": 0,
                         "deferred": False})
        self.ticks = 0
        self.cut_at = None

    def _tick(self):
        if self.cut_at is not None and self.ticks == self.cut_at:
            raise PowerLoss(f"tick {self.ticks}")
        self.ticks += 1

    def bootable(self, slot, floor):
        r = self.flash[slot]
        if r is None or r.seq < floor:
            return False
        if hashlib.sha256(b"".join(r.chunks)).digest() != r.digest:
            return False
        return ed_verify_strict(self.pub, r.manifest(), r.manifest_sig)

    # -------------------------------------------------------- the update ---
    def install(self, release, store_ok=True):
        """Chunked and resumable. Only the final flips are atomic commits.
        Starts only with the energy of the commit in the island store."""
        if not store_ok:
            return "REFUSED: no energy for the commit"
        s = self.nvm.read()
        inactive = "B" if s["active"] == "A" else "A"
        if s["target"] != release.seq:
            s.update(target=release.seq, next=0)
            self._tick()
            self.nvm.commit(s)
            self.flash[inactive] = Release(release.seq, [b""] * len(release.chunks),
                                           release.manifest_sig)
        slot = self.flash[inactive]
        while s["next"] < len(release.chunks):
            i = s["next"]
            self._tick()                                   # the chunk write
            slot.chunks[i] = release.chunks[i]
            self._tick()                                   # the progress commit
            s["next"] = i + 1
            self.nvm.commit(s)
        self._tick()                                       # the verify
        if not self.bootable(inactive, 0):
            return "REJECTED"
        self._tick()                                       # mark the trial
        s.update(pending=inactive, trials=0, deferred=False)
        self.nvm.commit(s)
        return "TRIAL_PENDING"

    # ---------------------------------------------------------- the boot ---
    def boot(self, trial_clean=True):
        """Returns (slot, verdict). Never a brick while one slot verifies."""
        s = self.nvm.read()
        slot = s["active"]
        if s["pending"] is not None:
            if s["trials"] >= TRIAL_LIMIT or not self.bootable(s["pending"], s["floor"]):
                s.update(pending=None, trials=0, deferred=True, target=None, next=0)
                self.nvm.commit(s)
                slot = s["active"]
            else:
                s["trials"] += 1
                self.nvm.commit(s)
                if trial_clean:
                    new = s["pending"]
                    s.update(active=new, floor=self.flash[new].seq, pending=None,
                             trials=0, target=None, next=0, deferred=False)
                    self._tick()
                    self.nvm.commit(s)                     # one atomic flip
                    return new, "COMMITTED"
                # a refused part reverts the whole set at once, floors unchanged
                s.update(pending=None, trials=0, deferred=True, target=None, next=0)
                self.nvm.commit(s)
                return s["active"], "REVERTED"
        if not self.bootable(slot, s["floor"]):
            other = "B" if slot == "A" else "A"
            if self.bootable(other, s["floor"]):
                return other, "FALLBACK"
            return None, "BRICK"
        return slot, "DEFERRED" if s["deferred"] else "OK"


# ==================================================== the sizing numbers ===
def store_capacitance_mF(e_mJ, v_hi=3.3, v_lo=2.2):
    """C = 2 E / (V1^2 - V2^2). v_lo is the brownout floor plus the margin."""
    return 2 * e_mJ * 1e-3 / (v_hi ** 2 - v_lo ** 2) * 1e3


def store_sizing(e_sign_mean_mJ, mean_iters=3.85, quantile=1e-4, margin=1.5):
    """The island store for three designs. ML-DSA-87 repeats its signing loop
    3.85 times on average [PUBLICATION] FIPS 204 Table 1. The store covers one
    iteration, the mean signature, or the 99.99 percent signature."""
    p = 1 / mean_iters
    kmax = math.ceil(math.log(quantile) / math.log(1 - p))
    e1 = e_sign_mean_mJ / mean_iters
    return {
        "e_iter_mJ": e1,
        "k_99_99": kmax,
        "C_iteration_mF": store_capacitance_mF(margin * e1),
        "C_mean_mF": store_capacitance_mF(margin * e_sign_mean_mJ),
        "C_worst_mF": store_capacitance_mF(margin * kmax * e1),
    }


def loop_count_entropy_bits(mean_iters=3.85):
    """Entropy of the signing-loop count K, geometric with p = 1/mean. This is
    what an unpadded recharge pattern shows the host, per signature."""
    p = 1 / mean_iters
    return (-p * math.log2(p) - (1 - p) * math.log2(1 - p)) / p


def line_attenuation_db(f_hz, f_reg_hz=20e3):
    """A non-isolated bridge: the host line current follows the load current
    through a first-order regulation loop. Filtering is a cost, not a cure."""
    return -10 * math.log10(1 + (f_hz / f_reg_hz) ** 2)


def sideband_precharge_ms(e_handshake_uJ=200.0, p_sideband_mW=1.8):
    """Bare tier, dead body: the first handshake lives on the sideband alone
    (hw/energy/03 Section 3.4 item 2: 1 mA at 1.8 V). [HYPOTHESIS]"""
    return e_handshake_uJ * 1e-3 / p_sideband_mW * 1e3


def update_window_s():
    """The NOR program time of a full update, read from fw/boot (read only)."""
    here = os.path.dirname(os.path.abspath(__file__))
    boot = os.path.join(here, "..", "..", "..", "fw", "boot")
    sys.path.insert(0, boot)
    try:
        import bootsm
        return bootsm.budgets()["update_write_nor_s"]
    finally:
        sys.path.remove(boot)


# ============================================================ the report ===
def report():
    print("THE CLASSES (power at the Leaf input, [HYPOTHESIS] windows)")
    for c, (n, lo, hi, pw) in CLASSES.items():
        amp = (pw / lo / VHV_LEAVES) if c else 0.0
        print(f"  {n}: {lo/1000:5.2f}-{hi/1000:5.2f} V  {pw/1000:5.1f} W  "
              f"{amp:4.2f} A per VHV leaf at the low edge  "
              f"(rating {LEAF_RATING_A} A)")
    print("\nTHE POLICY TABLE")
    for k, v in POLICY_ROWS.items():
        print(f"  {k}: {v}")
    print(f"\nHostRecord frame: {REC_LEN} B record + 64 B signature = {FRAME_LEN} B")
    print("\nTHE ISLAND RAIL, 100 uF bridge, 20 mA load (simulate_rail)")
    print(f"  ride-through to the brownout trip: {ride_through_ms():.1f} ms")
    for ms in (0.5, 2.0, 5.0, 20.0):
        r = simulate_rail(drop_wave(100, ms * 1000), 100 + ms * 1000 + 3000, dt_us=2.0)
        trip = "no trip" if r.bod_trip_us == float("inf") else f"trip at {r.bod_trip_us/1000 - 0.1:.1f} ms"
        lead = "island kept" if r.bod_margin_us == float("inf") else f"trip leads the loss by {r.bod_margin_us/1000:.2f} ms"
        print(f"  host drop {ms:5.1f} ms: island {r.v_island_min:.2f}-{r.v_island_max:.2f} V, "
              f"BOD {trip}, {lead}, in window {r.in_window}")
    for us in (1, 100, 5000):
        r = simulate_rail(spike_wave(100, us), 100 + us + 3000, dt_us=0.5)
        print(f"  host 20 V spike {us:5d} us: island {r.v_island_min:.3f}-{r.v_island_max:.3f} V, "
              f"in window {r.in_window}")
    print("\nTHE ISLAND STORE for isolated signing (V 3.3 to 2.2, margin 1.5)")
    print("  E_sign mean   iteration   mean sig    99.99 pct sig   (loop count max)")
    for e in (1.0, 5.0, 20.0):
        z = store_sizing(e)
        print(f"  {e:5.1f} mJ    {z['C_iteration_mF']:6.2f} mF  {z['C_mean_mF']:6.2f} mF"
              f"  {z['C_worst_mF']:8.2f} mF   ({z['k_99_99']})")
    print(f"  loop count entropy {loop_count_entropy_bits():.2f} bits per signature "
          "(unpadded recharge pattern)")
    print(f"  sideband pre-charge for one handshake: {sideband_precharge_ms():.0f} ms")
    print(f"  line attenuation, non-isolated: " +
          ", ".join(f"{f:g} Hz {line_attenuation_db(f):.0f} dB" for f in (1e3, 20e3, 1e6, 100e6)))
    print(f"  full update NOR program time (fw/boot budgets): {update_window_s():.1f} s")


if __name__ == "__main__":
    report()
