# BUDLUM LEAF · BATTERY-FREE PANEL · AUDIT AND HARDENING

**Revision L.8 · 2026-10-20**. This is a live report. The founder's battery-free directive takes priority on every topic it covers. `[DECISION]`

## 1 · Conflict inventory before correction

The repository contains a working directive, historical investigations, active build instructions, code models and rendered artefacts.
The lists below name the conflicts, not a new product specification. A historic claim does not become active because a file preserves it.

| File or group | Conflicting statement | Correction |
|---|---|---|
| `FINAL/00`, `01`, `14` | the one-paragraph system and the product summary put the wallet, radio and cells in the surface | put identity, radios, wallet and battery in the attached Core |
| `FINAL/02` | the sample backplane uses a high-temperature carrier-glass release process | transfer from a temporary carrier onto a PC product carrier, with no product glass |
| `FINAL/03`, `04` | the four screen-battery quadrants, `12 Wh`, Qi coils, the cassette and a fixed `2.00 mm` stack | remove panel energy and give panel thickness as a measured flex result under `2.00 mm` |
| `FINAL/05`, `06` | radio windows sit in the body; the B module contains only part of the electronics | move all antennas, radios and electronics to the Core |
| `FINAL/07` | the lens uses a glass option and a temple cell not assigned to the Core | keep PC in the lens stack and put the battery in the attached frame Core |
| `FINAL/08`, `09` | the safe screen and wallet act with the module or energy cassette absent | a detached panel has no safe screen, wallet, keys or power |
| `FINAL/11`, `12`, `13`, `15`, `16` | charge, heat, tools, gates and gap rows test a battery inside the panel | retire or replace each invalid gate and work package |
| `FINAL/17`, `18`, `19`, `20` | a full-area energy sheet, dual-face cell, panel Qi coil and fixed battery geometry | keep dual-face screens, move energy and charging to the Core |
| `FINAL/21` | `128` panel micro cells and a glass micro-LED carrier | remove cell and glass; keep only verified thin PC panel technology |
| `FINAL/22` | Bare, Buffer and Full panel energy tiers and a bridge cell in the body | retire all panel energy tiers; a power gap turns the panel off |
| `FINAL/23` | a cell-powered cordless Skin, remote Core at C1/C2 and the Heartbeat/Paper layer | retire remote Core product modes and the panel energy layer |
| `HARDWARE/`, `MASTER/`, `program/`, `hw/` | old battery, mass, charge and production assumptions in active work briefs | replace live specifications; mark archived studies as historical |
| `cad/`, `pafta/`, `sim/`, `fw/`, `rtl/`, `proto/`, `mfg/` | models, sheets and tests include the old battery stack | rebase active models; label unconverted rendered outputs as obsolete |
| `BUDLUM-LEAF-DIRECTIVE.md`, `BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md` | assembled copies repeat all conflicts | generate only from corrected `FINAL/` parts |

**The detailed inventory**. `MASTER/STATE.md:27-37` presents Heartbeat and panel cells as live.
`MASTER/02-STRUCTURE-MASS-ENERGY.md:87-115` gives the old cell stack.
`HARDWARE/02-ELECTRONICS-AND-BUSES.md:14-30` puts the BMS and rectifier in the panel.
`HARDWARE/16-THE-SCREEN-PART-BY-PART.md:40-42` keeps glass and battery in the panel BOM.
`program/TEAM-BRIEF.md:25-27` calls for glass tiles and panel cells.
`hw/display/SPEC.md:59-80` selects through-glass vias.
`BUDLUM-LEAF-ARGE-PLAN.md:471-472` carries the old battery work.
`NEREDE-NE-VAR.md:1-9` calls the old battery geometry current.
Old audits and the studies of `hw/energy/`, `hw/hostpower/` and `hw/core/` are historical evidence, not active authority.
The detailed source locations come from the read-only file inventory of 2026-10-20. `[TREE]`

**The code inventory**. `hw/energy/cell/microcell.py:7-17` sizes `128` cells inside the panel.
`sim/thermal/leaf_thermal.py:9-31` allocates panel cell nodes.
`cad/leaf_v2.py:426-513` draws screen-battery quadrants and coils.
`hw/qi/qi_core.py:3-17` models panel Qi reception.
`hw/seam/seam_params.py:19-36` budgets cell and coil layers.
`fw/boot/chips.json:188-190` assigns quadrant charge control.
`program/budget.py:82-101` prices panel cells and coil.
`tools/multi_agent_optimize.py:58-64` tests the old battery geometry, and its runner rewrites the assembled directive.
The code inventory finds `21` of `25` sheets with old battery or Qi content.
No new battery-free CAD, firmware or sheet build is verified yet. `[TREE]`

**The weakest first fault**. A battery-free panel has no power during a Core exchange. No safe screen remains on the detached panel.
The session must live in the Core and in B.U.D., not in panel memory. `[DECISION]`

## 2 · H1 to H12 status board

| Task | Status | Risk or result | Evidence |
|---|---|---|---|
| H1 panel-resident parts | **NEEDS TEST** | driver trace and bend analysis determines minimum silicon | `hw/panelfree/link/` |
| H2 power and data link | **NEEDS TEST** | a sealed attach zone must carry video and power | `hw/panelfree/link/` |
| H3 power and runtime | **NEEDS TEST** | large and dual-face members can exceed a portable Core | `hw/panelfree/core/` |
| H4 PC stack | **NEEDS TEST** | a standard hot TFT process exceeds the PC heat limit | `hw/panelfree/stack/` |
| H5 scratch | **NEEDS TEST** | a hard coat can fail under repeated bends | `hw/panelfree/stack/` |
| H6 barrier | **NEEDS TEST** | a PC carrier alone cannot seal OLED from water | `hw/panelfree/stack/` |
| H7 mechanical | **NEEDS TEST** | inorganic crack and edge peel set the dynamic radius | `hw/panelfree/stack/` |
| H8 Core | **NEEDS TEST** | `60 W` wireless power needs a heat and charge limit | `hw/panelfree/core/` |
| H9 security | **NEEDS TEST** | a passive panel has no secret for cryptographic self-authentication | `hw/panelfree/trust/` |
| H10 glasses | **NEEDS TEST** | frame heat and prescription optics need a head-form test | `hw/panelfree/glasses/` |
| H11 patents | **NEEDS TEST** | no patent-free path is certified by a web search | `hw/panelfree/patents/` |
| H12 consistency | **NEEDS TEST** | the old files remain until rewritten or retired | this report and the gate results |

## 3 · Release gates and the weakest points

1. **The power and data attach is the first weak point.** A zone without either channel cannot carry an image. H2 measures the channel at all positions.
2. **The PC stack is the second weak point.** H4 to H7 measure cracks, edge ingress, coat fatigue and TFT yield.
3. **The energy density is the third weak point.** H3 states runtime for each size, not one "all day" claim.
4. **The Core thermal path is the fourth weak point.** H8 measures peak compute and `60 W` charging separately.
5. **Patent clearance is open.** H11 can name a design-around, but only counsel can clear production.

**The baseline tests**. The code inventory ran `19` boot state tests with `19` passes.
The full boot suite has `2` import errors because `cryptography` is absent.
The wallet test suite passes `23` integration tests. The protocol suite cannot import `google.protobuf`.
These are baseline tool results, not tests of the new architecture. `[TREE]`

**The release rule**. No result becomes a public claim without a measured gate, a raw record and a date. `[DECISION]`
