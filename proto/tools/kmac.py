#!/usr/bin/env python3
"""Pure-python Keccak, cSHAKE256 and KMAC256 (NIST SP 800-185).

hashlib has SHA3 and SHAKE but not cSHAKE or KMAC, which the Leaf uses for
the 16-byte line-rate tags (slices, input batches). The sponge is checked
against hashlib.sha3_256 and hashlib.shake_256, and KMAC256 against the NIST
SP 800-185 sample (KMAC_samples.pdf, sample #4) in self_test().
Speed is irrelevant here: this is a reference model, not the U6 engine.
"""
import hashlib

_RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
_ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
M = (1 << 64) - 1


def _rol(x, n):
    return ((x << n) | (x >> (64 - n))) & M if n else x


def _f(a):
    for rc in _RC:
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        a = [[a[x][y] ^ d[x] for y in range(5)] for x in range(5)]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rol(a[x][y], _ROT[x][y])
        a = [[b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) for y in range(5)]
             for x in range(5)]
        a[0][0] ^= rc
    return a


def keccak(rate, data, suffix, out_len):
    a = [[0] * 5 for _ in range(5)]
    msg = bytearray(data) + bytes([suffix])
    while len(msg) % rate:
        msg.append(0)
    msg[-1] |= 0x80
    for off in range(0, len(msg), rate):
        blk = msg[off:off + rate]
        for k in range(rate // 8):
            a[k % 5][k // 5] ^= int.from_bytes(blk[8 * k:8 * k + 8], "little")
        a = _f(a)
    out = bytearray()
    while True:
        for k in range(rate // 8):
            out += a[k % 5][k // 5].to_bytes(8, "little")
        if len(out) >= out_len:
            return bytes(out[:out_len])
        a = _f(a)


def _left_encode(x):
    n = max(1, (x.bit_length() + 7) // 8)
    return bytes([n]) + x.to_bytes(n, "big")


def _right_encode(x):
    n = max(1, (x.bit_length() + 7) // 8)
    return x.to_bytes(n, "big") + bytes([n])


def _encode_string(s):
    return _left_encode(len(s) * 8) + s


def _bytepad(x, w):
    z = _left_encode(w) + x
    return z + bytes((-len(z)) % w)


def cshake256(data, out_len, n=b"", s=b""):
    if not n and not s:
        return keccak(136, data, 0x1F, out_len)
    return keccak(136, _bytepad(_encode_string(n) + _encode_string(s), 136) + data, 0x04, out_len)


def kmac256(key, data, out_len, custom=b""):
    x = _bytepad(_encode_string(key), 136) + data + _right_encode(out_len * 8)
    return cshake256(x, out_len, b"KMAC", custom)


def tag16(key, domain, data):
    """The Leaf line-rate tag: KMAC256 with the BDLM domain tag as S, 16 bytes."""
    return kmac256(key, data, 16, domain)


def self_test():
    for msg in (b"", b"abc", bytes(range(200)) * 3):
        assert keccak(136, msg, 0x06, 32) == hashlib.sha3_256(msg).digest()
        assert cshake256(msg, 64) == hashlib.shake_256(msg).digest(64)
    key = bytes(range(0x40, 0x60))
    want = bytes.fromhex(
        "20C570C31346F703C9AC36C61C03CB64C3970D0CFC787E9B79599D273A68D2F7"
        "F69D4CC3DE9D104A351689F27CF6F5951F0103F33F4F24871024D9C27773A8DD")
    got = kmac256(key, bytes([0, 1, 2, 3]), 64, b"My Tagged Application")
    return got == want


if __name__ == "__main__":
    print("sponge vs hashlib: ok; KMAC256 NIST sample #4:", "ok" if self_test() else "MISMATCH")
