# BUDLUM LEAF · CORE AND SKIN · TRUST · 03 · THE GATE MAP

**Revision L.7 candidate · 2026-10-19 · TRUST seat of block HP-2**. Every rule of `02-DESIGN-RULES.md` maps to a gate that exists, or to a new gate `HC-T..`. A rule with no gate is a defect, as PRG-15 says. `[DECISION]`

**The gates of hostpower**. The `HST-T..` gates are proposals of `hw/hostpower/trust/`. This seat reuses them where the Skin chip or the link repeats a host problem.

## 1 · The rules and their gates

| Rule | The existing gate | What that gate already holds | The gap | The new gate |
|---|---|---|---|---|
| R-P1 two presses | ENR-19, MON-10 | challenge and response before power | a button on a Skin and a Core | HC-T2 |
| R-P2 the SAS | none | none | a relay at pairing | HC-T2 |
| R-P3 record for this Core only | HST-T2 | the HostRecord checks | the SkinRecord checks | HC-T2 |
| R-P4 vendor cert, listed firmware | SW-16, FW-2 | provisioning, older releases refused | a decoder digest list | HC-T2 |
| R-P5 pairing in contact | RL-14, RL-18 | pairing in `4 s`, a keyed seat | pairing over a radio | HC-T2 |
| R-P6 four slots | none | none | slot exhaustion | HC-T9 |
| R-L1 signed transcript | SW-22 | the validator hello is signed | a Skin session | HC-T3 |
| R-L2 suites in the transcript | none | none | a downgrade run | HC-T3 |
| R-L3 suite floors | none | none | a floor test | HC-T3 |
| R-L4 per-slice AEAD | SW-21, DST-12 | the compositor, the handover | the Skin decoder at line rate | HC-T3 |
| R-L5 rekey in one hour | none | none | a long session | HC-T3 |
| R-L6 dead-man, no fallback | none | none | a jamming run | HC-T15 |
| R-L7 a lost link locks the Core | none | none | a lock test | HC-T15 |
| R-R1 revoke by the button | SW-15 | the lost device is revoked | the Skin as a device | HC-T4 |
| R-R2 revoke ends the session | none | none | a latency test | HC-T4 |
| R-R3 commitment on the chain | PRG-9 | the privacy assessment | a registry with no serial | HC-T17 |
| R-R4 counters refuse replay | SW-14 | the anti-rollback counter | a wallet counter for pairings | HC-T4 |
| R-R5 clone alert | none | none | a concurrent clone run | HC-T9 |
| R-R6 the Core enforces | none | none | an offline Skin run | HC-T4 |
| R-M1 per-Core pairing | none | none | a roam run | HC-T11 |
| R-M2 guest has no lane | MON-7 | the microphones exist | a lane gate | HC-T8, HC-T12 |
| R-M3 one active Core | none | none | a switch test | HC-T11 |
| R-M4 the trusted strip | none | none | a paint-over test | HC-T8 |
| R-M5 one account, several keys | SW-15 | the t of n recovery | a cap per key | HC-T16 |
| R-W1 the Core derives the summary | SW-22 | a stream refused outside the set | a summary parser test | HC-T6 |
| R-W2 the press binds to the display | none | none | a display swap test | HC-T6 |
| R-W3 a path that skips the Skin | none | none | a path for each distance | HC-T5, HC-T14 |
| R-W4 a hardware token | none | none | a forgery test on the button | HC-T6 |
| R-W5 the blind budget | none | none | a flood run | HC-T5 |
| R-W6 an input carries no value | SW-17 | the page capability model | a value in a batch | HC-T5 |
| R-W7 a trusted part change locks | Z5, Z6 | measured, gated parts | the display path as a trusted part | HC-T6 |
| R-W8 an image is untrusted | none | none | an address swap run | HC-T12 |
| R-C1 a SECRET never streams | SW-21 | no program runs on the device | a seeded secret run | HC-T7 |
| R-C2 a PIN on the Core path | none | the L.6.0 files hold no unlock factor | an unlock design | HC-T7 |
| R-C3 lock on link loss | none | none | a lock test | HC-T7 |
| R-V1 compute outside the boundary | SW-22 | the stream check | a red team run | HC-T13 |
| R-V2 no handle to the press | none | none | a press mint attempt | HC-T13 |
| R-V3 two keys | SW-16 | keys never leave the secure element | two keys in one Core | HC-T13 |
| R-V4 no shortcut for the owner | SW-22, SW-24 | active set and distance | an own-stream run | HC-T13 |
| R-X1 no authority from distance | none | none | a relay run | HC-T14 |
| R-X2 end to end at C2 | SW-22 | frames from active validators only | a cipher, not only a tag | HC-T15 |
| R-X3 RTT bounds from above | SW-24 | the distance classes | a slack measurement | HC-T15 |
| R-X4 UWB for the room class | SW-24 | the STS commitment | a ghost peak style campaign | HC-T15 |
| R-X5 jamming ends safe | none | none | a jamming run | HC-T15 |

## 2 · The proposed gates

The pass conditions are `[HYPOTHESIS]` until the Program Lead signs them. The owner of every gate is the security line.

| Gate | The test | The pass condition |
|---|---|---|
| **HC-T1** | the stolen Skin | `30` Skins go through decap, probe and glitch work. The lab recovers no identity key, no wallet key and no session key. The frame store is empty `100 ms` after power loss |
| **HC-T2** | the pairing | `100 000` forged, replayed, tampered, cloned and uncertified frames pair nothing above S1. No pairing without two presses and a matching SAS. A relay is caught in every run |
| **HC-T3** | the link | `10^8` tampered, replayed, reflected and reordered slices are accepted `0` times. A downgrade is refused every time. A Skin decoder at `12.3 Gbit/s` adds `50 µs` or less and takes `5 %` of the surface load or less |
| **HC-T4** | the revocation | a revoked session ends in `100 ms` or less. A reconnect, also by a clone, is refused every time. The chain refuses every older record. An offline Skin stays refused by the Core |
| **HC-T5** | the forged tap | `10^6` forged taps and false summaries sign `0` key operations. A tap signs a value only up to the blind budget per day. No batch signs a value |
| **HC-T6** | the trusted display and press | the Core summary equals the parsed transaction in `10^5` of `10^5` cases. Software cannot mint a press. A change of any trusted part locks signing |
| **HC-T7** | the content classes | `10^6` frames with a seeded SECRET carry it `0` times. A viewer Skin gets no PRIVATE pixel. A locked Core shows the lock screen only |
| **HC-T8** | the rogue Core and the guest | an unpinned Core opens `0` sessions. A guest opens no camera or microphone lane without a press on the Skin. The pixel stream cannot paint the trusted strip |
| **HC-T9** | the clone | a concurrent clone raises the alert in every run. A clone against a locked Core sees the lock screen only. Only the button reinstates a key. A fifth pairing is refused |
| **HC-T10** | the Skin identity chip | `10^6` glitches yield `0` faulty attest signatures. The rate limit holds. A Welch t-test of the line current stays under `4.5` in magnitude |
| **HC-T11** | the roam | `1 000` moves of a Skin among `4` Cores carry no capability, end each old session and leave the camera off for a guest |
| **HC-T12** | the camera and the lanes | `10^4` injected images with swapped addresses show the true address on the Core display every time. No lane opens without two presses |
| **HC-T13** | the validator Core | a red team on the validator compute cannot reach the wallet API or mint a press. Its own stream passes SW-22 like any other |
| **HC-T14** | the distance classes | at C1 no value above the budget signs without the confirmation device. At C2 a validator holds no authority. A relay at every class unlocks nothing |
| **HC-T15** | the long link | a rogue base station and a relay read `0` pixels and forge `0` slices at C2. The RTT slack is measured. A UWB distance reduction campaign reports its success rate. A jammed Skin blanks in `100 ms` and the Core locks |
| **HC-T16** | the mixed fleet | a stolen Leaf key drains its cap per day and no more. The root key revokes it by the next block. A capped key adds and revokes no key |
| **HC-T17** | the registry privacy | `1 000` pairings of one Skin to `1 000` wallets give unlinkable commitments. No Skin key or serial appears on the chain |
| **HC-T18** | the owner lock | a stolen Skin cannot be re-paired by a thief without the owner release. The owner can still sell it with a release. The decision is open, issue O7 |

## 3 · The sources the gates name

| Item | The source |
|---|---|
| X25519 | `[PUBLICATION]` RFC 7748, the vectors of Section 6.1 pass in the tests |
| ChaCha20-Poly1305 | `[PUBLICATION]` RFC 8439, the vectors of Sections 2.5.2 and 2.8.2 pass in the tests |
| HKDF | `[PUBLICATION]` RFC 5869, test case 1 passes in the tests |
| the Qi, ML-DSA and leakage sources | see `hw/hostpower/trust/03-GATE-MAP.md` Section 3 |
| distance reduction on HRP UWB | `[PUBLICATION]` Leu, Camurati, Heinrich, Roeschlin, Anliker, Hollick, Capkun, Classen, Ghost Peak, USENIX Security 2022 |
