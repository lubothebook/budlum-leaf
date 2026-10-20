# BUDLUM LEAF · BATTERY-FREE PANEL · THE TEAM BRIEF

**Revision L.8 candidate · 2026-10-20 · the Program Lead**. Every seat of `hw/panelfree/` reads this brief first. It is the charter of Part 24. `[DECISION]`

## 1 · The order (the directive of the founder, 2026-10-20)

**The Leaf panel contains no battery.** The panel works only when the core module (the camera module, here "the Core") is attached. Without the Core the panel is passive.

| The Core holds | The panel holds |
|---|---|
| camera, all antennas (cellular, Wi-Fi, Bluetooth, UWB, GNSS), battery, SoC, memory, storage | the emissive layer (OLED or micro-LED) |
| power management, charging input, display controller, timing controller | the TFT backplane |
| secure element and keys | the touch sensor |
| every sensor that needs no fixed place on the panel | the encapsulation and barrier layers |
| | the polycarbonate carrier and the scratch-resistant hard coat |
| | the interconnect traces to the attach zones |
| | the minimum driver silicon, only if analysis proves it cannot move to the Core |

Rules fixed by the directive:

1. The panel must be as flexible, scratch resistant and durable as a polycarbonate carrier permits. The panel has no thickness target. `2 mm` is an upper limit. Make the panel as thin as the flex goals need.
2. Polycarbonate is the carrier and the outer layer. Glass is not a candidate anywhere in the panel.
3. The Core has the charging input: about `60 V` input rating and `60 W` wireless charging. The Budlum charging base (the transmitter) stays in scope.
4. An auxiliary magnetic battery module attaches to the Core, never to the panel.
5. The Core attaches to the panel edge, the front face, the rear face or a glasses frame. Each attach position must deliver power and data to the panel.
6. One Core drives panels of any size and shape: carried member, small and large surfaces, glasses, dual-face panel. The dual-face panel stays in scope. The Core powers both faces.
7. All other Leaf rules stay: Linux and free software, hardware openness, patent rules, B.U.D. storage.

## 2 · The reference members (the naming law holds: write "Budlum Leaf" and the size)

| The member | The geometry | The pixels | The refresh | The directive class |
|---|---|---|---|---|
| Leaf Frame lens | one clear lens per eye, about `50 x 40 mm` blank, prescription | the glasses seat decides | the glasses seat decides | glasses |
| Leaf 80 | `80 x 80 mm` | `1 600 x 1 600` at `508 ppi` | `144 Hz`, variable to `1 Hz` | small |
| Leaf 160 | `160 x 80 mm` | `3 200 x 1 600` at `508 ppi` | `144 Hz`, variable to `1 Hz` | the carried member |
| Leaf 160² | `160 x 160 mm` | `3 200 x 3 200` at `508 ppi` | `144 Hz`, variable to `1 Hz` | the tablet class |
| Leaf 480 | `480 x 240 mm` | `2 880 x 1 440` at `152 ppi` | `144 Hz`, variable to `1 Hz` | the desk class |
| Leaf 1400 and 2800 | `1 400 x 800` and `2 800 x 1 600 mm` | `61 ppi` | `120 Hz` and `60 Hz` | the wall class, mains only |
| Dual-face | any member, two faces back to back | two frames | per face | the second face |

The wall class draws `73 W` and more. A battery-free panel on a small Core cannot carry it. Say so with numbers.

## 3 · What is already settled, and what the directive retires

Settled and kept: PC carrier, `508 ppi`, `144 Hz`, Linux, free software, B.U.D., the secure element and the `fw/u7` wallet.
The lease rule of Part 11 and the naming law stay.

Retired by this order (do not design with them):

1. The battery quadrants, the `128` rotating tiles, the micro cells, the energy sheet and the cassette are retired. The panel has no cell.
2. The glass micro-LED tile carriers of L.6.0. The directive refuses glass.
3. The Heartbeat Law, the Paper layer, the host-power tiers Bare, Buffer and Full, the cordless Skin. They put a cell in the panel.
4. The far Core at kilometres (C1 and C2 of Part 23). The Core is attached to the panel. The Core reaches validators by its own radios.
5. The B module of `4.00 mm` with a `1.00 mm` bar as the whole Core. The Core is larger now. The seats decide the size from the battery volume.

The existing studies of `hw/hostpower/`, `hw/core/`, `hw/energy/`, `hw/dock/`, `hw/rf/`, `hw/display/`, `sim/` are inputs. Read them, import their models read only, and say when a number is stale.

## 4 · The seats and the directories

| Seat | Directory | The tasks (the directive section) |
|---|---|---|
| S1 Stack | `hw/panelfree/stack/` | H4 low-temperature stack on polycarbonate, H5 scratch resistance, H6 barrier, H7 mechanical durability |
| S2 Link | `hw/panelfree/link/` | H1 panel-resident parts and the driver ICs, H2 the Core-to-panel link and the attach zones |
| S3 Core | `hw/panelfree/core/` | H3 power budget and runtime, H8 Core design (volume, heat at `60 W`, chemistry, magnets, drop, seal) |
| S4 Trust | `hw/panelfree/trust/` and `hw/panelfree/glasses/` | H9 security, H10 glasses |
| S5 Patents | `hw/panelfree/patents/` | H11 patent-free path for each decision |

One seat writes in one directory. The Lead writes `FINAL/`, `HARDWARE/`, `MASTER/`, `tools/`, `program/`, `AUDIT/`, `DECISIONS.md` and the questions file.

## 5 · The result format

For each numerical claim show the calculation (a script and its output) or give the source (a real URL or paper that you opened). Mark every result as one of:

| Mark | The meaning |
|---|---|
| **DECIDED** | the numbers close, the physics holds, the seat picks it |
| **NEEDS TEST** | the numbers close on paper, a named test decides it |
| **NOT FEASIBLE** | the physics or the numbers refuse it. Give the number that refuses it, and the nearest feasible path |

## 6 · The rules of every seat

1. **Write only inside your own directory.** Read everything. Do not edit another seat's files, `FINAL/`, `HARDWARE/`, `MASTER/`, `tools/`. Do not run git.
2. **Never downgrade a target to make it pass.** Design the most ambitious real path. If it fails, write the failing number first, then the nearest path that holds.
3. **Prove a number with code.** Use `python3` (numpy, scipy and matplotlib are installed; shapely and trimesh are not). A number without a script is `[HYPOTHESIS]`. Run each script and keep its output in `out/`.
4. **Tag every claim**: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]` with the source, `[GENERAL]`, `[TREE]`. A `[PUBLICATION]` needs a real source that you opened with WebSearch or WebFetch. Never invent a source, a part number or a figure. If you cannot verify a published value, tag it `[HYPOTHESIS]` and write "unverified".
5. **Honesty beats a good story.** If a result weakens the architecture, say so first. The Lead needs the true answer, and the weakest point most of all.
6. **The prose rules apply to every `.md`** in present tense. Use no em dash and at most 25 words per sentence.
   Use at most 20 words per step and 25 words per cell. Run `python3 tools/check_prose.py <file>` (read only).
7. **Naming law**: write "Budlum Leaf" and the size. Do not write phone, tablet or computer in a claim.
8. **Each seat writes a `README.md`**: list the files, the run command, marked results, open issues and proposed gates.
   The Lead renumbers the gates.
9. **Cross-seat inputs.** S3 owns the panel power model. S2 owns the link data rate and loss. S1 owns the stack and the strain. If you need another seat's number, use the stated placeholder of Section 7 and mark it. The Lead reconciles in task 2.
10. **Report** in fewer than `400` words: files, five key numbers with marks, architecture damage and open issues.

## 7 · Placeholders for cross-seat numbers (replace them when the owner publishes)

| The input | The placeholder | The owner |
|---|---|---|
| Leaf 160 panel power, display and address, typical and maximum | `0.8 W` and `2.5 W` | S3 |
| Leaf 160 pixel data, uncompressed `8 bit` RGB at `144 Hz` | `17.7 Gbit/s` (`3 200 x 1 600 x 24 x 144`) | S2 |
| the link power loss | `15 %` at the attach zone | S2 |
| the panel stack thickness, one face | `0.30 mm` | S1 |
| the Core reference envelope | `70 x 30 x 10 mm` bar, `19.5 cm³` after the corner radii | S3 |

## 8 · The source files to read first

| The topic | The files |
|---|---|
| the old panel and stack | `FINAL/02-panel.md`, `FINAL/03-body.md`, `FINAL/18-screen-fold-seal.md`, `HARDWARE/12-THE-BEND-LAW.md` |
| the old energy | `FINAL/04-energy.md`, `FINAL/17-energy-architecture.md`, `FINAL/22-host-power-and-the-living-leaf.md`, `FINAL/23-core-skin-and-the-heartbeat.md` |
| the Core study of the Split | `hw/core/` (`link`, `power`, `heat`, `trust`, `parts`, `far`) |
| the module | `FINAL/06-module.md`, `FINAL/20-charge-path-and-both-face-module.md`, `FINAL/21-stretch-stem-and-projection.md`, `HARDWARE/05`, `HARDWARE/13` |
| the clear family and the glasses | `FINAL/07-frame-field.md`, `FINAL/17-energy-architecture.md` Section 17.8 |
| the security | `FINAL/22` Section 22.8, `FINAL/23` Section 23.7, `fw/boot/`, `fw/u7/`, `hw/hostpower/trust/`, `hw/core/trust/` |
| the heat | `sim/thermal/`, `hw/hostpower/thermal/`, `hw/core/heat/` |
| the rules | `program/TEAM-BRIEF.md` Section 3, `FINAL/19` (patents and the ledger) |
