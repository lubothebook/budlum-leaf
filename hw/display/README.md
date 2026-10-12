# BUDLUM LEAF · HW · DISPLAY · README

**Revision L.6.0 · 2026-10-12 · Display team**. This directory specifies the `508 ppi` micro-LED tile, the invisible seam and the display data path. The density stays `508 ppi` in every state. `[DECISION]`

## 1 · What is here

| The file | The content |
|---|---|
| `SPEC.md` | the tile, the seam proof, the interface, the warp, the yield, the gates and the open issues |
| `REFERENCES.md` | the state of the art and the candidate partners |
| `seam_lattice.py` | the lattice of a tile, a `2 x 2` block and the whole face; gate DSP-19 |
| `tile_spec.py` | the drive scheme fit, the PWM, the TGVs and the power per tile |
| `interface.py` | the bandwidth, the `12` leaves, the hinge mesh and the hinge copper |
| `warp.py` | the rotating-square kinematics and the `U1` warp; gate DSP-17 |
| `yield_repair.py` | the defects, the repair and the known-good tile |
| `out/` | the saved outputs, two PNG files and the lattice `.npz` files |

## 2 · How to run it

1. Run `python3 seam_lattice.py`. It exits `0` when the seam geometry passes.
2. Run `python3 tile_spec.py`, `python3 interface.py`, `python3 warp.py` and `python3 yield_repair.py`.
3. Read the results in `out/*.txt`. Each script runs in under `10 s`.

The scripts need numpy, scipy and matplotlib.

## 3 · The key results

| The result | The value | The gate |
|---|---|---|
| seam gap, every seam and the 4-tile corner, kerf `0` to `10 µm` | `50.000 µm` | DSP-19 |
| same-colour gap across every seam, R, G, B and S | `50.000 µm` | DSP-19 |
| the chip and the layout | `5 µm` chips in a `7 µm` RGBS quad, parallel to every edge | DSP-19 |
| chip-to-cut margin | `16 µm` at the nominal `6 µm` kerf, `14 µm` at `10 µm` | DSP-19 |
| drive | one `28 nm` CMOS uIC per `2 x 2` pixels, `1 926` T per pixel; LTPS PWM does not fit | DSP-19 |
| PWM | `12` bits, two PAM levels, `960 Hz` fundamental, `240 Hz` frame | DSP-21 proposed |
| TGVs | `288` per tile, `Ø12 µm`, `100 µm` minimum pitch | DSP-19 |
| power per tile, QD baseline | `14.8 mW` at `500 nits`, `24.2 mW` at `1 000 nits`, full white | DSP-21 proposed |
| link | DSC `10 bpp`, `13.43 Gb/s`, two `10 Gb/s` pairs over the leaves | MON-23, DSP-20 proposed |
| hinge | `3` lanes at `3.2 Gb/s`, `13` of `33` lines, copper strain `0.197 %` at `41 %` | MEC-42 |
| warp | circle error `0.42 %` at `0.5°` rms angle error; no warp gives `7.4 %` | DSP-17 |
| yield | known-good tiles give `P(< 5 dead) = 0.99994` per device | DSP-19 |

## 4 · The open issues

1. The pixel glass must stay full square. A chamfer under the pixels opens a hole at every 4-tile corner.
2. The rest tile pitch must hold `10.000 +0 / -0.002 mm`. A `+1 µm` pitch fails DSP-19.
3. Part 21 quotes a coverage of `61 %` and `47.5 %`. Full-square glass gives `63.5 %` and `50.0 %`.
4. The `16 µm` edge margin holds at the nominal kerf only. The team asks for "at least `14 µm`".
5. The hub die needs a seat in the coil or spreader layer of each tile.
6. The `12` leaves and the `33` hinge lines are shared with the energy, port and Qi teams.
7. The more-room view needs a `2:1` compressed frame store in `U1` and `U6`.
8. `HARDWARE/16` promises "zero PWM". A micro-LED face uses PWM, at a `960 Hz` fundamental.

`SPEC.md` Section 7 holds each issue with its owner.
