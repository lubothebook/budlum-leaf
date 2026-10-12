# BUDLUM LEAF · HARDWARE · 09 · THE OPEN VERIFICATION LIST

**Revision L.5.0 · 2026-10-12**.
This file tracks bench verification for Revision L.5.0: the `80.0 x 160.0 x 2.00 mm` (`68.0 g`) 4-Quadrant (`+`) screen-battery body. Also, the `90°`-bent-stem B module (`20.0 g`).

---

## 1 · `90°`-bent-stem B module (`20.0 g`, 32 parts, `pafta/P14`, `pafta/P15`, `pafta/P21`)

| Item | Bench verification target | Gate | Owner |
| --- | --- | --- | --- |
| **`90°`-bent stem (`çubuk`) & `±90°` Ti micro-hinge** | verify `50 000`-cycle fatigue life of the reversible `±90°` Grade-5 Ti hinge and 4-edge front (`+Z`) / back (`-Z`) docking | MON-1, MON-5, MON-9 | Mechanics |
| **Sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`) in `90°` stem** | verify `10 000` plug cycles, `40 W` thermal rise (`<4.2 K`), and `IP68` sealing with zero USB-C on the screen body | RL-1, MON-12 | Power & I/O |
| **Flat ring `50 MP` folded camera (`z = 0.90..3.60 mm`)** | verify `12.8 x 9.6 x 0.65 mm` CMOS, 4-axis OIS, folded prism, and `5P` lens MTF. It covers the flat ring on the screen | MON-3, CAM-1 | Optics |
| **Rear round AMOLED (`Ø22.4 mm`) & `0.15 mm` shield** | verify `480 x 480 px` (`300 ppi`, `1-120 Hz`) LTPO AMOLED and `0.15 mm` Cu-graphite isolation behind the camera | MON-4, CAM-2 | Display |
| **Zero-CPU 6L ring PCBA (`U1` TCON + `U2` `UWB / mmWave` SiP)** | verify `<1.5 ms` wireless link latency, 4-quadrant seam LUT calibration (`<0.5%` ΔL), and `SAR = 0.054 W/kg` in eyewear mode | MON-10, RF-19 | RF & Silicon |

---

## 2 · 4-Quadrant (`+`) solid-state battery & eyewear health safety (`pafta/P11`, `pafta/P12`, `pafta/P17`)

| Item | Bench verification target | Gate | Owner |
| --- | --- | --- | --- |
| **Non-flammable `LLZO/PEO` cells (`4 x 3.0 Wh = 12.0 Wh`)** | nail-penetration, cutting, and `150 °C` oven test: `0` fire, `0.0 ppm` HF gas (` FTIR`), `0.0%` swelling over `1 000` cycles | ENR-11, ENR-15 | Battery Safety |
| **Eyewear ocular thermal (`<=36.2 C`) & `ISO 10993` safety** | verify hardware NTC cut-off at `36.2 C`, `ISO 10993-5` (`>98%` viability), `<0.08 µT` bifilar ELF, and `IEC 62471` RG0 | ENR-16, CLR-10 | Health & Regulatory |
| **Universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` wireless charging** | verify `15-25 W` `Qi2.2` MPP charging across assembled `+` cross and `5-10 W` charging of a single detached quadrant on any pad | ENR-12, RL-2 | Power |
| **`<3 s` tool-free quadrant hot-swap (`EU 2023/1542` Art. 11)** | verify `10 000` tool-free quadrant swaps (`11.2 N` pull) while remaining 3 tiles (`9.0 Wh`) keep the display live | ENR-13, F-07 | Mechanics |

---

## 3 · `<15 µm` (`n = 1.585`) zero-scratch `+` optical seam & `2.00 mm` flex (`pafta/P09`, `pafta/P18`)

| Item | Bench verification target | Gate | Owner |
| --- | --- | --- | --- |
| **`<15 µm` (`n = 1.585`) self-healing optical `+` seam** | verify Fresnel reflection `R < 0.0001%`, `<2.5 µm` Z-step on Ti pins,. Also, zero visible seam or scratch at `150 mm` viewing distance | DSP-15, DSP-16 | Optics & Display |
| **`2.00 mm` (`68.0 g`) 4-quadrant flex at `R 25.5 mm`** | verify `0.38%` outer PC strain (`0.22%` `LLZO` strain) across `10 000` full wraps and `IP68` immersion after flex | B-1..10, F-06 | Mechanics |
