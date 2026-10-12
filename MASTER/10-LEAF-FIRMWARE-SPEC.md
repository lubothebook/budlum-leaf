# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME X · THE LEAF FIRMWARE SPECIFICATION

**Version:** 4.2 (revision D) · part of `MASTER/00-INDEX.md`
**Purpose:** the document that a coding AI implements. It defines the four layers, every interface, every state, every refusal and every test hook. It contains no application code: a code fragment here is an **interface specification**, and it is marked.

**Rule L1**. No implementation starts before this volume is accepted. A surface counts as existing only when it is wired from the module root and covered by a gate. `[TREE]` the `src/sdk/` precedent.

---

## 1 · The shape of the firmware

```
leaf/firmware/
  boot/       the signed image, the A and B slots, the safe screen
  link/       LF-1  the radio set, the path manager, the fail-safe ladder
  stream/     LF-2  the decoder, the tile and panel scheduler, the class set
  surface/    LF-4  the local scene renderer, the input, the labels, the manifest
  authority/  LF-3  the secure element, the session keys, the leases, the records
  tests/      the gate tests, one file per gate id
```

Six crates, one workspace, a fixed function target. The firmware has no allocator beyond a static pool, no threads beyond four fixed tasks, and no dynamic code loading. `[DECISION]`

| The resource | The budget |
|---|---|
| The flash image | 4 MB, signed, two slots |
| The working memory | the fixed pools of Section 2.3, inside the 1 GB of the hub |
| The tasks | `link`, `stream`, `surface`, `authority`, with fixed priorities |
| The latency classes | the safe screen is allowed 60 ms from power on |

---

## 2 · LF-1 · The link

### 2.1 The objects

```text
PathCandidate { kind: Wifi|Cell|Mmwave|Satellite|Relay, rtt_ms: u16, up_mbit: u16,
                down_mbit: u16, energy_mw: u16, trusted: bool, operator: Option<OperatorId> }

PathPlan      { primary: PathCandidate, mirrors: [PathCandidate; 2], floor: LocalFloor }
```

`[INTERFACE SPECIFICATION]` A path plan is chosen by three rules, in this order: **trust, then latency, then energy**. The device never sends an intent over a path whose operator fails the trust test, whatever its latency.

### 2.2 The fail-safe ladder

| The state | The trigger | The behaviour |
|---|---|---|
| Full | a path above the class of the session | the session runs at its class |
| Reduced | the measured round trip above the class for 1 s | the class drops by one step, and the surface shows the class line |
| Cellular | the local path lost | the session moves, the class is restated |
| Satellite | everything else lost | the message class only |
| No link | no path | the local floor and the safe screen |
| Optical | a link is refused by the user or by the lease | the optical path of RG-12 |

### 2.3 The energy policy

The battery state table of RG-1 runs in `link/energy.rs` as a pure function of charge state, temperature, class and user setting. **The function never silently downgrades a class**: a change is a visible event on the surface.

---

## 3 · LF-2 · The stream

### 3.1 The frame classes

```text
FrameClass = C0Safe | C0bModel | C1Delta | C2Video | C3Still | C4CameraUp
FrameHeader { session: SessionId, seq: u64, class: FrameClass, bytes: u32, digest: [u8; 32],
              operator: OperatorId, model: Option<ModelId>, effort: Option<EffortTier> }
```

| The class | The payload | The budget | The fallback |
|---|---|---|---|
| C0Safe | a local frame, no network | 0 | the safe screen, the wallet, the local floor |
| C0bModel | a signed display list and its difference | 2 to 200 kbit | the previous model |
| C1Delta | a regioned delta of pixels | 10 kbit/s to 2 Mbit/s | C0bModel |
| C2Video | a coded video stream | 10 to 30 Mbit/s at 1080p60 | C1Delta at 5 frames per second |
| C3Still | a high resolution still or a 4K page | 30 to 80 Mbit/s | C2Video |
| C4CameraUp | the camera payload of Volume IX | 10 to 130 Mbit/s | the local preview and a stated wait |

### 3.2 The scheduler

The panel scheduler writes only changed regions at the manifest refresh rate and never exceeds the panel temperature policy. A region that has not changed is not written. **A full frame write on a static page is a defect. `[DECISION]`**

### 3.3 The local scene renderer

```text
SceneModel { version: u64, glyphs: GlyphCache, ops: [Op], palette: Palette,
             images: [ImageRef], signature: [u8; 64] }
Op = Rect{..} | Text{..} | Path{..} | Image{..} | Blend{..}
```

Rules. 1. The renderer draws only a signed model. 2. It cannot label a document, a lease or an inference. 3. A model that fails its signature is refused and the last good model stays on the surface. 4. The renderer reports the drawn version to the session, so the operator knows what the user sees.

### 3.4 The reprojection unit

```text
Reprojection { frame: FrameHandle, motion: Motion, mode: Shift|Scale|Rotate, max_ms: 40 }
```

Rules. 1. It runs only on the last decoded frame. 2. It is disabled automatically when the measured artefacts pass the threshold of gate DST-3. 3. It never runs across a scene cut, and the session marks the cuts.

---

## 4 · LF-3 · The authority

### 4.1 The key chain

```text
Wallet ── signs ──▶ SessionGrant { scope, term, energy_policy, operators, classes }
SessionGrant ── derives ──▶ SessionKey { id, expires, scope }
SessionKey ── signs ──▶ the ordinary actions, one at a time
```

`[TREE]` the wallet is `crates/wallet-core` with FIPS 204 ML-DSA-87: a public key of 2 592 bytes and a signature of 4 627 bytes. The device signs once per session, not once per tap, and every ordinary action carries the session key.

### 4.2 The transaction classes

| The class | The example | The path |
|---|---|---|
| Local | the input echo, the cursor, the safe screen | the firmware, no signature |
| Session | a message, a payment inside the grant | the session key, one signature over the intent |
| High value | a new operator, a new module, a part change, a revocation | the wallet, and a second authority when a module is present (t of n, Volume IV, Section 4) |

### 4.3 The lease

```text
Lease { purpose: Purpose, model: ModelId, sensors: [SensorId], classes: [FrameClass],
        expiry: Timestamp, retention: Retention, subject: SubjectId }
```

Four visible, fail-closed refusals cover: wrong model, wrong purpose, expired lease, and unnamed sensor. `[DECISION]`

### 4.4 The component record

```text
ComponentRecord { part_class, part_id, origin, measures, history, signatures, reference }
```

The device verifies the record of the cassette, the module, the pen and a replaced panel before it accepts the part. A mismatch beyond the tolerance refuses the part and shows the reason. RG-6 and RG-13.

---

## 5 · LF-4 · The surface

### 5.1 The manifest

Every member publishes a manifest: outline, panel map, grade, seam map, keep-out band, bend band, refresh range, calibration and mode set. A manifest without a bend band refuses a bend claim. Volume I, Section 9.

### 5.2 The labels

The panel draws four protected labels: mixed-surface evidence, class line, battery/energy state, and camera state. **A page cannot cover a label**, and a page that tries is refused and recorded. `[DECISION]` RG-16.

### 5.3 The input

| The input | The path | The latency |
|---|---|---|
| touch and pen | the mesh layer, the hub, the local echo | 3 to 8 ms |
| proximity and gesture | the mesh and a ranging radio | 10 to 20 ms |
| gaze | the front sensor under a lease, or the panel's own touch of the eye region in the Field mode | stated per case |
| voice | the microphone set of the module, the mask on the device, the intent | stated |
| the wallet | the secure element, one action | local |

### 5.4 The format and the mode change

A mode change (flat, book, Field, clear, docked) is a manifest event with a grace period. The old surface holds the last frame until the new surface acknowledges. A stuck frame is a defect with a gate. SW-5.

---

## 6 · The refusals

| No. | The case | The behaviour |
|---|---|---|
| R1 | a model that is not the leased model | refuse, keep the last good model, record |
| R2 | a purpose mismatch | refuse, show the purpose, record |
| R3 | an expired lease | refuse, offer a renewal with one action |
| R4 | a sensor the lease does not name | refuse, and the hardware light stays off |
| R5 | a part with a bad record | refuse the part, show the field that failed |
| R6 | a path whose operator fails the trust test | never use, and say why on the class line |
| R7 | a class the path cannot carry | refuse the class at start, never degrade silently |
| R8 | an unsigned or a badly signed scene model | refuse, keep the last good model, record |
| R9 | a pressure to read without a grant | refuse with no override, `[TREE]` the constitution |
| R10 | a page that tries to cover a label | refuse the cover, draw the label, record |

---

## 7 · The test hooks

Every gate of `MASTER/00-INDEX.md` has a hook in `leaf/firmware/tests/`. A hook is a named scenario with an input, an expected state and a record. The rule of the program holds: **a result without data is an opinion**. `[DECISION]`

| The hook family | The gates |
|---|---|
| `test_link_*` | SW-1, SW-2, SW-8, SW-9, SW-10, DST-5, DST-6 |
| `test_stream_*` | SW-3, DSP-5, DSP-7, DST-1 to DST-3 |
| `test_authority_*` | SW-4, SW-6, SW-7, SW-12, SW-13 |
| `test_surface_*` | SW-5, SW-11, DSP-9, FLD-5, FLD-6 |
| `test_camera_*` | CAM-2 to CAM-5, CAM-8 |
| `test_thermal_*` | MEC-6, MEC-9, CAM-6 |

---

## 8 · The build order for the coding agents

| Step | The package | The dependency | The gate |
|---|---|---|---|
| 1 | the workspace, the pool allocator, the four tasks, the record format | none | the build and the style checks |
| 2 | LF-3 the key chain against a bench secure element | step 1 | SW-6 on a bench |
| 3 | LF-4 the scene renderer and the labels | step 1 | DST-1, SW-11 on a bench |
| 4 | LF-2 the decoder and the scheduler against a recorded stream | step 1 | SW-3 on a bench |
| 5 | LF-1 the path manager against a link emulator | steps 1 and 2 | SW-1, SW-8, SW-9 |
| 6 | the boot chain, the A and B slots, the safe screen | steps 1 to 5 | the boot matrix, R1 to R5 |
| 7 | the camera path, the sentinel contract, the lease | steps 2 and 4 | CAM-2 to CAM-5 |
| 8 | the mode and the manifest, the Field mode | steps 3 and 4 | DSP-9, FLD-5, FLD-6 |

**The rule of one branch**. One work package, one branch, the test written with the code, no merge without a gate. `[DECISION]`
