# BUDLUM LEAF · PROTO · THE TRANSPORT MAPPING ON MULTIPATH QUIC

**Revision L.6.0 · 2026-10-12 · the Wire-Protocol team**. This file maps every message of `budlum/leaf/v1/leaf.proto` onto QUIC. The numbers come from `model/bitrate.py` and `model/handover.py`. Gates: DST-11, DST-12, SW-22, SW-23, SW-24.

## 1 · The connections

| The connection | The peers | The paths | What it carries |
|---|---|---|---|
| `C1` primary | the Leaf and the serving validator | Wi-Fi on `U2A`, 5G on `U5`, `60 GHz` on `U2B` | every message of the session |
| `C2` shadow | the Leaf and the hot shadow validator | the same radios | `ShadowHeartbeat` when WARM, slices too when HOT |
| `Cp` probe | the Leaf and each of `3` to `5` candidates | the primary path | `PathProbe` and `PathProbeAck` as DATAGRAM, once per second |

1. `C1` is one QUIC connection with several paths, per draft-ietf-quic-multipath. `[PUBLICATION]`
2. The shadow is a different validator, so it needs its own connection `C2`. `[GENERAL]`
3. `Cp` resumes with a stored ticket, so a probe costs no handshake. `[HYPOTHESIS]`

**The handshake**. TLS 1.3 with the hybrid group `X25519MLKEM768`. The validator authenticates with a raw public key bound to its ML-DSA-65 consensus key. The Leaf authenticates inside `Hello` with its wallet grant. `[HYPOTHESIS]`

**The channel binding**. `Admission.transcript_hash` covers `Hello`, `Admission` and a TLS exporter value. A relay cannot splice two handshakes. `[HYPOTHESIS]`

**The keys of `U6` and `U7`**. Two TLS exporter labels give the line-rate keys. No key travels on the wire.

| The exporter label | The key | The holder on the Leaf | What it tags |
|---|---|---|---|
| `EXPORTER-BDLM_LEAF_SLICE_MAC_V1` | `K_slot`, one per connection | `U6` key slot `1` (primary) or `2` (shadow) | `Slice`, `FrameCommit`, `LayerUpdate`, `GlyphAtlasUpdate`, `SpeculativeFrameSet` |
| `EXPORTER-BDLM_LEAF_INPUT_MAC_V1` | `K_in` | `U7` | `InputBatch`, `HandoverCommand`, `CameraCaptureOpen` |

**Where the QUIC endpoint runs**. FINAL/21 allows firmware on the small core of each radio. The QUIC state machine runs on the `U2A` core. `U5` and `U2B` hand their packets to it over the ring bus. `[HYPOTHESIS]` See open issue 1 of the README.

## 2 · The carriers and the priorities

The urgency is the RFC 9218 urgency, `0` the highest. `[PUBLICATION]` The validator sender and the Leaf sender both obey it.

| The message | The direction | The carrier | Urgency | Reliable | The deadline |
|---|---|---|---|---|---|
| `InputBatch` | up | DATAGRAM, also copied on a second path | `0` | no, the next batch supersedes | `2.08 ms` |
| `HandoverCommand`, `HandoverAck` | both | control stream, also copied on a second path | `0` | yes | the switch frame |
| `Slice`, committed timeline | down | one uni stream per slice (stream mode) | `0` | yes, until the deadline | the present time |
| `SliceFragment` | down | DATAGRAM with XOR parity (datagram mode) | `0` | FEC only | the present time |
| `FrameCommit` | down | the stream of the last slice of the frame | `0` | yes | the present time |
| `KeyUpdate` | down | control stream | `0` | yes | before `from_frame` |
| `AudioFrame` | both | DATAGRAM | `1` | no, Opus conceals a loss | `10 ms` |
| `LayerUpdate`, `SpeculationResolve` | down | control stream | `1` | yes | `apply_at_frame` |
| `SpeculativeFrameSet` and its slices | down | uni streams | `2` | yes, until `valid_until_frame` | `valid_until_frame` |
| `ActionTx` | up | control stream | `2` | yes | the slot of `6 s` |
| `Hello`, `Admission`, `Lease`, `LeaseRevoke`, `ClassStatement`, `Error`, `Goodbye` | both | control stream | `3` | yes | none |
| `GlyphAtlasUpdate` | down | uni stream | `3` | yes | before its first echo |
| `ShadowHeartbeat` | down on `C2` | DATAGRAM | `3` | no | none |
| `PathProbe`, `PathProbeAck` | both on `Cp` | DATAGRAM | `3` | no | `1 s` |
| `FrameRequest` | up | control stream | `0` | yes | none |
| `MerkleRoot`, `Receipt` | both | control stream | `4` | yes | the slot window |
| `ShadowAnnounce` | down | control stream | `4` | yes | none |
| `CameraResult` | down | control stream | `5` | yes | the deadline class |
| `CameraCaptureOpen`, `CameraRawChunk`, `CameraCaptureClose` | up | one uni stream per capture, incremental | `7` | yes | the deadline class |

**The framing**. A stream holds varint-length-prefixed `LeafMessage`s. A DATAGRAM holds one `LeafMessage`. The first message of each stream or datagram flow sets `wire_version`.

**The mode rule for slices**. A retransmission helps only when it arrives in time. `[HYPOTHESIS]`

1. Use stream mode when the path RTT is under one frame period, `4.17 ms`.
2. Use datagram mode with FEC when the RTT is longer. That is 5G and the far class.
3. The validator resets a slice stream when the slice misses its present time.
4. The Leaf sends `STOP_SENDING` for a frame that `U1` has already replaced.

## 3 · The multipath scheduler

1. The primary path is the trusted path with the lowest RTT, per FINAL/08 Section 8.3.
2. Slices ride the primary path only.
3. `InputBatch` and `HandoverCommand` go on two paths at once. The copy costs about `0.6 Mbit/s`.
4. A slice lost to a probe timeout goes again on the second path.
5. A path that fails the operator trust test is never opened, per R6.
6. An idle path stays in standby. It keeps one keep-alive per second.

## 4 · L4S, DSCP, Wi-Fi and 5G

**L4S**. Every flow of urgency `0` to `4` is marked ECT(1), per RFC 9331. The validator runs a scalable congestion control, Prague class. `[PUBLICATION]` RFC 9330 to RFC 9332. The Leaf returns the ECN counts in `ACK_ECN` and the CE rate in `Receipt.paths`.

**The rate loop**. The validator sets the encoder target each frame. The target is the congestion rate times the frame period, minus the speculative share. `FrameCommit.rc_target_bits` carries it, so a shadow encoder stays bit-identical.

**The camera upload** is a background flow. It uses a less-than-best-effort control and the classic queue, so it never fills the L4S queue. `[HYPOTHESIS]`

| The flow | DSCP | The Wi-Fi access class | The 5G QoS flow |
|---|---|---|---|
| input, handover | `46` EF | AC_VO, restricted TWT | 5QI `80`, configured grant |
| slices, commits, speculative | `45` NQB, draft-ietf-tsvwg-nqb | AC_VI, restricted TWT | 5QI `80` |
| audio | `46` EF | AC_VO | 5QI `80` |
| control, proofs, probes | `0` | AC_BE | 5QI `80` |
| camera upload | `1` LE, RFC 8622 | AC_BK | 5QI `9`, the default flow |

`[PUBLICATION]` 5QI `80` is the non-GBR low-latency eMBB flow of 3GPP TS 23.501, Table 5.7.4-1, with a `10 ms` packet delay budget. Release 18 adds L4S marking in the RAN, TS 23.501 Section 5.37.3.

## 5 · The handover, WARM and HOT

The shadow re-executes every frame, so it holds the same state and the same chain hash. `[DECISION]` FINAL/21 Section 21.5.4.

| The state | What the shadow sends | The entry condition | The cost |
|---|---|---|---|
| WARM | `ShadowHeartbeat`, once per frame | always, once `ShadowAnnounce` arrives | `0.26 Mbit/s` |
| HOT | the heartbeat and every slice, under key slot `2` | the primary RTT or loss trend crosses the warning line | one more slice stream, `76.3 Mbit/s` for game AV1 |
| SWITCH | the shadow becomes the primary | `HandoverCommand`, or the primary falls silent | none |

**A planned switch**. The Leaf names `switch_frame` a few frames ahead. The primary sends up to `switch_frame - 1`. The shadow sends from `switch_frame`. No frame is lost.

**A switch from HOT**. `U6` already decodes both streams and keeps the first good slice of each number. A dead primary costs zero frames.

**A switch from WARM after a sudden loss**. Frames are missing until the shadow starts. `U1` covers them by reprojection and speculative frames.

| The shadow RTT | The planned lead | The frames `U1` covers from WARM | The covered time | Inside the `40 ms` reprojection limit |
|---|---|---|---|---|
| `1 ms` | `2` frames | `3` | `12.5 ms` | yes |
| `6 ms` | `4` frames | `5` | `20.8 ms` | yes |
| `25 ms` | `8` frames | `9` | `37.5 ms` | yes |

**The honest reading**. "Zero frames" is exact for a planned switch and for HOT. From WARM it means zero frames *seen* lost, because `U1` covers the gap. Gate DST-12 measures both.

**The check before a switch**. `HandoverCommand.expected_chain_hash` must equal the shadow's heartbeat chain hash. A mismatch refuses the switch with `ERROR_CODE_SHADOW_NOT_IN_SYNC`, and the mismatch is evidence for RG-18.
