# BUDLUM LEAF · HARDWARE · 18 · THE DOCK AND THE STAND, PART BY PART (27 PARTS)

**Revision L.5.0 · 2026-10-12**.
`08-CONNECTION-SPEC.md` states the dock interface, and `01-SYSTEM-ARCHITECTURE.md` states what it carries. **This file states the dock in 27 parts**. A `240 x 120 x 12 mm` anodized deck integrating a **`25 W` `Qi2.2` MPP wireless transmitter pad**. It covers the portless 4-quadrant screen body plus **four power and two data gold pads (`27 W` + `2.5 GbE`)**. Also, an optional **45 TOPS room validator board**. `[DECISION]`

---

## 1 · The dock, in numbers

| The quantity | The value |
| --- | --- |
| the deck | **240 x 120 x 12 mm**, on four silicone feet, at 8 degrees of rake |
| wireless charging pad | **integrated `Ø54.0 mm` `Qi2.2` MPP (`25 W`) + `4 x Ø22.0 mm` (`10 W`) wireless transmitter array** |
| the wired seat | **four gold power pads (`10 mm` pitch) + two data pads (`27 W` + `2.5 Gbit/s`)** mating. It uses the `90°` B stem or dock seat |
| the power in / out | **140 W USB-C wall feed in; `25 W` `Qi2.2` wireless + `27 W` gold pads + `5 W` B module post out** |
| the wired network | **2.5 Gbit/s Ethernet over the data pair**, bridged into the `60 GHz` / `UWB` room link |
| the validator board | **optional**, `28 W`, `45 TOPS`, in the thermally isolated `100 x 60 x 8 mm` deck bay |
| the camera post | holds the **`90°`-bent-stem B module (`20.0 g`)** when using large desk/wall members (`Leaf 480 / 1400 / 2800`) |
| the mass | **310 g** standard, and **360 g** with the `45 TOPS` validator board |

---

## 2 · The dock, part by part (27 parts)

| No | The part | The material | The size | The function | The gate |
| --- | --- | --- | --- | --- | --- |
| 1 | the deck top | 6061-T6 aluminium + ceramic `Qi2.2` window | `240 x 120 x 3.0 mm` | the seat face, `Qi2.2` wireless surface, and radiator | DK-1 |
| 2 | the deck body | 6061-T6 aluminium | `2.0 mm` wall shell | structural stiffness, validator bay, and cable routing | DK-1 |
| 3 | the seat land | machined aluminium + polymer cradle | `160 mm` wide x `12 mm` deep | cradles the `80 x 160 x 2.00 mm` 4-quadrant body or `90°` B stem | DK-2 |
| 4 | the power pad set | hard gold over nickel on copper | `4` pads, `Ø6.0 mm`, `10 mm` pitch | `27 W` direct contact feed at `0.5 mΩ` each | DK-3 |
| 5 | the data pad set | hard gold, `2.4 mm` wide | `2` pads, `12 mm` apart | `2.5 Gbit/s` wired network link | DK-4 |
| 6 | the pad spring set | 17-7 stainless, `0.35 N` per pad | `6` springs | contact wipe and uniform seating force | DK-3 |
| 7 | `Qi2.2` MPP transmitter coil & magnets | Litz copper `Ø54 mm` + `4 x Ø22 mm` coils + `N52H` ring | `80 x 160 x 1.8 mm` under deck window | charges the portless 4-quadrant body (`25 W`) or individual tiles (`10 W`) | DK-2, DK-3 |
| 8 | the lead-in chamfer | `45°` facet of `1.5 mm` | around the seat land | guides the `2.00 mm` body into the cradle with one hand | DK-2 |
| 9 | the pad gasket | 40 Shore A silicone, `0.40 mm` | around the pad set | `IP52` environmental seal on the deck | DK-5 |
| 10 | the deck board | 6-layer PCB | `180 x 70 x 1.2 mm` | hosts `Qi2.2` inverter, PD sink, `2.5 GbE` PHY, and fan controller | DK-4 |
| 11 | the PD 3.1 sink controller | `140 W` USB-PD 3.1 controller | `4.0 x 4.0 mm` | negotiates `20 V / 28 V` wall power | DK-3 |
| 12 | the `Qi2.2` & pad power stage | `95%` GaN half-bridge + buck-boost | `18 x 12 mm` block | drives `25 W` `Qi2.2` MPP wireless and `27 W` gold pads | DK-3 |
| 13 | the `2.5 Gbit/s` Ethernet PHY | `2.5GBASE-T` + `USB 3.2` bridge | `7.0 x 7.0 mm` | wired room network interface | DK-4 |
| 14 | the room network switch | 4-port `2.5 GbE` + `60 GHz` AP bridge | `9.0 x 9.0 mm` | links the validator bay, wired LAN, and `U2` `60 GHz` B module | DK-4 |
| 15 | the wall feed socket | `USB-C`, `140 W` rated | `8.9 x 7.6 mm` | single rear wall power and data receptacle | DK-3 |
| 16 | the heat pipe & fin stack | `Ø6 mm` flattened Cu pipe + `60 x 60 mm` fins | `120 mm` run | removes `28 W` validator heat away from the screen cradle | DK-6 |
| 17 | the whisper blower | `60 mm` hydrodynamic fan (`22 dBA`) | `60 x 60 x 7 mm` | runs only when validator bay exceeds `12 W` sustained | DK-6 |
| 18 | the validator bay | keyed slot with thermal pads | `100 x 60 x 8 mm` | houses the optional `45 TOPS` room validator board | DK-7 |
| 19 | the validator board | optional 8-core NPU/SoC (`45 TOPS`, `28 W`) | `96 x 56 x 4.5 mm` | local Zero-CPU compute node and Budlum network validator | DK-7 |
| 20 | the bay seal | `0.15 mm` labyrinth + captive thumbscrew | perimeter seal | tool-free validator swap with dust protection | DK-7 |
| 21 | the `90°` B module post | anodized post with `2.00 mm` edge profile | `40 x 14 x 28 mm` | docks the `90°`-bent-stem B module for desk/wall screens | DK-8 |
| 22 | the post `12`-pad link | hard-gold pads + `3 ms` Dead-Pad switch | `22.0 x 2.8 mm` | supplies `5 W` and `10 Gbit/s` to the B module on the post | DK-8 |
| 23 | the VESA 75 wall mount | `4 x M4` stainless inserts + `0.5°` level | `75 x 75 mm` pattern | mounts the dock and large `Leaf 1400 / 2800` sheets on a wall | DK-9 |
| 24 | the anti-rotation guide pins | `2 x Ø3.0 mm` hardened stainless pins | `6.0 mm` pitch | prevents torsional twist under cable pull | DK-2 |
| 25 | the non-slip feet | `4` pads of 40 Shore A silicone | `Ø14.0 x 2.0 mm` | anchors the deck on glass or wood desks | DK-1 |
| 26 | the status light bar | diffused RGBW micro-LED bar | `24.0 x 2.0 mm` | indicates `Qi2.2` charge state, `3 ms` auth, and validator status | DK-10 |
| 27 | the serial plate & secure element | laser-etched stainless + `1-Wire` IC | `20.0 x 5.0 mm` | cryptographic dock identity (`3 ms` Dead-Pad handshake) | DK-10 |
