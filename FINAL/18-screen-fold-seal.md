# BUDLUM LEAF · THE DIRECTIVE · PART 18 · THE SCREEN COST, THE BEND AND THE SEAL

**The questions of Ayaz that created this part**. *The screen makes the picture. Does the validator not cover the cost of the screen working? Explain this at length.* And: *the flexibility test. Even if the screen bends edge to edge, does it survive without breaking, without damage, without the inside falling apart? That is the test for the carried member. The other members have no bend to the half.* And: *the body must be water resistant.* `[DECISION]`

---

## 18.1 The question, stated exactly

**The question of Ayaz**. The validators carry the processor, the storage and the operating system. The network is paid from the wallet. Then why does the device still carry an energy cost for the screen? Must the validator not pay that cost too?

**The short answer**. The validator covers **three of the five terms** of a session. It can never cover the fourth, because of where the light is made. And there is a fifth term, the *shape* of the content, that the network can cut by almost half. The program has never counted it. That last point is the real answer to the question, and it is worth a whole section. `[DECISION]`

---

## 18.2 The ledger of five terms: who can reduce what

| The term | The delta session | Who reduces it | The mechanism | The floor |
|---|---|---|---|---|
| **1 · the photons** | 0.60 W | **the device alone, and by design** | lower luminance, a darker interface, a lower average picture level, a better emitter | the light that the eye needs at the chosen comfort |
| **2 · the hub work** | 0.70 W | **the network, in part** | a pre-composited, pre-scaled, pre-tone-mapped frame leaves the hub at the decoder floor; the local floor still runs | the local floor of Part 10 cannot leave the device |
| **3 · the radio** | 0.40 W | **the network, in full** | the class: C0b at 2 to 200 kbit/s against C2 video at 10 to 30 Mbit/s, plus the cache and the delta | the bytes that the user's action needs |
| **4 · the addressing** | 0.20 W | **the network, in part** | the refresh policy: a static page at 1 Hz instead of 144 Hz | the refresh that the content needs |
| **5 · the authority and the housekeeping** | 0.12 W | **nobody** | the wallet must answer with no network | fixed |
| **the sum** | **2.02 W** | | | |

**The reading**. Three of the five terms are **the network's business** (2, 3 and 4: 1.30 W of the 2.02 W). One is **the device's own** (1: the photons), and one is fixed. `[DECISION]`

---

## 18.3 Why the photons can never come from the network

**This is thermodynamics, not engineering taste**. A lumen is a photon that has to arrive at a retina. The network can move information at the speed of light, but it cannot move light to a place where the light is not made. The panel is the transducer. **The energy that the eye receives must be emitted within the eye's field, by a surface that the eye is looking at**. A validator 8 000 km away cannot send one photon into a room in Istanbul. `[GENERAL]`

The physical floor, stated as a number:

```
a comfortable page at 250 nits over 110 cm² at a 35 percent picture level
      = 0.60 W at the panel, at a 2026 emitter efficacy
the same page at 150 nits and 30 percent
      = 0.31 W
the same page at 800 nits for the sun
      = 3.84 W
```

**The judgement**. The absolute floor of the fourth term is **the light that the user's own eye needs**, and the entire industry is bound to it. What is *not* fixed is how much light the design asks for. `[DECISION]`

---

## 18.4 What the network can do about the screen: four mechanisms with numbers

This is the part of the answer that had never been written. It is a **round trip between the device and the network**. The device reports the energy, and the network is built to spend less of it.

| No. | The mechanism | The saving on a delta session | How it is done |
|---|---|---|---|
| 1 | **the photon-honest interface** | **0.60 W → 0.31 W** | network-side interfaces are dark-first: true black background, low average picture level, no large white fields, and high-contrast text at low luminance |
| 2 | **the delta transport and the cache** | **0.40 W → 0.10 W** | interfaces arrive as signed `C0b` display lists (`2 to 200 kbit/s`), cached locally so repeats use zero traffic; video streams only on demand |
| 3 | **the pre-composited frame** | **0.70 W → 0.55 W** | the validator sends pre-composed, scaled, tone-mapped frames so the hub stays at its decoder floor while Part 10 keeps local interaction instant |
| 4 | **the refresh policy** | **0.20 W → 0.02 W** | the address term follows the manifest's refresh range: 1 Hz for a static page, 144 Hz only for motion. The network marks the regions that move, so the scheduler writes less |
| | **the sum** | **2.02 W → about 0.98 W** | **the network covers about half of the cost of the surface working** |

**And the third term of the ledger is not free money**. The network side pays for mechanisms 1 to 4 in engineering. Mechanisms 2 to 4 are **work on the validator**, which the wallet already pays for. Mechanism 1 is **work on the interface system**, which costs a designer's time and nothing per hour. So the sentence is now true in the way Ayaz meant it:

> **The validator covers about half of the cost of the screen working. It does not pay joules. It shapes what the screen has to do**. `[HYPOTHESIS]` gates DST-9 and DST-10 measure both sides of the round trip.

---

## 18.5 The two currencies, and who pays which

| The currency | Where it is spent | Who pays |
|---|---|---|
| **joules** | in the hand: the photons, the hub, the radio and the addressing | the user, from the energy sheet, the module or the hub (Part 17) |
| **meters** | on the network: the effort tier of an answer, the bytes of a class, the storage of a session | the user, **from the wallet**, inside the session grant (Part 17, Section 17.14) |

**Why the two cannot be merged**. A payment can move value across a network. It cannot move energy into a place where no one is generating it. A validator payment cannot create photons in a dark room, so the device keeps a cell even when compute is free. `[DECISION]`

**And the honest consequence for the sales pitch**. A Leaf does not sell "an unlimited screen". It sells **a screen whose work the network compresses**, and a body whose thickness is chosen by the user. The class line, the energy meter and the fill table are the three honest surfaces of that claim. `[DECISION]`

---

## 18.6 The photon-honest interface rule, and the energy meter

| The rule | The content |
|---|---|
| **the photon budget** | every Leaf interface declares an energy budget per screen minute (`mWh`) as a required design input |
| **the meter on the surface** | the device shows the energy per screen minute and per session, in the same place where it shows the class |
| **the dark-first default** | a true black background is the default; a large white field is a deliberate choice that the interface declares |
| **the static rule** | a page that does not change runs at the lowest refresh of the manifest, and the interface must not force a repaint |
| **the review rule** | an interface that exceeds its declared budget is refused by the same review that refuses a page that hides its class |
| **the claim rule** | a runtime claim always names the luminance, the average picture level and the interface budget, exactly as Part 17, Section 17.13 requires |

**The ownership**. the surface line and the network line, gates DST-9 and DST-10.

---

## 18.7 The continuous bend: the answer to the flexibility question

**The requirement of Ayaz**. *Even if the screen bends edge to edge, does it survive without breaking, without damage and without the inside coming apart? That is the test for the carried member. The other members have no bend to the half.* `[DECISION]`

**The correction of Ayaz, 2026-10-06**. *"I did not say there would be a strip that folds. I said the screen flexes. What is done here is not two screens folded onto each other. It has to be flexible enough to place the two ends onto each other"*. The book model of revision K is therefore retired, and this section is rewritten. Hardware file `HARDWARE/12-THE-BEND-LAW.md` carries the full arithmetic and the ten gates. `[DECISION]`

### 18.7.1 The bend, in numbers

| The quantity | The value |
|---|---|
| **the bend** | the surface bends over its **whole area**, and the two long edges can be brought together |
| **the hinge** | **none**. This product has no hinge, no crease line and no closed state |
| **the wrap circle** | the 160 mm long side closes into a **360 degree arc at R 25.5 mm**, which is 160 divided by two pi |
| **the scroll** | with the 3.54 mm stack the scroll measures about **59 mm outside and 47 mm inside** |
| **the gentle bend** | **R 70 mm is free and unlimited**, and it is the shape of a hand held session |
| **the pocket curve** | an arc at R 120 mm holds the gap between the long edges at **1.0 mm** |
| **the flat recovery** | the surface returns flat within **0.15 mm over 160 mm** |
| **the cycle targets** | **5 000 full wraps** (B-1) and **50 000 gentle bends** at R 70 mm (B-2) |
| **the part in the bend** | a seated part holds to **R 60 mm**, and a tighter curl releases it with no damage (B-10) |
| **the crease** | none. The curvature is spread over 160 gaps and ten wrap columns |

**Why the two edges can meet**. In Revision L.5.0, each `17 g` quadrant uses `G = 0.08 MPa` silicone OCA slip layers and a neutral-axis `LLZO/PEO` core (`HARDWARE/12`). The `2.00 mm` (`68.0 g`) 4-Quadrant (`+`) sheet bends to `R 25.5 mm` at `0.38 percent` outer polycarbonate strain (`0.22%` `LLZO` strain). `[DECISION]`

### 18.7.2 The layers in the bend, layer by layer

**The rule**. The layers are not bonded into one beam. A bonded 3.54 mm stack at R 25.5 mm puts 6.9 percent on its outer fibre, and nothing in this program survives that. Each layer bends about its **own** thin axis instead, and every interface shears by design.

| The layer | Its own bending thickness | The strain at R 25.5 mm | Its limit | The reading |
|---|---|---|---|---|
| the cover film | 50 µm | **0.10 percent** | 3 percent | colourless polyimide, comfortable |
| the touch layer | 30 µm | 0.06 percent | 3 percent | on cell, silver mesh |
| the panel tile | 320 µm | **0.63 percent** | 1.0 percent at the barrier | the barrier sits near the tile axis |
| the structural adhesive | 50 µm | 0.10 percent | 50 percent | low modulus film, and it creeps by design |
| the heat spreader | 100 µm | 0.20 percent | 1 percent | graphite, in plane only |
| the steel foil of the field | 150 µm | 0.29 percent, and **0 percent inside a tile** | 1 percent | the foil tiles stay rigid |
| the cell tiles | 2 840 µm | **0 percent inside a tile** | 0 percent | the curvature lives in the gaps |
| the carrier film | 25 µm | 0.05 percent | 3 percent | it follows the tiles |
| the copper bus | 18 µm | 0.04 percent | 0.2 percent | rolled annealed copper, a serpentine at each gap |
| the sealant bead | the edge | stated per joint | its own elongation | a flexible bead, never a rigid weld |

**The slip rule, which answers F-03**. Every interface carries a low-modulus shear layer (`0.4 to 0.8 MPa`) with **0.35 to 0.6 mm of allowed slip at R 25.5 mm**. The audit asked for the slip of two free faces. The two faces move against each other by under a millimetre because each face bends about its own axis. Gates **B-5** and **B-6** measure the gaps and the shear. `[DECISION]`

**The three audit corrections, restated in the terms of this revision**.

1. **F-02, the strain rule**. Layer strain is `d / R`, where `d` is half of the layer thickness. Every row above uses its own thickness, and no row uses the 3.54 mm body.
2. **F-03, the crease stack**. There is no crease stack. The 9 mm book-model slip channel is withdrawn, and the decoupled slip rule takes its place.
3. **F-04, polycarbonate in the crease**. No crease exists, so polycarbonate is banned nowhere. Cover strain is 0.10 percent, twelve times below the 1.21 percent crazing point. The crease inserts are **withdrawn**, saving 0.02 g and a second material stream. `[DECISION]`

### 18.7.3 The test, and the honest claim

| The test | The method | The pass condition |
|---|---|---|
| **the full wrap** | the two long edges are brought together 5 000 times, at 23 °C and at 40 °C | the edges meet with no tool, no crack, no pixel loss, and the bus resistance inside 10 percent of new |
| **the gentle bend** | R 70 mm, 50 000 cycles | no crack, no set over 1 mm per 100 mm, no delamination |
| **the flat recovery** | a granite table after 5 000 wraps | **flat within 0.15 mm over 160 mm**, and the touch map unchanged |
| **the no crease scan** | a luminance scan across the surface before and after the wraps | **no line above 2 percent of luminance**, and no mark at any viewing angle |
| the honest sentence | the product says: **the screen curls, the two edges can meet, it holds the curve while you hold it, and it comes back flat. There is no crease, no hinge line and no closed state**. | the claim policy of Part 12 |

### 18.7.4 The strain budget of every layer

The values are limits for the cycle counts of Section 18.7.1. They carry the tag `[HYPOTHESIS]` until a coupon or a supplier confirms them. `[PUBLICATION]` marks the reported ranges.

| The layer | The allowed strain | The rule |
|---|---|---|
| the colourless polyimide cover | 3 percent | a flexible film class `[COMPANY]` |
| the polycarbonate cover, every face | 1 percent | the yield strain is higher, and crazing and fatigue set the cyclic limit |
| the polyimide backplane | 3 percent | keep the neutral axis at the transistor layer |
| the inorganic barrier | **0.3 percent** | single inorganic layers report a critical strain near 1 percent, and the safe design point is a third of it `[PUBLICATION]`. Keep the barrier within 10 µm of the tile axis |
| the touch layer | 3 percent | **no indium tin oxide**. Silver nanowire or a metal mesh |
| the hard coat | 3 percent, flexible hybrid type only | a rigid type is refused below R 25 mm |
| the copper bridge | 0.2 percent | rolled annealed copper in a serpentine shape, with the strain computed in the copper |
| the cell tile | 0 percent | a tile never bends |
| the adhesive | 50 percent | measure the creep and the relaxation over 1 000 hours at the radius |
| the sealant bead | a stated elongation | measure at R 25.5 mm after 10 000 cycles |

**The margin, in one line**. In Section 18.7.2, the highest layer strain is 0.88 percent in the electrode laminate. Every other layer sits well below its limit. The bend is a working state and not a stunt. `[DECISION]`

### 18.7.5 The test matrix of the bend

Every test uses at least **30 coupons** per condition, and the report gives the failure statistics. All numbers are `[HYPOTHESIS]` until the verification line confirms them.

| The test | The condition | The pass condition |
|---|---|---|
| static bend | 1 000 hours at R 25.5 mm, at 23 °C and 60 °C | no crack, no delamination, set under 2 mm per 100 mm |
| dynamic wrap | the 5 000 full wraps of B-1, at 23 °C and 40 °C | no broken line, pixel loss under the limit, capacity inside 5 percent |
| gentle cycles | R 70 mm, 50 000 cycles | no crack, no set over 1 mm per 100 mm |
| cold and hot wrap | R 25.5 mm at -10 °C and at 45 °C, 500 cycles each | the same pass as B-1 |
| reverse bend | the wrong direction, 1 000 cycles | no crack, and the guard stops the user before the limit |
| twist | a stated angle over 150 mm, 10 000 cycles | no crack, and the tiles unharmed |
| point load | a pen drop and a ball drop, wrapped and flat | no crack, no dead line |
| pinch | a stated force on a wrap column | no crack, no short |
| abrasion then bend | steel wool or sand, then 10 000 gentle bends | no coat crack that grows |
| chemical and strain | the seven chemicals of Section 18.7.6 at 1 percent strain for 24 hours | no craze under polarised light |
| thermal shock | -20 °C to 60 °C, 500 cycles, flat and wrapped | no delamination, and the seal intact |
| seal after the bend | the IP test after the wrap cycles and after 1 000 slip cycles | the class holds |
| drop | 1.2 m, six faces, with and without the monogram | no crack, and the session resumes |

### 18.7.6 The polycarbonate risk table

| The risk | Why it matters | The control | The test |
|---|---|---|---|
| environmental stress cracking | polycarbonate crazes at about 1.21 percent strain in isopropyl alcohol and 1.5 percent in a lipid `[PUBLICATION]` | keep every face under 1 percent, and the worst case is 0.10 percent | the seven chemical set: skin oil, sunscreen, hand cream, an alcohol wipe, a cleaning spray, the adhesive and the electrolyte vapour |
| the notch at a cut edge | a laser edge holds small flaws | polish or flame treat the edge, and keep the R 3.20 mm corner and r 0.80 mm softened edge | the edge under the wrap |
| thermal expansion mismatch | polycarbonate expands about 65 to 70 ppm/K `[GENERAL]`, and the barrier much less | measure the curl and the delamination | 500 cycles of -20 °C to 60 °C |
| creep under a long bend | a body held curved for weeks keeps a set | hold at R 70 mm for 1 000 hours | the set, and the layer strain |
| moisture uptake | the dimensions and the curl move with humidity | measure at 85 °C and 85 percent relative humidity | the dimensional and the curl report |
| UV yellowing | the cover loses clarity | a hard coat with a UV absorber | the light chamber |
| coat adhesion | the coat peels at a wrap column | the cross-cut tape test after the cycles | adhesion after the wrap |

### 18.7.7 The detection methods and the bend guard

**Five detection methods run on every coupon, before and after each test**.

1. an optical microscope at 50 times, with polarised light for the crazing of a polymer.
2. a daisy chain of conductors, read during the test. A 10 percent rise in resistance stops the test.
3. a luminance map of the panel: dead lines and dark spots.
4. a gap measure of the wrap columns, read with the drum and an optical gauge.
5. a water vapour test of the barrier, by a calcium test or an equal method, after the wrap.

**The bend guard is three parts, because a product must not rely on the user**. `[DECISION]`

| The part | The function | The gate |
|---|---|---|
| the mechanical limit | the perforated spine and the carrier stop the curl at R 22 mm, which is inside the proven R 25.5 mm | MEC-20 |
| the strain mesh | a printed conductive ink line in the cover reads the strain, and the hub reads it with the tile temperature sensors | MEC-23 |
| the bend log | the hub counts the wraps and the over-curls, and writes them into the part record, signed by the secure element. The user sees a warning at the limit, and the service reads the log | MEC-23 |

### 18.7.8 The claim wording of the bend

1. Public claims state the **number**: "long edges meet at R 25.5 mm, 5 000 times, at 23 and 40 °C".
2. Product claims forbid **fold, folds, folding, hinge, book**, **closed state**, and *a Leaf 160 becomes a Leaf 80*. `[DECISION]`
3. The claim states the flatness: **flat within 0.15 mm over 160 mm** after the wraps.
4. The claim states the no crease result: **no luminance line above 2 percent**, measured before and after.
5. Excluded damage covers tool-pressed creases, cuts, punctures, crush loads, unlisted chemicals, and curls tighter than R 25.5 mm.

### 18.7.10 The gates of the bend

The ten gates live in `HARDWARE/12-THE-BEND-LAW.md`, and they are counted here because the product claim rests on them. Every test uses at least **30 coupons** per condition. `[DECISION]`

| The gate | The subject | The pass condition |
|---|---|---|
| **B-1** | the full wrap: the two long edges are brought together 5 000 times, at 23 °C and at 40 °C | the edges meet with no tool, no crack and no pixel loss, and the bus resistance stays inside 10 percent of new |
| **B-2** | the gentle bend: R 70 mm, 50 000 cycles | no crack, no set over 1 mm per 100 mm, and no delamination |
| **B-3** | the flat recovery: the surface on a granite table after 5 000 wraps | flat within **0.15 mm over 160 mm**, and the touch map unchanged |
| **B-4** | the no crease scan: a luminance scan flat and at an angle, before and after the wraps | **no line above 2 percent of luminance**, and no visible mark |
| **B-5** | the gap budget: the opening of 50 gaps, measured optically at the wrap | **1.15 to 1.25 mm** in the wrap zone, and 0.35 to 0.45 mm in the normal area |
| **B-6** | the decoupled slip: the slip of the interfaces at the wrap, and the shear over 1 000 hours | the slip and the shear of Section 18.7.2 |
| **B-7** | the cold and the hot: the wrap at -10 °C and at 45 °C, 500 cycles each | the same pass as B-1 |
| **B-8** | the seal in the bend: a 3 mm rain of 10 minutes and 96 hours of salt spray, after 2 000 wraps | IP54, and no water past the bead |
| **B-9** | the edge condition: the two long edges meet with the rail module seated | the module stays seated, and the rail takes no damage |
| **B-10** | the wrap with a part on a face: a part seated, then the wrap | the part holds to **R 60 mm**, and a tighter curl releases it with no damage to the glass |

### 18.7.9 The cell and the body risks that the bend tests do not cover

| The risk | Why it matters | The control | The gate |
|---|---|---|---|
| the swelling of a silicon carbon cell over life | a silicon anode changes volume `[GENERAL]`, and a stack of 2 to 4 mm pushes on the panel | a soft compliance layer, and the swelling measured at 500 cycles | **ENR-9** |
| a sealed body with no vent | a cell that vents gas inside an IP67 body opens the weld or the panel | a controlled vent path: a membrane that passes gas and holds water, tested with a forced cell failure | **MEC-24** |
| the gap wear of the wrap zone | ten wide gaps close and open at every wrap | a coated gap edge, and the gap measure of B-5 at the end of life | **B-5** |
| the decoupled slip | the interfaces shear at every wrap | the 0.4 to 0.8 MPa rule, and the shear measured over 1 000 hours | **B-6** |
| the copper bridge fatigue | the bridges bend at every wrap | a serpentine shape and rolled annealed copper, with an S-N curve at the real strain | MEC-16 |
| the weld and the tab fatigue | a weld at a bridge is a stress point | a pull test after the wrap cycles | MEC-16 |
| a short at a wrap column | a wrap column presses a foil through a separator | an insulating guard layer at every column, and a short test after the wraps | ENR-9 |
| the compression set of the gasket | a gasket loses force with time and cycles | the seal measured at 1 000 cycles and after 1 000 hours of compression | MEC-22 |

---

## 18.8 The seal, decided

| The question | The answer of Ayaz | The design |
|---|---|---|
| water resistance | **required** | **route A+: the gasketed slip carrier**. The continuous battery sheet carries a dual-lip FKM gasket that seals its own bottom slot |
| the class | a target | **IP67, with IP68 as a target after the gate**, measured with a module fitted and with none |
| the ports | sealed | a gasketed USB-C receptacle, a sealed module interface, a sealed pad door |
| the rule | a removable part seals on the part, never on the body | a worn seal is replaced with the part |
| the gates | **MEC-19** and **MEC-22** | the class per architecture, and the 1 000 cycle seal |

**The earlier conflict is resolved by the architecture**. A slide out part and a water tight body conflicted because the cassette needed a **bay with a lid**. The sheet has no bay: the carrier is the seal. `[DECISION]`

---

## 18.9 The double sided panel, decided

| The path | The decision of Ayaz | The effect |
|---|---|---|
| **the first product** | **two independent panels** | no new supply risk; the product ships on a proven part |
| **the common carrier panel** | **researched in parallel** | one substrate, one backing, two independent arrays, about **0.20 to 0.30 mm** saved. Gate **DSP-11** |
| the single matrix, one image both ways | refused | the two faces show different content, and a screen readable from behind is a privacy defect |
| the transparent panel | Part 7 | a different product |

**The rule**. The first product does not wait for the common carrier. If gate DSP-11 passes, the second revision is thinner by 0.2 to 0.3 mm with no other change. `[DECISION]`

---

## 18.10 The cassette, decided

| The item | The decision |
|---|---|
| the first product | the energy sheet, with no cassette |
| the cassette | **the backup line and the buffer of the large members**: Leaf 480, Leaf 1400, and Leaf 2800 keep a buffer cassette |
| the module | keeps its 20 Wh and stays the energy part that travels with the camera |
| the reference envelope | 3.90 to 4.00 mm stays as the fallback envelope, not as the design target |

---

## 18.11 The next block: the CAD first

| The order | The line | The deliverable |
|---|---|---|
| 1 | **the drawing line** | **the CAD of the body**: `80 x 160 x 2.00 mm` (`68 g`) 4-Quadrant (`+`) solid-state body, `Qi2.2` coils, and `90°` B module (`20 g`) |
| 2 | the partner line | the sample orders that the CAD unlocks: the panel with the wrap zone, the sheet cells, the gasket carrier, the common carrier panel study |
| 3 | the software line | the firmware skeleton and the photon-honest interface rules of Section 18.6 |
| 4 | the drawing line, later | the pafta re-issue: **P01 to P21 and E01 to E03**, twenty four sheets at OVER 0, COVERED 0 and COLLIDE 0 |

**The rule**. The CAD is the gate of every quotation and every fixture, so it is first. `[DECISION]`

---

## 18.12 The decisions of revision K

| No. | The question | The answer |
|---|---|---|
| Q43 | the seal | **A+, the gasketed slip carrier, IP67 with IP68 as a target** |
| Q44 | the double sided panel | **two panels in the first product; the common carrier researched in parallel** |
| Q45 | the screen cost | **Sections 18.2 and 18.4: the network cuts session energy by half through dark-first display lists, never by sending photons** |
| Q46 | the first prototype | **the full wrap**: a Leaf 160 bending to `R 25.5 mm` for `5 000` cycles without damage or crease |
| Q47 | the cassette | **the backup line and the buffer of the large members** |
| Q48 | the next block | **the CAD of the new body first**, then the samples, then the software |

**The one sentence of this part**. *A validator can pay for a computation, and it can teach a screen to need less light. It cannot send light itself, so the device keeps the photons, bends with no hinge, and seals on the sliding part*. `[DECISION]`
