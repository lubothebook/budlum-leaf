# BUDLUM LEAF · THE DIRECTIVE · PART 11 · THE HEAT DOCTRINE

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ: the local renderer is a fixed-function compositor in `U1` with four jobs. No program runs on the device. Part 21, Section 21.5.4.

**The order that created this part:** *look at what can be done so that it does not heat up.* `[DECISION]`

---

## 11.1 The numbers

| The surface | The area | A 4 W load | The rise without a spreader |
|---|---|---|---|
| the module face | 111 cm² | 0.036 W/cm² | 10 to 18 °C above ambient |
| the leaf, both faces | 256 cm² | 0.016 W/cm² | 3 to 6 °C above ambient |
| the leaf plus the module, coupled | 367 cm² | 0.011 W/cm² | 2 to 4 °C above ambient |

**The conclusion**. The leaf is an excellent radiator because it is large, thin and two-faced. **The engineering problem is not the total heat; it is the local hot spot in the module**. `[DECISION]`

---

## 11.2 The twelve mechanisms

| No. | The mechanism | The how | The number |
|---|---|---|---|
| 1 | **Keep the heavy compute off the module** | the computational photograph runs on the validator | a local compute block would need 5 to 15 W and would turn a 4 mm module into a 60 °C surface |
| 2 | **A spreader inside the module** | a 30 to 50 µm graphite or annealed copper layer under the sensors, bonded to the shell | gate MEC-11 measures the path |
| 3 | **A thermal bridge at the interface** | a soft thermal pad at the contact band between the module and the spine | a target below 3 K/W |
| 4 | **A latent buffer** | 1 to 4 g of an encapsulated phase change material in the shell | about 200 J per gram: a 4 W burst of 60 s is 240 J |
| 5 | **The cell away from the sensor block** | a gap band and a thermal wall inside the module; the cell temperature is in the record | the cell is not heated by the camera |
| 6 | **Sensor-side power reduction** | binning and line skipping in video, an in-sensor HDR merge, a lower readout rate where the class allows | about 0.15 W per camera in video against 0.25 W in a full readout |
| 7 | **The encode moves to the hub where the class allows** | the sentinel compresses lightly (3 to 6 to 1) and the hub does the full encode | the heat moves from 111 cm² to 256 cm²; the flex carries 2 to 4 Gbit/s |
| 8 | **Duty and rate rules** | a 4K120 take of up to 10 s with a 20 s cooldown, or a 15 minute cap with a derate to 4K60 | measured by gate MEC-12 |
| 9 | **A temperature aware capture policy** | the camera refuses a 4K120 start above a stated module temperature and says why | the same honesty rule as the uplink wait |
| 10 | **A dark frame recalibration on the sensor temperature** | the temperature is carried in the record | a hot sensor drifts, and the number is known |
| 11 | **Air and radiation rules** | no insulating layer over a tile or a panel; the module shell is matte and dark | a matte surface radiates better than a gloss |
| 12 | **The ambient rule** | the thermal test set runs at 35 °C ambient, in a hand, in the sun and in a bag | gate MEC-11 |

---

## 11.3 The thermal budget of a capture

| The case | The total | The time | The rule |
|---|---|---|---|
| the viewfinder | 0.45 W | continuous | no limit |
| one still, three cameras metered | 1.65 W | 0.5 s | no limit |
| a night burst of 20 frames | 2.85 W | 2 to 4 s | no limit; the uplink can continue after the capture, and the capture itself is short |
| a 4K60 video | 2.50 W | continuous | no limit inside a 35 °C ambient |
| a 4K120 video | 4.00 W | continuous | a 10 s take and a 20 s cooldown, or a 15 minute cap and a derate to 4K60, whichever the gate measures as safer |

**The surface states what it is doing**. `cooling`, `warm`, `capture limited` are three visible states, and each says the reason. `[DECISION]`

---

## 11.4 The charging heat

| The path | The input | The loss at 80 percent | The mitigation |
|---|---|---|---|
| wired, USB-C | 45 to 65 W | 9 to 13 W | the spreader of the cell field, and the derating curve |
| the dock and the rail, by contact | 25 W | **about 0.1 W**, and 0.31 W at a worn pad | gold pads on the fixed edge, spring pins in the dock |
| the wireless paths | **withdrawn** | n.a. | the order of Ayaz: no wireless charging. The 5 W that the induction link lost at 25 W stays out of the body |

**The derating curve**. Full power holds below 38 °C of the surface. Power derates linearly to 20 percent at 45 °C and stops above 48 °C with a message. `[DECISION]`

---

## 11.5 The thermal gates

| Gate | The test | The pass condition |
|---|---|---|
| MEC-11 | the module path: the spreader, the interface pad, the latent buffer, at 35 °C ambient, five capture classes | the module rise, the leaf rise and the cell temperature inside their limits |
| MEC-12 | the capture policy: a hot start, a long take, a cooldown, the message | the refusal works and the user sees the reason |
| MEC-6 | the charge heat at 10, 25, 45, 60 and 80 W, seated and removed | the derating curve and a surface inside the safety limit |
| CAM-6 | the camera thermal set, the duty rules, the cell temperature | the curve, the derate, a cell inside its limit |
