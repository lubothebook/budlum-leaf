# BUDLUM LEAF · CORE AND SKIN · TRUST SEAT

**Revision L.7 candidate · 2026-10-19 · TRUST seat of block HP-2**. The question: if every key lives in a Core and the surface is a Skin, what is the trust model? Does a stolen Skin hold nothing? This is a study. It changes no L.6.0 or L.6.1 decision.

## 0 · The worst hole

**The lying Skin**. The Skin is the eyes and the fingers of the user, and it sits outside the trust boundary. It can paint a false summary and report a tap on "sign". No cryptography tells a real tap from a forged one. The attack turns a stolen or rogue Skin from a window into a thief. `[HYPOTHESIS]`

The model closes it only by taking authority away from the Skin.

1. A tap never confirms a key operation.
2. A tap confirms a value only up to a small blind budget per day. A flood of `100` forged taps against a budget of `100` signs exactly `10` requests of `10`.
3. Every other signature needs a press that does not cross the Skin. At C0 it is the button and the display of the Core. At C1 it is a separate confirmation device. At C2 it is the local floor of the Leaf.

**What this costs the Split**. The big surface leaves the signing path. The user looks at a small display and presses a small button, on the Core or on a ring. At C1 the Split needs a second trusted part that no design has specified. The one Core for many screens is a viewing idea, not a signing idea.

**The second hole, in confidentiality**. A paired Skin that is hostile reads every PRIVATE pixel it gets. A hardware implant in a genuine Skin is not detectable. Only the content classes bound it: a PIN or a seed never enters the stream.

**The third hole, in the program**. A signed tap is evidence, and a chain program can treat it as authority. The Core refuses an input batch that names a value. The program semantics sit outside `U7`. Open issue O6.

## 1 · What is here

| File | Content |
|---|---|
| `01-THREAT-MODEL.md` | the assets, the parties, `24` threats in a STRIDE-lite table with attack, asset, countermeasure and gate |
| `02-DESIGN-RULES.md` | `44` rules: the Skin keeps, pairing, the SkinRecord, the link, revocation, roam, what you see is what you sign, content classes, the validator Core, the long link, the mixed fleet |
| `03-GATE-MAP.md` | every rule mapped to an existing gate or to one of `18` new gates `HC-T1` to `HC-T18` |
| `skinauth.py` | the model: pairing, link keying, AEAD, revocation, the chain registry, the confirmation rule, distance classes, the account |
| `tests/test_skinauth.py` | `81` tests |

The model imports `hw/hostpower/trust/hostauth.py` read only, for ed25519 and the NVM. It edits nothing outside this directory.

## 2 · How to run

1. Run `python3 skinauth.py` in this directory. It prints the frame size, the cipher budget and the stolen-Skin readout.
2. Run `python3 -m unittest discover -s tests`. All `81` tests pass in about `4 s`.
3. Run `python3 tools/check_prose.py` on each `.md` file from the repository root. The four files pass.

The tests need only the Python standard library. X25519, HKDF and ChaCha20-Poly1305 are references, checked against the RFC vectors. They are a model and not a product part.

## 3 · The key results

| Result | Value | Where |
|---|---|---|
| tests that run and pass | `81` of `81` | `tests/test_skinauth.py` |
| the SkinRecord frame | `276` bytes | `parse_frame` |
| a stolen hardened Skin gives | the pinned Core public keys, the vendor certificate and the frame store until power loss | `test_a_stolen_skin_holds_no_wallet_key_and_no_session_key` |
| an unhardened chip adds | the identity key, so a clone | `test_the_honest_leak_an_unhardened_chip_gives_the_identity_key` |
| the cipher in a Skin decoder at `12.3 Gbit/s` | `31.3 KiB` buffer, `20.8 µs` added, `12.3 mW` at `1 pJ/bit`, `61.5 mW` at `5 pJ/bit` | `aead_budget` |
| the same as a share of the `0.80 W` surface load | `1.5 %` and `7.7 %` | arithmetic |
| the cipher at C2, `0.15 Gbit/s` | `0.15 mW` at `1 pJ/bit` | `aead_budget` |
| a forged-tap flood of `100` against a budget of `100` | `10` signed | `test_a_flood_of_forged_taps_loses_at_most_the_blind_budget` |
| the margin of SW-24 hides | `100 km` of fibre one way | `fibre_slack_km` |
| a cut in an NVM commit | old or new value, never junk | the NVM of `hostauth.py` |

### 3.1 · The six cases that the order named

| Case | The test | The result |
|---|---|---|
| a cloned Skin | `test_two_live_sessions_under_one_identity_raise_a_clone_alert`, `test_a_clone_against_a_locked_core_sees_only_the_lock_screen` | alert, both dropped, a lock screen only |
| a replayed pairing | `test_a_replayed_pairing_frame_is_refused`, `test_a_replayed_counter_with_a_fresh_nonce_is_refused_even_after_a_power_cut` | refused, also across a power cut |
| a revoked Skin | `test_a_revoked_skin_is_cut_off_and_refused`, `test_the_chain_refuses_a_replayed_pairing_or_revocation` | session dead, reconnect refused, chain replay refused |
| a forged tap | `test_a_forged_tap_cannot_confirm_a_key_operation`, `test_a_lying_skin_summary_is_ignored_and_the_press_binds_to_the_core_summary` | refused, or bounded by the budget |
| a rogue Core | `test_a_rogue_core_cannot_drive_a_skin_it_is_not_paired_to`, `test_a_paired_rogue_core_shows_a_different_strip_and_has_no_camera` | no session, or a visible strip and no lane |
| a Skin moved to a new Core | `test_a_skin_moved_to_a_new_core`, `test_a_session_does_not_roam_with_the_skin` | a new pairing, a guest role, no session carried |

### 3.2 · The residuals that the tests record

1. `test_the_residual_a_user_who_ignores_the_sas_pairs_the_attacker`: a user who skips the strings pairs the attacker.
2. `test_the_residual_a_clone_of_an_unlocked_core_session_is_not_detectable_alone`: a clone looks like the Skin while the real one is off.
3. `test_the_residual_the_rogue_skin_reads_every_private_pixel_it_is_given`: the PRIVATE class is visible by design.

## 4 · The distance classes

BRIEF Section 8 sets C0 up to `2 m`, C1 up to `30 m` and C2 up to kilometres. The trust model changes with the class. `trust_model()` holds the table.

| Class | Wallet | The far end | The confirmation | The cipher |
|---|---|---|---|---|
| C0 | the Core `U7` | a zero-key Skin | the button and display of the Core | AEAD Core to Skin |
| C1 | the Core `U7` | a zero-key Skin | a confirmation device | AEAD Core to Skin |
| C2 | the Leaf `U7`, as L.6.0 | a validator with no authority | the local floor of the Leaf | AEAD validator to `U6` |

**The mixed fleet**. One account holds a root key in the Core and a capped key in the Leaf. A Skin at C0 holds no key and spends nothing. A stolen Leaf holds a key, so it is not glass. It drains its cap per day until the root revokes it. A stolen Core loses everything, because the Split moves the key from many surfaces into one Core.

**The long-link threats**. A rogue base station reads no pixel and forges no slice if the cipher is end to end. The RTT proof of SW-24 bounds a distance from above, and a relay only adds delay. The room class rests on UWB, and a published attack reduced a `12 m` distance to `0 m` with up to `4 %` success. `[PUBLICATION]` Ghost Peak, USENIX Security 2022. A downgrade changes the signed transcript and fails. Jamming ends in a blank Skin and a locked Core.

## 5 · Open issues

| ID | The issue |
|---|---|
| O1 | a hardened identity chip is a secure element on every Skin. That is a cost against the cheaper Skin. The study seat prices it |
| O2 | the L.6.0 files hold no unlock factor: no PIN, passcode or biometric. The Split needs one on the Core path |
| O3 | the confirmation device at C1 is not specified. It is a part of hardware-wallet class, and a Leaf can fill the role |
| O4 | the chain has no registry for pairings and no cap per key. `U7` cannot read the registry, because it has no state proofs, U7-4 |
| O5 | L.6.0 says the Leaf runs no session cipher. Pixel confidentiality at C2 needs an end-to-end cipher from the validator to `U6` |
| O6 | the program semantics of a signed input batch. A rule is needed that no program reads a tap as value authority |
| O7 | owner lock against resale. A lock makes a stolen Skin glass. It also kills the second-hand market. Ayaz decides |
| O8 | the SAS needs a trusted strip with digits, drawn by the Skin. That is fixed-function and needs a Z-test |
| O9 | a Core that is a validator runs on-chain programs, which are third-party code. That clashes with the Zero-CPU rule. Seats `study` and `session` read it |
| O10 | the clone alert is a lever for a denial of service. The idle time of `5 s` is a guess |
| O11 | the list of listed decoder firmware digests needs a release registry on the chain |
| O12 | the cipher numbers are a sweep of `pJ/bit`. No part is measured |
| O13 | the new tags join U7-3: the Skin pair, the Skin session, the pair ack, the confirm device and the account key |

## 6 · The proposed gates

`03-GATE-MAP.md` holds the full pass conditions. The owner of each gate is the security line.

| Gate | The pass condition in one line |
|---|---|
| HC-T1 | a lab recovers no identity, wallet or session key from `30` stolen Skins |
| HC-T2 | `100 000` bad pairing frames pair nothing above S1, and a relay is always caught |
| HC-T3 | `10^8` bad slices are accepted `0` times, a downgrade fails, the decoder adds `50 µs` or less |
| HC-T4 | a revoked session ends in `100 ms` and no clone reconnects |
| HC-T5 | `10^6` forged taps sign `0` key operations and a value only up to the budget |
| HC-T6 | the Core summary equals the transaction, a press cannot be minted, a part change locks |
| HC-T7 | `10^6` frames carry a seeded SECRET `0` times |
| HC-T8 | an unpinned Core opens `0` sessions, a guest opens no lane, the strip cannot be painted |
| HC-T9 | a concurrent clone is always caught, and a fifth pairing is refused |
| HC-T10 | `10^6` glitches on the identity chip give `0` faulty signatures |
| HC-T11 | `1 000` roams carry no capability and keep the camera off for a guest |
| HC-T12 | `10^4` swapped addresses always show the true address on the Core display |
| HC-T13 | a red team on the validator compute cannot mint a press |
| HC-T14 | at every distance class the confirmation path holds, and a relay unlocks nothing |
| HC-T15 | the long link leaks no pixel and forges no slice, and a jammed Skin blanks in `100 ms` |
| HC-T16 | a stolen Leaf key drains its cap and no more, and the root revokes it |
| HC-T17 | `1 000` pairings give unlinkable commitments |
| HC-T18 | a thief cannot re-pair a stolen Skin, and the owner can still sell it |

## 7 · The answer

**Is "a stolen Skin is worth a piece of glass" true, partly true or false?** Partly true.

It is true for the money. A stolen hardened Skin holds no wallet key and no session key at rest. It drains nothing, and the account stays whole. The tests show it.

It is false in four ways.

1. A chip that is not hardened gives up its identity key, and the key makes a clone.
2. The Skin names the Cores of its owner, and a clone can read the pixels of any unlocked Core.
3. The Skin resells. Today a press on the Skin unpins everything. A thief can sell it or reuse it. A lock for glass is an open decision, O7.
4. A modified Skin holds the eyes and the fingers of the user. That is worth more than glass, and it is the worst hole.
