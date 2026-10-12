# BUDLUM LEAF · PROGRAM · THE PLAN FROM CONCEPT TO MASS PRODUCTION

**Revision L.6.0 · 2026-10-12 · the Program Office**. This plan replaces the phase table of `FINAL/13`, Section 13.1, for the L.6.0 architecture. `FINAL/21` is the source of truth. The plan keeps every target of Part 21. It never trades a target for a date. `[DECISION]`

## 1 · What is here

| The file | The content |
|---|---|
| `PLAN.md` | the phases, the milestones, the critical path, the gate map |
| `schedule.py` | the critical path solve over `35` work packages, writes `schedule.json` |
| `PARTNERS.md` | the candidate partners per technology, with the reasons |
| `RISK-REGISTER.md` | the top `25` risks, linked to a gate, a gap and an owner team |
| `BUDGET.md`, `budget.py` | the NRE and the unit cost model, writes `budget.json` |

**How to run it**.

1. Run `python3 schedule.py` in `program/`.
2. Run `python3 budget.py` in `program/`.
3. Read `schedule.json` and `budget.json`. Each script runs in under `1 s`.

## 2 · The phases

Month `0` is `2026-11-01`. Every duration is `[HYPOTHESIS]` until a partner signs a quotation. The dates are the output of `schedule.py`. `[TREE]`

| Phase | The window | The work | The exit gate set |
|---|---|---|---|
| **P0 Concept freeze** | `2026-11` to `2027-02` | L.6.0 frozen, partner short list, NDAs, sample orders, coupon designs | every open issue of the team READMEs has a ruling or an owner |
| **P1 Technology proof** | `2027-02` to `2029-01` | the `508 ppi` tile, the micro cell, the `4 x 4` hinge coupon, the sector coil, U1 and U6 silicon, the modem SiP, RG-18 beta | DSP-19 on a coupon, ENR-22 on an A-sample, MEC-42, ENR-24 on a pad coupon |
| **P2 EVT** | `2029-07` to `2029-11` | `200` working Leafs from the `128`-tile body and B module rev A | MEC-39 to MEC-42, DSP-17, DSP-18, RF-21 to RF-23, SW-21 to SW-23 |
| **P3 DVT** | `2029-11` to `2030-12` | `500` units on production tools, the full gate list, the C-sample cell | ENR-22, ENR-23, CAM-21, MON-21 to MON-23, DST-11, DST-12 |
| **P4 Certification** | `2030-12` to `2031-06` | Qi2.2 `25 W`, GCF, PTCRB, the operator, safety, battery, SAR, the EU battery rule | ENR-24 certificate, DST-11 on an operator network |
| **P5 PVT and pilot** | `2031-06` to `2031-10` | `2 000` units at line rate, the pilot in Turkey, the service workshop | the line yield, the field return rate, PRG gates |
| **P6 Mass production** | from `2031-10` | SOP, the second line in Asia, the ramp to `1 000 000` per year | the monthly gate review of `FINAL/13`, Section 13.6.1 |

**The total**. `59` months from concept to SOP. `[TREE]` `schedule.py`

## 3 · The milestones

| No. | The milestone | The date | The proof |
|---|---|---|---|
| M0 | L.6.0 concept frozen, partner NDAs signed | `2027-02` | the signed NDAs and the sample orders |
| M1 | first `508 ppi` test tile lights at `50.0 µm` pitch | `2028-02` | a DSP-19 coupon photograph and its pitch scan |
| M2 | first micro cell A-sample cycles at `600 Wh/L` or more | `2028-06` | ENR-22 data on `20` cells |
| M3 | the `4 x 4` hinge coupon passes `10 000` cycles at `25 %` | `2027-10` | MEC-42 and MEC-39 raw data |
| M4 | U1 and U6 first silicon on the bench | `2028-12` | SW-21 bench data |
| M5 | RG-18 beta: a forged frame is slashed on a testnet | `2028-08` | the RG-18 acceptance test of `FINAL/21`, Section 21.7 |
| M6 | integrated tile passes DSP-19 with uIC and TGV glass | `2029-01` | the seam gap scan at `50.0 µm` or less |
| M7 | EVT: the first Leaf stretches, shows and charges | `2029-11` | the EVT gate report |
| M8 | DVT complete, full gate list | `2030-12` | the DVT gate report |
| M9 | Qi2.2 `25 W` certificate and 5G carrier approval | `2031-06` | the WPC listing and the GCF and PTCRB certificates |
| M10 | SOP | `2031-10` | the first lot of the line |

## 4 · The critical path

The critical path runs through the display. `[TREE]` `schedule.py`

**T00 → D2 → D3 → D4 → EVT → C5 → DVT → M4 → PVT → MP**.

| The step | The months | Why it is on the path |
|---|---|---|
| D2 pixel uIC, `28 nm` | `14` | the `508 ppi` drive fits only a CMOS uIC per `2 x 2` pixels. LTPS PWM does not fit. `[TREE]` `hw/display` |
| D3 integrated tile | `9` | uIC, TGV glass, `16 µm` edge margin and the black cut face meet for the first time |
| D4 `128`-tile EVT set | `6` | known-good tiles and laser repair for `P(< 5 dead) = 0.99994` |
| C5 cell C-sample and abuse file | `7` | IEC 62133-2 and UN 38.3 need the DVT-grade cell |
| M4 5G carrier certification | `6` | the outdoor `30 ms` path needs a certified modem on a live network |

### 4.1 The six named tracks

| The track | Its float | The start of its longest item | What closes it |
|---|---|---|---|
| `508 ppi` micro-LED tiles | `0` months | D2 and D1 in parallel from `2027-02` | DSP-19, gap G-40 |
| micro cells | `5` months to EVT, `0` at C5 | C2 can and feedthrough supplier | ENR-22, ENR-23, gap G-41 |
| edge-on hinge | `15` months | H1 coupon | MEC-39, MEC-42, gap G-41 |
| Qi2.2 certification | `2` months | Q3 at a WPC laboratory | ENR-24 |
| 5G modem packaging | `5` months in design, `0` at M4 | M2 SiP in `10.0 x 8.0 x 0.80 mm` | RF-17, DST-11 |
| validator software RG-18 | `22` months in V1 to V3, `3` at V4 | V1 fixed-point render | RG-18, SW-22, DST-12, gap G-42 |

**The hinge float is a trap**. The hinge has `15` months of float only while it passes on the first coupon. A laminate change for the graphite leaves of `sim/thermal` re-runs MEC-42. So the hinge coupon starts at M0 anyway. `[DECISION]`

**The RG-18 float is a trap too**. The reference render takes `38.5 ms` per `1600 x 3200` frame on one CPU thread. The budget is `4.3 ms`. `[TREE]` `validator/leaf-duty/results/bench-render.txt` A GPU fixed-point render path joins V1. `[DECISION]`

### 4.2 How the path shortens, with no target change

1. Run two display partners in parallel to M6. The faster one sets D4.
2. Build a `32`-tile quadrant EVT-0 at `2028-10` from D1 tiles. It de-risks the body three quarters early.
3. Start C5 abuse tests on B-samples. Only the final file waits for the C-sample.
4. Start GCF pre-tests on EVT units. Only the final approval waits for DVT.
5. Each step keeps `508 ppi`, `7.2 Wh`, `25 W` and `30 ms` as written. `[DECISION]`

## 5 · The work package owners

| The track | The owner team | The gates |
|---|---|---|
| tile, seam, warp, yield | `hw/display`, `hw/seam`, `rtl/u1` | DSP-17, DSP-19, MEC-40 |
| micro cell, pack, power tree | `hw/energy` | ENR-22, ENR-23, ENR-24 |
| body, hinge, skin | `sim/mechanics`, `cad/l6` | MEC-39, MEC-41, MEC-42 |
| heat | `sim/thermal` | MEC-11, ENR-24 |
| radios, antennas, modem SiP | `hw/rf`, `hw/electronics` | RF-17, RF-21 to RF-23 |
| camera, audio | `hw/camera`, `hw/audio` | CAM-21, MON-22 |
| dock and Leaf pad | `hw/dock` | SW-20, ENR-24 |
| decoder and check | `rtl/u6` | SW-21, SW-22 |
| boot and secure element | `fw/boot`, `fw/u7` | SW-22, FW-1 to FW-3 proposed |
| wire protocol | `proto` | DST-4, DST-11, DST-12, SW-23 |
| nearest validator | `net/discovery` | SW-24, DST-12 |
| validator duty | `validator/leaf-duty` | RG-18 |
| latency | `sim/latency` | DST-11 |
| plan, partners, risk, budget, certification | `program` | PRG gates, G-15, G-24, G-27 |

## 6 · The gaps this plan closes

| Gap | The item | How this plan answers it |
|---|---|---|
| G-07 | partner samples and second sources | `PARTNERS.md` names two or more candidates per technology |
| G-15 | the certification gap analysis | Section 7 and phase P4 |
| G-24 | the cost model numbers | `BUDGET.md` and `budget.py` |
| G-27 | the schedule with dates and resources | Sections 2 to 4 and `schedule.py` |

**The rule of `FINAL/16`**. A gap closes only with an artefact. These four close as plans. They close as facts with signed quotations. `[DECISION]`

## 7 · The certification file of L.6.0

| The rule | The subject | The phase |
|---|---|---|
| WPC Qi2.2, `25 W` magnetic power profile | the sector coil receiver | P4, gate ENR-24 |
| 3GPP conformance through GCF and PTCRB | the `U5` 5G SA modem | P4, gate DST-11 |
| IEC 62368-1 | the electrical safety and the touch temperature | P3 |
| IEC 62133-2 and UN 38.3 | the `128` micro cells and the B cell | P3 |
| EU 2023/1542, Article 11, from `2027-02-18` | the user-removable battery `[PUBLICATION]` Regulation (EU) 2023/1542 | P3, a quadrant holds `32` cells and lifts out in under `3 s` |
| Directive (EU) 2022/2380 | the common charger, met by the USB-C port part `[PUBLICATION]` | P3 |
| RED 2014/53/EU, BTK Turkey, FCC | the radios | P4 |
| SAR, IEC/IEEE 62209-1528 | the ring on the face and the bar on the edge | P4 |
| RoHS and REACH | the materials | P3 |

**The order of the markets**. Turkey first, then the European Union. `[DECISION]` `FINAL/13`, Section 13.4.
