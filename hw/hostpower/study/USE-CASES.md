# BUDLUM LEAF · HOST POWER · STUDY · 04 · THE EXTERNAL USE CASES

**Revision L.6.1 (proposed) · 2026-10-19 · Study team**. The ranking is the team's judgement. Every rank is a `[HYPOTHESIS]` until the pilot gives data. The host classes H0 to H6 are in `STANDARDS.md` Section 5.

## 1 · The two questions

| The question | The test |
|---|---|
| where does host life matter most? | hours per day on a host, and the cost of a flat cell or a hot cell |
| where is the best first pilot? | the value above, the host class margin, the standards burden and the trust risk |

The two ranks differ. The place that gains most is not the place to start.

## 2 · The ranking by host life value

| Rank | The case | The host class | Why host life matters here | The main cost |
|---|---|---|---|---|
| 1 | vehicles: taxi, fleet, intercity bus | H3 | the hours are long. Samsung names hot vehicles as the reason for No Battery Mode. `[PUBLICATION]` | load dump, EMC and a hot cabin |
| 2 | counters and kiosks: retail, cafe, bank branch, reception | H0, H2 | power is always there. A flat cell is a lost sale | the public setting and shared hosts |
| 3 | industrial HMI and machine panels | H4, H3 | a panel runs a shift and sits on a machine. PoE and vehicle supply are common | dust, shock, isolation and plant rules |
| 4 | desks: office, home, trading | H0, H2 | the Leaf rests on a dock for hours and leaves for minutes | the lowest gain, the lowest risk |
| 5 | medical carts | H4, H5 | carts already use hot swap power. `PRIOR-ART.md` row 18 | IEC 60601 class and hospital rules. `[HYPOTHESIS]` |
| 6 | glasses with a worn pack | H5 | the Frame has a `2` to `3 Wh` temple cell. A pack lengthens the day | heat near the face and a cable on the body |
| 7 | aircraft seats | H2 | seat power is steady. The flight is long | airworthiness rules for any seat device. `[HYPOTHESIS]` |

**Samsung is a signal.** A large maker built No Battery Mode for kiosks and vehicles. That shows a market need for rows 1 and 2. `[PUBLICATION]` `PRIOR-ART.md` row 8.

## 3 · The ranking as a first pilot

| The case | Value | Margin | Standards load | Trust risk | The pilot fit |
|---|---|---|---|---|---|
| counters and kiosks with a Budlum dock | high | `+27.3 W` on H0 | low | low if the program owns the dock | **best** |
| desks | medium | `+27.3 W` on H0, `+9.9 W` on H2 | low | low | second |
| industrial HMI | high | `+2.4 W` on PoE class 3 | high | low | later |
| vehicles | highest | set by the adapter | high | medium | after the transient lab gate |
| medical carts | medium | set by the cart | highest | medium | no |
| glasses with a pack | medium | set by the pack | medium | low | later |
| aircraft seats | low | set by the seat | highest | low | no |

## 4 · The recommended first pilot

**Counters and kiosks with a Budlum-owned dock, in one Turkish city.** The host is H0, a wall dock. Its margin over the peak is `+27.3 W`. `[HYPOTHESIS]`

### 4.1 The reasons

1. **The program owns the host.** The dock is Budlum hardware, so the power door has one trusted host. Public USB risk is outside the pilot.
2. **The power is the easy class.** H0 needs no vehicle test and no PoE isolation. The peak of `8.7 W` has a wide margin.
3. **The host life data is rich.** A counter session gives hours on the host and many hand-overs a day. Those data feed the continuity and thermal gates.
4. **It fits the program.** Gate PG-8 is a pilot of `100` units, one workshop and a claim file. `[TREE]` `FINAL/13`
5. **It fits the wallet.** A counter is where a payment is confirmed. The wallet pays from a session grant. `[TREE]` `FINAL/17` Section 17.14
6. **It keeps the legal path short.** The Turkish rule in force has no removability clause that the team found. `STANDARDS.md` Section 3.3
7. **It makes the safe sentence true.** The sentence of `CLAIMS.md` Section 3.3 names a dock. The pilot dock gives the record.

### 4.2 The risks

| The risk | The answer |
|---|---|
| shared counters invite a hostile host | use only Budlum docks in the pilot. No public USB port. A third party dock is out of scope |
| heat at a counter in a warm shop | the thermal gate runs at the shop ambient. The pilot logs the ambient |
| a power cut at the shop | the Buffer tier carries the hand-over. Chain state is checked after every gap |
| the Bare tier cannot carry a peak on a weak host | the pilot uses H0 only. A weaker host waits for the shaped peak test |
| the legal class of the Leaf | gate HPS-3 runs before the pilot sale. The pilot units are on loan |
| a claim runs ahead of the data | the pilot text uses sentence 3.3 only. The word "first" stays out |
| the pilot proves the easy case only | vehicles follow as the second pilot, after gate HPS-5 |

### 4.3 The second pilot

**A taxi or a fleet vehicle with a cradle and a type tested PD adapter.** The value is highest. The risk is highest. It starts after gates HPS-4 and HPS-5 and a thermal run at a cabin ambient. A dashboard can reach `60` to `70 °C` in sun, which is above the skin limit of `36.2 °C`. `[HYPOTHESIS]` search summary, dash cam sources.

## 5 · The data the pilot must collect

| The record | The use |
|---|---|
| hours on the host per day, per unit | the claim "runs for as long as the host supplies power" |
| count and length of every hand-over | the Buffer energy gate |
| chain state check after every power gap | the continuity gate |
| hottest face point and the shop ambient | the thermal gate |
| the number of power cuts at the host | the ride-through gate |
| the user note on a hand-over | the trust and comfort check |

## 6 · The proposed gate of this file

| Gate | The test | The pass condition |
|---|---|---|
| HPS-7 | a pilot of `100` units on Budlum docks for `60` days | every record of Section 5 kept, no chain state lost, hottest face point at or under `36.2 °C` |
