# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME IV-B · DISTANCE INDEPENDENCE

**Version:** 4.1 (revision A) · part of `MASTER/00-INDEX.md`
**The order of Ayaz that created this volume:** *the distance must not matter. Which validator will carry the hardware is uncertain. The device chooses the nearest one, but the nearest one can be far. Calculate this.* `[DECISION]`

---

## 1 · The theorem

**Distance independence theorem**. Perceived distance is **the distance to the last device answering inside the interaction budget**, not to the compute host. A program that places the interaction inside the device, and the correctness and the heavy compute anywhere, is distance independent. `[DECISION]`

The theorem is proved by five mechanisms, and each one has a number, a gate and an owner.

| The mechanism | What it removes from the network path | The remaining distance | The gate |
|---|---|---|---|
| 1 · The local floor | the input echo, the cursor, the wallet approval, the safe screen | zero | SW-4, MEC-9 |
| 2 · The local scene renderer | text, the interface, lists, the keyboard, the buttons, the menus | zero | DST-1, DST-2 |
| 3 · The frame reprojection unit | the delay of a scroll, a pan, a zoom and a tilt of the last video frame | zero to 8 ms | DST-3 |
| 4 · The edge agent | the near part of the session: the cache, the composition, the buffer, the relay | 1 to 5 ms, wherever the user is | DST-4, DST-5 |
| 5 · The honest class ladder | nothing. It states where the fidelity falls, and it is visible on the surface | stated | DST-6 |

---

## 2 · Mechanism 2 · The local scene renderer

The network does not send pixels for the interface. It sends a **document model**: a signed, versioned display list of text runs, shapes, image references, colours and a difference against the acknowledged version. The hub of the Leaf renders it locally at 144 Hz. `[DECISION]`

| Property | The value |
|---|---|
| The parts | a glyph cache, a vector fill, an alpha blend, an image blit, a colour engine |
| The silicon | about 2 mm² of fixed function logic inside the hub, and 2 MB of cache |
| The power | 0.15 W at a working screen, 0.02 W on a static page |
| The latency of one keystroke | 3 to 8 ms, measured locally, with no network in the path |
| The latency of a scroll | 4 to 10 ms locally for a text surface |
| The limit | a photograph and a video are not rendered locally; they arrive as a stream. A page that needs the full layout engine of the network arrives as a stream or as a verified layout result. |
| The rule | the local scene renderer draws only what the network signed. It cannot display a local computation as a verified result. |

**The consequence for the user**. Typing, scrolling, the menus, the keyboard, the wallet and the cursor are instant, at any distance from the validator. The distance that remains is the distance of the *content*, not of the *use*. `[DECISION]`

---

## 3 · Mechanism 3 · The frame reprojection unit

The hub holds the last decoded video frame. The local motion of the finger or the inertial unit moves that frame at 144 Hz: a shift, a scale, a rotation. When the true frame arrives, it replaces the projection. `[DECISION]`

| Property | The value |
|---|---|
| The latency that it hides | 10 to 40 ms of the network and the encoder |
| The refresh of the reprojection | up to 144 Hz |
| The artefacts | the edges of the frame, which the unit fills from the previous frame, and a disocclusion after a large move |
| The limit | it is used for a scroll, a pan, a zoom and a tilt. It is not used across a scene cut. Gate DST-3 measures the artefacts, and the unit is disabled where the measured quality falls below the threshold. |
| The power | 0.08 W at 144 Hz with a moving image, 0.01 W on a static image |

---

## 4 · Mechanism 4 · The edge agent

**The network is live before the Leaf ships**. Budlum is already live as one validator ecosystem, and near services are a capability of that set. The Leaf needs no second system or separate seed program (Ayaz, questions 7 and 18). `[DECISION]`

**The near part of a session is served by a Budlum validator that the user can own**. `[DECISION]` (the answer of Ayaz, question 7: if separate hardware is bought, it already counts as a validator, because it registers with Budlum)

There is **no separate near node system**. Near services belong to the existing validator role, which the registry accepts via its open `u32` `RoleId`. `[TREE]` A validator that a household owns earns for the near work and carries a stake like any other.

| Property | The value |
|---|---|
| What it holds | the cache of static content, the document model of the local scene renderer, the video buffer, the input predictor, the relay path |
| What it does not hold | the user's data in the clear, a wallet key, a signing authority, or the ability to alter a verified result |
| The power class | 3 to 15 W, a mini computer or a small board with a network accelerator |
| The cost class | a small box in the home, or a shelf in a room of a community building |
| Who can run one | anyone: a user, a household, a shop, a community, an operator. The role is open and permissionless, like the relayer (`[TREE]` open `u32` `RoleId`) |
| The trust rule | the agent is not trusted; frames carry the staked validator hash, the input transcript is checked, and any altered frame is excluded |
| The reward rule | the agent earns for the near work: the cache hit, the buffer, the relay, the prediction |

### 4.1 The Leaf Dock is an edge agent

The stand that carries a Leaf 160 on a desk, and the rail that carries a Leaf 1400, have room for a small board. **The dock is the near node of that home**. `[DECISION]`

| The benefit | The number |
|---|---|
| The distance from the device to its near node | 0.2 to 2 m of radio, under 2 ms |
| The distance from the near node to the compute | any distance, and it stops mattering for the interaction |
| The user's independence | the user owns the near node, so the product does not depend on the site of a third party |
| The energy | the dock is on the mains, so the near work does not cost the cassette |

**This is the answer to the concern of Ayaz**. The product does not wait for a validator to be near. The near part is in the room, and the far part is verified. `[DECISION]`

---

## 5 · Mechanism 5 · The honest class ladder

| The case | Input to the eye | The text and the interface | The video | The 3D and the Field mode | The statement on the surface |
|---|---|---|---|---|---|
| The validator or the edge agent within 15 km | 2 to 6 ms | local | 20 to 45 ms of glass to glass, smooth | 20 to 45 ms | the full class |
| Within 200 km | 4 to 10 ms | local | 30 to 60 ms | 30 to 60 ms | the full class |
| Within 1 500 km | 6 to 14 ms | local | 40 to 90 ms, buffered | 60 to 120 ms, degraded | a note in the class line |
| Across a continent, 8 000 km and more, with an edge agent in the room | 2 to 8 ms | local | 40 to 90 ms, smooth, because the buffer and the agent absorb it | 40 to 70 ms with the reprojection unit | the full class for the interaction, and a video class note |
| Across a continent, with no edge agent | 8 to 20 ms | local | 150 to 300 ms: usable for a page and for a message, poor for a motion | not offered | the class line states the reduction |
| A satellite only | 25 to 60 ms | local | not offered | not offered | the message class |

`[PUBLICATION]` Light in fibre travels 200 km/ms, and a near validator at 10 to 15 km measures 1 to 5 ms. `[HYPOTHESIS]` for the glass to glass columns, which gate DST-5 measures in two markets.

**The rule**. The surface never promises a class that the path cannot carry. It states the class, and a reduction is visible to the user. `[DECISION]`

---

## 6 · What this changes in the program

| The item | The change |
|---|---|
| The hub | the hub H1 gains a **local scene renderer** and a **frame reprojection unit**, about 2 mm² of logic, 0.15 W and 0.08 W |
| The display transport (RG-3) | a new class **C0b: the document model**, beside the pixel classes. A page arrives as a model and, where it needs it, as a stream. |
| The session (RG-4) | a session names its edge agent, and a move between edge agents is a handoff with the same rules |
| The Budlum tree | **no new role and no new system**: near services belong to the validator role, and a user validator registers normally. Rule L5 holds |
| The Leaf Dock and the Leaf 1400 rail | **mains path by default and validator board as an option** (Q32): base price stays low, and households can add a validator board |
| The claim policy | the distance claim is a table, never a single number: the class per case, per market |

---

## 7 · The distance gates

| Gate | The test | The pass condition |
|---|---|---|
| DST-1 | the local scene renderer against a reference engine: a photograph of a text page, a table, a menu, in three languages | the difference is below the stated threshold, and a page cannot be faked as a verified result |
| DST-2 | the input to the eye time for a keystroke, a scroll and a tap | the values of Section 2, measured |
| DST-3 | the reprojection artefacts on a scroll, a pan, a zoom and a scene cut | the stated quality, and the automatic disable |
| DST-4 | a malicious edge agent: an altered frame, a replayed frame, a forged class | every case is detected and the agent is excluded |
| DST-5 | the glass to glass time in two markets: a near validator, a far validator with an edge agent, a far validator without one | the table of Section 5 |
| DST-6 | the class line on the surface in each of the six cases | the user sees the class, and a reduction is visible |
| DST-7 | the dock as an edge agent: a Leaf 160 at 1 m from the dock, the compute at 8 000 km | the interaction values of Section 5, and the video within the stated band |
| DST-8 | the energy of the distance work on a device: the renderer, the reprojection and the radio | each term measured, and the sum inside the accounting of Volume II, Section 5 |

---

## 8 · The one sentence of this volume

**The device answers instantly locally, the network answers correctly by verification, and a user-owned validator joins the two**. `[DECISION]`
