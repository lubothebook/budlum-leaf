# BUDLUM LEAF · CORE AND SKIN · TRUST · 02 · THE DESIGN RULES

**Revision L.7 candidate · 2026-10-19 · TRUST seat of block HP-2**. The model is `skinauth.py`. The tests are `tests/test_skinauth.py`. It is a study. Every rule here is `[HYPOTHESIS]` until Ayaz rules and the Program Lead signs it.

## 1 · The trust boundary

**The idea**. The Skin is a host of pixels and fingers, in the way that the power host of Part 22 is a host of energy. The Skin never gains authority. `[DECISION]` for the study.

**Inside the boundary** are `U7`, the `U4` ROM, the trusted display path (the `U1` ROM and the rear panel driver) and the button. At C2 the local floor of the Leaf joins them. Everything else is outside. The Skin, the link, the radios, the camera, the validator compute and every host are outside.

| Distance class | The Skin or far end | Where the wallet lives | The trust model |
|---|---|---|---|
| C0, a tether up to `2 m` | a zero-key Skin | the Core `U7` | the model of this sheet, button reachable |
| C1, a room up to `30 m` | a zero-key Skin | the Core `U7` | the model of this sheet, a confirmation device carries the press |
| C2, kilometres | the Leaf as in L.6.0 | the Leaf `U7` | the L.6.0 model, the Core is a remote validator with no authority |

`trust_model()` in `skinauth.py` holds this table. `[DECISION]` BRIEF Section 8 for the classes.

## 2 · What the Skin keeps

The Skin keeps the least that it needs. The slogan "nothing that signs" is false in a literal sense: the identity chip signs. The true sentence is that the Skin holds nothing that signs for the wallet.

| The item | Where | The rule |
|---|---|---|
| an identity key | the identity chip, hardened | signs a pairing challenge and a session challenge, and nothing else |
| the vendor certificate | the identity chip | proves the key came from the factory, as SW-16 provisions |
| up to `4` pinned Core keys | Skin NVM | each with an epoch, a role and a capability mask |
| the decoder firmware digest | the identity chip measures it | goes into the SkinRecord |
| the link keys | RAM only | die at power loss, never in NVM |
| the frame store | RAM only | blanked at power loss and `100 ms` after the last valid slice |

**What the Skin never keeps**. The wallet key. A session key at rest. A PIN. A seed. The authority to confirm a summary.

## 3 · Pairing

**Rule R-P1**. Pairing needs a press on the Core button and a press on the Skin button. A tap never pairs. `[HYPOTHESIS]`

**Rule R-P2**. Both sides show a six digit short authentication string. The owner compares them, and then the Core takes a second press. A relay at pairing makes the strings differ.

**Rule R-P3**. The Core accepts a record only for its own key, with a fresh counter, a fresh nonce and an expiry above the anchor.

**Rule R-P4**. A Skin without a vendor certificate gets the viewer tier at most. So does a Skin with an unlisted decoder firmware digest.

**Rule R-P5**. Pairing happens in contact range, C0. A pairing over a radio link is refused. `[HYPOTHESIS]`

**Rule R-P6**. The Skin keeps `4` pairing slots. Unpinning all of them needs a press on the Skin.

**The limit of R-P2**. A user who ignores the strings pairs the attacker. The test `test_the_residual_a_user_who_ignores_the_sas_pairs_the_attacker` shows it. A certified attacker Skin gets the owner tier.

### 3.1 · The tiers

| Tier | Meaning | Pixels it receives | What its tap can do |
|---|---|---|---|
| S0 | the Core is locked | a fixed lock screen | nothing |
| S1 | a viewer, uncertified or unlisted | public class only | nothing |
| S2 | an owner Skin | public, private and summary classes | an input batch, and a value up to the blind budget |

## 4 · The SkinRecord

The record generalises the HostRecord of `hw/hostpower/trust`. The frame is `276` bytes: `148` of record, `64` of chip signature and `64` of vendor certificate.

| The HostRecord field | The SkinRecord field | The change |
|---|---|---|
| host key id | skin key | the identity key of the chip |
| class | tier | `S1` or `S2` requested, the Core decides |
| lanes | capability mask | touch, camera, microphone, speaker |
| maximum power and window | link class | `0` to `3` |
| expiry, counter, nonce | the same | the counter lives in the Core NVM |
| measured volts (the channel binding) | the link transcript | the session signatures bind the link |
| role validator | none | a Skin has no role |
| none | core key | the record names one Core |
| none | decoder digest | the chip measures the decoder |

The signature tags are `BDLM_SKIN_PAIR_V1` and `BDLM_SKIN_SESSION_V1`. They join the open issue U7-3 of `fw/u7`.

## 5 · The link

**Rule R-L1**. The session key exchange is a signed transcript. Each side makes an ephemeral X25519 key and signs the whole transcript with its identity key.

**Rule R-L2**. The transcript holds both keys, both nonces, both identities, the offered suites and the chosen suite. A downgrade changes it, so the signature fails.

**Rule R-L3**. The Skin refuses any suite below its floor. The Core holds a floor too.

**Rule R-L4**. HKDF makes one key per direction. The link seals each slice with ChaCha20-Poly1305 under a strict counter. A replay or a reorder is refused.

**Rule R-L5**. A session lasts one hour at most. After that the pair rekeys.

**Rule R-L6**. No plaintext fallback exists. A Skin with no valid slice for `100 ms` blanks its frame store and shows its own no-link pattern.

**Rule R-L7**. A lost link locks the Core. An unlock needs the button path of the Core.

### 5.1 · The cost in a minimal Skin decoder

The tag is checked per slice, so a slice waits for its tag. Output of `aead_budget()`. The rows for `pJ/bit` are a sweep, and no part is measured. `[HYPOTHESIS]`

| Link rate | Slice, `16` rows at `240 Hz` | Buffer | Added latency | Power at `1 pJ/bit` | At `5 pJ/bit` |
|---|---|---|---|---|---|
| `6.1 Gbit/s` | `20.8 µs` | `15.5 KiB` | `20.8 µs` | `6.1 mW` | `30.5 mW` |
| `9.2 Gbit/s` | `20.8 µs` | `23.4 KiB` | `20.8 µs` | `9.2 mW` | `46.0 mW` |
| `12.3 Gbit/s` | `20.8 µs` | `31.3 KiB` | `20.8 µs` | `12.3 mW` | `61.5 mW` |
| `0.15 Gbit/s`, C2 | `20.8 µs` | `0.4 KiB` | `20.8 µs` | `0.15 mW` | `0.75 mW` |

One pipelined `128` bit engine at `400 MHz` gives `51.2 Gbit/s`, so one engine carries every row. The tag adds `0.05 %`. At `5 pJ/bit` and `12.3 Gbit/s`, the cipher takes `7.7 %` of the `0.80 W` surface load. At `1 pJ/bit` it takes `1.5 %`. The slice counter reaches `2^32` after `24.9 h`, so a rekey each hour is safe.

**The cost that is not power**. The Skin needs a key store, a replay window and a verify engine. It is no longer the plain decoder of the first sketch.

## 6 · Revocation and the chain

**Rule R-R1**. The owner revokes a Skin with the Core button. A revocation is a key operation.

**Rule R-R2**. A revocation ends the live session at once. The next connect is refused, for the clone as well as the original.

**Rule R-R3**. The chain records a pairing as a commitment: the hash of the Skin key and a salt that the Core keeps. The chain never holds a Skin key or a serial.

**Rule R-R4**. Pairing and revocation records carry a wallet counter. The chain refuses an older record, so a replay after a revocation fails.

**Rule R-R5**. Two live sessions under one Skin key are a clone alert. The Core drops both and marks the key suspect. Only the button reinstates it.

**Rule R-R6**. A revoked Skin that is offline learns nothing. The Core enforces the revocation, because the Skin cannot reach the chain.

**The cost of R-R5**. An attacker who holds the clone key can raise the alert on purpose. That is a denial of service, and a button press ends it.

## 7 · A Skin that roams

A Skin roams. A wallet session does not. A session binds to the wallet key, and the key lives in one `U7` and never moves. `[DECISION]` `fw/u7` README.

**Rule R-M1**. Each Core has its own pairing with the Skin, its own link keys and its own role. A Core that is not the owner gets the guest role.

**Rule R-M2**. A guest Core never gets the camera or the microphone. Both sides press to enable a lane, the Core and the Skin.

**Rule R-M3**. The Skin has one active Core. A new session ends the old one.

**Rule R-M4**. A trusted strip shows a fingerprint of the active Core. The Skin draws it. The pixel stream cannot paint over it.

**Rule R-M5**. Continuity across two Cores of one owner needs one account with several device keys, as SW-15 describes. Each key has its own cap. The model has `Account`.

## 8 · What you see is what you sign

The surface is outside the boundary. A rogue Skin shows a false summary and reports a tap on "sign". No cryptography tells a real tap from a forged one. The rule takes the authority away from the Skin.

**Rule R-W1**. The Core derives the summary from the transaction bytes. A summary from the Skin is ignored.

**Rule R-W2**. The Core shows the summary on its own trusted display. The press binds to the hash of what the display showed. A second request replaces the display, so a press for the first fails.

**Rule R-W3**. A value above the blind budget needs a confirmation that does not cross the Skin. A key operation always needs one.

| Distance | The confirmation path |
|---|---|
| C0 | the button and the display of the Core |
| C1 | a confirmation device with its own button and display, paired with the Core |
| C2 | the local floor of the Leaf, which a page cannot paint |

**Rule R-W4**. The press is a hardware token that software cannot mint. A press counts once. It expires after `30 s`. The summary must show for `1.5 s` first.

**Rule R-W5**. A tap from an owner Skin can confirm a value up to the blind budget per day. The budget lives in NVM, so a power cut does not reset it.

**Rule R-W6**. An input batch carries no value. The Core refuses an input request that names an amount.

**Rule R-W7**. A change of a trusted part locks signing until the owner confirms with the button. The trusted parts are `U7`, `U4`, `U1`, the rear panel driver and the button.

**Rule R-W8**. A camera image is untrusted input. An address from the camera shows on the Core display, from the transaction bytes.

**The trusted tile, considered and not chosen**. A tile with its own key would attest the tap. It needs a secure element on every Skin. A lab can extract its key, and then the attacker owns a tile. The button of the Core is cheaper and stronger.

**The blind budget**. A forged-tap flood of `100` requests of `10` units against a budget of `100` signs exactly `10`. The loss is at most the budget per day. The test `test_a_flood_of_forged_taps_loses_at_most_the_blind_budget` shows it.

## 9 · The screen content

| Class | Examples | Where it goes |
|---|---|---|
| PUBLIC | menus, a lock screen | any tier S1 or higher |
| PRIVATE | balances, messages, photos | an owner Skin on an unlocked Core |
| SECRET | a PIN, a seed phrase, a recovery share | the Core display only, never the Skin |
| TXSUM | a summary mirror, for comfort | an owner Skin, never as the authority |

**Rule R-C1**. A SECRET item never enters the pixel stream. The Skin gets a placeholder.

**Rule R-C2**. A PIN is entered on the Core path. A keypad drawn on a Skin shows its layout and its taps to the Skin.

**Rule R-C3**. The Core locks when the link is lost. The owner unlocks it on the Core path.

**The limit**. A paired Skin that is hostile reads every PRIVATE pixel it gets. The tier and the lock bound it. Nothing else does. `[HYPOTHESIS]`

## 10 · The Core that is also a validator

**Rule R-V1**. The validator compute is outside the boundary. It reaches `U7` through the same API as any remote validator.

**Rule R-V2**. The validator compute has no handle to the button secret. It cannot mint a press.

**Rule R-V3**. The validator key and the wallet key are different keys. The wallet key never signs frames.

**Rule R-V4**. A Core that streams to its own Skin passes SW-22 like any validator. No shortcut exists for the owner's Core.

**The tension**. A validator runs on-chain programs, and that is third-party code. It cannot sit inside the Zero-CPU boundary of the Leaf. Study seat `study` and seat `session` read this cost.

## 11 · The long link, C1 and C2

**Rule R-X1**. No authority comes from distance or from proximity. A session near the Core does not unlock it.

**Rule R-X2**. The pixel link at C2 is end to end: the validator seals, and `U6` opens. A base station is not an endpoint. The L.6.0 text says the Leaf runs no session cipher. The study needs one. Open issue O5.

**Rule R-X3**. The distance proof of SW-24 bounds a distance from above only. A round trip can grow by a relay and never shrink. The margin of `1 ms` hides `100 km` of fibre one way.

**Rule R-X4**. The room class needs UWB with the signed STS commitment. A distance reduction attack on the UWB receiver remains. `[PUBLICATION]` Leu et al., Ghost Peak, USENIX Security 2022. It cut `12 m` to `0 m` with up to `4 %` success on HRP UWB.

**Rule R-X5**. Jamming ends in a blank Skin, a locked Core and the safe screen. It never ends in a plaintext link or a stale private frame.

### 11.1 · The mixed fleet

One account holds several device keys. The Core key is the root and has no cap. The Leaf key has a daily cap. A key that is not the root cannot add or revoke keys. The model assumes that the chain can hold a cap per key. `[HYPOTHESIS]`

| The stolen item | What it holds | What it can spend |
|---|---|---|
| a Skin at C0 or C1 | no signing key | nothing |
| a Leaf at C2 | a device key of its own | up to its cap per day, until the root revokes it |
| a Core | the root key | all, until recovery, so the Core is the item to protect |

**The weakest key**. The daily loss from stolen non-root keys is the sum of their caps. A stolen root key loses everything.
