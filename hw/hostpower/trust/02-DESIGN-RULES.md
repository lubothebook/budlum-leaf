# BUDLUM LEAF · HOST POWER · TRUST · 02 · THE DESIGN RULES

**Revision L.6.1 (proposed) · 2026-10-19 · TRUST team**. The model is `hostauth.py`. The tests are `tests/test_hostauth.py`. Every new rule here is a proposal to the Program Lead. A proposal carries `[HYPOTHESIS]` until it is signed.

## 1 · The law, as extended

**The law of `fw/boot`**. Every seam leaf and every B pad stays at `0 V` until its handshake passes. `[DECISION]` ENR-19, MON-16.

**The extension**. The host power pads fall under the same law. Power is a door, and the host never holds the key. `[DECISION]` BRIEF Section 3.

Three corrections come from the model. Each one changes the wording of the law.

1. **Dead means no rail is connected**. It does not mean `0 V` at every terminal. A Qi coil and a host cable carry voltage that the Leaf cannot switch off.
2. **The host touches two things before its handshake ends**. They are the bridge rail and the sideband parser. Both get hard limits below.
3. **The handshake proves the adapter, not what stands behind it**. The host needs its own record, in addition to the pad handshake.

## 2 · The island rail

**Rule R-I1**. `U7` and the `U4` ROM never take power from the host rail. They take it from a regulated bridge rail only. `[HYPOTHESIS]`

**Rule R-I2**. The bridge rail has a capacitor store, a hysteretic pre-regulator and a brownout detector at `2.4 V`. `[HYPOTHESIS]`

**Rule R-I3**. `U7` stays in reset until the rail has held its window for a fixed time. The brownout detector trips before the island rail leaves its window.

**Rule R-I4**. With a B cell, the `1.8 V` always-on LDO feeds from the cell and not from the host. The Bare tier feeds from the island store.

The simulation `simulate_rail` shows the margin. `[HYPOTHESIS]` Every parameter is an assumption until bench gate HST-T3 runs.

| Case, 100 µF bridge, 20 mA load | Result |
|---|---|
| ride through to the brownout trip | `4.5 ms` |
| host drop of `2 ms` | island stays at `1.80 V` |
| host drop of `20 ms` | detector trips at `4.5 ms`, the rail leaves its window `2.45 ms` later |
| `20 V` spike, `1 µs` to `5 ms` | island stays at `1.80 V` |

## 3 · The dead-pad law for host power

**Rule R-D1**. Two switches stand in series between a host and the Leaf. The adapter holds one. `S_SEAT` of the Leaf holds the other.

**Rule R-D2**. A host never touches a Leaf pad. It connects through a Budlum adapter: the port part, the dock or the quadrant node.

**Rule R-D3**. The adapter passes the pad handshake of ENR-19 first. A failed handshake leaves the pads at `0 V`. That state is class P0.

**Rule R-D4**. After the pad handshake, the pads carry class P1 only. P1 is a power-only low class. The data lanes stay dead.

**Rule R-D5**. The Leaf, as the sink, requests a contract. It requests a higher voltage only after U7 grants the class.

**Rule R-D6**. The bridge envelope is analog. A window comparator and a current limit hold it, with no firmware in the path. It is the same for every class. `[HYPOTHESIS]`

**Rule R-D7**. For wireless power, dead means the rectifier output is isolated from the rails. An unauthenticated field gets P1. Qi 1.3 requires receiver-side authentication above `5 W`. `[PUBLICATION]` Wireless Power Consortium, Qi 1.3, IEC 63563-9.

**Rule R-D8**. The quadrant node runs the Qi authentication, and then signs a vouch to `U7`. A vouch carries class P2 at most.

### 3.1 · The classes

All windows and powers are `[HYPOTHESIS]`. The thermal team and the power-path team own the final values.

| Class | Volts at the Leaf input | Maximum power | Per VHV leaf, low edge | Lanes | What it feeds |
|---|---|---|---|---|---|
| P0 | `0 V` | `0 W` | none | dead | nothing, the pads stay dead |
| P1 | `4.75` to `5.50 V` | `0.5 W` | `0.05 A` | dead | the islanded ring, `0.40 W`, and the safe screen |
| P2 | `8.1` to `9.9 V` | `15 W` | `0.93 A` | dead, or owner allowed | a session and a top-up |
| P3 | `13.5` to `16.5 V` | `27 W` | `1.00 A` | dead, or owner allowed | the full load and a fast top-up |

The leaf rating is `1.5 A`. `[TREE]` `hw/energy/03` Section 2.1. The test `test_every_class_row_inside_the_leaf_rating` checks the table.

## 4 · The HostRecord

The record is `105` bytes. The signature adds `64`. The frame is `169` bytes, fixed. `[HYPOTHESIS]`

| Field | Size | Meaning |
|---|---|---|
| version | `1` | the value `1` |
| chain id | `8` | the chain of the Leaf |
| host key id | `32` | the ed25519 public key of the host, as a validator address is |
| kind | `1` | `0` the host signs for itself, `1` an adapter vouches |
| class | `1` | the class requested, `1` to `3` |
| maximum power, window | `4 + 2 + 2` | the power and the volts the host claims, inside its class row |
| role | `1` | `0` none, `1` validator, a claim only |
| lanes | `1` | `1` asks for the data lanes |
| expiry | `8` | an anchor height, the chain clock of the light client |
| counter | `8` | strictly above the stored counter of this key |
| nonce | `32` | the `U7` challenge, echoed |
| measured volts, amps | `2 + 2` | what the host reads at its own output |

The signature covers the tag `BDLM_LEAF_HOST_RECORD_V1` and the record. The tag is a sixth tag for open issue U7-3 of `fw/u7`.

### 4.1 · The handshake

1. The pad handshake of ENR-19 passes. The Leaf sits at P1, or at P0 when the volts are wrong.
2. `U7` sends one random `32` byte nonce. Nothing else leaves `U7`.
3. The host answers with the frame.
4. The bounded parser checks the length, the version and every enum. A bad frame ends here.
5. `U7` checks the nonce, the chain, then the ed25519 strict signature.
6. `U7` looks the key up in the trust store. An unknown key ends here.
7. `U7` checks the counter, the expiry, the anchor age, the ceiling and the class row.
8. `U7` compares the measured volts of the host with its own reading, within `5 %`.
9. `U7` commits the counter to NVM, and then programs the limiter and the contract request.
10. The grant dies after `30 s` unless a fresh record renews it.

Every failed step leaves the Leaf at P1. A failed step never ends below P1 when the adapter passed.

### 4.2 · The rules of the record

**Rule R-H1**. The nonce is single use. The challenge carries no wallet address and no stable value. The host learns nothing before it proves itself.

**Rule R-H2**. The check is ed25519 `verify_strict`, as in `fw/u7/src/session.rs`. `[TREE]` The model refuses a malleable S and a small-order key.

**Rule R-H3**. The counter lives in NVM. A RAM counter is void, because the host controls every power cycle.

**Rule R-H4**. The expiry is an anchor height. If the anchor is older than `6 h` of uptime, every record counts as expired. `[HYPOTHESIS]`

**Rule R-H5**. A request above the ceiling of the key is refused. It is not clipped. The refusal is a signal.

**Rule R-H6**. The claimed window and power must sit inside the class row. A vouch never exceeds P2.

**Rule R-H7**. The power channel binding: the host signs the volts it reads. `U7` compares them with its own ADC. A relay shows other volts.

**Rule R-H8**. Only the owner adds a key to the trust store, with a physical press and a safe-screen line that names the key and the ceiling.

**Rule R-H9**. The data lanes open only when four conditions hold. The owner allowed lanes for this key. The kind is host. The class is P2 or higher. The record asks.

## 5 · The policy table

| Row | The condition | The class | Lanes | The render |
|---|---|---|---|---|
| R1 | no attach, or the adapter fails ENR-19 | P0 | dead | none from the host |
| R2 | the adapter passes, the host is unknown, or any check fails | P1 | dead | safe screen or the session on the Leaf radios |
| R3 | an adapter vouches for a dumb source | P2 at most | dead | as R2 |
| R4 | a valid record from a key paired by the owner | its class, at the ceiling at most | by Rule R-H9 | as R2 |
| R5 | any valid row with the role validator, key in the active set | the class of its own row | by Rule R-H9 | stream only after SW-22 and the admission of `U7` |
| R6 | a fresh check fails later | falls to P1 within `30 s` | dead | unchanged |

The test `test_every_policy_row_is_reached` reaches all six rows.

### 5.1 · What a class never grants

| The authority | Granted by a class | Who decides it |
|---|---|---|
| a wallet signature | never | `U7`, with the owner |
| a firmware slot or a floor | never | the program key and a clean trial |
| the content of the display | never | SW-22 and the admission of `U7` |
| the trust anchor and the clock | never | finality proofs |
| the thermal limit | never | the NTC comparator, ENR-16 |
| the time of an update | only the energy to start it | `U7`, by Rule R-A1 |

The test `test_render_needs_no_power_class` and the test `test_validator_host_with_a_bad_stream_key` show that power and render are independent.

## 6 · The validator host

**Rule R-V1**. A validator host is trusted for rendering only after SW-22 passes. It is never trusted for power authority.

**Rule R-V2**. The role field is a claim. It counts only when the host key is in the active set. It never moves the class.

**Rule R-V3**. The stream key must be in the active set, and the anchor must be fresh. A stale anchor shows the safe screen.

**Rule R-V4**. A host is never the only network path of the Leaf. The Leaf keeps its own Wi-Fi and 5G radios.

**The reason for R-V3**. `fw/u7/src/session.rs` refuses a hello only if the claimed head is more than `200` blocks above the anchor. The validator makes that claim. The light client has no time bound. A host that is the only path can withhold a rotation and keep a rotated-out validator alive. `[TREE]`

## 7 · The atomic-commit rule

**The rule**. No signature, counter, key, floor or slot marker straddles a power loss. A step either completes or leaves the old state. `[HYPOTHESIS]`

| Rule | The statement |
|---|---|
| R-A1 | `U7` starts an atomic step only when the island store holds `1.5` times the energy of that step |
| R-A2 | during a signing step, the host switch is open and `U7` runs from the island store |
| R-A3 | the counter burns before the signature is released, so a counter is never used twice |
| R-A4 | `U7` verifies its own signature before release. A failed check releases nothing and counts a fault |
| R-A5 | after `3` faults on one attachment, `U7` refuses to sign while the host stays attached |
| R-A6 | NVM keeps two slots with a sequence and a checksum. The checksum is the commit point |
| R-A7 | an update writes the inactive slot in chunks, with a progress commit after each chunk |
| R-A8 | the floor and the active slot flip in one commit, after one clean trial |
| R-A9 | a trial cut by a power loss counts. After `3` cuts the update is deferred, and the old release stays |
| R-A10 | pairing, unpairing and the fault count are NVM commits under R-A6 |

The tests prove the rules.

| Test | What it proves |
|---|---|
| `test_island_signing_survives_a_host_cut_at_every_phase` | a host cut at any phase leaves one valid signature and one burned counter |
| `test_the_naive_design_loses_or_reuses` | a design that feeds `U7` from the host loses a signature or reuses a counter |
| `test_nvm_cut_at_every_step_reads_old_or_new` | a cut at any NVM step reads the old or the new value |
| `test_update_cut_at_every_tick_never_bricks_and_resumes` | all `16` cut points of an update leave a bootable slot and resume |
| `test_a_hostile_host_cutting_every_trial_only_defers` | repeated cuts deny the update and never brick or lower a floor |

## 8 · The island store

Isolated signing needs energy inside the island. The ML-DSA-87 signing loop repeats `3.85` times on average. `[PUBLICATION]` NIST FIPS 204, Table 1. The signing energy of `U7` is not measured. `[HYPOTHESIS]` open issue U7-7.

The store covers one loop iteration, the mean signature, or the `99.99` percent signature. The window is `3.3` to `2.2 V`, and the margin is `1.5`. Output of `hostauth.py`.

| Mean signing energy | One iteration | Mean signature | `99.99` percent signature, `31` iterations |
|---|---|---|---|
| `1 mJ` | `0.13 mF` | `0.50 mF` | `3.99 mF` |
| `5 mJ` | `0.64 mF` | `2.48 mF` | `19.96 mF` |
| `20 mJ` | `2.58 mF` | `9.92 mF` | `79.85 mF` |

**The choice**. Size the store for one iteration. `U7` signs one iteration isolated, reconnects to recharge, and goes on. The tail of the loop then costs time and not capacitance.

**The cost of that choice**. The recharge pattern shows the loop count to the host. The entropy of a geometric count with a mean of `3.85` is `3.18` bits per signature. Padding the pattern removes it. Whether the count is secret is a question for the silicon certification. `[HYPOTHESIS]`

## 9 · The side channel on the host line

**Rule R-S1**. The wallet signs from the island store with the host switch open. No path from the signing core to the host exists during the step.

**Rule R-S2**. Filtering alone is not a defence. A first-order loop at `20 kHz` gives `34 dB` at `1 MHz` and `74 dB` at `100 MHz`. That is a cost to the attacker and not a cure.

**Rule R-S3**. The recharge after a step uses a fixed current and a padded or random duration.

**What stays open**. The open switch has an off-state capacitance, and a ground return exists. Gate HST-T6 measures both.
