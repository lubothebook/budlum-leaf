# U7 · The secure-element applet of the wallet

**Team U7 · Revision L.6.0 · 2026-10-12**. This directory holds the applet logic of `U7`, the secure element of the Leaf. It implements FINAL/21 section 21.5.4, 21.5.5 and 21.5.8. `[DECISION]`

## 1 · What is here

| Path | The content |
|---|---|
| `Cargo.toml` | a standalone crate, `budlum-leaf-u7`, with an empty `[workspace]` table |
| `src/lib.rs` | the crate root, `#![no_std]` with `alloc`, and the error enum `U7Error` |
| `src/chain.rs` | mirrors of the Budlum types: header, snapshot, certificate, set hashes, wallet address |
| `src/bls.rs` | the BLS12-381 finality check and the PoP check, mirrored from the tree |
| `src/light_client.rs` | the validator-set light client: bootstrap, advance, and the U7 set rotation |
| `src/wallet.rs` | the ML-DSA-87 wallet key, the TRNG trait and the monotonic clock trait |
| `src/session.rs` | admission, distance classes, the lease, input batches, frame roots and receipts |
| `tests/u7.rs` | `23` tests, with a test for each gate check |
| `scripts/vectors.py` | an independent Python reading of the tree hashes, for golden vectors |

## 2 · How to run it

1. Run `cargo test` in `fw/u7`. All `23` tests pass in about `1 s` after the first build.
2. Run `python3 scripts/vectors.py`. It prints the golden values that `golden_vectors_match_python` pins.
3. Run `cargo build --target thumbv7em-none-eabihf`. It proves the bare-metal `no_std` build.
4. Run `cargo clippy --all-targets`. It reports no warning.

## 3 · The match to the Budlum tree

Every mirror cites the tree file and line in its doc comment. `[TREE]`

| The U7 item | The tree source | The match |
|---|---|---|
| validator identity | `src/crypto/signer.rs:6-8`, `src/core/block.rs:151-162` | the address is the Ed25519 key; `verify_strict` as in `primitives.rs:726-760` |
| validator role | `src/registry/role.rs` `roles::VALIDATOR` | the lease writes `RoleId(1)` |
| header hash | `src/core/block.rs:84-149`, `src/core/hash.rs:13-36` | `BDLM_BLOCK_V4`, length-prefixed SHA-256, recomputed, never read |
| snapshot hash | `src/chain/finality.rs:52-73` | SHA3-256, sorted, length-prefixed BLS, PoP and PQ keys |
| header set hash | `src/core/account.rs:990-1025` | `BDLM_CONSENSUS_VALIDATOR_SET_V1`, with the VRF key |
| quorum | `src/chain/finality.rs:119-134` | exact `u128` stake over `2/3`, and `ceil(2n/3)` signers |
| finality certificate | `src/chain/finality.rs:789-935` | canonical bitmap, subgroup checks, aggregate pairing, RFC 9380 DST |
| PoP | `src/chain/finality.rs:270-286`, `402-445` | `BDLM_BLS_POP_V1`, chain id and address bound |
| light client | `src/light_client/mod.rs:162-470` | one anchor, strictly forward, header chain continues the anchor |
| wallet key | `src/crypto/primitives.rs:831-914` | ML-DSA-87, hedged, empty context, `SHA3-256("BUDLUM_ADDRESS_V2" ‖ pk)` |
| Merkle root | `src/consensus/merkle_tree.rs:34-165` | SHA3 pairs, odd node promoted under `BDLM_MERKLE_ODD_PROMOTE_V1` |
| slot | `src/consensus/pos.rs:42` | `6 s`; the lease length is counted in these slots |

The crates and majors are the tree's: `ed25519-dalek 3.0.0`, `bls12_381 0.8.0`, `sha2 0.11`, `sha2 0.9.9`, `sha3 0.12`, `ml-dsa 0.1.1`. `[TREE]`

The Python script reads the tree independently. Seven golden values agree with the Rust. `[TREE]`

## 4 · The API

| The call | What it does |
|---|---|
| `WalletKey::generate(rng)` | makes the key on the device from `32` TRNG bytes; no call exports it |
| `WalletKey::sign(msg, rng)` | hedged FIPS 204 `ML-DSA.Sign`, `4627` bytes, accepted by `verify_ml_dsa_87_signature` |
| `LightClient::bootstrap(params, anchor, snapshot)` | binds the set to the anchor and checks every PoP |
| `Applet::advance(header, cert, snapshot)` | verifies a checkpoint of the same set and moves the anchor |
| `Applet::rotate(segment, cert, current, next)` | moves to the next set; drops a session whose validator left |
| `Applet::select_nearest(probes)` | the lowest round trip among active keys only |
| `Applet::challenge(program)` | a single-use nonce; U7 starts its own timer |
| `Applet::admit(hello, sig, evidence)` | the gate checks, then the wallet-signed `SessionLease` |
| `Applet::sign_input_batch(first, count, samples)` | a signed batch with a strict sequence number |
| `Applet::begin_rtt_probe()` | a nonce for the next frame root; U7 starts its timer |
| `Applet::on_frame_root(root, sig, shown)` | checks the root against the shown frames, then countersigns the receipt |
| `Applet::display_gate()` | `Stream` or `SafeScreen`, read by `U6` and `U1` |

**Admission, in order**. Each failed step refuses the stream.

1. The hello answers the open challenge and session, once.
2. The chain id is the Leaf's chain.
3. The Ed25519 signature verifies under the validator address.
4. The address is in the active set of the light client.
5. The claimed head is at most `200` blocks above the U7 anchor.
6. The program entry equals the program the user opened.
7. The distance evidence gives a class, or refuses a false room claim.

**The lease** names the chain, the wallet, the validator and its role. It also names the session, the program entry, the heights, the class and the round trip. The wallet signs it. `[DECISION]`

**The receipt** names the lease hash, the frame root, the hash of the validator signature and the round trip. U7 measures the round trip from its own probe nonce. `[DECISION]`

**The distance classes**. The ceilings are the air and network rows of FINAL/21 section 21.5.7, plus `1 ms`. The test `rtt_limits_follow_the_budget_table` recomputes them. `[HYPOTHESIS]` until DST-11 measures them.

| Class | The proof | The ceiling |
|---|---|---|
| room | UWB at `10 m` or less, with the STS commitment the validator signed | `3.1 ms` |
| metro, Wi-Fi | the round trip alone, `100 km` of fibre | `5.0 ms` |
| cell, 5G | the round trip alone | `4.9 ms` |
| far | any round trip over the ceiling | none; the session runs with speculative frames |

## 5 · The threat model

| The attacker | The attack | The defence |
|---|---|---|
| a non-validator server | streams frames to the Leaf | refused at step 4; the safe screen shows (SW-22) |
| a validator that left the set | keeps streaming after an epoch change | `rotate` drops the session at once (SW-22) |
| a relay in the room | relays a far validator as near | the STS commitment differs, or the round trip exceeds the room ceiling (SW-24) |
| a hostile host chip | replays an old hello | the challenge is single use |
| a hostile host chip | feeds a forged snapshot | the snapshot must hash to the anchored set, with every PoP valid |
| a stake whale | finalizes with few keys | the count quorum refuses it |
| a forged next set | rotates U7 to attacker keys | the current set must finalize the header that commits the new set |
| a validator | lies about latency | U7 measures the round trip; no probe, no receipt |
| a validator | signs a root over frames it did not send | U7 keeps the signed root as slashing evidence and shows the safe screen |
| a server | streams another application | the program entry must match the lease |
| a thief of the host flash | reads the wallet key | the key lives in U7 only; no call returns it |

**Out of scope**. Side channels and fault injection on the U7 die belong to the silicon certification. The per-slice tag check belongs to `U6`. `[DECISION]`

## 6 · The gates

| Gate | The test that holds it | The state |
|---|---|---|
| **SW-22** | `sw22_a_key_outside_the_active_set_gets_the_safe_screen`, `sw22_forged_replayed_or_wrong_program_hellos_are_refused`, `sw22_a_validator_rotated_out_loses_the_stream`, `a_root_signed_by_another_key_gets_the_safe_screen` | logic passes; the silicon run is open |
| **SW-24** | `sw24_uwb_room_proof_and_relay_refusal`, `sw24_classes_follow_the_measured_round_trip`, `sw24_nearest_is_the_lowest_round_trip_among_active_keys` | logic passes; radio and coverage-map runs are open |
| DST-12 | `handover_keeps_the_session_and_a_failed_one_keeps_the_stream` | logic passes; a failed handover keeps the primary |

## 7 · The open issues

1. **U7-1, set rotation**. The tree's light client refuses any set change (`src/light_client/mod.rs:431-449`). U7 adds its own rule. The outgoing set must finalize a checkpoint after the new set's first header. The tree must confirm that its aggregator does this. `[HYPOTHESIS]`
2. **U7-2, the PQ path**. The ML-DSA-65 quorum blob (`src/consensus/qc.rs`) is not verified yet. Only the BLS certificate is.
3. **U7-3, the tags**. The five `BDLM_LEAF_*` tags are not in `src/crypto/domain_tags.rs`. The tree has no session, lease or receipt program yet. `[TREE]`
4. **U7-4, the program proof**. U7 checks that the program entry matches the lease. It does not yet prove the program exists against the state root.
5. **U7-5, the UWB binding**. `U2B` must export the STS key commitment of each ranging session. The validator signs it in its hello.
6. **U7-6, key checks**. U7 checks the VRF and PQ key lengths only. The curve checks stay with the validators.
7. **U7-7, the cost on the die**. ML-DSA-87 signing time and BLS pairing time on the U7 core are not measured. `[HYPOTHESIS]`
8. **U7-8, persistence**. The anchor, the key and an anti-rollback counter need NVM. The APDU framing is not written.
9. **U7-9, hex fields**. The header string roots are taken as lowercase 64-hex, as `hex::encode` writes them. An uppercase root is refused.
10. **U7-10, the toolchain**. The tree pins Rust `1.97.1`. This crate declares `1.97`, the toolchain on this host.
