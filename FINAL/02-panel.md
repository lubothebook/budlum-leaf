# BUDLUM LEAF · THE DIRECTIVE · PART 2 · THE PANEL AND THE LIGHT

---

## 2.1 The light technology

| The technology | The brightness | The lifetime | The flexibility | The class | The verdict |
|---|---|---|---|---|---|
| **Flexible organic light emitting stack with a quantum dot colour layer** | 800 to 1 500 nits, peak on a window | 20 000 to 40 000 h | a 25 mm radius is standard in current products | 1× | **the choice** `[DECISION]` |
| Micro light emitting diode | 2 000 to 5 000 nits | above 60 000 h | good, on a stiffer backplane | 3 to 8× | the later upgrade for a bright outdoor surface |
| Transparent emissive panel | 300 to 800 nits at the eye | 10 000 to 20 000 h | on a polymer substrate | 4× | the clear family, Part 7 |
| A liquid crystal surface with a backlight | 1 000 nits | high | poor in a bend | 0.6× | refused: a Leaf bends and a backlight doubles the thickness |

`[PUBLICATION]` for the ranges, `[COMPANY]` for the supply statements, `[HYPOTHESIS]` for the Leaf values, which gates DSP-1 and DSP-5 measure.

---

## 2.2 The stack of one face, layer by layer, with the process

| Layer | The thickness | The material | The job | The process step |
|---|---|---|---|---|
| Hard coat | 10 µm | a plasma deposited scratch coat | the scratch and the strain limit of the cover | a plasma deposition on the cut panel, after bonding |
| Cover | 250 µm | polycarbonate, high heat grade, optically clear | impact, optics, the outer surface | cut to the outline, printed with the R 3.20 mm corner and r 0.80 mm softened edge |
| Optical adhesive | 50 µm | a low modulus, bend rated, index matched | the neutral axis tool | a vacuum lamination at 40 °C, then a 24 h cure |
| Touch | 50 µm | metal mesh on a film | the input, with no indium tin oxide in a bend | laminated with the same adhesive |
| Emissive stack | 20 µm | a flexible organic stack with a quantum dot colour layer | the light | a printed or a deposited stack on the backplane |
| Encapsulation | 30 µm | a multilayer barrier film | below 10⁻⁶ g/m²/day of water | the thin film encapsulation, with the edge seal |
| Backplane | 30 µm | polyimide with a thin film transistor array, the row drivers, and a copper row line for 144 Hz | the address | a laser lift off from the carrier glass |
| Backing | 120 µm | polycarbonate | stiffness and the neutral axis | bonded after the encapsulation |
| **The total per face** | **0.46 mm** | | | the spine of 0.06 mm and the weld of 0.04 mm are body parts, Part 3, Section 3.2 |

`[HYPOTHESIS]` gate MEC-2 measures the real stack. **A glass part anywhere in this stack is a defect**. `[DECISION]`

---

## 2.3 How a panel is made: the process route

| Step | The operation | The parameter | The defect it prevents |
|---|---|---|---|
| 1 | the backplane on a carrier glass, a polyimide coat, a laser lift off | polyimide 12 to 15 µm, a lift off fluence with a stated window | a cracked backplane |
| 2 | the thin film transistor array, the row and the copper column lines | a 50 µm pitch, a 144 Hz rate, a measured line resistance | a slow charging time, a smear |
| 3 | the emissive stack and the quantum dot layer | a blue emitter with a printed red and green conversion | a narrow colour volume, a short blue life |
| 4 | the thin film encapsulation and the edge seal | below 10⁻⁶ g/m²/day, a 0.10 mm seal border | a dark spot, a growing edge failure |
| 5 | the backing lamination and the neutral axis placement | the neutral axis inside ±10 percent of the stack middle | a cracked inorganic layer in a bend |
| 6 | the cut to the outline: the R 3.20 mm corner and the 12-edge softened rectangular prism silhouette | a laser cut with a cold assist, a radius tolerance of ±0.05 mm | a chipped corner, a short crack |
| 7 | the cover lamination, the touch lamination, the vacuum step | a 50 µm adhesive, a 40 °C vacuum, a 24 h cure | a bubble, a delamination |
| 8 | the plasma hard coat | a 10 µm deposition with a measured hardness and haze | a scratch and a finger polish |
| 9 | the driver bonding and the flex attach | an anisotropic conductive film or a laser weld | an open row, a broken flex |
| 10 | the calibration and the identity write | the panel brightness, the colour, the uniformity, the bow and warp; a signed identity | a panel that cannot be compensated at the hub |
| 11 | the ageing and the test | a 24 h burn in, a photograph at three greys, a grain check | an early failure reaching the line |

**The yield rule**. A panel that fails step 10 or 11 is a coupon, not a product; it goes to the bend and the drop test pool. `[DECISION]`

---

## 2.4 The seam, and the number that decides it

| The member | One pixel at the distance | A 0.12 mm bond line | The verdict |
|---|---|---|---|
| Leaf 160 at 30 cm | 50 µm | 2.4 px | visible: one panel per face |
| Leaf 160² at 40 cm | 50 µm | 2.4 px | visible: the seam sits in the wrap zone, where the tiles already part by 1.20 mm |
| Leaf 480 at 60 cm | 166 µm | 0.72 px | invisible |
| Leaf 1400 at 2.5 m | 416 µm | 0.29 px | invisible |
| Leaf 2800 at 4 m | 416 µm | 0.29 px | invisible |

**How a far seam is made invisible**. 1. A 0.10 mm seal border instead of 0.15 mm. 2. A 0.04 mm overlap at the bond line. 3. A 30 percent wider aperture on the two edge pixel columns, so the pair reads as one wider pixel. 4. A clear, index matched, low modulus bond medium. 5. An alignment of ±20 µm in x and y and ±0.1 degree in rotation. `[HYPOTHESIS]` gate DSP-3 measures the assembled line at the intended distance.

---

## 2.5 The brightness, the colour and the refresh

| The property | The carried members | The Leaf 480 | The Leaf 1400 and 2800 |
|---|---|---|---|
| Peak brightness, a 10 percent window | 1 500 nits | 1 200 nits | 1 000 nits |
| Full field brightness | 800 nits | 800 nits | 700 nits |
| Colour volume | 92 percent of Rec.2020 | 90 percent | 85 percent |
| Refresh | 144 Hz, variable to 1 Hz | 144 Hz, variable to 1 Hz | 120 Hz, variable to 1 Hz |
| Uniformity between parts | below 2 percent | below 2 percent | below 2 percent |
| Dark line at a seam | not applicable | below the threshold | below the threshold |

**How the uniformity is achieved**. The quantum dot layer is printed per panel. Each panel carries its own calibration in its identity record, and the hub compensates at the boundary. This is the mechanism behind the 2 percent rule. `[DECISION]`

---

## 2.6 The power model, and how each term is measured

```
P_display = area × luminance × APL / (the emitter efficacy × the optical efficiency)
P_address = lines × refresh × capacitance × the panel factor
P_hub     = the decoder, the local scene renderer and the reprojection unit
P_radio   = the link class of the session
```

| The case | Display | Address | Hub | Radio | Authority | The total |
|---|---|---|---|---|---|---|
| Leaf 160, a delta session at 144 Hz | 0.60 W | 0.20 W | 0.70 W | 0.40 W | 0.12 W | **2.02 W** |
| Leaf 160, a video session | 1.10 W | 0.25 W | 1.20 W | 0.60 W | 0.12 W | **3.27 W** |
| Leaf 160, a static page at 10 Hz | 0.15 W | 0.02 W | 0.10 W | 0.05 W | 0.03 W | **0.35 W** |
| Leaf 160, the safe screen, no link | 0.10 W | 0.02 W | 0.05 W | 0.00 W | 0.03 W | **0.20 W** |
| Leaf 160², a video session | 2.20 W | 0.50 W | 1.40 W | 0.60 W | 0.12 W | **4.82 W** |
| Leaf 1400, a video session at 30 percent APL | 60 W | 4 W | 6 W | 3 W | 0.5 W | **73.5 W** |

**How it is measured**. Use a calibrated luminance meter on standard images at 1, 5, 10 and 30 percent APL. Place a current probe on each rail after a 30 minute thermal soak. `[DECISION]` gate DSP-5.

---

## 2.7 The far members: how a Leaf 1400 is built

| Step | The operation | The rule |
|---|---|---|
| 1 | the tiles are bonded into columns of 20 | the bond line of Section 2.4 |
| 2 | the columns are laid on the rail | 35 rail segments, 40 cm each |
| 3 | the bus runs along the rail | the rail carries the corridor and the mount |
| 4 | the one continuous cover is laid over the face | a 0.15 mm polymer sheet, no seam visible from the front |
| 5 | the hub H3, the radio and the power input are fitted | a 4 to 9 W hub, 128 tiles maximum |
| 6 | the buffer cassette is fitted | it holds the session through a power cut |
| 7 | the calibration of every tile is read into the hub | the 2 percent uniformity rule |
| 8 | the mount plate is registered | one person, no tool, under two minutes |

**The mass of a Leaf 1400**. A 1 400 × 800 mm surface weighs **4.25 kg** (`0.9 kg` tiles, `1.4 kg` rail, `0.9 kg` cover, `0.9 kg` mount, `0.15 kg` hub). `[COMPANY]` A 65 in consumer panel surface of 2026 weighs 17 to 24 kg with its stand. Its panel rides on glass and a steel frame. `[GENERAL]`

**The heat rule**. No tile is covered by an insulating layer, and the bay has a vent path. A 73 W surface with 20 percent loss is 15 W over 11 200 cm², which is 0.0013 W/cm². Natural convection is enough.

---

## 2.8 The panel gates

| Gate | The test | The pass condition |
|---|---|---|
| DSP-1 | a P80 and a P160 panel: brightness, colour volume, lifetime estimate, bend at the class radius, 144 Hz | every value of Sections 2.5 and 2.6 |
| DSP-2 | the addressing power from 1 Hz to 144 Hz, and the copper row line | a measured curve, and the derating curve for a large surface |
| DSP-3 | the seam on a Leaf 480 and a Leaf 1400: the dark line, the luminance step, the alignment | invisible at the intended distance, alignment inside ±20 µm |
| DSP-4 | the tile replacement and the service time | under 15 minutes, and the uniformity test passes after the replacement |
| DSP-5 | the power model on a real Leaf 160, 160² and 1400 | each term measured, the total inside 10 percent |
| DSP-6 | the daylight legibility of the carried members | the stated contrast at 20 000 lux |
| DSP-7 | the variable refresh saving, 144 Hz to 1 Hz | the stated saving on a static page |
| DSP-8 | the bend durability of a Leaf 160 and a Leaf 160² | 10 000 cycles at the class radius, then 100 000, with a capacity, an image and a touch report |
| DSP-9 | the geometry manifest and the format change | a session moves between two members with no lost state and no stuck frame |
| DSP-10 | the cut quality of the R 3.20 mm corner and the r 0.80 mm softened rectangular prism edges, and the corner touch behaviour | a chip free cut, a working corner tap, and no false input from a diagonal grip |
