# BUDLUM LEAF · THE DIRECTIVE · PART 23 · THE CORE, THE SKIN AND THE HEARTBEAT

**Revision L.7 candidate · 2026-10-19 · the standing of this part**. This part adds to Parts 21 and 22 and changes no L.6.0 number. Part 23 is a candidate for Ayaz, and each ruling in it is a candidate until Ayaz signs. Where it finds a fault in an earlier part, Section 23.14 names it. Tags follow Part 20: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]`, `[GENERAL]` and `[TREE]`.

**The three orders that created this part**. All were given by Ayaz on 2026-10-19.

1. *Keep all the components of the screen in a separate hardware. The screen then costs less. One hardware serves many screens.*
2. *The hardware and the device can be kilometres apart. The antenna of the hardware can be large. The Leaf keeps its antennas where the designs show them.*
3. *Whatever is needed stays in the part that holds the camera hardware. Everything else lives in the hardware. The battery can sit in the Leaf, but very small. The energy is then unlimited. This must be an invention.*

Ayaz also set the method for the third order: try wild directions, fail, and go on. Section 23.10 is that search. `[DECISION]`

**The standing**. Nine study seats and the Lead ran the work. The files are in `hw/core/`. Every number is `[HYPOTHESIS]` until its gate runs. The studies narrowed the idea. This part writes the narrow form and what it still wins.

---

## 23.1 The verdict in one table

| The aim of Ayaz | The result | The tag |
|---|---|---|
| the screen costs less | **fails in part**. A Skin costs `15 %` less. The micro-LED tiles are `76 %` of the unit and never move | `[HYPOTHESIS]` |
| the screen is lighter | **holds**. A Skin weighs `17` to `40 g` against a `47 g` body, and `0.90` to `1.00 mm` against `2.00 mm` | `[HYPOTHESIS]` |
| one hardware serves many screens | **holds**. The break-even is `2` Skins on one Core | `[HYPOTHESIS]` |
| parts change in the hardware | **holds**, at C0 and C1 | `[HYPOTHESIS]` |
| nothing but the camera stays in the screen part | **fails**. The radio, the decoder and a ROM must stay for physics | `[HYPOTHESIS]` |
| the hardware is kilometres away | **holds, with no change to the Leaf**. At C2 the Leaf is the L.6.0 Leaf | `[HYPOTHESIS]` |
| the energy is unlimited | **holds where a host stands**. It does not hold in a held hand in the open air | `[HYPOTHESIS]` |
| a stolen screen is worth glass | **partly**. It is true for the money, and false for an unhardened chip | `[HYPOTHESIS]` |
| it is a world first | **not as stated**. Section 23.12 gives the claim that survives | `[PUBLICATION]` |

**The one-line answer**. The Split works as a wired Skin on a Core that sits within about `30 m`. At a greater distance the Leaf keeps its silicon, and the energy question is answered by a law of three zones: the Heartbeat. `[DECISION]`

---

## 23.2 The two names and the three distance classes

| The part | The name | What it holds |
|---|---|---|
| the surface, with the camera part | **the Skin** | the emitters, the tile drivers, the link, a decoder, an identity and the camera part |
| the hardware | **the Core** | the silicon, the radios, the wallet, the session, the image processing and the energy |

The names are working names of this study. The naming law holds: a claim says "Budlum Leaf" and the size. `[DECISION]`

| Class | The reach | The link | What the Skin keeps |
|---|---|---|---|
| **C0** | contact or a tether, up to `2 m` | the `12` gold leaves and a `0.3 m` flex clip | emitters, tile drivers, link PHY, decoder, identity, ROM |
| **C1** | a room, up to about `30 m` | a fibre clip, or `60 GHz` in line of sight to `52 m` | the same, and a cell for a cordless Skin |
| **C2** | kilometres | the Leaf radios and a validator at the radio end | everything of the L.6.0 Leaf |

---

## 23.3 The Rule of Necessity

**The ruling of Ayaz**. Whatever is needed stays in the part that holds the camera hardware. Everything else lives in the Core. `[DECISION]`

**The reading of the Lead**. A part stays in the B module only if physics forces it at the distance class. `[DECISION]`

| The part | At C0 | At C1 | At C2 | The physics that forces it |
|---|---|---|---|---|
| lens, sensor, flash | stays | stays | stays | the optics sit where the light is |
| microphones, speaker, jack | stays | stays | stays | a transducer sits where the air is |
| antennas as designed | stays | stays | stays | the Leaf keeps its antennas by the order |
| radio front end and baseband | on the line | stays | stays | the radio SiPs hold both in one die |
| slice decoder and frame store | stays | stays | stays | no radio carries the raw stream |
| local compositor | on the line | stays | stays | the `30 ms` budget at distance |
| hardened identity element | stays | stays | stays | a Skin must prove who it is |
| safe screen ROM | stays | stays | stays | `U1` holds it, so a ROM die stays |
| wallet signer and session | Core | Core | Leaf | at C2 the wallet stays in the Leaf |
| camera encoder | stays | stays | stays | a raw camera stream dies on the uplink past `0.3 km` |
| image processing after the encoder, AI | Core | Core | Core | no physics forces it |
| validator role | Core | Core | Core | by Part 21 Section 21.5 |
| cells, `128` of them | Core | stay | Leaf or host | the energy host and the compute host differ |

### 23.3.1 What actually leaves the Leaf

| The result | The value |
|---|---|
| mass that leaves at C0 | `20.85 g`, which is `40.5 %` of `51.5 g` |
| of that, the cells | `19.57 g` |
| of that, silicon, cans and the oscillator | `1.28 g` |
| mass that leaves at C1 and C2 | `0 g` |
| cost that leaves at C0, at one million units a year | about `158 USD`, which is `10 %`, with a range of `111` to `231` |
| ring volume freed at C0 | `377 mm³`, which is `24 %` of the electronics layer |
| ring board area needed today | `114 %` of the free area. At C0 it needs `35 %` |

`[HYPOTHESIS]` `hw/core/parts/`.

**What the table says**. "Move the components out" means, in mass, "move the cell out". The silicon is `1.28 g`. The unit cost is the micro-LED tile, and it stays. `[HYPOTHESIS]`

**The stale numbers**. The `68 g` body and the `88 g` complete figures are L.5.0 numbers. They count the withdrawn LLZO cells and a `20 g` module. The L.6.0 Leaf weighs `51.5 g` bottom up, with a body of about `41` to `47 g`. The figure of `68 g` stays in older parts as history. `[HYPOTHESIS]`

---

## 23.4 The wired Skin

The link seat found that the Split lives as a wired Skin, and dies as a cordless Skin. `[TREE]` `hw/core/link/`.

| The result | The value |
|---|---|
| the pixel stream, `1600 x 3200`, `240 Hz`, `10 bit` | `36.9 Gbit/s` raw |
| display stream compression at `10 bpp` | `13.1 Gbit/s` on the leaf lanes, and `19.4 Gbit/s` for the pair |
| the best published ratio | `5:1`, which is `7.4 Gbit/s`. The `6:1` of the first brief is outside the range |
| the Skin, the body without cells, coil and ring | `17 g` and `1.00 mm`, `64 %` under the `47 g` body |
| the Skin load | `0.95 W` delta, `1.57 W` video, `1.97 W` full motion |
| a wired tether | adds `0.094 ms` |
| the input to photon `p99` | `18.9 ms` on the Wi-Fi room path and `24.3 ms` on the 5G path |
| the compression the mesh needs with a hinge broken | at least `2.08:1`, so the decoder stays on the Skin |

**Three seats weigh three Skins.** The link seat weighs the body alone at `17 g`. The study seat gets about `40 g`. The power seat includes the ring and gets `46` to `53 g`, against `78.8 g` for the old device. All three are lighter than the L.6.0 Leaf, and the figures differ by definition. `[HYPOTHESIS]`

**The pick for the first Skin**. The `12` gold leaves with a `0.3 m` flex clip. Every tether is a clip on one seat. `[DECISION]`

**The stretch goal**. A hybrid fibre clip for C1 reach, with the Skin unchanged. `[DECISION]`

**The cordless Skin**. It needs its own cell of `4.8` to `5.7 Wh` and weighs `48` to `52 g`, so it is the L.6.0 body again. A `60 GHz` cordless Skin draws about `3.35 W` against the `1.73 W` limit. The cordless Skin is refused. `[DECISION]`

**The hub caveat**. The surface loads of `0.80` and `1.35 W` leave out the tile hubs. Full motion at `240 Hz` is `1.97 W` and fails the `1.73 W` limit. If the hub domain sits on the tiles, video is `2.59 W` and fails both limits. Gap G-49. `[HYPOTHESIS]`

### 23.4.1 The heat of the Skin

| The case, `25 °C`, still air | The hottest face point |
|---|---|
| the L.6.0 body, delta | `41.3 °C` |
| the Skin alone, delta `0.80 W` | `28.7 °C` |
| the Skin alone, video `1.35 W` | `30.6 °C` |

`[HYPOTHESIS]` `hw/core/heat/`. The sustained display and address power of a Skin is `2.93 W`, against `1.73 W` for the L.6.0 body.

| The finding | The value |
|---|---|
| the old hot spot under the ring | gone. The face is flat to `0.2 K` |
| a `0.25 W` link PHY on the seat tile | adds `4.0 K` |
| a `0.34 W` seat loss | adds `5.9 K`, and delta then fails at `37.7 °C` |
| gap G-46 closes at C0 | to `30 °C` ambient |
| gap G-46 closes at C1 | to `25 °C` ambient, with a `0.9 W` PHY |
| gap G-46 at `35 °C` | does not close. Delta reaches `38.6 °C` |
| gap G-46 at C2 | does not close. Delta reaches `39.5` to `51.2 °C` |
| the Frame limit | moves from `1.05 W` to at most `1.24 W` at `25 °C` |

**The new hot spot is a source on one tile.** One watt on the seat tile costs `2.95 W` of display power. Spread, it costs `0.99 W`. `[HYPOTHESIS]`

---

## 23.5 The Core

| The result | The value |
|---|---|
| one Skin and its Core | `2.53 W` at delta, against `2.24 W` for the L.6.0 Leaf, so `13 %` more |
| one Skin on a room Core of C1 | `149 %` more, because of the Core radio array |
| `8` mixed Skins | `19.5 W` at delta and `29.4 W` at video |
| the host class that carries `4` Skins | H0 at most |
| the host classes that carry `8` | USB-C PD, vehicle and PoE type 3 |
| the Core heat, `1` to `8` Skins | `1.7` to `35 W`, and a validator adds `20 W` |
| a passive box of `140 x 90 x 30 mm`, `43 °C` peak | `4` delta Skins or `2` video Skins at `25 °C`, and `1` at `35 °C` |
| a box with a fan and fins | `28` Skins |
| the Core cell for `8` Skins at `3 C` | `11.2 Wh`, which the micro cells cannot deliver |
| a Core Buffer of `5 min` | ages out in `2.7` years |

`[HYPOTHESIS]` `hw/core/power/`, `hw/core/heat/`.

**The Core is a heat product.** Above `4` Skins it needs a fan. The tether heats both ends, and a fixed contact loss is a large share of the small Skin heat. `[HYPOTHESIS]`

**The energy bill**. The Split costs energy at every distance. At C2 the Skin is the L.6.0 Leaf, so the Split buys nothing on energy there. `[HYPOTHESIS]`

---

## 23.6 The far Core, kilometres away

The far-link seat built a link budget from `100 m` to `10 km`. `[TREE]` `hw/core/far/`.

| The result | The value |
|---|---|
| the best Leaf radio, `802.11ay` on one stream | `13.6 Gbit/s`, so the raw stream of `36.9` fits no radio at any distance |
| a compressed pixel stream with a `25 dBi` Core array | `29 m` at `3:1`, and at most `52 m`, in `60 GHz` line of sight only |
| the slice stream of `150 Mbit/s`, urban shadow | `570 m` |
| the slice stream of `150 Mbit/s`, line of sight | `4.4 km` |
| the slice stream of `150 Mbit/s`, rural line of sight | `7.3 km` |
| the slice stream of `25 Mbit/s` in the same three cases | `1.6`, `5.9` and `11.7 km` |
| the input to photon `p99`, Core at the radio | `21.5 ms` at every distance where the link exists |
| the backhaul the Core can sit behind | `7.6 ms` round trip, about `490 km` of fibre |

**The distance law**. Up to about `30 m` a wired or `60 GHz` Skin can show a pixel stream, and the decoder stays. Beyond about `50 m`, or with a wall or a hand in the path, the Leaf needs `U6` and `U1`. At C2 the slice stream crosses kilometres, and the Leaf keeps its silicon. `[HYPOTHESIS]`

| What the large Core antenna does not buy | The reason |
|---|---|
| more Wi-Fi downlink | BTK and ETSI cap the Core EIRP, so a bigger antenna adds no power |
| a better Leaf uplink | the Leaf uplink under SAR limits the link before the downlink does |
| a long link through a wall or a hand | the Leaf antenna efficiency drops near a body |

**So C2 means 5G on licensed spectrum.** That is an operator site and not a box that a user owns. `[HYPOTHESIS]`

**The faults the far link found in the Leaf**. `hw/rf` gives the A1 efficiency as `-9.7 dB` by moments and `-15.3 dB` by the line model. The gate says `-2.5 dB`. The bandwidth is `5 MHz`. That cuts the 5G uplink range by `33 %`. The 5G antennas A5 and A6 are not in L.6.0 and set every 5G range. A signed input batch of `3.4 kB` breaks the `30 ms` gate at the cell edge: `72 ms` at `1 km` on `700 MHz`. Gaps G-52 and G-53. `[HYPOTHESIS]`

### 23.6.1 The two hosts law

**The law**. Power does not travel kilometres. At C2 the energy host is local, and the compute host is remote. The Host Life Law of Part 22 governs the energy host only. `[DECISION]`

| The class | The energy host | The compute host |
|---|---|---|
| C0 | the Core, through the tether | the same Core |
| C1 | the Core by cable, or a cell in a cordless Skin | the room Core |
| C2 | the Leaf cell, or a near host of Part 22 | the validator at the radio |



### 23.6.2 The fleet: how many Leafs one Core serves

The fleet seat built a capacity model, a two hosts model, an economics model and a roaming simulation. `[TREE]` `hw/core/fleet/`.

| The result | The value |
|---|---|
| a C2 sector at `1 km` | `249` delta sessions, `44` video sessions, or `1 074` registered Leafs. The radio binds |
| a C2 sector at `2 km` | `76` delta sessions, `5` video sessions and `133` registered Leafs |
| a site of `3` sectors | `3 222` registered Leafs |
| a C1 room | `28` registered Leafs and `5` delta sessions. The encoder binds |
| a C0 dock | `1` Leaf, the pad |
| the reach of a delta session under SAR | `2.0 km` under the ruling and `1.2 km` with the wallet in the Leaf |
| the reach of video, and of a live camera stream | `1.3 km` and `0.3 km` |
| the cost at scale | about `58 USD` per registered Leaf and year, from a `187 k USD` site |
| below about `490 000` Leafs in a `400 km²` metro | coverage sets the cost |

| The roaming day | The value |
|---|---|
| time on C0, C1 and C2 | `7.2 h`, `8.8 h` and `8.0 h` |
| C2 hand-overs and class changes per Leaf and day | `17.6` and `7.8` |
| hand-overs of a vehicle | `25` an hour |
| Leaf draw at C2 on delta, `1 km` | `2.43 W`, against `2.19 W` on Wi-Fi |
| a Leaf with the full cell at C2 | `3.0 h` |
| a Leaf with the Buffer cell at C2 | `31 min` |
| far-field power at `0.5 m` | `254` times short of the need |

`[HYPOTHESIS]` The fleet seat used its own link budget. The far seat's budget is the one to use.

**What the fleet says against the Split**. The kilometre Core exists only as a slice stream, so at C2 no Skin exists and no Leaf silicon is saved. Pixel Skins reach `2` per dock and `1.4` to `2.8` per room. Moving image processing to the Core puts the camera stream on the uplink, and the camera encoder must stay. The Core moves the watts and does not remove them: a site draws `6.3 W` per live delta session, and the Leaf draws `2.2 W`. One site is one event. It holds `3 222` wallet signers and is dark `168 min` a year. `[HYPOTHESIS]`

**The unique join, tested**. The fleet model supports the many-Leafs-per-Core idea at C2 with numbers. It weakens the many-Skins-per-Core idea at C0 and C1, because the pad, the encoder and the room radio limit it. `[HYPOTHESIS]`

---

## 23.7 The trust of the Split

The trust seat built a model of pairing, link keys, revocation and the signing rule. `[TREE]` `hw/core/trust/`, `81` tests pass.

**The worst hole: the lying Skin.** It paints a false summary and forges a tap on "sign". No cryptography can tell a forged tap from a real one. The model closes it by taking authority away from the Skin. `[HYPOTHESIS]`

| The rule | The meaning |
|---|---|
| a tap never confirms a key operation | a key operation needs a press that does not cross the Skin |
| a tap confirms a value only up to a blind budget per day | `100` forged taps against a budget of `100` sign exactly `10` |
| the press that does not cross the Skin | at C0 the Core button and display, at C1 a confirmation device, at C2 the Leaf local floor |
| a hardened identity element on every Skin | an unhardened chip leaks its identity key and gives a clone |
| a Core wallet, one account, capped device keys | a mixed fleet needs one account with caps |

| The finding | The value |
|---|---|
| link cost at `12.3 Gbit/s` | `31.3 KiB` buffer, `20.8 µs`, `12.3 mW` at `1 pJ/bit` and `61.5 mW` at `5 pJ/bit` |
| the same link at C2 | `0.15 mW` |
| the SW-24 distance margin | hides `100 km` of fibre one way |
| room class UWB | open to a published distance reduction attack |

`[HYPOTHESIS]` The pJ per bit figures are a sweep and not a measurement.

**Is a stolen Skin worth a piece of glass?** For the money, yes: the Skin holds no wallet key and no session key at rest. It is false in three cases: an unhardened identity chip, resale of a Skin that stays paired, and a Skin that is modified. A stolen Core loses everything, and a stolen Leaf at C2 is not glass. `[HYPOTHESIS]`

**What narrows the Split here**. The big surface leaves the signing path. C1 needs a confirmation device that no file specifies. A paired hostile Skin reads every private pixel it is given. The key concentrates in one Core. A validator Core clashes with the Zero-CPU definition. Gaps G-50 and G-54. `[HYPOTHESIS]`

---

## 23.8 The session of the Split

The session seat extended the model to many Skins on one Core. `[TREE]` `hw/core/session/`, `133` tests pass.

| The result | The value |
|---|---|
| a Skin roams to a standby vehicle Core | first pixel `156 ms`, live frame `0.30 s` on a cable and `0.41 s` over `60 GHz` |
| the same with a cold modem | `2.14 s` |
| a TakeOver cuts a roam where Core A has died | from `1.12 s` to `0.30 s` |
| a Skin on a link loss | a ROM screen at `15 ms`, and back `105` to `156 ms` after the link returns |
| a Leaf from C0 to C2, asleep | `509` frames lost |
| a Leaf from C0 to C2, awake | `21` frames lost, and `0` seen with a hot shadow |
| a Leaf back to a Core | `203 ms` on a cable |

| The finding | The value |
|---|---|
| `3` Skins on one Core, the chance that no screen works | `50` times that of `3` Leafs |
| dark screen minutes a year | equal at `45`, and `920` on `60 GHz` |
| a `60 GHz` Skin with `72 J` | cannot attach after an hour of carry |
| the blast radius at C2 | about `100` users per Core |

`[HYPOTHESIS]` The failure rates and the users per Core are guesses.

**What narrows the Split here**. A Skin cannot carry a lit session, so the zero-frame handover is lost for a roaming Skin. The Core is a single point at C0 and C1. At C2 the single point moves to the replica count. A TakeOver lets a stolen Core with a live grant take a session, and the trust seat marks it as a conflict. The pairing record puts a pseudonymous Skin id on chain. Gaps G-54. `[HYPOTHESIS]`

---

## 23.9 The cost

| The result | The value |
|---|---|
| a Skin | `1 331 USD` against `1 575 USD` for the all-in-one Leaf, so `15 %` less |
| a wired Core for `1`, `4` and `8` Skins | `154`, `195` and `250 USD` |
| the system saving at `4` Skins | `559 USD`, which is `8.9 %` |
| the system saving at `8` Skins | `1 264 USD`, which is `10 %` |
| the break-even | `2` Skins on one Core |
| a wired Skin | about even at one Skin, `+30 USD` at the base case |
| the micro-LED tile share of the unit | `76 %`, with `P10` at `67 %` and `P90` at `83 %` |
| the BOM that leaves the Leaf | `12.1 %` at C0, `9.5 %` at `60 GHz`, `9.0 %` at C1, `0 %` at C2 |

`[HYPOTHESIS]` `hw/core/study/`. The Core cell, the link chips, the radio power and the `25` to `70 M USD` of extra NRE are ranges and not quotes. The royalty base moves the `4` Skin saving by about `210 USD`.

**What it means for the aim**. The tile cost has no effect on the saving, and the tile is the cost. The cost aim is met only in part, at C0 and C1. The weight aim and the many-screens aim are met. `[HYPOTHESIS]`

---

## 23.10 The search for an unlimited battery

Ayaz asked for an invention: the battery can sit in the Leaf if it is very small, and the whole event lives in the hardware. The Lead tested each door that physics offers. The notebook is `hw/core/invent/LAB-NOTEBOOK.md`, and `explore.py` holds the probes. `[TREE]`

### 23.10.1 The failures

| The direction | The result | The verdict |
|---|---|---|
| far-field radio power | `26` to `64 mW` at the public cap of `10 W/m²`, against `0.95 W` | fails by `15` to `40` times |
| radio from a legal Wi-Fi source | `1.2 mW` at `1 m`, `0.14 mW` at `3 m` | fails |
| magnetic power across a room | a `150 mm` pad gives `49 %` at `1 cm`, `7 %` at `10 cm`, `0.04 %` at `30 cm` | fails beyond about `10 cm` |
| current through the body | `24` to `96 mW` at SELV and touch limits | fails |
| energy from the stretch | `0.09` to `0.53 Wh` over the whole hinge life | fails: the cycle life is the limit |
| one beam for power and pixels | the best converter carries `3.8 Gbit/s` against `13.1` | fails for the pixels |
| the passive Sheet lit by the Core | `12.6 lm` suffices, but a diffuse sheet gets `127` to `25 465` nits of ambient and a laser scan needs `81` to `325 kHz` | fails for a handheld Leaf |

### 23.10.2 What survived

| The direction | The result | The verdict |
|---|---|---|
| light on a back panel | `0.8`, `2.4` and `8.1 mW` at `100`, `300` and `1000 lux` | survives for the heartbeat if the back faces the light |
| the face as a photodiode | `18` to `182 µW` at an unmeasured `1 %` | open |
| heat of the pocket | `1.3 mW` from a recalled `20 µW/cm²` | survives for the heartbeat |
| the near-field tap | `15` to `40 mJ`, enough for one signature or a badge | survives |
| the infrared beam for power | passes at a converter of `35` to `62 %`, record `68.9 %` | survives, but the geometry blocks it |
| the Paper layer | a partial update every `11` to `53 s` on `8 mW` of light | survives |
| the heartbeat floor | `9.6` to `42 µW` against `61 mW` today | survives |

### 23.10.3 The three laws that come out of it

**The geometry law**. Energy comes from below and information goes up. The Leaf rests on its back, and its face looks at the user. A lamp or a beam sees the face. A micro-LED face is a poor solar panel. `[HYPOTHESIS]`

**The tiny cell law**. A tiny cell covers everything except the bright active hour. `[HYPOTHESIS]`

| The day away from any host | The B cell of `0.144 Wh` lasts |
|---|---|
| heartbeat and `100` partial Paper updates | `40` to `53` days |
| heartbeat and `300` updates of a third of a face | `3.6` days |
| `100` updates and `5` min of delta session | `1.6` days |
| `100` updates and `15` min of delta session | `0.5` day |

**The Heartbeat Law**. The Leaf is alive at microwatts, visible at millijoules and bright only where a host stands. `[DECISION]`

| The zone | The energy | The Leaf shows |
|---|---|---|
| **Heartbeat** | microwatts, always | nothing, but it listens and it signs on a tap |
| **Paper** | millijoules per update | a held image, text, a map, a balance |
| **Light** | watts, from a host | the full micro-LED surface |

### 23.10.4 Where the host stands

| The place | The host |
|---|---|
| a desk, a table, a car console, a stand | the surface under the Leaf |
| a hand, a street, a train | a worn Core with a thin breakaway cable |
| a pocket, a bag | the heartbeat and the tap |
| a room with a lamp | light on the face, for the heartbeat only |

**The honest answer to "unlimited"**. The battery is unlimited in the places where a host stands. It is not unlimited in a held hand in the open air. No tested physics carries watts to a held Leaf without a wire. The wire is the answer for that zone, and tethered glasses already use it. `[DECISION]`

---

## 23.11 The Paper layer and the freed cell layer

When the cells leave the Skin, each tile frees a layer of `0.90 mm`. The Lead proposes to put a bistable reflective layer there. `[DECISION]` as a candidate for Ayaz.

| The property | The value |
|---|---|
| the energy of a full update at `128 cm²` | `0.25` to `1.26 J`, from a `7.6 cm²` panel at `15` to `75 mJ` |
| a partial update | a third of that |
| the hold | `0 W` |
| a tap of `15` to `40 mJ` | a badge, `1` to `16 %` of a face |
| outdoors | the layer gains contrast with the sun, where the emissive layer needs `4.24 W` for `800 nits` |

**The sun and host law**. The two layers follow opposite light. Hosts stand indoors and in vehicles, where the emissive layer runs. The sun stands outdoors, where the reflective layer reads at no energy. `[HYPOTHESIS]`

**What it costs**. The stack changes. The sparse micro-LED must sit over a reflective layer. A reflective layer has less colour and less density than `508 ppi`. Prior art exists for two screens in one phone and for transflective layers. Gate CSK-7. `[HYPOTHESIS]`

---

## 23.12 The prior art and the claims

The study seat listed `25` rows, each with a URL. Several pages did not load. `[PUBLICATION]` `hw/core/study/PRIOR-ART.md`.

| The row | What exists |
|---|---|
| compute packs and pucks | Magic Leap, Meta Orion, XREAL Beam, Apple Vision Pro battery |
| wireless pixel links | Vive, LG M3, AR2 |
| one-box panels | LG M3, Samsung One Connect |
| a large far antenna for a small device | Starlink Direct to Cell |
| radio, light and coil power | Wi-Charge, power beacons, Qi furniture |
| near-field powered e-paper | small tags and badges |
| head-mounted projection on a retroreflective sheet | studied for years, and castAR did not ship |

**The verdict**. The Split is not new. The Heartbeat Law is not searched yet. The open join has five parts. They are a wallet Core, many zero-key Skins and a Skin that roams with its session. The other two are a Paper layer in the freed cell layer and a host-only bright mode. `[HYPOTHESIS]`

| The sentence | The verdict |
|---|---|
| the strong one: *the first screen with unlimited battery* | do not use. "First" fails, and "unlimited" is false in a held hand |
| the defensible one | use at the Designed tier |
| the safe one | use in public text until a prototype passes |

> On a host, a Budlum Leaf lives as long as the host feeds it. Away from a host, it stays alive for months on a very small cell, and it shows a held image at no energy.

**The rule for the word "first"**. The word stays out until gates CSK-1 and CSK-29 pass. `[DECISION]`

---

## 23.13 The recommended configuration

| The decision | The ruling | The reason |
|---|---|---|
| D-16 the Rule of Necessity | the camera part keeps what physics forces. The Core holds all else | the order of Ayaz, and `1.28 g` of silicon is all that physics lets leave at C0 |
| D-17 the first Skin | wired, with the `12` leaves and a `0.3 m` flex clip, at C0 and C1 | the cordless Skin returns the cell and fails the heat |
| D-18 the cordless Skin | refused | `3.35 W` at `60 GHz` against `1.73 W` |
| D-19 the Leaf at C2 | unchanged | nothing leaves the Leaf at C2 |
| D-20 the cell | the `0.144 Wh` B cell is the tiny cell, and the `128` body cells leave at C0 | the Heartbeat Law and the tiny cell law |
| D-21 the Paper layer | a candidate in the freed `0.90 mm` | the layer is free and the heartbeat needs a face |
| D-22 the signing rule | a tap never confirms a key operation | no cryptography tells a forged tap |
| D-23 the Skin identity | a hardened element on every Skin | an unhardened chip clones |
| D-24 the claim | the defensible sentence, with no "first" | Section 23.12 |
| D-25 the product line | the L.6.0 Leaf stays the product, and the Split is a second line for desks, rooms and vehicles | C2 gives the Split nothing |

`[DECISION]` of the Program Lead, as candidates under the orders of 2026-10-19. Ayaz can reverse any row.

---

## 23.14 What this part found wrong in earlier text

| Where | The fault | The fix |
|---|---|---|
| the first brief of `hw/core` | the `6:1` compression is outside the published range | `5:1` at most, and `7.4 Gbit/s` |
| the first brief of `hw/core` | the surface loads of `0.80` and `1.35 W` leave out the tile hubs | gap G-49 |
| `HARDWARE/03`, `HARDWARE/17` and Part 22 | the `68 g` and `88 g` figures are L.5.0 numbers | the L.6.0 Leaf is `51.5 g` bottom up |
| `FINAL/21` Section 21.2.7 | a `0.24 mm` margin and a `0.04 mm` margin in one part | the Bare store needs the cell layer number, not either margin |
| Part 21, the link claim | the `6:1` figure and two coverage figures of `61` and `47.5 %` have no owner | an owner in the next revision |
| `hw/rf` and the L.6.0 radio | A1 efficiency of `-9.7` to `-15.3 dB` against the `-2.5 dB` gate | gap G-52 |
| `hw/rf` and the L.6.0 radio | A5 and A6, the 5G antennas, are not in L.6.0 | gap G-52 |
| `0.054 W/kg` SAR | no reference power in any file | gap G-52 |
| `hw/energy` and `sim/thermal` | the 5G outdoor load reads `6.66 W` in one and `4.18 W` in the other | one load map for both |
| the ring stack | `3.90 + 0.30 mm` against `4.00 mm` does not close from the files | a CAD check |

---

## 23.15 The research order for the Budlum tree

| Order | The work | The acceptance test |
|---|---|---|
| **RG-20** | Skin pairing, TakeOver and roaming: rules R12 to R17, a Skin id, a pairing record and a view id on chain | a Skin pairs, roams to a second Core and keeps the state root. A cloned or revoked Skin is refused. A forged tap never signs a key |

The draft is `hw/core/session/RG-19A-skins.md`, with `proto/skin_chain.proto` at wire `1.2` and `proto/skin_link.proto`. The seat ran `133` tests. `buf lint` has not run. `[TREE]`

---

## 23.16 The new gates

The seats proposed many gates under nine prefixes. The Lead merged them into one series. The source gates stay in the seat files.

| Gate | The test | The pass condition |
|---|---|---|
| **CSK-1** | a professional prior art search and a patent opinion for the Split and the Heartbeat Law | a dated report and a signed opinion on the exact sentence |
| **CSK-2** | a legal opinion on the class of a Skin and a Core under 2023/1670, Article 11 and the royalty base | each question answered in writing |
| **CSK-3** | the wired Skin link: a `10 Gbit/s` eye on the spring leaf, and visually lossless compression at `508 ppi` | the eye opens at the leaf, and a panel of viewers sees no loss at `5:1` |
| **CSK-4** | the Skin load with the tile hubs, delta, video and full motion | the load at or under the `2.93 W` heat limit, and the number recorded per domain |
| **CSK-5** | the Skin heat at `25`, `30` and `35 °C`, with the PHY spread across the tiles | the hottest face point at or under `36.2 °C` to `30 °C` at C0 and `25 °C` at C1 |
| **CSK-6** | the idle floor of the secure element, the wake-up path and the power chip, measured | the sum at or under `50 µW` |
| **CSK-7** | a Paper layer in the cell layer of one tile, with its update energy at `128 cm²` | the update energy recorded, and an update fed by `8 mW` of light |
| **CSK-8** | the back panel on a desk, in a hand and on a stand, and the micro-LED as a photodiode | the harvested power recorded per pose, and the geometry law confirmed or voided |
| **CSK-9** | the Core box heat at `25` and `35 °C`, passive and with a fan | the surface temperature under the touch limit for the stated Skin count |
| **CSK-10** | the Core energy and the host class for `1`, `4` and `8` Skins | each host class carries its Skins at the peak, and the table is within `10 %` |
| **CSK-11** | the Core cell at the peak of `8` Skins | the cell holds `3.4 V` at the peak, or the Core states a limit |
| **CSK-12** | the hardened identity element of a Skin | the chip resists key extraction in a lab test |
| **CSK-13** | pairing, link keying and revocation | a cloned, replayed or revoked Skin is refused |
| **CSK-14** | the signing rule: `100` forged taps against a blind budget of `100` | exactly `10` sign, and no key operation signs |
| **CSK-15** | pixel confidentiality: a paired hostile Skin and an end-to-end cipher at C2 | the private pixel is not readable outside the trust boundary |
| **CSK-16** | a mixed fleet with one account and capped device keys, and a stolen Core with a live grant | no session is taken after a revoke, and the cap holds |
| **CSK-17** | a Skin roams between two Cores, cable and `60 GHz` | the first pixel under `200 ms`, and the live frame under `0.5 s` |
| **CSK-18** | a Skin link loss | a ROM screen within `20 ms`, and a return within `200 ms` after the link |
| **CSK-19** | a Core failure, with replicas, for `1` to `8` Skins | the joint dark time is stated, and a second Core takes over |
| **CSK-20** | the far link: the slice stream at `500 m`, `1`, `3` and `5 km`, and the A1 efficiency | the rate holds at the stated distance, and A1 meets `-2.5 dB` or the range is restated |
| **CSK-21** | the `30 ms` budget at the cell edge with a signed `3.4 kB` batch | `p99` under `30 ms`, or the batch is compressed |
| **CSK-22** | the Core EIRP under BTK and ETSI, and a 5G licence at C2 | the Core class is stated for each band |
| **CSK-23** | the ring packing at C0 | all parts placed and the packer result reproducible |
| **CSK-24** | quotations for the Core cell, the link chips and the radio | each cost range replaced by a quote |
| **CSK-25** | the fleet capacity of one Core at C0, C1 and C2 | the Leafs per Core measured against the model |
| **CSK-26** | the two hosts test: a Leaf at C2 with a near host and with only its cell | the energy per hour is within `10 %` of the table |
| **CSK-27** | the near-field tap: one signature and one badge | both complete within one tap on a dead Leaf |
| **CSK-28** | the day away from a host with the B cell | the days match the table within `20 %` |
| **CSK-29** | the claim check against PRG-6 | each public sentence maps to a gate record or to a study |

---

## 23.17 What this part leaves open, and the new gaps

**The new gaps**. The gap register of Part 16 carries them as G-49 to G-54.

| The gap | The item |
|---|---|
| **G-49** | the tile hub load and the Skin power budget |
| **G-50** | what you see is what you sign: the confirmation device at C1 and the trusted amount on a Skin |
| **G-51** | the `10 Gbit/s` spring leaf eye and visually lossless compression at `508 ppi` |
| **G-52** | the Leaf radio: A1 efficiency, the 5G antennas A5 and A6, and the SAR reference power |
| **G-53** | the Core as a product: the box heat, the cell and the legal class |
| **G-54** | the pairing registry on chain, the per key caps and the TakeOver conflict |

---

## 23.18 Where the work lives, and the next moves

| The seat | The directory | The tests |
|---|---|---|
| link | `hw/core/link/` | `linkmodel.py`, `15` of `19` model checks pass, and the failures are the damage |
| power | `hw/core/power/` | `run_all.py` |
| heat | `hw/core/heat/` | `run_all.py` reproduces `41.3 °C` |
| trust | `hw/core/trust/` | `81` tests |
| session | `hw/core/session/` | `133` tests |
| study | `hw/core/study/` | `cost.py` and `25` listed rows |
| far | `hw/core/far/` | `farlink.py` |
| parts | `hw/core/parts/` | `parts.py`, `84` cited rows |
| fleet | `hw/core/fleet/` | `fleet.py` |
| the Lead | `hw/core/invent/` | `explore.py` |

**The next moves**.

1. Measure the idle floor and the tap path of the `U7`. This decides the Heartbeat Law.
2. Build one tile with a Paper layer in the cell layer.
3. Build the wired Skin on the `12` leaves with a `0.3 m` flex clip, and run CSK-3 and CSK-5.
4. Fix the A1 antenna and add A5 and A6, because the far Core depends on them.
5. Close G-50: design the press that does not cross the Skin.
6. Order the prior art search for the Split and the Heartbeat Law.
