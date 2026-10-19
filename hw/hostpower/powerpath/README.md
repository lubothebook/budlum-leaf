# BUDLUM LEAF · HOST POWER · POWER-PATH TEAM

**Revision L.6.1 (proposed) · 2026-10-19 · power-path team**. Charter: `hw/hostpower/BRIEF.md`. Every number below comes from a script in this directory, unless a tag says otherwise.

## 1 · What is here

| The file | The job |
|---|---|
| `common.py` | shared inputs: loads, cell data read from `hw/energy/out`, the open-circuit curve, the plot style |
| `tiers.py` | question 1: the Bare, Buffer and Full tiers, the capacitor technologies, the savings against Full |
| `powerpath.py` | question 2: the topology, the four modes, the time-stepped simulator and six scenarios |
| `celllife.py` | question 3: cell life, cycled against host-fed, the lithium and cobalt mass |
| `hosts.py` | question 4: the host classes H0 to H6 and where the capacity goes |
| `thesis_check.py` | question 5: pass or fail against the four conditions of BRIEF Section 5 |
| `run_all.py` | runs the five scripts in order |
| `out/*.txt`, `out/*.json` | the printed results and the data of every script |
| `out/*.png` | plots: `tiers_buffer`, `tiers_bare`, `pp_S1` to `pp_S6`, `celllife`, `hosts` |

## 2 · How to run

1. Install numpy, scipy and matplotlib.
2. Run `python3 hw/hostpower/powerpath/run_all.py`. It takes about one minute.
3. Read `out/thesis.txt` first, then the other `out/*.txt` files.
4. Read the hw/energy outputs only. The scripts never write outside `out/`.

## 3 · The power path

### 3.1 The topology, in the rail names of `hw/energy/03`

```
 host --> VHV (leaves 5, 8, or Q1 rectifier) --> D_HOST ideal diode (new) --> U_Q x4, 3:1 SC, 6.25 W each
                                                                                   |
 VBUS grid = the enabled micro cells = the bridge cell (TCM switches) <------------+
   |  tile nodes: the display power never crosses the bar
   +-- S_SEAT (leaves 2, 11) --> U4 --> VSYS_B = max(VBUS, B cell) by ideal diodes --> ring rails
 B cell --> U4 charger (from VBUS, 1 C) ;  B cell --> U7 always-on 1.8 V = the island rail (secure element, U4 ROM)
```

1. **D_HOST** is a new ideal diode at the U_Q input. It blocks any back-flow into a host. `[DECISION]` proposed
2. **The cell is the bridge, with no switch.** The enabled cells sit on VBUS. A host only pushes current into that node.
3. **The load switch** is S_SEAT plus the U4 ring cap of `0.40 W`. It parts the ring from VBUS when the bar lifts.
4. **No back-feed.** The B cell never feeds the body. The body never charges the B cell above its float.
5. **Dead pad.** VHV leaves stay at `0 V` until the `3 ms` challenge and the PD contract pass. The host gets no authority. `[DECISION]` BRIEF 3.3

### 3.2 The charge-current policy

| The item | The value | The tag |
|---|---|---|
| float band of the body cells | `45` to `55 %` SOC, the 40 to 60 % storage band | `[DECISION]` proposed |
| top-up current | `0.5 C` of the enabled cells, while SOC is under `55 %` | `[DECISION]` proposed |
| B cell float | `60 %`, charged by U4 at `1 C` (`37 mA`) | `[DECISION]` proposed |
| top-up to full | only on user request or a stated long gap, never by default | `[DECISION]` proposed |
| host power split | the host carries the load first. The top-up takes only the headroom | `[DECISION]` proposed |

### 3.3 The modes

| Mode | What runs | Pack current |
|---|---|---|
| `HOST_FEED` | the host carries the whole load. The cells float | `0` |
| `HOST_TOPUP` | the host carries the load and charges the cells to the float | up to `0.5 C` in |
| `BRIDGE` | no host. The cells carry the load by the shed ladder below | out |
| `ISLAND` | body dark, the ring on the B cell at `0.40 W` at most, then `U7` and U4 ROM only | `0` |

### 3.4 The thresholds and transitions

| The transition | The condition | The tag |
|---|---|---|
| host accepted | VHV at or over `9.0 V` for `20 ms`, after the `3 ms` challenge and the PD contract | `[HYPOTHESIS]` |
| host lost | VHV under `8.0 V`, or the sideband heartbeat missing for `100 µs` | `[HYPOTHESIS]` |
| `BRIDGE` to `HOST_TOPUP` | host accepted and pack SOC under `55 %` | `[DECISION]` proposed |
| `BRIDGE` to `HOST_FEED` | host accepted and pack SOC at or over `55 %` | `[DECISION]` proposed |
| `HOST_FEED` to `HOST_TOPUP` | pack SOC under `45 %` | `[DECISION]` proposed |
| `HOST_TOPUP` to `HOST_FEED` | pack SOC at or over `55 %` | `[DECISION]` proposed |
| host modes to `BRIDGE` | host lost. The pack is already on VBUS, so no gap opens | `[DECISION]` proposed |
| `BRIDGE` shed ladder | over `30 %`: cell limit. `30` to `18 %`: delta class. `18` to `12 %`: safe screen | `[DECISION]` proposed |
| `BRIDGE` to `ISLAND` | pack at `12 %`: close the session and save state. Floor `10 %`, or no cells on the bus | `[DECISION]` proposed |
| `ISLAND` to `BRIDGE` | cells back on the bus and SOC over `15 %`. A host takes it to a host mode | `[DECISION]` proposed |
| ring on the B cell | B cell SOC over `15 %`. Under it, the B cell serves `U7` and U4 ROM only | `[DECISION]` proposed |

### 3.5 The simulator

`powerpath.py` steps an adaptive `dt` from `0.2 ms` near an event to `0.5 s` at rest. It solves the VBUS node for parallel cell groups, a constant-power load and the host current. It tracks the pack SOC, the B cell SOC and the rails `VHV`, `VBUS`, `VSYS_B`, `V_BCELL` and `1V8_AON`. The island rail drops if the B cell voltage falls under `2.3 V`.

## 4 · The results

### 4.1 Tier sizing (question 1)

**The cells.** The S cell at `750 Wh/L` holds `0.0577 Wh`, `14.8 mAh`, `0.114 g`, `4.36 Ω`. Cells floated at `60 %` give `0.485` of their energy down to a `10 %` reserve. Topped to `100 %` they give `0.911`. `[TREE]`

Least cells of the `128`, S cell, floated at `60 %`. The letter marks the limit: `i` is the `3 C` rate cap, `e` is energy. A dash means more than `128`.

| Load, W at VBUS | `0.1 s` | `1 s` | `3 s` | `30 s` | `5 min` | `30 min` |
|---|---|---|---|---|---|---|
| standby `0.061` | 1 | 1 | 1 | 1 | 1 | 2 e |
| safe screen `0.219` | 2 i | 2 i | 2 i | 2 i | 2 i | 5 e |
| delta session `2.24` | 14 i | 14 i | 14 i | 14 i | 15 i | 41 e |
| video `3.65` | 22 i | 22 i | 22 i | 23 i | 24 i | 67 e |
| outdoor `7.5` | 46 i | 46 i | 46 i | 46 i | 48 i | - |
| peak `8.7` | 53 i | 53 i | 53 i | 53 i | 56 i | - |

1. **The reading.** A gap under 5 min is a power problem, not an energy problem. The `3 C` cap sets the count. `[HYPOTHESIS]` for the cap.
2. **The cap decides.** At `3 s` the delta class needs `14`, `9` or `6` cells at `3`, `5`, `10 C`. The peak needs `53`, `33`, `22`.
3. **Topped cells need fewer.** The delta class for `30 min` needs `41` cells floated and `23` cells topped. The topped case hits the `3.40 V` floor.
4. **The BRIEF range of `0.3` to `1.5 Wh`** is `6` to `27` S cells. It carries the delta class for `5 min`. It misses the `30 min` class by `58 %`.
5. **The quadrant swap.** Three quadrants must carry the `3 s`. The delta class then needs `20` cells in all, `5` per quadrant. The peak needs `72`.

**Tiles that must hold a cell, per Buffer duration.** S cell, floated, spread over four quadrants so that three carry a `3 s` swap. The count is the least cells times `4/3`, rounded up to a multiple of `4`.

| The duration | Delta session `2.24 W` | Video `3.65 W` | Peak `8.7 W` |
|---|---|---|---|
| up to `3 s` | `20` tiles | `32` tiles | `72` tiles |
| `5 min` | `20` tiles | `32` tiles | `76` tiles |
| `30 min` | `56` tiles | `92` tiles | more than `128` |

The G cell at `600 Wh/L` needs `20` to `25 %` more cells in every row. `out/tiers.txt` has the full tables.

**Full.** All `128` cells carry the delta class for `2.98 h` from `100 %` and `1.59 h` from the `60 %` float. They carry the peak for `0.76 h` and `0.40 h`. `[TREE]`

**Bare, capacitor technologies, from published figures.**

| The technology | Usable Wh/L | ESR times volume | The source |
|---|---|---|---|
| EDLC, large cell | `4.8` | `0.11 Ω·cm³` | `[PUBLICATION]` Maxwell BCAP3000 P270 datasheet, `3000 F`, `2.7 V`, `0.23 mΩ`, `475 g` |
| EDLC, thin chip | `1.7` | `1.2 Ω·cm³` | `[PUBLICATION]` Seiko CPH3225A, `11 mF`, `3.3 V`, `0.9 mm` thick. The `160 Ω` ESR is unconfirmed |
| lithium-ion capacitor | `11.3` | `9.4 Ω·cm³` | `[PUBLICATION]` Taiyo Yuden LIC1030RS3R8206, `20 F`, `3.8` to `2.2 V`, `4 Ω` max |
| thin solid-state cell | `21` | `15.5 Ω·cm³` | `[PUBLICATION]` ST EnFilm EFL700A39, `0.7 mAh`, `3.6` to `4.2 V`, `0.2 mm` thick, `10 mA` pulse |
| micro cell, for scale | `750` to `850` | | `[TREE]` hw/energy/01 |

Densities are my derivation from the datasheet figures, with the window of the second column. A converter at `0.90` and a cut at half the rated voltage apply to the EDLC. `[HYPOTHESIS]`

**Does a Bare store fit the `0.24 mm` margin?** The room is half of the `12 800 mm²` body. At `0.24 mm` that is `1.54 cm³`. The answer is no, with one exception.

| The load and gap | EDLC, large cell | Thin solid-state | The verdict |
|---|---|---|---|
| safe screen `0.219 W`, `3 s` | `0.06 cm³` | `1.76 cm³` | the EDLC fits the volume and misses the thickness. The thin cell misses by `15 %` |
| delta session `2.24 W`, `3 s` | `0.60 cm³` | `18 cm³` | the EDLC misses the thickness. The thin cell is `12` times too large |
| peak `8.7 W`, `3 s` | `2.32 cm³` | `70 cm³` | the best EDLC misses the volume by `51 %` and the thickness |
| standby `0.061 W`, `5 min` | `1.19 cm³` | `0.77 cm³` | only the thin cell fits both. It cannot carry a screen |

1. **Thickness decides.** The thinnest published EDLC found is `0.9 mm`. The margin is `0.24 mm`. If the coil takes `0.20 mm` of it, only `0.04 mm` is free.
2. **Bare needs cell volume.** A `3 s` safe screen takes `3` tiles of chip EDLC.
3. **The peak by capacitor is out.** A `3 s` peak takes `31` tiles of EDLC cell volume. `0.1 s` takes `9`. Ceramics need `13 cm³` for `0.1 s`. `[HYPOTHESIS]`
4. **Cells win beyond `1 s`.** `2` cells carry the safe screen for `5 min`. A capacitor needs `2.5` to `12 cm³` for the same job.

**The savings against Full** (`128` cells, `7.38 Wh`, `14.6 g` of cells).

| The tier | Cells | Energy | Cell mass saved | The thickness |
|---|---|---|---|---|
| Bare | `0` | `0` | `14.6 g`, `100 %` | `1.10 mm` body, `0.90 mm` saved |
| Buffer, delta `5 min` | `15` to `20` | `0.9` to `1.2 Wh` | `12.3` to `12.9 g`, `84` to `88 %` | `2.00 mm` unless the cells leave the body |
| Buffer, peak `3 s` | `53` to `72` | `3.1` to `4.2 Wh` | `6.4` to `8.5 g` | `2.00 mm` unless the cells leave the body |
| Full | `128` | `7.38 Wh` | `0` | `2.00 mm` |

A tile with no cell is `1.10 mm` thick. A flat body is `1.10 mm` thick only if every cell sits outside it, for example in the B module. `[TREE]` stack of FINAL/21 21.2.7.

### 4.2 The power path simulation (question 2)

All runs use S cells, `20` Buffer cells (`5` per quadrant) unless a row says otherwise.

| The scenario | The result |
|---|---|
| S1: desk dock `60 s`, walk `4 min` at `2.24 W`, vehicle with a `0.9 s` cranking dropout and a `0.35 s` PD re-contract | Buffer: VBUS minimum `3.48 V`, pack `35` to `22 %` on the walk. Bare: session closes `3 s` after the lift |
| S2: host dips to `6 V` for `150 ms` and to `0 V` for `2 s` | Buffer: VBUS minimum `3.72 V`. No collapse. Mode `BRIDGE` for `2.2 s` in all |
| S3: host vanishes in a video session, no new host | Buffer closes the session at `1 601 s` and enters `ISLAND`. Full walks the ladder for `2.5 h` and ends at `12.8 %` |
| S4: hot swap of Q3, B module on the Q3 seat, host on Q1 | VBUS minimum `3.72 V`. The ring runs `3 s` on the B cell. The budget in hw/energy/03 is `0.33 mWh` |
| S5a: quadrant swap, no host, cells spread | VBUS minimum `3.72 V`. No mode change |
| S5b: quadrant swap, no host, all cells in the removed quadrant | The body bus is lost for `3 s`. Place Buffer cells in all four quadrants |
| S6: `5 W` pad against outdoor video `7.5 W` for `15 min` | Full assists with no fault, SOC `55` to `46 %`. Buffer drops under the `3.40 V` floor for `12 s` |

**The island rail never dropped in any of the `13` runs.** `1V8_AON` stayed at `1.80 V`. `[TREE]` `out/powerpath.txt`

**The island run time is short.** A B cell floated at `60 %` runs `U7` and U4 ROM alone for `2.5 h`. From `100 %` it runs `4.4 h`. The budget is `0.025 W` at `1.8 V`, `0.031 W` at the cell. `[HYPOTHESIS]`

### 4.3 Cell life (question 3)

**The model.** `[PUBLICATION]` Schmalstieg, Käbitz, Ecker and Sauer, J. Power Sources 257 (2014) 325-334, fitted to a Sanyo UR18650E (NMC and graphite, `2.05 Ah`). I took the constants and Eq. 3 to 6 from Lee, Bjurek, Hagman, Li and Zou, IFAC-PapersOnLine 56(2) (2023) 6624-6629, `doi:10.1016/j.ifacol.2023.10.362`. I did not read the original paper.

```
C_lost = alpha * T^0.75 + beta * sqrt(Q)
alpha  = (7.543e6 * Vmean - 23.75e6) * exp(-6976 / theta)      T in days, theta in K
beta   = 7.348e-3 * (Vrms - 3.667)^2 + 7.600e-4 + 4.081e-3 * dDoD      Q in Ah
```

**The transfer to the Leaf cell is a hypothesis.** The micro cell is LiCoO2 at `4.45 V`, not NMC at `4.2 V`. I apply the model by SOC and count one cycle of the micro cell as one cycle of the `2.05 Ah` cell. The uncertainty is a `2` times band on alpha and on beta, from the 10th to the 90th percentile. A `1` to `2` times factor covers the `100 %` dwell. `[HYPOTHESIS]`

| The case | Years to `80 %`, `25 °C` | At `33 °C` | Monte Carlo P10, P50, P90 |
|---|---|---|---|
| A: cycled daily `100` to `20 %`, `6 h` at `100 %` | `1.8` | `1.3` | `0.3`, `0.8`, `2.4` |
| A2: cycled daily, no dwell at `100 %` | `2.1` | `1.5` | `0.7`, `1.9`, `4.7` |
| B1: host-fed Full, float `50 %`, `6` bridges a day of `4 min` | `13.4` | `6.3` | `5.6`, `13.0`, `29.5` |
| B2: host-fed Buffer `20` cells, the same bridges | `7.7` | `4.3` | `3.2`, `6.9`, `15.6` |
| B3: host-fed Buffer `20` cells, `2` bridges of `2 min` | `12.7` | `6.1` | `5.4`, `12.2`, `27.4` |
| C: host-fed Full, charger holds `100 %` | `4.9` | `2.5` | `1.1`, `2.5`, `6.3` |

1. **The gain.** A host-fed Full cell floating at `50 %` lives `7.2` times as long as a cell cycled daily. The Monte Carlo medians give `16` times.
2. **The float is the gain.** The same host-fed cell held at `100 %` by the charger lives `4.9` years. Float policy is a firmware duty.
3. **A small Buffer works hard.** `20` cells do all the bridging, so they see `0.78` cycles a day. They live `7.7` years, not `13.4`.
4. **Heat counts.** Life at `33 °C` is about half of life at `25 °C`. The skin limit of `36.2 °C` is the cell limit too.
5. **The EU story.** Regulation (EU) 2023/1670 counts cycles: `800` cycles at `80 %`. `[PUBLICATION]` The model gives `630` to `720` full cycles for a 2013 NMC cell.
6. **A host-fed Leaf is calendar-limited.** It reaches `800` cycles after `13` years or more. The cycle count is the wrong figure for it.
7. **The legal class** of the Leaf under 2023/1670 is a legal reading, not a number.

**Lithium and cobalt, by stoichiometry** `[GENERAL]`. An S cell holds `5.9 mg` of lithium (`31 mg` Li2CO3 equivalent) and `49 mg` of cobalt. Full holds `0.75 g` of lithium and `6.3 g` of cobalt.

| The tier | Lithium saved | Li2CO3 equivalent saved | Cobalt saved |
|---|---|---|---|
| Buffer `20` cells | `0.64 g` | `3.4 g` | `5.3 g` |
| Buffer `52` cells | `0.45 g` | `2.4 g` | `3.8 g` |
| Bare | `0.75 g` | `4.0 g` | `6.3 g` |

The saving is small per Leaf. Per million Leaf units, Buffer `20` saves `635 kg` of lithium and `5.3 t` of cobalt.

### 4.4 Host classes (question 4): where does the capacity go

Offered power is on VHV. "Eff" is the host-side chain. The energy columns are host Wh per hour of Leaf at the bus load, path loss included. The 8.7 W peak is `9.0 W` on VHV.

| Host | Offered | Eff | Carries `8.7 W` | Carries the `25 W` case | Wh per hour, delta / video / peak | Interface heat at `8.7 W` |
|---|---|---|---|---|---|---|
| H0 wall dock | `25 W` | `0.89` | yes | yes | `2.8` / `4.4` / `10.3` | `0.28 W` |
| H1 dock pack `20 Wh` | `25 W` | `0.89` | yes | yes | `2.8` / `4.5` / `10.4` | `0.28 W` |
| H2 desk USB-C PD | `7.5` to `100 W` | `0.88` | yes | yes at `15 V` | `2.6` / `4.3` / `10.2` | `0.28 W` |
| H3 vehicle `12 V` | `30` to `100 W` | `0.88` | yes | yes | `2.6` / `4.3` / `10.2` | `0.28 W` |
| H3 vehicle `24 V` | `30` to `100 W` | `0.87` | yes | yes | `2.7` / `4.3` / `10.3` | `0.28 W` |
| H4 industrial `24 V` | `25 W` | `0.92` | yes | yes | `2.5` / `4.1` / `9.8` | `0.28 W` |
| H4 PoE type 2 | `22.9 W` | `0.87` | yes | no, `2.1 W` short | `2.7` / `4.3` / `10.3` | `0.28 W` |
| H4 PoE type 3 | `45.9 W` | `0.87` | yes | yes | `2.7` / `4.3` / `10.3` | `0.28 W` |
| H5 worn bank or belt | `18 W` | `0.86` | yes | no, `7 W` short | `2.7` / `4.4` / `10.4` | `0.29 W` |
| H6 Qi pad `5 W` | `5 W` | `0.80` | no, `4 W` short | no | `3.6` / `5.8` / `13.8` | `0.76 W` |
| H6 Qi2 pad `15 W` | `15 W` | `0.80` | yes | no | `2.9` / `4.7` / `11.2` | `0.76 W` |
| H6 Qi2.2 pad `25 W` | `25 W` | `0.80` | yes | yes | `2.9` / `4.7` / `11.2` | `0.76 W` |

1. **The interfaces.** H0, H1 use the 12 bar pads. H2 to H5 use the port part on a seat. H6 uses the Q1 rectifier.
2. **The clamp is outside the Leaf.** The PD adapter or the cradle stage owns the vehicle and industrial clamps. The Leaf sees a PD output of `20 V` at most.
3. **The `12 V` window.** Run `9` to `16 V`. Cranking minimum `6` to `10.5 V`. Load dump `35 V` suppressed, `79` to `101 V` not. `[PUBLICATION]` ISO 16750-2, secondary summary.
4. **The `24 V` window.** Run `16` to `32 V`. Cranking minimum `10` to `22 V`. Load dump `58 V` suppressed, `151` to `202 V` not. `[PUBLICATION]` same source.
5. **The load dump energy** into a clamp is `61` to `145 J` at `12 V`. At `24 V` it is `255` to `275 J`. `[GENERAL]`
6. **A cranking dropout** is a gap of `0.1` to `3 s` at the Leaf. The cell bridges it in S1.
7. **PoE** carries `1.5 kV` isolation by its standard. `[PUBLICATION]` IEEE 802.3 PD classes, `12.95`, `25.5`, `51`, `71.3 W` at the PD. The `25 W` case needs Type 3.
8. **A `5 V` host has no `3:1` ratio.** U_Q needs a bypass mode at `0.79` efficiency. The Leaf heat is then about `2.3 W` at `8.7 W`. `[HYPOTHESIS]` Open issue 2.
9. **Qi heats the Leaf `2.7` times more than contact** at `8.7 W`: `0.76 W` against `0.28 W`. The thermal team owns the number. `[HYPOTHESIS]`

**How long a host battery runs the Leaf.**

| The host battery | Delivered to VHV | Standby | Delta `2.24 W` | Video `3.65 W` | Peak `8.7 W` |
|---|---|---|---|---|---|
| H1 dock pack `20 Wh`, dock AP off | `17.7 Wh` | `60 h` | `7.0 h` | `4.4 h` | `1.9 h` |
| H1 dock pack, dock Wi-Fi AP and `60 GHz` on | `17.7 Wh` | | `3.0 h` | | |
| H5 worn bank `18.5 Wh` | `15.2 Wh` | `240 h` | `6.6 h` | `4.0 h` | `1.7 h` |
| Leaf Full cell `7.38 Wh`, run to empty, for scale | `7.1 Wh` | `116 h` | `3.2 h` | `1.9 h` | `0.8 h` |

**The honest reading.** The capacity moved to the dock pack and the bank, and it grew. A `20 Wh` pack runs the delta session `7.0 h`, `2.2` times the Leaf Full cell. With the dock radios on, it runs `3.0 h`, the same as the Leaf alone. The dock radios use `3.7 W` at idle. A bank can shut off under `50` to `100 mA`, so standby needs the cell. `[HYPOTHESIS]`

Of `20 Wh` nominal, `17.1 Wh` reaches the Leaf bus. The steps are the usable window `0.95`, the pack `0.97`, the dock stage `0.96` and U_Q with the leaves `0.97`. `[HYPOTHESIS]`

### 4.5 The thesis check (question 5)

| The condition | The test | The verdict |
|---|---|---|
| 1 power | peak `8.7 W` plus top-up, hosts H0 to H4, H6 Qi2 and Qi2.2, H5 | pass. The smallest margin is `+2.2 W` (Qi2 `15 W`, Full top-up) and `+5.2 W` (H5) |
| 1 power | H6 Qi `5 W` | fail by `6.8 W` with Buffer top-up. A pack assist carries Full `15 min`, not Buffer |
| 1 power | the `25 W` port part case | fail on PoE type 2 by `2.1 W`, on the worn bank by `7 W`, on the `5 W` and `15 W` pads |
| 4 continuity | energy form `E_buffer >= 8.7 W x 3 s` for `20` cells | pass by a factor of `77` |
| 4 continuity | the same, as power: `20` cells at `3 C` carry `3.1 W` | fail by `5.6 W`. The peak needs `53` cells at `3 C` |
| 4 continuity | walk of `5 min` at the delta class | pass with `15` cells, `0.86 Wh`, inside the BRIEF range |
| 4 continuity | `30 min` at the delta class | fail floated: `41` cells, `2.36 Wh`, over the range by `58 %`. Pass topped: `23` cells |
| 4 continuity | Bare store, `3 s` at the peak, in the `0.24 mm` margin | fail. The best EDLC needs `2.32 cm³` against `1.54 cm³`, and it is too thick |
| 4 continuity | Bare store, `3 s` safe screen, to close a session | pass, with `1` to `3` tiles of cell volume. It fails inside the margin |
| 4 continuity | island rail over `13` runs | pass. `1V8_AON` never dropped |
| 4 continuity | quadrant swap with no host | pass with cells spread. Fail with cells in one quadrant: `3 s` of dark body |
| 2 heat | interface heat at `8.7 W` | not mine to rule. Contact `0.28 W`, Qi `0.76 W` |
| 3 trust | host before the handshake | by design: VHV stays at `0 V`. The simulator never takes a host before the proof |

**The thesis damage, said first.**

1. The Buffer of `0.3` to `1.5 Wh` does not ride the `8.7 W` peak. It rides the delta class (`2.24 W`).
2. The peak needs `53` cells at `3 C`, about `3.1 Wh`, `2.1` times the top of the BRIEF range.
3. Bare does not fit the `0.24 mm` margin. It needs `3` tiles of cell volume to close a session, and a `0.1 s` peak needs `9`.
4. A host that offers under `9 W` on VHV does not carry the peak. That is every `5 W` pad. A bank of `18 W` carries it.
5. A Buffer ages faster than Full, because the few cells do all the bridging. The gain from float holds only with the float policy.
6. The island rail holds, but `2.5 h` on the B cell is not days.

**What holds.** The delta class bridges any gap up to `5 min` with `15` to `20` cells. Every host from H0 to H4 carries the peak. A host-fed Full cell lives `7` times longer than a cycled one.

## 5 · The open issues

1. **The margin is `0.24 mm` or `0.04 mm`.** FINAL/21 21.2.7 lists the coil as its own `0.20 mm` layer. Item 4 of 21.2.6 says the coil takes `0.20 mm` of the margin. One of them is wrong.
2. **The U_Q input window.** A fixed `3:1` ratio needs VHV near `3 x VBUS`, `11.6 V` at the float. PD fixed levels are `5`, `9`, `15`, `20 V`. U_Q needs a hybrid mode or the host needs PPS.
3. **A `5 V` host** needs a bypass in U_Q. It loses `21 %` as heat in the body.
4. **The C-rate cap of `3 C`** is my assumption. The Buffer count scales with it: `53`, `33`, `22` cells at `3`, `5`, `10 C` for the peak.
5. **The micro cell DCIR** of `4.4` to `4.8 Ω` is a model value. It sets the bus sag under the `3.40 V` floor.
6. **The aging model** was fitted to NMC at `4.2 V`. The `4.45 V` LiCoO2 micro cell needs its own data. I did not read the original paper.
7. **Published inputs I checked only in part.** The Seiko ESR comes from a distributor. The Taiyo Yuden part is marked non-preferred. The ST sheet differs by revision: `0.20` or `0.22 mm`.
8. **ISO 16750-2 values** come from search summaries, not from the standard. USB PD, IEEE 802.3, Qi and IEC 61131-2 values are `[GENERAL]`.
9. **Chain state** is not modelled. The continuity team owns the claim that a gap never loses chain state.
10. **The island rail** is fed from the B cell by a regulator at `0.80`. A `1.8 V` linear regulator would give `0.46`. Feeding U7 from VSYS_B spares the B cell.
11. **Bare needs a B module** with its B cell. A body alone has no island rail.
12. **Legal.** A Buffer shrinks the removable battery of `hw/energy/06`. Whether Article 11 still reads the same is for a lawyer.
13. **The host chain efficiencies** are `[HYPOTHESIS]`. Only the dock `0.96` comes from `hw/dock/params.py`.
14. **Python 3.14 here had no numpy.** The run needs a path to numpy, scipy and matplotlib.

## 6 · The proposed gates

The Program Lead renumbers these when the teams merge.

| Gate | What it measures | The pass condition |
|---|---|---|
| HST-1 | a Bare store: `3 s` of the safe screen `0.219 W` | the store takes at most `3` tiles of cell volume and VBUS stays at or over `3.40 V` |
| HST-2 | Buffer group power: `15` micro cells, `2.24 W` for `5 min` from `60` to `10 %` | VBUS at or over `3.40 V`, rate at or under the measured cap, no cell over `45 °C` |
| HST-3 | the micro cell pulse rate: `10 s` pulse at `3`, `5` and `10 C` | the rate the BRIDGE cap uses holds the `3.40 V` floor. Else the cap is the delta class |
| HST-4 | U_Q host window: VHV `9`, `12`, `15 V` and `5 V` | VBUS `3.40` to `4.48 V` at `0.93` efficiency or better. A `5 V` host stays under `1.0 W` of body heat |
| HST-5 | micro cell cycles and storage: `800` cycles at `80 %`, `1 000 h` at `3.86 V` and `33 °C` | `800` cycles met, and the fitted alpha within `2` times of the model |
| HST-6 | float policy over `30` days on a host | pack SOC `45` to `55 %`, B cell `60 %`, no excursion over `70 %` |
| HST-7 | island rail: `1 000` random host drops and brownouts, `100` quadrant swaps | `1V8_AON` never under `1.75 V`. The B cell island-only run is at least `2.5 h` |
| HST-8 | hand-over: S1 and S2 on a bench, `100` runs | VBUS never under `3.40 V`, no mode flicker over `3` per event |
| HST-9 | Buffer placement: no-host quadrant swap with cells spread | VBUS at or over `3.40 V` for the whole `3 s` at the delta class |
| HST-10 | host classes: H0 to H6 each carry `8.7 W` for `10 min` | table of this README within `10 %`, and no host gains access to VBUS before the proof |
| HST-11 | vehicle: cranking and load dump A and B with a Leaf on the cradle | VHV never over `20 V`. The Leaf holds the session through the dropout |
| HST-12 | interface heat at `8.7 W`, contact and Qi, for the thermal team | contact at or under `0.4 W`, Qi at or under `1.0 W`, skin at or under `36.2 °C` |
| HST-13 | the B cell float and island budget | `U7` and U4 ROM at or under `0.031 W` at the cell, measured |

## 7 · The sources

1. `[PUBLICATION]` Schmalstieg, Käbitz, Ecker, Sauer. J. Power Sources 257 (2014) 325-334. Constants taken through Lee et al. below.
2. `[PUBLICATION]` Lee, Bjurek, Hagman, Li, Zou. IFAC-PapersOnLine 56(2) (2023) 6624-6629, `doi:10.1016/j.ifacol.2023.10.362`, open text at research.chalmers.se.
3. `[PUBLICATION]` Maxwell BCAP3000 P270 datasheet `3003279-EN.3`, and its product matrix for the size.
4. `[PUBLICATION]` Taiyo Yuden LIC1030RS3R8206 device page, ds.yuden.co.jp.
5. `[PUBLICATION]` ST EnFilm EFL700A39 datasheet DocID 17370. Seiko Instruments CPH3225A datasheet.
6. `[PUBLICATION]` ISO 16750-2:2023 Tables 11 to 13, as summarised by the Microchip note DS00006186.
7. `[PUBLICATION]` Regulation (EU) 2023/1670, Annex II, as in `hw/energy/06`.
