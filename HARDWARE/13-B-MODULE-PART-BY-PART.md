# BUDLUM LEAF · HARDWARE · 13 · THE B MODULE, PART BY PART (32 PARTS)

**Revision L.6.0 · 2026-10-12**. This file lists the **32 parts** of the Budlum B module (`12.0 g`). The decisions behind it live in `FINAL/21-stretch-stem-and-projection.md`. Where an older sheet or STL disagrees, this file and Part 21 win until the sheet is redrawn.

---

## 1 · The architecture of the 32-part B module

Modeled from `uploads/b.png`. The stem (`çubuk`) is bent `90°` to the ring in one moulded corner. No hinge is added.

- **The stem, `8.0 x 32.0 x 1.00 mm`**. A glass-filled LCP wall that stands perpendicular to the screen, against its edge. It holds the antennas A1, A2 and A4, and the `12` dock contact leaves. It holds no port, no magnet and no metal shell.
- **The flat ring, `Ø32.0 x 4.00 mm`**. It lies on the front or the back face. It holds the camera, the rear panel, the audio and the bridge cell. It also holds the rim USB-C receptacle and all the silicon.
- **No metal shell**. The ring and stem shells are LCP-GF40, so the antennas radiate. The metal inside is the camera, the shields and the cans.

---

## 2 · The bill of materials (`12.01 g`)

| No | Part | Material and specification | Dimensions (`mm`) | Mass (`g`) | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | Stem shell with the moulded `90°` corner | LCP, 40 % glass fibre, `r = 0.40 mm` edges | `8.0 x 32.0 x 1.00` | `0.44` | MON-20, MEC-42 |
| 2 | A1 inverted-F and A2 coupled arm | laser direct structured copper on the stem | `29.4 x 5.5 x 0.05` | `0.02` | RF-9, RF-22 |
| 3 | A4 `1 x 4` `60 GHz` patch array | two-layer LCP flex on the mmWave layer | `14.0 x 3.2 x 0.10` | `0.05` | RF-19 |
| 4 | Dock contact leaves | `12` hard-gold spring leaves, `0.15 mm` stroke | `30.0 x 2.0 x 0.20` | `0.08` | MON-18, MON-16 |
| 5 | Corner flex through the moulded bend | 20-line LCP flex, `100 000` flex cycles | `16.0 x 6.5 x 0.10` | `0.10` | MON-11 |
| 6 | Ring shell | LCP, 40 % glass fibre, matte, no metal | `Ø32.0 x 4.00` | `2.20` | MON-1, RF-23 |
| 7 | Front sapphire window | sapphire with AR coat | `Ø24.0 x 0.30` | `0.54` | MON-3 |
| 8 | Rear sapphire window | sapphire with oleophobic coat | `Ø24.0 x 0.30` | `0.54` | MON-4 |
| 9 | Rear round LTPO AMOLED | `480 x 480 px`, `1-120 Hz` | `Ø23.2 x 0.40` | `0.25` | MON-4 |
| 10 | Cu-graphite shield | thermal and EMI barrier | `Ø23.6 x 0.15` | `0.15` | MON-13 |
| 11 | Camera module | `13 MP`, `1/3.06"` class, direct `4P` stack | `8.5 x 8.5 x 3.40` | `0.60` | CAM-21 |
| 12 | LED flash | `2700K + 5600K` CSP | `2.4 x 1.6 x 0.65` | `0.10` | MON-8 |
| 13 | Micro-speaker | balanced micro-speaker | `9.0 x 3.2 x 2.20` | `0.60` | MON-6 |
| 14 | Two MEMS microphones | `68 dB` SNR, ePTFE mesh | `2 x (2.7 x 1.8 x 0.9)` | `0.06` | MON-7 |
| 15 | Ring PCBA | 8-layer HDI, rigid | `Ø30.0 x 0.55` | `1.40` | MON-10 |
| 16 | `U1` TCON and local compositor | quad-tile drive, stretch warp, four fixed jobs | `5.2 x 5.2 x 0.45` | `0.10` | DSP-17, SW-21 |
| 17 | `U2A` Wi-Fi 7 and BT combo | `2 x 2`, `320 MHz`, multi-link `5 + 6 GHz` | `5.0 x 5.0 x 0.60` | `0.10` | RF-22 |
| 18 | `U2B` `60 GHz` and UWB | dock link and ranging | `5.0 x 4.5 x 0.60` | `0.10` | RF-19 |
| 19 | `U5` 5G RedCap modem | with RF front end and eSIM | `8.0 x 7.0 x 0.80` | `0.40` | RF-17 |
| 20 | `U6` slice decoder and frame store | AV1 and HEVC, `16 MB` store | `6.0 x 6.0 x 0.70` | `0.15` | SW-21 |
| 21 | `U7` secure element | wallet keys, lease check, receipts | `2.0 x 2.0 x 0.40` | `0.02` | SW-22 |
| 22 | `U8` IMU | seat, face and tuner input | `2.0 x 2.0 x 0.70` | `0.02` | RF-23 |
| 23 | `U3` audio codec and `U4` power chip | codec, PMIC, dead-pad switch | `2 x (3.2 x 3.2 x 0.4)` | `0.10` | MON-16 |
| 24 | A3 ring loop | laser direct structured copper on the ring rim | `Ø31.0 loop` | `0.02` | RF-22 |
| 25 | Aperture tuners | three switched matching networks | `3 x (1.5 x 1.0 x 0.4)` | `0.03` | RF-23 |
| 26 | USB-C receptacle | mid-mount, `IP68`, in the ring rim | `8.9 x 7.3 x 3.10` | `0.60` | MON-22 |
| 27 | `U_PD` controller | USB-PD 3.1 and DP Alt mode | `3.5 x 3.5 x 0.40` | `0.05` | RL-1 |
| 28 | Dock magnets | `8` N52H in the ring underside, away from A1 | `8 x (3.2 x 1.6 x 1.1)` | `0.34` | MON-5 |
| 29 | Bridge cell | solid-state, `0.45 Wh` | `18.0 x 4.2 x 1.20` | `1.20` | MON-13 |
| 30 | Gaskets | FKM, 60 Shore A | `30.0 x 3.6 x 0.40` | `0.25` | MON-12 |
| 31 | Spreader and latent buffer | graphite sheet and `1.0 g` phase change material | `Ø28.0 x 0.80` | `1.10` | MEC-11 |
| 32 | Shield cans | nickel silver, over `U2A`, `U2B`, `U5` | `3 cans` | `0.30` | RF-17 |
| **Total** | **32 parts** | **`1.00 mm` stem and flat ring** | **`40 x 32 x 8.0 mm` envelope** | **`12.01`** | |

All masses are `[HYPOTHESIS]` until the first build weighs them.

---

## 3 · What changed from L.5.0

| L.5.0 | L.6.0 | Why |
| --- | --- | --- |
| stem `4.50 mm`, titanium | stem `1.00 mm`, LCP-GF40 | the order of Ayaz, and metal defeats the antenna |
| `±90°` titanium hinge | moulded corner | the original `b.png` has no hinge |
| USB-C in the stem | USB-C in the ring rim | a `3.10 mm` receptacle does not fit a `1.00 mm` wall |
| `50 MP` folded camera | `13 MP` direct module | the old camera did not fit the ring (gap G-13) |
| one `U2` SiP | `U2A`, `U2B` and `U5` | no single shipping part does all three jobs |
| aluminium ring | LCP-GF40 ring | no metal shell around the radios |
| `20.0 g` stated, `22.00 g` summed | `12.01 g` summed | one number, from the list |
