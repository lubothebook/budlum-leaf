# BUDLUM LEAF · hw/energy · THE ENERGY AND BMS TEAM

**Revision L.6.0 · 2026-10-12**. Source of truth: `FINAL/21` Section 21.2.5, `HARDWARE/11`, `HARDWARE/15`, `HARDWARE/13`. Where this directory and `HARDWARE/11` or `HARDWARE/15` differ, FINAL/21 rules, and this directory implements it.

## 1 · What is here

| The file | The content |
|---|---|
| `01-MICRO-CELL.md` | the `9.25 x 9.25 x 0.90 mm` hermetic cell: can, stack, two chemistries, feedthrough, vent, swell, fuse |
| `02-PACK-ARCHITECTURE.md` | the `1S128P` pack, the hinge crossing, the fuse and the switch per cell, the balance, the `4 x 32` multiplexer, ENR-23 |
| `03-POWER-TREE-AND-BAR-PINS.md` | the power tree to every load, the `12` bar leaves with current per leaf, the dead pad |
| `04-ENERGY-BUDGET.md` | the budget per use case, the run times, the charge plan |
| `05-DOCK-PACK-AND-B-CELL.md` | the `20 Wh` dock pack and the `0.14 Wh` B cell |
| `06-EU-2023-1542-REMOVABILITY.md` | the removability note for Article 11 and the phone ecodesign rules |
| `cell/microcell.py` | designs the electrode stack in the can; prints mAh, Wh, Wh/L |
| `pack/network.py` | solves the 128-node body bus: loads, charge, faults, fuse, balance |
| `pack/bar_pins.py` | the leaf map, the mirror check, the current per leaf, the probe leakage |
| `budget/runtime.py` | the use-case budget, the run times, the B cell, the dock refills |
| `run_all.py` | runs all four scripts in order and prints the gate checks |
| `out/` | the outputs: `.txt` for reading, `.json` for other teams |

## 2 · How to run it

1. Run `python3 hw/energy/run_all.py` from the repo root.
2. Read the gate checks at the end of the output.
3. Read the details in `hw/energy/out/*.txt`.

It needs `numpy` and `scipy` only. The whole run takes a few seconds.

## 3 · The key results

| The result | The value | The tag |
|---|---|---|
| cell, G: graphite / LiCoO2 `4.45 V` | `13.79 mAh`, `0.0534 Wh`, `1 036 Wh/L` stack, **`694 Wh/L` cell**, target `600` | `[TREE]` |
| cell, S: Si-C / LiCoO2 `4.48 V` | `17.19 mAh`, `0.0653 Wh`, `1 334 Wh/L` stack, **`850 Wh/L` cell**, target `750` | `[TREE]` |
| electrode stack, both | `3` double-sided cathodes, `4` anodes, `6` separators of `7 µm`, in `0.84 mm` | `[TREE]` |
| body at the targets | **`5.90 Wh`** at `600 Wh/L`, **`7.38 Wh`** at `750 Wh/L`, above the `5.7` and `7.2 Wh` of FINAL/21 | `[TREE]` |
| ENR-22 per quadrant | `1.476 Wh` against `1.42`, `1.845 Wh` against `1.80` | `[TREE]` |
| pack topology | `1S128P`, `3.40-4.48 V` bus, fuse and switch per cell | `[DECISION]` |
| hinge power line | `2 µm` Cu, `18.7 mΩ`; with EGaIn in parallel `8.2 mΩ` | `[TREE]` |
| bus loss | `23 mW` in video, `137 mW` at a `8.7 W` peak | `[TREE]` |
| balance | SOC spread `19.5 %` without, **`2.2 %`** with the TCM balance | `[TREE]` |
| ENR-23, one cell shorted | its fuse opens in `0.45-0.79 µs` at `15-20 A`. The other `127` stay under `0.34 A` | `[TREE]` |
| fuse selectivity | hinge melt I²t is `506` times the fuse melt I²t | `[TREE]` |
| bar leaves | GND `1,12`, VBUS `2,11`, lanes `3,4,9,10`, VHV `5,8`, sidebands `6,7`. Mirror-safe | `[DECISION]` |
| worst leaf current | `0.74 A` for the B at a `4.5 W` peak; `1.50 A` for a port part at `27 W, 9 V` | `[TREE]` |
| dead-pad probe | `0.0014 µA` average in salt water, against `1 µA` | `[TREE]` |
| delta session `2.02 W` | `2.6 h` (G `600`) to `3.6 h` (S model) | `[TREE]` |
| video session `3.27 W` | `1.6 h` (G `600`) to `2.2 h` (S model) | `[TREE]` |
| wallet standby | `95-133 h` | `[TREE]` |
| Qi2.2 `25 W` | `20.4 W` to the cells, `2.8 C` mean on G, `50 %` in `8.7 min`, `5.8 W` heat | `[TREE]` |
| dock `20 Wh` | `2.84` refills of the `600 Wh/L` body through the pads, `2.13` by Qi | `[TREE]` |
| B cell in the hermetic can | `0.189 Wh` model against the `0.14 Wh` commitment | `[TREE]` |

## 4 · The gates this directory feeds

| Gate | What this directory gives it |
|---|---|
| ENR-22 | the cell and quadrant energy, the `800`-cycle pass condition |
| ENR-23 | the fuse, the cell switch, the coordination, the fault table |
| ENR-24 | the charge plan, the `5.8 W` heat of a `25 W` charge |
| ENR-19, MON-16 | the dead-pad law and the probe leakage |
| MON-21, MON-23 | the leaf currents and the B power path |
| MEC-39, MEC-42 | the hinge copper current, `0.70 A` peak |
| MEC-40 | the `0.38 A` join of a swapped quadrant |
| SW-20 | the dock pack and its two paths |

## 5 · The open issues

1. **The S variant needs a scaffold Si-C anode with about `22 %` swell**. A plain Si-graphite blend at `50 %` swell gives `733 Wh/L` and misses `750`.
2. **The hinge ribbon must give `0.90 mm` of its height to power**. The display lanes share the rest. Interface with the hinge and display teams.
3. **One shorted cell still heats its own tile**. `192-235 J` in a `0.53 g` tile. The vent and gate ENR-15 carry it.
4. **A `25 W` charge is `2.8-3.5 C`**. Graphite needs `25 °C` or more. The `5.8 W` heat sets the sustained rate.
5. **FINAL/21 runtimes of `1.9-3.7 h` left out converter losses**. At the targets the band is `1.74-3.26 h`. The S model with better converters reaches `3.80 h` at `2 W`.
6. **Three dock refills of the `750 Wh/L` body need `26.3 Wh`**. A third pouch gives `30.3 Wh` in the same deck. A decision for Ayaz.
7. **The B cell has `0.18 mm` of clearance** to the camera column. The B team owns the ring layout.
8. **The handshake must not lock out compatible quadrants**. It checks a safety certificate, with a free pairing tool.
9. **The B cell under Article 11**. Treat the B module as the replaceable battery unit, or add a screwed back window.
10. **Custom silicon**: TCM per tile, U_Q per quadrant, seat controller per edge. None exists today.
