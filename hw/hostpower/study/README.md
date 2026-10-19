# BUDLUM LEAF · HOST POWER · THE STUDY TEAM

**Revision L.6.1 (proposed) · 2026-10-19 · Study team**. This team tests the idea of Ayaz against prior art, law and standards. It gives the program the strongest claim that is true. It is a risk review, not legal advice.

## 1 · What is here

| The file | The content |
|---|---|
| `PRIOR-ART.md` | `21` real products and patents, with URL, power path, host-gone behaviour and a read or search status. What is not new. What is open |
| `CLAIMS.md` | three claim sentences with gates, the recommendation, the rule for the word "first", the claim record |
| `STANDARDS.md` | Regulation 2023/1542 and 2023/1670 against the three tiers, safety classes, host classes H0 to H6, questions for a lawyer and a lab |
| `USE-CASES.md` | the ranked use cases, the best first pilot for the Turkish-first program, its risks and its data |
| `host_margin.py` | the margin of each host class against the `8.7 W` peak, the mean session power and the hand-over energy |
| `out/host_margin.txt` | the output of the script |

## 2 · How to run it

1. Run `python3 hw/hostpower/study/host_margin.py` from the repo root.
2. Read `hw/hostpower/study/out/host_margin.txt`.
3. Check the prose with `python3 tools/check_prose.py hw/hostpower/study/*.md`.

The script needs only the Python standard library and reads no other file.

## 3 · The key results

| The result | The value | The tag |
|---|---|---|
| the verdict on "first" | **not supported today**. A wallet with no cell (Ledger Nano S) and a computer that runs with the cell removed (Samsung No Battery Mode) exist | `[PUBLICATION]` |
| what remains open | the join of a chain session, a bridge between hosts and a power door. Not found in this survey | `[HYPOTHESIS]` |
| the recommended claim | "On a host, a Budlum Leaf 160 by 80 mm runs for as long as the host supplies power. A small bridge store keeps the wallet session when the power changes hands." | `[DECISION]` proposed |
| Bare tier and the law | likely outside Article 11 of 2023/1542 and the slate tablet class, if the store is a true capacitor and the body holds no cell | `[HYPOTHESIS]` |
| hosts that fail the `8.7 W` peak | plain PC port `2.5` to `4.5 W`, PoE class 1 and 2, Qi basic `5 W` | `[PUBLICATION]` and `[HYPOTHESIS]` |
| the best first pilot | counters and kiosks with a Budlum dock, host class H0, margin `+27.3 W` | `[HYPOTHESIS]` |

## 4 · The thesis damage

1. **The word "first" fails.** The program must not use it before gates HPS-1 and HPS-2.
2. **Capacity moves, and so does the story.** The Host Life Law is mostly known engineering. The new part is the join with the wallet, the session and the power door.
3. **The Bare tier has a legal gain that depends on chemistry.** A lithium-ion capacitor or a clock cell removes it.
4. **A weak host cannot carry the peak.** Samsung limits speed and brightness for the same reason. The Leaf needs a shaped peak or the Buffer.

## 5 · The open issues

| No. | The issue | The owner |
|---|---|---|
| 1 | no patent search was made. The web survey found one patent | patent searcher |
| 2 | pages for Zebra, Plugable, the Commission notice and others did not load. Their rows say Search | study team |
| 3 | the capacitor, battery and class questions L1 to L9 need a lawyer | regulatory lawyer |
| 4 | the PS class and the EPR margin, questions S1 to S6, need a laboratory | accredited lab |
| 5 | the efficiencies in `host_margin.py` are assumptions | powerpath team |
| 6 | the shaped peak test for a Bare Leaf on a weak host is not run | powerpath and continuity teams |
| 7 | the Turkish rule text was not read in full, only its date and number | Turkish counsel |

## 6 · The proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| HPS-1 | a professional prior art search of patents and products | a dated written report, with no product that joins a chain session, a host bridge and a power door |
| HPS-2 | a patent attorney opinion on every sentence that uses "first" | a signed opinion naming the sentence |
| HPS-3 | a written legal opinion on questions L1 to L9 | each question answered in writing |
| HPS-4 | an accredited lab report under IEC 62368-1 for one Leaf and one dock | ES1 and a stated PS class on every host input |
| HPS-5 | an ISO 16750-2 and ISO 7637-2 run on the vehicle cradle | no loss of function and no damage in the stated tests |
| HPS-6 | a Qi receiver test at an authorised lab | the receiver refuses an uncertified pad above `5 W` |
| HPS-7 | a pilot of `100` units on Budlum docks for `60` days | every pilot record kept, no chain state lost, hottest face point at or under `36.2 °C` |
| HPS-8 | the claim check against PRG-6 | each public sentence maps to a gate record or a study |

## 7 · The sources

The URLs are in `PRIOR-ART.md` for products and in `STANDARDS.md` for law and standards. Each row carries its status: Opened, Search or Recall.
