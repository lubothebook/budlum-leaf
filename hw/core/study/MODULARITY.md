# BUDLUM LEAF · CORE AND SKIN · STUDY · 03 · THE MODULARITY STORY

**Revision L.7 candidate · 2026-10-19 · Study seat**. This is an engineering risk review, not legal advice. A regulatory lawyer confirms every `[HYPOTHESIS]` before the CE file closes.

## 1 · The verdict first

**The Split makes part change natural.** The Core has room for a door, a standard cell and a swap board.

It also makes three standards urgent, since a Skin must stay readable by Cores of other years. They are the link version, the identity and the part record. `[HYPOTHESIS]`

**The Split moves the legal class.** A Core with a modem, a voice path and a cell can read as a mobile phone under 2023/1670. The Skin alone is outside it. See Section 4.

## 2 · The part swaps that open in the Core

| The part | The swap | Who swaps it | The rule or the risk |
|---|---|---|---|
| silicon: compositor, encoder, decoder share | a new Core board in the same shell | a repairer or the user | the Skin link must stay at the old version. Section 3.1 |
| radio: Wi-Fi, BT, UWB | the radio board | a repairer | a radio is regulated equipment. A new board needs a new conformity file. `[HYPOTHESIS]` |
| modem: 5G SiP | the modem board, with the SIM or eSIM kept | a repairer | the SEP royalty base follows the part. Section 5 of `COST.md` |
| camera processing | the processing block | a repairer | the sensor and lens stay on the Skin. The Core only changes how the image is processed |
| secure element and wallet | a new element | the user, at a pairing | the keys do not move. The wallet is restored from the chain. `hw/core/trust` owns the rule |
| energy: the Core cell | a cell the user lifts out | the user | Article 11 asks for removal by the end user. A large Core has room for a door |
| antenna: the large Core antenna | an external antenna on a mast or a roof | an installer | at C2 the antenna is a site part, not a Leaf part |

**The user part, the repairer part and the site part.** The user lifts out the cell. A repairer swaps boards. An installer owns the far antenna. Each class has its own record. `[DECISION]` for the study.

## 3 · What the Skin must standardise

### 3.1 The three standards

| The standard | What it fixes | The rule | Why |
|---|---|---|---|
| the link version | lanes, rate, the slice and pixel format, the handshake | a version byte and a capability record in every Skin. A Core drives every version it has ever sold, for at least `7` years after the last sale | a Skin must outlive the Core it first met |
| the identity | one key per Skin in an identity chip, with a certificate and a revoke list | the key proves which Skin it is. It never signs for the wallet | a stolen Skin holds nothing worth taking |
| the part record | serial, version, cycle count, a safety certificate, the paired Core | one record on every Skin part and every Core part (law L9) | a part change then needs no account and no fee |

### 3.2 The proof from other products

| The case | What happened | Source | Status |
|---|---|---|---|
| Samsung One Connect | a box from 2020 does not fit a 2023 TV | https://help.framemytv.com/samsung-one-connect-box-explained | Search |
| Project Ara | the revised design fixed the antenna, battery, display and chip as parts that cannot be upgraded. The project was cancelled in 2016 | https://en.wikipedia.org/wiki/Project_Ara | Opened |
| Fairphone 5 | the core module cannot be bought on its own. It goes through a repair centre | https://support.fairphone.com/hc/en-us/articles/18744611991825-Fairphone-5-Replace-a-spare-part | Search |

**The reading.** Modular products fail on the part that holds the bus. A fixed link version with a long support rule is the answer. `[HYPOTHESIS]`

## 4 · The law

### 4.1 Regulation (EU) 2023/1542

| The provision | The text read | The effect on the Split | The tag |
|---|---|---|---|
| Article 3(1), battery | a device delivering energy from "direct conversion of chemical energy" | a Skin with no cell is outside the definition. A Skin with cells is not | `[PUBLICATION]` lawplayer.com/eu/act/32023R1542 |
| Article 11(1) | portable batteries "readily removable and replaceable by the end-user" | the Core cell is a portable battery and must lift out. A wireless Skin cell follows the quadrant route of `hw/energy/06` | `[PUBLICATION]` same page |
| Article 11, date | applies from `18 February 2027` | the Core and every wireless Skin fall under it from that day | `[PUBLICATION]` lawplayer.com/eu/article/32023R1542/art_96 |
| Article 11(3) | no duty if continuity is needed for safety, or for data integrity in a data product | the Core is a wallet, not a data product. Do not rely on it | `[PUBLICATION]` same page. The reading is `[HYPOTHESIS]` |

**The wired Skin is the clean case.** It has no cell, so Article 11 has nothing to remove. The Bare tier argument of `hw/hostpower/study/STANDARDS.md` Section 2.3 applies. A wireless Skin with a cell is a battery product again.

### 4.2 Regulation (EU) 2023/1670, ecodesign of phones and tablets

| The provision | The text read | The effect on the Split | The tag |
|---|---|---|---|
| Article 2(1), mobile phone | cordless, handheld, long range voice, "designed for battery mode usage" | the Core has a modem, a voice path and a cell. It can read as a mobile phone | `[PUBLICATION]` lawplayer.com/eu/act/32023R1670 |
| Article 2(8), slate tablet | "powered by an internal battery and is not intended to work without battery", with a mobile platform system | a Skin has no cell and no such system. It is outside | `[PUBLICATION]` same page |
| Annex II, endurance | `800` cycles at `80 %` for smartphones, `500` for other mobile phones | a Core cell must pass the number of its class | `[PUBLICATION]` same page |
| Annex II, serialised parts | a maker can ask only for notification and authorisation of a replacement. The way must be public and possible remotely | Skin and Core pairing must work this way. It must not lock a part | `[PUBLICATION]` same page |
| Annex II, software | operating system updates free for at least `5` years after the end of placement | applies to a Core that has a system. The Core has none, which is a question | `[PUBLICATION]` same page |
| Annex II, dismantling | dismantling information online for at least `15` years after the last unit | the part record and the dismantling file for Skin and Core | `[PUBLICATION]` same page |

**The hard finding.** The L.6.0 Leaf sat at the border of two classes, and the Split moves the border to the Core. A Core is cordless, held in a pocket or on a desk, has a modem and a voice path, and has a cell. The phone class is the risk. `[HYPOTHESIS]`

**The pairing finding.** The serialised parts rule says pairing is allowed with a public, remote, free path. It matches the rule of `hw/energy/06` Section 3.1: the handshake proves safety, not origin. `[PUBLICATION]` `[TREE]`

### 4.3 Other rules

| The rule | The point | The tag |
|---|---|---|
| Regulation (EU) 2024/1781, ecodesign for sustainable products | in force `18 July 2024`. The digital product passport comes by product group in delegated acts. Electronics are not yet set | `[HYPOTHESIS]` search summary |
| the part record and the passport | the record of Section 3.1 can feed a passport later | `[HYPOTHESIS]` |
| the Radio Equipment Directive | a Core, a wireless Skin and any radio board are radio equipment, each with a conformity file | `[HYPOTHESIS]` recall |
| the Turkish battery regulation | the rule in force is the 2004 regulation. No removability clause was seen. Alignment work is under way | `hw/hostpower/study/STANDARDS.md` Section 3.3 |

### 4.4 The questions for the lawyer

| No. | The question |
|---|---|
| M1 | Is the Core a mobile phone under Article 2(1) of 2023/1670? Which endurance class applies? |
| M2 | Is a Skin with no cell outside Article 11 and outside 2023/1670? |
| M3 | Does a wireless Skin cell fall under Article 11, and does a quadrant meet it? |
| M4 | Is the Skin and Core pairing a serialised part procedure? Does a revoke list break the rule? |
| M5 | Does a Core with no operating system owe the `5` year update duty? |
| M6 | Does a new Core board for a radio need a new radio conformity file? |

## 5 · The proposed gates of this file

| Gate | The test | The pass condition |
|---|---|---|
| CSG-11 | a Core of year N drives a Skin of year N minus six, on the bench | the Skin shows the right picture at the old link version |
| CSG-12 | a Skin and Core pairing, with no account and no fee | the user finishes it remotely, with the public procedure |
| CSG-13 | a written legal opinion on M1 to M6 | each question answered in writing |
| CSG-14 | a Core cell lift-out by the end user with no tool | removal in under `30 s` and a compatible cell accepted |
