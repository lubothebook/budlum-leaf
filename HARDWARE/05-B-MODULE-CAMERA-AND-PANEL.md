# BUDLUM LEAF · HARDWARE · 05 · THE B MODULE · ONE MILLIMETRE BAR, FLAT RING, CAMERA, RADIOS AND PROJECTION SILICON

**Revision L.6.0 · 2026-10-12 · the single source of truth for the B module (`10.8 g`, 32 parts)**. The decisions live in `FINAL/21-stretch-stem-and-projection.md`. The part list lives in `HARDWARE/13-B-MODULE-PART-BY-PART.md`.

---

## 1 · The seven rules of the B module

1. **The module is `4.00 mm` thick and the bar is `1.00 mm`**. The bar is `32.0 x 4.0 x 1.00 mm` of glass-filled LCP. It lies on the top edge of the body.
2. **The bar is the antenna**. It holds A1 (`2.4 GHz` inverted-F), A2 (`5` to `7 GHz`) and A4 (`60 GHz` array). The ring rim holds A3, the second Wi-Fi antenna.
3. **No hinge and no metal shell**. The `90°` corner is moulded. The shells are LCP-GF40.
4. **The module flips**. It seats on any of the four edges, on the front or the back face. The IMU reports the seat, and the tuners follow it.
5. **The ring holds the rest**. Camera, rear round panel, speaker, microphones, flash, `3.5 mm` jack, cell, and the silicon `U1` to `U8`.
6. **No general-purpose processor**. Every chip is fixed-function with signed firmware. The validators run the Leaf as they run the chain, and the Leaf shows. This is the projection of Part 21.
7. **A wallet on the nearest validator**. `U7` holds the keys and shows a stream only from an active Budlum validator.

---

## 2 · Key numbers

| Parameter | Value | Gate |
| --- | --- | --- |
| module thickness | `4.00 mm` | MON-23 |
| bar envelope | `32.0 x 4.0 x 1.00 mm`, on the top edge | MON-23 |
| ring envelope | `Ø32.0 x 4.00 mm` | MON-1 |
| Wi-Fi | `2 x 2` Wi-Fi 7, multi-link `5 + 6 GHz`, A1 and A3 | RF-22 |
| cellular | 5G standalone with eSIM, `U5` | RF-17 |
| dock link | `60 GHz` `1 x 4` array and UWB, `U2B` | RF-19 |
| decoder | AV1 and HEVC slices, inline check, `16 MB` frame store, `U6` | SW-21 |
| camera | `50 MP` small-pixel sensor, `f/2.0`, focus from `10 cm`, `3.90 mm` column | CAM-21 |
| jack | `3.5 mm` in the ring rim | MON-22 |
| USB-C | a separately sold port part | none |
| body link | `12` gold spring leaves over the seat tile | MON-18 |
| cell | `0.14 Wh` | ENR-22 |
| magnets | `8` N52H in a sliding pad | MON-5 |
| mass | `10.8 g` | MON-13 |
