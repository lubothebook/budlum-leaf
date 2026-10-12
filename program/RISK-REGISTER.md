# BUDLUM LEAF · PROGRAM · THE RISK REGISTER, TOP 25

**Revision L.6.0 · 2026-10-12 · the Program Office**. This register replaces the table of `FINAL/13`, Section 13.7, for L.6.0. It draws on the findings of every team README in the tree on this date. Every mitigation keeps the target. A risk is never closed by a lower number. `[DECISION]`

## 1 · The scales

| The score | Likelihood (L) | Impact (I) |
|---|---|---|
| 1 | under `10 %` | a local fix, no gate moves |
| 2 | `10` to `30 %` | one gate slips under `1` month |
| 3 | `30` to `50 %` | one gate slips `1` to `3` months |
| 4 | `50` to `70 %` | a milestone slips, or a second partner is needed |
| 5 | over `70 %` | the critical path moves, or a claim is blocked |

The rank is `L x I`. Each L and I is `[HYPOTHESIS]` of the Program Office. The review runs every month. `FINAL/13`, Section 13.6.1.

## 2 · The register

| No. | The risk | L | I | L x I | The mitigation | The owner | The gate | The gap |
|---|---|---|---|---|---|---|---|---|
| R01 | the `508 ppi` tile on glass is not reached in time. The best shipping face is about `326 ppi` | 4 | 5 | 20 | two tile partners in parallel to M6, JBD chips, CMOS uIC per `2 x 2` pixels | `hw/display` | DSP-19 | G-40 |
| R02 | the display is `82 %` of the unit cost at `100 000` units, about `3 218 USD` | 4 | 5 | 20 | second partner, transfer yield learning, `1 205 USD` at `1 000 000` units | `program`, `hw/display` | DSP-19 | G-24 |
| R03 | the outdoor `30 ms` path needs a cell-site validator, configured grant and a `2.5 ms` TDD pattern. The operator owns them | 4 | 5 | 20 | an operator partner in Turkey, testnet V3 from `2028-08`, mini-slots and URLLC tables | `sim/latency`, `net/discovery` | DST-11 | G-42 |
| R04 | the validator render takes `38.5 ms` per frame on one CPU thread. The budget is `4.3 ms` | 4 | 5 | 20 | a GPU fixed-point render path in V1, tile-parallel render, one slice per tile | `validator/leaf-duty` | RG-18, DST-11 | G-42 |
| R05 | MEC-11 fails at `35 °C` ambient for every design. The `36.2 °C` limit leaves `1.2 K` | 5 | 4 | 20 | a program ruling names one test condition. The `36.2 °C` limit stays. Fixes F1 to F7 | `sim/thermal`, `program` | MEC-11 | PG-01 |
| R06 | the rest tile pitch must hold `10.000 +0 / -0.002 mm`. A `+1 µm` pitch fails the seam | 4 | 4 | 16 | seat metrology per tile, the `3.125 µm` image shift of `U1`, the closed loop per seam | `hw/display`, `hw/seam` | DSP-19, MEC-40 | G-43 |
| R07 | `25 W` holds as a sustained rate only on the regulated Leaf pad. A puck throttles to `8.5 W` | 4 | 4 | 16 | certify on the WPC test transmitter with the throttle law. Ship the regulated pad with the Leaf | `hw/energy`, `hw/dock` | ENR-24 | PG-02 |
| R08 | the modem, RF front end and eSIM fit a `10.0 x 8.0 x 0.80 mm` SiP | 4 | 4 | 16 | double-side moulded SiP at an OSAT, two modem vendors to M1, early RF-17 desense test | `hw/rf`, `hw/electronics` | RF-17 | PG-03 |
| R09 | RG-18 is not in the Budlum tree: session-key grant, domain tags, the firmware release record | 4 | 4 | 16 | the orders written into the tree with tests by M5 | `validator/leaf-duty`, chain team | RG-18, SW-22 | G-42, G-05 |
| R10 | the micro-LED tile, the micro cell, U1 and U6 have no second source | 4 | 4 | 16 | dual partners, a licence to second-source, the supply rule of `FINAL/13`, Section 13.3 | `program` | all | G-07 |
| R11 | the video session of `2` to `3 W` sustains only `1.73 W` at `25 °C` | 5 | 3 | 15 | fixes F1 to F7, less ring power by validator-side work, the Leaf stand with a fan | `sim/thermal` | MEC-11 | PG-01 |
| R12 | the edge-on hinge cracks before `10 000` cycles at `2θ = 35°` or `1 000` at `90°` | 3 | 5 | 15 | the `4 x 4` coupon from M0. Strain is `0.48 %` and `1.23 %` against a `3 %` yield | `sim/mechanics` | MEC-42, MEC-39 | G-41 |
| R13 | the Si-C anode swells over `22 %` and the cell misses `750 Wh/L` | 3 | 4 | 12 | a scaffold Si-C, coin-cell dilatometry in C1. The `600 Wh/L` floor holds `5.7 Wh` | `hw/energy` | ENR-22 | G-41 |
| R14 | no supplier co-fires a `1.10 mm` alumina feedthrough with a platinum via at volume | 3 | 4 | 12 | implant feedthrough houses, a glass-to-metal seal as the second path | `hw/energy` | ENR-22 | G-41 |
| R15 | the `2 µm` hinge copper carries `6.8 x 10⁴ A/cm²` during a charge and fails by electromigration | 3 | 4 | 12 | an EM test at `40 °C`, split strands, liquid-metal lines for the power pair | `hw/energy`, `sim/mechanics` | MEC-39 | G-41 |
| R16 | the four-sector series coil and `16` small magnets fail Qi2.2 alignment or foreign object tests | 3 | 4 | 12 | a WPC lab pre-test on the Q1 coupon in `2027`, the magnet ring to the MPP geometry | `hw/energy` | ENR-24 | PG-02 |
| R17 | Rel-15 handover fails the gate at one handover per `2 s` | 3 | 4 | 12 | DAPS or LTM in the modem purchase spec, the HOT shadow of DST-12 | `sim/latency`, `proto` | DST-12 | G-42 |
| R18 | a HOT shadow needs a bit-identical encoder build on two validators | 3 | 4 | 12 | a deterministic fixed-point encoder spec with conformance vectors | `proto`, `validator/leaf-duty` | DST-12, RG-18 | G-42 |
| R19 | the hostless Wi-Fi 7 combo, the eSIM and `11` of `14` Zero CPU entries stay conditional | 3 | 4 | 12 | purchase conditions per chip, a ruling of Ayaz on the eSIM | `fw/boot`, `proto` | SW-22 | G-17 |
| R20 | `128` cells at `4.45 V` fail the abuse set, or a vent harms the back skin | 3 | 4 | 12 | B-sample abuse tests before the C-sample, the vent to the back, the per-cell fuse | `hw/energy` | ENR-23 | G-14 |
| R21 | `U7` signs input batches at `480 Hz` with ML-DSA-87. A secure element is too slow | 4 | 3 | 12 | a session MAC per batch, ML-DSA once per second in the receipt | `fw/u7`, `rtl/u6` | SW-22 | G-16 |
| R22 | the sun at `600 W/m²` lifts the face over `36.2 °C` with the power off | 4 | 3 | 12 | the safe screen with the stated reason, a low-absorption cap coat | `sim/thermal` | MEC-11 | PG-01 |
| R23 | the EU rule of a user-removable battery reads `128` welded cells as not removable | 2 | 5 | 10 | the quadrant of `32` cells lifts out in under `3 s`. A legal review in P0 | `program` | MEC-40 | G-15 |
| R24 | the latency proof cannot place a validator inside `50 km`. A false claim of `50 km` passes `64` to `77 %` of trials | 3 | 3 | 9 | VRF challengers fall to `3` to `9 %` at `100 km`. UWB proof in the room, stake at risk | `net/discovery` | SW-24 | G-34 |
| R25 | the `50 MP` column misses CAM-9, or the RAW upload of `35 MB` takes `2.8 s` on 5G | 3 | 3 | 9 | the `0.56 µm` upgrade path, the deadline class stated before the shutter | `hw/camera`, `proto` | CAM-21 | G-13 |

**The sources of the numbers**. R02 `budget.py`. R03, R17 `sim/latency/README.md`. R04 `validator/leaf-duty/results/bench-render.txt`. R05, R07, R11, R22 `sim/thermal/README.md`. R06 `hw/display/README.md`. R13 to R15 `hw/energy`. R18 `proto/README.md`. R19 `fw/boot/README.md`. R21 `rtl/u6/README.md`. R24 `net/discovery/results/pol.json`. `[TREE]`

## 3 · The proposed program gaps

These gaps are not in `FINAL/16` yet. The Part 16 owner adds them. The Program Office does not write in `FINAL/`.

| No. | The item | The class | What it blocks |
|---|---|---|---|
| PG-01 | the thermal ruling: one test condition for the `36.2 °C` limit across Part 4 and Part 11 | **B** | MEC-11 and the video claim |
| PG-02 | the Qi2.2 power path on the tile body, with the Leaf pad as part of the product | **M** | ENR-24 certification |
| PG-03 | the modem SiP, its vendor and its RF front end | **M** | RF-17, DST-11 |

**A stale gap**. G-14 still names the withdrawn `LLZO/PEO` cell of `12.0 Wh`. The Part 16 owner rewrites it to the `128` micro cells. `[DECISION]`

## 4 · The watch list

| The item | The note | The owner |
|---|---|---|
| the `16 MiB` boot NOR | not on the part list of `HARDWARE/13` | `hw/electronics` |
| the "zero PWM" text of `HARDWARE/16` | a micro-LED face uses PWM at a `960 Hz` fundamental. The claim needs a rewrite | `hw/display` |
| the `3.5 mm` jack in a `4.00 mm` ring | `5 000` plug cycles and a side load | `hw/audio`, gate MON-22 |
| the coverage figures of Part 21 | full-square glass gives `63.5 %` and `50.0 %`, not `61 %` and `47.5 %` | `hw/display` |
| the Keccak core has no masking | the prefix registers hold key-equivalent data | `rtl/u6` |
