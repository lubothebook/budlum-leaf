# BUDLUM LEAF · CORE AND SKIN · STUDY · 02 · THE COST AND THE BREAK-EVEN

**Revision L.7 candidate · 2026-10-19 · Study seat**. Every number here is a `[HYPOTHESIS]`. The model is `cost.py`. It imports `program/budget.py` read only. Cost means bill of materials in USD per unit, before margin.

## 1 · The verdict first

**The Split does not make the screen cheap.** Micro-LED tiles are `76 %` of the unit (P10 `67 %`, P90 `83 %`). The Split moves none of that cost.

A Skin costs `1 331 USD` against `1 575 USD` for the all-in-one Leaf. That is `15 %` less for the Skin. A system of four Skins on one Core is `8.9 %` cheaper.

**The Split makes the surface lighter and thinner.** The Skin is about `40 g` against `68 g`, and `0.90 mm` against `2.00 mm`. That is the real gain. It is a weight and thickness story and a service story, and a cost story only at two Skins or more.

**The break-even is two Skins per Core.** At one Skin, a wired Skin is a coin flip near zero, and a wireless Skin loses. At two Skins every draw of the sweep is cheaper for the Split. `[HYPOTHESIS]`

**The distance order narrows the saving.** At C0 only `12 %` of the BOM leaves the Leaf. At C1 and the 60 GHz case it is `9` to `9.5 %`. At C2 nothing leaves, since the Skin keeps the radio and decoder.

## 2 · The model

### 2.1 Where the numbers come from

| The input | The source | The tag |
|---|---|---|
| the all-in-one unit cost, three volumes, low, base, high | `program/budget.py`, read by import | `[TREE]` and a `[HYPOTHESIS]` of the Program Office |
| the micro-LED tile cost and yield, the cell cost, the other blocks | the same tables, reused with no copy | `[TREE]` |
| what the Skin keeps and what the Core takes | the study seat, Section 2.2 | `[HYPOTHESIS]` |
| the Core board, enclosure, cell, link chips, radios | the study seat. Each has a low, base and high in `PARAMS` | `[HYPOTHESIS]` |
| the surface and silicon loads | `hw/energy/04` through `hw/core/BRIEF.md` Section 3 | `[TREE]` |
| the free-air limit `1.73 W` still, `2.37 W` light wind | `hw/core/BRIEF.md` Section 3 | `[TREE]` |

The sweep draws every budget group and every `PARAMS` term at random, `6 000` draws at `1 M` per year.

### 2.2 What the Skin keeps and what the Core takes

| The part | In the Skin | In the Core |
|---|---|---|
| micro-LED tiles, tile mechanics, touch | all | none |
| decoder and TCON (U1, U6) | `60 %` at C0, all at C1 | the rest, with an extra lane per added Skin |
| camera column and a stub of the B module | all, since the sensor stays where the optics are | none |
| identity chip | one per Skin | none |
| 5G modem, Wi-Fi, secure element, audio, power | the IMU share only | all, with the wallet |
| cells | none at C0. A small cell at C0r and C1 | a conventional cell sized to the session |
| Qi coil | none at C0 | one, for the Core |
| link | a cable end, or a radio, or the Wi-Fi share | the other end, one per Skin |
| royalties | none | on the system in the base case |

### 2.3 The classes

| The class | The link | What the model does |
|---|---|---|
| C0, to `2 m` | a tether cable, a chip at each end | the Core powers the Skin through the cable |
| C0r, to about `10 m` | a 60 GHz radio at each end, clear path | the Skin carries a cell, a coil and its radio |
| C1, to `30 m` | Wi-Fi 7 carrying a slice stream | the Skin keeps the whole decoder and the Wi-Fi share, and carries a cell |
| C2, kilometres | the 5G modem of the Leaf | the Skin is the L.6.0 Leaf. The far Core is a validator |

## 3 · The results at one million per year, base draw

### 3.1 The cost of one Skin and one Core

| The item | USD | The tag |
|---|---|---|
| all-in-one Leaf 160, L.6.0 | `1 575` | `[TREE]` `budget.py` base |
| Skin, C0 wired, with camera | `1 331` | `[HYPOTHESIS]` |
| Skin, C0r 60 GHz | `1 370` | `[HYPOTHESIS]` |
| Skin, C1 Wi-Fi 7 | `1 378` | `[HYPOTHESIS]` |
| Skin, C2 | `1 515` before royalties, the same as the Leaf | `[HYPOTHESIS]` |
| Core for `1`, `2`, `4`, `8` Skins, wired | `154`, `168`, `195`, `250` | `[HYPOTHESIS]` |
| Core for `1`, `2`, `4`, `8` Skins, 60 GHz | `164`, `188`, `236`, `331` | `[HYPOTHESIS]` |
| Core for `1`, `2`, `4`, `8` Skins, Wi-Fi 7 | `144`, `150`, `162`, `192` | `[HYPOTHESIS]` |

### 3.2 The saving and the break-even, a Leaf 160 class Skin

| The class | N=1 | N=2 | N=4 | N=8 | The break-even |
|---|---|---|---|---|---|
| C0 wired | `+30 USD` (`1.9 %`) | `+207` (`6.6 %`) | `+559` (`8.9 %`) | `+1 264` (`10.0 %`) | `1`, by a hair |
| C0r 60 GHz | `-20` (`-1.3 %`) | `+105` (`3.3 %`) | `+356` (`5.7 %`) | `+858` (`6.8 %`) | `2` |
| C1 Wi-Fi 7 | `-8` (`-0.5 %`) | `+128` (`4.1 %`) | `+401` (`6.4 %`) | `+938` (`7.4 %`) | `2` |
| C2 far | `0` | `0` | `0` | `0` | not applicable |

### 3.3 The spread of the sweep, wired

| The result | P10 | P50 | P90 |
|---|---|---|---|
| all-in-one Leaf 160 | `1 113` | `1 604` | `2 452` |
| Skin | `887` | `1 356` | `2 185` |
| Core, N=4 | `189` | `218` | `250` |
| saving at N=1 | `-16` | `+15` | `+49` |
| saving at N=2 | `+130` | `+187` | `+254` |
| saving at N=4 | `+415` | `+532` | `+667` |
| saving at N=8 | `+982` | `+1 223` | `+1 498` |

**The probability that the Split is cheaper.** Wired: `0.72` at one Skin and `1.00` from two. Wireless 60 GHz: `0.04` at one Skin and `0.94` at two. Wi-Fi 7: `0.12` at one Skin and `1.00` from two. `[HYPOTHESIS]`

### 3.4 The volumes

| The volume per year | All-in-one | Skin wired | Core N=4 | Saving N=1 | Saving N=4 |
|---|---|---|---|---|---|
| `100 000` | `3 949` | `3 456` | `328` | `+89` (`2.3 %`) | `+1 076` (`6.8 %`) |
| `1 000 000` | `1 575` | `1 331` | `195` | `+30` (`1.9 %`) | `+559` (`8.9 %`) |
| `5 000 000` | `803` | `644` | `147` | `+12` (`1.5 %`) | `+382` (`11.9 %`) |

## 4 · Mixed sizes

The Core is one unit for the whole family. Costs are at `1 M` per year, wired, base draw.

| The set of Skins | Split | All-in-one | Saving | Core |
|---|---|---|---|---|
| Leaf 160 | `1 545` | `1 575` | `+30` (`1.9 %`) | `154` |
| 2 x Leaf 80 and 1 x Leaf 160 | `3 050` | `3 355` | `+304` (`9.1 %`) | `181` |
| Leaf 80, Leaf 160, Leaf 160 squared | `4 989` | `5 411` | `+422` (`7.8 %`) | `181` |
| Leaf 80, 160, 160 squared and 480 | `6 133` | `6 727` | `+594` (`8.8 %`) | `195` |
| 2 x Leaf 160 and 1 x Leaf 480 | `4 087` | `4 466` | `+378` (`8.5 %`) | `181` |
| 8 x Leaf 80 | `6 168` | `7 117` | `+950` (`13.3 %`) | `250` |

**The break-even by size.** A Leaf 80 Skin breaks even at two Skins, because its silicon share is larger. Leaf 160, 160 squared and 480 break even at one Skin by a small margin. `[HYPOTHESIS]`

**The Leaf 480 is a weak case.** It uses the `152 ppi` T40 B tiles. The model gives them the emitter cost of the `508 ppi` tile and keeps the Leaf cell. A quote replaces both. `[HYPOTHESIS]`

## 5 · What dominates the cost

| The term | Share of the all-in-one unit | The reading |
|---|---|---|
| micro-LED tiles, `128` | `76 %` (P10 `67 %`, P90 `83 %`) | the Skin keeps all of it |
| silicon and radio (U1, U6, U5, U2, U7) | about `5 %` | this moves to the Core |
| cells and their protection | about `5 %` | this moves to the Core as a cheaper cell |
| cellular royalties | about `4 %` | the base of the royalty decides what stays |
| camera column | about `1 %` | stays in the Skin |
| everything else | about `9 %` | mechanics, assembly, pack, touch, Qi, B module |

**The silicon does not dominate.** The ASICs, the modem and the radios cost `82 USD` of `1 515`. A Core cannot save a large sum by taking silicon alone.

**The tornado.** At N=4 wired, the saving moves most with the cell cost group (`263 USD` swing). Silicon (`105`), mechanics (`95`) and the assembly factor (`94`) follow. The tile cost swings it by `0`, since the tile sits on both sides. `[HYPOTHESIS]`

## 6 · What it means for the aim of Ayaz

| The aim | The result |
|---|---|
| a lighter screen | **yes.** About `40 g` against `68 g`, so `41 %` lighter. The thickness falls from `2.00` to about `0.90 mm`. `[HYPOTHESIS]` |
| a cheaper screen | **only a little.** The Skin is `15 %` cheaper. The system is `9 %` cheaper at four Skins. The tile is the cost |
| one hardware for many screens | **yes, by two Skins.** The Core costs `154` to `250 USD` for one to eight Skins |
| a part changes in the Core and not in the screen | **yes.** See `MODULARITY.md` |

**What lowers the screen cost.** Only the tile. If the tile cost falls to `0.31` of the base, a Skin costs `500 USD`. At `0.25` the Split saves `22 %` of the system. At `0.10` it saves `31 %`. The Split gains weight as the tile gets cheaper, because the silicon share grows. `[HYPOTHESIS]` The tile work of `hw/display` is the lever of the screen cost.

**A public signal.** Apple ended its micro-LED watch display, and reports name cost and difficulty. `[PUBLICATION]` Search row 20 of `PRIOR-ART.md`.

## 7 · The mass and the Core

| The item | The value | The tag |
|---|---|---|
| the L.6.0 body | `68.0 g`, `2.00 mm` | `[TREE]` |
| the cells | about `25 g` for `128` cells at `2.5 g/cm3` | `[GENERAL]` density |
| the Skin at C0 | about `40 g`, `0.90 mm` | `[HYPOTHESIS]` |
| the Core for `1`, `2`, `4`, `8` Skins | `11.0`, `16.3`, `26.8`, `47.8 Wh` and about `114`, `135`, `177`, `261 g` | `[HYPOTHESIS]` |

**A Core for four Skins** is about `177 g`. Meta quotes `182 g` for the Orion puck, which is a public figure of the same class. `[PUBLICATION]` Search row 3.

## 8 · The heat finding

| The Skin load, video session | Low, base, high | The reading against `1.73 W` still |
|---|---|---|
| C0 wired: surface `1.35 W` and a link end | `1.55`, `1.75`, `2.15 W` | at the limit. Inside with a light wind |
| C0r 60 GHz: surface and a radio | `2.35`, `3.35`, `4.85 W` | over the limit and over the wind figure |
| C1 Wi-Fi 7: surface, decoder and store | `1.95`, `2.35`, `2.95 W` | over the still limit, near the wind figure |
| C2 | the L.6.0 load | no heat moves out |

**A wireless Skin breaks the heat law.** A 60 GHz radio at about `2 W` doubles the surface load. This is a `[HYPOTHESIS]` for the radio terms. The link and heat seats own it.

## 9 · The assumptions that carry the result

| The assumption | If it fails |
|---|---|
| the Core uses a conventional cell at `0.7 USD/Wh`, and not the micro cell | with the micro cell the Core energy costs more and the saving falls |
| the royalty base is the whole system | with the Core only as the base, N=4 saves `772 USD`, not `559` |
| the Skin carries the camera column | a Skin with no camera is `26 USD` cheaper |
| the extra NRE is `40 M USD` | at N=4 the extra NRE is repaid after about `71 600` systems |
| the Leaf 480 has the Leaf cell and the `508 ppi` emitter cost | a quote changes the large Skin cost |

## 10 · The proposed gates of this file

| Gate | The test | The pass condition |
|---|---|---|
| CSG-8 | supplier quotes for the tile, the link chips and the Core cell, with a date | each `[HYPOTHESIS]` range of `PARAMS` is replaced or kept inside the quote range |
| CSG-9 | a measured Skin of a Leaf 160 class with no cell | mass at or under `45 g` and thickness at or under `1.00 mm` |
| CSG-10 | the break-even rerun on the quotes | a written break-even number, with the sweep, for C0, C0r and C1 |
