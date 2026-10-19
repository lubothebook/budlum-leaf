# BUDLUM LEAF · HOST POWER · THE TEAM BRIEF

**Revision L.6.1 (proposed) · 2026-10-19 · the Program Lead**. Every team of `hw/hostpower/` reads this brief first. It is the charter of Part 22.

## 1 · The order

Ayaz, 2026-10-19: *"Donanım çalıştığı sürece çalışabilecek bir cihaz aslında bir ilktir. Asıl pil donanımda olsa ve sürekli Budlum Leaf çalışsa ne olacak? Bataryanın kapasitesi önemli olmuyor."* The order is to think how to set this up in the best way, and to write it into the program. `[DECISION]`

## 2 · The thesis

**The Host Life Law**. On a host, a Leaf lives as long as the host lives. The cell stops being the source of the Leaf's life and becomes the bridge between two hosts. `[DECISION]`

| The idea | The L.6.0 reading | The host-power reading |
|---|---|---|
| where the energy lives | `5.9` to `7.4 Wh` in the body | in the place: a dock, a vehicle, a desk, a machine, a worn pack |
| what the cell is for | the run time | the ride-through between hosts, and the safe end of a session |
| what limits the day | `2` to `3.7 h` of a delta or video session | the host, which is a wall, a vehicle or a pack |
| where the heat comes from | cells, charge loss and the session | the session and the interface loss only |

## 3 · The four corrections to hold, with no pride

1. **Capacity does not vanish. It moves.** A host has a cell or a wall. The honest sentence is: the Leaf stops paying for capacity in grams, millimetres and heat.
2. **"First" is a claim, and a claim needs a gate.** Tethered glasses and USB-C monitors run on a host today. The claim that can survive is a combination. It joins a wallet surface, a chain session, a bridge cell and a power hand-over. Team `study` settles the wording.
3. **Power is a door.** A host that feeds the Leaf must never gain authority over it. The dead-pad law of `fw/boot` covers the power pads too.
4. **The heat law still binds.** The skin limit is `36.2 °C`. Qi2.2 at `25 W` puts `5.8` to `6.9 W` of heat in the body. Contact puts about `0.1` to `0.34 W`. The interface decides if always-on is possible.

## 4 · The three energy tiers

| Tier | The store in the body | The job | The sentence |
|---|---|---|---|
| **Bare** | a capacitor store of seconds | lives on a host only, ends a session cleanly | *a surface, not a device* |
| **Buffer** | a few of the `128` micro cells, about `0.3` to `1.5 Wh` | walks between hosts, minutes of a session | *the bridge* |
| **Full** | all `128` cells, `5.9` to `7.4 Wh` (L.6.0) | hours with no host | *the freedom* |

The tiers are a decision for the teams to test, not a claim. `[HYPOTHESIS]`

## 5 · The four conditions of the law

1. **Power**: `P_host >= P_load + P_topup`, with the worst peak at `8.7 W` and the path loss included.
2. **Heat**: the hottest face point stays at or under `36.2 °C` for the whole session.
3. **Trust**: the host never touches the secure rail, the wallet or the data lanes before its handshake passes.
4. **Continuity**: `E_buffer >= P_peak x t_handover`, and a power gap never loses chain state.

## 6 · The source files to read

| The topic | The files |
|---|---|
| the decisions | `FINAL/21-stretch-stem-and-projection.md`, `FINAL/17-energy-architecture.md` |
| the energy and the power tree | `hw/energy/` (`03`, `04`, `05`), `budget/runtime.py`, `pack/network.py` |
| the heat | `sim/thermal/leaf_thermal.py` and its `README.md` |
| the dock | `hw/dock/` |
| the firmware states | `fw/boot/STATE-MACHINE.md`, `fw/boot/bootsm.py`, `fw/boot/ZERO-CPU.md` |
| the network and the validator | `FINAL/21` Section 21.5, `validator/leaf-duty`, `proto/`, `net/discovery` |
| the rules | `program/TEAM-BRIEF.md`, Section 3 |

## 7 · The rules of every team

1. **Write only inside your own directory** of `hw/hostpower/`. Read everything. Do not edit `FINAL/`, `HARDWARE/`, `MASTER/`, `tools/` or another team's files. Do not run git.
2. **Never downgrade a target.** If a target is hard, design the most ambitious real path and say what it needs.
3. **Prove a number with code.** Use `python3` with numpy, scipy and matplotlib. A number without a script is `[HYPOTHESIS]`. Reuse the models of other directories by import, read only.
4. **Tag every claim**: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]` with the source, `[GENERAL]`, `[TREE]`. A `[PUBLICATION]` needs a real source. Do not invent one.
5. **Honesty beats a good story.** If your result weakens the thesis, say so first. The program needs the true answer.
6. **Prose rules for every `.md`**: see `program/TEAM-BRIEF.md`, Section 3, rule 5. Check with `python3 tools/check_prose.py <file>`.
7. **Each team writes a `README.md`**: the files, how to run, key results, open issues and proposed gates with pass conditions.
8. **Naming law**: write "Budlum Leaf" and the size. Never call it a phone, tablet or computer in a claim.
9. **Report** in your final message: the files, the five key numbers, the thesis damage if any, and the open issues. Keep it under `350` words.

## 8 · The standing after the studies (2026-10-19)

The five studies ran against this brief. Part 22 of the directive holds the result. Two statements of this brief changed.

1. **Section 3, item 3 and Section 5, condition 3**. The host that powers the handshake touches the bridge rail first. The corrected rule: the host never touches the wallet, the signing core, the firmware slots or the data lanes.
2. **Section 5, condition 2**. In free air no interface holds `36.2 °C` in a delta session. The dock plate holds every case.
3. **Section 4, the Buffer range**. The range of `0.3` to `1.5 Wh` carries the delta class only. The `8.7 W` peak needs about `3.1 Wh`.
4. **Gate names**. The seats proposed `52` gates under the prefixes `HST-`, `HST-T`, `HST-C` and `HPS-`. Part 22 merges them into `HST-1` to `HST-29`. The seat files keep their own names.
