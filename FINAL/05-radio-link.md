# BUDLUM LEAF · THE DIRECTIVE · PART 5 · THE RADIO AND THE LINK

---

## 5.1 The radio set

| The radio | The class | The part | The note |
|---|---|---|---|
| Wi-Fi 7 | tri-band, multi-link operation, 320 MHz, 2 streams minimum and 4 preferred | a combo part with the Bluetooth radio | the main path indoors |
| 5G | standalone, sub-6 GHz, 4 × 4 MIMO, carrier aggregation | the same front end with a sub-6 module | the main path outdoors |
| Millimetre wave | an antenna in package, a 15 × 15 mm block per band | optional | short range, high rate, a dock path |
| Satellite | non-terrestrial through the cellular radio | no extra antenna | the last resort, a message class |
| Bluetooth | the wallet authenticator, the pen, the keyboard, the ear part | mandatory | the answer of Ayaz, question 14 |
| Near field | the tap and the pairing | | |
| Ultra-wide band | the ranging and the find-my-module function | a candidate | Part 6 |
| Navigation | multi-constellation | | |

---

## 5.2 The antenna law for a 160 × 80 mm body

1. **The upright B bar is the primary antenna**. On the top edge (`y = +80 mm`), the upright B bar projects into air. Because the top edge runs parallel to the `X` bend axis, the antenna never bends at `R 25.5 mm`. `[DECISION]`
2. **No radiator sits over the pixel area**. The panel stack costs 6 to 10 dB and detunes elements by 8 percent. Every antenna stays in the upright B bar and perimeter frame. Gates RF-9 and RF-11 measure the rule.
3. **The AgNW/ITO mesh and `90°`-bent B stem form the RF system**. Transparent `AgNW/ITO` layers inside the `2.00 mm` body couple to the `90°` B stem (`SAR = 0.054 W/kg`). Gate RF-10 measures the ground reference.
4. **The upright B bar houses `Wi-Fi 7`, `BT 5.4`, and `UWB`**. A module on the top edge gives `+2.4 to +3.4 dBi` gain, and a detached module acts as a relay. Gate RF-13 measures both states.
5. **The top-edge gold pads bridge the RF reference**. Pad 12 grounds the upright B bar to the prism frame across the `y = +80.0 mm` seat. When detached, the B module uses its `400 Mbit/s` link.
6. The match is measured flat, at the gentle bend and at the wrap, because the bend changes the geometry. The keep-out is a 6 mm ring of thinned ground and print around every radiator.

**The part by part file is `HARDWARE/19-THE-RADIO-AND-ANTENNAS-PART-BY-PART.md`**. It carries the 21 parts, the eight radiators, the ground arithmetic and gates **RF-9 to RF-20**. `[DECISION]`

---

## 5.3 The five conflicts, and the budget of each

| The conflict | The budget | The gate | The mitigation if it fails |
|---|---|---|---|
| The cassette sits between the antennas | the loss through the cassette | RF-2 | the window extends under the cassette edge, or the antennas move to the corners |
| The metal spine near the radiator | the efficiency of each antenna | RF-1 | the ring thinning, and a 3 mm stand off |
| The charge path against the radios | the desense of each receiver with the cable attached and on the dock | MEC-6, RF-3 | the shield of the receptacle, the pad routing and a filter. **The coil left the design, so the coil schedule left with it** |
| The bend changes the match | the return loss at R 70 mm and at R 25.5 mm against flat | RF-4 | a tunable matching network, written into the record |
| The module magnet over an antenna | the gain loss | RF-1, MEC-10 | the keep-out area, or the clip of Section 5.3.1 |

### 5.3.1 The decision rule of the attach

**An attach that costs 3 dB of antenna gain is worse than a mechanical clip, because the link is the product**. If the magnet loses more than 1.5 dB, the module moves to a clip, and the measurement decides. `[DECISION]`

---

## 5.4 The link classes

| The class | The downlink | The uplink | The round trip | The radio |
|---|---|---|---|---|
| C0 safe | none | none | none | the local floor |
| C0b model | a signed display list | a small intent | sub 20 ms | any |
| C1 delta | 10 kbit/s to 2 Mbit/s | below 100 kbit/s | 20 to 60 ms is good | Wi-Fi, 5G |
| C2 video | 10 to 30 Mbit/s | 100 kbit/s | below 40 ms | Wi-Fi 7, 5G |
| C3 still and 4K | 30 to 80 Mbit/s | 100 kbit/s | below 40 ms | Wi-Fi 7, millimetre wave |
| C4 camera up | 5 to 130 Mbit/s | the capture payload | the deadline classes of Part 10 | Wi-Fi 7, 5G, a near validator |
| The satellite class | measured only | | 20 to 40 ms | the message class |

`[PUBLICATION]` In 2026 bands, Wi-Fi 7 multi-link reaches a 12 ms 99th percentile and under 2 ms average at close range. Field 5G air latency is 8 to 12 ms, and an edge node 10 to 15 km away adds 1 to 5 ms. A central cloud is 50 to 100 ms, and direct-to-cell satellite is 20 to 40 ms.

---

## 5.5 The path manager, and how it chooses

```
PathCandidate { kind, rtt_ms, up_mbit, down_mbit, energy_mw, trusted, operator }
PathPlan      { primary, mirrors[2], floor }
```

| The order | The rule | Why |
|---|---|---|
| 1 | trust | an operator that fails the bond, the stake or the record test is out, whatever its latency |
| 2 | latency | the lowest measured round trip that can carry the class |
| 3 | energy | the least milliwatt per delivered megabit |
| 4 | the mirrors | two paths carry the critical intent, so a handover is invisible |

**How it is measured**. A rolling median and a 99th percentile per path, a 1 Hz probe on a silent link, and a full measurement on every class change. The numbers are kept in the session record. `[DECISION]`

---

## 5.6 The fail-safe ladder

| The state | The trigger | The behaviour | The user sees |
|---|---|---|---|
| Full | a path at or above the class | the session at its class | nothing |
| Reduced | the round trip above the class for 1 s | the class drops one step | the class line |
| Cellular | the local path is lost | the session moves | a move note |
| Satellite | everything else is lost | the message class | the satellite class |
| No link | no path at all | the local floor and the safe screen | the state |
| Optical | the user or the lease refuses a link | the optical path of Section 5.7 | the optical mode |

**The rule**. A session never enters a stuck state, and a reduction is always visible. `[DECISION]`

---

## 5.7 The optical path

1. The Budlum tree already carries the parts in B.U.D.. The note packing crate defines compressed, encrypted payloads and deterministic QR frames. `[TREE]`
2. **The rule**. A surface shows a signed receipt or payload as optical frames on the panel. The other device reads it with no radio. `[DECISION]`
3. **The cost, measured**. A 4 627 byte ML-DSA-87 signature payload takes about 240 frames. The transfer takes a few seconds on a held screen. `[TREE]`
4. **The implementation duty**. The device calls the note packing crate and never re-derives the packing. A second field definition is a silent failure class.

---

## 5.8 How the link is tested

| The test | The method | The number |
|---|---|---|
| The free hold and the hand hold | a calibrated range, a phantom head and hand, 3 bands | the efficiency and the pattern |
| The desense set | the transmitter on, the receiver measured | the desense per band |
| The bend | flat, R 70, R 25.5 | the return loss and the efficiency delta |
| The module as a site | attached, detached, on a table | the gain and the pattern |
| The class measurement | a 30 minute trace in two cities | the median and the 99th percentile |
| The handover | a planned and an unplanned move | the interruption time |

---

## 5.9 The radio gates

| Gate | The test | The pass condition |
|---|---|---|
| RF-1 | the antenna set: the efficiency, the pattern, the window, the anchor ring, the module gain | every budget of Section 5.3, and the 1.5 dB rule |
| RF-2 | the cassette in the field | the loss inside the stated budget |
| RF-3 | the desense with the charge cable attached and on the dock | both radios inside their stated margin in both states |
| RF-4 | the bent match | the return loss at the radius inside the limit |
| RF-5 | the path manager: a slow path, a lost path, a lying operator | the plan is correct and the untrusted path is never used |
| RF-6 | the fail-safe ladder, all six states | each state is reached and each is visible |
| RF-7 | the optical path: a receipt and a small payload, no radio | the reader verifies the receipt, and the frame count and the time are in the record |
| RF-8 | the satellite class, measured in a real market | the measured rate and delay, and the claim limited to it |
| RF-9 | the eight radiators: the band, the peak gain, the efficiency and the keep-out print | each band inside its window, the gain inside 1 dB, and the print hides the metal |
| RF-10 | the tiled steel as the RF ground, from 0.7 to 60 GHz | the mosaic behaves as solid ground, and the ripple stays under 0.5 dB |
| RF-11 | the panel keep-out: a radiator under the panel, and the detune it causes | no radiator over the pixel area, and under 0.5 dB of loss from the field |
| RF-12 | the bend: a radiator across the width, and the feed across the wrap zone | the match flat and at R 25.5 mm inside the limit, and no crack after 5 000 wraps |
| RF-13 | the module slot: the diversity path, the detached relay and the 1.5 dB rule | under 1.5 dB when seated, and a link at 10 m when the module is detached |
| RF-14 | the camera link: the part's own 400 Mbit/s link and the Wi-Fi Direct pair | 400 Mbit/s coded, no dropped frame in 30 minutes, and the pairing holds |
| RF-15 | the NFC coil, its ferrite and the first seat pairing | a 30 mm read range, and the pairing completes in one touch |
| RF-16 | the SAR at 1 g and 10 g, and the power back-off | the limits of the market are met, and the back-off is in the record |
| RF-17 | the coexistence of Wi-Fi, Bluetooth, 5G, UWB and GNSS at once | every chain inside its margin, and the cans hold the transmitters |
| RF-18 | the aperture tuner over 0.7 to 3.8 GHz, and the GNSS under a hand | the band covered at -3 dB, and the position inside 3 m in the open |
| RF-19 | the millimetre wave module, optional: the scan and the rate | the beam finds the dock, and 800 Mbit/s at 5 m |
| RF-20 | the field against the radio: a part seated on the band, and the pen dock | under 0.5 dB of loss, and no desense with the charge in |
