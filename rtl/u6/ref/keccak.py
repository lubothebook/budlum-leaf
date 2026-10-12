"""Bit-exact Keccak-f[1600], SHA3-256, cSHAKE128 and KMAC128 (FIPS 202, SP 800-185).

This is the golden model of the U6 checker core. It works on 25 lanes of
64 bits, in the same lane order as the RTL (lane index = x + 5*y).
The self-test checks it against hashlib (SHA3-256, SHAKE128) and the
NIST SP 800-185 KMAC128 sample #1.
"""
import hashlib

MASK = (1 << 64) - 1

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]

# rho offsets, indexed [x][y]
ROT = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]


def rol(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & MASK if n else v


def keccak_round(a, rc):
    """One round on a list of 25 lanes, a[x + 5*y]. Returns a new list."""
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
    a = [a[i] ^ d[i % 5] for i in range(25)]
    b = [0] * 25
    for x in range(5):
        for y in range(5):
            b[y + 5 * ((2 * x + 3 * y) % 5)] = rol(a[x + 5 * y], ROT[x][y])
    out = [0] * 25
    for x in range(5):
        for y in range(5):
            out[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y])
    out[0] ^= rc
    return out


def keccak_f(a):
    for r in range(24):
        a = keccak_round(a, RC[r])
    return a


def bytes_to_lanes(b):
    assert len(b) % 8 == 0
    return [int.from_bytes(b[i:i + 8], "little") for i in range(0, len(b), 8)]


def lanes_to_bytes(lanes):
    return b"".join(v.to_bytes(8, "little") for v in lanes)


class Sponge:
    """A byte sponge with an exposed lane state, so a caller can snapshot it."""

    def __init__(self, rate_bytes, state=None):
        self.rate = rate_bytes
        self.state = list(state) if state else [0] * 25
        self.buf = b""
        self.perms = 0

    def absorb(self, data):
        self.buf += data
        while len(self.buf) >= self.rate:
            blk, self.buf = self.buf[:self.rate], self.buf[self.rate:]
            for i, v in enumerate(bytes_to_lanes(blk)):
                self.state[i] ^= v
            self.state = keccak_f(self.state)
            self.perms += 1

    def finish(self, dsbyte, outlen):
        blk = bytearray(self.buf + bytes(self.rate - len(self.buf)))
        blk[len(self.buf)] ^= dsbyte
        blk[-1] ^= 0x80
        for i, v in enumerate(bytes_to_lanes(bytes(blk))):
            self.state[i] ^= v
        self.state = keccak_f(self.state)
        self.perms += 1
        out = b""
        while True:
            out += lanes_to_bytes(self.state)[:self.rate]
            if len(out) >= outlen:
                return out[:outlen]
            self.state = keccak_f(self.state)
            self.perms += 1


def sha3_256(data):
    s = Sponge(136)
    s.absorb(data)
    return s.finish(0x06, 32)


# --- SP 800-185 encodings --------------------------------------------------

def left_encode(x):
    n = max(1, (x.bit_length() + 7) // 8)
    return bytes([n]) + x.to_bytes(n, "big")


def right_encode(x):
    n = max(1, (x.bit_length() + 7) // 8)
    return x.to_bytes(n, "big") + bytes([n])


def encode_string(s):
    return left_encode(8 * len(s)) + s


def bytepad(x, w):
    z = left_encode(w) + x
    return z + bytes((-len(z)) % w)


def kmac128_prefix_state(key, custom=b""):
    """Lane state after the cSHAKE128 prefix block and the key block.

    U7 computes this once per session and loads it into U6. The tag of a
    message X is then one extra block: X || right_encode(L) with pad 0x04.
    """
    s = Sponge(168)
    s.absorb(bytepad(encode_string(b"KMAC") + encode_string(custom), 168))
    s.absorb(bytepad(encode_string(key), 168))
    assert s.buf == b""
    return s.state


def kmac128(key, data, outbits, custom=b""):
    s = Sponge(168, kmac128_prefix_state(key, custom))
    s.absorb(data + right_encode(outbits))
    return s.finish(0x04, outbits // 8)


def _selftest():
    import os
    for n in (0, 1, 135, 136, 137, 271, 272, 1000):
        m = os.urandom(n)
        assert sha3_256(m) == hashlib.sha3_256(m).digest(), n
        s = Sponge(168); s.absorb(m)
        assert s.finish(0x1F, 64) == hashlib.shake_128(m).digest(64), n
    # NIST SP 800-185 KMAC sample #1 (KMAC128, S = "")
    key = bytes(range(0x40, 0x60))
    tag = kmac128(key, bytes([0, 1, 2, 3]), 256)
    assert tag.hex().upper() == ("E5780B0D3EA6F7D3A429C5706AA43A00"
                                 "FADBD7D49628839E3187243F456EE14E"), tag.hex()
    # NIST SP 800-185 KMAC sample #2 (KMAC128, S = "My Tagged Application")
    tag = kmac128(key, bytes([0, 1, 2, 3]), 256, b"My Tagged Application")
    assert tag.hex().upper() == ("3B1FBA963CD8B0B59E8C1A6D71888B71"
                                 "43651AF8BA0A7070C0979E2811324AA5"), tag.hex()
    return True


if __name__ == "__main__":
    print("keccak self-test:", _selftest())
