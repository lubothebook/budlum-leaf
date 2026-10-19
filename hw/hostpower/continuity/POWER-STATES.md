# BUDLUM LEAF · HOST POWER · THE POWER STATES BESIDE THE DEAD-PAD MACHINE

**Revision L.6.1 (proposed) · 2026-10-19 · Continuity team**. The model is `powersm.py`. Tests: `tests/test_powersm.py`. It imports `fw/boot/bootsm.py` read only. Charter: `hw/hostpower/BRIEF.md`.

## 1 · What this file adds

The machine of `fw/boot/STATE-MACHINE.md` answers one question: how does a dead Leaf boot. It has no host in it. It has no time between two hosts. This file adds both. `[DECISION]` proposed.

| The old machine | The new machine |
|---|---|
| DEAD, WAKE, ROOT, PAD_AUTH, SAFE_SCREEN, VERIFY, ATTEST, LINK, ANCHOR, SESSION | HOST_AUTH, HOST, BRIDGE, ISLAND, PAUSING, SUSPENDED, RESUMING, RESUME_STATED |
| a Leaf wakes, boots and ends in a visible state | a Leaf lives across the loss of a host and ends in a visible state |
| the two laws: dead pad and safe screen | the two laws, and the three laws below |

The two machines meet at two places. A host at the contact is the wake event of DEAD. The state RESUMING runs the boot path of `bootsm.py` unchanged.

## 2 · The three laws of this file

1. **P-law 1, the dead host pad**. A host pad stays at `0 V` until U7 passes the host. This extends ENR-19 and MON-16 to the power pads. `[DECISION]`
2. **P-law 2, no authority in power**. A host never holds a key, a grant or a vote. U7 is the only signer in every state. `[DECISION]`
3. **P-law 3, one place for a session**. A session is live in one place, or it is paused on chain. It is never both. `[DECISION]`

The model checks all three after every step. `test_fuzz_event_sequences_break_no_law` runs `60 000` random steps and finds `0` violations.

## 3 · The states

| State | Entry | What lives | The face | The rear round display |
|---|---|---|---|---|
| HOST_AUTH | a host is at the contact | U4 ROM, U7, the rear display; the host pads at `0 V` | what the last state showed | host glyph and the word CHECKING |
| HOST | the host passed the U7 handshake | everything; the host carries the load and refills the store | the session, full class | host glyph and the store level |
| BRIDGE | the host left and the store holds the floor | the session, the link radios, U7; the face while the body store lasts | the session, then dark with the frame store kept | bridge glyph and the minutes left |
| ISLAND | Full tier, no host, past the bridge horizon or by choice | the session under the energy policy of `FINAL/08` Section 8.3 | the session, the tier on the class line | island glyph and the hours left |
| PAUSING | the store reached its floor with a live session | U7 signs a SessionPause, one radio sends it, U7 commits it | the last frame and the line SESSION PAUSED | pause glyph |
| SUSPENDED | the pause is committed | U4 ROM and U7 on the B cell at `25 mW` | dark | on a touch: PAUSED, the host needed, the hours left |
| RESUMING | a host passed the handshake on a paused Leaf | the boot path of `bootsm.py`, then SessionResume | the safe screen at `23 ms`, then the session | the word RESUMING |
| RESUME_STATED | the resume was refused: grant, anchor or state root | the safe screen, the wallet, the update class | the safe screen and one stated line | the reason code |

DEAD stays as in `bootsm.py`: no energy at all. A DEAD Leaf with a paused session is not a lost session. The chain holds it.

**The rear glance**. The round display on the back of the B module draws `0.04 W` for `5 s` per glance. The B cell pays `0.2 J`. It is the only surface in SUSPENDED. It is the first surface on a host: `25 ms` after contact on a cold Leaf. `[TREE]` `hw/energy` budget, `[HYPOTHESIS]` the glyph set.

## 4 · The transitions

```text
HOST ──host lost──▶ BRIDGE ──floor──▶ PAUSING ──committed──▶ SUSPENDED ──B cell empty──▶ DEAD
 ▲                    │  ▲                                      │                         │
 │                    │  └── host refused ◀── HOST_AUTH ◀── host seen ──────────────────────┘
 │                    └──── host seen ──────────▶ HOST_AUTH
 │                                                    │ pass
 └── resume ok ◀── RESUMING ◀── pass, session paused ─┘
 BRIDGE ──horizon, Full tier──▶ ISLAND ──5 percent reserve──▶ PAUSING
 RESUMING ──refused──▶ RESUME_STATED ──user regrant──▶ RESUMING
```

| From | Event | To | Guard |
|---|---|---|---|
| HOST | host lost | BRIDGE | the store holds the floor; else PAUSING |
| BRIDGE, ISLAND, SUSPENDED, DEAD | host seen | HOST_AUTH | none; the host pads stay at `0 V` |
| HOST_AUTH | pass | HOST | the session is live: it never stopped |
| HOST_AUTH | pass | RESUMING | the session is paused |
| HOST_AUTH | fail | the previous state | the pads stay dead and a line is stated |
| BRIDGE | store at floor | PAUSING | body store empty and B cell at its floor |
| BRIDGE | horizon | ISLAND | Full tier only, after `600 s` |
| ISLAND | `5 %` reserve | PAUSING | the reserve tier of `FINAL/08` Section 8.3 |
| PAUSING | committed | SUSPENDED | link up: the validator acknowledged |
| PAUSING | unsent | SUSPENDED | no link: the validator pauses by lapse |
| SUSPENDED | B cell empty | DEAD | the pause stays on chain |
| RESUMING | resume ok | HOST | the state root equals the paused root |
| RESUMING | refused | RESUME_STATED | grant expired, anchor stale or root mismatch |
| RESUMING | host lost | SUSPENDED | the resume was not acknowledged: the pause stands |

**Make before break**. HOST_AUTH from BRIDGE keeps the store load. The session continues while the host is checked. A refused host costs nothing but time.

**The handshake counts as gap**. The time of the host pass is part of the gap. A Qi pass of `250 ms` or a PD contract of `350 ms` comes out of the store. `[HYPOTHESIS]` the trust team owns the values.

## 5 · What each tier keeps alive, in time

`python3 powersm.py` prints this table. The body store is the capacitor plus the micro cells of the tier. The B cell is the `0.144 Wh` cell of the ring.

| Tier | Body store | Face lit at `2.24 W` | Hold on the B cell at `0.40 W` | Live at the `8.7 W` peak | SUSPENDED after that |
|---|---|---|---|---|---|
| Bare-0, no B cell | `5 J` | `2.0 s` | none | `0.57 s` | none: DEAD |
| Bare | `5 J` | `2.2 s` | `16.2 min` | `0.57 s` | `1.2 h` |
| Buffer, `0.3 Wh` | `1 042 J` | `7.7 min` | `16.2 min` | `2.0 min` | `1.2 h` |
| Buffer, `0.9 Wh` | `3 115 J` | `23.2 min` | `16.2 min` | `6.0 min` | `1.2 h` |
| Buffer, `1.5 Wh` | `5 189 J` | `38.6 min` | `16.2 min` | `9.9 min` | `1.2 h` |
| Full, `5.9 Wh` | `20 395 J` | `5.6 h` with reduced tiers | none | `39 min` | `5.5 h` |

**The Full row**. The face stays lit for `5.6 h` only because the policy steps down. It steps at `60 %` and `20 %` of the charge, to `1.0 W` and `0.385 W`. Each step is a visible class change. At the full `2.24 W` the Full tier lives `2.5 h`.

**Bare-0 is a stress case**. Rule 5 of `hw/energy/05-DOCK-PACK-AND-B-CELL.md` keeps the U7 always-on supply on the B cell. A Bare Leaf with that cell is the row Bare. The row Bare-0 shows a Leaf with a flat or absent B cell.

**The peak column is an energy bound**. The power-path team finds that `20` cells carry `3.1 W` at `3 C`. The Buffer carries the `2.24 W` session. It does not carry the `8.7 W` peak.

**The pause costs little**. Signing, sending and committing a SessionPause draws about `17 mJ`. The model keeps `0.5 J`, which is a margin of `29`. `[HYPOTHESIS]` `test_the_pause_costs_far_less_than_its_reserve`.

## 6 · How the new machine meets bootsm

| The step | Time from the wake event | Source |
|---|---|---|
| the rear display lights | `22.2 ms` | `bootsm.boot(["PAD_B"])`, plus `3 ms` for a host AON feed |
| the safe screen is on the face | `23.2 ms` | `bootsm.boot()`, after the host pass |
| the link is up, Wi-Fi with a cached association | `123.7 ms` | `bootsm.boot` with the modem out |
| the link is up, 5G, modem attached in idle | `75.0 ms` | `bootsm.boot` with Wi-Fi out |
| the link is up, 5G, modem cold | `2 015 ms` | `bootsm.boot` with Wi-Fi out and `U5_COLD` |
| the session is offered | `120` to `2 060 ms` | the same runs |

**The cold modem is the largest term**. A SUSPENDED Leaf has its modem detached to save the B cell. The first link then costs `2.0 s`. Keeping the modem attached in idle raises the SUSPENDED draw from `25 mW` to `55 mW`. The guaranteed SUSPENDED life falls from `72 min` to `33 min`. Open issue O3.

**The host pass comes first**. The safe screen waits for the host pass, because the body rails come from the host. On a dock this is `20 ms`. On Qi it is `250 ms`. On a PD contract it is `350 ms`. The rear display shows CHECKING meanwhile.

## 7 · What the user sees, step by step

The user walks from a desk dock to a vehicle. The walk takes `75 s`.

1. The Leaf leaves the dock. The face keeps the session. The rear display shows the bridge glyph.
2. A Bare Leaf drops the face to dark after `2.2 s`. The radios stay alive on the B cell.
3. A Buffer Leaf keeps the face lit for `23 min`. The user sees no change.
4. The Leaf meets the vehicle host. The rear display shows CHECKING at once.
5. The host passes in about `350 ms`. A Buffer Leaf shows no break. A Bare Leaf shows the last frame, then live.
6. A Bare-0 Leaf boots from the chain record. The safe screen shows at host pass plus `23 ms`. The live frame comes at about `2.5 s` on a cold 5G modem.

The face is never blank without a reason. The rear display and the safe screen always say what is happening.

## 8 · The proof

| Check | Result |
|---|---|
| random event sequences against P-law 1 to 3, energy and visibility | `80 000` steps, `0` violations (`python3 powersm.py --fuzz`) |
| unit tests of the states and the energy times | `42` tests pass |
| the model reproduces `bootsm.py` times | `23.2 ms`, `75.0 ms` and `120.0 ms` read, not copied |

## 9 · The open issues of this file

| No. | The issue | The owner |
|---|---|---|
| O1 | HOST_AUTH needs an AON feed from a host before the handshake. The pads are dead, so the path is the Qi coil or a seat sense. The power-path and trust teams must define it | power-path, trust |
| O2 | BRIDGE must cap the load at the session profile, `2.24 W`. A peak of `8.7 W` empties a Bare store in `0.57 s`. A cap is a visible class change | firmware, `FINAL/08` Section 8.3 |
| O3 | The cold modem costs `2.0 s` at every resume. An attached idle modem costs `30 mW` in SUSPENDED | radio, energy |
| O4 | The B cell carries the Bare tier. Its `0.18 mm` clearance and its `37 mA` charge rate are open items of `hw/energy` | energy |
| O5 | The power values of the table are `[HYPOTHESIS]` until the power-path team measures a Bare store | power-path |
| O6 | The power-path team finds that `5 J` of capacitor does not fit the body margin. A Bare store of `1.2 J` lights the face for `0.5 s`. The row Bare-1.2J of `handover_sim.py` shows the effect | power-path |
| O7 | The power-path team calls a dark body on the B cell ISLAND. Here that is the hold phase of BRIDGE and SUSPENDED. The names need one reading | power-path |
