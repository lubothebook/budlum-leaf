# BUDLUM LEAF · MASTER DIRECTIVE · VOLUME IX · THE CAMERA MODULE AND THE PROCESSING SPLIT

**Version:** 4.2 (revision D) · the answer to the question of Ayaz. *80 MP, three cameras side by side: does the 4 mm hold, where does the processing run, and does the hardware get hot*?

**The standing at Revision L.5.0, of 2026-10-12**. This volume answers the question of revision D about a **module with three cameras**. That module was replaced by **the `90°`-bent-stem Budlum B module of Revision L.5.0** (`20.0 g`, `32` parts, `uploads/b.png` 1:1). Only its stem (`USB-C` + antenna) bends `90°` along any of the 4 edges. Its `Ø32 mm` ring (`50 MP` camera + rear AMOLED + Zero-CPU SiP) lies flat on the screen (`+Z` or `-Z`). Rows below that name three cameras or a 20 Wh module cell are **struck**; see `HARDWARE/05`, `HARDWARE/13`, and `HARDWARE/20`. What survives from this volume is the **processing split of Section 3** and the rule that uplink wait is stated before the shutter. `[DECISION]`

---

**The live numbers, in one table**.

| The item | At revision D | At Revision L.5.0 |
|---|---|---|
| the camera | three folded stacks of 80 MP in a 4.00 mm module | **`90°`-bent-stem B module (`20.0 g`, `32` parts)**: fixed front camera (`17.4 mm` folded, `f/1.8`) inside the flat `Ø32.0 / Ø24.0 mm` ring |
| the sensor | 80 MP, 1/1.4 in class | **50 MP daylight and 12.5 MP everyday**, 1 inch class (`12.8 x 9.6 mm`) |
| the energy of the camera | a 20 Wh cell in the module | **`0.45 Wh` solid-state bridge cell in the B ring**, for standalone capture and the rear round AMOLED. The main phone energy is the **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`, `68 g`) 4-Quadrant (`+`) `LLZO/PEO` solid-state screen body** |
| the placement | the module covers a face | **only the stem (`8 x 32 mm`) bends `90°`** on 4 edges; the **`Ø32 mm` ring lies flat on screen (`+Z / -Z`)** |
| the claim | three lenses | **one lens and a crop**, with no optical zoom, stated plainly |

---

## 1 · The three answers in one table

| The question | The answer |
|---|---|
| Does the 4.00 mm device thickness hold with three cameras? | **The question is retired**. The camera is **the Budlum module** of `HARDWARE/20`: one **fixed Ø22.0 mm camera** inside the ring, folded into 3.40 mm. The device stays 4.00 mm and so does the module |
| Where does the processing run? | **In three zones**: sensor silicon (readout, binning, HDR), module sentinel (remosaic, compression, focus, motion), and **validators** (stacking, denoise, HDR, depth, super-resolution). The viewfinder stays local |
| Does it get hot? | **The heat is bounded by the split, and it is the part that carries it**. A still burst is 2 to 3 W for two seconds. A sustained 4K120 video is 2.5 to 3 W, which needs a stated derate. The heavy compute is not on the module, so the module never becomes a hot brick |

---

## 2 · The geometry of three cameras in one 3 mm module

### 2.1 The module

| Property | The value |
|---|---|
| The footprint | 150 by 74 mm inside the 160 by 80 mm leaf, so it does not cover the antenna windows or the pen magnet zone |
| The thickness, fixed | **4.00 mm** (Q26: the module is 4.00 mm thick, flush with the 4.00 mm body) |
| The arrangement | Revision D placed three cameras side by side (`150 x 74 mm`); Revision L.5.0 places one fixed camera inside the `90°` B module ring |
| The fallback ladder | 4.0 mm with three folded optics · 5.5 mm with two folded and one conventional · 6.5 to 7 mm with three conventional stacks |
| The mass | 80 to 88 g with the cell, the connector and the three cameras |
| The cell inside the module | **20 Wh nameplate, 16 Wh effective** (the answer of Ayaz, question 26) |

### 2.2 The optics, one camera at a time

A conventional stack grows along the optical axis, so its height equals lens diameter plus sensor. A folded stack turns the axis sideways with a prism, so the focal length runs across the module.

| Camera | The role | The optical path | The stack height | The sensor |
|---|---|---|---|---|
| 1 · the main, and the only one at revision L.4.0 | the light, the everyday photograph | folded, **28.4 mm equivalent** | 3.40 mm in the ring, folded **17.4 mm** | **50 MP daylight, 12.5 MP everyday**, 1 inch class, 12.8 by 9.6 mm |
| 2 · the wide | the room, the group, the landscape | folded, a 15 mm equivalent | 3.5 mm | 80 MP, 1/2.5 in class |
| 3 · the long | the far, the portrait | folded, a 90 to 120 mm equivalent, a periscope of four folded passes | 3.5 mm | 80 MP, 1/2.5 in class |

**The rule that makes 4.0 mm possible**. Every camera is folded, and the three 9 mm barrels sit side by side across 27 mm of the 74 mm width. Each prism needs 12 mm of depth. A folded stack keeps the height at 3.5 mm and the module shell adds 0.5 mm. `[HYPOTHESIS]` The real design is the work of the optical partner, and gate CAM-1 replaces this table with a drawing and a measurement.

### 2.3 The 4 mm claim stays true

```
the leaf alone                     4.00 mm   (the fixed answer of Ayaz)
the module alone                   4.00 mm   (the answer of Ayaz, question 26)
the leaf with the module attached  8.00 mm   (a stack that the user removes in one action)
```

**The rule**. Any product sentence about thickness names the part. "The device is 4 mm" means **the leaf alone**, and the module is a separate, removable part. A sentence that hides the module and claims 4 mm for the stack is a defect of the claim policy. `[DECISION]`

---

## 3 · The processing split, in three zones

### 3.1 Zone 1 · The sensor and its immediate silicon

| The work | The hardware | The power |
|---|---|---|
| the readout of 80 MP at 12 bit | the sensor, stacked with a small logic die | 0.20 to 0.25 W per camera in a still capture |
| binning to a 2 MP or a 5 MP preview | the sensor logic | inside the same budget |
| the black level, the defect map, the lens shading | the sensor logic, with the calibration of the record | |
| a two frame HDR merge | the sensor logic | |
| the mechanical and the optical stabilisation | the actuator and the gyro | 0.05 to 0.15 W |
| **the rule** | **no operating system, no user code, no writable firmware on the module beyond a signed update** | |

### 3.2 Zone 2 · The sentinel block on the module

| The work | The note |
|---|---|
| the remosaic of the 80 MP quad pattern into a Bayer or an RGB frame | a fixed function block |
| the compression of the capture to a 10 bit intra stream | about 8 to 40 MB per still, 2 to 6 Mbit per preview frame |
| the focus stack, the gyro timeline and the motion metadata | the payload that the validators need for a good result |
| the frame selection of a burst | 8 to 30 frames, ranked locally, so the uplink carries the useful ones |
| the video encode, 4K120 and 4K60 | 1.2 to 2.0 W, the largest single term of the module |
| **the rule** | the sentinel **cannot** invent a result, cannot paint an image and cannot sign a photograph as a verified inference. It prepares a payload |

### 3.3 Zone 3 · The validators

| The work | The note |
|---|---|
| multi frame stacking, denoise, deblur | the computational photograph, at the effort tier that the user pays for |
| the portrait depth, the semantic masks, the relight | the models of the operator, under the perception lease |
| the super resolution and the tone mapping | the final image |
| the archive, the search and the recall | B.U.D., under the user authority, with Pollen in the read path |
| the verification | every processed image carries the operator identity, the model identity and the effort tier in its record |

**The latency classes of a photograph**. `[HYPOTHESIS]` gate CAM-4 measures all four.

| The case | What the user sees | The uplink | The time |
|---|---|---|---|
| a preview | local, 2 MP at 30 frames per second, never leaves the device | 0 | instant |
| a fast still, small | a locally tone mapped image, replaced when the processed one arrives | 3 to 8 MB | 1 to 3 s on a near validator |
| a full still, 80 MP | the printed preview with a progress mark, then the full image | 8 to 40 MB | 2 to 6 s near, 10 to 30 s far |
| a night burst, 20 frames | the same, with the mark | 200 to 500 MB | 20 to 90 s near, minutes far, and it is stated before the capture |
| a 4K120 video | local encode, the stream stored in B.U.D. | 30 to 80 Mbit/s sustained | live |

**The rule of the honest camera**. A capture that needs a long uplink says so **before** the shutter, with the time and the class on the screen. A camera that hides the wait is a defect. `[DECISION]`

---

## 4 · The heat

### 4.1 The terms

| The case | The sensor set | The sentinel | The radio | The total | The time |
|---|---|---|---|---|---|
| the viewfinder only | 0.15 W | 0.25 W | 0.05 W | 0.45 W | continuous |
| one still, 80 MP, three cameras metered | 0.75 W | 0.60 W | 0.30 W | 1.65 W | 0.5 s |
| a night burst of 20 frames | 0.75 W | 0.90 W | 1.20 W | 2.85 W | 2 to 4 s |
| a 4K60 video | 0.60 W | 1.30 W | 0.60 W | 2.50 W | continuous |
| a 4K120 video | 0.80 W | 2.00 W | 1.20 W | 4.00 W | continuous, derated |

### 4.2 The thermal answer

1. The module face is 150 by 74 mm (`111 cm²`) and couples to the leaf heat spreader. A burst of 2.85 W over 111 cm² is 0.026 W/cm², so the rise is a few degrees. `[GENERAL]`
2. Sustained 4K120 video at 4.0 W has a 15-minute limit before derating to 4K60, with state shown on screen. `[HYPOTHESIS]` gate CAM-6 measures the curve on a real module.
3. The module holds its own cell behind an internal thermal wall, sparing the battery contacts from camera heat. The cell temperature limit is respected by the layout, and gate CAM-6 records both temperatures.
4. **The heavy compute is not here**. Computational photography needs hundreds of giga-operations, which would demand 5 to 15 W locally. Validators run that workload so the camera fits in a 4 mm part. Volume XIV, Sections 2 and 3 cover the burst thermal path and local provisional preview.

---

## 5 · The camera and the rules of the program

1. **The hardware minimum of the device is unchanged**: the leaf has no camera, and the camera lives in the module. A Leaf without a module is a complete product for everything except a photograph. `[DECISION]`
2. **The module declares its sensor state**. A hardware indicator and a signed secure-element declaration prevent software from faking or hiding camera state. `[DECISION]` RG-5.
3. **The camera works only under a perception lease**: the purpose, the model, the frame classes, the expiry and the retention. Four fail-closed cases. RG-5.
4. **A photograph is data in B.U.D.** under user authority, recording the operator, model and effort tier. `[TREE]`
5. **The pen magnet and the camera magnets are one design problem**. No magnet sits within 8 mm of the optical stabiliser, and the pen docks on the side rail. Gate CAM-7.
6. **The module is renewable**. A new module on an old leaf is a supported configuration, and the record carries the pair. `[DECISION]`

---

## 6 · The camera gates

| Gate | The test | The pass condition |
|---|---|---|
| CAM-1 | the optical design: **6 elements in 4 groups on a folded path of 17.4 mm inside 3.40 mm** | drawing, measured MTF, CRA under 25 degrees, and gate CAM-3 of `HARDWARE/05`; fallback ladder invoked with written reason if it fails |
| CAM-2 | the sensor set: 80 MP readout, binning, the HDR merge, three cameras metered in one capture | the power, the time and the image quality of Section 3.1 |
| CAM-3 | the sentinel: remosaic, compression, the focus stack, the metadata | the payload sizes of Section 3.2, and no invented result |
| CAM-4 | the four latency classes of Section 3.3 | the times, on a near and a far validator |
| CAM-5 | the lease and the sensor declaration: the four refusals, the hardware light, the record | all six behave as specified |
| CAM-6 | the heat: the table of Section 4.1, the 15 minute rule, the cell temperature | the curve, the derate, and a cell inside its limit |
| CAM-7 | the magnets: the pen dock, the joint's sixteen poles and the stabilisers | the image quality of the module holds with the pen attached |
| CAM-8 | a new module on an old leaf, and a lost module revoked | both behave as specified, with the record updated |
