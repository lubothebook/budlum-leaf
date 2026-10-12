# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME II · STRUCTURE, MASS, ENERGY AND RADIO

**Version:** 4.1 (revision A) · part of `MASTER/00-INDEX.md`
**Scope**. Mass, energy sheet, structure, heat and radio of the `80 x 160 x 4.00 mm` Leaf 160. It answers Ayaz's question: **why does a surface whose heavy compute runs on the network last longer at half the mass**?

---

## 1 · The answer in one table

| Configuration | Mass | Energy, nameplate | Energy, effective | A delta session | A video session |
|---|---|---|---|---|---|
| **Leaf 160, Feather cassette** | **78 g** | 20 Wh | 16 Wh | **7.9 h** | 4.9 h |
| Leaf 160, Standard cassette | 92 g | 25 Wh | 20 Wh | 9.9 h | 6.1 h |
| Leaf 160, Feather plus the module | 156 g | 45 Wh | 36 Wh | 17.8 h | 11.0 h |
| Leaf 160, Standard plus the module | 170 g | 50 Wh | 40 Wh | 19.8 h | 12.2 h |
| A carried surface of 2026, 160 mm by 80 mm class | 190 to 230 g | 19 to 22 Wh | | 6 to 9 h | 4 to 6 h |

**The table is the legacy cassette reference line**. In Revision L.5.0, the bulky external bottom battery is cancelled. The **`80 x 160 x 2.00 mm` 4-Quadrant (`+`) body (`4 x 17 g`) weighs `68 g` (`12.0 Wh`)**, or **`88 g` complete** (`HARDWARE/17`). `[DECISION]`

**The two corrections to the earlier draft**.

1. **The mass**. Splitting the `2.00 mm` body into `4 x 17 g` quadrants gives **68 g**, and **88 g complete**. `[DECISION]`
2. **The runtime**. Four `750 Wh/L` `LLZO/PEO` solid-state cells (`12.0 Wh` / `3 200 mAh`) give **>14.1 h** in a delta session. `[HYPOTHESIS]` Gate MEC-9 measures the table.

**The comparison, in one line**. Same energy as a carried surface of today, less than half the mass, and a longer day, because the compute is not in the body. `[DECISION]`

---

## 2 · The mass theorem and its law

**The theorem**. Every gram that is not display, not energy, not radio or not anchor is a design error. `[DECISION]`

```
M = 9 g per 100 cm² of device area   (the panel pair, the touch, the covers, the spine, the bus, the seal)
  + 2.9 g per Wh of nameplate energy (the cells, the protection and the shell of the cassette)
  + 7.5 g                            (the hub, the radio, the secure element, the connectors, the magnets)
```

**Superseded on 2026-10-12**. `HARDWARE/17` counts **12 body groups (`68.0 g`, `2.00 mm`, `52` parts)** and **2 B module groups (`20.0 g`, `32` parts = `88.0 g`)**. `[DECISION]`

`[HYPOTHESIS]` Gates MEC-2 and MEC-3 replace the coefficients with measurements.

### 2.1 Where the mass of a carried surface of 2026 goes, and where it does not go here

| The part | A carried surface of 2026 | A Leaf 160 4-Quadrant (`+`) Body | The saving |
|---|---|---|---|
| Cover glass, 0.6 mm | 17 g | 12.2 g (`2 x 0.20 mm` `ISO 10993` PC across `Q1..Q4`) | shatterproof medical-grade optical polycarbonate |
| Metal frame or midframe | 20 to 30 g | 8.2 g (perimeter spine + `(0,0)` Ti hub + `24` N52H + `64` gold leaves) | `<15 µm` (`n=1.585`) `+` cross seam and Ti/N52H micro-latch |
| Board, processor, shields, heat spreader | 25 to 40 g | 0 g CPU in body (`2.8 g` graphene/Mu-metal shield) | Zero CPU and Zero RAM; `U1` TCON + `U2` UWB/mmWave SiP in `90°` B ring |
| Camera island and lens set | 3 to 8 g | 0 in the body | the `50 MP` camera is in the `20 g` `90°`-bent-stem B module |
| Speaker and haptic parts | 3 to 6 g | 0 in the body | the sound set (`2 x MEMS` + speaker) is in the B module ring |
| Internal solid-state battery + `Qi2.2` coils | 50 to 58 g | **37.8 g in body** (`32.0 g` `LLZO/PEO` + `5.8 g` `Qi2.2` coils) | `4 x 3.0 Wh = 12.0 Wh` (`750 Wh/L`) non-flammable `LLZO` + `Qi2.2` wireless |
| T-OLED, PDLC film, AgNW/ITO, silicone OCA | 14 to 20 g | 11.8 g | dual T-OLED (`5.2 g`), PDLC (`2.1 g`), AgNW/ITO (`1.3 g`), silicone OCA (`3.2 g`) |
| **Total** | **190 to 230 g** | **68 g 4-Quadrant body** (`88 g` complete) | |

---

## 3 · The structure

### 3.1 The spine

The spine is one laminate that is the structure, the bus, the heat path, the antenna ground and the magnetic anchor. `[DECISION]`

| Layer | Thickness | Material | The job |
|---|---|---|---|
| Carrier | 60 µm | 301 stainless steel, perforated to 40 percent open area inside the wrap zone | stiffness where it is flat, no stiffness in the wrap |
| Conductor | 18 µm | copper | power and the video lane reference |
| Dielectric | 12 µm | a bend rated polyimide | insulation |
| Antenna windows | openings | through the laminate | the radio passes the metal |
| Anchor pattern | 0.4 mm pole pitch | in the steel | the module and the mount hold on it |

Mass 0.85 g per 100 cm², so 1.1 g for a Leaf 160. `[HYPOTHESIS]` Gate MEC-5 measures it.

### 3.2 The bend: the slip rule

1. The layers are **not bonded into one beam** across their whole area. Each layer bends about its **own** thin axis, and every interface shears by design.
2. **The numbers**. Interfaces see **0.4 to 0.8 MPa of shear** and **0.35 to 0.6 mm of slip at R 25.5 mm**. `[HYPOTHESIS]` Gates B-5 and B-6 measure both.
3. **Why it is required**. A bonded 3.54 mm stack at R 25.5 mm puts **6.9 percent** on its outer fibre. Decoupled, the panel sees **0.63 percent** and each `0.45 mm` battery laminate sees **0.38 percent** foil strain.
4. The Leaf 160² uses the same mechanism at its centre wrap zone (Volume I, Section 3.3). The round numbers are in `HARDWARE/12-THE-BEND-LAW.md`.

### 3.3 The edge, the seal and the impact

| Property | The value |
|---|---|
| The edge | `80 x 160 x 4.00 mm` prism with `R 3.20 mm` corners and `r 0.80 mm` softened prism edges (Volume I, Section 1.1) |
| The finish | a mat polymer with an anti-fingerprint texture; no visible fastener; the coat carries the hardness |
| The service by the user | the user replaces the panel, battery sheet, and module; spare parts are held for five years after the last sale (Q16) |
| The class | IP68 (`1.5 m`, `30 min`): dust tight and water resistant via the dual-lip FKM collar on the continuous battery sheet |
| The earlier cassette note | the earlier unsealed cassette note is superseded by the dual-lip FKM collar on the continuous battery sheet (`HARDWARE/11`, `ENR-12`) |
| The impact | the `20 g` Bare Leaf (`87 g` complete) at 1.2 m is under 1.0 J; a 200 g surface is 2.4 J. Gate MEC-4 |
| The area density | 0.61 g/cm² for the Leaf against 1.6 g/cm² for a carried surface of today |

---

## 4 · The energy cassette

### 4.1 The mechanical standard

| Property | Value |
|---|---|
| Thickness | 2.88 mm, fixed for the whole family |
| Footprint | 122 cm² inside a Leaf 160, and one cassette per two panels in the larger carriers |
| Removal | slide out at the fixed edge, no tool, target below 15 s, 1 000 cycles |
| Contacts | 8 spring contacts at the fixed edge, wiped and released on the slide, plus 2 sense lines |
| Latch | a polymer snap with a magnetic assist and a secondary catch |
| Identity | a secure element in the cassette, and the record of RG-6 |
| Interface | 4.5 V power, a one wire identity, a temperature pair, a cell voltage pair |

### 4.2 The two fills

| Fill | The cells | Cell volume | Nameplate | Effective | Mass | A delta session on a Leaf 160 |
|---|---|---|---|---|---|---|
| **Feather** | 1.82 mm of a tiled silicon carbon cell, plus a 0.46 mm shim | 22.2 cm³ | 20 Wh | 16 Wh | 58 g | 7.9 h |
| **Standard** | 2.28 mm of the same cell | 27.8 cm³ | 25 Wh | 20 Wh | 68 g | 9.9 h |
| A cell upgrade, later | the same cassette with a 1 000 Wh/L cell | 27.8 cm³ | 27.8 Wh | 22 Wh | 75 g | 10.9 h |

`[PUBLICATION]` Graphite cells reach 730 Wh/L, 2026 flagship cells reach 700 to 950 Wh/L, and high-silicon cells pass 1 000 Wh/L. `[HYPOTHESIS]` Gates ENR-1 and ENR-2 measure the continuous polymer-gel sheet.

### 4.3 The module, and what it adds

The `90°`-bent-stem B module (`20 g`, `32` parts) clips onto any of the 4 outer edges on Front (`+Z`) or Back (`-Z`). Only its stem (`USB-C` + antenna) bends `90°` while its `Ø32 mm` ring (`50 MP` camera + AMOLED + SiP) lies flat on the screen. `[DECISION]`

| Property | Value |
|---|---|
| Cell volume | `4 x 2.835 cm³ = 11.34 cm³` (`35 x 75 x 1.08 mm` per quadrant) |
| Nameplate | **0.45 Wh** in the B ring and **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh` at `750 Wh/L`)** across `Q1..Q4` (`HARDWARE/15`) |
| Mass | **68 g 4-Quadrant (`+`) body (`4 x 17 g`)** + **20 g `90°`-bent-stem B module** = **88 g** complete (`HARDWARE/17`, `HARDWARE/20`) |
| The device with the module | 88 g complete (`68 g` 4-Quadrant body + `20 g` `90°`-bent-stem B module), `12.0 Wh` (`3 200 mAh`) + `0.45 Wh` |
| The runtime with the 4 quadrants | `>14.1 h` in a delta session (`12.0 Wh` `LLZO/PEO` solid-state + `<3 s` single-tile swap) |

**The mass rule of the module**. The module is a second energy store, a second sensor and the sound set of the product, and it is not a cosmetic part. A module that adds mass without energy, without a sensor or without sound is refused.

### 4.4 The `2.00 mm` (`68 g`) 4-Quadrant (`+`) solid-state body and `<3 s` tile swap (`HARDWARE/11`)

1. The bulky bottom battery is cancelled; the `2.00 mm` (`68 g`) body splits into **`4 x 17 g` quadrants (`Q1..Q4`)**. `[DECISION]`
2. The `2.00 mm` symmetric 11-layer sheet bends effortlessly to `R 25.5 mm` at `0.38 percent` T-OLED strain (`0.18%` `LLZO` strain). Gate ENR-4.
3. Each tile packs a non-flammable **`LLZO/PEO` solid-state cell (`3.0 Wh`, `<=36.2 °C` NTC)** and **`Qi2.2` wireless coils**. `[HYPOTHESIS]` Gate ENR-1 measures the real capacity.
4. `Q1..Q4` join across the `<15 µm` `+` seam via **`24` N52H (`11.2 N`)** and **`64` gold leaves (`<3 s` swap)**. `[DECISION]`

### 4.5 The charging ladder

| Path | The input | The heat at 80 percent efficiency | The note |
|---|---|---|---|
| **Universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` `Qi` wireless charging on the screen body** | `15-25 W` (`Qi2.2` MPP) / `5-10 W` (`Qi` BPP/EPP) | `0.4 W` (`<=36.2 °C` NTC) | charges the assembled 4-quadrant screen or any detached tile on any wireless pad (`R-1`) |
| Wired, the **sole `USB Type-C` receptacle in the `90°`-bent B stem** | up to 40 W peak (`25 W` flat) | 0.5 W | zero USB-C on the screen body; wired charging/data requires the B module (`HARDWARE/04`) |
| The Leaf Desk Dock (`Qi2.2` + 4 gold contact pads) | 27 W (`20 V` at `1.25 A`) | 0.1 W | contact or `Qi2.2` charging with spring pins and identification handshake |

**The heat is the ceiling**. 65 W at 80 percent is 13 W over 128 cm², which is 0.10 W/cm². `[GENERAL]` Three thermal paths are measured: through the faces, across the graphite-copper spreaders, and out to the perimeter frame. Gate MEC-6 sets the derating curve: full power below 38 °C, linear derate to 20 percent at 45 °C, and stop above 48 °C.

### 4.6 The pen, the keyboard and the port chain (the answers of Ayaz, question 14)

| The item | The value | The note |
|---|---|---|
| The pen | **active**: its own radio, pressure, tilt and a low latency ink path | the answer of Ayaz |
| How the pen charges | **it attaches magnetically to the module and charges on it** | the module is the energy part, so the pen does not need its own cradle |
| How the pen connects | **Bluetooth is mandatory**, and a wired path exists through the USB-C port of the module | |
| The module port | a USB-C receptacle on the module, so a pen, a keyboard, a headset or a service tool connects at the module and reaches the device | the answer of Ayaz: from the camera hardware, from there to the device |
| The device port | a USB-C receptacle at the fixed edge for power, service and a display output | Volume II, Section 4.5 |
| The keyboard | a Bluetooth accessory with its own cell | no keyboard inside the body, because the body holds no input hardware beyond the panel |
| The sound set | **the microphone array and a small speaker live in the module** (the answer of Ayaz, question 31) | a call is heard and a voice is captured; the body gains no hardware |
| The headphone path | **a 3.5 mm headphone jack on the module** (the answer of Ayaz, question 33) | a wired headset works with no adapter and no radio |
| The mass | a pen of 12 to 17 g, a keyboard of 180 to 260 g | |
| The power | the pen draws 0.05 W in use, charged from the module; a five minute attach gives about six hours of writing | `[HYPOTHESIS]` gate MEC-10 |
| The rule | a magnet for a charger in a device that must keep its radio budget | the pen magnet sits on the module, away from the antenna windows of the leaf, and gate MEC-8 measures it |

---

## 5 · The energy accounting

| Format and case | Display | Address | Hub | Radio | Authority | Total | Cassette | Runtime |
|---|---|---|---|---|---|---|---|---|
| Leaf 80, delta | 0.35 W | 0.10 W | 0.60 W | 0.35 W | 0.10 W | 1.50 W | Feather 20 Wh | 10.7 h |
| Leaf 160, delta | 0.60 W | 0.20 W | 0.70 W | 0.40 W | 0.12 W | 2.02 W | Feather 20 Wh | 7.9 h |
| Leaf 160, delta, with the module | 0.60 W | 0.20 W | 0.70 W | 0.40 W | 0.12 W | 2.02 W | 45 Wh | 17.8 h |
| Leaf 160, video | 1.10 W | 0.25 W | 1.20 W | 0.60 W | 0.12 W | 3.27 W | Standard 25 Wh | 6.1 h |
| Leaf 160, static page at 10 Hz | 0.15 W | 0.02 W | 0.10 W | 0.05 W | 0.03 W | 0.35 W | Feather 20 Wh | 45 h |
| Leaf 160, safe screen only | 0.10 W | 0.02 W | 0.05 W | 0.00 W | 0.03 W | 0.20 W | Feather 20 Wh | 80 h |
| Leaf 160², video | 2.20 W | 0.50 W | 1.40 W | 0.60 W | 0.12 W | 4.82 W | 2 × Feather | 13.3 h |
| Leaf 480, static work | 5.00 W | 0.80 W | 1.60 W | 0.60 W | 0.12 W | 8.12 W | the rail | mains |
| Leaf 1400, video at 30 percent APL | 60 W | 4 W | 6 W | 3 W | 0.50 W | 73.5 W | the rail | mains |

**The rule**. A runtime claim names the format, the cassette, the session class and the term table. The phrase "all day" is forbidden. `[DECISION]`

---

## 6 · The radio and the antenna

### 6.1 The radio set

| Radio | Class | The note |
|---|---|---|
| Wi-Fi 7 | tri-band, multi-link operation, 320 MHz, 2 streams minimum and 4 preferred | the main path indoors |
| 5G | standalone, sub-6 GHz, 4 × 4 MIMO, carrier aggregation | the main path outdoors |
| Millimetre wave | an antenna in package, a 15 mm by 15 mm block per band | optional, short range, high rate |
| Satellite | non-terrestrial through the cellular radio | the last resort, a message class |
| Bluetooth | the wallet authenticator and the accessories | the pen, the keyboard, the ear part |
| Near field | the tap and the pairing | |
| Ultra-wide band | ranging and the find-my-module function | a candidate |
| Navigation | multi-constellation | |

### 6.2 The antenna law for a 160 by 80 mm body

1. The upright B bar (`çubuk`) on the top edge (`y = +80 mm`) is the primary antenna. A diversity slot antenna sits in the bottom rail (`y = -80.0 mm`). `[DECISION]`
2. **The module is the primary free-space antenna site**. Standing upright above the top edge, the B bar stays clear of the hand and never bends. Gate MEC-8 measures the gain of both.
3. The match is measured flat, at the gentle bend and at the wrap, because the bend changes the geometry.

### 6.3 The conflicts, each with a budget

| The conflict | The budget | The gate |
|---|---|---|
| The battery sheet serves as the ground plane | continuous `109.4 cm²` reference plane with zero tile gaps | MEC-8 |
| The metal spine is close to the radiator | the pattern and the distance | MEC-8 |
| Wired and dock charging against the radios | the desense of each receiver with the cable or dock connected (`R-1`: no wireless coil) | MEC-6, MEC-8 |
| The bend changes the match | the return loss at R 70 mm and at R 25.5 mm against flat | MEC-8 |
| The module magnet over an antenna | the gain loss, then the keep-out area | MEC-8 |

**The decision rule**. An attach that costs 3 dB of antenna gain is worse than a mechanical clip, because the link is the product. If the magnet loses more than 1.5 dB, the module moves to a clip. `[DECISION]`

---

## 7 · The structure, mass and energy gates

| Gate | The test | The pass condition |
|---|---|---|
| MEC-1 | the bend durability, a bonded stack against a decoupled stack | the stated cycle counts at R 25.5 mm and at R 70 mm, and the measured pair. Gates B-1 and B-2 carry the claim |
| MEC-2 | the mass of a real Leaf 160, part by part | inside 10 percent of the law of Section 2 |
| MEC-3 | the cassette: removal time, 1 000 cycles, contact resistance, the record | below 15 s, no damage, the record complete |
| MEC-4 | the drop set: 6 faces, 1.2 m, concrete, with a cassette and with a module | a working surface, with a damage report |
| MEC-5 | the spine: stiffness, heat spread, the antenna windows, the anchor force | every value stated, the anchor holds the module at the stated force |
| MEC-6 | the charge heat and the power ceiling at 10, 25, 45, 60 and 80 W, seated and removed | the derating curve, and a surface temperature inside the safety limit |
| MEC-7 | the seal class IP54 and the dust behaviour | as stated |
| MEC-8 | the radio set in a free hold and a hand hold, the desense set, the module gain, the match flat and bent | every budget of Section 6.3, and the 1.5 dB rule |
| MEC-9 | the energy accounting of Section 5 on a real device | each term measured, and the total inside 10 percent |
| ENR-1 | the volumetric energy density (`750 Wh/L`, `4 x 3.0 Wh = 12.0 Wh` / `3 200 mAh`) of the 4-Quadrant `LLZO/PEO` solid-state battery | the measured effective energy against the nameplate |
| ENR-2 | the cell samples at 750, 900 and 1 000 Wh/L | the chosen fill, and the second source named |
| ENR-3 | the gauge against the record: a cell swap, a worn cassette and a counterfeit shell | the device refuses a mismatch beyond the tolerance |
| ENR-4 | one tile fault and the isolation | one tile opens, the neighbour survives, and the surface reports it |
| MEC-10 | the pen: attach, charge, latency, pressure, and the antenna effect of its magnet | the numbers of Section 4.6, and no radio penalty |
