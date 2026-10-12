# BUDLUM LEAF · THE DIRECTIVE · PART 21 · THE STRETCH, THE ONE MILLIMETRE BAR AND THE PROJECTION

**Revision L.6.0 · 2026-10-12 · the standing of this part**. This part supersedes every earlier statement it names in Section 21.1. Tags follow Part 20: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]`, `[GENERAL]` and `[TREE]`.

**The orders that created this part, as Ayaz gave them on 2026-10-12**.

1. *"1 mm çubuk ve esneme olması şart."* The B bar is `1.00 mm`. The screen body stretches, and bending alone is not enough.
2. *"Yansıtmadan kastım, işlemin ağırlıkla validatörden gelmesi."* Projection means the Leaf shows what the network computes. It does not mean an optical projector.
3. *"Validatörler Budlum'u çalıştırdığı gibi bizim cihazımızı çalıştırıyor."* The validators run the Leaf as they run the chain. Distance must not be a problem. Section 21.5.
4. *"50 MP kamera olacak."* The camera stays `50 MP`, and it is the best camera the ring can hold. Section 21.3.5.
5. *"Esnemesi mümkün, polikarbonat cam yerine kullanılıyor."* The polycarbonate face stays, and the body stretches. Section 21.2.
6. *"Modelin kalınlığı 4 mm, çubuğun kendisi de 1 mm."* The module is `4.00 mm` thick. The bar itself is `1.00 mm`. Section 21.3.
7. *"Esner ama pil düşer diyorsun; yeni bir stil, biraz daha araştır."* The stretch must not cost the battery. Section 21.2.
8. *"Bunlar bir cüzdandır, en yakın validatöre bağlanır."* The Leaf is a wallet. It connects to the nearest validator. Section 21.5.4.

**The answers of Ayaz to the scan questions, 2026-10-12**.

| No. | The question | The answer | Where it lands |
|---|---|---|---|
| 1 | the `1 mm` bar | the module is `4.00 mm` thick and the bar is `1.00 mm` | Section 21.3 |
| 2 | the place of the B | the ring lies on the screen face, front or back | Section 21.3.1 |
| 3 | the energy at full stretch | more battery in the B module and in the dock | Sections 21.2.5 and 21.6 |
| 4 | wireless charging | Qi2.2 stays | Section 21.2.6 |
| 5 | USB-C | a separately sold port part | Section 21.3.4 |
| 6 | the camera | a small-pixel `50 MP` sensor, and the best possible camera | Section 21.3.5 |
| 7 | the B contents | rear display, speaker, microphones, flash, small battery and the `3.5 mm` jack all stay | Sections 21.3.6 and 21.6 |
| 8 | the session | no session cipher. The Leaf is a wallet and connects to the nearest validator | Section 21.5.4 |
| 9 | the dock validator | optional | Section 21.5.4 |
| 10 | outdoor latency | `30 ms` stays the target outdoors | Section 21.5.7 |
| 11 | the pixel density | `508 ppi` stays | Section 21.2.3 |
| 12 | the seams | a seam inside the screen is invisible, and the panels stay removable | Section 21.2.4 |
| 13 | the remote agent mode | removed, because it never worked and leaked a key | `tools/multi_agent_optimize.py` |
| 14 | `heypcb-post.txt` | rewritten to L.6.0 | `teslim/heypcb-post.txt` |

---

## 21.1 What this part supersedes

| The earlier statement | Where it was | The ruling of L.6.0 |
|---|---|---|
| the stem is `8.0 x 32.0 x 4.50 mm` | `HARDWARE/05`, `HARDWARE/13`, `HARDWARE/01` | the bar is `32.0 x 4.0 x 1.00 mm` on the top edge, in a `4.00 mm` module. Section 21.3 `[DECISION]` |
| the sole USB-C receptacle lives in the stem | `HARDWARE/05`, Part 0, Part 20 | USB-C leaves the B module. It is a separately sold port part. Section 21.3.4 |
| a `±90°` Grade-5 titanium micro-hinge joins stem and ring | `HARDWARE/13`, part 13 | no hinge. The `90°` bend is moulded into one part, as `NEREDE-NE-VAR.md` already said |
| the stem housing is titanium and the ring is 6061 aluminium | `HARDWARE/13`, parts 11, 14, 31 | glass-filled LCP. A metal case around an antenna defeats the antenna. Section 21.4.1 |
| the body bends at `R 25.5 mm` and does not stretch | `HARDWARE/12`, Part 18 | the body stretches `25 %` in every direction, and `41 %` at most. Section 21.2 `[DECISION]` |
| four large pouch cells hold `12.0 Wh` | `HARDWARE/15`, Part 4 | `128` hermetic micro cells, one per tile, hold `5.7` to `7.2 Wh`. Section 21.2.5 |
| the conductors are `AgNW/ITO` | `HARDWARE/02`, `HARDWARE/16` | ITO cracks near `1 %` strain. The conductors are AgNW, copper on the neutral plane and liquid metal |
| T-OLED pixels | Part 3 | micro-LED tiles at `508 ppi` on glass carriers. Section 21.2.3 |
| a `<15 µm` index-matched seam | Part 3, `HARDWARE/12` | a lattice-continuous seam: the pixel pitch stays `50.0 µm` across every cut. Section 21.2.4 |
| "Zero CPU and Zero RAM" | `HARDWARE/02`, `HARDWARE/19` | no general-purpose processor and no operating system. Fixed-function silicon and a frame store are allowed. Section 21.5.1 |
| the interaction budget is served by "a local scene renderer" | Part 10, `MASTER/14` | a fixed-function compositor inside `U1` serves it. Section 21.5.6 |
| one `U2` SiP holds Wi-Fi 7, UWB and `60 GHz` | `HARDWARE/13`, part 17 | no such single part exists. The radio set splits into `U2A` and `U2B`. Section 21.4.2 |
| 5G antennas exist and no modem exists | `HARDWARE/19`, A5 and A6 | a full 5G standalone modem `U5` joins the ring. Section 21.4.2 |
| a `50 MP`, `12.8 x 9.6 mm` sensor with a folded `13.8 mm` barrel lives in a `4.00 mm` ring | `HARDWARE/13`, parts 20 to 27 | a `50 MP` small-pixel sensor in a vertical `3.90 mm` column. Section 21.3.5 |
| a `0.45 Wh` bridge cell in `18.0 x 4.2 x 1.20 mm` | `HARDWARE/13`, part 29 | that is about `4 960 Wh/L` and impossible. The B cell is `0.14 Wh`. Section 21.2.5 |
| the module mass is `20.0 g` | `HARDWARE/05` | the old list summed to `22.00 g`. The L.6.0 list lives in `HARDWARE/13` |

**The rule of this part**. Where an older part and this part disagree, this part wins until the older part is rewritten. `[DECISION]`

---

## 21.2 The stretch

### 21.2.1 The new style: rotating squares

**The finding of the research of 2026-10-12**. The energy of a stretchable body does not depend on the stretch. It depends on how much of the relaxed area is cell. `[DECISION]`

The first L.6.0 body put cells on `5 mm` islands with `4 mm` serpentine lanes. Only `31 %` of the area held cells, so it reached `13.3 %` at `1.7 Wh`. That body is withdrawn.

**The rotating-square body**. The body is a tessellation of rigid square tiles. Each tile joins its neighbours only at its corners, through a hinge. Under a pull, neighbouring tiles turn in opposite directions, and the body grows in both directions at once. No tile and no cell strains. The tiles only turn. `[PUBLICATION]` Rotating-square displays were shown in 2024 in npj Flexible Electronics.

| The item | The value |
|---|---|
| the tile | `10.0 x 10.0 mm`, rigid |
| the tile count | `8 x 16 = 128`, so `32` per quadrant `Q1..Q4` |
| the stretch factor | `cos θ + sin θ`, in both directions |
| the default stretch | `θ = 17.5°`: `25.4 %` in every direction, `1.57` times the area |
| the maximum stretch | `θ = 45°`: `41.4 %` in every direction, `2.00` times the area |
| the body at maximum | `80 x 160 mm` grows to `113 x 226 mm` |
| the cell area at rest | about `83 %` of the face, against `31 %` for the withdrawn body |

**The behaviour**. The lattice grows equally in both directions, because it is auxetic. A pull along one axis also widens the other axis. The body has one degree of freedom, so `U1` reads the turn of every tile. Gate DSP-17.

### 21.2.2 The hinge and the seal

1. **The hinge stands on edge**. Neighbouring tiles counter-rotate, so a corner hinge turns through `2θ`. A flat ligament in the face would bend about its width and break near `15 %` strain.
2. **The ribbon**. Each hinge is a polyimide ribbon `12.5 µm` thick, `1.2` to `1.5 mm` tall and `0.8 mm` long. The tile corners are chamfered to give the free length.
3. **The strain**. The ribbon strain is `0.48 %` at `25 %` stretch and `1.23 %` at `41 %` stretch. Polyimide yields near `3 %`. `[HYPOTHESIS]` gate MEC-42.
4. **The conductors**. Copper of `2 µm` or less runs on the neutral plane of the ribbon in the `25 %` mode. Liquid-metal EGaIn channels carry the lines that serve the `41 %` mode.
5. **No slit filler**. A gap opens to `6.0 mm` at `17.5°`, so no elastomer can fill it. Each tile is sealed on its own: PC cap, pixel tile and welded cell can.
6. **The floating back skin**. A clear TPU or silicone skin, `50` to `100 µm`, is bonded to small pads at the tile centres. It sees only the global strain of `25` to `41 %`. It breaks at `300` to `900 %`. `[GENERAL]` Gate MEC-41.
7. **The polycarbonate face stays**. Every tile carries its own solid, hard-coated PC cap. A cap never strains, so its hard coat never cracks. `[DECISION]`

### 21.2.3 The `508 ppi` display

**The ruling**. The density stays `508 ppi`, a pitch of `50.0 µm`, in every state. `[DECISION]` The pixels live on rigid tiles, so the stretch never stretches the pixel pitch.

| The item | The value |
|---|---|
| the emitter | micro-LED, `5` to `8 µm` chips, or a blue micro-LED with quantum-dot colour conversion |
| the carrier | glass, `3.2 ppm/K`, with through-glass vias for the drive lines |
| the pixels per tile | `200 x 200` |
| the face at rest | `1 600 x 3 200` pixels, the frame size of Section 21.5.1 |
| the refresh | `240 Hz`, which micro-LED reaches easily `[GENERAL]` |
| the dead pixels | under `5` per device, by inspection and laser repair |

**The stretched view**. At `25 %` stretch the pixels cover `61 %` of the stretched face, and dark diamonds open between the tiles. Each tile keeps `508 ppi`. `U1` warps the image tile by tile, so a circle stays a circle. At `41 %` the pixels cover `47.5 %`. `[DECISION]`

**The honest distance**. The best shipping micro-LED face is about `326 ppi` (Garmin and AUO, 2025). `[PUBLICATION]` A `508 ppi` tile is `1.56` times that, so gap G-40 stays open until gate DSP-19 passes.

### 21.2.4 The invisible seam

**The order**. A seam inside the screen must not show, and the panels stay removable. `[DECISION]`

**The principle: a lattice-continuous seam**. The edge pixel sits `20 µm` from the cut. The cut is at most `10 µm`. So the pitch across the seam is `20 + 10 + 20 = 50.0 µm`, the same as everywhere else. The eye sees no seam, because the lattice has none. `[DECISION]`

| The rule | The value | The reason |
|---|---|---|
| the sub-pixel row | parallel to the cut | a triad across the cut leaves only `5 µm` of edge margin |
| the edge margin | `16 µm` from the chip to the cut | above the `5` to `10 µm` chipping of an ultrafast-laser cut |
| the cut face | black-coated | no grazing light scatters from it |
| the PC cap kerf | `10 µm` at `+50 °C`, `37 µm` at `-10 °C` | a `10 mm` cap grows `27 µm` over `40 K` |
| why the cap kerf hides | over `92 %` of a micro-LED face is black | a dark line under `50 µm` between continuous pixel columns is not seen |
| the glass carrier | `1.3 µm` of growth over `40 K` | the lattice stays continuous over temperature |
| the stack | glass, pixel layer and glass, or a floating carrier on slip OCA | an asymmetric PC on glass bond curls about `1.8 mm` over `40 mm` |

**The removable quadrants**. Each quadrant `Q1..Q4` lifts out and seats again in under `3 s`.

1. **The locator**. A kinematic seat of silicon-nitride balls in tungsten-carbide vees, held by N52H magnets. It repeats to under `1 µm`. `[GENERAL]`
2. **No overconstraint**. The `24` dovetails and the edge lip become non-locating, so they do not fight the seat.
3. **The hinges at the quadrant line**. They are split couplers that close on the seat. Gate MEC-40.
4. **The closed loop**. A capacitive strip and a thermistor sit on each seam face. `U1` shifts the image in `3.125 µm` steps, a sixteenth of a pixel.
5. **The calibration**. Each tile stores its edge luminance and colour. `U1` recalibrates within the `3 ms` dead-pad window after a swap.

### 21.2.5 The energy, with no loss to the stretch

| The store | The volume | The energy | The tag |
|---|---|---|---|
| the body at `600 Wh/L` | `12 800 mm² x 0.83 x 0.90 mm = 9.56 cm³` | `5.7 Wh` | `[HYPOTHESIS]` |
| the body at `750 Wh/L`, silicon anode | the same | `7.2 Wh` | `[HYPOTHESIS]` |
| the B module cell | `20.0 x 8.0 x 1.50 mm` at `600 Wh/L` | `0.14 Wh` | `[HYPOTHESIS]` |
| the dock pack | in the dock body | `20 Wh` | `[HYPOTHESIS]` |

**The result**. The body keeps the full `5.7 Wh` of the unstretched body and stretches `25 %`. With a silicon-anode cell it holds `7.2 Wh`. Against the withdrawn body, that is `1.9` times the stretch and `3.4` to `4.2` times the energy. `[DECISION]` gate ENR-22.

**The run time**. A video session draws about `2` to `3 W`. The body and the B cell run it for about `1.9` to `3.7 h`. The dock pack refills the Leaf about three times away from a wall. `[HYPOTHESIS]`

**The cells**. Each tile holds one hermetic micro cell, `9.25 x 9.25 x 0.90 mm`, in a laser-welded `30 µm` steel or titanium can. Each cell has its own fuse and balance channel. A `4 x 32` multiplexer in the B ring watches them. Gate ENR-23.

**The silicon anode**. A shipping silicon-anode phone cell measures about `935 Wh/L`. `[PUBLICATION]` Enovix AI-1. A `0.90 mm` micro can loses `15` to `25 %` to its walls, so `750 Wh/L` is the target. If the cells reach only `600 Wh/L`, the body still holds `5.7 Wh`.

**The old energy claims**. The L.5.0 cell of `3.0 Wh` was about `1 060 Wh/L`. The L.5.0 bridge cell was about `4 960 Wh/L`. Both are withdrawn, because no cell reaches them.

### 21.2.6 Qi2.2 on a stretching body

**The ruling**. Qi2.2 stays, at the `25 W` magnetic power profile. `[DECISION]`

1. **The coil**. Four sector coils, one per quadrant, are wired in series around the `+` crossing. They act as one round receiver coil of about `Ø44` to `46 mm`.
2. **The seam links**. Only two series links cross each quadrant seam, through gold leaves in the seat.
3. **The conductor**. Two layers of plated copper, `50` to `75 µm`, on polyimide. Each turn splits into `3` or `4` strands, so it crosses a hinge on the neutral plane.
4. **The layer**. Coil and shield take `0.20 mm` of the `0.24 mm` margin in the tile stack. No cell volume is taken.
5. **The magnets**. `16` small N52 magnets sit in the chamfered tile corners on the alignment circle.
6. **The charge state**. Charging runs at rest, when every hinge reads `θ = 0`. A pull during charging pauses the coil.
7. **The heat**. `25 W` into `5.7 Wh` is about `4.4 C`. A cooled pad and the `36.2 °C` skin limit set the sustained rate. `[HYPOTHESIS]` gate ENR-24.

**The honest distance**. The best published stretchable receiver carries about `3.8 W` (npj Flexible Electronics, 2024). `[PUBLICATION]` This design keeps the coil on rigid tiles, so it is a phone coil cut into sectors. Certification is gate ENR-24.

### 21.2.7 The tile stack, `2.00 mm`

| The layer | The thickness |
|---|---|
| hard-coated PC cap with the AgNW touch grid | `0.25 mm` |
| optical adhesive | `0.05 mm` |
| glass, micro-LED layer and glass | `0.25 mm` |
| slip OCA | `0.03 mm` |
| Qi coil and shield, or a graphite spreader outside the coil | `0.20 mm` |
| hermetic micro cell in its can | `0.90 mm` |
| floating back skin | `0.08 mm` |
| the hinge routing and the tolerance | `0.24 mm` |
| **total** | **`2.00 mm`** |

---

## 21.3 The B module: a `4.00 mm` module with a `1.00 mm` bar

### 21.3.1 The geometry, read from the CAD

The figures come from `uploads/b.png`, `cad/monogram_letter.py` and `cad/models/monogram-module.stl`. `[DECISION]`

| The item | The value | The source |
|---|---|---|
| the unfolded `b` | `40.0 x 32.0 mm` | `b.png` |
| the bar width in the drawing | `4.0 mm` | `STEM_W = 4.0` |
| the bar | `32.0` along the edge `x 4.0` across the edge `x 1.00 mm` high | `STEM_THICK = 1.00` |
| the bar stance | horizontal, seated on the top edge of the `2.00 mm` body | `monogram_letter.py` |
| the module thickness | `4.00 mm` | `monogram-module.stl`, `Z = -2.00..+2.02` |
| the ring | `Ø32.0` outside, `Ø24.0` inside, lying on the screen face | `RING_RO`, `RING_RI` |
| the bend | one moulded `90°` corner at the natural gap of `4.0 mm`, no hinge | `b.png` |
| the seats | any of the four edges, on the front or the back face | Part 5 |

**What changed from the first L.6.0 text**. The first text read the bar as a `1.00 mm` wall standing `8 mm` off the face. Ayaz corrected it: the bar is `1.00 mm` and lies on the edge. The cantilever table is withdrawn, because the edge backs the whole bar.

**A note on the CAD**. `cad/leaf_v2.py` still sets `MOD_T = 2.00`. The module STL is `4.00 mm`. The sheets and renders are redrawn to `4.00 mm` with the next sheet set.

### 21.3.2 The `1.00 mm` bar stack

| The layer | The thickness | The material | The duty |
|---|---|---|---|
| top skin | `0.20 mm` | LCP, 40 % glass fibre | the hard face, RF transparent |
| antenna layer | `0.05 mm` | laser direct structured copper | A1 and A2 radiators |
| core | `0.40 mm` | LCP, 40 % glass fibre | the stiffness |
| mmWave layer | `0.10 mm` | two-layer LCP flex | the `60 GHz` array, looking up and out |
| contact layer | `0.25 mm` | LCP with `12` gold spring leaves | the body link, on the seat tile |
| **total** | **`1.00 mm`** | | |

**The body link**. The `12` leaves sit in a `9.6 mm` field over one edge tile, the seat tile. The other edge tiles turn under the bar without moving the contacts. `[DECISION]` gate MON-23.

### 21.3.3 The ring on a stretching face

1. The ring covers about three tiles. Its underside is a low-friction pad with magnets.
2. The bar holds the module on the seat tile. The ring slides on the face as the tiles turn.
3. The pad carries no contacts, so a turning tile breaks no link. Gate MON-21.

### 21.3.4 USB-C is a separate part

1. **The ruling**. USB-C leaves the B module. It is a separately sold port part, as Ayaz ordered before L.5.0. `[DECISION]`
2. **The fit**. The port part clips on any free body edge and uses the same `12` contact pads as the bar.
3. **The EU rule**. Directive (EU) 2022/2380 covers a product that charges by wire. The port part carries the USB-C receptacle for that duty. `[PUBLICATION]`
4. **What it frees**. The ring rim loses a `8.9 x 7.3 x 3.10 mm` receptacle and its controller. The `3.5 mm` jack takes the rim.

### 21.3.5 The best `50 MP` camera in a `4.00 mm` ring

**Why the fold is withdrawn**. A last `45°` fold over a flat `1/1.56"` sensor needs at least the sensor's short side, `6.14 mm`, in height. The ring has `4.00 mm`. So the first L.6.0 camera cannot be built. `[DECISION]`

**The camera of L.6.0**. A vertical column through the ring, with the first lens element as the front window.

| The item | The value |
|---|---|
| the sensor | `50 MP`, `0.61` to `0.64 µm` pixels, `5.2 x 3.9 mm` class, chip-on-board |
| the lens | five elements, `f = 3.3 mm`, `f/2.0`, the first element is the sapphire window |
| the view | about `88°`, a `22 mm` equivalent wide main camera |
| the focus | `0.12 mm` of stroke, sharp from `10 cm` to infinity |
| the stabiliser | in-plane, with `0.08 mm` of clearance |
| the height | `3.30` optics, `0.12` focus, `0.08` clearance, `0.35` sensor, `0.05` cover: `3.90 mm` |
| the rear display hole | `6.5 x 5.3 mm`, about `12 %` of the rear panel |
| the processing | `12.5 MP` binned stream at video rate. The validators run multi-frame fusion |

**The upgrade path**. A `0.56 µm` `50 MP` sensor is `4.59 x 3.44 mm`. Its lens is about `3.0 mm` long. The saved height buys `f/1.8`. `[PUBLICATION]` Samsung shipped `0.56 µm` pixels in 2022.

**The option of three columns**. Three `50 MP` columns at `f/2.0` gather about the light of one `1/1.56"` sensor. They cost `36 %` of the rear panel. The single column is the default. `[DECISION]` gate CAM-21.

### 21.3.6 The `3.5 mm` jack in the ring

1. **The bore**. `Ø3.6 mm` with `0.20 mm` walls, so `4.0 mm` across. It runs along a chord of the ring at `13.8 mm` from the centre.
2. **The fit**. The bore spans `r = 12.0` to `15.6 mm`. It clears the windows at `r = 12.0 mm` and the outer wall at `r = 16.0 mm`.
3. **The form**. A `5 mm` closed blind end and a `9 mm` open trough in the rim. A rim boss of `0.5` to `1.0 mm` seats the plug collar.
4. **The contacts**. Tip, ring and detect sit in the closed end. The sleeve contact grips in the trough.
5. **The seal**. A gasketed contact pocket keeps the module sealed.
6. **The antenna**. The A3 loop routes around the groove. Gate MON-22 and RF-22.

**A precedent**. The vivo X5 Max of 2014 carried a `3.5 mm` jack in a `4.75 mm` body. `[PUBLICATION]`

---

## 21.4 The strongest Wi-Fi with no local processor

### 21.4.1 The antennas

1. **A1, the bar inverted-F**. The `2.4 GHz` quarter wave is about `31 mm`, and the bar is `32 mm`. The bar lies on the body edge, so it radiates from the end of the ground plane. That is the classic top-edge place of a phone antenna. `[GENERAL]`
2. **The height**. The radiator stands `1.00 mm` over the edge ground. A low height narrows the bandwidth, so the aperture tuner re-centres the band. Target efficiency `-2.5 dB`. `[HYPOTHESIS]` gate RF-22.
3. **A2, the bar coupled arm**. A `12 mm` arm on the same layer covers `5.15` to `7.125 GHz`.
4. **A3, the ring loop**. A loop on the ring rim is the second Wi-Fi antenna. The bar lies on the edge and the ring lies on the face, so the two polarisations differ. This gives true `2 x 2` MIMO. Target `-3 dB`. `[HYPOTHESIS]` gate RF-22.
5. **A4, the `1 x 4` `60 GHz` array**. It sits on the mmWave layer of the bar and looks up and out.
6. **No metal in the module shell**. The ring and bar shells are LCP-GF40. The camera, the jack contacts and the shields are the only metal, and they sit away from the bar.
7. **The magnets stay in the ring**. A magnet near A1 costs gain. The 1.5 dB rule of Part 5, Section 5.3.1 holds.
8. **A tuner per antenna**. The IMU reports the edge and the face. `U2A` loads a matching state for each of the eight seats. Gate RF-23.
9. **The body under stretch**. The edge ground turns with the tiles. The tuner reads the hinge angles and re-matches. Gate RF-21.

### 21.4.2 The radios

| The part | The duty | Why it is separate |
|---|---|---|
| `U2A` Wi-Fi 7 and BT 6.0 combo | `2 x 2`, `320 MHz`, multi-link on `5 GHz` and `6 GHz`, BT channel sounding | a shipping class of part `[GENERAL]` |
| `U2B` `60 GHz` and UWB | the dock link and secure ranging with the scrambled timestamp sequence | a separate class of part |
| `U5` 5G standalone modem | configured grant, dual active protocol stack handover, low-latency mobility | the outdoor `30 ms` path needs a full modem, not RedCap |

Each of these carries firmware on its own small core. That is allowed: Section 21.5.1. The modem and its front end inside the `4.00 mm` ring are gate RF-17.

### 21.4.3 The settings that lower the latency

| The setting | The effect |
|---|---|
| multi-link with simultaneous transmit and receive on `5` and `6 GHz` | a packet takes the clean link, so a spike on one link does not stall the frame |
| `6 GHz` first | a cleaner band with wide channels |
| restricted target wake time for the stream | the stream gets reserved air time |
| power save off during a session | no wake-up delay on each frame |
| the low-latency queue and L4S marking end to end | the queue does not grow under load `[GENERAL]` |
| 5G configured grant and a low-latency QoS flow | the uplink does not wait for a scheduling request |
| 802.11bn (Wi-Fi 8) in the roadmap | its main goal is reliability and latency `[PUBLICATION]` |

### 21.4.4 The strongest signal is the shortest path

**The antenna gains a few dB. The distance to the serving validator decides the latency.** The best path for Leaf is a validator near the radio. `[DECISION]`

**The Leaf Dock**. One box holds a Wi-Fi 7 access point, a `60 GHz` radio, a UWB anchor and a `20 Wh` pack. A full Budlum validator inside it is an option, as Q32 said. Gate SW-20.

---

## 21.5 The projection: the validators run the Leaf

### 21.5.1 What "Zero CPU" means from now on

**The definition**. Leaf has no general-purpose application processor and no operating system. It runs no third-party code. `[DECISION]`

**What is allowed**. Fixed-function silicon with signed firmware: the radios, the modem, the video decoder, the TCON, the ISP, the power chip and the secure element. Also a frame store, because a decoder needs one.

**Why the frame store is needed**. A Leaf 160 face is `1 600 x 3 200` pixels, near `15 MB` per frame. A slice decoder with a compressed frame store holds it in about `16 MB`. `[HYPOTHESIS]`

### 21.5.2 The principle: the Leaf is a part of the chain

**The validators run the Leaf as they run Budlum**. The state of every Leaf session is chain state. The applications are on-chain programs. The validators execute them in the same way that they execute blocks. The Leaf holds no state that the network cannot rebuild. `[DECISION]`

| The reading of the Budlum tree | The fact `[TREE]` | The consequence |
|---|---|---|
| `src/registry/role.rs` | `VALIDATOR` is `RoleId(1)`, the role that produces blocks and finality | the same validators run the Leaf. No new role is needed |
| `src/consensus/pos.rs` | the slot is `6` seconds | the frame path does not wait for a block |
| `src/ai/types.rs` | bonded results, with deadlines counted in blocks | a signed, bonded result is already a pattern in the tree |
| `budzero/` | an in-tree zkVM with STARK proofs | a frame result can carry a proof later |

### 21.5.3 Two speeds inside one validator

1. **The state speed**. A user action becomes a transaction. Consensus orders it and finalises it in the slot of `6` s.
2. **The frame speed**. The serving validator applies the same action to its copy of the state at once. It renders and streams the frame at once. It does not wait for the slot.
3. **The rule that joins them**. The frame is optimistic. If finality orders the actions differently, the next frame shows the final state. This is rare, because one user's session has one writer. `[DECISION]`
4. **The honesty of the frame**. Rendering is deterministic, in fixed point. Another validator re-executes a sample of the frames and compares the hash chain. A mismatch is slashed like a double sign. `[DECISION]` research order RG-18.

### 21.5.4 The wallet and the nearest validator

**The Leaf is a wallet**. `U7` holds the keys. The Leaf connects to the nearest validator, as a wallet connects to a node. It runs no session cipher of its own. `[DECISION]`

**Finding the nearest validator, in three layers**. A layer runs only when the layer above finds nothing.

| Layer | The reach | The method |
|---|---|---|
| L0, the room | `0` to `10 m` | BLE or Wi-Fi Aware finds a validator. UWB secure ranging proves the distance to about `±10 cm`, so a relay cannot fake it |
| L1, the metro | under `100 km`, ideally under `20 km` | an anycast bootstrap returns `3` to `5` validators from the on-chain registry. The Leaf probes each once per second and takes the lowest round trip |
| L1, the cell | a few km from the 5G cell | validators at operator edge sites, found by 3GPP edge discovery `[PUBLICATION]` TS 23.558 |
| L2, far | anything beyond | the `far` class, carried by speculative frames and the `U1` compositor |

**A handover costs zero frames**. The sampling re-executor of RG-18 doubles as a hot shadow. It holds the same session state and streams the frame hash chain. When the primary's round trip or loss crosses a limit, `U6` switches at the next slice. Rendering is deterministic, so the decoder needs no new key frame. Multipath QUIC carries both paths. Gate DST-12.

**The proof that a frame is real, with no CPU**.

1. Once per session and on handover, `U7` checks that the validator key is in the active set. It keeps the set current from finality proofs.
2. On every slice, an inline authentication engine in `U6` checks the tag at line rate.
3. Once per second, the validator signs a Merkle root of the frame hashes. `U7` countersigns a receipt with the measured round trip.

**The density, by the protocol**. The dock validator is optional, so density cannot rest on homes alone. `[DECISION]`

1. The receipts carry signed round trips, so the chain holds a live latency map.
2. Emission pays per served session minute, only in areas where the 99th percentile is under `30 ms`.
3. Location is checked by latency from many challengers, not trusted.
4. A validator that forges a frame or lies about latency is slashed.

**The targets**. A validator within `20 km` in a city, about `0.2 ms` of fibre each way. Within `100 km` everywhere covered. The `far` class elsewhere. Gate SW-24.

### 21.5.5 The projection path, part by part

1. The touch grid scans at `480 Hz`. `U7` signs the input batch.
2. `U2A` or `U5` sends the input to the nearest validator, as a transaction and as a frame request.
3. The validator applies the input to the session state and renders the frame, plus the speculative frames.
4. It encodes in low-latency slices and signs a hash chain of the frames.
5. `U6` checks and decodes each slice as it arrives. `U1` composes it into the frame store and scans it out at `240 Hz`.
6. `U7` signs a receipt over the frame hashes it showed. The receipts settle the session in the slot window.

### 21.5.6 The local compositor

The interaction budget of Part 10 is under `10 ms`. `U1` holds a fixed-function compositor for four jobs only: the cursor, the scroll offset, the typed glyph echo and the stretch warp. The validator sends the layers, the glyph atlas and the speculative frames. `U1` only moves, picks and composes them. It runs no program. `[DECISION]` gate SW-21.

### 21.5.7 The latency budget, input to photon

**The order**. `30 ms` holds outdoors too. `[DECISION]`

| The step | Wi-Fi, room validator | Wi-Fi, city validator | 5G, cell-site validator | Far validator |
|---|---|---|---|---|
| the touch scan at `480 Hz` and the controller | `1.8 ms` | `1.8 ms` | `1.8 ms` | `1.8 ms` |
| the air uplink | `1.0 ms` | `1.0 ms` | `2.3 ms` | `1.0 ms` |
| the network, both ways | `0.1 ms` | `1.2 ms` | `0.3 ms` | `80.0 ms` |
| the execute and render | `4.3 ms` | `4.3 ms` | `4.3 ms` | `4.3 ms` |
| the first-slice encode | `1.5 ms` | `1.5 ms` | `1.5 ms` | `1.5 ms` |
| the air downlink | `1.0 ms` | `1.0 ms` | `1.3 ms` | `1.0 ms` |
| the first-slice decode | `1.5 ms` | `1.5 ms` | `1.5 ms` | `1.5 ms` |
| the scan-out at `240 Hz` and the pixel response | `2.4 ms` | `2.4 ms` | `2.4 ms` | `2.4 ms` |
| **mean, a new action** | **`13.6 ms`** | **`14.7 ms`** | **`15.4 ms`** | **`93.5 ms`** |
| **99th percentile, a new action** | **under `20 ms`** | **under `21 ms`** | **about `21 ms`** | **over `100 ms`** |
| **a predicted action** | **about `5 ms`** | **about `5 ms`** | **about `5 ms`** | **about `5 ms`** |

**How the 5G column holds**. The uplink waits for a slot of the `2.5 ms` operator pattern, and one retransmission adds about `3 ms`. A simulation of the stages as independent delays gives a 99th percentile of about `21 ms`. A sum of the stage percentiles is not the percentile of the sum. `[HYPOTHESIS]`

**What the 5G column needs**. A validator at the cell site or the operator edge, with local breakout. A low-latency QoS flow with configured grant and L4S. A block error target of `10 %` or less. Without them, a loaded public cell gives about `35` to `60 ms`. Gate DST-11.

**The predicted action**. It skips the network: the touch scan, the pick in `U1` and the scan-out. All rows are `[HYPOTHESIS]` until gate DST-11 measures them.

### 21.5.8 Only decentralised applications

1. `U7` accepts a frame stream only from a key that is an active Budlum validator.
2. The session names the application by its on-chain program entry.
3. A stream that fails either check shows nothing but the local safe screen. Gate SW-22.

---

## 21.6 The B module of L.6.0, block by block

| Block | Location | L.6.0 content |
|---|---|---|
| radiators | bar | A1 inverted-F, A2 coupled arm, A4 `60 GHz` array |
| body link | bar contact layer | `12` gold spring leaves over the seat tile |
| radiator | ring rim | A3 loop, routed around the jack groove |
| `U1` | ring PCBA | quad-tile TCON, local compositor, per-tile warp, seam shift |
| `U2A`, `U2B` | ring PCBA | Wi-Fi 7 and BT 6.0, `60 GHz` and UWB |
| `U5` | ring PCBA | 5G standalone modem with eSIM |
| `U6` | ring PCBA | AV1 and HEVC slice decoder, inline slice check, `16 MB` frame store |
| `U7` | ring PCBA | secure element: the wallet keys, the validator set, the receipts |
| `U8` | ring PCBA | IMU for the seat, the face and the tuner |
| `U3`, `U4` | ring PCBA | audio codec, power and dead-pad chip, cell multiplexer |
| camera | ring centre | `50 MP` small-pixel sensor in a `3.90 mm` vertical column, `f/2.0`, focus and stabiliser |
| rear display | ring back | round panel with a `6.5 x 5.3 mm` camera hole |
| audio | ring | speaker, two microphones, `3.5 mm` jack in the rim |
| flash | ring | two-tone LED |
| cell | ring | `0.14 Wh` |
| magnets | ring underside | `8` N52H in a sliding pad, away from A1 |

The part list with masses lives in `HARDWARE/13-B-MODULE-PART-BY-PART.md`.

---

## 21.7 The research order for the Budlum tree

| Order | The work | The acceptance test |
|---|---|---|
| **RG-18** | the validator Leaf duty: session state as chain state, fixed-point render, frame hash chain, sampled re-execution, hot shadow, receipts, coverage rewards and slashing | `10 000` frames stream from one validator, a second validator matches a sample bit for bit, and a forged frame is slashed |

---

## 21.8 The new gates

| Gate | The test | The pass condition |
|---|---|---|
| **MEC-39** | the rotating-square body, biaxial | `10 000` cycles at `25 %` and `1 000` at `41 %`, no open trace, no tile crack |
| **MEC-40** | the quadrant swap and the seam | swap in under `3 s`, repeat under `1 µm` over `10 000` swaps, step under `1 µm` from `-10` to `+50 °C` |
| **MEC-41** | the PC caps and the floating back skin | no cap crack, hard coat intact, no skin delamination after `10 000` cycles at `41 %` |
| **MEC-42** | the edge-on polyimide hinge | `10 000` cycles at `2θ = 35°` and `1 000` at `90°`, no crack |
| **ENR-22** | the micro-cell energy | at least `1.42 Wh` per quadrant at `600 Wh/L`, and `1.80 Wh` at `750 Wh/L` |
| **ENR-23** | the cell fuse: a short in one cell | the fuse opens, and the other cells stay in service |
| **ENR-24** | Qi2.2 on the tile body | it passes Qi2.2 `25 W` certification, and the coil resistance moves under `5 %` after `10 000` stretch cycles |
| **DSP-17** | the per-tile warp: a circle and a grid at `25 %` and `41 %` | the shape error under `1 %` |
| **DSP-18** | the touch under stretch | no false touch at full stretch, position error under `1 mm` |
| **DSP-19** | the `508 ppi` micro-LED tile and the seam | the largest pixel gap at a seam is `50.0 µm` or less, and under `5` dead pixels per device |
| **RF-21** | the antennas under stretch | the return loss inside the limit, at rest and at `41 %` |
| **RF-22** | the bar and ring pair as `2 x 2` MIMO, with the jack groove | the envelope correlation under `0.3`, A1 at `-2.5 dB` or better |
| **RF-23** | the eight seats, front and back on four edges | each seat inside `1.5 dB` of the best seat |
| **MON-21** | the module drop, `1.5 m`, six faces, and the ring slide on a stretching face | the bar intact, the seat holds, the body link stays closed |
| **MON-22** | the `3.5 mm` jack | `5 000` plug cycles, a side load, and the seal passes |
| **MON-23** | the bar and the module | bar `1.00 ± 0.05 mm`, module `4.00 ± 0.05 mm` on every unit |
| **CAM-21** | the `50 MP` vertical column in the `4.00 mm` ring | it fits at `f/2.0` or faster, focuses from `10 cm`, and meets CAM-9 after validator fusion |
| **SW-20** | the Leaf Dock with its pack, and with the optional validator | it charges the Leaf away from a wall, and the validator option serves a room session |
| **SW-21** | the local compositor: cursor, scroll, glyph echo, warp | each job under `10 ms`, with no program run on the device |
| **SW-22** | the stream check: a key that is not an active validator | the stream is refused and the safe screen shows |
| **SW-23** | the speculative frames: scroll, button and menu | a predicted action shows in under `10 ms` with the network cut |
| **SW-24** | the nearest validator: UWB distance proof, probes and the coverage map | the Leaf serves from the lowest round trip, and a relayed validator fails the distance proof |
| **DST-11** | input to photon, four paths including 5G outdoors | Wi-Fi and 5G cell-site paths under `30 ms` at the 99th percentile |
| **DST-12** | the validator handover while the user moves | the switch loses no frame and causes no reload |
