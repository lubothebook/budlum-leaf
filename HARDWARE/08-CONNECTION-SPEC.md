# BUDLUM LEAF · HARDWARE · 08 · THE CONNECTION SPECS · THE (+) CROSS SEAMLESS INTERFACE AND REVERSIBLE 90° B STEM DOCK

**Revision L.5.0 · 2026-10-12**.
The Budlum Leaf Revision L.5.0 has three mechanical, optical, and electrical interfaces (`pafta/P10`, `pafta/P13`, `pafta/P16`):
1. **Central `+` Cross Quadrant Seam (`x = 0`. `y = 0`)** joining the four `40.0 x 80.0 x 2.00 mm` (`17.0 g`) polycarbonate screen-battery tiles (`Q1..Q4`).
2. **4-Edge Reversible `90°`-Bent B Stem Dock** allowing the `20.0 g` B module to clip onto any of. The 4 outer edges (`Top`, `Bottom`, `Left`, `Right`). Also, onto either the **Front (`+Z`) or Back (`-Z`)** of the screen.
3. **Universal `Qi / Qi2.2` Wireless Charging & Desk Dock (`240 x 120 x 12 mm`)**. It uses zero USB-C on the screen body and the sole `USB Type-C` (`40 W PD 3.1`). It covers the `90°`-bent B stem.

---

## 1 · The Central `+` Cross Quadrant Interface (`x = 0`, `y = 0`)

1. **Zero-scratch `<15 µm` (`n = 1.585`) self-healing optical lip**. A `12 µm` phenyl-fluorosilicone elastomer micro-lip on the inner `+` edges matches the refractive index of the. `ISO 10993` polycarbonate shell (`n = 1.586`, Fresnel `R = 9.9e-8 < 0.0001%`). It seals to **`IP68`** with **zero visible line and zero scratch**.
2. **Center `(0,0)` cruciform Titanium hub & `8` tapered Ti micro-dovetail pins**. Two tapered Grade-5 Titanium pins (`Ø0.70 x 2.40 mm`) per internal edge lock Z-coplanarity to **`<2.5 µm`**. It covers all four tiles.
3. **`24` bipolar `N52H` magnets & `64` gold micro-leaf contacts (`3 ms` Dead-Pad)**. Six `N52H` magnets (`11.2 N` pull, `18.5 N` shear). Also, `16` recessed gold micro-leaves (`18 mΩ`) per half-axis transfer `VSYS_HV`, `QI2_AC_RING`, and `MIPI_TILE_SYNC`. Any tile snaps out or in within **`<3 seconds`** (`EU 2023/1542` Article 11).

| Parameter | `+` Cross Seam (`Q1..Q4`) | `90°` B Stem Edge Dock (`4` edges, `+Z / -Z`) |
| --- | --- | --- |
| Normal / pull hold force | **`11.2 N` per half-axis** (`24` bipolar `N52H` total) | **`7.2 N`** (`8` `N52H` magnets + `±90°` Ti hinge clip) |
| Coplanarity / alignment | **`<2.5 µm` Z-step, `<15 µm` (`n = 1.585`) optical gap** | **`±0.08 mm`** self-centering on Top, Bottom, Left, or Right edge |
| Electrical contacts | **`64` gold micro-leaves** (`16` per half-axis, `18 mΩ`) | **`12` hard-gold pogo pins** (`18 mΩ`, symmetric front/back pinout) |
| Dead-Pad security handshake | **`3 ms` cryptographic challenge-response** (`0 V` when open) | **`3 ms` cryptographic challenge-response** before power/TCON enable |
| Hot-Swap / bridge window | **any 1 tile swaps in `<3 s`** while remaining 3 tiles (`9.0 Wh`) run | **`0.45 Wh` solid-state bridge cell** in B ring holds session during flip |
| Waterproof rating | **`IP68`** (`12 µm` phenyl-fluorosilicone optical lip) | **`IP68`** (`0.40 mm` FKM perimeter gasket) |

---

## 2 · Portless Wireless Body & Sole `USB Type-C` in the `90°`-Bent B Stem

- **Screen body (`80 x 160 x 2.00 mm`)**: **zero USB-C ports and zero buttons**. Charges wirelessly on any pad via the central `Ø54.0 mm` `Qi2.2` (`15-25 W`) 4-sector coil or the. `4 x Ø22.0 mm` (`5-10 W`) per-quadrant `Qi` coils.
- **`90°`-bent B stem (`8.0 x 32.0 x 4.50 mm`)**. Houses the **only `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68)** receptacle on the device,. While the flat `Ø32.0 mm` ring sits on the screen and houses `U1` Master TCON. Also, `U2` `UWB / mmWave` SiP.
