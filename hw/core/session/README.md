# BUDLUM LEAF · CORE AND SKIN · SESSION SEAT

**Revision L.7 candidate · 2026-10-19 · continuity seat, block HP-2**. A study. It changes no L.6.0 or L.6.1 decision until Ayaz rules. Charter: `hw/core/BRIEF.md`, with the distance order of Section 8. The model extends the RG-19 model of `hw/hostpower/continuity/`, imported read only. `[HYPOTHESIS]` for every result.

## 0 · The damage to the Split, first

The program needs the true answer, so the damage comes before the results.

1. **A Skin cannot carry a lit session**. A Buffer Leaf crosses a `75 s` walk with `0` frames lost. A Skin has no frame store and no signer. Its session pauses at pickup. The roam to a new Core costs `0.3 s` to `2.1 s`. A Skin store does not change that on a cable.
2. **The Core is a single point**. For three screens, the chance that no screen works is `50` times higher with one Core than with three Leafs. The dark screen-minutes per year are equal. The Split moves the risk into one event.
3. **A wireless Skin needs its own cell**. A 60 GHz Skin with no cell cannot attach. The link seat gives it `4.8 Wh`. A 60 GHz Skin with `72 J` fails an hour of carry.
4. **The 60 GHz Skin is the weak tether**. Blockage costs `920` dark screen-minutes per year for three Skins, against `45` on a cable. The link seat agrees: the p99.9 of a 60 GHz tether is `41 ms`.
5. **The Skin shows a stated screen, never a held frame**. A held frame looks live. The Skin has no memory to hold one. With no store and no cable power it is black.
6. **The zero-frame handover covers C2 and the Core side only**. A move from a C0 Core to a C2 Core loses `509` frames if the Leaf was asleep. It loses `21` if the Leaf was awake. It loses `0` seen if the Leaf ran a hot shadow while tethered. The hot shadow costs about `1.1 W` on the tether. `[HYPOTHESIS]`

What the Split strengthens is in Section 6.

## 1 · What is here

| File | Content |
|---|---|
| `skinsession.py` | the model: Skin, Core, pairing, views, the four modes, the merge, the writer ledger with TakeOver |
| `roam_sim.py` | a Skin from Core A to Core B, and a Leaf from C0 to C2 and back |
| `corefail.py` | the Core as a single point, the joint failure rates, the Skin on a link loss |
| `RG-19A-skins.md` | the order: rules R12 to R17, the stored state, the acceptance test |
| `proto/skin_chain.proto` | the draft for the chain and the Leaf wire, wire `1.2`, additive |
| `proto/skin_link.proto` | the draft for the Skin to Core link, package `budlum.skin.v1` |
| `skinproto.py` | merges the drafts in memory on top of `leaf.proto` and the RG-19 draft, checks and sizes them |
| `tests/` | `133` tests in four files |
| `out/` | `roam.md`, `roam.json`, `corefail.md`, `corefail.json`, `proto_sizes.md` |
| `run_all.sh` | runs everything and the prose check |

## 2 · How to run

```sh
sh hw/core/session/run_all.sh
```

No third-party package is needed. numpy and matplotlib are not installed, so there are no plots. Tests run with `python3 -m unittest discover -s tests`. The seeds are fixed.

## 3 · The key results, by distance class

Distance classes: C0 is a contact or tether to `2 m`. C1 is a room to about `30 m`. C2 is far. The class of each result is stated.

### 3.1 One session on many Skins (C0 and C1)

| Mode | The rule | Checked by |
|---|---|---|
| MIRROR | every Skin shows the canvas, scaled | the touch maps to the canvas |
| EXTEND | one canvas, one tile range per Skin | tiles are disjoint and cover the canvas |
| SPLIT | one session per Skin | an event changes only its own session |
| HANDOFF | the view moves, the session does not pause | the old Skin is cut off at once |

**The Skin holds nothing durable.** Its identity is in ROM. Its link key, its scan lines and its counter are volatile. A power cycle at any instant leaves the session root equal to a twin with no cycle.

**The merge.** The Core stamps a `480 Hz` tick and orders by tick, class rank, Skin id and sequence. `300` events from four Skins give the same order in `20` shuffled arrivals. Each Skin keeps its own order. IMU samples and camera pixels are not transactions.

**The load.** N Skins share one store.

| N | Mirror | Extend or split | Lit time on `0.9 Wh`, mirror | N Leafs, each |
|---|---|---|---|---|
| 1 | `2.23 W` | `2.23 W` | `23.3 min` | `23.3 min` |
| 3 | `4.19 W` | `5.52 W` | `12.4 min` | `23.3 min` |
| 6 | `7.13 W` | `10.46 W` | `7.3 min` | `23.3 min` |

### 3.2 The Skin that roams (C0 and C1)

Times run from the moment the Skin touches Core B. Medians of `2 000` draws. The attach and relink times are an assumption. The rates follow `hw/core/link`.

| Scenario | First pixel | Live frame | Full session | Frames not live |
|---|---|---|---|---|
| R1 desk Core to a standby vehicle Core, 5G, cable | `156 ms` | `300 ms` | `367 ms` | `35` |
| R2 to a second desk Core, awake, proximity hint | `156 ms` | `197 ms` | `201 ms` | `10` |
| R3 to a vehicle Core with a cold modem | `156 ms` | `2.14 s` | `2.20 s` | `475` |
| R4 Core A dead, `30 s` carry | `156 ms` | `300 ms` | `367 ms` | `35` |
| R5 Core A dead, `1 s` carry, pause and lapse | `156 ms` | `1.12 s` | `1.19 s` | `232` |
| R6 the same, by TakeOver | `156 ms` | `0.30 s` | `0.37 s` | `35` |
| R1 over 60 GHz | `256 ms` | `410 ms` | `477 ms` | `37` |

**The store of the Skin**. Three stores give the same times on a cable: none, seconds and minutes. Seconds is `2 J`, a `17 s` ROM screen. Minutes is `72 J`, a `10 min` ROM screen. The cable powers the Skin and its attach takes longer than its boot. The store buys the ROM screen during the carry and nothing else.

**What decides the time.** The state of Core B decides: awake, standby or cold modem. Then comes the RG-19 resume. A TakeOver saves the `2 s` lapse wait.

**The input path.** The Skin hop adds `1.8 ms`. The link seat measures `0.1 ms` for the tether alone. The rest is the Core transcode and the Skin decode.

| Path | A new action, mean and p99 | A predicted action, mean and p99 |
|---|---|---|
| Wi-Fi, a Leaf | `13.6` and `17.5 ms` | `4.4` and `7.1 ms` |
| Wi-Fi, a Skin on a cable | `15.4` and `19.3 ms` | `6.2` and `8.9 ms` |
| 5G cell-site, a Leaf | `15.5` and `20.9 ms` | `4.4` and `7.1 ms` |
| 5G cell-site, a Skin on a cable | `17.2` and `22.7 ms` | `6.2` and `8.9 ms` |

All four stay under `30 ms` at the `99`th percentile. Gate DST-11 measures the real values.

### 3.3 C0 to C2 and back (the distance order)

At C2 the device is the L.6.0 Leaf. It renders locally with its slice decoder. Its own U7 signs. The session moves by one TakeOver. The round trips come from `sim/latency`: `5.0 ms` for the cell-site path, `81 ms` for the far path.

| Class and path | Input to photon, mean and p99 |
|---|---|
| C0, a Skin on a cable | `15.4` and `19.3 ms` |
| C1, a Skin on 60 GHz | `16.7` and `20.6 ms` |
| C2 km, 5G cell-site, large Core antenna | `16.5` and `21.5 ms` |
| C2 far, far validator | `92.7` and `103.0 ms` |

**Out, the tether is lost.**

| C2 path | The Leaf before | Live frame, p50 | Frames not live | Frames covered by U1 |
|---|---|---|---|---|
| km | asleep | `2.14 s` | `509` | `0` |
| km | awake, decoder idle | `100 ms` | `21` | `0` |
| km | hot shadow while tethered | `18 ms` | `0` | `3`, inside the `40 ms` limit |
| far | asleep | `2.34 s` | `557` | `0` |
| far | awake | `180 ms` | `40` | `0` |
| far | hot shadow | `98 ms` | `0` | `23`, outside the `40 ms` limit |

**Back.** The Leaf stays live on its C2 stream while the tether trains. The Core takes over in `203 ms` on a cable and `311 ms` on 60 GHz. `0` frames are not live. U1 covers `5` to `7` frames.

**Energy at C2.** Power does not travel kilometres. At C2 the energy is the Leaf cell. A Bare Leaf lives `2.2 s` lit and `16 min` dark. The Bare tier is a C0 and C1 idea.

### 3.4 The Core as a single point (C0, C1 and C2)

The rates per hour and the repair times are `[HYPOTHESIS]`. Core box: `1/20 000` and `600 s`. Skin panel: `1/50 000` and `3 600 s`. Cable link: `1/50 000` and `60 s`. 60 GHz blockage: `2` and `1 s`. The validator figures come from `net/discovery`. A Leaf is a Core and a panel in one body. The common-cause share is `0.02`. A simulation checks the closed form to within `15 %`.

| Failure | What it costs, N = 3 on one Core |
|---|---|
| C1 host power lost | all `3` Skins run `12 min` lit on one store, against `23 min` each for three Leafs |
| C2 one Skin link lost | that Skin shows the ROM screen in `15 ms`, back in `109 ms` on a cable |
| C3 the Core box dies | all `3` dark at once, the live frame on another Core in `0.30 s` |
| C4 the validator role fails | `4` to `5` frames covered, the Skins see no break |
| C5 a Skin dies | that screen only |

| N = 3 | No screen at all, minutes per year | Dark screen-minutes per year |
|---|---|---|
| one Core, cable | `4.4` | `45` |
| three Leafs | `0.09` | `45` |
| one Core, 60 GHz | `4.4` | `920` |

**At C2 the single point reads differently.** The Leaf keeps its silicon, frame store and compositor. A box death of the Core does not darken a Leaf. The compositor covers `4` to `5` frames at the km class, inside the limit. At the far class it covers `23`, outside the limit. A cold start without a shadow takes `133 ms` at km and `495 ms` far.

The single point moves to the replica count and to a common cause.

| Fleet | k = 1 | k = 2 | k = 4 |
|---|---|---|---|
| stress fleet of `net/discovery` | `8 680 min` per year | `312` | `174` |
| healthy fleet, one tenth of the crashes | `875` | `19` | `17.5` |

These count a validator outage, not a dark screen. More replicas stop helping at the common-cause floor.

**The blast radius grows.** A large C2 Core serves about `100` users. `[HYPOTHESIS]` The fleet seat sets the number. One box death touches all of them. A cold start of `100` sessions needs `25.6 MB` of intra frames in about `0.15 s`.

### 3.5 The frame capture on a link loss (C0 and C1)

A Skin has no frame store, so it cannot hold the last frame. Detection takes `8.3 ms`. The ROM screen follows at `15 ms`.

| Cause and tether | Store | The Skin shows | Back after the link returns |
|---|---|---|---|
| cable glitch | any | the ROM screen | `105 ms` |
| cable pulled | none | black | `156 ms` |
| cable pulled | seconds, `10 s` outage | the ROM screen | `155 ms` |
| cable pulled | minutes, `15 min` outage | the ROM screen, then black at `10 min` | `156 ms` |
| 60 GHz blockage | minutes or a cell | the ROM screen | `74 ms` |

**What the user sees.** A ROM screen with the words NO LINK and a ring. It is not a held frame. The session runs on at the Core. The Skin misses `240` frames per second of outage. The Core resends the last frame from its own store when the link returns. No intra frame from the validator is needed.

### 3.6 The session as chain state, for Skins

RG-19A adds a Skin id, a pairing record and a view id. A Core on the allowed list takes a Skin with no wallet action. A granted writer takes a live session with one TakeOver. `58` model tests pass, `40` random roams reproduce the no-move state root, and the old writer is refused every time.

## 4 · The draft proto

| Message | Bytes |
|---|---|
| PairingRecord | `4 799` |
| WriterGrant | `4 720` |
| WriterTakeOver | `2 544` |
| SessionPause with two views | `2 885` |
| SessionResume with two views | `2 784` |
| SkinEvent on the link | `32` |

It adds three `LeafMessage` bodies, five error codes and a pause reason. The Skin link is its own package. No Skin message carries a signature.

## 5 · The proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| **HC-S1** | four Skins on one Core, `10^6` random events, shuffled arrival | one order, per-Skin order kept, none lost, ticks stamped by the Core |
| **HC-S2** | power-cycle a Skin at `10 000` random instants in a session | the session root equals a twin with no cycle; no key material is readable in the Skin |
| **HC-S3** | pair, move, revoke and guess | a Skin runs only on its paired Core; a stale or revoked epoch and a guessed key are refused |
| **HC-S4** | the roams R1 to R3 on hardware, cable and 60 GHz | first pixel `200 ms` at p99 on a cable; live frame `0.4 s` at p99 on a standby Core, `3 s` on a cold modem |
| **HC-S5** | `1 000` random moves between two Cores and a Leaf | the state root of a run with no move; the old writer and an ungranted Core are refused |
| **HC-S6** | cut the stream to each Skin, then restore it | the ROM screen in `20 ms`; no pixel of the old frame after `2` frames; back in `250 ms` |
| **HC-S7** | kill the Core box with `3` Skins, and kill the validator role | all Skins show the ROM screen in `20 ms`; the live frame on another Core in `0.4 s` at p99; at most `9` frames covered on a failover |
| **HC-S8** | a Leaf from a C0 Core to a C2 Core and back, with a hot shadow | out in `30 ms` at p99 at km, no stale frame; back in `400 ms` with `0` frames not live; the far class stated as outside the `40 ms` limit |
| **HC-S9** | measure the Core box and the tether failure rates | each rate inside `3` times of the table, or the table is rerun and the verdict restated |

## 6 · Which Part 22 findings the Split moves

| Finding | The Split | Why |
|---|---|---|
| zero-frame handover (DST-12) | **weakens it for a roaming Skin**; **keeps it at C2**; **strengthens the Core side** | a Skin cannot bridge a walk; a C0 to C2 move needs a hot shadow for zero frames; one shadow serves all `N` Skins of a mirror or extend session |
| the volatile frame store | **strengthens it for a Skin gap** | the Core holds the frame store, so a Skin gap needs no intra frame from the validator: back in `0.1` to `0.16 s`; a Core power loss is as before |
| the `7 s` of lost input | **keeps the bound, raises the blast radius** | the Core flush rule is unchanged; one Core window now covers `N` Skins; touches on a dark Skin are lost but are not chain state |
| the dock pair analysis | **extends it and sharpens it** | the Core is the dock pair with `N` loads; the joint loss is `50` times more frequent at `N = 3`; the shadow in another power domain still removes the visible cost |

**What also changes in RG-19.** Rule R5 allows several granted writers. A TakeOver replaces the lapse wait when a grant exists. The pause stores the views.

## 7 · The open issues

| No. | The issue | The owner |
|---|---|---|
| 1 | The attach and relink times of a tether are an assumption. The link seat gives rates and delays, not these times | link seat |
| 2 | A TakeOver lets a granted writer take a live session. A stolen Core with a live grant is a threat | trust seat |
| 3 | The pairing record is on chain and shows a pseudonymous Skin id to every validator | trust seat |
| 4 | A Skin needs a secret in OTP to prove its ROM id. Without it a clone pairs | trust seat |
| 5 | The Core box, Skin panel and link failure rates are guesses. The `50` times figure moves with them | study seat |
| 6 | The hub scaling of extend and split mode, `0.7 W` per extra Skin, is a guess. The power seat has its own fit | power seat |
| 7 | The cable tether fails the link seat gate HC-L4 on power: `4.75 V` at the Skin end. A cable Skin can brown out | link seat, power seat |
| 8 | `leaf-duty` assumes one writer per session. Two writers need a test in the crate | RG-18 |
| 9 | A hot shadow while tethered costs about `1.1 W` and `76 Mbit/s`. The Core energy and the shadow link must carry it | power seat, far seat |
| 10 | The far class, `81 ms`, leaves the `40 ms` reprojection limit. A far Core needs a prediction rule | far seat |
| 11 | The blast radius, `100` users per Core, and the herd of cold starts need the fleet seat | fleet seat |
| 12 | numpy and matplotlib are not installed. There are no plots. No ML-DSA library is installed. Signatures are stand-ins | this seat |
