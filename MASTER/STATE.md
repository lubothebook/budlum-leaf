# BUDLUM LEAF · PROGRAM STATE

**Revision:** L.6.1 · 2026-10-19 · the living picture. The first file a new collaborator reads.
**Owner:** the Leaf Program Lead. It is rewritten in every working block (Volume XII, Section 7).

---

## 1 · The artefacts

| The artefact | The state |
|---|---|
| **`LEAF/BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md`** | **THE FINAL DIRECTIVE, v5, Revision L.5.0**: 21 files assembled into one, **20 numbered parts**, **251 gates**, and gap register G-01 to G-39 |
| `LEAF/FINAL/00` to `20` | the parts of v5, kept separately for editing. **Edit the parts, never the assembled file** |
| `LEAF/tools/assemble.py` | **the assembler**, gate PRG-16: each part once, in ascending order |
| `LEAF/HARDWARE/` | **the hardware volume of Revision L.5.0** (`00` to `20`): `4 x 40x80x2.00 mm` (`68 g`) `+` solid-state body, `Qi2.2`, and `90°`-bent-stem B module (`20 g`) |
| `LEAF/cad/` | `monogram_letter.py`, `leaf_geom.py`, `leaf_v2.py`, `render3d.py`, `heypcb_post.py`, `leaf_classes.py`, `monogram_detail.py`, `rail_detail.py`, `render_iso.py`, and all 13 STL models in `cad/models/` |
| `LEAF/teslim/` | high-resolution 3D renders (`render-whole.png`, `render-face.png`, `render-back.png`, `render-battery.png`, `render-apart.png`, `render-module.png`, `render-module-back.png`, `heypcb-post.png`) |
| `LEAF/NEREDE-NE-VAR.md` | **the map of the whole program in Turkish**: which file holds the directive, the hardware, the sheets, the models and the gates |
| `LEAF/pafta/check_sheets.py` + `check_widths.py` | the drawing checks: overflow, collision, cover and line width (`OVER 0, COVERED 0, COLLIDE 0` across all 25 sheets) |
| `LEAF/tools/check_prose.py` | **the writing check**, gate PRG-12: em dashes zero, sentences inside the limit |
| `LEAF/tools/check_crossrefs.py` + `canon.json` | **the count check**, gate PRG-15: one number per count, held in one file |
| `LEAF/tools/multi_agent_optimize.py` | **multi-agent Arena API self-optimization runner**: coordinates CAD, Pafta, Hardware, and QA agents using `ARENA_API_KEY` from the environment |
| `LEAF/pafta/P01` to `P22`, and `E01` to `E03` | **all 25 SVG sheets pass `OVER 0, COVERED 0, COLLIDE 0`**: `E01..E03` engineering sections, `P01..P13` core sheets, and `P14..P22` part-by-part sheets |

---

## 2b · The block of Revision L.6.1 (2026-10-19 · host power and the living Leaf)

Part 22 (`FINAL/22-host-power-and-the-living-leaf.md`) holds the numbers. It adds to Part 21 and changes no L.6.0 number. The work lives in `hw/hostpower/`.

- **The order**. Ayaz asked for a Leaf that lives as long as its host, with the main energy in the hardware. Ayaz gave the management of the program to the Program Lead.
- **The Host Life Law**. On a paired host with a heat path, a Leaf lives as long as the host feeds it. Between hosts, a bridge store keeps the session.
- **The first host-power tier is Buffer**: `15` to `20` micro cells over four quadrants. Bare does not fit the margin. Full stays.
- **The host feeds the load and the cell floats near `50 %`**. The model gives `13.4` years of cell life against `1.8` years cycled daily.
- **Always-on needs a host that pulls heat**. The dock plate passes `72` of `72` cases. Free air passes none, with a battery or with a host.
- **The word "first" is held**. A wallet with a screen, a tablet with the cell removed and a display with no cell all exist.
- **Not yet done**: the secure element has no NVM counters (G-44). The prior art search and the legal opinion are not ordered (G-47).
- **The count**. `29` new gates `HST-1` to `HST-29`, research order RG-19, and gaps G-44 to G-48.

---

## 2a · The closed decisions of Revision L.6.0 (2026-10-12 · stretch, `1.00 mm` bar, projection)

Part 21 (`FINAL/21-stretch-stem-and-projection.md`) holds the numbers. It wins over the L.5.0 list below where they differ.

- **The body stretches with no loss of battery**. `128` rotating PC-capped tiles give `25 %` stretch, and `41 %` at most. The body holds `5.7` to `7.2 Wh`.
- **The display stays `508 ppi`**. Micro-LED tiles meet in lattice-continuous seams, so no seam shows. The quadrants stay removable. Qi2.2 stays.
- **The B module is `4.00 mm` thick and its bar is `1.00 mm`**. The bar is `32.0 x 4.0 x 1.00 mm` LCP-GF40 on the top edge. It holds the antennas and the body link only.
- **USB-C is a separately sold port part**. The `3.5 mm` jack sits in the ring rim. The camera stays `50 MP`: a small-pixel sensor in a `3.90 mm` column.
- **"Zero CPU" means no general-purpose processor and no operating system**. Fixed-function chips and a `16 MB` frame store are allowed.
- **The validators run the Leaf as they run the chain**. Session state is chain state, and the nearest validator renders at frame speed. Finality follows in the `6` s slot (research order RG-18).
- **The radio set is `U2A` Wi-Fi 7, `U2B` `60 GHz` and UWB, and `U5` 5G standalone**. The Leaf is a wallet on the nearest validator. The dock validator is optional, and `30 ms` holds outdoors.
- **Not yet redrawn**: the 25 sheets, the STL models and the renders still show L.5.0.

## 2 · The closed decisions of Revision L.5.0 (2026-10-12 · 4-Quadrant `+` Puzzle-Interlocking Body & `90°` Natural-Gap Bent B Module)

- **The bulky external bottom battery pack is cancelled**. The `2.00 mm` (`68 g`, `R = 6.35 mm`) body splits across `+` into `4 x 17 g` quadrants (`Q1..Q4`).
- **Internal bi-directional puzzle interlock (`yapboz girdili-çıktılı`) and `<15 µm` (`n = 1.585`) `+` seam**. Inside the `2.00 mm` stack, `24` `Nitinol/Ti-PEEK` dovetail puzzle joints (`10 N/mm`) hold `R 25.5 mm` bends together.
- **Eyewear-safe `LLZO/PEO` all-solid-state battery (`4 x 3.0 Wh = 12.0 Wh` / `3 200 mAh`)**. Each tile uses non-flammable `LLZO/PEO` (`0%` liquid, `0` HF), `<=36.2 C` NTC cut-off, and `ISO 10993` PC.
- **Portless universal `Qi2.2` wireless charging on the screen body; zero USB-C on body**. A central `Ø54.0 mm` `Qi2.2` (`15-25 W`) coil and `4 x Ø22.0 mm` `Qi` coils charge on any wireless pad.
- **The exact `b.png` module (`20.0 g`, 32 parts) turns `90°` and bends `90°` across its natural gap (`boşluk`)**. Its `1.00 mm` (`bir milim`) `çubuk` sits horizontally on top of the screen edge, while its round ring faces us.
- **Sole `USB Type-C` (`40 W PD 3.1`) and Zero-CPU silicon live in the B module**. All non-wireless functions (`U1` TCON, `U2` `UWB / mmWave` SiP, camera, audio, RF, USB-C) require the B module.

---

## 3 · The gate board

| The family | The gates | The state |
|---|---|---|
| The structure, the mass, the heat | MEC-1 to MEC-38, B-1 to B-10 | `80 x 160 x 2.00 mm` (`68 g`, `R = 6.35 mm`) 4-Quadrant (`+`) puzzle body verified against CAD |
| The energy & `<3 s` Hot-Swap | ENR-1 to ENR-21 | `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) `LLZO/PEO` solid-state + `Qi2.2` (`Ø54 mm`) + `<=36.2 C` eyewear safety |
| The display & privacy film | DSP-1 to DSP-16, CLR-1 to CLR-11 | flicker-free DC-dimming `T-OLED` + switchable `PDLC` privacy film + `AgNW/ITO` + `ISO 10993` PC |
| The Field mode | FLD-1 to FLD-6 | specified in Part 7 |
| The camera and `90°` natural-gap B module | CAM-1 to CAM-20, MON-1 to MON-20 | `90°`-bent-at-gap B module (`20 g`, `32` parts): `1.00 mm` horizontal top `çubuk`, front-facing ring |
| The Portless Qi2.2 Body & Stem USB-C | RL-1 to RL-18 | zero USB-C on screen body; sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`) in `1.00 mm` horizontal B `çubuk` |
| The radio and Zero-CPU link | RF-1 to RF-20, SW-1 to SW-19, DST-1 to DST-10 | `1.00 mm` horizontal B `çubuk` LCP + `60 GHz` antennas (`SAR 0.054 W/kg`) + `U2` `UWB / mmWave` SiP |
| The second face and the shape | DUO-1 to DUO-7, SZ-1 to SZ-5 | 12-edge softened `2.00 mm` 4-Quadrant (`+`) sheet (`R 6.35 mm`, `r 0.62 mm`) |
| The program and research | PRG-1 to PRG-16, RG-1 to RG-17 | PRG-12, PRG-15, PRG-16 tools live and passing |
| The drawing check | overflow, collision, cover, line width | passing: `OVER 0, COVERED 0, COLLIDE 0` on all 25 sheets |
