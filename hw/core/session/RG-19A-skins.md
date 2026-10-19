# BUDLUM LEAF · CORE AND SKIN · RG-19A · THE SESSION ORDER FOR SKINS

**Revision L.7 candidate · 2026-10-19 · session seat**. A study. It extends RG-19 of `hw/hostpower/continuity/RG-19-session-pause-resume.md`. It changes no L.6.0 or L.6.1 decision until Ayaz rules. The model is `skinsession.py`. The wire drafts are `proto/skin_chain.proto` and `proto/skin_link.proto`. `[HYPOTHESIS]` for every number.

## 1 · The order

| Order | The work | The acceptance test |
|---|---|---|
| **RG-19A** | a Skin id, a pairing record and a view id; a writer grant and a TakeOver; one ordered stream from many Skins; a pause that stores the views | `1 000` random moves of a session between two Cores and a Leaf give the same state root as a run with no move. The old writer is refused after each move. A rogue Skin and a stale pairing are refused |

## 2 · What each part holds

| Part | Holds | Never holds |
|---|---|---|
| the Skin | its identity in ROM, a volatile link key, a few scan lines | a key that signs, a nonce, a grant, a frame store, any session field |
| the Core | U7, the wallet-side keys, the frame store, the views, the sessions, the radios | nothing is missing: it is the device |
| the validator | the session state, the pause record, the writer list | a pairing secret |
| the chain | the PairingRecord, the WriterGrant, the pause and resume records | the views of a live session |

## 3 · The modes

| Mode | Sessions | Canvas | What a Skin gets |
|---|---|---|---|
| MIRROR | one | the session viewport, scaled to each Skin | the whole canvas |
| EXTEND | one | the union of the Skin rectangles | the tile range of its rectangle |
| SPLIT | one per Skin | each Skin alone | its own session |
| HANDOFF | one | moves | the view moves from one Skin to another; the session never pauses |

The Core merges all events by the key `(tick, class rank, skin id, seq)`. The tick is a `480 Hz` scan tick that the Core stamps on arrival. The class rank is pen, touch, key, shutter, IMU, camera. The key is total, so the order never depends on arrival. IMU samples and camera pixels are not transactions. A shutter press is.

## 4 · The six rules

The rules R1 to R11 of RG-19 stay. Rule R5 changes: a session can have several writers, all granted by the wallet.

| Rule | Text | Test |
|---|---|---|
| **R12** | A Skin is paired to one Core at a time. A new pairing needs the wallet. A move to a Core on the allowed list needs no wallet. Each move raises the pairing epoch, and the old link key dies. | `test_a_new_pairing_moves_the_skin_and_raises_the_epoch`, `test_an_allowed_core_takes_the_skin_without_the_wallet` |
| **R13** | A granted writer takes a live session with one TakeOver transaction. No pause and no lapse. The epoch rises, so the old writer is refused. | `test_takeover_changes_the_writer_and_not_the_state`, `test_the_old_writer_is_refused_after_a_takeover` |
| **R14** | A view is not durable. A pause stores the view list. A resume names the views to rebind. A Skin that is gone drops out of the list, and the Core says so. | `test_a_skin_power_cycle_leaves_the_session_root` |
| **R15** | A Skin sends events with a MAC and never a signature. The Core stamps, merges and signs. The validator sees one writer. | `test_the_ledger_sees_one_writer_for_every_mode`, `test_the_order_never_depends_on_arrival_order` |
| **R16** | The last view that leaves a Core pauses the session, with the reason VIEWS_LOST, unless a TakeOver follows. A session with other views stays. | `test_split_pause_of_one_session_leaves_the_others` |
| **R17** | At C2 the device is a Leaf. Its U7 is a granted writer. A move between C0 or C1 and C2 is a TakeOver. | `test_two_cores_pass_the_session_back_and_forth` |

**Why R13 is new.** In RG-19 a dead Core would need a lapse of `2 s` before another writer resumes. A TakeOver removes the wait. In the model it cuts a `1.12 s` roam to `0.30 s`.

**What R13 risks.** Two granted writers can take the session from each other with no proof that the other is gone. Both belong to one wallet. The wallet revokes a grant. A stolen Core with a live grant is a threat. The trust seat owns it. Open issue A1.

## 5 · The messages

All sizes come from `skinproto.py`. They use stand-in signatures of the exact FIPS 204 length.

| Message | Where | Bytes | Purpose |
|---|---|---|---|
| ViewRef | inside a pause or resume | about `45` each | Skin id, view id, mode, rectangle, epochs |
| PairingRecord | chain | `4 799` | the Core of a Skin, the allowed Cores, the wallet signature |
| WriterGrant | chain | `4 720` | the wallet makes a Core a writer |
| WriterTakeOver | chain | `2 544` | a granted writer takes a live session |
| SkinLinkLost | Core to validator | `31` | a view went dark |
| SessionPause with two views | Leaf wire | `2 885` | the RG-19 pause, now with the views and the Core id |
| SessionResume with two views | Leaf wire | `2 784` | the RG-19 resume, now with the writer change |
| SkinAttach, SkinAttachAck, ViewBind, ViewUnbind | Skin link, `budlum.skin.v1` | `24` to `62` | attach and bind |
| SkinEvent | Skin link | `32` | one raw event with a `16` byte tag |

The draft adds three `LeafMessage` bodies, `39` to `41`, five error codes, `1100` to `1104`, and the pause reason VIEWS_LOST. It edits no existing field. The wire minor becomes `1.2`.

## 6 · The acceptance test of RG-19A

| Step | The test | The pass condition |
|---|---|---|
| 1 | `1 000` random moves of a session across Core A, Core B and a Leaf, by pause and by TakeOver | the same state root as a run with no move |
| 2 | an input of the old writer after each move | refused |
| 3 | a Core with no grant, a forged grant, an expired grant | each refused with its code |
| 4 | four Skins on one Core, `10^6` events, shuffled arrival | one order, per-Skin order kept, none lost |
| 5 | a rogue Skin, a stale pairing, a revoked pairing | each refused |
| 6 | a Skin power cycle at `10 000` random instants | the session root equals a twin with no cycle |
| 7 | the model on `validator/leaf-duty` with three validators | the same result as the model |

The model passes the model version of each step. The crate test is still to run. Step 7 stays `[HYPOTHESIS]`.

## 7 · The open issues

| No. | The issue | The owner |
|---|---|---|
| A1 | A TakeOver gives a granted writer power over a live session. A stolen Core with a live grant is a risk. Revocation must be fast | trust seat |
| A2 | The pairing record is on chain. It shows a pseudonymous Skin id to every validator. A privacy rule is open | trust seat |
| A3 | `leaf-duty` has one writer per session. The `writers` list exists, but the optimistic path assumes one. RG-18 must test two | RG-18 |
| A4 | A Skin cannot prove it is the Skin of its ROM id without a secret in OTP. The pairing secret is the trust seat's | trust seat |
