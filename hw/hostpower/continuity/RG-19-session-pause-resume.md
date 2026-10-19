# BUDLUM LEAF · HOST POWER · RESEARCH ORDER RG-19 · SESSION PAUSE AND RESUME

**Revision L.6.1 (proposed) · 2026-10-19 · Continuity team**. This order follows `FINAL/21` Section 21.7. It extends RG-18, the validator Leaf duty of `validator/leaf-duty`. The reference model is `sessionchain.py`. The wire draft is `proto/session_continuity.proto`. The model tests are `tests/test_sessionchain.py` and `tests/test_proto_draft.py`.

## 1 · The order

| Order | The work | The acceptance test |
|---|---|---|
| **RG-19** | the validator pause duty: a SessionPause on chain, a lapse pause with evidence, a resume rule that binds the state root, an input epoch, a value-action outbox, a dual send | `1 000` random pauses of `1 s` to `30 days` in a `10 000` frame stream give the same final state root and the same frame hash chain as a run with no pause. A second validator resumes from the chain record and matches the first frame bit for bit |

**The reason**. A Leaf on a host lives as long as the host lives. Then a host goes. The session must not go with it. `FINAL/21` Section 21.5.2 says the Leaf holds no state that the network cannot rebuild. RG-19 turns that sentence into rules for the gap. `[DECISION]` proposed.

## 2 · What the validator stores

The session state is chain state. RG-19 adds `249` bytes to it. A paused session costs about `450` bytes of state, plus one transaction of `2.8 kB` in a block. `[HYPOTHESIS]` sizes from `protodraft.py`.

| Field | Bytes | What it is for |
|---|---|---|
| status | `1` | ACTIVE, PAUSED, PAUSED_LAPSE or CLOSED |
| pause_seq | `4` | one more than the last pause; never reused |
| resume_seq, the epoch | `4` | counts completed resumes; every input carries it |
| paused_root, the session root | `32` | the state root frozen at the pause; the resume must match it |
| paused_frame_link, the last frame hash | `32` | the head of the frame hash chain; frames continue from it |
| paused_frame_no | `8` | the session clock at the pause |
| paused_slot | `8` | the slot that anchors the pause; any validator rebuilds from its snapshot |
| last_leaf_second | `8` | the last second with a Leaf-signed receipt or input; the evidence for a lapse |
| grant_until | `8` | the session grant term; a resume after it needs the wallet |
| anchor | `72` | checkpoint height, block hash and validator set hash the Leaf held |
| input_chain_head, last_input_seq | `40` | the end of the input chain at the pause |
| pending_root | `32` | the Merkle root of the pending action hashes |
| **total** | **249** | |

**The pending actions** are hashes, never actions. A predicted action is a speculative frame that U1 showed. It was never sent. The resume drops it. A value action is a wallet-signed `ActionTx` in the U7 outbox. The Leaf resends it. The validator keeps only its hash, to refuse a double. `[DECISION]` proposed.

## 3 · The eleven rules

Each rule names its test in `tests/test_sessionchain.py`.

| Rule | Text | Test |
|---|---|---|
| **R1** | The session clock stops while the session is paused. A pause of any length leaves the state root unchanged. | `test_pause_of_any_length_leaves_the_state` |
| **R2** | Only the Leaf pauses a live session. The Leaf signs SessionPause with the session key. | `test_a_validator_cannot_sign_a_leaf_pause`, `test_inputs_are_refused_while_paused` |
| **R3** | A validator can pause by lapse only after `2 s` with no Leaf-signed receipt or input, and only with that evidence. A lapse changes no state and gives no authority. | `test_lapse_pause_needs_silence`, `test_lapse_with_wrong_evidence_is_refused` |
| **R4** | A resume names the paused root. The Leaf checks that root against a finality proof first. A different root is refused. | `test_resume_against_a_stale_root_is_refused` |
| **R5** | Only the Leaf resumes. A resume is single use, counted by `resume_seq`. | `test_a_validator_cannot_resume`, `test_second_resume_is_refused` |
| **R6** | A resume under a live grant uses the session key. After the grant term it needs the wallet key and a new grant. | `test_expired_grant_needs_the_wallet` |
| **R7** | Every input carries the epoch. An input of an old epoch is refused. An input expires `1 s` after it is signed. | `test_input_withheld_across_a_pause_cannot_fire_later` |
| **R8** | A value action is written to the U7 journal before it is sent. It carries its own nonce and expiry, and the chain admits it while the session is paused. | `test_a_signed_action_is_in_nvm_before_it_is_sent` |
| **R9** | On a host loss U7 signs the input chain head within `30 ms`. The Leaf sends inputs and receipts to the primary and to the shadow, and keeps its unacknowledged inputs for a resend. | `test_dual_send_loses_nothing_when_the_primary_dies`, `test_a_flush_on_host_loss_keeps_the_open_second` |
| **R10** | A pause lives `30 days`, then the session closes. The validator accepts at most one pause per session per `10 s`. | `test_a_pause_older_than_the_ttl_closes`, `test_a_second_pause_inside_10_seconds_is_limited` |
| **R11** | A resume after the weak-subjectivity window needs a re-anchor by a second channel, as in `FINAL/08` Section 8.5. | `handover_sim.py`, outcome STATED_ANCHOR |

**The flush trigger**. R9 starts on the host-lost threshold of the power-path team. That is VHV under `8.0 V`, or a missing sideband heartbeat for `100 µs`. A store of `5 J` covers the `30 ms` flush `1 000` times over. `[HYPOTHESIS]`

**Why R7 matters**. A hostile host can hold a signed tap and deliver it after the resume. Without an epoch the nonce is still current and the tap fires. With the epoch it is refused.

**Why R9 matters**. One lost input leaves a nonce gap. Every later input of the epoch is then refused. `test_single_replica_loses_the_in_flight_window` shows the wedge. The ring resend heals it while the Leaf is alive. The resume rebuilds the nonce from the chain when the Leaf lost power.

## 4 · The messages

The draft keeps the rules of `proto/VERSIONING.md`. It adds messages, six `LeafMessage` bodies and ten error codes. It edits no existing field. The wire minor becomes `1.1`.

| Message | Direction | Envelope bytes | Purpose |
|---|---|---|---|
| SessionPause | Leaf to validator, then chain | `2 764` | the pause, signed by the session key |
| SessionPauseAck | validator to Leaf | `3 409` | the slot that anchors the pause |
| LapseNotice | validator to chain | `3 449` | a lapse pause with evidence |
| SessionResume | Leaf to validator, then chain | `2 629`, or `8 711` with a renewed grant | the resume, signed by the session key or the wallet |
| ResumeAck | validator to Leaf | `3 486` | the state root, the first frame number and the intra refresh |
| PowerNotice | Leaf to validator | `39` | the power state, the minutes left and whether the face is lit |

`Hello.resume_session_id` already exists for a path loss. A power resume sends that Hello, then SessionResume as the first control message. The sizes use stand-in signatures of the exact FIPS 204 length.

| Model code | Wire code |
|---|---|
| BAD_SIGNATURE | `106` GRANT_BAD_SIGNATURE or `204` RECEIPT_BAD_SIGNATURE |
| BAD_NONCE, REPLAY | `205` REPLAY |
| GRANT_EXPIRED | `105` GRANT_EXPIRED |
| RESUME_STATE_MISMATCH | `1000` |
| PAUSE_UNKNOWN, SESSION_NOT_PAUSED, SESSION_NOT_ACTIVE | `1001`, `1002`, `1003` |
| STALE_EPOCH, EXPIRED | `1004`, `1009` |
| PAUSE_TTL_EXPIRED, LAPSE_TOO_EARLY, LAPSE_BAD_EVIDENCE, PAUSE_RATE_LIMIT | `1005`, `1006`, `1007`, `1008` |

## 5 · The resume, step by step

1. A host passes U7. The Leaf boots by `bootsm.py` to the link.
2. The Leaf sends Hello with `resume_session_id`. U7 checks the validator key in the active set.
3. The validator names the snapshot slot. It rebuilds the state from the chain record.
4. U7 checks the paused root against a finality proof. A mismatch ends in RESUME_STATED.
5. U7 signs SessionResume with the session key, or with the wallet if the grant expired.
6. The validator checks the rules R4 to R6 and submits the resume to the chain.
7. The validator sends ResumeAck and a full intra frame. The frame store was lost in the gap.
8. The Leaf resends its outbox. It rebuilds its input nonce from ResumeAck. The input epoch rises by one.

## 6 · What the validator must do

1. Store the `249` bytes of Section 2 for each paused session. Rebuild the state from the snapshot slot.
2. Send no slices to a dark face. Act on PowerNotice and keep the session state hot for `60 s`.
3. Submit a LapseNotice only after `2 s` of silence, with the last receipt second as evidence.
4. Accept inputs and receipts from the Leaf and from the shadow. Drop a duplicate by its hash.
5. Check every resume against R4 to R6 before it goes to the chain.
6. Send a full intra frame after every resume, because the Leaf frame store does not survive.
7. Count no served minute for a paused session in the coverage rewards.
8. Refuse a second pause in `10 s`, and close a session after the pause TTL.

## 7 · What a gap still loses

Say it first. A power gap never loses finalized chain state and never moves a key. These cases still lose something. Each one is stated, never silent.

| Case | What is lost | The bound | The mitigation |
|---|---|---|---|
| a cut with no flush, per-second signed head | the open second of inputs | up to `1 s`, `5` events on average at `10` events per second | R9: flush the head on the host loss |
| a cut with a flush | the inputs in flight | one gossip delay, about `17 ms` | the ring resend, while the Leaf lives |
| a dock with no uplink and no other radio path, then a power cut | every input since the last finality | up to `7 s`: the slot of `6 s` and the lag of `1 s` | label the class line LOCAL; dual send over the Leaf radio |
| a predicted action | the action, by design | one speculative frame | the resume shows the confirmed state |
| a gap longer than the grant term | the live session, not the state | the term, `24 h` here | one wallet action |
| a gap longer than the anchor window | the ability to verify alone | the window, `14 days` here | a re-anchor by a second channel |
| a pause older than the TTL | the session view, not the account state | `30 days` | open a new session on the same account |
| the Leaf frame store | the last frame | always | a full intra frame, `256 kB` |

The two windows, `24 h` and `14 days`, are `[HYPOTHESIS]`. The real window of the validator set is a Budlum parameter. This team did not read it.

## 8 · The acceptance test of RG-19

Run on `validator/leaf-duty` with three validators and the U7 model.

| Step | The test | The pass condition |
|---|---|---|
| 1 | stream `10 000` frames with `1 000` random pauses of `1 s` to `30 days` | final state root and frame hash chain equal a run with no pause |
| 2 | a second validator resumes from the chain record | its first frame matches the first validator bit for bit |
| 3 | `100` cuts with no pause | each ends in a lapse pause, and two validators replay it to the same root |
| 4 | a forged lapse, a withheld receipt, a validator resume, a stale root, a withheld input | each is refused with its code of Section 4 |
| 5 | `1 000` power cuts at random instants of a U7 journal write | the record is the old or the new one, never a mix |
| 6 | a grant that expires in the gap | the session key resume is refused and the wallet resume works |
| 7 | the primary dies with the Leaf dual-sending | no input is lost |
| 8 | the primary dies with a single send | the lost window is at most one gossip delay, and the resend heals it |

The model passes the model version of each step. It does not replace the crate test. `[HYPOTHESIS]` until the crate runs it.

## 9 · What RG-18 must change

| File | Change |
|---|---|
| `session.rs` | add the fields of Section 2 to `SessionState`; add the epoch to the `InputTx` signing hash |
| `chain.rs` | add the Pause, Lapse and Resume transactions and the rules R1 to R11; stop `tick` while paused |
| `validator.rs` | add the lapse timer, the dual send and the full intra frame after a resume |
| `receipt.rs` | count no `frames_shown` for a paused session |
| `evidence.rs` | decide if a false lapse is slashable; see the open issue |
| `mirror.rs` | add the `BDLM_LEAF_SESSION_PAUSE_V1` and `BDLM_LEAF_SESSION_RESUME_V1` tags to the inventory |

## 10 · The open issues

| No. | The issue | The owner |
|---|---|---|
| G1 | `leaf-duty` signs every `InputTx` with the wallet. The wire draft signs a chain head once per second. R9 needs one reading. The loss window depends on it | RG-18, wire team |
| G2 | `leaf-duty` uses a `32` byte session id. The wire protocol uses `uint64`. The pause record needs one | RG-18, wire team |
| G3 | Is a false lapse slashable? Without a Leaf-signed receipt held by the shadow, the proof does not exist | chain team |
| G4 | The grant term and the anchor window are `[HYPOTHESIS]`. The Budlum parameters decide them | chain team |
| G5 | `PAUSE_RATE_LIMIT` must stop a spam of pauses and still let a Leaf on a bad connector pause often | chain team |
| G6 | An FRAM journal of events would cut the L3 loss of Section 7 to zero. It adds a part and a cost | firmware, B module |
