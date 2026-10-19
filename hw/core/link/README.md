# BUDLUM LEAF · CORE AND SKIN · LINK SEAT · THE PIXEL LINK AND THE SMALLEST SKIN

**Revision L.7 candidate · 2026-10-19 · seat link (new), block HP-2**. This is a study. It changes no L.6.0 or L.6.1 decision. Every result is `[HYPOTHESIS]` until a gate measures it. Every number comes from `python3 linkmodel.py`.

## 1 · The damage report, first

**The verdict**. The Split lives as a wired Skin at distance class C0 and C1. It dies as a cordless Skin. `[HYPOTHESIS]`

1. **A cordless Skin gives back the mass.** Wi-Fi 7 and 60 GHz carry no power. The Skin then holds `4.8` to `5.7 Wh` of cell.
2. **That cell is `81` to `97 %` of the `5.9 Wh` body.** The radio Skin weighs `48` to `52 g`. The L.6.0 body weighs `47 g`.
3. **Neither radio carries the design case.** The case is `13.1 Gb/s`. Wi-Fi 7 gives `2.5 Gb/s` typical. A 60 GHz client gives `3.7` typical.
4. **A full-face change fails the gate on radio.** Wi-Fi 7 gives p99 `38.9 ms`. 60 GHz gives `32.3 ms`. The gate is `30 ms`.
5. **Blockage breaks 60 GHz.** A hand costs `20 dB`. The p99.9 is `41 ms` even for a four-tile change.
6. **No Skin is empty.** A floor stays. It holds emitters, micro-ICs, `128` hubs with a decoder, a seat PHY and a safe screen.
7. **The mesh forces the decoder.** One hinge carries `9.31 Gb/s`. A raw stream needs `2.08:1` compression with one root hinge broken.
8. **The Lead's `6:1` is outside the published range.** DSC is rated at `8 bpp`. VDC-M is rated at `6 bpp`, which is `5:1` of `10` bit.
9. **The Lead's body column leaves out the tile hubs.** The Skin load is `0.95`, `1.57` and `1.97 W`. The Lead used `0.80` and `1.35 W`.
10. **Full motion at `240 Hz` fails the still-air limit.** `1.97 W` is over `1.73 W`. It passes in light wind at `2.37 W`.
11. **A second reading is worse.** If the Hub domain sits on the tiles, video is `2.59 W`. It fails both limits.
12. **Thin flex reaches `0.25` to `0.8 m`. Twinax reaches `1` to `3 m`.** Beyond that only fibre works.
13. **A coil power seat heats the Skin.** At `k = 0.2` the Skin keeps `0.44 W` for `1.8 W` delivered. Power stays on leaves.
14. **At C2 the Skin is the L.6.0 Leaf.** The decoder, the `16 MB` store and the compositor stay. The smallest Skin is a C0 and C1 result.

**What survives.** A `17 g`, `1.00 mm` Skin on a wired tether. It runs `240 Hz` DSC at `13.1 Gb/s` with a `0.1 ms` hop. `[HYPOTHESIS]`

## 2 · What is here

| The file | The content |
|---|---|
| `linkmodel.py` | the model, sections A to H, about `40 s` |
| `out/pixel_budget.txt`, `out/use_cases.csv` | Section A: codecs, use cases, stretch, mesh |
| `out/links.txt` | Section B: the options, the `60 GHz` budget, flex loss, inductive power |
| `out/skin_bom.txt` | Section C: the Skin mass, hub area, BOM, load, heat |
| `out/latency.txt` | Section D: the tether hop on Part 21 Section 21.5.7, the angle age |
| `out/power_link.txt` | Section E: the cable and pad design |
| `out/connector_life.txt` | Section F: mating and bend life |
| `out/distance_classes.txt` | Section G: C0, C1, C2 |
| `out/gates.txt` | Section H: HC-L1 to HC-L11 evaluated |
| `out/*.png`, `out/summary.json` | three figures and every number of the run |

**How to run.** Run `python3 linkmodel.py` in this directory. It needs `numpy` and `matplotlib`. `scipy` is not used. All were present in this environment.

The model imports `sim/latency/model.py` read only and writes no bytecode there. It writes only inside `out/`.

## 3 · The idea that organises the answer: link-as-clip

**The Skin has one seat.** It is the `12` gold leaf field of FINAL/21 Section 21.3.2. It holds two `10 Gb/s` pairs, two sideband pins, VBUS, VHV and GND. `[DECISION]` for the study.

**Every tether is a clip on that seat.** The clip holds the link silicon, the voltage conversion and the connector. The Skin does not know which link it has.

1. A cable clip is the "port part" of Section 21.3.4 with a flex pigtail.
2. A fibre clip holds the VCSEL, the photodiode and a hybrid pigtail.
3. A radio clip is the L.6.0 B module in disguise. It needs a cell.

This keeps the Lead's aim: a part change happens in the clip and not in the Skin. The clip heat sits outside the Skin heat budget. `[HYPOTHESIS]`

## 4 · The pixel budget

### 4.1 The raw and compressed rates, full face

The face is `1 600 x 3 200` px, `128` tiles of `200 x 200` px. Payload in Gb/s, no packet share, no line coding.

| Refresh | Raw 8 bit | Raw 10 bit | DSC 10 bpp | DSC 8 bpp | VDC-M 6 bpp |
|---|---|---|---|---|---|
| `60 Hz` | `7.37` | `9.22` | `3.07` | `2.46` | `1.84` |
| `120 Hz` | `14.75` | `18.43` | `6.14` | `4.92` | `3.69` |
| `240 Hz` | `29.49` | `36.86` | `12.29` | `9.83` | `7.37` |

With the first line of each slice and the line headers, DSC `10 bpp` at `240 Hz` is `12.71 Gb/s`. On the `128b/132b` lanes it is `13.10 Gb/s`. The display team's `13.43` uses a `1.06` packet share.

### 4.2 What compression is honest

| The codec | The honest range | The source |
|---|---|---|
| DSC 1.2b | up to `3:1`, "any image to `8 bpp`", so `3.75:1` of `10` bit | `[PUBLICATION]` VESA DSC page; Rambus |
| VDC-M 1.2 | up to `5:1`, `30` bpp to `6` bpp | `[PUBLICATION]` VESA press release, 2018 |
| The Lead's `4:1` | `7.5 bpp`, under the DSC rating, at the edge | `[HYPOTHESIS]` |
| The Lead's `6:1` | `5 bpp`, under the VDC-M rating, outside | `[HYPOTHESIS]` |

1. "Visually lossless" is a viewing test at phone density. The Leaf at `508 ppi` is close to that density.
2. Text edges and grey ramps are the known weak content. Gate HC-L2 tests them.
3. DSC and VDC-M are intra-only. A delta frame means skipping tiles or strips, not temporal coding.
4. The honest set is `3:1`, `3.75:1` and `5:1`. The floor is `7.4 Gb/s` payload at `240 Hz`.

### 4.3 The skin decoder, gates and watts

| The item | The value | The basis |
|---|---|---|
| DSC decoder per hub | about `60 kgate` and `3 kB` of buffer, `0.025 mm2` at `28 nm` | `[HYPOTHESIS]`, scaled from the encoder below |
| the reference encoder | `440 kgate`, `36.8 KB` SRAM, `0.6 mm2`, `2.0 Gpx/s`, `28 nm` | `[PUBLICATION]` UC Davis and Asilomar 2018; verify |
| energy per pixel | encoder `84` to `163 pJ`; decoder taken at `60 pJ` | `[PUBLICATION]` Wu 2021; decoder `[HYPOTHESIS]` |
| the whole face at `240 Hz` | `1.23 Gpx/s` times `60 pJ` is `74 mW` | model |
| VDC-M decoder | `8 x 2` blocks, at least `2` line buffers | `[PUBLICATION]` arXiv 2502.17729 |
| share of the hub logic | the decoder is `3 %` | model |

The decoder is cheap. The mesh ports, the analog fronts and the memory fill the hub.

### 4.4 The tile layout, the seams and the stretch

1. A tile sends `200` lines of `200` px. The seam rules of `hw/display` do not change the stream.
2. The seam shift is a `1/16` px step in the hub. It adds no bandwidth.
3. The warp stays in the Core. The stream is `5.12 Mpx` at every stretch. `[DECISION]` for the study.
4. A warp in the Skin grows the stream `1.58` times at `25 %` and `2.00` times at `41 %`.
5. At `41 %` that is `26.2 Gb/s`. It also needs a `4`-tap engine and a line buffer in each hub.
6. The cost of the Core warp is the age of the angles. Section 7.4 holds it.

### 4.5 The bandwidth by use case

Mb/s before line coding, DSC `10 bpp`, `10` bit. Tile mode sends whole `200 x 200` slices. Strip mode sends `16`-line strips. The dirty fractions are `[HYPOTHESIS]`.

| The use case | fps | Tile mode | Strip mode | VDC-M `6 bpp`, tile |
|---|---|---|---|---|
| static page, cursor and clock | `10` | `10.6` | `2.2` | `6.5` |
| UI, typing, small animation | `60` | `762` | `278` | `467` |
| mixed delta session | `60` | `1 324` | `902` | `812` |
| scroll, `85 %` of the face | `60` | `2 700` | `2 760` | `1 656` |
| scroll, `85 %` of the face | `120` | `5 400` | `5 520` | `3 311` |
| video `16:9` in portrait | `30` | `496` | `456` | `304` |
| video vertical | `60` | `2 827` | `2 890` | `1 733` |
| full motion | `120` | `6 353` | `6 494` | `3 895` |
| full motion | `240` | `12 706` | `12 988` | `7 791` |

1. The panel scans at `240 Hz` from the uIC buffers. The link carries only frames that change.
2. Only full motion needs `240 Hz` on the link. A video session needs `0.5` to `2.8 Gb/s`.
3. The Skin has no frame store. A scroll is a full update of the view, so it costs as much as a video.
4. The Part 21 local compositor cannot sit on a Skin with no store. It stays in the Core.
5. A page turn is a burst of `52.9 Mbit`. Section 7.2 gives the time to draw it.

### 4.6 The hinge mesh

| The stream, `240 Hz` | Root hinge, `3` hinges | Root hinge, one broken | Against `9.31 Gb/s` |
|---|---|---|---|
| raw `10` bit | `12.92` | `19.39` | fails |
| DSC `10 bpp` | `4.31` | `6.46` | fits |
| VDC-M `6 bpp` | `2.58` | `3.88` | fits |

The mean retime path is `7.5` to `9.5` hops. The retime load is the largest hub load. It is `0.34 W` at full motion. Heavier compression cuts it in step.

## 5 · The link options

### 5.1 The comparison

Net payload is after line coding. Power is the Skin end at the design case. The sources are in 5.3. Cost is a class and a rough USD per end. `[HYPOTHESIS]`

| Option | Net Gb/s, low, typical, high | Latency, fixed | Skin-end power | Range | Class | Cost |
|---|---|---|---|---|---|---|
| (a) `12` contact leaves | `9.7`, `19.4`, `19.4` | `2 µs` | `85 mW` | touching | C0 | low, `3` |
| (b) flex or ribbon, connector | `9.7`, `19.4`, `38.8` | `2 µs` | `85 mW` | `0.25` to `0.8 m` | C0 | low to mid, `8` |
| (c) fibre tether | `19.4`, `48.5`, `97` | `3 µs` | `90 mW` | to `100 m` | C0, C1 | mid to high, `25` |
| (d) `60 GHz` radio | `1.8`, `3.7`, `7.4` | `0.5 ms` | `600 mW` | LOS to `18 m`; `1.8 m` blocked | C0, C1 LOS | high, `30` |
| (e) near-field coupler | `5.4`, `18`, `18` | `1 µs` | `45 mW` | `1` to `5 mm` | C0 seat | mid, `10` |
| (f) Wi-Fi 7, `2 x 2`, `320 MHz` | `1.0`, `2.5`, `3.5` | `1 ms` | about `1 W` | `30 m` | C0, C1 | mid, `6` |
| (f) UWB, 802.15.4z | `0.007`, `0.027` | `0.5 ms` | `200 mW` | `30 m` | C0, C1 | low, `4` |

### 5.2 The heat, the failure modes and the cell

| Option | The heat at the Skin | The failure modes | A cell on the Skin |
|---|---|---|---|
| (a) leaves | `85 mW` of PHY, leaf loss `14 mW` at peak | wear, dirt, salt, eye margin at `10 Gb/s` | no |
| (b) flex | the same; the cable heats itself `0.19 W` at peak | connector wear, kink, shield break, EMI | no |
| (c) fibre | `90 mW`; the clip holds the optics | dust on the core, glass break, bend under `5 mm` | no |
| (d) `60 GHz` | `0.6 W` plus the cell and the buck | hand blockage, beam retrain, `40 dBm` EIRP rule | `4.8 Wh` |
| (e) coupler | `45 mW`; a coil for power adds `0.25` to `0.9 W` | gap and tilt, metal near the pads | no, if power is on leaves |
| (f) Wi-Fi 7 | about `1 W` plus the cell and the buck | contention, DFS, SAR, band collision with the Core | `5.7 Wh` |

### 5.3 The sources and what they hold

| The number | The source |
|---|---|
| `60 GHz` close-range, up to `6 Gb/s` | `[PUBLICATION]` Keyssa Kiss, bought by Molex |
| `6 Gb/s`, `6 pJ/b`, `5 mm`, `6 mm2` coupler | `[PUBLICATION]` ISSCC 2015, paper 10.1 |
| `10 Gb/s` QPSK at `340 mW`; MAC link `1.8 Gb/s` at `40 cm` for `788` and `984 mW` | `[PUBLICATION]` Tsukizawa et al., 802.11ad chipset |
| `10.56 Gb/s` at `186`, `155` and `64 mW`; `64QAM` to `0.13 m` | `[PUBLICATION]` Okada et al., 802.11ad and ay |
| Wi-Fi 7 peak `5.76 Gb/s`; measured `3.5` to `3.7 Gb/s` close; `1 Gb/s` at `40 ft` | `[PUBLICATION]` Intel footnote; WBA and press |
| `5 mm` bend radius for G.657.B3 | `[PUBLICATION]` ITU-T G.657, 2024 |
| `25G` VCSEL cable under `1 W`; `10.3 mW/Gbps` HDMI driver | `[PUBLICATION]` vendor listings; driver paper |
| A-PHY `16 Gb/s`, `6 µs`, `15 m` | `[PUBLICATION]` MIPI Alliance |
| USB-C `10 000` mating cycles | `[PUBLICATION]` USB-IF |
| UWB `6.8` and `27.2 Mb/s` | `[PUBLICATION]` IEEE 802.15.4z |
| pogo `1` to `3 A`, `20` to `50 mΩ`, `10 000` to `100 000` cycles | `[GENERAL]` vendor guides |

The `85 mW` PHY, the `90 mW` optics, the `600 mW` and `1 W` radio ends are `[HYPOTHESIS]`. They come from the pJ/b values above.

### 5.4 Which options carry which stream

| Option | `240 Hz`, DSC `10` | `240 Hz`, VDC-M `6` | `120 Hz`, DSC `8` | `60 Hz` scroll or video | Delta and UI |
|---|---|---|---|---|---|
| (a) leaves | both pairs | yes | yes | yes | yes |
| (b) flex | both pairs | yes | yes | yes | yes |
| (c) fibre | yes | yes | yes | yes | yes |
| (d) `60 GHz` | no | no | no | typical rate only | yes |
| (e) coupler | `3` couplers | typical rate | yes | yes | yes |
| (f) Wi-Fi 7 | no | no | no | no | yes |
| (f) UWB | no | no | no | no | no, control only |

"Both pairs" means the stream needs both lane pairs. With one pair lost, VDC-M `6 bpp` still fits (HC-L1b).

### 5.5 The `60 GHz` budget

The model uses `8 dBm` transmit power and `8.8 dBi` at the Skin (A4). Noise figure is `7 dB` and implementation loss is `8 dB`. It allows `16QAM` and `2` channels at most.

| Distance | LOS, Core `8.8 dBi` | LOS, Core `20 dBi` | Blocked `20 dB`, Core `20 dBi` |
|---|---|---|---|
| `1 m` | `9.2 Gb/s` PHY | `9.2` | `4.6` |
| `2 m` | `9.2` | `9.2` | `2.3` |
| `5 m` | `4.6` | `9.2` | none |
| `10 m` | none | `4.6` | none |
| `30 m` | none | none | none |

Net payload is `0.8` of PHY. The range for `2.6 Gb/s` net is `18 m` in LOS and `1.8 m` blocked. For `5.1 Gb/s` it is `8 m` and `0.8 m`. The `7.8 Gb/s` VDC-M case is not carried.

### 5.6 The copper and the coil

| The item | The result |
|---|---|
| LCP flex trace, `100`, `200`, `400 µm` wide | `49`, `26`, `15 dB/m` at `5 GHz`; `12 dB` reach `0.24`, `0.46`, `0.82 m` |
| shielded twinax, `30`, `34`, `40` AWG | reach `1.2` to `3.3 m` at `12 dB` |
| coil power, `k 0.4`, Q `30` | efficiency `0.85`; Skin heat `0.25 W` at `1.8 W` out |
| coil power, `k 0.2`, Q `30` | efficiency `0.72`; Skin heat `0.44 W` at `1.8 W` out |
| near-field data, design case | `3` coupler pairs, `18 mm2`, `39 mW` Skin share |

## 6 · The smallest Skin

### 6.1 The BOM, the mass and the area

| The part | Count | Area and mass | The duty |
|---|---|---|---|
| face stack: cap, OCA, glass and LED, slip OCA, hub layer, back skin | one face | `12 800 mm2`, `1.00 mm`, `15.8 g` | the surface |
| hinges, `232` ribbons, pins | `232` | `0.9 g` | the joints |
| tile hub die | `128` | `2.56 mm2` each, `0.06 g` total | decoder, row drivers, mesh, touch, angle |
| micro-IC, `28 nm` | `1.28 M` | `21.8 cm2` in the streets | the pixel drive |
| seat controller | `4` | `9 mm2`, `40 mg` each | PHY, crossbar, dead pad, ROM, trip |
| identity, no wallet key | `1` | `6 mm2`, `60 mg` | part record and link key |
| accelerometer | `1` | `4 mm2`, `30 mg` | the Skin orientation |
| thermistor | `128` | `0.5 mm2` each | heat sense |
| bridge cell, one tile cell | `1` | `46 mWh`, `1.2 g` | safe screen and swap |

**The Skin mass is `17.0 g`** without cells, coil or module. The L.6.0 body is `47 g`. The Skin is `64 %` lighter. `[HYPOTHESIS]`

**The hub die.** The parts sum to `0.76 mm2` of the `2.56 mm2` die. The decoder is `0.025 mm2`.

### 6.2 What leaves the Skin

These parts leave: U1, U6 with its `16 MB` store, U2A, U2B, U5, U7, U8, U3 and U4. The camera and audio paths leave too. So do the `128` cells, the `4` U_Q chargers and the Qi coils.

### 6.3 Is everything off the screen possible

No. A floor remains.

1. A pixel needs its own driver. The count of lines forces the micro-ICs.
2. A touch grid is analog. A hinge angle is a local analog value.
3. The mesh copper forces a decoder, whatever the tether.
4. A lost link needs a screen that says so. A heat limit needs a trip that does not wait for the Core.
5. A pairing needs a part identity. It holds a link key and no wallet key.

### 6.4 The Skin load, W

| The case | Body column | Hubs, mesh, PHY | Skin | Reading R2 |
|---|---|---|---|---|
| safe screen | `0.120` | `0.029` | `0.149` | `0.130` |
| static page | `0.170` | `0.099` | `0.268` | `0.196` |
| delta session | `0.800` | `0.154` | `0.954` | `1.530` |
| video Wi-Fi | `1.350` | `0.217` | `1.567` | `2.589` |
| full motion `240 Hz`, `250 nits` | `1.350` | `0.615` | `1.965` | `2.635` |

**The limits.** `1.73 W` still and `2.37 W` light wind at `25 °C` for the whole L.6.0 body. A ringless plate bound is `3.15 W`. `[HYPOTHESIS]`

**Reading R2.** The energy table has a Hub domain of `0.70` and `1.20 W` in the ring column. It equals `5.4 mW` per tile. If it is the tile electronics, it moves to the Skin. The heat seat and the power seat must settle it.

### 6.5 The choice

| The pick | The link | The reason |
|---|---|---|
| **first Skin** | (a) and (b): the `12` leaves with a `0.3 m` flex clip | carries `240 Hz` and power in one cable, `0.1 ms`, `85 mW`, low cost, already designed |
| **stretch goal** | (c): a hybrid fibre clip, `1` to `30 m`, Skin unchanged | adds C1 reach, `5 ns/m`, raw rate headroom, no EMI |
| **sealed variant** | (e) data coupler with power on leaves | no exposed data contact; coil power is rejected for heat |
| **not for the Skin** | (d), (f) | no power path, no `240 Hz`, a cell returns |

1. The leaf eye at `10 Gb/s` is unproven. Gate MON-23 and HC-L1 test it.
2. The flex clip keeps a user connector of `10 000` cycles. A ZIF connector gives `30`.
3. The stretch fibre keeps the Skin silicon the same. Only the clip changes.

## 7 · Latency

### 7.1 The method

The baseline is `sim/latency/model.py`, `400 000` samples per path. The tether adds the touch uplink and the downlink of the dirty tiles. K is the number of tiles that change.

| Path | Baseline mean | Baseline p99 |
|---|---|---|
| Wi-Fi, room validator | `12.8 ms` | `16.1 ms` |
| 5G, cell-site validator | `16.5 ms` | `21.5 ms` |

### 7.2 The result

p99 in ms. The gate is `30 ms`.

| Option | Wi-Fi room, K=4 | K=32 | K=128 | 5G cell, K=4 | K=128 | p99.9, K=4 |
|---|---|---|---|---|---|---|
| (a), (b), (c) wired | `16.2` | `16.8` | `18.9` | `21.6` | `24.3` | `17.3` |
| (e) coupler | `16.2` | `16.9` | `19.2` | `21.6` | `24.6` | `17.3` |
| (d) `60 GHz` | `18.8` | `21.5` | `32.3` | `24.5` | `38.2` | `41.2` |
| (f) Wi-Fi 7 | `18.4` | `23.0` | `38.9` | `23.7` | `44.2` | `19.7` |
| (f) UWB | `79` | `508` | `1 979` | `85` | `1 984` | `80` |

1. **The wired tether adds `0.094 ms`** at K=4. The `30 ms` p99 holds with `8 ms` to spare on the 5G path.
2. **A full-face change on wired costs `2.8 ms`** (DSC `10`) or `1.7 ms` (VDC-M `6`).
3. **Wi-Fi 7 needs `21 ms`** for the same page turn. 60 GHz needs `10.6 ms`.
4. **60 GHz fails at p99.9.** Blockage adds up to `30 ms` with a `0.5 %` chance. `[HYPOTHESIS]`
5. **UWB carries no pixels.** One tile at `27 Mb/s` takes `15 ms`. It carries touch, angles and the heartbeat.

### 7.3 The mitigation

A tile-local scan restart lowers the Wi-Fi room p99 from `16.1` to `13.1 ms`. It needs a hub mode that restarts the tile row when its slice lands. The hub does this by nature. A sprite echo in the hub (cursor, touch ripple) hides a radio hop. It costs a few kgate per hub. It is not needed for wired.

### 7.4 The angle age of the Core warp

The Core warps from angles sampled at `480 Hz`. The age is `1.55 ms` on a wired tether and `3.11 ms` on Wi-Fi 7.

| Option | rms error at `100 deg/s` | at `300 deg/s` | with a predictor, `100 deg/s` |
|---|---|---|---|
| wired | `0.17 deg` | `0.50 deg` | `0.06 deg` |
| `60 GHz` | `0.30 deg` | `0.89 deg` | `0.20 deg` |
| Wi-Fi 7 | `0.32 deg` | `0.96 deg` | `0.07 deg` |

The DSP-17 limit is `1.0 deg` rms and the target is `0.1 deg`. The `480 Hz` sample dominates the age. The tether adds little. The uplink needs `5.6 Mb/s`.

## 8 · Power in the link

### 8.1 The result

The tether carries the Skin power with the data. The Skin loads are `0.95` (delta), `1.57` (video) and `3.75 W` (peak, full white at `1 000 nits`).

| The design | Source | Loop | Peak current | Skin end at peak | Cable loss at peak |
|---|---|---|---|---|---|
| `12` leaves, dock pads | `4.2 V` | `18 mΩ` | `0.90 A` | `4.18 V` | `14 mW` |
| flex `0.3 m`, `2` strips per side | `5.0 V` | `0.312 Ω` | `0.79 A` | `4.75 V` | `0.19 W` |
| round `28` AWG, `2 m`, at `5 V` | `5.0 V` | `0.443 Ω` | `0.81 A` | `4.64 V` | `0.29 W` |
| round `28` AWG, `2 m`, `12 V`, clip buck | `12 V` | `0.443 Ω` | `0.34 A` | `11.85 V` | `0.05 W` |
| hybrid fibre, `10 m`, `20 V`, clip buck | `20 V` | `4.25 Ω` | `0.21 A` | `19.1 V` | `0.19 W` |
| hybrid fibre, `30 m`, `20 V`, clip buck | `20 V` | `5.03 Ω` | `0.21 A` | `18.9 V` | `0.23 W` |

1. Each leaf carries `0.45 A` at peak. The rating is `1.5 A`.
2. The sinks need `3.40 V`. The design keeps `3.60 V` at the Skin end.
3. The buck sits in the clip. Its `7 %` loss (`0.13 W` at video) is clip heat.
4. The tether has `8` data lines and `4` power conductors. A `0.3 m` flex of `12` lines weighs `1.3 g`.
5. A radio carries no power. A coil seat heats the Skin by `0.25` to `0.9 W`.
6. A hot unplug needs `2 mWh` for `60 s` of safe screen. One tile cell holds `46 mWh`.

## 9 · Distance classes

| The option | C0, to `2 m` | C1, to `30 m` | C2, kilometres |
|---|---|---|---|
| (a) leaves | yes | no | no |
| (b) flex or twinax | yes | no | no |
| (c) fibre | yes | yes | no |
| (d) `60 GHz` | yes | LOS only, to `18 m` | no |
| (e) coupler | mm only | no | no |
| (f) Wi-Fi 7, UWB | yes | yes | no |
| Leaf radios: U5, U2A, bar and ring antennas | yes | yes | yes |

**C2 carries slice streams only.** An AV1 or HEVC stream is `0.1` to `31 Mb/s` in the low estimate. The high estimate reaches `125 Mb/s`. `[HYPOTHESIS]` The DSC stream is `107` to `427` times larger.

**What stays on the Skin at C2.** It is the L.6.0 Leaf:

1. the U6 AV1 and HEVC decoder;
2. the frame store, `15.4 MB` at `8` bit, `19.2 MB` at `10` bit, `30.7 MB` for the more-room canvas;
3. the U1 compositor and the `4.92 Gtap/s` warp;
4. U2A, U2B, U5, U7 and the `5.9 Wh` cell.

**Why.** At C2 the path takes more than `1 ms` to `20 ms` by air. The predicted-action path of Part 21 needs a local store. The Skin is `47 g` and `2.02 W` (delta) plus the module.

**Result by class.**

| The class | The smallest Skin | The mass | The load, video |
|---|---|---|---|
| C0 wired | the common Skin | `17 g` | `1.57 W` |
| C1 fibre | the common Skin plus a `4 g` clip | `21 g` | `1.57 W` |
| C1 `60 GHz` | the common Skin, a radio, a cell | `48 g` | `2.17 W` |
| C1 Wi-Fi 7 | the common Skin, a radio, a cell | `52 g` | `2.57 W` |
| C2 | the L.6.0 Leaf | `47 g` plus module | `3.27 W` |

The smallest Skin is a C0 and C1 wired result. The far seat `hw/core/far/` owns the C2 budget.

## 10 · Connector and cable life

| The part | Cycles | Years at `4` mates a day |
|---|---|---|
| FPC ZIF or board-to-board | `30` | `0.02` |
| USB-C receptacle | `10 000` | `6.8` |
| gold leaf or pogo, wearable class | `30 000` | `20.5` |
| expanded-beam optical | `5 000` | `3.4` |
| near-field coupler on a kinematic seat | `100 000` | `68` |
| flex, `5 mm` radius | `200 000` bends | `137` |

A user tether needs `10 000` cycles or more. A ZIF connector fails in a month.

## 11 · The proposed gates

| Gate | The condition | Pass | Model |
|---|---|---|---|
| **HC-L1** | the design case crosses the tether, BER under `1e-12`, `25 %` eye margin | `13.1 x 1.25 = 16.4` under `19.4 Gb/s`, one-lane fallback `8.0` under `9.7` | pass |
| **HC-L2** | DSC `10`, `8` and VDC-M `6 bpp` on the Leaf test set, with text edges and grey ramps, at `508 ppi` | ISO/IEC 29170-2 flicker test at the standard's limit for `90 %` of images | needs a test |
| **HC-L3** | Skin load with the link PHY at the tile | delta under `1.73 W`; video under `2.37 W`; full motion under `1.73 W` | `3` of `5` pass |
| **HC-L4** | tether power at peak `3.75 W` from `5.0 V` | Skin end at least `3.60 V`, loop under `0.35 Ω`, cable loss under `0.25 W` | pass |
| **HC-L5** | input to photon, `30 ms` p99, wired tether | K=128 under `30 ms` on Wi-Fi room and 5G cell; tether adds under `0.5 ms` p99 at K=4 | pass |
| **HC-L6** | angle age of the Core warp | rms error at most `1.0 deg` at `100 deg/s`; target `0.1 deg` with a predictor | pass |
| **HC-L7** | the seat and tether life | at least `10 000` mating cycles, contact at most `50 mΩ`; flex at least `100 000` bends | pass in model |
| **HC-L8** | the Skin mass and thickness | at most `20 g` and under `1.2 mm`, no cells | `17.0 g`, `1.00 mm` |
| **HC-L9** | the safe screen and the trip | safe screen within `100 ms` of heartbeat loss; thermal trip with no Core; no key on the Skin that signs a spend | bench test |
| **HC-L10** | the decoder floor | the stream needs at least `2.08:1` with one root hinge broken; DSC `10` gives `3:1` | pass |
| **HC-L11** | the C2 stream | at most `150 Mb/s` for every use case | `125 Mb/s` high estimate |

The FAIL lines of `out/gates.txt` are HC-L3 full motion (`1.97 W`) and reading R2 (`2.59 W`), plus the radio rows of HC-L5. They are the damage in Section 1.

## 12 · The open issues

1. **The leaf eye.** A spring leaf at `10 Gb/s` is unproven (MON-23). One pair fails to VDC-M `6 bpp` at best.
2. **The hub power.** Reading R1 (`0.95` to `1.97 W`) or R2 (`1.53` to `2.64 W`) decides if video passes. The power and heat seats must say.
3. **The heat limit.** `1.73 W` is for the whole body with a ring hot spot. A ringless Skin has no hot spot. The heat seat sets the Skin limit.
4. **The DSC decoder cost.** No decoder datasheet is public. `60 kgate` and `60 pJ/px` are scaled from an encoder. Verify with a vendor quote.
5. **The 60 GHz and Wi-Fi 7 power.** The `0.6` and `1.0 W` ends come from papers and a guess. A part quote replaces them.
6. **Visually lossless at `508 ppi`.** The VESA tests ran at phone densities. Gate HC-L2 closes this.
7. **The dirty fractions.** The use cases are `[HYPOTHESIS]`. A trace of real Leaf sessions replaces them.
8. **The clip heat.** The clip sits on the Skin edge. A share of its `0.1` to `0.2 W` reaches the seat tile.
9. **Several Skins on one Core.** The session seat owns it. One wired tether per Skin. A fibre Skin shares a Core of `4 x 20 Gb/s`.
10. **The far seat.** `hw/core/far/` was empty at this run. The C2 numbers here are a bitrate model, not a link budget.
11. **The mass of a cell-free Skin.** The `46 mWh` bridge cell is one of the `128` tile cells. The power seat must confirm the pack split.
12. **The Part 21 edits.** Section 21.2.3 coverage, the `6:1` claim and the hub row of `hw/energy/04` need an owner.
