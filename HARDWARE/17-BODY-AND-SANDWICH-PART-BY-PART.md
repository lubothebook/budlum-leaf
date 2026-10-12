# BUDLUM LEAF · HARDWARE · 17 · THE 2.20 MM (72 G) 4-QUADRANT (+) BODY AND 90° B MODULE (22 G), PART BY PART

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. The body is `128` rotating PC-capped tiles. The B module is `10.8 g`, `4.00 mm` thick, with a `1.00 mm` LCP bar and no titanium hinge.

**Revision L.5.0 · 2026-10-12**.
The Budlum Leaf 160 cancels the bulky external bottom battery pack (`çok kaba duruyor`). Also, divides the `80.0 x 160.0 x 2.00 mm` (`68.0 g`) body across a central `+` cross (`x = 0`. `y = 0`) into **four equal `40.0 x 80.0 x 2.00 mm` (`17.0 g`) snap-together polycarbonate screen-battery quadrants (`Q1..Q4`)**. Combined with the **`20.0 g` `90°`-bent-stem B module**, the complete device weighs **`88.0 g`** (`84` modeled internal subparts, `pafta/P19`).

---

## 1 · The 14 component groups of the 68.0 g 4-Quadrant (`+`) body and 20.0 g `90°` B module (`88.0 g` complete)

| Group | Component group | Mass (`g`) | Role and specification | Gate |
| --- | --- | --- | --- | --- |
| 1 | `ISO 10993` medical-grade BPA-free PC shells (`x 8`) | `12.8` | `4` tiles x `2` faces (`40.0 x 80.0 x 0.20 mm`), outer `R = 6.35 mm`. 12 edges `r = 0.65 mm`, `n = 1.586` | F-01..03, DSP-16 |
| 2 | Silicone OCA shear-decoupling slip layers (`x 8`) | `1.6` | `0.05 mm` (`G = 0.08 MPa`) optical silicone limiting outer PC strain to `0.38%` at `R 25.5 mm` | B-6 |
| 3 | Flicker-free DC-dimming `T-OLED` panels (`x 8`) | `6.8` | `79.6 x 159.6 mm` combined per face (`508 ppi`, `1-144 Hz`, `<415 nm` HEV cut, `IEC 62471` RG0) | DSP-15 |
| 4 | Invisible `AgNW / ITO` mesh & Corning edge-wrap (`x 8`) | `1.6` | `0.04 mm` (`12 Ω/sq`) transparent mesh + side-wall edge-wrapped electrodes (`0.00 mm` internal bezel) | MEC-34, DSP-9 |
| 5 | Switchable `PDLC` privacy film cores (`x 4`) | `1.9` | `0.09 mm` low-voltage matte privacy lock / `0 V` transparent core in each quadrant | CLR-1..11 |
| 6 | Orthotropic graphene + `Mu-metal` ocular shields (`x 8`) | `3.4` | `k_xy = 1 100 W/m·K`, `k_z = 1.5 W/m·K` thermal insulator + `Mu-metal` (`<0.08 µT` ELF at eye) | ENR-16, MEC-38 |
| 7 | All-solid-state `LLZO/PEO` battery cells (`x 4`) | `34.4` | `4 x (35.0 x 75.0 x 1.08 mm)`, `4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`), `0%` liquid. `0.0 ppm` HF | ENR-11, ENR-15 |
| 8 | Bifilar foil tabs, `36.2 °C` NTCs & `180 mF` buffers (`x 4`) | `2.4` | current-canceling tabs (`<0.08 µT`), hardware `36.2 °C` ocular cut-off, `<3 s` hot-swap holdover | ENR-13, ENR-16 |
| 9 | Universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` `Qi` coils & `U_QI` | `3.2` | `15-25 W` whole-body `Qi2.2` MPP + `5-10 W` single-tile `Qi` wireless charging (zero USB-C on body) | ENR-12, RL-2 |
| 10 | `<15 µm` (`n = 1.585`) `+` lip, `(0,0)` Ti hub, `24` N52H, `64` leaves | `3.9` | zero-scratch optical seam (`R < 0.0001%`), `<2.5 µm` Z-step, `11.2 N` latch, `3 ms` Dead-Pad (`EU 2023/1542`) | DSP-16, ENR-13 |
| **4-Quad Body** | **Groups 1 to 10 (`80.0 x 160.0 x 2.00 mm`, `52` parts)** | **`68.0 g`** | **`4 x 17.0 g` (`Q1..Q4`), `12.0 Wh` solid-state, eyewear-safe (`<=36.2 C`), `Qi2.2`, zero USB-C on body** | **F-01..10, B-1..10** |
| 11 | **`90°`-bent B stem (`USB-C` + Ti hinge + LCP/`60 GHz` RF)** | **`7.6 g`** | `8.0 x 32.0 x 4.50 mm` stem bent `90°` via `±90°` Ti hinge; **sole `USB Type-C` (`40 W`)** + antennas | MON-1, MON-5, RL-1 |
| 12 | **Flat B ring housing & `50 MP` folded camera (`z = 0.90..4.00`)** | **`9.8 g`** | `32.0 x 32.0 x 4.00 mm` ring flat on screen; `Ø24 mm` sapphire, `12.8x9.6` CMOS, 4-axis OIS, prism, `5P` lens | MON-1, MON-3 |
| 13 | **Annular 6L Zero-CPU PCBA (`U1` TCON + `U2` SiP + `0.45 Wh`)** | **`3.8 g`** | `Ø30.2 / Ø24.4 x 0.55 mm` ring board: `U1` Master TCON, `U2` `UWB / mmWave` SiP, `U3` DSP, `U4` PMIC | MON-10, RF-19 |
| 14 | **Rear round LTPO AMOLED (`Ø22.4 mm`) & `0.15 mm` shield** | **`0.8 g`** | `z = 0.00..0.90 mm`: `0.35 mm` rear sapphire, `480x480 px` (`1-120 Hz`) AMOLED, `0.15 mm` Cu-graphite shield | MON-4, MON-12 |
| **Complete** | **4-Quad Body (`68.0 g`) + `90°`-Bent B Module (`20.0 g`)** | **`88.0 g`** | **`84` modeled internal subparts; `<15 µm` `+` seam; `12.0 Wh` `LLZO`; `Qi2.2`; reversible `90°` B module** | **ALL GATES** |
