# BUDLUM LEAF · HARDWARE · 05 · THE 90°-BENT-STEM B MODULE · FLAT RING ON SCREEN, SOLE USB-C, CAMERA, REAR PANEL AND ZERO-CPU CORE

**Revision L.5.0 · 2026-10-12 · single source of truth for the `90°`-bent-stem B module (`20.0 g`, 32 parts)**.
Modeled 1:1 from `uploads/b.png` (`40.0 x 32.0 mm` plan silhouette), the B module bends **only its straight antenna. Also, USB-C stem (`çubuk`) at a `90°` right angle (`dik açıyla`)** so that **only the stem stays up along the screen edge**. While the **entire circular ring (`yuvarlak`) lies flat on top of the screen surface** (`pafta/P14`, `pafta/P15`, `pafta/P21`).

---

## 1 · The six rules of the `90°`-bent-stem B module

1. **Only the stem (`çubuk`) bends `90°` (`dik açıyla`); the round ring (`yuvarlak`) lies flat on the screen**. A reversible `±90°` Grade-5 Titanium micro-hinge (`Ø2.2 x 18.0 mm`) lets the `8.0 x 32.0 x 4.50. Mm` stem stand perpendicular (`90°`) to the screen edge. While the `32.0 x 32.0 x 4.00 mm` ring rests flat on the screen (`z = +1.10..+5.10. Mm` front or `-1.10..-5.10 mm` back).
2. **Reversible 4-edge and Front (`+Z`) / Back (`-Z`) placement**. By hooking the `90°`-bent stem onto the Top (`y = +80 mm`), Bottom (`y = -80 mm`). Left (`x = -40 mm`), or Right (`x = +40 mm`) edge. The user docks the B module on **either the front or the back of the screen**.
3. **The `90°`-bent stem holds the 3-band antenna, `60 GHz` array, and the ONLY `USB Type-C` port**. Because the screen body has zero USB-C ports, the `40 W` `USB-PD 3.1. Also, DP 2.1` (`IP68`) receptacle lives exclusively inside the `90°`-bent stem alongside the `Wi-Fi 7`, `BT 5.4`, `UWB`. And `1x4` `60 GHz` antennas (`SAR = 0.054 W/kg`).
4. **The flat circular ring (`Ø32.0 mm` outer / `Ø24.0 mm` inner aperture, `4.00 mm` thick) holds the camera. Rear round AMOLED, and acoustics**:
   - **Upper optical & audio stack (`z = 0.90..4.00 mm`)**. Front `Ø24.0 mm` sapphire window, `50 MP` (`12.8 x 9.6 x 0.65 mm`) CMOS sensor, 4-axis OIS. Folded prism, `5P` lens barrel, `2 x MEMS` mics, `9.0 x 3.2 x 2.2 mm` speaker, and dual-CCT flash.
   - **Lower display stack (`z = 0.00..0.90 mm`)**. `0.15 mm` Cu-graphite shield, `Ø22.4 mm` (`480 x 480 px`, `1-120 Hz`) round LTPO AMOLED,. Also, `0.35 mm` rear sapphire window.
5. **Aside from wireless charging, all functions require the B module**. Its 6-layer annular PCBA (`Ø30.2 / Ø24.4 x 0.55 mm`) houses `U1` Quad-Tile Master TCON. `U2` Zero-CPU `UWB / mmWave` SiP, `U3` Audio DSP, and `U4` `3 ms` Dead-Pad PMIC.
6. **All 90-degree outer edges of the stem and ring are softened (`r = 0.55 mm`)**.

---

## 2 · Key dimensions and performance numbers

| Parameter | Value | Gate |
| --- | --- | --- |
| Flat ring envelope on screen | `32.0 x 32.0 x 4.00 mm` (`Ø32.0 mm` outer / `Ø24.0 mm` inner opening, `r = 0.55 mm` edges) | MON-1, MON-2 |
| `90°`-bent stem (`çubuk`) envelope | `8.0 x 32.0 x 4.50 mm` bent at `90°` via reversible `±90°` Grade-5 Ti micro-hinge (`50 000` cycles) | MON-1, MON-9 |
| Sole `USB Type-C` receptacle | `40 W` USB-PD 3.1 + `DP 2.1` + USB 3.2 (`IP68`), located exclusively in the `90°`-bent stem | RL-1, MON-5 |
| Zero-CPU silicon in annular ring | `U1` Quad-Tile Master TCON + `U2` `UWB / mmWave` SiP (`<1.5 ms` latency) + `U3` Audio DSP + `U4` PMIC | MON-10, RF-19 |
| Front camera sensor & optics | `50 MP` (`12.8 x 9.6 x 0.65 mm`) CMOS + 4-axis OIS + folded prism. Also, `5P` lens barrel (`z = 0.90..3.60 mm`) | MON-3 |
| Rear round AMOLED panel | `Ø22.4 mm` active (`480 x 480 px`, `300 ppi`, `1-120 Hz` LTPO, `z = 0.35..0.75 mm`) + `0.35 mm` sapphire | MON-4 |
| In-ring audio and flash | `2 x MEMS` microphones (`68 dB` SNR) + `9.0 x 3.2 x 2.2 mm` speaker (`78 dB`) + dual-CCT flash | MON-6, MON-7, MON-8 |
| Multi-edge magnetic & pogo dock | `8 x N52H` (`7.2 N` hold) + `12` gold pogo pins (`3 ms` Dead-Pad, `IP68`) on Top, Bottom, Left, or Right edge | MON-5, MON-11, MON-12 |
| Bridge cell and total module mass | `0.45 Wh` (`120 mAh`) solid-state bridge cell (`32` internal parts), **`20.0 g` total mass** | MON-13 |
