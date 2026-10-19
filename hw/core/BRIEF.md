# BUDLUM LEAF · CORE AND SKIN · THE TEAM BRIEF

**Revision L.7 candidate · 2026-10-19 · the Program Lead**. Every seat of `hw/core/` reads this brief first. It opens block `HP-2`. It is a study. It changes no L.6.0 or L.6.1 decision until Ayaz rules. `[DECISION]` for the study, `[HYPOTHESIS]` for every result.

## 1 · The order

Ayaz, 2026-10-19, second message: keep all the components of the screen in a separate hardware. The screen then costs less. One hardware serves many screens. The screen is lighter. A part change happens in the hardware and not in the screen. Ayaz wants something extreme, new and unique, and says time is plentiful.

## 2 · The idea in the words of the program

**The Split**. The Leaf divides into two things.

| The part | The name in this study | What it holds |
|---|---|---|
| the surface | **the Skin** | the emitters, the tile drivers, a link, a minimal decoder, an identity. Nothing that can sign |
| the hardware | **the Core** | the silicon, the radios, the secure element, the energy, the camera processing, the validator role |

The Core is the host of Part 22. The host and the device become one idea: the Core is the device and the Skin is its window. `[DECISION]` for the study.

## 3 · What the Lead already measured

| The number | The value | The source |
|---|---|---|
| raw pixel stream, `1600 x 3200`, `240 Hz`, `10 bit` | `36.9 Gbit/s` | the Lead, arithmetic |
| the same stream at `3:1`, `4:1`, `6:1` | `12.3`, `9.2`, `6.1 Gbit/s` | the Lead, arithmetic |
| the surface load, delta and video | `0.80 W` and `1.35 W` | `hw/energy/04-ENERGY-BUDGET.md`, body column |
| the silicon and radio load, delta and video | `1.22 W` and `1.92 W` | the same, ring column |
| the sustained free-air load of the L.6.0 body | `1.73 W` still, `2.37 W` light wind | `hw/hostpower/thermal/` |

**The reading**. The pixel link decides if the Split lives. The heat reading is good: the surface-only load passes the free-air limit in a delta and a video session. Both are `[HYPOTHESIS]`.

## 4 · The corrections to hold, with no pride

1. **The Skin is never empty.** Pixels must arrive. A link and some decoder stay on the surface. The question is the smallest honest Skin.
2. **Splitting a compute pack from a display is not new.** Compute packs and pucks exist. The seat `study` finds what is still open.
3. **The camera sensor stays where the optics are.** The Core takes the processing, not the lens.
4. **The Skin shows everything.** A rogue Skin reads every pixel. The pairing and the link key are the whole trust model.
5. **A tether is a product.** A cable or a radio link has a failure rate, a price and a heat. The link seat prices them.
6. **The Core is a single point.** One Core serves many Skins, so one failure darkens all of them. The session seat reads that cost.

## 5 · The candidates for what is unique

The Lead holds these as questions to test, not as claims.

1. **One wallet, many surfaces.** A stolen Skin holds no key and is worth a piece of glass.
2. **A chain-attached Skin.** The chain records the paired Core, so a Skin roams with its session.
3. **The Core is a validator.** The room is the network node. This joins Part 21 Section 21.5 and Part 22.
4. **The part record on every part** (law L9) lets a Core part change without touching a Skin.
5. **One Core drives the whole family**: Leaf 80, 160, 480 and the Frame. The size is the Skin.

## 6 · The seats and their directories

| Seat | Directory | The question |
|---|---|---|
| link (new) | `hw/core/link/` | the pixel link, the tether options, the smallest Skin |
| power | `hw/core/power/` | the Skin power tree, the Core energy, N Skins on one Core |
| heat | `hw/core/heat/` | the heat of the Skin alone and of the Core alone |
| trust | `hw/core/trust/` | the zero-key Skin, the pairing, the link key, the rogue Skin |
| session | `hw/core/session/` | one session on many Skins, a Skin that roams, the Core as a failure point |
| study | `hw/core/study/` | the prior art, the unique join, the cost and the break-even of N Skins |

## 7 · The rules of every seat

1. **Write only inside your own directory** of `hw/core/`. Read everything. Never edit `FINAL/`, `HARDWARE/`, `MASTER/`, `tools/`, `hw/hostpower/` or another seat's files. Do not run git.
2. **Never downgrade a target.** Design the most ambitious real path and say what it needs.
3. **Prove a number with code.** Reuse the models of `hw/hostpower/` and `sim/` by import, read only.
4. **Tag every claim**: `[DECISION]`, `[HYPOTHESIS]`, `[PUBLICATION]` with a real source, `[GENERAL]`, `[TREE]`.
5. **Honesty beats a good story.** If your result kills or narrows the Split, say so first.
6. **Prose rules**: see `program/TEAM-BRIEF.md`, Section 3, rule 5. Check with `python3 tools/check_prose.py <file>`.
7. **Each seat writes a `README.md`**: the files, how to run, key results, open issues and proposed gates with pass conditions.
8. **Naming law**: write "Budlum Leaf". Never call it a phone, tablet or computer in a claim.
9. **Report** in the final message: the files, five key numbers, the damage to the Split, and the open issues. Keep it under `350` words.
10. **Install nothing outside your user space.** If a package is missing, say which one in the README.

## 8 · The distance order (Ayaz, 2026-10-19, third message)

Between the hardware and the device there can be kilometres. The antenna of the Core can be large. The Leaf keeps its antennas where the designs show them: the bar and the ring of the B module, and the 5G modem. No design of the Leaf changes. `[DECISION]`

**What the Lead draws from it**. All of it is `[HYPOTHESIS]` until a seat tests it.

1. **Three distance classes.** C0 is a contact or a tether, up to `2 m`. C1 is a room, up to about `30 m`. C2 is far, up to kilometres.
2. **The pixel link fails at C2.** `6` to `12 Gbit/s` does not cross a kilometre to a Leaf antenna. Slice streams of tens to about `150 Mbit/s` do. Part 21 designed this: the decoder, the frame store and the local compositor stay on the Leaf.
3. **The minimal Skin is a C0 and C1 idea.** At C2 the Skin is the L.6.0 Leaf. The Core is a validator.
4. **The energy host and the compute host are two hosts.** Power does not travel kilometres. At C2 the energy is local, in the Leaf cell or a near host, and the compute is remote. The Host Life Law of Part 22 governs the energy host only.
5. **A large Core antenna helps both ways.** It adds downlink gain and uplink receive gain. The Leaf uplink under SAR stays weak.

**Questions added to every seat**. State the distance class of each result. Say which results hold at C0, C1 and C2.

**The new seats of block `HP-3`**

| Seat | Directory | The question |
|---|---|---|
| far link | `hw/core/far/` | the link budget at `100 m` to `10 km` with a large Core antenna and the Leaf antennas as designed |
| parts | `hw/core/parts/` | every part of the Leaf, kept on the Leaf or movable to a Core, by distance class |
| fleet | `hw/core/fleet/` | how many Leafs one large Core serves, and the two hosts law |

## 9 · The standing after the studies (2026-10-19)

Nine seats ran, and the Lead ran block `HP-4` alone. Part 23 of the directive holds the result. These statements of this brief changed.

1. **Section 2, the Skin**. A Skin is never empty. The slice decoder, the link PHY and a hardened identity element stay. The Rule of Necessity fixes the rest: the camera part keeps what physics forces. The Core holds all else.
2. **Section 3, the numbers of the Lead**. The `6:1` compression is outside the published range. The `0.80 W` and `1.35 W` loads omit the tile hubs.
3. **Section 4, item 6 and Section 5, item 1**. A stolen Skin is worth a piece of glass for the money only. An unhardened identity chip clones, and a modified Skin lies.
4. **Section 8, the distance order**. The Split lives at C0 and at the near edge of C1, as a wired Skin. At C2 nothing leaves the Leaf.
5. **Gate names**. The seats proposed their own prefixes. Part 23 merges them into `CSK-1` to `CSK-29`.
