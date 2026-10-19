# BUDLUM LEAF · CORE AND SKIN · THE STUDY SEAT

**Revision L.7 candidate · 2026-10-19 · Study seat, block HP-2 with the distance order of HP-3**. This seat tests the Split against prior art, cost, law and the market. It is a study. It changes no L.6.0 or L.6.1 decision. It is a risk review, not legal advice.

## 1 · What is here

| The file | The content |
|---|---|
| `PRIOR-ART.md` | `25` real products and services, with URL, split, link, numbers and a read or search status. Near rows and far rows. What is not new. What is open at C0, C1 and C2 |
| `COST.md` | the BOM model results: cost per Skin, cost of the Core, break-even for `1`, `2`, `4`, `8` Skins and for mixed sizes, by distance class |
| `MODULARITY.md` | the part swaps in the Core, the three standards a Skin needs, the EU rules and the questions for a lawyer |
| `CLAIMS.md` | three claim sentences with gates, the rule for "first", the recommendation and the class matrix |
| `cost.py` | the BOM model. It imports `program/budget.py` read only |
| `out/` | `cost_table.txt`, `sweep.txt`, `tornado.txt`, `cost.json`, `breakeven.png` |

## 2 · How to run it

1. Run `python3 hw/core/study/cost.py` from the repo root. It takes about `10 s`.
2. Read `hw/core/study/out/cost_table.txt`, then `sweep.txt` and `tornado.txt`.
3. Check the prose with `python3 tools/check_prose.py hw/core/study/*.md`.

The script needs numpy and matplotlib. It writes only inside `hw/core/study/out/`.

## 3 · The verdict on novelty

**The Split is not new.** Compute packs, wireless pixel links, one-box panels, zero clients, cloud rendering and cell-site compute all exist. So does a large far antenna that serves an unmodified small device (Starlink Direct to Cell). `[PUBLICATION]` `PRIOR-ART.md`.

**What is open is the join.** One wallet Core, many zero-key Skins and a Skin that roams with its session. No source found joins them. `[HYPOTHESIS]` The Core as a validator and one Core for a size family are design choices that add weight. A professional search (CSG-1) must confirm.

## 4 · The five key numbers

| The number | The value | The tag |
|---|---|---|
| the micro-LED share of the all-in-one unit | `76 %` (P10 `67 %`, P90 `83 %`) at `1 M` per year | `[HYPOTHESIS]` on `[TREE]` |
| a Skin against the all-in-one Leaf 160 | `1 331` against `1 575 USD`, so `15 %` less | `[HYPOTHESIS]` |
| the Core, wired, for `1`, `4`, `8` Skins | `154`, `195`, `250 USD` | `[HYPOTHESIS]` |
| the break-even and the saving | `2` Skins per Core. `+559 USD` (`8.9 %`) at four, `+1 264 USD` (`10.0 %`) at eight | `[HYPOTHESIS]` |
| the Skin mass and thickness | about `40 g` against `68 g`, and `0.90 mm` against `2.00 mm` | `[HYPOTHESIS]` |

## 5 · The results by distance class

| The class | The BOM that leaves the Leaf | The break-even | The claim that is open |
|---|---|---|---|
| C0, tether to `2 m` | `12.1 %` | `1` by a hair, `2` for safety | one wallet Core, zero-key Skins, a roaming Skin |
| C0r, 60 GHz to about `10 m` | `9.5 %` | `2` | the same. The Skin load is `3.35 W` against `1.73 W`, so heat fails |
| C1, Wi-Fi 7 to `30 m` | `9.0 %` | `2` | the same. The Skin keeps a decoder, so "no processor" is false |
| C2, far | `0 %` | not applicable | the Core as a validator. The Split is not a hardware claim |

## 6 · The damage to the Split

1. **The cost aim fails.** The tile is `76 %` of the unit and stays in the Skin. The Split cuts the system cost by `9 %` at four Skins.
2. **The weight aim holds.** The Skin is about `41 %` lighter and under half as thick.
3. **A wireless Skin breaks the heat law.** A 60 GHz radio doubles the surface load. C1 is near the limit.
4. **At C2 nothing leaves.** The Skin keeps the radio and decoder and is the L.6.0 Leaf.
5. **The legal class moves to the Core.** The Core can read as a mobile phone under 2023/1670. `[HYPOTHESIS]` `MODULARITY.md` Section 4.
6. **A Skin shows what a rogue Skin chooses.** A hardware wallet owns its screen for this reason.

## 7 · The hardest question: what would make the Split fail in the market

Ranked by how likely each is to kill it. The first is a physics limit and the last is a legal class. `[HYPOTHESIS]`

| Rank | The failure | The evidence | The test |
|---|---|---|---|
| 1 | **The link.** A cable is a tether. A wireless Skin is too hot. Far, the pixel link cannot cross a kilometre | the heat table of `cost.py`: `3.35 W` over `1.73 W`. WiGig is a few metres in the source read. The pixel stream is `6` to `13 Gbit/s` | CSG-6 and CSG-7 |
| 2 | **The loss of the one object.** The user carries two parts, not one | Magic Leap 1 is end of life, and the source says the tether did not survive. HoloLens 2 put everything on board | a pilot with a user who owns one Core and two Skins |
| 3 | **The cost story fails.** A buyer pays for the Skin, and the Skin is `85 %` of the old cost | the model: `8.9 %` at four Skins. The tile swing is zero | CSG-8, the tile quote |
| 4 | **The screen cannot be trusted.** A rogue Skin shows a false amount | Ledger says a host screen can change an amount, and drives its screen from the secure element | CSG-3 |
| 5 | **The latency.** The link adds a stage between touch and light | Vive latency was noticeable. The L.6.0 law answers touch inside the device | CSG-6 at each class |
| 6 | **Support.** One Core down means every Skin dark. Two parts means two warranties. Old Skins meet new Cores | Samsung boxes do not cross years (Search). Ara died on the bus part | CSG-11 and CSG-12 |
| 7 | **The law.** The Core is a phone class and its cell must lift out | `MODULARITY.md` Section 4 | CSG-13 |

**The honest reading.** Failure 1 can end the program at C0r and C1. Failure 3 does not end it. It changes the reason to build it. The case that stands is weight, thickness, one wallet and one service for many surfaces. `[HYPOTHESIS]`

## 8 · The open issues

| No. | The issue | The owner |
|---|---|---|
| 1 | no patent search was made. The web survey found no patent | patent searcher |
| 2 | pages for FlatpanelsHD, HP, Azure and Verizon did not load. Their rows say Search | study seat |
| 3 | the Core cell cost, the link chips and the radio costs are ranges, not quotes | procurement |
| 4 | the Leaf 480 uses the emitter cost of the `508 ppi` tile and the Leaf cell | display seat |
| 5 | the royalty base of a Core is unknown. It moves the saving by about `210 USD` at four Skins | lawyer |
| 6 | the radio power of a 60 GHz end is a guess of `1` to `3.5 W` | link seat |
| 7 | the trusted amount on a Skin has no design yet | trust seat |
| 8 | the wallet at C2 sits in the Leaf. The zero-key claim needs it to move | trust seat |
| 9 | the extra NRE of the Split is a guess of `25` to `70 M USD` | program office |

## 9 · The proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| CSG-1 | a professional prior art search | a dated report, with no product that joins a wallet Core, zero-key Skins and a roaming Skin |
| CSG-2 | a patent attorney opinion on each "first" sentence | a signed opinion naming the sentence |
| CSG-3 | the zero-key proof and a trusted amount | a rogue Skin cannot sign or change a confirmed amount |
| CSG-4 | `2`, `4` and `8` Skins on one Core, mixed sizes | each Skin shows its session at the stated class |
| CSG-5 | a Skin changes Core during a session | no lost chain state |
| CSG-6 | the link measured at C0, C1 and C2 | the stated rate and latency at the stated range |
| CSG-7 | the heat of a Skin alone | the hottest face point at or under `36.2 °C` |
| CSG-8 | supplier quotes and the break-even rerun | a written break-even number with the sweep |
| CSG-9 | a measured Skin of a Leaf 160 class | mass at or under `45 g`, thickness at or under `1.00 mm` |
| CSG-11 | a Core of year N drives a Skin of year N minus six | the Skin shows the right picture |
| CSG-12 | a pairing with no account and no fee | the user finishes it remotely |
| CSG-13 | a written legal opinion on questions M1 to M6 | each question answered in writing |
| CSG-14 | a Core cell lift-out by the end user | removal in under `30 s` with no tool |
