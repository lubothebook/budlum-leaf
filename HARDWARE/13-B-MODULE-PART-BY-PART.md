# BUDLUM LEAF · HARDWARE · 13 · THE 90°-BENT-STEM B MODULE, PART BY PART (32 PARTS)

**Revision L.5.0 · 2026-10-12**.
This file lists all **32 internal parts** of the **`90°`-bent-stem Budlum B module (`20.0 g`)**, matching `pafta/P14-B-MODULU-PARCA-PARCA.svg`, `pafta/P15-B-MODULU-OPTIK-VE-PANEL.svg`, `pafta/P21-BUDLUM-MODULU.svg`, and `cad/models/monogram-module.stl`.

---

## 1 · Architecture of the 32-part `90°`-bent-stem B module

Modeled 1:1 from `uploads/b.png`, **only the straight antenna + USB-C stem (`çubuk`) is bent at a `90°` right angle (`dik açıyla`)**. While the **entire circular ring (`yuvarlak`) lies flat on top of the screen surface**:
- **90°-bent stem (`çubuk`, `8.0 x 32.0 x 4.50 mm`, `r = 0.55 mm` soft edges)**. Joined to the ring via a **reversible `±90°` Grade-5 Titanium micro-hinge**. So the module clips onto any of the 4 edges (`Top`, `Bottom`, `Left`, `Right`). Also, onto either the **Front (`+Z`) or Back (`-Z`)** of the screen. It houses the **3-band LCP antenna (`Wi-Fi 7`, `BT 5.4`, `UWB`)**, **`1x4` `60 GHz` phased array**,. Also, the **sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68) receptacle**.
- **Flat circular ring (`yuvarlak`, `32.0 x 32.0 x 4.00 mm`, `Ø24.0 mm` aperture) lying on the screen**.
  - **Upper optical & audio stack (`z = 0.90..4.00 mm`)**. Front `Ø24.0 mm` sapphire window, `50 MP` (`12.8 x 9.6 x 0.65 mm`) CMOS sensor, 4-axis OIS. Folded prism, `5P` lens barrel, `2 x MEMS` mics, `9.0 x 3.2 x 2.2 mm` speaker, and dual-CCT flash.
  - **Annular 6-layer Zero-CPU core (`Ø30.2 / Ø24.4 x 0.55 mm`)**. Houses `U1` Quad-Tile Master TCON, `U2` Zero-CPU `UWB / mmWave` SiP, `U3` Audio DSP,. Also, `U4` `3 ms` Dead-Pad PMIC.
  - **Lower display stack (`z = 0.00..0.90 mm`)**. `0.15 mm` Cu-graphite shield (`z = 0.75..0.90 mm`), `Ø22.4 mm` (`480 x 480 px`. `1-120 Hz`) round LTPO AMOLED (`z = 0.35..0.75 mm`), and `0.35 mm` rear sapphire window (`z = 0.00..0.35 mm`).

---

## 2 · Complete 32-part bill of materials (`22.00 g` total)

| No | Part name | Material / spec | Dimensions (`mm`) | Mass (`g`) | Tolerance | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| 32 | Front sapphire optical window | optical sapphire + 7-layer AR coat (`z = 3.60..4.00`) | `Ø24.0 x 0.40` | `0.45` | `±0.02 mm` | MON-3 |
| 31 | Front camera & acoustic ring bezel | anodized 6061-T6 aluminum (`r = 0.55 mm`) | `Ø24.0 x 2.30` | `1.35` | `±0.02 mm` | MON-3 |
| 30 | Flush dual-CCT LED flash | `2700K + 5600K` CSP LED + micro-Fresnel lens | `2.4 x 1.6 x 0.65` | `0.10` | `±0.03 mm` | MON-8 |
| 29 | In-ring micro-speaker transducer | neodymium balanced micro-speaker (`78 dB`) | `9.0 x 3.2 x 2.20` | `0.60` | `±0.03 mm` | MON-6 |
| 28 | In-ring dual MEMS microphones | `68 dB` SNR + ePTFE `IP68` acoustic mesh | `2 x (2.7 x 1.8 x 0.9)` | `0.30` | `±0.03 mm` | MON-7 |
| 27 | 4-blade mechanical aperture shutter | carbon-fiber micro-blades (`f/1.8` - `f/4.0`) | `Ø12.8 x 0.35` | `0.15` | `±0.01 mm` | MON-3 |
| 26 | `G1` front aspheric doublet | molded glass (`2` elements) | `Ø12.0 x 1.35` | `0.35` | `±2 µm` | MON-3 |
| 25 | `45°` lanthanum folding prism | high-index lanthanum glass (`n = 1.88`) | `3.4 x 3.4 x 2.60` | `0.55` | `±5 arcsec` | MON-3 |
| 24 | `5P` horizontal apochromatic lens barrel | `5` glass/polymer elements (`f = 8.9 mm`, `f/1.8`) | `Ø11.6 x 13.8` | `0.70` | `±2 µm` | MON-3 |
| 23 | Closed-loop VCM autofocus actuator | ball-guided voice-coil motor (`200 µm` stroke) | `14.0 x 11.0 x 0.9` | `0.30` | `±2 µm` | MON-3 |
| 22 | Blue-glass IR-cut filter & field flattener | anti-reflective `650 nm` cut filter | `13.2 x 10.0 x 0.35` | `0.18` | `±5 µm` | MON-3 |
| 21 | 1-inch class `50 MP` CMOS sensor | `12.8 x 9.6 x 0.65 mm` (`z = 0.90..1.55 mm`) | `12.8 x 9.6 x 0.65` | `0.85` | `±0.02 mm` | MON-3 |
| 20 | 4-axis sensor-shift OIS flexure stage | SMA/piezo 4-axis OIS carriage (`±1.8°`) | `15.2 x 12.2 x 0.85` | `0.55` | `±0.02 mm` | MON-3 |
| 19 | Annular 6-layer HDI main PCBA | `Ø30.2 / Ø24.4 x 0.55 mm` inside ring wall | `Ø30.2 / Ø24.4 x 0.55` | `1.45` | `±0.03 mm` | MON-10 |
| 18 | `U1` Quad-Tile Master TCON & LUT ASIC | drives `Q1..Q4` + `<0.5%` seam luminance LUT | `5.2 x 5.2 x 0.45` | `0.22` | `±0.02 mm` | DSP-10, MON-10 |
| 17 | `U2` Zero-CPU `UWB / mmWave` SiP | `60 GHz` + `UWB` + `Wi-Fi 7` thin-client transceiver | `6.0 x 5.5 x 0.50` | `0.30` | `±0.02 mm` | RF-19, MON-10 |
| 16 | `U3` Audio DSP & `U4` `3 ms` Dead-Pad PMIC | spatial audio codec + `3 ms` challenge-response IC | `2 x (3.2 x 3.2 x 0.4)` | `0.15` | `±0.02 mm` | MON-6, MON-10 |
| 15 | Solid-state `LLZO` bridge cell (`0.45 Wh`) | curved `120 mAh` solid-state arc cell in ring wall | `18.0 x 4.2 x 1.20` | `1.20` | `±0.04 mm` | MON-13 |
| 14 | Flat circular ring housing (`r = 0.55` soft) | anodized 6061-T6 (`#93a68c`, lies flat on screen) | `32.0 x 32.0 x 4.00` | `4.50` | `±0.03 mm` | MON-1, MON-9 |
| 13 | **Reversible `±90°` Grade-5 Ti micro-hinge** | twin-cam detented Ti barrel (`+90° / 0° / -90°`) | `Ø2.2 x 18.0` | `0.95` | `±0.01 mm` | MON-1, MON-5 |
| 12 | **20-line LCP coaxial hinge flex ribbon** | rated `100 000` cycles across `±90°` stem bend | `16.0 x 6.5 x 0.18` | `0.20` | `±0.02 mm` | MON-5, MON-11 |
| 11 | **`90°`-bent stem housing (`r = 0.55` soft)** | Grade-5 Ti + LCP RF window (`8.0 x 32.0 x 4.50 mm`) | `8.0 x 32.0 x 4.50` | `2.35` | `±0.03 mm` | MON-1, MON-9 |
| 10 | **Sole `USB Type-C` receptacle (`40 W` PD, `IP68`)** | 24-pin waterproof USB-C port inside `90°` B stem | `8.9 x 7.3 x 3.10` | `0.85` | `±0.03 mm` | RL-1, MON-5 |
| 9 | `U_PD` `USB-PD 3.1` (`40 W`) + `DP 2.1` controller | bidirectional power & DisplayPort Alt-Mode IC | `3.5 x 3.5 x 0.40` | `0.10` | `±0.02 mm` | RL-1, RL-2 |
| 8 | Stem 3-band LCP antenna (`Wi-Fi 7` / `BT` / `UWB`) | laser-structured monopole + slot in `90°` stem | `29.4 x 3.4 x 0.25` | `0.25` | `±0.02 mm` | MON-11, RF-9 |
| 7 | Stem `1x4` `60 GHz` phased-array patch antenna | beam-steered Zero-CPU video link (`SAR 0.054 W/kg`) | `14.0 x 3.2 x 0.30` | `0.20` | `±0.02 mm` | RF-19, MON-11 |
| 6 | Multi-edge magnetic dock array (`8 x N52H`) | bipolar `N52H` magnets in `90°` stem clip (`7.2 N`) | `8 x (3.2 x 1.6 x 1.1)` | `1.55` | `±0.02 mm` | MON-5 |
| 5 | Symmetric 12-pin gold pogo contact array | `12` hard-gold pogo pins (`18 mΩ`, front/back reversible) | `22.0 x 3.0 x 0.55` | `0.45` | `±0.02 mm` | MON-5 |
| 4 | Stem & ring waterproof `IP68` FKM gaskets | 60 Shore A fluoroelastomer seals + soft screen pad | `30.0 x 3.6 x 0.40` | `0.25` | `±0.02 mm` | MON-12 |
| 3 | Mid-plane Cu-graphite optical-to-display shield | `1 200 W/m·K` thermal & EMI barrier (`z = 0.75..0.90`) | `Ø23.6 x 0.15` | `0.15` | `±0.02 mm` | MON-4, MON-13 |
| 2 | Rear round LTPO AMOLED panel (`Ø22.4 mm`) | `480 x 480 px` (`300 ppi`, `1-120 Hz`, `z = 0.35..0.75`) | `Ø23.2 x 0.40` | `0.25` | `±0.02 mm` | MON-4 |
| 1 | Rear sapphire window (`z = 0.00..0.35 mm`) | optical sapphire + oleophobic coat against screen | `Ø24.0 x 0.35` | `0.20` | `±0.02 mm` | MON-4, MON-12 |
| **Total** | **32 internal parts** | **`90°`-bent stem (`USB-C` + RF) + flat ring on screen** | **`40 x 44 x 6.70 mm` bent** | **`22.00 g`** | | **MON-1..20** |
