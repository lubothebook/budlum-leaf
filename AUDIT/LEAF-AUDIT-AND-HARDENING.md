# LEAF AUDIT AND HARDENING ORDER

**Date:** 2026-10-05. Updated 2026-10-12 for Revision L.5.0 (`80 x 160 x 2.00 mm`, `68 g` body, `20 g` B module, `88 g` total). All findings F-01 to F-15 are closed in `FINAL/` and `HARDWARE/`.
**Audited:** the workspace archive `workspace-01a10db2` (state: Revision K -> closed in Revision L.5.0). The main files are `LEAF/BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md` and `LEAF/FINAL/00` to `20`.
**Place this file in:** `LEAF/AUDIT/`.
**Writing standard:** ASD-STE100. Use the same standard for all fixes.
**Evidence tags:** the tags of the audited files (`[DECISION]`, `[PUBLICATION]`, `[COMPANY]`, `[TREE]`, `[HYPOTHESIS]`, `[GENERAL]`).

---

## 0. Scope and Method

**What was read in full**: Parts 0, 15, 16, 17, 18, and `MASTER/STATE.md`.

**What was checked by search and calculation**: Parts 1 to 14 (density, strain, thickness, IP class, gates, patents, crazing, screens, sizes, and style).

**What was not checked**: SVG sheets (`P01` to `P08`), `check_sheets.py`, `check_widths.py`, and Parts 2, 3 and 6 line by line. Do a second pass on these three parts. They hold the polycarbonate stack and the module.

**Limit of this audit.** No gate has data. Every number in the files is a plan. This audit finds errors in the plan. It does not prove the product.

---

## 1. What Is Strong

1. The claim policy: a claim needs a gate, a raw data set and a date. Keep it.
2. The hardening pass (Part 15) found real errors in the earlier text and published them. Keep this habit.
3. Part 17 matches Ayaz's aim: a full-area body energy layer, removable in one tool-free motion.
4. Part 18.2 and 18.4 state the true limit: a validator cannot send photons. The ledger of five terms is clear.
5. The EU route (A+, the removable sheet) is the right answer to Article 11 of Regulation (EU) 2023/1542. `[PUBLICATION]`

---

## 2. Findings

Severity: **S1** a wrong physical claim. **S2** a conflict between two parts. **S3** an Ayaz decision that is missing from the files. **S4** a writing standard fault.

| ID | S | Where | Finding | Fix |
|---|---|---|---|---|
| F-01 | S1 | Part 4.2, Part 17.3 | The Energy Sheet uses 900 Wh/L for tiles of 0.6 mm to 2.28 mm. Evidence for flexible cells is far lower (Section 3). | Section 3 |
| F-02 | S1 | Part 18.7.1 | The strain formula is wrong by a factor of 2. | Section 4 |
| F-03 | S1 | Part 18.7.2 | "The stack in the crease is under 150 µm" is true for one face only. The body has two faces. | Section 4 |
| F-04 | S1 | Part 18.7 | A fold at R 2.0 mm with 100 000 cycles gives 5.5 percent strain at the hard coat. No proof exists for polycarbonate at this strain. | Section 5 |
| F-05 | S2 | Part 4.2 and Part 17.3 | The same 1.82 mm tile layer gives 20 Wh in Part 4.2 and 18.0 Wh in Part 17.3. | Use one value. |
| F-06 | S2 | Part 16.1 | The text says 35 items (11 B, 18 M, 6 m). The table has 39 items (13 B, 19 M, 7 m). | Correct the count. |
| F-07 | S2 | Part 12, Part 15 H-3 | The gate count is 90 in Part 12 and 103 in H-3. Gates were added after H-3 (MEC-15 to MEC-22, ENR-7, ENR-8, DSP-11, DST-9, DST-10). The count is now at least 105 for device and network. | Recount. One count only. |
| F-08 | S2 | Part 3.5, claim table, MEC-7, ENR-8 | These say IP54 and "IP68 is refused". Part 17.6 to 17.7 and Part 18.8 say IP67 with IP68 as a target. | Update the old parts. Keep one class for one claim. |
| F-09 | S2 | `STATE.md`, Part 0.5, Part 17.5 | The closed decisions say "160 by 80 mm by 4.00 mm". Part 17.5 says 4.00 mm is the maximum envelope, not the target. | Rewrite the closed decisions. |
| F-10 | S2 | `BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md` | Part 14 sits after Part 18. | Move it to its place or rename it. |
| F-11 | S3 | All files | The second screen and the backup screen (the Duo use) are missing. | Section 7 |
| F-12 | S3 | Part 1, Part 13 | Custom size and shape: only the word "parametric" exists. No rules. | Section 8 |
| F-13 | S3 | `FINAL/*` | No patent screen. The word "patent" does not appear in Parts 0 to 18. | Section 9 |
| F-14 | S3 | Part 15, Part 18 | The crack and break hardening misses six tests and a bend guard. | Sections 5 and 6 |
| F-15 | S4 | All files | 108 em dashes (52 in v5). In the v5 prose, 47 percent of the sentences have more than 25 words and 78 have more than 40 words. Ayaz asked for STE and no em dashes. | Section 10 |

---

## 3. Energy Density of the Energy Sheet (F-01)

**What the files say.** The sheet is a tiled layer of rigid cells with flexible bridges. The nameplate uses 900 Wh/L. The effective energy is 0.8 times the nameplate. A delta session needs 2.02 W. `[HYPOTHESIS]`

**What the evidence says.**
- Bendable lithium batteries on sale: cell thickness 0.4 mm to 0.7 mm, 100 Wh/L to 200 Wh/L. `[PUBLICATION]`
- Research textile lithium battery: 120 Wh/L to 460 Wh/L. `[PUBLICATION]`
- The text of Part 4.2 gives 700 Wh/L to 950 Wh/L for "a 2026 flagship cell". Such cells are rigid and several millimeters thick. Thin 0.6 to 1.0 mm layers lose density because foil, separator and tabs take a larger volume share. `[GENERAL]`

**The effect on the run time** (the model of the files: effective = 0.8 times the nameplate, 2.02 W):

| Cell density | Sheet 60 | Sheet 100 | Sheet 182 | Sheet 228 |
|---|---|---|---|---|
| 150 Wh/L | 0.4 h | 0.7 h | 1.2 h | 1.5 h |
| 200 Wh/L | 0.5 h | 0.9 h | 1.6 h | 2.0 h |
| 450 Wh/L | 1.2 h | 2.0 h | 3.6 h | 4.5 h |
| 600 Wh/L | 1.6 h | 2.6 h | 4.8 h | 6.0 h |
| 750 Wh/L | 2.0 h | 3.3 h | 5.9 h | 7.5 h |
| **900 Wh/L (the files)** | 2.4 h | 3.9 h | 7.1 h | 8.9 h |

**Required fixes.**
1. Mark the 900 Wh/L value as the upper limit of the study. Do not use it as the base case.
2. Add 150, 450 and 600 Wh/L samples to gate ENR-2. Today ENR-2 tests 750, 900 and 1 000 Wh/L only.
3. Show the run time table of Part 17.3 as a range: one column for each density. A product claim uses the measured column only (claim policy, Part 12).
4. The sentence "Sheet 228 holds 13 percent more energy than today's cassette" depends on the 900 Wh/L value. Remove it or add the condition.
5. Compare the tile and bridge sheet with a bendable thin-cell sheet. Both are candidates. Keep the better one after ENR-1 and ENR-2.
6. Check the tile gap. The text says "a 3 mm pitch with 1.5 mm free bridges" and "the bridge area is about 12 percent". For bending in one direction, the gap fraction is about t/R (1.82 mm / 25 mm = 7 percent). For a twist or a saddle shape, the gaps open in two directions and the loss is larger. State the bend directions that the 12 percent covers.
7. Check the tile facets. A rigid tile of length L on a curve of radius R tilts by L/R radians. A tile of 20 mm at R 25 mm tilts by 46 degrees. The face stack above it must follow a polygon. State L, the facet angle and the effect on the display surface.

---

## 4. Strain Formula and the Crease Stack (F-02, F-03)

**The error.** Part 18.7.1 says "a layer at t from the neutral axis sees t/(2R)". The correct formula is:

```
strain = d / Rn
d  = distance of the layer from the neutral axis
Rn = radius of the neutral axis
```

The form `t/(2R)` applies only to the outer fiber of a thickness-`t` plate at `t/2` from the axis. The files use the right form in Part 4.3 (the cell thickness) and the wrong form in Part 18.7.1.

**Corrected values at Rn = 2.0 mm** (the files give half of these values):

| Distance from the axis | Files | Correct |
|---|---|---|
| 50 µm | 1.25 percent | **2.5 percent** |
| 110 µm (hard coat of a thinned face) | 2.75 percent | **5.5 percent** |
| 230 µm | 5.75 percent | **11.5 percent** |

**The crease stack, layer by layer** (Part 18.7.2 layers, with a 40 µm thinned panel and mid-plane neutral axis):

| Layer | Outer edge from the axis | Strain at Rn = 2.0 mm |
|---|---|---|
| Backing (25 µm) | 45 µm | 2.25 percent |
| Adhesive and touch (50 µm) | 70 µm | 3.5 percent |
| Cover (30 µm) | 100 µm | 5.0 percent |
| Hard coat (10 µm) | 110 µm | **5.5 percent** |

**Two faces.** One face in the crease is 155 µm thick. The body has two faces and a spine of 60 µm. The crease is 370 µm thick if the faces are bonded. The outer surface is then 185 µm from the mid-plane. The strain is **9.2 percent**. For 0.5 percent strain at this surface, the radius must be 37 mm. For 1 percent it is 18.5 mm.

**Required fixes.**
1. Correct the formula in Part 18.7.1. Recompute the table.
2. Change "the stack in the crease is under 150 µm" to "one face is under 160 µm". Add the two-face value.
3. State if the two faces are bonded or free in the crease. When free, each face bends around its own axis with end slip of `pi` times the axis spacing. Write the slip value and the slot that allows it.
4. Put every inorganic layer (the barrier, the thin-film encapsulation) at the neutral axis. At Rn = 2.0 mm, a layer 10 µm away sees 0.5 percent. `[GENERAL]` Crack onset strain of inorganic barrier layers is 0.3 to 1 percent in most reports. Verify with the barrier supplier. `[PUBLICATION]`
5. Do not use ITO for the touch layer in the crease. Use silver nanowire or metal mesh. `[GENERAL]`

---

## 5. Hardening of the Fold and the Bend (F-04, F-14)

### 5.1 Strain budget for each layer

The values are limits for 100 000 cycles. They have the tag `[HYPOTHESIS]` until a supplier or a coupon test confirms them.

| Layer | Allowed strain | Rule |
|---|---|---|
| Polycarbonate cover, bulk | 1 percent | The yield strain in a tensile test is higher. Crazing and fatigue set the cyclic limit. |
| PI or CPI backplane | 3 percent | Place the neutral axis at the TFT layer. |
| Inorganic barrier | 0.3 percent | Place within 10 µm of the neutral axis. |
| Touch layer (silver nanowire or mesh) | 3 percent | Do not use ITO. |
| Hard coat | 1 percent for a rigid type, 3 percent for a flexible hybrid type | Choose the flexible hybrid type for any layer that bends below R 25 mm. |
| Copper bridge in the cell field | 0.2 percent | Use rolled annealed copper in a serpentine shape. Calculate the strain in the copper, not in the carrier. |
| Cell tile | 0 percent | A tile never bends. It sits between bridges. |
| Adhesive | 50 percent | Check creep and stress relaxation over 1 000 hours at the bend radius. |

### 5.2 Staged fold target

The files go straight to R 2.0 mm and 100 000 cycles. The corrected strain makes this a research aim. Use stages. Each stage has its own gate and its own claim.

| Stage | Radius | Cycles | Claim after the pass |
|---|---|---|---|
| S1 | 8 mm | 100 000 | "bends to 8 mm" |
| S2 | 5 mm | 100 000 | "bends to 5 mm" |
| S3 | 3.5 mm | 100 000 | "bends to 3.5 mm" |
| S4 | 2.0 mm | 100 000 | "folds closed" (the present aim) |

**Rule.** The product claim is the radius of the last stage that passed. A bend guard (Section 5.5) limits the radius to the proven value.

### 5.3 Polycarbonate-specific risks

| Risk | Why it matters | Control |
|---|---|---|
| Environmental stress cracking | Polycarbonate crazes when it is under strain and meets certain chemicals. `[GENERAL]` | Test the cover under strain with skin oil, sunscreen, hand cream, alcohol wipes, cleaning sprays, the adhesive and the electrolyte vapor. |
| Notch effect at a cut edge | A laser-cut or knife-cut edge holds small flaws. A crack starts there. | Polish or flame-treat the edge. Test the edge under bend. Round the corner (the 32 mm corner helps). |
| Thermal expansion mismatch | Polycarbonate expands about 65 ppm/K to 70 ppm/K. PI and the barrier layers expand much less. `[GENERAL]` | Measure the curl and the delamination after 500 cycles of -20 °C to 60 °C. |
| Creep under a long static bend | A body held at a curve for weeks relaxes and keeps a set. | Hold at the bend radius for 1 000 hours. Measure the set and the strain in each layer. |
| Moisture uptake | Dimensions change with humidity and the stack curls. | Measure at 85 °C and 85 percent relative humidity. |
| UV yellowing | The cover loses clarity. | Use a hard coat with a UV absorber. Test in a light chamber. |
| Hard coat adhesion | The hard coat peels at the fold. | Cross-cut tape test after the fold cycles. |

### 5.4 Test matrix

All numbers have the tag `[HYPOTHESIS]`. Ayaz and the verification line confirm them. Use at least 30 coupons for each fatigue condition and report the failure statistics (Weibull).

| Test | Condition | Pass condition |
|---|---|---|
| Static bend | 1 000 hours at the stage radius, 23 °C and 60 °C | No crack, no delamination, set under 2 mm per 100 mm |
| Dynamic bend | The stage cycles in Section 5.2 at 23 °C and 40 °C | No broken line, pixel loss under the stated limit, capacity inside 5 percent |
| Cold bend | The stage radius at -10 °C, 1 000 cycles | No crack in the cover or the hard coat |
| Reverse bend | The wrong direction, 1 000 cycles at the stage radius | No crack. The bend guard must stop the user earlier. |
| Twist | A stated angle over 150 mm, 10 000 cycles | No crack, tiles unharmed |
| Point load | Pen drop and ball drop on the bent state and the flat state | No crack, no dead pixel line |
| Pinch | A stated force on a fold edge | No crack, no short |
| Abrasion then bend | Steel wool or sand abrasion, then 10 000 bends | No hard coat crack that grows |
| Chemical and strain | Section 5.3, at 1 percent strain for 24 hours | No craze in polarized light |
| Thermal shock | -20 °C to 60 °C, 500 cycles, flat and bent | No delamination, seal unharmed |
| Seal after the bend | IP test after the full bend cycles and after 1 000 slip cycles | The IP class holds |
| Drop | 1.2 m on a hard floor, six faces, with and without the module | No crack, the session resumes |

### 5.5 Crack detection and bend guard

**Detection.** Use five methods on every coupon, before and after each test:
1. Optical microscope at 50 times, with polarized light for crazing in polycarbonate.
2. A daisy chain of the conductors, read during the test (a rise of 10 percent in resistance stops the test).
3. A luminance map of the panel (dead lines, dark spots).
4. A water vapor test of the barrier (a calcium test or an equal method) after bending.
5. Ultrasound or CT for delamination in the body and for tile damage.

**Bend guard.** A product must not rely on the user. Add three parts:
1. **A mechanical limit.** The spine (the perforated carrier) stops the bend at the proven radius.
2. **A strain mesh.** A printed conductive-ink line in the cover reads the strain. The hub reads it with the tile temperature sensors.
3. **A bend log**. The hub logs bends and over-bends to the signed part record. The user sees a warning at the limit. Service can read the log. `[HYPOTHESIS]` Gate MEC-23 (new).

### 5.6 Cell and body risks that the bend tests do not cover

| Risk | Why it matters | Control |
|---|---|---|
| Silicon-carbon cells swell during life | A silicon anode changes volume. `[GENERAL]` A laminated and sealed body of 2 mm to 4 mm pushes on the panel. | Add a soft compliance layer. Measure the swelling at 500 cycles and the pressure on the panel. New gate ENR-9. |
| A sealed body with no vent | A cell that vents gas in an IP67 body can open the weld or the panel. | Add a controlled vent path, a membrane that lets gas out and keeps water out. Test with a forced cell failure. New gate MEC-24. |
| Copper bridge fatigue | The bridges bend at every curve. | Serpentine shape, rolled annealed copper, S-N data at the real strain. |
| Weld and tab fatigue | A weld at a bridge is a stress point. | Pull test after the bend cycles. |
| A short at the crease | A bent edge can press a foil through a separator. | Insulating guard layer at the crease, and a short test after folding. |
| Gasket compression set | A gasket loses force with time and cycles. | Measure the seal at 1 000 cycles and after 1 000 hours of compression. |

---

## 6. Requirement From Ayaz: No Break, No Crack

Ayaz asked that the body does not break or crack when it is bent. The files use the right words in Part 18.7.3 ("no broken line, no pixel loss beyond the limit, no delamination"). Make three changes:

1. Replace every "does not break" sentence by the pass condition and the test name. A public claim says "passed S3 at 3.5 mm, 100 000 cycles, 23 °C". Do not write "unbreakable".
2. State the crease honestly. A crease can show after many folds (Part 18.7.3 already does).
3. State what is excluded: sharp folds below the proven radius, cuts, punctures, crushes and unlisted chemicals.

---

## 7. Second Screen and Backup Screen (F-11)

**The decision of Ayaz**. The second face serves as both second screen and backup screen, like a dual-screen Surface Duo device. The files have two panels with the same specification (Part 18.9) but no use rule for the second face.

**Add a part "Duo mode" with these rules.**

| Mode | What the second face does | Rule |
|---|---|---|
| Backup | It stands by. It takes the session when the first face fails or is off. | Takeover in less than 1 s `[HYPOTHESIS]`. The session id stays the same. |
| Second screen | It shows its own page set, for example a companion page, a note, a camera view or a second app. | The hub drives two scanouts. Each face has its own permission set (gate G-I2 style). |
| One face only | The other face is off. | Default. Saves the photon energy of the second face. |

**Takeover triggers (Backup).** A dead panel line count over a limit. A touch failure. A crack detected by the strain mesh (Section 5.5). A face pressed against a surface. A user command.

**Face in use.** The device knows which face the user looks at. It uses the motion sensor, the touch pattern and the grip. The other face dims or turns off. A palm on the back face is rejected.

**Wallet and privacy.** A wallet approval appears only on the face in use. The single-matrix design (one image readable from both sides) stays refused (Part 18.9).

**Energy.** The second face adds up to 0.6 W for the photons (Part 18.2). Add a run time line for "two faces on".

**Glasses.** The outer face of a Frame lens is the same second and backup screen. The inner face is the near-eye optics (Part 7, H-1). A flat panel placed directly at the lens plane cannot be focused by the eye. The inner image needs optics.

**Camera module.** It attaches to either face. The hub knows which face. `[DECISION]`

**New gates.**

| Gate | Subject | Pass condition |
|---|---|---|
| DUO-1 | Takeover time and session continuity | Under 1 s, no session loss |
| DUO-2 | Face in use detection | Right face in 99 percent of 1 000 handling cases `[HYPOTHESIS]` |
| DUO-3 | Power in each mode | A table: one face, two faces, backup stand-by |
| DUO-4 | Palm rejection | No false touch from the back face |
| DUO-5 | Wallet prompt placement | The prompt never shows on the face not in use |
| DUO-6 | Heat with two faces on | The surface temperature stays inside the limit of Part 11 |

---

## 8. Custom Size and Shape (F-12)

**The decision of Ayaz.** The user or designer chooses the size. This includes devices and glasses. The files say "parametric size". Add rules.

| Rule | Content |
|---|---|
| Parameters | Width, length, corner radius, curve class, number of faces, tile grid, outline. |
| Limits | The panel maker's design rules set the limits: minimum and maximum size, aspect ratio, distance of the cut line to the active area, corner radius. An OLED panel cannot be cut after it is made. The outline is fixed at the cut stage. A user cannot cut a Leaf. |
| Battery | Use a standard tile grid (a tile of 20 mm by 20 mm is a start value `[HYPOTHESIS]`). Any outline gets a tile layout. The energy follows the tile count. The bridge rule of Part 4.3 applies to every tile row. |
| Scaling | The antenna count, the hub class and the heat path follow the size class. Write a table of size classes with the limits. |
| Geometry manifest | The configurator creates a signed geometry manifest (Part 1.6). The manifest checks the limits. An outline outside the limits is refused. |
| Glasses | A lens outline is cut from a prescription blank. The waveguide has a fixed aperture, so the lens outline must keep the aperture inside. The frame, the interpupillary distance and the prescription range are inputs. |
| Cost | A custom outline needs a new cut program and a new tile layout. State the minimum order. Do not state a price (Part 15, H-13). |

**New gates.**

| Gate | Subject | Pass condition |
|---|---|---|
| SZ-1 | Limits table | The panel maker confirms the limits in writing |
| SZ-2 | Tile layout | Three test outlines get a valid layout and pass the bend test |
| SZ-3 | Manifest check | A wrong outline is refused with the failing field |
| SZ-4 | Lens outline | Three lens shapes keep the waveguide aperture and pass the drop test |

---

## 9. Patents (F-13)

Ayaz asked to avoid patents, and to be warned when there is no patent-free route. The files have no patent screen. Add a part with these rules:

1. For each design choice, list the known patents. Record the number, the owner and the expiry date.
2. A patent expires 20 years after the filing date in most countries. `[GENERAL]` Verify each date.
3. Prefer expired patents, free standards, licensed parts with IP protection in the supplier contract, and a different design.
4. Do not copy claim text. Keep a dated design log.
5. A patent attorney does a freedom-to-operate review before the first sale. The attorney also decides how engineers read patents.
6. If the attorney marks a design choice as blocked, remove it from the directive and use a design-around route.

**Start list for the screen** (from the work of the first directive):

| Area | Known risk | Low-risk route |
|---|---|---|
| Electrolyte fill and port | The fill step is common. A Meta patent covers a glasses-temple cell with a polymerized electrolyte. `[PATENT]` | Use the standard fill with an own cell shape. Do not copy the claim features. |
| Structural carbon fiber battery | Chalmers and Sinonus hold IP. `[COMPANY]` | Do not use carbon fiber as an electrode. |
| Flexible and tiled cell layouts | Patents exist, for example US10637017 and US11417890. `[PATENT]` | Check claims and expiry. Use an own tile and bridge layout. |
| Wireless charging at 60 W | Qi and Qi2 have WPC terms. Xiaomi, OnePlus and Honor use proprietary systems. `[GENERAL]` | There is no known free route. Join the WPC for Qi2 25 W now. Develop the own dock with an FTO review. |
| Waveguides and eye glow | The area has a very large number of patents. `[GENERAL]` | Buy from a licensed supplier with IP protection in the contract. |
| Flexible OLED and micro-LED | Display makers hold many patents. | Buy the panel from a licensed maker. |
| Modular attachable camera | Earlier modular phone projects exist. | Search prior art. Use an own attach and wallet binding design. |

---

## 10. Writing Standard (F-15)

Ayaz asked for ASD-STE100 and no em dashes.

**Facts.** The audited archive has 108 em dashes (52 in v5). In the v5 prose, 47 percent of the sentences have more than 25 words. 78 sentences have more than 40 words.

**Required changes.**
1. Remove every em dash. Use a full stop or a comma.
2. Descriptive sentences: 25 words or less. Procedural sentences: 20 words or less.
3. One idea in one sentence. Use the active voice. Use the simple present tense.
4. A rule uses **must** or **can**. Do not use "should", "may", "might" or "could" for a rule.
5. Use one term for one thing. Do not use synonyms. Keep a glossary (the Part 14 glossary can be the base).
6. Paragraphs of 6 sentences or less.
7. Add a prose check tool (`PRG-12`) counting em dashes and sentences over 25 words.

Do the conversion part by part. Start with Parts 0, 15, 17 and 18. They are the parts that a coding AI, a partner or a factory reads first.

---

## 11. Order of Work

| Order | Action | Closes |
|---|---|---|
| 1 | Correct the strain formula and the crease table (Section 4). | F-02, F-03 |
| 2 | Replace the 900 Wh/L base case by a range. Add 150, 450 and 600 Wh/L to ENR-2 (Section 3). | F-01, F-05 |
| 3 | Add the staged fold plan and the bend guard (Sections 5.2 and 5.5). | F-04, F-14 |
| 4 | Add the test matrix, the polycarbonate risk table and the cell and body risks (Sections 5.3, 5.4, 5.6). | F-14 |
| 5 | Add Duo mode and the size and shape rules (Sections 7 and 8). | F-11, F-12 |
| 6 | Add the patent part (Section 9). | F-13 |
| 7 | Fix the counts, the IP class and the thickness conflict (F-05 to F-10). | F-05 to F-10 |
| 8 | Convert Parts 0, 15, 17, 18 to STE and remove em dashes (Section 10). | F-15 |

**Closing rule.** A finding is closed by an edited file and a changed gate. A statement in a chat closes nothing (Part 16.3).

---

## 12. Sources

- Bendable battery comparison table (PolyU press release annex): https://www.polyu.edu.hk/web/filemanager/en/content_155/20190523/20190523_PR_Textile_Battery_en.pdf
- Textile lithium battery, 450 Wh/L: https://www.newelectronics.co.uk/content/news/a-flexible-high-energy-textile-lithium-battery
- Flexible battery patent US10637017: https://patents.google.com/patent/US10637017
- Flexible battery assembly patent US11417890: https://patents.justia.com/patent/11417890
- Meta patent, glasses temple cell: https://patent.nweon.com/44585
- EU Commission guidance on Article 11 of Regulation (EU) 2023/1542: https://eur-lex.europa.eu/eli/C/2025/214/oj
- Qi2 50 W plan and proprietary 80 W systems: https://9to5google.com/2026/06/29/qi2-50w-upgrade-meeting-report/
- Vuzix INCOGNITO eye glow reduction: https://www.auganix.org/?p=14920
- Geometric waveguide and privacy: https://lumus.com/everyday-privacy-how-ar-glasses-with-geometric-waveguides-are-getting-it-right/
- Inorganic barrier layers under bending (search result): verify the strain limit with the barrier supplier before use.
