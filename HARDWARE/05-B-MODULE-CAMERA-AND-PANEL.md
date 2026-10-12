# BUDLUM LEAF · HARDWARE · 05 · THE B MODULE · ONE MILLIMETRE STEM, FLAT RING, CAMERA, RADIOS AND PROJECTION SILICON

**Revision L.6.0 · 2026-10-12 · the single source of truth for the B module (`12.7 g`, 32 parts)**. The decisions live in `FINAL/21-stretch-stem-and-projection.md`. The part list lives in `HARDWARE/13-B-MODULE-PART-BY-PART.md`.

---

## 1 · The seven rules of the B module

1. **The stem is `1.00 mm` thick**. It is `8.0 x 32.0 x 1.00 mm` of glass-filled LCP. It stands perpendicular to the screen, against the screen edge.
2. **The stem is the antenna**. It holds A1 (`2.4 GHz` inverted-F), A2 (`5` to `7 GHz`) and A4 (`60 GHz` array). The ring rim holds A3, the second Wi-Fi antenna.
3. **No hinge and no metal shell**. The `90°` corner is moulded. The shells are LCP-GF40.
4. **The module flips**. It seats on any of the four edges, on the front or the back face. The IMU reports the seat, and the tuners follow it.
5. **The ring holds the rest**. Camera, rear round panel, audio, bridge cell, USB-C in the rim, and the silicon `U1` to `U8`.
6. **No general-purpose processor**. Every chip is fixed-function with signed firmware. The validators run the Leaf as they run the chain, and the Leaf shows. This is the projection of Part 21.
7. **Only validator streams**. `U7` shows a stream only from an active Budlum validator.

---

## 2 · Key numbers

| Parameter | Value | Gate |
| --- | --- | --- |
| stem envelope | `8.0 x 32.0 x 1.00 mm`, `r = 0.40 mm` edges | MON-23 |
| stem pry strength | `5 N` at the tip, margin `1.5` in LCP-GF40 | MEC-42 |
| ring envelope | `Ø32.0 x 4.00 mm` | MON-1 |
| Wi-Fi | `2 x 2` Wi-Fi 7, multi-link `5 + 6 GHz`, A1 and A3 | RF-22 |
| cellular | 5G RedCap with eSIM, `U5` | RF-17 |
| dock link | `60 GHz` `1 x 4` array, `U2B` | RF-19 |
| decoder | AV1 and HEVC slices, `16 MB` frame store, `U6` | SW-21 |
| camera | `50 MP`, `1/1.56"` flat sensor, double-fold D-cut periscope, about `f/2.2` | CAM-21 |
| USB-C | mid-mount receptacle in the ring rim, `IP68` | MON-22 |
| dock contacts | `12` gold spring leaves in the stem contact band | MON-18 |
| magnets | `8` N52H in the ring underside | MON-5 |
| mass | `12.7 g` | MON-13 |
