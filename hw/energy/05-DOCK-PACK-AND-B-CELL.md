# BUDLUM LEAF · ENERGY · 05 · THE DOCK PACK AND THE B CELL

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. Scripts: `budget/runtime.py`, `cell/microcell.py`. Output: `out/budget.txt`, `out/cell_spec.txt`. Gates ENR-22, SW-20, MON-21.

## 1 · The B cell, `0.14 Wh`

### 1.1 The cell

| The item | The value | The tag |
|---|---|---|
| envelope | `20.0 x 8.0 x 1.50 mm`, `240 mm³` | `[DECISION]` FINAL/21 21.2.5 |
| energy at `600 Wh/L` | `0.144 Wh`, `37.2 mAh` at `3.87 V` | `[TREE]` |
| build | the hermetic `30 µm` can of the body cell, same line, same chemistry | `[DECISION]` this team |
| the same can, G chemistry, model | `4` cathodes, `48.8 mAh`, `0.189 Wh`, `788 Wh/L` | `[TREE]` `microcell.py` |
| the same can, S chemistry, model | `5` cathodes, `59.5 mAh`, `0.226 Wh`, `943 Wh/L` | `[TREE]` |
| committed value | `0.14 Wh`. The model excess is margin | `[DECISION]` |
| protection | its own fuse neck and a TCM, as a body cell | `[DECISION]` |

**Why the hermetic can**. A `1.50 mm` pouch loses `2-3 mm` of each edge to the heat seal. On a `8.0 mm` cell that is a third of the width. The welded can loses `0.38 mm` per side. `[GENERAL]` `[TREE]`

### 1.2 The fit in the ring

The ring shell is `Ø32.0 mm` with a `1.0 mm` wall. A `20.0 mm` long cell placed on a chord reaches the wall at `11.18 mm` from the centre. Its inner edge then sits `3.18 mm` from the centre. The camera column reaches `3.00 mm`. The clearance is `0.18 mm`. `[TREE]` `runtime.py`

**This is tight**. The B team owns the ring layout. The cell, the jack trough and the speaker share one half of the disc. Interface item with the B team. Gate MON-21.

### 1.3 The duties of the B cell

| The duty | The power | The time on the B cell | The rate | The tag |
|---|---|---|---|---|
| quadrant swap or bar lift: radios kept, decoder idle | `0.40 W` | `19.7 min` | `2.9 C` | `[TREE]` |
| a `3 s` swap | `0.40 W` | uses `0.33 mWh` | `2.9 C` | `[TREE]` |
| B alone, rear display glance | `0.105 W` | `75.0 min` | `0.8 C` | `[TREE]` |
| B alone, wallet standby | `0.055 W` | `143 min` | `0.4 C` | `[TREE]` |
| B alone, voice call on 5G | `0.73 W` | `10.8 min` | `5.3 C`, a pulse duty | `[TREE]` |
| a ring peak of `4.50 W` | not served | | `33 C`, refused | `[TREE]` |

**The rules**. `[DECISION]` this team.

1. The B cell serves the ring when the bar is off the seat, or during a swap.
2. U4 caps the islanded ring at `0.40 W`. A voice call runs at `0.73 W` for `10 min`, then U4 asks for the seat.
3. Peaks always come from the body bus. The B cell never carries a flash or a 5G burst on its own.
4. U4 charges the B cell from VBUS at `1 C`, `37 mA`.
5. `U7` keeps its always-on supply from the B cell. The wallet answers with no body and no network.

## 2 · The dock pack, `20 Wh`

### 2.1 The pack

| The item | The value | The tag |
|---|---|---|
| energy | `20 Wh` | `[DECISION]` FINAL/21 21.2.5 |
| build | two pouch cells, `70 x 60 x 3.7 mm`, graphite / LiCoO2 `4.45 V`, `1S2P` | `[DECISION]` this team |
| density | `650 Wh/L`, a shipping phone-cell class | `[GENERAL]` |
| capacity | `20.2 Wh`, `5 220 mAh` at `3.87 V` | `[TREE]` |
| place | in the `240 x 120 x 12 mm` dock deck, under the Qi2.2 transmitter coil | `[DECISION]` HARDWARE/18 |
| protection | a fuel gauge, a protector with its own FETs, and one NTC per cell | `[GENERAL]` |
| removal | a battery door with two standard screws. See `06-EU-2023-1542-REMOVABILITY.md` | `[DECISION]` |

### 2.2 The two paths from the dock to the Leaf

| The path | The chain | Delivered to the Leaf cells |
|---|---|---|
| Qi2.2, the dock coil | usable `95 %`, boost `94 %`, coil to cell `72 %` | `12.9 Wh` |
| the `12` pads, a seat field in the dock slot | usable `95 %`, dock converter `95 %`, U_Q and bus `95 %` | `17.2 Wh` |

All rows are `[TREE]`. The coil-to-cell figure of `72 %` is `[HYPOTHESIS]` until gate ENR-24.

### 2.3 The refills

| The Leaf store, body plus B cell | Refills by Qi | Refills by the pads |
|---|---|---|
| G at `600 Wh/L`, `6.05 Wh` | `2.13` | **`2.84`** |
| G at the model, `6.97 Wh` | `1.84` | `2.46` |
| S at `750 Wh/L`, `7.52 Wh` | `1.71` | `2.28` |
| S at the model, `8.50 Wh` | `1.51` | `2.02` |

All rows are `[TREE]`.

**The reading**. FINAL/21 states that the dock refills the Leaf about three times. That holds for the `600 Wh/L` body through the pads: `2.84`. A larger body stores more, so it gets fewer, larger refills. The energy the dock delivers stays `17.2 Wh`. `[TREE]`

**The path to three refills of the `750 Wh/L` body, with no target lowered**. Three pad refills need a `26.3 Wh` pack. A third `70 x 60 x 3.7 mm` cell fits in the `240 x 120 x 12 mm` deck. It gives `30.3 Wh`. That is a decision for Ayaz. `[TREE]` `[HYPOTHESIS]` for the deck space.

### 2.4 The rules of the dock

1. The dock prefers the pads when the Leaf stands in the slot. The pads deliver `90 %` of the usable pack energy, and Qi delivers `68 %`.
2. The pads follow the dead-pad law of `03-POWER-TREE-AND-BAR-PINS.md`. The dock answers the challenge as role "dock".
3. The dock charges its own pack from a USB-C PD supply. Its own port is a dock port, so Directive (EU) 2022/2380 applies to it. `[PUBLICATION]`
4. The validator board of the dock draws from mains only. It never drains the pack. Gate SW-20.

## 3 · The open items

1. The `0.18 mm` clearance of the B cell needs the B team's ring layout.
2. A dock slot with a seat field is new to `HARDWARE/18`. Interface item with the dock team. Gate SW-20.
3. The `30 Wh` dock pack is a proposal for Ayaz. The `20 Wh` decision stands until he answers.
