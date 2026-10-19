# BUDLUM LEAF · THE DIRECTIVE · PART 22 · HOST POWER AND THE LIVING LEAF

**Revision L.6.1 (proposed) · 2026-10-19 · the standing of this part**. This part adds to Part 21 and changes no L.6.0 number. Where it finds a fault in an earlier part, Section 22.16 names it. Tags follow Part 20: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]`, `[GENERAL]` and `[TREE]`.

**The order that created this part**. Ayaz, 2026-10-19: *"Donanım çalıştığı sürece çalışabilecek bir cihaz aslında bir ilktir. Asıl pil donanımda olsa ve sürekli Badlam Leaf çalışsa ne olacak? Bataryanın kapasitesi önemli olmuyor."* Ayaz also handed the whole management of the program to the Program Lead. The Lead ran five study seats, and their work is in `hw/hostpower/`. `[DECISION]`

**The standing**. The thesis is a recommendation with measured limits, in the manner of Part 17. Every number is `[HYPOTHESIS]` until its gate runs. The five studies found that the thesis holds in a narrower form than the order states. This part writes the narrower form, and it writes what the narrower form still wins.

---

## 22.1 The question and the honest answer

**The question**. What happens if the main energy lives in the hardware, and the Leaf keeps only a screen and a small cell? The Leaf then works as long as the hardware works. `[DECISION]`

| The part of the idea | The result of the studies | The tag |
|---|---|---|
| the cell is not the source of life | true on a paired host. The cell becomes the bridge between hosts | `[HYPOTHESIS]` |
| capacity does not matter | false as stated. Capacity moves into the place. The Leaf stops paying for it in grams, millimetres and heat | `[DECISION]` |
| the cell lasts longer | true and large: `13.4` years against `1.8` years in the model, `7.2` times | `[HYPOTHESIS]` |
| the heat falls | false. The heat comes from the session, and the battery path adds only `0.04 W` | `[HYPOTHESIS]` |
| the heat is solved by a host | only by a host that pulls heat: the dock plate holds all `72` cases | `[HYPOTHESIS]` |
| a host gives no risk | false until the power door of Section 22.8 exists | `[HYPOTHESIS]` |
| a session survives a power gap | true for finalized chain state and keys. Section 22.9 lists the losses | `[HYPOTHESIS]` |
| this is a world first | false as stated. Section 22.11 gives the claim that survives | `[PUBLICATION]` |

**The one-line answer**. The Leaf lives as long as its host feeds it, if the host is a paired host with a heat path. The cell stops being the fuel and becomes the bridge. `[DECISION]`

---

## 22.2 The Host Life Law

**The law**. On a paired host with a heat path, a Leaf lives as long as the host supplies power. Between two hosts, a bridge store keeps the session. `[DECISION]`

The first brief of the program stated four conditions. The studies corrected two of them.

| No. | The condition, as corrected | What changed |
|---|---|---|
| 1 | **Power**. `P_host >= P_load + P_topup`, with the `8.7 W` peak and the path loss included | a host under `9 W` on the VHV rail fails the peak |
| 2 | **Heat**. The hottest face point stays at or under `36.2 °C`, in the ambient of the host | in free air no interface passes. The dock plate passes |
| 3 | **Trust**. The host never touches the wallet, the signing core, the firmware slots or the data lanes | the old text said "before its handshake". A host that powers the handshake touches the bridge rail first |
| 4 | **Continuity**. A power gap never loses finalized chain state or keys, and `E_buffer >= P_peak x t_handover` for the live frame | chain state holds. The open second of input and the live frame can be lost |

**The scope rule**. The law holds for a paired host or a host that a paired party vouches for. An unknown host gives `0.5 W` and the safe screen. `[DECISION]` Trust studies, `hw/hostpower/trust/`.

---

## 22.3 The three energy tiers, as the studies left them

| Tier | The store | What it does | The finding |
|---|---|---|---|
| **Bare** | a capacitor store of about `5 J` | lights the face for `2.2 s` at `2.24 W` and `0.57 s` at `8.7 W`, then ends the session | it does not fit the margin. It is an accessory, not a product |
| **Buffer** | `15` to `20` micro cells of the `128` | carries the delta class for `5 min` between hosts | power limited: `20` cells carry `3.1 W` at `3 C` |
| **Full** | all `128` cells, `5.9` to `7.4 Wh` | runs `2.6` to `3.6 h` of a delta session with no host | unchanged from L.6.0 |

`[HYPOTHESIS]` `hw/hostpower/powerpath/`, `tiers.py`.

### 22.3.1 What decides each tier

1. **Bare does not fit.** The thinnest published double layer capacitor is `0.9 mm`. A `3 s` safe screen takes `3` tiles of cell layer. `[PUBLICATION]` source in the study.
2. **Bare ends in a cold restart.** The B cell then holds the radios, face dark, for `16.2 min`. Then the Leaf restarts from chain state.
3. **Buffer is limited by power, not energy.** The `8.7 W` peak needs `53` cells at `3 C`, about `3.1 Wh`. `[HYPOTHESIS]`
4. **A `30 min` delta bridge needs `2.4 Wh`.** That is `58 %` over the first brief.
5. **Buffer cells sit in all four quadrants.** One quadrant holding all blacks the body `3 s` on a swap.
6. **Buffer keeps Article 11.** The cells sit in the four removable quadrants, as the L.6.0 cells do. `[DECISION]`

**The ruling**. Buffer is the first host-power product tier. Full stays as the freedom tier. Bare stays a study until a store fits the margin. `[DECISION]`

### 22.3.2 The saving of the Buffer tier

| The saving, per Leaf | The value | The tag |
|---|---|---|
| mass of cells | `12 g` | `[HYPOTHESIS]` |
| lithium | `0.64 g` | `[HYPOTHESIS]` |
| cobalt | `5.3 g` | `[HYPOTHESIS]` |
| thickness | `0.9 mm`, only if the cells leave the body | `[HYPOTHESIS]` |

The saving is small per Leaf. At one million Leafs it is `635 kg` of lithium and `5.3 t` of cobalt. `[GENERAL]`

---

## 22.4 The power path: the host feeds the load and the cell floats

**The rule**. The host carries the load. The cell floats near `50 %` and never takes a charge above `0.2 C` during a session. `[DECISION]`

| The rail mode | The meaning | The cell current |
|---|---|---|
| `HOST_FEED` | the host carries the whole load and the cells float | `0` |
| `HOST_TOPUP` | the host carries the load and fills the cells up to the float | up to `0.5 C` in |
| `BRIDGE` | no host, and the cells carry the load by a shed ladder | out |
| rail island | body dark, ring on the B cell, then `U7` and U4 ROM only | `0` |

The thresholds are `HOST_FEED` at `55 %` pack charge and `HOST_TOPUP` below `45 %`. The shed ladder is the cell limit above `30 %`, the delta class to `18 %`, and the safe screen to `12 %`. `[DECISION]` proposed in `hw/hostpower/powerpath/powerpath.py`.

### 22.4.1 Why the float matters

| The case | Years to `80 %` capacity | The tag |
|---|---|---|
| Full cell, cycled daily from `100` to `20 %` | `1.8` | `[HYPOTHESIS]` |
| Full cell, host fed, floating at `50 %` | `13.4` | `[HYPOTHESIS]` |
| Buffer of `20` cells, doing all the bridging | `7.7` | `[HYPOTHESIS]` |

The model is Schmalstieg 2014 with the constants of Lee et al. 2023. It was fitted to a `4.2 V` NMC cell and not to the LiCoO2 micro cell. `[PUBLICATION]` The uncertainty is wide, and gate HST-4 measures it.

**What it buys**. The claim "the battery does not matter" becomes "the battery does not wear out first". That claim helps the repair story and the EU lifetime rules. `[DECISION]`

### 22.4.2 The choice of the interface

| The interface | The heat in the Leaf at `8.7 W` | The use |
|---|---|---|
| the `12` bar pads or the dock pads (contact) | `0.28 W` | the always-on path |
| the port part on a seat | `0.28 W` | desks, vehicles, industry |
| Qi2 `15 W` and Qi2.2 `25 W` pad, feeding the load | `0.76 W` | allowed in float mode |
| Qi `5 W` pad | `0.76 W` and `4 W` short of the peak | wake and safe screen only |
| Qi2.2 charging the cell at `25 W` | `9.19 W` in the delta case | at rest, screen off |

**The ruling**. Contact is the always-on interface. Qi is a convenience. A Qi pad feeds the load and never charges the cell during a session. `[DECISION]`

---

## 22.5 The heat: always-on needs a host that pulls heat

The thermal seat ran the L.6.0 model with each host interface. `[TREE]` `hw/hostpower/thermal/`.

| The case, delta session, `25 °C` | The hottest face point | The limit `36.2 °C` |
|---|---|---|
| battery only, free air, still | `41.3 °C` | fails by `5.1 K` |
| contact feed, free air | `42.1` to `44.6 °C` | fails |
| Qi float feed, free air | `42.0` to `42.2 °C` | fails |
| any interface on the dock plate at `22 °C` | margin `+3.1` to `+9.4 K` | passes in `72` of `72` cases |

**What the table says**. A delta session of `2.5 W` is too hot for a still `2.00 mm` body in free air, with a battery or a host. Host power does not change that. The dock plate does. `[HYPOTHESIS]`

1. **The host feeds the load.** Feeding saves `0.15 W` against a `0.2 C` top-up, and `1.0 W` against `1 C`.
2. **A `25 W` charge adds `6.4 W`.** It reaches `37.3 °C` even on the dock, `1.1 K` over the limit.
3. **The sustained delta load in free air is `1.73 W`.** Light wind lifts it to `2.37 W`.
4. **At `30 °C` in free air a Leaf holds `30` to `35 %` of delta power.** Video falls lower.
5. **The Frame** holds `1.05 W` at `25 °C` and `0.20 W` at `35 °C`. A `0.8 W` Frame holds to `24 °C`.

**The dock is a heat sink first.** The dock plate admits `5.7` to `7.2 W`, and the Qi basic profile caps at `4.67 W`. The plate at `22 °C` sits under the dew point at `35 °C` and `60 %` humidity, so the set-point needs a rule. `[HYPOTHESIS]` Gate HST-10.

**The hard consequence**. A claim of always-on in the hand, in free air, is false for the L.6.0 body. The claim holds on a dock, and in a vehicle or machine cradle with a heat path. `[DECISION]` Gap G-46.

---

## 22.6 The host classes

The offered power is on the VHV rail. The `8.7 W` peak is `9.0 W` on VHV. `[TREE]` `hw/hostpower/powerpath/hosts.py`.

| Host | Offered | Carries `8.7 W` | Carries the `25 W` port case | The note |
|---|---|---|---|---|
| H0 wall dock | `25 W` | yes | yes | contact. The pilot host |
| H1 dock pack `20 Wh` | `25 W` | yes | yes | `7.0 h` of delta, `3.0 h` with the dock radios on |
| H2 desk USB-C PD | `7.5` to `100 W` | yes | yes at `15 V` | port part on a seat |
| H3 vehicle `12 V` and `24 V` | `30` to `100 W` | yes | yes | a load dump rated adapter is outside the Leaf |
| H4 industrial `24 V` | `25 W` | yes | yes | clamp in the cradle |
| H4 PoE type 2 | `22.9 W` | yes | no, `2.1 W` short | type 3 needed |
| H5 worn bank or belt | `18 W` | yes | no, `7 W` short | a face worn case |
| H6 Qi pad `5 W` | `5 W` | no, `4 W` short | no | wake only |
| H6 Qi2 `15 W` and Qi2.2 `25 W` | `15` and `25 W` | yes | `25 W` pad only | float mode only |

1. **The clamp lives outside the Leaf.** The adapter or the cradle owns the vehicle and industrial clamps.
2. **The Leaf sees `20 V` at most.** A load dump of `79` to `202 V` stops at the cradle. `[PUBLICATION]` ISO 16750-2, secondary summary.
3. **A `5 V` host has no `3:1` ratio.** The U_Q stage needs a bypass mode at `0.79` efficiency. `[HYPOTHESIS]`

**Where the capacity went**. A `20 Wh` dock pack runs a delta session `7.0 h`, which is `2.2` times the Leaf Full cell of `3.2 h`. An `18.5 Wh` worn bank runs it `6.6 h`. With the dock radios on, the pack runs `3.0 h`, the same as the Leaf alone. The capacity moved and it grew, and the radios took part of it back. `[HYPOTHESIS]`

---

## 22.7 The pilot

The study ranked the places where host life matters. `[HYPOTHESIS]` `hw/hostpower/study/USE-CASES.md`.

| The rank | The place | The host | The reason |
|---|---|---|---|
| 1 | counters and kiosks with a Budlum dock | H0 | margin `+27.3 W`, a heat path, a Budlum owned host |
| 2 | vehicles | H3 | a load dump rated cradle, long dwell time |
| 3 | industrial panels | H4 | steady power, `24 V` clamp |

**The pilot ruling**. One Turkish city, `100` units on Budlum docks, `60` days. Gate HST-28. `[DECISION]`

---

## 22.8 The power door: a host never gains authority

The trust seat found that power is a door, and a host that powers the handshake already stands inside it. `[TREE]` `hw/hostpower/trust/`, `60` tests pass.

| The rule | The meaning |
|---|---|
| the island rail | `U7` and U4 ROM sit on a regulated bridge rail with brownout detect, never on the host rail |
| the dead pad, widened | the host pads stay at `0 V`, or at a power-only low class, until the handshake passes. At a Qi coil: no rail connected |
| the HostRecord | class, maximum power, voltage window, host key id, optional validator role, expiry and counter, checked by `U7` |
| the policy | an unknown host gets `0.5 W` and the safe screen. A paired host gets its class. A role claim never moves the class |
| the one frame | `U7` hears the host only through one fixed `169` byte frame |
| the atomic commit | no signature and no update straddles a power loss |
| the anchor age | the Leaf refuses the stream when the anchor is older than `6 h` |

**The findings that change the design**.

1. **A RAM replay counter is void.** The host controls every power cycle. A test accepts a replay with RAM counters and refuses it with NVM counters.
2. **`fw/u7` has no NVM and no HostRecord program.** Gap G-44.
3. **Fault injection and power analysis enter the scope.** The signing store needs `0.13` to `2.6 mF`. The unpadded recharge leaks `3.18` bits per signature.
4. **A double glitch can skip the self check and release a bad signature.** The risk is open. Gate HST-16 measures it.
5. **ENR-19 assumes a powered `U7`.** On the sideband alone one handshake takes about `111 ms`.
6. **A host that is the only network path can starve a rotation.** The anchor age rule closes it.
7. **Nobody enrols a host yet.** The authority and the chain revocation of a host key are open. Gap G-48.

`[HYPOTHESIS]` Every island rail number. The ed25519 code is the RFC 8032 reference and stands in for the ML-DSA-87 wallet.

---

## 22.9 The continuity: a power gap is not a loss

The continuity seat added the session states beside the dead-pad machine of `fw/boot`. `[TREE]` `hw/hostpower/continuity/`, `119` tests pass and an `80 000` step fuzz found `0` law violations.

| The session state | The meaning |
|---|---|
| `HOST_AUTH` | a host is at the contact and the pads stay at `0 V` |
| `HOST` | the host passed the `U7` handshake and carries the load |
| `BRIDGE` | the host left and the store holds the floor |
| `ISLAND` | Full tier, no host, past the bridge horizon of `600 s` |
| `PAUSING`, `SUSPENDED` | the pause is committed on chain and `U4` ROM and `U7` stay alive on the B cell |
| `RESUMING`, `RESUME_STATED` | a host passed the handshake on a paused Leaf, or the resume was refused with a stated reason |

**The naming fault.** The power path seat uses `ISLAND` for a rail mode, and this seat uses it for a session state. The directive keeps both and writes the rail one as "rail island". Gap G-45.

### 22.9.1 What the numbers say

| The result | The value |
|---|---|
| cold restart, safe screen after the host pass | `23 ms` |
| live frame after a cold restart | `0.29 s` Wi-Fi, `0.48 s` warm 5G, `2.4 s` cold 5G |
| Buffer and Full on a `75 s` walk | no break. `0` frames lost in `95 %` of draws, `3` at p99 |
| RG-19 chain state added | `249 B`, and a SessionPause of `2 764 B` |
| `120` random pauses, `2` frames to `10^8` frames | the same state root as a run with no pause, every time |

### 22.9.2 What a power gap can still lose

1. **Up to `7 s` of input.** An offline dock with no other radio path cannot flush.
2. **The open second of input, about `5` events.** A host loss without a flush drops it.
3. **The live frame.** The frame store is volatile, so zero-frame handover covers only the live case.
4. **A long gap.** A gap past the grant term or the anchor window needs a wallet action or a re-anchor.

**The ruling**. The session is chain state, and a power gap loses no finalized state or key. The Leaf states each of the four losses to the user. `[DECISION]`

---

## 22.10 The dock: the partner of the living Leaf

The dock gives energy, pulls heat and can serve a room session. `[TREE]` `hw/dock/`.

| The job | The finding |
|---|---|
| energy | the `20 Wh` pack refills the `600 Wh/L` body `2.84` times through the pads |
| heat | the plate and the thermoelectric stage hold every case. The TEC needs `3.8 W` at `35 °C` for delta |
| compute | the optional dock validator serves the room session at `30 ms` |
| failure | a dock pair makes the joint loss of power and primary validator about `60` times more frequent (assumed rates) |

**The ruling**. The Host Life Law never depends on a dock validator. No dock module serves two sessions, and a sudden box death costs `4` to `5` frames that `U1` covers. The Leaf fails over to the nearest other validator while power holds. `[DECISION]`

---

## 22.11 The claim

The study listed `21` products and papers, each with a URL, and some pages did not load. The Ledger Nano S is a wallet with a screen and no cell. The Galaxy Tab Active runs with the cell removed on a PD supply. The XREAL Air 2 is a display with no cell. Dash cams and laptops use bridge cells and capacitors. `[PUBLICATION]` `hw/hostpower/study/PRIOR-ART.md`.

| The sentence | The verdict |
|---|---|
| the strong one: *the first wallet surface that lives as long as its host* | do not use. "First" fails today |
| the defensible one | use at the Designed tier, as written below |
| the safe one | use in public text until a prototype passes |

> On a host, a Budlum Leaf 160 by 80 mm runs for as long as the host supplies power. A small bridge store keeps the wallet session when the power changes hands.

**The rule for the word "first"**. The word stays out of every text until gates HST-25 and HST-26 pass. The open combination is a chain session, a bridge between hosts and a power door that gives the host no authority. The survey is a web search and not a patent search. `[DECISION]`

---

## 22.12 The law and the standards

| The question | The reading | The tag |
|---|---|---|
| is a capacitor a battery under 2023/1542 Article 3(1) | no. A lithium-ion capacitor or a clock cell removes that gain | `[PUBLICATION]` and `[HYPOTHESIS]` |
| does the Buffer tier keep Article 11 | yes, if the cells sit in the removable quadrants | `[HYPOTHESIS]` |
| does Article 11(3) save a fixed Buffer | not safely. The main function is a surface and a wallet | `[HYPOTHESIS]` |
| Qi above `5 W` | needs certificate authentication | `[PUBLICATION]` |
| a vehicle supply | needs ISO 16750-2 test A, load dump rated: `101 V` on `12 V`, `202 V` on `24 V` systems | `[PUBLICATION]` secondary |
| a host fed body worn device | IEC 62368-1 class ES1 and a stated power source class on every host input | `[HYPOTHESIS]` |

**The honest limits**. Several pages did not load, among them EUR-Lex and the Commission notice. The PS limits, the PoE ranges and the ISO 7637-2 pulses are recalled and carry `[HYPOTHESIS]`. This is a risk review and it is not legal advice. Nine questions go to a lawyer and six to a laboratory. Gates HST-26 and HST-27.

---

## 22.13 The recommended configuration, in one table

| The decision | The ruling | The reason |
|---|---|---|
| D-9 the first host-power tier | Buffer, `15` to `20` cells over four quadrants | Bare does not fit. Full is the freedom tier |
| D-10 the always-on interface | contact, on the dock and the port part | Qi loses `0.76 W` against `0.28 W`, and Qi `5 W` fails the peak |
| D-11 the cell policy on a host | float near `50 %`, top-up at `0.2 C` or less | `7.2` times the cell life and `1.0 W` less heat than `1 C` |
| D-12 the dock | a heat sink and a power host first, a validator second | the plate passes `72` of `72` cases |
| D-13 the trust base | `U7` with NVM counters and a HostRecord | a RAM counter is void on a host |
| D-14 the claim | the defensible sentence, with no "first" | a web survey of `21` rows found no join. It is not a patent search |
| D-15 the pilot | counters and kiosks on Budlum docks, one Turkish city | `+27.3 W` margin and a heat path |

`[DECISION]` of the Program Lead, under the order of 2026-10-19. Ayaz can reverse any row.

---

## 22.14 The research order for the Budlum tree

| Order | The work | The acceptance test |
|---|---|---|
| **RG-19** | session pause and resume: SessionPause, SessionResume, a grant term, an anchor window, and a resume rule that checks the state root | `120` random pauses keep the no-pause state root. A second validator matches a sample bit for bit. A late pause is refused with a stated reason |

The reference model is `sessionchain.py`, and the proto draft is `proto/session_continuity.proto` in `hw/hostpower/continuity/`. It adds `6` messages and `10` error codes at wire `1.1`. `buf lint` has not run. `[TREE]`

---

## 22.15 The new gates

The five study seats proposed `52` gates under four prefixes. The Lead merged them into one series. The right column names the source gates.

| Gate | The test | The pass condition |
|---|---|---|
| **HST-1** | a Bare store: `3 s` of the safe screen | the store takes at most `3` tiles of cell volume, and VBUS holds `3.40 V`. Source: power path 1 |
| **HST-2** | Buffer group power: `15` cells at `2.24 W` for `5 min`, and the pulse rate at `3`, `5` and `10 C` | VBUS holds `3.40 V`, no cell over `45 °C`. Source: power path 2 and 3 |
| **HST-3** | the U_Q host window at `5`, `9`, `12` and `15 V` | VBUS `3.40` to `4.48 V` at `0.93` efficiency, and a `5 V` host stays under `1.0 W` of body heat |
| **HST-4** | cell cycles and storage: `800` cycles, `1 000 h` at `3.86 V`, and the `30` day float policy | `800` cycles met, alpha within `2` times of the model, pack charge `45` to `55 %` |
| **HST-5** | the island rail: `1 000` host drops and `100` quadrant swaps | `1V8_AON` stays over `1.75 V`, and the B cell alone runs `2.5 h`. Source: power path 7 and trust 3 |
| **HST-6** | hand-over on a bench, `100` runs, with Buffer cells spread | VBUS holds `3.40 V` for the whole `3 s`, with at most `3` mode changes per event |
| **HST-7** | host classes H0 to H6 each carry `8.7 W` for `10 min` | the table of Section 22.6 within `10 %`, and no host reaches VBUS before the proof |
| **HST-8** | vehicle cradle: cranking and load dump A and B | VHV never over `20 V`, the session holds through the dropout, and ISO 16750-2 passes |
| **HST-9** | the free air delta session at `25 °C`, still, `60 min` | the gate records the result against `36.2 °C`. The model expects a failure of `5.1` to `8.4 K` |
| **HST-10** | the dock plate session at `20`, `25`, `30` and `35 °C`, with the dew point set-point | at or under `36.2 °C` for `60 min`, and no condensation. The model predicts `28` to `31 °C` |
| **HST-11** | the feed the load rule: Qi float with cell current under `20 mA`, and a charge during a session | float within `0.3 W` of the battery run, and the cell charges only below `34.2 °C` at `0.2 C` or less |
| **HST-12** | the interface loss of the `12` pads, new and worn, at `1.9` and `3.3 W` | at or under `0.10 W`. A value over `0.34 W` is a stop |
| **HST-13** | the throttle test at `30 °C` in free air | the delta session holds at least `30 %` of its power at or under `36.2 °C` |
| **HST-14** | the Frame on a head form, `0.8 W` plus a `0.34 W` connector loss, at `25 °C` | both surfaces at or under `36.2 °C` for `60 min` |
| **HST-15** | counterfeit adapters, a `0` to `36 V` sweep, bad frames and data-only pairing | pads and island at `0 V`, zero grants above the unknown class, zero keys added |
| **HST-16** | `10^6` glitches during signing, and a Welch test of the line current over `10^6` signatures | zero faulty signatures, and the t value under `4.5` |
| **HST-17** | `10 000` power cuts at random instants, including a U7 journal write | the old or the new record, no reused counter, an action sent once or never |
| **HST-18** | a rogue Qi transmitter and the cable breakaway | no face point over `36.2 °C`, draw under the unknown class, the cable parts at `6.5 N` or less |
| **HST-19** | the anchor age rule: a host as the only path for `6 h` | the stream is refused |
| **HST-20** | `10 000` random plug and unplug sequences on a fake host | no pad current before the pass, every state shows a surface, no host holds a key |
| **HST-21** | a host cut at `8.7 W` and at `2.24 W` on each tier | lit time at least `0.95` of the table, and the pause finishes with `10` times its energy |
| **HST-22** | RG-19 on `validator/leaf-duty` | the same state root and frame hash chain as a run with no pause |
| **HST-23** | the dock cut and a dock box kill, with and without a second radio path | at most `9` frames covered, no reload, and the lost input at most one gossip delay |
| **HST-24** | a resume after `2` days and after `30` days, and the cold against the attached modem | a stated refusal and never a silent resume, and the live frame in `600 ms` at p99 with the modem attached |
| **HST-25** | a professional prior art search of patents and products | a dated report that finds no product that joins a chain session, a host bridge and a power door |
| **HST-26** | a patent attorney opinion on "first", and a legal opinion on nine questions | each sentence and each question answered in writing |
| **HST-27** | an accredited lab report under IEC 62368-1, and a Qi receiver test | ES1 and a stated power class on every host input, and the receiver refuses an uncertified pad above `5 W` |
| **HST-28** | a pilot of `100` units on Budlum docks for `60` days | every record kept, no chain state lost, hottest face point at or under `36.2 °C` |
| **HST-29** | the claim check against PRG-6 | each public sentence maps to a gate record or to a study |

The names of the source gates stay in the team files, so each raw plan keeps its own trace. `[TREE]`

---

## 22.16 What this part found wrong, and the new gaps

**The faults found in earlier text**.

| Where | The fault | The fix |
|---|---|---|
| `FINAL/21` Sections 21.2.6 and 21.2.7 | the routing margin reads `0.24 mm` in the stack table and `0.04 mm` after the coil | the next revision of Part 21 picks one number |
| `hw/energy` and `sim/thermal` | the `5G` outdoor load reads `4.18 W` in one and `6.66 W` in the other | one load map for both |
| `FINAL/12` and the L.6.0 body | a free air delta session fails the `36.2 °C` limit | gap G-46 and a derate rule |
| `fw/boot` and `hw/hostpower` | two meanings of `ISLAND` | Section 22.9 keeps both with distinct names |

**The new gaps**. The gap register of Part 16 carries them as G-44 to G-48.

1. **G-44** the secure element: NVM counters, the HostRecord program and the anchor age rule in `fw/u7`.
2. **G-45** the Bare store and the vocabulary: a store that fits, and one name per state.
3. **G-46** the heat of the body in free air, and the dock plate dew point.
4. **G-47** the claim: the prior art search, the patent opinion and the legal questions.
5. **G-48** the host authority: who enrols a host, and the chain revocation of a host key.

---

## 22.17 Where the work lives

| The seat | The directory | The tests |
|---|---|---|
| power path | `hw/hostpower/powerpath/` | simulator and `11` plots, `thesis_check.py` |
| thermal | `hw/hostpower/thermal/` | `run_all.py` reproduces the L.6.0 model at `41.3 °C` |
| trust | `hw/hostpower/trust/` | `60` tests |
| continuity | `hw/hostpower/continuity/` | `119` tests |
| study | `hw/hostpower/study/` | `21` listed rows, each with a URL |

The brief of the program is `hw/hostpower/BRIEF.md`. The ledger of the agents is `program/AGENT-ROSTER.md`. `[TREE]`

**The next three moves**.

1. Close G-44: give `fw/u7` NVM counters and the HostRecord program.
2. Build the Buffer tier on a bench with `20` cells over four quadrants, and run HST-2, HST-6 and HST-11.
3. Order the prior art search and the legal opinion, so the claim can move from Designed to Proven.
