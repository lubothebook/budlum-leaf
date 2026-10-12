#!/usr/bin/env python3
"""Bitrate model of the Leaf link: 1600 x 3200 at 240 Hz, AV1 and HEVC slices,
the camera uplink, audio and control. Prints the tables of out/bitrate.md.

Every anchor below is tagged. [HYPOTHESIS] numbers wait for gate DST-11 and
the encoder bench of RG-18. Run:  python3 model/bitrate.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

# ---------------------------------------------------------------- panel ---
W, H, HZ = 1600, 3200, 240                  # [DECISION] FINAL/21 21.2.3
TILES_X, TILES_Y, TILE_PX = 8, 16, 200      # [DECISION] 128 tiles of 200 px
PX = W * H
RAW_BITS_PER_PX = 15                        # 10 bit 4:2:0
SLICES_PER_FRAME = 16                       # one tile row (8 tiles) per slice [HYPOTHESIS]
TILES_PER_SLICE = TILES_X * TILES_Y // SLICES_PER_FRAME

# ------------------------------------------------------ codec anchors ---
# bits per pixel at a 60 Hz reference, low-delay AV1 (no B frames).
# Anchor: 4K60 low-latency AV1 game streaming near 40 Mbit/s = 0.080 bpp.
# [HYPOTHESIS], consistent with cloud gaming practice [GENERAL].
BPP60_AV1 = {
    "game, full motion": 0.080,
    "game, high quality (2x bpp)": 0.160,
    "video, natural": 0.055,
    "ui, validator scroll": 0.030,
}
# Content frame rate: video is sent at its own rate, the panel repeats.
CONTENT_HZ = {"game, full motion": 240, "game, high quality (2x bpp)": 240, "video, natural": 60, "ui, validator scroll": 240}
ALPHA = 0.55          # rate ~ fps^alpha: higher fps, smaller residual [HYPOTHESIS]
LOW_DELAY = 1.12      # 16 independent slices + gradual intra refresh [HYPOTHESIS]
HEVC_OVER_AV1 = 1.30  # AV1 saves about 25-30 % over HEVC [GENERAL]
SPECULATIVE = 0.20    # speculative branches, share of the main stream [HYPOTHESIS]
FEC_DATAGRAM = 1 / 8  # one XOR parity per 8 fragments, datagram mode only
MTU_PAYLOAD = 1200    # QUIC DATAGRAM payload that every path carries [GENERAL]
UDP_IP_QUIC = 28 + 1 + 8 + 4 + 16 + 3  # IPv4+UDP, short header, CID 8, PN 4, AEAD 16, frame 3


def video_rate_bps(content, codec="AV1", quality=1.0):
    bpp = BPP60_AV1[content] * quality
    hz = CONTENT_HZ[content]
    r = PX * 60 * bpp * (hz / 60) ** ALPHA * LOW_DELAY
    return r * (HEVC_OVER_AV1 if codec == "HEVC" else 1.0)


def slice_payload_bytes(content="game, full motion", codec="AV1"):
    r = video_rate_bps(content, codec)
    return int(r / CONTENT_HZ[content] / SLICES_PER_FRAME / 8)


def _wrap_overhead():
    """Envelope + SliceHeader + MAC bytes around a slice payload, measured
    with the real canonical encoder."""
    import protolite as pl
    s = pl.parse(os.path.join(ROOT, "budlum/leaf/v1/leaf.proto"))
    hdr = {"key_slot": 1, "frame_no": 10_000_000, "slice_no": 15, "slice_count": 16,
           "first_tile": 120, "tile_count": 8, "codec": "CODEC_AV1",
           "kind": "SLICE_KIND_INTER", "ref_frame": 9_999_999, "payload_bytes": 3000}
    payload = bytes(3000)
    b = pl.encode(s, "LeafMessage", {"slice": {"header": hdr, "payload": payload, "mac": bytes(16)}})
    commit = pl.encode(s, "LeafMessage", {"frame_commit": {
        "frame_no": 10_000_000, "slice_count": 16, "frame_hash": bytes(32),
        "chain_hash": bytes(32), "rc_target_bits": 250_000,
        "present_at_us": 3_600_000_000, "state_height": 2_000_000, "mac": bytes(16)}})
    return len(b) - len(payload), len(commit)


def downlink_table():
    wrap, commit = _wrap_overhead()
    rows = []
    for content in BPP60_AV1:
        for codec in ("AV1", "HEVC"):
            r = video_rate_bps(content, codec)
            hz = CONTENT_HZ[content]
            frame_b = r / hz / 8
            slice_b = frame_b / SLICES_PER_FRAME
            frags = math.ceil((slice_b + wrap) / MTU_PAYLOAD)
            proto = hz * (SLICES_PER_FRAME * wrap + commit) * 8
            packets = hz * SLICES_PER_FRAME * frags
            udp = packets * UDP_IP_QUIC * 8
            spec = r * SPECULATIVE
            stream_total = r + proto + udp + spec
            dgram_total = stream_total * (1 + FEC_DATAGRAM)
            rows.append(dict(content=content, codec=codec, hz=hz, video=r, frame_b=frame_b,
                             slice_b=slice_b, proto=proto, udp=udp, spec=spec,
                             stream_total=stream_total, dgram_total=dgram_total))
    return rows, wrap, commit


# ------------------------------------------------------------ air time ---
# Effective downlink goodput of each path [HYPOTHESIS]; first-slice air time.
PATHS = {
    "Wi-Fi 7, 2x2, 320 MHz, room": (2000e6, 1500e6),
    "Wi-Fi 7, 2x2, 160 MHz, city": (1000e6, 600e6),
    "5G SA, 100 MHz TDD, good cell": (600e6, 100e6),
    "5G SA, loaded cell": (150e6, 30e6),
}


def air_table(rows):
    game = next(r for r in rows if r["content"].startswith("game") and r["codec"] == "AV1")
    hevc = next(r for r in rows if r["content"].startswith("game") and r["codec"] == "HEVC")
    out = []
    for name, (down, up) in PATHS.items():
        t_slice = game["slice_b"] * 8 / down * 1e3
        load = hevc["dgram_total"] / down
        out.append((name, down, up, t_slice, load))
    return out


# ------------------------------------------------------------- camera ---
SENSOR = (8160, 6144)                    # 50.1 MP [DECISION] FINAL/21 21.3.5
BINNED = (4080, 3072)                    # quad-Bayer 2x2 binning [GENERAL]
LOSSLESS_RATIO = 1.8                     # lossless RAW, Bayer [HYPOTHESIS]
CAPTURES = {
    "full 50 MP RAW10 lossless": [(SENSOR, 10, 1)],
    "full 50 MP RAW12 lossless": [(SENSOR, 12, 1)],
    "binned 12.5 MP RAW10 lossless": [(BINNED, 10, 1)],
    "fusion burst: 1 full + 8 binned, RAW10 lossless": [(SENSOR, 10, 1), (BINNED, 10, 8)],
}
DEADLINES = (("interactive", 5.0), ("standard", 60.0))  # FINAL/10 10.3


def capture_bytes(parts):
    return sum(w * h * bits / 8 / LOSSLESS_RATIO * n for (w, h), bits, n in parts)


def camera_table():
    rows = []
    for name, parts in CAPTURES.items():
        b = capture_bytes(parts) * (1 + 0.004)  # chunk framing, 16 KiB chunks
        times = {p: b * 8 / up for p, (_, up) in PATHS.items()}
        rows.append((name, b, times))
    return rows


def video_capture_table():
    px = 3840 * 2160 * 60
    bayer = px * 10          # RAW10 Bayer, one sample per pixel
    yuv = px * 15            # 10-bit 4:2:0 after the ISP
    return [
        ("RAW10 Bayer, lossless (no encoder)", bayer / LOSSLESS_RATIO),
        ("mezzanine, JPEG XS class, 10:1 on 4:2:0, fixed function", yuv / 10),
        ("HEVC Main10, 4K60, fixed-function encoder", 60e6),
    ]


# -------------------------------------------------- uplink and audio ---
def uplink_table(sizes):
    """sizes: encoded LeafMessage byte sizes from the round-trip test."""
    per_pkt = UDP_IP_QUIC
    rows = [
        ("InputBatch, 480 Hz, 2 contacts", 480, sizes["input_batch"]),
        ("FrameRequest, on change, 10 Hz", 10, sizes["frame_request"]),
        ("Receipt, 1 Hz", 1, sizes["receipt"]),
        ("PathProbe, 5 validators, 1 Hz", 5, sizes["path_probe"]),
        ("AudioFrame, mic Opus 64 kbit/s, 100 Hz", 100, sizes["audio_frame_mic"]),
    ]
    return [(n, hz, b, hz * (b + per_pkt) * 8) for n, hz, b in rows]


def main():
    rows, wrap, commit = downlink_table()
    out = []
    p = out.append
    p("# The Leaf link bitrate model (generated by model/bitrate.py)\n")
    p(f"Panel {W} x {H} = {PX/1e6:.2f} Mpx at {HZ} Hz. Raw 10-bit 4:2:0: "
      f"{PX*RAW_BITS_PER_PX*HZ/1e9:.1f} Gbit/s.\n")
    p(f"Slices per frame: {SLICES_PER_FRAME}, each {TILES_PER_SLICE} tiles (one tile row). "
      f"Slice wrapper (envelope, header, MAC): {wrap} bytes. FrameCommit: {commit} bytes.\n")
    p("## Downlink video\n")
    p("| content | codec | sent Hz | video Mbit/s | frame kB | slice kB | protocol Mbit/s | "
      "UDP/QUIC Mbit/s | speculative Mbit/s | total, stream mode | total, datagram + FEC |")
    p("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        p(f"| {r['content']} | {r['codec']} | {r['hz']} | {r['video']/1e6:.1f} | "
          f"{r['frame_b']/1e3:.1f} | {r['slice_b']/1e3:.2f} | {r['proto']/1e6:.2f} | "
          f"{r['udp']/1e6:.2f} | {r['spec']/1e6:.1f} | {r['stream_total']/1e6:.1f} | "
          f"{r['dgram_total']/1e6:.1f} |")
    p("\nA static page sends no slices at all: only the Merkle root once per second.\n")
    p("## Air time of the first slice, and the path load\n")
    p("| path | down goodput Mbit/s | up goodput Mbit/s | first slice air time, game AV1 | "
      "load, game HEVC datagram |")
    p("|---|---|---|---|---|")
    for name, down, up, t, load in air_table(rows):
        p(f"| {name} | {down/1e6:.0f} | {up/1e6:.0f} | {t*1e3:.0f} us | {load*100:.0f} % |")
    p("\n## Camera RAW uplink\n")
    p("| capture | MB | " + " | ".join(PATHS) + " |")
    p("|---|---|" + "---|" * len(PATHS))
    for name, b, times in camera_table():
        cells = []
        for t in times.values():
            cls = "interactive" if t <= 5 else ("standard" if t <= 60 else "deferrable")
            cells.append(f"{t:.1f} s, {cls}")
        p(f"| {name} | {b/1e6:.1f} | " + " | ".join(cells) + " |")
    p("\n## Video capture uplink, 4K60\n")
    p("| method | Mbit/s | " + " | ".join(f"uplink load, {k}" for k in PATHS) + " |")
    p("|---|---|" + "---|" * len(PATHS))
    for name, r in video_capture_table():
        p(f"| {name} | {r/1e6:.0f} | " + " | ".join(
            f"{r/up*100:.0f} %" for _, up in PATHS.values()) + " |")
    sizes_path = os.path.join(ROOT, "out", "sizes.csv")
    if os.path.exists(sizes_path):
        sizes = {}
        for line in open(sizes_path).read().splitlines()[1:]:
            k, v = line.split(",")[:2]
            sizes[k] = int(v)
        p("\n## Uplink control and audio (sizes from tests/test_roundtrip.py)\n")
        p("| flow | Hz | message bytes | kbit/s with UDP/QUIC |")
        p("|---|---|---|---|")
        tot = 0
        for n, hz, b, bps in uplink_table(sizes):
            tot += bps
            p(f"| {n} | {hz} | {b} | {bps/1e3:.0f} |")
        p(f"| total | | | {tot/1e3:.0f} |")
        down = [("FrameCommit", 240, sizes["frame_commit"]),
                ("ShadowHeartbeat, warm shadow", 240, sizes["shadow_heartbeat"]),
                ("SpeculativeFrameSet", 20, sizes["speculative_frame_set"]),
                ("AudioFrame, Opus stereo 128 kbit/s", 100, sizes["audio_frame_down"]),
                ("MerkleRoot", 1, sizes["merkle_root"])]
        p("\n## Downlink control and audio, beside the slices\n")
        p("| flow | Hz | message bytes | kbit/s with UDP/QUIC |")
        p("|---|---|---|---|")
        tot = 0
        for n, hz, b in down:
            bps = hz * (b + UDP_IP_QUIC) * 8
            tot += bps
            p(f"| {n} | {hz} | {b} | {bps/1e3:.0f} |")
        p(f"| total | | | {tot/1e3:.0f} |")
        mlsig = 480 * (2420 + UDP_IP_QUIC) * 8
        p(f"\nPer-batch ML-DSA-44 signing would add {mlsig/1e6:.1f} Mbit/s and 480 "
          "signatures per second in U7. The KMAC tag plus one signed receipt per second avoids it.\n")
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    open(os.path.join(ROOT, "out", "bitrate.md"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
