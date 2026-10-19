# BUDLUM LEAF · CORE AND SKIN · STUDY · 04 · THE CLAIMS OF THE SPLIT

**Revision L.7 candidate · 2026-10-19 · Study seat**. This is a risk review of wording. It is not legal advice. A patent attorney and a lawyer for the battery rules confirm every sentence before it is public. The rule for "first" is the one of `hw/hostpower/study/CLAIMS.md` Section 2.

## 1 · The rules that bind the wording

| The rule | The source | The effect here |
|---|---|---|
| a claim needs a gate, a raw data set and a date | law L7, `FINAL/00` Section 0.3 | each sentence names its gates |
| a claim is published only at the step that supports it | `FINAL/12` Section 12.1 | the three sentences sit at different steps |
| any unverified superlative is forbidden | `FINAL/12` Section 12.5.2 | "first" and "cheaper" are superlatives until a gate backs them |
| forbidden terms: all day, no hardware, a private display | `FINAL/12` Section 12.5.2 | a Skin is never "a screen with no hardware" |
| the Leaf is never a phone, tablet or computer in a claim | `hw/core/BRIEF.md` Section 7, rule 8 | the sentences say Budlum Leaf, Skin and Core |
| every result states its distance class | `hw/core/BRIEF.md` Section 8 | each sentence below carries a class |

## 2 · The verdict on the word "first"

**The word "first" does not survive today.** The Split in general is old. Packs, wireless panels, zero clients and one-box displays all sell. See `PRIOR-ART.md` rows 1 to 14. A Skin that holds no data a thief can use is the thin client idea, row 13. `[PUBLICATION]`

**The rule for the word "first".** `[DECISION]` proposed for the Program Lead.

1. The word "first" stays out of every public and program text until gates CSG-1 and CSG-2 pass.
2. CSG-1 is a written prior art search by a professional searcher, dated within six months of the claim.
3. CSG-2 is a written opinion by a patent attorney on the exact sentence that uses the word.
4. The sentence names its scope: a wallet Core, a zero-key Skin, a Skin that roams. It never says "first screen".
5. Ayaz signs the sentence after both gates. The Program Lead logs it in the claim register (PRG-6).
6. A product found by any later search voids the sentence until the opinion is renewed.

**The words "extreme" and "unique".** These are superlatives too. They follow the same rule. `[DECISION]` proposed.

## 3 · The three sentences

### 3.1 The strong sentence (what Ayaz wants)

> **Budlum Leaf Skins are the first screens with no key. One wallet Core serves all of them, and a Skin roams with its session.**

| The part | The gate that backs it | The state |
|---|---|---|
| "first" | CSG-1 search and CSG-2 attorney opinion | **fails today**. Thin clients and hardware wallets are near |
| "hold no key" | CSG-3, the zero-key proof of `hw/core/trust` | not measured |
| "one wallet Core serves all of them" | CSG-4, N Skins on one Core, of `hw/core/power` and `hw/core/fleet` | not measured |
| "roams with its session" | CSG-5, a Skin changes Core with no lost chain state, of `hw/core/session` | not measured |

**The verdict.** Do not use it. The risk is a false claim and a loss of trust in every other claim. `[DECISION]` proposed.

### 3.2 The defensible sentence (the recommendation)

> **A Budlum Leaf Skin holds no signing key and cannot sign. One Core serves several Skins of different sizes, and the session follows the Skin to another Core.**

| The part | The gate that backs it | The state |
|---|---|---|
| "holds no signing key and cannot sign" | CSG-3, with a rogue Skin test and a trusted confirmation of the amount | design target |
| "one Core serves several Skins" | CSG-4, at `2`, `4` and `8` Skins | design target |
| "of different sizes" | CSG-4 with a mixed set: Leaf 80, 160 and 480 | design target |
| "the session follows the Skin" | CSG-5 | design target |
| the link under it | CSG-6, the pixel or slice link measured at the stated class | design target |
| the heat of the Skin | CSG-7, the hottest face point at or under `36.2 °C` | design target |

**Why it holds.** It says "holds no" and "serves" and "follows". Each is a test. It claims no rank and no price. `[DECISION]` proposed.

**The condition on the first clause.** A Skin shows the screen. A rogue Skin can show a false amount. Hardware wallets own their screen for this reason (`PRIOR-ART.md` row 19). The clause stays only if CSG-3 proves a trusted confirmation. `[HYPOTHESIS]`

### 3.3 The safe sentence (for marketing)

> **A Budlum Leaf Skin is a thinner, lighter surface than a full Budlum Leaf of the same size. The energy, the radio and the wallet sit in the Core it pairs with.**

| The part | The gate that backs it | The state |
|---|---|---|
| "thinner" | CSG-9, a measured Skin of a Leaf 160 class: at or under `1.00 mm` | design target `0.90 mm` |
| "lighter" | CSG-9: mass at or under `45 g` against `68.0 g` | design target about `40 g` |
| "the energy, the radio and the wallet sit in the Core" | the powerpath and trust gates, per paired Core | design target |
| the class | the sentence is true at C0 only | see Section 4 |

**What the safe sentence does not say.** It makes no claim about price, rank, novelty or hours. A price claim needs gate CSG-8, since the model gives `15 %` less for a Skin and `9 %` less for a system of four. `[HYPOTHESIS]`

## 4 · What is open for a claim at each distance class

| The class | Sentence 3.3 | Sentence 3.2 | What is open |
|---|---|---|---|
| C0, a tether to `2 m` | holds, if CSG-9 passes | holds, if CSG-3 to CSG-7 pass | the join of one wallet Core, zero-key Skins and a roaming Skin |
| C1, a room to `30 m` | not as written. The Skin carries a decoder, a radio and a cell, so about `50 g` and not `40 g` | holds, as the Skin still has no signing key | the same join. "No processor" is false at C1 |
| C2, far to kilometres | does not hold. The Skin is the L.6.0 Leaf | holds only if the wallet moves to the far Core, which `hw/core/trust` must prove | the Core as a validator that keeps the wallet session. Not the Split as hardware |

**The weight at C1.** A `3.5 Wh` Skin cell is about `12 g` of cells at the density used in `COST.md`. The Skin is then about `52 g`. `[HYPOTHESIS]`

**At C2 the claim is a network claim.** The Leaf holds its modem, decoder and store. Remote compute is old (`PRIOR-ART.md` rows 21 to 25). What is open is the validator role and the zero-frame handover of the session. `[HYPOTHESIS]`

## 5 · The recommendation

**Use sentence 3.2 as the program claim at the Designed tier, for C0 and C1. Use sentence 3.3 for public text, for C0 only, until a prototype passes CSG-9.** `[DECISION]` proposed.

| The use | The sentence | The earliest step |
|---|---|---|
| the program, the directive, the investor deck | 3.2, with the words "design target" | step 1 and 2 |
| the website and the press | 3.3 | step 3, after CSG-9 |
| any use of "first", "extreme" or "unique" | 3.1 reworded after CSG-1 and CSG-2 | not before step 5 |

## 6 · The wording traps

| The trap | The wrong text | The right text |
|---|---|---|
| price | "a cheaper screen" | "a lighter, thinner surface". Price waits for CSG-8 |
| the Skin | "a screen with no hardware" | "a surface that holds no signing key" |
| the Core | "a phone in the pocket" | "the Core" |
| the link | "wireless, zero latency" | "a link measured at class C0, C1 or C2" |
| the key | "cannot be hacked" | "holds no signing key" |
| the distance | "works across the city" | "at C2 the Leaf is complete, and remote compute is the validator" |
| the law | "complies with the EU rules" | "design target. The legal class of the Core is under review" |

## 7 · The claim record

```text
ClaimRecord { claim_id, sentence, tier, distance_class, gates[], raw_pointer,
              prior_art_search_date, attorney_opinion_date, owner, decision }
```

## 8 · The proposed gates of this file

| Gate | The test | The pass condition |
|---|---|---|
| CSG-1 | a professional prior art search of patents and products | a dated written report, with no product that joins a wallet Core, zero-key Skins and a roaming Skin |
| CSG-2 | a patent attorney opinion on each sentence that uses "first" | a signed opinion naming the sentence |
| CSG-3 | the zero-key proof, a rogue Skin test and a trusted confirmation of the amount | a rogue Skin cannot sign and cannot change a confirmed amount |
| CSG-4 | `2`, `4` and `8` Skins on one Core, with mixed sizes | every Skin shows its session at the stated class |
| CSG-5 | a Skin changes Core during a session | no lost chain state and no dark frame beyond the stated gap |
| CSG-6 | the link measured at C0, C1 and C2 | the stated rate and latency at the stated range |
| CSG-7 | the heat of a Skin alone | the hottest face point at or under `36.2 °C` in free air |
| CSG-8 | supplier quotes and the break-even rerun | a written break-even number with the sweep |
| CSG-9 | a measured Skin of a Leaf 160 class | mass at or under `45 g`, thickness at or under `1.00 mm` |
