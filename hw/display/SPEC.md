# BUDLUM LEAF · HW · DISPLAY · THE `508 ppi` MICRO-LED TILE AND ITS DATA PATH

**Revision L.6.0 · 2026-10-12 · Display team**. This file specifies the tile, the seam, the interface, the warp and the yield. It works under `FINAL/21` Sections 21.2.3 and 21.2.4. Every number comes from a script in this directory. The density stays `508 ppi` (`50.0 µm`) in every state. `[DECISION]`

| Script | What it proves | Output |
|---|---|---|
| `seam_lattice.py` | the lattice and the seam gap, gate DSP-19 | `out/seam_lattice.txt`, `out/seam_corner_zoom.png`, `out/*.npz` |
| `tile_spec.py` | drive scheme fit, PWM, TGVs, power per tile | `out/tile_spec.txt` |
| `interface.py` | bandwidth, leaves, hinge mesh, hinge copper | `out/interface.txt` |
| `warp.py` | the stretched view, gate DSP-17 | `out/warp.txt`, `out/stretched_view.png` |
| `yield_repair.py` | defects, repair and known-good tiles, gate DSP-19 | `out/yield_repair.txt` |

---

## 1 · The tile

### 1.1 The geometry

| The item | The value | The tag |
|---|---|---|
| tile pitch at rest | `10.000 mm`, `+0 / -0.002 mm` | `[DECISION]` of this team, needs MEC-40 |
| pixels | `200 x 200` at `50.0 µm` | `[DECISION]` Part 21 |
| glass carrier | `9.994 mm` square, so a nominal kerf of `6 µm` | `[DECISION]` of this team |
| kerf window | `4` to `10 µm` | Part 21 limit `≤ 10 µm` |
| edge pixel centre to the cut | `22.0 µm` nominal, `20.0 µm` at the `10 µm` limit | `seam_lattice.py` |
| glass corners | full square, not chamfered | required, see Section 7 |

**The seam law, proven**. The gap across a seam is the tile pitch minus `9 950 µm`. The kerf does not enter it. The kerf only trades against the edge margin. `seam_lattice.py` shows `50.000 µm` at every kerf from `0` to `10 µm`.

### 1.2 The emitter and the sub-pixel layout

**The chip**. `5.0 µm` square micro-LED chips, the low end of the `5` to `8 µm` range of Part 21. `[DECISION]`

**The layout: an RGBS quad**. Each pixel holds a `2 x 2` quad of chips on a `7.0 µm` sub-pitch. R and G form the top row, B and S the bottom row.

1. The quad has rows parallel to the horizontal cuts and columns parallel to the vertical cuts.
2. So the layout is parallel to every edge at once. The corner pixel is the same as every other pixel.
3. No triad ever lies across a cut. No pixel needs a special layout.
4. The quad spans `12.0 µm`, so every chip edge is `6.0 µm` from the pixel centre.
5. The chip-to-cut margin is `16.0 µm` at the nominal kerf, and `14.0 µm` at the `10 µm` limit.
6. Both clear the `5` to `10 µm` chipping of an ultrafast-laser cut.
7. The chip-to-chip clear space inside a quad is `2.0 µm`. The space across a seam is `38.0 µm`.

**The S site**. S holds a second red chip. Red is the weakest colour at `5 µm`, so two red chips halve its current density. A red chip that fails open is carried by its twin. `[DECISION]`

**Why not a triad**. Three `5 µm` chips in a row span `≥ 18 µm`. Across a cut that leaves `≤ 13 µm` at the nominal kerf. A uniform quad avoids that, and every colour lattice stays a pure `50.0 µm` lattice.

### 1.3 The colour: direct RGB or the quantum-dot option

| The option | The chips | The colour | The verdict |
|---|---|---|---|
| A: direct RGB | InGaN B, InGaN G, InGaN red twin | native | red needs `494 A/cm²` at `1 000 nits` on a single chip |
| **B: blue + QD, the baseline** | four blue InGaN chips | photo-patterned QD over G, R and S | one chip type; test and repair the blue array before the QD |

**The baseline is option B**. `[DECISION]` One epitaxy, one transfer, one repair flow. The QD layer is `≤ 6 µm` thick under a blue-cut filter. The QD option draws `16 %` less power than option A in the model. `[HYPOTHESIS]`

**The risk of option B**. QD life at a high blue flux, and the `5 µm` QD pattern. Option A stays open until gate DSP-19 measures both.

### 1.4 The drive scheme: CMOS micro-ICs on a passive glass carrier

**The finding**. A micro-LED pixel needs PWM, because its colour shifts with current. A PWM pixel circuit in LTPS does not fit `50 µm`. `tile_spec.py`

| The circuit | Per pixel | Area needed | Usable area `1 500 µm²` |
|---|---|---|---|
| `7T1C` PAM, OLED class | `21T3C` | `1 290` to `2 550 µm²` | fits only at the tightest rule |
| `8T2C` sweep PWM | `24T6C` | `1 680` to `3 120 µm²` | does not fit |
| `13T3C` PWM, PAM and threshold compensation | `39T9C` | `2 670` to `5 010 µm²` | does not fit |
| **CMOS micro-IC, one per `2 x 2` pixels** | **`1 926` T per pixel** | **`1 541 µm²` per IC at `28 nm` HV** | **fits a `20 x 85 µm` street slot** |

**The micro-IC (uIC)**. One `20 x 85 x ≤10 µm` CMOS die serves `4` pixels. It holds `7 704` transistors. `[DECISION]`

1. A bus receiver with a hard-wired row address.
2. A `144`-bit back buffer that loads during the frame.
3. A `144`-bit front buffer that drives the light.
4. Twelve `12`-bit comparators against one local PWM counter.
5. Sixteen current sinks with two PAM levels, including the S sites.
6. It sits in the `38 µm` street between pixel rows, with `9 µm` clear on each side.
7. A `40 nm` die needs `3 852 µm²` and does not fit. The `28 nm` HV node of display driver ICs is required.

**The carrier is passive**. Glass with two copper RDL layers and TGVs. It needs no TFT fab. `[DECISION]` The tile carries `10 000` uICs, so the device carries `1.28 M`.

### 1.5 The refresh and the PWM

| The item | The value |
|---|---|
| refresh | `240 Hz`, frame `4.167 ms` |
| PWM depth | `12` bits, LSB `1.017 µs`, counter `0.983 MHz` |
| PAM | two levels, low level `1/16`, so `16` bits of range |
| smallest step at `1 000 nits` | `15 mnit` |
| flicker | the PWM splits into `4` segments, so the fundamental is `960 Hz` |
| buffering | double buffered in each uIC, so a load never darkens the frame |

**A correction for `HARDWARE/16`**. It promises "100 % DC dimming, zero PWM". A micro-LED face uses PWM. The honest claim is a `960 Hz` fundamental with PAM at low grey. `[DECISION]`

### 1.6 The TGV set

| The net | TGVs per tile |
|---|---|
| row-bus data, a redundant pair per uIC row | `200` |
| clock roots | `8` |
| latch and frame strobe | `4` |
| `VLED_GB 3.3 V`, `VLED_R 2.8 V`, `VDD 0.9 V`, `GND` | `16`, `16`, `8`, `32` |
| test, thermistor and seam sense | `4` |
| **total** | **`288` per tile, `36 864` per device** |

1. The via is `Ø12 µm` in `150 µm` glass, copper filled, aspect `12.5:1`. `R = 22.8 mΩ`.
2. The data vias form one column on the tile centre line at a `100 µm` pitch.
3. They sit at the street crossings `(50, 50) µm` mod `100 µm`, clear of every chip.
4. The power vias sit on a `2.5 mm` grid. The IR drop of the front mesh is `0.01 mV`.
5. The minimum pitch is `100 µm`, which is `8.3` via diameters.

**The tile hub**. One die on the back of the carrier per tile. It holds the `4` mesh ports, the DSC decoder, the per-pixel calibration (`1 Mb` eMRAM) and the `100` row-bus drivers. It needs a `1.6 x 1.6 x 0.08 mm` seat in the coil or spreader layer. `[HYPOTHESIS]` See Section 7.

### 1.7 The power of one tile

Full white, D65, Lambertian, stack transmission `0.85`. The overhead is `5.4 mW` per tile: uIC counters, bias, row buses and the hub. `tile_spec.py`

| The option | `500 nits` per tile | `1 000 nits` per tile | Device at `500` | Device at `1 000` |
|---|---|---|---|---|
| A: direct RGB | `17.2 mW` | `28.9 mW` | `2.20 W` | `3.70 W` |
| **B: blue + QD** | **`14.8 mW`** | **`24.2 mW`** | **`1.89 W`** | **`3.10 W`** |

1. The radiation efficacy of the white is `276` to `286 lm/W`.
2. The chip current density at `1 000 nits` full white runs `69` to `187 A/cm²` in option B.
3. A video frame at `25 %` mean level and `500 nits` takes about `1.0 W` for the face. `[HYPOTHESIS]`
4. To hold the mean luminance, the drive rises `1.57 x` at `25 %` stretch and `2.00 x` at `41 %`.
5. The EQE values of the model are `[HYPOTHESIS]` until gate DSP-19 measures a tile.

---

## 2 · The seam proof, gate DSP-19

`seam_lattice.py` builds the tile, the `2 x 2` block and the whole `1 600 x 3 200` face. The block holds `160 000` centres and `640 000` emitters.

| The check | The result |
|---|---|
| neighbour gap inside a tile | `50.000 µm` |
| gap across the vertical seam, every row | `50.000 µm` |
| gap across the horizontal seam, every column | `50.000 µm` |
| diagonal gap across the 4-tile corner | `70.711 µm`, the same as the interior |
| largest empty circle at the corner | `35.355 µm`, the same as the interior |
| same-colour gap for R, G, B and S across every seam | `50.000 µm` |
| whole face, `1 600 x 3 200` | every gap `50.000 µm` |
| kerf sweep `0` to `10 µm` | the gap stays `50.000 µm` |
| tile pitch `+1 µm` | gap `51.0 µm`, **fails** |

**The result**. The geometric half of DSP-19 passes for every kerf up to `10 µm`. It fails only if the rest tile pitch exceeds `10.000 mm`. So the mechanical team holds the pitch at `+0 / -0.002 mm`. `[DECISION]` gate MEC-40.

**The picture**. `out/seam_corner_zoom.png` shows the 4-tile corner at the nominal `6 µm` and at the `10 µm` limit.

---

## 3 · The display interface

### 3.1 The path

1. `U6` decodes the validator stream into the frame store.
2. `U1` composes, warps per tile and encodes `128` DSC slices of `200 x 200` px.
3. Two `10 Gb/s` pairs cross the `12` bar leaves into the seat tile hub.
4. The hubs form a mesh over the `232` hinges. Each hub retimes and forwards.
5. Each hub decodes its own slice, applies its calibration and drives `100` row buses.
6. Each uIC takes its `144` bits per frame and latches on the frame strobe.

### 3.2 The bandwidth

| The format | On the wire, with packets | Per tile |
|---|---|---|
| raw `30` bits | `36.86 Gb/s` payload | `288 Mb/s` |
| DSC 1.2b `8 bpp` | `10.75 Gb/s` | `77 Mb/s` |
| **DSC 1.2b `10 bpp`, the design case** | **`13.43 Gb/s`** | **`105 Mb/s`** |
| VDC-M `6 bpp`, the fallback | `8.06 Gb/s` | `58 Mb/s` |

The stream size does not change with the stretch. `U1` always sends the warped `200 x 200` image of each tile.

### 3.3 The `12` bar leaves

`VSYS · GND · D0+ · D0- · GND · BC+ · BC- · GND · D1- · D1+ · GND · VSYS`

1. The map is mirror symmetric. A front-back flip or a `180°` turn only swaps the lanes and the polarity. The PHY corrects both.
2. Display takes `4` leaves for `D0` and `D1`, and shares the `GND` leaves.
3. `BC` is a `400 Mb/s` back channel: touch at `480 Hz`, hinge angles, seam sense, telemetry and enumeration.
4. Two pairs carry `19.39 Gb/s`, so the design case has `40 %` margin.
5. With one pair lost, VDC-M `6 bpp` still fits one pair.
6. A spring leaf at `10 Gb/s` is `[HYPOTHESIS]`. Gate MON-23 gains an eye-diagram test.

### 3.4 The hinge mesh and the lines per hinge

`interface.py` solves the flow on the `8 x 16` mesh for each of the four seat tiles.

| The routing | Worst hinge load |
|---|---|
| the bound, total over the `3` root hinges | `4.44 Gb/s` |
| optimal table (LP) | `4.44 Gb/s` |
| optimal table with one root hinge broken | `6.66 Gb/s` |
| plain XY routing | `12.59 Gb/s`, rejected |

**The lanes**. Three bidirectional lanes at `3.2 Gb/s` per hinge carry `9.31 Gb/s`. That covers the broken-hinge case at `74 %` use. `[DECISION]`

**The route tables**. The validators compute them, and `U1` loads them at enumeration. The device runs no program. `[DECISION]`

**The lines per hinge**: `G D0+ D0- G D1+ D1- G D2+ D2- G BC+ BC- G`, so `13` lines.

### 3.5 The proof that it fits the hinge copper

| The check | The value |
|---|---|
| ribbon height, low end | `1.2 mm`, `0.1 mm` keep-out at each end |
| line and space | `15 / 15 µm`, one copper layer on the neutral plane |
| lines per ribbon | `33` |
| display share | `13` of `33`, so `39 %`; `20` lines remain for power, balance and Qi |
| copper strain, `2 µm` Cu centred, at `25 %` | `0.077 %` |
| copper strain at `41 %` | `0.197 %`, under the `0.2-0.3 %` endurance of thin copper `[GENERAL]` |
| line resistance over `0.8 mm` | `0.46 Ω` |
| pair impedance and length | about `191 Ω`, `1.9°` at Nyquist |
| reflection of the hinge step | `\|S11\| = 0.023`, `-32.6 dB`, harmless |

**The result**. The display lines fit one copper layer of the hinge in both modes. They need no liquid metal. `[DECISION]` gate MEC-42.

### 3.6 Addressing and timing

1. **The address**. Each hub learns its `(x, y)` by hop count. Its four ports are wired N, E, S and W.
2. **The identity**. Each hub holds a `64`-bit identity and its tile calibration. The calibration travels with the tile in a quadrant swap.
3. **The packet**. `[x3|y4|type4|line8|len12|payload|CRC32]`, the field widths in bits.
4. **The sync**. A broadcast packet carries a hop count. Every hub latches within `1 µs`.
5. **The latch**. Each tile latches when its slice is complete, so the face scans like a rolling shutter.
6. **The latency**. The worst path is `19` hops, about `0.5 µs`. One tile row of the frame arrives in `0.26 ms`.
7. **Partial update**. A static tile gets no packet, and its uICs hold the last frame.

---

## 4 · The stretched view: the warp requirement of `U1`

**The kinematics, checked**. Tile `(i, j)` turns by `(-1)^(i+j) θ`. The tile centres stay on a square lattice of pitch `10 (cos θ + sin θ) mm`. The hinge points meet to `1e-11 µm`. `warp.py`

| `θ` | Stretch | Pixel coverage |
|---|---|---|
| `17.5°` | `25.4 %` | `63.5 %` |
| `45.0°` | `41.4 %` | `50.0 %` |

**A note to Part 21**. Part 21.2.3 quotes `61 %` and `47.5 %`. Full-square pixel glass gives `63.5 %` and `50.0 %`. Chamfered glass would also put a hole in the lattice at rest. See Section 7.

**The requirement of `U1`, per frame, per tile `k`**. `[DECISION]` gates DSP-17 and SW-21.

1. Read `θ_k` for each tile at `480 Hz` over the back channel, as a `16`-bit angle.
2. For each pixel `u` of the tile, find its place `X = c_k + R((-1)^(i+j) θ_k) u`.
3. Sample the canvas at `X / s` in the zoom mode, or at `X` in the more-room mode.
4. Filter bilinear. Hold coordinates as `13` integer bits and `4` fraction bits.
5. Add the seam shift in `1/16` px steps, `3.125 µm`.
6. Scale the drive by `s²` when the user keeps the mean luminance.
7. Use angles at most one frame old, so the warp stays under the `10 ms` of SW-21.

| The load | The value |
|---|---|
| output | `5.12 Mpx` per frame, `1.23 Gpx/s` |
| bilinear taps | `4.92 Gtap/s` |
| source window per tile | `251 x 251` px at `17.5°`, `283 x 283` px at `45°` |
| more-room canvas | `2 007 x 4 014` at `25 %`, `2 263 x 4 525` at `41 %`, up to `30.7 MB` raw |

**The more-room mode exceeds the `16 MB` store raw**. It needs a compressed frame store of at least `2:1`. That is a requirement on `U1` and `U6`. The zoom mode needs no more store.

**The result, DSP-17 in the model**. A `25 mm` circle and a grid line, at `25 %` and `41 %`.

| The case | Circle error at `17.5°` | Circle error at `45°` |
|---|---|---|
| no warp | `7.38 %`, fails | `15.36 %`, fails |
| warp, exact angles | `0.10 %`, the pixel floor | `0.10 %` |
| warp, `0.5°` rms angle error | `0.42 %` | `0.32 %` |
| warp, `1.0°` rms angle error | `0.92 %` | `0.69 %` |

**The angle sensing target**. `0.1°` rms per tile. It moves a tile corner `0.25 px`, and the error stays near the floor. The hard limit for DSP-17 is `1.0°` rms. `out/stretched_view.png` shows both views.

---

## 5 · Yield and repair, gate DSP-19

The device carries `20.48 M` chips, `1.28 M` uICs and `36 864` TGVs. `yield_repair.py`

| Chip fault rate | uIC fault rate | Repairs per device | Line time at `2 s` | Tiles with zero dead pixels |
|---|---|---|---|---|
| `1e-4` | `1e-4` | `1 254` | `42 min` | `95.7` to `98.0 %` |
| `1e-5` | `1e-5` | `125` | `4.2 min` | `99.6` to `99.8 %` |
| `1e-6` | `1e-5` | `24` | `0.8 min` | `99.9 %` |

The model holds a repair success of `95` to `99 %` over two passes, and `0.2 %` inspection escapes. `[HYPOTHESIS]`

**The known-good tile is the answer**. A `1 cm²` tile is tested through its own hub before assembly. Only tiles with zero dead pixels go into a quadrant. So the dead count of a device comes from assembly damage. At `0.2` expected per device, `P(< 5) = 0.99994`. `[HYPOTHESIS]`

**The edge band rule**. A dead pixel within `2` px of a cut doubles the seam gap to `100 µm`. The bin rejects it, even when the tile count allows it.

**The real limit is repair time, not the dead count**. A chip fault rate of `1e-5` or better keeps repair under `5 min` per device. That is the mass-transfer target. `[DECISION]`

**The TGVs**. The data vias come in pairs, so a dead row bus needs two faults. The expected loss is `1.3e-6` rows per device.

---

## 6 · The gates of this file

| Gate | What this file adds |
|---|---|
| DSP-19 | the lattice proof; the `5 µm` RGBS quad; the known-good-tile bin; the edge band rule |
| DSP-17 | the per-tile affine warp; the `0.1°` sensing target, the `1.0°` limit |
| SW-21 | the warp at scan-out with angles at most one frame old |
| MEC-40 | the rest tile pitch `10.000 +0 / -0.002 mm` |
| MEC-42 | `13` display lines on one neutral-plane copper layer |
| MON-23 | an eye test of two `10 Gb/s` pairs across the leaves |
| **DSP-20, proposed** | the body link: `13.4 Gb/s` across the leaves and the mesh, bit error rate under `1e-12`, one hinge broken |
| **DSP-21, proposed** | one tile at `1 000 nits` full white under `25 mW`, colour within `0.005 Δu'v'` across a seam |

---

## 7 · The open issues

1. **The chamfer**. Part 21 chamfers the tile corners for the hinge. If the pixel glass is chamfered, each 4-tile corner shows a dark diamond at rest. The display requires full-square glass and caps. The chamfer lives only below the slip OCA. The hinge pivot must stay at the glass corner within `3 µm`, or the corners collide. Owner: mechanical team.
2. **The rest pitch**. The seam gap equals the pitch minus `9 950 µm`. A `+1 µm` pitch fails DSP-19. The `U1` image shift does not move a pixel. Owner: mechanical team, MEC-40.
3. **The edge margin rule**. The `16 µm` rule of Part 21 holds at the nominal `6 µm` kerf. At the `10 µm` limit the margin is `14 µm`. The display team asks Part 21 to read "at least `14 µm` over the kerf window".
4. **The hub seat**. Each tile needs a `1.6 x 1.6 x 0.08 mm` hub seat in the coil or spreader layer. Owner: stack team.
5. **The leaves**. The display asks for `4` of the `12` leaves and the `BC` pair. The power pins belong to the energy and port teams.
6. **The hinge lines**. The display takes `13` of `33` lines. Power, balance and the Qi strands share the other `20`.
7. **The overhead power**. `5.4 mW` per tile is `0.69 W` per device. The hub gates idle ports and static tiles to cut it.
8. **The red chip**. Direct red at `5 µm` runs near `500 A/cm²` at `1 000 nits`. That is why option B is the baseline.
9. **The frame store**. The more-room mode needs a `2:1` compressed store in `16 MB`. Owner: `U1` and `U6`.
10. **The seat tiles**. Part 21 does not fix the seat tile on each edge. The mesh study assumes the middle of each edge. Any edge tile works with its own route table.
