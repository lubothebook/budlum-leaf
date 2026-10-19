#!/usr/bin/env python3
"""skinauth.py - the trust model of the Split: a Core that signs, a Skin that shows.

TRUST seat of hw/core, block HP-2, study of revision L.7 candidate. The model
behind 01-THREAT-MODEL.md, 02-DESIGN-RULES.md and 03-GATE-MAP.md.

The Skin holds the emitters, a link and an identity. The Core holds U7, the
wallet and the radios. The question: does a stolen Skin hold nothing, and what
stops a Skin that lies? This file models:

  1. a Skin identity chip that signs pairing challenges and nothing else
  2. the SkinRecord, the generalisation of the HostRecord of hw/hostpower/trust
  3. pairing with two physical presses and a short authentication string
  4. a signed-transcript key exchange (X25519, HKDF) and an AEAD link
     (ChaCha20-Poly1305, RFC 8439) with a replay window
  5. the chain registry of pairings, with commitments and counters
  6. revocation, clone detection, guest Cores and a Skin that roams
  7. content classes, and the confirmation rule for a signature: what you
     see is what you sign when the surface is outside the trust boundary
  8. the cost of the AEAD in a minimal Skin decoder

The primitives are references for the model. Every physical number is
[HYPOTHESIS]. The wallet key of the real U7 is ML-DSA-87; the model signs
with ed25519 as a stand-in. ed25519 and the NVM come from
hw/hostpower/trust/hostauth.py, imported read only.

Run: python3 skinauth.py        the budgets and the policy
     python3 -m unittest discover -s tests
"""
import hashlib
import hmac
import math
import os
import struct
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hostpower", "trust"))
import hostauth as H  # noqa: E402  read only

# ================================================================ X25519 ===
_P = 2 ** 255 - 19


def x25519(k, u):
    """RFC 7748 section 5."""
    kb = bytearray(k)
    kb[0] &= 248
    kb[31] &= 127
    kb[31] |= 64
    k = int.from_bytes(kb, "little")
    x1 = int.from_bytes(u, "little") & ((1 << 255) - 1)
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (k >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a = (x2 + z2) % _P
        aa = a * a % _P
        b = (x2 - z2) % _P
        bb = b * b % _P
        e = (aa - bb) % _P
        c = (x3 + z3) % _P
        d = (x3 - z3) % _P
        da = d * a % _P
        cb = c * b % _P
        x3 = pow(da + cb, 2, _P)
        z3 = x1 * pow(da - cb, 2, _P) % _P
        x2 = aa * bb % _P
        z2 = e * (aa + 121665 * e) % _P
    if swap:
        x2, x3, z2, z3 = x3, x2, z3, z2
    return (x2 * pow(z2, _P - 2, _P) % _P).to_bytes(32, "little")


X_BASE = (9).to_bytes(32, "little")


def x25519_public(k):
    return x25519(k, X_BASE)


# ====================================================== HKDF and the AEAD ===
def hkdf(ikm, salt, info, n):
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    out, t = b"", b""
    i = 1
    while len(out) < n:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:n]


def _rotl(v, n):
    return ((v << n) & 0xFFFFFFFF) | (v >> (32 - n))


def _qr(s, a, b, c, d):
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 7)


def chacha_block(key, counter, nonce):
    init = (list(struct.unpack("<4I", b"expand 32-byte k")) +
            list(struct.unpack("<8I", key)) + [counter] +
            list(struct.unpack("<3I", nonce)))
    s = init[:]
    for _ in range(10):
        _qr(s, 0, 4, 8, 12)
        _qr(s, 1, 5, 9, 13)
        _qr(s, 2, 6, 10, 14)
        _qr(s, 3, 7, 11, 15)
        _qr(s, 0, 5, 10, 15)
        _qr(s, 1, 6, 11, 12)
        _qr(s, 2, 7, 8, 13)
        _qr(s, 3, 4, 9, 14)
    return struct.pack("<16I", *[(a + b) & 0xFFFFFFFF for a, b in zip(s, init)])


def chacha_xor(key, counter, nonce, data):
    out = bytearray()
    for i in range(0, len(data), 64):
        blk = chacha_block(key, counter + i // 64, nonce)
        out += bytes(x ^ y for x, y in zip(data[i:i + 64], blk))
    return bytes(out)


def poly1305(key, msg):
    r = int.from_bytes(key[:16], "little") & 0x0ffffffc0ffffffc0ffffffc0fffffff
    s = int.from_bytes(key[16:], "little")
    acc, p = 0, (1 << 130) - 5
    for i in range(0, len(msg), 16):
        n = int.from_bytes(msg[i:i + 16] + b"\x01", "little")
        acc = (acc + n) * r % p
    return ((acc + s) & ((1 << 128) - 1)).to_bytes(16, "little")


def _pad16(b):
    return b"\x00" * (-len(b) % 16)


def aead_seal(key, nonce, aad, pt):
    otk = chacha_block(key, 0, nonce)[:32]
    ct = chacha_xor(key, 1, nonce, pt)
    mac = poly1305(otk, aad + _pad16(aad) + ct + _pad16(ct) +
                   struct.pack("<QQ", len(aad), len(ct)))
    return ct + mac


def aead_open(key, nonce, aad, sealed):
    if len(sealed) < 16:
        return None
    ct, tag = sealed[:-16], sealed[-16:]
    otk = chacha_block(key, 0, nonce)[:32]
    mac = poly1305(otk, aad + _pad16(aad) + ct + _pad16(ct) +
                   struct.pack("<QQ", len(aad), len(ct)))
    if not hmac.compare_digest(mac, tag):
        return None
    return chacha_xor(key, 1, nonce, ct)


# ============================================================ constants ===
TAG_PAIR = b"BDLM_SKIN_PAIR_V1"          # a seventh and eighth tag for U7-3
TAG_SESSION = b"BDLM_SKIN_SESSION_V1"
TAG_ACK = b"BDLM_CORE_PAIR_ACK_V1"
TAG_CERT = b"BDLM_SKIN_VENDOR_CERT_V1"
TAG_CHAIN_PAIR = b"BDLM_LEAF_SKIN_PAIR_V1"
TAG_CHAIN_REVOKE = b"BDLM_LEAF_SKIN_REVOKE_V1"
TAG_SIGN = b"BDLM_LEAF_CONFIRMED_SIGN_V1"
TAG_CONFIRM = b"BDLM_LEAF_CONFIRM_DEVICE_V1"
TAG_ACCT = b"BDLM_LEAF_ACCOUNT_KEY_V1"

# tiers: what the Core trusts the Skin to do
S0, S1, S2 = 0, 1, 2
TIER_NAME = {S0: "S0 lock screen", S1: "S1 viewer", S2: "S2 owner Skin"}

# capability bits: what the Skin may carry for a Core
CAP_TOUCH, CAP_CAMERA, CAP_MIC, CAP_SPEAKER = 1, 2, 4, 8
CAP_DEFAULT = CAP_TOUCH | CAP_SPEAKER

# content classes of the screen
PUBLIC, PRIVATE, SECRET, TXSUM = "PUBLIC", "PRIVATE", "SECRET", "TXSUM"

# confirmation sources
SKIN_TAP, CORE_BUTTON, CONFIRM_DEVICE = "SKIN_TAP", "CORE_BUTTON", "CONFIRM_DEVICE"

IDLE_S = 5.0                 # a session silent this long can be replaced
SUITE_STRONG, SUITE_WEAK = 2, 1          # 1 stands for a legacy suite
SUITES_OFFERED = (SUITE_STRONG, SUITE_WEAK)
SUITE_FLOOR = SUITE_STRONG               # the Skin refuses anything below
DEADMAN_S = 0.1              # no valid slice for this long blanks the frame store
MAX_PINS = 4                 # pairing slots in a Skin, [HYPOTHESIS]
CONFIRM_TTL = 30             # seconds a confirmation lives
MIN_DWELL = 1.5              # seconds the summary shows before a press counts
DAY_BLOCKS = 14400           # one day of 6 s slots
ATTEST_MIN_GAP_S = 0.1       # the identity chip signs at most 10 times a second
TCB_PARTS = ("U7", "U4", "U1", "RDISP", "BUTTON")

_REC = ">B32s32sBBBQQ32s32s"
REC_LEN = struct.calcsize(_REC)
FRAME_LEN = REC_LEN + 64 + 64        # record, chip signature, vendor cert


class ParseError(ValueError):
    pass


class SkinRecord:
    """The HostRecord of Part 22, generalised. host_key becomes skin_key,
    class becomes tier, lanes become caps, the measured volts become the link
    transcript, and the record binds to one Core."""

    def __init__(self, core_key, skin_key, tier, caps, link_class, expiry,
                 counter, nonce, fw_digest, version=1):
        self.version, self.core_key, self.skin_key = version, core_key, skin_key
        self.tier, self.caps, self.link_class = tier, caps, link_class
        self.expiry, self.counter, self.nonce = expiry, counter, nonce
        self.fw_digest = fw_digest

    def pack(self):
        return struct.pack(_REC, self.version, self.core_key, self.skin_key,
                           self.tier, self.caps, self.link_class, self.expiry,
                           self.counter, self.nonce, self.fw_digest)

    def signing_bytes(self):
        return TAG_PAIR + self.pack()


def parse_frame(frame):
    """Bounded and fixed. Returns (SkinRecord, chip signature, vendor cert)."""
    if not isinstance(frame, (bytes, bytearray)) or len(frame) != FRAME_LEN:
        raise ParseError("length")
    f = struct.unpack(_REC, bytes(frame[:REC_LEN]))
    ver, ck, sk, tier, caps, lc, exp, ctr, nonce, fw = f
    if ver != 1:
        raise ParseError("version")
    if tier not in (S1, S2):
        raise ParseError("tier")
    if caps & ~0x0F or lc > 3:
        raise ParseError("caps or link class")
    return (SkinRecord(ck, sk, tier, caps, lc, exp, ctr, nonce, fw, ver),
            bytes(frame[REC_LEN:REC_LEN + 64]), bytes(frame[REC_LEN + 64:]))


def sas(core_key, skin_key, nonce_c):
    """The short authentication string, 6 digits, shown on both sides."""
    h = hashlib.sha256(b"BDLM_SAS_V1" + core_key + skin_key + nonce_c).digest()
    return "%06d" % (int.from_bytes(h[:4], "big") % 1_000_000)


# ================================================================ chain ===
class Chain:
    """The registry of pairings. It stores commitments, never a Skin serial."""

    def __init__(self):
        self.records = []
        self.latest = {}                       # wallet -> counter

    def post(self, kind, wallet_pub, commit, tier, epoch, ctr, expiry, sig):
        body = (kind + wallet_pub + commit + bytes([tier]) +
                struct.pack(">QQQ", epoch, ctr, expiry))
        if not H.ed_verify_strict(wallet_pub, body, sig):
            return "REFUSED: bad wallet signature"
        if ctr <= self.latest.get(wallet_pub, 0):
            return "REFUSED: counter not new"
        self.latest[wallet_pub] = ctr
        self.records.append((kind, wallet_pub, commit, tier, epoch, ctr, expiry))
        return "OK"

    def state_of(self, wallet_pub, commit):
        st = None
        for kind, w, c, tier, epoch, ctr, exp in self.records:
            if w == wallet_pub and c == commit:
                st = "PAIRED" if kind == TAG_CHAIN_PAIR else "REVOKED"
        return st


# =========================================================== the vendor ===
class Vendor:
    """The factory. It certifies a Skin identity key at provisioning (SW-16)."""

    def __init__(self, seed=b"vendor"):
        self._sk = hashlib.sha256(seed).digest()
        self.pub = H.ed_public(self._sk)

    def certify(self, skin_pub):
        return H.ed_sign(self._sk, TAG_CERT + skin_pub)


# ============================================================ the Skin ===
class SkinChip:
    """The identity chip of a Skin and its minimal decoder state.

    It signs challenges in two domains and nothing else. It holds a link key
    in RAM only. It never holds a wallet key and it cannot sign a value."""

    def __init__(self, seed, vendor=None, hardened=True, fw=b"skin-fw-1",
                 clock=lambda: 0.0):
        self._sk = hashlib.sha256(b"skin:" + seed).digest()
        self.pub = H.ed_public(self._sk)
        self.cert = vendor.certify(self.pub) if vendor else b"\x00" * 64
        self.hardened = hardened
        self.fw_digest = hashlib.sha256(fw).digest()
        self.pins = {}                  # core_key -> {caps, role, epoch}
        self.clock = clock
        self._last_attest = -1e9
        self.active = None              # the core_key of the live session
        self._eph = None
        self.send = self.recv = None
        self.residual = b""             # the last slice in the frame store
        self.counter = 0                # SkinRecord counter, in NVM

    # ------------------------------------------------------ the signer ---
    def attest(self, msg):
        if not (msg.startswith(TAG_PAIR) or msg.startswith(TAG_SESSION)):
            raise PermissionError("the chip signs pairing and session challenges only")
        now = self.clock()
        if now - self._last_attest < ATTEST_MIN_GAP_S:
            raise PermissionError("rate limit")
        self._last_attest = now
        return H.ed_sign(self._sk, msg)

    # -------------------------------------------------------- pairing ---
    def pair_respond(self, core_key, nonce_c, press, tier=S2, caps=CAP_DEFAULT,
                     expiry=10 ** 9):
        if not press:
            raise PermissionError("pairing needs a press on the Skin")
        self.counter += 1
        rec = SkinRecord(core_key, self.pub, tier, caps, 2, expiry, self.counter,
                         nonce_c, self.fw_digest)
        sig = self.attest(rec.signing_bytes())
        return rec.pack() + sig + self.cert, sas(core_key, self.pub, nonce_c)

    def pin(self, core_key, ack, nonce_c, match, press, role="GUEST",
            caps=CAP_DEFAULT):
        """Keep a Core. Needs a press, a matching SAS and a valid ack."""
        if not press or not match:
            raise PermissionError("pin needs a press and a matching SAS")
        epoch, tier = struct.unpack(">QB", ack[:9])
        sig = ack[9:]
        msg = TAG_ACK + nonce_c + self.pub + ack[:9]
        if not H.ed_verify_strict(core_key, msg, sig):
            raise PermissionError("bad ack")
        if len(self.pins) >= MAX_PINS and core_key not in self.pins:
            raise PermissionError("no free pairing slot")
        self.pins[core_key] = {"caps": caps, "role": role, "epoch": epoch}

    def enable_cap(self, core_key, cap, press):
        if not press:
            raise PermissionError("a capability needs a press on the Skin")
        self.pins[core_key]["caps"] |= cap

    def unpin_all(self, press):
        if not press:
            raise PermissionError("needs a press")
        self.pins.clear()
        self.active = None
        self.send = self.recv = None

    def strip(self):
        """The trusted strip: the fixed overlay the Core cannot draw over."""
        if self.active is None:
            return "NO CORE"
        return "CORE " + hashlib.sha256(self.active).hexdigest()[:8]

    # -------------------------------------------------------- session ---
    def hello(self, rng):
        self._eph = rng(32)
        self._nonce_s = rng(32)
        return x25519_public(self._eph), self._nonce_s, bytes(SUITES_OFFERED)

    def finish(self, core_key, core_hello, skin_hello):
        """Verify the Core, sign the transcript, derive the link keys."""
        if core_key not in self.pins:
            return None
        eph_c, nonce_c, chosen, sig_c = core_hello
        eph_s, nonce_s, offered = skin_hello
        if chosen not in offered or chosen < SUITE_FLOOR:
            return None
        tr = transcript(self.pub, core_key, eph_s, eph_c, nonce_s, nonce_c,
                        offered, chosen)
        if not H.ed_verify_strict(core_key, TAG_SESSION + b"core" + tr, sig_c):
            return None
        sig = self.attest(TAG_SESSION + b"skin" + tr)
        shared = x25519(self._eph, eph_c)
        self._eph = None
        c2s, s2c = derive(shared, tr)
        self.recv, self.send = End(c2s), End(s2c)
        self.active = core_key
        return sig

    # ------------------------------------------------------ the thief ---
    def readout(self, level):
        """What a thief gets. level: 'powered_off' or 'decap' (a lab)."""
        got = {"pinned_cores": sorted(k.hex() for k in self.pins),
               "vendor_cert": self.cert.hex()}
        if level == "decap":
            if not self.hardened:
                got["identity_key"] = self._sk.hex()
            got["residual_pixels"] = self.residual.hex()
        return got

    def rx(self, frame, now):
        """A slice arrives. A valid one refreshes the frame store."""
        if self.recv is None:
            return None
        pt = self.recv.open(frame)
        if pt is not None:
            self.residual = pt[-32:]
            self._last_rx = now
        return pt

    def tick(self, now):
        """The dead-man. With no valid slice for DEADMAN_S the frame store is
        blanked and the Skin shows its own fixed no-link pattern."""
        if self.recv is not None and now - getattr(self, "_last_rx", now) > DEADMAN_S:
            self.residual = b""
            return "NO LINK"
        return "LINK"

    def power_off(self):
        """Session keys and the frame store do not survive power loss."""
        self.send = self.recv = None
        self.active = None
        self._eph = None
        self.residual = b""


def transcript(skin_key, core_key, eph_s, eph_c, nonce_s, nonce_c,
               offered=b"", chosen=0):
    """Everything both sides said, including the offered suites and the choice.
    A downgrade changes the transcript, so the signatures fail."""
    return hashlib.sha256(b"BDLM_SKIN_TRANSCRIPT_V1" + skin_key + core_key +
                          eph_s + eph_c + nonce_s + nonce_c +
                          bytes([len(offered)]) + offered + bytes([chosen])).digest()


def derive(shared, tr):
    okm = hkdf(shared, tr, b"BDLM_SKIN_LINK_KEYS_V1", 64)
    return okm[:32], okm[32:]


class End:
    """One direction of the link: a key and a counter. Nonce = counter."""

    def __init__(self, key):
        self.key, self.n, self.last = key, 0, -1

    def seal(self, plain, aad=b""):
        self.n += 1
        nonce = b"\x00" * 4 + struct.pack(">Q", self.n)
        return struct.pack(">Q", self.n) + aead_seal(self.key, nonce, aad, plain)

    def open(self, frame, aad=b""):
        if len(frame) < 8 + 16:
            return None
        n = struct.unpack(">Q", frame[:8])[0]
        if n <= self.last:
            return None                       # replay or reorder
        nonce = b"\x00" * 4 + struct.pack(">Q", n)
        pt = aead_open(self.key, nonce, aad, frame[8:])
        if pt is not None:
            self.last = n
        return pt


# ============================================================ the Core ===
class Hardware:
    """The button and the trusted display. The Core software has no handle to
    the secret, so it cannot mint a press."""

    def __init__(self):
        self._secret = os.urandom(32)
        self._n = 0
        self._last = 0
        self.shown_hash = None
        self.shown_at = None

    def press(self):
        self._n += 1
        n = struct.pack(">Q", self._n)
        return n + hmac.new(self._secret, n, hashlib.sha256).digest()

    def verify(self, token):
        """A press counts once. The hardware keeps the last counter it saw."""
        if token is None or len(token) != 40:
            return False
        n = token[:8]
        if not hmac.compare_digest(token[8:], hmac.new(self._secret, n, hashlib.sha256).digest()):
            return False
        v = struct.unpack(">Q", n)[0]
        if v <= self._last:
            return False
        self._last = v
        return True

    def show(self, summary, now):
        """The U1 ROM path draws the summary on the rear panel."""
        self.shown_hash = hashlib.sha256(summary).digest()
        self.shown_at = now


class Session:
    def __init__(self, skin_key, tier, caps, send, recv):
        self.skin_key, self.tier, self.caps = skin_key, tier, caps
        self.send, self.recv = send, recv       # Core seals with send
        self.live = True
        self.last_seen = 0.0


class Core:
    """The part of U7 that judges a Skin and a signature."""

    def __init__(self, vendor_pub, wallet_seed=b"wallet", chain=None,
                 rng=os.urandom, anchor=1000, hw=None, parts=None,
                 blind_budget=100, nvm=None):
        self.vendor_pub = vendor_pub
        self._wallet = hashlib.sha256(b"wallet:" + wallet_seed).digest()
        self.wallet_pub = H.ed_public(self._wallet)
        self._core = hashlib.sha256(b"core:" + wallet_seed).digest()
        self.core_pub = H.ed_public(self._core)
        self.chain = chain if chain is not None else Chain()
        self.rng = rng
        self.anchor = anchor
        self.hw = hw if hw is not None else Hardware()
        self.nvm = nvm if nvm is not None else H.NVM()
        self.blind_budget = blind_budget
        self.fw_list = set()                 # listed decoder firmware digests
        self.min_suite = SUITE_STRONG        # the downgrade floor, in NVM in a product
        self.distance = "C0"                  # the distance class of the Skin link
        parts = parts or {p: hashlib.sha256(p.encode()).digest() for p in
                          ("U7", "U4", "U1", "RDISP", "BUTTON", "U2A", "U6")}
        if self.nvm.read() is None:
            self.nvm.commit({"skins": {}, "epoch": 0, "chain_ctr": 0,
                             "parts": {k: v.hex() for k, v in parts.items()},
                             "tcb_ok": True, "spent": {"day": 0, "amount": 0},
                             "skin_ctr": {}})
        self.power_cycle()

    # ------------------------------------------------------------ RAM ---
    def power_cycle(self):
        self.sessions = {}
        self._pair = None
        self._accepted = None
        self._pending = {}
        self.unlocked_until = -1
        self._hs = {}

    @property
    def state(self):
        return self.nvm.read()

    def _button(self, token):
        return self.hw.verify(token)

    def _sign_wallet(self, body):
        return H.ed_sign(self._wallet, body)

    # ------------------------------------------------------ the unlock ---
    def unlock(self, token, now, ttl=600):
        """The owner unlocks on the Core's own path, never through a Skin."""
        if not self._button(token):
            return False
        self.unlocked_until = now + ttl
        return True

    def unlocked(self, now):
        return now < self.unlocked_until

    # --------------------------------------------------------- pairing ---
    def pair_challenge(self, token):
        if not self._button(token):
            raise PermissionError("pairing needs the button of the Core")
        nonce = self.rng(32)
        self._pair = {"nonce": nonce, "rec": None}
        return nonce, self.core_pub

    def pair_accept(self, frame):
        """Judge a SkinRecord. Returns (verdict, SAS). A pass is pending until
        the owner confirms the SAS with a second press."""
        p, self._pair = self._pair, None
        self._accepted = None
        if p is None:
            return "REFUSED: no open challenge", None
        try:
            rec, sig, cert = parse_frame(frame)
        except ParseError as e:
            return f"REFUSED: parse {e}", None
        if rec.nonce != p["nonce"]:
            return "REFUSED: nonce mismatch", None
        if rec.core_key != self.core_pub:
            return "REFUSED: record names another Core", None
        if not H.ed_verify_strict(rec.skin_key, rec.signing_bytes(), sig):
            return "REFUSED: bad signature", None
        s = self.state
        if rec.counter <= s["skin_ctr"].get(rec.skin_key.hex(), 0):
            return "REFUSED: replayed counter", None
        if rec.expiry <= self.anchor:
            return "REFUSED: expired", None
        tier = rec.tier
        note = "OK"
        if not H.ed_verify_strict(self.vendor_pub, TAG_CERT + rec.skin_key, cert):
            tier, note = S1, "uncertified Skin: viewer tier at most"
        if tier == S2 and not self._fw_listed(rec.fw_digest):
            tier, note = S1, "unlisted decoder firmware: viewer tier at most"
        self._accepted = {"rec": rec, "tier": tier, "nonce": p["nonce"]}
        return note, sas(self.core_pub, rec.skin_key, p["nonce"])

    def _fw_listed(self, digest):
        return digest in self.fw_list or not self.fw_list

    def pair_commit(self, user_match, token):
        """The second press. The owner has compared the two SAS strings."""
        p, self._accepted = getattr(self, "_accepted", None), None
        if p is None:
            return None
        if not user_match or not self._button(token):
            return None
        rec, tier = p["rec"], p["tier"]
        s = self.state
        salt = self.rng(16)
        commit = hashlib.sha256(rec.skin_key + salt).digest()
        s["skin_ctr"][rec.skin_key.hex()] = rec.counter
        s["chain_ctr"] += 1
        s["skins"][rec.skin_key.hex()] = {
            "commit": commit.hex(), "salt": salt.hex(), "tier": tier,
            "caps": rec.caps & CAP_DEFAULT, "status": "ACTIVE"}
        self.nvm.commit(s)
        body = (TAG_CHAIN_PAIR + self.wallet_pub + commit + bytes([tier]) +
                struct.pack(">QQQ", s["epoch"], s["chain_ctr"], rec.expiry))
        self.chain.post(TAG_CHAIN_PAIR, self.wallet_pub, commit, tier,
                        s["epoch"], s["chain_ctr"], rec.expiry, self._sign_wallet(body))
        ack = struct.pack(">QB", s["epoch"], tier)
        sig = H.ed_sign(self._core, TAG_ACK + p["nonce"] + rec.skin_key + ack)
        return ack + sig

    # --------------------------------------------------------- revoke ---
    def revoke(self, skin_key, token):
        """A key operation: the Core button only."""
        if not self._button(token):
            raise PermissionError("revocation needs the button of the Core")
        s = self.state
        e = s["skins"].get(skin_key.hex())
        if e is None:
            return "UNKNOWN"
        e["status"] = "REVOKED"
        s["epoch"] += 1
        s["chain_ctr"] += 1
        self.nvm.commit(s)
        commit = bytes.fromhex(e["commit"])
        body = (TAG_CHAIN_REVOKE + self.wallet_pub + commit + bytes([e["tier"]]) +
                struct.pack(">QQQ", s["epoch"], s["chain_ctr"], 0))
        self.chain.post(TAG_CHAIN_REVOKE, self.wallet_pub, commit, e["tier"],
                        s["epoch"], s["chain_ctr"], 0, self._sign_wallet(body))
        sess = self.sessions.pop(skin_key, None)
        if sess:
            sess.live = False
        return "REVOKED"

    def drop(self, skin_key):
        """The link ended. The session goes."""
        sess = self.sessions.pop(skin_key, None)
        if sess:
            sess.live = False
        if not self.sessions:
            self.unlocked_until = -1          # a lost link locks the Core

    def reinstate(self, skin_key, token):
        if not self._button(token):
            raise PermissionError("needs the button of the Core")
        s = self.state
        e = s["skins"][skin_key.hex()]
        if e["status"] == "SUSPECT":
            e["status"] = "ACTIVE"
            self.nvm.commit(s)

    def enable_cap(self, skin_key, cap, token):
        """The Core side of a camera or microphone lane: the button."""
        if not self._button(token):
            raise PermissionError("a capability needs the button of the Core")
        s = self.state
        s["skins"][skin_key.hex()]["caps"] |= cap
        self.nvm.commit(s)

    # -------------------------------------------------------- session ---
    def hello(self, skin_key, skin_hello, now=0.0):
        """First half of the key exchange. Refuses a Skin that is not active."""
        e = self.state["skins"].get(skin_key.hex())
        if e is None:
            return "REFUSED: unknown Skin"
        if e["status"] == "REVOKED":
            return "REFUSED: revoked Skin"
        if e["status"] == "SUSPECT":
            return "REFUSED: suspect Skin, re-pair or reinstate"
        old = self.sessions.get(skin_key)
        if old is not None and old.live and now - old.last_seen > IDLE_S:
            old.live = False                  # a link that dropped, not a clone
            del self.sessions[skin_key]
            old = None
        if old is not None and old.live:
            # two live sessions under one identity: a clone
            old.live = False
            del self.sessions[skin_key]
            s = self.state
            s["skins"][skin_key.hex()]["status"] = "SUSPECT"
            self.nvm.commit(s)
            return "REFUSED: clone alert, both sessions dropped"
        eph_s, nonce_s, offered = skin_hello
        common = [x for x in offered if x in (SUITE_STRONG, SUITE_WEAK) and x >= self.min_suite]
        if not common:
            return "REFUSED: no suite at or above the floor"
        chosen = max(common)
        eph = self.rng(32)
        nonce_c = self.rng(32)
        eph_c = x25519_public(eph)
        tr = transcript(skin_key, self.core_pub, eph_s, eph_c, nonce_s, nonce_c,
                        bytes(offered), chosen)
        sig = H.ed_sign(self._core, TAG_SESSION + b"core" + tr)
        self._hs[skin_key] = (eph, eph_s, tr)
        return (eph_c, nonce_c, chosen, sig)

    def finish(self, skin_key, sig_skin, now=0.0):
        eph, eph_s, tr = self._hs.pop(skin_key, (None, None, None))
        if eph is None:
            return None
        if not H.ed_verify_strict(skin_key, TAG_SESSION + b"skin" + tr, sig_skin):
            return None
        shared = x25519(eph, eph_s)
        c2s, s2c = derive(shared, tr)
        e = self.state["skins"][skin_key.hex()]
        sess = Session(skin_key, e["tier"], e["caps"], End(c2s), End(s2c))
        sess.last_seen = now
        self.sessions[skin_key] = sess
        return sess

    # ----------------------------------------------------- the screen ---
    def compose(self, items, skin_key, now):
        """What goes into the pixel stream for one Skin. SECRET never does."""
        sess = self.sessions.get(skin_key)
        if sess is None or not sess.live:
            return []
        eff = sess.tier if self.unlocked(now) else S0
        out = []
        for cls, text in items:
            if cls == SECRET:
                out.append((cls, "[shown on the Core only]"))
            elif cls == PUBLIC and eff >= S1:
                out.append((cls, text))
            elif cls in (PRIVATE, TXSUM) and eff >= S2:
                out.append((cls, text))
        if eff == S0:
            return [(PUBLIC, "locked")]
        return out

    # ------------------------------------------------- the confirmation ---
    @staticmethod
    def summarise(tx):
        """The Core derives the summary from the transaction bytes itself."""
        return (b"SEND " + str(tx["amount"]).encode() + b" TO " +
                tx["to"].hex().encode() + b" FEE " + str(tx.get("fee", 0)).encode())

    def request_sign(self, kind, tx, now):
        if kind == "INPUT" and any(k in tx for k in ("amount", "to", "fee")):
            return "REFUSED: an input batch carries no value"
        if kind == "VALUE" and not self.state["tcb_ok"]:
            return "REFUSED: a trusted part changed, owner must confirm"
        if kind == "KEYOP" and not self.state["tcb_ok"]:
            return "REFUSED: a trusted part changed, owner must confirm"
        summary = self.summarise(tx) if kind == "VALUE" else repr(sorted(tx.items())).encode()
        rid = self.rng(8).hex()
        self._pending[rid] = {"kind": kind, "tx": tx, "summary": summary,
                              "dnonce": self.rng(16),
                              "hash": hashlib.sha256(summary).digest(), "t": now,
                              "used": False}
        if kind in ("VALUE", "KEYOP"):
            self.hw.show(summary, now)       # the trusted display path
        return rid

    def _budget_left(self, now):
        s = self.state
        day = int(self.anchor // DAY_BLOCKS)
        if s["spent"]["day"] != day:
            return self.blind_budget
        return self.blind_budget - s["spent"]["amount"]

    def pair_confirm_device(self, dev_pub, token):
        """Pin a confirmation device: a separate part with its own button and
        display. Needs the button of the Core."""
        if not self._button(token):
            raise PermissionError("pairing a confirmation device needs the button")
        s = self.state
        s.setdefault("devices", []).append(dev_pub.hex())
        self.nvm.commit(s)

    def confirm_blob(self, rid):
        """What the Core sends to the confirmation device: the summary that the
        Core derived, and a nonce."""
        req = self._pending[rid]
        return req["summary"], req["dnonce"]

    def confirm(self, rid, source, now, token=None, skin_key=None,
                presented_hash=None, device_pub=None, device_sig=None):
        """The rule. A tap never confirms a key operation or a large value."""
        req = self._pending.get(rid) if isinstance(rid, str) else None
        if req is None or req["used"]:
            return "REFUSED: no such request or already used"
        if now - req["t"] > CONFIRM_TTL:
            return "REFUSED: confirmation expired"
        kind = req["kind"]
        if kind == "INPUT":
            sess = self.sessions.get(skin_key)
            if source != SKIN_TAP or sess is None or not sess.live:
                return "REFUSED: no live Skin session"
            if sess.tier < S2 or not self.unlocked(now):
                return "REFUSED: tier or lock"
            return self._finish(req)
        amount = req["tx"].get("amount", 0) if kind == "VALUE" else None
        if source == SKIN_TAP:
            sess = self.sessions.get(skin_key)
            if (kind == "VALUE" and sess is not None and sess.live and
                    sess.tier >= S2 and self.unlocked(now) and
                    amount <= self._budget_left(now)):
                s = self.state
                day = int(self.anchor // DAY_BLOCKS)
                if s["spent"]["day"] != day:
                    s["spent"] = {"day": day, "amount": 0}
                s["spent"]["amount"] += amount
                self.nvm.commit(s)
                return self._finish(req)
            return "REFUSED: a tap cannot confirm this"
        if source == CONFIRM_DEVICE:
            if device_pub is None or device_pub.hex() not in self.state.get("devices", []):
                return "REFUSED: not a paired confirmation device"
            if not H.ed_verify_strict(device_pub, TAG_CONFIRM + req["hash"] + req["dnonce"],
                                      device_sig or b"\x00" * 64):
                return "REFUSED: the device did not confirm this request"
            return self._finish(req)
        if source == CORE_BUTTON:
            if self.distance != "C0":
                return "REFUSED: the button of the Core is out of reach at this distance"
            if presented_hash is not None and presented_hash != req["hash"]:
                return "REFUSED: the hash is not the request"
            if self.hw.shown_hash != req["hash"]:
                return "REFUSED: the trusted display did not show this request"
            if now - self.hw.shown_at < MIN_DWELL:
                return "REFUSED: the summary was not shown long enough"
            if not self._button(token):
                return "REFUSED: no hardware press"
            return self._finish(req)
        return "REFUSED: unknown source"

    def _finish(self, req):
        req["used"] = True
        body = TAG_SIGN + req["hash"] + struct.pack(">Q", self.state["chain_ctr"])
        return ("SIGNED", self._sign_wallet(body), req["hash"])

    # --------------------------------------------------- the parts (L9) ---
    def measure(self, parts):
        """Compare the measured parts with the pinned record. A trusted part
        that changed locks signing until the owner confirms with the button."""
        s = self.state
        changed = [k for k, v in parts.items() if s["parts"].get(k) != v.hex()]
        tcb = [k for k in changed if k in TCB_PARTS]
        if tcb:
            s["tcb_ok"] = False
            self.nvm.commit(s)
        return changed, tcb

    def ack_config(self, parts, token):
        if not self._button(token):
            raise PermissionError("needs the button of the Core")
        s = self.state
        s["parts"] = {k: v.hex() for k, v in parts.items()}
        s["tcb_ok"] = True
        self.nvm.commit(s)


class ConfirmDevice:
    """A separate trusted part with its own button and display, for the
    distances where the button of the Core is out of reach. It can be a Leaf
    with its own U7 (the local floor of L.6.0 is its display). It signs only a
    hash that it showed."""

    def __init__(self, seed=b"dev"):
        self._sk = hashlib.sha256(b"device:" + seed).digest()
        self.pub = H.ed_public(self._sk)
        self.hw = Hardware()

    def confirm(self, summary, dnonce, t_show, t_press):
        self.hw.show(summary, t_show)
        tok = self.hw.press()
        if t_press - self.hw.shown_at < MIN_DWELL or not self.hw.verify(tok):
            return None
        return H.ed_sign(self._sk, TAG_CONFIRM + self.hw.shown_hash + dnonce)


class Account:
    """The chain side of one account with several device keys (SW-15). The
    model assumes the chain can hold a spending cap per key. [HYPOTHESIS]"""

    def __init__(self, root_pub):
        self.keys = {root_pub: {"cap": None, "revoked": False, "spent": {}}}
        self.ctr = 0

    def _body(self, tag, pub, a, b):
        return tag + pub + struct.pack(">QQ", a, b)

    def add(self, signer, pub, cap, ctr, sig):
        k = self.keys.get(signer)
        if k is None or k["revoked"] or k["cap"] is not None or ctr <= self.ctr:
            return "REFUSED"
        if not H.ed_verify_strict(signer, self._body(TAG_ACCT + b"add", pub, cap, ctr), sig):
            return "REFUSED"
        self.ctr = ctr
        self.keys[pub] = {"cap": cap, "revoked": False, "spent": {}}
        return "OK"

    def revoke(self, signer, pub, ctr, sig):
        k = self.keys.get(signer)
        if k is None or k["revoked"] or k["cap"] is not None or ctr <= self.ctr:
            return "REFUSED"
        if not H.ed_verify_strict(signer, self._body(TAG_ACCT + b"rev", pub, 0, ctr), sig):
            return "REFUSED"
        self.ctr = ctr
        self.keys[pub]["revoked"] = True
        return "OK"

    def spend(self, pub, amount, day, sig):
        k = self.keys.get(pub)
        if k is None or k["revoked"]:
            return "REFUSED: unknown or revoked key"
        if not H.ed_verify_strict(pub, self._body(TAG_ACCT + b"spend", pub, amount, day), sig):
            return "REFUSED: bad signature"
        used = k["spent"].get(day, 0)
        if k["cap"] is not None and used + amount > k["cap"]:
            return "REFUSED: over the cap of this key"
        k["spent"][day] = used + amount
        return "OK"


def trust_model(c):
    """Which trust model holds at each distance class. [HYPOTHESIS]"""
    if c not in ("C0", "C1", "C2"):
        raise ValueError(c)
    near = c in ("C0", "C1")
    return {
        "wallet_in": "Core U7" if near else "Leaf U7, as L.6.0",
        "skin_zero_key": near,
        "surface_in_boundary": not near,
        "core_button_reachable": c == "C0",
        "confirm_sources": (
            {"C0": (CORE_BUTTON, CONFIRM_DEVICE), "C1": (CONFIRM_DEVICE,),
             "C2": ("LEAF_LOCAL_FLOOR",)}[c]),
        "tap_value_authority": "blind budget only" if near else "local floor only",
        "far_end_authority": ("none, a Skin" if near else "none, a validator"),
        "pixel_cipher": ("AEAD Core to Skin" if near else "AEAD validator to U6"),
    }


# the SW-24 ceilings of fw/u7 session.rs, microseconds, and the margin inside
RTT_CEIL_US = {"room": 3100, "metro": 5000, "cell": 4900}
MARGIN_US = 1000
FIBRE_KM_PER_MS = 200.0


def fibre_slack_km(margin_us=MARGIN_US):
    """A round trip margin hides this much extra one-way fibre. A relay or a
    validator can stand this much farther than the class says. Light is slow
    in glass, so an RTT proof only ever bounds distance from above."""
    return margin_us / 1000.0 * FIBRE_KM_PER_MS / 2


def rtt_class(rtt_us, bearer, uwb_ok):
    if uwb_ok and rtt_us <= RTT_CEIL_US["room"]:
        return "room"
    ceil, name = ((RTT_CEIL_US["metro"], "metro") if bearer == "wifi"
                  else (RTT_CEIL_US["cell"], "cell"))
    return name if rtt_us <= ceil else "far"


# ================================================================ glue ===
def pair(core, skin, hw_press_core=True, hw_press_skin=True, user_match=None,
         role="OWNER", relay=None):
    """The whole pairing, in process. relay lets a test sit in the middle."""
    tok = core.hw.press() if hw_press_core else None
    nonce, ck = core.pair_challenge(tok)
    if relay:
        nonce, ck = relay.to_skin(nonce, ck)
    frame, skin_sas = skin.pair_respond(ck, nonce, hw_press_skin)
    if relay:
        frame = relay.to_core(frame)
    verdict, core_sas = core.pair_accept(frame)
    if core_sas is None:
        return verdict, None, None
    match = (core_sas == skin_sas) if user_match is None else user_match
    ack = core.pair_commit(match, core.hw.press())
    if ack is None:
        return "REFUSED: owner did not confirm the SAS", None, (core_sas, skin_sas)
    skin.pin(ck, ack, nonce, match, hw_press_skin, role=role)
    return verdict, ack, (core_sas, skin_sas)


def effective_caps(core, skin):
    """A lane opens only when the Core and the Skin both allow it."""
    e = core.state["skins"].get(skin.pub.hex())
    pin = skin.pins.get(core.core_pub)
    if e is None or pin is None:
        return 0
    return e["caps"] & pin["caps"]


def connect(core, skin, rng, mitm=None, now=0.0):
    """The session key exchange. mitm(name, msg) can alter a message in flight."""
    sh = skin.hello(rng)
    wire = mitm("skin_hello", sh) if mitm else sh
    ch = core.hello(skin.pub, wire, now)
    if isinstance(ch, str):
        return ch, None
    wire = mitm("core_hello", ch) if mitm else ch
    sig = skin.finish(core.core_pub, wire, sh)
    if sig is None:
        return "REFUSED: the Skin refused the Core", None
    if mitm:
        sig = mitm("skin_sig", sig)
    sess = core.finish(skin.pub, sig, now)
    if sess is None:
        return "REFUSED: the Core refused the Skin signature", None
    return "OK", sess


# ===================================================== the AEAD budget ===
def slice_time_us(hz=240, rows=3200, slice_rows=16):
    return 1e6 / hz * slice_rows / rows


def aead_budget(rate_gbps, slice_rows=16, engine_gbps=51.2,
                pj_per_bit=(0.5, 1.0, 2.0, 5.0)):
    """What the link cipher costs a minimal Skin decoder. [HYPOTHESIS]
    engine_gbps: one pipelined 128 bit datapath at 400 MHz. pj_per_bit is a
    sweep, not a measurement. The tag is checked per slice, so a slice is
    held until its tag passes."""
    t_us = slice_time_us(slice_rows=slice_rows)
    slice_bytes = rate_gbps * 1e9 / 8 * t_us * 1e-6
    slices_per_s = 240 * 3200 / slice_rows
    return {
        "rate_Gbps": rate_gbps,
        "slice_us": t_us,
        "slice_bytes": slice_bytes,
        "buffer_KiB": slice_bytes / 1024,
        "latency_added_us": t_us,
        "engines": math.ceil(rate_gbps / engine_gbps),
        "tag_overhead_pct": 16 / slice_bytes * 100,
        "power_mW": {pj: rate_gbps * 1e9 * pj * 1e-12 * 1e3 for pj in pj_per_bit},
        "slices_per_s": slices_per_s,
        "hours_to_2_32_slices": 2 ** 32 / slices_per_s / 3600,
    }


def report():
    print("THE FRAME")
    print(f"  SkinRecord {REC_LEN} B + chip signature 64 B + vendor cert 64 B = {FRAME_LEN} B")
    print("\nTHE LINK CIPHER IN A MINIMAL SKIN DECODER (slice of 16 rows, 240 Hz)")
    for r in (6.1, 9.2, 12.3):
        b = aead_budget(r)
        pw = ", ".join(f"{pj:g} pJ/bit {v:5.1f} mW" for pj, v in b["power_mW"].items())
        print(f"  {r:5.1f} Gbit/s: slice {b['slice_us']:.1f} us, buffer {b['buffer_KiB']:6.1f} KiB, "
              f"tag {b['tag_overhead_pct']:.4f} %, engines {b['engines']}; {pw}")
    b = aead_budget(12.3)
    print(f"  slices per second {b['slices_per_s']:.0f}; 2^32 slices after "
          f"{b['hours_to_2_32_slices']:.1f} h, so rekey every hour")
    print("\nWHAT A STOLEN SKIN GIVES (model readout)")
    v = Vendor()
    for hardened in (True, False):
        s = SkinChip(b"demo", v, hardened=hardened)
        s.residual = b"last slice"
        print(f"  hardened={hardened}: powered off -> {sorted(s.readout('powered_off'))}; "
              f"decap -> {sorted(s.readout('decap'))}")


if __name__ == "__main__":
    report()
