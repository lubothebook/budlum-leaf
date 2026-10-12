# BUDLUM LEAF · THE DIRECTIVE · PART 15 · THE HARDENING ADDENDA

**What this part is**. The hardening pass of 2026-10-05. It corrects the errors that the audit found. It adds the policies that a program of this kind needs, and that the earlier parts left to habit. Every item has a number, a rule, a gate and an owner line. `[DECISION]`

---

## H-1 · The near-eye density correction (a real error, found and fixed)

**The error**. The earlier text stated "176 ppd at the eye" for the Leaf Frame. That number came from the flat screen formula `ppd = pixels per mm × millimetres per degree` at a 20 mm eye relief. **It is wrong**, because the optics map the whole panel onto a field of view. The eye reads the panel pixels across divided by the field across. `[GENERAL]`

```
ppd (near eye) = the panel pixels across / the field of view across in degrees
```

| The case | The panel | The pixels across | The field | The density |
|---|---|---|---|---|
| the family panel in a Frame lens | P80 | 1 600 | 70° | **23 ppd** |
| the family panel in a Frame lens | P80 | 1 600 | 60° | 27 ppd |
| **the Frame, the corrected requirement** | a 4K class microdisplay | 4 200 | 70° | **60 ppd** |
| the requirement at the panel | n.a. | 4 200 px across a 45 mm clear aperture | n.a. | **about 2 400 ppi** |
| the Field mode, one eye of a Leaf 160 | P160 | 3 200 px across a 152° panel, of which one eye sees about 100° | 100° | **about 21 ppd** |
| the Field mode, to reach 40 ppd | n.a. | 4 000 px across the visible field | 100° | a panel that does not exist in the family today |

**The corrections**.

1. The Frame uses a **4K class microdisplay of about 2 400 ppi** behind the clear lens, not the family panel. The family panel stays in the Leaf Window and in the surface over glass. There the user holds the surface at arm's length, and the flat formula applies.
2. The **Field mode is a scene mode at about 20 to 25 ppd per eye**. A text page is the poor case, and the claim states it.
3. **A near eye claim states the pixels across and the field across, and divides**. The rule applies everywhere. A claim using pixels per inch for a near-eye surface is refused.
4. The Frame density is a new gate, **CLR-11**, and the microdisplay joins the partner ask of Part 13, Section 13.3.

`[HYPOTHESIS]` The microdisplay class exists in the supply chain; the exact part, the price and the clear aperture are the subject of gate CLR-11.

---

## H-2 · The thickness ledger, one sum

The audit found two numbers for one face (0.46 and 0.59). The ledger is now single, and every thickness table in this directive adds to it.

| The element | The thickness | The note |
|---|---|---|
| the face stack | 0.46 mm | the coat, the cover, the adhesive, the touch, the emissive stack, the encapsulation, the backplane, the backing |
| the cassette | 2.88 mm | the fixed standard |
| the second face stack | 0.46 mm | identical |
| the shared spine | 0.06 mm | at the edge and in the wrap zone |
| the weld bead | 0.04 mm | the perimeter |
| **the closed body** | **3.90 mm nominal** | and **4.00 mm maximum** with the adhesive and the fit allowance |

**The rule**. 0.46 + 2.88 + 0.46 + 0.06 + 0.04 = 3.90. The 4.00 mm answer of Ayaz is the maximum, and the ledger proves the nominal. `[DECISION]`

---

## H-3 · The gate register, corrected

The audit found 90 in Part 12 and 89 in the register. **A count is a fact, and two counts is a defect**. The register before this part was MEC 13, ENR 6, DSP 10, RF 8, CAM 9, CLR 10, FLD 6, SW 13 and DST 8. That made 83 device and network gates, plus the 6 program gates. **The counting is a tool now**: `tools/check_crossrefs.py`, gate PRG-15, with the canonical numbers in `tools/canon.json`. Every count claim is measured against them. `[DECISION]`

| The register at revision L, from the tool | The value |
|---|---|
| the device and the network gates | **123** |
| the program gates | **16** |
| the research gates of the Ar-Ge plan | **17** |
| **the total** | **150** |
| the gap items of Part 16 | **39: 13 blockers, 19 major, 7 minor** |

**The rule that follows**. A gate exists when it has a written pass condition, an instrument and an owner. A gate that is named in prose and has no row is not a gate, and gate PRG-15 reports it. Section H-16 writes the rows that the addenda had left in prose.

**The rule**. A gate is added only with a pass condition, an instrument and an owner. The gate count is maintained by the verification line, and Part 12 is corrected at its next revision.

---

## H-4 · The firmware update, the rollback and the attestation policy

| The item | The rule |
|---|---|
| The slots | two signed images, A and B, with a monotonic anti-rollback counter in the secure element |
| The update | signed by the program key **and** accepted by the secure element; the device verifies before it boots the new slot |
| The rollout | staged: the program ring, then a 1 percent ring, then 10 percent, then all; a fault in a ring stops the rollout |
| The rollback | one action, always available, to the last known good image; the counter permits a rollback to a stated floor |
| The recovery | a recovery image in a protected region that can restore a device with no working slot |
| The attestation | the device reports the hash of the running image and the counter in every session handshake. An operator can require a stated floor |
| The rule | **a Leaf never becomes a brick**, and an update that cannot be rolled back is not shipped |
| The ownership | the firmware line, gate SW-14 |

---

## H-5 · The wallet recovery and the device replacement flow

| The step | The rule |
|---|---|
| The guardians | a t of n guardian set chosen by the user, each guardian holding a share, and the set changeable only with a quorum |
| The recovery | a new or recovered device rebuilds the authority from the quorum. A delay window applies, and the old device gets a notice if it is online |
| The lost device | one action revokes the device key, and a lost device cannot answer a challenge after the next period |
| The replacement device | it binds to the user authority, imports the session state from B.U.D., and re-binds the module and the cassette with one action each |
| The module and the cassette | a part keeps its record; the new pair is written into all three records, and an old pair is revoked with one action |
| The grace | a 72 hour notice window for a recovery, during which the user is told through every live surface |
| The ownership | the authority line, gate SW-15 |

---

## H-6 · The factory provisioning and the personalization chain

| The step | The rule |
|---|---|
| The birth certificate | the device is created with its serial, its secure element identity, its panel identity, its cassette and its module. All of it is signed at the line |
| The key injection | in a protected cell, at the secure element maker or at the line; the private keys never leave the element |
| The personalization | the element holds the device key, the attestation counter and the pairing records; the injection is audited and the audit is part of the record |
| The test record | the function test, the calibration, the radio power, the bend and the leak results, signed and stored |
| The manifest | the geometry manifest of Part 1, Section 1.6 is signed at the line and stored in B.U.D. |
| The anti-counterfeit chain | a part is genuine when its record signature chains to the maker key; the chain is checked on every part insertion |
| The rule | a part without a chain is refused with the failing field on the surface |
| The ownership | the partner line and the firmware line, gate SW-16 |

---

## H-7 · The page capability model and the developer surface

**The gap this closes**. The directive said "a page cannot cover a label" and "a page cannot paint the local floor". It never said what a page **is**. That is written now. `[DECISION]`

```text
PageManifest { page_class: C0b|C1|C2|C3, sensors: [SensorId], labels: bool,
               energy_hint: Tier, deadline: DeadlineClass, signature }
```

| The element | The rule |
|---|---|
| The page model | a page is a **signed display list** (`SceneModel` of Part 8) plus the class it declares and the sensors it asks for |
| The capabilities | a page declares its class, its sensors, its energy hint and its deadline; a capability token is granted per session, per class, per sensor |
| What a page never does | paint the local floor. Cover a label. Take a sensor that the lease does not name. Ask for a class the path cannot carry. Hide its class |
| The Budscan split | **the browser engine runs on the validator, and the device renders the display list and the video classes**. The device never runs a browser engine. A Gecko class engine in a 4 mm body with no processor is a contradiction. `[TREE]` Budscan's fetchers and its name rule stay on the validator side. Their honesty rule (each fetcher declares its own strength) becomes the page honesty rule |
| The render classes | C0b model, C1 delta, C2 video, C3 still: the page declares one, and the surface shows it |
| The developer surface | an SDK that emits a signed `PageManifest` and a `SceneModel` stream. A simulator of the device classes. The review rule: a page that cannot declare its class is not published |
| The ownership | the surface line and the network line, gates SW-17 and SW-18 |

---

## H-8 · The acoustic design specification

| The item | The value |
|---|---|
| The microphones | 3, across the module, at 55 mm and 45 mm spacing, on a 0.5 mm acoustic port each |
| The beam | a target of a 30 dB front to back ratio in the voice band, and a 6 dB beam width stated |
| The noise floor | below 30 dBA equivalent at 30 cm in a quiet room |
| The speaker | one 1 W class full range driver at 75 dB SPL and 30 cm. A rear volume of 1.2 cm³, and a vent to the module edge |
| The jack | a 3.5 mm receptacle with a detection switch; the headset path disables the speaker |
| The haptics | one linear actuator in the module or the keep-out band, four waveforms: a tap, a tick, a bump, a long buzz |
| The wind and the water | a mesh at the port that holds the class of gate MEC-19, and a wind noise rule at 5 m/s |
| The ownership | the module line, gate CAM-10 |

---

## H-9 · The simulation plan, and the rule that a simulation is not a gate

| The simulation | The tool class | What it predicts | The acceptance |
|---|---|---|---|
| The structure | a non linear finite element model of the decoupled stack in the wrap | the layer strain, the interface shear, the slip and the flat recovery | inside 15 percent of the coupon measurement |
| The thermal | a 3D model of the leaf, the module, the cassette and the hand | the steady state and the burst rise | inside 3 °C of the bench |
| The optics | a ray trace of the monogram, 8 elements in 4 groups on the folded path, and the Frame lens | the modulation transfer, the field curvature, the distortion and the CRA under **25 degrees** | inside 10 percent of the bench |
| The antenna | a full wave model of the leaf, the spine, the cassette and the module | the efficiency, the pattern, the desense | inside 1 dB of the range |
| The acoustics | a boundary element model of the module and the head | the beam and the SPL | inside 3 dB of the bench |
| **The rule** | a simulation narrows a design space and orders the coupons. **It never replaces a gate**, and a claim never rests on it alone. `[DECISION]` |
| The ownership | the systems line, gate PRG-7 |

---

## H-10 · The accessibility rules

| The item | The rule |
|---|---|
| The text | a minimum text scale on every member, stated in millimetres of cap height at the intended distance. A scale control that never breaks the layout |
| The contrast | a stated contrast floor for body text on every background the surface can draw, including the clear panel over a bright scene |
| The control | **every core action is reachable by voice and by gaze**, not by touch alone: the wallet, the class change, the session move, the camera lease |
| The one hand | the core actions are reachable one handed on a carried member; the corner and the edge rules of Part 3 help here |
| The colour | no meaning is carried by colour alone: the class line, the energy state and the camera state each carry a shape or a word |
| The hearing | the sound set is never the only channel for a state; a visual and a haptic channel carries every alert |
| The Frame | the prescription path and the interpupillary range are part of the product, and a user outside the range is told so at the order |
| The ownership | the surface line, gate PRG-8 |

---

## H-11 · The privacy impact assessment and the data map

| The class of data | The examples | The default | The retention |
|---|---|---|---|
| The identity | the authority, the guardians, the session grants | on | until the user revokes |
| The session state | the buffers, the checkpoints, the class history | on | a stated window, then dropped |
| The camera and the audio | the captures and the derived events | **off until a lease** | per the lease |
| The telemetry | six groups under the Pollen rules | off, opt in | a stated window |
| The part records | the cassette, the module, the service events | on | the life of the part |
| The gate data | the test results | on, under the program authority | the life of the program |

| The rule | The statement |
|---|---|
| The impact assessment | a written DPIA in the Turkish and the European frames before the pilot, with the data map above as its spine |
| The child safety | no camera and no microphone without a lease, a stated age stance, and no behavioural profile of a minor by default |
| The defaults | every sensor and every telemetry class is off until the user turns it on |
| The wipe | a return, a repair and a resale each run a stated wipe, and the wipe is recorded |
| The ownership | the privacy line, gate PRG-9 |

---

## H-12 · The end of life, the take-back and the support window

| The item | The rule |
|---|---|
| The software support | **7 years of security updates** from the last sale of a member, with the end date published on the surface and on the box |
| The parts | 5 years of spare parts, with the list public |
| The take-back | a take-back path in every market of sale, under the electrical and electronic waste rules |
| The cell | a cassette returns to a cell recycling path, and the record follows the cell |
| The panels | a panel returns to the panel partner's recovery line where one exists |
| The data | the wipe of H-11 runs before a device leaves the user |
| The ownership | the program line, gate PRG-10 |

---

## H-13 · The cost model: the structure only, because the numbers are deferred by order

| The level | The content |
|---|---|
| The BOM tree | the panel pair, the touch and the cover, the spine. The hub and the memory, the radios, the secure element. The cassette (cells, protection, gauge, shell). The module (cameras, cell, sound, magnetics, shell). The pen and the packing |
| The cost drivers | the panel yield and the mask count. The cell energy density and its price. The folded optics yield. The module assembly time, the weld cycle time and the test time |
| The tooling | the panel mask set, the cut line, the module fixture, the cassette fixture, the assembly fixture, the test fixtures |
| The price classes | a structure of three classes per member (a base class, a mid class, a collector class), with no number stated before a partner quotation `[DECISION]` |
| The rule | a cost number enters this directive only with a quotation reference and a date. Until then the structure stands alone, and no price claim is made in public `[DECISION]` |
| The ownership | the program line, gate PRG-11 |

---

## H-14 · The dock, the rail and the coupler interface

| The interface | The contacts | The signals |
|---|---|---|
| The edge coupler | 12 | 4 power (2 pairs), 4 ground, 2 data lanes, 1 identity, 1 sense |
| The dock | 14 | as above, plus the mains pair |
| The rail | a bus along the spine | 48 V and ground, a serial pixel link, a control pair, a sense pair |
| The module | 10 | 4 power, 3 ground, a data pair, an identity, a sense |
| The rule | a connector is rated at 1 000 cycles, wiped on insertion, and it never carries a signal that a wrong insertion can damage `[DECISION]` |
| The ownership | the structure line, gate MEC-14 |

---

## H-15 · The economics of the network, in structure

| The item | The structure |
|---|---|
| The meter | a session is metered in milliseconds of the effort tier and in bytes of the class, and the meter is visible to the user |
| The classes | an interactive class, a standard class and a deferred class, each with its own meter and its own honesty line on the surface |
| The validator reward | a near validator earns for the cache, the composition, the buffer and the relay, and it carries a stake and a challenge like any validator |
| The rule | **the device never spends another user's compute without a stated price**. This directive states no price, because the cost items are deferred by the order of Ayaz `[DECISION]` |
| The honesty | the surface shows what a session is costing, in the same way it shows the class |
| The ownership | the network line, gate SW-19 |

---

## H-16 · The rows of the gates that the addenda introduced

**Why this section exists**. The addenda H-1 to H-15 introduced gates in prose. A gate without a written pass condition is not a gate, and the count check of PRG-15 refuses one. This section writes the rows. `[DECISION]`

| Gate | The subject | The pass condition | The owner |
|---|---|---|---|
| **CLR-11** | the near-eye density of the Frame: the microdisplay class, the clear aperture and the price | a measured figure of pixels across divided by field across, with a named part, a clear aperture and a price | the optics line |
| **CAM-10** | the acoustic design specification of the module: the microphone array, the small speaker and the 3.5 mm jack | the stated loudness, distortion and wind noise at 5 m/s, inside the limits of Part 6 | the module line |
| **SW-14** | the firmware update, the rollback and the attestation policy | a staged rollout with a rollback in every case, and no brick in 1 000 forced failure updates | the firmware line |
| **SW-15** | the wallet recovery and the device replacement flow | a recovery from the t of n quorum inside the grace window, the lost device revoked, and each re-binding in one action | the authority line |
| **SW-16** | the factory provisioning and the personalization chain | a signed birth certificate per unit, the keys never leaving the secure element, and the provisioning audit in the record | the partner line and the firmware line |
| **SW-17** | the page capability model | a page declares its capability, a page without a grant cannot read, and a lying stub is refused by a gate | the surface line |
| **SW-18** | the developer surface and the SDK | the SDK builds against the model, and the sample application passes the permission set of the model | the network line |
| **SW-19** | the economics of the network, in structure | a unit cost for every network function, with a source per number, and the structure only per the deferral of H-13 | the network line |
| **PRG-7** | the simulation plan | every simulation names its model, its inputs and its error bar, and **a simulation is not a gate** | the systems line |
| **PRG-8** | the accessibility rules | every core task is reachable without sight, with a hearing aid and with one hand, against the named audit rule set | the surface line |
| **PRG-9** | the privacy impact assessment and the data map | a data map per function, a lawful basis per field, and an assessment before the first sale in Turkey and in the European Union | the privacy line |
| **PRG-10** | the end of life, the take-back and the support window | a take-back route per member, a parts window of the stated years, and the recycling and wipe flows as procedures | the program line |
| **PRG-11** | the cost model, in structure | the structure of the cost with every driver named, and the numbers deferred by the order of Ayaz | the program line |
| **PRG-12** | the writing check: the em dashes and the sentence length | no em dash in any file, a descriptive sentence of 25 words or less, and a procedural sentence of 20 words or less | the directive line |
| **PRG-13** | the legal reading of the energy route A and route B in Turkey and in the European Union | a written opinion per route, and the route that ships is the route the opinion supports | the legal line |
| **PRG-14** | the freedom to operate: the register, the dates, the design-arounds and the design log | an attorney signs the register before the first sale, every date is verified, and a blocked choice is out of this directive | the legal line |
| **PRG-15** | the count check | one count per number, held in `tools/canon.json` and measured by `tools/check_crossrefs.py`, and a named gate with no row is a defect | the verification line |
| **PRG-16** | the assembly check | each part once, in ascending order, and one H1 header per FINAL file, measured by `tools/assemble.py` and `tools/check_crossrefs.py` | the directive line |
| **MEC-14** | the dock, the rail and the coupler interface | the coupler draws the stated force, the rail carries the stated load, and the optional board fits every size of the family | the structure line |
| **MEC-25** | the interface ring of the module: the retention, the shear, the peel, the attach cycles and the drop with the module fitted | 25 N normal new (20 N after 1 000 cycles), 12 N shear, 8 N peel, and zero release in 1.2 m drops (30 coupons/condition) | the structure line |
| **MEC-26** | the cell notch: the capacity, the insulation, the clearance and the bend at a notch | the capacity inside 10 percent of the notched table of Part 20, no short, and no crack after 10 000 cycles at R 25 mm | the energy line |
| **CAM-11** | the top-edge seat of the upright B module: identity, `6.5 N` magnetic hold, alignment and balance | the part holds `6.5 N` normal and `3.2 N` shear at `y = +80.0 mm`, registers within `±0.10 mm`, and keeps `0 mm²` screen covered | the camera line |
| **CAM-12** | the upright B module on the desk, the room and the wall members | the camera axis inside 2 degrees of the stated line, with no user tool | the camera line |
| **DUO-7** | the fitted upright B module on the top edge leaves both rectangular screens 100 percent open | `11 947 mm²` live at `508 ppi` on both faces (`0 mm²` covered), nothing scaled, and text size unchanged | the surface line |
| **DSP-12** | the touch map with the upright B module fitted on the top edge and with none | no dead touch zone on either `76.4 x 156.4 mm` face, and full `240 Hz` touch/pen reporting | the display line |
| **DSP-13** | the full `11 947 mm²` canvas of each face with the upright B module seated | the page model uses the full `1 528 x 3 128 px` rectangular screen (`R = 1.40 mm` screen corner) | the display line |
| **CAM-13** | the camera interface and the wait | the live view inside 20 ms on the main screen and rear round panel, and uplink time stated before shutter | the camera line |
| **MEC-27** | the top-edge B module joint: `6.5 N` hold, `3.2 N` shear, hand release and `IP68` gasket over `50 000` seats | the numbers of `HARDWARE/08` and `HARDWARE/10` on 30 modules | the camera line |
| **MEC-29** | the top-edge magnetic array (`8 + 8` `N52H` alternating poles) and `R 25.5 mm` body bend compatibility | `6.5 N` normal hold, `3.2 N` lateral shear, `<0.5 mT` stray flux at `8 mm`, and zero unseating at `R 25.5 mm` | the structure line |
| **MEC-30** | the 12-pad top-edge gold interface: contact sequencing, `5 Gbit/s` wired link and `400 Mbit/s` wireless link | ground mates `0.25 mm` early, 1-wire auth in `<3 ms`, `20 mΩ` contact resistance | the surface line |
| **MEC-31** | curved stand and Desk Dock posture with the upright B module seated | stable self-standing arc or `8°` dock posture with `27 W` charging | the structure line |
| **MEC-32** | the full-length bend of the `2.00 mm` 4-Quadrant (`+`) body: `10 000` wraps at `R 25.5 mm` and `50 000` bends at `R 70 mm` | zero T-OLED or `LLZO` crack, `<15 µm` `+` seam intact, and flat recovery `<0.05 mm` | the energy line |
| **MEC-33** | the `80.0 x 160.0 x 2.00 mm` 4-Quadrant (`+`) body mass (`4 x 17 g`) and complete modular mass | **68 g inside 4 percent** (**`88 g`** complete with the `20 g` `90°`-bent-stem B module) | the structure line |
| **MEC-34** | the `2.00 mm` 11-layer `ISO 10993` polycarbonate + `T-OLED` + `LLZO` stack and `<15 µm` (`n = 1.585`) `+` seam | **2.00 mm inside 0.03 mm**, Z-step `<2.5 µm`, and flat within `0.05 mm` over `160.0 mm` | the structure line |
| **MEC-35** | the waterproof seal of the `<15 µm` (`n = 1.585`) `+` cross lip and `90°`-bent B stem edge dock | **IP68 (`1.5 m`, `30 min`)** before and after `5 000` wraps and `5 000` quadrant swaps | the structure line |
| **MEC-36** | the attachment forces: `11.2 N` `+` seam magnetic pull, `18.5 N` shear and `7.2 N` `90°` B module hold | each force inside `1 N` over the stated cycle life | the structure line |
| **MEC-37** | the drop, twist, and 12 softened edges (`R = 6.35 mm` corners + `r = 0.65 mm` body and `r = 0.55 mm` B edges) | **1.5 m** on six faces with no crack, and all 12 edges pass the `10 N` tactile roll test | the structure line |
| **MEC-38** | the heat of the body: corrugated graphite-Cu spreaders (`1 200 W/m·K`), faces and derate | under **3 K/W** across the spreader, and surface `<43 °C` under load | the structure line |
| **DK-1** | the deck: the stiffness, the feet and the 310 g mass | under 0.2 mm of flex under 25 N at the land, and the mass inside 4 percent | the dock line |
| **DK-2** | the seat: the insertion, the shear, the peel, the pegs and 5 000 cycles | 25 N, 12 N and 8 N inside 1 N each, and no wear of the land | the dock line |
| **DK-3** | the power path: the pads, the contract, the boost and the dead pad law | 27 W with 0.06 W in the pads, and a dead pad with no device seated | the dock line |
| **DK-4** | the network: the PHY, the switch, the data pair and the dock radiators | 2.5 Gbit/s inside 10 percent of the reference eye | the dock line |
| **DK-5** | the deck seal | IP52 on the deck, and IP54 at the seat with a device on it | the dock line |
| **DK-6** | the heat: the deck at 27 W, the bay at 28 W and the noise | 6.4 K on the deck, under 70 °C at the bay, and 22 dBA | the dock line |
| **DK-7** | the bay and the validator board: the seat, the seal and the swap | the board seats in one motion, seals, and is read in 4 s | the dock line |
| **DK-8** | the B module post: the hold, the power and the alignment | the axis inside 2 degrees, 5 W, and the top-edge seat holds `6.5 N` | the dock line |
| **DK-9** | the wall mount: the VESA pattern, the level and a 21 g part | level inside 0.5 degree, and no twist with the part on | the dock line |
| **DK-10** | the light, the label and the identity of the deck | three states readable at 1 m, and the identity answered in 3 ms | the dock line |
| **DSP-14** | the top-edge joint and perimeter frame against the panel: touch map and antenna efficiency | no dead touch zone within `1.8 mm` bezel, and under `0.5 dB` of antenna coupling loss | the display line |
| **DSP-15** | the polycarbonate + flexible AMOLED stack at the wrap: `10 000` wraps at `R 25.5 mm` and `50 000` bends at `R 70 mm` | no barrier crack, zero pixel loss, and `0.63 percent` strain held elastically | the display line |
| **DSP-16** | the face: `250 µm` optical polycarbonate + `10 µm` hard coat abrasion, bond, `IP68` edge seal and mass | 2H pencil and 1.5 kg steel wool with no visible mark, no delamination, and **7.2 g per face inside 4 percent** | the display line |
| **RL-1** | the life of the three connectors | 10 000 USB-C mates and 10 000 USB-A insertions, each under 100 mΩ | the rail line |
| **RL-2** | the power path and the contract | 40 W through the pads with a compliant PD contract, and the derate at 38 °C | the rail line |
| **RL-3** | the USB-A host output | 5 V at 1.5 A, and a drop under 150 mV at the limit | the rail line |
| **RL-4** | the jack and its detect order | the detect before the bias, 3 µV of noise and 2.8 V of microphone bias | the rail line |
| **RL-5** | the hub and the board path | 2.0 A of charging in, and the USB 3.2 split at the stated rate | the rail line |
| **RL-6** | the wired network over the rail pair | 2.5 Gbit/s inside 10 percent of the reference eye | the rail line |
| **RL-7** | hot removal at 40 W | no arc, no reset, and the path opens 1.2 ms before separation | the rail line |
| **RL-8** | the pad life | 5 000 mates under 100 mΩ, and no gold transfer to the wiper | the rail line |
| **RL-9** | water with the module seated | IP68 after the 5 000 mate set | the rail line |
| **RL-10** | water with the module off | IP68 on the recessed receiver pads, and the moisture record of the receiver | the rail line |
| **RL-11** | the audio chain | 30 mW into 32 Ω with the stated noise floor | the rail line |
| **RL-12** | the drop with the module seated | 1.5 m on six faces, and the module stays on | the rail line |
| **RL-13** | the latch life | 5 000 cycles inside the 3.5 to 5.0 N window | the rail line |
| **RL-14** | the identity of the module | pairing in 4 s, and the challenge answered in 3 ms | the rail line |
| **RL-15** | the module thermal | 0.10 W and 4.6 K at 40 W with no data running | the rail line |
| **RL-16** | the wiper and the seat | 3 × 0.35 N on the module, and a seat of 5.40 and 6.00 mm | the rail line |
| **RL-17** | the cable strain | 30 N of pull on the module, with no damage to the seat or the pads | the rail line |
| **RL-18** | the keyed seat | a wrong module does not seat, and the record names it | the rail line |
| **ENR-11** | the 4-Quadrant (`+`) `LLZO/PEO` solid-state battery (`4 x 3.0 Wh = 12.0 Wh`, `3 200 mAh`, `750 Wh/L`) | **`12.0 Wh` (`3 200 mAh`)** target capacity in `68.0 g` (`4 x 17 g`) body, resistance `<28 mΩ` | the energy line |
| **ENR-12** | the central `Ø54.0 mm` 4-sector `Qi2.2` (`15-25 W`) + `4 x Ø22.0 mm` `Qi` coils, `64` gold leaves, and `3 ms` Dead-Pad | universal wireless charging on any pad, **`3 ms` Dead-Pad auth**, and **`IP68`** sealed | the energy line |
| **ENR-13** | the **`<3 s` tool-free quadrant hot-swap (`EU 2023/1542` Art. 11)** and `180 mF` holdover buffers | any 1 tile swaps in **`<3 seconds`** while remaining 3 tiles (`9.0 Wh`) keep session active | the energy line |
| **ENR-14** | the `750 Wh/L` `LLZO/PEO` solid-state cells over `1 000` charge cycles | `>88%` capacity retention at `1 000` cycles, `0.0%` cell swelling | the energy line |
| **ENR-15** | non-flammable `LLZO/PEO` puncture/cut safety (`0%` liquid, `0.0 ppm` HF) and sole `USB-C` (`40 W`) protection | zero fire, zero smoke, `0.0 ppm` HF gas on nail penetration and `150 °C` oven test | the energy line |
| **ENR-16** | eyewear ocular thermal limiter (`<=36.2 °C` hardware NTC), `<0.08 µT` bifilar ELF, and `ISO 10993` biocompatibility | hardware comparator cuts current at **`36.2 °C`**; `ISO 10993-5/-10` and `SAR = 0.054 W/kg` verified | the energy line |
| **ENR-17** | coplanarity and optical invisibility of the `<15 µm` (`n = 1.585`) `+` cross seam and `(0,0)` Ti hub | Fresnel reflection `R < 0.0001%`, Z-step `<2.5 µm` on tapered Grade-5 Ti pins | the energy line |
| **ENR-18** | `2.00 mm` (`68 g`) 4-Quadrant (`+`) bending fatigue (`10 000` wraps at `R 25.5 mm`) | **`0.38 percent` max polycarbonate strain**, `0.22%` `LLZO` strain, `<+2%` ΔR | the energy line |
| **ENR-19** | cryptographic Dead-Pad IC (`3 ms` handshake) across all `64` `+` seam leaves and `12` B dock pins | contacts stay at `0 V` until `3 ms` auth passes; laser mark legible at `0.3 m` | the energy line |
| **ENR-20** | `+` cross magnetic & Ti pin hot-swap life (`10 000` swap cycles) | `10 000` swaps inside `11.2 ± 1.0 N` pull hold, retaining `IP68` seal and `<18 mΩ` resistance | the energy line |
| **ENR-21** | the `750 Wh/L` `LLZO/PEO` all-solid-state cell chemistry inside each `40 x 80 x 2.00 mm` polycarbonate tile | `3.0 Wh` (`800 mAh`) per tile (`12.0 Wh` total), verified `1 000`-cycle curve | the energy line |
| **ENR-10** | the silicone OCA shear-slip layers (`2 x 0.05 mm`, `G = 0.08 MPa`) inside the `2.00 mm` 11-layer tile stack | `0.16 mm` smooth shear slip at `R 25.5 mm`, keeping outer `ISO 10993` PC strain at `0.38%` | the energy line |
| **MON-1** | the upright 1:1 `uploads/b.png` silhouette (`40.0 × 32.0 × 4.00 mm`, `IoU >= 0.998`, open concave valley) | contour within `±0.10 mm` of `uploads/b.png`; zero parts in the upper valley | the camera line |
| **MON-2** | the `4.00 mm` thickness flush with the `4.00 mm` rectangular prism body | `4.00 ± 0.03 mm` across both vertical bar and ring; zero front or back protrusion | the structure line |
| **MON-3** | the fixed front camera inside the `Ø24.0 mm` ring opening (`3.4 + 14.0 mm` folded optics, `12.8 x 9.6 mm` sensor) | zero rotating barrel or gears; MTF and `84°` FOV verified inside `2.36 mm` front depth | the camera line |
| **MON-4** | the rear round AMOLED panel (`Ø22.4 mm` active, `220 x 220 px`, `250 ppi`, `1-60 Hz`, `600 nits`) | clock, chronometer, widgets, animations and selfie viewfinder inside `1.56 mm` rear depth | the display line |
| **MON-5** | upright attachment at the bottom baseline (`y = 0.0 mm`) onto the top-left edge (`x = -40..0 mm`, `y = +80.0 mm`) | `6.5 N` normal hold, `3.2 N` shear, `±0.10 mm` self-centering snap, `0 mm²` screen covered | the structure line |
| **MON-6** | the in-ring micro-speaker (`11.0 x 3.2 x 1.2 mm` inside the upper front bezel of the `Ø24.0 mm` opening) | `78 dB SPL` at `100 mm`, sealed to `IP68`, zero external speaker block in the stem-to-ring valley | the camera line |
| **MON-7** | the in-ring dual MEMS microphones (`68 dB` SNR inside the lower front bezel of the `Ø24.0 mm` opening) | clear voice and video capture with beamforming and `IP68` hydrophobic acoustic mesh | the camera line |
| **MON-8** | the in-ring flush dual-tone LED flash (`2700K + 5600K`) | guide number `4.0` at ISO 100, recessed flush at `z = 3.84..3.97 mm` inside the ring bezel | the display line |
| **MON-9** | softening of all 90 degree edges on both the vertical bar (`çubuk`) and cylindrical ring (`r = 0.55 mm`) | `r = 0.55 ± 0.05 mm` radius transition verified by CMM and `10 N` tactile probe | the structure line |
| **MON-10** | cryptographic 1-wire authentication and main logic board ("beyin") inside the ring | `<3 ms` challenge-response before power enable; `8 GB` LPDDR5 frame buffer | the security line |
| **MON-11** | the vertical bar (`çubuk`, `x = 0..5 mm`, `y = 0..32 mm`) as the `Wi-Fi 7`, `BT 5.4` and `UWB` antenna | `>60 percent` efficiency across `2.4 / 5 / 6 GHz` and `6.2-8.2 GHz` UWB; zero extra antenna | the radio line |
| **MON-12** | waterproof sealing of the front sapphire window, rear polycarbonate cover, acoustics and bottom gasket | **`IP68` (`1.5 m`, `30 min`)** before and after `5 000` top-edge matings | the structure line |
| **MON-13** | the `0.55 Wh` internal module pouch cell and pyrolytic graphite thermal bridge | `25 min` standalone capture or `48 h` standby clock; surface `<43 °C` during `4K 60` capture | the energy line |
| **MON-14** | drop durability of the `21.0 g` upright B module (`1.5 m` onto 6 orientations, seated and standalone) | zero optical decentering (`<5 µm`), zero sapphire or polycarbonate crack | the structure line |
| **MON-15** | full `R 25.5 mm` body bend with the upright B module seated on the top edge (`y = +80.0 mm`) | module stays seated at `6.5 N` with zero contact interruption and `0 MHz` antenna detuning | the structure line |
| **MON-16** | first-contact ground sequencing (`0.25 mm` early `GND`) and dead-pad safety (`1 MΩ` unmated) | zero hot-plug arc across `50 000` matings, and `<1 µA` leakage in salt water | the security line |
| **MON-17** | tool-free hand removal (`<2 s`) and re-attachment (`<1 s`) on the top edge | smooth `6.5 N` pull or `4.2 N` peel release without tools | the structure line |
| **MON-18** | `50 000`-seat mechanical and electrical endurance of the 12 gold pads and `8 + 8` magnets | contact resistance stays `<30 mΩ` and magnetic hold within `±10 percent` | the structure line |
| **MON-19** | `96 h` salt-fog corrosion and skin-oil resistance of the `#93a68c` anodized 6061-T6 shell | zero corrosion pit, zero discoloration (`ΔE < 1.0`), and intact laser serial | the camera line |
