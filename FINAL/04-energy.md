# BUDLUM LEAF · THE DIRECTIVE · PART 4 · THE 4-QUADRANT (+) BIOCOMPATIBLE SOLID-STATE BATTERY AND QI2.2 WIRELESS CHARGING

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. The body holds `5.7` to `7.2 Wh` in `128` micro cells, with no loss to the stretch. The B module adds `0.14 Wh` and the dock carries a `20 Wh` pack.

---

## 4.1 The mechanical, electrical, and eyewear-safety standard (`HARDWARE/11`, `HARDWARE/15`)

| The property | The value |
|---|---|
| The dimensions & mass | `4 x (40.0 x 80.0 x 2.00 mm)` snap-together polycarbonate quadrants (`17.0 g` each) = **`80.0 x 160.0 x 2.00 mm` (`68.0 g` total body)** |
| The cell chemistry | **non-flammable `LLZO/PEO-Ceramic` all-solid-state cells** (`4 x 3.0 Wh = 12.0 Wh` / `3 200 mAh` at `750 Wh/L`, `0%` liquid, `0.0 ppm` HF gas) |
| Eyewear & ocular safety | **`<=36.2 °C` hardware NTC cut-off**, **`ISO 10993-5/-10`** medical-grade BPA-free PC, `<0.08 µT` bifilar ELF, **`SAR = 0.054 W/kg`**, `IEC 62471` RG0 |
| The `+` cross optical seam | **`12 µm` (`<15 µm`) phenyl-fluorosilicone self-healing lip (`n = 1.585` vs `n_PC = 1.586`, Fresnel `R < 0.0001%`)**, `<2.5 µm` Z-step (zero scratch/line) |
| Tool-free quadrant hot-swap | **`(0,0)` Ti hub + `8` Ti pins + `24` N52H (`11.2 N`) + `64` gold leaves** (`<3 s` swap, `EU 2023/1542` Art. 11) |
| Universal wireless charging | **Central `Ø54.0 mm` 4-sector `Qi2.2` MPP (`15-25 W`)** + **`4 x Ø22.0 mm` (`5-10 W`) local `Qi` coils**; **zero USB-C and zero buttons on body** |
| Sole `USB-C` & Zero-CPU core | **sole `USB Type-C` (`40 W`)** in the `90°` B stem; `U1` TCON + `U2` `UWB / mmWave` SiP in the B ring (`20 g`) |
| Screen bending strain | **`0.38 percent` outer polycarbonate strain (`0.22%` `LLZO` strain) at `R 25.5 mm`** via `G = 0.08 MPa` silicone OCA slip layers |

---

## 4.2 The modular 4-Quadrant (`+`) solid-state battery family

| The member | `+` Screen-battery body | Solid-state cell density | Target capacity | Delivered energy | Body mass | Active session (`0.85 W`) |
|---|---|---|---|---|---|---|
| **Leaf 80 (1 tile)** | `40 x 80 x 2.00 mm` (`17 g`) | `750 Wh/L` `LLZO/PEO` solid-state | `800 mAh` | **3.0 Wh** | `17 g` | **3.5 h** (or eyewear visor) |
| **Leaf 160 (4 tiles)** | `80 x 160 x 2.00 mm` (`68 g`) | `750 Wh/L` `LLZO/PEO` solid-state | **`3 200 mAh`** | **12.0 Wh** | `68 g` | **>14.1 h** |
| **Leaf 160² (8 tiles)** | `160 x 160 x 2.00 mm` (`144 g`) | `750 Wh/L` `LLZO/PEO` solid-state | `6 400 mAh` | **24.0 Wh** | `144 g` | **>22.0 h** |
| **Leaf 480 (48 tiles)** | `320 x 480 x 2.40 mm` | `750 Wh/L` `LLZO/PEO` solid-state | `38 400 mAh` | **144.0 Wh** | modular | **>30.0 h** |

`[DECISION]` Cancelling the bulky bottom pack and splitting the `2.00 mm` (`68 g`) body across `+` creates four `17 g` tiles (`Q1..Q4`). Gates ENR-1 and ENR-2 measure the `12.0 Wh` `LLZO/PEO` capacity, `Qi2.2` wireless charging, and `<3 s` quadrant swap.

| The architecture class | The density / bend behavior | The source standing |
|---|---|---|
| Non-flammable `LLZO/PEO` all-solid-state cell inside each polycarbonate tile | **`750 Wh/L`**, delivering **`3.0 Wh` (`800 mAh`) per tile = `12.0 Wh` (`3 200 mAh`) total** (`0%` liquid, `0` HF) | `[DECISION]` |
| `2.00 mm` (`68.0 g`) 11-layer `ISO 10993` polycarbonate + `T-OLED` + `PDLC` stack | **`0.38%` outer polycarbonate strain (`0.22%` `LLZO` strain) at `R 25.5 mm`** via `G = 0.08 MPa` OCA slip | `[DECISION]` |
| `<15 µm` (`n = 1.585`) `+` cross optical seam + `(0,0)` Ti hub + `64` gold leaves | Fresnel `R < 0.0001%` (zero visible line/scratch), `<2.5 µm` Z-step, **`<3 s` tool-free swap (`EU 2023/1542` Art. 11)** | `[DECISION]` |
| Bulky external bottom battery module (`80 x 36 x 4 mm`) | **cancelled in Revision L.5.0**: replaced by 4-Quadrant (`+`) internal solid-state cells + `Qi2.2` wireless body | `[DECISION]` |

---

## 4.3 Why the 4-Quadrant (`+`) solid-state architecture solves ergonomics, eyewear safety, and EU replaceability

1. Cancelling the bulky bottom pack restores a clean **`2.00 mm` (`68 g`)** outline (`4 x 17 g` tiles). `[DECISION]`
2. Each tile combines **`ISO 10993` polycarbonate**, **flicker-free `T-OLED`**, **`PDLC` privacy film**, **`AgNW/ITO` mesh**, and a **`3.0 Wh` `LLZO/PEO` solid-state cell**.
3. The `+` seam uses a **`12 µm` (`n = 1.585`) self-healing lip** and **Corning edge-wrap traces** (`0.00 mm` internal bezel).
4. Eyewear safety uses **`0%` flammable liquid**, **`<=36.2 °C` NTC cut-off**, **`<0.08 µT` bifilar tabs**, and **`SAR = 0.054 W/kg`**.
5. The portless body charges on any **`Qi / Qi2.2` (`15-25 W`)** pad. The **sole `USB Type-C` (`40 W`)** lives in the `90°`-bent B stem. `[DECISION]` gate ENR-1.

---

## 4.4 The gauge and the record

| The field | The source | Why it matters |
|---|---|---|
| The part class and the part id | the secure element | an anchor and a revocation |
| The cell chemistry and the batch | the maker | a recall can be scoped |
| The rated capacity and the measured capacity | the maker and the gauge | a mismatch beyond the tolerance refuses the cassette |
| The cycle count and the depth of discharge history | the gauge | a worn cassette is visible before it fails |
| The temperature history, the peak and the time above 45 °C | the gauge | the heat record |
| The protection events: over current, over voltage, over temperature | the protection circuit | a hard failure leaves a trace |
| The signatures: the maker, the line, the calibration | the maker and the device | a counterfeit shell is detected |
| The reference: the pair of the cassette with the leaf serial | the device | a stolen cassette is visible |

**How the gauge is protected**. The gauge is sealed inside the cassette shell, its key is burned at the line, and it signs every reading with a monotonic counter. A rewritten record breaks the chain, and the device refuses the cassette. `[DECISION]` gate ENR-3.

---

## 4.5 The charging ladder

| The path | The input | The heat at 80 percent efficiency | The note |
|---|---|---|---|
| **Wired, a USB-C receptacle at the fixed edge** | **40 W peak, 25 W flat**, with a 45 W ceiling in the hand | about 0.5 W at 25 W, and 9 to 13 W at the 45 W ceiling | the fast path, the service path and the common charger rule of the European Union |
| **The dock and the rail, by contact** | **25 W**, 20 V at 1.25 A per power pad | **about 0.1 W** at 30 mΩ, and 0.31 W at a worn 100 mΩ pad | four gold pads on the fixed edge, and spring pins in the dock. **This path replaces the coil** |
| the wireless paths | **withdrawn** | n.a. | **the order of Ayaz of 2026-10-06: no wireless charging**. Part 20, Section 20.1, states what it cost and what the withdrawal returns |

**The derating curve**. Full power holds below 38 °C of the surface. Power derates linearly to 20 percent at 45 °C and stops above 48 °C with a message. `[DECISION]` gate MEC-6 fixes the numbers.

**Why the heat is the ceiling and not the connector**. Three thermal paths are measured: through the leaf, through the battery back, and along the sheet to the edge. At 80 W and 80 percent, 16 W over 200 cm² is 0.08 W/cm², which needs the spreader of Part 11.

---

## 4.6 The energy accounting, per member

| The member and the case | Display | Address | Hub | Radio | Authority | The total | The cassette | The runtime |
|---|---|---|---|---|---|---|---|---|
| Leaf 80, a delta session | 0.35 W | 0.10 W | 0.60 W | 0.35 W | 0.10 W | 1.50 W | Feather 20 Wh | 10.7 h |
| Leaf 160, a delta session | 0.60 W | 0.20 W | 0.70 W | 0.40 W | 0.12 W | 2.02 W | Feather 20 Wh | 7.9 h |
| Leaf 160, a delta session, with the module | the same | | | | | 2.02 W | 40 Wh | 15.8 h |
| Leaf 160, a video session | 1.10 W | 0.25 W | 1.20 W | 0.60 W | 0.12 W | 3.27 W | Standard 25 Wh | 6.1 h |
| Leaf 160, a static page at 10 Hz | 0.15 W | 0.02 W | 0.10 W | 0.05 W | 0.03 W | 0.35 W | Feather 20 Wh | 45 h |
| Leaf 160, the safe screen, no link | 0.10 W | 0.02 W | 0.05 W | 0.00 W | 0.03 W | 0.20 W | Feather 20 Wh | 80 h |
| Leaf 160², a video session | 2.20 W | 0.50 W | 1.40 W | 0.60 W | 0.12 W | 4.82 W | 2 × Feather | 13.3 h |
| Leaf 480, a static work session | 5.00 W | 0.80 W | 1.60 W | 0.60 W | 0.12 W | 8.12 W | the rail | mains |
| Leaf 1400, a video session | 60 W | 4 W | 6 W | 3 W | 0.50 W | 73.5 W | the rail | mains |

**The rule**. A runtime claim names the member, the cassette, the session class and the term table. The phrase "all day" is forbidden. `[DECISION]`

---

## 4.7 The safety and the rules of the market

| The rule | The subject | The design answer |
|---|---|---|
| IEC 62133-2 | the cells and the cassette | the abuse set of gate ENR-4: over charge, over discharge, a short, a crush, a nail, a thermal chamber |
| UN 38.3 | the transport of the cells and the cassette | every shipment, and a test summary in the record |
| IEC 62368-1 | the electrical safety of the product | the double insulation at the connector and the fault test |
| EU 2023/1542, Article 11, from 18 February 2027 | a removable and a replaceable battery | **the slide out cassette is the design answer**, and the answer is written into the claim file |
| The common charger rule | the wired path | USB-C at the fixed edge |
| RoHS and REACH | the materials | with the panel and the cell partners |
| The battery passport | portables are outside its scope today | it is watched, and the record format already carries the fields |

---

## 4.8 How the 4-Quadrant (`+`) solid-state screen-battery tiles are built

| Step | The operation | The parameter |
|---|---|---|
| 1 | `35.0 x 75.0 x 1.08 mm` non-flammable `LLZO/PEO` solid-state cells (`3.0 Wh` each) are hermetically sealed with bifilar tabs | **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`)**, `0%` liquid, `0.0 ppm` HF gas |
| 2 | `Qi2.2` `90°` sector coil (`Ø54 mm`), local `Ø22 mm` `Qi` coil, `U_QI` BMS, `36.2 °C` NTCs, and `Mu-metal`/graphene shield are laminated | `<0.08 µT` stray ELF field and `15-25 W` `Qi2.2` wireless charging |
| 3 | front/back `T-OLED` (`0.14 mm`), `AgNW/ITO` (`0.04 mm`), `PDLC` (`0.09 mm`), and `ISO 10993` PC (`0.20 mm`) are bonded with `G = 0.08 MPa` OCA | `2.20 ± 0.02 mm` tile stack (`17.0 g` per tile), `0.38%` strain at `R 25.5 mm` |
| 4 | Corning edge-wrapped conductors are formed on the inner `+` faces and coated with the `12 µm` (`n = 1.585`) phenyl-fluorosilicone optical lip | Fresnel reflection `R < 0.0001%`, zero internal bezel, zero scratch |
| 5 | `(0,0)` Ti hub seat, tapered Ti pins, `6` bipolar `N52H` magnets, and `16` gold micro-leaf contacts are fitted on each internal edge | `<2.5 µm` Z-step, `11.2 N` pull hold, `3 ms` Dead-Pad, `IP68` seal |
| 6 | formation cycling, `3 ms` Dead-Pad authentication burn-in, `<=36.2 °C` ocular thermal lock test, and `<3 s` hot-swap verification | `12.0 Wh` capacity and serial recorded into the cryptographic element |
| 7 | batch verification on the ENR-4 abuse set, `IP68` immersion, and `10 000`-bend 4-quadrant flex test | passes `IP68` (`1.5 m`, `30 min`) and `0.38%` strain at `R 25.5 mm` |

---

## 4.9 The energy gates

| Gate | The test | The pass condition |
|---|---|---|
| ENR-1 | the `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`, `750 Wh/L`) `LLZO/PEO` solid-state battery capacity and impedance | **`>=12.0 Wh` (`3 200 mAh`)** at Leaf 160 (`68.0 g` 4-tile body), resistance `<28 mΩ` |
| ENR-2 | the `2.00 mm` (`68 g`) 4-Quadrant (`+`) flex at **`R 25.5 mm` over `10 000` bends** and **`<3 s` tool-free swap** | **`0.38 percent` max PC strain (`0.22%` `LLZO` strain)**, zero reboot during `<3 s` swap |
| ENR-3 | the gauge and `3 ms` Dead-Pad cryptographic handshake against a counterfeit shell | pins remain at `0 V` until `<3 ms` handshake passes; refuses mismatched record |
| ENR-4 | the abuse set: over charge, over discharge, a short, a crush, a nail, a thermal chamber | no fire, `0.0 ppm` HF gas, `<=36.2 °C` eyewear limit, and a report per case |
| ENR-5 | the `10 000` cycle `+` seam magnetic latch (`11.2 N`), `64` gold leaves, and `<15 µm` (`n = 1.585`) `IP68` lip | contact resistance `<18 mΩ`, step `<2.5 µm`, passes `IP68` after `10 000` swaps |
| ENR-6 | the charge from 0 to 80 percent via `Qi2.2` wireless (`15-25 W`), `90°` B stem USB-C (`40 W`), and Dock (`27 W`) | follows the derating curve with eyewear temperature `<=36.2 °C` |
