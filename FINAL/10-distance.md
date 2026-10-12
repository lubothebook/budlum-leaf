# BUDLUM LEAF · THE DIRECTIVE · PART 10 · THE DISTANCE DOCTRINE

**The order that created this part**. *Everything runs on the validator, and the far validator case must be solved so distance is not a problem*. `[DECISION]`

---

## 10.1 The two-budget rule

| The budget | What it covers | The time | Where it is served | Does the distance matter |
|---|---|---|---|---|
| **The interaction budget** | the input echo, the cursor, the drag, the typing, the menu, the wallet, the gaze pointer | under 10 ms | **inside the device** | **no** |
| **The processing budget** | the finished photograph, the re-encode, the full layout, the answer of a model, the search | 1 s to 60 s | **anywhere on the network** | **no** |

**The rule**. A function is judged against the budget that the human sense uses. The eye tracks motion, so the interaction budget is hard. Nobody watches a photograph being developed, so the processing budget is soft. **Putting a photograph on the interaction budget was the error, not the validator**. `[DECISION]`

---

## 10.2 The five mechanisms that make distance irrelevant

| No. | The mechanism | What it removes from the network path | The remaining latency | The gate |
|---|---|---|---|---|
| 1 | **the local floor** | the input echo, the cursor, the wallet approval, the safe screen | zero | SW-4, MEC-9 |
| 2 | **the local scene renderer** | text, the interface, lists, the keyboard, the buttons, the menus | zero | DST-1, DST-2 |
| 3 | **the reprojection unit** | the delay of a scroll, a pan, a zoom, a tilt | zero to 8 ms | DST-3 |
| 4 | **the near validator** | the near part of the session: the cache, the composition, the buffer, the relay | 1 to 5 ms, wherever the user is | DST-4, DST-5 |
| 5 | **the honest class ladder** | nothing: it states where the fidelity falls, visibly | stated | DST-6 |

### 10.2.1 The local scene renderer, in detail

The network does not send pixels for an interface. It sends a **document model**: a signed, versioned display list of text runs, shapes, image references, colours and a difference against the acknowledged version. The hub renders it locally at 144 Hz.

| The property | The value |
|---|---|
| The parts | a glyph cache, a vector fill, an alpha blend, an image blit, a colour engine |
| The silicon | about 2 mm² of fixed function logic in the hub, and 2 MB of cache |
| The power | 0.15 W at work, 0.02 W on a static page |
| A keystroke | 3 to 8 ms, measured locally, with no network in the path |
| A scroll | 4 to 10 ms locally for a text surface |
| The limit | a photograph and a video are not rendered locally; they arrive as a stream |

### 10.2.2 The reprojection unit, in detail

The hub holds the last decoded video frame and shifts, scales, or rotates it locally at up to 144 Hz. When the true frame arrives it replaces the projection. The latency that it hides is 10 to 40 ms. Artefacts appear at frame edges after a large move, so reprojection stops below the quality threshold. It never runs across a scene cut.

### 10.2.3 The near validator

| The property | The value |
|---|---|
| What it holds | the cache of static content, the document model, the video buffer, the input predictor, the relay path |
| What it does not hold | the user's data in the clear, a wallet key, a signing authority, the ability to alter a verified result |
| The power class | 3 to 15 W, a mini computer or a small board |
| Who runs one | **anyone, as a Budlum validator**: it registers, it earns and it stakes like any other. There is no separate near node system `[DECISION]` (the answers of Ayaz, questions 7 and 18) |
| The trust rule | the frames carry the hash of the staked validator, and the input transcript is checked; an agent that alters a frame is detected and excluded |
| The dock and the rail | they carry a mains path by default and a **validator board as an option** (the answer of Ayaz, question 32) |

---

## 10.3 The nine far-validator mechanisms

| No. | The mechanism | The number |
|---|---|---|
| 1 | **The split**: the device and the module deliver a complete image; the validator delivers the reference | the local provisional pipeline reaches 60 to 75 percent of the final quality |
| 2 | **Provisional first**: the local image is stored at once and labelled `local provisional`; the validator result replaces the view and the record keeps both | the user is never without a photograph |
| 3 | **A deadline class per job**: interactive still at 5 s, standard still at 60 s, or deferrable job waiting for a good link | stated before the shutter |
| 4 | **Job mobility**: a render job is checkpointed and can be picked up by a nearer validator or by the user's own later. The pipeline is deterministic and signed, so the result is identical | RG-4 |
| 5 | **The validator in the room**: the dock, the stand or the rail can carry a validator board | Volume 4-B, and the answer of Ayaz, question 32 |
| 6 | **Predictive prefetch and cache**: the working set lives near the user; the far validator computes only new work | the renderer and the agent |
| 7 | **Deferrable scheduling**: a job of the class "no hurry" rides the cheap path and the idle capacity | the night burst |
| 8 | **The optical and the no-link path**: a signed receipt or a small payload as optical frames | RG-12 |
| 9 | **The class statement per market**: no global latency figure; the measured class of each market, and every reduction visible | DST-5, DST-6 |

### 10.3.1 The answer in one paragraph

**The far validator is not a problem because the user never waits for it**. The user touches, and the device answers in a few milliseconds from a renderer inside the device. When the user takes a photograph, a local provisional image exists immediately at three-quarters quality. The finished validator image arrives later, as stated before the shutter. A live conversation with a large model uses a near validator and streams at the delta class. `[DECISION]`

---

## 10.4 The class ladder, with the numbers

| The case | The input to the eye | The text and the interface | The video | The 3D and the Field | What the surface states |
|---|---|---|---|---|---|
| a validator or a near node inside 15 km | 2 to 6 ms | local | 20 to 45 ms glass to glass | 20 to 45 ms | the full class |
| inside 200 km | 4 to 10 ms | local | 30 to 60 ms | 30 to 60 ms | the full class |
| inside 1 500 km | 6 to 14 ms | local | 40 to 90 ms, buffered | 60 to 120 ms, degraded | a note in the class line |
| across a continent, with a near node | 2 to 8 ms | local | 40 to 90 ms, smooth | 40 to 70 ms | the full class for the interaction, a video note |
| across a continent, no near node | 8 to 20 ms | local | 150 to 300 ms: a page and a message are usable, a motion is poor | not offered | the reduction |
| a satellite only | 25 to 60 ms | local | not offered | not offered | the message class |

`[PUBLICATION]` Light in fibre travels about 200 km per millisecond. A near validator 10 to 15 km away is 1 to 5 ms, and a central cloud is 50 to 100 ms. `[HYPOTHESIS]` The glass to glass columns, measured by gate DST-5 in two markets.

---

## 10.5 What must be built for this doctrine

| No. | The item | The owner | The gate |
|---|---|---|---|
| 1 | the local scene renderer and the reprojection unit in the hub | the firmware line | DST-1 to DST-3 |
| 2 | the local provisional camera pipeline in the module | the camera line | CAM-9 |
| 3 | the job object: a deadline class, a checkpoint, a mobility rule | the network line | RG-4 |
| 4 | the state words on the surface: `local`, `near`, `far`, `deferred` | the surface line | DST-6 |
| 5 | the market measurement in two cities | the verification line | DST-5 |

---

## 10.6 The distance gates

| Gate | The test | The pass condition |
|---|---|---|
| DST-1 | the local scene renderer against a reference engine: a text page, a table, a menu, in three languages | the difference is below the stated threshold, and a page cannot be faked as a verified result |
| DST-2 | the input to the eye time for a keystroke, a scroll and a tap | the values of Section 10.2.1, measured |
| DST-3 | the reprojection artefacts on a scroll, a pan, a zoom and a scene cut | the stated quality, and the automatic disable |
| DST-4 | a malicious near validator: an altered frame, a replayed frame, a forged class | each case is detected and the node is excluded |
| DST-5 | the glass to glass time in two markets: near, far with a near node, far without one | the table of Section 10.4 |
| DST-6 | the class line in each of the six cases | the user sees the class, and a reduction is visible |
| DST-7 | the dock as a near validator: a Leaf 160 at 1 m from the dock, the compute 8 000 km away | the interaction values of Section 10.4, and the video inside the stated band |
| DST-8 | the energy of the distance work: the renderer, the reprojection, the radio | each term measured, and the sum inside the accounting of Part 4 |
