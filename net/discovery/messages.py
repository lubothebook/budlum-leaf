#!/usr/bin/env python3
"""messages.py: the L0 beacon codec and the size budget of every discovery message.

FINAL/21 Section 21.5.4. Gate SW-24. The wire definitions are in
discovery.proto; this script packs the raw beacon, encodes the protobuf
messages with typical contents, and checks each against its carrier.

    python3 messages.py        # prints the table and writes results/messages.json
"""
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

# [PUBLICATION] FIPS 203 ML-KEM-768 and FIPS 204 ML-DSA-65 sizes.
MLKEM768_EK, MLKEM768_CT = 1184, 1088
MLDSA65_PK, MLDSA65_SIG = 1952, 3309

# ------------------------------------------------------------- the beacon ---
BEACON = struct.Struct(">BBQ16sIBBHHI")
assert BEACON.size == 40


def pack_beacon(chain_id, key_hash, epoch, uwb_ch=9, preamble=10, load=250,
                psm=0x0081, counter=0, uwb=True, nan=True, dock=False, open_now=True):
    flags = (uwb << 0) | (nan << 1) | (dock << 2) | (open_now << 3)
    return BEACON.pack(1, flags, chain_id, key_hash[:16], epoch & 0xFFFFFFFF,
                       uwb_ch, preamble, load, psm, counter)


def unpack_beacon(b):
    v, flags, chain, kh, ep, ch, pre, load, psm, ctr = BEACON.unpack(b)
    if v != 1:
        raise ValueError("beacon version")
    return dict(flags=flags, chain_id=chain, key_hash_prefix=kh, epoch=ep,
                uwb_channel=ch, preamble=pre, load=load, psm=psm, counter=ctr)


# ------------------------------------------------- a minimal pb encoder ---

def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def f_int(no, v):
    return varint(no << 3) + varint(v) if v else b""


def f_bytes(no, b):
    return varint((no << 3) | 2) + varint(len(b)) + b if b else b""


def signature(scheme=2, sig_len=MLDSA65_SIG):
    return f_int(1, scheme) + f_bytes(2, b"k" * 32) + f_bytes(3, b"s" * sig_len)


def active_set_proof(n_val=10_000):
    depth = max(1, (n_val - 1).bit_length())
    return (f_int(1, 12_345_678) + f_bytes(2, b"v" * 32) + f_bytes(3, b"h" * 32)
            + f_int(4, n_val - 1) + b"".join(f_bytes(5, b"p" * 32) for _ in range(depth))
            + f_bytes(6, b"c" * 32))


def ranging_offer():
    return (f_int(1, 1) + f_int(2, 1) + f_bytes(3, b"e" * MLKEM768_EK)
            + f_bytes(4, b"n" * 32) + f_int(5, 9) + f_int(6, 8) + f_int(7, 1))


def ranging_accept():
    return (f_bytes(1, b"c" * MLKEM768_CT) + f_bytes(2, b"n" * 32)
            + f_bytes(3, b"k" * MLDSA65_PK) + f_bytes(4, active_set_proof())
            + f_int(5, 77) + f_bytes(6, signature()))


def ranging_report():
    return (f_int(1, 77) + f_int(2, 7) + f_int(3, 250_000_000) + f_int(4, 251_000_000)
            + f_int(5, 312) + f_bytes(15, b"t" * 16))


def bootstrap_query():
    core = f_int(1, 1) + f_int(2, 1) + f_int(3, 12_345_600) + f_int(4, 5) + f_int(5, 2) + f_bytes(6, b"q" * 16)
    pad = 256 - len(core) - 3
    return core + f_bytes(15, b"\0" * pad)


def candidate(n_val=10_000):
    depth = max(1, (n_val - 1).bit_length())
    return (f_bytes(1, b"h" * 32) + f_bytes(2, b"quic://[2001:db8:1:2::10]:4433")
            + f_int(3, 0x85283473FFFFFFF) + f_int(4, 0x83283FFFFFFFFFF)
            + f_int(5, 6_200) + f_int(6, 40) + f_int(7, 1)
            + b"".join(f_bytes(8, b"p" * 32) for _ in range(depth)) + f_int(9, 4321))


def bootstrap_reply(n=5):
    return (f_int(1, 12_345_678) + f_bytes(2, b"r" * 32) + f_bytes(3, b"g" * 32)
            + b"".join(f_bytes(4, b"p" * 32) for _ in range(8))
            + b"".join(f_bytes(5, candidate()) for _ in range(n))
            + f_bytes(6, b"h" * 32) + f_bytes(7, b"q" * 16) + f_bytes(8, signature()))


def path_probe():
    # leaf.proto PathProbe with the clock field left out (SPEC.md Section 7),
    # padded by the QUIC packet to 64 bytes of UDP payload.
    return f_int(1, 0xDEADBEEFCAFEF00D)


def challenge_report():
    return (f_bytes(1, b"c" * 32) + f_bytes(2, b"h" * 32) + f_int(3, 24) + f_int(4, 3_210)
            + f_int(5, 9_870) + f_int(6, 3_100) + f_int(7, 1) + f_bytes(8, b"t" * 32)
            + f_bytes(9, signature()) + f_bytes(10, signature()))


def coverage_claim():
    return (f_bytes(1, b"h" * 32) + f_int(2, 0x83283FFFFFFFFFF) + f_int(3, 2 * 4_101_234)
            + f_int(4, 2 * 2_897_654) + f_int(5, 640) + f_bytes(6, signature()))


# carriers, bytes and rate
BLE_EXT_ADV = 254         # [PUBLICATION] Bluetooth Core 5.x, AUX_ADV_IND AdvData max 254 bytes
BLE_L2CAP_BPS = 1.4e6     # LE 2M PHY with data length extension, effective [HYPOTHESIS]
NAN_BPS = 50e6            # Wi-Fi Aware data path, effective [HYPOTHESIS]
UWB_FRAME = 127           # [PUBLICATION] IEEE 802.15.4 aMaxPhyPacketSize (HRP allows 1023)
QUIC_MIN = 1200           # [PUBLICATION] RFC 9000 Initial datagram minimum


def main():
    kh = bytes(range(32))
    b = pack_beacon(chain_id=0xB0D1, key_hash=kh, epoch=640)
    d = unpack_beacon(b)
    assert d["key_hash_prefix"] == kh[:16] and d["epoch"] == 640
    ad = 1 + 1 + 16 + len(b)          # AD length, type 0x21, 128-bit UUID, data
    rows = {
        "L0 beacon (BLE ext adv AD)": (ad, BLE_EXT_ADV, "BLE AUX_ADV_IND"),
        "L0RangingOffer": (len(ranging_offer()), None, "BLE L2CAP CoC or NAN"),
        "L0RangingAccept": (len(ranging_accept()), None, "BLE L2CAP CoC or NAN"),
        "L0RangingReport": (len(ranging_report()), UWB_FRAME, "UWB data frame"),
        "BootstrapQuery": (len(bootstrap_query()), 256, "QUIC stream, padded"),
        "BootstrapReply (5 candidates)": (len(bootstrap_reply()), None, "QUIC stream"),
        "PathProbe (no clock)": (len(path_probe()), 64, "QUIC 1-RTT, padded 64"),
        "CoverageClaim": (len(coverage_claim()), None, "transaction"),
        "ChallengeReport": (len(challenge_report()), None, "transaction"),
    }
    out = {}
    for k, (n, cap, carrier) in rows.items():
        t_ble = n * 8 / BLE_L2CAP_BPS * 1000
        t_nan = n * 8 / NAN_BPS * 1000
        out[k] = dict(bytes=n, limit=cap, fits=(cap is None or n <= cap), carrier=carrier,
                      ble_ms=round(t_ble, 2), nan_ms=round(t_nan, 3))
        print(f"{k:34s} {n:6d} B  limit {str(cap):>5s}  fits {out[k]['fits']!s:5s} "
              f"BLE {t_ble:7.2f} ms  NAN {t_nan:6.3f} ms  {carrier}")
    l0_ble = (len(ranging_offer()) + len(ranging_accept())) * 8 / BLE_L2CAP_BPS * 1000
    l0_nan = (len(ranging_offer()) + len(ranging_accept())) * 8 / NAN_BPS * 1000
    out["L0 key exchange time"] = dict(ble_ms=round(l0_ble, 1), nan_ms=round(l0_nan, 2))
    print("L0 key exchange: BLE %.1f ms, NAN %.2f ms (plus U7 ML-DSA-65 verify)" % (l0_ble, l0_nan))
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "messages.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
