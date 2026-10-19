# BUDLUM LEAF · HOST POWER · TRUST · 03 · THE GATE MAP

**Revision L.6.1 (proposed) · 2026-10-19 · TRUST team**. Every rule of `02-DESIGN-RULES.md` maps to a gate that exists, or to a new gate `HST-T..`. A rule with no gate is a defect, as PRG-15 says. `[DECISION]`

**The numbering**. Other hostpower teams propose gates named `HST-..`. The Program Lead renumbers. The trust gates carry the letter T to avoid a clash.

## 1 · The rules and their gates

| Rule | The existing gate | What that gate already holds | The gap | The new gate |
|---|---|---|---|---|
| R-I1 island fed by the bridge only | none | no gate names the supply of `U7` | a host rail feeds `U7` today in the Bare tier | HST-T3, HST-T4 |
| R-I2 store, regulator and detector | ENR-13 | the `180 mF` holdover buffers of the body | the island store is in the ring, and it is smaller | HST-T3 |
| R-I3 reset until the rail holds | none | the boot model starts at `U4` ROM up | the reset condition has no test | HST-T4 |
| R-I4 cell feeds the always-on LDO | none | `hw/energy/03` Section 1.2 states the LDO from the B cell | no gate tests it, and the Bare tier has no cell | HST-T4 |
| R-D1 two switches in series | ENR-19, MON-16 | the seat switch and its `1 MΩ` leak | the host-side adapter switch | HST-T1 |
| R-D2 only Budlum adapters | RL-14, RL-18, MON-10 | identity and the keyed seat | a bare host contact on a pad | HST-T1 |
| R-D3 P0 until the pad handshake | ENR-19, MON-16 | `0 V` until `3 ms` auth, `<1 µA` leak | a counterfeit adapter at any input volts | HST-T1 |
| R-D4 P1 only, lanes dead | ENR-19 | the order of the handshake | the power-only low class has no row | HST-T7 |
| R-D5 the sink requests the contract | ENR-15 | the `USB-C` protection | a source that offers more than the contract | HST-T3 |
| R-D6 analog envelope | MON-16, ENR-15, ENR-23 | arcs, leakage and cell fuses | the window comparator and the surge | HST-T3 |
| R-D7 wireless: rectifier isolated | ENR-12, ENR-16, ENR-24 | Qi2.2 and the `36.2 °C` comparator | a rogue transmitter with false reports | HST-T8 |
| R-D8 node vouch, P2 at most | ENR-12 | the `3 ms` answer carries the node hash | the vouch format and the ceiling | HST-T2 |
| R-H1 single-use nonce, nothing else | none | no host challenge exists | the pre-grant frame content | HST-T12 |
| R-H2 ed25519 strict | SW-22 | the same primitive for a validator hello | the same check for a host | HST-T2 |
| R-H3 counter in NVM | SW-14, FW-2 | the anti-rollback counter for releases | a counter per host key | HST-T2, HST-T5 |
| R-H4 expiry on the anchor, age bound | SW-22 | the active set | no time bound exists in the light client | HST-T11 |
| R-H5 over-class refused | none | none | a refusal test | HST-T2 |
| R-H6 record inside its class row | none | none | a row test | HST-T2 |
| R-H7 power channel binding | none | none | a relay test | HST-T2 |
| R-H8 owner pairing | SW-15, SW-16 | recovery and provisioning in the secure element | a physical press for a host key | HST-T13 |
| R-H9 lanes need four conditions | ENR-19 | lanes start after the handshake | a per-class lane test | HST-T7 |
| R-V1 render after SW-22 only | SW-22 | a key outside the active set gets the safe screen | the role claim as an attack | HST-T11 |
| R-V2 role never moves the class | none | none | a role test | HST-T2 |
| R-V3 fresh anchor for the stream | SW-22, SW-24 | the active set and the distance class | the stale anchor | HST-T11 |
| R-V4 never the only path | DST-12 | handover between validators | a host as the only path | HST-T11 |
| R-A1 energy token | SW-14 | no brick in `1 000` forced failures | the energy to start a step | HST-T5 |
| R-A2 isolated signing | none | none | the host switch during a signature | HST-T4, HST-T6 |
| R-A3 burn before use | SW-22 | a single-use challenge | a counter across a power cut | HST-T5 |
| R-A4 self-verify before release | none | none | a faulty signature test | HST-T4 |
| R-A5 fault count and lockout | none | none | a lockout test | HST-T4 |
| R-A6 two-slot NVM | SW-14, FW-2 | slots A and B, the counter | a cut at every NVM step | HST-T5 |
| R-A7 chunked resumable update | SW-14, FW-1 | rollback and a bit-flip test | a cut at every chunk | HST-T5 |
| R-A8 one flip after a clean trial | FW-2, FW-3 | replay of old releases, revocation | a cut during the flip | HST-T5 |
| R-A9 trial limit of `3` | SW-14 | one-action rollback | a hostile host that cuts every trial | HST-T5 |
| R-A10 pairing in NVM | SW-15 | the wallet recovery flow | a cut during pairing | HST-T5, HST-T13 |
| R-S1 sign with the host switch open | none | none | the line current during a signature | HST-T6 |
| R-S2 filtering is not relied on | none | none | the leakage figure | HST-T6 |
| R-S3 padded recharge | none | none | the recharge pattern | HST-T6 |

## 2 · The proposed gates

The pass conditions are `[HYPOTHESIS]` until the Program Lead signs them. The owner of every gate is the security line.

| Gate | The test | The pass condition |
|---|---|---|
| **HST-T1** | the dead host pads | a host emulator sweeps `0` to `36 V` and `10 000` counterfeit adapters attach. Every Leaf pad and the island stay at `0 V` until the pad handshake passes. Leakage stays under `1 µA` |
| **HST-T2** | the HostRecord | `100 000` frames: unknown key, forged signature, tampered class, replay, expired, over-class, bad binding, bad vouch. Zero grants above P1. A valid record grants in `5 ms` or less from the challenge |
| **HST-T3** | the bridge envelope | steps from `0` to `36 V`, a `60 V` surge of `1 ms`, a short, an inrush. `S_SEAT` opens in `10 µs` outside the class window. The island stays at `1.80 V` within `5 %`. No part degrades after `1 000` surges |
| **HST-T4** | the glitch campaign | `10^6` glitches on the host side and `10^6` on the bridge input, during signing. Zero faulty signatures leave `U7`. Every fault is counted. The lab report names the glitch window |
| **HST-T5** | the atomic commit | `10 000` power cuts at random instants in a signing, a counter commit, a pairing and a full update. Each ends in the old or the new state. No counter is reused. No brick. The update resumes |
| **HST-T6** | the line leakage | a Welch t-test on the host line current over `10^6` ML-DSA-87 signatures, fixed against random message. The value stays under `4.5` in magnitude, and the recharge duration is padded |
| **HST-T7** | the data lanes | L0 and L1 stay high impedance in every class and every refused case. A `72 h` fuzz run on the adapter port puts nothing on `U7` or `U6` except the `169` byte frame. No parser fault in `10^8` frames |
| **HST-T8** | wireless abuse | a rogue Qi transmitter with false loss reports and a metal object at `25 W`. Every face point stays at or under `36.2 °C`. Without authentication, the draw never passes P1 |
| **HST-T9** | the vehicle surge | ISO 7637-2 pulses, an ISO 16750-2 load dump and a cranking dip through the vehicle adapter. No grant above class. No `U7` fault. No wallet state lost. The session returns after the dip |
| **HST-T10** | the breakaway | a pull test at the cable in six directions. Separation at `6.5 N` or less. The pads open in `0.8 ms`. No contact on the cable side holds more than `5 V` after separation |
| **HST-T11** | the stale clock and the eclipse | the host is the only path for `6 h`. The Leaf refuses the stream at the anchor age limit and shows the safe screen. A rotated-out validator never streams past the limit |
| **HST-T12** | the privacy of the handshake | a capture of every frame before the grant, over `1 000` attaches. It shows random nonces and the adapter role only. No wallet address and no value that repeats per Leaf |
| **HST-T13** | the pairing | `1 000` attempts to add a key by data alone add zero entries. One press removes a key. The safe screen names the key and its ceiling |

## 3 · The standards the gates name

| Item | The source |
|---|---|
| the Qi authentication above `5 W`, ECDSA P-256 and X.509 | `[PUBLICATION]` Wireless Power Consortium Qi 1.3, published as IEC 63563-9 |
| the expected `3.85` signing-loop repetitions of ML-DSA-87 | `[PUBLICATION]` NIST FIPS 204, Table 1 |
| the leakage test, a Welch t-test with a threshold of `4.5` | `[PUBLICATION]` Goodwill, Jun, Jaffe, Rohatgi, NIST Non-Invasive Attack Testing Workshop, 2011 |
| vehicle supply pulses and load dump | `[PUBLICATION]` ISO 7637-2 and ISO 16750-2, named without their limits |

The Qi authentication proves the maker of a transmitter. It does not prove that the owner trusts it. `[PUBLICATION]` The vouch row R3 caps such a source at P2.
