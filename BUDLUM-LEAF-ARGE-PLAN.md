# BUDLUM LEAF · END-TO-END FULL-AREA BENDABLE POLYCARBONATE SCREEN AND NETWORK R&D PLAN

**Version**: 2.0 · Revision L.5.0 · 2026-10-12
**Parent document**: `LEAF/BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md`. The directive holds the rules and the gates. This file holds the end-to-end R&D plan (`Ar-Ge Planı`) for the 100% bendable polycarbonate screen (`2.00 mm`, `68.0 g`). It also covers the `90°`-bent `b` module (`20.0 g`) and the Zero-CPU network protocols (`RG-1` to `RG-17`).
**Drawing package**: `LEAF/pafta/E01` to `E03` and `P01` to `P22`. Sheet `P06` maps the 17 work orders, while `P11`, `P12`, `P17`, `P18`, `P21`, and `P22` detail the bendable polycarbonate stack.
**Writing standard**: ASD-STE100. One term has one meaning. Short sentences. No process narrative.
**Tag set**: the tags of the directive apply. This file adds one tag: `[TREE]` means an artefact read from the `budlum-xyz/budlum` tree on 2026-10-05 over the GitHub API.

---

## 0 · Master R&D Architecture: 100% Full-Area Bendable Polycarbonate Screen (`Ekranın Tamamı Esneyebilen Polikarbonat Yapı`)

1. **Core R&D rule**. All `100%` of the `80 x 160 x 2.00 mm` (`R = 6.35 mm`) screen bends as polycarbonate. `[DECISION]`
2. **Zero rigid zones**. No rigid metal block, brittle ceramic plate, or rigid cell sits inside the `2.00 mm` screen. `[DECISION]`
3. **Optical Siloxane-Polycarbonate (`PC-PDMS`)**. Outer shells (`2 x 0.18 mm`), puzzle teeth, and the `(0,0)` hub use optical `PC-PDMS` (`ISO 10993`). `[PUBLICATION]`
4. **High elastic elongation**. `PC-PDMS` copolymer (`EP2707418A1`, `US6657018B1`) provides `> 30%` elastic elongation before yield, `> 55%` break elongation, and zero stress-whitening. `[PUBLICATION]`
5. **Multi-neutral-plane silicone `OCA` decoupling**. Two `0.04 mm` silicone `OCA` slip layers (`G = 0.035 MPa`, `n = 1.585`) decouple the `0.18 mm` skins. `[PUBLICATION]`
6. **Strain reduction (`3.92%` down to `0.35%`)**. Each `0.18 mm` polycarbonate skin bends around its own neutral plane, holding strain at `0.35%` at `R = 25.5 mm`. `[DECISION]`
7. **Effortless leaf flex (`1.4 N`)**. Multi-neutral-plane shear decoupling lowers flexural rigidity by `48x`, so the `2.00 mm` polycarbonate screen bends with `1.4 N` finger force. `[DECISION]`

### 0.1 Five-Pillar Full-Screen Polycarbonate R&D Matrix (`Ar-Ge Matrisi`)

| R&D Pillar | Polycarbonate Material & Mechanism | Key Physical Metric | Verification Gate |
|---|---|---|---|
| **P1 · Outer & Carrier Skins** | `2 x 0.18 mm` optical `PC-PDMS` (`ISO 10993`, `n = 1.585`) + `2 x 0.04 mm` `G = 0.035 MPa` `OCA` | `ε_PC = 0.35%` at `R = 25.5 mm` (`0.58%` at `R = 15 mm`); `1.4 N` bend force | MEC-1, MEC-14, B-1 |
| **P2 · `+` Puzzle Lock & `(0,0)` Hub** | `24` `+Z/-Z` dovetail puzzle joints + `(0,0)` hub co-molded in `PC-PDMS` over `80 µm` superelastic `NiTi` | `EI_seam / EI_tile = 1.00`; `100 N/tooth` (`10 N/mm`); `< 15 µm` (`n = 1.585`) lip | MEC-2, DSP-4, B-4 |
| **P3 · Full-Area Flex Solid-State Cell** | `1.06 mm` `LLZO/PEO-LiBOB` cell in `PC-PDMS` elastomer on a `2.5 x 2.5 mm` grid (`1 680` micro-cells) | `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`); `0%` liquid; `0.0 ppm` HF; `<= 36.2 °C` | ENR-1, ENR-8, B-6 |
| **P4 · Flex `Qi2.2` & `T-OLED / PDLC`** | `60 µm` `FeSiBCuNb` nanocrystalline + `PC` elastomer shield (`µ_r = 12 000`) + `AgNW/IZO` on `PC` film | `Ø54 mm` (`15-25 W`) + `4 x Ø22 mm` `Qi2.2`; `12 Ω/sq`; `< 0.8%` `ΔR` at `R = 15 mm` | ENR-12, DSP-1, CLR-1 |
| **P5 · `90°` Natural-Gap `b` Module** | Exact `uploads/b.png` turned `90°` and bent `90°` across its natural gap (`boşluk`), zero extra hinge blocks | `1.00 mm` horizontal top `çubuk` (LCP antenna + sole `USB-C`); front-facing ring (`20.0 g`) | MON-1 to MON-20 |

### 0.2 Four-Phase Hardware & Materials R&D Execution Plan (`Baştan Sona Ar-Ge Fazları`)

| R&D Phase | Scope & Deliverables | Target Acceptance Metric |
|---|---|---|
| **Phase 1 · `PC-PDMS` & Multi-Neutral-Plane Stack** | Extrude optical `0.18 mm` `PC-PDMS` skins (`R = 6.35 mm`) and laminate with `0.04 mm` `G = 0.035 MPa` silicone `OCA`. | `%T >= 90%`, haze `< 0.6%`, `ε_PC = 0.35%` at `R = 25.5 mm`, zero whitening after `200 000` cycles. |
| **Phase 2 · Biaxial Flex `LLZO` Cell & Flex `Qi2.2`** | Laser-articulate `2.5 x 2.5 mm` `LLZO/PEO-LiBOB` micro-cells in `PC-PDMS` elastomer and laminate `60 µm` nanocrystalline `Qi2.2` coils. | `12.0 Wh` (`3 200 mAh`), `< 1.1%` impedance shift under `R = 25.5 mm` flex, `0.0 ppm` HF, `<= 36.2 °C`. |
| **Phase 3 · Co-Molded `PC-PDMS + NiTi` Puzzle Lock** | Injection-mold the `24` `+Z/-Z` dovetail puzzle teeth and `(0,0)` hub in `PC-PDMS` over `80 µm` superelastic `NiTi` cores. | `100 N/tooth` (`10 N/mm`) pull lock, `< 2.5 µm` Z-step, `< 15 µm` (`12 µm`, `n = 1.585`) optical seam. |
| **Phase 4 · `90°` `b` Module & Zero-CPU Network Integration** | Form the turned `b.png` module at its `4.0 mm` gap (`1.00 mm` top `çubuk`) and verify `RG-1` to `RG-17` over `UWB / mmWave`. | `20.0 g` `b` module (`88.0 g` total), `SAR = 0.054 W/kg`, `SW-1` to `SW-13` passing with raw bench data. |

---

## 1 · The delegation boundary

### 1.1 What the device keeps

| Function | Why it stays on the device | Artefact |
|---|---|---|
| Panel scanout, the Quad-Tile timing controller (`U1`), the display driver | Physics. Every pixel on the 4 polycarbonate quadrants must be driven synchronously across the `+` seam. | Panel and driver register, directive Section 4 |
| The hardware decoder in the `b` module | The link carries compressed video. A software decoder needs a general processor, and the device has none. | RG-3 |
| The secure element and the wallet authority | Rule: the device holds the wallet authority, and the wallet is never a key-custody service. `[TREE]` | `src/account_abstraction/`, `crates/wallet-core` |
| The radios and the `1.00 mm` horizontal `b` `çubuk` antennas | The link is the product. `[DECISION]` | Directive Section 7, sheet P05, sheet P20 |
| The safe screen, the wallet approval, the input echo, the battery state | Rule H11: the local floor must not depend on the link. | Sheet P05, panel E |

### 1.2 What the device delegates, and to whom

| Delegated function | The Budlum artefact that already serves it | Status |
|---|---|---|
| Storage of the user data and of the session state | B.U.D. and the storage module, `bud/` with the `.bud` v2 container `[TREE]` | exists |
| Consent for a read | Pollen, the Data Rights gate: a read without a grant is refused, with no override `[TREE]` | exists |
| Consensus, blocks and votes | VALIDATOR role, RoleId 1 `[TREE]` | exists |
| Shard storage and challenge | STORAGE_OPERATOR role, RoleId 5 `[TREE]` | exists |
| Inference compute and the result | AI_OPERATOR role, RoleId 8, with a compute bond and effort tiers `[TREE]` | exists |
| Model identity and the perception declaration | `src/ai_inference/`, declaration V3, fail-closed `[TREE]` | exists, one gap: RG-5 |
| Succinct verification of the chain | the light client with one trust anchor and finality certificates `[TREE]` | exists, one gap: RG-2 |
| A transaction without a key in the relayer | `src/relayer/`, permissionless, with a policy envelope `[TREE]` | exists, one gap: RG-10 |
| The browser and the page engine | Budscan, the decentralised browser with a Gecko patch layer `[TREE]` | exists, one gap: RG-14 |
| The identity and the evidence surface | the D-Web Passport and the wallet context atlas in the gateway `[TREE]` | exists, one gap: RG-16 |
| The name rule and the resolution | BNS with `bns_proof.rs`, and ENS, and four fetchers that declare their strength `[TREE]` | exists |

**The first finding**. The network side of this device is almost complete. The device adds no new system, no new chain and no new storage layer. The work is at the boundary: the device profile, three protocols, one leasing rule, one record type and the naming discipline. `[DECISION]`

---

## 2 · RG-1 · The Leaf node profile

### 2.1 What exists

`src/network/mobile.rs` already holds a mobile node profile. It is called Mobile Self. `[TREE]` It contains:

- a node that runs on a phone,
- a challenge policy that is aware of the battery,
- relay and STUN traversal for a device behind a router or a carrier NAT,
- self-hosted storage of the B.U.D. slice that the device holds,
- lightweight stateless sync.

### 2.2 What is missing

Mobile Self assumes a conventional phone with a general CPU and an operating system. Budlum Leaf has a Zero-CPU `b` module (`U1` TCON, `U2` `UWB / mmWave` SiP, secure element). Its `2.00 mm` (`68.0 g`) bendable polycarbonate body holds a `12.0 Wh` (`4 x 3.0 Wh`) solid-state battery. A profile that assumes a local CPU will not run.

Two questions are open in the tree today:

1. What does a node with no processor keep, and what does it delegate?
2. What challenge frequency can a `12.0 Wh` (`3 200 mAh`) solid-state battery carry, and who decides it?

### 2.3 The order

**RG-1**. Define the LEAF NODE PROFILE as a named profile beside Mobile Self. The profile must state, in this order:

1. **The kept set**. The device caches "on device" B.U.D. objects, one trust anchor, 4-quadrant `+` seam calibration, component records, and the last N finality certificates.
2. **The delegated set**. Everything else, with the exact artefact named per function, as in Section 1.2.
3. **The challenge policy table**. The policy depends on battery and charge state (`Qi2.2` or `b` `USB-C`), not a constant. Proposed table:

| Device state | Challenge answer | Storage service | Note |
|---|---|---|---|
| On charge (`Qi2.2` or `b` `USB-C`) | full | on | the device can serve while it charges |
| Above 60 percent (`> 7.2 Wh`) | normal | on | the default state across all 4 polycarbonate quadrants |
| 20 to 60 percent (`2.4-7.2 Wh`) | reduced | on, reduced rate | the reward drops with the rate |
| Below 20 percent (`< 2.4 Wh`) | minimum | off | the device keeps the wallet and the screen |
| Below 5 percent (`< 0.6 Wh`) | stop | off | the device announces its state and leaves the set |

4. **The announcement**. The device publishes its state to its validators so the network never waits for an impossible answer. A state change must be visible inside one challenge period.
5. **The energy accounting**. The profile must state the joule cost of one challenge answer, measured on the real device. This number sets the reward that the device earns, and it is the input of the honest answer to RG-11.

### 2.4 The acceptance test

1. A Leaf profile node on an emulated processor-less host answers challenges in time and refuses work above its state.
2. The measurement of one challenge answer, in joules, on the real hardware, is in the record.
3. The device leaves the storage set before the battery reaches 5 percent, in every test of the state table. `[HYPOTHESIS]` The cost is small; the test decides it.

---

## 3 · RG-2 · The trust anchor and the finality budget

### 3.1 What exists

`src/light_client/mod.rs` holds the verification path. `[TREE]`

- One trust anchor: a checkpoint height, a block hash and a validator-set hash.
- A `FinalityCert`: a BLS aggregate signature over a stake-weighted quorum.
- A `QcBlob`: the post-quantum quorum certificate.
- `sync_plan`: a GetHeaders locator plus a per-checkpoint QC blob fetch.
- The rule: a validator-set change needs a new anchor, delivered out of band.
- A binary, `budlum-light`, exists for the host case.

`crates/budscan` holds the same discipline inside the browser, with evidence labels. `[TREE]`

### 3.2 What is missing

A small secure element must verify a BLS aggregate and a post-quantum blob. Nobody has measured that budget on a part that fits inside the `2.00 mm` polycarbonate body and `2.00 mm` `b` module ring.

### 3.3 The order

**RG-2**. Produce the FINALITY VERIFICATION BUDGET.

1. Choose two candidate secure elements, one with a BLS accelerator and one without.
2. Measure `FinalityCert` and `QcBlob` verification times, peak current, energy per verification, and storage per anchor.
3. Define the refresh rule: how often the device must refresh its anchor, and what happens when the refresh fails. A stale anchor must produce a visible state on the screen, not a silent success.
4. Define anchor delivery: out-of-band channel, anchor signature, and the user action accepting a new validator set. The device must never accept a new set over the block channel, preserving the trust anchor.

### 3.4 The acceptance test

1. A device-class secure element verifies a real `FinalityCert` and `QcBlob` within the screen refresh budget.
2. A stale anchor, a wrong anchor and a forged certificate are each refused, and the refusal is visible.

---

## 4 · RG-3 · The display transport across the 4-quadrant bendable polycarbonate screen

### 4.1 What exists

The directive defines the display protocol as a requirement (directive Section 12, interface orders). The tree has client transports and RPC surfaces, and Budscan has a light client inside a browser. `[TREE]` The tree does not hold a named home for a pixel transport.

### 4.2 What is missing

**The open question**. A pixel-delta transport is a client transport. A consensus layer is a different thing. Putting the display protocol inside consensus lets a screen refresh stall a block. That is an architecture error.

### 4.3 The order

**RG-3**. Define the DISPLAY TRANSPORT as a client-facing protocol with four frame classes, and place it outside the consensus path.

| Class | Content | Budget | Loss tolerance |
|---|---|---|---|
| C0 safe | text and the wallet surface, drawn locally from the local floor | no link | none, it is local |
| C1 delta | the changed region only, with a codec for text and flat colour | 10 kbit/s to 2 Mbit/s | high |
| C2 video | 1080p at 60, hardware decode in `U1` Quad-Tile TCON | 10 to 30 Mbit/s | medium, conceal the error |
| C3 still | one full frame on demand, for a photograph or a document | burst | low |

Rules for the protocol:

1. Every frame carries a sequence number, a class and the session id.
2. The device declares its classes and its 4-quadrant (`Q1..Q4`) decoder profile at session start.
3. A class that the device cannot decode is refused at start, not degraded in silence.
4. The session states the `+` optical seam LUT rule (`< 15 µm`, `n = 1.585`) and calibration record.
5. The placement decision belongs to Ayaz: this protocol is a client transport and must not enter the consensus path. `[HYPOTHESIS]` The tree can need a new module name for it. The name and the location need the architecture decision of Section 17, item D3.

### 4.4 The acceptance test

1. A 1080p at 60 stream runs with a hardware decoder on the device and the glass-to-glass time is measured.
2. A delta session runs on a 2 Mbit/s carrier link and stays usable.
3. Measure the `+` puzzle seam after `200 000` bends at `R = 25.5 mm` (`< 2.5 µm` step).

---

## 5 · RG-4 · The live session handoff

### 5.1 What exists

The wallet authorizes; the relayer carries an intent; the validator computes. `[TREE]` There is no session object that survives a change of validator.

### 5.2 What is missing

A session that a second operator can resume. Without it, a failing or repricing validator ends the work and breaks the session-survival promise.

### 5.3 The order

**RG-4**. Define the SESSION HANDOFF.

1. **The session object**: session id, user authority, class set, decoder profile, effort tier, energy policy, deadline, and counter. The object is stored in B.U.D. under the user authority. The device holds a reference and a hash, never the only copy.
2. **The binding**: a session is bound to one operator at a time. The binding has a term and a notice period.
3. **The resume token**: single use, short lived, signed by the user authority, addressed to one named operator. A token that is reused or that names a different operator is refused.
4. **The handoff**: the leaving operator publishes the state hash; the joining operator fetches the state from B.U.D. under a Pollen grant; the device renders the transition, not a blank screen.
5. **The grace period**: the time during which the device keeps the screen alive and the session frozen. The measured value goes into the record.
6. **The failure set**: interrupted transfer, expired token, or an operator disappearing before the first frame. Each one has a defined end state.

### 5.4 The acceptance test

1. A live delta session moves from operator A to B without state loss in clean and unplanned cuts.
2. A reused token and a redirected token are refused.
3. The grace period is measured, and the device never shows a stuck screen in the test set.

---

## 6 · RG-5 · The perception lease

### 6.1 What exists

`src/ai_inference/` holds the model registry, the compute bond, the effort tiers, the perception declaration V3 and the rule that a failure is closed. `docs/AI_VERIFICATION_STATUS.md` records the same. `[TREE]` The declaration is per request.

### 6.2 What is missing

A viewfinder is continuous. A gesture model runs at 30 to 60 frames per second. A declaration per frame is not possible, and a declaration per second turns the gate into a formality. Without a lease, the gate must refuse every frame, leaving the camera module unusable.

### 6.3 The order

**RG-5**. Define the PERCEPTION LEASE.

1. **The lease object**: a time-bounded document. It states purpose, model version, sensor, frame classes, expiry, revocation and retention rules.
2. **The default duration**: short. Photo leases last seconds; viewfinder leases last minutes with a visible indicator.
3. **The revocation**: one action by the user revokes a lease and stops the work. The device must show that the sensor is closed.
4. **The declaration trail**: the lease and every covered read are recorded under model and operator identities. A read without a lease is refused, exactly as a read without a grant is refused today.
5. **The fail-closed set**: expired lease, mismatched model or purpose, or an unnamed sensor. Each is a refusal, not a warning.
6. **The user surface**: the wallet grants and revokes leases, and sensor state stays visible on the device. The device shows a hardware state, not a software icon that a program can paint.

### 6.4 The acceptance test

1. A viewfinder session runs for 30 minutes under one lease with the necessary declarations, at the designed frame rate.
2. The four fail-closed cases each refuse.
3. The revocation stops the work inside the stated time, measured.

---

## 7 · RG-7 and RG-8 · The signature budget and the authorization path

### 7.1 What exists

`crates/wallet-core` holds BIP39 and FIPS 204 ML-DSA-87 at category 5. `[TREE]` The sizes:

| Item | Size |
|---|---|
| ML-DSA-87 public key | 2 592 bytes |
| ML-DSA-87 signature | 4 627 bytes |
| A t-of-n multisig authorization | t separate signatures, each verified on its own |

`src/account_abstraction/threshold_mldsa.rs` is now `MultisigAuthorization`: t separate ML-DSA-87 verifications, with the secret sharing removed by design. `[TREE]` Account abstraction also holds the private transfer authorization and the TEE attestation path.

The wallet is explicitly not a relayer; the relayer is permissionless, and it works with stake and slashing and no whitelist. `[TREE]`

### 7.2 What is missing

A number, not a definition: what travels over the link for a normal user action, and what the device must sign itself.

### 7.3 The order

**RG-7 · the transport budget**. State, for each action, the bytes that cross the link and the direction, with ML-DSA-87 sizes as the input:

| Action | The signature | The payload | Direction | Note |
|---|---|---|---|---|
| Wallet approval of one payment | 1 signature, 4 627 B | the intent | device to relayer | the device signs; the relayer holds no key |
| Session grant for one operator | 1 signature | the session object hash | device to network | once per session |
| Perception lease grant | 1 signature | the lease | device to operator | once per lease |
| Component record of a replaced part | 1 signature from the part, 1 from the wallet | the record | part and device to B.U.D. | RG-13 |
| Optical receipt with no radio | 1 signature in QR frames | the receipt | device to a reader | RG-12 |

A 4 627 byte signature takes about 240 QR frames, so the optical path must carry a compressed or aggregated form. State the form and the frame count.

**RG-8 · the authorization path**. A wallet that signs every tap is unusable, and a session key that never expires is unsafe. State the chain:

1. The wallet authority signs one session grant.
2. The session grant authorizes one session key, with a scope, a term and an energy policy.
3. The session key signs the ordinary actions inside the scope.
4. Above the scope, the wallet authority signs again.
5. Revoking one session key is a single action that neither moves funds nor requires a new seed.

The account-abstraction registry is the home of this chain. State the fields and the storage of the grant.

### 7.4 The acceptance test

1. A device-class secure element signs one ML-DSA-87 message inside the time budget that a user tap allows, measured.
2. A scoped session grant is created once, used repeatedly, and revoked once, with bytes and time measured.
3. The optical receipt path carries one signed receipt with a stated frame count and a stated time.

---

## 8 · RG-6 and RG-13 · Component records and the part anchor

### 8.1 What exists

The gateway holds the D-Web Passport: a read-only, evidence-labelled identity profile, with a maximum of 64 evidence items, wired from the RPC server. `[TREE]` The atlas holds the wallet context graph and the evidence cards. `[TREE]` B.U.D. holds content-addressed objects. `[TREE]` The account abstraction holds the TEE attestation path. `[TREE]`

### 8.2 What is missing

The hardware parts are removable and renewable: 4 bendable polycarbonate quadrants (`Q1..Q4`, `17.0 g`, `3.0 Wh` `LLZO/PEO`) and the `90°`-bent `b` module (`20.0 g`). The tree has no object for a hardware part.

There is also a naming risk. The word "passport" already means the identity profile in the gateway. If a battery quadrant also gets a "passport", one term has two meanings, and the tree breaks its own rule.

### 8.3 The order

**RG-6 · the component record**. Define one object:

| Field | Content |
|---|---|
| The class | `leaf`, `core`, `module`, `rim` |
| The identity | the part serial, and the public key of the secure element in the part |
| The origin | the maker, the batch, the date |
| The measures | mass (`17.0 g`), thickness (`2.00 mm`), capacity (`3.0 Wh`) and bend/charge cycles for each polycarbonate quadrant (`Q1..Q4`) |
| The history | the installation, the removal, the `+` seam LUT calibration, the fault |
| The signatures | the maker or the part element, plus the wallet authority when the part joins the device |
| The reference | the content address in B.U.D. |

Rules:

1. The record is written by the part when the part joins and when the part leaves. The authority is the wallet, not a factory key. `[DECISION]`
2. The device refuses any part with a mismatched record and shows the reason on the safe screen.
3. Each polycarbonate quadrant record supplies the cycle count and health used by the RG-1 policy.
4. Pollen gates a read of a record that belongs to another user.

**RG-13 · the part anchor**. One root of trust for the device and its parts:

1. Device identity is anchored in the body secure element; wallet authority is never stored in a removable part.
2. A replaced polycarbonate quadrant (`Q1..Q4`) or `b` module is authorized by the wallet: install, calibrate, accept.
3. One wallet action revokes a lost module on the network, preventing it from joining another device.

### 8.4 The acceptance test

1. A replaced quadrant, core, and `b` module each produce a record, and mismatched parts are refused.
2. The wallet authorizes installation in one action, and module revocation appears on the network within one challenge period.

---

## 9 · RG-9 and RG-11 · Roles, effort tiers and the honest job

### 9.1 What exists

`docs/VALIDATOR_ROLES.md` defines VALIDATOR (RoleId 1), STORAGE_OPERATOR (RoleId 5) and AI_OPERATOR (RoleId 8), with separate stakes and separate slashing. `[TREE]` The effort tiers run from 0.5x to 10x in `src/ai_inference/effort.rs`. `[TREE]` An operator that cannot serve a 10x request refuses the request; it does not answer with cheaper work. `[TREE]` The RoleId is an open `u32`, so the registry is extensible. `[TREE]`

### 9.2 The order

**RG-9 · the reverse battery policy**. The device sends its energy state to the validator, and the render mode follows the cell state:

| Device state | The network answer |
|---|---|
| On charge | the highest class, the deepest effort tier that the user allows |
| Above 60 percent | the normal class |
| 20 to 60 percent | a reduced class, and the honest statement of the reduction |
| Below 20 percent | the safe class, plus wallet and messages only |
| Below 5 percent | the safe screen, the wallet and the state, with no session |

The device must state the reduction to the user. A silent downgrade is a lie about the product.

**RG-11 · can the device serve storage at all**. Answer three questions:

1. What is the lowest honest challenge cost for a device of this class?
2. Is an on-charge-only device a useful storage member, or does it only earn while plugged in?
3. Which is better for the product: the device serves and earns, or the device pays and stays light? Give the numbers for both. Cost is deferred by the user, so give the energy and the time, not the price.

### 9.3 The acceptance test

1. A 10x request to a 1x operator is refused, and the device renders it as a refusal.
2. Over 24 hours, the device answers challenges in high states and leaves the set in low states.
3. The render class follows the battery state in every one of the five states.

---

## 10 · RG-10 · The relayer and the network edge

### 10.1 What exists

`src/relayer/` holds `UserIntent`, `SolverBid`, `PolicyEnvelope`, `IntentSettlement` with a status, `RelayerPolicyRegistry` and `RelayerWorker`. `[TREE]` The wallet holds no staking and no whitelist code. `[TREE]` The mobile profile holds relay and STUN traversal. `[TREE]`

### 10.2 What is missing

A device behind carrier NAT roaming across Wi-Fi, cellular and satellite needs a stated reachability and fee policy. Without it, the relayer path works in a laboratory and fails in a moving car.

### 10.3 The order

**RG-10**. Define the LEAF REACHABILITY AND FEE PLAN.

1. **The identity**. The device identity is a key and a record, not an address. The address changes; the identity does not.
2. **The paths**. The direct path when one exists, the relay path when it does not, and the rule that chooses. The choice is measured, not guessed.
3. **The fee plan**. How an offline device settles intents upon return: queue, expiry, cancellation, and maximum intent age.
4. **The policy envelope**. The device states its own limits: maximum fee, maximum delay, class set, and purpose. A relayer that cannot meet the envelope refuses instead of degrading.
5. **The privacy rule**. The relayer carries the intent. The relayer must not learn the identity of the user beyond what the intent needs. State what the envelope hides.

### 10.4 The acceptance test

1. A device behind a carrier NAT reaches a relayer and settles one intent, with the path in the record.
2. The path changes from Wi-Fi to cellular mid-session, and the session continues.
3. An intent older than the stated maximum age is refused by the network and cancelled on the device.

---

## 11 · RG-14 and RG-16 · The surfaces

### 11.1 What exists

Budscan is a decentralised browser on a Gecko patch layer. It resolves names via BNS (`bns_proof.rs`) or ENS, then fetches through four fetchers that declare their strength. `[TREE]` The gateway provides the identity profile and the atlas, read-only and evidence-labelled. `[TREE]` Lubot is a reading AI with an Android bridge and a rule that secrets are masked on the device before a question leaves it. `[TREE]`

### 11.2 The order

**RG-14 · the Budscan render target**. On this device, the Budscan engine runs at the validator and sends delta frames to the screen. The order must state:

1. The split: which part of the browser runs where.
2. The name rule and the verification: on this device, the light client of RG-2 is the verifier.
3. The renderable page classes (`C0` to `C3` of RG-3) and their honest indicator on the screen.
4. What happens when a page needs a class that the link cannot carry today.

**RG-16 · the evidence rule**. An evidence label means a statement with a status. Because the device has no render engine, the session draws each label with a fixed shape and size. State:

1. The label set and one meaning per label.
2. Where the label is drawn, and the rule that a page cannot cover it.
3. The behaviour when a statement has no evidence: the label states that, and the surface does not pretend.

### 11.3 The acceptance test

1. A mixed-evidence page renders labels accurately, and any page attempting to cover a label fails.
2. The class of the render is visible on the screen for a video page and for a text page.

---

## 12 · RG-12 · The optical transfer

### 12.1 What exists

B.U.D. has a QR and a receipt line. `[TREE]` `crates/note-packing` defines one canonical note-field packing with compressed, encrypted payloads and deterministic QR frames. `[TREE]`

### 12.2 The order

**RG-12**. Define the OPTICAL TRANSFER as a first-class feature of the device, because it is the only path that works with no radio at all.

1. **The payloads**. A signed receipt, a small authorization, a contact, a payment request. State the maximum size for each.
2. **The packing**. Use the note-packing crate. Never derive the packing again in the device code: call the crate. A second definition in the device is the exact failure mode that the crate was created to prevent. `[TREE]`
3. **The frame budget**. State frames per payload, frame rate, distance, light level, and transfer time. A 4 627 byte signature must be either compressed or replaced by an aggregate form. State which.
4. **The reading side**. A reader app must verify the signature and anchor before showing any result.
5. **The display rule**. The session draws frames at fixed size and stored luminance so a dimmed panel cannot fail.

### 12.3 The acceptance test

1. A signed receipt transfers optically between two radio-silent devices and is verified by the second device.
2. Transferring the same payload at minimum brightness fails as expected and is logged in the record.

---

## 13 · RG-15 · The device telemetry schema

### 13.1 The order

**RG-15**. Define one schema for the state that leaves the device:

| Group | Fields | Who reads it |
|---|---|---|
| Energy | per-quadrant (`Q1..Q4`) charge, health, cycle count, `Qi2.2` state, and dual NTC ocular temperature (`<= 36.2 °C`) | the policy of RG-1 and RG-9 |
| Thermal | the polycarbonate panel temperature, the `LLZO` core temperature, the eyewear derating state | the render policy and the charge policy |
| Optical | the 4-quadrant `+` seam LUT calibration record, the seam step (`< 2.5 µm`), the brightness level | the render path |
| Link | the path, the class that the link can carry, the jitter, the loss | the session and the fail-safe ladder |
| Session | the id, the class set, the effort tier, the counter | the operator |
| Privacy | the sensor state, the active leases | the user surface and the audit |

Rules: the schema is small and versioned, with units and resolution on every field. Every telemetry read obeys Pollen rules and is visible to the user in the audit view.

### 13.2 The acceptance test

1. The device publishes the schema, the operator reads it, and the render class follows the state.
2. A read without a grant is refused, and the refusal is logged.

---

## 14 · RG-17 · Naming and tree hygiene

1. **One term, one meaning**. The D-Web Passport is an identity profile in the gateway. A hardware record is a COMPONENT RECORD. `[DECISION]`
2. **The stub rule**. A surface counts as existing only when wired from the module root and covered by a gate. The `src/sdk/` precedent is the reason: five files, 1 871 lines, never compiled, with stubs that returned success. `[TREE]` A Budlum Leaf binding to such a surface is a promise that nothing keeps.
3. **The rule for this program**. Every bound artefact must be named with its path and test in the interface order. A name without a test is not a binding.
4. **The style rule**. The tree is English-only, with the Turkish baseline file as the single exception. `[TREE]` Budlum Leaf adds no exception.

---

## 15 · The build order for the next developer

The order below respects the dependencies. It is a specification order; rule L1 still holds.

| Step | Task | Depends on | The artefact |
|---|---|---|---|
| 1 | Laminate and test the full-area bendable `PC-PDMS` + `OCA` + `LLZO` + `Qi2.2` quadrant tiles (`Q1..Q4`) | Section 0 | `LEAF/HARDWARE/11` to `17`, bench report |
| 2 | Write the LEAF NODE PROFILE (RG-1) beside Mobile Self for the `12.0 Wh` 4-quadrant body | step 1 | `src/network/mobile.rs`, a new profile |
| 3 | Measure the finality budget and choose the secure element (RG-2) | step 2 | a bench report and one part choice |
| 4 | Fix the display transport location and the 4-quadrant `+` seam LUT classes (RG-3) | Section 17 D3 | a client transport protocol |
| 5 | Write the perception lease and its four refusals (RG-5) | nothing | `src/ai_inference/` |
| 6 | Write the session object and the resume token (RG-4) | steps 2 and 4 | a session protocol |
| 7 | Write the signature transport budget and the session-key chain (RG-7, RG-8) | step 6 | `src/account_abstraction/` |
| 8 | Write the component record and the part anchor for `Q1..Q4` and the `b` module (RG-6, RG-13) | step 3 | one object type |
| 9 | Write the reverse battery policy (RG-9) | steps 2, 4 and 8 | a policy |
| 10 | Answer the storage question with numbers (RG-11) | step 2 | a study |
| 11 | Write the reachability and fee plan (RG-10) | step 2 | `src/relayer/` |
| 12 | Write the Budscan render target and the evidence rule (RG-14, RG-16) | steps 4 and 8 | `crates/budscan`, `src/gateway/` |
| 13 | Write the optical transfer (RG-12) | step 8 | a device feature and a reader |
| 14 | Publish the telemetry schema (RG-15) and clean the naming (RG-17) | steps 2 and 9 | one schema and the tree |

---

## 16 · The software verification plan

| Gate | The test | The pass condition |
|---|---|---|
| SW-1 | a Leaf profile node in a device-class emulator | answers inside the period, follows the state table of RG-1 |
| SW-2 | the finality budget on the chosen element | inside the stated time, energy and storage |
| SW-3 | the frame classes over an impaired link | every class meets its stated budget, and a class the device cannot decode is refused at start |
| SW-4 | a lease, its four refusals, and a revocation | all six behave as specified, with the times measured |
| SW-5 | a handoff in a clean cut and in an unplanned cut | no stuck screen, no lost state, the token rules hold |
| SW-6 | the signature budget | the bytes and the times match the table, per action |
| SW-7 | a component record and a part refusal (`Q1..Q4` and `b` module) | the device refuses a mismatched part and shows the reason |
| SW-8 | the reverse battery policy over 24 hours | the render class follows the state in all five cases |
| SW-9 | a challenge answer from a device on charge and off charge | the energy numbers in joules, and the earned credit |
| SW-10 | a relayer path behind a carrier NAT, with a path change | the intent settles, the path is in the record |
| SW-11 | a page with mixed evidence, and a page that covers a label | the labels render, the cover attempt fails |
| SW-12 | an optical receipt with no radio | the reader verifies the receipt, the frame count and the time are in the record |
| SW-13 | a telemetry read with and without a grant | the granted read succeeds, the ungranted read is refused and logged |

**One rule for every gate**. A gate needs raw data. A result without data is an opinion. `[DECISION]`

---

## 17 · The decisions settled in Revision L.5.0

| No. | The decision | The Revision L.5.0 settlement | The reason |
|---|---|---|---|
| D1 | 100% full-area bendable polycarbonate screen (`R = 25.5 mm`) | `80 x 160 x 2.00 mm` (`R = 6.35 mm`, `68 g`) `PC-PDMS` + `G = 0.035 MPa` `OCA` (`0.35%` strain) | every millimeter of the polycarbonate screen bends smoothly with zero rigid zones |
| D2 | Turned & `90°`-bent-at-gap `b` module (`1.00 mm` top `çubuk`) | exact `b.png` turned `90°` and bent `90°` at its gap (`boşluk`); `1.00 mm` `çubuk` sits horizontally on top | zero added hinge blocks; front-facing ring houses `50 MP` OIS camera and rear AMOLED |
| D3 | The home of the display transport | a client transport outside the consensus path | a screen refresh must not stall a block |
| D4 | Co-molded `PC-PDMS + NiTi` `+` puzzle lock & `(0,0)` hub | `24` `+Z/-Z` dovetail puzzle teeth (`10 N/mm`) + `(0,0)` hub in `PC-PDMS` + `80 µm` `NiTi` (`EI` ratio `1.00`) | tiles snap from either side and bend continuously across `+` without separating |
| D5 | Full-area flex `LLZO/PEO` battery & flex nanocrystalline `Qi2.2` | `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) biaxial `LLZO/PEO` (`<= 36.2 °C`) + `60 µm` nanocrystalline `Qi2.2` | portless screen body (`0` `USB-C` on body; sole `USB-C` in `1.00 mm` `b` `çubuk`), `EU 2023/1542` `< 3 s` swap |
| D6 | The window application | Budscan as the only browser, with the gateway as the identity and evidence layer | one surface, one identity, one evidence rule |
| D7 | The claim wording | the class and the case at the limits, never a superlative on a specification | the product's honesty is its differentiator |

**Closed decisions**. The `80.0 x 160.0 x 2.00 mm` (`R = 6.35 mm`, `68.0 g`) screen is a 100% bendable polycarbonate (`PC-PDMS`) structure with zero rigid zones. It pairs with the `20.0 g` turned and `90°`-bent-at-gap `b` module (`88.0 g` total). `[DECISION]`

---

## 18 · Sources of this file

- The `budlum-xyz/budlum` tree (`2026-10-05`): `mobile.rs`, `light_client`, `relayer`, `gateway`, `threshold_mldsa.rs`, `effort.rs`, `pollen`, `wallet-core`, `note-packing`, `budscan`, `bud`, and `VALIDATOR_ROLES.md`. All `[TREE]`.
- The directive `LEAF/BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md` (`LEAF/FINAL/00` to `20`) and hardware volume `LEAF/HARDWARE/00` to `20`. `[DECISION]`
- The pafta set `LEAF/pafta/` (`E01` to `E03` and `P01` to `P22`). `[DECISION]`
- Published data on `PC-PDMS` copolymers (`EP2707418A1`), `OCA` decoupling, flex `LLZO/PEO` cells, and nanocrystalline `Qi2.2` (sheets `P04`, `P11`, `P12`, `P22`). `[PUBLICATION]` and `[COMPANY]`

**Records**
- This file, version 2.0 (Revision L.5.0), 2026-10-12
- `LEAF/BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md`, Revision L.5.0
- `LEAF/pafta/E01` to `E03` and `P01` to `P22`
