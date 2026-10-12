# BUDLUM LEAF · PROTO · THE LEAF TO VALIDATOR WIRE PROTOCOL

**Revision L.6.0 · 2026-10-12 · the Wire-Protocol team**. This directory defines how a Leaf talks to the validator that runs it. The source of truth is FINAL/21 Section 21.5, FINAL/08 and FINAL/10.

## 1 · What is here

| The path | What it is |
|---|---|
| `budlum/leaf/v1/leaf.proto` | the protocol: `50` messages, `23` enums, one envelope `LeafMessage` with `31` bodies |
| `buf.yaml` | the `buf` gate, STANDARD lint, in the shape of `/home/claude/budlum/buf.yaml` |
| `TRANSPORT.md` | the mapping on multipath QUIC: carriers, urgencies, L4S, DSCP, Wi-Fi, 5G, the handover states |
| `VERSIONING.md` | the version rules, the canonical bytes, the domain tags, the error codes |
| `tools/protolite.py` | a minimal proto3 parser, a descriptor builder and a hand-rolled canonical codec |
| `tools/kmac.py` | Keccak, cSHAKE256 and KMAC256, checked against `hashlib` and the NIST sample |
| `tests/test_roundtrip.py` | the round trip of every message and the integrity checks |
| `model/bitrate.py` | the bitrate model: the downlink, the camera uplink, the control and the audio |
| `model/handover.py` | the timing of the shadow handover |
| `out/` | the generated tables: `sizes.md`, `sizes.csv`, `bitrate.md`, `handover.md` |

## 2 · How to run it

```sh
sh proto/run_all.sh
```

The script runs the KMAC self test, the round trip, the two models and the prose check. Each script also runs alone with `python3`.

**Why no protoc**. Neither `protoc` nor `buf` is installed here. `protolite.py` parses the `.proto` into a `FileDescriptorProto`. The official `google.protobuf` runtime then builds the real classes. The test compares that runtime with the hand-rolled codec byte for byte.

## 3 · The protocol in one table

| The job | The messages | The source |
|---|---|---|
| hello and admission | `Hello`, `SessionGrant`, `Admission`, `ActiveSetProof`, `UwbDistanceProof` | FINAL/21 21.5.4, FINAL/08 8.5 |
| the lease | `Lease`, `LeaseRevoke` | FINAL/08 8.5, R1 to R4 |
| the input, signed by `U7` | `InputBatch`, `TouchSample`, `KeyEcho`, `StretchState`, `ActionTx` | FINAL/21 21.5.5 step 1 |
| the frame request | `FrameRequest` | FINAL/21 21.5.5 step 2 |
| the slices | `Slice`, `SliceHeader`, `SliceFragment`, `FrameCommit` | FINAL/21 21.5.5 steps 4 and 5 |
| the speculative frames | `SpeculativeFrameSet`, `SpeculativeBranch`, `SpeculationResolve` | FINAL/21 21.5.6, SW-23 |
| the `U1` compositor | `LayerUpdate`, `Layer`, `EchoContext`, `GlyphAtlasUpdate`, `GlyphEntry` | FINAL/21 21.5.6, SW-21 |
| the proof | `MerkleRoot` once per second, `Receipt` countersigned by `U7` | FINAL/21 21.5.4 |
| the handover | `ShadowAnnounce`, `ShadowHeartbeat`, `HandoverCommand`, `HandoverAck`, `PathProbe`, `PathProbeAck` | FINAL/21 21.5.4, DST-12 |
| the camera | `CameraCaptureOpen`, `CameraRawChunk`, `CameraCaptureClose`, `CameraResult` | FINAL/10 10.3 |
| the audio | `AudioFrame` | FINAL/21 21.6 |
| the control | `ClassStatement`, `KeyUpdate`, `Error`, `Goodbye` | FINAL/10 10.4, FINAL/08 8.7 |

## 4 · The key decisions of this team

All are `[HYPOTHESIS]` until review, unless a FINAL decision is named.

1. **The format is proto3**, because Budlum uses proto3 with `prost` and `buf`. `[TREE]`
2. **The package starts lint-clean**. `budlum.network` carries three lint exemptions. `budlum.leaf.v1` needs none.
3. **One signature per second, not per batch**. `U7` tags each `InputBatch` with a `16`-byte KMAC. It chains the batches and signs the head in `Receipt`.
4. **The reason for rule 3**. An ML-DSA-44 signature per batch costs `9.5 Mbit/s` and `480` signatures per second.
5. **The wallet key signs once per session**, in `SessionGrant`. FINAL/08 Section 8.5. `[DECISION]`
6. **The slice MAC key comes from the TLS exporter**. Each validator connection has its own `U6` key slot.
7. **The encoding is canonical**, because `U6` parses `SliceHeader` in hardware and MACs cover bytes.
8. **A slice is one tile row**: `8` tiles of `200 x 200` px, `16` slices per frame.
9. **The shadow has a HOT state**. Both validators send slices, so a dead primary costs zero frames.

## 5 · The key results

**The round trip**. All `31` bodies and all `50` message types pass. The hand-rolled codec and `google.protobuf 7.36.1` give identical bytes. All `13` integrity checks pass. See `out/sizes.md`.

| The message | The bytes | The rate | The load with UDP and QUIC |
|---|---|---|---|
| `InputBatch`, two contacts | `90` | `480 Hz` | `576 kbit/s` |
| `Slice` wrapper: envelope, header, MAC | `53` | `3 840 Hz` | about `1.6 Mbit/s` |
| `FrameCommit` | `108` | `240 Hz` | `323 kbit/s` |
| `Receipt` | `2 629` | `1 Hz` | `22 kbit/s` |
| `MerkleRoot` | `3 440` | `1 Hz` | `28 kbit/s` |
| `Hello`, with the ML-DSA-87 key and the grant | `9 028` | once | none |
| `Admission`, with the ML-DSA-65 key | `5 798` | once | none |

**The downlink at `1600 x 3200`, `240 Hz`**. From `model/bitrate.py`. All bpp anchors are `[HYPOTHESIS]`.

| The content | AV1, total | HEVC, total |
|---|---|---|
| game, full motion, `240` frames per second | `76 Mbit/s` | `99 Mbit/s` |
| game, high quality | `151 Mbit/s` | `195 Mbit/s` |
| video, natural, sent at `60` frames per second | `25 Mbit/s` | `31 Mbit/s` |
| interface scroll the compositor cannot cover | `30 Mbit/s` | `38 Mbit/s` |
| a static page | `0`, only the Merkle root | `0` |

The totals hold the protocol, the UDP and QUIC headers and a `20 %` speculative share. Datagram mode adds `12.5 %` for FEC.

**The first slice**. A game slice is `1.9 kB`. Its air time is `8 µs` on room Wi-Fi and `26 µs` on a good 5G cell. That is small against the `1.0` and `1.3 ms` rows of the FINAL/21 budget. Gate DST-11.

**The camera uplink**. A `50 MP` RAW10 frame, lossless, is `35 MB`.

| The capture | Room Wi-Fi | Good 5G cell | Loaded 5G cell |
|---|---|---|---|
| one `50 MP` RAW10 frame | `0.2 s` | `2.8 s` | `9.3 s` |
| the fusion burst, `105 MB` | `0.6 s` | `8.4 s` | `28 s` |

The deadline class follows from the path and is stated before the shutter, per FINAL/10.

**The control uplink** is `0.74 Mbit/s` with the microphone. **The downlink control** is `0.87 Mbit/s` with the audio.

**The handover**. A planned switch loses no frame. HOT loses no frame. From WARM, `U1` covers `3` to `9` frames for a shadow RTT of `1` to `25 ms`. That stays inside the `40 ms` reprojection limit.

## 6 · The gates

| Gate | What this directory gives it |
|---|---|
| DST-4 | the slice MAC, the frame chain and the Merkle root detect a forged or replayed frame |
| DST-11 | the urgencies, L4S, 5QI `80` and the first-slice air time |
| DST-12 | the WARM, HOT and SWITCH states and their timing |
| SW-6 | one wallet signature per session and one session signature per second |
| SW-21 | `LayerUpdate`, `EchoContext` and `GlyphAtlasUpdate` feed the four compositor jobs |
| SW-22 | `Admission.active_set` and the codes `103` and `104` |
| SW-23 | `SpeculativeFrameSet` and `InputBatch.taken_branch` |
| SW-24 | `UwbDistanceProof`, `PathProbe` and the signed round trips in `Receipt` |
| CAM-9, CAM-21 | the RAW upload times per path and the deadline class |

## 7 · The open issues

| No. | The issue | The owner |
|---|---|---|
| 1 | The QUIC endpoint runs on the `U2A` core. The radio team must confirm the core can hold it | radio team |
| 2 | FINAL/21 says the Leaf runs no session cipher. QUIC TLS is the transport cipher. Ayaz must confirm this reading | Ayaz |
| 3 | `src/account_abstraction` in the Budlum tree has no session-key grant. `SessionGrant` needs one | chain team, RG-18 |
| 4 | No ML-DSA library is installed. Signatures are stand-ins of the exact FIPS 204 size | this team |
| 5 | 4K60 video capture needs a fixed-function encoder. RAW needs `2.8 Gbit/s`. HEVC needs about `60 Mbit/s` | camera team |
| 6 | A HOT shadow needs a bit-identical encoder build on both validators | RG-18 |
| 7 | The bpp anchors and the fps exponent need an encoder bench at `1600 x 3200` | RG-18, DST-11 |
| 8 | The `BDLM_LEAF_*` tags must join `src/crypto/domain_tags.rs` | chain team |
| 9 | `buf lint` has not run, because `buf` is not installed | this team |
| 10 | On a loaded 5G cell, game HEVC in datagram mode loads the cell to `75 %`. The class ladder must step down visibly | this team, DST-6 |
