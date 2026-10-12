# BUDLUM LEAF · HARDWARE · 12 · THE BEND LAW · THE 100% FULL-AREA BENDABLE 2.00 MM (+) POLYCARBONATE LAMINATE

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ: the body bends at `R 25.5 mm` and also stretches about `8 %` in every direction. The strain lives in the elastomer bridges, and the polycarbonate stays in the islands.

**Revision L.5.0 · 2026-10-12**.
A Budlum Leaf is **not** a folding phone with a narrow hinge or rigid ceramic plates. All `100 percent` of its `80 x 160 x 2.00 mm` (`R = 6.35 mm`, `68.0 g`) body bends as polycarbonate. Each `40 x 80 x 2.00 mm` (`17.0 g`) quadrant (`Q1..Q4`) uses optical **Siloxane-Polycarbonate (`PC-PDMS`, `ISO 10993`)** and `G = 0.035 MPa` silicone `OCA`. The entire screen bends to **`R 25.5 mm`** at **`0.35 percent` outer strain** (`1.4 N` force) and recovers flat within `0.05 mm` (`pafta/P11`, `pafta/P22`).

---

## 1 · Why 100% of the 2.00 mm 4-Quadrant (`+`) polycarbonate screen bends without rigid zones

1. **Optical Siloxane-Polycarbonate (`PC-PDMS`) outer shells and carriers (`2 x 0.18 mm`)**. Outer skins, puzzle housings, and the `(0,0)` hub use optical `PC-PDMS` (`EP2707418A1`, `>30 percent` yield elongation, zero whitening).
2. **Multi-neutral-plane silicone `OCA` shear decoupling (`G = 0.035 MPa`, `2 x 0.04 mm`)**. Soft silicone `OCA` slip planes decouple the `0.18 mm` polycarbonate skins from the core. Each skin bends around its own neutral axis at **`0.35 percent` strain**, lowering bend force by `48x` to **`1.4 N`**.
3. **Co-molded `PC-PDMS + NiTi` puzzle interlock (`yapboz girdili-çıktılı`) and `(0,0)` hub**. Inside `z = -0.45..+0.45 mm`, `24` puzzle joints (`10 N/mm`) and the `(0,0)` hub use `PC-PDMS` over `80 µm` `NiTi`. Because `EI_seam / EI_tile = 1.00`, the `+` cross bends smoothly with a `<15 µm` (`n = 1.585`) optical lip.
4. **Full-area biaxial `LLZO/PEO-LiBOB` battery and flexible nanocrystalline `Qi2.2` coils**. The `1.06 mm` battery uses a `2.5 x 2.5 mm` biaxial grid (`1 680` micro-cells) in `PC-PDMS` elastomer. The `Qi2.2` coils use a `60 µm` `FeSiBCuNb` nanocrystalline + polycarbonate shield (`R = 5 mm` flex, zero brittle ferrite).

---

## 2 · Strain budget across the 2.00 mm 11-layer polycarbonate cross-section at `R 25.5 mm`

| Layer | Thickness | Distance to local neutral axis | Strain at `R 25.5 mm` | Safe elastic limit | Result |
| --- | --- | --- | --- | --- | --- |
| `ISO 10993` optical `PC-PDMS` polycarbonate shell (`x 2`) | `180 µm` (`0.18 mm`) | `90 µm` (`OCA` shear-decoupled) | **`0.35 percent`** | `6.0-30.0 percent` | elastic, zero whitening or craze |
| Silicone `OCA` shear-slip layer (`x 2`) | `40 µm` (`0.04 mm`) | shears in plane (`G = 0.035 MPa`) | `0.18 mm` shear slip | `400 percent` elongation | decouples outer `PC-PDMS` skins |
| Flicker-free `T-OLED` on polycarbonate film (`x 2`) | `130 µm` (`0.13 mm`) | `65 µm` | **`0.25 percent`** | `1.2 percent` | elastic, zero pixel loss |
| Hybrid `AgNW / IZO` mesh on polycarbonate (`x 2`) | `40 µm` (`0.04 mm`) | `50 µm` | **`0.20 percent`** | `2.0 percent` (`AgNW`) | elastic, `<0.8%` ΔR after `200 000` wraps |
| `PC`-microencapsulated `PDLC` + shield (`x 2`) | `80 µm` (`0.08 mm`) | `45 µm` | **`0.18 percent`** | `2.5 percent` | maintains privacy & EMI shield |
| **Biaxial `LLZO/PEO` cell + flex `Qi2.2` + `PC/NiTi` puzzle** | **`1 060 µm` (`1.06 mm`)** | **neutral plane (`z = 0`)** | **`0.21 percent` max** | **`1.5 percent` (`LLZO/PEO`)** | **`200 000` wraps, zero rigid zone** |
| **Total 4-Quadrant (`+`) bendable polycarbonate body** | **`2 000 µm` (`2.00 mm`)** | **symmetric 11-layer `PC` stack** | **`0.35 percent` max** | **`200 000` full wraps** | **`68.0 g` (`4 x 17 g`), `12.0 Wh`** |

---

## 3 · What happens to the `+` puzzle seam and `90°`-bent-at-gap B module during bending

- **Central `+` puzzle seam (`x = 0`, `y = 0`) and `(0,0)` flexible `PC-PDMS` hub**. The `24` puzzle teeth (`10 N/mm`), `12 µm` lip, and `64` gold leaves bend continuously (`R < 0.0001%`).
- **Turned and `90°`-bent-at-gap B module (`20.0 g`)**. Its `1.00 mm` (`bir milim`) horizontal top `çubuk` sits on the `2.00 mm` screen top edge (`y = +80 mm`). Its front-facing ring (`Ø32 / Ø24 mm`) rests on a soft pad, isolating the `50 MP` optics.

---

## 4 · Verification gates `B-1` to `B-10`

| Gate | Test | Condition | Pass criterion |
| --- | --- | --- | --- |
| **B-1** | Full-area `R 25.5 mm` wrap of `2.00 mm` polycarbonate body | `200 000` cycles to `R 25.5 mm` | zero `T-OLED` pixel loss, `<1.1%` `LLZO` impedance drift, `+` puzzle seam locked |
| **B-2** | Gentle everyday flex across full polycarbonate surface | `R 70 mm`, `200 000` cycles | zero delamination, zero permanent set `>0.05 mm` |
| **B-3** | Flat recovery | granite table check after `200 000` wraps | flat within **`0.05 mm` over `160.0 mm`** (`<2.5 µm` `+` seam Z-step) |
| **B-4** | Crease-free luminance & `<15 µm` `+` seam optical scan | optical scan across `x = 0` and `y = 0` after `200 000` wraps | `<0.5 percent` seam luminance step, Fresnel `R < 0.0001%` |
| **B-5** | `+` cross `PC-PDMS/NiTi` puzzle & micro-leaf continuity | 4-wire resistance logging across all `64` gold leaves during `R 25.5 mm` flex | `<25 mΩ` contact resistance, zero micro-drop `>1 µs` |
| **B-6** | Silicone `OCA` (`G = 0.035 MPa`) & `n = 1.585` lip fatigue | `1 000 h` at `45 °C` and `200 000` flex cycles | zero yellowing, zero optical index drift `>0.001` |
| **B-7** | Cold and hot flex | `R 25.5 mm`, `500` cycles at `-10 °C` and `+45 °C` | passes `B-1` with full `LLZO` discharge and `Qi2.2` charging |
| **B-8** | Waterproof `IP68` seal after `200 000` wraps & `1 000` tile swaps | `IP68` (`1.5 m`, `30 min`) immersion test | zero water ingress across `+` cross lip or `1.00 mm` B `çubuk` gasket |
| **B-9** | Solid-state battery ocular safety after `200 000` wraps | thermal & FTIR gas audit after `200 000` wraps at `R 25.5 mm` | `<=36.2 °C` ocular surface, `0.0 ppm` outgassing, `0.0%` swelling |
| **B-10** | Flex with `90°`-bent-at-gap B module docked on any edge | `R 25.5 mm` flex with B module docked on Top, Bottom, Left, or Right edge | B module remains locked at `7.2 N` with zero frame drop |
