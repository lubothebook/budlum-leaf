# BUDLUM LEAF · ENERGY · 06 · THE EU 2023/1542 REMOVABILITY NOTE

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. This is an engineering note, not legal advice. A regulatory lawyer confirms it before the CE file closes. Gates ENR-13, MEC-40, ENR-22.

## 1 · The rules that apply

| The rule | What it asks | The tag |
|---|---|---|
| Regulation (EU) 2023/1542, Article 11, from `18 February 2027` | a portable battery in an appliance is readily removable and replaceable by the end-user | `[PUBLICATION]` |
| "readily removable" | removal with commercially available tools. No specialised tool unless supplied free, no proprietary tool, no heat, no solvent | `[PUBLICATION]` Commission guidance on Article 11, summarised by Hogan Lovells, 2026 |
| Article 11, spare batteries | the battery stays available as a spare part for `5` years after the last unit of the model | `[PUBLICATION]` ComplianceGate summary |
| Article 11, the wet-environment route | an appliance made to work near water can use a professional-only route, with proof | `[PUBLICATION]` Commission guidance, 14 July 2026 update, secondary source |
| Regulation (EU) 2023/1670, ecodesign of phones and slate tablets, from `20 June 2025` | battery `800` cycles with `80 %` capacity left; spare parts for `7` years; repair software open to professionals | `[PUBLICATION]` European Commission, energy-efficient-products page |
| 2023/1670 against Article 11 | for phones and slate tablets, the 2023/1670 battery rules prevail | `[PUBLICATION]` ComplianceGate summary of the Commission guidance |
| Regulation (EU) 2023/1669, energy label of phones and tablets | the label shows battery endurance in cycles, a drop class, a repair class and the IP class | `[PUBLICATION]` European Commission |

**The class of the Leaf**. The Leaf has a 5G modem, a voice path and a `17.9 cm` (`7.04 in`) diagonal at rest. The Commission page puts smartphones at `4-7 in` and slate tablets at `7-17.4 in`. So the Leaf sits on the border of the two classes. Both classes fall under 2023/1670. `[TREE]` `[HYPOTHESIS]` for the legal class, since the Leaf runs no operating system.

## 2 · How the Leaf meets Article 11

### 2.1 What the battery is

1. **The cells**. `128` hermetic micro cells, one per tile. Each is a battery cell in the sense of 2023/1542. `[GENERAL]`
2. **The removable unit**. A quadrant, `Q1..Q4`, holds `32` cells, their fuses, their TCMs and one U_Q. It is a battery pack with display tiles bonded to it.
3. **The user-replaceable battery is the quadrant**. `[DECISION]` this team.

### 2.2 The check against "readily removable and replaceable"

| The test | The Leaf | The verdict |
|---|---|---|
| removal with commercially available tools | no tool at all. The quadrant lifts off its kinematic seat | meets it, better than the rule |
| no heat, no solvent, no adhesive to break | the seat is magnets and balls in vees | meets it |
| the time | under `3 s`, gate MEC-40 | meets it |
| the user can do it at any time | yes, with the body on or off | meets it |
| replaceable with a compatible battery | a new quadrant joins in `3 ms`, gate ENR-19 | meets it, subject to Section 3 |
| instructions and safety information | a removal card in the box and on the support page | to be written |
| the spare part | quadrants for `7` years after the last sale, the longer of `5` and `7` | design rule, see Section 4 |

**The wet-environment route is not needed**. The Leaf removes its battery with no tool, so it uses the end-user route. `[DECISION]`

## 3 · The two risks and the fixes

### 3.1 Risk one: the dead-pad handshake as parts pairing

**The risk**. The `3 ms` challenge refuses an unknown quadrant. If only Budlum keys pass, a compatible third-party quadrant fails. That reads as a proprietary lock on replacement. 2023/1670 also asks for open repair software. `[HYPOTHESIS]`

**The fix**. `[DECISION]` this team.

1. The handshake proves safety, not origin. It checks a cell-safety certificate.
2. Any supplier that passes the Leaf cell tests gets a certificate from a published scheme.
3. A failed check falls back to safe mode: `0.5 C` charge, no fast charge, and a notice. It never refuses the quadrant.
4. The pairing tool is free to the user and to every repairer. No account and no fee.
5. The dead-pad law for water and coins stays. A wet pad answers no challenge at all.

### 3.2 Risk two: the price of the spare battery

**The risk**. A quadrant carries `32` micro-LED tiles. Its price is far above a phone battery. A battery spare at a display price can fail the "reasonable" test of the spare-part rule. `[HYPOTHESIS]`

**The fix**. `[DECISION]` this team.

1. **The exchange quadrant**. The user returns the old quadrant. Budlum re-cells it and resells it at a battery price.
2. **The re-cell line**. A professional opens each tile from the back skin and replaces the cell. The cell has two pads and no adhesive across the can faces.
3. **The cell spare**. The micro cell itself stays a spare part for professionals for `7` years.
4. **The display stays**. A re-cell keeps the display tiles, so the user pays for the energy only.

## 4 · The endurance rule of 2023/1670

**The rule**. The battery keeps `80 %` of its capacity after `800` full cycles. `[PUBLICATION]`

| The variant | The risk | The design answer | The gate |
|---|---|---|---|
| G, graphite / LiCoO2 `4.45 V` | low. Phone cells of this class meet `800` cycles | `100 %` DoD per cycle with the balance of `02` Section 4 | ENR-22 |
| S, Si-C / LiCoO2 `4.48 V` | high. Silicon fades faster | prelithiation, the scaffold Si-C, and the compliance pad | ENR-22 |
| both, at a `25 W` charge | plating and heat | the charge rules of `04` Section 5 | ENR-24 |

**The pass condition we add to gate ENR-22**. Ten cells of each variant run `800` full cycles at `25 °C`. Each keeps `80 %` or more. `[DECISION]`

## 5 · The other duties of 2023/1542 for these batteries

| The duty | The Leaf answer | The tag |
|---|---|---|
| CE marking and the EU declaration of conformity | on the quadrant and in the file | `[GENERAL]` |
| labels: capacity, chemistry, separate collection symbol | on the quadrant back skin; capacity in Wh on each quadrant | `[GENERAL]` |
| extended producer responsibility and take-back | the exchange quadrant feeds the take-back | `[GENERAL]` |
| hazardous substances: mercury, cadmium, lead limits | no Hg, Cd or Pb in the cells, the braze or the feedthrough | `[DECISION]` |
| the battery passport | not for portable batteries | `[GENERAL]` |
| the dock pack | a portable battery inside the dock. A door with two standard screws gives user removal | `[DECISION]` |
| the B cell | a portable battery inside the B module. The B module itself lifts off with no tool | `[HYPOTHESIS]` |

**The B cell needs a second look**. The B module is removable from the body, but the B cell sits sealed inside the ring. Article 11 asks for the battery, not the module, to be removable. Two answers exist. `[HYPOTHESIS]`

1. Treat the B module as the replaceable battery unit, as for the quadrant. An exchange B module ships at a battery price.
2. Or give the ring a back window held by two standard screws, with the cell on two spring contacts.

The B team and the lawyer choose. This team recommends answer 1 for the `4.00 mm` ring.

## 6 · The sources

1. Regulation (EU) 2023/1542, Article 11. Summary: ComplianceGate, "How to Comply with the EU Replaceable Battery Rules".
2. Commission guidance on Article 11, 14 July 2026 update. Summary: Hogan Lovells, "Avoiding the redesign: the EU's latest position on battery removability".
3. Regulation (EU) 2023/1670 and 2023/1669. Summary: European Commission, energy-efficient-products page, "Smartphones and tablets".
4. The primary texts on EUR-Lex are the reference for the lawyer. This note quotes secondary summaries and tags them so.
