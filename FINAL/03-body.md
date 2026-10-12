# BUDLUM LEAF · THE DIRECTIVE · PART 3 · THE BODY

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. The body is `128` rotating PC-capped tiles with `508 ppi` micro-LED layers and lattice-continuous seams. It stretches `25 %`, and `41 %` at most.

---

## 3.1 The mass theorem

**Every gram that is not display, not energy, not radio or not anchor is a design error**. `[DECISION]`

**The theorem of revision A, kept as the record**. `M = 9 g per 100 cm² + 2.9 g per Wh + 7.5 g`. **It is superseded by the 4-Quadrant (`+`) budget of `HARDWARE/17`**. Four `40 x 80 x 2.00 mm` (`17.0 g`) polycarbonate screen-battery quadrants (`Q1..Q4`) total **68.0 g** (`12.0 Wh` `LLZO/PEO` solid-state). The `90°`-bent-stem B module adds **20.0 g** (**88.0 g** complete). `[DECISION]`

| The configuration | The mass | The energy, delivered | Active session (`0.85 W` Zero-CPU draw) |
|---|---|---|---|
| **Single Quadrant Tile (`Q1..Q4` / Leaf 80)** (`40 x 80 x 2.00 mm`, `ISO 10993` PC + `LLZO`) | **17 g** | **`3.0 Wh` (`800 mAh`) solid-state + `Ø22 mm` Qi coil** | **3.5 h** (or eyewear module) |
| **Leaf 160 4-Quadrant (`+`) screen-battery body** (`80 x 160 x 2.00 mm`, `4 x 17 g`) | **68 g** | **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) + `Ø54 mm` Qi2.2** | **>14.1 h** (portless wireless body) |
| **Leaf 160 complete (`4-Quadrant body + 90°-bent-stem B module`)** | **88 g** | **`12.0 Wh` body + `0.45 Wh` B bridge (`3 320 mAh`)** | **>14.1 h** |
| **Leaf 160 on the legacy cassette reference line** | **78 g** with the Feather cassette, **92 g** with the Standard | 16 Wh and 20 Wh | 7.9 h and 9.9 h |
| A carried surface of 2026, the same area | 190 to 230 g | 19 to 22 Wh | 6 to 9 h |

**The rule**. A mass figure belongs to a configuration, and the configuration names its energy part and its seated parts. The sentence "the device weighs X" without the sheet, the cassette and the part state is forbidden. `[DECISION]`

**The rule**. A mass figure belongs to a configuration. The sentence "the device weighs X" without the cassette and the module state is forbidden. `[DECISION]`

### 3.1.1 Where the mass went, and why the figure fell

| The part | A carried surface of 2026 | A Leaf 160 4-Quadrant (`+`) Body | The saving, in the Revision L.5.0 comparison |
|---|---|---|---|
| Cover glass 0.6 mm | 17 g | 12.8 g (`8 x 0.20 mm` `ISO 10993` PC) | shatterproof medical-grade optical polycarbonate |
| Metal frame or midframe | 20 to 30 g | 3.9 g (`(0,0)` Ti hub + `8` Ti pins + `24` N52H) | `<15 µm` (`n = 1.585`) zero-scratch `+` seam and Ti micro-dovetail locks |
| Board, processor, shields, spreader | 25 to 40 g | 3.4 g graphene/Mu-metal (`3.8 g` PCBA in B ring) | Zero CPU and Zero RAM; `U1` Master TCON + `U2` `UWB/mmWave` SiP in B ring |
| Camera island | 3 to 8 g | 0 in the body | the camera is in the flat ring of the `90°`-bent-stem B module (`20 g`) |
| Speaker, haptic parts | 3 to 6 g | 0 in the body | the sound set and sole `USB Type-C` port are in the `90°`-bent B module |
| Internal battery inside screen | 50 to 58 g | **34.4 g (`4 x 8.6 g` `LLZO/PEO` cells)** | `4 x 3.0 Wh = 12.0 Wh` non-flammable solid-state cells (`EU 2023/1542` `<3 s` swap) |
| T-OLED panels, PDLC, AgNW/ITO, Qi2.2 coils | 14 to 20 g | 17.5 g | dual T-OLED (`6.8 g`), OCA (`1.6 g`), PDLC (`1.9 g`), AgNW (`1.6 g`), `Qi2.2` (`5.6 g`) |
| **The total** | **190 to 230 g** | **68 g** 4-Quadrant body (**88 g** complete) | the reading of the detailed pass of `HARDWARE/17` |

---

## 3.2 The body stack, from the outside in

```
face A: coat 0.01 + cover 0.15 + adhesive 0.05 + touch 0.05 + panel 0.10 + backing 0.10 = 0.46 mm
core:   the cassette 2.88 mm, in the bay
face B: the same 0.46 mm
spine:  0.06 mm shared at the edges and the wrap zone
seal and weld: 0.09 mm at the perimeter
        -----------------------------------------------
        the closed body: 4.00 mm  (the answer of Ayaz, K1)
```

| The part | The value |
|---|---|
| The leaf alone | 4.00 mm |
| The cassette | 2.88 mm, fixed |
| The module | 4.00 mm |
| The attached stack | 8.00 mm, and every claim names the part |
| The visible edge | a 0.9 mm bead at the weld |
| The bend | the wrap circle is **R 25.5 mm** and the gentle bend is **R 70 mm** and free. There is no hinge and no crease line |

---

## 3.3 The spine: one laminate, five jobs

| Layer | The thickness | The material | The job |
|---|---|---|---|
| Carrier | 60 µm | 301 stainless steel, perforated to 40 percent open area inside the wrap zone | stiffness where it is flat, no stiffness in the wrap |
| Conductor | 18 µm | copper | power and the video lane reference |
| Dielectric | 12 µm | a bend rated polyimide | insulation |
| The antenna windows | openings | through the laminate, one per antenna | the radio passes the metal |
| The anchor pattern | a 0.4 mm pole pitch | in the steel | the module and the mount hold |

**How it is made**. 1. The steel is etched with the perforation and the anchor pattern in one pass. 2. The copper is laminated and etched to the bus pattern. 3. The polyimide is bonded. 4. The laminate is cut to the edge profile with the R 3.20 mm corner. 5. The windows are punched. 6. The wrap zone is formed to R 25.5 mm and relaxed. 7. The continuity and the resistance of every lane are tested. The mass is 0.85 g per 100 cm², so 1.1 g in a Leaf 160. `[HYPOTHESIS]` gate MEC-5.

---

## 3.4 The bend, and the slip rule

1. The layers are **not bonded into one beam** across their whole area. Each layer bends about its **own** thin axis, and the interfaces shear by design.
2. **The numbers**. No interface sees more than **0.4 to 0.8 MPa of shear**. Each interface carries **0.35 to 0.6 mm of slip at R 25.5 mm**. `[HYPOTHESIS]` gates B-5 and B-6 measure both.
3. **Why it is required**. A bonded 4.00 mm stack at R 25.5 mm puts **7.8 percent** on its outer fibre. Nothing in this program survives that. Decoupled, the worst layer is the panel tile at **0.63 percent**.
4. **How the slip is built**. The layers register at the ends, and each interface carries a low-modulus silicone slip film. The 4 continuous polymer-gel battery layers slide over 3 `50 µm` silicone interlayers.
5. **The failure modes to watch**. Watch creep at 60 °C over 1 000 hours and film wicking into the display gap. Also watch foreign particles and interlayer wear over 10 000 wraps. Each has a test in gates B-5, B-6 and B-1.

---

## 3.5 The edge, the seal and the impact

| The property | The value | The how |
|---|---|---|
| The edge | an ultrasonic weld of the two polymer covers at a 1.5 mm land, a 0.4 mm bead | a horn at 20 kHz, a pressure and a hold time with a stated window, and a pull test on a sample from every shift |
| The class | **IP67 is the claim, and IP68 is the target**, measured with a module fitted and with none | a two bead gasket on the energy sheet carrier, a sealed connector, a labyrinth at the module contacts and the vent membrane of gate MEC-24 |
| The old refusal, withdrawn | the earlier revision refused IP68, because a bay with a lid and a water tight body are contradictory. **The energy sheet has no bay and no lid: the carrier is the seal**. The refusal is therefore withdrawn (the audit F-08) | route A+ of Part 17, Section 17.6, and gate MEC-19 |
| The impact | 78 g at 1.2 m is 0.9 J | the cover is the impact layer, the spine carries the load to the weld, the cassette floats on a 0.2 mm elastic land |
| The drop set | 6 faces, 1.2 m, concrete, with a cassette and with a module | gate MEC-4, with a damage report per face |

---

## 3.6 The cassette bay, mechanically

| The element | The specification |
|---|---|
| The bay | a 2.88 mm slot inside the outline, with a 0.2 mm elastic land and a lead-in chamfer |
| The slide | one straight motion at the fixed edge, 18 mm of travel, no tool, target below 15 s |
| The contacts | 8 spring contacts, wiped and released on the slide, plus 2 sense lines, gold on gold |
| The latch | a polymer snap with a magnetic assist and a secondary mechanical catch, rated 1 000 cycles |
| The gasket | a 0.5 mm lip seal, replaced with the cassette service interval |
| The detection | the device reads the cassette identity at the first contact and *before* it enables the power path |

**The rule of the first contact**. A cassette is identified before it is used, and a cassette whose record fails is refused with the failing field on the surface. `[DECISION]` Part 4, Section 4.4.

---

## 3.7 How a Leaf 160 is assembled: the line procedure

| Step | The operation | The parameter | The check |
|---|---|---|---|
| 1 | the panel pair arrives calibrated with its identity | the calibration hash | the identity read |
| 2 | the spine is bonded to face A and face B at the edge zones | a 20 s press at 80 °C | the pull test on a sample |
| 3 | the bus is connected and the hub is placed in the keep-out band | a 1 mm alignment window | the continuity and the enumeration |
| 4 | the two faces are brought together with the cassette bay former in place | the bay former is a 2.88 mm gauge | the slot gauge per unit |
| 5 | the ultrasonic weld closes the perimeter | the horn window, a bead of 0.4 mm | a bead photograph and a leak test on a sample |
| 6 | the cassette is fitted and identified | the record read and verified | the power path enabled |
| 7 | the module is fitted, if ordered | the anchor force and the contact wipe | the module record and the antenna check |
| 8 | the full function test and the calibration | the screen, the touch, the radio, the radio frequency power, the bend | the test record |
| 9 | the ageing: a 2 h burn in at 45 °C with a moving image | the temperature and the current | the defect screen |
| 10 | the packing and the record upload to B.U.D. | the serial, the cassette, the module, the panel identities | the manifest signed |

**The yield rule**. A unit that fails step 8 twice goes to the teardown pool, and the failure is written into the record. `[DECISION]`

---

## 3.8 The user service procedures, written for a person

| The task | The tool | The time | The rule |
|---|---|---|---|
| Replace the cassette | none | below 15 s | the device is powered down by the latch event, or stays alive on the buffer capacitor for a stated time |
| Replace the module | none | below 10 s | the session keeps the state on the validator |
| Replace the panel | the kit tool and the guide | 20 to 30 min | the panel is a field replaceable unit; the corner alignment uses the two registration pins |
| Replace the battery cells | no; the cassette is the unit | n.a. | a cell swap inside a cassette is a workshop operation, and the gauge record makes an unauthorized swap visible |
| Replace the pen | none | n.a. | the pen pairs again through the module |

**The five year rule**. Spare parts are held for at least five years after the last sale of a member, and the parts list is public. `[DECISION]` (the answer of Ayaz, question 34 and the European removability rule.)

---

## 3.9 The body gates

| Gate | The test | The pass condition |
|---|---|---|
| MEC-1 | the bend durability: a bonded stack against a decoupled stack, at R 25.5 mm and at R 70 mm | the stated cycles, the measured pair, and no interface wicking. B-1 and B-2 carry the product claim |
| MEC-2 | the mass of a real Leaf 160, part by part | inside 10 percent of the law of Section 3.1 |
| MEC-3 | the cassette: the removal time, 1 000 cycles, the contact resistance, the record | below 15 s, no damage, the record complete |
| MEC-4 | the drop set | a working surface, with a damage report |
| MEC-5 | the spine: stiffness, heat spread, the antenna windows, the anchor force | every value stated |
| MEC-6 | the charge heat and the power ceiling at 10, 25, 45, 60 and 80 W, seated and removed | the derating curve, a surface inside the safety limit |
| MEC-7 | the seal class and the dust behaviour: **IP67 claimed, IP68 as the target**, with a module fitted and with none | the class claimed is the class measured, and gate MEC-19 owns the number |
| MEC-8 | the radio set: the free hold, the hand hold, the desense, the module gain, the match flat and bent | every budget of Part 5, Section 5.3 |
| MEC-9 | the energy accounting on a real device | each term measured, the total inside 10 percent |
| MEC-10 | the pen: the attach, the charge, the latency, the pressure, the magnet effect on the antenna | the numbers of Part 6, Section 6.6, and no radio penalty |
| MEC-11 | the module thermal path: the spreader, the interface pad, the latent buffer at 35 °C ambient | the module rise, the leaf rise and the cell temperature inside their limits |
| MEC-12 | the capture policy: a hot start, a long take, a cooldown, the message | the refusal works and the user sees the reason |
| MEC-13 | the soft corner: a diagonal grip on 20 users, in a pocket, a hand and a bag | no accidental input, and no corner tap missed |
