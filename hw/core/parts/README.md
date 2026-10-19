# BUDLUM LEAF · CORE · PARTS · README

**Revision L.7 candidate study · block `HP-3` · seat parts · 2026-10-19**. This seat checks the Split against the designs, part by part. It changes no L.6.0 or L.6.1 decision. Every number is `[HYPOTHESIS]` until a gate runs. A change to a design appears only as a candidate for Ayaz.

**The rule of Ayaz, applied here**. A part stays in the B module only if physics forces it at the distance class. The body keeps the emitters and the tile drivers. Everything else is Core. `[DECISION]`

---

## 1 · The damage report: what narrows the Split

**The Split is real at C0 and empty at C1 and C2**. Under the rule, nothing in the Budlum Leaf leaves at a room or at a kilometre. At contact about `40 %` of the mass leaves, and almost all of it is energy. `[HYPOTHESIS]`

| Class | Mass that leaves | Cost that leaves at 1 M a year | Ring volume freed | Energy that leaves |
|---|---|---|---|---|
| C0, contact or tether, up to 2 m | `20.85 g`, `40.5 %` of the Leaf | `158 USD`, `10.0 %` (range `111` to `231`) | `377 mm³`, `1.6` B cells | `5.9` to `7.4 Wh` |
| C0R, C0 with the radio SiPs kept | `19.84 g`, `38.5 %` | `104 USD`, `6.6 %` | `283 mm³` | `5.9` to `7.4 Wh` |
| C1, a room, up to about 30 m | `0 g` | `0 USD` | `0` | `0` |
| C2, far, up to kilometres | `0 g` | `0 USD` | `0` | `0` |

The Leaf is `51.5 g` on the derived L.6.0 basis (range `46.8` to `56.8 g`). Section 6 explains the basis. The Skin at C0 is `30.7 g`.

**What narrows the Split, in order of weight**.

1. **The emitters are the cost**. The micro-LED tiles are `76.5 %` of the unit cost at 1 M a year. It is `68.9 %` at 5 M and `81.5 %` at 100 k. No class moves them. At most `23.5 %` of the cost can leave.
2. **C2 is the L.6.0 Leaf**. A kilometre of air does not carry `6.1` to `12.3 Gbit/s`. Your ruling keeps the link PHY, decoder, frame store and compositor in the module at C1 and C2. The Core is a validator, as Part 21 designed.
3. **C1 moves nothing**. Wi-Fi 7 `2 x 2` at `320 MHz` gives `5.76 Gbit/s` of PHY. A `6.1 Gbit/s` stream does not fit. Power does not travel `30 m`, so the energy stays. The three radios stay as the link PHY.
4. **At C0 the mass that leaves is energy**. The cells, TCMs, mux, B cell and the Qi path are `19.57 g` of the `20.85 g`. The silicon, cans and TCXO are `1.28 g`.
5. **The Skin is not empty**. Three small parts join it at C0: an identity chip, a safe-screen ROM die and a ring serdes. They add `0.06 g` and `5 USD`. Touch front ends, sensors, NTC cut-off, tile hubs and seat controllers stay by physics.
6. **The radio SiPs sit on the line**. `U2A`, `U2B` and `U5` hold the front end that must stay and the baseband that can move, in one part. C0 and C0R are the two bounds. Moving them whole leaves the bar antennas dormant, and the Skin cannot roam (X13).
7. **A Skin alone is dark**. At C0 the rear glance, the clock, the wallet standby and the camera framing need the Core. Off its tether the Skin shows the ROM safe screen only.
8. **The Host Life Law collides with the rule**. Part 22 asks for a bridge store at a host swap. The rule sends all `128` cells to the Core. Keeping `20` cells costs `2.4 g` and `12 USD` (line item L2).
9. **The module stays `4.00 mm` and the bar `1.00 mm`**. The camera column stands `3.90 mm`, so freed volume is room and not thickness. The bar holds only parts that must stay.
10. **Moving is not saving**. A moved part reappears in the Core at its own cost. The saving needs one Core to serve `N` Skins (`hw/core/study/`).
11. **The catalogues disagree**. The `68 g` body counts `34.4 g` of withdrawn LLZO cells. The `88 g` total counts a withdrawn `20 g` module. The L.6.0 body has no mass list (candidate K-5, gate `HC-A8`).

**What the Split gains**. The L.6.0 ring asks for `114 %` of the free board area in the flat scenario. The placement study fails `3` parts in every scenario. At C0 the staying parts fill `35 %`, and the packer places all `25` of them. At C0R they fill `71 %`, and the packer places all `29`. `[HYPOTHESIS]` The B cell is the part that does not fit today.

---

## 2 · The rule applied, and the parts on the line

The table gives each part a verdict at each class: Body, Module or Core. A star marks a part on the line. Section 5 counts the verdicts and the codes. `out/line.md` holds the full text.

**The parts on the line**. Each row is a place where the rule meets a law, a gate, a physical fact or an unsplittable part.

| No. | The parts | What the rule says | What the table holds, and why |
|---|---|---|---|
| L1 | cells, TCMs, mux, B cell, Qi coil, rectifier, magnets | the ruling lists no energy part, so Core | Core at C0. Module and body at C1, C2: physics, watts do not cross `30 m` |
| L2 | `128` cells, the Buffer | all Core at C0 | all Core. A `20`-cell Buffer is the sensitivity: Part 22 law, not physics |
| L3 | `U2A`, `U2B`, `U5`, cans, TCXO, tuners | front end stays, baseband is Core | one SiP holds both. C0 moves it whole, C0R keeps it |
| L4 | safe-screen ROM in `U1` | `U1` is Core at C0 | a ROM die stays on the Skin: law, no visible state means a dark Skin |
| L5 | `U7` and the identity | a hardened identity element stays | `U7` stays at C1, C2. At C0 a small chip holds identity and part records |
| L6 | touch front ends, hinge and seam sensors, tile hubs | the body keeps emitters and tile drivers | they stay: an electrode or sensor is read at the tile |
| L7 | `36.2 °C` NTC cut-off | not an emitter, so Core | stays: it acts with the link lost (`ENR-16`) |
| L8 | IMU `U8` | not in the list, so Core | stays: it senses the Leaf, not the Core |
| L9 | `U3`, `U4`, boot NOR, rail parts | not in the list, so Core | stay: DAC and amp at the transducer, local rails, dead-pad answer |
| L10 | spreader, phase change buffer, shields | not in the list, so Core | stay: the camera and emitters make heat. The buffer can shrink (K-1) |
| L11 | seat fields, seam leaves, `12` bar leaves, serdes | not an emitter, so Core | stay: the only wired seat, and the tether interface at C0 |
| L12 | camera encoder block in `U6` | processing, so Core | stays at C1, C2: the uplink is weak. Moves at C0 on a switched pair |

---

## 3 · What is here

| File | Content |
|---|---|
| `parts_data.json` | the data file: `84` rows with a citation each, `12` line items, `19` collisions, `13` gates, `7` candidates, the cost groups |
| `parts.py` | validates the data, builds every table, reads `program/budget.py` read only |
| `ringfit.py` | the ring area check and the optional packer on the reduced part list (gate `HC-A2`) |
| `parts_table.csv` | the allocation table: mass, basis, citation, place, code and verdict per class, line items, reason, cost group, service, gates |
| `out/parts_table.md` | the same table in seven groups |
| `out/line.md` | the parts on the line and why |
| `out/summary.txt`, `out/summary.json` | mass, energy and volume by class |
| `out/cost.txt`, `out/cost.md`, `out/cost.json` | the cost share and what leaves, at `100 k`, `1 M` and `5 M` a year |
| `out/service.md` | the service story: swap units by class and the record law |
| `out/collisions.md` | the `19` collisions with the resolution in each class |
| `out/gates.md` | the gates `HC-A1` to `HC-A13` and the candidates `K-1` to `K-7` |
| `out/lanes.txt` | the lane budget of the twelve leaves and the Wi-Fi 7 check |
| `out/ringfit.txt`, `out/ringfit.json` | the ring fit by area and by packing |

**How to run**.

1. Run `python3 parts.py`. It exits `1` on a validation fault and `0` otherwise.
2. Run `python3 ringfit.py` for the area check. Add `--pack` for the packer, about `3` minutes.
3. Check the prose with `python3 tools/check_prose.py README.md out/*.md` from the repository root.

The scripts need numpy, scipy and the standard library. The packer needs `shapely`, which the machine of this seat lacked. Install it in your own environment. Without `shapely` the area check still runs. `placement.py` is then imported through stub modules for its part list only.

---

## 4 · The classes and the codes

| Class | Meaning |
|---|---|
| C0 | contact or tether up to `2 m`. The maximum Split under the rule. The radio SiPs, wallet, B cell and all `128` cells move |
| C0R | C0 with `U2A`, `U2B`, `U5`, their cans and the TCXO kept. This is the lower bound of line item L3 |
| C1 | a room up to about `30 m`, with the compressed slice stream of Part 21 |
| C2 | far, up to kilometres. The Skin is the L.6.0 Leaf |

| Code | Meaning |
|---|---|
| P | must stay: physics, law or an order of Ayaz |
| S | stays by design: it moves only with a Leaf redesign, or moving gains nothing |
| M | can move to the Core. The table gives the fraction that moves |
| A | added by the Split at that class |
| W | in an older catalogue and not in L.6.0 |
| D | a dock or port part, not a Leaf part |

---

## 5 · The allocation table

The full table is `parts_table.csv` and `out/parts_table.md`. It has `84` rows. The body has `23`, and the module has `32` parts from `HARDWARE/13`. `6` ring parts come from the placement study and `3` are added by the Split. The port part has `6`, the dock `7` and the withdrawn L.5.0 groups `7`. The module sum is `10.80 g`, as `HARDWARE/13` states.

**Parts by verdict and class**, derived basis, mass in grams. Rows are Body, Module and Core. `32` of the `61` counted rows are on the line.

| Class | Body | Module | Core | Rows Body / Module / Core |
|---|---|---|---|---|
| C0 | `21.7` | `9.0` | `20.85` | `18 / 28 / 15` |
| C0R | `21.7` | `10.0` | `19.84` | `18 / 33 / 10` |
| C1 | `40.6` | `10.9` | `0` | `23 / 38 / 0` |
| C2 | `40.6` | `10.9` | `0` | `23 / 38 / 0` |

**Parts by code and class**, derived basis, mass in grams. M is the moving mass.

| Class | P | S | M moves | Rows P / S / M |
|---|---|---|---|---|
| C0 | `25.5` | `5.1` | `20.85` | `36 / 10 / 15` |
| C0R | `25.5` | `6.1` | `19.84` | `36 / 15 / 10` |
| C1 | `26.9` | `24.5` | `0` | `41 / 20 / 0` |
| C2 | `26.9` | `24.5` | `0` | `41 / 20 / 0` |

**The parts that can move at C0**. Every other counted part is P or S in every class.

| Part | Mass | C0 | C1 | C2 | The gate that holds it |
|---|---|---|---|---|---|
| `128` micro cells (BD08) | `14.72 g` | Core | Body | Body | ENR-22, ENR-23 |
| TCM per cell (BD09) and the mux (M27) | `0.33 g` | Core | stay | stay | ENR-23 |
| Qi coil, `U_Q`, magnets (BD06, BD07, BD23) | `3.92 g` | Core | Body | Body | ENR-24 |
| B cell, `0.14 Wh` (M29) | `0.60 g` | Core | Module | Module | ENR-22 |
| `U1` TCON and compositor (M16) | `0.10 g` | Core | Module | Module | SW-21, DSP-17 |
| `U6` decoder, encoder, `16 MB` store (M20) | `0.15 g` | Core | Module | Module | SW-21, CAM-3 |
| `U7` secure element (M21) | `0.02 g` | Core | Module | Module | SW-22 |
| `U2A`, `U2B`, `U5` (M17 to M19) | `0.70 g` | Core | Module | Module | RF-17, RF-19, RF-22 |
| shield cans and TCXO (M32, X03) | `0.31 g` | Core | Module | Module | RF-17 |

**The parts that must stay, by reason**.

| Reason | The parts |
|---|---|
| light and the surface | PC caps, micro-LED layer and uICs, back skin, hinges, seam, adhesive layers |
| the tile drivers | tile hubs, seat controllers, the ring serdes at C0 |
| the sensors | touch front ends, hinge and seam sensors, NTC cut-off, IMU |
| the seat and the interface | hub and magnets, four seat fields, `64` seam leaves, `12` bar leaves, dead-pad parts |
| antennas as designed | bar shell, A1, A2, A3, A4, A5 to A8, corner flex, tuners |
| the camera and the user | lens and window, sensor column, rear panel and window, flash, speaker, mics, jack |
| the heat | graphite and Mu-metal shield, spreader and phase change buffer, Cu-graphite shield |
| the local services | `U3`, `U4`, boot NOR, rail inductors, ring board, the safe-screen die, the identity chip |

**The packer result**. The packer is greedy, and its result moves with the library versions. The baseline ran in the same session.

| Case | S2 flat board | S4 stacked cell and rim face |
|---|---|---|
| baseline (L.6.0) | `5` parts fail | `3` parts fail |
| C0 | `0` fail, `25` placed | `0` fail, `25` placed |
| C0R | `0` fail, `29` placed | `0` fail, `29` placed |

---

## 6 · The mass and volume summary

**The basis**. The L.6.0 module has an exact list: `HARDWARE/13`, `10.80 g`. The L.6.0 body has none. This seat derives it from the layers of Part 21 Section 21.2.7 with stated densities, and from the cell file. The result is `40.6 g` (range `35.9` to `45.9`). Rows marked stated use the catalogue number. `[HYPOTHESIS]`

| The Leaf | Mass |
|---|---|
| body, derived, L.6.0 | `40.6 g` |
| module, `HARDWARE/13` | `10.80 g` |
| Leaf, derived | `51.5 g` (`46.8` to `56.8`) |
| Leaf, the stated `68.0 g` body plus the module | `78.8 g` |
| Leaf, the stated total | `88.0 g` (counts a withdrawn module) |

**The mass that leaves and the Skin that stays**, derived basis.

| Class | Leaves | Added to the Skin | The Skin or Leaf | On the stated basis |
|---|---|---|---|---|
| C0 | `20.85 g` | `0.06 g` | `30.7 g` (`30.2` to `31.9`) | `36.3 g` leaves, `46.1 %` |
| C0 with the Buffer | `18.47 g` | `0.06 g` | `33.1 g` | not computed |
| C0R | `19.84 g` | `0.06 g` | `31.7 g` | `35.3 g`, `44.8 %` |
| C1 | `0` | `0` | `51.5 g` | `0` |
| C2 | `0` | `0` | `51.5 g` | `0` |

The module alone falls from `10.88 g` to `9.03 g` at C0 and `10.04 g` at C0R. The stated basis counts the withdrawn `34.4 g` of cells, so its percentages are not a result of L.6.0.

**The energy**. The body holds `5.9 Wh` at `600 Wh/L` and `7.4 Wh` at `750 Wh/L`. All of it leaves at C0. A `20`-cell Buffer keeps `0.92` to `1.15 Wh`. A body cell is `77 mm³`. The cell layer is `0.90 mm` of the `2.00 mm` stack.

**The volume of the B ring**. The ring envelope is `3 217 mm³`. The layer above the board is `1 572 mm³`.

| Class | Ring volume freed | Share of the layer | In B cells | Body cell volume freed |
|---|---|---|---|---|
| C0 | `377 mm³` | `24.0 %` | `1.6` | `9 857 mm³` |
| C0R | `283 mm³` | `18.0 %` | `1.2` | `9 857 mm³` |
| C1, C2 | `0` | `0` | `0` | `0` |

The B cell is `240 mm³` of the `377 mm³` at C0. Without it the silicon and the mux free `137 mm³`.

**What it does to the three numbers of Ayaz**.

| The number | What the Split does |
|---|---|
| the `4.00 mm` module | nothing in any class. The camera column stands `3.90 mm`, and gate `MON-23` holds `4.00 ± 0.05 mm`. Freed volume is room |
| the `1.00 mm` bar | nothing. The bar holds A1, A2, A4, the corner flex and the `12` leaves. All stay. At C0 the leaves become the tether interface |
| the `0.14 Wh` B cell | it leaves at C0 and C0R, with `U7`. It stays at C1 and C2 as the island rail of the wallet |
| the `2.00 mm` body | at C0 the cell layer can go from all `128` tiles, so they fall to `1.10 mm`. This is candidate K-6 |

**The Part 21 decisions the Split touches**. Each touch is a candidate for Ayaz, never a ruling.

| Decision of Part 21 | The touch |
|---|---|
| 3, more battery in the B module and the dock | at C0 the cells and the B cell leave the Leaf. Part 22 D-9 asks for a Buffer of `20` cells (line item L2) |
| 7, the B contents all stay | rear display, speaker, mics, flash and jack stay. The small battery and the silicon leave at C0 |
| 8, the Leaf is a wallet | at C0 the wallet moves to the Core and the Skin keeps an identity chip |
| 9, the dock validator is optional | the dock is the natural C0 Core (candidate K-4) |
| 4, Qi2.2 stays | at C0 the Skin omits the Qi path, since the tether powers it. It stays at C1 and C2 |
| 12, the panels stay removable | the quadrant keeps its swap. At C0 it holds no cell, and Article 11 applies to the Core cells |
| Section 21.5.1, Zero CPU | the Skin and the relocated silicon stay fixed-function. The validator role is a node |
| Section 21.5.8, SW-22 | at C0 the Skin trusts the paired Core key instead of an active validator key |

**The decisions the Split leaves intact**. The `1.00 mm` bar and the `4.00 mm` module (1). The ring on the face (2). The separate USB-C port part (5). The `50 MP` column (6). The `508 ppi` density (11). The `30 ms` target (10), which the Split does not test at C0. The `128` tiles, the hinges, the seat and the antennas. The decision that validators run the Leaf holds at C1 and C2, and at C0 the Core takes the role.

---

## 7 · The cost share

Source: `program/budget.py`, base case, read only. The unit cost is `3 949 USD` at `100 k`, `1 575 USD` at `1 M` and `803 USD` at `5 M` a year. `[HYPOTHESIS]` of the Program Office.

**The share of each group at 1 M a year, and what leaves**. USD per Leaf. Assembly and packaging are not allocated to parts and count as staying.

| Group | USD | Share | C0 leaves | C0R | C1, C2 |
|---|---|---|---|---|---|
| micro-LED tiles x `128` | `1 204.7` | `76.5 %` | `0` | `0` | `0` |
| micro cells x `128` | `66.0` | `4.2 %` | `66.0` | `66.0` | `0` |
| cellular royalties | `60.6` | `3.8 %` | `60.6` if it follows the modem | `0` | `0` |
| `U5` 5G modem SiP | `42.0` | `2.7 %` | `42.0` | `0` | `0` |
| tile mechanics | `32.0` | `2.0 %` | `0` | `0` | `0` |
| `U1` and `U6` ASICs | `20.0` | `1.3 %` | `20.0` | `20.0` | `0` |
| `50 MP` camera column | `18.0` | `1.1 %` | `0` | `0` | `0` |
| B module mechanics | `17.0` | `1.1 %` | `0` | `0` | `0` |
| `U2A` and `U2B` | `12.0` | `0.8 %` | `12.0` | `0` | `0` |
| TCM x `128` | `9.6` | `0.6 %` | `9.6` | `9.6` | `0` |
| ring PCBA | `8.5` | `0.5 %` | `0` | `0` | `0` |
| `U7`, `U8`, `U3`, `U4`, NOR | `7.5` | `0.5 %` | `2.7` | `2.7` | `0` |
| touch grid | `6.0` | `0.4 %` | `0` | `0` | `0` |
| Qi2.2 coils and rectifier | `5.0` | `0.3 %` | `4.6` | `4.6` | `0` |
| rear AMOLED | `5.0` | `0.3 %` | `0` | `0` | `0` |
| B cell | `1.3` | `0.1 %` | `1.3` | `1.3` | `0` |

**Missing costs**. Five groups are not in `budget.py`. Each is a hypothesis with a range, in USD at 1 M a year.

| Group not in budget.py | Range | Leaves at C0 |
|---|---|---|
| tile hub die x `128` | `5` to `19`, base `10` | `0` |
| NTCs, hinge sensors, seam strips, seat controllers | `3` to `12`, base `6` | `0` |
| ring small parts: flash, tuners, mux, magnets, spreader, cans, TCXO | `3` to `10`, base `6` | `1.6` (range `0.8` to `2.7`) |
| the parts the Split adds to the Skin | `3.3` to `8.5`, base `5.35` | added, not removed |
| the port part, sold apart | `6` to `16`, base `10` | not in the Leaf unit cost |

**What leaves, by volume**. Budget lines only, in USD (low, base, high) and as a share of the base unit cost.

| Volume a year | C0 | C0R | C1, C2 |
|---|---|---|---|
| `100 k` | `206` / `296` / `432`, `7.5 %` | `144` / `218` / `328`, `5.5 %` | `0` |
| `1 M` | `111` / `158` / `231`, `10.0 %` | `68` / `104` / `160`, `6.6 %` | `0` |
| `5 M` | `79` / `111` / `163`, `13.8 %` | `45` / `67` / `106`, `8.4 %` | `0` |

**The royalty**. The cellular royalty is `3.8 %` of the unit cost. If it follows the modem it is `152`, `61` or `31 USD` at the three volumes. That adds `38 %` to the saving at 1 M and is a legal question. The table above leaves it out.

**The Buffer**. Keeping `20` cells lowers the cost that leaves by `25`, `12` and `7.5 USD` at the three volumes.

**The reading**. The display is `68.9` to `81.5 %` of the cost and stays. Cells and the 5G modem are the next two items, and both leave only at C0. The Skin gains `5 USD` of new parts at C0. The cost that leaves the Leaf is a cost that the Core pays unless one Core serves many Skins.

---

## 8 · The service story

Detail in `out/service.md`. Law L9: a part is renewable and carries a record. Article 11 of 2023/1542 and `FINAL/17` Section 17.6: the user removes the battery. `FINAL/22` Section 22.12: the Buffer cells keep Article 11 only inside removable quadrants.

| Swap unit | Today | At C0 |
|---|---|---|
| quadrant `Q1..Q4`, under `3 s` | `39.8 g`: tiles, `32` cells, TCMs, coil sector | `20.8 g`: tiles only, with no cell |
| B module, under `10 s` | `10.9 g`: camera, silicon, radios, wallet, B cell | `9.0 g`: the ring stub with camera, panel, audio, antennas |
| the Core | none | `20.85 g` of today's Leaf mass, in its own swap units |
| fixed in the Leaf | `0.8 g` | `0.8 g` |

1. **Swappable in the Core at C0**. `U1`, `U6`, `U7`, `U2A`, `U2B`, `U5` with its eSIM and the B cell. Also the `128` cells with TCMs, and the Qi path.
2. **What that buys**. A radio, decoder or wallet upgrade needs no touch of the Skin. The Core part holds its own record, and the Skin pairs again by the chain record.
3. **What stays in the Leaf in every class**. Hinges, caps, emitters, seat, bar antennas, camera, rear panel, audio, jack, IMU and the touch grid. A fault there is a quadrant, a module or a Leaf swap.
4. **Article 11 at C0**. The Core cells need tool-free removal. The Skin quadrant holds no cell, so it is display only. A lawyer decides (X15 and X16).
5. **At C1 and C2**. The service story is the L.6.0 story. Nothing becomes swappable in a Core.

---

## 9 · The collisions

Full text in `out/collisions.md`. The gate or section is named in each row. `X1` to `X19` are the ids of the data file.

| No. | The collision | Gate or section | C0 | C1 | C2 |
|---|---|---|---|---|---|
| X1 | `50 MP` column and camera processing in the Core | CAM-21, CAM-3, MASTER/09 3.1 and 3.2 | sensor stays. Sentinel moves only on a switched pair | sentinel stays | sentinel stays |
| X2 | the `4.00 mm` module is set by the column | F21 21.3.5, MON-23 | module stays `4.00 mm` | same | same |
| X3 | camera indicator and signed declaration | MASTER/09 section 5, RG-5, CAM-5 | indicator on the sensor rail. Core signs | `U7` stays | same |
| X4 | the `12` gold leaves, the one wired seat | MON-23, MON-21, MON-18 | Core plug on the leaves. Test a `30 N` pull | no change | no change |
| X5 | the dead-pad law | ENR-19, MON-16, RL-7 | Skin chip verifies the Core in `3 ms` | not used | not used |
| X6 | the Zero CPU definition | F21 21.5.1 | claim it for the Skin. Name the validator as a node | same | no change |
| X7 | local compositor, warp, predicted action | F21 21.5.6, SW-21, SW-23 | Core runs it. Cut the Core uplink, not the tether | stays on the Leaf | stays on the Leaf |
| X8 | stream check and the wallet | F21 21.5.8, SW-22 | check moves to the Core. Skin trusts the pair key | no change | no change |
| X9 | safe-screen ROM lives in `U1` | FINAL/08 8.2, state machine I2 | keep a ROM die on the Skin | no change | no change |
| X10 | seam loop and `3 ms` recalibration | F21 21.2.4, MEC-40, DSP-17 | read over a pair, `0.13 ms`, not the back channel, `3.15 ms` | no change | no change |
| X11 | frame store, decoder, compositor | F21 21.5.1, BRIEF 8 item 2 | not needed | stay, as the ruling says | stay |
| X12 | radios and antennas are one design | RF-9, RF-17, RF-19, RF-22 | between C0 and C0R | radios stay | radios stay |
| X13 | dormant antennas, no roaming | RF-21 to RF-23 | C0R or a tether-only Skin | no change | no change |
| X14 | Qi2.2 with no cell behind it | F21 21.2.6, ENR-24 | Skin omits the Qi path. K-2 restores it | no change | no change |
| X15 | Article 11 and the removable quadrant | FINAL/17 17.6, FINAL/22 22.12 | Core cells removable. Skin holds none | no change | no change |
| X16 | the legal class of the Leaf | hw/energy/06 section 1 | ask a lawyer which box is the product | no change | no change |
| X17 | the mass figures of the catalogues | FINAL/03 3.1, MEC-2 | state Skin, Core and tether apart | state Leaf and Core | no change |
| X18 | rear glance and wallet standby with no Core | hw/energy/04, hw/energy/05 | Skin shows the safe screen only | no change | no change |
| X19 | the Host Life Law and a Skin with no store | FINAL/22 22.2, D-9, HST-1, HST-2 | keep `20` cells or accept `3 s` dark (K-7) | no change | no change |

**Two numbers behind X1, X4 and X10**. The leaves carry two `9.70 Gbit/s` display pairs and a `0.4 Gbit/s` back channel. The camera at `12.5 MP`, `10 bit`, `30 fps` needs `3.75 Gbit/s`, so it needs a pair (`out/lanes.txt`). The rear panel at `120 Hz` with DSC needs `0.22 Gbit/s`, or `55 %` of the back channel.

---

## 10 · The proposed gates

Full text in `out/gates.md`. The Lead merges them into the series of Part 21 if Ayaz rules for the Split.

| Gate | The test | The pass condition |
|---|---|---|
| HC-A1 | the allocation table against the catalogues | each part of `HARDWARE/13` and each group of `HARDWARE/14` to `19` has a cited row. `parts.py` exits `0`. Module sum `10.80 g` within `0.01 g` |
| HC-A2 | the ring after the move | staying parts fill `60 %` or less of the free area at C0. The packer places every part with `0` errors |
| HC-A3 | the safe screen with the link cut | the Skin shows the ROM screen within `60 ms`. No updatable code is on the path. `65 536` fault sets pass |
| HC-A4 | the Core plug on a seat | pads at `0 V` until the `3 ms` answer. First break under `0.8 ms` at a `30 N` pull. `1 000` mates, no damage |
| HC-A5 | the camera path at C0 | a pair carries `12.5 MP` at `60 fps` (`7.5 Gbit/s`) with no dropped frame. The indicator follows the sensor rail |
| HC-A6 | the quadrant swap on a Skin with no cells | swap under `3 s`. The calibration of `32` tiles loads in under `3 ms`. Core cells leave with no tool in under `30 s` |
| HC-A7 | the part record and the identity chip | each moved part has a record on the Core. The chip signs challenges only. A wrong pair is refused |
| HC-A8 | the first weighed build | each part is weighed. The Skin is within `10 %` of the derived value. The weighed Leaf replaces `68 g` and `88 g` |
| HC-A9 | the necessity test at C1 | the `60 GHz` array at `30 m` for `1 h` gives under `13.43 Gbit/s`, which confirms the rule. A higher rate goes to Ayaz |
| HC-A10 | the Zero CPU and naming claims | no text calls a Core that hosts the validator role Zero CPU. A search for banned product names returns `0` hits |
| HC-A11 | the stream check on the Skin | a stream from an unpaired Core key shows the safe screen in `1 000` of `1 000` trials |
| HC-A12 | the antennas at C0 and C0R | C0R passes `RF-21` to `RF-23` unchanged. At C0 the Leaf states that it cannot roam |
| HC-A13 | the host swap with no store (L2) | the Skin shows the safe screen through a `3 s` swap and resumes. If not, the `20`-cell Buffer is added |

**The candidates for Ayaz**. None is a decision.

| No. | The candidate |
|---|---|
| K-1 | shrink the ring board and the spreader after the C0 move, to buy a larger sensor or a thinner module |
| K-2 | put the Qi coil, rectifier and magnets (`3.9 g`) back on the C0 Skin, if it must charge off its tether |
| K-3 | choose C0 or C0R for the radio SiPs. C0R keeps `1.0 g` and `54 USD` on the Leaf, plus the royalty |
| K-4 | build the C0 Core in the dock family: pad, heat path, `20 Wh` pack, validator bay |
| K-5 | add a mass list of the L.6.0 body to `HARDWARE`, and retire `68 g` and `88 g` |
| K-6 | delete the cell layer from all `128` tiles at C0, so the stack falls from `2.00` to `1.10 mm` |
| K-7 | keep `20` Buffer cells on the C0 Skin for the Host Life Law: `2.4 g`, `0.9` to `1.2 Wh`, about `12 USD` |

---

## 11 · The open issues

1. **The mass basis**. The body mass is derived, not stated. The range is `±10 %`. Gate `HC-A8` weighs it.
2. **The catalogue masses disagree**. The same `8` N52H magnets weigh `0.34 g` in `HARDWARE/13` and `1.55 g` in `HARDWARE/14`. The `24` seam magnets weigh `0.76 g` by volume and `1.80 g` in `HARDWARE/15`. The stated IC masses imply about `8 g/cm³`, which is high.
3. **The ring stack**. The column is `3.90 mm`, the rear window `0.30 mm` and the module `4.00 mm`. The parts list does not close this. The CAD can show an aperture in the rear window. I did not check it.
4. **The PDLC film and the holdover capacitors** are in the L.5.0 catalogue and not in the `2.00 mm` stack. Part 21 does not say they are withdrawn.
5. **The antennas A5 to A8** are in `HARDWARE/19` and Part 21 does not restate them.
6. **The part list lacks parts**. `U9` NOR, `U4B`, two crystals, `7` inductors and two flexes appear in `placement.py` and not in `HARDWARE/13`. This seat adds them as `6` rows.
7. **The packer is not stable**. Its baseline gives `5` failures here and `3` in `placement_results.txt`. The area check is the stable test.
8. **Lanes**. The camera uplink at C0 needs a display pair to run backwards. That is a SerDes feature the display team has not designed. The calibration read of `154 KB` is a guess of `4.8 KB` per tile.
9. **The link and far seats**. `hw/core/link/` and `hw/core/far/` were empty when this seat ran. Gate `HC-A9` checks their number against the rule.
10. **The radio SiP split**. No part list gives the front end share of `U2A`, `U2B` and `U5`. A vendor answer closes line item L3.
11. **The legal questions** X15 and X16 and the royalty go to a lawyer.
12. **The port part** uses L.5.0 masses and costs. Part 21 gives it no list. **The dock** has no mass list, and its `310 g` is an L.5.0 figure.

**Tags**. `[HYPOTHESIS]` for every derived mass, every cost range, every fraction and every resolution. `[TREE]` for the stated masses copied from the cited files. `[GENERAL]` for the Wi-Fi 7 rate. `[DECISION]` for the rule of Ayaz. The program rules of `BRIEF.md` Section 7 apply.
