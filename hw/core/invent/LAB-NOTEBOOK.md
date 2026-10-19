# BUDLUM LEAF · THE SEARCH FOR AN UNLIMITED BATTERY · THE LAB NOTEBOOK

**Revision L.7 candidate · 2026-10-19 · the Program Lead, with no sub-agent**. Ayaz asked for an invention. The battery can sit in the Leaf if it is very small. The whole event lives in the hardware, so the energy is unlimited. Ayaz also set the method: try wild directions, fail, and go on. `[DECISION]`

**The method of this notebook**. Each direction gets a test with a script, `explore.py`. A failure is written down with its number. A direction that survives is the one that fails last. Every figure is `[HYPOTHESIS]` unless a source is named.

## 1 · The question in numbers

| The need | The value | The source |
|---|---|---|
| wallet standby today | `61 mW` | `[TREE]` `hw/energy/04` |
| Skin delta session | `0.95 W` | `[TREE]` `hw/core/link` |
| Skin video session | `1.57 W` | `[TREE]` `hw/core/link` |
| the B cell, the tiny battery that already exists | `0.144 Wh` | `[TREE]` `hw/energy` |
| sustained heat in free air, `25 °C` | `1.73 W` for the L.6.0 body, `2.93 W` for a Skin | `[TREE]` `hw/hostpower/thermal`, `hw/core/heat` |

**The test of every door**. Does the energy that arrives cover the need, and does the heat stay under the limit?

## 2 · The failures, in the order they happened

### Direction 1 · Far-field radio power

| The idea | The Core beams radio power to the Leaf, like Wi-Fi |
|---|---|
| The test | the whole face as an ideal rectenna at the exposure cap of `10 W/m2` |
| The result | `26` to `64 mW`, and `256 mW` at the optimistic `40 W/m2` |
| The second test | a legal Wi-Fi transmitter of `36 dBm` EIRP gives `1.2 mW` at `1 m` and `0.14 mW` at `3 m` |
| The verdict | **fails by `15` to `40` times** for a session |
| The lesson | the cap protects the person who holds the Leaf, so no Core antenna can raise it |

`[PUBLICATION]` ICNIRP 2020 sets `10 W/m2` for the public above `2 GHz`, and the FCC sets `1 mW/cm2`, which is the same number. The two sources agree.

### Direction 2 · Magnetic power across a room

| The idea | a large coil in the ceiling or the desk feeds the small Leaf coil |
|---|---|
| The test | coaxial loops, `Q` of `200` and `60`, a `46 mm` receiver coil, by the Neumann formula |
| The result | a `150 mm` pad gives `49 %` at `1 cm`, `7 %` at `10 cm` and `0.04 %` at `30 cm` |
| The second test | a `400 mm` desk mat gives `4 %` at `10 cm`, a `1 m` ceiling loop gives `0.4 %` at `10 cm` |
| The verdict | **fails beyond about `10 cm`** |
| The lesson | one big coil is worse than many small coils under the Leaf, as free positioning mats show |

`[GENERAL]` The coupling falls with the cube of the distance over the coil size. The model is crude and it is an upper bound for a mismatched pair.

### Direction 3 · Power through the body

| The idea | the worn Core pushes a small current through the hand that holds the Leaf |
|---|---|
| The test | `60 V` SELV at `0.5` and `2 mA` |
| The result | `24` and `96 mW` |
| The verdict | **fails by `10` to `40` times**, and it needs two skin contacts |
| The lesson | the safety limit on touch current is the ceiling |

`[HYPOTHESIS]` The touch current limits are recalled from IEC 60990, and not read.

### Direction 4 · Energy from the stretch

| The idea | the body stretches `25 %`, so the stretch charges the cell |
|---|---|
| The test | an `80 µm` TPU skin of `128 cm²`, a dielectric elastomer generator at `5` and `30 %` |
| The result | one stretch stores `0.64 J`, and the hinge life of `10 000` cycles gives `0.09` to `0.53 Wh` in total |
| The verdict | **fails**: one video hour is `3.65 Wh` |
| The lesson | the cycle life of the hinge is the limit, so the design that stretches cannot also live on stretching |

### Direction 5 · One light beam for power and pixels

| The idea | an infrared beam feeds the Leaf and carries the pixel stream |
|---|---|
| The test | the best published receivers, against the `13.1 Gbit/s` of the Skin stream |
| The result | the power converter carries `3.8 Gbit/s`, which is `3.4` times short, and the multi-junction type carries about `1 Gbit/s` |
| The verdict | **fails for the pixels**, and it passes for the power alone |
| The lesson | the data needs a separate photodiode of `66` to `131 mW` |

`[PUBLICATION]` The `3.8 Gbit/s` result uses a multi-segment GaAs converter at `39.7 %`. Multi-junction InGaAsP reaches above `55 %` with gigabit data over `3 m`. See Section 7.

### Direction 6 · The passive Sheet, light from the hardware

| The idea | the Leaf has no emitter, and the Core paints it with light |
|---|---|
| The test | the flux, the ambient wash and the scan rate |
| The result | `12.6 lm` lights a diffuse sheet to `250 nits`, and a retroreflective sheet needs `0.25` to `1.3 lm` |
| The second result | a diffuse sheet gets `127` nits of ambient in an office, `2 546` in shade and `25 465` in sun, against a `250` nit image |
| The third result | a laser scan of `1356` lines needs `81 kHz` at `60 Hz` and `325 kHz` at `240 Hz`. A fast MEMS mirror gives about `60 kHz` |
| The verdict | **fails for the handheld Leaf**, and it works only as a head-worn projector with one viewer |
| The lesson | the emitter is `76 %` of the cost, so removing it is the biggest saving, and light alone cannot replace it in a hand |

`[PUBLICATION]` Head-mounted projection with a retroreflective screen is a studied field. Pico-projectors of `15` to `30 lm` give a usable image. The castAR product that used it did not ship and was liquidated in `2017`.

## 3 · What survived

### Direction 7 · Light in, on the right face

| The test | a GaAs panel of `25 %` on `80 %` of the face, from `100` to `1000 lux` |
|---|---|
| The result | `0.8`, `2.4` and `8.1 mW`, against a floor of `50 µW` |
| The catch | the panel must face the light, and a Leaf that lies face up gets `0` on its back |
| The second result | the face as a micro-LED photodiode gives `18` to `182 µW` at `1 %`, and nobody has measured that `1 %` |
| The third result | one sun on the back gives `2.56 W`, with the heat of that sun not counted |
| The verdict | **survives for the heartbeat**, if the geometry is solved |

### Direction 8 · The heat of the pocket

| The test | a thermoelectric patch of `20 µW/cm²` on half the face |
|---|---|
| The result | `1.3 mW` in a pocket, where there is no light |
| The verdict | **survives for the heartbeat**, and the figure is recalled and not measured |

### Direction 9 · The tap

| The test | the energy of one near-field tap, `15` to `40 mJ` |
|---|---|
| The result | enough for one signature of `1` to `20 mJ`, and for a badge on a bistable layer |
| The verdict | **survives**: a dead Leaf can still sign and show a badge |
| The limit | one tap covers `1` to `16 %` of a full face, so a tap gives a badge and not a page |

### Direction 10 · The Paper layer

| The idea | a bistable reflective layer holds an image at `0 W` and costs energy per update |
|---|---|
| The test | a `7.6 cm²` panel at `15` to `75 mJ`, scaled to `128 cm²` |
| The result | `0.25` to `1.26 J` for a full update, and a third of that for a partial update |
| The feed | `8 mW` of indoor light gives a partial update every `11` to `53 s`. `64 mW` of radio gives one every `1` to `7 s` |
| The verdict | **survives**: the face is never black |
| The place | the `0.90 mm` cell layer, which is free once the cells leave the Skin |

### Direction 11 · The heartbeat floor

| The part | The power |
|---|---|
| secure element in deep sleep | `1` to `5 µW` |
| wake-up receiver | `0.3` to `3 µW` |
| power chip quiescent current | `2` to `8 µW` |
| real-time clock | `0.3` to `1 µW` |
| touch or motion wake | `5` to `20 µW` |
| near-field tag listen | `1` to `5 µW` |
| bistable glance layer, holding | `0` |
| **the sum** | **`9.6` to `42 µW`**, which is `1 450` to `6 350` times under today's `61 mW` |

`[PUBLICATION]` Wake-up receivers reach sub-microwatt to a few microwatts. `[HYPOTHESIS]` The other lines are recalled and need a datasheet each.

## 4 · The hard result: the tiny cell and the active hour

| The day away from any host | The energy | The B cell lasts |
|---|---|---|
| heartbeat and `100` partial Paper updates, no active use | `2.5` to `3.2 mWh` | `40` to `53` days |
| the same with `300` updates of a third of a face | `35` to `36 mWh` | `3.6` days |
| `100` updates and `5` minutes of delta session | `82 mWh` | `1.6` days |
| `100` updates and `15` minutes of delta session | `240 mWh` | `0.5` day |

**The reading**. The `0.144 Wh` cell carries the heartbeat for months and the Paper layer for days. Five minutes of a bright session spend more than half of it. `[HYPOTHESIS]`

**The law that follows**. A tiny cell covers everything except the bright active hour. The bright active hour must be hosted. `[DECISION]`

## 5 · The conclusion

### 5.1 The three zones of a Leaf

| The zone | The energy | The Leaf shows | The cell does |
|---|---|---|---|
| **Heartbeat** | microwatts, always | nothing, but it listens and it signs on a tap | carries it for months |
| **Paper** | millijoules per update, from light, heat, radio, the tap or the cell | a held image, text, a map, a balance | carries it for days |
| **Light** | watts, from a host | the full micro-LED surface | bridges between hosts for minutes |

### 5.2 Where the host stands

| The place | The host | The proof in this notebook |
|---|---|---|
| a desk, a table, a car console, a stand | the surface under the Leaf: contact or near field | direction 2: the field works within `10 cm` |
| a hand, a street, a train | a worn Core with a thin breakaway cable | directions 1, 2, 3 and 5: nothing wireless carries watts to a held Leaf |
| a pocket, a bag | the heartbeat and the tap | directions 8 and 9 |
| a room with a lamp | light on the face, for the heartbeat only | direction 7 |

**The geometry law**. Energy comes from below and information goes up. The Leaf rests on its back, and its face looks at the user. A light beam or a lamp sees the face. So the face-side surface is the only wireless way in, and a micro-LED face cannot be a good solar panel. `[HYPOTHESIS]`

### 5.3 The honest answer to "unlimited"

The battery is unlimited in the places where a host stands. It is not unlimited in a held hand in the open air. No tested physics carries watts to a held Leaf without a wire. The wire is the answer for that zone, and every shipping host-powered display, such as tethered glasses, already uses it. `[DECISION]`

### 5.4 What is an invention here, and what is not

| The element | The state |
|---|---|
| power by radio, light, coil, body or stretch | not new, and each fails or sits at a known limit |
| a cable to a worn Core | not new: tethered glasses and compute packs |
| a free positioning mat | not new: Qi furniture and car mats |
| a near-field powered e-paper tag | not new, on a small panel |
| a bistable layer beside an emissive layer | not new as two screens in one phone, and rare as one layered face |
| **the Heartbeat Law as a design rule of a full-size stretchable wallet surface** | **not yet searched**: a floor of tens of microwatts, a Paper layer in the freed cell layer, a host-only bright mode. Gate CSK-1 |
| **the cell reduced to the one that already exists, the B cell** | **a consequence of the Law**: the `128` body cells leave, and the tiny cell stays |

The word "first" stays out, as in Part 22. The survey is a web search and not a patent search. `[DECISION]`

## 6 · What to build next

| The step | The gate |
|---|---|
| measure the real idle floor of the `U7`, the wake-up path and the power chip | CSK-6 |
| prototype a Paper layer in the cell layer of one tile | CSK-7 |
| measure the Paper update energy at `128 cm²` | CSK-7 |
| test the back panel geometry on a desk, a hand and a stand | CSK-8 |
| measure the micro-LED as a photodiode | CSK-8 |
| order the prior art search for the Heartbeat Law | CSK-1 |

## 7 · The sources

| The fact | The source | The state |
|---|---|---|
| Wi-Charge: `3 W` over `15 ft`, Class 1, line of sight | [Wi-Charge, Wikipedia](https://en.wikipedia.org/wiki/Wi-Charge) | search result |
| a `400 mW` beam gave `85 mW` over `100 ft` | [Sejong University result, via the search](https://www.tweaktown.com/news/88219/wireless-charging-power-transmitted-with-lasers-up-to-100-feet-away/index.html) | search result |
| `10 W/m²` for the public above `2 GHz` | [ICNIRP 2020 guidelines](https://www.icnirp.org/cms/upload/publications/ICNIRPrfgdl2020.pdf) | search result |
| `1 mW/cm²` equals `10 W/m²` | [FCC, Federal Register 2020](https://www.federalregister.gov/documents/2020/04/06/2020-06966/human-exposure-to-radiofrequency-electromagnetic-fields) | search result |
| wake-up receivers from sub-nW to µW | [MDPI review, 2025](https://www.mdpi.com/2079-9268/15/4/55) | search result |
| `1000 lux` of LED light is about `315 µW/cm²`, GaAs about `29 %` | [Nature Energy, indoor PV metrics](https://www.nature.com/articles/s41560-026-02101-x) | search result |
| GaAs laser power converter `68.9 %` at `858 nm` | [Fraunhofer ISE](https://www.ise.fraunhofer.de/en/press-media/press-releases/2021/record-efficiency-68-9-percent-for-gaas-thin-film-photovoltaic-cell.html) | search result |
| `3.8 Gbit/s` and `39.7 %` with a multi-segment GaAs converter | [arXiv 2510.06205](https://arxiv.org/html/2510.06205v1) | search result |
| NFC powered e-paper, `15 mW` class | [Good Display NFC driver board](https://www.good-display.com/product/390.html) | search result |
| head-mounted projection with retroreflective screens | [Hua lab, Arizona](https://wp.optics.arizona.edu/3dvis/research/polarized-head-mounted-projection-display-p-hmpd/) | search result |

**The honest limit**. The pages were read through a search summary and not opened in full. Every figure from them carries `[HYPOTHESIS]` until a person opens the paper.
