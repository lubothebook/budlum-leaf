# BUDLUM LEAF · HOST POWER · STUDY · 02 · THE CLAIMS

**Revision L.6.1 (proposed) · 2026-10-19 · Study team**. This is a risk review of wording. It is not legal advice. A patent attorney and a lawyer for the battery rules confirm every sentence before it is public.

## 1 · The rules that bind the wording

| The rule | The source | The effect here |
|---|---|---|
| a claim needs a gate, a raw data set and a date | law L7, `FINAL/00` Section 0.3 | each sentence below names its gates |
| a claim is published only at the step that supports it | `FINAL/12` Section 12.1 | the three sentences sit at different steps |
| three tiers of claim: Proven, Designed, Studied | `FINAL/12` Section 12.5.1 | the strong and defensible sentences are Designed |
| any unverified superlative is forbidden | `FINAL/12` Section 12.5.2 | the word "first" is a superlative |
| the Leaf is never a phone, tablet or computer in a claim | BRIEF Section 7, rule 8 | the sentences name Budlum Leaf and the size |
| the runtime names the member, the cassette and the session class | `FINAL/12` Section 12.5.3 | a claim names the tier and the host class |

## 2 · The verdict on the word "first"

**The word "first" does not survive today.** Row 15 of `PRIOR-ART.md` is a wallet with a screen and no cell. Row 8 is a computer that runs with the cell removed. Row 1 is a display with no cell. `[PUBLICATION]`

**The rule for the word "first"**. `[DECISION]` proposed for the Program Lead.

1. The word "first" stays out of every public and program text until gates HPS-1 and HPS-2 pass.
2. HPS-1 is a written prior art search by a professional searcher, dated within six months of the claim.
3. HPS-2 is a written opinion by a patent attorney on the exact sentence that uses the word.
4. The sentence names its scope: a wallet surface, a chain session, a bridge. It never says "first device".
5. Ayaz signs the sentence after both gates. The Program Lead logs it in the claim register (PRG-6).
6. A new product found by any later search voids the sentence until the opinion is renewed.

## 3 · The three sentences

### 3.1 The strong sentence (what Ayaz wants)

> **Budlum Leaf is the first wallet surface that lives as long as its host and carries a chain session to the next host.**

| The part | The gate that backs it | The state |
|---|---|---|
| "first" | HPS-1 search and HPS-2 attorney opinion | **fails today**. Rows 8 and 15 are close |
| "lives as long as its host lives" | continuity and power gates of `hw/hostpower`, run on each host class | not measured |
| "carries a chain session to the next host" | the continuity team hand-over gate, with a power gap and no lost chain state | not measured |
| the tag | Designed at step 3, Proven at step 4 | none yet |

**The verdict**. Do not use it. The risk is a false claim, a rival filing and a loss of trust in every other claim. `[DECISION]` proposed.

### 3.2 The defensible sentence (the recommendation)

> **On a host, a Budlum Leaf 160 by 80 mm runs for as long as the host supplies power. A small bridge store keeps the wallet session when the power changes hands.**

| The part | The gate that backs it | The state |
|---|---|---|
| "runs for as long as the host supplies power" | the powerpath gate: `P_host >= P_load + P_topup` per host class, with the `8.7 W` peak and the path loss | design target |
| the heat | the thermal gate: the hottest face point at or under `36.2 °C` in the host ambient | design target |
| "a small bridge store" | the continuity gate: `E_buffer >= P_peak x t_handover` | design target |
| "keeps the wallet session" | the same gate, with chain state checked after each gap | design target |
| the host classes it covers | the sentence names the class in the record: H0, H2 and H4 first | see `STANDARDS.md` |

**Why it holds.** It says "runs" and "keeps", which are measurable. It claims no rank. Every verb has a gate. `[DECISION]` proposed.

**The tier line.** The sentence is true of the Buffer and Full tiers. For the Bare tier the bridge is a capacitor of seconds. The Bare record says "ends the session cleanly", not "keeps the session". `[HYPOTHESIS]`

### 3.3 The safe sentence (for marketing)

> **Budlum Leaf 160 by 80 mm takes its power from the place it sits on. On a dock, a desk or a vehicle supply, the session goes on when you change places.**

| The part | The gate that backs it | The state |
|---|---|---|
| "takes its power from the place" | the powerpath gate on one named host | design target |
| "on a dock, a desk or a vehicle supply" | one gate record per named host. A host with no record is left out of the text | design target |
| "the session goes on when you change places" | the continuity gate with a stated gap time | design target |

**The limits of the safe sentence.** It makes no claim about hours, rank or novelty. It does not use "all day" or "no hardware", which are forbidden terms. `[PUBLICATION]` `FINAL/12` Section 12.5.2.

## 4 · The recommendation

**Use sentence 3.2 as the program claim at the Designed tier. Use sentence 3.3 for public text until a prototype passes the gates.** `[DECISION]` proposed.

| The use | The sentence | The earliest step |
|---|---|---|
| the program, the directive, the investor deck | 3.2 | step 1 and 2, with the word "design target" |
| the website and the press | 3.3 | step 3, after one host class passes |
| any use of "first" | 3.1 reworded after HPS-1 and HPS-2 | not before step 5 |

## 5 · The claim record

Each sentence has one record in the format of `FINAL/12` Section 12.3.

```text
ClaimRecord { claim_id, sentence, tier, host_class, gates[], raw_pointer,
              prior_art_search_date, attorney_opinion_date, owner, decision }
```

## 6 · The wording traps

| The trap | The wrong text | The right text |
|---|---|---|
| capacity | "no battery limit" | "the Leaf stops paying for capacity in grams, millimetres and heat" |
| the host | "powered by anything" | "powered by a named host class" |
| always on | "never turns off" | "stays on while the host supplies power" |
| the tier | "battery free" | "Bare tier, a capacitor store of seconds" |
| the device class | "a screen that needs no charger" | "Budlum Leaf 160 by 80 mm on a dock" |
| the law | "complies with the EU battery rules" | "design target; the legal route is under review" |

## 7 · The proposed gates of this file

| Gate | The test | The pass condition |
|---|---|---|
| HPS-1 | a professional prior art search of patents and products | a dated written report, with no product that joins elements 2, 3 and 5 of `PRIOR-ART.md` Section 6 |
| HPS-2 | a patent attorney opinion on each sentence that uses "first" | a signed opinion naming the sentence |
| HPS-8 | the claim check against PRG-6 | each public sentence maps to a gate record or a study |
