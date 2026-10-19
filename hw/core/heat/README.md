# BUDLUM LEAF · CORE AND SKIN · HEAT · THE HEAT OF THE SPLIT

**Revision L.7 candidate · 2026-10-19 · the Heat seat of `hw/core`, block HP-2**. This study tests the arithmetic of the Lead. With the silicon and the radio off the surface, the Skin heat is `0.80 W` in delta and `1.35 W` in video. The L.6.0 free-air limit is `1.73 W`. It is a study. It changes no L.6.0 or L.6.1 decision. Every number is `[HYPOTHESIS]` unless a source is named.

## 1 · The verdict, the damage first

**The Split closes gap G-46 at C0 up to `30 °C` ambient and at C1 up to `25 °C`, with two conditions. It does not close it at C2, and it does not close it at `35 °C`.** `[HYPOTHESIS]`

1. **The Lead's arithmetic holds and is too cautious.** Without the ring the old hot spot is gone. The Skin sustains `2.93 W` of display and address power at `25 °C` in still air. The L.6.0 body sustains `1.73 W`.
2. **Placement is the first damage.** A link PHY of `0.25 W` on one tile costs `4.0 K`. A seat loss of `0.34 W` costs `5.9 K`. The same watts spread over the face cost almost nothing. Video at `25 °C` fails by `0.5 K` with a `0.35 W` PHY on the seat tile.
3. **A contact loss hurts the Skin.** With `0.34 W` and the PHY on the seat tile, delta reaches `37.7 °C`. It fails by `1.5 K`.
4. **At C2 the Split gives nothing.** The Leaf keeps the ring, the radio and the decoder. The ring alone fails `36.2 °C` above `24 °C` ambient, and above `20 °C` with a `0.8 W` radio.
5. **The heat moves to the Core.** A Core for `1` to `8` Skins dissipates `1.7` to `35 W`. A validator adds `20 W`. A hand-size passive box holds `4` Skins of delta at `43 °C`. It holds `2` of video.
6. **The 35 °C wall stays.** In still air at `35 °C` the Skin delta session reaches `38.6 °C`. Only a heat path to a cold plate passes.

**The sentence the program can keep**. The Skin passes the free-air limit at C0 to `30 °C` and at C1 to `25 °C`. Every watt on the face must be spread. A Core of more than `4` Skins needs a fan or a large case.

## 2 · What is here

| The file | The content |
|---|---|
| `coreheat.py` | the library: the Skin without the ring, the Core box model, the C2 body, the worn Frame |
| `run_all.py` | self check, then all items, writes `out/` |
| `out/selfcheck.txt` | the L.6.0 value `41.3 °C` is reproduced, the ring is empty, the heat balance closes |
| `out/skin_cases.{json,txt}` | the Skin hottest point for five loads, four ambients, wind, three feeds, three PHY powers, two placements |
| `out/skin_sustained.{json,txt}` | the sustained display power and the picture level |
| `out/core_box.{json,txt}` | the Core box temperature, the Skins per box, the 5G modem and the validator |
| `out/tether.{json,txt}` | the Skin-end loss sweeps and seven named link and power options |
| `out/frame.{json,txt}` | the worn Skin: the limit before and after the Split |
| `out/c2.{json,txt}` | class C2: the L.6.0 body with the ring and a radio of `0.4` to `1.6 W` |
| `out/damage.{json,txt}` | the dock plate, the dew point, the TEC power, the throttle |
| `out/plots/01` to `06` | fields, sustained power, Core box, tether, Frame, C2 |

**How to run it**.

1. Install `numpy`, `scipy` and `matplotlib` for `python3`. Nothing else is needed.
2. Run `python3 run_all.py` in this directory. The run takes about `5 s`.
3. Read `out/selfcheck.txt`, then the item files.
4. Check the prose with `python3 tools/check_prose.py hw/core/heat/README.md` from the repository root.

The scripts import `hw/hostpower/thermal/`, `sim/thermal/` and `hw/dock/` read only. They write nothing outside this directory.

## 3 · The model and the assumptions

**The Skin**. The fixed L.6.0 body F1 to F4 of `sim/thermal`, with the ring radius set to zero. No cover sits on the face. No ring node or bar node carries heat. `[HYPOTHESIS]` The stack, the hinges and the `128` hermetic cells stay as L.6.0, so a Skin with no cells is thermally the same.

| The load | The values | The source |
|---|---|---|
| delta, `0.80 W` | display `0.60 W`, address `0.20 W` | `hw/energy` body column |
| delta, `1.25 W` | display `1.00 W`, address `0.25 W` | map (a) tiles of `sim/thermal` |
| video, `1.35 W` | display `1.10 W`, address `0.25 W` | `hw/energy` body column |
| 5G-like, `2.10 W` | display `1.80 W`, address `0.30 W` | map (c) tiles of `sim/thermal` |
| outdoor `800 nit`, `4.24 W` | display `3.84 W`, address `0.40 W` | `hw/energy` outdoor video |

**The link load**. The link PHY and the minimal decoder take `0.15`, `0.25` or `0.35 W`. Two placements are run. In "dist" the load spreads over all tiles. In "seat" it sits on the seat tile at the top edge. The seat run is the worst case.

**The feeds**. "cells" is the own-cell Skin of L.6.0 with no host: cell `I²R` and the DC lattice. "Contact feed" has the cell floating or absent and a fixed `0.10` or `0.34 W` loss on the seat pads. The two bounds come from `hw/hostpower/thermal`.

**The gate quantity**. The hottest front cap tile or back skin tile. The Skin has no ring shell and no bar.

## 4 · Items 1 and 2: the Skin alone, and gap G-46

Hottest face point in °C at `25 °C` ambient, still air, PHY `0.25 W`. "Seat" puts the PHY on the seat tile. `[HYPOTHESIS]` Full tables are in `out/skin_cases.txt`.

| The load | L.6.0 with ring | Skin, own cells, PHY spread | Skin, PHY on seat | Feed `0.10 W`, spread | Feed `0.34 W`, seat |
|---|---|---|---|---|---|
| delta `0.80 W` | `39.5` (energy loads) | `28.7` pass | `32.7` pass | `30.3` pass | `37.7` fail |
| delta `1.25 W` (map a) | `41.3` | `30.2` pass | `34.3` pass | `31.8` pass | `39.2` fail |
| video `1.35 W` | `46.2` | `30.6` pass | `34.6` pass | `32.1` pass | `39.6` fail |
| 5G-like `2.10 W` | `44.9` | `33.2` pass | `37.2` fail | `34.6` pass | `42.1` fail |
| outdoor `800 nit`, `4.24 W` | n.a. | `40.9` fail | `44.8` fail | `42.0` fail | `49.6` fail |

The L.6.0 column uses the energy loads of the delta and video sessions with a `0.4 W` radio. The 5G case uses the thermal map in light wind. `[TREE]` `out/c2.txt`

**The old hot spot is gone**. At `25 °C` the delta session on the L.6.0 body has a field of about `11 K` across the face, peaking under the ring. The Skin face is flat. The hottest and coldest front tile differ by `0.13` to `0.19 K`. The face sits at its mean temperature. `[HYPOTHESIS]` Plot `01_skin_fields.png`.

**The new hot spots**. There are three, in this order of strength.

1. **A source on the seat tile.** A PHY of `0.25 W` there adds `4.0 K`. At `0.35 W` it adds `5.9 K`.
2. **The seat pad loss.** The back skin there adds `1.6 K` at `0.10 W`, `5.9 K` at `0.34 W`.
3. **The centre of the face, at tile `(3,8)`.** It is the hottest tile of a spread load by `0.1 K`. It is not a hot spot in practice.

**The sustained power**. The load is uniform, so the sustained power does not depend on the session shape. Plot `02_skin_sustained.png`.

| The condition | `20 °C` | `25 °C` | `30 °C` | `35 °C` |
|---|---|---|---|---|
| own cells, still air, PHY `0.25 W` spread | `4.26 W` | `2.93 W` | `1.54 W` | `0.10 W` |
| same, range over PHY `0.15` to `0.35 W` and placement | `2.62` to `4.36` | `1.22` to `3.03` | `0.00` to `1.64` | `0.00` to `0.20` |
| own cells, light wind | `6.80 W` | `4.71 W` | `2.54 W` | `0.30 W` |
| contact feed `0.10 W`, still air | `3.96 W` | `2.57 W` | `1.10 W` | `0.00 W` |
| contact feed `0.34 W`, still air | `2.72 W` | `1.29 W` | `0.00 W` | `0.00 W` |

**The highest picture level the Skin holds**. By `FINAL/17` Section 17.13, `P_display = 0.60 W x (nits / 250) x (APL / 35 %)`. The numbers are for the delta shape, own cells, PHY spread.

| The condition | Display power | Luminance at `35 %` picture level | Full white field | Picture level at `800 nits` |
|---|---|---|---|---|
| `25 °C`, still | `2.20 W` | `915 nits` | `320 nits` | `40 %` |
| `25 °C`, light wind | `3.53 W` | `1 471 nits` | `515 nits` | `64 %` |
| `30 °C`, still | `1.16 W` | `482 nits` | `169 nits` | `21 %` |
| `30 °C`, light wind | `1.91 W` | `795 nits` | `278 nits` | `35 %` |
| `35 °C`, still | `0.08 W` | `32 nits` | `11 nits` | `1 %` |

The outdoor session needs `70 %` at `800 nits`, which is `3.84 W` of display. No ambient above `20 °C` holds it. The throttle law at `30 °C` in still air holds `0.85` of delta, `0.81` of video, `0.59` of 5G-like and `0.33` of the outdoor display. Light wind lifts them to `1.00`, `1.00`, `0.85` and `0.51`.

**Does the Split close G-46?** The test is `36.2 °C`. The PHY is `0.25 W`, spread over the face, with own cells.

| The class and the case | `20 °C` | `25 °C` | `30 °C` | `35 °C` |
|---|---|---|---|---|
| C0 and C1, delta `0.80 W`, PHY `0.25 W`, still air | pass `23.7` | pass `28.7` | pass `33.6` | fail `38.6` |
| C0 and C1, video `1.35 W`, still air | pass `25.7` | pass `30.6` | pass `35.5` | fail `40.5` |
| C0 and C1, video `1.35 W`, light wind | pass `23.6` | pass `28.6` | pass `33.5` | fail `38.5` |
| C0 and C1, 5G-like `2.10 W`, still air | pass `28.4` | pass `33.2` | fail `38.2` | fail `43.1` |
| C0 and C1, outdoor `800 nit` | pass `36.1` | fail `40.9` | fail | fail |
| C2, delta, radio `0.4 W`, still air | pass `34.6` | fail `39.5` | fail `44.4` | fail `49.2` |
| C2, video, radio `0.4 W`, still air | fail `41.4` | fail `46.2` | fail | fail |

**The count**. In the full grid of `360` Skin runs, `124` pass, counting the worse of the two placements. The failures are the `35 °C` rows, the outdoor rows, most 5G-like rows, and the seat-placed or `0.34 W` cases from `30 °C` up.

**The two conditions for the closure**. The PHY, the decoder and the power path must be spread, or sit on a spreader that holds the seat tile rise under `1.5 K`. The contact loss on the seat pads must stay at `0.10 W` or less. `[HYPOTHESIS]`

**The PHY budget**. The largest PHY and decoder power that holds the nominal load at `25 °C` in still air is `2.38 W` for delta. For video it is `1.83 W`. The PHY is spread. At `30 °C` it is `0.99 W` for delta and `0.44 W` for video. At `35 °C` it is zero. So a `0.9 W` radio PHY at C1 closes the video session at `25 °C` (`32.9 °C`) and fails at `30 °C` (`37.8 °C`).

## 5 · Item 3: the Core alone

A sealed aluminium box, matte, emissivity `0.90`. Natural convection and radiation use the textbook simple forms for air. `[GENERAL]` The peak case rise is `1.25` times the mean rise. `[HYPOTHESIS]` The box stands on a desk with the bottom half blocked. "Fan" is `2 m/s` over all faces. "Fan and fins" multiplies the area by `3`. "Plate" is the footprint on a `22 °C` plate with `400 W/m²K`. Plot `03_core_box.png`.

**The Core heat**. Rails divided by `0.90`, plus `6 %` loss on the Skin supply, plus `0.25 W` of link PHY per Skin. The radio and the authority chips run once. The hub chips run per Skin. `[HYPOTHESIS]` The 5G modem adds `1.20 W`. The validator of `hw/dock` takes `5.4` idle, `20.4` typical and `29.6 W` peak.

| The Core | `N = 1` | `N = 2` | `N = 4` | `N = 8` |
|---|---|---|---|---|
| delta, shared radio | `1.7 W` | `2.8 W` | `5.0 W` | `9.3 W` |
| video, shared radio | `2.5 W` | `4.2 W` | `7.5 W` | `14.3 W` |
| video, unshared, every Skin carries `1.92 W` of ring load | `2.5 W` | `5.0 W` | `9.9 W` | `19.9 W` |
| video, 5G modem and validator typical | `24.0 W` | `25.7 W` | `29.1 W` | `35.8 W` |

**The touch limits assumed**. All three are `[HYPOTHESIS]`, recalled and not read from the standard. I did not verify them against the text of IEC 62368-1.

1. `41 °C`: a worn or pocket Core. It is near the figure recalled for applied parts in IEC 60601-1.
2. `43 °C`: a Core that is held or rests on skin.
3. `48 °C`: a part held over a minute. It is near the TS1 limit recalled from IEC 62368-1 Table 38.

The limits are absolute and apply to the peak case temperature.

**The Skins a passive Core holds**, peak case at or under `43 °C`, delta session, shared radio, `25 °C` ambient. `[HYPOTHESIS]`

| The box | Passive heat limit | Delta, passive | Video, passive | Delta, fan and fins | Delta, `35 °C`, passive |
|---|---|---|---|---|---|
| S `90 x 60 x 18 mm` | `2.3 W` | `1` | `0` | `11` | `0` |
| M `140 x 90 x 30 mm` | `5.2 W` | `4` | `2` | `28` | `1` |
| L `200 x 130 x 45 mm` | `10.4 W` | `8` | `5` | `61` | `3` |
| XL `300 x 200 x 70 mm` | `23.1 W` | `20` | `13` | more than `64` | `8` |

**The reading**. A pocket box of `90 mm` holds one Skin and no more. A `140 mm` box holds `4` delta Skins and `2` video Skins at `25 °C`. At `35 °C` it holds one. A fan with fins lifts the same box to `28` Skins. A cold plate holds `22` to `28` Skins. The TEC reaches its pumping limit of `27 W` at `35 °C`, and the search stops at `32 W`.

**The options**. With a 5G modem a passive M box holds `3` delta Skins. A Core with one video Skin, the 5G modem and the validator (`24.0 W`) peaks at `43.7 °C` in a passive XL box. That fails `43 °C` and passes `48 °C`. In an M box with a fan and fins it peaks at `35.8 °C` mean and `38.5 °C` peak. `[HYPOTHESIS]` A Core with the validator is a dock, not a pocket part.

## 6 · Item 4: the tether heat at the Skin end

`hw/core/power/` and `hw/core/link/` held no files when this study ran. The options below are sweeps and named hypotheses. Tether heat is the link PHY, the decoder and the Skin-end power path loss. Plot `04_tether.png`.

**The sweeps**. At `25 °C` in still air, own cell-less Skin.

1. **A loss at the seat tile** from `0.1` to `1.0 W` costs `2.95 W` of sustained display power per watt. At `0.5 W` the sustained power falls from `2.95` to `0.41 W`. At `0.75 W` it is zero.
2. **The same watt spread over the tiles** costs `0.99 W`. Where the loss sits matters by a factor of `3`.
3. **The PHY power** from `0.10` to `1.0 W`, spread, lowers the sustained power from `3.10` to `2.20 W`. It is a one for one trade.

| The option | PHY and decoder | Path loss | Tether heat | Video, `25 °C` | Sustained, loss on seat | Sustained, loss spread |
|---|---|---|---|---|---|---|
| wired, VBUS `3.85 V`, `12` pads | `0.25 W` | `0.12 W` | `0.37 W` | `32.4 °C` | `2.48 W` | `2.84 W` |
| wired, `12 V` in, 3:1 charger | `0.25 W` | `0.18 W` | `0.43 W` | `33.5 °C` | `2.14 W` | `2.77 W` |
| wired, `48 V` EPR in, buck | `0.25 W` | `0.26 W` | `0.51 W` | `35.0 °C` | `1.71 W` | `2.69 W` |
| optical fibre, `12 V` power | `0.35 W` | `0.19 W` | `0.54 W` | `34.0 °C` | `2.01 W` | `2.67 W` |
| cable `10 Gbit/s` PHY, `12 V` power | `0.40 W` | `0.19 W` | `0.59 W` | `34.2 °C` | `1.95 W` | `2.62 W` |
| `60 GHz` link, Qi-class power | `0.90 W` | `0.19 W` | `1.09 W` | `36.0 °C` | `1.41 W` | `2.11 W` |
| `60 GHz` link, own cells | `0.90 W` | `0.00 W` | `0.90 W` | `32.9 °C` | `2.28 W` | `2.28 W` |

**The reading**. Every option passes the video session at `25 °C`. The `60 GHz` and Qi-class pair passes by `0.2 K`. Each option with a power path loses more than `0.3 W` of sustained power when that path sits on one tile. The `48 V` option loses `1.0 W`. The Qi-class chain uses `12 V` and the model of `hw/hostpower/thermal`. `[HYPOTHESIS]`

**The Core end**. The Core supply loses `6 %` of the Skin power. The PHY takes `0.25 W` per Skin. Both are in item 3.

## 7 · Item 5: the Frame

The model is the two-node face model of `hw/hostpower/thermal/eyewear.py`. Skin is `34 °C`. The exposed area is `100 cm²`. The contact is `8 cm²`. Before the Split the unsplit Frame holds `1.05 W` at `25 °C` in still air. `[HYPOTHESIS]` Plot `05_frame.png`.

**The change**. The Split takes the SoC and the radio off the face. The microdisplay load spreads over the lens and the rim. Only the temple load, which is the PHY, the decoder and the connector, sits behind the `3 K/W` hot spot. The microdisplay is assumed at `0.20` to `0.50 W`. `[HYPOTHESIS]`

| The temple load | `20 °C` | `25 °C` | `30 °C` | `35 °C` |
|---|---|---|---|---|
| `0.25 W` (PHY `0.15`, connector `0.10`): display limit | `1.53 W` | `0.99 W` | `0.44 W` | `0.00 W` |
| same: total heat limit | `1.78 W` | `1.24 W` | `0.69 W` | fails |
| `0.59 W` (PHY `0.25`, connector `0.34`): display limit | `1.02 W` | `0.48 W` | `0.00 W` | `0.00 W` |
| same: total heat limit | `1.61 W` | `1.07 W` | fails | fails |
| the unsplit Frame, total heat limit | `1.47 W` | `1.05 W` | `0.63 W` | `0.20 W` |

**The reading**. The total heat the face holds rises from `1.05` to `1.24 W` at `25 °C` with a small connector loss. It stays at `1.07 W` with a `0.34 W` loss. The gain is `0.0` to `0.2 W`. The real gain is the load. The unsplit Frame draws `0.4` to `1.2 W`. The Split Frame draws the display plus the temple load, from `0.45` to `1.1 W`.

**The verdict at `25 °C`, still air**. A display of `0.35 W` with a `0.25 W` temple load peaks at `32.9 °C`, `3.3 K` of margin. With a `0.59 W` temple load the margin is `0.8 K`. A display of `0.50 W` with a `0.59 W` temple load fails by `0.1 K`.

**The ambient limit**. A `0.8 W` unsplit Frame with a `0.34 W` connector holds up to `24.0 °C`. A Split Frame with display `0.35 W` holds to `26.2 °C` with a `0.59 W` temple load. With `0.25 W` it holds to `30.8 °C`. At `35 °C` nothing holds.

**What the Split does to the Frame**. It strengthens the face-side result by removing the radio hot spot. It also ties the Frame to a tether, so the `0.10` to `0.34 W` connector and the PHY take about half the heat budget. Frame class: C0 only. A Frame at C1 with a `0.90 W` PHY, display `0.35 W` and a `0.10 W` connector peaks at `39.1 °C` at `25 °C`. It fails by `2.9 K`. `[HYPOTHESIS]`

## 8 · Class C2: the Leaf keeps the radio

BRIEF Section 8 sets three classes. C0 is a tether up to `2 m`. C1 is a room up to `30 m`. C2 is far. At C2 the Leaf keeps the ring, the radio, the 5G modem, the decoder and the compositor. The body is L.6.0 with the ring. The ring carries hub, authority and a radio of `0.4` to `1.6 W`. Plot `06_c2.png`.

| The case, delta session `2.02 W` plus the radio step | `20 °C` | `25 °C` | `30 °C` | `35 °C` |
|---|---|---|---|---|
| radio `0.4 W`, still air | `34.6` pass | `39.5` fail | `44.4` fail | `49.2` fail |
| radio `0.8 W`, still air | `38.5` fail | `43.4` fail | `48.2` fail | fail |
| radio `1.6 W`, still air | `46.5` fail | `51.2` fail | `56.0` fail | fail |
| radio `0.4 W`, light wind | `30.7` pass | `35.7` pass | `40.6` fail | fail |
| radio `1.6 W`, light wind | `39.7` fail | `44.6` fail | fail | fail |

**The hot spot returns**. It is the ring shell, as in L.6.0. The video session fails at every ambient and radio power in still air. At `20 °C` it reaches `41.4 °C` with a `0.4 W` radio. `[HYPOTHESIS]`

**The ring alone**. With the display off, the ring holds `36.2 °C` in still air up to the ambient below. The radio is `0.4`, `0.8`, `1.2` and `1.6 W`: `24.2`, `20.2`, `16.2` and `12.0 °C`. The Leaf cannot hold a long-range radio in free air at room temperature. A display-only throttle cannot help. `[HYPOTHESIS]`

**The sustained display power at C2**, delta, radio `0.4 W`: `1.27 W` at `20 °C` in still air and `0.00 W` above. With light wind: `3.34 W` at `20 °C`, `1.06 W` at `25 °C`, `0.00 W` at `30 °C`.

**On the dock plate at `35 °C`**. The ring gets a heat path again. The hottest point is `27.9 °C` with a `0.4 W` radio and `32.2 °C` with `1.6 W` in the delta session. The video session reaches `34.2 °C`. Every C2 case passes on the plate.

**Which classes close G-46**.

| The class | Closes G-46 in free air? | The condition |
|---|---|---|
| C0, tether to `2 m` | yes, to `30 °C` | PHY and power path spread, contact loss at `0.10 W` or less |
| C1, room to `30 m` | yes, to `25 °C` with a `0.9 W` PHY | the PHY spread, own cells or a spread regulator. To `30 °C` the PHY must stay under `0.44 W` |
| C2, far | no | the ring and the radio stay on the Leaf. Needs a dock plate or wind |
| any class at `35 °C` | no | needs a heat path, such as the dock plate |

## 9 · Item 6: the damage report

**What the Split strengthens in Part 22**.

1. **The free-air claim.** Part 22 calls always-on in the hand false for the L.6.0 body. For a Skin it holds at C0 to `30 °C` and at C1 to `25 °C`. The sustained limit rises from `1.73` to `2.93 W`.
2. **The Qi charge heat.** The `25 W` charge adds `6.4 W` and reaches `37.3 °C` on the dock. A Skin has no cell. The charge heat moves to the Core.
3. **The throttle.** At `30 °C` in still air the L.6.0 body holds `30` to `35 %` of its delta power. The Skin holds `0.85` of delta and `0.81` of video.
4. **The dock plate and the dew point.** The Skin lets the plate rise. At `35 °C` the warmest plate that holds the Skin is `35.8 °C` for delta and `35.6 °C` for video. The L.6.0 body allows `30.9 °C`. The dew point at `35 °C` is `26.1 °C` at `60 %` humidity and `31.0 °C` at `80 %`. The L.6.0 plate limit `30.9 °C` clears the `80 %` dew point by `-0.1 K`. The Skin clears it by `+4.6 K`. `[GENERAL]` Magnus formula.
5. **The TEC power.** At `35 °C` and a `22 °C` set-point the TEC takes `3.25 W` for Skin video. The L.6.0 delta session takes `3.75 W`. A plate at `28 °C` takes `1.02 W`. A plate at `30 °C` takes `0.58 W`. The set-point can rise and the dew point issue closes for the Skin.

**What the Split weakens**.

1. **Placement.** A source on one tile is a hot spot. The L.6.0 ring was one such source. The Skin needs a spread power path. A seat connector loss of `0.34 W` breaks the delta session at `25 °C`.
2. **The Core is a heat product.** `1.7` to `35 W` in a box. A `90 mm` pocket box holds one Skin passive. A validator Core needs a fan or an XL case. The Part 22 heat findings did not cover the Core.
3. **The tether heats both ends.** The Core loses `0.25 W` of PHY per Skin and `6 %` of the supply. The Skin loses `0.37` to `1.09 W`, by option.
4. **C2 and `35 °C` are unchanged.** The Split cannot cool the ring at C2. No Skin passes at `35 °C` in free air.
5. **The Frame.** The gain in heat limit is at most `0.2 W`. The temple connector uses half of the budget.
6. **The 5G map.** The 5G-like `2.10 W` Skin load fails from `30 °C` in still air. The outdoor `800 nit` session fails above `20 °C`. A Skin does not run the outdoor session in free air.

## 10 · The open issues

1. **The link seat and the power seat have not published.** The tether options are sweeps. A real PHY and a real power tree replace them.
2. **The uniform load.** Real micro-LED loads follow the picture. A bright patch of `20 %` of the face is a local load. A nonuniform run is needed.
3. **The cell-less Skin stack.** The model keeps the `0.90 mm` cell layer. A Skin with no cell has a different stack and a different conductance through the face.
4. **The Core box model is lumped.** A real case has fins, vents, a pack and a board. A bench test with a dummy load replaces it. The `1.25` peak factor is a guess.
5. **The touch limits are recalled.** They need a read of IEC 62368-1 Table 38 and IEC 60601-1 Clause 11. Tag `[HYPOTHESIS]`.
6. **The Core shares the radio.** The shared model assumes one radio for all Skins. A Skin of a different session type adds hub load. The unshared model is the upper bound.
7. **The Frame display power is assumed.** `0.2` to `0.5 W` has no source in the program. The display seat owes the number.
8. **The ring alone at C2.** It fails above `24 °C` with a `0.4 W` radio. This is a L.6.0 fact and it is stated here for the C2 class. A radio duty rule or a ring redesign closes it.
9. **The dock plate at C2.** The reference run assumes a full-face plate. A Leaf in a vehicle cradle has less contact.
10. **Steady state only.** No bursts and no PCM. `[DECISION]` out of scope.

## 11 · The proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| HC-H1 | the Skin, delta `0.80 W` and video `1.35 W` plus the real PHY and decoder, free air `25 °C`, still, `60 min` | the hottest face point is at or under `36.2 °C`. The model says `28.7` and `30.6 °C` |
| HC-H2 | the Skin at `30 °C`, still, video `1.35 W` plus the real PHY | the hottest face point is at or under `36.2 °C`. The model says `35.5 °C` and a margin of `0.7 K` |
| HC-H3 | the face uniformity of the Skin on a thermal camera, video, `25 °C` | the hottest tile is at most `1.5 K` over the face mean. The model says `0.2 K` |
| HC-H4 | the link PHY and the power path loss at the Skin end, measured per tile | no tile carries more than `0.10 W` more than the mean. The seat tile source is at most `0.10 W` |
| HC-H5 | the contact loss of the `12` pads, new and worn, at the Skin power | the loss is at or under `0.10 W`. A value over `0.34 W` is a stop |
| HC-H6 | the Core box at the stated `N`, with the dummy load, `25 °C`, still, `60 min` | the peak case temperature is at or under the touch limit of the use. The model gives `43 °C` for `4` delta Skins in `140 x 90 x 30 mm` |
| HC-H7 | the Core with the validator typical load, in its case, with its fan | the peak case is at or under `48 °C` and the fan failure test ends the validator duty without a fault |
| HC-H8 | the touch limits: a lab read of IEC 62368-1 Table 38 and IEC 60601-1 Clause 11 | the limits of this study are confirmed or replaced, and the Section 5 table is rerun |
| HC-H9 | the C2 Leaf, delta session, radio at its range limit, `25 °C`, light wind | the hottest point is at or under `36.2 °C`, or the radio duty rule holds it there. The model says `35.7 °C` at `0.4 W` and a failure at `1.6 W` |
| HC-H10 | the Split Frame on a head form, display `0.35 W`, temple `0.59 W`, `25 °C` | the contact surface and the outer surface are at or under `36.2 °C` for `60 min`. The model says `35.4 °C` |
| HC-H11 | the dock plate set-point with a Skin at `35 °C` and `80 %` humidity | the plate sits at least `2 K` over the dew point and the Skin holds `36.2 °C` |
