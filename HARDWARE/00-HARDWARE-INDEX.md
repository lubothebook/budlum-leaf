# BUDLUM LEAF · HARDWARE · 00 · THE INDEX

**Revision L.5.0 · 2026-10-12 · the hardware volume of the program**.
**What this directory is**. Every hardware fact of a Budlum Leaf is stated here so a factory, a partner or an engineer can build and test it. The directive (`LEAF/FINAL/`) states the product law, and this directory states the hardware that obeys it.

**The rule of this directory**. A part exists here when it has a name, a number, a bus, an owner and a gate. A part with a name and no number is a wish.

---

## 1 · The files

| The file | What it settles |
| --- | --- |
| `01-SYSTEM-ARCHITECTURE.md` | the end-to-end path: `4 x (40 x 80 x 2.00 mm)` (`68 g`) `+` screen-battery body and `90°`-bent-stem B module (`20 g`) |
| `02-ELECTRONICS-AND-BUSES.md` | invisible AgNW/ITO mesh, `64` gold `+` seam contacts, universal `Qi2.2` wireless charging, and `90°` B module Zero-CPU electronics |
| `03-PART-CATALOGUE.md` | every part with its class, its key numbers, its mass (`68.0 g` 4-quadrant body, `20.0 g` B module. `88.0 g` total) and its gate |
| `04-PORT-RAIL.md` | the portless screen body (`Qi2.2` wireless charging, zero USB-C on body) and the sole USB Type-C port on the `90°`-bent B stem |
| `05-B-MODULE-CAMERA-AND-PANEL.md` | the `90°`-bent-stem B module (`20.0 g`): only the stem bends `90°` up while the `Ø32 mm` ring lies flat on the screen |
| `06-FORM-LANGUAGE-AND-EDGES.md` | the `80 x 160 x 2.00 mm` 4-quadrant (`+`) polycarbonate screen-battery body (`R 3.20 mm`, `r 0.65 mm`, `<15 µm` seam) |
| `07-MODELS-AND-3D.md` | how the 13 watertight 3D STL models and 8 perspective renders in `teslim/` are generated and verified |
| `08-CONNECTION-SPEC.md` | the `+` cross seamless interface (`24` N52H magnets, `64` gold leaves, `<15 µm` optical lip) and 4-edge reversible B module docking |
| `09-OPEN-ITEMS.md` | what hardware is under bench verification, with an owner and the next action |
| `10-ANY-PLACE-AND-THE-MAGNETIC-FIELD.md` | the `24` bipolar N52H `+` seam magnets, `64` gold micro-leaf contacts, and 4-edge reversible `90°` B stem clip (`3 ms` Dead-Pad, IP68) |
| `11-THE-ENERGY-SHEET.md` | the `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) biocompatible `LLZO/PEO` solid-state battery and eyewear safety (`<=36.2 C`, `ISO 10993`) |
| `12-THE-BEND-LAW.md` | **the bend law**: how the `2.00 mm` 4-quadrant solid-state polycarbonate laminate bends to `R 25.5 mm` at `0.38%` strain |
| `13-B-MODULE-PART-BY-PART.md` | **the `90°`-bent-stem B module in 32 parts**: `±90°` Ti hinge, stem USB-C + antenna, flat ring camera, rear AMOLED, and Zero-CPU SiP |
| `14-PORT-RAIL-PART-BY-PART.md` | **the portless Qi2.2 body & `90°` B stem USB-C interface in 42 parts**: `Ø54 mm` Qi2.2 coil. `4 x Ø22 mm` coils, and stem USB-C |
| `15-THE-ENERGY-SHEET-PART-BY-PART.md` | **the 4-quadrant (`+`) solid-state battery & Qi2.2 system in 25 parts**: `LLZO/PEO` cells (`12.0 Wh`), optical lip, and ocular protection |
| `16-THE-SCREEN-PART-BY-PART.md` | **the 4-quadrant (`+`) T-OLED + PDLC + AgNW/ITO screen in 10 parts**: `<15 µm` (`n=1.585`) zero-scratch seam and `ISO 10993` polycarbonate |
| `17-BODY-AND-SANDWICH-PART-BY-PART.md` | **the `2.00 mm` (`68.0 g`) 4-quadrant body and `90°` B module (`20.0 g`) in 14 groups (`88.0 g` total, `84` modeled subparts)** |
| `18-THE-DOCK-PART-BY-PART.md` | **the dock in 27 parts**: `240 x 120 mm` Qi2.2 + gold-pad deck, `27 W` charging, `2.5 Gbit/s` network,. Also, gates `DK-1` to `DK-10` |
| `19-THE-RADIO-AND-ANTENNAS-PART-BY-PART.md` | **the radio in 21 parts**: `90°`-bent B stem antenna + `60 GHz` array (`SAR 0.054 W/kg`) and `AgNW/ITO` perimeter diversity |
| `20-THE-BUDLUM-MONOGRAM.md` | **`90°`-bent-stem B module specification (`20.0 g`, `32` parts)**: 1:1 `uploads/b.png` silhouette, flat ring on screen, and gates `MON-1..20` |
| `../cad/` | the 3D generators (`leaf_v2.py`, `leaf_geom.py`, `monogram_letter.py`, `monogram_detail.py`, `heypcb_post.py`) and the 13 STL models |

---

## 2 · The device in one paragraph

A Budlum Leaf 160 divides its `80.0 x 160.0 x 2.00 mm` (`68.0 g`) body across a central `+` cross (`x = 0`. `y = 0`). It forms **four equal `40.0 x 80.0 x 2.00 mm` (`17.0 g`) snap-together polycarbonate screen-battery quadrants (`Q1..Q4`)**. The bulky external bottom battery module is cancelled. Each quadrant integrates an `ISO 10993` polycarbonate shell, flicker-free `T-OLED`, `PDLC` privacy film, `AgNW/ITO` mesh,. Also, a **`3.0 Wh` (`800 mAh`) `LLZO/PEO` solid-state battery (`12.0 Wh` / `3 200 mAh` total)**. The `+` seam uses a `<15 µm` (`n = 1.585`) self-healing optical lip with zero visible line or scratch. The screen body has **zero USB-C and zero buttons**, charging on any wireless pad via a `Ø54 mm` `Qi2.2` (`15-25 W`) coil. Also, `4 x Ø22 mm` local `Qi` coils. All other functions require the **`90°`-bent-stem B module (`20.0 g`)**, where only the antenna + `USB-C` stem bends `90°` up. While the round camera ring lies flat on the screen (`88.0 g` total).

---

## 3 · The five members, and what each one carries

| The member | The `+` screen-battery body | Corner and 12 edges | Internal solid-state battery & Qi2 | The `90°`-bent-stem B module | The ports |
| --- | --- | --- | --- | --- | --- |
| **Leaf 80** | `40.0 x 80.0 x 2.00 mm` (`17 g`, 1 tile) | corner `R 2.69 mm`, 12 edges `r 0.65 mm` | `3.0 Wh` (`800 mAh`) `LLZO` + `Ø22 mm` Qi coil | docks on any edge, front or back (`20 g`) | zero USB-C on body; sole USB-C in B stem |
| **Leaf 160** | `80.0 x 160.0 x 2.00 mm` (`68 g`, `4 x 17 g`) | corner `R 3.20 mm`, 12 edges `r 0.65 mm` | `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) + `Ø54 mm` Qi2.2 | docks on all 4 edges, front (`+Z`) or back (`-Z`) | zero USB-C on body; sole USB-C in B stem |
| **Leaf 160²** | `160.0 x 160.0 x 2.00 mm` (`144 g`, 8 tiles) | corner `R 3.81 mm`, 12 edges `r 0.65 mm` | `24.0 Wh` (`6 400 mAh`) `LLZO` + dual `Qi2.2` | docks on any edge, front or back | zero USB-C on body; sole USB-C in B stem |
| **Leaf 480** | `320.0 x 480.0 x 2.40 mm` (`48 tiles`) | corner `R 4.53 mm`, 12 edges `r 0.65 mm` | `144.0 Wh` modular tile array + Dock | docks on edge or Dock post | B stem USB-C and Dock |
| **Leaf 1400 / 2800** | desk and wall (`2.40 mm`) | corner `R 5.86 / 6.40 mm`, 12 edges `r 0.65 mm` | modular tile array + wall/dock feed | Dock B module | B stem USB-C and Dock |

---

## 4 · The hardware laws of the program

1. **The bulky external bottom battery is cancelled. The `80 x 160 x 2.00 mm` (`68 g`) body splits into 4 `+` quadrants (`Q1..Q4`)**. Each `40 x 80 x 2.00 mm` (`17 g`) polycarbonate tile snaps together in `<3 s` (`EU. 2023/1542` Article 11) with a `<15 µm` (`n = 1.585`) zero-scratch optical seam.
2. **Each tile houses an eyewear-safe `LLZO/PEO` all-solid-state battery (`3.0 Wh`, `12.0 Wh` total)**. It contains `0%` flammable liquid, `0.0 ppm` HF gas, a `<=36.2 C` ocular thermal cut-off. `<0.08 µT` bifilar routing, `SAR 0.054 W/kg`, and `ISO 10993` polycarbonate.
3. **The screen body has zero USB-C ports and zero buttons, and charges wirelessly on any `Qi / Qi2.2` pad**. A central `Ø54.0 mm` 4-sector `Qi2.2` (`15-25 W`) coil. Also, `4 x Ø22.0 mm` (`5-10 W`) local coils charge the whole body or any single tile.
4. **Only the stem (`çubuk`) of the B module (`20.0 g`) is bent `90°` (`dik açıyla`). While the round ring lies flat on the screen**. By moving the `90°` stem around the 4 edges. The B module docks to the front (`+Z`) or back (`-Z`) face.
5. **USB Type-C (`40 W PD 3.1 + DP 2.1`) lives exclusively inside the `90°`-bent B stem**. Aside from wireless charging on any pad, all other functions (`U1` Master TCON. `U2` Zero-CPU `UWB / mmWave` SiP, camera, audio, antenna, and wired USB-C) require the B module.
6. **Every `+` seam contact and B dock pad stays at `0 V` until a `3 ms` cryptographic. Dead-Pad handshake completes**.
