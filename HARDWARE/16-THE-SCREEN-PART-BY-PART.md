# BUDLUM LEAF · HARDWARE · 16 · THE 4-QUADRANT (+) SEAMLESS T-OLED + PDLC + AgNW/ITO SCREEN, PART BY PART

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ: the screen is an island-bridge panel. The stretch zone targets `250 ppi`. The face stays polycarbonate, with hard-coated caps on the islands and serpentine PC lanes between them. `U1` warps the image by the measured strain.

**Revision L.5.0 · 2026-10-12**.
This file specifies the **`80.0 x 160.0 x 2.00 mm` (`68.0 g`) 4-Quadrant (`+`) seamless display-battery sheet**. Also, the `<15 µm` (`n = 1.585`) zero-scratch optical seam (`pafta/P09`, `pafta/P18`).

---

## 1 · The 4-Quadrant (`+`) seamless T-OLED + PDLC screen in numbers

| Parameter | Value at Leaf 160 (`Q1..Q4`) |
| --- | --- |
| Full 4-quadrant outer dimensions | **`80.0 x 160.0 x 2.00 mm` (`68.0 g` = `4 x 17.0 g` tiles of `40.0 x 80.0 x 2.00 mm`)** |
| Outer corner radius & 12 softened edges | **`R = 6.35 mm`** (4 outer vertical corners) and **`r = 0.65 mm`** (8 horizontal face-to-wall edges) |
| Central `+` cross optical seam (`x=0, y=0`) | **`12 µm` (`<15 µm`) phenyl-fluorosilicone self-healing lip (`n = 1.585` vs `n_PC = 1.586`)** |
| Seam Fresnel reflection & Z-step | **`R = ((1.586 - 1.585)/(1.586 + 1.585))^2 = 9.9e-8 < 0.0001%`**, Z-step **`<2.5 µm`** (zero visible line, zero scratch) |
| Internal `+` seam bezel width | **`0.00 mm`** (Corning `US20200243738A1` edge-wrapped gate/source conductors route down the `2.00 mm` side walls) |
| Combined active screen per face | **`79.6 x 159.6 mm`** (`1 592 x 3 192 px`, **`508 ppi`**, `1-144 Hz` LTPO, `12 696 mm²` continuous canvas) |
| Eyewear photobiological safety | **100% DC + hybrid high-frequency dimming (zero PWM flicker), `<415 nm` HEV blue cut, `IEC 62471` RG0** |
| Outer biocompatible surfaces | **`ISO 10993-5 / -10` medical-grade BPA-free optical polycarbonate (`0.20 mm`) + `8 µm` hard coat (`3H`)** |
| Privacy & thermal/EMI barrier | **`0.09 mm` switchable `PDLC` privacy film + orthotropic graphene (`1 100 W/m·K`) + `Mu-metal` shield** |
| B module rear round AMOLED panel | **`Ø22.4 mm` active** inside the flat `Ø32.0 / Ø24.0 mm` ring (`480 x 480 px`, `300 ppi`, `1-120 Hz` LTPO) |
| Bending strain at `R 25.5 mm` | **`0.38 percent`** on outer `ISO 10993` polycarbonate (`0.22%` on `LLZO/PEO` core, `10 000+` wraps) |

---

## 2 · The 10 part groups of the 4-Quadrant (`+`) display-battery sheet (`68.0 g`)

| No | Part | Count (`Q1..Q4`) | Material and dimensions | Mass (`4` tiles) | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | `ISO 10993` optical polycarbonate shells | `8` (`2` per tile) | `40.0 x 80.0 x 0.20 mm` medical-grade BPA-free PC (`n = 1.586`, `r = 0.65 mm`) | `12.8 g` | DSP-16, ENR-16 |
| 2 | Silicone OCA shear-slip layers | `8` (`2` per tile) | `39.6 x 79.6 x 0.05 mm` low-modulus (`G = 0.08 MPa`) optical silicone | `1.6 g` | B-6, DSP-16 |
| 3 | Flicker-free DC-dimming `T-OLED` panels | `8` (`2` per tile) | `39.8 x 79.8 x 0.14 mm` LTPO T-OLED (`508 ppi`, `<415 nm` HEV cut, RG0) | `6.8 g` | DSP-15 |
| 4 | Invisible `AgNW / ITO` + edge-wrap traces | `8` (`2` per tile) | `39.8 x 79.8 x 0.04 mm` (`12 Ω/sq`) + Corning edge-wrapped side electrodes | `1.6 g` | MEC-34, DSP-9 |
| 5 | Switchable `PDLC` privacy film cores | `4` (`1` per tile) | `39.6 x 79.6 x 0.09 mm` low-voltage matte privacy / `0 V` transparent core | `1.9 g` | CLR-1..11 |
| 6 | Orthotropic graphene + `Mu-metal` shields | `8` (`2` per tile) | `36.0 x 76.0 x 0.05 mm` graphene (`1 100 W/m·K`) + `Mu-metal` (`<0.08 µT`) | `3.4 g` | ENR-16, MEC-38 |
| 7 | `<15 µm` (`n = 1.585`) self-healing `+` seam lip | `4` (`+` cross) | `12 µm` phenyl-fluorosilicone optical lip (`R < 0.0001%`, zero scratch, `IP68`) | `0.2 g` | DSP-15, DSP-16 |
| 8 | `(0,0)` Ti hub, `8` Ti pins & `24` N52H magnets | `1` set (`+` cross) | Grade-5 Ti keystone + tapered pins (`<2.5 µm` Z-step) + `24` bipolar N52H (`11.2 N`) | `2.9 g` | ENR-13, F-07 |
| 9 | `64` gold `+` seam leaves & `Qi2.2` wireless coils | `1` set (`Q1..Q4`) | `64` gold micro-leaves (`3 ms` Dead-Pad) + `Ø54 mm` `Qi2.2` + `4 x Ø22 mm` `Qi` coils | `6.4 g` | ENR-12, RL-2 |
| 10 | All-solid-state `LLZO/PEO` battery cores | `4` (`1` per tile) | `35.0 x 75.0 x 1.08 mm` non-flammable `LLZO` cells (`4 x 3.0 Wh = 12.0 Wh`) | `34.4 g` | ENR-11, ENR-15 |
| **Total** | **10 part groups (`52` body subparts)** | **4 `+` Quadrants** | **`80.0 x 160.0 x 2.00 mm` seamless screen + `12.0 Wh` `LLZO` + `Qi2.2`** | **`68.0 g` (`4 x 17 g`)** | **DSP-15..16, ENR-11..16** |
