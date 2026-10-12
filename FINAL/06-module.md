# BUDLUM LEAF · THE DIRECTIVE · PART 6 · THE 90°-BENT-STEM B MODULE, THE SOLE USB-C PORT, THE PEN AND THE SOUND

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. Part 21 and `HARDWARE/05` define the B module. It is `4.00 mm` thick with a `1.00 mm` LCP bar on the top edge and no hinge. The `50 MP` camera sits in a vertical column, and the `3.5 mm` jack in the rim. USB-C is a separate part.

**The standing of this part at Revision L.5.0, of 2026-10-12**. Modeled 1:1 from `uploads/b.png` (`20.0 g`), **only the stem (`çubuk`, `8 x 32 x 4.5 mm`) bends at a `90°` right angle (`dik açıyla`)**. Its **circular ring (`yuvarlak`, `32 x 32 x 4.0 mm`) lies flat on top of the screen**. Moving the `90°`-bent stem around the 4 edges docks the B module to the **Front (`+Z`) or Back (`-Z`)** of the screen.

| The item | The state at Revision L.5.0 |
|---|---|
| the camera | **fixed inside the upper Z-stack (`z = 0.90..3.60 mm`)** of the flat `Ø32.0 / Ø24.0 mm` ring lying on the screen (`HARDWARE/05`, `13`, `20`) |
| the ports | **zero USB-C and zero buttons on the screen body** (`Qi2.2` wireless charging). **The sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`) lives inside the `90°`-bent B stem** (`HARDWARE/04`, `14`) |
| the cells | **`12.0 Wh` (`3 200 mAh`) `LLZO/PEO` solid-state battery** across `Q1..Q4` (`68.0 g`) + **`0.45 Wh` bridge cell** in the B ring (`HARDWARE/11`) |
| the processing split | **Zero-CPU thin-client architecture**: `U1` Master TCON + `U2` `UWB / mmWave` SiP in the 6L B ring PCBA; compute runs on validators (`Section 6.3`) |
| the heat of Section 6.4 | `1.4 W` capture heat in the B module is isolated from the rear AMOLED by a `0.15 mm` (`1 200 W/m·K`) Cu-graphite mid-plane shield |
| the magnets and docking of Section 6.5 | `24` N52H + `64` gold leaves join `+` (`<15 µm` seam); `8` N52H (`7.2 N`) + `12` pins dock the `90°` B stem |
| the pen of Section 6.6 | **stays valid**, and it docks magnetically along the side edge |
| the sound set of Section 6.7 | **in-ring dual MEMS mics (`68 dB` SNR) and `9.0 x 3.2 x 2.2 mm` speaker (`78 dB`)** inside the flat B ring (`HARDWARE/13`) |
| the gates of Section 6.8 | the **CAM-1 to CAM-20 family of `HARDWARE/05-B-MODULE-CAMERA-AND-PANEL.md`** and **MON-1 to MON-20 of `HARDWARE/20-THE-BUDLUM-MONOGRAM.md`** |

**The rule of the retirement**. A claim about the retired module is struck, and the replacement is named. The sections below keep their text until the next block re-issues them. Every row that names three cameras, a 20 Wh cell or a bulky bottom battery pack is **struck**. `[DECISION]`

---

## 6.1 The retired module, and the Revision L.5.0 architecture

**This section is re-issued**. The bulky external bottom battery pack is cancelled. The **`2.00 mm` (`68 g`) body** splits across `+` into **four `17 g` solid-state quadrants (`Q1..Q4`, `12.0 Wh`, `Qi2.2`)**. The **`90°`-bent-stem B module (`20.0 g`, 32 parts)** bends only its stem (`USB-C` + antennas) by `90°` along any of the 4 edges. Its circular ring (`50 MP` camera, rear `Ø22.4 mm` AMOLED, `U1` TCON, `U2` `UWB / mmWave` SiP) lies flat on the screen (`88.0 g` total).

| The property | The value at Revision L.5.0 |
|---|---|
| the thickness | each of the 4 screen-battery quadrants (`Q1..Q4`) is **`2.00 mm`** (`68.0 g` total). The flat B ring is **`4.00 mm`** (`r = 0.55 mm`) and its `90°`-bent stem is `8.0 x 32.0 x 4.50 mm` |
| the camera | **one** 1-inch-class sensor (`12.8 x 9.6 x 0.65 mm`, `50 MP`), **fixed inside the upper Z-stack (`z = 0.90..3.60 mm`)** of the flat ring (`HARDWARE/05`) |
| the rear panel & acoustics | **no rotating parts**. Lower Z-stack (`z = 0.00..0.90 mm`) holds the **`0.15 mm` shield**, **`Ø22.4 mm` round LTPO AMOLED** (`480 x 480 px`), and `0.35 mm` sapphire |
| the cells & `<3 s` Hot-Swap | the 4 quadrants hold **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) `LLZO/PEO` cells** (`<3 s` swap per `EU 2023/1542` Art. 11), and the B ring holds a **`0.45 Wh`** bridge cell |
| the identity | every `+` seam quadrant and the `90°` B module answer a cryptographic Dead-Pad challenge in **3 ms** before power switches on |
| the mass | **17 g** per quadrant (`68 g` 4-Quadrant body) and **88 g** complete with the `20 g` `90°`-bent-stem B module |
| the rows struck | all legacy rotating-barrel, 317-dot matrix, and bulky bottom battery pack designs are permanently removed. `HARDWARE/20`, `HARDWARE/13`, `HARDWARE/15` and `HARDWARE/05` specify the live hardware |

---

## 6.2 The one camera, and what happened to the other two

**One lens does the work of three, and the crop does the rest**. The order of Ayaz asks for **one large round camera instead of three**. The three folded stacks of revision L.2 are therefore struck, and the single fixed camera of the module takes their place. `[DECISION]`

| The role that the three cameras covered | What covers it at revision L.3 |
|---|---|
| the light, the everyday photograph | the 1 inch class sensor at **f/1.5**, with **5.2 times** the light collecting area of the standard phone sensor |
| the room, the group, the landscape | the **66 degree** diagonal field of the 10.5 mm lens, which is **28.4 mm equivalent** |
| the far, the portrait | the **crop**: 2 times keeps 12.5 MP at **56.8 mm equivalent**, and 3 times keeps 5.6 MP at 85.2 mm |
| the self portrait | the **panel**: the camera looks forward, the round AMOLED on its back shows a live preview, and the user frames with the main lens |

**The honest reading**. A crop is not a telephoto lens, and the program says so. What the single fixed camera buys is a larger sensor, more light and one lens to certify. What it costs is the optical zoom, and that cost is accepted and recorded in Part 20, Section 20.3.4. `[DECISION]`

**Why folded optics are the answer**. A straight stack grows along the optical axis, so its height becomes the focal length. A folded stack turns the axis with a prism, and the path runs across the plate. That is how 17.4 mm of path stands inside 3.40 mm. `[DECISION]` gate CAM-1 and gate CAM-3 replace this with a drawing and a measurement.

**Why the path folds, and where it runs**. The module folds its optical path inside the ring: **3.4 mm in and 14.0 mm across**. That puts **17.4 mm of optical path inside 3.40 mm of depth**. A straight path of 16.0 mm cannot stand in a body of 4.00 mm, so the prism is not a preference. It is the only geometry that fits. The eight elements sit in four groups, and two of them are aspheres. `[DECISION]` **The fallback ladder**: if the partner cannot hold 8 elements in 3.40 mm, a 6-element path fits the same 4.00 mm ring.

---

## 6.3 The processing split, in three zones

### 6.3.1 Zone 1: the sensor and its immediate silicon

| The work | The power |
|---|---|
| the readout of 50 MP at 12 bit | 0.20 to 0.25 W in a still |
| the binning to a 12.5 MP everyday frame and a 2 MP preview | inside the same budget |
| the black level, the defect map, the lens shading | the calibration comes from the record |
| a two frame HDR merge | in the sensor logic |
| the mechanical and the optical stabilisation | 0.05 to 0.15 W |

**The rule**. Zone 1 has no operating system, no user code and no writable firmware beyond a signed update.

### 6.3.2 Zone 2: the sentinel on the ring board

| The work | The number |
|---|---|
| the remosaic of the quad pattern | a fixed function block |
| the compression of a capture to a 10 bit intra stream | 12 to 30 MB per still, and 8 MB at 12.5 MP |
| the focus stack, the gyro timeline, the motion metadata | the payload the validators need |
| the frame selection of a burst | 8 to 30 frames ranked locally |
| the video encode, 4K120 | 1.2 to 2.0 W, the largest single term. 8K is coded in the part, and the link never sees raw 8K |

**The rule**. The sentinel **prepares a payload**; it cannot invent a result, cannot paint an image, and cannot sign a photograph as a verified inference.

### 6.3.3 Zone 3: the validators

| The work | The note |
|---|---|
| multi frame stacking, denoise, deblur | the computational photograph at the paid effort tier |
| the portrait depth, the semantic masks, the relight | the operator models under the lease |
| the super resolution and the tone mapping | the final image |
| the archive, the search, the recall | B.U.D., under the user authority, with Pollen in the read path |
| the verification | the operator, the model and the tier are in the record |

### 6.3.4 The four latency classes of a photograph

| The case | What the user sees | The uplink | The time |
|---|---|---|---|
| a preview | local, 2 MP at 30 frames per second, never leaves the device | 0 | instant |
| a fast still | a locally tone mapped image, replaced when the processed one arrives | 3 to 8 MB | 1 to 3 s near, longer far |
| a full still, 50 MP | the printed preview with a progress mark, then the full image | 12 to 30 MB | 2 to 6 s near, 10 to 30 s far |
| a night burst of 20 frames | the same, with the mark | 200 to 500 MB | 20 to 90 s near, minutes far |
| a 4K120 video | a local encode, stored in B.U.D. | 30 to 80 Mbit/s | live |

**The rule of the honest camera**. A capture that needs a long uplink states the time and the class **before** the shutter. `[DECISION]` (the answer of Ayaz, question 28.)

**The provisional pipeline**. The module runs a local provisional pipeline (demosaic, two-frame HDR, tone map, light denoise) reaching 60 to 75 percent of reference quality. The user gets an immediate photograph labelled `local provisional`. The validator result then replaces the view while the record keeps both. `[HYPOTHESIS]` gates CAM-9 and DST-5.

---

## 6.4 The heat of the monogram

| The case | The sensor and the plate | The sentinel | The link | The total | The time |
|---|---|---|---|---|---|
| the viewfinder only | 0.15 W | 0.25 W | 0.05 W | 0.45 W | continuous |
| one still, metered | 0.35 W | 0.45 W | 0.20 W | **1.00 W** | 0.5 s |
| a night burst of 20 frames | 0.60 W | 0.70 W | 0.90 W | 2.20 W | 2 to 4 s |
| a 4K60 video | 0.50 W | 1.30 W | 0.60 W | 2.40 W | continuous |
| a 4K120 video | 0.70 W | 2.00 W | 1.20 W | 3.90 W | continuous, derated |

**Where the heat goes**. The module contacts the top edge over **128 mm²**. Its **1 280 mm²** shell acts as a fin, and the body is a **256 cm²** radiator. The part is the hot spot and the surface spreads it. Twelve mechanisms make the pair survive, and they are written in Part 11. They include the graphite spreader, the `<3 K/W` interface, sensor power reduction, hub encoding, and duty rules. They also include temperature-aware capture, cell thermal isolation, dark-frame recalibration, and honest surface state reporting.

---

## 6.5 The magnets, the guests and the keep-outs

| The item | The rule |
|---|---|
| The pen dock | at the rail end of the long edge, away from the monogram |
| The stabiliser of the camera, inside the ring | **no magnet within 8 mm** of the sensor carriage, and the ring wall carries the shield |
| The antenna windows of the leaf | no magnet over a window; the pattern keeps a 6 mm clear ring |
| The guest parts | a guest card or a key fob must not sit on the field band; the case states it |
| The measurement | with the pen attached, the monogram holds its image quality, and the part holds at R 60 mm; gates CAM-7 and B-10 |

---

## 6.6 The pen

| The property | The value |
|---|---|
| The class | **active**: its own radio, pressure, tilt, a low latency ink path |
| The charge | it attaches magnetically to the field band and charges there; a five minute attach gives about six hours of writing |
| The connection | Bluetooth is mandatory; a wired path exists through the USB-C of the rail module |
| The mass | 12 to 17 g |
| The first product | **the pen ships with the first product** `[DECISION]` |
| The latency | the ink follows the touch layer at 3 to 8 ms locally |

---

## 6.7 The sound set

| The part | The placement | The number |
|---|---|---|
| The microphone array | three microphones in the rail module, spaced for a beam | a 30 dB front to back ratio target `[HYPOTHESIS]` |
| The speaker | one small full range driver in the rail module | 1 W class, for a call and a prompt |
| The jack | a 3.5 mm receptacle in the rail module | a wired headset with no adapter and no radio |
| The rule | the faces gain no sound hardware; a Leaf 160 with the rail removed is a silent surface with a haptic and a screen | `[DECISION]` |

**The privacy rule of the sound set**. The microphone follows the lease rule of Part 11. A capture without a lease is refused, and the module declares the sensor state in hardware.

---

## 6.8 The camera gates

| Gate | The test | The pass condition |
|---|---|---|
| CAM-1 | the optical design: 6 elements in 4 groups, a folded path of **17.4 mm inside 3.40 mm** | the drawing, the measured modulation transfer, the CRA under **25 degrees**, and gate CAM-3 |
| CAM-2 | the sensor: the readout, the binning, the HDR merge, metering | the power, the time and the quality of Section 6.3.1 |
| CAM-3 | the sentinel: the remosaic, the compression, the focus stack, the metadata | the payload sizes of Section 6.3.2, and no invented result |
| CAM-4 | the four latency classes | the times on a near and a far validator |
| CAM-5 | the lease and the sensor declaration: the four refusals, the state on the panel, the record | all six behave as specified |
| CAM-6 | the heat of Section 6.4, the duty rules, the cell temperature | the curve, the derate, a cell inside its limit |
| CAM-7 | the magnets: the pen dock, the attach of the part, the stabilisers | the monogram holds with the pen attached, and the part holds to R 60 mm in the wrap |
| CAM-8 | a new module on an old leaf, and a lost module revoked | both behave as specified, the record updated |
| CAM-9 | the local provisional pipeline against the validator reference: a day shot, a night shot, a document | the local image is at least 60 percent of the reference, and it is labelled |

**The extended camera and rear round panel gates (`CAM-14` to `CAM-20`) of revision L.4.1**. They are defined in `HARDWARE/05-B-MODULE-CAMERA-AND-PANEL.md` alongside `MON-1` to `MON-20` of `HARDWARE/20-THE-BUDLUM-MONOGRAM.md`. `[DECISION]`

| Gate | The test | The pass condition |
|---|---|---|
| CAM-14 | the front ring camera assembly: mass and flush fit at `z = 1.60..4.00 mm` | **21.0 g** total B module mass, and front sapphire window flush within **0.03 mm** |
| CAM-15 | the B module link: `5 Gbit/s` wired on top-edge pads and `400 Mbit/s` wireless off-device | no dropped frame in 30 minutes, and no loss of pairing |
| CAM-16 | the 2-axis piezo OIS and autofocus stage inside the `Ø24.0 mm` ring bore | `±1.5°` OIS stroke (`3.5 EV` stabilization) and `12 cm` to infinity focus in **15 ms** |
| CAM-17 | the rear round AMOLED panel (`Ø22.4 mm` active, `220 x 220 px`, `250 ppi`, `1-60 Hz`) | `600 nits` peak, `<20 ms` selfie viewfinder latency, and `8 mW` at `1 Hz` clock |
| CAM-18 | the folded optics: 8 elements in 4 groups on the folded `3.4 + 14.0 mm` path | modulation transfer `>45%` at `120 lp/mm` center, CRA under **24 degrees**, focus at `0.12 m` |
| CAM-19 | the in-ring acoustics and flash: `2 x MEMS` mics (`68 dB` SNR), speaker (`78 dB SPL`), dual-tone LED | all sit inside the `Ø24.0 mm` ring bezel, sealed to **IP68**, zero parts in the concave valley |
| CAM-20 | the waterproof bore seals: front sapphire and rear polycarbonate O-rings | passes **IP68** (`1.5 m`, `30 min`) and `1.5 m` drop on 6 faces |
