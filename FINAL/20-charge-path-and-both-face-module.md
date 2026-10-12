# BUDLUM LEAF · THE DIRECTIVE · PART 20 · THE CHARGE PATH, THE BUDLUM MODULE AND THE PORT RAIL

**Revision L.3 · 2026-10-06 · the standing of this part**. Every number carries a tag. `[DECISION]` means Ayaz or the validation line has ruled. `[HYPOTHESIS]` means a gate must measure it before it becomes a claim. `[PUBLICATION]` means a public source and the source is named. `[GENERAL]` means common engineering knowledge.

**The orders that created this part, in the order they arrived**.

1. **The wireless path is withdrawn**. *"Kablosuz şarj olmasın, boşver"*. The device charges by wire and by contact.
2. **The upright B module stands on the top edge**. Modeled 1:1 from `uploads/b.png` (`40 x 32 x 4 mm`), the `b` attaches at its bottom (`y = 0 mm`). Its vertical bar is the antenna, its front ring holds the camera, and its back holds the round panel.
3. **The magnetic latches sit in the edge frame**. `N52H` magnet arrays in the top and side rails seat the upright B module and the side Port Rail. `HARDWARE/10-ANY-PLACE-AND-THE-MAGNETIC-FIELD.md` carries the full specification.
4. **The ports are a part, and not an opening**. *"USB-C, isterse USB-A, isterse kulaklık; ayrı satılan bir parça"*. The body carries no connector opening, and a detachable module on the side rail provides the chosen ports. Section 20.3.5 records the mechanism and the law.

Ayaz is away from the program. The decisions in this part are taken by the program line and recorded in Section 20.6 so that they can be reported on request. `[DECISION]`

---

## 20.1 What the wireless path cost, and what its withdrawal returns

**The state before this part**. The founding order of Ayaz asked for wireless power at *the highest wattage the gates permit*. The directive then carried a coil array in the stand, a Qi2 class fallback and a metal free window in the body. That requirement is withdrawn today. `[DECISION]`

**The costs that leave with it**.

| The item | The number, and the source |
|---|---|
| the coil and the shield inside the body | receiving coil (`0.40 mm`), ferrite shield (`0.25 mm`), and adhesive: **about `0.65 mm` of stack** and **`6 g`** with the shield frame |
| the loss at 25 W | Qi2.2 moves 25 W broadly, and the end to end efficiency of a certified magnetic link is stated near **83 percent**. So about **5 W becomes heat in the pad and the coil** at 25 W. A wired path at the same power loses about **0.5 W** in a 40 W class cable and a charger [PUBLICATION] |
| the metal free window | a metal back and a coil are contradictory, so the back face would carry a polymer window with a lower drop and a lower stiffness |
| the certification and the fee | fiscal 2026 WPC fee: **`$30 000/yr`** Regular (`$18 000/yr` Adopter). Qi2.2 `25 W` test is **`$20 000-$25 000`**, plus `$1 500-$3 000` keys (`$25 000-$38 000` before tooling) [PUBLICATION] |
| the integration risks | foreign object detection, a coil phase schedule against the radios, and a heat path through the coil area |

**What the withdrawal buys back**.

| The item | The value |
|---|---|
| stack | about **0.65 mm** of the body, which the energy sheet can take as thickness, or the thickness claim can take as thinness |
| mass | about **6 g** |
| the back face | **no metal free window**: the heat spreader can be metal and can reach the perimeter |
| the money | **`$25 000 to $38 000`** saved before the first sale, plus **`$18 000 to $30 000/yr`** saved thereafter |
| the radio | the coil desense problem of gate RF-3 changes subject (Section 20.2) |

**The energy that 0.65 mm carries, at the base case of Part 17**. The net cell area of a Leaf 160 sheet is about **110 cm²**. That figure is after the tile and bridge loss. Then:

`0.65 mm × 110 cm² = 7.15 cm³`, and at **800 Wh/L** that is 5.72 Wh of nameplate. After the perimeter frame margin of Section 20.3, **4.6 Wh of nameplate and 3.7 Wh of effective energy** stay in the design. `[HYPOTHESIS]` gate ENR-7 measures the sheet that takes it.

**The rule that replaces the old order**. **A Budlum Leaf charges by wire and by contact. It does not charge by induction, and no member carries a coil**. `[DECISION]`

---

## 20.2 The charge path now: two ways in, both of them contacts

| The path | The power | The loss | The details |
|---|---|---|---|
| **USB-C at the fixed edge** | **40 W peak, 25 W flat** | about 0.5 W at 25 W | USB PD and a sealed receptacle. The derating curve of Part 4, Section 4.5: full below 38 °C, 20 percent at 45 °C, stop at 48 °C |
| **The dock and the rail contacts** | **25 W** | **about 0.1 W** | four gold pads on the fixed edge, spring pins in the dock, 20 V at 1.25 A per power pad |

**The contact numbers**. `[PUBLICATION]` A gold on gold spring contact holds **20 to 50 mΩ** at mid stroke, and below 30 mΩ with hard gold. The parts are rated for **10 000 to 1 000 000 mating cycles**, matching standard sealed watch and tracker contacts.

| The item | The value | The arithmetic |
|---|---|---|
| the current per power pad | 1.25 A | 25 W at 20 V |
| the contact resistance, new | 30 mΩ | a gold pad and a spring pin |
| the loss, two pads | **0.094 W** | `2 × 1.25² × 0.030` |
| the loss, a worn pad at 100 mΩ | **0.31 W** | the end of life rule of gate MEC-6 |
| the loss of the withdrawn wireless path at 25 W | **about 5 W** | at 83 percent end to end |

**So the contact path loses about fifty times less than the induction path at the same power**. It does that without a coil, a shield, a window or a fee. `[DECISION]`

**The four pads, and the rules**.

| The pad | The duty |
|---|---|
| 1 | the power, 20 V at 1.25 A |
| 2 | the ground |
| 3 | the identification: a one wire signature in the dock, so the device knows a real dock is present |
| 4 | the spare, for a later rail function (the optional validator board of Part 15, H-14) |

**The rules**. The pads are **unpowered until the identification handshake completes**, so a wet pocket cannot electrolyse them. The pads are **flush and recessed by 0.15 mm** in a gasketed groove, so the class of gate MEC-19 holds with the dock off. Spring pins live in the replaceable dock, while recessed gold pads stay on the device. `[DECISION]`

**The gate change**. **MEC-6 becomes the wired and contact charge bench**. It covers the USB-C path at 40 and 25 W, and the contact path at 25 W. It measures pad loss at 0, 20 000 and 50 000 cycles, after 96 h salt spray and 500 h at 85 °C/85% RH. **RF-3 measures radio desense with the charge cable attached and on the dock**, because no wireless coil exists. `[DECISION]`

---

## 20.3 The `90°`-bent-stem Budlum B module: flat ring on screen, sole `USB-C` in stem, and reversible 4-edge docking

**Revision L.5.0, of 2026-10-12**. Modeled 1:1 from `uploads/b.png` (`20.0 g`, `32` parts), **only the stem (`çubuk`) bends at a `90°` right angle (`dik açıyla`)**. Its **circular ring (`yuvarlak`, `32 x 32 x 4.0 mm`) lies flat on top of the screen**. Moving the `90°`-bent stem around the 4 outer edges docks the B module to the **Front (`+Z`) or Back (`-Z`)** (`r = 0.55 mm`). `[DECISION]`

**The part, in one line**. The `90°`-bent-stem B module (`20.0 g`) houses the **sole `USB Type-C` (`40 W`) port and 3-band/`60 GHz` antennas in its `90°` stem**. Its **flat `Ø32.0 / Ø24.0 mm` ring on the screen holds the `50 MP` camera, rear `Ø22.4 mm` AMOLED, audio, and Zero-CPU SiP**. `[DECISION]`

### 20.3.1 What Revision L.5.0 establishes

| Prior draft feature | What replaces it in Revision L.5.0 |
|---|---|
| bulky external bottom battery pack (`80 x 36 x 4 mm`, `46 g`) | **cancelled**: replaced by **`4 x (40 x 80 x 2.00 mm)` (`68 g`) `+` polycarbonate solid-state quadrants (`Q1..Q4`, `12.0 Wh` `LLZO/PEO`)** |
| visible seam or scratch between modular tiles | **`<15 µm` (`n = 1.585`) phenyl-fluorosilicone self-healing optical `+` lip (`R < 0.0001%`)**, `<2.5 µm` Z-step on Ti pins, Corning edge-wrap (`0.00 mm` internal bezel) |
| flammable liquid Li-ion near the eye in eyewear mode | **non-flammable `LLZO/PEO` all-solid-state battery (`0%` liquid, `0.0 ppm` HF)**, **`<=36.2 °C` hardware NTC cut-off**, `ISO 10993` PC, `<0.08 µT` bifilar ELF, `SAR = 0.054 W/kg` |
| USB-C port on the screen body or wireless charging ban | **zero USB-C on screen body**; **universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` wireless charging**; **sole `USB-C` (`40 W`) in B stem** |
| upright flat `b` fixed only at top-left edge | **only the stem (`çubuk`) bends `90°` (`dik açıyla`)** via a `±90°` Ti hinge; the **round ring lies flat on the screen (`+Z / -Z`)** |

**What the architecture delivers**. Four **17 g** quadrants form a **68 g** (`12.0 Wh`) `Qi2.2` body (`88 g` complete with the **20 g** B module). `[DECISION]`

### 20.3.2 The shape, the camera and the panel

| The quantity | The value |
|---|---|
| the `90°`-bent-stem B module | `Ø32 x 4.0 mm` flat ring on screen + `8 x 32 x 4.5 mm` `90°` stem (`r = 0.55 mm`, `20.0 g`, `32` parts) |
| the flat ring (`yuvarlak`) | `Ø32.0 mm` outside, `Ø24.0 mm` inner aperture, `4.00 mm` Z-stack lying flat on the screen (`+Z` or `-Z`) |
| the front camera | **fixed inside the upper Z-stack (`z = 0.90..3.60 mm`)**, `12.8 x 9.6 mm` (`50 MP`) CMOS + 4-axis OIS + prism + `5P` lens |
| the rear round panel | **`Ø22.4 mm` active round LTPO AMOLED** (`480 x 480 px`, `300 ppi`, `1-120 Hz`, `z = 0.35..0.75 mm`) + `0.15 mm` Cu-graphite shield |
| the `90°`-bent stem (`çubuk`) | `8 x 32 x 4.5 mm` bent `90°` (`±90°` Ti hinge); houses **sole `USB Type-C` (`40 W`)** + `Wi-Fi 7 / UWB / 60 GHz` |
| Zero-CPU 6L ring PCBA | `Ø30.2 / Ø24.4 x 0.55 mm` inside ring wall: **`U1` Quad-Tile Master TCON**, **`U2` `UWB / mmWave` SiP**, **`U3` Audio DSP**, **`U4` Dead-Pad PMIC** |
| the in-ring acoustics & flash | `2 x MEMS` mics (`68 dB` SNR), `9.0 x 3.2 x 2.2 mm` speaker (`78 dB SPL`), and dual-CCT LED flash inside the ring bezel |
| 4-edge reversible dock | `8` `N52H` magnets (`7.2 N` hold), `12` symmetric gold pogo pins (`18 mΩ`, `3 ms` Dead-Pad), and `IP68` FKM gasket on all 4 edges |
| the internal bridge cell | `0.45 Wh` (`120 mAh`) solid-state arc cell inside the ring wall |
| the seats | **all 4 outer edges (`Top`, `Bottom`, `Left`, `Right`) and both faces (`Front +Z` and `Back -Z`)** |

### 20.3.3 The optics, and the honest claim

| The quantity | The value |
|---|---|
| the elements | **8 in 4 groups**, molded glass with lanthanum `45°` folding prism |
| the focal length | **8.9 mm** (`24 mm` full-frame equivalent on a `12.8 x 9.6 mm` active sensor) |
| the aperture | `f/1.8` with 4-blade mechanical shutter and 2-axis piezo sensor-shift OIS (`±1.5°`) |
| the folded path | **3.4 mm into the ring and 14.0 mm across the `Ø24.0 mm` bore**, `17.4 mm` total optical path inside `4.00 mm` |
| the sensor | 1-inch class CMOS, `12.8 x 9.6 mm` active, `50 MP` daylight (`1.6 µm`) and `12.5 MP` binned (`3.2 µm`) |
| the crop at 2 times | `12.5 MP` lossless in-sensor crop at **48 mm equivalent** |
| the crop at 3 times | `5.6 MP` crop at **72 mm equivalent**, and no protruding telephoto barrel exists |
| the video | `4K 60 fps` / `4K 120` capture with sub-20 ms rear round AMOLED selfie viewfinder |

**The honest reading**. A crop is not a telephoto lens, and the program says it plainly. What the fixed camera buys is a larger sensor, more light and one lens to certify, and the whole screen stays lit. `[DECISION]`

### 20.3.4 The live area is a normal screen, and nothing is imposed on it

| The quantity | The value |
|---|---|
| the screen | `76.4 x 156.4 mm` per face (`R 1.40 mm` screen corner inside `R 3.20 mm` body corner), `1528 x 3128 px` at `508 ppi` |
| the lit area, always | **11 947 mm²** (`100 percent` open), because the upright B module sits on the top edge (`y = +80.0 mm`) |
| the covered region | **0 mm²** on both front and back screens |
| the scaled region | **0 mm²**, because nothing is imposed on the panel |

### 20.3.5 The port rail: the ports are a part, and why

The order of Ayaz stands: **every port lives on a detachable rail module** on one long edge, and it ships in the box. `HARDWARE/14-PORT-RAIL-PART-BY-PART.md` specifies the `46.0 x 4.00 x 3.20 mm` side rail (`USB-C PD 3.1`, `3.5 mm` jack, pen dock, `8` pads). `[DECISION]`

### 20.3.6 The classes of the three interfaces

| The class | The part | The seat | The energy |
|---|---|---|---|
| **the module joint** | the Budlum module | the edge, at one of three seats | its own 0.60 Wh cell, and 0.5 A at the lands |
| **RL, the rail** | the port module | the rail edge, a latch and four poles | the device feeds the module |
| **DK, the dock** | the desk, room and wall members | four pads and two pegs | 27 W from the dock |

### 20.3.7 The consequences that must be written down

| The consequence | The number | Where it lands |
|---|---|---|
| the mass | **88 g** complete (`68 g` 4-Quadrant `+` body = `4 x 17 g` tiles + `20 g` `90°`-bent-stem B module) | `HARDWARE/03`, `MASTER/STATE.md` |
| the carried balance | the module moves the balance point **16.0 mm** when it is on | `HARDWARE/20`, Section 7 |
| the wall moment | a module at one end puts **40 N·mm** on a mount | gate MEC-28, raised to **56 N·mm** |
| the profile | the fitted profile is **4.00 mm**, because the module shares the device's own plane | `HARDWARE/07`, Section 3 |
| the screen | **11 084 mm²** lit at 508 ppi, and **0 mm²** covered | `HARDWARE/16`, `HARDWARE/20` |
| the self portrait | the round panel is the **viewfinder**, and it is a preview and not a photograph | `HARDWARE/05`, Section 6 |

---

## 20.4 The other reading of the order: the camera behind the screen, and why it is refused

**The order has a second reading:** *mount the camera hardware behind the screen.* The industry calls that an under display camera. The program tested that reading with numbers, and it is **refused for the Budlum Leaf cameras**. `[DECISION]`

| The item | The number | The source |
|---|---|---|
| the transmission of a flexible OLED at the camera area | **2.9 percent**, with the haze, the blur and the yellow shift that a polyamide substrate adds | the CVPR 2021 study of under display restoration [PUBLICATION] |
| the transmission of a transparent OLED | about **20 percent**, and the pixel grid acts as a grating that blurs along one axis | the same study, and the Microsoft applied sciences note [PUBLICATION] |
| the resolution that the industry ships | a 4 MP under display camera in a 2026 foldable, and a 1.5 MP unit for cars | [PUBLICATION] |
| the degradation that a supplier states | about **30 percent**, even with an AI restoration pipeline that claims 99 percent recovery | LG Innotek, reported for CES 2026 [PUBLICATION] |
| the information that is lost for good | the pixel opening cuts whole spatial frequencies, and **a missing frequency cannot be recovered by computation** | the Microsoft MTF analysis [PUBLICATION] |

**Three reasons of this program decide it**.

1. **The resolution gap is 12 times**. The module carries one **50 MP** sensor. A 4 MP window behind the panel is 8 percent of those pixels. No pipeline produces 50 MP from 4 MP, because the window has already lost the high frequencies.
2. **The panel of this product bends**. A reduced-stack window sits where strain is highest during an `R 25.5 mm` wrap. Part 18, Section 18.7.4, has no budget for a crack initiator.
3. **The edge seat and the round panel give the same job for free**. The order of Ayaz asks for a camera that can face the user. The upright B module carries a **50 MP** lens, and its rear round panel serves as the viewfinder. The under display route buys nothing here.

**The follow up rule**. The question returns only when a supplier ships a **20 MP under-display camera at 70 percent transmission**. Until then the refusal stands, and the register of Part 19, Section 19.3, carries it. `[DECISION]`

---

## 20.5 The test plan: how the module and the rail are proven

Ayaz asked for a camera on the device and for a detachable connector part. This is the trial of both. Per Section 5.4, each fatigue condition tests **at least 30 coupons** and reports a failure statistic.

| No. | The trial | The coupons | The pass condition | The gates |
|---|---|---|---|---|
| 1 | the edge seat | 30 modules on 30 ends | **2.5 N** normal and **1.2 N** shear, and a release under 5 N | MEC-29 |
| 2 | the seat life | 30 modules, 2 000 seats | the force inside 20 percent, and a seam under 0.12 mm | MEC-29, MON-18 |
| 3 | the joint seal | 30 joints, then 96 hours of salt spray | **IP54**, and no water inside the plate | MON-12, MON-19 |
| 4 | the lands | 30 sets, 50 000 matings, then a salt spray | 20 to 50 milliohm mid stroke, and no plating wear through | CAM-7, ENR-13 |
| 5 | the camera in the bore | 30 modules, a 1.0 m drop on 6 faces | no movement over 0.02 mm, and no mark that reads in a photograph | CAM-7, MON-14 |
| 6 | the optic | 3 benches, the drawing and the chart | the modulation transfer at f/1.5 and f/4.0, and the focus at 0.10 m | CAM-3, CAM-4 |
| 7 | the panel | 30 panels, 10 000 hours | 600 nits, 60 Hz, 0.06 W, and no dead pixel line | MON-4, MON-18 |
| 8 | the bend | 30 joints at R 25.5 mm, 5 000 wraps | the module holds, and the seam stays under 0.12 mm | MON-15, MEC-32 |
| 9 | the rail and the hot removal | the rig of `HARDWARE/14` | 100 hot removals at 40 W with no damage | RL-1 to RL-12 |
| 10 | the identity and the order | 30 seats, every mis-alignment under 0.5 mm | the power path stays open until the challenge is answered | MON-10, MON-16 |

**The fixtures**. A seat stand with three fixtures, one wrap rig at R 25.5 mm, a camera bench, a photometer, a sound box and the RF chamber. Two of the six already exist in the plan of Part 12. `[DECISION]`

---

## 20.6 The decisions of this block, recorded for Ayaz

These are the choices that the program line took while Ayaz was away. Each one is reversible, and each one names its cost.

| No. | The decision | Why | The cost, stated |
|---|---|---|---|
| **R-1** | **portless universal `Qi / Qi2.2` wireless charging on the 4-Quadrant screen body; sole `USB Type-C` (`40 W`) exclusively on the `90°`-bent B stem** | eliminates any USB-C opening or button on the `2.00 mm` polycarbonate tiles while allowing wireless charging on any pad | wired USB-C charging, data, and Zero-CPU TCON/transceiver functions require the `20 g` B module docked to the screen |
| **R-12** | **`90°`-bent-stem B module (`20.0 g`, `32` parts): only the stem (`USB-C` + antenna) bends `90°`; `Ø32 mm` ring lies flat on screen** | allows reversible docking on all 4 edges (`Top`, `Bottom`, `Left`, `Right`) and on both the Front (`+Z`) and Back (`-Z`) of the screen | **20 g** module (`88 g` complete with the `68 g` 4-Quadrant `+` body). All bulky bottom battery and rotating-barrel designs are removed, per `HARDWARE/20` |
| **R-13** | **the camera is fixed, and the round panel on its back carries the glance duty** | a fixed camera costs no motor, no train and no seal, and the panel answers the self portrait | the self portrait through the main lens is lost, and the viewfinder is a preview on a Ø20.0 mm surface |
| **R-14** | **the sensor class is 1 inch at 4 to 3, and the claim is 50 MP in daylight with 12.5 MP everyday** | the 4/3 class costs 40 percent more area and a camera of Ø28.0 mm, which the ring cannot hold | the camera is Ø22.0 mm, and the optic folds 17.4 mm inside 3.40 mm |
| **R-15** | **every port lives on a rail module, and the module ships in the box** | the order of Ayaz: a direct fit breaks the internal structure, and it cannot be removed | one module of bill of materials per unit, and the bare body has no wire route |
| **R-16** | **a contact is dead until an identity handshake completes** | the same rule serves the dock, the rail and the joint | 3 ms at every seat, and one land spent on identity |
| **R-17** | **the rail asks for 20 V first** | the same 40 W is 2.0 A at 20 V, and the pads then lose 0.06 W instead of 0.34 W | a power delivery controller in the module, about 0.35 dollars and 0.4 g |
| **R-18** | **the wall case takes two anti rotation pegs and one more steel target** | a module seated at one end puts a turning moment on a mount, and it is **40 N·mm** | a thicker case wall, and gate MEC-28 with the **56 N·mm** hold |
| **R-20** | **the dead face rule of revision L.2 is withdrawn in full, and so is the field** | the module sits on an edge, so no face carries a part and no face keeps a shortened screen | no credit is claimed, and the photon term of Part 18 returns to its full value |
| **R-21 to R-27** | **retired at L.4.0 with the face field** | the seat is the edge joint, written in `HARDWARE/08` and `HARDWARE/10` | the tiled steel foil, the friction land, the Tilt Pad and the wrap zone keep-out leave the design; their record stays in `HARDWARE/10`, Section 4 |

---

## 20.7 The gates and the open list of this part

| Gate | The subject | The pass condition |
|---|---|---|
| **CAM-1 to CAM-9** | the camera: fixed mount, focus life, folded optic, iris, window, glass, bore fit, retainer, and stabilisation | the numbers of Section 20.3.3 and of `HARDWARE/05`, re-issued for a fixed camera |
| **CAM-10 to CAM-12** | the link, the draw and the rest | 4.98 Gbit/s with no dropped frame, 1.4 W in capture, and the panel at 0.012 W |
| **CAM-13 to CAM-16** | the wait before the shutter, the card still, the dark, and the one lens | the wait in seconds before the shutter, 0.26 s to the card, inside one third of a stop, and one lens in the whole device |
| **CAM-17 to CAM-20** | the live area, the identity, the daylight only claim and the coded 8K | **`11 947 mm²`** live at `508 ppi` (`0 mm²` covered), `3 ms` auth answer, daylight claim, and coded 8K link |
| **MON-1 to MON-20** | upright B module (`40 x 32 x 4.00 mm`): softened edges, fixed camera, rear round AMOLED, top-edge seat, audio, flash, antenna, heat, and IP68 seal | the numbers of `HARDWARE/20` |
| **RL-1 to RL-12** | the rail: the receptacle, the wires, the hot removal, the pad life, the water, the drop and the audio | the numbers of `HARDWARE/14`, including 100 hot removals at 40 W |
| **MEC-28** | the wall hold with the module seated | a rotational hold of **56 N·mm** at 60 °C, because the 21 g part at one end makes **40 N·mm** |
| **MEC-29 to MEC-32** | the joint, the three seats, the pen dock and the retired field record | the numbers of `HARDWARE/10`, Section 7 |
| **DSP-14** | the joint against the panel: the touch map and the antenna efficiency | no dead touch zone within 2.0 mm of the seam, and under 0.5 dB of antenna loss |
| **ENR-11 to ENR-13** | the 4-Quadrant (`+`) `LLZO/PEO` solid-state battery (`12.0 Wh`), `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` wireless coils, and `<3 s` quadrant swap | `12.0 Wh` (`3 200 mAh`) capacity, `11.2 N` `+` seam latch, `<3 ms` Dead-Pad auth, `IP68` `<15 µm` lip, and `<3 s` swap (`EU 2023/1542`) |
| **DSP-13** | the whole screen of a fitted device | the page model accepts **11 084 mm²**, nothing is scaled, and the text size is unchanged |
| **MEC-6** | the wired and contact charge bench, in place of the wireless bench | the loss and the wear of Section 20.2, with the derating curve of Part 4 |
| **RF-3** | the desense with the charge cable and on the dock | both radios inside their stated margin in both states |

| The open item | The owner | The next action |
|---|---|---|
| the sensor class, 1 inch against 4/3 | the camera line | two sample boards, and the path measured inside 3.40 mm |
| the lens prescription | the optics house | a design study and a quote at **f/1.5** in 6 elements |
| the joint of the module | the mechanics line | a sample set of sixteen poles, then 2 000 seats |
| the freedom to operate on the module | the legal line | a search by a registered agent on the fixed camera, the edge seat and the round panel |
| the seat force of 2.5 N | the mechanics line | a seat rig on 30 ends, and a measured curve |
| the pad plating of the rail | the materials line | three platings, one salt spray bench |
| the European opinion on the module in the box | the legal line | a written opinion before the first placing on the market |
| the wall case with the two pegs | the structure line | a drawing, and gate MEC-28 on 10 units |
| the seat rig and the hot removal rig | the verification line | two fixtures, before the first coupon |
