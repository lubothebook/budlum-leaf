# BUDLUM LEAF · THE DIRECTIVE · PART 17 · THE ENERGY ARCHITECTURE REVIEW

**The question of Ayaz that created this part**. *The compute, the storage and the operating system are all on the network, at the validators. If the device holds none of them, does a Budlum Leaf need a battery this large, and does it need a sandwich at all? Can the cell live inside the panel itself, in the polymer, and can the middle disappear? And a second question: two ways to sell. One is a subscription that pays for what the validators spend. The other is a hardware unit that is bought separately, with the screen in the hand and the hardware elsewhere.* `[DECISION]`

**The standing of this part**. It is a **review with a recommendation**, not a settled decision. Every number below is `[HYPOTHESIS]` until its gate runs. The recommendation is D-8, and it is Ayaz's to take.

---

## 17.1 The question is right, and the answer is a smaller cell, not no cell

The premise is correct: the Leaf holds no processor, no operating system and no archive. That removes **the compute** from the energy bill, and compute was the largest term in the surface of 2026. A carried surface of today spends 2 to 5 W on its own silicon. A Leaf spends 0.70 W on a fixed function hub. The energy bill that remains is three things that cannot be moved to a validator:

| The term | Why it cannot move | The power |
|---|---|---|
| **the light** | the panel is the product; the photons are made in the hand | 0.60 to 1.10 W |
| **the hub** | the decoder, the local scene renderer and the reprojection unit are inside the device by definition of Part 10 | 0.70 to 1.20 W |
| **the radio** | the link is the product; the bytes cross the air here | 0.40 to 0.60 W |
| the authority and the housekeeping | the wallet must answer with no network | 0.12 W |

**The bill**. A delta session is **2.02 W** and a video session **3.27 W** (Part 4, Section 4.6). A working day of eight hours is therefore **16 to 26 Wh**. No part of it can move off the device, because it is light, local rendering and radio.

**And it cannot be harvested**. Indoor light is 10 to 100 µW/cm². Over the 256 cm² of a Leaf 160 that is 2.5 to 25 mW, against a 2 000 mW need: **80 to 800 times short**. `[PUBLICATION]` for the indoor light band, `[GENERAL]` for the conclusion. A surface that lives on ambient light is a scientific instrument, not a product.

**So the conclusion of Section 17.1 is: a cell must exist**. But the question remains: *must it be thick, and must it be a sandwich?* Sections 17.2 to 17.7 answer that. The answer is no on both counts. `[DECISION]`

---

## 17.2 The geometry of energy

Energy is a volume, and the volume has only two factors:

```
E = area × thickness × the energy per litre        (110 cm² available inside the body)
1 Wh of a 700 Wh/L cell = 1.4 cm³ of volume = 110 cm² × 0.13 mm
```

| The truth | The number |
|---|---|
| One hour of a delta session | 2.02 Wh = **0.10 mm** of a full area cell layer |
| One working day, eight hours | 16 Wh = **0.81 mm** of a full area layer |
| Today's Feather cassette | 20 Wh = 22.2 cm³, in a 2.88 mm bay |
| The same 20 Wh as a full area layer | **1.82 mm**, with no shell, no latch, no contacts cage and no bay |

**The insight of this section**. A cell that is **spread over the whole area** uses the area that the device already has. It needs no packaging of its own, because **the device is the packaging**. That is where the sandwich loses. The sandwich built a second box inside the body. That box had walls, a lid, a latch and an air gap. `[DECISION]`

---

## 17.3 The 4-Quadrant (`+`) 2.00 mm (`68 g`) Solid-State Screen-Battery Body, Universal `Qi2.2`, and `90°`-Bent-Stem B Module (`20 g`): the Revision L.5.0 architecture

**Definition**. In Revision L.5.0, the bulky external bottom battery pack is cancelled. The `2.00 mm` (`68 g`) body splits across `+` into **four `17 g` quadrants (`Q1..Q4`)** (`HARDWARE/11`, `HARDWARE/17`). Each quadrant integrates a `3.0 Wh` (`800 mAh`) `LLZO/PEO` solid-state cell (`12.0 Wh` total) and `Qi2.2` wireless charging (`0` USB-C on body). All other functions (`U1` Master TCON, `U2` `UWB / mmWave` SiP, camera, audio, antenna, and `USB Type-C`) live in the **`90°` B module (`20 g`)**.

| The property | The value at Revision L.5.0 |
|---|---|
| The 4-Quadrant (`+`) body | `80.0 x 160.0 x 2.00 mm` (`4 x 17.0 g` = **`68.0 g`**; zero USB-C and zero buttons on body) |
| The display & `<15 µm` `+` seam | **dual flicker-free `T-OLED` + `PDLC` privacy film + `AgNW/ITO` + `<15 µm` (`n = 1.585`) self-healing optical `+` seam (`R < 0.0001%`)** |
| Internal solid-state battery | **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`, `750 Wh/L`) non-flammable `LLZO/PEO` cells (`0%` liquid, `0.0 ppm` HF, `>14.1 h` at `0.85 W`)** |
| Eyewear & ocular safety | **`<=36.2 °C` hardware NTC cut-off**, **`ISO 10993-5/-10`** medical-grade BPA-free PC, `<0.08 µT` bifilar ELF, **`SAR = 0.054 W/kg`** |
| Universal wireless charging | **Central `Ø54.0 mm` 4-sector `Qi2.2` MPP (`15-25 W`)** + **`4 x Ø22.0 mm` (`5-10 W`) local `Qi` coils** (charges whole body or 1 tile) |
| Tool-free quadrant hot-swap | **`(0,0)` Ti hub + `8` Ti pins (`<2.5 µm` step) + `24` N52H (`11.2 N`) + `64` gold leaves** (`<3 s` swap, `EU 2023/1542`) |
| `90°`-bent-stem B module (`20.0 g`) | **only the stem (`8 x 32 mm`) bends `90°`** on 4 edges; **`Ø32 mm` ring lies flat on screen (`+Z / -Z`)** |
| Sole `USB-C` & Zero-CPU core | **sole `USB Type-C` (`40 W`)** in the `90°` B stem; **`U1` Master TCON + `U2` `UWB / mmWave` SiP** in the flat B ring |

**Why the middle is the right place, and not a compromise**. In a closed stack that bends, the strain is zero at the mid-plane. So the middle of the body is the **best** mechanical place for the least flexible layer. There the sheet bends as little as any layer can while the body bends. The two faces shield it from the cover strain, the impact and the light. The earlier cassette also sat in the middle, but it sat in a **shell** with a latch, an air gap and a fixed 2.88 mm. The shell is what this part removes, and not the middle. `[GENERAL]`

**The fills, and what each one buys**. The energy density is a **range, not a number**, and the range depends on the tile thickness. A thin cell loses density because the foil, the separator and the tab take a larger part of a small volume. `[PUBLICATION]` Three numbers set the band. A bendable cell on sale gives **under 200 Wh/L** at a 25 mm radius. A research textile cell gives **450 Wh/L** at a 1 mm radius. A 2024 flexible cell reached **374 Wh/L** with 40 000 bends. A rigid cell of 2 mm and more reaches **700 to 950 Wh/L**. The audit F-01 is accepted: **900 Wh/L is the upper limit of the study and not the base case**.

| The tile thickness | A useable density band | The base case of this directive | The note |
|---|---|---|---|
| 0.60 mm and a flexible film | the band of the family, 600 to 720 Wh/L at 2.2 g/cm³ | **600 Wh/L**, the bottom of the band | a thin flexible cell, or thin rigid tiles |
| 1.00 mm | the same band | **650 Wh/L** | the transition band |
| 1.82 mm | the same band | **700 Wh/L** | a rigid tile with a low tile penalty, and the Sheet 182 of Part 4 |
| 2.28 mm | the same band | **720 Wh/L**, the top of the band | the cassette class |

| The fill | The sheet | The volume | The nameplate, the base case | Effective | A delta session | The body | The device mass | The range of the delta session |
|---|---|---|---|---|---|---|---|---|
| **4-Quadrant `+` Solid-State (Chosen L.5.0)** | **`4 x 1.08 mm` `LLZO/PEO` (`750 Wh/L`)** | **11.3 cm³ (`4 x 2.83 mL`)** | **`12.0 Wh` (`3 200 mAh`)** | **12.0 Wh** | **>14.1 h (`0.85 W`)** | **2.00 mm** | **68 g (`4 x 17 g`)** (`88 g` w/ B) | **12.0 to 16.0 h** |
| **Sheet 60** (legacy study) | 0.60 mm | 6.6 cm³ | **3.5 Wh** | **3.1 Wh** | **1.5 h** | 1.62 mm | **21 g** | 0.4 to 1.5 h |
| **Sheet 100** (legacy study) | 1.00 mm | 11.0 cm³ | **6.4 Wh** | **5.6 Wh** | **2.8 h** | 2.02 mm | **30 g** | 0.8 to 2.7 h |
| **Slim Chin 400** (4.00 mm H-frame) | 4.00 mm | 5.2 cm³ | **4.8 Wh** | **4.5 Wh** | **5.3 h** | 4.00 mm | **46 g** | 5.3 h at 0.85 W |
| **Sheet 228** | 2.28 mm | 25.1 cm³ | **16.1 Wh** | **14.2 Wh** | **7.0 h** | 3.30 mm | **57 g** | 4.5 to 9.0 h |
| the cassette, for reference | a 2.88 mm bay | 22.2 cm³ | 20 Wh | 16 Wh | 7.9 h | 3.90 mm | 78 g | 4.5 to 9.0 h |

**The comparisons that stay true after the correction**.

1. Sheet 228 delivers **14.2 Wh** against the cassette's 16 Wh. It saves **0.60 mm** of thickness with no shell, latch or bay. The earlier sentence "13 percent more" is **withdrawn** because it depended on the 900 Wh/L base case (F-01).
2. Sheet 100 is **1.9 mm thinner than today**. It carries a quarter of a working day at the base case.
3. Bare is **1.2 mm and 20 g**, the thinnest member. The module or the hub supplies its energy.
4. **The thin body buys thickness, not energy**. The energy of a thin sheet is small, and the claim says so. `[HYPOTHESIS]` gates ENR-7, ENR-8, ENR-21 and ENR-2, which samples 600, 650, 700 and 720 Wh/L at 2.2 g/cm³.

**What the module adds, after revision L.3**. **Nothing, and that is deliberate**. The 20 Wh cell of the module is **struck** (decision R-11): the module is a door for ports, and it carries no energy. The energy parts of a Leaf are the **sheet** and the **cassette**; a Bare Leaf on a module still runs on power. This paragraph replaces the whole of the earlier claim.rgy part that is bought once and renewed**.

---

## 17.4 What the sandwich was for, and what it gives up

| What the sandwich gave | Is it still needed | The answer if not |
|---|---|---|
| the cell out of the bending stack | **no** | the sheet sits at the neutral axis, which is the best place for it |
| a removable cell | **yes, and by law** | Section 17.6: the slip sheet keeps the removability with no shell and no latch |
| a thick, cheap cell | **mostly no** | the fills of Section 17.3 cover 0.6 to 2.28 mm |
| the middle structure of the body | **no** | the spine carries the load, and the weld closes the perimeter |
| the ability to swap capacity on the road | **yes, by the sheet** | the user swaps the energy sheet, or attaches the cassette on the backup line: capacity is a sheet choice |
| a hard stop for the wrap | **no** | the wrap zone carries no cell tile, and its gaps open to 1.20 mm while the mosaic stays in the sheet |
| heat spreading from the middle | **no, it is better** | a full area sheet of 110 cm² spreads heat better than a 22 cm³ block |

**The four things the sandwich cost, and which the sheet returns**. A shell, a lid, a latch and a set of wiped contacts. That is about 9 g and about 1.0 mm of the body. Those four parts are exactly the parts that the design had to justify in the first place. `[DECISION]`

---

## 17.5 The three bodies of the family, and the death of the fixed 4 mm

| The body | The build | The thickness | The mass | The energy | The sentence that sells it |
|---|---|---|---|---|---|
| **Bare** | two faces welded at the perimeter, the spine, no cell | 1.02 to 1.20 mm | about 20 g | on power and on the module | *"a surface, not a device"* |
| **Sheet** | the same body plus the energy sheet of the chosen fill | 1.62 to 3.30 mm | **21 to 57 g** | **3.5 to 16.1 Wh at the base case**, and the band moves with the cell partner | *"the thickness you choose is the energy you choose"* |
| **Sandwich** | the cassette bay of Parts 3 and 4 | 3.90 to 4.00 mm | 78 to 92 g | 20 to 25 Wh | the reference envelope, and the fallback if the slip sheet of Section 17.6 fails its gate |

**The rule of this part**. **4.00 mm is the maximum envelope, and it is not the design target** (the audit F-09). The product states the body thickness fixed by the order, alongside the mass and runtime. `[DECISION]`

---

## 17.6 The legal route A: the slip sheet (the recommendation)

**The design**. The sheet is a replaceable part. It slides out through a 0.4 mm lip at the fixed edge, on a 50 µm carrier with a pull tab. The contacts sit in the edge band.

| The property | The value |
|---|---|
| The removal | one straight motion, no tool, target below 30 s |
| The cycles | 300 cycles at a 0.35 mm lip, with the seal tested at each 50 |
| The seal | the first variant, superseded: a doubled polymer lip with a silicone bead, and a class of IP54 to IP56. **This variant is not sold as water resistant**. Route A+ replaces it with the gasketed carrier and the class of gate MEC-19 |
| The compliance | **the user replaces the part that stores the energy**, which is the substance of the European removability duty |
| The thickness cost | about 0.06 mm for the lip and the carrier tolerance |
| The refusal | a sheet whose record fails is refused with the failing field on the surface, as any part is |

`[HYPOTHESIS]` gate ENR-8 proves the cycles, the seal and the record. This route is recommended because it keeps the European answer that the program already chose, and because it costs 0.06 mm.

---

## 17.7 The legal route B: the sealed sheet (the honest analysis)

**What Ayaz asked**. The cell lives in the polymer, and the device is charged without opening it. **The engineering side of that is real:** a sealed sheet is thinner by the lip, stiffer in the seal and cheaper.

| The question | The honest answer |
|---|---|
| Is a sealed cell legal in Europe from 18 February 2027? | **not by default**. Article 11 of EU 2023/1542 puts the removability and replaceability duty on the end user for portable batteries. The derogations exist and they are narrow, and a display surface does not obviously sit in one |
| Does the fact that the *real* energy source is the validator change it? | **no**. The law looks at the cell that is in the product, not at where the compute runs |
| Is there an argument in the data integrity clause? | there is an argument to test with a lawyer: the wallet authority and the session state depend on continuous power. It is an argument, not a settled position |
| The cost of the argument | a legal opinion, a market-by-market reading, and the risk of a redesign at the worst moment |
| The alternative | **route A**, which gives the same design in 0.06 mm more, with no argument |

**The rule that this part proposes**. Build route A. Keep route B as a **market variant** released only with a written legal opinion after the sheet passes its gate. `[DECISION]` pending D-8.

**And the "charge once" idea, answered honestly**. A cell is spent by the light it makes. A Leaf cannot be charged once and live forever because photons cost 0.6 to 1.1 W per hour. What **can** be built is the feeling Ayaz is describing:

1. **the hub of Section 17.9**, so the surface rests on the hub and stays full;
2. **the Bare tier**, so a user who lives near power never thinks about energy at all;
3. **the module**, so a swap is one action of ten seconds and the capacity travels with the camera.

---

## 17.8 The glasses, and why the clear lens cannot hide a cell

| The case | The answer |
|---|---|
| the Frame | a 2 to 3 Wh cell in the temple, as Part 7 says. **The temple is the right place**, because it is the only part of a pair of glasses with volume outside the optical path |
| the Clear Leaf Window and the surface over glass | a cell behind the clear panel is allowed **outside the optical path**: in the frame band, rim, or opaque margin |
| a transparent cell inside the lens | **refused as a plan**. A transparent electrochemical cell is a laboratory object with a low capacity and a short life. A cell in the lens would also block the world, and the clear family never does that |
| the honest statement | the clear family carries its energy in the parts that the eye does not look through, and the claim says so |

`[PUBLICATION]` for the state of transparent cell research, `[DECISION]` for the refusal.

---

## 17.9 The hardware unit: the Leaf Hub, and the two ways to buy

**The split that Ayaz described is the correct architecture of the product line**. The energy follows the compute. **The energy for the light stays in the hand, and the energy for the compute goes where the compute is**.

| The product | What it is | What it holds |
|---|---|---|
| **Leaf Screen** | the surface: the panel pair, the spine, the hub, the radio, the secure element and an Energy Sheet of the chosen fill | the light, the link, the wallet |
| **Leaf Hub** | a separate hardware unit that the user or an operator buys: a stand, a puck or a pack | **a large cell (40 to 100 Wh), the ports, the sound set, the near validator services of Part 10, and optionally the Budlum validator board** |
| **Leaf Module** | the rail module of Part 6, and the monogram beside it | the ports, the sound set and the pen dock, and **no cell**; the camera is the monogram of Part 20 |

**What the hub does for the surface**.

| The function | The number |
|---|---|
| the charge | **a contact pair in the stand**, so the surface is full when it rests. No coil, per decision R-1 |
| the power | the surface on the hub draws from the hub and spends nothing of its own sheet |
| the near services | the cache, the document model composition, the video buffer and the relay at 1 to 5 ms (Part 10) |
| the validator duty | the board is optional, and a household that carries it earns for the near work and stakes like any validator |
| the ports | USB-C, a network port, an audio output |

**The two ways to buy, and both are honest**.

| The buyer | What the buyer takes | What the buyer pays |
|---|---|---|
| **the user** | the Leaf Screen, optionally a hub, optionally a module | the hardware, and a **pay as you go** meter for the network work |
| **the operator** | a Leaf Hub with a validator board, and one or more surfaces | the hardware, and the operator earns for the store, the near services and the answers |

**The pay as you go meter, in structure**.

| The meter | The unit | The visibility |
|---|---|---|
| the interactive class | milliseconds of the effort tier | the surface states it |
| the standard class | milliseconds of the effort tier | the same |
| the deferred class | milliseconds at the idle price | the same |
| the bytes | the class of the transfer | the same |
| the near services | the hub earns what it serves, and a household hub pays for itself over a stated period | the hub states its own earnings |

**The rule**. The surface never spends another party's compute without a stated price. The price structure is written here while the numbers stay deferred by Ayaz. `[DECISION]`

---

## 17.10 What must be measured before this part becomes a claim

| Gate | The test | The pass condition |
|---|---|---|
| **ENR-7** | the sheet: the energy per litre and per gram, the 0.60, 1.00, 1.82 and 2.28 mm samples, the 0.8 tile and bridge factor, the carrier | every fill inside 10 percent of the table of Section 17.3 |
| **ENR-8** | the slip sheet: 300 edge cycles, the carrier seal, the record and the refusal | under 30 s, the class of gate MEC-19 holds after the cycles, and the record is complete |
| **MEC-15** | the thin body: the stiffness, the drop of a 1.62 mm and a 2.02 mm body, the weld at the land | a working surface after the set of gate MEC-4 |
| **MEC-16** | the sheet at the neutral axis: the bend at R 40 and R 25, the bridge strain, 10 000 and 100 000 cycles | no capacity loss beyond 5 percent, no open tile |
| **MEC-17** | the charge heat of a sheet between two faces: 30, 45 and 65 W, seated and in the hand | the derating curve of Part 4, Section 4.5 |
| **MEC-18** | the mass of a Bare body and of a Sheet 100 body, part by part | inside 10 percent of Section 17.3 |
| **PRG-13** | the legal reading of route A and route B in Turkey and in the European Union | a written opinion per route, and the route that ships is the one the opinion supports. **Renamed from PRG-12 in revision L**, so that PRG-12 is the writing check of Part 19, Section 19.4 |
| **MEC-19** | the seal: the bare body, the sealed sheet, the plain slip lip and the **gasketed slip carrier** of route A+ | the class of each, measured with a module fitted and with none, and the class claimed is the class measured |
| **MEC-20** | the wrap of Part 18 and `HARDWARE/12`: `5000` wraps at `R 25.5 mm`, `50000` bends at `R 70 mm`, decoupled slip, and flat recovery | every gate of B-1 to B-6 passes, the edges meet with no tool, and the surface returns flat within 0.15 mm |
| **MEC-21** | the no crease scan: a luminance scan with the surface flat and at an angle, before and after the wraps | no line above 2 percent of luminance, and the claim is published with the scan |
| **MEC-22** | the gasket: 1 000 slip cycles of the sheet and 1 000 hours of compression at 45 °C | the seal force stays inside its window, and the IP class of gate MEC-19 holds |
| **MEC-23** | the bend guard: the mechanical limit, the strain mesh and the bend log | the limit stops the user at the proven radius, and the service can read the log |
| **MEC-24** | the vent: a gas passing, water holding membrane, with one forced cell failure | no weld opens, no panel lifts, and the IP class holds after the event |
| **ENR-9** | the swelling of a silicon carbon cell at 500 cycles, the pressure it puts on the panel, and the short test after the wraps | the swelling stays inside the compliance budget, and no short appears after 5 000 wraps |
| **DSP-11** | the shared substrate panel: two independent arrays on one carrier, the thickness saved, the cross talk and the reliability | at least 0.20 mm saved with no cross talk and no life penalty, or the study is closed |

---

## 17.11 The sealing doctrine: because Ayaz requires water resistance

**The requirement (the answer of Ayaz, question 37)**. *The body must be water resistant*. The audit of the seal against the new architecture gives one clear result. It also gives one tension.

| The architecture | The openings | The reachable class | The cost |
|---|---|---|---|
| **Bare**, no cell | the USB-C receptacle, the module contacts, the pen dock | **IP68**, with a sealed receptacle, a gasketed module interface and a sealed pad door | the class is a design task, not a claim |
| **Sheet, sealed (route B)** | the same, and no cell opening at all | **IP68** | it needs the legal opinion of Section 17.7 |
| **Sheet, slip lip (route A as first written)** | the same, plus a 0.4 mm lip at one edge | **IP54 to IP56** | the lip is a path for water and dust |
| **Sheet, gasketed slip carrier (route A+)** | the same, plus a lip with a **two bead gasket on the carrier itself** | **IP67, IP68 as a target** | about 0.1 mm instead of 0.06 mm, and the carrier becomes a sealing part |

**The finding**. A slide out part and a water tight body are not in conflict by nature. The usual conflict comes from a **bay with a lid**. The energy sheet has no bay: it is a laminated carrier that plugs its own slot. **The carrier is the seal**. That is route A+, and it is the recommendation of this section. One part answers the removability duty and the water requirement at once. `[DECISION]` pending gate MEC-19.

**The three sealing rules of the family**.

1. A port is sealed by its own gasket and a door that has a state, as the module interface does.
2. A removable part seals with a dual-lip gasket on the part itself. Worn seals are replaced with the part.
3. **No claim exceeds the class measured by gate MEC-19**. The class is stated with the module state.

---

## 17.12 The double sided panel, examined (the answer of Ayaz, question 37)

**The question**. *Would a double sided emissive panel not minimise the thickness, with the cell in its middle?*

**The examination**. Three different products are often called a double sided panel, and only one of them is usable here. `[GENERAL]`

| The class | What it is | The thickness it saves | The verdict for a Leaf |
|---|---|---|---|
| **A · shared substrate, two independent arrays** | one polymer substrate and one carrier, two full thin film transistor arrays and two emissive stacks, one on each side | about 0.20 to 0.30 mm: one substrate, one backing and one adhesive layer leave the stack | **usable**, and worth asking the panel partner for, because the two faces keep independent content. Added as gate DSP-11 |
| **B · one array, one image, emitted both ways** | a single pixel matrix that emits from both faces, so both sides show **the same image** | about 0.45 to 0.55 mm | **refused**. A Leaf shows different content on the two faces: one faces the user, the other faces away. The same image both ways is also a privacy defect: the screen would be readable from behind |
| **C · a transparent panel** | the world passes through and the image is emitted towards one side | it does not save thickness | it is the clear family of Part 7, a different product |

**The correction to the thickness hope**. Class A is real and it saves about 0.2 to 0.3 mm. A Sheet 182 body can reach about 2.55 mm, and a Bare body about 0.95 mm. It does **not** change the energy geometry and it does **not** remove the cell: the cell still needs its 0.6 to 2.28 mm. **The thinness comes from the integrated sheet, and a shared substrate is a bonus on top of it**. `[DECISION]`

**And the middle stands**. A class A panel laminates the cell between the two arrays. The cell then sits at the mid-plane of the stack, which is the neutral axis. That is the same place this part already puts it. Ayaz's picture is the correct picture; what changes against the earlier draft is only the shell.

---

## 17.13 The honest hours: what the numbers of Section 17.3 assume

**The doubt of Ayaz, question 39**. *Are those hours right? There is Wi-Fi, the screen is on: does the battery really last that long, and what does a Leaf need?*

**The honest answer**. The hours are correct **for a stated brightness and a stated content load**. They are wrong as a single number, because a panel is paid for the photons it makes. The model:

```
P_display follows luminance × the average picture level
the anchor measured in gate DSP-5: 0.60 W at 250 nits and a 35 percent average picture level
```

| The case | The luminance and the load | The display | The delta session | Sheet 100 | Sheet 182 | Sheet 228 | The video session | Sheet 228 |
|---|---|---|---|---|---|---|---|---|
| a dark room | 150 nits, 30 percent | 0.31 W | 1.73 W | 4.6 h | 8.3 h | **10.5 h** | 2.74 W | 6.6 h |
| **indoors, mixed** | 250 nits, 35 percent | 0.60 W | **2.02 W** | 3.9 h | 7.1 h | **9.0 h** | 3.27 W | 5.5 h |
| a bright room | 500 nits, 50 percent | 1.71 W | 3.13 W | 2.5 h | 4.6 h | 5.8 h | 4.38 W | 4.1 h |
| outdoors, a bright page | 800 nits, 70 percent | 3.84 W | 5.26 W | 1.5 h | 2.7 h | 3.4 h | 7.04 W | 2.6 h |

**What a Leaf needs for these hours: the answer to the second half of the question**.

| The item | The target | Why |
|---|---|---|
| the panel at a **250 nit** working band with a variable refresh to 1 Hz | 0.60 W at a 35 percent load | the light is the largest term, and the refresh of a static page costs 60 percent of it `[HYPOTHESIS]` |
| **a Wi-Fi association that sleeps**: target wake time and multi-link power save | 0.05 to 0.15 W associated, 0.40 W in a delta session | an associated radio that never sleeps is the classic drain of a thin client |
| **the fixed function hub capped at 0.70 W** | the decoder, the local renderer and the reprojection | the voice of the chip is the price of the local floor of Part 10 |
| **the class line honesty** | the session class is visible, so a heavy session is a user decision | a user who knows the cost spends less |
| the sheet as the store | the user's sheet choice, one action | capacity travels with the sheet, and the module carries none |

**The claim rule that follows**. A runtime claim names the member, the fill, the **luminance**, the **average picture level**, the session class and the Wi-Fi state. A single number without them is refused by the claim policy. `[DECISION]`

---

## 17.14 The settlement: the wallet pays (the answer of Ayaz, question 41)

**The answer**. The network cost is settled **from the wallet**, inside the session grant. The grant carries the energy policy and the spending policy. The meter of Part 15, H-15 reports to it. There is no separate subscription product, no invoice and no second account. `[DECISION]`

| The element | The rule |
|---|---|
| The meter | milliseconds of the effort tier and bytes of the class, visible on the surface |
| The settlement | the wallet's session grant, one signature per session, not per tap (Part 9, Section 9.4) |
| The cap | the user sets a cap per session, per day and per month in the grant |
| The stop | at the cap the session stops **at a class boundary**, never in the middle of a frame |
| The near validator | a household validator earns for the near work, and its earnings and its costs are in the same wallet |
| The numbers | the price amounts stay deferred by the order of Ayaz |

---

## 17.15 The Leaf Hub is deferred, and the option stays open (the answer of Ayaz, question 40)

| The element | The decision |
|---|---|
| The hub as a product | **deferred**: it is studied, not committed |
| The dock and the rail today | the charge, the stand and the rail, with the validator board as an option |
| What stays in the design | the interface of Section 17.9: a hub can be added later without a change to the device. The device already draws from the dock when it rests on it |
| What opens the decision later | the market measurement of gate DST-5 and the earnings of a household board, measured on a pilot |

---

## 17.16 The decisions of this review (the answers of Ayaz, questions 37 to 42)

| No. | The question | The answer | The standing |
|---|---|---|---|
| Q37 | where the cell lives, and the sandwich | the cell is the **laminated middle layer at the neutral axis**; the old rigid shell is retired, and the body must be **water resistant** | Section 17.11, and the replacement of the shell by the carrier |
| Q38 | the European route | **route A, the removable sheet, in every market** | Section 17.6, upgraded to route A+ by the gasket of Section 17.11 |
| Q39 | the hours | the table of Section 17.13, with the luminance and the load named in every claim | `[HYPOTHESIS]` until gate DSP-5 |
| Q40 | the hub | deferred, the option open | Section 17.15 |
| Q41 | the payment | settled **from the wallet**, inside the session grant | Section 17.14 |
| Q42 | the module and the cassette | **the module carries no cell**; the sheet is the energy part and the cassette stays on the backup line | Section 17.3 |

---

## 17.17 The recommendation to Ayaz

1. **Adopt the Energy Sheet as the energy architecture of the family**. It gives a thinner, lighter body with fewer parts and a better thermal path. It removes the shell, latch and bay.
2. **Keep the European removability answer with route A, the slip sheet**, at a cost of 0.06 mm. Do not argue with Article 11 when a 0.06 mm lip settles it.
3. **Keep the cassette as the reference envelope and fallback**. No partner conversation or gate re-opens the body geometry.
4. **Make Bare a real tier**. A 1.2 mm, 20 g surface is unmatched for a user who lives near power.
5. **Build the Leaf Hub as a product**. Energy follows compute, near services need a stand, and hub operators also earn.
6. **Hold the sentence until the gates run**. Gates ENR-7 and MEC-16 decide the numbers, and the numbers decide the claim.

**The one sentence of this part, once the gates run**. *The compute left the device, and the energy did not have to leave with it. The cell it still needs is spread so thin that the device is no longer a sandwich. It is a surface with a day inside it.* `[HYPOTHESIS]`
