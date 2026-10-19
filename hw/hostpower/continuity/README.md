# BUDLUM LEAF · HOST POWER · CONTINUITY

**Revision L.6.1 (proposed) · 2026-10-19 · Continuity team**. The question is how a Budlum Leaf lives across power gaps and hosts. It must lose no session and no authority. The second question is what the validator must do. Charter: `hw/hostpower/BRIEF.md`.

## 0 · The thesis check, first

The program needs the true answer, so the damage comes before the results. Condition 4 of BRIEF Section 5 has two halves. Each half breaks in some case.

| The half | The finding |
|---|---|
| a power gap never loses chain state | True for finalized chain state and for every key. False for unfinalized input. See the three losses below |
| `E_buffer >= P_peak x t_handover` | False for Bare at every gap over `0.57 s`. True for Buffer: `2.0` to `9.9 min` at the `8.7 W` peak |

**The losses that remain**. Each one is bounded and stated. None is silent.

1. **No uplink and no other radio path**. A power cut then loses all input since the last finality. The bound is `7 s`: the slot of `6 s` plus the lag of `1 s`.
2. **A cut with no flush**. The Leaf signs its input chain head once per second. A cut then loses the open second. That is `5` events on average at `10` events per second. A flush on the host loss cuts it to one gossip delay, about `17 ms`.
3. **A gap past the grant term or the anchor window**. The state stays intact. The session cannot resume alone. It needs one wallet action, or a re-anchor by a second channel. The two windows are `[HYPOTHESIS]`: `24 h` and `14 days`.

**The Bare tier is a cold restart, not a bridge**. A Bare Leaf with capacitors only lives `2.0 s` at the session load. With the `0.144 Wh` B cell it holds the radios for `16.2 min` more, but the face is dark. The B cell is a rule of `hw/energy/05`, so it is a real part. It is not a capacitor.

**The Bare store can be smaller than the model**. The power-path team finds that `5 J` of capacitor does not fit the `0.24 mm` margin of the body. A store for the safe screen and one pause is about `1.2 J`. It lights the face for `0.5 s`. Row Bare-1.2J of Section 3.3 shows that every gap over `0.5 s` then goes dark at once.

**The Buffer peak is power-limited, not energy-limited.** The power-path team finds that `20` cells carry `3.1 W` at `3 C`. The column for `8.7 W` in Section 3.2 is the energy bound only. The Buffer carries the delta class, `2.24 W`, and not the peak.

**The zero-frame handover covers the live case only**. A resume after a pause needs a boot and a full intra frame, because the frame store is volatile. Gate DST-12 does not cover it.

**The dock validator is not proven**. `hw/dock/out/validator_sizing.txt` finds no single module that serves two sessions at `240 Hz`. The Host Life Law must not depend on the dock being a validator.

**A rewrite of condition 4, proposed**.

> `E_store >= P_bridge x t_handover`, with `P_bridge` capped at the session profile and every cap shown on the class line. A power gap never loses finalized chain state or a key. The unfinalized loss is one gossip delay with the flush rule, and is stated otherwise.

## 1 · What is here

| File | Content |
|---|---|
| `POWER-STATES.md` | the new states, their entry, what lives, what the user sees, the laws |
| `powersm.py` | the executable state machine; imports `fw/boot/bootsm.py` read only |
| `handover_sim.py` | host A to host B: first pixel, full session, frames lost, three tiers, three scenarios |
| `RG-19-session-pause-resume.md` | the research order: what the validator stores, the rules, the test |
| `sessionchain.py` | the reference model of the RG-19 rules, with a U7 journal and replicas |
| `proto/session_continuity.proto` | the wire draft, in the conventions of `proto/VERSIONING.md` |
| `protodraft.py` | merges the draft into `leaf.proto` in memory, checks it and sizes it |
| `dockpair.py` | the dock validator pair: six failure cases, the pack, the joint loss |
| `tests/` | `119` tests in four files |
| `out/` | `handover.md`, `handover.json`, `dockpair.md`, `dockpair.json`, `proto_sizes.md` |
| `run_all.sh` | runs everything and the prose check |

## 2 · How to run

```sh
sh hw/hostpower/continuity/run_all.sh
```

Each script also runs alone with `python3`. The tests run with `python3 -m unittest discover -s tests`. No third-party package is needed. numpy and matplotlib are not installed here, so there are no plots. The runs use fixed seeds.

## 3 · The key results

### 3.1 The states

Eight states sit beside DEAD to SESSION of `bootsm.py`: HOST_AUTH, HOST, BRIDGE, ISLAND, PAUSING, SUSPENDED, RESUMING and RESUME_STATED. Three laws hold in every state. A host pad is dead until the pass. A host never holds authority. A session is live in one place only. A fuzz of `80 000` random steps finds `0` violations.

### 3.2 How long each tier lives

| Tier | Body store | Face lit at `2.24 W` | Hold on the B cell | Live at `8.7 W`, energy bound only |
|---|---|---|---|---|
| Bare | `5 J` | `2.2 s` | `16.2 min` | `0.57 s` |
| Buffer, `0.3 Wh` | `1 042 J` | `7.7 min` | `16.2 min` | `2.0 min` |
| Buffer, `0.9 Wh` | `3 115 J` | `23.2 min` | `16.2 min` | `6.0 min` |
| Buffer, `1.5 Wh` | `5 189 J` | `38.6 min` | `16.2 min` | `9.9 min` |
| Full, `5.9 Wh` | `20 395 J` | `5.6 h` with reduced tiers | none | `39 min` |

### 3.3 The three handovers

Times run from the moment host B touches the Leaf. The medians come from `3 000` draws per cell. Bare-0 has no B cell. Bare-1.2J has a `1.2 J` capacitor and the B cell. `[HYPOTHESIS]` every stage time.

| Scenario | Tier | Outcome | First pixel | Live frame p50 | Live frame p99 | Frames not live, p50 |
|---|---|---|---|---|---|---|
| S1 dock, `75 s` walk, vehicle PD host | Bare-0 | cold restart | `376 ms` | `2.53 s` | `2.82 s` | `517` |
| S1 | Bare-1.2J | hold, face dark `74 s` | `369 ms` | `369 ms` | `637 ms` | `1` |
| S1 | Bare | hold, face dark `73 s` | `370 ms` | `370 ms` | `646 ms` | `0` |
| S1 | Buffer, Full | live, no break | `0` | `0` | `0` | `0` |
| S2 dock to a cell-site validator, `8 s`, Qi host | Bare-0 | cold restart | `274 ms` | `2.42 s` | `2.61 s` | `515` |
| S2 | Bare-1.2J | hold, face dark `7.5 s` | `267 ms` | `267 ms` | `453 ms` | `1` |
| S2 | Bare | hold, face dark `5.8 s` | `269 ms` | `269 ms` | `458 ms` | `1` |
| S2 | Buffer, Full | live, no break | `0` | `0` | `0` | `0` |
| S3 two docks side by side, `1.5 s` | Bare-0, Bare, Buffer, Full | live, no break | `0` | `0` | `0` | `0` |
| S3 | Bare-1.2J | hold, face dark `0.97 s` | `39 ms` | `40 ms` | `103 ms` | `1` |

**Frames lost**. A live handover loses `0` frames in `95 %` of the draws. The other `5 %` cut over to the shadow without warning. That costs `3` frames at the `99`th percentile. The share comes from `net/discovery`.

**The Bare result, honestly**. Bare passes S3 only because `1.5 s` of the session load is `3.4 J`, under its `5 J`. At the `8.7 W` peak the same move needs `13 J`, so Bare fails condition 4 there. Bare needs the B cell for S1 and S2. Without it, Bare restarts from the chain record.

**What a Bare-0 Leaf shows on a restart**.

1. The rear round display lights `25 ms` after contact with the word RESUMING.
2. The face shows the safe screen at the host pass plus `23 ms`. The pass takes `20 ms` on a dock, `250 ms` on Qi and `350 ms` on a PD contract.
3. The live frame follows the link: `0.29 s` on Wi-Fi, `0.48 s` on warm 5G, `2.4 s` on cold 5G.
4. The state is exact. The face shows the confirmed state, and the line says what was dropped.

### 3.4 The cold restart, by link

| Link | Rear glance | Safe screen | Live frame p50 | Full session p50 |
|---|---|---|---|---|
| Wi-Fi, a known dock | `25 ms` | `46 ms` | `293 ms` | `357 ms` |
| 5G, modem attached in idle | `25 ms` | `276 ms` | `478 ms` | `547 ms` |
| 5G, modem cold | `25 ms` | `276 ms` | `2.42 s` | `2.49 s` |
| 5G, loaded cell, modem cold | `25 ms` | `376 ms` | `2.53 s` | `2.60 s` |

An attached modem costs `30 mW` in SUSPENDED. It cuts the restart by `1.9 s` and the guaranteed SUSPENDED life from `72` to `33 min`.

### 3.5 The session as chain state

RG-19 adds `249` bytes to the session state. A SessionPause is `2 764` bytes on the wire. A resume is `2 629` bytes, or `8 711` with a renewed grant. The model checks eleven rules with `40` tests.

| Check | Result |
|---|---|
| `120` random sessions, a pause of `2` frames to `10^8` frames | the final state root equals the run with no pause, every time |
| a validator resumes, pauses or moves a paused session | refused |
| a lapse pause with fresh receipts, or with wrong evidence | refused |
| a signed tap withheld across a pause, then delivered | refused: stale epoch |
| a torn write at any of three cut instants, and `1 000` random cuts | the journal holds the old or the new record |
| a value action in the outbox | sent once or never, and admitted while paused |
| the primary dies, inputs sent to both replicas | `60` of `60` runs lose nothing |
| the primary dies, single send | the nonce gap blocks the epoch until the ring resend |

### 3.6 The dock validator pair

| Item | Value |
|---|---|
| a plain dock, typical draw | `10.4 W`, `111 min` on its pack |
| a dock with the validator and the frame engine | `40.8 W`, `28 min` on its pack |
| joint loss of power and primary, pair against a split design | `60` times more frequent, `[HYPOTHESIS]` rates |
| the shadow takes over after a sudden box death | `4` to `5` frames covered by U1 |
| a cold start on a new validator, on the store | `133 ms` p50, `152 ms` p99 |

**The verdict**. The pair is a strength for latency and for the Bare tier at a desk. It is a weakness for failure independence. It turns two failures into one box event. That costs the Leaf almost nothing, because a shadow in another power domain takes over in `5` frames. It costs real state in one case: the dock offline, with no other radio path for the Leaf, then a power cut. The rule is simple. A shadow must sit in another power domain, and the Leaf must dual-send over its own radio. With that rule, the pair loses no finalized state and no key. Without it, the Host Life Law makes the Leaf as fragile as one box.

## 4 · The answer in short

1. A Leaf has eight power states beside the boot machine. A host never holds authority in any of them.
2. The tier decides what lives in the gap: seconds, minutes or hours. The B cell holds the radios for `16 min` in every tier.
3. A pause is a chain record of `249` bytes. The session clock stops. A resume restores the same root.
4. The validator stores the record and sends a full intra frame after a resume.
5. It accepts a lapse only with evidence. It accepts inputs from the shadow.
6. A restart from the chain costs `0.3` to `2.6 s`. The state is exact. The face states what it dropped.

## 5 · The proposed gates

The letter C marks the continuity team. The program lead assigns final numbers.

| Gate | The test | The pass condition |
|---|---|---|
| **HST-C1** | `10 000` random plug and unplug sequences of a Leaf on a fake host | no host pad current before the pass, every state shows a surface, no host holds a key |
| **HST-C2** | cut a host at `8.7 W` and at `2.24 W` on each tier | the lit time is at least `0.95` of the table of Section 3.2, and the pause finishes with `10` times its energy |
| **HST-C3** | the three handovers of Section 3.3 on a bench with a real host | Buffer shows no break; Bare with the B cell goes live in `700 ms` at p99; a restart goes live in `3.0 s` at p99 on cold 5G |
| **HST-C4** | RG-19 step 1 and 2 on `validator/leaf-duty` | the same state root and frame hash chain as a run with no pause; a second validator matches bit for bit |
| **HST-C5** | `1 000` power cuts at random instants of a U7 journal write | the record is the old or the new one; an action is sent once or never |
| **HST-C6** | cut the dock and the Leaf at random instants, with and without a second radio path | the lost input is at most one gossip delay with the flush rule; without a path the class line says LOCAL |
| **HST-C7** | kill the dock box mid-session with a shadow in another power domain | at most `9` frames covered, no reload, and the session reaches the next host |
| **HST-C8** | resume after `2` days and after `30` days | a stated refusal, never a silent resume; a wallet grant or a re-anchor restores the session |
| **HST-C9** | the cold modem against the attached modem | the live frame in `600 ms` at p99 with the modem attached; SUSPENDED life of `30 min` or more |

## 6 · The open issues

| No. | The issue | The owner |
|---|---|---|
| 1 | The host AON feed before the handshake has no definition. The pads are dead, so the path is the Qi coil or a seat sense | power-path, trust |
| 2 | BRIDGE must cap the load at the session profile. The cap is a visible class change | firmware, `FINAL/08` |
| 3 | The host pass takes `20 ms` on a dock, `250 ms` on Qi and `350 ms` on PD in this model. Each value is a guess, and it sets the first pixel | trust, power-path |
| 4 | The B cell carries the Bare tier. Its fit, its `37 mA` charge and its cycle life are open | energy |
| 5 | `leaf-duty` signs each input with the wallet. The wire draft signs a head per second. RG-19 needs one reading | RG-18, wire team |
| 6 | `leaf-duty` has a `32` byte session id. The wire has `uint64` | RG-18, wire team |
| 7 | The grant term and the anchor window are guesses. Budlum sets the real values | chain team |
| 8 | The failure rates of the dock are guesses. The `60` times figure moves with them | dock team |
| 9 | The dock validator needs a frame engine. No single module serves two sessions at `240 Hz` | dock team, RG-18 |
| 10 | A false lapse has no slashing proof unless the shadow holds a Leaf-signed receipt | chain team |
| 11 | A power-side channel: the host sees the load of the Leaf. The trust team owns the leak | trust |
| 12 | No ML-DSA library is installed. The model uses stand-in signatures of the exact size | this team |
| 13 | The `buf` tool is not installed. The draft passes the checks of `protolite`, not `buf lint` | wire team |
| 14 | The power-path team names its modes HOST_FEED, HOST_TOPUP, BRIDGE and ISLAND. Their ISLAND is a dark body on the B cell. Here that is the hold phase of BRIDGE and SUSPENDED. The names and the pause threshold (`12 %` there, `5 %` here) need one reading | power-path, this team |
| 15 | The flush of rule R9 needs the host-lost trigger. The power-path team sets VHV under `8.0 V` or a missing sideband heartbeat for `100 µs`. Use it | power-path, firmware |
