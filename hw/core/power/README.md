# BUDLUM LEAF · CORE AND SKIN · POWER SEAT

**Revision L.7 candidate · 2026-10-19 · the power seat, block HP-2 and the distance order of HP-3**. Charter: `hw/core/BRIEF.md`. It is a study. It changes no L.6.0 or L.6.1 decision. Every result is `[HYPOTHESIS]` unless a tag says more.

## 1 · The verdict, damage first

1. **The Split costs energy at every distance.** One Skin and its Core take `2.53 W` at delta. The L.6.0 Leaf takes `2.24 W`: `+13 %`.
2. **At C2 the Split buys nothing on energy.** The Skin is the L.6.0 Leaf and keeps its `2.24 W`. The remote Core adds a validator share on top.
3. **A Skin needs no cell.** A `0.1` to `1 s` store takes `1` to `12` tiles of cell layer.
4. **The Skin gets lighter by `25.3` to `32.7 g`.** That is `32` to `41 %` of the `78.8 g` device. The `128` cells, `14.6 g`, leave.
5. **The Skin heat passes at C0 and fails at C2.** The Skin takes `1.03` and `1.65 W`. The still-air ceiling is `1.73 W`.
6. **Eight Skins break most hosts.** They take `19.5 W` at delta on the host and `29.4 W` at video. Only USB-C PD, vehicle and PoE type 3 carry them.

## 2 · What is here

| The file | The job |
|---|---|
| `cpcommon.py` | shared inputs: the Skin load model, the add-on ranges, imports of `hw/hostpower/powerpath` read only |
| `skin_tree.py` | question 1: the Skin power tree, the Skin load per use case, the Bare and Buffer sizing, the tier verdict |
| `link_power.py` | question 2: power over the pads, a flex tether, a Qi-class coupling and a hybrid cable |
| `core_energy.py` | question 3: the Core for `1`, `2`, `4` and `8` Skins, its energy, heat, life and the host classes |
| `mass.py` | question 4: the Skin mass, the Core mass and the system mass |
| `distance.py` | the distance column: C0, C1 and C2 for the tree, the tier answer and the Core |
| `damage.py` | question 5: which Part 22 findings the Split strengthens or weakens |
| `run_all.py` | runs the six scripts in order |
| `out/*.txt`, `out/*.json` | the printed results and the data of every script |
| `out/*.png` | plots: `skin_loads`, `skin_bare`, `link_power`, `core_energy`, `mass` |

## 3 · How to run

1. Install `numpy`, `scipy` and `matplotlib` in user space.
2. Run `python3 hw/core/power/run_all.py`. It takes about `40 s`.
3. Read `out/damage.txt` first, then the other `out/*.txt` files.
4. Run the first scripts of `hw/hostpower/powerpath` once. This seat reads their `out/` files.

The scripts import `hw/hostpower/powerpath`, `hw/dock/params.py` and `hw/energy/out` read only. They write no bytecode and write nothing outside `out/`.

## 4 · The distance classes

| Class | The range | What reaches the Skin | The Skin in this seat |
|---|---|---|---|
| C0 | contact or tether, up to `2 m` | power and pixels, both by wire | the minimal Skin of Section 5 |
| C1a | a room, up to `30 m`, pixels at Gb/s by radio | pixels by radio. Power from a near energy host | the minimal Skin plus a radio client and a stream decoder |
| C1b | a room, slice stream at tens of Mbit/s | a slice stream | the L.6.0 Leaf, as at C2 |
| C2 | far, kilometres | slice streams at tens of Mbit/s | the L.6.0 Leaf. The Core is a validator |

**The two hosts law.** Power does not cross a room or a kilometre. At C1 and C2 the energy host is local to the Skin and the compute host is remote. The Host Life Law of Part 22 governs the energy host only. `[DECISION]` BRIEF Section 8

## 5 · Question 1: the Skin power tree

### 5.1 What stays and what moves

| The part | The call |
|---|---|
| micro-LED drivers, row and column address, hinge sensor, thermistor | stays: the emitters and the tile drivers |
| tile hub with DSC decode and `4` retimed ports, `3 mW` per tile | stays: the minimal decoder. `hw/display` already holds it in the tile `[TREE]` |
| AgNW touch front end | stays |
| seat controller, link receiver on `D0` and `D1`, back channel `BC` | stays: the link PHY |
| identity chip with the part record, no signing key | stays, and replaces `U7` `[HYPOTHESIS]` |
| `50 MP` sensor with AF and OIS | stays with the lens. Its processing moves to the Core |
| `U_Q` x4 with the `3:1` stage | stays only if the Skin takes VHV. The pad option of Section 6 needs none |
| `U1`, `U6`, `U2A`, `U2B`, `U5`, `U7`, `U8`, `U3`, `U4`, rear panel, audio, flash, jack | move to the Core |
| `128` cells, TCM, the `B cell` | leave: the cells go to the Core |

### 5.2 The Skin power tree

```
 CORE --- power ---> seat field, leaves 2 and 11 VBUS --- S_SEAT, dead-pad law of hw/energy/03 s3 ---+
                                                                                                    v
 VBUS grid, 3.40 to 4.48 V, set by the Core, no cell (a Bare store or a few cells are options)
    |-- tile nodes: micro-LED drivers, row and column address (1.0 V buck per four tiles), AgNW touch, hinge sensor
    |-- tile hub: DSC decode and 4 retimed ports
    '-- seat tile: seat controller, link RX on D0 and D1, back channel, identity chip, edge router
 CORE <--- pixels, D0 and D1, 2 pairs at 10 Gb/s ---> seat tile <--- touch, hinge angles, telemetry on BC ---> CORE
```

The Skin has no island rail, no `U4` and no B cell. It never holds a key. A power gap loses no chain state on it, because no state lives on it. `[HYPOTHESIS]`

### 5.3 The Skin load per use case

The body column of `hw/energy/04` plus the link and decoder assumed here. W at the VBUS grid, tile drivers at `0.92`, local bucks at `0.88`. The link seat refines the add-ons.

| The use case | Body | Add-ons | Low | Nominal | High | Link Gb/s |
|---|---|---|---|---|---|---|
| standby, rear glance, music, voice | `0` | `0.005` | `0.002` | `0.006` | `0.011` | `0` |
| safe screen, no link | `0.12` | `0.085` | `0.167` | `0.227` | `0.324` | `0` |
| static page at `10 Hz` | `0.17` | `0.128` | `0.246` | `0.330` | `0.475` | `0.56` |
| delta session, `250 nits` | `0.80` | `0.142` | `0.940` | `1.031` | `1.192` | `3.36` |
| delta at `41 %` stretch | `0.81` | `0.142` | `0.951` | `1.042` | `1.203` | `3.36` |
| `50 MP` camera, viewfinder | `0.80` | `0.142` | `1.329` | `1.420` | `1.581` | `3.36` |
| video, Wi-Fi | `1.35` | `0.159` | `1.549` | `1.648` | `1.828` | `6.71` |
| video outdoors, `800 nits` | `4.24` | `0.159` | `4.691` | `4.789` | `4.969` | `6.71` |

1. **The assumptions.** Link receiver `3`, `5`, `10 pJ/bit` and `15`, `30`, `60 mW` static. Touch `20`, `50`, `100 mW`. Router `10`, `30`, `60 mW`. `[HYPOTHESIS]`
2. **The Lead numbers.** The surface load of the BRIEF is `0.80` and `1.35 W` at the load. At VBUS with the add-ons it is `1.03` and `1.65 W`.
3. **The heat budget.** The ceiling is `1.73 W` still and `2.37 W` in a light wind. `[HYPOTHESIS]` `hw/hostpower/thermal`.
4. **Delta passes** by `0.70 W` nominal and `0.54 W` high. **Video passes** by `0.08 W` nominal and fails by `0.10 W` high.
5. **The link budget at video.** The video body takes `1.47 W` at VBUS. The link, decoder, touch and interface share `0.26 W` in still air.
6. **Outdoor video** at `4.79 W` fails every ceiling. The load causes it.

### 5.4 The tier question: does a Skin need Buffer, Bare or no cell

Least volume of a capacitor store for the Skin loads, in `cm³`, large-cell EDLC density behind a `0.90` converter. `[PUBLICATION]` inputs from `hw/hostpower/powerpath`.

| The load | `0.1 s` | `1 s` | `3 s` | `30 s` |
|---|---|---|---|---|
| Lead delta body `0.80 W` | `0.060` | `0.109` | `0.214` | `1.61` |
| Lead video body `1.35 W` | `0.101` | `0.184` | `0.361` | `2.71` |
| Skin delta nominal `1.03 W` | `0.077` | `0.141` | `0.275` | `2.07` |
| Skin video nominal `1.65 W` | `0.123` | `0.225` | `0.440` | `3.31` |
| Skin safe screen `0.23 W` | `0.017` | `0.031` | `0.061` | `0.456` |

1. **Part 22 asked `0.60` and `0.97 cm³`** for `3 s` at `2.24` and `3.65 W`. The Skin store is `2.8` times smaller.
2. **A capacitor store does not fit the `0.24 mm` margin, and not the `0.04 mm` margin.** The volume fits. The thickness does not.
3. **The thickness decides.** The thinnest published EDLC is `0.9 mm`. The thin solid-state cell is `0.2 mm` and cannot carry `0.8 W` through `100 Ω`.
4. **The answer needs one FINAL/21 number: the `0.90 mm` cell layer.** The margin choice does not change it.
5. **The room is there.** A `3 s` store at `0.80` to `1.35 W` takes `3` to `5` tiles.
6. **Margin volumes.** Half of the body is `1.54 cm³` at `0.24 mm` and `0.26 cm³` at `0.04 mm`. A `3 s` store at `1.35 W` fits the first by volume and misses the second.

Least micro cells of the `128`, S cell floated at `60 %`, `3 C` cap.

| The load | `3 s` | `5 min` | `30 min` |
|---|---|---|---|
| Lead delta body `0.80 W` | `5` | `6` | `15` |
| Skin delta nominal `1.03 W` | `7` | `7` | `19` |
| Skin video nominal `1.65 W` | `10` | `11` | `31` |
| Skin safe screen `0.23 W` | `2` | `2` | `5` |
| Skin outdoor video `4.79 W` | `29` | `31` | `88` |

**The verdict, per tier.**

| The tier | The call for a Skin |
|---|---|
| Full | never. The Skin holds no energy of its own |
| Buffer | not needed for continuity. A Skin without a Core shows no pixels. Option: `5` cells, `0.29 Wh`, hold the safe screen `30 min` |
| Bare | yes, a store of `0.1` to `1 s` rides a contact bounce. It lives in the cell layer, not in the margin |
| no cell at all | the default. The Skin goes dark in a gap and re-syncs when the link returns |

## 6 · Question 2: power over the link

Four ways. The Skin load is the nominal one of Section 5.3. The pads are worn, a factor `3.97` on `18 mΩ` per leaf, the worst case. `[HYPOTHESIS]`

| The option | V | I at video | Loop | Path loss | Heat on the Skin | Skin total | Efficiency |
|---|---|---|---|---|---|---|---|
| P1 pads, Core regulates VBUS | `3.9` | `0.42 A` | `71 mΩ` | `12.8 mW` | `12.8 mW` | `1.66 W` | `99.2 %` |
| P2 pads at VHV, `U_Q` on the Skin | `12` | `0.14 A` | `71 mΩ` | `52.4 mW` | `52.4 mW` | `1.70 W` | `96.9 %` |
| P3 flex tether `0.5 m`, `U_Q` on the Skin | `12` | `0.14 A` | `244 mΩ` | `55.8 mW` | `51.8 mW` | `1.70 W` | `96.7 %` |
| P3 flex tether `2.0 m` | `12` | `0.14 A` | `735 mΩ` | `65.7 mW` | `51.8 mW` | `1.70 W` | `96.2 %` |
| P4 Qi-class coupling, power only | `12` | `0.14 A` | none | `473 mW` | `104 mW` | `1.75 W` | `77.7 %` |
| P4 Qi plus a `60 GHz` radio for the pixels | `12` | `0.20 A` | none | `669 mW` | `153 mW` | `2.48 W` | `77.7 %` |
| P5 hybrid cable, `1 m`, `24 AWG` | `12` | `0.16 A` | `193 mΩ` | `61.8 mW` | `57.2 mW` | `1.90 W` | `96.8 %` |

1. **P1 wins.** The Core holds VBUS at `3.90 V` through the back channel. The worn drop is `30 mV` and a leaf carries `0.21 A` of `1.5 A`.
2. **P2 costs `40 mW` more** on the Skin at video, for the `U_Q` stage. It buys a lower current for a long lead.
3. **The flex tether is the same physics** with a longer loop. A `2 m` lead adds `13 mW` to the cable and nothing on the Skin beyond the stage. `[HYPOTHESIS]`
4. **Qi puts `104 mW` on the Skin**, `2.0` times the P2 value. It gives no pixels. A radio for the pixels adds `0.68 W` to the Skin.
5. **The hybrid cable shares one connector** with the pixels. It is the best product shape. It costs the Skin the PHY, `+0.19 W`.
6. **Pixels.** The pad pairs carry `19.4 Gb/s` payload against `13.9 Gb/s` needed. `[TREE]` `hw/display/out/interface.txt`.
7. **At the delta load** P1 puts `1.3 mW` new and `5 mW` worn on the Skin. Qi puts `63 mW`.
8. **Outdoor video** at `4.79 W` fails the `1.73 W` ceiling in every option. The load causes that, not the link.

## 7 · Question 3: the Core

### 7.1 The Skin catalogue and the model

| The Skin | Pixels | Body, delta and heavy | Skin at VBUS, delta and heavy | Link, delta and heavy |
|---|---|---|---|---|
| Leaf 80 | `2.6 Mpx` | `0.45` and `0.76 W` | `0.60` and `0.95 W` | `1.7` and `3.4 Gb/s` |
| Leaf 160 | `5.1 Mpx` | `0.80` and `1.35 W` | `1.03` and `1.65 W` | `3.4` and `6.7 Gb/s` |
| Leaf 480 | `4.1 Mpx` | `5.80` and `9.79 W` | `6.97` and `11.32 W` | `0.45` and `2.7 Gb/s` |
| Frame | `16.6 Mpx` | `0.80` and `1.20 W` | `1.00` and `1.46 W` | `10.9` and `16.3 Gb/s` |

The Core load is radio plus authority plus a hub fixed part plus, per Skin, a hub variable part and a link transmitter. The hub fit reproduces four rows of FINAL/04 4.6 exactly: fixed `0.50 W` (delta) and `1.00 W` (video), plus `0.10 W` per `2.56 Mpx`. The Core cell takes the load at `0.90`. The Skin supply takes `0.93`. The host input takes `0.95`.

The mixes. `N=1`: Leaf 160. `N=2`: Leaf 160 and Leaf 80. `N=4`: two Leaf 160, Leaf 80, Frame. `N=8`: Leaf 480, three Leaf 160, two Leaf 80, two Frames.

### 7.2 The Core power and heat, W

| N | Class | Core load | Skins | Bus | Host input | Core heat |
|---|---|---|---|---|---|---|
| 1 | delta | `1.28` | `1.03` | `2.53` | `2.66` | `1.63` |
| 1 | heavy | `2.00` | `1.65` | `4.00` | `4.21` | `2.56` |
| 1 | peak | `4.08` | `4.79` | `9.69` | `10.20` | `5.41` |
| 2 | delta | `1.42` | `1.63` | `3.33` | `3.51` | `1.88` |
| 2 | heavy | `2.16` | `2.60` | `5.19` | `5.46` | `2.87` |
| 4 | delta | `2.44` | `3.66` | `6.65` | `7.00` | `3.34` |
| 4 | heavy | `3.25` | `5.71` | `9.75` | `10.26` | `4.56` |
| 4 | peak | `5.33` | `8.85` | `15.44` | `16.25` | `7.40` |
| 8 | delta | `3.80` | `13.26` | `18.49` | `19.46` | `6.20` |
| 8 | heavy | `4.71` | `21.08` | `27.91` | `29.38` | `8.29` |
| 8 | peak | `6.79` | `24.22` | `33.60` | `35.37` | `11.14` |

1. **The price of the Split at N=1.** The bus takes `2.53 W` against `2.24 W` at delta, `+13 %`. Video is `+10 %`. Peak is `+11 %`.
2. **The extra** is the second conversion of the Skin supply, the link transmitter and the link receiver.
3. **The Core heat** is the Core load plus the conversion losses. The Skin power leaves the Core as electricity.
4. **The Core heat grows slowly.** At delta: `1.6 W` for one Skin, `6.2 W` for eight.
5. **The Skin heat** moves out of the hand and into the Skin at `1.0` to `7.0 W` each. The heat seat owns that.

### 7.3 The Core energy

Nominal cell energy for a session on the Core alone at the delta class. Cells at the S model, `574 Wh/kg` and `750 Wh/L`. A pack adds about `1.3` times the mass. `[HYPOTHESIS]`

| N | `1 h` | `4 h` | `8 h` |
|---|---|---|---|
| 1 | `2.7 Wh` | `10.9 Wh`, `19 g` | `21.7 Wh`, `38 g` |
| 2 | `3.6 Wh` | `14.3 Wh`, `25 g` | `28.6 Wh`, `50 g` |
| 4 | `7.1 Wh` | `28.6 Wh`, `50 g` | `57.1 Wh`, `100 g` |
| 8 | `19.9 Wh` | `79.4 Wh`, `138 g` | `158.8 Wh`, `277 g` |

**The power limit of the Core cell.** The cell must carry the power, not only the energy. At `3 C` the Core needs `5.1 Wh` of cells for `4` Skins at peak and `11.2 Wh` for `8`. The `128` micro cells carry about `20 W` at `3 C`. So eight Skins at peak need a Core cell, not the micro cells.

**The Core cell life**, host-fed, float `50 %`, `25 °C`, `6` hand-overs a day of `4 min` at delta, `4` Skins. `[HYPOTHESIS]`

| The Core Buffer or cell | Energy | Cycles a day | Years to `80 %` |
|---|---|---|---|
| Buffer for `5 min` | `1.2 Wh` | `2.17` | `2.7` |
| Buffer for `30 min` | `7.4 Wh` | `0.36` | `10.8` |
| Core for `4 h` | `59 Wh` | `0.05` | `14.6` |
| Core for `8 h` | `118 Wh` | `0.02` | `15.2` |

### 7.4 What N Skins cost the host classes of Part 22 Section 22.6

The need is the Core host input of the class plus a top-up at `0.2 C` of a `4 h` Core cell. The letters are delta, heavy, peak. `y` carries it.

| Host | Offered | N=1 | N=2 | N=4 | N=8 |
|---|---|---|---|---|---|
| H0 wall dock | `25 W` | y y y | y y y | y y y | none |
| H1 dock pack `20 Wh` | `25 W` | y y y | y y y | y y y | none |
| H2 desk USB-C PD | `45 W` at `15 V` | y y y | y y y | y y y | delta only |
| H3 vehicle `12 V` and `24 V` | `45 W` | y y y | y y y | y y y | delta only |
| H4 industrial `24 V` | `25 W` | y y y | y y y | y y y | none |
| H4 PoE type 2 | `22.9 W` | y y y | y y y | y y y | none |
| H4 PoE type 3 | `45.9 W` | y y y | y y y | y y y | delta and heavy |
| H5 worn bank or belt | `18 W` | y y y | y y y | delta and heavy | none |
| H6 Qi pad `5 W` | `5 W` | none | none | none | none |
| H6 Qi2 pad `15 W` | `15 W` | y y y | y y y | delta only | none |
| H6 Qi2.2 pad `25 W` | `25 W` | y y y | y y y | y y y | none |

1. **Four Skins** run on every host except the `5 W` pad. The `15 W` pad runs them at delta only. The bank loses the peak.
2. **Eight Skins** need `19.5 W` at delta and `29.4 W` at video. Only H2, H3 and H4 type 3 carry them, and only at delta or heavy.
3. **The top-up decides** at N=8. A `4 h` Core cell of `79 Wh` takes `15.9 W` of top-up at `0.2 C`. The load alone is `19.5 W`.
4. **The batteries.** At N=8 the H1 pack runs `0.9 h` and the H5 bank `0.8 h`. At N=1 they run `6.1` and `5.7 h`.
5. **Host energy per hour** at N=8 and delta: `22 Wh` on contact hosts, `24 Wh` on a Qi pad.

## 8 · The distance column

### 8.1 The Skin load and the tree

| The class | Skin delta | Skin video | Margin to `1.73 W` still | The tree |
|---|---|---|---|---|
| C0 minimal Skin | `1.03 W` | `1.65 W` | `+0.70` and `+0.08 W` | the tree of Section 5.2. Pads or tether, no cell, no ring |
| C1a radio client and stream decoder | `1.70 W` | `2.76 W` | `+0.03` and `-1.03 W` | the C0 tree plus a radio and a decoder. Power from a near host or a cell |
| C1b slice stream | `2.24 W` | `3.65 W` | `-0.51` and `-1.92 W` | the full L.6.0 tree of `hw/energy/03` |
| C2 far | `2.24 W` | `3.65 W` | `-0.51` and `-1.92 W` | the full L.6.0 tree. The energy host is local. The compute host is remote |

**At C2 the Skin keeps** the radio, the `5G` modem, the decoder, the frame store, the compositor and the authority of L.6.0. The load is the battery power of `hw/energy/04`: `2.24 W` at delta and `3.65 W` at video. `[TREE]` The Split buys nothing on energy there.

### 8.2 The tier answer per class

| The class | The Skin tier answer |
|---|---|
| C0 | no cell by default. A store of `1 s` in `2` to `3` tiles of cell layer. Buffer only as the `5` cell safe screen |
| C1a | a Skin with no tether needs a near energy host or a cell. On a contact host the C0 answer holds. A free Skin is Full. Buffer at `3 s` needs `11` cells at delta and `17` at video |
| C1b and C2 | the Part 22 answer holds unchanged: Buffer `14`, `22`, `53` cells at `3 s`, Bare outside the margin, Full to roam |

### 8.3 The Core per class, host input in W

| N | C0 wired Core, delta and heavy | C1a radio Core, delta and heavy | C2 validator |
|---|---|---|---|
| 1 | `2.66` and `4.21` | `3.88` and `4.47` | `18 W` for `1` Leaf, `18.0 W` per Leaf |
| 2 | `3.51` and `5.46` | `4.35` and `4.94` | `18 W` for `2` Leaves, `9.0 W` per Leaf |
| 4 | `7.00` and `10.26` | `6.04` and `6.63` | `18 W` for `4` Leaves, `4.5 W` per Leaf |
| 8 | `19.46` and `29.38` | `8.75` and `9.33` | `18 W` for `8` Leaves, `2.25 W` per Leaf |

1. **The C0 column** holds the whole system, because the Core feeds the Skins. The **C1a column** is the Core alone. The Skins sit on their own hosts.
2. **The C1a Core radio** is a `60 GHz` array: `2.5 W` for one Skin, `0.3 W` for each more. `[TREE]` `hw/dock/params.py`.
3. **The system at N=1, delta:** C0 `2.53 W`, C1a `5.59 W` (`+149 %`), C2 `2.24 W` plus the validator share.
4. **The C2 validator** is one `18 W` module in `hw/dock/params.py`. The dock sizing found that module short of the `240 Hz` frame rate. The fleet seat counts the sessions.
5. **Hosts at C1 and C2.** Each Skin or Leaf stands on its own Part 22 host. The `5 W` pad fails the Core and the C2 Leaf peak. It carries the C1a Skin.

### 8.4 What holds at C0, C1 and C2

| The result | C0 | C1 | C2 |
|---|---|---|---|
| no cell on the Skin | holds | holds on a near host | does not hold |
| Bare store in the cell layer | holds | as Part 22, bigger load | as Part 22 |
| Buffer `3 C` power limit | `5` to `10` cells | `11` to `17` cells | `14` to `53` cells |
| Skin heat under `1.73 W` | holds at delta, marginal at video | marginal at delta | fails |
| Core energy and the host classes | holds | holds for the Core alone | not needed: the Core is on mains |
| energy price of the Split | `+10` to `+13 %` | `+149 %` at N=1 | no gain, plus the validator share |

## 9 · Question 4: the mass

The reference is the L.6.0 device: body `68.0 g` plus B module `10.80 g`, `78.8 g`. The `10.80 g` is the sum of the `32` parts of `HARDWARE/13`, `[HYPOTHESIS]` until weighed. The `68 g` is stated in FINAL/21.

**The 68 g needs a warning.** The tile stack of `hw/seam` weighs `54.3 g` for `128` tiles. With the micro cell at `0.114 g` it weighs `43.3 g`. The stated `68 g` leaves `24.7 g` for hinges, lips, magnets and ribbons. It is a carry-over of the L.5.0 body, not a L.6.0 weighing. The saving below does not depend on it.

| The Skin | Mass | Saves | Body thickness |
|---|---|---|---|
| S0 no cell, Qi coil kept | `53.5 g` | `25.3 g`, `32.1 %` | `1.10 mm` |
| S1 no cell, no coil, pads power | `46.1 g` | `32.7 g`, `41.5 %` | `1.00 mm` |
| S2 S1 plus a Bare store of `1 s` | `46.3 g` | `32.5 g`, `41.3 %` | `1.00 mm` |
| S3 S1 plus `5` cell Buffer | `46.6 g` | `32.2 g`, `40.8 %` | `1.00 mm` |
| S4 S1 plus a camera pod | `47.3 g` | `31.5 g`, `40.0 %` | `1.00 mm` |
| S5 S0 plus camera pod and `5` cell Buffer | `55.3 g` | `23.5 g`, `29.8 %` | `1.10 mm`, pod thicker |

1. **What leaves.** The `128` cells `14.6 g`, `7.38 Wh`. The B module `10.8 g`. The coil layer `7.4 g` net of a `0.10 mm` graphite spreader.
2. **The cells leave the Skin by default.** Options: `0.2 g` of Bare store or `0.57 g` of `5` cells.
3. **The Skin is lighter by `25.3` to `32.7 g`.** It adds `0.15 g` of chips. A camera pod adds `1.2 g`.
4. **The Core mass** for `3 h` is `33`, `47`, `75`, `132 g` at `1`, `2`, `4`, `8` Skins.
5. **The system.** At N=1 the pair weighs `79 g` (S1) against `79 g`. At N=2 it is `-12 %`. At N=4 it is `-18 %`. At N=8 it is `-21 %`.
6. **Break-even on mass** is two Skins on one Core. A Skin worn alone is lighter. The pair at N=1 is not.
7. **The thickness.** With no cell the stack is `1.10 mm` with the coil and `1.00 mm` without. `[TREE]` stack of FINAL/21 21.2.7.

## 10 · Question 5: the damage report

| The Part 22 finding | The Split | Why |
|---|---|---|
| Bare store does not fit the margin | strengthened at C0, unchanged at C2 | the store is `2.8` times smaller and fits the cell layer in `3` to `5` tiles. It still misses both margins on thickness |
| Buffer power limit | weakened for the Skin, strengthened for the Core | the Skin needs `5` to `10` cells, not `14` to `53`. The Core needs `5.1 Wh` at `3 C` for `4` Skins at peak |
| host peak of `8.7 W` | weakened | the pair takes `+13 %` at delta. `8` Skins take `19.5` to `29.4 W`. H0 carries `4` Skins |
| cell life | strengthened | no cell in the surface. A Core cell for `4 h` lives `14.6` years host-fed. A Buffer for `5 min` lives `2.7` |
| free-air heat | strengthened at C0 only | the Skin takes `1.03 W` at delta and passes. At C2 it takes `2.24 W` and fails |
| mass | strengthened | the Skin is `32` to `41 %` lighter. The pair breaks even at `2` Skins |
| energy | weakened | `+13 %` at C0, `+149 %` at C1a for one Skin, no gain at C2 |

**The sentence for the study.** The Split pays on Skin mass and Skin heat at C0. It costs energy at every distance. It does not pay at C2.

## 11 · The open issues

1. **The add-ons are mine.** The link, router, touch and identity loads are `[HYPOTHESIS]`. The link seat refines them. A high case passes delta and fails video by `0.10 W`.
2. **The touch load can be counted twice.** `hw/energy/04` lists no touch row. I added `0.05 W`. If the hub row holds it, the Skin load falls by `0.06 W`.
3. **A Skin without a frame store** cannot hold a static page. The safe screen needs a local image in the tiles. The display team owns that.
4. **The `68 g` body** does not match the bottom-up tile stack. I cannot say how much of the `24.7 g` gap is real.
5. **The thin EDLC** is the open part. A part under `0.2 mm` with an ESR times volume under `0.2 Ω·cm³` would fit the `0.24 mm` margin. None is published.
6. **The `0.24 mm` or `0.04 mm` margin** of FINAL/21 does not change my answer. A thin part would feel it.
7. **The C1a numbers** take the radio column of `hw/energy/04` and a decoder of `0.25` and `0.45 W`. Both are `[HYPOTHESIS]`.
8. **The C2 validator share** uses one `18 W` module. The dock sizing says the module cannot serve `240 Hz`. The fleet seat counts the sessions.
9. **The Core is a single point of power.** A Core fault darkens every Skin on it. The session seat reads that cost.
10. **The heat of the Core box** needs the heat seat. My Core heat is a power balance, not a temperature.
11. **A Core cell for peaks** is a different cell from the micro cell. It needs `3 C` or better and `11 Wh` at eight Skins. No such cell is in the program.
12. **Python 3.14 here had no numpy.** The run needs a path to numpy, scipy and matplotlib.

## 12 · The proposed gates

| Gate | What it measures | The pass condition |
|---|---|---|
| HC-P1 | the Skin load at VBUS, delta and video, link on, free air | at most `1.19 W` and `1.83 W`, the high case. The nominal is `1.03` and `1.65 W` |
| HC-P2 | the link, router, touch and identity budget at the video load | at most `0.26 W` in still air, with the interface included |
| HC-P3 | Core-regulated VBUS on worn pads at `1.25 A` | at tiles `3.90 V` within `0.05 V`, drop at most `60 mV`, no leaf over `1.5 A` |
| HC-P4 | the pad interface heat at the video load, new and worn | at most `0.02 W`, and a value over `0.10 W` is a stop |
| HC-P5 | a Bare store in the cell layer, `1 s` at `1.65 W` | at most `3` tiles at large-cell density or `15` of chip EDLC, VBUS at or over `3.40 V` |
| HC-P6 | the cold start of a Skin with no cell, from `0 V` | VBUS at `3.40 V` within `5 ms` of the proof, and no host before the proof |
| HC-P7 | the Core input for `1`, `2`, `4` Skins | within `10 %` of Section 7.2 at delta and heavy |
| HC-P8 | the Core cell power: `4` Skins at peak | the cell carries `15.4 W` for `3 s` at `3.40 V` or more, at `3 C` or better |
| HC-P9 | `4` Skins on H0, H5 and H6 Qi2 | the carry table of Section 7.4, and no host reaches VBUS before the proof |
| HC-P10 | the Skin mass, S0 and S1 | at most `54 g` and `47 g`, `10 %` allowed, with the part list weighed |
| HC-P11 | the price of the Split at N=1, delta | system power at most `2.8 W`, that is `+25 %` against `2.24 W` |
| HC-P12 | the C1a Skin, delta, radio and decoder on | at most `1.80 W`. A higher value ends the C1a Skin |
| HC-P13 | the two hosts law at C2 | the Leaf passes its Part 22 gates with the Core remote. The Core adds no load above authority |

## 13 · The sources

1. `[TREE]` `hw/energy/03`, `04`, `05` and `out/`, `hw/display/out/interface.txt` and `tile_spec.txt`, `hw/seam/kinematic_seat.py`, `hw/dock/params.py`.
2. `[TREE]` `hw/hostpower/powerpath` and `hw/hostpower/thermal`: the tiers, the hosts, the cell life, the heat ceiling.
3. `[PUBLICATION]` the capacitor and cell datasheets of `hw/hostpower/powerpath/README.md`: Maxwell BCAP3000, Seiko CPH3225A, Taiyo Yuden LIC1030RS3R8206, ST EFL700A39.
4. `[PUBLICATION]` Schmalstieg et al., J. Power Sources 257 (2014) 325-334, through Lee et al., IFAC-PapersOnLine 56(2) (2023).
5. `[TREE]` `HARDWARE/13` for the B module masses. `FINAL/04` section 4.6 for the Leaf 80 and Leaf 480 loads.
