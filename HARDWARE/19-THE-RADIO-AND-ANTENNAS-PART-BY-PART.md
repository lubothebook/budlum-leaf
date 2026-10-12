# BUDLUM LEAF · HARDWARE · 19 · THE RADIO, ANTENNAS AND ZERO-CPU UWB / MMWAVE TRANSCEIVER

**Revision L.5.0 · 2026-10-12**.
In Revision L.5.0, the Budlum Leaf operates on a **Zero-CPU (`Sıfır CPU`) and Zero-RAM** thin-client architecture. This heavy compute runs on network validators or hubs. Aside from `Qi2.2` wireless charging on the screen body, all active RF and compute-link functions live inside the **`90°`-bent-stem B module (`20.0 g`)**. Assisted by transparent `AgNW/ITO` diversity apertures in the 4-quadrant screen perimeter (`pafta/P05`, `pafta/P20`).

---

## 1 · Why placing the antennas and `60 GHz` array in the `90°`-bent B stem protects the eye (`SAR = 0.054 W/kg`)

1. **Spatial and angular isolation from the eye and hand**. Because **only the stem (`çubuk`, `8.0 x 32.0 x 4.50 mm`) is bent at a `90°` right. Angle (`dik açıyla`)** along the outer edge while the round ring lies flat on the screen. All primary RF radiators (`Wi-Fi 7`, `BT 5.4`, `UWB`,. Also, `1x4` `60 GHz` phased array) sit outside the periocular zone and away from the user's grip.
2. **Orthotropic graphene + `Mu-metal` ocular shield in every quadrant (`Q1..Q4`)**. Each `40 x 80 x 2.00 mm` tile contains a `Mu-metal`. Also, graphene ground plane (`>35 dB` front-to-back isolation), directing `60 GHz` and `UWB` beams outward. Also, keeping Head/Eye **`SAR = 0.054 W/kg`** (`37x` below the ICNIRP `2.0 W/kg` limit).
3. **Zero-CPU `U2` `UWB / mmWave` SiP in the flat B ring**. The `U2` transceiver (`6.0 x 5.5 x 0.50 mm`). It covers the `Ø30.2 / Ø24.4 mm` 6-layer ring PCBA feeds the `90°` stem antennas. It covers the 20-line LCP coaxial hinge flex (`<0.35 dB` loss at `60 GHz`). Delivering `<1.5 ms` compressed frame streaming to `U1` Quad-Tile Master TCON.

---

## 2 · The 8 antenna and transceiver elements across the `90°` B stem and 4-Quadrant (`+`) perimeter

| ID | Location | Frequency band | Construction | Peak gain / spec | Gate |
| --- | --- | --- | --- | --- | --- |
| **A1** | `90°`-bent B stem (`çubuk`, long arm) | `2.40 to 2.485 GHz` (`Wi-Fi` / `BT 5.4`) | `29.4 mm` laser-structured LCP monopole in `90°` stem | `+2.6 dBi` | MON-11, RF-9 |
| **A2** | `90°`-bent B stem (`çubuk`, coupled arm) | `5.15 to 7.125 GHz` (`Wi-Fi 7` 6E/7) | `12.8 mm` coupled LCP radiator in `90°` stem | `+3.6 dBi` | MON-11, RF-9 |
| **A3** | `90°`-bent B stem (`çubuk`, cavity slot) | `6.20 to 8.20 GHz` (`UWB` ranging & sync) | `9.6 x 1.2 mm` cavity-backed slot in `90°` stem | `+2.8 dBi`, `±2 cm` ToF | MON-11, RF-9 |
| **A4** | `90°`-bent B stem (`1x4` `60 GHz` array) | `57.0 to 66.0 GHz` (`802.11ay` / Zero-CPU stream) | `14.0 x 3.2 x 0.30 mm` 4-element LCP patch array | `+8.8 dBi`, `<1.5 ms` latency | RF-19, MON-11 |
| **A5** | Quadrant `Q1 / Q2` top `AgNW/ITO` slot | `0.70 to 3.80 GHz` (`5G Sub-6` primary) | `38.0 mm` transparent `AgNW/ITO` perimeter slot | `+1.8 dBi` (coupled via B dock) | RF-9, RF-18 |
| **A6** | Quadrant `Q3 / Q4` bottom `AgNW/ITO` slot | `0.70 to 3.80 GHz` (`5G Sub-6` diversity) | `38.0 mm` transparent `AgNW/ITO` perimeter slot | `+1.8 dBi` | RF-9, RF-18 |
| **A7** | Quadrant `Q2` outer corner patch | `1.575 / 1.176 GHz` (`GNSS L1/L5`) | `12.0 x 18.0 mm` transparent `AgNW/ITO` patch | `+1.4 dBi` | RF-18 |
| **A8** | Central `+` cross `Qi2.2` / `NFC` loop | `13.56 MHz` (`NFC`) + `110-360 kHz` (`Qi2.2`) | `Ø54.0 mm` 4-sector coil + `30 x 16 mm` `NFC` loop | `40 mm` NFC read / `15-25 W` Qi2.2 | RF-15, ENR-12 |
