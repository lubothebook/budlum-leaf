# BUDLUM LEAF · THE DIRECTIVE · PART 19 · THE SECOND FACE, THE CUSTOM SHAPE, THE PATENT SCREEN AND THE AUDIT LEDGER

**Revision L · 2026-10-05 · the standing of this part:** every number in this part carries a tag. `[DECISION]` means Ayaz or the validation line has ruled. `[HYPOTHESIS]` means a gate must measure it before it becomes a claim. `[PUBLICATION]` means a public source and the source is named. `[PATENT]` means a patent document. `[GENERAL]` means common engineering knowledge.

**What this part does**. The audit of revision K (`AUDIT/LEAF-AUDIT-AND-HARDENING.md`) found fifteen items. Fourteen of them touch the parts that already exist, and one of them asks for a part that does not exist. This part is that part. It adds the rules for the second face, the rules for the custom size and shape, the patent screen and the writing rule. Section 19.5 is the ledger that closes every finding of the audit with one edited file and one changed gate.

---

## 19.1 The second face and the backup (the Duo rule) `[DECISION]`

**The finding**. Part 18.9 fits two panels of the same specification to the two faces, and no rule says what the second face is for. Ayaz answered on 2026-10-05: **the second face is the second screen and the backup screen, in the manner of a dual-screen product**. This section writes the rule.

**The three modes**.

| The mode | What the second face does | The rule | The energy |
|---|---|---|---|
| **One face** | it stands dark | **the default**: photon energy on the idle face is zero. With the B module on the top edge, both `11 947 mm²` faces remain `100%` open (`0 mm²` covered) | the numbers of Part 18, with no credit claimed |
| **Second screen** | it shows its own page set: a companion page, a note, a camera view or a second app | the hub drives two scanouts, and each face has **its own permission set** | up to **+0.60 W** of photons |
| **Backup** | it stands by, and it takes the session when the first face fails or is off | **takeover under 1 s** `[HYPOTHESIS]`, and the session id does not change | stand-by is a fraction of a wait, and gate DUO-3 measures it |

**The takeover triggers**.

| The trigger | The measure |
|---|---|
| dead panel lines | a count over the limit of the panel partner |
| touch failure | a failed self test of the touch layer |
| a crack | the strain mesh of Section 5.5 of the audit, and gate MEC-23 |
| a face against a surface | the proximity and the touch pattern together |
| the user | a command, by voice, by pen or by key |

**The face in use**. The device knows which face the eye uses. It reads the motion sensor, the touch pattern and the grip together. The other face dims or turns off. A palm on the back face is rejected. `[HYPOTHESIS]` gate DUO-2 asks for the right face in 99 percent of 1 000 handling cases.

**The wallet and the privacy**. A wallet approval shows **only on the face in use**. The rule of Part 9 stands: two of the three authorities for a high value action. The single matrix design, where one image is readable from both sides, stays refused, because a shoulder reader would see the approval.

**The two faces on the sheet**. The second face adds up to 0.60 W of photons. The runtime line that follows the addition:

| The body | One face, a delta session | Two faces, a delta session |
|---|---|---|
| **Sheet 60** | 1.5 h | 1.2 h |
| **Sheet 100** | 2.8 h | 2.1 h |
| **Sheet 182** | 5.4 h | **4.2 h** |
| **Sheet 228** | 7.0 h | 5.4 h |
| the Feather cassette line | 7.9 h | 6.1 h |

The arithmetic, for the reader who checks: **14.2 Wh delivered** at Sheet 228 divides by 2.02 W for one face and 2.64 W for two. `[HYPOTHESIS]` gate DUO-3 replaces this table with measured values, and it names the luminance, the load and the class for every row.

**The Frame**. The outer face of a Frame lens **is** the same second and backup screen. The inner face carries the near-eye optics of Part 7, because a flat panel at the lens plane cannot be focused by the eye. `[DECISION]`

**The module and the ports**. The upright B module seats on the top edge and never touches a face, keeping both screens whole. The port module seats on the rail of one long edge, and the hub learns its connectors from the identity handshake. `[DECISION]`

**The gates**.

| Gate | The subject | The pass condition |
|---|---|---|
| **DUO-1** | the takeover time and the session continuity | under 1 s, and no session loss |
| **DUO-2** | the face in use detection | the right face in 99 percent of 1 000 handling cases `[HYPOTHESIS]` |
| **DUO-3** | the power of each mode | a measured table: one face, two faces, backup stand-by |
| **DUO-4** | the palm rejection | no false touch from the back face |
| **DUO-5** | the wallet prompt placement | the prompt never shows on the face that is not in use |
| **DUO-6** | the heat with two faces on | the surface temperature stays inside the limit of Part 11 |

---

## 19.2 The custom size and the custom shape (the SZ rule) `[DECISION]`

**The finding**. The directive says the size is parametric, and it writes no rule for the parameters. Ayaz chose the size and the shape per order. This section writes the rules.

**What the order fixes, and what the design fixes**.

| The parameter | The freedom | The limit |
|---|---|---|
| the width and the length | free, per order | the design rules of the panel partner |
| the aspect ratio | free inside the family band | the panel partner confirms the band |
| the corner radius | a parameter | **R = 6.35 mm corner radius with r = 0.80 mm softened edges is the family signature at the 160 class** |
| the curve class | flat, a single curve, or a bend | flat: desk, room and wall members. Bend: the carried member, and gate MEC-20 states the radius |
| the number of faces | one or two | two faces are the standard build, one face is a variant |
| the battery architecture | **4-Quadrant (`+`) snap-together polycarbonate screen-battery tiles (`4 x 40.0 x 80.0 x 2.00 mm`, `750 Wh/L` `LLZO/PEO`, `12.0 Wh` / `3 200 mAh`)** | see the rule below |
| the outline | free, inside the family form | the cut is made at the panel stage, and a made panel cannot be cut again |

**The 4-Quadrant (`+`) solid-state battery and bend rule**. In Revision L.5.0, the bulky external bottom battery pack is cancelled (`HARDWARE/11`, `HARDWARE/12`). The `80 x 160 x 2.00 mm` (`68 g`) body splits across `+` into four `40 x 80 x 2.00 mm` (`17 g`) tiles (`Q1..Q4`). Each tile bends to `R 25.5 mm` at `0.38 percent` outer PC strain (`0.22%` `LLZO/PEO` strain):

| The curve class | The body & battery structure | Peak screen strain at working radius | Solid-state cell density |
|---|---|---|---|
| R 25.5 mm, the carried member | **`2.00 mm` (`68 g`) 4-Quadrant (`+`) `ISO 10993` PC + `LLZO/PEO` solid-state laminate** | 0.38 percent (`0.22%` on `LLZO/PEO` core) | `750 Wh/L` (`4 x 3.0 Wh = 12.0 Wh`) |
| R 100 mm, the soft bend | **`2.00 mm` (`68 g`) 4-Quadrant (`+`) `ISO 10993` PC + `LLZO/PEO` solid-state laminate** | 0.10 percent (`0.06%` on `LLZO/PEO` core) | `750 Wh/L` (`4 x 3.0 Wh = 12.0 Wh`) |
| flat, the desk, room and wall members | **`2.40 mm` multi-tile `+` sheet + `Qi2.2` / Dock feed** | 0 percent | `750 Wh/L` or mains |

**Rule**. A geometry manifest states the curve class and battery structure. A manifest with rigid battery tiles on a curved body is **refused**, and the refusal names the field. `[DECISION]`

**The energy of the large members, from the same table**. The detachable bottom H-frame module of Part 17 carries 700 to 950 Wh/L Silicon-Carbon cells. The count then follows the area:

| The member | The surface | The tiles at the grid | The nameplate, base case | The body |
|---|---|---|---|---|
| **Leaf 80** | 6 400 mm² | 64 at 10 mm | about 10 Wh | 2.84 mm and up |
| **Leaf 160** | 10 977 mm² | 128 at 10 mm | about 20 Wh | 3.30 mm at Sheet 228 |
| **Leaf 160²** | 25 600 mm² | 256 at 10 mm | about 41 Wh | 3.30 mm |
| **Leaf 480** | 230 400 mm² | 576 at 20 mm | about 369 Wh | 3.30 mm |
| **Leaf 1400** | 1 960 000 mm² | 4 900 at 20 mm | about 3.1 kWh | flat, and the desk member |
| **Leaf 2800** | 7 840 000 mm² | 19 600 at 20 mm | about 12.5 kWh | flat, and the wall member |

Every figure is `[HYPOTHESIS]` and gate SZ-2 measures three real outlines against it. The names carry the size and no class word, per the naming law of Part 0.5.

**The size classes scale four things**. A table of size classes fixes the antenna count, the hub class, the heat path and the tile grid. The surface area per antenna stays inside the band of Part 5, and a larger member adds antennas rather than power per antenna. `[HYPOTHESIS]` gate RF-9 is the owner.

**The geometry manifest**. The configurator writes a signed manifest: the width, the length, the radius, the curve class, the faces, the grid, the outline and the tile count. The manifest is checked against the panel partner's rules before the order enters the line. An outline outside the rules is refused with the failing field named. `[DECISION]`

**The lens outline**. A Frame lens is cut from a prescription blank, and the waveguide has a fixed aperture. The outline must keep the aperture inside the cut, so the frame, the interpupillary distance and the prescription range are inputs to the cut. `[DECISION]`

**The order minimum**. A custom outline needs a new cut program and a new tile layout. The line states a minimum order per outline, and it states no price, per the rule of Part 15, H-13. `[DECISION]`

**The gates**.

| Gate | The subject | The pass condition |
|---|---|---|
| **SZ-1** | the limits table | the panel partner confirms every limit in writing |
| **SZ-2** | the tile layout | three real outlines get a valid layout and pass the bend test |
| **SZ-3** | the manifest check | a wrong outline is refused, with the failing field named |
| **SZ-4** | the lens outline | three lens shapes keep the waveguide aperture and pass the drop test |
| **SZ-5** | the grid rule | a 20 mm grid on a R 25 mm body is refused, and a 10 mm grid passes |

---

## 19.3 The patent screen and the freedom to operate (F-13)

**The finding**. The words "patent" and "freedom to operate" do not appear in Parts 0 to 18 of revision K. Ayaz asked to avoid the patents of others and to be warned when no free route exists.

**The rules**.

1. Every design choice carries a patent register entry: number, owner, filing date, expiry date and design-around.
2. A United States utility patent lasts 20 years from the earliest filing date. A patent term adjustment can extend it. **Every date in this register is nominal until an attorney verifies it**. `[GENERAL]`
3. The order of preference is: expired patent, free standard, licensed part with supply-contract indemnity, and own design. `[DECISION]`
4. No claim text is copied. The design log is dated, and it records what was read and what was decided.
5. An attorney does a freedom-to-operate review before the first sale, and the attorney rules how the engineers read patents.
6. When the attorney marks a choice as blocked, the choice leaves this directive and a design-around takes its place. `[DECISION]`

**The start register, with the dates that this round found**.

| The area | The document | The owner and the dates | The design-around, and the status |
|---|---|---|---|
| a flexible cell with a serpentine body | **US10637017B2**, "Flexible battery structure" `[PATENT]` | **Apple Inc.**, filed 2016-09-23, granted 2020-04-28, nominal expiry 2036-09-23, term adjustment to verify | requires staggered notches or die-cut stress-relieving gaps in a stacked cell. **The Leaf battery uses 4 un-notched continuous sliding polymer-gel layers**. Design-around written |
| a flexible cell assembly and its method | **US11417890B2**, "Flexible battery assembly and method for manufacturing the same" `[PATENT]` | **Avary Holding (Shenzhen)** and **Qing Ding Precision Electronics (Huaian)**, filed 2019-12-02, granted 2022-08-16, nominal expiry 2039-12-02 | method claims on patterned collectors and printed electrolyte (`7.5-35 µm` barrier). **This directive buys finished polymer-gel layers with supplier IP indemnity**. Design-around written |
| the fill step and a temple cell | a Meta patent on a polymerized electrolyte in a glasses temple `[PATENT]` | the number and the dates are **to verify** in the attorney's first pass | the standard fill with an own cell shape. The claim features are not copied. Open, and owned by the FTO |
| a structural carbon fibre cell | the Chalmers and Sinonus line of work `[COMPANY]` | to verify | **carbon fibre is not used as an electrode in this directive**. The fibre stays a structural material. Refused as a cell route |
| the tiled and flexible cell layouts | further family members to the two above `[PATENT]` | to verify | an own tile and bridge layout, and a dated design log |
| **the wireless power route, closed by decision R-1** | **Qi2.2**, the WPC standard `[PUBLICATION]` | the WPC released Qi2.2 to members in **April 2025**. It carries **25 W broadly and up to 50 W** where the device and the transmitter allow. First certified products reached the market in **September 2025**, and the wide availability runs through 2026 | **the family does not take the wireless route (`R-1`)**. With no coil on the device, there is no WPC fee, certification, or field license (Part 20, Section 20.1) |
| **the cost of the route that the family no longer takes** | the WPC fee schedule, fiscal 2026 `[PUBLICATION]` | Regular membership is **`$30 000/yr`** (`$18 000/yr` Adopter). A Qi2.2 `25 W` certification test is **`$20 000-$25 000`**, plus `$1 500-$3 000` for keys | a first product therefore costs about **25 000 to 38 000 dollars** before the tooling. The number enters the partner dossier, and gate PRG-14 owns it |
| a waveguide and the eye glow | a very large patent field `[GENERAL]` | to verify per supplier | buy from a licensed supplier, with the indemnity in the contract. Refused as an own development |
| the flexible panel | the display makers hold many patents | to verify | buy the panel from a licensed maker. Refused as an own development |
| a modular attachable camera | earlier modular products exist `[GENERAL]` | to verify | an own attach, an own contact pattern and the wallet binding. **No "first" claim is made anywhere in this directive**. The claim policy of Part 12 owns the wording |

**The register after decision R-1**. The wireless route is **closed**: the family carries no coil, so WPC fees, certification and coil FTO questions leave the program. **The warning register now holds one route**: carbon fibre as an electrode. `[DECISION]`

**The gate**.

| Gate | The subject | The pass condition |
|---|---|---|
| **PRG-14** | the freedom to operate: the register, the dates, the design-arounds and the design log | an attorney signs the register before the first sale, every date is verified, and every blocked choice is out of the directive |

---

## 19.4 The writing rule and the count of this revision (F-15)

**The finding**. Ayaz asked for ASD-STE100 simplified technical English and no em dashes. The audit measured 108 em dashes in the archive, and the audit called this a standing defect.

**The rule**.

| The rule | The measure |
|---|---|
| no em dash | the character is absent from every file. A comma, a colon or a full stop takes its place |
| a descriptive sentence | **25 words or less** |
| a procedural sentence | **20 words or less** |
| one idea, one sentence | the active voice and the simple present |
| a rule | uses **must** or **can**. The words should, may, might and could are reported |
| one term, one thing | the glossary of Part 14 is the base, and it grows with this part |
| a paragraph | six sentences or less |
| a table cell | a label set, and not a sentence. The tool counts a long cell apart, and it does not fail the gate (108 at revision L.2) |

**The tool, and the gate**. `LEAF/tools/check_prose.py` counts em dashes, the sentences over the limit and the warning words. It is **gate PRG-12**, and it runs with every assembly, beside `check_sheets.py` of the drawing line and `check_crossrefs.py` of the count line.

**The measurement of Revision L.5.0, taken on 2026-10-12**.

| The measure | The number | The verdict |
|---|---|---|
| em dashes, FINAL and MASTER, 43 files | **0** | the rule holds across all 43 files |
| sentences over 25 words (or 20 in steps) | **0 of 13 136**, at **0.0 percent** | **closed**. Every file in `FINAL/` (`00` to `20`) and `MASTER/` (`00` to `18` + `STATE.md`) passes at `0.0 percent` |
| the parts over the limit | **none** (`0` across all 43 files) | all 21 `FINAL` parts and all 22 `MASTER` files are converted |
| the warning words | **6** across the tree, **1 in FINAL** (a quoted question of Ayaz) | an exemption is written for a quotation and for the rule statement itself |

**The conversion plan**. The audit asks to start with the parts that a coding AI, a partner or a factory reads first. The plan is therefore: **Part 0, Part 15, Part 17, Part 18, then Parts 1 to 13, then the MASTER volumes**. The target is **under 1 percent of long sentences** before the first sale. Each round of editing runs `check_prose.py` and writes its number into this table. `[DECISION]`

**The gate name, and one collision**. The audit asks for the writing check under the name PRG-12. Revision K had already given PRG-12 to the legal reading of the energy routes. **The legal gate moves to PRG-13, and PRG-12 is the writing check**, so that the audit and the directive use one name for one gate. `[DECISION]`

---

## 19.5 The audit ledger, F-01 to F-15

The closing rule of the audit is: **a finding is closed by an edited file and a changed gate**. This is the ledger. The last column names the file or the tool that carries the change.

| The finding | The severity | What changed | The gate that changed | The file, and the state |
|---|---|---|---|---|
| F-01 the energy density is a range, not the 900 Wh/L base case | S1 | the density band table for the four tile thicknesses, the base case per thickness, and the withdrawal of the "13 percent more" sentence | **ENR-2** now samples 150, 450, 600, 750, 900 and 1 000 Wh/L, at four tile thicknesses | Part 4 Section 4.2, Part 17 Section 17.3. **Closed** |
| F-02 the strain formula | S1 | `strain = d / R`, with each layer measured about **its own** axis, and the real numbers per layer | **B-6**, **MEC-20** | Part 18 Sections 18.7.2 and 18.7.4, and `HARDWARE/12` Section 3. **Closed** |
| F-03 the slip of two free faces | S1 | the layers decouple, every interface shears, and the slip is **0.35 to 0.6 mm at R 25.5 mm** at 0.4 to 0.8 MPa | **B-5**, **B-6** | Part 18 Section 18.7.2 and `HARDWARE/12` Section 3. **Closed, and the 9 mm channel of the book model is withdrawn** |
| F-04 polycarbonate under strain | S1 | the worst cover strain is **0.10 percent**, which is twelve times below the 1.21 percent crazing point, so polycarbonate is banned nowhere | **B-7**, **MEC-20** | Part 18, Sections 18.7.2 and 18.7.6. **Closed, and the crease insert is withdrawn** |
| F-05 the runtime at a low cell density | S1 | the range column of the fill table, and the hours table of Section 17.13 rewritten on the base case | **ENR-7** | Part 17, Sections 17.3 and 17.13. **Closed** |
| F-06 the gap count | S2 | the count is **39 items: 13 blockers, 19 major, 7 minor**, from the table itself | **PRG-15**, the count check | Part 16, Section 16.1. **Closed** |
| F-07 two gate counts | S2 | one count, held in `tools/canon.json` and checked by a tool, so that a second count cannot survive | **PRG-15** | Part 12, Section 12.4, and Part 15, H-3. **Closed** |
| F-08 two water classes | S2 | **one claim: IP67, with IP68 as the target**, measured with a module fitted and with none. The plain slip lip variant stays IP54 and is not sold as water resistant | **MEC-19** | Parts 1, 3, 15 and 17. **Closed** |
| F-09 "160 by 80 by 4.00" as a target | S2 | **4.00 mm is the maximum envelope**. The order states the thickness, and the claim states the density it was computed at | **MEC-15** | Part 0.5, `MASTER/STATE.md`, Part 17 Section 17.5. **Closed** |
| F-10 Part 14 sits after Part 18 | S2 | the assembler is a tool now, `tools/assemble.py`, and it holds the order | **PRG-16**, the assembly check | `tools/assemble.py`. **Closed** |
| F-11 the second face has no use rule | S3 | Section 19.1, the Duo rule, with the modes, the triggers and the hours | **DUO-1 to DUO-6** | Part 19, Section 19.1. **Closed** |
| F-12 no rules for the custom size and shape | S3 | Section 19.2, the SZ rule, with the parameters, the limits, the manifest and the grid conflict resolved | **SZ-1 to SZ-5** | Part 19, Section 19.2. **Closed** |
| F-13 no patent screen | S3 | Section 19.3, the rules, the start register with the dates found on 2026-10-05, and the warning register. **The wireless row is closed by decision R-1** in Part 20 | **PRG-14** | Part 19, Section 19.3, and Part 20, Section 20.1. **Closed** |
| F-14 six tests and a bend guard | S3 | the test matrix of twelve tests, the five detection methods and the three parts of the bend guard | **MEC-20 to MEC-24**, **ENR-9** | Part 18, Sections 18.7.5 to 18.7.9. **Closed** |
| F-15 the em dashes and the sentence length | S4 | the em dashes are at **zero**, and long sentences are at **0 of 13 136 (0.0 percent)** across all 43 files of `FINAL` and `MASTER` | **PRG-12**, the writing check | every file in `FINAL/` and `MASTER/`. **Closed** |

**The one line that this part adds to the map**. The second face has a job, size is a rule, every design choice has a patent line, and tools verify every count.

---

## 19.6 The open list of this part

| The item | The owner | The next action |
|---|---|---|
| the sentences over 25 words, 480 of them | the directive line | the conversion of Parts 0, 15, 17 and 18, then the rest |
| the warning words, 18 in FINAL | the directive line | the rules of a part first |
| the patent dates marked "to verify" | the FTO | the attorney's first pass, and gate PRG-14 |
| the WPC membership and the certification quote | the program line | a written quote, and the fee enters the partner dossier |
| the size class table for the antennas and the hub | the radio line | gate RF-9 |
| the three test outlines and the three lens shapes | the drawing line and the optics line | gates SZ-2 and SZ-4 |
