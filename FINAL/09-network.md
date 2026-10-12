# BUDLUM LEAF · THE DIRECTIVE · PART 9 · THE NETWORK AND THE BUDLUM INTEGRATION

---

## 9.1 The split of work

| Where | What runs | The artefact |
|---|---|---|
| **On the Leaf** | the Leaf Firmware: the link, the stream, the wallet and the surface | `leaf/firmware/`, a fixed function image, no user code |
| **On the validator** | Budlum OS and the session host: the page engine, the model, the game, the encoder | the Budlum tree as it stands `[TREE]` |
| **In B.U.D**. | the user data, the session state, the manifests, the records | `bud/`, Pollen, the storage module `[TREE]` |
| **In the wallet authority** | the authorization, the session key chain, the leases | `crates/wallet-core`, `src/account_abstraction/` `[TREE]` |

---

## 9.2 The Budlum tree, as the program reads it

| The artefact | What it gives the Leaf | The state |
|---|---|---|
| `src/network/mobile.rs` | a phone node profile: battery aware challenge policy, NAT traversal, self-hosted serving, stateless sync | the Leaf extends it, it does not replace it |
| `src/light_client/mod.rs` | one trust anchor, a finality certificate, a post-quantum blob, a sync plan | the device is a light client with a wallet |
| `crates/wallet-core` | BIP39, ML-DSA-87, the seed rule, the wallet and relayer separation | the authority layer |
| `crates/note-packing` | one definition of a note field element | called, never re-derived |
| `src/relayer/` | the signed intent, the solver bid, the policy envelope, the settlement status | the reachability path |
| `src/gateway/passport.rs`, `atlas` | the identity surface, the evidence cards, the Pollen summary | the identity and evidence layer |
| `crates/budscan` | the browser with the classification rule and the four fetchers | the window of the device |
| `src/pollen/` | the consent rule, the content gate, the strict refusal | the read path |
| `src/account_abstraction/threshold_mldsa.rs` | a t of n multisig authorization | the high value path |
| `src/ai_inference/effort.rs` | the effort tiers | the promise about hardware |
| `bud/` | the lossless container | the archive |
| The constitution | the six invariants | the boundary of every Leaf change |

**The invariants that no Leaf change bends**. `[TREE]` No read without a Pollen grant; no governance override; no administrator whitelist; island isolation; no private key custody; no plaintext on an evidence surface.

---

## 9.3 The session, and its objects

| The object | The content | Who signs | Where it lives |
|---|---|---|---|
| The session | id, the user authority, the class set, the decoder profile, the effort tier, the energy policy, the deadline, the counter | the wallet authority | B.U.D. under the user authority; the device holds a hash |
| The binding | the operator, the term, the notice period | the operator and the user | B.U.D. |
| The resume token | single use, short lived, one named operator | the user authority | the wire only |
| The lease | the purpose, the model, the sensors, the classes, the expiry, the retention | the user authority | B.U.D., the operator holds a reference |
| The job | the deadline class, the checkpoint, the mobility rule | the session key | B.U.D. |
| The record | the part, the measures, the history, the signatures | the part and the wallet | B.U.D. |

**The flow of one delta frame**.

```
input            -> the device encrypts and sends the intent, duplicated on two paths when the link is unstable
the operator     -> renders the delta against the acknowledged state, with a monotonic sequence number
the wire         -> the delta frames at class C1, with the session id and the class
the device       -> the hub decodes, the scheduler writes the changed region, the panel shows it
the local floor  -> the echo of the touch, the cursor and the wallet never wait for the network
```

**The operator choice**. Trust comes first, latency second, and cost third (cost is deferred; units are effort-tier milliseconds and class bytes). A validator within 200 km keeps the round trip under 10 ms; an edge node 10 to 15 km away delivers 1 to 5 ms. `[PUBLICATION]`

---

## 9.4 The wallet, the keys and the signature budget

1. The wallet signs once per session, not once per tap.
2. The chain runs: wallet → session grant → scoped session key → ordinary actions.
3. A t of n authorization is t separate verifications, one by one. `[TREE]`
4. A Leaf with a module and a battery sheet holds three authorities. A high-value action requires two of them.
5. The relayer carries an intent and holds no key. Neither side ever signs for the other.
6. The optical path carries a signed receipt with no radio. The note packing crate is **called, never re-derived**.
7. A lost module is revoked with one wallet action, and the network sees it inside one challenge period.

---

## 9.5 What the AI can do

1. **Lubot is the family assistant**. It reads and answers, and it never acts without a grant. `[TREE]`
2. **The device masks first**. A secret is masked on the device before a question leaves it.
3. **The camera works only under a lease**, and the sensor state is a hardware light.
4. **The effort tier is a hardware promise**. A request above the advertised tier is refused, and the device shows the refusal.
5. **Every read is recorded and every read costs**; the record is a B.U.D. object under the user authority, readable by the user at any time.
6. **The four refusals are a feature**. They cover model mismatch, purpose mismatch, expired lease, and unnamed sensor.

---

## 9.6 The research orders RG-1 to RG-17, with the acceptance test of each

| No. | The order | The acceptance test |
|---|---|---|
| RG-1 | the Leaf node profile beside Mobile Self, with a battery and challenge table and the joule cost of an answer | the profile answers inside the challenge period at every battery state, and the energy per answer is measured |
| RG-2 | the finality budget on two candidate secure elements: the BLS aggregate and the post-quantum blob | the time, the energy and the storage are measured, and the out-of-band anchor rule is written |
| RG-3 | the display transport: C0 safe, C1 delta, C2 video, C3 still, plus the new C0b model class | each class is measured on an impaired link, and a class is refused at start when the path cannot carry it |
| RG-4 | the session object, the single use resume token, the grace period and the failure set | a clean and an unplanned handoff both pass, with no stuck frame |
| RG-5 | the perception lease: the object, a short default, one action revocation, the declaration trail, four fail-closed cases | all six cases behave as specified, and the hardware sensor state is proven |
| RG-6 | the component record fields: class, identity, origin, measures, history, signatures, reference | a part is accepted, refused and revoked, each with the field that decided |
| RG-7 | the transport byte budget per action: a payment, a message, a lease, an inference request | the bytes are measured, and the optical frame count is computed from them |
| RG-8 | the wallet to session grant to session key chain, with one action revocation | the chain is proven on a bench, and a revocation takes one action |
| RG-9 | the reverse battery policy: the class follows the cell state, never a silent downgrade | the five states of Section 8.3 are proven over 24 hours |
| RG-10 | the relayer reachability and the fee plan behind a carrier address translation | an intent settles, and the path is in the record |
| RG-11 | can the device serve storage honestly, and what the shard rule is | the measurement, and the honest answer either way |
| RG-12 | the optical transfer must call the note packing crate | the packing is called, and a second implementation is refused at review |
| RG-13 | the part anchor and the lost module revocation | one action revokes, and the network sees it inside one challenge period |
| RG-14 | the Budscan render target: the split, the verifier as a light client, the page class, the visible class statement | a page renders at the class it declares, and the verifier is the light client |
| RG-15 | the telemetry schema: six groups, under the Pollen rules | a granted read succeeds, an ungranted read is refused and logged |
| RG-16 | the evidence label drawn by the panel, which a page cannot cover | the cover attempt fails, and the label renders on every page class |
| RG-17 | one term one meaning, and the stub rule | the term list is enforced, and a stub surface is refused at review |

---

## 9.7 The delegation boundary

| The device keeps | The network takes |
|---|---|
| the panel scan out and the timing controller | the page engine and the layout |
| the hardware decoder | the heavy compute and the models |
| the secure element and the wallet authority | the consensus and the settlement |
| the radios | the storage and the shard duty |
| the safe screen and the local floor | the consent path, through Pollen |
| the local scene renderer and the reprojection | the browser engine, through Budscan |
| the manifest and the labels | the identity and the evidence surface |

**The rule**. A duty that crosses the line is a defect, and the review says which line it crossed. `[DECISION]`

---

## 9.8 The network gates

| Gate | The test | The pass condition |
|---|---|---|
| SW-7 | a component record and a part refusal | the device refuses a mismatched part and shows the reason |
| SW-8 | the reverse battery policy over 24 hours | the class follows the state in all five cases |
| SW-9 | a challenge answer on charge and off charge | the energy in joules, and the earned credit |
| SW-10 | a relay path behind a carrier address translation, with a path change | the intent settles and the path is in the record |
| SW-11 | a page with mixed evidence, and a page that covers a label | the labels render, the cover attempt fails |
| SW-12 | an optical receipt with no radio | the reader verifies the receipt; the frame count and the time are in the record |
| SW-13 | a telemetry read with and without a grant | the granted read succeeds, the ungranted read is refused and logged |
