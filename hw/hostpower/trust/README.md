# BUDLUM LEAF · HOST POWER · TRUST TEAM

**Revision L.6.1 (proposed) · 2026-10-19 · TRUST team**. The question: a host that feeds the Budlum Leaf must never gain authority over it. We design that and test it.

## 0 · The holes first

The idea that power can be borrowed safely holds. It holds only with five conditions, and one sentence of the brief is false as written.

1. **Condition 3 of BRIEF Section 5 is false as written**. It says the host never touches the secure rail, the wallet or the data lanes before its handshake passes. In the Bare tier the host powers the handshake itself. It touches the bridge rail and the sideband parser first. The true sentence is in Section 3 below.
2. **A replay guard in RAM is void**. The host controls every power cycle, so it resets any RAM counter. `fw/u7` keeps session state in RAM, open issue U7-8. The test `test_the_hole_ram_counters_reopen_replay_after_a_power_cut` shows a replay accepted.
3. **Fault injection is in scope now**. The `fw/u7` README leaves it to the silicon certification. A host reaches the supply of `U7` from a cable. Signing must run isolated from the host, which needs an island store of `0.13` to `2.6 mF`.
4. **The staleness check trusts the checked party**. `session.rs` compares the head that the validator claims with the anchor. The light client has no time bound. A host that is the only path can starve the anchor.
5. **The dead-pad law cannot hold at a coil**. A field induces voltage whatever the Leaf does. The law must say that no rail is connected.

**The damage to the thesis**. The Host Life Law holds for a paired host or a vouched source. An unknown host gives `0.5 W` and the safe screen. A wall charger is not a host until the owner pairs it, or an adapter vouches for it at P2 or less. The Bare tier cannot be bare at the island: it needs its own store, or it never signs while attached. The handshake of ENR-19 takes `3 ms` only with a powered `U7`. On the sideband alone, one handshake takes about `111 ms` of charging. `[HYPOTHESIS]`

## 1 · What is here

| File | Content |
|---|---|
| `01-THREAT-MODEL.md` | the assets, the attacker, `17` threats in a STRIDE-lite table with attack, asset, countermeasure and gate |
| `02-DESIGN-RULES.md` | `38` rules: island rail, dead-pad extension, HostRecord, policy table, validator host, atomic commit, side channel |
| `03-GATE-MAP.md` | every rule mapped to an existing gate or to one of `13` new gates `HST-T1` to `HST-T13` |
| `hostauth.py` | the model: ed25519, the parser, the trust store, the policy, NVM, signing, update, the island rail, the sizing |
| `tests/test_hostauth.py` | `60` tests |

The model imports `fw/boot/bootsm.py` read only, for the update write time. It edits nothing outside this directory.

## 2 · How to run

1. Run `python3 hostauth.py` in this directory. It prints the classes, the policy rows and the island numbers.
2. Run `python3 -m unittest discover -s tests`. All `60` tests pass in about `1 s`.
3. Run `python3 tools/check_prose.py` on each `.md` file from the repository root. The four files pass.

The tests need only the Python standard library. The ed25519 code is the RFC 8032 reference, checked against two RFC vectors. It is a model, not a product part.

## 3 · The key results

**The restated condition 3**. The host never touches the wallet, the signing core, the firmware slots or the data lanes. It reaches the island only through the bridge rail, and it reaches `U7` only through one fixed `169` byte frame. `[HYPOTHESIS]`

| Result | Value | Where |
|---|---|---|
| tests that run and pass | `60` of `60` | `tests/test_hostauth.py` |
| the policy table | `6` rows, all reached by a test | `02-DESIGN-RULES.md` Section 5 |
| classes | P0 `0 W`, P1 `5 V` `0.5 W`, P2 `9 V` `15 W`, P3 `15 V` `27 W` | `hostauth.py` |
| every class row inside the leaf rating | `0.05`, `0.93`, `1.00 A` against `1.5 A` | `test_every_class_row_inside_the_leaf_rating` |
| the frame | `169` bytes, one parser, no loop | `parse_frame` |
| the island rail rides a host drop | `4.5 ms` to the brownout trip, and `2.45 ms` of warning after it | `simulate_rail` |
| the island store, one iteration | `0.13`, `0.64`, `2.58 mF` for `1`, `5`, `20 mJ` per signature | `store_sizing` |
| the signing loop count leaks | `3.18` bits per signature if the recharge is unpadded | `loop_count_entropy_bits` |
| a full update writes for | `9.04 s`, so only the final flip is atomic | `fw/boot` budgets |
| an update cut at any of its `16` ticks | never a brick, and it resumes | `test_update_cut_at_every_tick_never_bricks_and_resumes` |

### 3.1 · The seven cases that the order named

| Case | The test | The result |
|---|---|---|
| counterfeit host | `test_counterfeit_host_with_an_unknown_key`, `test_counterfeit_host_forges_a_trusted_key`, `test_tampered_record_fails_the_signature` | P1, no class gained |
| replayed record | `test_replayed_frame_and_single_use_nonce`, `test_replayed_counter_with_a_fresh_nonce`, `test_replay_after_a_power_cut_is_refused_with_nvm_counters` | refused, also across a power cut |
| expired record | `test_expired_record`, `test_a_stale_anchor_expires_every_record` | refused |
| over-class request | `test_over_class_request` | refused to P1 |
| glitch during signing | `test_a_glitch_during_signing_releases_nothing`, `test_a_glitch_campaign_ends_in_a_lockout_not_a_leak` | nothing released, lockout after `3` faults |
| mid-update power loss | `test_update_cut_at_every_tick_never_bricks_and_resumes`, `test_a_hostile_host_cutting_every_trial_only_defers` | old or new state, resume, no lower floor |
| validator host with a bad stream key | `test_validator_host_with_a_bad_stream_key` | the host keeps its class and the safe screen shows |

### 3.2 · The residual that the model shows

A double glitch that skips the self-verify releases a faulty signature. The chain refuses it, and the key can still leak. The test `test_residual_a_double_glitch_releases_a_faulty_signature` records this. The silicon needs redundant checks.

## 4 · Open issues

| ID | The issue |
|---|---|
| O1 | `fw/u7` has no NVM. The host counter, the trust store, the fault count and the floor need the two-slot commit of Rule R-A6. This is U7-8 |
| O2 | `fw/u7` has no HostRecord program and no sixth tag. It already has `verify_strict`, so the work is small |
| O3 | the double glitch. Redundant self-verify and random delay belong to the silicon |
| O4 | the island store depends on the signing energy of `U7`, which is unmeasured, U7-7 |
| O5 | the handshake on the sideband alone. At `1.8 mW`, one handshake of `200 µJ` takes `111 ms`. ENR-19 assumes `3 ms` |
| O6 | who enrols a host. The model has owner pairing and adapter vouches. A certificate authority for certified hosts is not decided |
| O7 | no clock when unpowered. The anchor age bound of `6 h` is a stand-in, and pairing never expires |
| O8 | the Qi authentication needs P-256 and X.509 in the quadrant node. The vouch format needs the energy team |
| O9 | the class windows and powers are placeholders for the power-path and thermal teams |
| O10 | the open switch has an off-state capacitance. The recharge pattern leaks the loop count. Gate HST-T6 measures both |
| O11 | no chain-level revocation of a compromised host key exists. Only the owner can unpair |
| O12 | the anchor age rule is a change in `fw/u7`. This team does not edit that crate. The U7 team owns it |

## 5 · The proposed gates

`03-GATE-MAP.md` holds the full pass conditions. The owner of each gate is the security line.

| Gate | The pass condition in one line |
|---|---|
| HST-T1 | pads and island stay at `0 V` against `10 000` counterfeit adapters and a `0` to `36 V` sweep |
| HST-T2 | `100 000` bad frames give zero grants above P1, and a valid record grants in `5 ms` or less |
| HST-T3 | `S_SEAT` opens in `10 µs` outside the window, and the island holds `1.80 V` within `5 %` |
| HST-T4 | `10^6` glitches during signing release zero faulty signatures |
| HST-T5 | `10 000` power cuts end in the old or new state, with no reused counter and no brick |
| HST-T6 | a Welch t-test of the line current stays under `4.5` over `10^6` signatures |
| HST-T7 | the lanes stay high impedance, and a `72 h` fuzz run reaches nothing but the frame |
| HST-T8 | a rogue Qi transmitter never pushes a face point over `36.2 °C` or the draw over P1 |
| HST-T9 | vehicle pulses and a load dump give no grant above class and no `U7` fault |
| HST-T10 | the cable separates at `6.5 N` or less, and the pads open in `0.8 ms` |
| HST-T11 | after `6 h` with the host as the only path, the stream is refused |
| HST-T12 | no frame before the grant carries a wallet address or a repeating value |
| HST-T13 | `1 000` data-only pairing attempts add zero keys |

## 6 · The mapped gates that exist

ENR-19 and MON-16 hold the pads at `0 V`. SW-22 holds the stream to active validators. ENR-12, ENR-16 and ENR-24 hold the wireless path and the skin limit. SW-14, FW-1 and FW-2 hold the update. MON-5, MON-17 and RL-17 hold the seat and the cable. `[DECISION]` The map is in `03-GATE-MAP.md`.
