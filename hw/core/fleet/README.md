# BUDLUM LEAF · CORE AND SKIN · FLEET SEAT · BLOCK HP-3

**Revision L.7 candidate · 2026-10-19 · seat FLEET**. This is a study. It changes no L.6.0 or L.6.1 decision until Ayaz rules. Every number is `[HYPOTHESIS]` unless a tag says otherwise. The brief is `hw/core/BRIEF.md`, Sections 5 and 8.

## 0 · The damage report: what narrows the Split at the fleet level

Honesty comes first. The fleet numbers do not kill the Split. They narrow it in nine places.

| No. | What narrows | The number | Where it comes from |
|---|---|---|---|
| 1 | The kilometre Core exists only as a slice stream. At C2 the Leaf keeps its decoder, frame store, compositor, radio and cell. There is no Skin at C2 | the pixel link of `6.1` to `12.3 Gbit/s` has no path at C2 | BRIEF Section 8.2, `fleet.py` section 7 |
| 2 | "One hardware, many screens" fails for pixel Skins | `2` Skins per dock on two tethers. `1.4` to `2.8` Skins per room Core on `60 GHz` | `fleet.py` section 7 |
| 3 | At C2 the Core adds cost per Leaf. It saves no Leaf silicon | about `USD 58` per Leaf and year at scale, over a Leaf at `USD 394` per year | `econ.py` sections 2 and 5 |
| 4 | The SAR uplink sets the range, and the signatures set the uplink. The wallet in the Leaf sends `681 kbit/s` at delta | reach `1.2 km` with the wallet in the Leaf, `2.0 km` under the ruling | `fleet.py` section 3 |
| 5 | Image processing in the Core puts the camera stream on the uplink | `37.5 Mbit/s` up. Live reach `0.3 km`. A photograph takes `36 s` at `1 km` and `198 s` at `2 km` | `fleet.py` section 3, `twohosts.py` section 7 |
| 6 | The range of a large antenna is power limited, not layer limited | `4` times the elements give `1.7` times the video sessions | `fleet.py` section 4b |
| 7 | The Core moves the watts and does not remove them | a site draws `6.3 W` per live delta session. The Leaf draws `2.2 W` | `econ.py` section 7 |
| 8 | One site is one event. It holds `3 222` registered Leafs and, under the ruling, their wallet signers | `168 min` dark per year for one site on a fair grid. Two sites on two feeders cost twice | `econ.py` section 7 |
| 9 | The energy host in the Core works at C0 only. Power does not travel | a far-field host gives `8.6 mW` at `0.5 m` against `2.2 W` needed: `254` times short | `twohosts.py` section 6 |

**What survives**. The slice stream scales. One site carries `133` to `3 222` registered Leafs by radius. A site settles `757` receipts per second as one transaction per slot. Sections 7 and 8 list what the fleet model supports and what it weakens.

## 1 · The ruling of Ayaz, applied

Ayaz ruled on 2026-10-19: what is needed stays in the part that holds the camera hardware, the B module. Everything else lives in the Core. The model uses this split and does not reopen it.

| Where | What sits there |
|---|---|
| The B module | the camera, the transducers, the antennas, the radio front end. At C1 and C2 also the link PHY, slice decoder, frame store, compositor and a hardened identity element |
| The Core | the wallet signer, the session, the AI, the image processing, the validator role, the energy host |

**What changed in the models**.

1. The Core signs each input batch and each receipt. No wallet signature crosses the radio.
2. The identity element attests once per second with an `ML-DSA-44` signature of `2 420 B`. A pairing MAC covers each input batch.
3. The authority load of the B module falls from `0.12` to `0.07 W` in a session. `[HYPOTHESIS]`
4. The camera stream goes up the link, because the image processing is in the Core. The model has a camera session of `37.5 Mbit/s` up.
5. The Core carries a signer. One signer holds `4 000` signatures per second. At the peak mix this serves `1 882` registered Leafs.

**One consequence of the same rule**. The ruling puts the energy host in the Core. Power does not travel kilometres. By the rule of necessity the cell or a near host stays on the Leaf at C1 and C2. The Core feeds the Leaf at C0 only. Section 4 gives the arithmetic.

## 2 · The files and how to run

| File | Content |
|---|---|
| `fleet.py` | the capacity model: radio, compute, memory and network. Sweeps, tiers, the Skin contrast, the Monte Carlo |
| `twohosts.py` | the Two Hosts Law numbers: radio duty, Leaf load, run time, heat, near host, photograph, far-field energy |
| `econ.py` | the cost of a site, the cost per Leaf, unit costs for SW-19, failure, power, replicas, receipts |
| `roam.py` | the roaming fleet: a simulated day of `1 500` Leafs in a city of `20 x 20 km` |
| `run_all.py` | runs the four in order. About `3` minutes |
| `out/` | `fleet.txt`, `twohosts.txt`, `econ.txt`, `roam.txt` and a `.json` of each |

1. Run `python3 hw/core/fleet/run_all.py`. It needs Python 3 and numpy. It writes only to `out/`.
2. Run `python3 hw/core/fleet/fleet.py --quick` for a smoke test of `25 s`.
3. Read `out/fleet.txt` first. Every table of this README is a cut of an `out/` file.

**Reads, all read only**. `hw/dock/validator_sizing.py` and its bench result, `hw/dock/budget.py` data, `validator/leaf-duty`, `net/discovery`, `sim/latency`, `program/budget.py`, `hw/energy/out/budget.json`, `hw/hostpower/powerpath/hosts.py`, `hw/hostpower/continuity` numbers.

**The naming trap**. This file calls the distance classes C0, C1 and C2, as the brief does. The link classes C0 to C4 of `FINAL/05` Section 5.4 are not used. The session kinds are called idle, delta and video.

## 3 · Question 1: Leafs per Core

### 3.1 What one session costs

| Session | Down | Up, ruled | Up, wallet in the Leaf | Hash | Encode |
|---|---|---|---|---|---|
| idle | `0.003 Mbit/s` | `2.5 kbit/s` | `6.5 kbit/s` | none | none |
| delta | `2.0 Mbit/s` | `52 kbit/s` | `681 kbit/s` | `0.68 GB/s` | `161 Mpix/s` |
| video | `30.3 Mbit/s` | `471 kbit/s` | `570 kbit/s` | `1.43 GB/s` | `307 Mpix/s` |
| camera | `2.7 Mbit/s` | `37.6 Mbit/s` | not modelled | `0.36 GB/s` | `77 Mpix/s` |

**The sources**. The stream rates are from `FINAL/05` Section 5.4. The header and signature sizes are from `validator/leaf-duty` and FIPS 204 `[PUBLICATION]`. The frame cost is the bench of `hw/dock`: `48.9 ms` of raster and `45.0 ms` of SHA-256 per full frame on one reference core. Only the dirty slices are rendered and hashed. The dirty share is `0.35` for delta and `1.0` for video. `[HYPOTHESIS]`

**The video uplink is the ACK stream**. `1.5 %` of `30 Mbit/s` is `450 kbit/s`. A lean ACK of `0.3 %` lifts the video reach from `1.27` to `1.75 km`.

### 3.2 The answer at the three distance classes

The base case. C2 is one sector of `256` elements at `100 W`, `3.5 GHz` and `100 MHz` TDD. The Leafs sit in a disc of `2 km` with `8 dB` of wall or vehicle loss. C1 and C0 use the build of `hw/dock`: an AGX Orin or an Orin NX with a `KU15P` frame engine.

| Class | Activity | Leafs per Core | Binds | Radio | Compute | Memory and network |
|---|---|---|---|---|---|---|
| C0 dock | delta | `1` | the pad | `1` pad | `2.5` | `45` |
| C0 dock | video | `1` | the pad | `1` pad | `1.3` | `28` |
| C1 room | idle | `256` | radio, the association table | `256` | `4 000` | `3 520` |
| C1 room | delta | `5.0` | compute, the encoder | `66` | `5.0` | `163` |
| C1 room | video | `2.6` | compute, the encoder | `13` | `2.6` | `28` |
| C1 room | peak mix | `28` | compute, the encoder | `238` | `28` | `820` |
| C2 site | idle | `8 000` | radio, the connected table | `8 000` | `16 000` | `162 240` |
| C2 site | delta | `76` | radio, the downlink | `76` | `79` | `7 530` |
| C2 site | video | `5.0` | radio, the downlink | `5.0` | `41.5` | `1 277` |
| C2 site | peak mix | `133` | radio, the downlink | `133` | `446` | `35 783` |

**The peak mix** is `85 %` idle, `12 %` delta and `3 %` video of the registered Leafs. It follows the `15 %` session peak of `net/discovery/density.py`. One number then counts registered Leafs.

**The three results**.

1. **C2 is a radio limit**. The downlink binds at `2 km`. At `1 km` the grants bind. A sector holds `249` delta or `44` video sessions, or `1 074` registered Leafs.
2. **C1 and C0 are an encoder limit**. The dock-class SoC encodes `500` to `1 000 Mpix/s`. One `MA35D` card `[PUBLICATION]` adds `3 981 Mpix/s`. With it a room Core serves `25` delta, `13` video and `139` registered Leafs.
3. **Memory and network never bind**. RAM, NIC and backhaul sit at least `10` times above the radio or the encoder.

### 3.3 The radius at C2

| Radius | Delta, radio only | Video, radio only | Covered, delta and video | The model |
|---|---|---|---|---|
| `0.5 km` | `249` | `84` | `100 %` and `100 %` | UMa, city |
| `1 km` | `249` | `44` | `100 %` and `100 %` | UMa, city |
| `2 km` | `76` | `5.0` | `98 %` and `41 %` | UMa, city |
| `3 km` | `14.5` | `0.96` | `45 %` and `18 %` | UMa, city |
| `3 km` | `244` | `16` | `100 %` and `72 %` | RMa, open country |
| `5 km` | `28` | `1.8` | `63 %` and `27 %` | RMa, open country |

**The reading**. Capacity falls by `9` times from `1` to `2 km` for video. Past `2 km` in a city the Core serves a few Leafs, and most of the disc has no link. The `Covered` column is the share of the disc with a link. The Leafs counted are those in that share.

### 3.4 The reach under SAR

The reach is the largest distance where a Leaf at `20 dBm` keeps a downlink and an uplink with `10 %` outage. It is a radio result with the sector empty. The far seat owns the link budget proper.

| Case | Downlink | Uplink | Reach |
|---|---|---|---|
| delta, ruled split, city, `8 dB` | `2.70 km` | `2.02 km` | `2.02 km` |
| delta, wallet in the Leaf, key inline | `2.70 km` | `1.16 km` | `1.16 km` |
| video, ruled split, ACK `1.5 %` | `2.70 km` | `1.27 km` | `1.27 km` |
| video, ruled split, ACK `0.3 %` | `2.70 km` | `1.75 km` | `1.75 km` |
| delta, ruled, outdoors `0 dB`, city | `4.32 km` | `3.24 km` | `3.24 km` |
| delta, ruled, indoors `15 dB`, city | `1.79 km` | `1.34 km` | `1.34 km` |
| delta, ruled, outdoors, open country | `8.60 km` | `6.42 km` | `6.42 km` |
| camera, ruled, live stream | `2.70 km` | `0.31 km` | `0.31 km` |

**Power, not layers, limits the range**. Past `1 km` the cell is noise limited. Spatial layers add little in that regime. A `4` times larger array lifts the video sessions at `1 km` by `1.7` times. The counts are `29`, `44`, `60` and `75` for `128`, `256`, `512` and `1 024` elements.

### 3.5 The compute side: where the walls stand

| Tier of the C2 box | Delta | Video | Full `240 Hz` worst case | What binds |
|---|---|---|---|---|
| render side, CPU only, `192` cores | `94` | `88` | `4.2` | DRAM traffic |
| render side, `4` FPGA frame engines | `267` | `197` | `12` | the engine LUTs |
| render side, `4` ASIC frame engines | `267` | `1 067` | `267` | the signer |
| the whole box with `4` MA35D encoders | `79` | `41.5` | `3.5` | the encoder |

**The dirty-slice rule removes the hash wall for sessions**. `hw/dock` found that no SoC serves two full `240 Hz` sessions with three renders per frame. That finding holds: the worst case column gives `4` sessions on `192` cores. A real delta session renders `0.35` of the slices at `30` frames per second. The box then serves `94` on the CPU alone. The encoder is the wall.

**The signer is a new limit**. Under the ruling the Core signs `11` times per second for a delta session. One signer of `4 000` signatures per second serves `267` delta sessions. `[HYPOTHESIS]`

### 3.6 The family

| Leaf | Pixels against Leaf 160 | Delta, compute side | Video, compute side | Video, radio side |
|---|---|---|---|---|
| Leaf 80 | `0.50` | `158` | `83` | `10` |
| Leaf 160 | `1.00` | `79` | `41.5` | `5.0` |
| Leaf 480 | `0.81` | `97` | `51` | `6.2` |

### 3.7 The Monte Carlo

`400` draws over every range of `fleet.py`. The design is held: array, boxes.

| Case | p10 | p50 | p90 | Binds in most draws |
|---|---|---|---|---|
| C2 delta | `11` | `34` | `111` | downlink `52 %`, encoder `43 %` |
| C2 video | `0.8` | `4.7` | `23` | downlink `98 %` |
| C2 peak mix, registered | `20` | `123` | `437` | downlink `77 %`, encoder `23 %` |
| C1 delta | `1.9` | `4.3` | `12` | the encoder |
| C1 peak mix, registered | `13` | `27` | `56` | the encoder |
| C0 | `1` | `1` | `1` | the pad |

## 4 · Question 2: The Two Hosts Law

### 4.1 The law

**The Two Hosts Law**. A Leaf has two hosts that need not stand in one place. The energy host feeds joules and pulls heat. The compute host feeds frames and holds the session, the wallet signer and the validator role. `[DECISION]` for the study.

1. **Energy travels metres. Frames travel kilometres**. The energy host is a contact, pad or tether at C0, a near host or the cell. It is never a C1 or C2 Core.
2. **The compute host is any Core in reach of the link**. It stands at C0, C1 or C2.
3. **The Host Life Law of Part 22 governs the energy host only**. The Leaf lives as long as its energy host feeds it, and as long as one compute host answers.
4. **A lost compute host does not end the life of the Leaf**. The B module shows the safe screen, the local scene and the compositor. The Leaf looks for another Core.
5. **Neither host gains authority**. The energy host never touches the wallet path or the data lanes (Part 22.8). The compute host never touches the energy path. The identity element attests what the Leaf showed.
6. **Two bridges, and neither needs the other**. The energy bridge is the Buffer store. The compute bridge is a shadow in another site.
7. **The class line names both hosts**. It states `power: dock, host or cell` and `compute: room, site or far`.

### 4.2 What "the Leaf lives as long as its host" means

| Class | Energy host | Compute host | The Host Life Law reads |
|---|---|---|---|
| C0 | the Core, by pads or tether | the same Core | as Part 22. One box is both hosts, so one failure takes both |
| C1 | a desk host, a pad, a dock or the cell | the room Core | the Leaf lives as long as the desk host feeds it. Leaving the room changes only the compute host |
| C2 | a near host (cradle, bank, dock) or the cell | the site Core | the Leaf lives as long as the near host or the cell. The site Core has no say in life |

**The failure at C0 is the dock pair**. A pair in one box makes the joint loss of power and primary validator `60` times more frequent `[TREE]` `hw/dock`. The shadow must stand in another power domain.

### 4.3 Why power does not travel

Take a far-field energy host at `915 MHz` and `36 dBm` EIRP `[PUBLICATION]` FCC 15.247, with a `50 %` rectifier. The table compares it with a delta session of `2.19 W`.

| Distance | Harvest | Short by |
|---|---|---|
| `0.5 m` | `8.6 mW` | `254` times |
| `2 m` | `0.54 mW` | `4 071` times |
| `5 m` | `0.086 mW` | `25 446` times |
| `30 m` | `2.4 uW` | `916 041` times |

Only contact or a pad at `0` to `2 m` closes. So the Core is the energy host at C0 and nowhere else.

### 4.4 The energy numbers of a Leaf at C2

The loads are those of `hw/energy/04`, with the authority domain cut by the ruling. The radio is a 5G modem. The near-cell figure is `0.60 W` for delta `[HYPOTHESIS]` and `1.10 W` for video `[TREE]`. The model adds the increment of the radio duty over a Leaf at `300 m`. The sector carries `2` layers. The Leaf sends at `20 dBm`.

| Case | Receive duty | Transmit duty | Radio | Leaf load | Full S cell | Buffer, 20 cells |
|---|---|---|---|---|---|---|
| C1, Wi-Fi, delta | none | none | `0.40 W` | `2.19 W` | `3.30 h` | `34 min` |
| C2, `0.3 km`, delta | `0.7 %` | `2 %` | `0.60 W` | `2.41 W` | `2.99 h` | `31 min` |
| C2, `1 km`, delta | `1.2 %` | `2 %` | `0.61 W` | `2.43 W` | `2.97 h` | `31 min` |
| C2, `2 km`, delta | `6.6 %` | `14 %` | `0.75 W` | `2.58 W` | `2.80 h` | `29 min` |
| C1, Wi-Fi, video | none | none | `0.60 W` | `3.59 W` | `2.01 h` | `21 min` |
| C2, `1 km`, video | `18 %` | `16 %` | `1.26 W` | `4.35 W` | `1.66 h` | `17 min` |

**The reading**.

1. **The long link costs little energy where it closes**. Delta costs `0.2` to `0.4 W` more than Wi-Fi, `11` to `18 %`. Video costs `0.8 W` more at `1 km`, `21 %`.
2. **The link fails before the energy matters**. Video has no uplink past `1.3 km`. The radio duty rises to `0.44` at `5 km` in open country.
3. **The heat does not change class**. Every C2 delta load is above the free-air limit of `1.73 W` and under the plate limit of `5.7 W`. The G-46 fault of Part 22.5 stands. A dock or a cradle holds it.
4. **The radio duty sweep**. Take receive duty `1.0` and transmit duty `0.2` at `20 dBm`. A delta session then draws `3.57 W` and Full S lasts `2.0 h`. See `out/twohosts.txt`, section 3.

### 4.5 The near host at C2

Host energy per hour of Leaf, delta at `1 km`, load `2.43 W` at the cells `[TREE]` `hosts.py`.

| Host | Host energy per hour | Run time of its store |
|---|---|---|
| H0 wall dock | `3.03 Wh` | mains |
| H1 dock pack, `20 Wh` | `3.06 Wh` | `6.5 h` |
| H2 desk USB-C PD | `2.84 Wh` | mains |
| H3 vehicle `12 V` | `2.84 Wh` | the vehicle |
| H5 worn bank, `18.5 Wh` | `2.90 Wh` | `6.1 h` |

### 4.6 What the Leaf needs when the two hosts are different places

| The need | The number | The source |
|---|---|---|
| a compute gap with the energy host alive and a shadow ready | `4` to `5` frames covered by U1. A cold start takes `133 ms` at p50, `152 ms` at p99 | `hw/dock` dockpair |
| a compute gap with no Core in reach | the safe screen in `15 ms`. The Leaf radio then finds a far validator at `93 ms` mean | `FINAL/21` 21.5.7 |
| an energy gap with the compute host alive | Buffer and Full lose `0` frames in `95 %` of draws on a `75 s` walk, `3` at p99 | Part 22.9.1 |
| both gaps at once, a cold cell site | the live frame after `0.48 s` warm, `2.4 s` cold, after the host pass | Part 22.9.1 |
| the energy bridge at far radio | `20` cells carry delta for `31 min` at `1 km` | `twohosts.py` |
| the peak at far radio | `54` of `128` cells for `3 C`, one more than at Wi-Fi | `twohosts.py`, `tiers.py` |
| its own radio | the PHY and front end stay in the B module: `0.60` to `1.26 W` | the ruling |
| a deferred class for the camera | a `12 MB` frame goes up in `36 s` at `1 km`, `198 s` at `2 km` | `twohosts.py` section 7 |
| an attestation per second | `2 420 B` up. The Core cannot forge it | gate HC-C4 |

## 5 · Question 3: The economics of a shared Core

All costs are `[HYPOTHESIS]` with a low, a base and a high value in `econ.py`. Spectrum and the validator stake are `UNKNOWN`. The base case excludes both. The price of a session is deferred by Ayaz (`FINAL/17` Section 17.14). This section gives costs, not prices.

### 5.1 The cost of a C2 site

Three sectors of `256` elements at `100 W`, one reference compute box, a `4 h` UPS.

| Line | Low | Base | High |
|---|---|---|---|
| arrays | `122 k` | `221 k` | `410 k` |
| the reference compute box | `51 k` | `80 k` | `131 k` |
| capex | `217 k` | `387 k` | `717 k` |
| annual cost | `77 k` | `158 k` | `443 k` |

**The sources**. The `MA35D` price of `USD 1 595` is `[PUBLICATION]`. The FPGA chip price of `USD 2 600` is `[TREE]` `hw/dock`. The array price per element has no public source. A `64T64R` AAU draws about `1 kW` `[PUBLICATION]`. The model gives `0.8 kW` per sector.

### 5.2 Registered Leafs per site and the cost per Leaf

The compute is right-sized. Each device type is bought on its own limit.

| Radius | Sectors | Leafs per site | Servers, engines, encoders, signers | USD per Leaf and year | USD per Leaf and month |
|---|---|---|---|---|---|
| `1 km` | `1` | `1 074` | `1, 3, 10, 1` | `107` | `9.0` |
| `1 km` | `3` | `3 222` | `1, 8, 29, 2` | `58` | `4.8` |
| `2 km` | `1` | `133` | `1, 1, 2, 1` | `798` | `66` |
| `2 km` | `3` | `398` | `1, 1, 4, 1` | `381` | `32` |

**The Monte Carlo of cost and capacity**. USD per Leaf and month at `1 km` with `3` sectors: p10 `4.9`, p50 `8.4`, p90 `80`. The tail is a high wall loss, which cuts the covered share.

### 5.3 The cost per Leaf by fleet size

A metro of `400 km2`. A site of `3` sectors at `1 km` covers `3.1 km2` and carries `3 222` registered Leafs.

| Leafs | Per km2 | R = 1: sites, USD per Leaf-month | R = 2: sites, USD per Leaf-month | Bound |
|---|---|---|---|---|
| `1 000` | `2.5` | `153`, `1 902` | `306`, `3 805` | coverage |
| `10 000` | `25` | `153`, `190` | `306`, `380` | coverage |
| `100 000` | `250` | `153`, `19.7` | `306`, `38` | coverage |
| `1 000 000` | `2 500` | `310`, `4.8` | `621`, `9.7` | capacity |
| `10 000 000` | `25 000` | `3 103`, `4.8` | `6 207`, `9.7` | capacity |

**The reading**. Below about `490 000` Leafs in the metro the area sets the cost. The shared Core pays only at the density of a city with real adoption.

### 5.4 The Core part per Leaf at each class

| Case | Core cost | Leafs | USD per Leaf and year |
|---|---|---|---|
| C0 dock Core, one Leaf | `3 600` | `1` | `950` |
| C0 dock Core, two pads | `3 600` | `2` | `475` |
| C1 room Core, one Leaf | `4 000` | `1` | `1 055` |
| C1 room Core, three Leafs | `4 000` | `3` | `352` |
| C1 room Core, six Leafs | `4 000` | `6` | `176` |
| C2 site, capacity bound | `457 818` | `3 222` | `58` |

**The Leaf unit cost** is `USD 1 575` at `1 M` a year, or `USD 394` per year over `4` years `[TREE]` `program/budget.py`. A room Core of one Leaf costs more than the Leaf. A shared site costs `15 %` of it.

### 5.5 The unit costs of gate SW-19

One site of `3` sectors at `1 km` with `1` server, `8` engines, `29` encoders and `2` signers. Annual cost `USD 186 513`.

| Function | USD per year | USD per delta session-hour at `25 %` use |
|---|---|---|
| array and radio | `62 949` | `0.039` |
| compute | `58 868` | `0.036` |
| site | `45 231` | `0.028` |
| backhaul | `15 000` | `0.009` |
| power | `4 466` | `0.003` |
| all, delta | `186 513` | `0.114` |
| all, video | `186 513` | `0.644` |

**The meter of H-15**. A delta session hour is `0.90 GB` down and a video hour `13.5 GB`. The cost at `25 %` use is `USD 0.127` per GB for delta and `0.048` for video. A `20 %` margin raises each by `25 %`.

### 5.6 The operator business case with the Core as the unit

1. **The unit of cost is the site**. It costs `USD 187 k` a year at scale and carries `3 222` registered Leafs.
2. **The unit of revenue is the session minute**. FINAL/21 pays coverage emission per served minute where the p99 is under `30 ms`. `net/discovery` holds the rule.
3. **Break-even at scale** is `USD 4.8` per registered Leaf and month. It is `USD 0.114` per delta session-hour at `25 %` use. Spectrum and stake are excluded.
4. **The receipts settle at the Core**. A site makes `757` receipts per second. Posted one by one they put `7.6 MB/s` on the chain. As one transaction per `6 s` slot they put `0.58 kB/s`. The ratio is `13 000` times.
5. **The price stays deferred**. The structure above gives a floor. It does not give a price.

### 5.7 The failure and the power of a site

**The power**. A site of `3` sectors with `3 222` registered Leafs draws `4.7 kW` peak and `3.3 kW` on average. That is `1.0 W` per registered Leaf and `6.3 W` per live delta session. The Leaf itself draws `2.2 W`.

**The failure**. The hardware fails `0.42` times a year and the site is dark `2.5 h` a year. Grid outages decide the rest.

| Grid | UPS `1 h` | UPS `4 h` | UPS `8 h` | UPS `24 h` |
|---|---|---|---|---|
| good, `0.5` a year, mean `1 h` | `0.2 h` dark | `0.0 h` | `0.0 h` | `0.0 h` |
| fair, `3` a year, mean `1.5 h` | `2.3 h` | `0.3 h` | `0.0 h` | `0.0 h` |
| poor, `12` a year, mean `3 h` | `25.8 h` | `9.5 h` | `2.5 h` | `0.0 h` |

**The replica count**. The share of time that one site is dark is `q`. It is `3.2e-4`, or `168 min` a year, on a fair grid with a `4 h` UPS.

| Sites in reach | Common cause | Dark minutes per year | Usable capacity per site | Cost against one site |
|---|---|---|---|---|
| `1` | none | `168` | `1.00` | `1.0` |
| `2` | `0.02` | `3.4` | `0.50` | `2.0` |
| `2` | `0.30` | `51` | `0.50` | `2.0` |
| `3` | `0.02` | `3.4` | `0.67` | `1.5` |

**The recommendation**. Put `2` sites in reach of every Leaf, on two feeders. Hold each at `50` to `60 %` of its sessions. Keep one spare compute device of each type. Fit a UPS of `4 h` on a fair grid and `8 h` on a poor one. Keep the shadow of a session in the other site. `[HYPOTHESIS]`

**What the Leaf sees**. The shadow takes over with `4` to `5` frames covered by U1. A cold start takes `133 ms`. With no Core in reach the Leaf drops to a far validator at `93 ms`: delta holds, video does not.

## 6 · Question 4: The roaming fleet

### 6.1 The simulation and its assumptions

`roam.py` moves `1 500` Leafs through a city of `20 x 20 km` for `24 h` in steps of `10 s`. C2 sites stand on a hexagonal grid with a sector radius of `1 km`. Room Cores stand at `60 %` of homes and desks. Docks stand at `50 %`.

The day runs: sleep, home, a `15 min` walk, a vehicle at `10 m/s`, a `10 min` walk, the desk. Then lunch, the desk, the way home and sleep. Times shift by `30 min` per Leaf. The activity mix is by segment. Paths are straight lines. Real paths add about `30 %` of the crossings. All of it is `[HYPOTHESIS]`.

### 6.2 The time on each class

| Deployment | C0 hours | C1 hours | C2 hours | From the cell, Wh per day | Hours above `1.73 W`, no plate |
|---|---|---|---|---|---|
| no room Core, no dock | `0.0` | `0.0` | `24.0` | `8.7` | `7.3` |
| docks only | `7.3` | `0.0` | `16.7` | `7.4` | `5.7` |
| base: `60 %` room, `50 %` dock | `7.2` | `8.8` | `8.0` | `7.2` | `5.7` |
| everyone has both | `14.3` | `7.7` | `1.9` | `5.8` | `4.2` |

### 6.3 The hand-over rate

| Measure | Value |
|---|---|
| C2 to C2 hand-overs, walking | `3.3` per hour |
| C2 to C2 hand-overs, in a vehicle | `25.1` per hour |
| C2 hand-overs per Leaf and day | `17.6` |
| class changes per Leaf and day (each a compute host change) | `7.8` |
| energy host changes per Leaf and day | `8.4` |

**The sector radius sets the rate**. At `0.5 km` a vehicle hands over `50` times an hour. At `3 km` it hands over `8` times an hour. At `3 km` most of the video and `63 %` of the delta minutes have no link.

| Sector radius | Walk, per hour | Vehicle, per hour | Delta minutes with no link | Video minutes with no link |
|---|---|---|---|---|
| `0.5 km` | `7.0` | `49.6` | `0 %` | `0 %` |
| `1.0 km` | `3.3` | `25.1` | `0 %` | `9.9 %` |
| `1.5 km` | `2.2` | `16.6` | `1.2 %` | `54 %` |
| `2.0 km` | `1.6` | `12.5` | `34 %` | `72 %` |
| `3.0 km` | `0.9` | `8.4` | `63 %` | `88 %` |

The `net/discovery` city run gives `4.5` per hour with validators `8 km` apart. The two agree in order.

### 6.4 The energy and the heat of each class

Per Leaf and day, base deployment.

| Measure | C0 | C1 | C2 |
|---|---|---|---|
| hours | `7.2` | `8.8` | `8.0` |
| load energy | `4.1 Wh` | `7.6 Wh` | `8.1 Wh` |
| from the cell | `0.0 Wh` | `3.1 Wh` | `4.0 Wh` |
| hours above `1.73 W` with no heat path | `0.0` | `3.0` | `2.7` |
| mean load per hour on the class | `0.56 W` | `0.86 W` | `1.01 W` |

**The reading**.

1. **C0 is the cool class**. The dock plate is a heat path and the host carries the load.
2. **C1 and C2 run hot in free air**. `5.7 h` a day sit above the free-air limit. The Split does not change that. The B module keeps the hub and the radio.
3. **The cell cycles once a day** on Full S: `7.2 Wh` from the cell against `7.1 Wh` usable. The float policy of Part 22.4 holds only on the hours with a host.
4. **C2 costs `17 %` more per hour** than C1 in the mean load. The long link adds duty.

### 6.5 The load on a site by the hour

The peak hour is `12:00`. `23.5 %` of all Leafs are in a C2 delta session and `6.5 %` in a C2 video session. A site of `3` sectors at `1 km` carries `747` delta or `132` video sessions. At the real peak it carries `475` registered Leafs per km2. The `15 %` mix of `fleet.py` would give `993`. The commute and lunch hours halve the density a site can carry.

## 7 · Question 5: The unique join

Candidates of `hw/core/BRIEF.md` Section 5. The verdict is on the fleet model only.

| Candidate | The verdict | The numbers |
|---|---|---|
| 1 One wallet, many surfaces | supported, with a new risk | A stolen B module holds an identity element and no wallet. A site holds `3 222` wallet signers. One signer serves `1 882` registered Leafs at the peak mix |
| 2 A chain-attached Skin | supported, and the Core is the right unit | `7.8` class changes and `17.6` C2 hand-overs per Leaf and day. A site settles `757` receipts per second as `1` transaction per slot |
| 3 The Core is a validator | supported at C2. Weakened at C0 and C1 | C2 carries `133` to `3 222` registered Leafs and costs `USD 4.8` per Leaf-month. Chain duty takes `1.5` of the `6.8` usable cores of a dock Core |
| 4 The part record on every part | neutral | A site holds `4` device types. A part change needs no Leaf action. No fleet number tests the record |
| 5 One Core drives the whole family | supported in slice mode | Leaf 80, 160 and 480 give `158`, `79` and `97` delta sessions per box. The pixel mode needs `1 229 Mpix/s` per Skin |

**What the fleet model weakens**.

1. **"One hardware, many screens" for the pixel Skin**. The room link carries `1.4` to `2.8` Skins and the dock `2`. The slice Leaf scales. The pixel Skin does not.
2. **"The room is the network node."** A room Core serves `5` delta sessions with the dock silicon. Chain duty is a fixed `1.5` cores and `6 GB`. The overhead is large against one family.
3. **"The Core is the device and the Skin is its window" at C2**. At C2 the window is the full Leaf. The join reduces to Part 21 with a remote validator plus the Two Hosts Law.
4. **"A stolen Skin holds no key."** It holds. The Core now holds the keys of `3 222` wallets. The B module keeps only the identity.
5. **The UWB distance proof of `SW-24` ends at about `10 m`**. At C1 beyond `10 m` and at C2 the proof of nearness is latency from challengers, not UWB.

**What is new and survives**. The Two Hosts Law, the site as the unit of settlement, and one rule: the radio and the signatures set the range, not the silicon.

## 8 · Proposed gates

Names are proposals for the Program Lead. A gate without a pass condition is not a gate.

| Gate | The test | The pass condition |
|---|---|---|
| **HC-C1** | sector capacity: a `256`-element array, `100 MHz` TDD at `3.5 GHz`, `100 W`, Leafs at `1 km` in a city with `8 dB` of loss | at least `30` video sessions or `150` delta sessions, each with the air delay of `sim/latency` |
| **HC-C2** | reach under SAR: a hand-held Leaf at `20 dBm` on the ruled uplink | delta holds at `1.7 km` and video at `1.0 km`, with BLER at or under `10 %` |
| **HC-C3** | the wire budget of the ruled split, with L2 and QUIC counted | the Leaf uplink is at or under `100 kbit/s` for delta and `600 kbit/s` for video, and no wallet signature crosses the link |
| **HC-C4** | the identity attestation: a Core with every Core key tries to forge the second attestation | the forgery fails. The attestation is at or under `2.5 kB` per second |
| **HC-C5** | the signer: a site of `1 000` wallets under a root attacker on the compute host | no wallet key is read, no signature without a user-presence attestation, and at least `1 000` signatures per second per signer |
| **HC-C6** | one reference compute box at `240 Hz` scan-out with sampled bit-exact re-execution | at least `70` delta or `38` video sessions, with the render and encode p99 at or under `6 ms` |
| **HC-C7** | the frame engine: raw slice hash and raster against the CPU reference | at least `20 GB/s` of hash and `10 Gpx/s` of raster per card, with every slice hash equal bit for bit |
| **HC-C8** | the encoder path at `1600 x 3200` | the first slice in `1.5 ms` or less and at least `13` video sessions per card of `4 Gpix/s` |
| **HC-C9** | receipt aggregation at a Core | at most one settlement transaction per slot for at least `500` live sessions. Each Leaf verifies its Merkle path. A challenger can open any second |
| **HC-C10** | the two hosts energy: a Leaf at `1 km` on a near host, then on its cell alone | the delta load is at or under `2.6 W`. Full S lasts `2.8 h` or more. Buffer lasts `28 min` or more. The hottest face point is recorded against `36.2 °C` |
| **HC-C11** | host changes in both orders, `100` runs each | an energy host change with the compute host fixed loses no frame at p95 and `3` at p99. A compute host change with the energy host fixed loses at most `5` frames |
| **HC-C12** | site failover: `2` sites, one killed at `500` live sessions | every session is on the shadow within `150 ms` at p99, with at most `5` frames lost and no reload. The other site stays under `60 %` |
| **HC-C13** | a `24 h` city day of `1 000` Leafs | no stuck frame at `17` or more C2 hand-overs per Leaf and day. At least `83 %` of planned hand-overs lose no frame |
| **HC-C14** | the unit cost sheet for SW-19 | one cost per function with a source. The cost per delta session-hour at `25 %` use is at or under `USD 0.15`. Spectrum and stake are named |
| **HC-C15** | the camera at C2 | a `12 MB` frame is delivered in `40 s` or less at `1 km`. The live stream is refused beyond `300 m`. The class line says `deferred` beyond `2 km` |
| **HC-C16** | the room pixel link, for the Skin contrast | at least `2` Skins at `6:1` in one room. A result under `2` closes the pixel Skin as a many-screen product |

## 9 · The open issues

1. **The link budget is this seat's own**. The path loss is 3GPP TR 38.901 UMa and RMa, recalled and not re-checked. The far seat owns the proper budget. Its numbers replace the reach table.
2. **The CSI at range is a hypothesis**. The model assumes a low-rank angular channel and `0.6` of the pilot SNR. A rich scattering city makes the downlink worse. Gate HC-C1 measures it.
3. **The scheduling grant limit is a hypothesis**. `8` users per slot and `40` grants per second per delta Leaf set the `249` delta sessions at `1 km`. A semi-persistent grant lifts it.
4. **The encoder binds, and the encoder numbers are datasheet recall**. The Orin NX and AGX Orin encode rates are `[HYPOTHESIS]`. The `MA35D` rate is `[PUBLICATION]` and is a preliminary AMD figure.
5. **The frame hash covers raw pixels**. A lossy codec decodes to a different picture. The hash must cover the decoded frame or a lossless slice. `FINAL/21` and `validator/leaf-duty` leave this open.
6. **The speculative frames are encoded and sent**. If they ride the compositor only, delta encode falls by a third.
7. **The wallet signer in the Core concentrates keys**. The trust seat owns the design. Gate HC-C5 is the test.
8. **The identity element needs an asymmetric attestation**. A shared MAC lets the Core forge the receipt. The signature size is open: `64 B` classical, `666 B` Falcon, `2 420 B` ML-DSA-44.
9. **The AI of the ruling is not in the model**. Its GPU time per session is unknown. It adds to the compute side and to the site power.
10. **Spectrum and stake are excluded**. Either can double the cost per Leaf at a small fleet.
11. **The grid outage law is a guess**. The three grids of section 5.7 bracket it. A measured grid replaces them.
12. **Paths are straight lines**. The roaming run under-counts hand-overs by about `30 %`.
13. **`density.py` assumes `256` render sessions per site**. This model gives `747` delta or `132` video sessions per site at `1 km`. The units differ: full-rate against dirty-slice.
14. **Python 3 and numpy are the only packages**. `matplotlib` is not needed. No figure is made.
