# BUDLUM LEAF · PROGRAM · THE TEAM BRIEF OF THE L.6.0 BUILD

**Revision L.6.0 · 2026-10-12**. Ayaz ordered the Leaf to be brought to life to the designs and the architecture, by a professional engineering team. This brief is the charter that every team reads first.

## 1 · The source of truth

1. `FINAL/21-stretch-stem-and-projection.md` holds every L.6.0 decision. It wins over every older file.
2. `HARDWARE/05` and `HARDWARE/13` define the B module and its 32 parts.
3. `uploads/b.png`, `cad/monogram_letter.py` and `cad/models/monogram-module.stl` define the B geometry.
4. The Budlum chain lives in `/home/claude/budlum`. Read it for types and roles. Do not edit it.

## 2 · The architecture in one page

| The block | The decision |
|---|---|
| body | `80 x 160 x 2.00 mm`, `128` rigid tiles of `10 x 10 mm` (`8 x 16`), `32` per quadrant `Q1..Q4` |
| stretch | rotating squares, `cos θ + sin θ`: `25.4 %` at `17.5°` by default, `41.4 %` at `45°` at most |
| hinge | edge-on polyimide ribbon, `12.5 µm` thick, `1.2-1.5 mm` tall, `0.8 mm` long, at the chamfered corners |
| skin | floating back skin, `50-100 µm` TPU or silicone, bonded to pads at the tile centres |
| face | each tile has its own solid hard-coated PC cap |
| display | micro-LED on glass, `508 ppi` (`50.0 µm`), `200 x 200` px per tile, `1600 x 3200` at rest, `240 Hz` |
| seam | lattice-continuous: edge pixel `20 µm` from the cut, cut `≤ 10 µm`, so `50.0 µm` across every seam |
| quadrant swap | kinematic seat, Si3N4 balls in WC vees, N52H preload, `< 1 µm` repeat, `< 3 s` swap |
| cells | one hermetic micro cell per tile, `9.25 x 9.25 x 0.90 mm`, `30 µm` welded can, own fuse |
| energy | `5.7 Wh` at `600 Wh/L`, `7.2 Wh` at `750 Wh/L`; B cell `0.14 Wh`; dock pack `20 Wh` |
| Qi2.2 | `25 W` MPP, four series sector coils round the `+` crossing, about `Ø44-46 mm`, coil and shield `0.20 mm`, charge at rest only |
| tile stack | cap `0.25`, OCA `0.05`, glass-LED-glass `0.25`, slip OCA `0.03`, coil or spreader `0.20`, cell `0.90`, skin `0.08`, routing `0.24` = `2.00 mm` |
| B module | `4.00 mm` thick, `10.8 g`, ring `Ø32 / Ø24` on the face, bar `32.0 x 4.0 x 1.00 mm` LCP-GF40 on the top edge |
| bar | A1 `2.4 GHz` inverted-F, A2 `5-7 GHz` arm, A4 `1 x 4` `60 GHz`, `12` gold leaves over one seat tile |
| ring | camera, rear round AMOLED, speaker, two mics, flash, `3.5 mm` jack in the rim, `0.14 Wh` cell, PCBA |
| camera | `50 MP` `0.61-0.64 µm` sensor, five-element `f = 3.3 mm` `f/2.0`, L1 is the window, `0.12 mm` AF, column `3.90 mm` |
| silicon | `U1` TCON and compositor, `U2A` Wi-Fi 7 and BT 6.0, `U2B` `60 GHz` and UWB, `U5` 5G SA modem, `U6` slice decoder with inline check and `16 MB` store, `U7` secure element (wallet), `U8` IMU, `U3` audio, `U4` power |
| Zero CPU | no general-purpose processor, no OS, no third-party code on the device |
| network | the Leaf is a wallet on the nearest validator; validators run the Leaf as they run Budlum; `6 s` slot; zero-frame handover |
| latency | `30 ms` p99 on Wi-Fi and on 5G with a cell-site validator; predicted action about `5 ms` |
| port | USB-C is a separately sold clip-on port part on a free body edge, using the same `12` pads |

## 3 · The rules of every team

1. **Write only inside your own directory.** Never touch another team's files, `FINAL/`, `HARDWARE/`, `MASTER/` or `tools/`. Do not run git.
2. **Never downgrade a target.** Ayaz's rule. If a target is hard, design the most ambitious real path and state what it needs.
3. **Prove numbers with code.** Every calculation is a script that runs with `python3` (numpy, scipy, matplotlib, trimesh, shapely, amaranth are installed) or `cargo`. A number without a script is `[HYPOTHESIS]`.
4. **Tag every claim**: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]` with the source, `[GENERAL]`, `[TREE]`.
5. **The prose rules of the repo apply to every `.md`**: no em dash, sentences of 25 words or less, steps of 20 words or less, table cells of 25 words or less, no "should", "may", "might" or "could". Check with `python3 tools/check_prose.py <file>`.
6. **Name the gates.** Link each result to the gates of Part 21, Section 21.8.
7. **Each team writes a `README.md`** in its directory: what is there, how to run it, the key results and the open issues.
