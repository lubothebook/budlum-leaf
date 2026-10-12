# BUDLUM LEAF · HARDWARE · 02 · THE ELECTRONICS AND THE BUSES

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ: the conductors are AgNW only, because ITO cracks under stretch. "Zero CPU" means no general-purpose processor, and a `16 MB` frame store is allowed. The MB block gains `U2A`, `U2B`, `U5` to `U8`. The ST block holds antennas and contacts only.

**Revision L.5.0 · 2026-10-12**.
This file specifies every circuit block, invisible `AgNW/ITO` bus, `64`-contact `+` seam bus, and wireless power rail in the Budlum Leaf (`pafta/E01-SISTEM-KAMERA-VE-PORT.svg`). The device uses a **Zero-CPU (`Sıfır CPU`) and Zero-RAM** thin-client architecture where heavy compute runs on network validators or hubs. The `90°`-bent-stem B module holds the **`U1` Quad-Tile Master TCON**, **`U2` `UWB / mmWave` SiP**, and **sole `USB Type-C` port**,. While the portless 4-quadrant screen body holds the `12.0 Wh` solid-state battery and `Qi2.2` wireless charging receivers.

---

## 1 · Electronic blocks across the 4-Quadrant (`+`) body and `90°`-bent-stem B module

| Block | Location | Dimensions | Subsystems | Typical draw |
| --- | --- | --- | --- | --- |
| **QB (`x 4` Quadrant BMS & Qi2 Nodes)** | inside each `40 x 80 x 2.00 mm` tile (`Q1..Q4`) | `14.0 x 4.5 x 0.45 mm` | `U_QI` Qi2.2/Qi rectifier, `3 ms` Dead-Pad FET, `36.2 C` hardware NTC comparator, tile LUT EEPROM | `0.06 W` per tile |
| **DB (Invisible AgNW/ITO & Edge-Wrap Bus)** | inside each tile + Corning edge-wrap conductors | `39.8 x 79.8 x 0.04 mm` | transparent `12 Ω/sq` power/data mesh, `PDLC` privacy drive, `240 Hz` touch/pen sensing | `0.28 W` total (4 tiles) |
| **SB (`+` Cross 64-Contact Seam Bus)** | along `x = 0` (`160 mm`) and `y = 0` (`80 mm`) | `4 x 16` gold micro-leaves | `VSYS_HV` (`3.8-4.4 V`), `QI2_AC_RING`, `MIPI_TILE_SYNC`, `1-Wire` Dead-Pad auth | `<8 mW` loss (`18 mΩ`) |
| **MB (`90°` B Module Annular 6L PCBA)** | inside the `Ø32.0 / Ø24.0 mm` flat ring of the B module | `Ø30.2 / Ø24.4 x 0.55 mm` | **`U1` Quad-Tile Master TCON**, **`U2` `UWB / mmWave` SiP**, **`U3` Audio DSP**, **`U4` Dead-Pad PMIC**, `50 MP` CMOS + round AMOLED | `0.55 W` active / `2.1 W` capture |
| **ST (`90°` Bent B Stem USB-C & RF Flex)** | inside the `8.0 x 32.0 x 4.50 mm` `90°`-bent stem | `7.2 x 30.4 x 0.35 mm` | **sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`)**, `U_PD` controller, 3-band LCP antenna + `1x4` `60 GHz` array | `0.04 W` idle |

---

## 2 · The 16-contact `+` seam bus (`64` contacts total) and 12-pin B module dock (`3 ms` Dead-Pad, `IP68`)

Each of the 4 internal `+` cross half-axes (`+X`, `-X`, `+Y`, `-Y`) carries `16` recessed gold-plated BeCu micro-leaf contacts (`64` total),. Also, the `90°` B stem clip mates via `12` gold pogo pins (`8` N52H magnets, `7.2 N`). All contacts stay at `0 V` (`Dead-Pad`) until a **`3 ms` cryptographic handshake** completes:

| Contacts | Signal | Specification |
| --- | --- | --- |
| **Contacts 1 to 3** | `VSYS_HV` (`3.8 V` to `4.4 V` solid-state bus, up to `3.0 A`) | balances the `4 x 3.0 Wh = 12.0 Wh` `LLZO/PEO` quadrant cells (`18 mΩ` gold-on-gold) |
| **Contacts 4 to 6** | `GND_RETURN` (bifilar current-canceling return) | mates `0.25 mm` first; pairs with `VSYS_HV` to keep external magnetic field `<0.08 µT` |
| **Contacts 7 to 8** | `QI2_AC_RING` (`110-360 kHz` AC phase bridge) | links the `4 x 90°` `Ø54.0 mm` `Qi2.2` MPP sectors into a closed `15-25 W` loop when all 4 tiles join |
| **Contacts 9 to 12** | `MIPI_TILE_SYNC` (`4 Gbit/s` differential display lanes) | routes pixel streams and `<0.5%` seam luminance LUT sync from `U1` Master TCON across `Q1..Q4` |
| **Contacts 13 to 14** | `TOUCH_PDLC_SYNC` (`240 Hz` touch + `PDLC` privacy AC drive) | synchronizes touch/pen coordinates and low-voltage `PDLC` privacy switching across all 4 tiles |
| **Contacts 15 to 16** | `1WIRE_DEADPAD_NTC` (`3 ms` auth + `36.2 C` ocular thermal line) | **`3 ms` challenge-response** before FET power-on; hardware cut-off at **`36.2 C`** in eyewear mode |
