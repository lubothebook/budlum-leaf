# BUDLUM LEAF · ENERGY · 01 · THE HERMETIC MICRO CELL

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. Source of truth: `FINAL/21` Section 21.2.5. Script: `cell/microcell.py`. Output: `out/cell_spec.txt`, `out/cell_spec.json`. Gates ENR-22, ENR-23.

## 1 · The envelope

| The item | The value | The tag |
|---|---|---|
| outside | `9.25 x 9.25 x 0.90 mm`, corner radius `0.40 mm` | `[DECISION]` FINAL/21 |
| envelope volume | `76.88 mm³` | `[TREE]` script |
| can | deep-drawn `316L` cup and lid, `30 µm`, laser seam weld | `[DECISION]` FINAL/21 |
| can option | titanium Grade 1, `30 µm`, lighter by `0.04 g` | `[HYPOTHESIS]` |
| can polarity | case negative | `[DECISION]` this team |
| inner cavity | `9.19 x 9.19 x 0.84 mm` | `[TREE]` script |
| count | `128`, one per tile, `32` per quadrant | `[DECISION]` FINAL/21 |

**Why case negative**. Stainless steel stays passive at the anode potential. At `4.45 V` against lithium it pits in a LiPF6 electrolyte. So the can is the negative terminal, and the positive terminal leaves through a ceramic feedthrough. `[GENERAL]`

## 2 · The section, from the wall inward

| The lateral margin, per side | The width |
|---|---|
| can wall | `30 µm` |
| weld clearance, no polymer in the heat zone | `100 µm` |
| PEEK locator frame | `50 µm` |
| separator overhang past the anode | `100 µm` |
| anode overhang past the cathode | `100 µm` |
| laser-cut dead rim on the cathode | `20 µm` |
| **anode side / cathode side** | **`8.69 mm` / `8.49 mm`** |

The cathode loses two corner notches. The feedthrough corner takes `1.40 x 1.40 mm`. The negative tab bundle takes `0.70 x 0.70 mm` on the opposite corner. The net cathode area is `68.87 mm²`. `[TREE]`

## 3 · The two variants

The script fits the largest number of electrode pairs and the highest loading into the `0.84 mm` cavity. It keeps a swelling allowance, a liner and a tolerance reserve. Three double-sided cathodes win for both variants.

| The layer | G: graphite / LiCoO2 `4.45 V` | S: Si-C composite / LiCoO2 `4.48 V` |
|---|---|---|
| cathodes | `3`, double-sided, LiCoO2 on `9 µm` Al | `3`, double-sided, LiCoO2 on `9 µm` Al |
| cathode coat, per side | `46.1 µm` | `55.6 µm` |
| anodes | `4`: `2` double-sided, `2` outer single-sided on the can | `4`: the same |
| anode coat, per side | `63.1 µm` graphite on `6 µm` Cu | `47.4 µm` Si-C blend on `6 µm` Cu |
| separators | `6 x 7 µm` (`5 µm` PE, `2 µm` Al2O3) | `6 x 7 µm` |
| areal loading | `3.34 mAh/cm²` per side | `4.16 mAh/cm²` per side |
| N/P ratio | `1.08` | `1.10`, prelithiated anode |
| height: cathodes / anodes / separators | `303.6 / 402.5 / 42.0 µm` | `360.9 / 308.3 / 42.0 µm` |
| swelling allowance | `43.4 µm` | `69.2 µm` |
| compliance pad, porous PTFE | `62.0 µm`, `70 %` compression at end of life | `98.9 µm`, `70 %` compression |
| liners and tolerance | `10 + 20 µm` | `10 + 20 µm` |
| **total height** | **`840.0 µm` of `840.0 µm`** | **`840.0 µm` of `840.0 µm`** |
| capacity | **`13.79 mAh`** | **`17.19 mAh`** |
| nominal voltage, window | `3.87 V`, `3.00-4.45 V` | `3.80 V`, `2.80-4.48 V` |
| energy | **`0.0534 Wh`** (`192 J`) | **`0.0653 Wh`** (`235 J`) |
| stack density, active layers only | `1 036 Wh/L` | `1 334 Wh/L` |
| **cell density, envelope** | **`694 Wh/L`** | **`850 Wh/L`** |
| target, FINAL/21 | `600 Wh/L` | `750 Wh/L` |
| design margin | `+15.7 %` | `+13.3 %` |
| DC resistance, 10 s | about `4.8 Ω` | about `4.4 Ω` |
| mass | about `0.115 g` | about `0.114 g` |

All rows are `[TREE]` outputs of `cell/microcell.py`. The material inputs carry the tags of Section 5.

**How to read the margin**. The model has no first-cycle loss beyond the N/P ratio and no excess electrolyte height. The margin above the target pays for those. The committed values stay `600` and `750 Wh/L`. `[DECISION]`

## 4 · The sensitivities

| The change | G cell | S cell |
|---|---|---|
| lateral margin `-0.05 mm` per side | `745 Wh/L` | `871 Wh/L` |
| lateral margin `+0.10 mm` per side | `691 Wh/L` | `809 Wh/L` |
| loading capped at `3.0 mAh/cm²` | `666 Wh/L` | `815 Wh/L` |
| anode swell `10 %` | not used | `912 Wh/L` |
| anode swell `35 %` | not used | `791 Wh/L` |
| anode swell `50 %`, a plain Si-graphite blend | not used | `733 Wh/L` |

**The finding**. In a `0.84 mm` cavity the swelling allowance decides the silicon variant. A Si-graphite blend that swells `50 %` misses `750 Wh/L`. A porous-carbon scaffold Si-C composite with about `22 %` electrode swell clears it. So the S variant needs a scaffold silicon. `[TREE]` `[HYPOTHESIS]` for the swell figure.

## 5 · The chemistry references

| The input | The value used | The source |
|---|---|---|
| LiCoO2 at `4.45-4.48 V` | `182-188 mAh/g`, `4.10 g/cm³`, `97 %` active | `[PUBLICATION]` Zhang J.-N. et al., Nature Energy 4, 594 (2019), LiCoO2 cycled to `4.6 V` |
| graphite | `350 mAh/g`, `1.70 g/cm³`, `96 %` active | `[GENERAL]` theoretical `372 mAh/g` |
| graphite swell | `6 %` reversible, `4 %` end of life | `[PUBLICATION]` Schweidler S. et al., J. Phys. Chem. C 122, 8829 (2018), about `10 %` lattice volume |
| silicon swell | Si expands up to about `280 %` by volume | `[PUBLICATION]` Obrovac M. N., Chevrier V. L., Chem. Rev. 114, 11444 (2014) |
| Si-C blend | `1 000 mAh/g`, `1.05 g/cm³`, `92 %` active, `22 %` swell | `[HYPOTHESIS]` scaffold Si-C class, gate ENR-22 |
| shipping silicon phone cell | `935 Wh/L` | `[PUBLICATION]` Enovix AI-1, Polaris Battery Labs, press release of 13 Jan 2026 |
| competing silicon-doped phone cell | about `835 Wh/L` | `[PUBLICATION]` the same release, `100 Wh/L` below AI-1 |

**The cross-check**. The S cell at `850 Wh/L` sits `9 %` under Enovix AI-1 at `935 Wh/L`. FINAL/21 expected a wall loss of `15-25 %`, which gives `700-795 Wh/L`. The model is more optimistic than that band. So the commitment is the `750 Wh/L` target, and the model excess is margin. `[DECISION]`

## 6 · The feedthrough, the vent and the fill

1. **The positive feedthrough**. A `1.10 x 1.10 x 0.90 mm` co-fired alumina insert sits in one corner. A platinum via crosses it. `[HYPOTHESIS]`
2. **The joint**. The insert is brazed into the can wall with an active-metal braze. Implant feedthroughs use the same alumina and platinum build. `[GENERAL]`
3. **The inner joint**. The aluminium tab bundle is welded to a titanium pad on the via. Aluminium never touches platinum directly. `[HYPOTHESIS]`
4. **The negative terminal**. The copper tab bundle is welded to the can floor in the opposite corner. The can is the negative pad.
5. **The pads**. Both terminals land on the back face. They meet the routing layer of the tile there.
6. **The fill port**. A `Ø0.15 mm` hole in the lid takes the electrolyte. Formation runs with the port open, so the formation gas leaves. A laser spot then seals the port. `[HYPOTHESIS]`
7. **The vent**. A laser-scored line in the back face leaves `15 µm` of steel. It opens near `0.3 MPa`. The gas goes to the back skin, away from the face and the eye. `[HYPOTHESIS]` gates ENR-15, ENR-16.

## 7 · The swelling and the stack pressure

1. **A `30 µm` face cannot hold the stack**. A clamped `9.19 mm` square plate of `30 µm` steel deflects about `1.8 mm` under `0.1 MPa`. `[GENERAL]` plate theory.
2. **So the tile holds the cell**. The can top bonds to the coil or spreader layer on the glass carrier. The can bottom bonds to the routing layer and its back frame.
3. **The compliance pad takes the swell**. A porous PTFE pad sits on the outer anode. It gives the stack pressure at assembly and compresses `70 %` at end of life.
4. **The can never grows**. The swelling allowance lives inside the `0.84 mm` cavity. The tile stack of FINAL/21 Section 21.2.7 stays `2.00 mm`. `[DECISION]`

## 8 · The fuse and the cell switch

Each cell meets the body bus through two parts in the tile routing layer. Details and proofs live in `02-PACK-ARCHITECTURE.md`.

| The part | The value | The tag |
|---|---|---|
| thin-film fuse | copper neck `2 x 20 x 200 µm`, `84 mΩ` | `[TREE]` `pack/network.py` |
| melt I²t | `1.76 x 10⁻⁴ A²s`, opens in under `1 µs` at `15-20 A` | `[TREE]` |
| hold | `0.30 A` with a `33 K` rise. The cell never exceeds `0.06 A` in service | `[TREE]` |
| steady fusing current | `1.69 A` | `[TREE]` |
| cell switch (TCM) | back-to-back NFET, `30 mΩ`, trips in `20 µs` above `0.25 A` | `[HYPOTHESIS]` custom WLCSP |

## 9 · The single-cell energy and safety

| The item | The value | The tag |
|---|---|---|
| stored energy, one cell | `192 J` (G), `235 J` (S) | `[TREE]` |
| compared to a LIR2032 coin cell | about `0.15 Wh`, or `530 J` | `[GENERAL]` |
| adiabatic rise of one tile, `0.53 g` | `362 K` (G), `443 K` (S) | `[TREE]` `pack/network.py` |

**The honest reading**. An internal short dumps the energy of one cell into one tile. The fuse stops the other `127` cells from feeding it. The cell's own energy still heats its tile. The vent, the ceramic separator and a flame-retardant electrolyte must hold the event inside the tile. Gate ENR-15 (nail test, one tile) carries it. `[HYPOTHESIS]`

## 10 · The open items of this sheet

1. The scaffold Si-C swell of `22 %` is the key input of the S variant. It needs a coin-cell dilatometry test. Gate ENR-22.
2. The `100 µm` overhangs need laser-cut electrodes with `±10 µm` placement. A `+0.10 mm` miss costs `3-5 %`.
3. A fast charge at `25 W` is `2.9-3.5 C` at these loadings. Graphite at `3.34 mAh/cm²` plates lithium below about `25 °C` at that rate. The charge plan of `04-ENERGY-BUDGET.md` handles it. Gate ENR-24.
4. The feedthrough insert needs a supplier able to co-fire `1.10 mm` alumina parts with a platinum via.
