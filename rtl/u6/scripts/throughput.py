"""Throughput and margin of the U6 checker at the Leaf stream.

The cycle model is fitted to nothing: it is derived from the FSM and then
checked against every slice of build/sim_cycles.json (amaranth.sim).
Run after sim/test_slice_auth.py:  python3 scripts/throughput.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = 24


def cycles(payload_bytes):
    """Cycles from the first word offered to res_valid, back-to-back input."""
    m = math.ceil(payload_bytes / 8)
    words = 4 + m + 2
    lanes = 2 + 4 + m                    # sid, header, payload
    blocks = lanes // 17 + 1             # the pad always lands in the last block
    padblk = 1 if lanes % 17 == 0 else 0
    return words + ROUNDS * (blocks + 1) + 1 + padblk + 1


# 1. check the model against the simulation
log = json.load(open(os.path.join(HERE, "..", "build", "sim_cycles.json")))
checked = 0
for e in log:
    if e["err"] in (4,):                # framing errors stop early
        continue
    p = (e["words"] - 6) * 8            # payload words; exact for the cycle count
    assert cycles(p) == e["cycles"], (e["name"], cycles(p), e["cycles"])
    checked += 1
print(f"cycle model matches amaranth.sim on {checked} slices")

# 2. the stream: 1600 x 3200 at 240 Hz, compressed 60-160 Mbit/s (FINAL/21.5)
W, Hh, FPS = 1600, 3200, 240
raw = W * Hh * 24 * FPS
print(f"raw stream {raw/1e9:.1f} Gbit/s; compressed 60-160 Mbit/s = {raw/160e6:.0f}:1 to {raw/60e6:.0f}:1")

HDR, TAG = 32, 16
rows = []
for clk in (200e6, 100e6):
    for spf in (16, 32, 64):
        for rate in (60e6, 160e6):
            sps = spf * FPS
            pay = rate / 8 / sps
            cyc_slice = cycles(pay)
            # the frame hash pass on the same core: (spf*32 + 28) bytes per frame
            fh_perm = math.ceil((spf * 32 + 12 + 16 + 12) / 136)
            busy = sps * cyc_slice + FPS * fh_perm * (ROUNDS + 17)
            util = busy / clk
            wire = rate * (pay + HDR + TAG + 4) / pay
            cap = pay * 8 / (cyc_slice / clk)          # Gbit/s at this slice size
            tail = (ROUNDS * 2 + 4) / clk                # after the last payload word
            rows.append((clk / 1e6, spf, rate / 1e6, pay, cyc_slice, util * 100, 1 / util,
                         cap / 1e9, wire / 1e6, tail * 1e6))
print("\nclk MHz | slices/frame | Mbit/s | B/slice | cyc/slice | core busy % | margin x | "
      "core Gbit/s | wire Mbit/s | tail us")
for r in rows:
    print("{:>6.0f} | {:>5} | {:>5.0f} | {:>7.0f} | {:>6} | {:>6.2f} | {:>6.1f} | {:>5.2f} | {:>6.1f} | {:>5.2f}".format(*r))
asym = 136 * 8 / (17 + ROUNDS)
print(f"\nasymptote: {asym:.1f} bit/cycle = {asym*0.2:.2f} Gbit/s at 200 MHz, {asym*0.1:.2f} at 100 MHz")
base = [r for r in rows if r[0] == 200 and r[1] == 32 and r[2] == 160][0]
print(f"baseline 200 MHz, 32 slices/frame, 160 Mbit/s: core busy {base[5]:.2f} %, margin {base[6]:.0f}x")
json.dump(dict(rows=rows), open(os.path.join(HERE, "..", "build", "throughput.json"), "w"), indent=1)
