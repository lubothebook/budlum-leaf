# BUDLUM LEAF · ENERGY · 03 · THE POWER TREE, THE 12 BAR LEAVES AND THE DEAD PAD

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. Scripts: `pack/bar_pins.py`, `pack/network.py`. Output: `out/bar_pins.txt`. Gates MON-16, MON-21, MON-23, ENR-19, ENR-23, ENR-24, SW-20.

## 1 · The power tree

```
 CHARGE INPUTS                         BODY (128 tiles, 2.00 mm)                         B MODULE (ring)
 Qi2.2 25 W --4 sector coils--> U_Q(Q1) rectifier --VHV 9-15 V--+
 port part  --leaves 5,8 VHV--> seat field --VHV spine---------+--> U_Q x4: 3:1 SC charger, 6.25 W each
 dock pads  --leaves 5,8 VHV--> seat field --VHV spine---------+          |
                                                                          v
             128 cells --fuse--TCM switch--> tile node ===== VBUS grid, 1S128P, 3.40-4.48 V
                                                |                     |
                          tile loads, from the tile node:             | seat tile switch S_SEAT
                          micro-LED drivers, row/column address,      | leaves 2,11 VBUS, 1,12 GND
                          AgNW touch front end, hinge-angle sensor,   v
                          TCM, U_Q (crossing tiles)              U4 power path --- B cell 0.14 Wh
                                                                      |
                                       +------+------+------+-------+-------+-------+-------+
                                       0.75 V 1.0 V  1.8 V  ET PA   2.8/1.1 ELVDD  flash  class-D
                                       U1 U6  U5 core IO    U5 5G   camera  rear   boost  speaker,
                                       U2A/B  frame         front   AF/OIS  AMOLED        jack amp
                                       mux 27 store         end
                                       U7 always-on LDO from the B cell (the wallet answers with no network)
```

### 1.1 Every load and its rail

| The load | Where | The rail | The source | The tag |
|---|---|---|---|---|
| micro-LED drivers, `200 x 200` px per tile | each tile | VBUS, `3.40 V` floor for the green sinks | tile node | `[DECISION]` |
| row and column address drivers | each tile | VBUS and a local `1.0 V` buck per four tiles | tile node | `[HYPOTHESIS]` |
| AgNW touch front end | each tile cap | `1.8 V` from the four-tile buck | tile node | `[HYPOTHESIS]` |
| hinge-angle sensor, seam strip, thermistor | each tile | `1.8 V` | tile node | `[HYPOTHESIS]` |
| TCM, one per tile | routing layer | the cell itself | the cell | `[DECISION]` |
| U_Q, one per quadrant | crossing tile | VHV in charge, VBUS at rest | crossing node | `[DECISION]` |
| seat controller SC, one per edge | seat tile | VBUS, or the sideband in a dead-body boot | seat node | `[DECISION]` |
| `U1` TCON and compositor, `U6` decoder and `16 MB` store | ring | `0.75 V` core, `1.8 V` IO | U4 | `[HYPOTHESIS]` |
| `U2A` Wi-Fi 7 and BT 6.0, `U2B` `60 GHz` and UWB | ring | `0.75 V`, `1.8 V`, PA from VSYS_B | U4 | `[HYPOTHESIS]` |
| `U5` 5G modem | ring | `1.0 V` core, envelope-tracking PA supply `0.5-4.5 V` | U4 | `[HYPOTHESIS]` |
| `U7` secure element, wallet | ring | always-on `1.8 V` LDO from the B cell | B cell | `[DECISION]` |
| `U8` IMU, part 27 multiplexer | ring | `1.8 V` | U4 | `[DECISION]` |
| `50 MP` sensor, AF, stabiliser | ring | `2.8 V` analog, `1.1 V` digital, VSYS_B for the actuators | U4 | `[HYPOTHESIS]` |
| rear round AMOLED | ring | ELVDD `4.6 V`, ELVSS `-2.4 V` | U4 | `[HYPOTHESIS]` |
| two-tone flash | ring | boost, `1.5 W` pulse limit | U4 | `[DECISION]` |
| speaker, `3.5 mm` jack, two mics | ring | class-D from VSYS_B, charge-pump headphone amp, `1.8 V` | U3 and U4 | `[HYPOTHESIS]` |

**The rule of local supply**. The display power never crosses the bar. Each tile draws its own light from its own node. Only the ring loads cross the `12` leaves. `[DECISION]`

### 1.2 The B power path, U4

1. **VSYS_B** is the larger of VBUS from the leaves and the B cell, through ideal diodes.
2. **The B cell charges from VBUS** at `1 C`, `37 mA`, while the bar is seated.
3. **The body carries the peaks**. A `4.50 W` peak from the B cell alone is `33 C`. U4 draws peaks from VBUS only. `[TREE]` `budget/runtime.py`
4. **No back-feed into the body**. The ideal diode blocks the B cell from the body bus. A `0.14 Wh` cell cannot help a `5.9 Wh` body.
5. **Islanded mode**. With the bar off the seat, U4 caps the ring at `0.40 W`. The B cell carries that for `19.7 min`. `[TREE]`

## 2 · The 12 leaves of the seat field

The field is `12` gold leaves at `0.80 mm` pitch, `9.6 mm` long, over one seat tile. `[DECISION]` FINAL/21 21.3.2. Each leaf is `18 mΩ`. The rating is `1.5 A` per leaf, continuous. `[HYPOTHESIS]` gate MON-16.

| Leaf | Net | The duty | Leaf length |
|---|---|---|---|
| 1 | GND | ground, mates first and breaks last | long, `+0.25 mm` |
| 2 | VBUS | body bus `3.40-4.48 V`, the B supply | short |
| 3 | L0+ | high-speed lane 0, positive | middle |
| 4 | L0- | high-speed lane 0, negative | middle |
| 5 | VHV | charge rail `5-20 V`, port part or dock | short |
| 6 | SBA | sideband A: dead-pad handshake, identity, cell telemetry | middle |
| 7 | SBB | sideband B: tile control, hinge angles, Qi status | middle |
| 8 | VHV | charge rail `5-20 V` | short |
| 9 | L1- | high-speed lane 1, negative | middle |
| 10 | L1+ | high-speed lane 1, positive | middle |
| 11 | VBUS | body bus | short |
| 12 | GND | ground, long leaf | long, `+0.25 mm` |

**The mirror rule**. The bar seats on the front or the back face, so leaf `k` lands on pad `13 - k`. GND, VBUS and VHV mirror onto themselves. L0 and L1 swap, and the lane crossbar in `U1` undoes it. SBA and SBB swap, and the handshake finds the one that answers. `bar_pins.py` passes the check. `[TREE]`

**The four seat fields**. One seat tile per edge, one per quadrant: `(3,0)` top in Q1, `(7,7)` right in Q2, `(0,8)` left in Q3, `(4,15)` bottom in Q4. Each field serves the front and the back seat, so `8` seats in all. `[DECISION]` gate RF-23.

### 2.1 The current per leaf

| The part on the seat | The case | VBUS leaves 2, 11 | VHV leaves 5, 8 | GND leaves 1, 12 | Leaf loss | Verdict |
|---|---|---|---|---|---|---|
| B module | video, `1.92 W` | `0.28 A` each | | `0.28 A` each | `5.7 mW` | pass |
| B module | peak, `4.50 W` at `3.40 V` | `0.74 A` each | | `0.74 A` each | `38.9 mW` | pass |
| B module | video plus B cell charge | `0.30 A` each | | `0.30 A` each | `6.6 mW` | pass |
| port part | `27 W` at `9 V` | | `1.50 A` each | `1.50 A` each | `162 mW` | pass, no margin |
| port part | `27 W` at `15 V` | | `0.90 A` each | `0.90 A` each | `58 mW` | pass |
| dock pads | `25 W` at `12 V` | | `1.04 A` each | `1.04 A` each | `78 mW` | pass |

All rows are `[TREE]` outputs of `pack/bar_pins.py`.

**The rule for the port part**. Above `20 W` it must take a USB PD contract of `12 V` or more. At `9 V` the leaves sit at their rating. `[DECISION]`

**The lanes**. L0 and L1 carry the frame stream from `U1` to the tiles. `1 600 x 3 200 x 240 Hz x 24 bit` is `29.5 Gbit/s` raw. Display stream compression at `3:1` brings it near `10 Gbit/s`, so about `5 Gbit/s` per lane. That is the display team's number to confirm. `[HYPOTHESIS]`

## 3 · The dead pad

**The law**. Every power leaf of a seat field sits at `0 V` until a part on the seat proves itself. Water, a coin or a key never sees a voltage. `[DECISION]` gates ENR-19, MON-16.

### 3.1 The unmated state

| The pad | The state | The leakage in salt water |
|---|---|---|
| VBUS, VHV | open by S_SEAT, `1 MΩ` to GND | none, no source |
| L0, L1 | high impedance, ESD clamp only | none |
| SBA, SBB | a probe pulse of `1.8 V` through `1 MΩ`, `200 µs` every `250 ms` | `0.0014 µA` average, against the `1 µA` limit |
| GND | ground | none |

`[TREE]` `pack/bar_pins.py`.

### 3.2 The mating sequence, `3 ms`

1. The magnets pull the bar onto the seat. GND leaves 1 and 12 touch first.
2. The probe on SBA or SBB sees a load. The seat controller wakes in `0.2 ms`.
3. The seat controller sends a `128 bit` challenge on the sideband that loads.
4. `U7` in the B, or the port part's secure ID, answers with a signed response in `0.5 ms`.
5. The U_Q of the seat quadrant checks it. A paired B uses HMAC in `0.1 ms`. A new part uses a certificate in `1.5 ms`.
6. The response names the role: B module, port part or dock.
7. A B module gets VBUS. S_SEAT ramps it at `0.5 A` for `0.5 ms`.
8. A port part or the dock gets VHV, after the USB PD contract.
9. The lanes and the telemetry start. The total stays under `3 ms`. `[HYPOTHESIS]` gate ENR-19.

### 3.3 The unmating sequence

1. The bar lifts. The seat controller loses the sideband heartbeat of `100 µs`.
2. S_SEAT opens VBUS and VHV in under `0.8 ms`.
3. The short power leaves break before the long GND leaves. At `4.48 V` no arc forms.
4. The B goes to its islanded mode on the B cell.
5. The body keeps its tiles and its compositor state. It shows the local safe screen.

### 3.4 The dead-body boot

1. **On a Qi pad**. The Q1 rectifier runs from the coil alone. It charges with no cell voltage. `[GENERAL]` Qi receivers do this.
2. **On a port part**. The seat controller has no VBUS. It takes its handshake power from the sideband at `1 mA`, limited. `[HYPOTHESIS]`
3. **The pre-charge**. U_Q charges cells below `3.00 V` at `0.1 C` until they pass `3.00 V`.

## 4 · The quadrant seam

1. A removed quadrant opens its U_Q switch first. Its seam leaves sit at `0 V`.
2. Its `32` TCMs open their switches. The cells go to storage at `1 µA`.
3. A new quadrant answers the same `3 ms` challenge over the seam data link.
4. U_Q joins it in current-limit mode at `0.38 A`. Gate MEC-40.
5. If the B sits on the removed quadrant, the B runs islanded. A `3 s` swap uses `0.33 mWh` of the B cell.

## 5 · The open items of the power tree

1. The lane rate of `5 Gbit/s` per leaf needs the display team and a leaf return-loss test. Gate MON-21.
2. The seat controller and U_Q are custom parts. Their area in the seat tile and the crossing tile needs the body team.
3. The handshake time of `3 ms` assumes a hardware signature check. Gate ENR-19.
4. `HARDWARE/08` still names `64` seam leaves and `VSYS_HV`. This sheet supersedes it for L.6.0.
