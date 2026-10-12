# BUDLUM LEAF · THE DIRECTIVE · PART 8 · THE FIRMWARE, AND HOW IT IS BUILT

---

## 8.1 The shape

```
leaf/firmware/
  boot/       the signed image, the A and B slots, the safe screen
  link/       LF-1  the radio set, the path manager, the fail-safe ladder
  stream/     LF-2  the decoder, the panel and tile scheduler, the class set
  surface/    LF-4  the local scene renderer, the input, the labels, the manifest
  authority/  LF-3  the secure element, the session keys, the leases, the records
  tests/      the gate tests, one file per gate id
```

Six crates, one workspace, a fixed function target. **No allocator beyond a static pool, four tasks, no dynamic code loading**. `[DECISION]`

| The resource | The budget |
|---|---|
| The flash image | 4 MB, signed, two slots |
| The working memory | the static pools of Section 8.4, inside the 1 GB of the hub |
| The tasks | `link`, `stream`, `surface`, `authority`, fixed priorities |
| The safe screen | on the panel within 60 ms of power on |

---

## 8.2 The boot chain, step by step

| Step | The time target | What happens | The failure behaviour |
|---|---|---|---|
| 1 | 20 ms | power on, the firmware signature is checked against the secure element | a bad signature boots the B slot; a bad B slot shows the recovery screen |
| 2 | 60 ms | the safe screen is on the panel, drawn by the firmware: the battery state, the wallet surface, the class line | it does not depend on the link, the anchor, the wallet being online or the cassette |
| 3 | 150 ms | the link comes up, the path is chosen, the trust anchor is compared with the stored anchor | a wrong anchor shows a stated state and offers a re-anchor through a second channel |
| 4 | 300 ms | the session is offered: the surface shows the last session or the surface menu | |
| 5 | | a missing cassette, a counterfeit part, an expired lease and a refused operator each produce a **stated visible state**, never a silent success | |

**The rule**. The safe screen is a hardware function of the firmware and the panel. A Leaf is never a brick. `[DECISION]`

---

## 8.3 LF-1 · the link layer

```text
PathCandidate { kind: Wifi|Cell|Mmwave|Satellite|Relay, rtt_ms: u16, up_mbit: u16,
                down_mbit: u16, energy_mw: u16, trusted: bool, operator: Option<OperatorId> }
PathPlan      { primary: PathCandidate, mirrors: [PathCandidate; 2], floor: LocalFloor }
```

**The selection rule, in code-shaped words**.

```text
fn choose(candidates) -> PathPlan:
    let trusted = candidates.filter(|c| c.trusted)
    let usable  = trusted.filter(|c| c.can_carry(class_of(session)))
    let best    = usable.min_by(|c| (c.rtt_ms, c.energy_mw))
    let mirrors = usable.filter(|c| c != best).take(2)
    PathPlan { primary: best, mirrors, floor: LocalFloor::safe_screen() }
```

**The energy policy** is a pure function of the state of charge, the temperature, the class and the user setting. **It never silently downgrades a class**: a change is a visible event on the surface.

| The state of charge | What happens |
|---|---|
| on charge | the challenge answers at the highest tier |
| above 60 percent | the normal tier |
| 20 to 60 percent | the reduced tier, and the session states it |
| below 20 percent | the essential tier: the wallet, the safe screen, the message |
| below 5 percent | the reserve: the safe screen and the optical path only |

---

## 8.4 LF-2 · the stream layer, and the memory proof

```text
FrameClass  = C0Safe | C0bModel | C1Delta | C2Video | C3Still | C4CameraUp
FrameHeader { session, seq: u64, class: FrameClass, bytes: u32, digest: [u8;32],
              operator, model: Option<ModelId>, effort: Option<EffortTier> }
```

```
one 4K frame, 10 bit, 4:2:0               = 12.4 MB
a codec holds 3 to 8 reference frames      = 37 to 100 MB
the decode context, the tile buffers       = 30 to 60 MB
an 8K reserve at four times the frame      = 240 MB
the floor for 4K with headroom             = 384 MB
the shipped value                          = 1 GB, at about 1.5 g and 0.35 W active
```

**The scheduler rules**. The decoder writes only changed regions and addresses the panel at the manifest refresh rate. It never exceeds the panel temperature policy. **A full frame write on a static page is a defect**. `[DECISION]`

**The class fallback chain**. The order is C4 → C3 → C2 → C1 → C0b → C0. A class that a path cannot carry is **refused at start**, never degraded in silence.

---

## 8.5 LF-3 · the authority layer

```text
Wallet ── signs ──▶ SessionGrant { scope, term, energy_policy, operators, classes }
SessionGrant ── derives ──▶ SessionKey { id, expires, scope }
SessionKey ── signs ──▶ the ordinary actions, one at a time

Lease { purpose, model, sensors[], classes[], expiry, retention, subject }

ComponentRecord { part_class, part_id, origin, measures, history, signatures, reference }
```

| The transaction class | The example | The path |
|---|---|---|
| local | the input echo, the cursor, the safe screen | the firmware, no signature |
| session | a message, a payment inside the grant | the session key, one signature over the intent |
| high value | a new operator, a new module, a part change, a revocation | the wallet, and a second authority when a module is present |

`[TREE]` ML-DSA-87 uses a 2 592 byte public key and a 4 627 byte signature. Therefore the device signs once per session and never once per tap.

**The set change rule**. A validator set change needs a new out-of-band anchor. The device stores one anchor (checkpoint height, block hash, validator set hash) and refuses network-only set changes. `[TREE]`

---

## 8.6 LF-4 · the surface layer

### 8.6.1 The local scene renderer

```text
SceneModel { version: u64, glyphs: GlyphCache, ops: [Op], palette: Palette,
             images: [ImageRef], signature: [u8;64] }
Op = Rect | Text | Path | Image | Blend
```

| The rule | The reason |
|---|---|
| the renderer draws only a signed model | no local computation is shown as a verified result |
| it cannot label a document, a lease or an inference | the labels belong to the panel layer |
| a model that fails its signature is refused, and the last good model stays on the surface | a silent blank is forbidden |
| it reports the drawn version to the session | the operator knows what the user sees |
| the parts: a glyph cache, a vector fill, an alpha blend, an image blit, a colour engine | about 2 mm² of logic and 2 MB of cache |

### 8.6.2 The reprojection unit

```text
Reprojection { frame: FrameHandle, motion: Motion, mode: Shift|Scale|Rotate, max_ms: 40 }
```

Rules. It runs only on the last decoded frame and stops when artefacts pass the threshold. It never runs across a scene cut, and the session marks the cuts.

### 8.6.3 The four labels of the panel layer

The evidence label of a mixed surface, the class line, the battery and energy state, and the camera state. **A page cannot cover a label**, and a page that tries is refused and recorded. `[DECISION]`

### 8.6.4 The input map

| The input | The path | The latency |
|---|---|---|
| touch and pen | the mesh layer, the hub, the local echo | 3 to 8 ms |
| proximity and gesture | the mesh and a ranging radio | 10 to 20 ms |
| gaze | a sensor under a lease, or the eye region in the Field mode | stated per case |
| voice | the module microphone array, masked on the device, then the intent | stated |
| the wallet | the secure element, one action | local |

---

## 8.7 The refusal set

| No. | The case | The behaviour |
|---|---|---|
| R1 | a model that is not the leased model | refuse, keep the last good model, record |
| R2 | a purpose mismatch | refuse, show the purpose, record |
| R3 | an expired lease | refuse, offer a renewal with one action |
| R4 | a sensor the lease does not name | refuse, the hardware light stays off |
| R5 | a part with a bad record | refuse the part, show the failing field |
| R6 | a path whose operator fails the trust test | never use, and say why on the class line |
| R7 | a class the path cannot carry | refuse at start, never degrade in silence |
| R8 | an unsigned or a badly signed scene model | refuse, keep the last good model, record |
| R9 | a pressure to read without a grant | refuse, with no override `[TREE]` |
| R10 | a page that tries to cover a label | refuse the cover, draw the label, record |

---

## 8.8 How the firmware is built: the work order

| Step | The package | The dependency | The gate |
|---|---|---|---|
| 1 | the workspace, the pool allocator, the four tasks, the record format | none | the build and the style checks |
| 2 | LF-3 the key chain against a bench secure element | 1 | SW-6 on a bench |
| 3 | LF-4 the scene renderer and the labels | 1 | DST-1, SW-11 on a bench |
| 4 | LF-2 the decoder and the scheduler against a recorded stream | 1 | SW-3 on a bench |
| 5 | LF-1 the path manager against a link emulator | 1, 2 | SW-1, SW-8, SW-9 |
| 6 | the boot chain, the A and B slots, the safe screen | 1 to 5 | the boot matrix, R1 to R5 |
| 7 | the camera path, the sentinel contract, the lease | 2, 4 | CAM-2 to CAM-5 |
| 8 | the mode and the manifest, the Field mode | 3, 4 | DSP-9, FLD-5, FLD-6 |

**The coding rules**. One work package, one branch, the test written with the code, no merge without a gate. A surface counts as existing only when it is wired from the module root and covered by a gate. The `src/sdk/` precedent is the standing warning. `[DECISION]`

---

## 8.9 The firmware gates

| Gate | The test | The pass condition |
|---|---|---|
| SW-1 | the Leaf node profile in a device class emulator | answers inside the challenge period and follows the battery table |
| SW-2 | the finality budget on the secure element | inside the stated time, energy and storage |
| SW-3 | the frame classes over an impaired link | every class inside its budget, an undecodable class refused at start |
| SW-4 | a lease, its four refusals, a revocation | all six behave as specified, with the times measured |
| SW-5 | a handoff, clean and unplanned | no stuck screen, no lost state, the token rules hold |
| SW-6 | the signature budget and the wallet path | the bytes and the times match the table, per action |
