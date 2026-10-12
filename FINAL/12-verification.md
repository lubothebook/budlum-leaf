# BUDLUM LEAF · THE DIRECTIVE · PART 12 · THE VERIFICATION AND THE CLAIM POLICY

---

## 12.1 The five steps of a claim

| Step | What it is | The cost | What it proves | The exit |
|---|---|---|---|---|
| 1 | the model and the simulation | the least | a number is plausible | a written model with its assumptions |
| 2 | the coupon | low | the material behaviour | a measured coupon set |
| 3 | the sub-assembly | medium | the pair works | a working cassette, module or panel pair |
| 4 | the prototype | high | the member works | a working Leaf 160 |
| 5 | the pilot | the most | the product works in a hand, in a city | a service network and a claim file |

**The rule**. A claim is published only at the step that supports it, and the step is named in the claim's record. "A result without data is an opinion." `[DECISION]`

---

## 12.2 The complete gate index

| The family | The gates | The subject |
|---|---|---|
| The structure, the mass, the heat | MEC-1 to MEC-13 | wrap/slip rule, mass, battery sheet, drop, spine, charge heat, seal, radio coupling, energy, pen, B module heat, capture policy, and prism edges (`B-1..10`) |
| The energy | ENR-1 to ENR-6 | the tile penalty, the cell samples, the gauge and the record, the abuse set, the slide cycles, the charge curve |
| The panel and the light | DSP-1 to DSP-10 | panel, addressing, seam, tile service, power model, daylight, variable refresh, bend, manifest, cut, and corner |
| The radio | RF-1 to RF-8 | antenna set, battery in the field, cable/dock desense, bent match, path manager, ladder, optical path, and satellite class |
| The camera | CAM-1 to CAM-9 | the optics, the sensors, the sentinel, the latency classes, the lease, the heat, the magnets, the renewal, the provisional pipeline |
| The clear family and the Frame | CLR-1 to CLR-10 | clear panel, Frame optics, daylight, mass, prescription, window alignment, family rule, eye safety, privacy, and surface over glass |
| The Field mode | FLD-1 to FLD-6 | the spacer, the angle, the latency, the density claim, the move, the isolation rule |
| The firmware | SW-1 to SW-6 | the node profile, the finality budget, the classes, the lease, the handoff, the signature budget |
| The network | SW-7 to SW-13 | the record and the refusal, the battery policy, the challenge energy, the relay path, the labels, the optical receipt, the telemetry |
| The distance | DST-1 to DST-8 | the renderer, the input time, the reprojection, the near validator, the market measurement, the class line, the dock, the energy |

**The count**. The history is 90 at this part's first writing, then 103, then 110, then 115. **At Revision L.5.0 the count comes from `tools/check_crossrefs.py` (gate PRG-15) against `tools/canon.json`**. Each gate has a written pass condition, an instrument and a raw data rule. The verification line owns the register. `[DECISION]`

---

## 12.3 The raw data rule and the record format

1. **One file name rule**. `GATE-ID__member__serial__date__instrument.csv`.
2. **One raw data format**. Use a plain text table with units in the header and a calibration comment block.
3. **One instrument per quantity**, with a calibration date inside its validity window.
4. **One record per gate in B.U.D.**. Store it under program authority, readable by the device owner.
5. **The negative results are kept**. A gate that fails keeps its data, and the failure is in the register with a date and an owner. A gate that passes keeps the data that proves it.

**The record fields of a gate**.

```text
GateRecord { gate_id, member, serial, date, instrument, calibration_date,
             conditions, raw_pointer, result, margin, owner, decision }
```

---

## 12.4 The laboratories and the rigs

| The asset | What it measures | The class |
|---|---|---|
| the bend rig | a cycle at a radius, with an image, a capacity and a touch report | a servo rig with an optical window |
| the coupon station | the stack strain, the adhesive creep, the gel behaviour | a universal test machine with a climate chamber |
| the cassette rig | 1 000 cycles, the contact resistance, the latch force | a custom rig |
| the wired and contact charge bench | the USB-C path at 40 and 25 W, the contact pads at 25 W, the pad loss at 0, 20 000 and 50 000 mates | a calibrated bench with a mating machine |
| the antenna range | the pattern, the efficiency, the desense, the bent match | an accredited range |
| the display metrology set | the brightness, the colour volume, the uniformity, the seam, the refresh | a calibrated photometer and a camera |
| the cell cycler and the abuse cell | the capacity, the cycle life, the abuse set | an accredited laboratory |
| the link impairment bench | the latency, the loss, the jitter, the class behaviour | a network emulator |
| the secure element bench | the boot, the signature timing, the energy, the anchor | a bench with a current probe |
| the mass and the thickness metrology | the gram, the micron, the flatness | a calibrated balance and a micrometer stage |
| the camera bench | the modulation transfer, the power, the heat, the magnets | an optical bench and a thermal camera |

---

## 12.5 The claim policy

### 12.5.1 The three tiers of a claim

| The tier | The support | The wording |
|---|---|---|
| **Proven** | a gate with raw data on a prototype or a pilot | a number, with the member and the configuration |
| **Designed** | a model with a written assumption and a named gate | "the design target is X, and gate Y measures it" |
| **Studied** | a study with a source and a date | "the study found X, and the case is stated" |

### 12.5.2 The forbidden words and phrases

Forbidden claim terms: *all day*, *unbreakable*, *zero latency*, *no hardware*, *VR ready*, *metaverse*, and *a private display*. Forbidden device-class words: *phone*, *tablet*, *television*, *monitor*, *laptop*, *computer*, and any unverified superlative. `[DECISION]`

### 12.5.3 The claim rules that follow from the physics

| The claim | The rule |
|---|---|
| the thickness | always names the part: the leaf 4.00 mm, the module 4.00 mm, the attached stack 8.00 mm |
| the mass | always names the cassette and the module state |
| the runtime | always names the member, the cassette and the session class |
| the sharpness | always states the angular density at the intended distance |
| the link | never a global latency figure; the measured class of the market |
| the camera in the sun | the honest limit of Part 7, Section 7.4 |
| the clear panel | the transmission number, and the dimmer state |

---

## 12.6 The verification gates of the program itself

| Gate | The test | The pass condition |
|---|---|---|
| PRG-1 | the number consistency: every quantity appears once per volume | no contradiction across the directive |
| PRG-2 | the tag check | no number without a tag, no claim without a gate |
| PRG-3 | the name check | no forbidden word in a claim, a file name or an identifier |
| PRG-4 | the drawing check | an overlap, an overflow, a covered text, a stale footer: all zero |
| PRG-5 | the plan check | no block without an owner, no gate without a data route |
| PRG-6 | the claim check | every public sentence maps to a gate or to a study |
