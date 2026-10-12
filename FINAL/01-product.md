# BUDLUM LEAF · THE DIRECTIVE · PART 1 · THE PRODUCT

---

## 1.1 The product law

1. A Budlum Leaf is a **surface that shows, a wallet that authorizes and a radio that connects**. `[DECISION]`
2. The body holds no processor, no operating system, no camera, no speaker, no headphone jack and no cooling part. The camera, the sound set and the jack live in the module. `[DECISION]`
3. The family shares one architecture across all sizes. A change of size is an order change, not a product change. `[DECISION]`
4. Each member name is **Budlum Leaf plus the size**. The catalogue names reference sizes, and the worn member is the Leaf Frame. `[DECISION]`
5. Device-class words (*phone*, *tablet*, *television*, *monitor*, *laptop*, *computer*, *VR headset*, *smart glasses*) never appear in claims, filenames or code. `[DECISION]`

**The acceptance test of the naming law**. A user says: "I use a Budlum Leaf." Calling the product by a device-class word is a defect of the product language.

---

## 1.2 The family

| The member | The geometry | The faces | The panel set | Density | The distance | ppd |
|---|---|---|---|---|---|---|
| **Leaf 80** | 80 × 80 mm | 2 | 2 × P80 | 508 ppi | 25 cm | 87 |
| **Leaf 160** | 160 × 80 mm | 2 | 2 × P160 | 508 ppi | 30 cm | 104 |
| **Leaf 160²** | 160 × 160 mm | 2 | 4 × P160 | 508 ppi | 40 cm | 130 |
| **Leaf 480** | 480 × 240 mm | 1 | 72 × T40 B | 152 ppi | 60 cm | 63 |
| **Leaf 1400** | 1 400 × 800 mm | 1 | 700 × T40 C | 61 ppi | 250 cm | 105 |
| **Leaf 2800** | 2 800 × 1 600 mm | 1 | 2 800 × T40 C | 61 ppi | 400 cm | 168 |
| **Leaf Frame** | a clear lens per eye | n.a. | 2 × a 4K class microdisplay | about 2 400 ppi | 20 mm | about 60 (Part 15, H-1) |
| The **Field** mode | a Leaf 160 or a Leaf 160² with a spacer | 2 | n.a. | n.a. | 20 mm | about 27 |

**The rule of the family**. A member is a count of panels or tiles, one bus, one or more cassettes and one hub. There is no second system. `[DECISION]`

**The size is an order parameter**. The reference sizes above are the catalogue classes, and the order fixes the number. The tooling band is a partner question, parked by the order of Ayaz. `[DECISION]`

---

## 1.3 The design language

| The property | The value | The reason |
|---|---|---|
| The corner radius (4 vertical edges) | **R = 6.35 mm** on Leaf 160 (`R 2.80 mm` on Leaf 80, `R 3.60 mm` on Leaf 240, `R 4.50 mm` on Leaf 480) | keeps a true rectangular screen (`11 947 mm²`) while removing sharp 90° corners |
| The 8 horizontal prism edges | **r = 0.80 mm radius transition** on all 4 front and 4 back perimeter edges | all 12 edges of the `4.00 mm` rectangular prism are softened for the hand |
| The upright B module edges | **r = 0.55 mm radius transition** on all 90° edges of the vertical bar and cylindrical ring | no sharp 90° edge on the `40.0 x 32.0 x 4.00 mm` top-edge module |
| The touch layer at the corner | the mesh follows the `R = 1.40 mm` screen corner with grip rejection along the `1.8 mm` bezel | a diagonal grip is not a swipe, and a corner tap still works |
| The finish | **mat polymer with an anti-fingerprint texture**; the hardness comes from the plasma coat, not from a gloss | the answer of Ayaz, question 13 |
| The colours | a deep black, a warm white, a sand, and one seasonal accent; no logo on the face | |
| The fasteners | none visible: the weld closes the body; the cassette and the module are the service paths | |
| The clear variant | the same outline in a clear or a smoky polymer with the clear panel of Part 7 | |

**The rule**. The form language is a property of the profile, so it holds at every size. `[DECISION]`

---

## 1.4 The panel law, in brief

| The panel | The geometry | The pixels | The density | The use |
|---|---|---|---|---|
| **P80** | 80 × 80 mm, 0.35 mm | 1 600 × 1 600 | 508 ppi at a 50 µm pitch | Leaf 80, the Frame lens, a control surface |
| **P160** | 160 × 80 mm, 0.35 mm | 3 200 × 1 600 | 508 ppi | Leaf 160, Leaf 160² |
| **T40 B** | 40 × 40 mm, 0.35 mm | 240 × 240 | 152 ppi | Leaf 480 |
| **T40 C** | 40 × 40 mm | 96 × 96 | 61 ppi | Leaf 1400, Leaf 2800 |

**The seam law**. Tiling is for the far members, and the near members use one panel per face. A seam is invisible when the bond line is narrower than one pixel at the viewing distance. `[DECISION]` Part 2, Section 2.4.

**The refresh law**. The carried members and the Leaf 480 run **144 Hz**, variable down to 1 Hz. The Leaf 1400 and Leaf 2800 run 120 Hz and 60 Hz. A 63 in surface at 144 Hz wastes energy on changes no eye reads. `[DECISION]`

---

## 1.5 The sharpness law

```
mm per degree = d × 0.01746        ppi = 25.4 / pitch_mm        ppd = (ppi / 25.4) × mm_per_degree
```

| The member | The distance | mm per degree | ppd | The verdict |
|---|---|---|---|---|
| Leaf 80 | 250 mm | 4.36 | 87 | premium |
| Leaf 160 | 300 mm | 5.24 | 104 | premium |
| Leaf 160² | 400 mm | 6.98 | 140 | beyond the eye |
| Leaf 480 | 600 mm | 10.47 | 63 | good |
| Leaf 1400 | 2 500 mm | 43.65 | 105 | premium |
| Leaf 2800 | 4 000 mm | 69.84 | 168 | beyond the eye |

**The hybrid rule (the answer of Ayaz, question 3)**. 1. The family standard is the **angular** reading: the surface is sharp for the eye at its intended distance, and it states the number. 2. A surface watched from one metre uses a denser grade. The order states the pixels, heat, power and panel class. 3. The **linear** reading is refused with its cost written. A Leaf 1400 at 508 ppi needs 466 Mp and 330 W of addressing. That is 56 times the pixels for a difference invisible at 2.5 m. `[HYPOTHESIS]` gate DSP-2 measures the addressing curve.

---

## 1.6 The format change law

1. The identity, the protocol, the permission set and the data location never change with the format. `[DECISION]`
2. **The edge coupler** joins two surfaces: power, ground, a two lane data link, and a mechanical registration inside 0.1 mm. It is the same part on every member.
3. **The dock tree**. A Leaf 160 docks to a Leaf 480 stand. A Leaf 160² docks to a Leaf 1400 rail as a second surface.
4. **The session moves, not the device**. A session binds to the user, and a surface change has a grace period. The old surface holds the last frame until the new surface acknowledges it.
5. **The geometry manifest** states the outline, panel map, grade, seam map, keep-out band, bend band, refresh range, modes, and calibration. It is signed and stored in B.U.D. A manifest without a bend band refuses a bend claim. `[TREE]`
6. **The count rule**. Two Leaf 80 members joined at the edge behave as one Leaf 160: one session, two panels, one bus. A user buys a panel, not a product. `[DECISION]`

---

## 1.7 The product boundaries: what a Budlum Leaf is not

| The expectation | The answer | The reason |
|---|---|---|
| "it must work with no network" | it works: the safe screen, the wallet, the local echo and the optical path. Everything else is a class, and the class is stated | the network is the product's second half |
| "it must run a program" | no. The device runs signed firmware only | rule L2, and the security model |
| "it must have a camera" | it has one, in the module, and only under a lease | Part 6, Part 11 |
| "it must be waterproof" | **IP67 is the claim, and IP68 is the target**. The dual-lip FKM collar on the continuous battery sheet seals the bottom slot with or without a module fitted (Q43) | Part 3, Section 3.5, and Part 18, Section 18.8 |
| "it must be repairable by anyone" | the panel, the cassette and the module are user replaceable; the weld is a workshop operation | Part 13, Section 13.6 |
| "it must hold a week" | it holds what the configuration and the session class give, and the surface states both | Part 4, Section 4.5 |

---

## 1.8 The step-by-step of a first product definition

The procedure that turns this part into a product brief, in the order it is done. `[DECISION]`

| Step | The action | The output |
|---|---|---|
| 1 | choose the member (default: Leaf 160) | the geometry line of the brief |
| 2 | choose the cassette fill (default: Feather) | the energy line |
| 3 | choose the module state (none, camera and battery) | the mass and the runtime lines |
| 4 | copy the panel law of Section 1.4 | the panel specification request |
| 5 | copy the sharpness law of Section 1.5 | the distance and the density claim |
| 6 | copy the design language of Section 1.3 | the industrial design brief |
| 7 | copy the answer log of Part 0, Section 0.5 | the constraint list |
| 8 | write the manifest of Section 1.6 | the signed geometry record |
| 9 | attach the gate list of Part 12 | the acceptance sheet |
| 10 | hand the brief to the three lines of Part 14 | the work orders |
