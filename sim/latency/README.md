# Latency team · input to photon · L.6.0

This directory holds the Monte Carlo model of the input-to-photon latency of the Leaf. It checks the table of Part 21, Section 21.5.7. It serves gate DST-11, and it informs DST-12, SW-21, SW-23 and SW-24.

## 1 · What is here

| File | Content |
|---|---|
| `model.py` | the stage models and the chain in absolute time |
| `run_all.py` | the four paths, the predicted action, every sweep, the plots and the summary |
| `results/results.json` | every number of the run |
| `results/summary.txt` | the same numbers as plain text |
| `plots/01..09_*.png` | the nine figures |

## 2 · How to run

1. Run `python3 run_all.py` in this directory. It takes about `95 s`.
2. Run `python3 run_all.py --quick` for a smoke test of `20 s`.
3. Read `results/summary.txt` for the numbers.

The main paths and the mitigation ladder use `2 000 000` samples each. Each sweep point uses `1 000 000`. Each heat-map cell uses `400 000`. The seeds are fixed, so a rerun gives the same numbers.

## 3 · The model

Each sample is one new action. The chain runs in absolute time, so the 5G frame phase at the downlink follows from the real delays before it. The scan-out phase runs free against the rest. `[GENERAL]`

| Stage | The model | The source |
|---|---|---|
| touch | wait `U(0, 2.08 ms)` for the `480 Hz` scan, then a controller gamma of mean `0.75 ms` | `[HYPOTHESIS]` |
| Wi-Fi 7 air | EDCA AC_VO per link: residual of a length-biased busy PPDU, AIFS, backoff `CW 3..7`, collisions, frame errors, retries | `[PUBLICATION]` IEEE 802.11be EDCA timing |
| Wi-Fi MLO | two links, `5 GHz` busy `30 %` and `6 GHz` busy `15 %`; the first link to win carries the frame | `[HYPOTHESIS]` |
| 5G TDD | `DDDSU`, `30 kHz`, slot `0.5 ms`, S slot `10:2:2` symbols; each opportunity found by its true position | `[PUBLICATION]` 3GPP TS 38.213 |
| 5G uplink | configured grant; `N2 = 12` symbols; gNB `0.3 ms`; retransmission via DCI, then the next U slot | `[PUBLICATION]` 3GPP TS 38.214 |
| 5G downlink | gNB `0.3 ms`, next D or S slot; HARQ-ACK after `N1 = 10` symbols; retransmission in the next D slot | `[PUBLICATION]` 3GPP TS 38.214 |
| HARQ | first BLER as set; a retransmission has `0.2 x` that BLER; `4` transmissions, then `8 ms` recovery | `[HYPOTHESIS]` |
| cell load | each DL opportunity is taken by others with a chance equal to the load; `0.1 x` the load with a priority QoS flow | `[HYPOTHESIS]` |
| handover | Poisson events; an action that starts in a gap waits its residual; a gap during the air stages adds the full gap | `[HYPOTHESIS]` |
| network | room `0.1 ms` RTT; city `1.2 ms` RTT with a `1 ms` GPON upstream cycle; cell-site UPF `0.3 ms`; far `80 ms` with WAN jitter | `[HYPOTHESIS]` |
| render | lognormal, mean `4.3 ms`, cv `0.12`, on demand | Part 21 mean `[DECISION]`, spread `[HYPOTHESIS]` |
| encode, decode | gamma, mean `1.5 ms` each, cv `0.10` | Part 21 mean `[DECISION]` |
| scan-out | U1 compose `0.2 ms`, the beam reaches the changed row after `U(0, 4.17 ms)`, micro-LED `0.05 ms` | `[HYPOTHESIS]` |
| predicted action | touch, a U1 pick of `0.2 ms`, the scan-out | Part 21 Section 21.5.6 |

## 4 · The key results

### 4.1 The four paths, `2 M` samples each

| Path | Mean | p50 | p99 | p99.9 | Part 21 mean | Part 21 p99 |
|---|---|---|---|---|---|---|
| Wi-Fi, room validator | `12.8` | `12.8` | `16.1` | `17.2` | `13.6` | under `20` |
| Wi-Fi, city validator | `13.9` | `13.9` | `17.3` | `18.5` | `14.7` | under `21` |
| 5G SA, cell-site validator | `16.5` | `16.4` | `21.5` | `23.5` | `15.4` | about `21` |
| far validator | `92.7` | `92.3` | `103.0` | `108.3` | `93.5` | over `100` |
| predicted action | `4.4` | `4.4` | `7.1` | `7.4` | about `5` | none |

All values are in ms. All values are `[HYPOTHESIS]` until DST-11 measures them on hardware. Figure `01_ccdf_paths.png` shows the tails.

### 4.2 The verdict on the Part 21 table

1. The Wi-Fi columns hold. The model gives `0.8 ms` less than the table. The table stays as a safe bound.
2. The 5G mean is wrong by `+1.1 ms`. The correct mean is `16.5 ms`, not `15.4 ms`.
3. The 5G uplink row is `2.8 ms`, not `2.3 ms`. The table left out HARQ at `10 %` and the U5 L2 time.
4. The 5G downlink row is `1.9 ms`, not `1.3 ms`. The table left out the gNB time and the DL HARQ.
5. The 5G p99 of about `21 ms` holds: the model gives `21.5 ms`. Write "about `22 ms`".
6. The claim "a sum of stage percentiles is not the percentile of the sum" holds. The sum of the stage p99 values is `27.9 ms` on 5G.
7. One retransmission costs `2.5 ms` on `DDDSU`, not "about `3 ms`". It is one TDD period.
8. The predicted action has a mean of `4.4 ms` and a p99 of `7.1 ms`. Add the p99 to the table.
9. The far column holds: a mean of `92.7 ms` and a p99 of `103 ms`.
10. The loaded public cell gives a mean of `34 ms` and a p99 of `50 ms` at `80 %` load. At `90 %` load the p99 is `69 ms`. The Part 21 range of `35` to `60 ms` holds for the mean and the p99 together.

The proposed 5G rows for Section 21.5.7 are: air uplink `2.8 ms`, air downlink `1.9 ms`, mean `16.5 ms`. The p99 is about `22 ms`, and the predicted p99 is `7 ms`. The Part 21 owner makes the edit. This team does not write in `FINAL/`.

### 4.3 The sensitivity of the 5G cell-site path

| The factor | The result (p99) | Figure |
|---|---|---|
| BLER, UL and DL, `0` to `50 %` | `19.7` to `25.4 ms`; BLER alone never breaks the gate | `03` |
| TDD `DDDSU`, `DDSUU`, `DSUUU`, `DDDSUDDSUU` | `21.5 ms` each | `04` |
| TDD `DDDDDDDSUU`, `DDDDDDDDSU` (`5 ms` period) | `25.4` and `25.7 ms`; `27.7 ms` at BLER `20 %` | `04` |
| load with a priority QoS flow, `0` to `95 %` | `21.5` to `21.6 ms` | `05` |
| load, best-effort scheduling | `29.7 ms` at `80 %`, `43.7 ms` at `90 %` | `05` |
| public cell, no configured grant, no QoS, central UPF | `40 ms` unloaded, `50 ms` at `80 %` | `05` |
| dynamic grant, no load | `23.2 ms` | none |
| validator at the operator edge, `2 ms` RTT | `23.1 ms` | none |
| render locked to a validator `240 Hz` tick | `24.2 ms` | none |
| Rel-15 handover, `1` per `10 s`, `1 %` failure | p99 `22.1 ms`, p99.9 `57.5 ms` | `06` |
| Rel-15 handover, `1` per `2 s` | p99 `47.7 ms`: the gate fails | `06` |
| DAPS or LTM handover, `1` per `2 s` | p99 `21.8 ms`, p99.9 `24.0 ms` | `06` |

### 4.4 What must hold for p99 under `30 ms` outdoors, gate DST-11

1. The network RTT from the gNB to the validator and back stays under `7.6 ms` at BLER `10 %`.
   The limit is `8.4 ms` at BLER `0 %`, `6.1 ms` at `30 %` and `4.7 ms` at `50 %` (figure `07`).
2. The validator sits at the cell site or the operator edge, with local breakout. A central UPF fails the gate.
3. The Leaf flow has configured grant and a delay-critical QoS flow. Without them, a loaded cell fails at `80 %` load.
4. The TDD period is `2.5 ms` or shorter. A `5 ms` period adds about `4 ms` to the p99.
5. Under `1 %` of the actions exceed `30 ms`. Rel-15 handover passes at one handover per `5 s` (`0.75 %`).
   It fails at one per `2 s` (`1.9 %`). DAPS or LTM removes the limit.
6. The validator renders on demand, not on its own frame tick. A tick costs `2.1 ms` of mean and `2.6 ms` of p99.
7. U2A and U5 never leave the session for a background scan or a power-save sleep. The model does not hold these events. `[HYPOTHESIS]`

### 4.5 The mitigations for the worst cases

The worst case outdoors is BLER `30 %`, load `80 %`, an operator-edge validator at `2 ms` RTT and a Rel-15 handover every `10 s`. It passes the gate at p99 `26.0 ms`, but its p99.9 is `60.7 ms`. Figure `08_mitigations.png` shows the ladder.

| Step | Mean | p99 | p99.9 | The design |
|---|---|---|---|---|
| worst case | `19.3` | `26.0` | `60.7` | none |
| robust MCS, BLER `1 %` | `17.9` | `22.3` | `59.3` | the input packet is under `200 B`, so a low MCS costs no capacity; DL first slice on the URLLC MCS table |
| mini-slots | `16.8` | `21.2` | `58.3` | a `2`-symbol PUSCH and a `7`-symbol PDSCH, type B |
| DAPS or LTM handover | `16.6` | `20.7` | `22.1` | make before break; the next validator holds the session state before the switch (DST-12) |
| capability-2 timing | `15.9` | `19.9` | `21.3` | U5 and the gNB run `N1 = 4.5` and `N2 = 5.5` symbols |
| tile-local scan restart | `14.0` | `17.1` | `18.3` | U1 restarts the scan of the one target tile when its slice lands |

All values are in ms. The handover step is the only step that fixes the p99.9. The tile restart gives the largest single gain on every path. `[HYPOTHESIS]`

The tile-local scan restart works because each tile has its own `200` rows. U1 starts that tile row at once, so the wait drops from `U(0, 4.17 ms)` to `U(0, 0.26 ms)`. On the Wi-Fi room path the mean drops to `10.9 ms` and the p99 to `13.1 ms`. The predicted action drops to a mean of `2.4 ms` and a p99 of `3.6 ms`. It needs a TCON mode in U1 and a check of brightness at the restart line. Gate SW-21 and DSP-19 own those tests. `[HYPOTHESIS]`

## 5 · The open issues

1. Every stage time is a model value. DST-11 must measure each stage on the U1, U2A, U5 and U6 silicon. `[HYPOTHESIS]`
2. The Wi-Fi model holds only channel access, collisions and frame errors. It has no off-channel scan, no TWT sleep and no rate-control collapse.
3. The first slice is assumed to fit one slot. At the cell edge a large slice needs two slots, and the mean grows by `0.5 ms`.
4. The handover model treats the gaps as independent events. A measured gap distribution from the operator replaces it.
5. The render spread of cv `0.12` has no source. A validator under load has a longer tail. The model takes a measured render trace as soon as one exists.
6. The far path is not a DST-11 path. Its jitter model is a simple WAN tail.
7. The operator owns the TDD pattern. The Leaf cannot choose it, so the S-slot and mini-slot mitigations need the operator.
