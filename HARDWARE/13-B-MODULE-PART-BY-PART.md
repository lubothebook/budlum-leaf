# BUDLUM LEAF · HARDWARE · 13 · THE B MODULE, PART BY PART (32 PARTS)

**Revision L.6.0 · 2026-10-12**. This file lists the **32 parts** of the Budlum B module (`10.8 g`). The decisions behind it live in `FINAL/21-stretch-stem-and-projection.md`. Where an older sheet or STL disagrees, this file and Part 21 win until the sheet is redrawn.

---

## 1 · The architecture of the 32-part B module

Modelled from `uploads/b.png`, `cad/monogram_letter.py` and `cad/models/monogram-module.stl`. The bar (`çubuk`) is bent `90°` to the ring in one moulded corner. No hinge is added.

- **The module is `4.00 mm` thick**. The module STL spans `Z = -2.00..+2.02 mm`.
- **The bar, `32.0 x 4.0 x 1.00 mm`**. It lies horizontally on the top edge of the `2.00 mm` body. It holds the antennas A1, A2 and A4, and the `12` body-link leaves. It holds no port, no magnet and no metal shell.
- **The flat ring, `Ø32.0 x 4.00 mm`**. It lies on the front or the back face. It holds the camera, the rear panel, the audio, the jack, the cell and the silicon.
- **No metal shell**. The ring and bar shells are LCP-GF40, so the antennas radiate. The metal inside is the camera, the jack contacts, the shields and the cans.
- **No USB-C**. USB-C is a separately sold port part. It clips on a free body edge.

---

## 2 · The bill of materials (`10.80 g`)

| No | Part | Material and specification | Dimensions (`mm`) | Mass (`g`) | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | Bar shell with the moulded `90°` corner | LCP, 40 % glass fibre | `32.0 x 4.0 x 1.00` | `0.20` | MON-23 |
| 2 | A1 inverted-F and A2 coupled arm | laser direct structured copper on the bar | `29.4 x 3.6 x 0.05` | `0.02` | RF-9, RF-22 |
| 3 | A4 `1 x 4` `60 GHz` patch array | two-layer LCP flex on the mmWave layer | `14.0 x 3.2 x 0.10` | `0.05` | RF-19 |
| 4 | Body-link leaves | `12` hard-gold spring leaves over the seat tile | `9.6 x 3.0 x 0.25` | `0.08` | MON-18, MON-23 |
| 5 | Corner flex through the moulded bend | 20-line LCP flex, `100 000` flex cycles | `16.0 x 3.5 x 0.10` | `0.10` | MON-11 |
| 6 | Ring shell | LCP, 40 % glass fibre, matte, no metal | `Ø32.0 x 4.00` | `2.20` | MON-1, RF-23 |
| 7 | Front sapphire window | sapphire with AR coat, the camera L1 bonded in | `Ø24.0 x 0.30` | `0.54` | MON-3 |
| 8 | Rear sapphire window | sapphire with oleophobic coat | `Ø24.0 x 0.30` | `0.54` | MON-4 |
| 9 | Rear round LTPO AMOLED | `480 x 480 px`, `1-120 Hz`, `6.5 x 5.3 mm` camera hole | `Ø23.2 x 0.40` | `0.25` | MON-4 |
| 10 | Cu-graphite shield | thermal and EMI barrier | `Ø23.6 x 0.15` | `0.15` | MON-13 |
| 11 | Camera column | `50 MP`, `0.61-0.64 µm`, five-element `f/2.0` lens, `0.12 mm` focus, in-plane OIS | `7.0 x 6.0 x 3.90` | `0.45` | CAM-21 |
| 12 | LED flash | `2700K + 5600K` CSP | `2.4 x 1.6 x 0.65` | `0.10` | MON-8 |
| 13 | Micro-speaker | balanced micro-speaker | `9.0 x 3.2 x 2.20` | `0.60` | MON-6 |
| 14 | Two MEMS microphones | `68 dB` SNR, ePTFE mesh | `2 x (2.7 x 1.8 x 0.9)` | `0.06` | MON-7 |
| 15 | Ring PCBA | 8-layer HDI, rigid | `Ø30.0 x 0.55` | `1.40` | MON-10 |
| 16 | `U1` TCON and local compositor | quad-tile drive, per-tile warp, seam shift | `5.2 x 5.2 x 0.45` | `0.10` | DSP-17, SW-21 |
| 17 | `U2A` Wi-Fi 7 and BT 6.0 combo | `2 x 2`, `320 MHz`, multi-link `5 + 6 GHz` | `5.0 x 5.0 x 0.60` | `0.10` | RF-22 |
| 18 | `U2B` `60 GHz` and UWB | dock link and secure ranging | `5.0 x 4.5 x 0.60` | `0.10` | RF-19, SW-24 |
| 19 | `U5` 5G standalone modem | configured grant, handover, RF front end, eSIM | `10.0 x 8.0 x 0.80` | `0.50` | RF-17, DST-11 |
| 20 | `U6` slice decoder and frame store | AV1 and HEVC, inline slice check, `16 MB` store | `6.0 x 6.0 x 0.70` | `0.15` | SW-21 |
| 21 | `U7` secure element | wallet keys, validator set, receipts | `2.0 x 2.0 x 0.40` | `0.02` | SW-22 |
| 22 | `U8` IMU | seat, face and tuner input | `2.0 x 2.0 x 0.70` | `0.02` | RF-23 |
| 23 | `U3` audio codec and `U4` power chip | codec, PMIC, dead-pad switch | `2 x (3.2 x 3.2 x 0.4)` | `0.10` | MON-16 |
| 24 | A3 ring loop | laser direct structured copper, routed around the jack groove | `Ø31.0 loop` | `0.02` | RF-22 |
| 25 | Aperture tuners | three switched matching networks | `3 x (1.5 x 1.0 x 0.4)` | `0.03` | RF-23 |
| 26 | `3.5 mm` jack | rim groove at `13.8 mm` chord, `5 mm` closed end, `9 mm` trough | `14.0 x 4.0 x 4.0` | `0.30` | MON-22 |
| 27 | Cell multiplexer | `4 x 32` channels for the `128` body cells | `3.0 x 3.0 x 0.40` | `0.03` | ENR-23 |
| 28 | Seat magnets | `8` N52H in the sliding pad, away from A1 | `8 x (3.2 x 1.6 x 1.1)` | `0.34` | MON-5, MON-21 |
| 29 | B cell | Li-ion, `600 Wh/L`, `0.14 Wh` | `20.0 x 8.0 x 1.50` | `0.60` | ENR-22 |
| 30 | Gaskets | FKM, 60 Shore A, and the jack contact pocket | `30.0 x 3.6 x 0.40` | `0.25` | MON-12 |
| 31 | Spreader and latent buffer | graphite sheet and `1.0 g` phase change material | `Ø28.0 x 0.80` | `1.10` | MEC-11 |
| 32 | Shield cans | nickel silver, over `U2A`, `U2B`, `U5` | `3 cans` | `0.30` | RF-17 |
| **Total** | **32 parts** | **`1.00 mm` bar and flat ring** | **`40 x 32 x 4.00 mm` envelope** | **`10.80`** | |

All masses are `[HYPOTHESIS]` until the first build weighs them.

---

## 3 · What changed from L.5.0

| L.5.0 | L.6.0 | Why |
| --- | --- | --- |
| stem `4.50 mm`, titanium | bar `32.0 x 4.0 x 1.00 mm`, LCP-GF40, on the top edge | the order of Ayaz, the CAD, and metal defeats the antenna |
| `±90°` titanium hinge | moulded corner | the original `b.png` has no hinge |
| USB-C in the stem | a separately sold port part | the order of Ayaz |
| no `3.5 mm` jack | a jack in the ring rim | the order of Ayaz, Q33 and Q7 |
| `50 MP` with a `13.8 mm` barrel standing in the ring | `50 MP` small-pixel sensor in a `3.90 mm` column | the old path did not fit `4.00 mm` |
| one `U2` SiP | `U2A`, `U2B` and `U5` | no single shipping part does all three jobs |
| aluminium ring | LCP-GF40 ring | no metal shell around the radios |
| `0.45 Wh` bridge cell in `91 mm³` | `0.14 Wh` cell in `240 mm³` | the old cell was about `4 960 Wh/L` |
| `20.0 g` stated, `22.00 g` summed | `10.80 g` summed | one number, from the list |
