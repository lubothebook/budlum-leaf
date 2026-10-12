# BUDLUM LEAF · HARDWARE · 01 · THE SYSTEM, END TO END

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. The body now stretches through `128` rotating PC-capped tiles (`25 %`, and `41 %` at most) and keeps `5.7` to `7.2 Wh`. The B module is `10.8 g` and `4.00 mm` thick, with a `1.00 mm` LCP bar on the top edge and silicon `U1` to `U8`. USB-C is a separate part.

**Revision L.5.0 · 2026-10-12**.
This file specifies the end-to-end Budlum Leaf Revision L.5.0 architecture (`pafta/E01-SISTEM-KAMERA-VE-PORT.svg` and `pafta/P22-CIHAZ-VE-KENAR-MODULU.svg`). It covers the `80.0 x 160.0 x 2.00 mm` (`68.0 g`) 4-Quadrant (`+`) screen-battery body and the `90°`-bent-stem B module (`20.0 g`. Total `88.0 g`).

---

## 1 · What the 4-Quadrant (`+`) 2.00 mm (`68.0 g`) screen-battery body holds

The bulky external bottom battery module is cancelled. The `80.0 x 160.0 x 2.00 mm` (`68.0 g`) screen body splits across `x = 0` and `y = 0`. It covers **four equal `40.0 x 80.0 x 2.00 mm` (`17.0 g`) snap-together polycarbonate quadrants (`Q1..Q4`)**:

| Block | What it is | Bus to `+` seam and B dock | Role |
| --- | --- | --- | --- |
| **Biocompatible polycarbonate & dual T-OLED (`x 4` tiles)** | `0.20 mm` `ISO 10993` BPA-free PC + `0.05 mm` silicone OCA. Also, `0.14 mm` flicker-free DC-dimming T-OLED (`<415 nm` HEV cut) on both faces | Corning edge-wrapped conductors + `AgNW/ITO` (`12 Ω/sq`) | shatterproof eyewear-safe transparent flexible display (`508 ppi`, `1-144 Hz`) on both faces |
| **Switchable PDLC & orthotropic graphene/Mu-metal shield** | `0.09 mm` PDLC privacy film + graphene spreader (`k_xy = 1 100 W/m·K`, `k_z = 1.5 W/m·K`) + Mu-metal foil | low-voltage AC drive on `AgNW/ITO` | locks privacy matte/opaque under low voltage and blocks heat/ELF toward the eye |
| **Eyewear-safe `LLZO/PEO` all-solid-state battery (`4 x 3.0 Wh`)** | `35.0 x 75.0 x 1.08 mm` (`3.0 Wh` / `800 mAh` per tile = `12.0 Wh` / `3 200 mAh`. Total at `750 Wh/L`) | bifilar foil tabs (`<0.08 µT`) + `64` gold `+` seam leaves | non-flammable (`0%` liquid, `0.0 ppm` HF), `<=36.2 C` ocular limit, `<3 s` swap (`EU 2023/1542` Art. 11) |
| **Zero-scratch `<15 µm` (`n = 1.585`) `+` seam & universal `Qi2.2`** | phenyl-fluorosilicone lip (`R < 0.0001%`), `(0,0)` Ti hub, `24` N52H magnets, `Ø54 mm` `Qi2.2` (`15-25 W`). Also, `4 x Ø22 mm` `Qi` coils | `U_QI` rectifiers + `3 ms` Dead-Pad switch (`0` USB-C on body) | seamless optical screen with zero scratch/line; charges whole body or 1 tile on any wireless pad |

---

## 2 · What the `90°`-bent-stem B module holds (`20.0 g`, 32 internal parts)

Modeled 1:1 from `uploads/b.png` and `Group 911.png`, **only the straight antenna. Also, USB-C stem (`çubuk`) is bent at a `90°` right angle (`dik açıyla`)**. While the **entire circular ring (`yuvarlak`) lies flat on top of the screen surface**:

1. **90°-bent stem (`çubuk`, `8.0 x 32.0 x 4.50 mm`, `r = 0.55 mm` soft edges)**. Wraps the screen edge via a reversible `±90°` Grade-5 Titanium micro-hinge. It houses the **3-band LCP antenna (`Wi-Fi 7`, `BT 5.4`, `UWB`)**, **`1x4` `60 GHz` phased array**,. Also, the **only `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68) receptacle** on the device.
2. **Flat circular ring (`yuvarlak`, `32.0 x 32.0 x 4.00 mm`, `Ø24.0 mm` aperture) on the screen surface**.
   - **Upper optical & audio stack (`z = 0.90..4.00 mm`)**. Front `Ø24.0 mm` sapphire window, `50 MP` (`12.8 x 9.6 x 0.65 mm`) CMOS sensor, 4-axis OIS. Folded prism, `5P` lens barrel, `2 x MEMS` mics, `9.0 x 3.2 x 2.2 mm` speaker, and dual-CCT flash.
   - **Annular 6-layer Zero-CPU core (`Ø30.2 / Ø24.4 x 0.55 mm`)**. Houses `U1` Quad-Tile Master TCON, `U2` Zero-CPU `UWB / mmWave` SiP, `U3` Audio DSP,. Also, `U4` `3 ms` Dead-Pad PMIC (`0` local CPU/OS).
   - **Lower display stack (`z = 0.00..0.90 mm`)**. `0.15 mm` Cu-graphite shield, `Ø22.4 mm` (`480 x 480 px`, `1-120 Hz`) round LTPO AMOLED,. Also, `0.35 mm` rear sapphire window.
3. **Reversible 4-edge front (`+Z`) and back (`-Z`) docking**. Moving the `90°`-bent stem around the 4 screen edges docks the B module on the Top, Bottom, Left. Or Right edge and on either the Front (`+Z`) or Back (`-Z`) face.
