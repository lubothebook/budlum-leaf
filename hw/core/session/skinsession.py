#!/usr/bin/env python3
"""skinsession.py - one session on many Skins, and a session that follows a Skin.

Session seat of hw/core, block HP-2. A study. It changes no L.6.0 or L.6.1
decision. It extends the RG-19 model of hw/hostpower/continuity (imported read
only) from one Leaf to one Core with N Skins.

The idea. The session is on the Core, in its U7 and its validator link. A Skin
is a view. A Skin holds nothing durable and signs nothing. Four modes:

  MIRROR   every Skin shows the same canvas (scaled to its size)
  EXTEND   one canvas laid over several Skins, a tile range for each
  SPLIT    a different session for each Skin
  HANDOFF  the session moves from one Skin to another on the same Core

The Core is the only signer and the only orderer. Skin events carry a MAC under
the link key. The Core stamps each event with a 480 Hz scan tick, merges all
Skins into one ordered stream and signs it. Validators see one writer.

A session also moves between Cores. Core A pauses (or lapses), Core B resumes
as a second writer that the wallet authorised. The epoch of RG-19 then refuses
every late input of Core A.

Every number is [HYPOTHESIS] unless a comment names a source.

Run: python3 skinsession.py     a demo of each mode and of one roam
"""
import hashlib
import os
import sys
from dataclasses import dataclass, field, replace

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "hw", "hostpower", "continuity"))
import sessionchain as S  # noqa: E402  read only: the RG-19 model

MIRROR, EXTEND, SPLIT, HANDOFF = "MIRROR", "EXTEND", "SPLIT", "HANDOFF"
TILE = 200                         # px, the 200 x 200 tile of FINAL/21 [DECISION]
SCAN_HZ = 480                      # the touch scan                       [DECISION]
TICK_MS = 1000.0 / SCAN_HZ

# kind: (rank in a tick, changes session state, carried in the ordered stream)
KINDS = {
    "pen": (0, True),
    "touch": (1, True),
    "key": (2, True),
    "shutter": (3, True),          # a camera trigger is ordered; the pixels are not
    "imu": (4, False),             # samples fold into the batch, never a transaction
    "camera": (5, False),          # RAW rides its own stream with a capture id
}


def H(*parts):
    return S.H(*parts)


# ------------------------------------------------------------------ the Skin ---
@dataclass(frozen=True)
class SkinStore:
    name: str
    energy_j: float


SKIN_STORES = {"none": SkinStore("none", 0.0),
               "seconds": SkinStore("seconds", 2.0),
               "minutes": SkinStore("minutes", 72.0),
               # the C1 radio Skin of hw/core/link/out/distance_classes.txt, G4: a 4.8 Wh cell
               "cell": SkinStore("cell", 4.8 * 3600.0)}
SKIN_ROM_W = 0.12                  # the safe screen of the body column   [TREE] hw/energy/out/budget.txt


def rom_screen_s(store):
    """Seconds that a Skin store keeps the ROM screen lit."""
    return store.energy_j / SKIN_ROM_W


@dataclass
class Skin:
    """The surface. Its identity is in ROM. Everything else is volatile."""
    skin_id: str
    w: int
    h: int
    store: SkinStore = SKIN_STORES["none"]
    core_id: str = ""
    pairing_epoch: int = 0
    link_key: bytes = b""          # volatile: derived at attach, lost at power loss
    tile_lines: tuple = ()         # volatile: a few lines for scan-out, no frame store
    seq: int = 0

    def held_state(self):
        """What the Skin holds. A durable session field here is a bug."""
        return {"identity": self.skin_id, "rom": "safe screen glyphs",
                "volatile": ["link_key", "tile_lines", "seq"]}

    def power_cycle(self):
        self.link_key = b""
        self.tile_lines = ()
        self.core_id = ""
        self.seq = 0

    def make_event(self, kind, x=0, y=0, payload=b""):
        """A raw event. The MAC is the whole authentication; there is no signature."""
        self.seq += 1
        mac = H(b"BDLM_SKIN_EVENT_V1", self.link_key, self.skin_id, self.seq, kind, x, y, payload)
        return SkinEvent(self.skin_id, self.seq, kind, x, y, payload, self.pairing_epoch, mac)


@dataclass(frozen=True)
class SkinEvent:
    skin_id: str
    seq: int
    kind: str
    x: int
    y: int
    payload: bytes
    pairing_epoch: int
    mac: bytes
    tick: int = -1                 # stamped by the Core on arrival, never by the Skin


# --------------------------------------------------------- the pairing record ---
class PairingRegistry:
    """The chain record of which Core a Skin is paired to. One Core at a time."""
    def __init__(self):
        self.rec = {}              # skin_id -> (core_id, epoch, revoked)
        self.allowed = {}          # skin_id -> the Cores the wallet allowed to take it
        self.log = []

    def pair(self, skin_id, core_id, wallet_signed):
        """Pairing is a high value action of FINAL/08 Section 8.5: the wallet signs."""
        if not wallet_signed:
            raise PermissionError("pairing needs the wallet")
        prev = self.rec.get(skin_id)
        epoch = (prev[1] + 1) if prev else 1
        self.rec[skin_id] = (core_id, epoch, False)
        self.log.append((skin_id, core_id, epoch))
        return epoch

    def allow(self, skin_id, core_id, wallet_signed):
        """The wallet lists a Core of the user as a Core that may take this Skin. Once."""
        if not wallet_signed:
            raise PermissionError("allow needs the wallet")
        self.allowed.setdefault(skin_id, set()).add(core_id)

    def take(self, skin_id, core_id):
        """A Core on the allowed list takes the Skin. No user action; the epoch rises."""
        if core_id not in self.allowed.get(skin_id, set()):
            raise PermissionError("the wallet did not allow this Core")
        prev = self.rec.get(skin_id)
        epoch = (prev[1] + 1) if prev else 1
        self.rec[skin_id] = (core_id, epoch, False)
        self.log.append((skin_id, core_id, epoch))
        return epoch

    def revoke(self, skin_id, wallet_signed):
        if not wallet_signed:
            raise PermissionError("revoke needs the wallet")
        core, epoch, _ = self.rec[skin_id]
        self.rec[skin_id] = (core, epoch, True)

    def current(self, skin_id):
        return self.rec.get(skin_id)


# ---------------------------------------------------------------- the views ---
@dataclass
class View:
    view_id: int
    skin_id: str
    session_id: str
    mode: str
    rect: tuple                    # (x, y, w, h) on the canvas of the session
    epoch: int = 0                 # rises at every bind; an old epoch is refused


def tiles_of(rect):
    x, y, w, h = rect
    return {(tx, ty) for tx in range(x // TILE, (x + w - 1) // TILE + 1)
            for ty in range(y // TILE, (y + h - 1) // TILE + 1)}


def extend_layout(skins, direction="x", gap=0):
    """Lay Skins side by side on one canvas. Returns the rects and the canvas size."""
    rects, off = [], 0
    for sk in skins:
        r = (off, 0, sk.w, sk.h) if direction == "x" else (0, off, sk.w, sk.h)
        rects.append(r)
        off += (sk.w if direction == "x" else sk.h) + gap
    cw = max(r[0] + r[2] for r in rects)
    ch = max(r[1] + r[3] for r in rects)
    return rects, (cw, ch)


def to_canvas(view, canvas, x, y, skin_wh):
    """Map a Skin-local point to the canvas of its session."""
    rx, ry, rw, rh = view.rect
    if view.mode == MIRROR:
        return (x * canvas[0] // skin_wh[0], y * canvas[1] // skin_wh[1])
    return (rx + x, ry + y)


# ---------------------------------------------------------- the multi-writer ledger ---
class _Proxy:
    def __init__(self, keys, writer):
        self.keys, self.writer = keys, writer

    def ok(self, name, sig, domain, *fields):
        return self.keys.ok(self.writer if name == "leaf_session" else name, sig, domain, *fields)

    def sign(self, name, domain, *fields):
        return self.keys.sign(self.writer if name == "leaf_session" else name, domain, *fields)


@dataclass(frozen=True)
class GrantWriterTx:
    """The wallet authorises a Core as a writer of the session, until a wall frame."""
    sid: str
    core: str
    until: int
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.core, self.until)


@dataclass(frozen=True)
class TakeOverTx:
    """A granted writer takes a live session in one transaction, with no pause and no lapse.

    The epoch rises, so every later input of the old writer is refused (RG-19A rule R13).
    """
    sid: str
    to_core: str
    resume_seq: int            # the epoch the new writer saw
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.to_core, self.resume_seq)


TAKEOVER_DOMAIN = b"BDLM_LEAF_WRITER_TAKEOVER_V1"
GRANT_DOMAIN = b"BDLM_LEAF_WRITER_GRANT_V1"


def sign_takeover(keys, tx):
    return replace(tx, sig=keys.sign(tx.to_core, TAKEOVER_DOMAIN, *tx.fields()))


def sign_grant(keys, tx):
    return replace(tx, sig=keys.sign("leaf_wallet", GRANT_DOMAIN, *tx.fields()))


class CoreLedger(S.Ledger):
    """The RG-19 ledger with a named writer Core, and writers that move.

    A writer other than the active one can resume a paused session if the wallet
    granted it (RG-19A rule R13). Every other transaction of a non-writer is refused.
    """
    def __init__(self, sid, keys, writer, **kw):
        super().__init__(sid, keys, **kw)
        self.writer = writer
        self.grants = {writer: 10 ** 12}
        self.writer_log = [(0, writer)]

    def _apply(self, tx):
        if isinstance(tx, GrantWriterTx):
            if not self.keys.ok("leaf_wallet", tx.sig, GRANT_DOMAIN, *tx.fields()):
                return "BAD_SIGNATURE"
            self.grants[tx.core] = tx.until
            return ""
        if isinstance(tx, TakeOverTx):
            return self._takeover(tx)
        if isinstance(tx, S.ResumeTx) and tx.signer not in ("leaf_session", "leaf_wallet"):
            return self._resume_as(tx)
        real = self.keys
        self.keys = _Proxy(real, self.writer)
        try:
            return super()._apply(tx)
        finally:
            self.keys = real

    def _takeover(self, tx):
        s = self.s
        if not self.keys.ok(tx.to_core, tx.sig, TAKEOVER_DOMAIN, *tx.fields()):
            return "BAD_SIGNATURE"
        if tx.to_core not in self.grants:
            return "NOT_A_WRITER"
        if self.wall > self.grants[tx.to_core]:
            return "GRANT_EXPIRED"
        if s.status != S.ACTIVE:
            return "SESSION_NOT_ACTIVE"
        if tx.resume_seq != s.resume_seq:
            return "STALE_EPOCH"
        self.s = replace(s, resume_seq=s.resume_seq + 1)
        self.writer = tx.to_core
        self.writer_log.append((self.wall, tx.to_core))
        return ""

    def _resume_as(self, tx):
        s = self.s
        if not self.keys.ok(tx.signer, tx.sig, S.DOMAIN[S.ResumeTx], *tx.fields()):
            return "BAD_SIGNATURE"
        if tx.signer not in self.grants:
            return "NOT_A_WRITER"
        if s.status not in (S.PAUSED, S.LAPSED):
            return "SESSION_NOT_PAUSED"
        if tx.pause_seq != s.pause_seq:
            return "PAUSE_UNKNOWN"
        if tx.resume_seq != s.resume_seq + 1:
            return "REPLAY"
        if self.wall > self.grants[tx.signer]:
            return "GRANT_EXPIRED"
        if tx.expected_root != s.paused_root:
            return "RESUME_STATE_MISMATCH"
        self.s = replace(s, status=S.ACTIVE, resume_seq=tx.resume_seq,
                         last_leaf_second=self.wall // S.FPS, last_resume_wall=self.wall)
        self.writer = tx.signer
        self.writer_log.append((self.wall, tx.signer))
        return ""


# ------------------------------------------------------------------- the Core ---
CLASS_NAMES = ("pen", "touch", "key", "shutter", "imu", "camera")


class Core:
    """The device. It holds U7, the frame store, the views and the sessions."""
    def __init__(self, core_id, keys, registry):
        self.core_id, self.keys, self.registry = core_id, keys, registry
        self.skins = {}
        self.views = {}              # view_id -> View
        self.ledgers = {}            # session id -> CoreLedger
        self.next_view = 1
        self.frame_store = {}        # session id -> last frame root (the Core holds it)
        self.dropped = []            # (reason, event) the Core refused
        self.ordered_log = []        # every merged event, in order
        self.nonce = {}              # session id -> next input nonce

    # ---- attach: the Skin is a view, never a writer ----
    def attach(self, skin):
        rec = self.registry.current(skin.skin_id)
        if rec is None or rec[2] or rec[0] != self.core_id:
            return False
        skin.core_id, skin.pairing_epoch = self.core_id, rec[1]
        skin.link_key = H(b"BDLM_SKIN_LINK_V1", self.core_id, skin.skin_id, rec[1])
        self.skins[skin.skin_id] = skin
        return True

    def detach(self, skin_id):
        sk = self.skins.pop(skin_id, None)
        for vid in [v for v, vw in self.views.items() if vw.skin_id == skin_id]:
            del self.views[vid]
        if sk:
            sk.power_cycle()

    def link_key_for(self, skin_id):
        rec = self.registry.current(skin_id)
        if rec is None:
            return None
        return H(b"BDLM_SKIN_LINK_V1", self.core_id, skin_id, rec[1])

    # ---- sessions ----
    def open_session(self, sid, grant_until=10 ** 12):
        led = CoreLedger(sid, self.keys, self.core_id, grant_until=grant_until,
                         validators=("val1", "val2"))
        self.ledgers[sid] = led
        self.nonce[sid] = 0
        return led

    def adopt_session(self, led):
        """A ledger that moved here: take the nonce from the chain."""
        self.ledgers[led.s.sid] = led
        self.nonce[led.s.sid] = led.s.nonce

    @staticmethod
    def app_event(ev):
        """The session event a Skin event stands for. Only the Core knows the app."""
        return {"touch": ("tap",), "pen": ("scroll", ev.y), "key": ("key", ev.x % 256),
                "shutter": ("tap",)}[ev.kind]

    def sign_input(self, sid, ev, wall):
        """The Core U7 signs one state event. A Skin never does."""
        led = self.ledgers[sid]
        tx = S.sign_tx(self.keys, S.InputTx(sid, led.s.resume_seq, self.nonce[sid], wall,
                                            self.app_event(ev)), signer=self.core_id)
        self.nonce[sid] += 1
        return tx

    def bind(self, mode, skins, sid=None, sids=None):
        """Bind Skins to sessions by mode. Returns the new views."""
        out = []
        if mode == MIRROR:
            for sk in skins:
                out.append(self._new_view(sk, sid, MIRROR, (0, 0, sk.w, sk.h)))
        elif mode == EXTEND:
            rects, canvas = extend_layout(skins)
            for sk, r in zip(skins, rects):
                out.append(self._new_view(sk, sid, EXTEND, r))
        elif mode == SPLIT:
            for sk, s in zip(skins, sids):
                out.append(self._new_view(sk, s, SPLIT, (0, 0, sk.w, sk.h)))
        else:
            raise ValueError(mode)
        return out

    def _new_view(self, sk, sid, mode, rect):
        v = View(self.next_view, sk.skin_id, sid, mode, rect)
        self.views[v.view_id] = v
        self.next_view += 1
        return v

    def view_of(self, skin_id):
        for v in self.views.values():
            if v.skin_id == skin_id:
                return v
        return None

    def handoff(self, sid, from_skin, to_skin):
        """Move the session view from one Skin to another. The session never pauses."""
        old = self.view_of(from_skin)
        if old is None or old.session_id != sid:
            raise KeyError("the session is not on that Skin")
        epoch = old.epoch + 1
        del self.views[old.view_id]
        sk = self.skins[to_skin]
        v = View(self.next_view, to_skin, sid, HANDOFF, (0, 0, sk.w, sk.h), epoch)
        self.next_view += 1
        self.views[v.view_id] = v
        return v

    # ---- the merge of many Skins into one ordered stream ----
    def receive(self, ev, arrive_ms):
        """Stamp, check the MAC and the pairing epoch. Returns the stamped event or None."""
        key = self.link_key_for(ev.skin_id)
        rec = self.registry.current(ev.skin_id)
        if key is None or ev.skin_id not in self.skins:
            self.dropped.append(("unknown skin", ev))
            return None
        want = H(b"BDLM_SKIN_EVENT_V1", key, ev.skin_id, ev.seq, ev.kind, ev.x, ev.y, ev.payload)
        if want != ev.mac:
            self.dropped.append(("bad mac", ev))
            return None
        if rec[2] or ev.pairing_epoch != rec[1]:
            self.dropped.append(("stale pairing", ev))
            return None
        if self.view_of(ev.skin_id) is None:
            self.dropped.append(("no view", ev))
            return None
        return replace(ev, tick=int(arrive_ms / TICK_MS))

    @staticmethod
    def merge(events):
        """One order for all Skins. The key is total, so the order never depends on arrival."""
        return sorted(events, key=lambda e: (e.tick, KINDS[e.kind][0], e.skin_id, e.seq))

    def ingest(self, batch):
        """batch: [(event, arrive_ms)]. Returns the ordered, accepted events."""
        stamped = [x for x in (self.receive(e, t) for e, t in batch) if x is not None]
        ordered = self.merge(stamped)
        self.ordered_log.extend(ordered)
        return ordered

    def state_changing(self, ordered):
        return [e for e in ordered if KINDS[e.kind][1]]

    def route(self, ev):
        """The session and the canvas point of an event."""
        v = self.view_of(ev.skin_id)
        sk = self.skins[ev.skin_id]
        led = self.ledgers[v.session_id]
        canvas = (extend_layout([self.skins[x.skin_id] for x in self._extend_views(v)])[1]
                  if v.mode == EXTEND else (sk.w, sk.h))
        return v.session_id, to_canvas(v, canvas, ev.x, ev.y, (sk.w, sk.h)), led

    def _extend_views(self, v):
        vs = sorted((x for x in self.views.values() if x.session_id == v.session_id and x.mode == EXTEND),
                    key=lambda x: x.rect[0] * 100000 + x.rect[1])
        return vs


def demo():
    keys = S.Keys(["leaf_wallet", "core_a", "core_b", "leaf_session", "val1", "val2"])
    reg = PairingRegistry()
    core = Core("core_a", keys, reg)
    skins = [Skin(f"skin{i}", 1600, 3200) for i in range(3)]
    for sk in skins:
        reg.pair(sk.skin_id, "core_a", wallet_signed=True)
        core.attach(sk)
    core.open_session("S")
    core.bind(EXTEND, skins, sid="S")
    ev = [(skins[1].make_event("touch", 10, 20), 5.0), (skins[0].make_event("pen", 3, 4), 5.0)]
    print("extend, ordered:", [(e.skin_id, e.kind, e.tick) for e in core.ingest(ev)])


if __name__ == "__main__":
    demo()
