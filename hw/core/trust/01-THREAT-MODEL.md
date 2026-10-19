# BUDLUM LEAF · CORE AND SKIN · TRUST · 01 · THE THREAT MODEL

**Revision L.7 candidate · 2026-10-19 · TRUST seat of block HP-2**. The rules are in `02-DESIGN-RULES.md`. The gates are in `03-GATE-MAP.md`. The model is `skinauth.py`.

**The question**. If every key lives in a Core and the surface is a Skin, what is the trust model? Does a stolen Skin hold nothing?

## 1 · The assets

| Asset | Why it matters | Where it lives |
|---|---|---|
| A1 the wallet key and its signatures | a forged signature is a theft of funds | the Core `U7`, or the Leaf `U7` at C2 |
| A2 the intent of the user | what the user sees must be what the wallet signs | the display path and the button |
| A3 the screen content | pixels carry balances, messages, a PIN, a seed | the pixel stream and the Skin |
| A4 the pairing and the identity | they decide who can drive whom | `U7` NVM, the Skin identity chip, the chain |
| A5 the firmware and the parts of the Core | a swapped part is a takeover | `U7`, `fw/boot`, the part record of law L9 |
| A6 the owner: habits and place | a Skin or a link must not track the owner | the identity, the link, the registry |
| A7 the camera and microphone feed | a sensor head sees and hears the owner | the Skin sensor head |

## 2 · The parties

| Party | Trust | Power it holds |
|---|---|---|
| the Core `U7` and the button | the root | signs, judges every Skin |
| the trusted display path | the root | shows the summary the Core derived |
| the Skin | none | shows pixels, reports taps, holds an identity key and a link key |
| the link, tether or radio | none | carries bytes |
| a Core that is a validator | none for authority | renders for others, streams to its Skin |
| a confirmation device | the root, by pairing | carries a press where the Core is out of reach |

## 3 · The threats

STRIDE-lite letters: S spoofing, T tampering, R repudiation, I information disclosure, D denial of service, E elevation of privilege. A gate named `HC-T..` is new. `03-GATE-MAP.md` defines it.

| ID | STRIDE | The attack | The asset | The countermeasure | The gate |
|---|---|---|---|---|---|
| T1 | I, S | a stolen Skin is read in a lab | A1, A3, A4 | no wallet key and no session key at rest. The frame store dies with power. A hardened chip protects the identity key | HC-T1, SW-16 |
| T2 | I | a rogue Skin pairs and reads every pixel | A3 | pairing needs two presses and the SAS. Content classes: a SECRET never enters the stream. Tier and lock bound the rest | HC-T2, HC-T7 |
| T3 | S | a cloned Skin, with the extracted identity key | A3, A4 | a clone alert on two live sessions. A locked Core gives a clone the lock screen. A revocation covers the key | HC-T9, HC-T4 |
| T4 | T, I | a man in the middle on the tether or the radio link | A1, A3 | a signed transcript, ephemeral keys, a per-slice AEAD, a strict counter, no plaintext fallback | HC-T3 |
| T5 | S, T | a man in the middle at pairing: a relay pairs with both sides | A4 | the SAS differs on the two sides. Contact range pairing. Two presses | HC-T2 |
| T6 | S, E | a rogue Core drives the Skin of the user and phishes a PIN | A2, A3 | the Skin pins its Cores. A new Core needs a press on the Skin. A trusted strip shows the Core fingerprint. A PIN goes on the Core path only | HC-T8 |
| T7 | I | a guest or rogue Core reads the camera and microphone | A7 | a lane needs a press on the Skin and the button on the Core. A guest never gets a lane | HC-T8, HC-T12 |
| T8 | E, T | a Core that is also a validator uses its compute to confirm its own request | A1, A2 | the validator compute is outside the boundary. It cannot mint a press. A different key signs frames | HC-T13, SW-22 |
| T9 | S | replay of a pairing, of a record or of a chain entry | A4 | a nonce in the signature, a counter in Core NVM, a wallet counter on the chain | HC-T2, HC-T4 |
| T10 | E, T | the worst hole: a Skin forges a tap on "sign" and paints a false summary | A1, A2 | a tap never confirms a key operation or a large value. The press binds to the Core summary hash. A blind budget bounds the rest | HC-T5, HC-T6 |
| T11 | T | the emitters or the touch controller are tampered with | A2 | the same as T10, since the Core cannot tell the tamper from a Skin that lies | HC-T5 |
| T12 | I, S | the camera sensor head on a Skin feeds a false image or leaks the scene | A2, A7 | an image is untrusted input. An address shows on the Core display from the transaction bytes. The lane needs two presses | HC-T12 |
| T13 | S, I | the Skin identity chip is counterfeit, glitched or probed | A4 | a vendor certificate, a hardened chip, a rate limit, the island rule and the line tests of hostpower | HC-T10, HST-T4, HST-T6 |
| T14 | T | a part swapped in the Core: a radio, the decoder, the display path | A5, A2 | `U7` measures the parts. A trusted part that changes locks signing until the owner presses | HC-T6, Z5, Z6 |
| T15 | I | the screen content as the asset: a PIN, a seed, a summary | A3 | classes PUBLIC, PRIVATE, SECRET and TXSUM. A SECRET shows on the Core only | HC-T7 |
| T16 | I | the registry on the chain links a Skin to an owner | A6 | the chain holds a salted commitment. The salt stays in the Core | HC-T17 |
| T17 | I | residual pixels in a stolen powered-off or jammed Skin | A3 | the frame store blanks at power loss and `100 ms` after the last valid slice | HC-T1, HC-T15 |
| T18 | D | slot exhaustion or a false clone alert, as a lever | A4 | a press for each pairing. A press ends a suspect state | HC-T9 |
| T19 | S, I | a rogue base station or a relay on the long link | A3 | the pixel cipher is end to end. A base station is not an endpoint | HC-T15 |
| T20 | S | distance bounding fraud on the nearest-validator proof of SW-24 | A6 | the RTT proof bounds distance from above. UWB with a signed STS commitment gates the room class | HC-T15, SW-24 |
| T21 | T | a downgrade of the link suite, or of the link class | A1, A3 | the offered suites and the choice are in the signed transcript. Both sides hold a floor | HC-T3 |
| T22 | D | jamming of the link | A3, A2 | a blank Skin, a locked Core and the safe screen. No plaintext fallback | HC-T15 |
| T23 | E | a mixed fleet: one account, a Skin at C0 and a Leaf at C2. The weakest device key sets the loss | A1 | one root key, capped device keys, revocation by the root. A Skin holds no key | HC-T16 |
| T24 | E | proximity as authority: a relay extends the reach of an unlock | A1 | no unlock from distance. A session is not an unlock | HC-T14 |

## 4 · The state of each threat in the model

| Threat | State | The reason |
|---|---|---|
| T4, T5, T9, T21 | closed in the model | a test refuses each one |
| T1, T3, T13, T17 | bounded | they depend on a hardened chip and a lab |
| T2, T15 | bounded by a class rule | the hostile paired Skin reads every PRIVATE pixel it gets |
| T6, T8, T14, T18, T24 | bounded | the model refuses them, and the hardware has to hold the press |
| T10, T11, T12 | bounded, with a cost | the Core confirms. The big surface leaves the signing path |
| T7 | closed in the model | a lane needs two presses |
| T16, T23 | open on the chain side | the chain needs a registry and a cap per key |
| T19, T20, T22 | open at the bench | radios and UWB need hardware |

## 5 · What the model does not claim

1. It does not prove that a chip resists a lab. The model holds a flag, `hardened`.
2. It signs with ed25519 as a stand-in for the ML-DSA-87 wallet.
3. The cipher numbers are a sweep. No part is measured.
4. The `SAS` protects only when the user compares the strings.
5. It does not model the chain program that reads a signed input batch. A program that treats a signed tap as authority for value is open to a forged tap. Open issue O6.
