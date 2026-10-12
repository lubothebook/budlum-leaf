# BUDLUM LEAF · HARDWARE · 06 · THE FORM LANGUAGE · THE 2.20 MM 4-QUADRANT (+) BODY AND 90°-BENT-STEM B MODULE

**Revision L.5.0 · 2026-10-12**.
The screen body of a Budlum Leaf 160 is an **upright `80.0 x 160.0 x 2.00 mm` (`68.0 g`) 4-Quadrant (`+`) snap-together. Polycarbonate screen-battery prism**. It divides across `x = 0` and `y = 0`. It covers **four equal `40.0 x 80.0 x 2.00 mm` (`17.0 g`) tiles (`Q1..Q4`)** with **`R = 6.35 mm` outer corners**. **`r = 0.65 mm` softened horizontal edges**, and a **`<15 µm` (`n = 1.585`) zero-scratch optical `+` seam**. `[DECISION]`

---

## 1 · The three-dimensional 4-Quadrant (`+`) sheet law

When snapped together across the central `+` cross (`x = 0`, `y = 0`). The four quadrants form a continuous `80.0 x 160.0 x 2.00 mm` prism:
- **4 outer vertical corner edges** (`R = 6.35 mm` on the outer corner of each quadrant `Q1..Q4`).
- **8 horizontal perimeter edges** (`4` front at `z = +1.10 mm`. Also, `4` back at `z = -1.10 mm`, softened with `r = 0.65 mm`).
- **Central `+` optical seam (`x = 0`, `y = 0`)**. `12 µm` phenyl-fluorosilicone self-healing lip (`n = 1.585` vs `n_PC = 1.586`, Fresnel `R = 9.9e-8 < 0.0001%`. Z-step `<2.5 µm`).

```
full plan       = upright rectangle, W = 80.0 mm x H = 160.0 mm (4 quadrants x 40.0 x 80.0 mm)
thickness       = T = 2.00 mm (symmetric 11-layer stack with 1.08 mm LLZO solid-state cell, 68.0 g)
outer corner(4) = R = round( 3.20 x (short side / 80) ^ 0.25 , 2 )    3.20 mm at Leaf 160
face edges  (8) = r = 0.65 mm fillet on all 4 front + 4 back edges    soft rounded edge
+ cross seam    = <15 um optical elastomer lip (n = 1.585)            zero scratch, zero line
```

| The check | The rule | The result at Leaf 160 |
| --- | --- | --- |
| full 4-quadrant envelope | `4 x (40.0 x 80.0 x 2.00 mm)` tiles (`Q1..Q4`) | `80.0 x 160.0 x 2.00 mm` (`68.0 g` = `4 x 17.0 g`) |
| 4 outer vertical corner edges | `R = 3.20 x (80 / 80) ^ 0.25` | **`R = 6.35 mm`** |
| 8 horizontal face edges | `r = 0.65 mm` smooth fillet (no 90° angle) | **`r = 0.65 mm`** on all 4 front + 4 back edges |
| `+` cross optical seam (`x=0, y=0`) | `12 µm` phenyl-fluorosilicone lip (`n = 1.585`) + Ti pins | **`<15 µm` gap, `<2.5 µm` step, `R < 0.0001%` (zero visible line)** |
| body USB-C ports and buttons | portless, buttonless `Qi2.2` wireless body | **`0` USB-C ports, `0` buttons on screen body** |
| continuous active screen per face | `79.6 x 159.6 mm` (`0.00 mm` internal seam bezel) | **`12 696 mm²` continuous dual-face T-OLED (`508 ppi`)** |

---

## 2 · The family classes from `cad/leaf_geom.py`

Every class uses the same `2.20 to 2.40 mm` solid-state polycarbonate tile law, verified by `python3 cad/leaf_geom.py`:

| The class | The plan (`W x H x T`) | Corner `R` | Edge `r` | Solid-state battery & Qi2 | The `90°`-bent-stem B module |
| --- | --- | --- | --- | --- | --- |
| **Leaf 80** | `40.0 x 80.0 x 2.00 mm` (`17 g`, 1 tile) | `2.69 mm` | `0.65 mm` | `3.0 Wh` (`800 mAh`) `LLZO` + `Ø22 mm` Qi | docks on any edge, front or back |
| **Leaf 160** | `80.0 x 160.0 x 2.00 mm` (`68 g`, 4 tiles) | `3.20 mm` | `0.65 mm` | `12.0 Wh` (`3 200 mAh`) `LLZO` + `Ø54 mm` Qi2.2 | docks on all 4 edges, front (`+Z`) or back (`-Z`) |
| **Leaf 160²** | `160.0 x 160.0 x 2.00 mm` (`144 g`, 8 tiles) | `3.81 mm` | `0.65 mm` | `24.0 Wh` (`6 400 mAh`) `LLZO` + dual `Qi2.2` | docks on any edge, front or back |
| **Leaf 480** | `320.0 x 480.0 x 2.40 mm` (`48 tiles`) | `4.53 mm` | `0.65 mm` | `144.0 Wh` modular tile array + Dock | docks on edge or Dock post |
| **Leaf 1400 / 2800** | `900x1400` / `1800x2800 x 2.40 mm` | `5.86 / 6.40 mm` | `0.65 mm` | modular tile array + wall/dock feed | on the Dock |

---

## 3 · What sits on the four outer edges and `+` internal edges

| The edge | Length | What it carries |
| --- | --- | --- |
| **Internal `+` cross (`x = 0`, `y = 0`)** | `160 mm` + `80 mm` | `(0,0)` cruciform Ti hub, `8` tapered Ti pins (`<2.5 µm` step), `24` bipolar N52H magnets, `64` gold leaves, `<15 µm` (`n=1.585`) lip |
| **All 4 outer edges (Top, Bottom, Left, Right)** | `2 x 80 mm` + `2 x 160 mm` | reversible magnetic (`8` N52H, `7.2 N`) and `12`-pad (`3 ms` Dead-Pad, `IP68`) docking tracks for the **`90°`-bent-stem B module** (`+Z` or `-Z`) |

---

## 4 · The 2.00 mm 11-layer symmetric cross-section stack (Eyewear-Safe Solid-State Battery Inside)

| Layer | Z-span (`mm`) | Thickness | Material and role |
| --- | --- | --- | --- |
| 1 · Front optical PC shell | `+0.90 .. +1.10` | `0.20 mm` | `ISO 10993-5/-10` medical-grade BPA-free PC (`n = 1.586`) + `8 µm` anti-smudge hard coat (`3H`) |
| 2 · Front silicone OCA slip layer | `+0.85 .. +0.90` | `0.05 mm` | ultra-low-modulus (`G = 0.08 MPa`) silicone OCA (`0.38%` outer strain at `R 25.5 mm`) |
| 3 · Front flicker-free T-OLED | `+0.71 .. +0.85` | `0.14 mm` | DC-dimming transparent AMOLED (`508 ppi`, `1-144 Hz`, `<415 nm` HEV cut, `IEC 62471` RG0) |
| 4 · Front AgNW / ITO mesh | `+0.67 .. +0.71` | `0.04 mm` | `12 Ω/sq` silver-nanowire + ITO power/data/touch mesh (`>89%` clear) + Corning edge-wrap electrodes |
| 5 · Front PDLC & graphene/Mu-metal | `+0.58 .. +0.67` | `0.09 mm` | switchable `PDLC` privacy film + orthotropic graphene (`k_xy = 1 100 W/m·K`, `k_z = 1.5 W/m·K`) + Mu-metal |
| **6 · All-solid-state `LLZO/PEO` core & `Qi2.2`** | **`-0.58 .. +0.58`** | **`1.16 mm`** | **`1.08 mm` non-flammable `LLZO/PEO` battery (`3.0 Wh`/tile = `12.0 Wh`, `0%` liquid, `0` HF, `<=36.2 C`) + `Qi2.2` coils** |
| 7 to 11 · Symmetric rear stack | `-1.10 .. -0.58` | `0.52 mm` | rear graphene/Mu-metal (`0.09`), rear `AgNW/ITO` (`0.04`), rear `T-OLED` (`0.14`), rear OCA (`0.05`), rear `ISO 10993` PC (`0.20`) |
| **Total per quadrant (`Q1..Q4`)** | **`-1.10 .. +1.10`** | **`2.00 mm`** | **`17.0 g` per tile (`68.0 g` total body, `12.0 Wh`, `EU 2023/1542` Art. 11 `<3 s` swap)** |
