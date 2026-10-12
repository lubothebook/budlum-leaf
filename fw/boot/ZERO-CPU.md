# BUDLUM LEAF · FW/BOOT · THE ZERO-CPU COMPLIANCE ARGUMENT

**Revision L.6.0 · 2026-10-12 · Firmware-Integrity team**. The data is `chips.json`. The check is `zero_cpu.py`. Tests: `tests/test_zero_cpu.py`.

## 1 · Ayaz's rule, as written

`FINAL/21` Section 21.5.1 `[DECISION]`:

1. Leaf has no general-purpose application processor and no operating system.
2. It runs no third-party code.
3. Fixed-function silicon with signed firmware is allowed.
4. The allowed parts: radios, modem, video decoder, TCON, ISP, power chip and secure element.
5. A frame store is allowed, because a decoder needs one.

## 2 · What makes a core "not general-purpose"

A small core inside a part is not a CPU of the Leaf when all six tests hold. `[DECISION]`

| Test | The rule | Why it separates firmware from a CPU |
|---|---|---|
| Z1 bounded job | a fixed list of at most `6` jobs, and no input carries instructions | a CPU takes new jobs; this part cannot |
| Z2 no OS shown | nothing outside the part sees a process, an API or a scheduler | an OS hosts programs; a scheduler inside a modem hosts none |
| Z3 no third-party code | the code comes from the chip vendor and Budlum only | no application, user or validator code ever executes |
| Z4 data only | no interpreter, no script, no JIT, no applet loader | data cannot become a program on the device |
| Z5 signed and measured | every code store is signed and `U7` measures it | the code on the device is the code the chain approved |
| Z6 gated | the outputs stay closed until `U7` passes the part | an unknown image reaches no antenna, pixel or speaker |

**The test of a general-purpose processor**. A processor is general-purpose when someone other than its maker can give it a new program. On the Leaf, nobody can. The validators send pixels, layers, glyphs and packets. They never send code. `[DECISION]`

## 3 · The verdict, part by part

Output of `python3 zero_cpu.py --markdown`:

| Part | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 | Verdict |
|---|---|---|---|---|---|---|---|
| `U7` secure element | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U4` power and dead-pad chip | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U1` TCON and local compositor | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U6` slice decoder and frame store | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U2A` Wi-Fi 7 and BT 6.0 combo | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U2B` 60 GHz and UWB | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U5` 5G standalone modem | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `EUICC` eSIM (eUICC) inside U5 | ok | ok | **no** | **no** | ok | ok | OPEN |
| `U3` audio codec | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `U8` IMU | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `CAM` 50 MP sensor and raw path | ok | ok | ok | ok | ok | ok | PASS |
| `RDISP` rear round AMOLED driver | ok | ok | ok | ok | ok | ok | PASS |
| `QN` quadrant node (x4) | ok | ok | ok | ok | ok | ok | CONDITIONAL |
| `PORT` port part U_PD | ok | ok | ok | ok | ok | ok | CONDITIONAL |

CONDITIONAL means the part passes when the supplier meets the conditions below. They go into the purchase specification.

## 4 · What code runs where

| Part | The code | Where it lives | Why it is not a CPU | The condition to buy |
|---|---|---|---|---|
| `U7` | native wallet and verifier firmware, `384 KiB` | inside `U7`, slots A and B | five jobs, it is the gate itself | no Java Card VM, no applet loader |
| `U4` | mask ROM, OTP trim, `32 KiB` patch | `U4` OTP and patch area | rail and pad sequencing only | the ROM alone powers the safe screen path |
| `U1` | safe-screen ROM, `256 KiB` timing and warp microcode | ROM, boot NOR | it moves, picks and composes layers; it runs no program (21.5.6) | the ROM path works with no microcode |
| `U6` | `1 MiB` decoder control firmware | boot NOR | it decodes slices; a slice is data | DICE or an owner-key boot |
| `U2A` | `4 MiB` radio firmware | boot NOR | MAC, PHY, association, framing | a hostless variant, DICE or owner key |
| `U2B` | `1.5 MiB` radio firmware | boot NOR | the dock link and ranging | DICE or owner key |
| `U5` | `48 MiB` modem firmware with a real-time scheduler | in-package NAND | the 3GPP stack, nothing else | owner key in OTP, signed report, SIM toolkit off |
| `U3` | `128 KiB` codec and voice-mask firmware | boot NOR | fixed filters; coefficients are data | program RAM locked after boot |
| `U8` | `16 KiB` state-machine settings | boot NOR | a sensor with fixed gesture states | settings lock after load |
| `CAM` | `8 KiB` register settings | boot NOR | a sequencer with no program core | none |
| `RDISP` | no code, OTP gamma only | inside the driver | no core | none |
| `QN` | `64 KiB` Qi receiver firmware per quadrant | quadrant flash | the Qi2.2 protocol only | the hash rides in the `3 ms` answer |
| `PORT` | `64 KiB` USB-PD firmware | port flash | the PD protocol only | its own product manifest |

All sizes are `[HYPOTHESIS]` until the supplier data sheets arrive.

## 5 · The schedulers inside parts

`U2A`, `U2B` and `U5` run a vendor scheduler inside the part. **This is not an operating system of the Leaf**. `[DECISION]`

1. It schedules the radio's own tasks. It hosts no program from outside.
2. No interface of the Leaf exposes a task, a file or a call.
3. Section 21.5.1 names the radios and the modem as allowed parts.
4. The test is Z2: nothing outside the part sees the scheduler.

## 6 · The one open case: the eSIM

The 5G path needs a USIM. A public 5G network refuses a device without one `[PUBLICATION]` 3GPP TS 33.501. The eUICC is a smart card with a card OS. An operator profile can carry operator applets. Those applets are third-party code, and they run inside the card.

**The most ambitious path that keeps the rule**. `[DECISION]`, pending Ayaz's ruling:

1. The eUICC is a sealed credential card. Its code never reaches a bus of the Leaf.
2. The `U5` firmware drops every SIM toolkit proactive command. A card applet cannot draw, call, send or open anything.
3. `U7` refuses a profile whose metadata lists toolkit applets, when the profile is installed.
4. The answer of the card is authentication data only.

**The ruling needed**. Ayaz decides whether a sealed credential card is inside the rule. If not, the 5G path needs a non-SIM credential. 3GPP allows that only on a standalone non-public network `[PUBLICATION]` 3GPP TS 23.501 Release 17. That loses the public 5G outdoors path of `DST-11`.

## 7 · What the rule forbids, and how the Leaf holds it

| Forbidden | How the design holds it |
|---|---|
| an application processor | none on the part list; every listed core passes Z1 |
| an operating system | none hosts a program; Section 5 |
| third-party code | signers are vendor and Budlum only (Z3); the eSIM is the open case |
| code from the network | validators send data only; `U7` accepts code only through a release on chain |
| a silent swap of firmware | Z5 and Z6: measured and gated |

## 8 · The gates

SW-21 holds the compositor to "no program run". SW-22 holds the stream to active validators. ENR-19 holds the pads at `0 V`. The proposed FW-1 to FW-3 of `MODEL.md` hold the firmware.
