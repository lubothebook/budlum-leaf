# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME XVII · THE LOGS OF REVISION G TO REVISION L

**Date:** 2026-10-05 · the blocks of work that carried the master from revision F to **revision L**.
**The rule of this volume**. A revision is a block of work with artefacts, and a log states what changed and where it landed. The logs of revisions A to F are the volumes VI, VII, VIII, XV and XVI. **The letter J was skipped by the board: revision I was followed by revision K**.

---

## 1 · The revision log, in one table

| The revision | The block | What landed | Where |
|---|---|---|---|
| **G** | the first self audit, and the hardened final edition | single thickness ledger (`0.46 mm` per face, `4.00 mm` max), hardening addenda H-1 to H-15, gap register G-01 to G-35, and audit rule | `FINAL/02`, `FINAL/15`, `FINAL/16`, and `FINAL/00`, Section 0.75 |
| **H** | the state after the hardened final edition | the assembled v5 rebuilt at 2 410 lines, the ppd row of Volume III corrected, `STATE.md` at revision H | `MASTER/03`, `MASTER/STATE.md` |
| **I** | the energy architecture | Energy Sheet at the neutral axis, Bare tier, routes A and B, hub, wallet settlement, drawing sheet P08, and v5.1 source footers | `FINAL/17`, `pafta/P08`, `MASTER/STATE.md` |
| (J) | not used | the board named the next block K | n.a. |
| **K** | the screen, the cost, the fold and the seal | five-term ledger (`2.02 W` to `0.98 W`), photon-honest interface, gasketed slip carrier of route A+, decision table Q43 to Q48, and sheet P09 | `FINAL/18`, `pafta/P09`, `MASTER/STATE.md` |
| **L.2** | **the charge path and the both face module** | wireless path withdrawn (`R-1`): USB-C PD (`40 W` peak) and dock contact (`27 W`, `0.06 W` loss). Under-display camera refused; 14-test trial plan (`+10` gates) | `FINAL/20`, `FINAL/04`, `FINAL/05`, `FINAL/07`, `FINAL/11`, `FINAL/12`, `FINAL/14`, `FINAL/15`, `FINAL/17`, `FINAL/19` |
| **L** | **the external audit pass, and the tools** | findings F-01 to F-15 closed, density band, strain rule `d / Rn`, Duo rule, SZ rule, patent screen, writing rule, and **four QA tools** | `FINAL/04`, `FINAL/15`, `FINAL/16`, `FINAL/17`, `FINAL/18`, **`FINAL/19`**, `tools/assemble.py`, `tools/check_prose.py`, `tools/check_crossrefs.py`, `tools/canon.json` |
| **L.3** | **the camera on the device, and the port rail** | ports leave the body and become a **detachable side Port Rail module** with USB-C, USB-A, and `3.5 mm` jack. Gate MEC-28 added | `FINAL/06`, `FINAL/20`, `HARDWARE/03` to `HARDWARE/09` |
| **L.3.1** | **the field, the sheet and the parts** | magnetic interface (`HARDWARE/10`), bottom battery & Hot-Swap (`HARDWARE/11`), part catalogue, connection spec, open items, sheets P11 to P13, and gates MEC-29..32, DSP-14, ENR-11..13 | `HARDWARE/03` to `HARDWARE/11`, `pafta/P11` to `P13` |
| **L.3.2** | **the bend law, and the part-by-part sheets** | book model retired: **no hinge, no crease**. Whole-area bend to `R 25.5 mm` (`HARDWARE/12`, `B-1..10`). Part-by-part specs for B module (`31` parts), rail (`42`), battery (`25`), screen (`10`), and body (`14`) | `HARDWARE/12` to `HARDWARE/17`, `pafta/P14` to `P19`, `cad/monogram_detail.py`, `cad/rail_detail.py` |
| **L.3.3 to L.4.1** | **Bare `1.02-1.20 mm` (`20 g`) T-OLED + PDLC + AgNW/ITO body, upright B module, and detachable bottom battery** | superseded by Revision L.5.0 (`4 x 40x80x2.00 mm` `+` solid-state quadrants + `90°`-bent-stem B module) | `AUDIT/ARENA-MULTI-AGENT-INTERNAL-PARTS-REPORT.md` |
| **L.5.0** | **4-Quadrant (`+`) solid-state (`12.0 Wh`) body (`68 g`), `<15 µm` (`n=1.585`) seam, `Qi2.2` wireless, eyewear safety (`<=36.2 °C`), and `90°`-bent-stem B module (`20 g`)** | bulky bottom battery cancelled; `4 x (40x80x2.00 mm)` `LLZO/PEO` tiles, `0` USB-C on body (`Qi2.2` wireless), and `90°`-bent stem B module (`84` internal parts) | `HARDWARE/00` to `20`, `pafta/E01` to `E03`, `pafta/P01` to `P22`, `cad/leaf_v2.py` |

## 2 · The four tools of revision L

| The tool | The gate | The duty | The state |
|---|---|---|---|
| `tools/assemble.py` | **PRG-16** | build the single source of truth from the parts, in ascending order, each part once | `3 775` lines, `20` numbered parts, and `1` front matter |
| `tools/check_prose.py` | **PRG-12** | no em dash, descriptive sentence `<= 25` words, procedural `<= 20` words, table cell `<= 25` words | **`0` em dashes, `0` long sentences, `0` long cells, and `0` warnings across all `70` files** |
| `tools/check_crossrefs.py` + `tools/canon.json` | **PRG-15** | one count per number; canonical numbers live in `tools/canon.json` and every count claim is checked | the counts of Section 3, held in `tools/canon.json` |
| `pafta/check_sheets.py` + `pafta/check_widths.py` | the drawing line | the overflow, collision, covered text, and line width of every sheet | passing on all `25` pafta sheets (`E01..E03`, `P01..P22`): `0, 0, 0` |

## 3 · The count of the register at revision L

| The family | The gates |
|---|---|
| MEC: the structure and the mechanics | 23 |
| ENR: the energy | 9 |
| DSP: the display | 11 |
| RF: the radio and the link | 8 |
| CAM: the camera and the module | 10 |
| CLR: the clear family and the Frame | 10 |
| FLD: the Field mode | 6 |
| SW: the software and the network | 13 |
| DST: the distance and the class | 8 |
| DUO: the second face | 6 |
| SZ: the size and the shape | 5 |
| **the device and the network subtotal at revision L** | **117** |
| the block of 2026-10-06 (Part 20) | **+10**: MEC-25 to MEC-27, CAM-11 to CAM-13, DUO-7, DSP-12, DSP-13, ENR-10 |
| **the device and the network subtotal at revision L.2** | **127** |
| **the device and the network subtotal at revision L.3** | **128**, with MEC-28 for the wall hold with the module fitted |
| **the device and the network subtotal at revision L.3.1** | **133**, with MEC-29 to MEC-32 (field, placement, Tilt Pad, wrap zone), DSP-14, and ENR-11 to ENR-13 |
| the bend family (revision L.3.2) | **+10**: B-1 to B-10 for full wrap, gentle bend, flat recovery, no-crease scan, gap budget, slip, thermal wrap, seal, rail edge, and seated wrap |
| the module family (revision L.3.2) | **+7**: module plate mass, flatness, optics, assembly and coupler gates |
| **the device and the network subtotal at revision L.3.2** | **150** |
| the part-by-part band (revision L.3.3 to L.5.0) | the gate families of the thirteen part-by-part files, from RL-1 to MON-20, each written in its own file |
| **the device and the network subtotal at revision L.5.0** | **218**, measured by `tools/check_crossrefs.py` from the gate rows of the FINAL files |
| PRG: the program | 16 |
| RG: the research plan | 17 |
| **the total at revision L.3.2** | **183** |
| **the total at revision L.5.0** | **251**, which is `218` device and network, `16` program and `17` research (`tools/canon.json`) |

**The rule that this volume adds to the program**. **A count without a tool is a memory, and a memory is not a register**. Gate PRG-15 fails the tree when a number in a file disagrees with `tools/canon.json`. `[DECISION]`

## 4 · What the audit pass changed in the physics, in one table

| The item | Before revision L | After revision L |
|---|---|---|
| the energy density | a single 900 Wh/L base case | a band per layer thickness (`400, 500, 700, 800 Wh/L` base case); gate ENR-2 samples `150` to `1 000 Wh/L` |
| the "13 percent more" sentence | a claim about Sheet 228 | **withdrawn**: the sheet and the cassette carry the same energy, and the sheet wins on thickness |
| the bend strain | `t / (2 R)` | **`d / R`**, where d is the distance to **each layer's own axis**, and the numbers per layer follow |
| the decoupled stack | one face under 160 µm, two bonded faces | **each layer bends about its own axis** (`0.38%` collector strain at `R 25.5 mm`, `0.35 mm` silicone interlayer slip) |
| the crease, and polycarbonate in it | polycarbonate banned in the crease | **retired by revision L.3.2**: there is no crease. The worst cover strain is 0.10 percent, so polycarbonate keeps every face |
| the book model | R 2.0 mm, 100 000 cycles, the stages S1 to S4 | **retired by revision L.3.2**: no hinge, no crease line, no closed state. The surface bends over its whole area, 5 000 wraps at R 25.5 mm and 50 000 gentle bends, gates B-1 to B-10 |
| the water class | IP54 and a refusal of IP68 | **IP67 claimed, IP68 a target**, on the gasketed slip carrier, measured with a module fitted and with none |
| the thickness | "160 by 80 by 4.00 mm" as a target | **4.00 mm is a maximum envelope**, and the order states the thickness |
| the second face | two identical panels, no use rule | the **Duo rule**: second screen, backup, a takeover under 1 s, and the hours table for two faces |
| the size and the shape | the word "parametric" | the **SZ rule**: the parameters, the limits, the manifest, the grid rule and the gates |
| the patents | no screen | the **register** of Part 19, Section 19.3, with the dates found on 2026-10-05 and the two warning routes |
| the writing | 108 em dashes, and no limit on the sentence | **0 em dashes**, a limit of 25 and 20 words, and a live gate |
