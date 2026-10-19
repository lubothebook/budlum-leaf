# BUDLUM LEAF · HOST POWER · TRUST · 01 · THE THREAT MODEL

**Revision L.6.1 (proposed) · 2026-10-19 · TRUST team**. The rules are in `02-DESIGN-RULES.md`. The gates are in `03-GATE-MAP.md`. The model is `hostauth.py`.

**The question**. A host that feeds the Budlum Leaf must never gain authority over it. This sheet lists how a host can try, and what stops it.

## 1 · The assets

| Asset | Why it matters | Where it lives |
|---|---|---|
| A1 the wallet key and its signatures | a leaked key or a forged signature is a theft of funds | `U7`, never exported |
| A2 the firmware, the slots and the floors | a swapped image is a permanent takeover | `U7`, boot NOR, `fw/boot` |
| A3 the content of the display | a false frame shows a false transaction | `U6`, `U1`, gate SW-22 |
| A4 the trust anchor and the clock | a stale anchor keeps a revoked validator alive | the light client in `U7` |
| A5 the body: heat, volts and the face | a face-worn Budlum Leaf must never burn or shock | `U4`, the NTC comparator, the seat |
| A6 the owner: identity and habits | a host must not track a Leaf or its owner | the sideband, the load profile |
| A7 the power policy itself | the class decides what the bridge draws | `U7` and the bridge |

## 2 · The attacker

A host is not a passive wall. A hostile host is a programmable device with five powers. `[GENERAL]`

1. It sets any voltage and current waveform on the line, inside what its adapter lets through.
2. It sees the current of the Leaf at fine time resolution.
3. It cuts power at any instant, and as often as it likes.
4. It speaks any bytes on the sideband and, if lanes were open, on the data lanes.
5. It can be the only network path of the Leaf, and it can be a validator.

**Out of scope**. A physical attacker with a probe on the `U7` die belongs to the silicon certification. The host can still do fault injection and power analysis from the cable, so those two threats are in scope now. The `fw/u7` README lists them as out of scope. That line changes with host power. `[TREE]`

## 3 · The threats

STRIDE-lite letters: S spoofing, T tampering, R repudiation, I information disclosure, D denial of service, E elevation of privilege. A gate named `HST-T..` is new, and `03-GATE-MAP.md` defines it.

| ID | STRIDE | The attack | The asset | The countermeasure | The gate |
|---|---|---|---|---|---|
| T1 | T, E | data over power, or juice jacking: bytes on the pads or the lanes reach code on the Leaf | A1, A2 | lanes stay high impedance in every class unless the owner allows them. The Leaf runs no host stack and takes one fixed `169` byte frame | ENR-19, MON-16, Z3, Z4, HST-T7 |
| T2 | S | a counterfeit host signs with its own key and asks for class P3, or forges a trusted key | A7 | `U7` verifies ed25519 strict. An unknown key gets P1. The trust store holds only keys that the owner paired | ENR-19, MON-10, RL-14, HST-T2 |
| T3 | S | a counterfeit adapter imitates a port part or a dock | A5, A7 | the pad handshake of ENR-19 refuses it. The pads stay at `0 V`, class P0 | ENR-19, RL-18, MON-10, HST-T1 |
| T4 | E | a host asks for more than its ceiling | A7 | the request is refused to P1. It is not clipped, so the signal is kept | HST-T2 |
| T5 | D, T | voltage and current abuse: over-voltage, reverse volts, a short, a hard inrush | A5, A7 | a window comparator opens `S_SEAT` in `10 µs`. A current limit holds the class power. The ideal diode blocks back-feed. GND mates first | MON-16, ENR-15, ENR-23, HST-T3 |
| T6 | T | fault injection on `U7` by a brownout or a glitch on the host line | A1 | `U7` lives on the island rail. The brownout detector trips before the rail fails. Signing runs isolated and self-verifies before release | HST-T4 |
| T7 | D, R | the host withdraws power in the middle of a signature, a counter commit or an update | A1, A2 | the atomic-commit rule: energy token, burn before use, two-slot NVM, resumable chunks, one flip | SW-14, ENR-13, HST-T5 |
| T8 | S | replay of a HostRecord, captured or pre-signed | A7 | single-use nonce inside the signature. A counter in NVM. An expiry on the anchor height | HST-T2 |
| T9 | S | a relay forwards the handshake of a genuine host while a cheap source supplies the power | A7 | the host signs its measured volts. `U7` compares them with its own ADC. The bridge envelope bounds the harm | HST-T2, HST-T3 |
| T10 | T, D | wireless: a rogue Qi transmitter lies about its loss, or a foreign object heats | A5 | the Leaf sets its own draw. An unauthenticated field gets P1. Qi authentication runs above `5 W`. The NTC comparator is independent | ENR-12, ENR-16, ENR-24, HST-T8 |
| T11 | D, T | vehicle surge: load dump, spikes, a cranking dip | A5, A7 | the vehicle adapter owns the clamp. The Leaf window comparator and the island rail cover the rest | ENR-15, HST-T9 |
| T12 | T | tether snag, or a live contact on a worn Budlum Leaf | A5 | the magnetic seat releases at `6.5 N`. The pads open in `0.8 ms`. The cable side is dead until the Leaf asks | MON-5, MON-16, MON-17, RL-17, HST-T10 |
| T13 | I | power analysis of the wallet signing on the host line | A1 | the signing step runs from the island store with the host switch open. Filtering is not relied on | HST-T6 |
| T14 | E, S | a hostile host that is also a validator claims the role to gain power, or streams false frames | A3, A7 | the role never moves the class. The stream needs SW-22 and the admission of `U7`. Frame roots stay as slashing evidence | SW-22, SW-24, HST-T11 |
| T15 | D, E | the host is the only network path. It starves the anchor, and a rotated-out validator keeps streaming | A3, A4 | the anchor age bound refuses the stream after `6 h`. The Leaf keeps its own radios | HST-T11 |
| T16 | I | the host tracks the Leaf by a wallet address or a stable value in the handshake | A6 | before the host proves itself, `U7` sends one random nonce and nothing else | HST-T12 |
| T17 | E | a paired host is later compromised, or the owner is tricked into pairing | A7 | pairing needs a physical press and a line that names the key and the ceiling. A grant lasts `30 s`. The envelope holds for every class | HST-T13 |

## 4 · The verdict by threat

| Threat | State | The reason |
|---|---|---|
| T1, T3, T4, T8 | closed in the model | a test refuses each one |
| T2, T5, T9, T17 | bounded | the model refuses the forgery, and the hardware envelope bounds the rest |
| T6, T13 | open at the silicon | the model proves the control flow, and the lab proves the leak |
| T7 | closed in the model, open in the code | `fw/u7` has no NVM yet, open issue U7-8 |
| T10, T11, T12 | open at the bench | the numbers need hardware |
| T14, T15 | bounded by a new rule | `fw/u7` has no clock bound today |

## 5 · The three findings that change the existing design

1. **A RAM counter is void**. The host controls power, so it resets every RAM counter. The test `test_the_hole_ram_counters_reopen_replay_after_a_power_cut` shows a replay accepted. The code in `fw/u7` keeps session state in RAM.
2. **The staleness check trusts the checked party**. `session.rs` compares the head that the validator claims with the anchor. A lying validator claims a low head. The light client has no time bound.
3. **The dead-pad law cannot hold at a coil**. A field induces voltage at the receiver whatever the Leaf does. The law has to say that no rail is connected.

## 6 · What the model does not claim

1. It does not prove that a signing core resists a glitch. It proves that a faulty signature does not leave a correct design.
2. It does not prove the numbers of the island rail. The simulation uses assumed parameters.
3. It signs with ed25519 as a stand-in for ML-DSA-87. It proves the control flow only.
4. A double glitch that skips the self-verify releases a bad signature. The test `test_residual_a_double_glitch_releases_a_faulty_signature` shows it. The chain refuses that signature, and the key can still leak. Open issue O3.
