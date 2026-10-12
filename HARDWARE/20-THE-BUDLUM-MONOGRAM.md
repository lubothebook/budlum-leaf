# BUDLUM LEAF · HARDWARE · 20 · THE 90°-BENT-STEM BUDLUM B MODULE · FLAT RING ON SCREEN, SOLE USB-C, CAMERA, REAR PANEL AND ZERO-CPU CORE

**Revision L.5.0 · 2026-10-12 (authoritative specification of the `20.0 g`, 32-part `90°`-bent-stem B module)**.
Modeled 1:1 from `uploads/b.png` (`40.0 x 32.0 mm` plan silhouette), the Budlum B module bends **only its straight antenna. Also, USB-C stem (`çubuk`) at a `90°` right angle (`dik açıyla`)** so that **only the stem stays up along the screen edge**. While the **entire circular ring (`yuvarlak`) lies flat on top of the screen surface** (`pafta/P14`, `pafta/P15`, `pafta/P21`, `pafta/P22`, `cad/models/monogram-module.stl`). `[DECISION]`

---

## 1 · Exact 1:1 geometry from `uploads/b.png` and the `90°` stem bend

| Feature of the B module | Unfolded 1:1 `uploads/b.png` (`51.25 px/mm`) | Revision L.5.0 `90°`-Bent-Stem 3D geometry | Role in the system |
| --- | --- | --- | --- |
| Overall silhouette | `2 050 x 1 638 px` (`40.00 x 32.00 mm`) | **`32.0 x 32.0 x 4.00 mm` flat ring on screen + `8.0 x 32.0 x 4.50 mm` `90°`-bent stem** | 1:1 `b` geometry with `90°` right-angle stem bend (`20.0 g`) |
| Straight stem (`çubuk`) | left bar (`4.0..8.0 mm` bridge x `32.0 mm`) | **bent `90°` (`dik açıyla`) via a reversible `±90°` Grade-5 Ti micro-hinge (`Ø2.2 x 18.0 mm`)** | **only the stem stays up/wraps the edge; holds sole `USB-C` + 3-band/60GHz antennas** |
| Circular ring (`yuvarlak`) | outer `Ø1 638 px` (`Ø32.0 mm`), inner `Ø1 230 px` (`Ø24.0 mm`) | **lies flat on top of the screen surface (`z = +1.10..+5.10 mm` front or `-1.10..-5.10 mm` back)** | **houses `50 MP` folded camera, rear `Ø22.4 mm` AMOLED, audio, and 6L Zero-CPU PCBA** |
| Reversible multi-edge docking | bottom baseline in L.4.1 | **clips onto all 4 edges (`Top`, `Bottom`, `Left`, `Right`) and both faces (`Front +Z` or `Back -Z`)** | moving the `90°` stem lets the camera module attach to the front or back of the screen |
| Softening of all 90° edges | all outer perimeter edges | **`r = 0.55 mm` radius fillet on all 90-degree edges of the stem and flat ring** | smooth tactile grip with zero sharp edges |

---

## 2 · What lives inside the `90°`-bent-stem B module (`32` internal parts, zero pieces outside `b`)

1. **The `90°`-bent stem (`çubuk`, `8.0 x 32.0 x 4.50 mm`) holds the antennas and the ONLY `USB Type-C` port**.
   - **Sole `USB Type-C` receptacle (`40 W PD 3.1 + DP 2.1`, IP68)** + `U_PD` controller. The 4-quadrant screen body has zero USB-C ports and zero buttons (charging wirelessly via `Qi2.2`),. So all wired charging/data goes through the `90°` B stem.
   - **3-band LCP antenna (`Wi-Fi 7`, `BT 5.4`, `UWB`) + `1x4` `60 GHz` phased array**. Kept away from the eye and hand along the `90°` stem (`SAR = 0.054 W/kg`).
   - **Reversible `±90°` Grade-5 Ti hinge + `8 x N52H` (`7.2 N`). Also, `12` gold pogo pins (`3 ms` Dead-Pad, IP68)**. Allows docking on any edge and flipping between Front (`+Z`) and Back (`-Z`).
2. **Upper Z-stack of the flat circular ring (`z = 0.90..4.00 mm` inside `Ø24.0 mm` bore): `50 MP` camera. OIS, prism, and audio**.
   - **Front sapphire window (`z = 3.60..4.00 mm`)**, **`50 MP` (`12.8 x 9.6 x 0.65 mm`) CMOS (`z. = 0.90..1.55 mm`)**, **4-axis OIS**, **lanthanum `45°` folding prism**, and **`5P` apochromatic lens barrel (`z = 0.90..3.60 mm`)**.
   - **In-ring audio & flash**. `2 x MEMS` mics (`68 dB` SNR), `9.0 x 3.2 x 2.2 mm` speaker (`78 dB`),. Also, dual-CCT LED flash.
3. **Annular 6-layer Zero-CPU PCBA (`Ø30.2 / Ø24.4 x 0.55 mm`) inside the ring wall**.
   - Houses **`U1` Quad-Tile Master TCON** (driving `Q1..Q4` + `<0.5%` `+` seam luminance LUT). **`U2` Zero-CPU `UWB / mmWave` SiP**, **`U3` Audio DSP**, **`U4` `3 ms` Dead-Pad PMIC**,. Also, a **`0.45 Wh` (`120 mAh`) solid-state bridge cell**.
4. **Lower Z-stack of the flat circular ring (`z = 0.00..0.90 mm`): shield and rear round AMOLED**.
   - **`0.15 mm` Cu-graphite shield (`z = 0.75..0.90 mm`)** isolating the camera sensor from the rear display.
   - **`Ø22.4 mm` round LTPO AMOLED (`480 x 480 px`, `300 ppi`, `1-120 Hz`, `z = 0.35..0.75 mm`)**. Also, **`0.35 mm` rear sapphire window (`z = 0.00..0.35 mm`)**.

---

## 3 · Verification gates `MON-1` to `MON-20`

| Gate | Subject | Pass criterion |
| --- | --- | --- |
| **MON-1** | 1:1 `uploads/b.png` silhouette with **only the stem (`çubuk`) bent `90°` (`dik açıyla`)** and the round ring flat on the screen | contour within `±0.10 mm`; `±90°` Ti hinge locks cleanly at `+90°` (Front) and `-90°` (Back) |
| **MON-2** | `4.00 mm` flat ring Z-stack (`z = 0.00..4.00 mm`) with zero internal Z-overlap across all `32` parts | `0.35` rear sapphire + `0.40` AMOLED + `0.15` shield + `2.70` CMOS/optics + `0.40` front sapphire = `4.00 mm` |
| **MON-3** | Fixed `50 MP` (`12.8 x 9.6 x 0.65 mm`) camera, 4-axis OIS, prism, and `5P` lens. It covers the flat ring (`z = 0.90..3.60 mm`) | MTF and `84°` FOV verified; zero collision with rear AMOLED |
| **MON-4** | Rear round LTPO AMOLED (`Ø22.4 mm`, `480 x 480 px`, `300 ppi`, `1-120 Hz`) + `0.15 mm` Cu-graphite shield | clock, widgets, and selfie viewfinder verified; `<0.5 K` thermal coupling from CMOS |
| **MON-5** | Reversible 4-edge (`Top`, `Bottom`, `Left`, `Right`) and Front (`+Z`) / Back (`-Z`) docking via `8` N52H (`7.2 N`) + `12` gold pins | `7.2 N ± 10%` hold on all 4 edges; automatic orientation & LUT flip in `<5 ms` |
| **MON-6..8** | In-ring micro-speaker (`9.0 x 3.2 x 2.2 mm`, `78 dB`), `2 x MEMS` mics (`68 dB` SNR), and dual-CCT flash | full acoustic and flash compliance inside the flat ring bezel |
| **MON-9** | Softening of all 90-degree edges on the `90°` stem and flat ring (`r = 0.55 mm`) | `r = 0.55 ± 0.05 mm` fillet verified; passes `10 N` tactile probe test |
| **MON-10** | `U1` Quad-Tile Master TCON, `U2` Zero-CPU `UWB / mmWave` SiP, and `3 ms` Dead-Pad authentication | `<3 ms` handshake; `<1.5 ms` wireless frame latency; `<0.5%` `+` seam luminance step |
| **MON-11** | `90°` stem 3-band LCP antenna + `1x4` `60 GHz` array and **sole `USB Type-C` (`40 W PD 3.1`)** port | `>62%` RF efficiency; `SAR = 0.054 W/kg`; `40 W` USB-C PD verified |
| **MON-12..20** | `IP68` sealing, `0.45 Wh` bridge cell, `1.5 m` drop, `50 000`-cycle hinge & dock life, salt fog, and laser marking | all 30 test units pass without defect |
