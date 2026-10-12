"""Budlum Leaf slice authentication: the Python reference model.

Roles:
  Validator  - renders, slices, tags every slice, signs a per-second Merkle root.
  U7         - the wallet secure element: the handshake, the validator-set check,
               the key load into U6, the root check and the countersigned receipt.
  U6Checker  - the line-rate checker. Bit-exact model of hdl/slice_auth.py.

There is no session cipher (Ayaz, FINAL/21.5.4). The payload is sent in clear.
Only authenticity, freshness and the validator's identity are proven.
"""
import hashlib
import struct

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, mldsa, mlkem, x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.exceptions import InvalidSignature

from keccak import sha3_256, kmac128, kmac128_prefix_state, keccak_f, bytes_to_lanes

VERSION = 1
SLICE_CUSTOM = b"BLF-SLICE-v1"
MAX_PAYLOAD = 65536          # bytes, one ingress slice buffer
HDR_LEN = 32
TAG_LEN = 16

# error codes, shared with the RTL
OK, BAD_TAG, REPLAY, NO_KEY, LENGTH, BAD_VERSION = range(6)
ERR_NAME = {OK: "OK", BAD_TAG: "BAD_TAG", REPLAY: "REPLAY", NO_KEY: "NO_KEY",
            LENGTH: "LENGTH", BAD_VERSION: "BAD_VERSION"}

# header flags
F_SLOT = 1 << 0        # key slot of the sender: 0 primary, 1 shadow
F_LAST = 1 << 1        # last slice of the frame
F_SPEC = 1 << 2        # speculative layer
F_INTRA = 1 << 3       # intra-refresh slice


def H(*parts):
    return hashlib.sha3_256(b"".join(parts)).digest()


# --------------------------------------------------------------------------
# the slice
# --------------------------------------------------------------------------

def pack_header(flags, slice_index, seq, frame_no, payload_len, y0, layer, version=VERSION):
    return struct.pack("<HHIQQIHH", version, flags, slice_index, seq, frame_no,
                       payload_len, y0, layer)


def unpack_header(h):
    v, fl, si, seq, fn, pl, y0, layer = struct.unpack("<HHIQQIHH", h)
    return dict(version=v, flags=fl, slice_index=si, seq=seq, frame_no=fn,
                payload_len=pl, y0=y0, layer=layer)


def pad8(b):
    return b + bytes((-len(b)) % 8)


def slice_digest(sid, header, payload):
    """d = SHA3-256(sid || header || payload padded to 8 bytes). Keyless, public."""
    return sha3_256(sid + header + pad8(payload))


def slice_tag(key, digest):
    return kmac128(key, digest, 128, SLICE_CUSTOM)


def make_slice(key, sid, flags, slice_index, seq, frame_no, payload, y0=0, layer=0):
    hdr = pack_header(flags, slice_index, seq, frame_no, len(payload), y0, layer)
    d = slice_digest(sid, hdr, payload)
    return hdr + pad8(payload) + slice_tag(key, d), d


def wire_words(wire):
    return [int.from_bytes(wire[i:i + 8], "little") for i in range(0, len(wire), 8)]


# --------------------------------------------------------------------------
# the U6 checker, bit-exact with the RTL
# --------------------------------------------------------------------------

class U6Checker:
    """Words in, one verdict per slice out. Mirrors hdl/slice_auth.py."""

    def __init__(self):
        self.sid = bytes(16)
        self.prefix = [None, None]   # KMAC128 prefix lane state per key slot
        self.last_seq = 0

    def load(self, slot, sid, prefix_lanes):
        self.sid = sid
        self.prefix[slot] = list(prefix_lanes)

    def clear(self, slot):
        self.prefix[slot] = None

    def check(self, words):
        """words: the u64 words of one wire slice; the last one carries in_last."""
        hdr = b"".join(w.to_bytes(8, "little") for w in words[:4]) if len(words) >= 4 else None
        if hdr is None:
            return dict(err=LENGTH)
        h = unpack_header(hdr)
        m = (h["payload_len"] + 7) // 8
        if h["payload_len"] > MAX_PAYLOAD or len(words) != 4 + m + 2:
            return dict(err=LENGTH)
        if h["version"] != VERSION:
            return dict(err=BAD_VERSION)
        slot = h["flags"] & F_SLOT
        body = b"".join(w.to_bytes(8, "little") for w in words[:4 + m])
        d = sha3_256(self.sid + body)
        res = dict(digest=d, seq=h["seq"], frame_no=h["frame_no"],
                   slice_index=h["slice_index"], flags=h["flags"])
        if self.prefix[slot] is None:
            return dict(res, err=NO_KEY)
        st = list(self.prefix[slot])
        blk = bytearray(168)
        blk[:32] = d
        blk[32:35] = b"\x80\x01\x04"     # right_encode(128) then the cSHAKE pad
        blk[167] ^= 0x80
        for i, v in enumerate(bytes_to_lanes(bytes(blk))):
            st[i] ^= v
        st = keccak_f(st)
        tag = st[0].to_bytes(8, "little") + st[1].to_bytes(8, "little")
        rx = words[-2].to_bytes(8, "little") + words[-1].to_bytes(8, "little")
        if tag != rx:
            return dict(res, err=BAD_TAG)
        if h["seq"] <= self.last_seq:
            return dict(res, err=REPLAY)
        self.last_seq = h["seq"]
        return dict(res, err=OK)


# --------------------------------------------------------------------------
# the frame hash and the per-second Merkle root
# --------------------------------------------------------------------------

def frame_hash(sid, frame_no, digests):
    return H(b"BLF-FRAME-v1", sid, struct.pack("<QI", frame_no, len(digests)), *digests)


def merkle_root(leaves):
    level = [H(b"\x00", f) for f in leaves]
    if not level:
        return bytes(32)
    while len(level) > 1:
        nxt = [H(b"\x01", level[i], level[i + 1]) for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])        # an odd node is promoted, not duplicated
        level = nxt
    return level[0]


def root_message(sid, second, first_frame, frame_hashes):
    return (b"BLF-ROOT-v1" + sid + struct.pack("<QQI", second, first_frame, len(frame_hashes))
            + merkle_root(frame_hashes))


def receipt_message(sid, second, root, validator_addr, root_sig_ed, rtt_us, shown):
    return (b"BLF-RCPT-v1" + sid + struct.pack("<Q", second) + root + validator_addr
            + H(root_sig_ed) + struct.pack("<II", rtt_us, shown))


# --------------------------------------------------------------------------
# the validator set, as U7 keeps it from finality proofs
# --------------------------------------------------------------------------

class ValidatorSet:
    """Mirror of core/account.rs::Validator. Address = Ed25519 public key [TREE]."""

    def __init__(self, epoch):
        self.epoch = epoch
        self.v = {}

    def add(self, ed_pub, pq_pub, active=True, slashed=False, jailed=False, roles=(1,)):
        self.v[ed_pub] = dict(pq=pq_pub, active=active, slashed=slashed,
                              jailed=jailed, roles=set(roles))

    def is_active_validator(self, ed_pub, pq_pub):
        r = self.v.get(ed_pub)
        return bool(r and r["active"] and not r["slashed"] and not r["jailed"]
                    and 1 in r["roles"] and r["pq"] == pq_pub)


# --------------------------------------------------------------------------
# the handshake: ML-KEM-768 + X25519 hybrid, Ed25519 + ML-DSA-87 signatures
# --------------------------------------------------------------------------

def transcript(ch, sh):
    return H(b"BLF-HS-v1", ch["x_pub"], ch["kem_pub"], ch["nonce"], ch["app"],
             struct.pack("<Q", ch["epoch"]), ch["sid_bind"], ch["slot"].to_bytes(1, "little"),
             sh["ed_pub"], sh["pq_pub"], sh["x_pub"], sh["kem_ct"], sh["nonce"])


def kdf(ikm, salt, info, n):
    return HKDF(hashes.SHA3_256(), n, salt, info).derive(ikm)


class Validator:
    def __init__(self, seed):
        self.ed = ed25519.Ed25519PrivateKey.from_private_bytes(H(b"ed", seed))
        self.pq = mldsa.MLDSA87PrivateKey.from_seed_bytes(H(b"pq", seed))
        self.ed_pub = self.ed.public_key().public_bytes_raw()
        self.pq_pub = self.pq.public_key().public_bytes_raw()
        self.seed = seed

    def server_hello(self, ch, nonce):
        xk = x25519.X25519PrivateKey.from_private_bytes(H(b"x", self.seed, nonce))
        kem_ct, kem_ss = mlkem.MLKEM768PublicKey.from_public_bytes(ch["kem_pub"]).encapsulate()
        sh = dict(ed_pub=self.ed_pub, pq_pub=self.pq_pub, x_pub=xk.public_key().public_bytes_raw(),
                  kem_ct=kem_ct, nonce=nonce)
        t = transcript(ch, sh)
        sh["sig_ed"] = self.ed.sign(t)
        sh["sig_pq"] = self.pq.sign(t)
        ss = xk.exchange(x25519.X25519PublicKey.from_public_bytes(ch["x_pub"])) + kem_ss
        self._derive(ch, t, ss)
        return sh

    def _derive(self, ch, t, ss):
        self.sid = ch["sid_bind"] if any(ch["sid_bind"]) else H(b"BLF-SID", t)[:16]
        self.key = kdf(ss, t, b"BLF-v1 slice-mac", 32)

    def slice(self, flags, slice_index, seq, frame_no, payload, slot, **kw):
        return make_slice(self.key, self.sid, flags | slot, slice_index, seq, frame_no, payload, **kw)

    def sign_root(self, second, first_frame, frame_hashes):
        msg = root_message(self.sid, second, first_frame, frame_hashes)
        return msg, self.ed.sign(msg), self.pq.sign(msg)


class U7:
    """The secure element. Holds the wallet key and the active validator set."""

    def __init__(self, seed, vset, programs):
        self.wallet = mldsa.MLDSA87PrivateKey.from_seed_bytes(H(b"wallet", seed))
        self.wallet_pub = self.wallet.public_key().public_bytes_raw()
        self.addr = H(self.wallet_pub)
        self.vset = vset
        self.programs = programs
        self.seed = seed
        self.sid = bytes(16)
        self.peer = {}

    def client_hello(self, app, slot, nonce):
        self._x = x25519.X25519PrivateKey.from_private_bytes(H(b"lx", self.seed, nonce))
        self._kem = mlkem.MLKEM768PrivateKey.from_seed_bytes(H(b"lk", self.seed, nonce) + H(b"lk2", self.seed, nonce))
        self._ch = dict(x_pub=self._x.public_key().public_bytes_raw(),
                        kem_pub=self._kem.public_key().public_bytes_raw(), nonce=nonce,
                        app=app, epoch=self.vset.epoch, sid_bind=self.sid, slot=slot)
        return self._ch

    def accept(self, sh):
        """Returns (ok, reason, prefix_lanes). Only ok loads a key into U6."""
        ch = self._ch
        if ch["app"] not in self.programs:
            return False, "app is not an on-chain program entry", None
        if not self.vset.is_active_validator(sh["ed_pub"], sh["pq_pub"]):
            return False, "key is not an active validator", None
        t = transcript(ch, sh)
        try:
            ed25519.Ed25519PublicKey.from_public_bytes(sh["ed_pub"]).verify(sh["sig_ed"], t)
            mldsa.MLDSA87PublicKey.from_public_bytes(sh["pq_pub"]).verify(sh["sig_pq"], t)
        except InvalidSignature:
            return False, "handshake signature invalid", None
        ss = self._x.exchange(x25519.X25519PublicKey.from_public_bytes(sh["x_pub"])) \
            + self._kem.decapsulate(sh["kem_ct"])
        if not any(self.sid):
            self.sid = H(b"BLF-SID", t)[:16]
        key = kdf(ss, t, b"BLF-v1 slice-mac", 32)
        self.peer[ch["slot"]] = sh["ed_pub"], sh["pq_pub"]
        return True, "ok", kmac128_prefix_state(key, SLICE_CUSTOM)

    def countersign(self, slot, second, first_frame, shown_frame_hashes, root_msg, sig_ed, sig_pq, rtt_us):
        """Check the validator's root against the frames U7 saw shown; sign a receipt."""
        ed_pub, pq_pub = self.peer[slot]
        mine = root_message(self.sid, second, first_frame, shown_frame_hashes)
        if mine != root_msg:
            return None, "root does not match the shown frames"
        try:
            ed25519.Ed25519PublicKey.from_public_bytes(ed_pub).verify(sig_ed, root_msg)
            mldsa.MLDSA87PublicKey.from_public_bytes(pq_pub).verify(sig_pq, root_msg)
        except InvalidSignature:
            return None, "root signature is not from the session validator"
        rm = receipt_message(self.sid, second, root_msg[-32:], ed_pub, sig_ed, rtt_us,
                             len(shown_frame_hashes))
        return (rm, self.wallet.sign(rm)), "ok"
