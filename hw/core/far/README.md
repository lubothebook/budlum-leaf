# BUDLUM LEAF · THE FAR LINK · block HP-3, seat far link

**Study of 2026-10-19**. It serves the distance order of `hw/core/BRIEF.md` Section 8. It changes no L.6.0 or L.6.1 decision. Every number is `[HYPOTHESIS]` unless the tag says otherwise. The Leaf antennas, the modem `U5` and the SAR design stay as designed.

## 0 · The damage report, first

What narrows the Split on the far link. Each line has its number, and each number is in `out/summary.txt` or `out/latency.txt`.

1. **No Leaf radio carries the raw pixel stream, at any distance**. The raw stream needs `36.9 Gbit/s`. The best Leaf radio is `802.11ay` on `8.64 GHz`, one stream, with a ceiling of `13.6 Gbit/s`. The raw stream needs a cable or a contact (C0).
2. **The compressed pixel stream lives only in `60 GHz` line of sight, and only to about `50 m`**. With a `25 dBi` Core antenna, `12.3 Gbit/s` (`3:1`) reaches `29 m` and `6.1 Gbit/s` (`6:1`) reaches `52 m`. With a `12 dBi` antenna the reach is `12 m` and `22 m`. A wall or a hand ends it. Wi-Fi 7 tops out at `2.9 Gbit/s` and 5G at `0.75 Gbit/s`, so neither carries a pixel stream.
3. **The minimal Skin is a C0 idea, with a thin C1 case**. The room class (`30 m`) holds only in free line of sight on `60 GHz`. A Skin that leaves its contact or tether needs `U6`, the `16 MB` store and `U1`. That is the L.6.0 Leaf.
4. **At C2 the Split saves the Leaf nothing**. The Leaf keeps `U5`, the antennas, `U6`, `U1` and `U7`. The Core is then the validator of Part 21 at the radio end. No part leaves the Leaf.
5. **The radio at C2 is 5G on licensed spectrum**. Wi-Fi Core power is capped by the regulator, so a large antenna adds no downlink. A `25 dBi` Wi-Fi Core gives `150 Mbit/s` to `130 m` (2.4 GHz) or `370 m` (5 GHz), in sight. A Core with a large 5G antenna is an operator cell site or a licensed private network. It is not a box that a user puts in a house.
6. **The Leaf uplink ends the link before the downlink does**. On 5G the uplink limits beyond about `100 m` in the urban model. With a `25 dBi` antenna, the `150 Mbit/s` slice stream reaches `570 m` in urban shadow. In line of sight it reaches `4.4 km`. At `10 km` only rural line of sight holds, on `700 MHz` or `3.5 GHz`. The uplink ends it at `11.7 km` and `7.3 km`.
7. **The A1 result of `hw/rf` is `7.2 dB` worse than the gate**. `hw/rf/out/a1_ifa.txt` gives `-9.7 dB` (moments) and `-15.3 dB` (line model). The target is `-2.5 dB`. The bandwidth is `5 MHz`. Applied to the whole Leaf, this cuts the uplink range by `33 %`.
8. **The latency gate holds, with a backhaul budget of `7.6 ms`**. The p99 is `21.5 ms` at every distance where the link exists, with the Core at the radio. The Core holds the gate behind about `490 km` of straight fibre. A signed input batch of `3.4 kB` breaks the gate at the cell edge. It gives `72 ms` at `1 km` on `700 MHz`.

## 1 · Files and how to run

| File | Content |
|---|---|
| `pathloss.py` | FSPL, 3GPP TR 38.901 UMa, UMi and RMa, O2I, ITU-R P.1238, oxygen, and a self test |
| `farlink.py` | link budget, rates, architectures, range per Core gain, aperture, beams, what the antenna does not buy |
| `farlatency.py` | input to photon with the far terms, built on `sim/latency/model.py` by import, read only |
| `farplots.py` | the five plots |
| `out/summary.txt` | every table of the link model, sections 0 to 12 |
| `out/latency.txt` | the latency tables and the backhaul budget |
| `out/budget.json` | `2 880` link rows: radio, scenario, distance, Core gain, rules, Leaf case |
| `out/range.json`, `out/arch.json`, `out/antenna.json`, `out/latency.json` | the same results in machine form |
| `out/plots/01..05_*.png` | rate against distance, range against Core gain, architecture reach, latency, aperture |

Run: `python3 -B farlink.py`, then `python3 -B farlatency.py` (about `15 s`), then `python3 -B farplots.py`. Python 3 with `numpy` and `matplotlib` is needed. Both are present here. `scipy` is not used.

## 2 · The model

**The Leaf**. Realised gain is directivity plus efficiency. `[HYPOTHESIS]` for each.

| Radio | Antenna | Design gain | Stress gain | Tx class |
|---|---|---|---|---|
| Wi-Fi 2.4 GHz | A1, `+2.6 dBi` and `-2.5 dB` | `+0.1 dBi` | `-7.1 dBi` | `20 dBm` |
| Wi-Fi 5 and 6 GHz | A2 and A3, `+3.6 dBi` and `-3 dB` | `+0.6 dBi` | `-6.6 dBi` | `20 dBm` |
| 5G `3.5 GHz` | A5 and A6, `+1.8 dBi` and `-3 dB` | `-1.2 dBi` | `-8.4 dBi` | `23 dBm` |
| 5G `700 MHz` | A5 and A6, small antenna, `-6 dB` | `-4.0 dBi` | `-11.2 dBi` | `23 dBm` |
| `60 GHz` | A4, `1 x 4` array | `+8.8 dBi` | `+1.6 dBi` | `10 dBm` |

The stress case applies the A1 gap of `hw/rf` (`7.2 dB`) to every Leaf antenna, because no other antenna has a `hw/rf` result. The `hand` case adds `6 dB`. `[HYPOTHESIS]` The A5 and A6 slots are from `HARDWARE/19` (L.5.0). FINAL/21 does not list a 5G antenna.

**The SAR**. The `0.054 W/kg` figure has no reference power in any file I read. It is `37 x` (`15.7 dB`) under the `2.0 W/kg` ICNIRP limit. With no reference power, the SAR cap on the Leaf Tx cannot be derived. The model takes the chip class power and the regulator cap, and tests the sensitivity with a `-10 dB` Tx case. Gate RF-16 must name the reference power.

**Path loss**. The models are FSPL and 3GPP TR 38.901 UMa (`25 m` tower), RMa (`35 m` tower) and UMi. The O2I model of Section 7.4.3 adds `18.9 dB` at `3.5 GHz` (low loss). ITU-R P.1238 covers the room. The oxygen loss at `60 GHz` is `15 dB/km`. A `90 %` location margin is `1.28 sigma`. Interference and noise rise cost `3 dB`. `[PUBLICATION]` formulas typed from the documents. The self test matches the known `100.2 dB` (FSPL, `2.44 GHz`, `1 km`) and `141.7 dB` (UMa non-LOS, `3.5 GHz`, `1 km`). Beyond `5 km` the UMa formulas are an extrapolation, and the tables mark them with `*`. Free space beyond the radio horizon (about `25 km`) is not physical.

**Rate**. Shannon with a gap (`4 dB` Wi-Fi, `3 dB` 5G), a modulation cap, a MAC efficiency and a duplex share. The scheduler narrows the allocation when the link is power limited, down to `20 MHz` on Wi-Fi and `6` resource blocks on 5G. Rank 2 is allowed when the SNR pays for it. The share is `0.75` down and `0.25` up on Wi-Fi, `0.74` and `0.23` on `DDDSU`, and `1` and `1` on the FDD band.

**The regulator**. Core EIRP is the smaller of the PA and the cap.

| Band | BTK and ETSI cap | FCC cap | Status of the number |
|---|---|---|---|
| `2.4 GHz` | `20 dBm` (`100 mW`) | `36 dBm` | BTK table read `[PUBLICATION]`. FCC `15.247` read from the eCFR `[PUBLICATION]` |
| `5 GHz`, `5470-5725 MHz` | `30 dBm` (`1 W`), indoor and outdoor | `36 dBm` (`5725-5850 MHz`) | the same two sources `[PUBLICATION]` |
| `5150-5350 MHz` | `200 mW`, indoor only | not modelled | BTK table `[PUBLICATION]` |
| `6 GHz` | `14 dBm` outdoor (VLP), `23 dBm` indoor | `36 dBm` standard power, `30 dBm` low power indoor | FCC from the FCC fact sheet `[PUBLICATION]`. ETSI from a secondary source. The BTK edition read has no 6 GHz row: `[HYPOTHESIS]` |
| `60 GHz` | `40 dBm`, not fixed outdoors | `40 dBm` | BTK `[PUBLICATION]`. FCC from memory `[HYPOTHESIS]` |
| 5G `700 MHz`, `3.5 GHz` | no cap in the model, PA `43` and `49 dBm` | same | licensed `[GENERAL]`. PA power `[HYPOTHESIS]` |

For FCC point-to-multipoint the conducted power falls `1 dB` per dB of gain over `6 dBi`, so the EIRP stays at `36 dBm`. The fixed point-to-point relief does not apply to a Core that serves moving Leafs. The BTK 5G tender of `2025-10-16` gave each operator `2 x 10 MHz` at `700 MHz` and `80 MHz` blocks at `3.5 GHz`. The source is press reports and the BTK news page, not the tender text. The model uses those widths `[HYPOTHESIS]`.

## 3 · The required rates (task 2)

| Architecture | Down | Up | Source |
|---|---|---|---|
| raw pixel stream | `36.9 Gbit/s` | `2.0 Mbit/s` | `1600 x 3200 x 240 x 30` bit |
| compressed pixel stream, `3:1` and `6:1` | `12.3` and `6.1 Gbit/s` | `2.0 Mbit/s` | the Lead, arithmetic |
| slice stream, upper | `150 Mbit/s` | `2.0 Mbit/s` | see below |
| slice stream, lower | `25 Mbit/s` | `2.0 Mbit/s` | Part 5 Section 5.4, classes C2 and C3 |
| camera uplink | `40 Mbit/s` (HEVC), `15 Gbit/s` (raw `50 MP`) | none | Part 5 class C4 gives `5` to `130 Mbit/s` |

**The slice assumption**. A full-screen, visually transparent `10 bit` stream at `60 Hz` needs about `0.16 bit` per pixel. That is `50 Mbit/s` on `307 Mpx/s`. HEVC class HDR streams run `0.1` to `0.3 bit` per pixel `[GENERAL]`. Part 21 sends two speculative frames with every frame (`hw/dock/validator_sizing.py`, `SPEC_COUNT = 2`). The upper bound is `3 x 50 = 150 Mbit/s`. A delta stream of the UI is far below. The local compositor `U1` moves, picks and composes at `240 Hz`, so the stream carries content at `60 Hz` and not at `240 Hz`. `[HYPOTHESIS]`

**The uplink**. The load is touch (`480 Hz x 64 B`), IMU (`1 kHz x 16 B`) and voice (`32 kbit/s`). A signed batch adds `60` ML-DSA-65 signatures per second (`3 309 B` each). The sum is `2.0 Mbit/s`. The signature is `80 %` of it. With a `16 B` session tag the uplink falls to `0.41 Mbit/s`. `[HYPOTHESIS]`

## 4 · The link budget per distance (task 1)

Rates in Mbit/s, down and up, per Leaf. Core `18 dBi`, BTK rules, Leaf as designed, `90 %` margin. The full set is in `out/summary.txt` Section 3 and in `out/budget.json`.

| Radio, scenario | `100 m` | `300 m` | `1 km` | `3 km` | `5 km` | `10 km` |
|---|---|---|---|---|---|---|
| 5G `3.5 GHz`, UMa line of sight | `753 / 87` | `753 / 87` | `753 / 49` | `258 / 1.9` | `122 / 0.2` | `17 / 0` |
| 5G `3.5 GHz`, RMa line of sight | `753 / 87` | `753 / 87` | `753 / 67` | `492 / 16` | `255 / 1.9` | `80 / 0.1` |
| 5G `3.5 GHz`, UMa non-LOS | `753 / 66` | `465 / 5` | `44 / 0` | `1 / 0` | `0 / 0` | `0 / 0` |
| 5G `3.5 GHz`, UMa non-LOS and O2I | `383 / 3` | `41 / 0` | `0 / 0` | `0 / 0` | `0 / 0` | `0 / 0` |
| 5G `700 MHz`, RMa line of sight | `127 / 47` | `127 / 47` | `127 / 47` | `102 / 28` | `57 / 9` | `24 / 0.8` |
| 5G `700 MHz`, UMa non-LOS | `127 / 47` | `127 / 41` | `46 / 3` | `3 / 0` | `0 / 0` | `0 / 0` |
| Wi-Fi 5 GHz, UMa line of sight | `339 / 174` | `180 / 91` | `24 / 31` | `0 / 0` | `0 / 0` | `0 / 0` |
| Wi-Fi 2.4 GHz, UMa line of sight | `167 / 120` | `88 / 84` | `0 / 22` | `0 / 0` | `0 / 0` | `0 / 0` |
| Wi-Fi 5 GHz, UMa non-LOS | `24 / 32` | `0 / 0` | `0 / 0` | `0 / 0` | `0 / 0` | `0 / 0` |
| `60 GHz` 2.16 GHz, free space | `1 071 / 0` | `0 / 0` | `0 / 0` | `0 / 0` | `0 / 0` | `0 / 0` |

**Where each side limits** (`out/summary.txt` Section 4). On Wi-Fi the downlink limits at every distance. The Core EIRP is capped at `20` to `30 dBm`. The Leaf uplink gets the full Core receive gain. On 5G the uplink limits from `100 m` on in the urban model. The Leaf radiates `23 dBm`, and the Core radiates `49 dBm` plus gain. At `1 km` in urban non-LOS on `3.5 GHz` the downlink margin is `+21 dB` and the uplink margin is `-2 dB`. On `60 GHz` the Leaf uplink (`10 dBm`) limits first.

**Indoors**. ITU-R P.1238, office, `100 m`, Core `18 dBi`. 5G `3.5 GHz` gives `753 / 87`. Wi-Fi 5 GHz gives `45 / 43`. Wi-Fi 6 GHz gives `0 / 59`. One floor in the way kills Wi-Fi 5 and 6 GHz at `100 m`.

## 5 · The architectures and where they stop (task 2)

Best radio, Core `25 dBi`, BTK rules, Leaf as designed. Both directions must hold. Source: `out/summary.txt` Section 5 and Section 12.

| Architecture | Free space, `60 GHz` | UMa LOS | RMa LOS | UMa non-LOS | UMa non-LOS and O2I |
|---|---|---|---|---|---|
| raw `36.9 Gbit/s` | never | never | never | never | never |
| compressed `3:1`, `12.3 Gbit/s` | `29 m` | none | none | none | none |
| compressed `6:1`, `6.1 Gbit/s` | `52 m` | none | none | none | none |
| slice `150 Mbit/s` | horizon | `4.4 km` | `7.3 km` | `570 m` | `170 m` |
| slice `25 Mbit/s` | horizon | `5.9 km` | `11.7 km` | `1.6 km` | `550 m` |

The `60 GHz` column holds a Core array of `3 cm`. The Leaf case `stress` gives `13 m` and `24 m` for the two compressed streams. With a `12 dBi` Core array the reach is `12 m` and `22 m`. BTK forbids fixed outdoor `60 GHz`.

**Which distances need the decoder on the Leaf**. All distances beyond `52 m`, and every path with a wall, a hand or a floor in it. Even inside `52 m` the compressed stream needs a decoder on the Skin. Only the raw stream needs none, and no radio carries it. At every C2 distance the Leaf needs `U6` (slice decoder, `16 MB` store) and `U1` (the compositor). `700 MHz` carries at most `127 Mbit/s` (`2 x 10 MHz`), so it carries the lower slice stream and not the upper one.

## 6 · The latency (task 3)

`out/latency.txt`. The model is `sim/latency/model.py` plus the far terms. The terms are propagation, the Wi-Fi coverage-class slot, the first-slice serialisation, HARQ that rises when the margin falls, and the backhaul. N is `100 000` actions per cell. `[HYPOTHESIS]`

| Core position, input `200 B`, 5G `3.5 GHz` LOS unless named | `100 m` | `1 km` | `5 km` | Gate `30 ms` |
|---|---|---|---|---|
| at the radio, 5G `3.5 GHz` LOS | `21.5` | `21.5` | `21.5` | pass |
| at the radio, 5G `700 MHz` LOS | `21.5` | `21.5` | `22.5` | pass |
| at the radio, Wi-Fi 5 GHz LOS | `16.1` | none | none | pass, but no stream past `300 m` |
| metro, `20 km` of fibre | `21.8` | `21.8` | `21.8` | pass |
| regional, `100 km` | `22.8` | `22.8` | `22.8` | pass |
| national, `500 km` | `30.1` | `30.1` | `30.1` | fail by `0.1 ms` |
| far validator, `80 ms` | `106.7` | `106.7` | `106.7` | fail |

All values are the p99 in ms. The rules found:

1. **Air propagation costs microseconds**. It is `3.34 us` per km each way. A `10 km` link adds `0.07 ms` to the path. Distance does not decide the latency.
2. **The backhaul decides it**. The budget is `7.6 ms` of round trip on 5G. On Wi-Fi at `100` to `300 m` it is `9.1` to `10.5 ms`. Fibre costs `4.9 us` per km on a route `1.5 x` the straight line. The Core stays within about `490 km`.
3. **Wi-Fi at kilometres needs a coverage class**. The slot time grows by the round trip, `9 us + 6.7 us per km`. Trigger-based uplink OFDMA fails when Leafs differ by more than about `480 m` in distance. 802.11 has no timing advance, and the guard interval is `3.2 us`. `[GENERAL]`
4. **The signed input batch breaks the gate at the edge**. With a `3.4 kB` batch (ML-DSA-65) the p99 is `72.5 ms` at `1 km` on `700 MHz` urban non-LOS. It is `46.5 ms` at `5 km` on `3.5 GHz` LOS and `57.5 ms` on `700 MHz`. A session tag keeps the input at `200 B`.
5. **A link with no margin raises the BLER**. The model lifts the first BLER when the margin falls under `3 dB`. The p99 grows by `3.5 ms` at `1 km` on `700 MHz` urban non-LOS.

## 7 · The big antenna trade (task 4)

**What it buys**. About `3.0 x` in range from `6` to `25 dBi` on any band (`19 dB` at `40 log d`). Each `+6 dBi` gives `x1.4`. The uplink gains the full receive gain. On Wi-Fi the downlink gains nothing, because the regulator caps EIRP.

| Radio, urban non-LOS, Leaf as designed | `6 dBi` | `12 dBi` | `18 dBi` | `25 dBi` |
|---|---|---|---|---|
| 5G `3.5 GHz`, down `25 Mbit/s` | `590 m` | `840 m` | `1.2 km` | `1.8 km` |
| 5G `3.5 GHz`, down `150 Mbit/s` | `290 m` | `410 m` | `570 m` | `870 m` |
| 5G `3.5 GHz`, up `2 Mbit/s` | `190 m` | `270 m` | `380 m` | `570 m` |
| 5G `700 MHz`, up `2 Mbit/s` | `530 m` | `760 m` | `1.1 km` | `1.6 km` |
| Wi-Fi 5 GHz, down `25 Mbit/s` | `100 m` | `100 m` | `100 m` | `100 m` |
| Wi-Fi 5 GHz, up `2 Mbit/s` | `90 m` | `130 m` | `190 m` | `290 m` |

The same table for LOS, RMa and O2I is in `out/summary.txt` Section 6 and `out/range.json`.

**The Core antenna as an object** (`out/antenna.json`, plot `05`). A square panel with aperture efficiency `0.6`, side in metres.

| Band | `6 dBi` | `12 dBi` | `18 dBi` | `25 dBi` | Area at `25 dBi` |
|---|---|---|---|---|---|
| `700 MHz` | `0.30` | `0.60` | `1.19` | `2.66` | `7.1 m2` |
| `2.4 GHz` | `0.09` | `0.18` | `0.36` | `0.80` | `0.63 m2` |
| `3.5 GHz` | `0.06` | `0.12` | `0.24` | `0.54` | `0.29 m2` |
| `5.6 GHz` | `0.04` | `0.08` | `0.15` | `0.35` | `0.12 m2` |
| `6.2 GHz` | `0.04` | `0.07` | `0.14` | `0.31` | `0.10 m2` |
| `62 GHz` | `0.00` | `0.01` | `0.01` | `0.03` | `0.001 m2` |

The beamwidth is `96`, `48`, `24` and `11 degrees`. A beamforming array of `5 dBi` patches needs `5`, `20` and `100` elements for `12`, `18` and `25 dBi`. The `25 dBi` beam of `11 degrees` is `190 m` wide at `1 km`, so the Core must track each Leaf. `[HYPOTHESIS]` gate HC-F8.

**Leafs served by beamforming**. Three sectors of `120 degrees`, a hybrid array with up to `16` simultaneous beams, urban non-LOS, all Leafs at the distance shown. The fleet seat owns the final count. `[HYPOTHESIS]`

| Radio and Core gain | Beams | At `300 m`, `150` and `25 Mbit/s` | At `1 km`, `150` and `25 Mbit/s` |
|---|---|---|---|
| 5G `3.5 GHz`, `18 dBi` | `4` | `21` and `132` Leafs | `0` and `6` Leafs |
| 5G `3.5 GHz`, `25 dBi` | `11` | `78` and `471` Leafs | `3` and `30` Leafs |
| 5G `700 MHz`, `25 dBi` | `11` | `18` and `120` Leafs | `6` and `39` Leafs |

Beams share the Core power, so each Leaf loses `10 log n` dB. At `1 km` the per-Leaf rate on `3.5 GHz` falls from `120` to `23 Mbit/s` with `11` beams.

**What it does not buy**. Slice `25 Mbit/s` down and `2 Mbit/s` up, urban non-LOS, Core `25 dBi`, 5G `3.5 GHz`. From `out/summary.txt` Section 10.

| Leaf case | Down range | Up range | Change in up range |
|---|---|---|---|
| as designed, free hand | `1.8 km` | `570 m` | none |
| hand grip `-6 dB` | `1.3 km` | `410 m` | `-28 %` |
| SAR stress, Tx `-10 dB` | `1.8 km` | `320 m` | `-44 %` |
| the A1 gap of `hw/rf`, `-7.2 dB` | `1.2 km` | `380 m` | `-33 %` |
| gap, hand and SAR together | `820 m` | `140 m` | `-75 %` |
| indoor, O2I low loss, as designed | `530 m` | `170 m` | `-70 %` |

1. **The Leaf uplink is fixed by the Leaf**. The Core antenna adds receive gain only. The Leaf EIRP is `23 dBm` plus the Leaf gain, whatever sits at the other end.
2. **Building penetration is a fixed offset**. It costs `18.9 dB` (low loss) to `33.1 dB` (high loss) at `3.5 GHz`. No antenna on the Core removes it.
3. **A hand or a head costs the Leaf gain**. The Leaf antenna is small and sits at the edge of the body. `[GENERAL]` The `6 dB` is a hypothesis. Gate RF-1 measures it.
4. **The regulator caps Wi-Fi**. The downlink range of Wi-Fi is the same at `6` and `25 dBi`.

## 8 · The distance law (task 5)

**The law**. `[HYPOTHESIS]` Up to `3 m` (C0), a cable or contact carries the raw `36.9 Gbit/s`. No Leaf radio does. To `30 m` (C1), only `60 GHz` in free line of sight carries a compressed pixel stream. With a `25 dBi` Core array, `12.3 Gbit/s` reaches `29 m` and `6.1 Gbit/s` reaches `52 m`. A worse Leaf antenna or a `12 dBi` Core halves that. Past `52 m`, and in any room with a wall, a floor or a hand in the path, the pixel stream is dead. The slice stream of `25` to `150 Mbit/s` is then the only architecture, with the decoder `U6` and the compositor `U1` on the Leaf. From `100 m` to `5 km` the slice stream holds on 5G only. With a `25 dBi` Core antenna it reaches `570 m` to `1.6 km` in urban shadow and `170` to `550 m` indoors. In line of sight it reaches `4.4` to `5.9 km`. At `10 km` it holds only in rural line of sight, on `700 MHz` or `3.5 GHz`. The uplink ends it at `11.7` and `7.3 km`. Wi-Fi carries the lower slice stream only to `550 m` (2.4 GHz) and `960 m` (5 GHz) in line of sight. The EIRP cap sets this. The `30 ms` p99 holds at every distance where the link exists. The Core sits at the radio or behind up to `7.6 ms` of backhaul round trip.

**The consequence for the Split of `hw/core/BRIEF.md`**. The Split lives at C0 and, in line of sight on `60 GHz` only, at the near edge of C1. The minimal Skin of the brief stays a C0 and C1 idea and shrinks to a tether and a short `60 GHz` hop. At C2 the Skin is the L.6.0 Leaf, with `U5`, `U6`, `U1`, `U7` and all its antennas. The Core at C2 is a validator that sits at the radio end, as Part 21 already specifies. A kilometre-scale Core is also an operator site or a licensed network. The two-hosts law of the brief holds: the energy stays with the Leaf, and the compute moves.

## 9 · Proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| HC-F1 | A1 and the 5G antennas measured on the Leaf body, free and in a hand phantom | A1 efficiency at or above `-3 dB` and a `-6 dB` bandwidth of `83.5 MHz`. The far tables rerun with the measured gains. Today `-9.7 dB` and `5 MHz` fail |
| HC-F2 | 5G down and up at the declared C2 radius, at the `90 %` edge, hand phantom | down at or above `150 Mbit/s` (`25 Mbit/s` for the lower class) and up at or above `2.0 Mbit/s`. The model gives `570 m` and `1.6 km` urban, Core `25 dBi` |
| HC-F3 | the Skin at a distance above C1 | the Skin refuses a pixel stream and shows the safe screen. Ranging or round trip names the class. A Skin without `U6` never shows C2 content |
| HC-F4 | `60 GHz` compressed stream at `30 m` line of sight, Core array `25 dBi` | at or above `6.1 Gbit/s` for `10 min` with no dropped slice. The model gives `52 m` |
| HC-F5 | input to photon p99 at `300 m`, `1 km` and `3 km` on 5G, Core at the radio | p99 at or below `30 ms` at the declared radius. The model gives `21.5 ms`. DST-11 shares the method |
| HC-F6 | backhaul round trip between the radio and the Core | at or below `7.6 ms` (5G) at p99 of the measured link. The model gives about `490 km` of fibre |
| HC-F7 | the size of the signed input on the uplink | the first input packet is at or under `200 B`, or the uplink at the radius is at or above `2.0 Mbit/s`. A `3.4 kB` batch fails at `1 km` |
| HC-F8 | beam tracking of a `25 dBi` Core antenna on a walking Leaf at `1 km` | pointing error at or under `2 degrees` and a pointing loss at or under `1 dB`, with updates every `20 ms` |
| HC-F9 | the path loss in the field at `1`, `3` and `5 km` | the median within `6 dB` of the 38.901 model of the matching scenario, per band |
| HC-F10 | the regulatory file of each C2 deployment | a written EIRP row per band for BTK, ETSI and FCC, an operator or private licence for 5G, and the BTK answer on `6 GHz` |
| HC-F11 | the SAR reference power | RF-16 names the Tx power of the `0.054 W/kg` figure. The SAR at `23 dBm` (5G) and `20 dBm` (Wi-Fi) is at or under `1.0 W/kg` in hand and head |
| HC-F12 | Wi-Fi at distance | coverage class set, and trigger-based uplink OFDMA off beyond a `480 m` spread of Leaf distances |

## 10 · Open issues

1. **The 5G antenna of the Leaf is not designed in L.6.0**. The A5 and A6 slots are from L.5.0, in the quadrant `AgNW/ITO` over the pixel area. FINAL/21 lists A1 to A4 only. The gain, `+1.8 dBi` at `3.5 GHz` and `-4 dBi` at `700 MHz`, is a hypothesis. It sets all 5G ranges.
2. **The A2, A3, A4 and 5G antennas have no `hw/rf` result**. The stress case borrows the A1 gap. `hw/rf` also has two A1 numbers (`-9.7 dB` method of moments, `-15.3 dB` line model).
3. **The sources that did not open fully**. BTK has no `6 GHz` row in the edition read. The text I extracted shows no edition date. The ETSI EN 303 687 PDF was unreadable here, so `23` and `14 dBm` come from a secondary source. The FCC `60 GHz` row is from memory. The BTK 5G tender widths come from press reports.
4. **The model has no weather, no foliage, no vehicles and no interference between cells**. The `3 dB` noise rise and the `22 dB` multi-beam cap are hypotheses. Rain at `60 GHz` is in `pathloss.py` and is off.
5. **The latency model keeps its own limits**. `sim/latency/README.md` Section 5 lists them. The far terms here add the Wi-Fi slot growth, the BLER rule and the serialisation, all hypotheses. No handover is in the far runs.
6. **The Leaf count per Core is a rough count**. The fleet seat owns it. The beam model has no inter-beam interference except a cap.
7. **The `60 GHz` Leaf uplink is weak** (`10 dBm` and `+8.8 dBi`). The A4 efficiency is not simulated.

## 11 · Sources, with their status

| Source | Used for | Status |
|---|---|---|
| 3GPP TR 38.901 V16, Tables 7.4.1-1 and 7.4.3 | UMa, UMi, RMa, O2I | formulas typed from memory of the document, self tested on two known values |
| ITU-R P.525, P.1238, P.676 | FSPL, indoor, oxygen | formulas typed, `[PUBLICATION]` |
| BTK, "Frekans Tahsisinden Muaf Telsiz Cihaz ve Sistemlerine Iliskin Teknik Olculer", `btk.gov.tr` | Turkey EIRP caps | opened and read `2026-10-19` |
| 47 CFR 15.247, eCFR | FCC `2.4` and `5.8 GHz` | opened and read `2026-10-19` |
| FCC fact sheet DOC-375609A1 and 47 CFR 15.407 | FCC `6 GHz` classes | read through a search summary |
| ETSI EN 303 687 V1.1.1 | ETSI `6 GHz` | not readable here, secondary source |
| `hw/rf/out/a1_ifa.txt` | A1 efficiency and bandwidth | read |
| `sim/latency/model.py`, `README.md` | latency chain | imported, read only |
| `hw/dock/validator_sizing.py` | speculative frames per frame | read |
