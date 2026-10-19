#!/usr/bin/env python3
"""sessionchain.py - the reference model of RG-19: a session that survives a power gap.

Continuity team of hw/hostpower, L.6.1 (proposed). It is a small executable
model of the pause and resume rules of RG-19-session-pause-resume.md. It does
not replace validator/leaf-duty, which this team cannot edit. It shows that the
rules keep the session state exact, and where a gap still loses something.

What it models
  Ledger    the canonical chain state of one session: input, action, receipt,
            pause, lapse and resume transactions, and the rules that admit them.
  U7        the Leaf secure element: a two-slot journal that survives a torn
            write, the outbox of signed value actions, the epoch counter.
  Replica   a validator that receives transactions and submits them to the
            chain after a gossip delay. It can die.

The signatures are HMAC-SHA256 stand-ins keyed per signer. The model checks the
logic of the rules and not the cryptography. Sizes of the real ML-DSA
signatures are in proto/session_continuity.proto and the spec.

The session clock. The state of a session is a function of the ordered events
and of the session frame count. The session frame count stops while the session
is PAUSED. Therefore a pause of any length leaves the state unchanged.

Run: python3 sessionchain.py        a demo of one pause and one lapse
Tests: python3 -m unittest discover -s tests
"""
import hashlib
import hmac
import json
import random
import sys
from dataclasses import dataclass, field, replace

sys.dont_write_bytecode = True

FPS = 240
FRAMES_PER_SLOT = 6 * FPS            # the 6 s slot of FINAL/21 Section 21.5.2
FINALITY_LAG = FPS                   # 1 s, chain.rs FINALITY_LAG_FRAMES
INPUT_TTL = FPS                      # an input expires 1 s after signing   [HYPOTHESIS]
LAPSE_AFTER_S = 2                    # seconds without a Leaf receipt      [HYPOTHESIS]
PAUSE_TTL = 30 * 86400 * FPS         # a pause lives 30 days                [HYPOTHESIS]
PAUSE_MIN_GAP = 10 * FPS             # one Leaf pause per 10 s after a resume [HYPOTHESIS]
MAX_TEXT = 24


def H(*parts):
    h = hashlib.sha256()
    for p in parts:
        b = p if isinstance(p, bytes) else repr(p).encode()
        h.update(len(b).to_bytes(8, "little"))
        h.update(b)
    return h.digest()


class Keys:
    """Stand-in signatures. A signer name is a key. Anyone can verify."""
    def __init__(self, names):
        self.secret = {n: H(b"secret", n) for n in names}

    def sign(self, name, domain, *fields):
        return hmac.new(self.secret[name], H(domain, *fields), hashlib.sha256).digest()

    def ok(self, name, sig, domain, *fields):
        if name not in self.secret:
            return False
        return hmac.compare_digest(sig, self.sign(name, domain, *fields))


# ---------------------------------------------------------------- the app ---
@dataclass(frozen=True)
class App:
    balance: int = 0
    text: tuple = ()
    scroll: int = 0
    vel: int = 0
    anim: int = 0


def app_apply(a, ev):
    k = ev[0]
    if k == "tap":
        return replace(a, balance=a.balance + 1)
    if k == "key":
        return replace(a, text=(a.text + (ev[1],))[:MAX_TEXT])
    if k == "scroll":
        return replace(a, scroll=max(0, min(100000, a.scroll + ev[1])), vel=0)
    if k == "fling":
        return replace(a, vel=ev[1])
    if k == "settext":
        return replace(a, text=tuple(ev[1])[:MAX_TEXT])
    raise ValueError(ev)


def app_tick(a, n=1):
    """n frames. A fling decays by 9/10 each frame, so it ends after a few frames."""
    while n > 0 and a.vel != 0:
        a = replace(a, scroll=max(0, min(100000, a.scroll + a.vel)),
                    vel=int(a.vel * 9 / 10), anim=a.anim + 1)
        n -= 1
    if n > 0:
        a = replace(a, anim=a.anim + n)
    return a


# ------------------------------------------------------------ the state ---
ACTIVE, PAUSED, LAPSED, CLOSED = "ACTIVE", "PAUSED", "PAUSED_LAPSE", "CLOSED"


@dataclass(frozen=True)
class SS:
    sid: str
    status: str = ACTIVE
    frame_no: int = 0               # the session clock: it stops in a pause
    nonce: int = 0                  # next input nonce
    anonce: int = 0                 # next action nonce
    vault: int = 0                  # value moved by actions
    app: App = App()
    pause_seq: int = 0
    resume_seq: int = 0             # also the epoch of the inputs
    paused_root: bytes = b""
    paused_at_wall: int = 0
    last_leaf_second: int = 0
    grant_until: int = 10 ** 12     # wall frame
    unconfirmed: int = 0            # frames the Leaf showed beyond the pause record
    dropped_after_pause: int = 0
    last_resume_wall: int = -10 ** 9

    def app_root(self):
        """The root that a pause freezes and a resume restores."""
        return H(b"BDLM_LEAF_SESSION_STATE_V1", self.sid, self.frame_no, self.nonce,
                 self.anonce, self.vault, self.app)


# ------------------------------------------------------ the transactions ---
@dataclass(frozen=True)
class InputTx:
    sid: str
    epoch: int
    nonce: int
    signed_at: int
    ev: tuple
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.epoch, self.nonce, self.signed_at, self.ev)


@dataclass(frozen=True)
class ActionTx:
    sid: str
    anonce: int
    amount: int
    valid_until: int
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.anonce, self.amount, self.valid_until)


@dataclass(frozen=True)
class ReceiptTx:
    sid: str
    second: int
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.second)


@dataclass(frozen=True)
class PauseTx:
    sid: str
    pause_seq: int
    reason: str
    last_frame: int
    claimed_root: bytes
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.pause_seq, self.reason, self.last_frame, self.claimed_root)


@dataclass(frozen=True)
class LapseTx:
    sid: str
    pause_seq: int
    last_receipt_second: int
    validator: str
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.pause_seq, self.last_receipt_second, self.validator)


@dataclass(frozen=True)
class ResumeTx:
    sid: str
    pause_seq: int
    resume_seq: int
    expected_root: bytes
    signer: str                    # "leaf_session" or "leaf_wallet"
    new_grant_until: int = 0
    sig: bytes = b""

    def fields(self):
        return (self.sid, self.pause_seq, self.resume_seq, self.expected_root,
                self.signer, self.new_grant_until)


DOMAIN = {InputTx: b"BDLM_LEAF_INPUT_TX_V2", ActionTx: b"BDLM_LEAF_ACTION_TX_V1",
          ReceiptTx: b"BDLM_LEAF_RECEIPT_V2", PauseTx: b"BDLM_LEAF_SESSION_PAUSE_V1",
          LapseTx: b"BDLM_LEAF_LAPSE_NOTICE_V1", ResumeTx: b"BDLM_LEAF_SESSION_RESUME_V1"}
SIGNER = {InputTx: "leaf_session", ActionTx: "leaf_wallet", ReceiptTx: "leaf_session",
          PauseTx: "leaf_session"}


def sign_tx(keys, tx, signer=None):
    name = signer or getattr(tx, "signer", None) or getattr(tx, "validator", None) \
        or SIGNER[type(tx)]
    return replace(tx, sig=keys.sign(name, DOMAIN[type(tx)], *tx.fields()))


# ------------------------------------------------------------- the ledger ---
class Ledger:
    """The canonical chain state of one session, stepped one wall frame at a time."""

    def __init__(self, sid, keys, grant_until=10 ** 12, validators=("val1", "val2")):
        self.keys = keys
        self.s = SS(sid, grant_until=grant_until)
        self.wall = 0
        self.validators = set(validators)
        self.pending = {}                 # wall frame -> [tx]
        self.rejects = []                 # (wall, kind, code)
        self.applied = []                 # (wall, kind)
        self.snapshots = {0: self.s}      # slot -> state at the slot boundary
        self.seen = set()                 # a transaction applies once
        self.dups = 0
        self.finalized_wall = 0

    def submit(self, at_wall, tx):
        self.pending.setdefault(max(at_wall, self.wall), []).append(tx)

    def run_to(self, wall_end):
        """Step the chain to `wall_end`. Idle stretches are fast-forwarded."""
        while self.wall < wall_end:
            if self.wall in self.pending:
                for tx in self.pending.pop(self.wall):
                    if tx in self.seen:
                        self.dups += 1
                        continue
                    code = self._apply(tx)
                    kind = type(tx).__name__
                    if code:
                        self.rejects.append((self.wall, kind, code))
                    else:
                        self.seen.add(tx)
                        self.applied.append((self.wall, kind))
                self._tick(1)
                self.wall += 1
                self._boundary()
                continue
            nxt = min([f for f in self.pending if f > self.wall] + [wall_end])
            nxt = min(nxt, (self.wall // FRAMES_PER_SLOT + 1) * FRAMES_PER_SLOT, wall_end)
            self._tick(nxt - self.wall)
            self.wall = nxt
            self._boundary()

    def _boundary(self):
        if self.wall % FRAMES_PER_SLOT == 0:
            self.snapshots[self.wall // FRAMES_PER_SLOT] = self.s
            self.finalized_wall = self.wall

    def _tick(self, n):
        if self.s.status == ACTIVE and n > 0:
            a = app_tick(self.s.app, n)
            self.s = replace(self.s, app=a, frame_no=self.s.frame_no + n)

    # the admission rules of RG-19
    def _apply(self, tx):
        s, k = self.s, self.keys
        dom = DOMAIN[type(tx)]
        if isinstance(tx, InputTx):
            if not k.ok("leaf_session", tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status != ACTIVE:
                return "SESSION_NOT_ACTIVE"
            if tx.epoch != s.resume_seq:
                return "STALE_EPOCH"
            if tx.nonce != s.nonce:
                return "BAD_NONCE"
            if self.wall - tx.signed_at > INPUT_TTL:
                return "EXPIRED"
            self.s = replace(s, app=app_apply(s.app, tx.ev), nonce=s.nonce + 1,
                             last_leaf_second=self.wall // FPS)
            return ""
        if isinstance(tx, ActionTx):
            if not k.ok("leaf_wallet", tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status == CLOSED:
                return "SESSION_NOT_ACTIVE"
            if tx.anonce != s.anonce:
                return "BAD_NONCE"
            if self.wall > tx.valid_until:
                return "EXPIRED"
            self.s = replace(s, vault=s.vault + tx.amount, anonce=s.anonce + 1)
            return ""
        if isinstance(tx, ReceiptTx):
            if not k.ok("leaf_session", tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status != ACTIVE:
                return "SESSION_NOT_ACTIVE"
            self.s = replace(s, last_leaf_second=max(s.last_leaf_second, tx.second))
            return ""
        if isinstance(tx, PauseTx):
            if not k.ok("leaf_session", tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status != ACTIVE:
                return "SESSION_NOT_ACTIVE"
            if tx.pause_seq != s.pause_seq + 1:
                return "PAUSE_UNKNOWN"
            if self.wall - s.last_resume_wall < PAUSE_MIN_GAP:
                return "PAUSE_RATE_LIMIT"
            root = s.app_root()
            self.s = replace(s, status=PAUSED, pause_seq=tx.pause_seq, paused_root=root,
                             paused_at_wall=self.wall,
                             unconfirmed=max(0, tx.last_frame - s.frame_no) if tx.last_frame > s.frame_no else 0)
            return ""
        if isinstance(tx, LapseTx):
            if tx.validator not in self.validators or \
               not k.ok(tx.validator, tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status != ACTIVE:
                return "SESSION_NOT_ACTIVE"
            if tx.pause_seq != s.pause_seq + 1:
                return "PAUSE_UNKNOWN"
            if tx.last_receipt_second != s.last_leaf_second:
                return "LAPSE_BAD_EVIDENCE"
            if self.wall // FPS - s.last_leaf_second < LAPSE_AFTER_S:
                return "LAPSE_TOO_EARLY"
            self.s = replace(s, status=LAPSED, pause_seq=tx.pause_seq,
                             paused_root=s.app_root(), paused_at_wall=self.wall)
            return ""
        if isinstance(tx, ResumeTx):
            if tx.signer not in ("leaf_session", "leaf_wallet") or \
               not k.ok(tx.signer, tx.sig, dom, *tx.fields()):
                return "BAD_SIGNATURE"
            if s.status not in (PAUSED, LAPSED):
                return "SESSION_NOT_PAUSED"
            if self.wall - s.paused_at_wall > PAUSE_TTL:
                self.s = replace(s, status=CLOSED)
                return "PAUSE_TTL_EXPIRED"
            if tx.pause_seq != s.pause_seq:
                return "PAUSE_UNKNOWN"
            if tx.resume_seq != s.resume_seq + 1:
                return "REPLAY"
            if tx.signer == "leaf_session" and self.wall > s.grant_until:
                return "GRANT_EXPIRED"
            if tx.expected_root != s.paused_root:
                return "RESUME_STATE_MISMATCH"
            grant = tx.new_grant_until if tx.signer == "leaf_wallet" and tx.new_grant_until else s.grant_until
            self.s = replace(s, status=ACTIVE, resume_seq=tx.resume_seq, grant_until=grant,
                             last_leaf_second=self.wall // FPS, last_resume_wall=self.wall)
            return ""
        return "UNKNOWN_TX"


# -------------------------------------------------------------------- U7 ---
class NVM:
    """A two-slot journal. A torn write leaves the old record readable.

    A record is valid only if its checksum holds. The reader takes the valid
    slot with the highest sequence number. Power can fail at four instants.
    """
    CRASH_POINTS = ("before", "partial", "complete")

    def __init__(self):
        self.slots = [None, None]       # (seq, payload bytes, crc)

    @staticmethod
    def _crc(seq, payload):
        return hashlib.sha256(seq.to_bytes(8, "little") + payload).digest()[:8]

    def _best(self):
        best = None
        for i, sl in enumerate(self.slots):
            if sl is None:
                continue
            seq, payload, crc = sl
            if crc == self._crc(seq, payload) and (best is None or seq > best[0]):
                best = (seq, i)
        return best

    def read(self):
        b = self._best()
        if b is None:
            return None
        return b[0], self.slots[b[1]][1]

    def write(self, payload, crash_at=None):
        """Write `payload` to the slot that is not current. Returns True if stored."""
        b = self._best()
        seq = b[0] + 1 if b else 1
        idx = (1 - b[1]) if b else 0
        if crash_at == "before":
            return False
        if crash_at == "partial":
            self.slots[idx] = (seq, payload[: len(payload) // 2], self._crc(seq, payload))
            return False
        self.slots[idx] = (seq, payload, self._crc(seq, payload))
        return crash_at is None


class U7:
    """The Leaf secure element, as far as RG-19 needs."""
    def __init__(self, keys, sid):
        self.keys, self.sid = keys, sid
        self.nvm = NVM()
        self.epoch = 0
        self.nonce = 0
        self.outbox = []              # signed ActionTx not yet acknowledged
        self.pause_seq = 0
        self.ring = []                # events shown and not yet acknowledged (RAM)

    def sign_input(self, ev, signed_at):
        tx = sign_tx(self.keys, InputTx(self.sid, self.epoch, self.nonce, signed_at, ev))
        self.nonce += 1
        self.ring.append(tx)
        return tx

    def sign_action(self, anonce, amount, valid_until, crash_at=None):
        """Write ahead: the action is in NVM before it is sent."""
        tx = sign_tx(self.keys, ActionTx(self.sid, anonce, amount, valid_until))
        rec = json.dumps(["action", anonce, amount, valid_until]).encode()
        stored = self.nvm.write(rec, crash_at=crash_at)
        if stored:
            self.outbox.append(tx)
            return tx
        return None

    def power_loss(self):
        """RAM goes. The NVM keeps the last valid record."""
        self.ring.clear()
        self.nonce = 0              # rebuilt from the chain at resume
        self.outbox = self._outbox_from_nvm()

    def _outbox_from_nvm(self):
        rec = self.nvm.read()
        if rec is None:
            return []
        t = json.loads(rec[1].decode())
        if t[0] != "action":
            return []
        return [sign_tx(self.keys, ActionTx(self.sid, t[1], t[2], t[3]))]

    def make_pause(self, last_frame, claimed_root, reason="HOST_LOST"):
        self.pause_seq += 1
        return sign_tx(self.keys, PauseTx(self.sid, self.pause_seq, reason, last_frame, claimed_root))

    def make_resume(self, ledger_state, signer="leaf_session", new_grant=0):
        """Resume what the chain records. The Leaf checks the record first."""
        s = ledger_state
        tx = ResumeTx(self.sid, s.pause_seq, s.resume_seq + 1, s.paused_root, signer, new_grant)
        self.epoch = s.resume_seq + 1
        self.nonce = s.nonce
        return sign_tx(self.keys, tx)


# -------------------------------------------------------------- replicas ---
class Replica:
    """A validator. It submits what it receives to the chain after `gossip` frames."""
    def __init__(self, name, ledger, gossip_frames, uplink=True):
        self.name, self.ledger, self.gossip = name, ledger, gossip_frames
        self.uplink = uplink
        self.alive = True
        self.held = []                 # (received_wall, tx) not yet submitted
        self.died_at = None

    def receive(self, wall, tx):
        if self.alive:
            self.held.append((wall, tx))
            if self.uplink:
                self.ledger.submit(wall + self.gossip, tx)

    def die(self, wall):
        """Transactions with submit time after `wall` never reach the chain."""
        self.alive = False
        self.died_at = wall
        if not self.uplink:
            return
        for w, tx in self.held:
            if w + self.gossip > wall:
                self._withdraw(w + self.gossip, tx)

    def _withdraw(self, at, tx):
        lst = self.ledger.pending.get(at, [])
        if tx in lst:
            lst.remove(tx)


def _poisson(rnd, lam):
    import math
    limit, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= rnd.random()
        if prod <= limit:
            return k
        k += 1


def open_second_loss(rnd, rate_hz, flush, cap_ms=2200.0, flush_ms=30.0, n_cuts=4000):
    """Events lost at a cut when the Leaf signs its input chain head once per second.

    The proto draft of the wire team tags each InputBatch with a KMAC and signs the
    chain head once per second in the Receipt. An event is chain-admissible only
    when a head covers it. A cut leaves the open second with no head, so its events
    are lost, unless U7 flushes a signed head on the host loss and the store lasts
    `flush_ms`. Returns the list of lost counts, one per cut.
    """
    out = []
    for _ in range(n_cuts):
        cut = rnd.random()                       # position of the cut in the open second
        times = [rnd.random() for _ in range(_poisson(rnd, rate_hz))]
        open_events = sum(1 for t in times if t < cut)
        out.append(0 if (flush and cap_ms >= flush_ms) else open_events)
    return out


def demo():
    keys = Keys(["leaf_session", "leaf_wallet", "val1", "val2"])
    led = Ledger("S1", keys)
    u7 = U7(keys, "S1")
    for i, f in enumerate((10, 50, 90)):
        led.submit(f, u7.sign_input(("tap",), f))
    led.run_to(200)
    pause = u7.make_pause(led.s.frame_no, led.s.app_root())
    led.submit(200, pause)
    led.run_to(300)
    print("paused:", led.s.status, "frame_no", led.s.frame_no, "balance", led.s.app.balance)
    led.run_to(300 + 3600 * FPS)
    print("after one hour:", led.s.status, "frame_no", led.s.frame_no)
    res = u7.make_resume(led.s)
    led.submit(led.wall, res)
    led.run_to(led.wall + 10)
    print("resumed:", led.s.status, "frame_no", led.s.frame_no, "rejects", led.rejects)


if __name__ == "__main__":
    demo()
