# BUDLUM LEAF · THE DIRECTIVE · PART 21 · THE STRETCH, THE ONE MILLIMETRE STEM AND THE PROJECTION

**Revision L.6.0 · 2026-10-12 · the standing of this part**. This part supersedes every earlier statement it names in Section 21.1. Tags follow Part 20: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]`, `[GENERAL]` and `[TREE]`.

**The orders that created this part, as Ayaz gave them on 2026-10-12**.

1. *"1 mm çubuk ve esneme olması şart."* The B stem is `1.00 mm` thick. The screen body stretches, and bending alone is not enough.
2. *"Yansıtmadan kastım, işlemin ağırlıkla validatörden gelmesi."* Projection means the Leaf shows what the network computes. It does not mean an optical projector.
3. *"Diğer dediklerini onaylıyorum."* Four review points are approved. A 5G modem joins the B module. "Zero CPU" means no general processor. The B shell has no metal. The camera fits the ring.

---

## 21.1 What this part supersedes

| The earlier statement | Where it was | The ruling of L.6.0 |
|---|---|---|
| the stem is `8.0 x 32.0 x 4.50 mm` | `HARDWARE/05`, `HARDWARE/13`, `HARDWARE/01` | the stem is `8.0 x 32.0 x 1.00 mm`. Section 21.3 `[DECISION]` |
| the sole USB-C receptacle lives in the stem | `HARDWARE/05`, Part 0, Part 20 | a `3.10 mm` receptacle cannot live in a `1.00 mm` wall. It moves to the ring rim. Section 21.3.4 |
| a `±90°` Grade-5 titanium micro-hinge joins stem and ring | `HARDWARE/13`, part 13 | no hinge. The `90°` bend is moulded into one part, as `NEREDE-NE-VAR.md` already said |
| the stem housing is titanium and the ring is 6061 aluminium | `HARDWARE/13`, parts 11, 14, 31 | glass-filled LCP. A metal case around an antenna defeats the antenna. Section 21.4.1 |
| the body bends at `R 25.5 mm` and does not stretch | `HARDWARE/12`, Part 18 | the body bends and also stretches. Section 21.2 `[DECISION]` |
| the conductors are `AgNW/ITO` | `HARDWARE/02`, `HARDWARE/16` | ITO cracks near `1 %` strain. The conductors are AgNW only |
| "Zero CPU and Zero RAM" | `HARDWARE/02`, `HARDWARE/19` | no general-purpose processor and no operating system. Fixed-function silicon and a frame store are allowed. Section 21.5.1 |
| the interaction budget is served by "a local scene renderer" | Part 11, `MASTER/14` | a fixed-function compositor inside `U1` serves it. Section 21.5.4 |
| one `U2` SiP holds Wi-Fi 7, UWB and `60 GHz` | `HARDWARE/13`, part 17 | no such single part exists. The radio set splits into `U2A` and `U2B`. Section 21.4.2 |
| 5G antennas exist and no modem exists | `HARDWARE/19`, A5 and A6 | a 5G RedCap modem `U5` joins the ring. Section 21.4.3 |
| a `50 MP`, `12.8 x 9.6 mm` sensor with a folded `13.8 mm` barrel lives in a `4.00 mm` ring | `HARDWARE/13`, parts 20 to 27 | it does not fit (gap G-13). A `1/3.06"` class module replaces it. Section 21.3.5 |
| the module mass is `20.0 g` | `HARDWARE/05` | the old list summed to `22.00 g`. The L.6.0 list sums to `12.0 g`. `HARDWARE/13` |

**The rule of this part**. Where an older part and this part disagree, this part wins until the older part is rewritten. `[DECISION]`

---

## 21.2 The stretch

### 21.2.1 Why polycarbonate alone cannot stretch

| The material | The elastic strain | The use in L.6.0 |
|---|---|---|
| polycarbonate (PC) | about `2 %` before yield, `6 %` at yield `[GENERAL]` | the rigid islands and the puzzle locks |
| PC-siloxane copolymer | tougher than PC, still a few percent `[GENERAL]` | the island shells, for impact |
| ITO | cracks near `1 %` `[GENERAL]` | removed |
| serpentine copper or AgNW on an elastomer | `30 %` to `100 %` of the bridge, with the metal under `1 %` `[GENERAL]` | the bridges |
| TPU, SEBS or PDMS elastomer | `100 %` and more `[GENERAL]` | the matrix that carries the islands |

**The conclusion**. A stretching sheet is not one material. It is rigid islands that carry the active parts, joined by elastomer bridges that carry the strain. The polycarbonate stays where it is strong: in the islands, the frame and the puzzle locks. `[DECISION]`

### 21.2.2 The island-bridge body

1. **The islands**. Each tile `Q1..Q4` holds a grid of PC-siloxane islands. An island carries pixels, a micro cell, a driver or a contact.
2. **The bridges**. Serpentine AgNW and copper traces on a TPU matrix join the islands. Every trace is a horseshoe serpentine, so the metal bends and does not elongate.
3. **The cover**. A self-healing polyurethane elastomer cover replaces the hard-coated PC face. A hard coat cracks when it stretches. A self-healing cover closes a fine scratch at room temperature. `[HYPOTHESIS]` gate MEC-41.
4. **The puzzle locks stay rigid**. The `24` dovetail locks hold the tiles together. The strain happens inside each tile, so the `<15 µm` seam does not open under stretch. `[HYPOTHESIS]` gate MEC-40.
5. **The thickness stays `2.00 mm`**. The island layer replaces the continuous cell layer at the same height.

### 21.2.3 The stretch arithmetic

The global strain of a tile is the bridge share of the pitch times the bridge strain: `ε_global = (gap / pitch) x ε_bridge`.

| The option | The island | The gap | The pitch | `ε_global` at `ε_bridge = 50 %` | Cells per tile | Energy per device |
|---|---|---|---|---|---|---|
| A | `8.0 mm` | `1.0 mm` | `9.0 mm` | `5.6 %` | `4 x 8 = 32` | `9.4 Wh` |
| **B, the default** | `8.0 mm` | `1.5 mm` | `9.5 mm` | **`7.9 %`** | `4 x 8 = 32` | **`9.4 Wh`** |
| C | `7.0 mm` | `2.0 mm` | `9.0 mm` | `11.1 %` | `4 x 8 = 32` | `7.2 Wh` |

The energy column scales the L.5.0 cell (`35.0 x 75.0 mm`, `3.0 Wh`) by the island area on a `38 x 78 mm` usable tile. `[HYPOTHESIS]`

**The decision**. Option B is the default: about `8 %` elastic stretch in every direction, and `9.4 Wh` instead of `12.0 Wh`. Stretch costs about one fifth of the energy. Option C is the path if Ayaz asks for `10 %` or more. `[DECISION]` gate MEC-39 and ENR-22.

### 21.2.4 What stretch does to the display, the touch and the image

| The subject | The effect | The answer |
|---|---|---|
| the pixel density | island displays reach about `100` to `250 ppi` today, not `508 ppi` `[GENERAL]` | the stretch zone targets `250 ppi`. `508 ppi` stays a goal for the rigid island centre. Gap G-40 |
| the image under stretch | the pixel pitch grows by `ε_global` | `U1` warps the frame by the measured strain, so a circle stays a circle. Gate DSP-17 |
| the touch | a capacitive grid reads stretch as touch | the grid measures its own strain, and `U1` subtracts it. Gate DSP-18 |
| the PDLC privacy film | its stretch limit is not known | it stays on the islands only. Gate DSP-19 |
| the antennas in the body | a stretched slot detunes | the tuner of RF-18 re-matches it from the strain reading. Gate RF-21 |
| the cells | a micro cell is rigid | each cell sits on its own island, with its own fuse in the bridge. Gate ENR-23 |

**A public reference**. Stretchable OLED and micro-LED panels with tens of percent of stretch were shown in 2023 and 2024 at about `100 ppi`. `[PUBLICATION]` The class exists. The density and the life at `250 ppi` are not proven, so the claim waits for gate MEC-39.

---

## 21.3 The one millimetre stem

### 21.3.1 The geometry

| The item | The value |
|---|---|
| the stem envelope | `8.0 (Z) x 32.0 (along the edge) x 1.00 mm` wall, `r = 0.40 mm` edges |
| the stance | perpendicular to the screen face, against the screen edge |
| the contact band | the `2.0 mm` of the stem next to the ring, facing the `2.00 mm` screen edge |
| the radiating zone | the `6.0 mm` of the stem that rises past the face plane, beside the ring |
| the bend | one moulded `90°` corner between ring and stem, no hinge, `r = 0.50 mm` inner radius |
| the flip | the module turns over to sit on the back face. The geometry is symmetric, so no hinge is needed |

### 21.3.2 The `1.00 mm` stack

| The layer | The thickness | The material | The duty |
|---|---|---|---|
| outer skin | `0.20 mm` | LCP, 40 % glass fibre | the hard face, RF transparent |
| antenna layer | `0.05 mm` | laser direct structured copper on LCP | the Wi-Fi, BT and UWB radiators |
| core | `0.45 mm` | LCP, 40 % glass fibre | the stiffness |
| mmWave layer | `0.10 mm` | two-layer LCP flex | the `60 GHz` array and its ground |
| contact layer | `0.20 mm` | LCP with `12` gold spring leaves in pockets | the dock contacts, `0.15 mm` stroke |
| **total** | **`1.00 mm`** | | |

**What leaves the stem**. The USB-C receptacle, the `U_PD` controller, the magnets and the titanium. The stem carries radiators, contacts and nothing else. `[DECISION]`

### 21.3.3 The strength of a `1.00 mm` wall

The free stem is a cantilever when the module is off the screen. On the screen, the edge backs the contact band, and the magnets in the ring carry the load.

| The case | The calculation | The result |
|---|---|---|
| second moment, thin axis | `I = 8.0 x 1.00³ / 12` | `0.667 mm⁴` |
| tip load `5 N` at `32 mm`, LCP-GF40 at `E ≈ 18 GPa` | `δ = F L³ / 3 E I` | `4.5 mm` elastic deflection |
| the root stress at `5 N` | `σ = F L (t/2) / I` | `120 MPa` |
| the strength of LCP-GF40 | `[GENERAL]` | about `180 MPa` |
| the margin | `180 / 120` | `1.5` |
| the same wall in PC-GF30 | `E ≈ 7 GPa`, strength about `130 MPa` | `11.7 mm` and margin `1.1`. Refused |

**The ruling**. LCP-GF40 holds a `5 N` pry with a margin of `1.5`. The `1.00 mm` stem is feasible in LCP, and not feasible in plain or glass-filled PC. A `1.5 m` drop is gate MON-21. `[HYPOTHESIS]`

### 21.3.4 Where the USB-C receptacle goes

1. The EU common charger rule applies to a product that charges by wire. `[PUBLICATION]` Directive (EU) 2022/2380. Leaf charges by contact, so the receptacle stays.
2. The receptacle is `8.9 x 7.3 x 3.10 mm`. It fits the `4.00 mm` ring height and not the `1.00 mm` stem.
3. **The decision**. A mid-mount USB-C receptacle sits in the ring rim, opposite the stem. The smaller camera of Section 21.3.5 frees the depth. `[DECISION]` gate MON-22.

### 21.3.5 The camera that fits

| The item | L.5.0 | L.6.0 |
|---|---|---|
| the sensor | `50 MP`, `12.8 x 9.6 mm` | `13 MP`, `1/3.06"` class, about `4.7 x 3.5 mm` |
| the optics | folded prism and a `13.8 mm` barrel | a direct `4P` stack, module height about `3.4 mm` `[HYPOTHESIS]` |
| the fit in a `4.00 mm` ring | no (gap G-13) | yes, with `0.6 mm` for window and shell |
| the quality path | local | the validator develops the final image (Part 11, the split) |

**Why this is right for Leaf**. The network develops the photograph, so a large sensor buys less than it costs here. The `1.00 mm` stem and the rim receptacle need the space. `[DECISION]` gate CAM-21. Gap G-13 closes to a gate.

---

## 21.4 The strongest Wi-Fi with no local processor

### 21.4.1 The antennas

1. **A1, the stem inverted-F**. The `2.4 GHz` quarter wave is about `31 mm`. The stem is `32 mm` long and stands `6 mm` above the screen ground. That is the classic inverted-F geometry. `[GENERAL]` Target efficiency `-1.5 dB`.
2. **A2, the stem coupled arm**. A `12 mm` arm on the same layer covers `5.15` to `7.125 GHz`.
3. **A3, the ring loop**. A loop on the ring rim is the second Wi-Fi antenna. It lies flat, the stem stands upright, so the two polarisations differ. This gives true `2 x 2` MIMO. Target `-3 dB`. `[HYPOTHESIS]` gate RF-22.
4. **A4, the `1 x 4` `60 GHz` array**. It sits on the mmWave layer and looks outward from the stem face.
5. **No metal in the module shell**. The ring and stem shells are LCP-GF40. The camera can and the shields are the only metal, and they sit away from the stem tip.
6. **The magnets stay in the ring**. A magnet near A1 costs gain. The 1.5 dB rule of Part 5, Section 5.3.1 holds.
7. **A tuner per antenna**. The IMU reports the edge and the face. `U2A` loads a matching state for each of the eight seats. Gate RF-23.

### 21.4.2 The radios

| The part | The duty | Why it is separate |
|---|---|---|
| `U2A` Wi-Fi 7 and BT combo | `2 x 2`, `320 MHz`, multi-link on `5 GHz` and `6 GHz` at once | a shipping class of part `[GENERAL]` |
| `U2B` `60 GHz` and UWB | the dock link and the ranging | a separate class of part |
| `U5` 5G RedCap modem | the outdoor path, about `150 Mbit/s` down `[PUBLICATION]` 3GPP Release 17 | enough for the C2 class, at lower power than full 5G |

Each of these carries firmware on its own small core. That is allowed: Section 21.5.1.

### 21.4.3 The settings that lower the latency

| The setting | The effect |
|---|---|
| multi-link with simultaneous transmit and receive on `5` and `6 GHz` | a packet takes the clean link, so a spike on one link does not stall the frame |
| `6 GHz` first | a cleaner band with wide channels |
| restricted target wake time for the stream | the stream gets reserved air time |
| power save off during a session | no wake-up delay on each frame |
| the low-latency queue and L4S marking end to end | the queue does not grow under load `[GENERAL]` |
| 802.11bn (Wi-Fi 8) in the roadmap | its main goal is reliability and latency `[PUBLICATION]` |

### 21.4.4 The strongest signal is the shortest path

**The antenna gains a few dB. The distance to the frame renderer decides the latency.** The best Wi-Fi for Leaf is an access point in the room. The render node sits inside it. `[DECISION]`

**The Leaf Dock, redefined**. One box holds a Wi-Fi 7 access point, a `60 GHz` radio and a bonded Budlum render node. It is the "validator in the room" of Part 11, made the default path. Gate SW-20.

---

## 21.5 The projection: the network computes, the Leaf shows

### 21.5.1 What "Zero CPU" means from now on

**The definition**. Leaf has no general-purpose application processor and no operating system. It runs no third-party code. `[DECISION]`

**What is allowed**. Fixed-function silicon with signed firmware: the radios, the modem, the video decoder, the TCON, the ISP, the power chip and the secure element. Also a frame store, because a decoder needs one.

**Why the frame store is needed**. A Leaf 160 face is about `1 600 x 3 150` pixels, near `15 MB` per frame. A slice decoder with a compressed frame store holds it in about `16 MB`. `[HYPOTHESIS]`

### 21.5.2 What the Budlum tree says about validators

| The reading | The fact | The consequence |
|---|---|---|
| `src/consensus/pos.rs` | the slot is `6` seconds `[TREE]` | a frame can never pass through a block |
| `src/ai/types.rs` | AI results come from a bonded operator role, with deadlines in blocks `[TREE]` | a bonded operator model already exists |
| `README.md` | Budlum is a settlement layer `[TREE]` | the chain settles and judges, and does not stream |

**The architecture**. A **render operator** is a bonded Budlum role, in the pattern of the AI operator. It streams frames off-chain, directly to the Leaf. The chain opens the session lease, settles it per slot window and judges disputes. `[DECISION]` research order RG-18 in Section 21.7.

### 21.5.3 The projection path, part by part

1. The touch grid scans at `240 Hz`. `U1` signs the input in a batch with the secure element.
2. `U2A` sends the input to the render operator.
3. The operator renders, encodes in low-latency slices and signs a hash chain of the frames.
4. `U2A` receives the slices. `U6` decodes each slice as it arrives.
5. `U1` composes the slice into the frame store and scans it out.
6. The secure element signs a receipt over the frame hashes it showed. The receipts settle the session.

### 21.5.4 The local compositor

The interaction budget of Part 11 is under `10 ms`, and no network meets it. `U1` holds a fixed-function compositor for four jobs only: the cursor, the scroll offset, the typed glyph echo and the stretch warp. The operator sends the layers and the glyph atlas. `U1` only moves and composes them. It runs no program. `[DECISION]` gate SW-21.

### 21.5.5 The latency budget, input to photon

| The step | Dock in the room | Metro edge | Far validator |
|---|---|---|---|
| the touch scan, half of `240 Hz` | `2.0 ms` | `2.0 ms` | `2.0 ms` |
| the air uplink | `1.0 ms` | `1.0 ms` | `1.0 ms` |
| the network, one way, twice | `1.0 ms` | `16.0 ms` | `80.0 ms` |
| the render | `6.0 ms` | `6.0 ms` | `6.0 ms` |
| the slice encode | `3.0 ms` | `3.0 ms` | `3.0 ms` |
| the air downlink | `2.0 ms` | `2.0 ms` | `2.0 ms` |
| the slice decode | `2.5 ms` | `2.5 ms` | `2.5 ms` |
| the scan-out, half of `120 Hz` | `4.2 ms` | `4.2 ms` | `4.2 ms` |
| **total** | **`21.7 ms`** | **`36.7 ms`** | **`100.7 ms`** |

All rows are `[HYPOTHESIS]` until gate DST-11 measures them. **The reading**. The dock meets a `30 ms` target. A metro edge meets `50 ms`. A far validator needs the local compositor for every motion. `[DECISION]`

### 21.5.6 Only decentralised applications

1. The secure element accepts a stream only from an operator whose key is bonded on the Budlum chain.
2. The session lease names the application by its on-chain registry entry.
3. A stream with no valid lease shows nothing but the local safe screen. Gate SW-22.

---

## 21.6 The B module of L.6.0, block by block

| Block | Location | L.6.0 content |
|---|---|---|
| radiators | stem | A1 inverted-F, A2 coupled arm, A4 `60 GHz` array |
| dock contacts | stem contact band | `12` gold spring leaves, dead-pad sequence of Part 20 |
| radiator | ring rim | A3 loop |
| `U1` | ring PCBA | quad-tile TCON, local compositor, stretch warp |
| `U2A`, `U2B` | ring PCBA | Wi-Fi 7 and BT, `60 GHz` and UWB |
| `U5` | ring PCBA | 5G RedCap modem with eSIM |
| `U6` | ring PCBA | AV1 and HEVC slice decoder with the `16 MB` frame store |
| `U7` | ring PCBA | secure element: the wallet keys, the lease check, the receipts |
| `U8` | ring PCBA | IMU for the seat, the face and the tuner |
| `U3`, `U4` | ring PCBA | audio codec, power and dead-pad chip |
| camera | ring centre | `13 MP` `1/3.06"` class module and ISP |
| USB-C | ring rim | mid-mount receptacle, PD and DisplayPort |
| magnets | ring underside | `8` N52H, away from A1 |

The part list with masses lives in `HARDWARE/13-B-MODULE-PART-BY-PART.md`.

---

## 21.7 The research order for the Budlum tree

| Order | The work | The acceptance test |
|---|---|---|
| **RG-18** | a render operator role: bond, session lease, frame receipt hash chain, slot window settlement and dispute | a lease opens, `10 000` frames stream off-chain, the receipts settle in one slot window, and a forged frame loses the bond |

---

## 21.8 The new gates

| Gate | The test | The pass condition |
|---|---|---|
| **MEC-39** | the island-bridge tile at `ε_global = 7.9 %`, biaxial | `10 000` cycles, no open trace, no island crack |
| **MEC-40** | the puzzle seam under tile stretch | the seam stays under `15 µm` at full stretch |
| **MEC-41** | the self-healing cover: a `0.5 N` scratch, then room temperature | the scratch is not visible within `24 h` |
| **MEC-42** | the `1.00 mm` LCP-GF40 stem: a `5 N` tip pry, `10 000` cycles | no crack, and the set under `0.2 mm` |
| **ENR-22** | the micro-cell grid: the energy of a tile | at least `2.35 Wh` per tile at Option B |
| **ENR-23** | the cell island fuse: a short in one cell | the fuse opens, and the other cells stay in service |
| **DSP-17** | the stretch warp: a circle and a grid at full stretch | the shape error under `1 %` |
| **DSP-18** | the touch under stretch | no false touch at full stretch, position error under `1 mm` |
| **DSP-19** | the PDLC film on islands under stretch | the switch works after `10 000` cycles |
| **RF-21** | the body slot antennas under stretch | the return loss inside the limit, flat and stretched |
| **RF-22** | the stem and ring pair as `2 x 2` MIMO | the envelope correlation under `0.3` |
| **RF-23** | the eight seats, front and back on four edges | each seat inside `1.5 dB` of the best seat |
| **MON-20** | the stem thickness | `1.00 mm ± 0.05 mm` on every unit |
| **MON-21** | the module drop, `1.5 m`, six faces | the stem intact and the seat still holds |
| **MON-22** | the rim USB-C: `10 000` plug cycles and `IP68` | the receptacle holds and the seal passes |
| **CAM-21** | the `13 MP` module inside the `4.00 mm` ring | it fits with the window, and the local image meets CAM-9 |
| **SW-20** | the Leaf Dock as access point and render node | a session runs at the dock class |
| **SW-21** | the local compositor: cursor, scroll, glyph echo, warp | each job under `10 ms`, with no program run on the device |
| **SW-22** | the lease check: an unbonded operator | the stream is refused and the safe screen shows |
| **DST-11** | input to photon, three distances | the dock under `30 ms`, metro edge under `50 ms` at the 99th percentile |
