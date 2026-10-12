# BUDLUM LEAF · FW/BOOT · THE DEAD-PAD AND SAFE-SCREEN STATE MACHINE

**Revision L.6.0 · 2026-10-12 · Firmware-Integrity team**. The model is `bootsm.py`. Tests: `tests/test_bootsm.py`. Targets: `FINAL/08` Section 8.2.

## 1 · The two laws

1. **The dead-pad law**. Every seam leaf and every B pad stays at `0 V` until its handshake passes. `[DECISION]` ENR-19, MON-16.
2. **The safe-screen law**. Every fault ends in a stated, visible state. A Leaf is never a brick. `[DECISION]` `FINAL/08` Section 8.2.

## 2 · Who does what with no CPU

| Job | Part | Why that part |
|---|---|---|
| wakes first, sequences rails, holds every reset and gate | `U4` ROM | it runs on the ring cell before anything else |
| root of trust, challenge of every pad, every measurement | `U7` | it holds the keys and the floors |
| the safe screen | the `U1` ROM path | a hardware path with no updatable code |
| the last resort | the flash LED, blinked by `U4` ROM | it needs neither `U1` nor `U7` |

## 3 · The states

```text
DEAD ──wake──▶ WAKE ──▶ ROOT ──▶ PAD_AUTH ──▶ SAFE_SCREEN ──▶ VERIFY ──▶ ATTEST ──▶ LINK ──▶ ANCHOR ──▶ SESSION
                         │          │              │                        │          │         │
                         ▼          ▼              ▼                        ▼          ▼         ▼
                     SE_FAULT   REAR_ONLY      LED_CODE                 SLOT_B     RECOVERY   ANCHOR_STATED
                                                                        (retry)    UPDATE_    STREAM_REFUSED
                                                                                   REQUIRED
```

| State | Entry | What happens | Exit |
|---|---|---|---|
| DEAD | rest | all `64` seam leaves and `12` B pads at `0 V` | a touch, the button, a Qi field or a seat event |
| WAKE | the event | the ring cell powers `U4` ROM, `U7` and `U1` | `U4` ROM up at `1 ms` |
| ROOT | `U4` up | the `U7` ROM checks `U7` slot A, then slot B | `U7` up, or SE_FAULT |
| PAD_AUTH | `U7` up | `U7` challenges the `12` B pads, then each quadrant by seam distance | the seat quadrant at VSYS, or REAR_ONLY |
| SAFE_SCREEN | the seat quadrant powered | the `U1` ROM draws the battery, the wallet, the class line and the part lines | always continues |
| VERIFY | `U7` up | ed25519 of the installed manifest and its stored digest | continues; a revoked release is marked |
| ATTEST | the radio domain powered | direct hashes, DICE reports, signed reports; gates open on PASS | slot B, or LINK |
| SLOT_B | `U6`, `U1` microcode or every link radio refused | the radio and stream domain restarts on slot B | ATTEST again |
| LINK | one link radio passed | the path manager of LF-1 picks the path | ANCHOR, or UPDATE_REQUIRED |
| ANCHOR | the link | the stored anchor is compared; the stream key is checked (SW-22) | SESSION, or a stated refusal |
| SESSION | all checks | the session offer of step 4 | SESSION or SESSION_STATED |

## 4 · The floor states

| State | Cause | The surface | What it says and offers |
|---|---|---|---|
| SE_FAULT | `U7` slots A and B refused | the rear panel, on the ring cell | wallet locked; service recovery on a Budlum service seat |
| REAR_ONLY | the B pads or the seat quadrant refused | the rear panel | body refused at the seat; reseat or swap the quadrant |
| LED_CODE | `U1` silicon dead | the flash LED | a blink code read by the service tool |
| RECOVERY | `U6`, `U1` microcode or both link radios lost in both slots | the face | no stream path; recovery through the port part or the dock |
| UPDATE_REQUIRED | the installed release is revoked on chain | the face | only the update class runs; the wallet stays usable |
| ANCHOR_STATED | the trust anchor differs | the face | re-anchor through a second channel, as in Part 8 |
| STREAM_REFUSED | the stream key is not an active validator | the face | the safe screen only (SW-22) |
| SESSION_STATED | any part refused, but a session is possible | the face | one line per refused part or quadrant |

## 5 · The dead-pad order

1. `U7` challenges the `12` B pads. The seat quadrant closes at `12 ms`.
2. The two neighbours of the seat close next, in parallel, at `15 ms`.
3. The diagonal quadrant closes through either neighbour at `18 ms`.
4. A refused quadrant stays dead. The diagonal still closes through the other neighbour.
5. Each answer carries the hash of the quadrant node firmware and the tile tables.

`test_diagonal_reached_round_the_other_side` checks step 4.

## 6 · The times

`python3 bootsm.py` gives these values. Every step time is `[HYPOTHESIS]` until the bench measures it.

| Milestone | Target (Part 8) | Model, nominal | Model, worst stated case |
|---|---|---|---|
| step 1: manifest checked by `U7` | `20 ms` | `15.0 ms` | `23.0 ms` with `U7` on slot B |
| step 2: safe screen on the panel | `60 ms` | `23.2 ms` | `31.2 ms`, all `2 x 65 536` fault sets under `60 ms` |
| step 3: link up | `150 ms` | `75.0 ms` on 5G, `123.7 ms` on Wi-Fi only | `214.3 ms`: `U7` on slot B, a slot B restart, Wi-Fi only |
| step 4: session offered | `300 ms` | `120.0 ms` | `259.3 ms` in the same case, under `300 ms` in every swept set |

**Step 3 in a fault case**. A slot B restart misses `150 ms`. The link is then a stated, late link, never a silent one. Only a multi-fault boot reaches it.

**The 5G resume**. The modem stays attached in standby and resumes in `60 ms`. A cold modem takes over `1.5 s`. The Wi-Fi path then meets step 3 alone.

**Step 1 with `U7` on slot B**. It takes `23 ms`, over the `20 ms` target. The safe screen still lands at `31 ms`. The fix is a faster `U7` boot. A `U7` slot check of `6 ms` meets `20 ms` again. `[HYPOTHESIS]` open issue O5.

## 7 · The proof of the law

`bootsm.sweep()` runs every subset of `16` faults, in normal and in trial mode. That is `131 072` boots. A random test adds `40 000` boots over all `29` faults. Every boot meets seven invariants:

| Invariant | The rule |
|---|---|
| I1 | the end state is visible |
| I2 | a safe screen, rear screen or LED code shows within `60 ms` |
| I3 | the wallet is up exactly when `U7` booted |
| I4 | every refused part is named on a stated line |
| I5 | a session with a refused part is a stated session |
| I6 | no session runs without `U6` and the `U1` microcode |
| I7 | a fault never yields a silent session, except a latent fault in an unused slot B |

**Result**: `0` violations. **The latent slot B fault**. A bad copy in the unused slot does not change the boot. The rest-time scrub of `U7` finds it and repairs it.

## 8 · The trial boot

1. After an install, the next boot runs the new slot as a trial.
2. Any refused part reverts the whole set to the previous slot.
3. A reverted trial leaves every floor unchanged.
4. A clean trial that reaches SESSION lets `U7` commit and raise the floors.

## 9 · The gates

| Result | Gate |
|---|---|
| the safe screen inside `60 ms` for every fault set | the boot matrix, `FINAL/08` Section 8.8 step 6 |
| pads at `0 V` until the handshake | ENR-19, MON-16 |
| a stream key outside the active set | SW-22 |
| a refused part shows its failing field | refusal R5 of `FINAL/08` Section 8.7 |
| the zero-frame handover keeps the session | DST-12, outside this boot model |
