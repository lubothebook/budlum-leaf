"""The 16 MB frame-store budget of U6 (FINAL/21.5.1). Run: python3 scripts/framestore_budget.py

16 MB is taken as 16 MiB = 16 777 216 bytes of on-package DRAM or SRAM.
The two full frames are held in a fixed-rate compressed form (10 bpp).
The validator's encoder models this exact compression in its reference
loop, so the decoder reference never drifts from the encoder.
"""
W, H = 1600, 3200
PX = W * H
CAP = 16 * 2**20
BPP = 10                       # fixed-rate frame-buffer compression, bits per pixel

items = [
    # name, bytes, why
    ("frame A: shown and reference", PX * BPP // 8, "U1 scans it out; the decoder predicts from it"),
    ("frame B: being decoded", PX * BPP // 8, "slices land here; flip at the last slice"),
    ("scroll overscan band, 10 %", W * (H // 10) * BPP // 8, "U1 scroll offset with no network"),
    ("speculative layers, 2 x 1600 x 400", 2 * W * 400 * BPP // 8, "menu and button frames, gate SW-23"),
    ("glyph atlas, A8, 1024 x 256", 1024 * 256, "typed glyph echo, gate SW-21"),
    ("cursor, 64 x 64 RGBA", 64 * 64 * 4, "U1 cursor plane"),
    ("warp meshes, 128 tiles x 17 x 17 x 8 B", 128 * 17 * 17 * 8, "per-tile stretch warp, gate DSP-17"),
    ("slice ingress buffers, 2 x 64 KiB", 2 * 65536, "verify before decode; double buffered"),
    ("slice digest FIFO to U7, 512 x 48 B", 512 * 48, "digest, seq, frame, flags"),
]
used = sum(b for _, b, _ in items)
full24 = PX * 3
print(f"one frame at 24 bpp: {full24:,} B = {full24/1e6:.2f} MB; two = {2*full24/2**20:.1f} MiB > 16 MiB")
print(f"so the store holds frames at {BPP} bpp: {PX*BPP//8:,} B each ({24/BPP:.1f}:1)\n")
print(f"{'item':<42}{'bytes':>12}  {'MiB':>6}")
for n, b, _ in items:
    print(f"{n:<42}{b:>12,}  {b/2**20:>6.3f}")
print(f"{'total':<42}{used:>12,}  {used/2**20:>6.3f}")
print(f"{'capacity, 16 MiB':<42}{CAP:>12,}  {CAP/2**20:>6.3f}")
print(f"{'margin':<42}{CAP-used:>12,}  {(CAP-used)/2**20:>6.3f}  ({(CAP-used)/CAP*100:.1f} %)")
assert used <= CAP

# bandwidth: decoder write + reference read + U1 scan-out read, at 10 bpp
bw = PX * BPP / 8 * 240 * 3 + PX * BPP / 8 * 240 * 0.25   # +25 % for motion fetch overlap
print(f"\nframe-store bandwidth at 240 Hz: {bw/1e9:.2f} GB/s "
      f"(write, reference read, scan-out, +25 % motion overfetch)")
# the highest bpp that still fits two frames and the rest
rest = used - 2 * PX * BPP // 8
best = (CAP - rest) * 8 / (2 * PX)
print(f"highest frame bpp that fits: {best:.2f} bpp")
