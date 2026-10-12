# BUDLUM LEAF · HARDWARE · 03 · THE PART CATALOGUE

**Revision L.5.0 · 2026-10-12**.
This file catalogs the two main assemblies of the Budlum Leaf 160 (`88.0 g` total, `84` modeled internal subparts). They are the **`80.0 x 160.0 x 2.00 mm` (`68.0 g`) 4-Quadrant (`+`) screen-battery body (`4 x 17.0 g` tiles, `52` parts)**. Also, the **`20.0 g` `90°`-bent-stem B module (`32` parts)**.

---

## 1 · The 80.0 x 160.0 x 2.00 mm 4-Quadrant (`+`) screen-battery body (`68.0 g` = `4 x 17.0 g`, 52 parts)

| Assembly (total across `Q1..Q4`) | Specification | Key numbers | Mass (`4` tiles) | Gate |
| --- | --- | --- | --- | --- |
| **Biocompatible optical PC shells (`x 8`)** | `ISO 10993-5/-10` medical-grade BPA-free PC (`0.20 mm` front & back) | `4 x (40.0 x 80.0 mm)`, outer `R = 6.35 mm`, 12 edges `r = 0.65 mm`. `0.38%` strain at `R 25.5 mm` | `12.8 g` | DSP-16, F-01 |
| **Flicker-free T-OLED + silicone OCA (`x 8`)** | DC-dimming transparent OLED (`0.14 mm`) + `0.05 mm` silicone OCA (`G = 0.08 MPa`) | `79.6 x 159.6 mm` combined (`508 ppi`, `1-144 Hz`, `<415 nm` HEV cut, `IEC 62471` RG0) | `8.4 g` | DSP-15 |
| **AgNW/ITO mesh + PDLC + graphene/Mu-metal (`x 4`)** | `2 x 0.04 mm` AgNW/ITO + `0.09 mm` PDLC privacy + graphene (`1 100 W/m·K`) + Mu-metal | `>88%` clear transmission, `<0.08 µT` ELF shielding, `<=36.2 C` ocular thermal spreading | `6.8 g` | CLR-1..11, MEC-38 |
| **All-solid-state `LLZO/PEO` batteries (`x 4`)** | non-flammable ceramic/polymer solid-state pouch cells (`35.0 x 75.0 x 1.08 mm` each) | **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`, `750 Wh/L`)**, `0%` liquid, `0.0 ppm` HF, `>14.1 h` runtime | `34.4 g` | ENR-11..16 |
| **Universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` Qi coils** | `4 x 90°` central `Qi2.2` MPP (`15-25 W`) sectors + `4 x Ø22 mm` (`5-10 W`) local coils + `U_QI` | portless body (zero USB-C on body); charges whole screen or 1 detached tile on any wireless pad | `4.8 g` | ENR-12, RL-2 |
| **`<15 µm` (`n = 1.585`) `+` seam, Ti hub & latches** | phenyl-fluorosilicone zero-scratch lip, `(0,0)` Ti hub, `8` Ti pins, `24` N52H magnets, `64` gold leaves | `<15 µm` invisible seam (`R < 0.0001%`), `<2.5 µm` Z-step, `<3 s` tool-free swap (`EU 2023/1542` Art. 11) | `4.8 g` | ENR-13, F-07 |
| **Total 4-Quadrant (`+`) screen-battery body** | **`80.0 x 160.0 x 2.00 mm` (`4 x 40.0 x 80.0 x 2.00 mm`)** | **`12.0 Wh` (`3 200 mAh`), eyewear-safe (`<=36.2 C`), `Qi2.2`, zero USB-C on body** | **`68.0 g` (`4 x 17 g`)** | **F-01..10** |

---

## 2 · The `90°`-bent-stem B module (`20.0 g`, 32 internal parts)

Modeled 1:1 from `uploads/b.png` (`pafta/P14`, `pafta/P15`, `pafta/P21`):
- **Only the stem (`çubuk`, `8.0 x 32.0 x 4.50 mm`) is bent `90°` (`dik açıyla`)**. It uses a reversible `±90°` Grade-5 Titanium micro-hinge so only the stem stays up along the edge.
- **Sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68) + 3-band LCP antenna (`Wi-Fi 7`. `BT 5.4`, `UWB`) + `1x4` `60 GHz` array** live inside the `90°`-bent stem (`SAR = 0.054 W/kg`).
- **Round ring (`yuvarlak`, `32.0 x 32.0 x 4.00 mm`, `Ø24.0 mm` bore) lies flat on the screen**. It holds the `50 MP` (`12.8 x 9.6 mm`) folded-optics camera, `Ø22.4 mm` rear round AMOLED. `2 x MEMS` mics, speaker, flash, and 6-layer Zero-CPU PCBA (`U1` Master TCON + `U2` `UWB / mmWave` SiP).
- **Reversible 4-edge front (`+Z`) and back (`-Z`) docking**. Docks on Top, Bottom, Left, or Right edge and on Front or Back face (`68.0 g` body. Also, `20.0 g` B module = **`88.0 g` total**).
