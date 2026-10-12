# BUDLUM LEAF · HARDWARE · 04 · THE PORTLESS QI2.2 BODY AND THE SOLE USB-C IN THE 90° BENT B STEM

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. USB-C leaves the B module and becomes a separately sold port part on a free body edge. The B bar is `32.0 x 4.0 x 1.00 mm` LCP on the top edge.

**Revision L.5.0 · 2026-10-12**.
This file settles two linked rules: **where wireless charging lives** and **where USB Type-C lives**. The 4-quadrant (`+`) screen body has **zero USB-C ports and zero buttons** and charges wirelessly on any `Qi / Qi2.2` pad. **USB Type-C lives exclusively on the `90°`-bent stem of the B camera module** (`pafta/P10`, `pafta/P16`).

---

## 1 · The Revision L.5.0 decision in one paragraph

The screen body (`80.0 x 160.0 x 2.00 mm`, `68.0 g`) carries **no USB-C opening and no mechanical button**. It charges wirelessly on any standard `Qi`, `Qi2.2` (`15-25 W` MPP), or `PMA` pad via a central `Ø54.0 mm` 4-sector coil. Also, four `Ø22.0 mm` (`5-10 W`) per-quadrant coils. The **only `USB Type-C` receptacle (`40 W PD 3.1 + DP 2.1`, IP68)** is integrated. It covers the `90°`-bent stem (`çubuk`) of the B camera module (`20.0 g`). Aside from wireless charging on any pad, all other functions require the B module docked to the screen.

---

## 2 · Why the screen body is portless and USB-C lives only in the `90°` B stem

1. **Thinness (`2.00 mm`) and bending (`R 25.5 mm`)**. A USB-C receptacle requires a `3.1 to 3.6 mm` rigid shell. Keeping USB-C out of the `2.00 mm` polycarbonate screen tiles lets all four quadrants (`Q1..Q4`) stay `2.20. Mm` thin and bend smoothly (`0.38%` strain).
2. **Universal wireless charging (`Qi / Qi2.2`) on the screen body**. When `Q1..Q4` snap together across `+`, their four `90°` Litz-wire sectors form a central `Ø54.0 mm` `Qi2.2`. (`15-25 W`) receiver coil. Each tile also has its own `Ø22.0 mm` (`5-10 W`) local `Qi` coil. So a single detached tile charges on any wireless pad.
3. **Single mandatory companion module (`b` module)**. Putting the sole `USB Type-C` port, `U1` Quad-Tile Master TCON, and `U2` Zero-CPU `UWB / mmWave` SiP. It covers the B module eliminates the bulky bottom chin module while keeping `40 W` wired charging. Also, `DP 2.1` video available whenever the B module is docked.
4. **Wear isolation**. If the `USB Type-C` receptacle wears after `10 000` cycles, only the `20.0 g` B module is serviced. The `4 x 17.0 g` screen-battery quadrants are untouched.

---

## 3 · The charging and I/O paths, side by side

| The path | Where it lives | Power / data rate | Works without B module? | Gate |
| --- | --- | --- | --- | --- |
| **1 · Central `Ø54.0 mm` 4-sector `Qi2.2` MPP coil** | centered at `(0,0)` across `Q1..Q4` (`4 x 90°` sectors) | **`15 to 25 W` wireless** (`86%` efficiency) | **Yes** (charges whole `12.0 Wh` screen on any pad) | ENR-12, RL-2 |
| **2 · Per-quadrant `4 x Ø22.0 mm` local `Qi` coils** | centered inside each `40 x 80 mm` tile (`Q1..Q4`) | **`5 to 10 W` wireless per tile** | **Yes** (charges any single detached `3.0 Wh` tile) | ENR-12, RL-2 |
| **3 · Sole `USB Type-C` in `90°`-bent B stem** | inside the `8.0 x 32.0 x 4.50 mm` `90°` B stem | **`40 W` USB-PD 3.1 + `10 Gbit/s` + `DP 2.1`** | **No** (requires B module docked to screen) | RL-1, MON-5 |
| **4 · Desk Dock (`240 x 120 mm`)** | `Qi2.2` transmitter + `6` gold dock pads | **`27 W` charge + `2.5 Gbit/s` LAN** | **Yes** (wireless charge) / **B module for compute** | DK-1..10 |

---

## 4 · The `90°` B stem dock and optional side accessories (`pafta/P16`)

| The element | The number | The reason |
| --- | --- | --- |
| Screen body USB-C & buttons | **`0` USB-C ports, `0` buttons on body** | pure `2.00 mm` waterproof (`IP68`) 4-quadrant screen-battery laminate |
| Sole `USB Type-C` receptacle | **1 port, inside `90°`-bent B stem (`40 W` PD 3.1)** | satisfies `EU 2022/2380` when shipped with the B module seated in the box |
| B stem edge-clip interface | `12` gold pogo pins (`18 mΩ`) + `8` N52H magnets (`7.2 N`) | docks on all 4 edges (Top, Bottom, Left, Right) and both faces (`+Z` / `-Z`) |
| Dead-Pad (`Ölü Pin`) security | **`3 ms` cryptographic challenge-response** | all `12` dock pads and `64` `+` seam pads stay at `0 V` until authenticated |
| Optional side rail modules (`PORT-CA`, `PORT-CJ`) | `44.0 x 11.0 mm` magnetic side-rail adapters | optional `3.5 mm` TRRS jack or `USB-A` host adapter for studio workflows |

---

## 5 · EU Common Charger (`EU 2022/2380`) and EU Battery (`EU 2023/1542`) compliance

- **Directive (EU) 2022/2380**. Every Budlum Leaf ships in the box with the `90°`-bent-stem B module seated. Providing `40 W` `USB Type-C` PD charging (`RL-D4`), plus universal `Qi / Qi2.2` wireless charging on the screen body.
- **Regulation (EU) 2023/1542 Article 11**. Every `40.0 x 80.0 x 2.00 mm` (`3.0 Wh`) screen-battery quadrant detaches. Also, snaps back in `<3 seconds` with zero tools, zero heat, and zero solvent.
