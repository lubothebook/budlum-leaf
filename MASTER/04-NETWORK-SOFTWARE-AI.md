# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME IV · NETWORK, SOFTWARE, SECURITY AND AI

**Version:** 4.0 · 2026-10-05 · part of `MASTER/00-INDEX.md`
**Scope**. Device firmware, network execution, session management, wallet authorization, AI permissions and system defence.

---

## 1 · The split

| Where | What runs | The artefact |
|---|---|---|
| **On the Leaf** | Leaf Firmware: the link, the stream, the wallet and the surface | `leaf/firmware/` (new), a fixed function image, no user code |
| **On the validator** | Budlum OS and the session host: the page engine, the model, the game, the encoder | the Budlum tree as it stands `[TREE]` |
| **In B.U.D**. | the user data, the session state, the manifests, the records | `bud/`, Pollen, the storage module `[TREE]` |
| **In the wallet authority** | the authorization, the session key chain, the leases | `crates/wallet-core`, `src/account_abstraction/` `[TREE]` |

**Rule**. The Leaf holds no user code and no user data as the only copy. A Leaf that can run a program that the network did not sign is a defect. `[DECISION]`

---

## 2 · Leaf Firmware

### 2.1 The four layers

| Layer | Function | The interface |
|---|---|---|
| **LF-1 link** | the radio set, the path choice, the relay and the traversal, the fail-safe ladder | RG-1 and RG-10 |
| **LF-2 stream** | the decoder, the tile scheduler, the frame classes C0 to C3, the panel calibration | RG-3 |
| **LF-3 authority** | the secure element, the session keys, the approvals, the leases, the component records | RG-6, RG-7, RG-8, RG-13 |
| **LF-4 surface** | the safe screen, the input, the evidence labels, the format change | RG-14, RG-16 |

### 2.2 The resources, with the memory proof

A Leaf has no operating system and no general processor. It has fixed function silicon, one hub and one memory. The memory is the item that a person questions, so it is proved here.

```
One 4K frame, 10 bit, 4:2:0           = 3 840 × 2 160 × 1.5 bytes  = 12.4 MB
A modern codec holds 3 to 8 reference frames                        = 37 to 100 MB
The decode context, the tile buffers, the colour pipeline          = 30 to 60 MB
Reserve for an 8K stream later, at four times the frame            = 240 MB
                                    ------------------------------------
The floor for 4K with headroom                                 = 384 MB
The comfortable value                                          = 1 GB
```

| Part | Value |
|---|---|
| Firmware image | 4 MB flash, signed, A and B slots |
| Working memory | 1 GB of low power double data rate memory, die stacked on the hub |
| The mass of the memory | about 1.5 g |
| The power of the memory | 0.35 W active, 0.05 W in a page refresh |
| The refusal | the memory is a decode buffer, not a user space, and no user code is loaded into it. `[DECISION]` |

### 2.3 The boot and the state machine

| Step | Time target | The state |
|---|---|---|
| 1 | 20 ms | power on, the firmware signature check against the secure element |
| 2 | 60 ms | the safe screen is on the panel, drawn from the firmware, with the battery state and the wallet surface |
| 3 | 150 ms | the link comes up, the path is chosen, the anchor is checked against the stored anchor |
| 4 | 300 ms | the session is offered; the surface shows the last session or the surface menu |
| 5 | | a wrong anchor, a missing cassette, a counterfeit part and a refused operator each produce a stated visible state, never a silent success |

**The rule**. The safe screen is a hardware function of the firmware and the panel. It does not depend on the link, on the anchor, on the wallet being online or on the cassette being present. It is rule H11 of the directive, and it is the reason a Leaf is never a brick. `[DECISION]`

---

## 3 · The session

### 3.1 The objects

| Object | The content | Who signs | Where it lives |
|---|---|---|---|
| The session | id, the user authority, the class set, the decoder profile, the effort tier, the energy policy, the deadline, the counter | the wallet authority | B.U.D. under the user authority, the device holds a hash |
| The binding | the operator, the term, the notice period | the operator and the user | B.U.D. |
| The resume token | single use, short lived, one named operator | the user authority | the wire only |
| The lease | the purpose, the model, the sensor, the frame classes, the expiry, the retention | the user authority | B.U.D., and the operator holds a reference |
| The record | the part, the measures, the history, the signatures | the part and the wallet | B.U.D. |

### 3.2 The flow of one delta frame

```
user input            ->  the device encrypts and sends the intent, duplicated on two paths when the link is unstable
the operator renders  ->  the delta is computed against the acknowledged state, the sequence number is monotonic
the wire              ->  the delta frames, class C1, with the session id and the class
the device            ->  the hub decodes, the tile scheduler writes the changed region, the panel shows it
the local floor       ->  the echo of the touch, the cursor and the wallet never wait for the network
```

### 3.3 The operator choice

1. **Trust first**. An operator that fails a bond, a stake or a record test is out, whatever its latency.
2. **Latency second**. Order the candidates by the measured round trip, then by the class they can serve.
3. **Cost third, and it is deferred**. Sessions are metered in effort-tier milliseconds and class bytes, with pricing deferred.
4. **Siting matters**. Validators within 200 km keep RTT under 10 ms. Edge nodes at 10 to 15 km deliver 1 to 5 ms. `[PUBLICATION]` The product states the class of a market, never a promise of a class.
5. **The change**. A departing validator is replaced via a resume token, state hash and grace period without blanking the screen. RG-4.

---

## 4 · The wallet, the keys and the signature budget

1. ML-DSA-87: a public key of 2 592 bytes and a signature of 4 627 bytes. `[TREE]` Every design choice follows from these two numbers.
2. The wallet authority signs once per session, not once per tap. The chain runs: wallet → session grant → scoped session key → ordinary actions. RG-8.
3. A t of n authorization is t separate signatures, verified one by one. `[TREE]` A Leaf with a module and a battery sheet holds three authorities, and high-value actions require two.
4. The relayer carries an intent and holds no key. `[TREE]` The device never signs on behalf of the relayer and the relayer never signs on behalf of the device.
5. The optical path carries a signed receipt with no radio via the note packing crate. RG-12.
6. A lost module is revoked with one wallet action, visible across the network within one challenge period. RG-13.

---

## 5 · What the AI can do

1. **Lubot is the assistant of the family**. It reads and answers. It does not generate and it does not act without a grant. `[TREE]` The rule stays.
2. **The device masks first**. Secrets are masked on the device before a question leaves it, matching the tree's reading assistant. `[TREE]`
3. **The camera works only under a lease**. The base Frame has no camera. A Leaf with a camera module shows a hardware state, and a read without a lease is refused. RG-5.
4. **The effort tier is a promise about hardware**. An operator advertises the depth that its hardware serves. A request above it is refused, not answered cheaply, and the device renders the refusal as a refusal. `[TREE]` RG-9.
5. **Every read is recorded and every read costs**. The record is a B.U.D. object under the user authority, readable by the user at any time.
6. **The refusal set is a feature**. Four visible refusals cover wrong model, wrong purpose, expired lease, and unnamed sensor.

---

## 6 · The security model

| Threat | The mechanism | The mitigation | The test |
|---|---|---|---|
| A fake operator answers the session | the anchor, the finality certificate and the bond | trust first, the bond, the slash, the record | SW-2 |
| A replay of a session message | the monotonic counter and the session id | the counter, and the refusal of a stale frame | SW-5 |
| The theft of a session | the resume token and the binding | single use, short life, one named operator | SW-5 |
| The theft of a module | the part anchor and the wallet revocation | one action revokes, the network sees it | SW-7 |
| A counterfeit cassette | the secure element in the cassette and the record | the device refuses a part with no matching record | SW-7 |
| A counterfeit cell inside a genuine shell | the record carries the measures, and the gauge checks them | a capacity disagreement beyond the tolerance refuses the cassette | ENR-3 |
| An eavesdropper on the link | the transport encryption and the delta | the end to end rule, the key per session | SW-3 |
| A malicious page | the class set, the evidence labels and the local floor | a page cannot paint the local floor and cannot cover a label | SW-11 |
| A camera abuse | the lease and the hardware indicator | four refusals, a light that software cannot paint | SW-4 |
| A side channel on the secure element | the fixed function firmware and the energy policy | a stated measurement, and a constant time path for the wallet | SW-6 |
| A supply chain part that lies | the component record and the calibration data | a part that fails the record test is refused | SW-7 |
| The loss of the network entirely | the fail-safe ladder | the safe screen, the wallet, the echo, and the optical path | MEC-9 of the link gate set |

**The invariants that this program does not break**.

1. No administrator can read a user's data. Pollen refuses a read without a grant, with no override. `[TREE]`
2. The wallet is never a key custody service. `[TREE]`
3. The core has no admin whitelist. `[TREE]`
4. An island that fails stays isolated. `[TREE]`
5. No plaintext leaves an evidence surface. `[TREE]`
6. A surface counts as existing only when it is wired from the module root and covered by a gate. The `src/sdk/` precedent is the reason. `[TREE]`

---

## 7 · The bridge between the two worlds

The Leaf is a thin client, and a thin client is only as good as the contract. The contract has five clauses. `[DECISION]`

| Clause | The promise | The proof |
|---|---|---|
| The class promise | the link states the class it can carry, and the session adapts in the open | the class is visible on the surface |
| The state promise | the session state lives in B.U.D., so the provider, the operator and the surface can change | RG-4 |
| The consent promise | no read without a grant, no sensor without a lease, no model without a declaration | RG-5, Pollen |
| The energy promise | the surface states the term that costs the energy, and the user chooses the class | RG-9 |
| The honesty promise | the product states the class of a market and the case at the limits, never a superlative | the claim policy of Volume V |

---

## 8 · The software gates

| Gate | The test | The pass condition |
|---|---|---|
| SW-1 | the Leaf node profile in a device class emulator | answers inside the challenge period, and follows the battery state table |
| SW-2 | the finality budget on the chosen secure element | inside the stated time, energy and storage |
| SW-3 | the frame classes over an impaired link | every class meets its budget, and an undecodable class is refused at start |
| SW-4 | a lease, its four refusals and a revocation | all six behave as specified, with the times measured |
| SW-5 | a handoff, clean and unplanned | no stuck screen, no lost state, the token rules hold |
| SW-6 | the signature budget and the wallet path | the bytes and the times match the table, per action |
| SW-7 | a component record and a part refusal | the device refuses a mismatched part and shows the reason |
| SW-8 | the reverse battery policy over 24 h | the class follows the state in all five cases |
| SW-9 | a challenge answer on charge and off charge | the energy in joules, and the earned credit |
| SW-10 | a relay path behind a carrier address translation, with a path change | the intent settles and the path is in the record |
| SW-11 | a page with mixed evidence, and a page that covers a label | the labels render, the cover attempt fails |
| SW-12 | an optical receipt with no radio | the reader verifies the receipt; the frame count and the time are in the record |
| SW-13 | a telemetry read with and without a grant | the granted read succeeds, the ungranted read is refused and logged |

**The rule for every gate**. A gate needs raw data, an instrument and a calibration date. A result without data is an opinion. `[DECISION]`
