# U6 · THE SLICE DECODER CHECK · SLICE AUTHENTICATION, RTL AND FRAME STORE

**Team U6 Silicon · Revision L.6.0 · 2026-10-12**. Sources: `FINAL/21` sections 21.5.1, 21.5.4, 21.5.5 and 21.5.8. Gates: SW-22, DST-12, SW-21, SW-23, SW-24, DST-11.

## 1 · The ruling that sets the scheme

1. The Leaf is a wallet. It runs no session cipher. `[DECISION]` FINAL/21.5.4.
2. A frame counts only when it comes from an active Budlum validator. `[DECISION]` FINAL/21.5.8.
3. So U6 proves three things per slice: the sender, the integrity and the freshness. It does not hide the payload.

Confidentiality on the air comes from the radio link layer, not from U6. `[GENERAL]`

## 2 · What is here

| Path | What it is |
|---|---|
| `ref/keccak.py` | bit-exact Keccak-f[1600], SHA3-256, cSHAKE128 and KMAC128, with a self-test |
| `ref/leafauth.py` | the scheme: handshake, validator set, slice tag, U6 checker model, frame hash, Merkle root, receipt |
| `ref/gen_vectors.py` | builds the test vectors and asserts every protocol outcome |
| `vectors/*.json` | valid stream, forged slice, replay, handover, wrong validator, and the RTL word stream |
| `hdl/slice_auth.py` | the Amaranth RTL of the line-rate checker |
| `sim/test_slice_auth.py` | replays the vectors into the RTL with `amaranth.sim` |
| `scripts/throughput.py` | the cycle model, checked against the simulation, and the margin at the Leaf stream |
| `scripts/framestore_budget.py` | the `16 MB` frame-store budget |
| `scripts/export_verilog.py` | Verilog export and a generic gate count |
| `build/` | `slice_auth.v`, `slice_auth.il`, `sim_cycles.json`, `throughput.json`, `gate_count.txt` |
| `run_all.sh` | runs everything in order |

## 3 · How to run

1. Run `./run_all.sh` from `rtl/u6/`.
2. Each step stops with an error when a check fails.
3. The Verilog step needs `pip install amaranth-yosys`. The other steps need only `amaranth` and `cryptography`.

ML-KEM encapsulation and ML-DSA signing are randomised. So the vectors change on each run. The RTL test always reads the current file.

## 4 · The authentication scheme

### 4.1 The four layers

| Layer | Who | How often | What it proves |
|---|---|---|---|
| key agreement | `U7` | once per session and on handover | the peer is an active validator; a fresh `256`-bit slice key |
| slice tag | `U6` | every slice, at line rate | this slice came from the keyed validator, unchanged and fresh |
| Merkle root | the validator signs | once per second | the validator commits to the frames it sent |
| receipt | `U7` countersigns | once per second | the Leaf showed those frames, with the measured round trip |

### 4.2 The key agreement in `U7`

The chain facts the scheme rests on: `[TREE]`

1. A validator address is its Ed25519 public key: `Address::from(sig_key.public_key_bytes())` in `src/consensus/pos.rs`.
2. A validator also holds `pq_public_key`. The default feature `pq-ml-dsa` makes it ML-DSA-87.
3. A wallet key is ML-DSA-87 by the default feature `wallet-ml-dsa`.
4. `Validator` carries `active`, `slashed`, `jailed` and `roles`. `VALIDATOR` is `RoleId(1)`.
5. The chain hash is SHA3-256: `hash_message` in `src/crypto/primitives.rs`.

The handshake, as `ref/leafauth.py` runs it:

1. `U7` sends: X25519 share, ML-KEM-768 key, nonce, program id, set epoch, session id, slot.
2. The validator answers: Ed25519 key, ML-DSA-87 key, X25519 share, ML-KEM ciphertext, nonce.
3. The validator signs the transcript hash with both keys.
4. `U7` checks that the program id is an on-chain program entry.
5. `U7` checks: in the set, `active`, not `slashed`, not `jailed`, role `1`, and the PQ key matches.
6. `U7` checks both signatures over the transcript.
7. Key: `K = HKDF-SHA3-256(X25519 || ML-KEM secret, salt = transcript)`, `32` bytes.
8. `U7` loads the KMAC prefix state of `K` into a `U6` key slot. Nothing else loads it.

The session id is `SHA3-256("BLF-SID" || first transcript)[0:16]`. The shadow handshake binds the same session id. `[DECISION]`

The hybrid exchange keeps the slice key safe if either X25519 or ML-KEM-768 holds. `[GENERAL]`

### 4.3 The slice and its tag

The wire slice is a run of 64-bit little-endian words. `[DECISION]`

| Words | Field |
|---|---|
| `w0` | `version` (16), `flags` (16), `slice_index` (32) |
| `w1` | `seq`, a session-wide slice counter, strictly rising |
| `w2` | `frame_no` |
| `w3` | `payload_len` (32), `y0` (16), `layer` (16) |
| `w4` to `w3+m` | the payload, zero padded to `8` bytes, `m = ceil(len / 8)` |
| `w4+m`, `w5+m` | the `128`-bit tag |

Flags: bit 0 key slot, bit 1 last slice of the frame, bit 2 speculative, bit 3 intra refresh.

The two steps of the tag:

1. `d = SHA3-256(sid || header with the slot bit cleared || padded payload)`. It is keyless and public.
2. `tag = KMAC128(K, d, 128, "BLF-SLICE-v1")`.

The slot bit is cleared in `d`, so the primary and the shadow give the same `d`. A wrong slot still fails, because the slot picks the key. `[DECISION]`

### 4.4 Why hash-then-KMAC on one Keccak core

All four candidates meet `160 Mbit/s` with a large margin. So line rate does not decide. These points decide:

| Candidate | The hardware | The flaw for U6 |
|---|---|---|
| GMAC | AES core plus a `128 x 128` GF multiplier | a repeated nonce leaks the hash key and allows forgery |
| Poly1305 | `130`-bit modular multiplier plus ChaCha20 per slice | two cores, a long carry chain |
| BLAKE3 keyed | `32`-bit adders | not the chain hash, so the Merkle leaves need a second SHA3 core |
| **KMAC128 over SHA3-256 `[DECISION]`** | one Keccak-f core, XOR, AND, NOT and rotate only | none found; one extra permutation per slice |

1. One core gives both the public slice hash and the MAC.
2. The slice hash is the chain hash, so the RG-18 re-executors and the chain recompute it directly.
3. KMAC needs no nonce. Freshness comes from `seq`, which the tag covers.
4. The round has no carry and no multiplier, so one round per clock is easy timing. `[GENERAL]`
5. U7 precomputes the two KMAC prefix blocks. The tag then costs one block of `24` rounds.

Security rests on SHA3-256 collision resistance and the KMAC PRF, both at `128` bits. `[PUBLICATION]` NIST FIPS 202 and SP 800-185.

The prefix state is key-equivalent. The `U6` key slots therefore have a write port from `U7` and no read port. `[DECISION]`

### 4.5 The frame hash, the per-second root and the receipt

1. Frame hash: `F = SHA3-256("BLF-FRAME-v1" || sid || frame_no || n || d_0 .. d_n-1)`.
2. Merkle tree over the frames of one second: leaf `H(0x00 || F)`, node `H(0x01 || L || R)`.
3. An odd node moves up unchanged. It is never duplicated.
4. The validator signs `"BLF-ROOT-v1" || sid || second || first frame || count || root` with Ed25519 and ML-DSA-87.
5. `U7` rebuilds the root from the digests that `U6` reported as shown.
6. `U7` checks the root and both signatures against the session validator.
7. `U7` signs the receipt with the wallet key: sid, second, root, validator, signature hash, round trip, frame count.

A root that differs from the shown frames gets no receipt. The validator then earns nothing for that second.

### 4.6 The verdicts

| Code | Name | Cause | U6 action |
|---|---|---|---|
| 0 | OK | tag good, `seq > last_seq`, key loaded | release the slice to the decoder; `last_seq := seq` |
| 1 | BAD_TAG | payload, header or tag changed, or another key | drop the slice |
| 2 | REPLAY | a good tag with `seq <= last_seq` | drop the slice |
| 3 | NO_KEY | the slot holds no key from `U7` | drop; safe screen |
| 4 | LENGTH | the stream length disagrees with `payload_len`, or over `64 KiB` | drop |
| 5 | BAD_VERSION | `version != 1` | drop; safe screen |

The safe-screen policy, proposed by U6: `[DECISION]`

1. Any NO_KEY or BAD_VERSION shows the safe screen at once.
2. Eight dropped slices inside `240` frames show the safe screen.
3. A single dropped slice keeps the old pixels of that region until the next intra refresh.

`last_seq` is one register for both slots. A slice from the old primary after a handover is therefore a REPLAY. `[DECISION]`

## 5 · The test vectors

`python3 ref/gen_vectors.py` asserts every outcome in the reference and writes the vectors. `[TREE]` of this team.

| File | Content | Expected |
|---|---|---|
| `valid_stream.json` | `3` frames of `4` slices, `0` to `3000` bytes, the root, the receipt | all OK, receipt countersigned |
| `forged_slice.json` | a flipped payload byte, tag bit, `seq` byte and `y0` byte; another session key | BAD_TAG each |
| `replay.json` | an old slice and the last good slice sent again | REPLAY |
| `handover.json` | the same slice from the shadow on slot 1 and from the primary on slot 0 | shadow OK, primary REPLAY, equal `d` |
| `wrong_validator.json` | inactive, slashed and unknown keys; program not on chain; stolen identity; foreign root | refused; U6 NO_KEY |
| `rtl_events.json` | the word stream of all `28` slices, with the key loads | verdict, digest and `seq` per slice |

## 6 · The RTL

`hdl/slice_auth.py` is one Keccak-f[1600] core with one round per clock. `[DECISION]`

1. ABSORB takes one word per clock into lanes `0` to `16`. The sid fills lanes `0` and `1`.
2. PERM runs `24` rounds. The pad is applied with the last hashed word.
3. KMAC loads the slot's prefix state, XORs in `d`, `right_encode(128)` and the pad, then permutes.
4. TAGRX takes the two tag words and XOR-accumulates them against the computed tag.
5. REPORT compares all `128` bits with no early exit, checks `seq` and emits one verdict.

### 6.1 Simulation against the reference

`python3 sim/test_slice_auth.py`: **`28 / 28` slices match** in verdict, `d` and `seq`. `[TREE]` of this team.

The cycle model of `scripts/throughput.py` equals the simulated count on all `25` slices with a full length. `[TREE]`

`cycles = words + 24 x (blocks + 1) + 2`, with `blocks = floor(lanes / 17) + 1`. Add `1` when `lanes` is a multiple of `17`.

### 6.2 Throughput and margin

| Case | Slice size | Cycles | Core busy | Margin |
|---|---|---|---|---|
| `200 MHz`, `32` slices per frame, `160 Mbit/s` | `2 604 B` | `838` | `3.26 %` | **`31 x`** |
| `200 MHz`, `32` slices per frame, `60 Mbit/s` | `977 B` | `347` | `1.37 %` | `73 x` |
| `200 MHz`, `64` slices per frame, `160 Mbit/s` | `1 302 B` | `435` | `3.42 %` | `29 x` |
| `100 MHz`, `32` slices per frame, `160 Mbit/s` | `2 604 B` | `838` | `6.51 %` | `15 x` |

The busy figure includes the frame-hash pass on the same core. `[TREE]` of this team, from the simulated cycle model.

1. The core peak is `26.5` bits per clock: `5.31 Gbit/s` at `200 MHz`. It keeps pace with a Wi-Fi 7 burst.
2. The raw stream is `29.5 Gbit/s`. The `60-160 Mbit/s` stream is a `184:1` to `492:1` compression.
3. The verdict comes `52` clocks after the last payload word: `0.26 µs` at `200 MHz`.
4. The first-slice decode budget is `1.5 ms` (FINAL/21.5.7). The check uses under `0.02 %` of it.
5. The header and tag add `52` bytes per slice: `2 %` of the wire at `2 604 B` slices.

The `200 MHz` clock is `[HYPOTHESIS]` until synthesis on the target node.

### 6.3 Verilog and size

`build/slice_auth.v` is the Verilog of module `u6_slice_auth`, `8 431` lines.

The generic gate map gives `6 052` flip-flops and about `64 kGE`, before logic minimisation. `[HYPOTHESIS]` until a real synthesis.

The two prefix states take `3 200` of the flops. An SRAM with a `25`-clock load per slice cuts this. The margin pays for it.

## 7 · The slice decoder interface

### 7.1 The path

1. The packet engine of `U2A` or `U5` reassembles a slice and writes it to a free ingress buffer.
2. It streams the same words into the checker.
3. On OK the ingress buffer is released to the decoder. On any other verdict it is freed unread.
4. The decoder writes the decoded rows into frame B at `y0`.
5. On the last slice of a frame, U6 flips frame B to U1.
6. The digest FIFO carries `d`, `seq`, `frame_no` and flags of every OK slice to `U7`.

Verify-before-decode means no unauthenticated byte reaches the decoder parser. `[DECISION]` The cost is the slice air time, which the `1.0 ms` downlink row already holds.

### 7.2 The ports

| Port | Direction | Width | Meaning |
|---|---|---|---|
| `cfg_we`, `cfg_addr`, `cfg_data` | `U7` to `U6` | `1`, `6`, `64` | prefix lanes, sid, slot valid, session reset; write only |
| `in_data`, `in_valid`, `in_last`, `in_ready` | packet engine to `U6` | `64`, `1`, `1`, `1` | slice words, ready-valid |
| `res_valid`, `res_err` | `U6` to the buffer manager | `1`, `3` | one verdict per slice |
| `res_digest`, `res_seq`, `res_frame`, `res_flags`, `res_slice` | `U6` to the FIFO and the decoder | `256`, `64`, `64`, `16`, `32` | the slice record |
| decoder write | `U6` to the frame store | `y0`, rows, tiles | decoded rows into frame B |
| `flip`, `frame_no` | `U6` to `U1` | `1`, `64` | frame B is complete; scan it out |
| `safe_screen` | `U6` to `U1` and `U7` | `1` | the policy of section 4.6 fired |

### 7.3 The handover, gate DST-12

1. `U7` runs the handshake with the shadow and loads slot `1`.
2. The shadow sends from the next `seq` with the slot bit set.
3. Its slices have the same `d`, because rendering is deterministic. No key frame is needed.
4. Any late primary copy is a REPLAY. `U7` then clears slot `0`.

The vector `handover.json` shows this with zero lost slices.

## 8 · The `16 MB` frame store

`python3 scripts/framestore_budget.py`. `[TREE]` of this team.

One frame at `24 bpp` is `15.36 MB`. Two frames are `29.3 MiB`. So the store keeps frames at a fixed `10 bpp`.

| Item | Bytes | MiB |
|---|---|---|
| frame A, shown and the reference | `6 400 000` | `6.104` |
| frame B, being decoded | `6 400 000` | `6.104` |
| scroll overscan band, `10 %` | `640 000` | `0.610` |
| speculative layers, `2 x 1600 x 400` | `1 600 000` | `1.526` |
| glyph atlas, A8 `1024 x 256` | `262 144` | `0.250` |
| cursor, `64 x 64` RGBA | `16 384` | `0.016` |
| warp meshes, `128` tiles `x 17 x 17 x 8 B` | `295 936` | `0.282` |
| slice ingress buffers, `2 x 64 KiB` | `131 072` | `0.125` |
| digest FIFO to `U7`, `512 x 48 B` | `24 576` | `0.023` |
| **total** | **`15 770 112`** | **`15.040`** |
| **margin in `16 MiB`** | **`1 007 104`** | **`0.960` (`6.0 %`)** |

1. The fixed-rate store compression is in the encoder's reference loop too. So the decoder reference never drifts. `[DECISION]`
2. `10 bpp` fixed rate is visually lossless for most content. `[PUBLICATION]` VESA DSC 1.2a. Confirmed only by gate DSP-19 viewing tests.
3. The largest rate that fits is `10.79 bpp`.
4. The store bandwidth at `240 Hz` is about `5.0 GB/s`. `[HYPOTHESIS]` A `x16` LPDDR5X channel carries it.

## 9 · The gates

| Gate | The U6 result |
|---|---|
| SW-22 | a key not in the active set gets no key slot; its slices give NO_KEY and the safe screen |
| DST-12 | the shadow slot and the shared `seq` give a handover with zero lost slices |
| SW-24 | the receipt carries the measured round trip, signed by `U7` |
| DST-11 | the check adds `0.26 µs` per slice to the `1.5 ms` decode row |
| SW-21, SW-23 | the overscan, speculative layers, glyph atlas and warp meshes fit the store |

## 10 · The open issues

1. The frame-hash pass on the core is specified and counted in the margin. Its RTL is the next step.
2. The packet engine, the buffer manager and the decoder are interfaces here, not RTL.
3. Clock, area and power are `[HYPOTHESIS]` until synthesis on the target node.
4. The Keccak core has no masking against power analysis yet. The prefix registers hold key-equivalent data.
5. The validator set in `U7` is a snapshot here. Production needs membership proofs against a finalised state root. Owner: U7.
6. `U7` signs input batches at `480 Hz` (FINAL/21.5.5). ML-DSA-87 at that rate is heavy for a secure element. Owner: U7.
7. The `10 bpp` store compression needs the codec team to build it into the validator encoder.
