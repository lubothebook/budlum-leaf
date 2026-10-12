# BUDLUM LEAF · PROTO · VERSIONING, CANONICAL BYTES AND ERROR CODES

**Revision L.6.0 · 2026-10-12 · the Wire-Protocol team**. This file holds the rules that keep `budlum.leaf.v1` stable. The round-trip test enforces the canonical rule and the refusal map.

## 1 · The version scheme

| The item | The rule |
|---|---|
| the package | `budlum.leaf.v1`. A wire break makes a new package `budlum.leaf.v2` |
| the wire version | `LeafMessage.wire_version = major * 65536 + minor`, set on the first message of each stream or datagram flow |
| a minor version | only additive: a new field, a new message, a new enum value, a new `LeafMessage` body |
| a field number | never reused and never retyped. A removed field becomes `reserved` |
| the `buf` gate | `buf lint` STANDARD and `buf breaking`, as in `/home/claude/budlum/buf.yaml` |

**The negotiation**.

1. `Hello.version` gives the major and the range of minors the Leaf accepts.
2. The validator answers with the highest common minor in `Admission`.
3. A different major gets `ERROR_CODE_VERSION_UNSUPPORTED`, and the Leaf shows the safe screen.
4. The test function `negotiate()` checks this rule.

**A new field on old silicon**. `U6` and `U1` are fixed-function. They parse a fixed field set. The rule is therefore strict:

1. A new field in a hardware-parsed message needs a new major. These are `SliceHeader`, `Slice`, `FrameCommit`, `LayerUpdate`, `Layer`, `GlyphAtlasUpdate`, `SpeculativeFrameSet` and `InputBatch`.
2. Every other message tolerates unknown fields outside a MAC or signature scope.
3. The validator sends no field above the negotiated minor.

## 2 · The canonical bytes

A MAC and a signature cover bytes, so every sender writes one encoding only. `[DECISION]` of this team.

1. Fields go in ascending number order.
2. A varint uses its minimal length.
3. A proto3 default is omitted. A set member of a oneof is always written.
4. A repeated scalar is packed.
5. A MAC or signature scope holds no unknown field.

The google runtime with `deterministic=True` writes the same bytes. The test compares the two encoders byte for byte on every message. The strict decoder of `tools/protolite.py` models `U6`: it rejects a field out of order, a repeated singular field and a padded varint.

## 3 · The domain tags

Each tag joins the Budlum inventory `src/crypto/domain_tags.rs` before use. That file belongs to the chain team.

| The tag | The use |
|---|---|
| `BDLM_LEAF_SLICE_V1` | KMAC customisation for `Slice.mac` |
| `BDLM_LEAF_FRAME_COMMIT_V1` | KMAC customisation for `FrameCommit.mac` |
| `BDLM_LEAF_SPECULATIVE_V1` | KMAC customisation for `SpeculativeFrameSet.mac` |
| `BDLM_LEAF_LAYER_V1` | KMAC customisation for `LayerUpdate.mac` |
| `BDLM_LEAF_ATLAS_V1` | KMAC customisation for `GlyphAtlasUpdate.mac` |
| `BDLM_LEAF_INPUT_V1` | KMAC customisation for `InputBatch.tag` |
| `BDLM_LEAF_HANDOVER_V1` | KMAC customisation for `HandoverCommand.tag` |
| `BDLM_LEAF_CAPTURE_V1` | KMAC customisation for `CameraCaptureOpen.tag` |
| `BDLM_LEAF_INPUT_CHAIN_V1` | the SHA3-256 input chain that `Receipt.input_chain_head` closes |
| `BDLM_LEAF_FRAME_CHAIN_V1` | the SHA3-256 frame hash chain of `FrameCommit.chain_hash` |
| `BDLM_LEAF_TRANSCRIPT_V1` | `Admission.transcript_hash` |
| `BDLM_LEAF_GRANT_V1`, `BDLM_LEAF_ADMISSION_V1`, `BDLM_LEAF_LEASE_V1`, `BDLM_LEAF_REVOKE_V1` | the signatures of the session setup |
| `BDLM_LEAF_MERKLE_V1`, `BDLM_LEAF_RECEIPT_V1`, `BDLM_LEAF_SHADOW_V1` | the signatures of the proof path |
| `BDLM_LEAF_CAPTURE_CLOSE_V1`, `BDLM_LEAF_CAMERA_RESULT_V1` | the signatures of the camera path |
| `EXPORTER-BDLM_LEAF_SLICE_MAC_V1`, `EXPORTER-BDLM_LEAF_INPUT_MAC_V1` | the TLS exporter labels of `K_slot` and `K_in` |

The Merkle trees use the prefix byte `0x00` for a leaf and `0x01` for a node, in the style of RFC 6962. `[PUBLICATION]`

## 4 · The error codes

`Error.fatal` ends the session with `Goodbye`. A non-fatal error is recorded and counted in the receipt window. Every visible change goes on the class line. The rule of FINAL/08 holds: never a silent success, never a silent degradation.

| The range | The code | What the Leaf does |
|---|---|---|
| `1xx` admission | `100` VERSION_UNSUPPORTED, `101` CHAIN_ID_MISMATCH | fatal, the safe screen |
| | `102` ANCHOR_MISMATCH, `109` NETWORK_SET_CHANGE_REFUSED | fatal, offer a re-anchor on a second channel |
| | `103` VALIDATOR_NOT_ACTIVE, `104` APP_NOT_ON_CHAIN | fatal, the safe screen only. Gate SW-22 |
| | `105` GRANT_EXPIRED, `106` GRANT_BAD_SIGNATURE | fatal, ask the wallet for a new grant |
| | `107` CAPACITY | try the next candidate from the probes |
| | `108` DISTANCE_PROOF_FAILED | drop the L0 candidate, record it. Gate SW-24 |
| `2xx` integrity | `200` SLICE_MAC_FAILED, `207` UPDATE_BAD_MAC | drop the slice or update, keep the last good tiles, count it |
| | `201` INPUT_TAG_FAILED, `205` REPLAY, `206` NON_CANONICAL | drop the message, count it |
| | `202` CHAIN_HASH_MISMATCH, `203` MERKLE_ROOT_MISMATCH | fatal to this validator, hand over, file evidence. Gate DST-4 |
| | `204` RECEIPT_BAD_SIGNATURE | the validator refuses the receipt window |
| `3xx` refusals | `301` to `310` are R1 to R10 of FINAL/08 Section 8.7 | each one as Section 8.7 states, and recorded |
| `4xx` stream | `400` CODEC_UNSUPPORTED | refuse the class at start, per R7 |
| | `401` FRAME_STORE_FULL, `402` SLICE_LATE, `403` DECODE_ERROR | reproject, ask for an intra refresh of the tile range |
| | `404` SPECULATION_EXPIRED, `405` LAYER_LIMIT, `406` ATLAS_LIMIT | drop the item, the validator resends a smaller set |
| `5xx` path | `500` PATH_LOST, `504` PROBE_TIMEOUT | move to the next path, keep the session |
| | `501` RTT_OVER_CLASS, `502` L4S_UNAVAILABLE | a visible class change on the class line |
| | `503` MTU_TOO_SMALL | switch slices to datagram mode with smaller fragments |
| `6xx` handover | `600` SHADOW_NOT_IN_SYNC, `601` HANDOVER_TOO_LATE, `602` SHADOW_UNKNOWN | refuse the switch, keep the primary, record |
| `7xx` capture and audio | `700` to `702` | keep the local provisional image, retry the upload on a cheap path |
| | `703` AUDIO_UNDERRUN | conceal, count it |
| `8xx` energy | `800` ENERGY_TIER_CHANGE, `801` THERMAL_LIMIT | a visible class change, never a silent one |
| `9xx` | `900` INTERNAL | non-fatal once, fatal when repeated in one second |
