# BUDLUM LEAF · ENERGY · 02 · THE 128-CELL PACK

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. Script: `pack/network.py`. Output: `out/network.txt`, `out/network.json`. Gates ENR-22, ENR-23, ENR-24, MEC-39, MEC-40, MEC-42.

## 1 · The topology: 1S128P on a distributed bus

**The decision**. All `128` cells sit in parallel on one body bus, `VBUS`. Each cell joins the bus through its own fuse and its own cell switch. The pack is one cell in series and `128` in parallel. `[DECISION]` this team.

| The pack value | G variant | S variant | The tag |
|---|---|---|---|
| voltage window | `3.00-4.45 V`, `3.87 V` nominal | `2.80-4.48 V`, `3.80 V` nominal | `[TREE]` |
| bus floor in service | `3.40 V` at the seat tile | `3.40 V` | `[DECISION]` |
| capacity at the target density | `1 525 mAh` at `600 Wh/L` | `1 942 mAh` at `750 Wh/L` | `[TREE]` |
| energy at the target density | **`5.90 Wh`** | **`7.38 Wh`** | `[TREE]` |
| energy at the model density | `6.83 Wh` | `8.36 Wh` | `[TREE]` |
| per quadrant at the target | `1.476 Wh` (ENR-22 asks `1.42`) | `1.845 Wh` (ENR-22 asks `1.80`) | `[TREE]` |
| pack DC resistance | about `38 mΩ` (`4.9 Ω / 128`) | about `35 mΩ` | `[TREE]` |

The cell volume is `128 x 76.88 mm³ = 9.84 cm³`. FINAL/21 used `9.56 cm³` with an `83 %` area factor. The real factor is `85.6 %`, so the body holds `5.90 Wh`, above the `5.7 Wh` of FINAL/21. `[TREE]`

### 1.1 Why parallel and not series

| The reason | Parallel 1S128P | A series string, for example 4S32P |
|---|---|---|
| a dead or shorted cell | `1/128` of the energy is lost | a string loses the cell, or the string |
| the balance | the OCV slope pulls cells together. The cell switch trims the rest | every series cell needs an active balancer |
| the fuse at a fault | `4.45 V` sustains no arc in a copper neck | `15-18 V` sustains an arc in a thin-film gap |
| a tile with a dead cell | its display still runs from the bus | the tile goes dark with the string |
| the quadrant swap | each quadrant is the same voltage, so it joins at once | a string that spans quadrants opens on a swap |
| the cost | higher current in the hinges | lower current |

The cost is the hinge current. The network solve of Section 3 shows that the hinge copper carries it. `[TREE]`

## 2 · How the cells cross the rotating hinges

1. **Each tile is a node**. Its cell, its fuse, its cell switch and its loads meet on a tile VBUS pad.
2. **Each hinge carries one VBUS line and one GND line**. Each line is `2 µm` copper, `0.45 mm` wide along the ribbon height, on the neutral plane.
3. **A liquid-metal channel runs in parallel**. An EGaIn channel of `50 µm x 0.40 mm` doubles each power line for the `41 %` mode.
4. **The line resistance**. Copper alone is `18.7 mΩ`. EGaIn alone is `14.7 mΩ`. Both together are `8.2 mΩ`. The solve uses copper alone, the worst case. `[TREE]`
5. **Inside a quadrant every hinge carries power**. The tiles form a `4 x 8` grid of nodes with `52` power hinges.
6. **Across a quadrant seam only the four crossing couplers carry power**. They join the four crossing tiles round `(0,0)` in a ring.
7. **Each crossing coupler passes the U_Q quadrant switch on both sides**. `10 mΩ` each. One ring link can fail, and the other three quadrants stay joined.

**What the hinge team must give**. A hinge ribbon of `1.2-1.5 mm` height must hold `0.90 mm` of power copper. That leaves `0.30-0.60 mm` for the display lanes and the telemetry line. This is an interface item with the hinge and display teams. Gate MEC-42.

The solve also ran with power on every seam coupler. The peak hinge current fell from `0.70 A` to `0.67 A` only. The ring of four is enough. `[TREE]`

## 3 · The network solve

The solve treats every tile as a node, every hinge as a loop resistance, and every cell as an OCV behind `4.9 Ω`. The B load sinks at the seat tile. It tries every edge tile as the seat and keeps the worst.

| The case | Seat voltage, worst | Cell current, min to max | Hinge max | Seam coupler max | Bus loss |
|---|---|---|---|---|---|
| video, body `1.35 W`, B `1.92 W` | `3.783 V` | `5.3-17.6 mA` | `0.287 A` | `0.135 A` | `23 mW` |
| outdoor video on 5G, body `4.24 W`, B `2.42 W` | `3.730 V` | `12.5-28.2 mA` | `0.367 A` | `0.174 A` | `38 mW` |
| peak, body `4.24 W`, B `4.50 W` | `3.646 V` | `15.2-45.2 mA` | `0.698 A` | `0.330 A` | `137 mW` |
| video, Q1 removed, seat on Q2 | `3.775 V` | up to `19.2 mA` | | `0.217 A` | |
| Qi2.2 `25 W` charge, G | | `35.3-48.9 mA` | `0.611 A` | `0.000 A` | |

All rows are `[TREE]`, G variant at `3.87 V`.

**The finding**. The cell resistance of `4.9 Ω` dwarfs the hinge resistance of `0.04 Ω`. So the bus loss stays under `1.6 %` even at the peak. `[TREE]`

**The imbalance**. Cells near the seat give up to `3.3` times the current of far cells. Section 4 shows how the cell switch evens this out.

## 4 · The balance

**The mechanism**. The cell switch can run its FET in the linear region. It adds resistance to a cell that lags the mean SOC. The gain is `2 x` the branch resistance per `1 %` of lag. `[DECISION]` this team.

| Discharge to empty, video, worst seat | No balance | Balance on |
|---|---|---|
| G, largest SOC spread during the run | `19.5 %` | **`2.2 %`** |
| S, largest SOC spread during the run | `19.7 %` | **`2.3 %`** |
| G, run time | `1.80 h` | `1.80 h` |

The balance costs no run time. It keeps every cell on the same cycle depth, so no cell ages first. `[TREE]`

**The swapped quadrant**. A fresh quadrant can sit `0.5 V` away from the body bus. U_Q joins it through its switch in current-limit mode. It holds the join current at `0.38 A`, which is `1 C` of the quadrant. Gate MEC-40.

## 5 · The cell monitor and the 4 x 32 multiplexer

### 5.1 The tile cell monitor, TCM, one per tile

| The function | The value | The tag |
|---|---|---|
| package | WLCSP, `0.9 x 0.7 x 0.15 mm`, in the routing layer | `[HYPOTHESIS]` custom |
| switch | back-to-back NFET, `30 mΩ`, charge pump gate drive | `[HYPOTHESIS]` |
| short-circuit trip | above `0.25 A`, either direction, for `20 µs` | `[DECISION]` |
| over-voltage / under-voltage | `4.47 V` (G) or `4.50 V` (S) / `3.00 V` (G) or `2.80 V` (S) | `[DECISION]` |
| over-temperature | on-die sensor, opens at `60 °C` cell, `36.2 °C` skin rule stays with U4 | `[DECISION]` |
| measurement | cell voltage `±2 mV`, switch current `±1 mA`, die temperature `±0.5 K` | `[HYPOTHESIS]` |
| interface | one-wire telemetry bus `TBUS`, `1 Mbit/s`, address set by the tile position | `[DECISION]` |
| quiescent | `1 µA` in storage, `8 µA` in service | `[HYPOTHESIS]` |

**The rule of local protection**. Every trip runs inside the TCM, with no bus traffic. A dead telemetry bus never disables a fuse or a trip. `[DECISION]`

### 5.2 The 4 x 32 multiplexer in the B ring

`HARDWARE/13` part 27 is a `4 x 32` channel multiplexer of `3.0 x 3.0 x 0.40 mm`. Analog wires from `128` cells cannot pass `12` bar leaves. So the channels are logical. `[DECISION]` this team.

1. **Four ports**. One port per quadrant, `Q1..Q4`. Each port addresses `32` TCMs.
2. **The path**. Sideband leaf `SBA` reaches the seat tile. The seat quadrant `TBUS` runs to its U_Q at the crossing. The four U_Q chips bridge to the other three quadrant buses.
3. **The scan**. One TCM report is `64` bits. One full scan of `128` cells takes about `8 ms` at `1 Mbit/s`. The multiplexer scans at `100 Hz`.
4. **The isolation**. U_Q cuts its quadrant segment when that segment stays stuck. The other three ports keep scanning.

### 5.3 The soft-short scan

1. Run it at rest on the charger, once per day.
2. Open one cell switch for one hour.
3. Read the OCV drift. A drift above `1 mV/h` marks a leak near `20 µA`.
4. Retire a leaking cell: keep its switch open and log its address in `U7`.
5. Step to the next cell. The body keeps `127` cells in service.

## 6 · The fault isolation, ENR-23

| The fault | The first actor | The time | What stays in service | The tag |
|---|---|---|---|---|
| internal short in one cell | its fuse opens at `15-20 A` | `0.45-0.79 µs` | `127` cells, every tile display | `[TREE]` |
| the same, if the fuse is slow | its TCM opens on reverse current | `20 µs` | `127` cells | `[DECISION]` |
| TCM FET fails short, then a cell fault | the fuse opens | under `1 µs` | `127` cells | `[TREE]` |
| TCM FET fails open | none needed | | `127` cells, the tile display on the bus | `[DECISION]` |
| one hinge VBUS line open | the grid reroutes | | all cells; each tile has `2-4` power hinges | `[TREE]` |
| VBUS shorted to GND in one tile | every TCM of the quadrant trips | `20 µs` | the other three quadrants, after U_Q opens | `[TREE]` |
| a cell over `60 °C` | its TCM opens | `1 ms` | `127` cells | `[DECISION]` |
| a soft short | the daily scan retires it | `24 h` | `127` cells | `[DECISION]` |
| a quadrant removed | U_Q opens before the seat breaks | `0.8 ms` | three quadrants | `[DECISION]` |
| telemetry bus stuck | U_Q cuts the segment | `10 ms` | all cells, with local trips | `[DECISION]` |

### 6.1 The numbers behind the fuse

| The check | The result |
|---|---|
| fault current into a shorted cell | `14.9 A` at a corner tile, `19.9 A` at a crossing tile |
| current in the next-worst cell during the fault | `0.34 A`, under the `1.69 A` steady fusing current |
| hinge current during a cell fault | `7.8 A` for under `1 µs` |
| hinge melt I²t against fuse melt I²t | `506` times larger, so the fuse always goes first |
| bus short in one tile | `29-55 A`, hinge peak `18.1 A` |
| hinge melt time at that peak | `0.27 ms`, against a `0.02 ms` TCM trip |

All rows are `[TREE]` outputs of `pack/network.py`. The coordination runs fuse first, cell switch second, hinge copper never.

**The pass condition of ENR-23**. The fuse opens and the other cells stay in service. The solve shows the other `127` cells stay under `0.34 A`. No other fuse or switch trips. `[TREE]` The hardware test is the gate.

## 7 · The charge through the body

1. **The coil**. Four Qi2.2 sector coils in series, one loop round the crossing. The coil ends land in the Q1 crossing tile. `[DECISION]` FINAL/21 21.2.6.
2. **The rectifier**. Every U_Q carries the rectifier die. Only the Q1 rectifier runs. It makes the `VHV` rail at `9-15 V`.
3. **The spread**. `VHV` crosses the four crossing couplers to the other U_Q chips.
4. **The charge**. Each U_Q runs a `3:1` switched-capacitor charger into its quadrant at `6.25 W` or less.
5. **The result**. At `25 W` in, `20.4 W` reach the cells. Each cell takes `35-49 mA`, `2.8 C` mean and `3.5 C` peak (G). Heat in the body is `5.8 W`. `[TREE]`
6. **The seat path**. A port part or the dock feeds `VHV` through leaves 5 and 8 of a seat field. A `VHV` spine of hinges runs from each seat tile to its crossing tile.

## 8 · The open items of the pack

1. The hinge ribbon must give `0.90 mm` of height to the two power lines. Interface with the hinge team. Gate MEC-42.
2. The `2 µm` copper carries `0.61 A` during a charge, `6.8 x 10⁴ A/cm²`. Electromigration at `40 °C` needs a test. Gate MEC-39.
3. The TCM is a custom part. A shipping protection IC with integrated FETs is the start. `[GENERAL]`
4. The heat of a `25 W` charge is `5.8 W`. The skin limit of `36.2 °C` sets the sustained rate. Gate ENR-24.
