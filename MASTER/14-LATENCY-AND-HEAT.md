# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME XIV · THE LATENCY AND HEAT DOCTRINE

**Version:** 4.3 (revision E) · the answer to two questions of Ayaz. *Everything runs on the validator, and how do we solve the far validator and prevent heating*?

---

## 1 · The two-budget rule

**A session has two budgets, and they are different kinds of budget**. Every latency problem in this program disappears when they are separated. `[DECISION]`

| The budget | What it covers | The time | Where it is served | Does the distance matter |
|---|---|---|---|---|
| **The interaction budget** | the input echo, the cursor, the drag, the typing, the menu, the wallet, the gaze pointer | under 10 ms | **inside the device**: the local scene renderer, the reprojection unit, the local floor | **no**. The network is not in the path |
| **The processing budget** | the finished photograph, the re-encoded video, the full layout, the answer of a model, the search | 1 s to 60 s | **anywhere on the network**: a queued, checkpointed job | **no**. Only the arrival time changes, and the arrival time is stated |

**The rule of the program**. A function is judged against the budget that the human sense uses. The eye tracks motion, so the interaction budget is hard. Nobody watches a photograph being developed, so the processing budget is soft. **Putting a photograph on the interaction budget was the error, not the validator**. `[DECISION]`

---

## 2 · The far-validator solution set, nine mechanisms

| No. | The mechanism | The number |
|---|---|---|
| 1 | **The split**: the device and the module deliver a complete image; the validator delivers the reference image | local provisional pipeline reaches 60 to 75 percent of final quality (demosaic, 2-frame HDR, tone map, denoise) `[HYPOTHESIS]` gate CAM-9 |
| 2 | **Provisional first**: the local image is stored at once as `local provisional`; the validator result replaces the view while keeping both | the user is never without a photograph |
| 3 | **A deadline class per job**: interactive still (5 s), standard still (60 s), or deferrable job (night shots, re-encode) | the class is shown before the shutter |
| 4 | **Job mobility**: a render job is checkpointed and can be picked up by a nearer validator or the user's validator later | RG-4 (deterministic signed pipeline) |
| 5 | **The validator in the room**: the dock, the stand or the rail can carry a validator board owned by the user | Volume IV-B, Section 4 |
| 6 | **Predictive prefetch and cache**: the working set lives near the user, and the far validator computes only new work | the local renderer and the agent |
| 7 | **Deferrable scheduling**: a job with a class of "no hurry" rides the cheap path and the idle capacity | the night burst of Volume IX |
| 8 | **The optical and the no-link path** for the extreme case: a signed receipt or a small payload as optical frames | RG-12, 240 QR frames for a signature class payload |
| 9 | **The class statement per market**: the product states the measured latency class of each market, and any reduction is visible | DST-5, DST-6 |

### 2.1 The answer in one paragraph

**The far validator is not a problem because the user never waits for it**. The user touches, and the device answers in a few milliseconds, from a renderer that lives inside the device. The user takes a photograph, and the photograph exists at once, locally, at three quarters of its quality. The finished image arrives later from the far validator, and the surface said so before the shutter. A live conversation with a large model uses a near validator and streams at the delta class. `[DECISION]`

### 2.2 What the program must build for this

1. The local scene renderer and reprojection unit in the hub (Volume I, Section 3.4; Volume IV-B, Sections 2–3).
2. The local provisional camera pipeline in the module (Volume IX, Section 3.2, extended).
3. The job object: a deadline class, a checkpoint, a mobility rule (RG-4 extended).
4. The class line and the state words on the surface: `local`, `near`, `far`, `deferred`.
5. The market measurement: two cities, two validator distances, the class of each (DST-5).

---

## 3 · The heat solution set, twelve mechanisms

### 3.1 The numbers

| The surface | The area | A 4 W load | The rise |
|---|---|---|---|
| the module face | 111 cm² | 0.036 W/cm² | the hot part: 10 to 18 °C above ambient without a spreader |
| the leaf, both faces | 256 cm² | 0.016 W/cm² | 3 to 6 °C above ambient |
| the leaf plus the module, coupled | 367 cm² | 0.011 W/cm² | 2 to 4 °C above ambient |

**The conclusion**. The leaf is an excellent radiator because it is large and thin and it has two faces. **The engineering problem is not the total heat; it is the local hot spot in the module**. `[DECISION]`

### 3.2 The mechanisms

| No. | The mechanism | The note |
|---|---|---|
| 1 | **Keep the heavy compute off the module** | computational photography needs 5 to 15 W; keeping heavy compute on the validator prevents a 60 °C module surface |
| 2 | **A spreader inside the module**: a 30 to 50 µm graphite or annealed copper layer under the sensors, bonded to the shell | the measured path, gate MEC-11 |
| 3 | **A thermal bridge at the module interface**: soft thermal pad between the module and the leaf spine, under 3 K/W | so the module's heat enters the leaf, which is 2.3 times its area |
| 4 | **A latent buffer**: 1 to 4 g of an encapsulated phase change material inside the module shell absorbs a burst | about 200 J per gram: a 4 W burst of 60 s is 240 J, so 1.2 g covers a take |
| 5 | **The cell away from the sensor block**: a gap band and thermal wall inside the module, with cell temperature logged | the cell is not heated by the camera |
| 6 | **Sensor-side power reduction**: binning and line skipping in video, an in sensor HDR merge, a lower readout rate where the class allows | a 4K120 readout with binning costs about 0.15 W per camera against 0.25 W in a full readout `[HYPOTHESIS]` |
| 7 | **The encode moves to the hub where the class allows** | sentinel compresses lightly (3:1 to 6:1) and the hub does full encode, spreading heat across the body (`2-4 Gbit/s` link) |
| 8 | **Duty and rate rules**: 4K120 take up to 10 s with 20 s cooldown, or 15 min cap with 4K60 derate | the answer to the question 29 of Ayaz: the derivative rule is measured, and a stated state appears on the surface |
| 9 | **A temperature-aware capture policy**: the camera refuses a 4K120 start above a stated module temperature, and it says why | the same honesty rule as the uplink wait |
| 10 | **A dark frame recalibration on the sensor temperature**, with the temperature in the record | a hot sensor drifts; the record carries the number |
| 11 | **Air and light rules of the surface**: no insulating layer over the panel; the module shell is matte, high-emissivity | a matte dark surface radiates better than a gloss |
| 12 | **The sun is not an enemy** | the leaf in the shade with a bright scene is normal use; gate MEC-11 tests at 35 °C ambient |

### 3.3 The heat gates

| Gate | The test | The pass condition |
|---|---|---|
| MEC-11 | the module thermal path: the spreader, the interface pad, the latent buffer, 35 °C ambient, five capture classes | the module rise, the leaf rise and the cell temperature, all inside their limits |
| MEC-12 | the capture policy: a hot start, a long take, a cooldown, the message | the refusal works and the user sees the reason |
| CAM-9 | the local provisional pipeline against the validator reference: a day shot, a night shot, a document | the local image is at least 60 percent of the reference quality, and it is labelled |

---

## 4 · The corner, softened

The answer of Ayaz, question 30: **when a thumb touches a corner diagonally, the touch must not land on a point**. The rule is written mechanically.

| The item | The value | The reason |
|---|---|---|
| The corner radius | **`R = 6.35 mm` on the carried member (`32` in `0.1 mm` design units)**, scaled proportionally on larger members | keeps the screen rectangular while eliminating sharp corner points |
| The 12 prism edges | **`r = 0.80 mm` fillet** on all 8 horizontal face-to-side edges plus the 4 `R = 6.35 mm` vertical corners | no sharp 90 degree angle, no point, and no edge that feels harsh in the hand |
| The touch layer at the corner | the mesh follows the corner with an expanded electrode pattern, and the corner region carries a palm and grip rejection rule | a diagonal grip is not misread as a swipe, and a deliberate corner tap still works |
| The visual corner | the panel is cut inside the same curve, so the picture and the body have one outline | the soft corner is a property of the product, not of the cover |
| The test | a diagonal grip set on 20 users, in a pocket, in a hand and in a bag | gate MEC-13: no accidental input, and no corner tap missed |

---

## 5 · What the two doctrine sections change in the other volumes

| The volume | The change |
|---|---|
| I, Section 7 | the power table gains a column of the class state: `local`, `near`, `far`, `deferred` |
| II, Section 4.6 | the pen, the module and the bridges gain the thermal bridge of Section 3 |
| IV-B | the class ladder gains the deadline classes of Section 2 |
| IX | the camera gains the local provisional pipeline, the deadline class and the capture policy |
| X | the firmware gains the job object, the class words and the capture policy state machine |
| XIII | Field mode gains the thermal note: a long film runs both faces at video class and states the thermal limit |
