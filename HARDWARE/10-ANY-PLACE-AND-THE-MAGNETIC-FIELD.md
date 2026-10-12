# BUDLUM LEAF · HARDWARE · 10 · THE (+) CROSS MAGNETIC LATCH, REVERSIBLE 90° B STEM CLIP AND 3 MS DEAD-PAD SECURITY

**Revision L.5.0 · 2026-10-12**.
This file specifies the magnetic, mechanical, and electrical docking systems of the 4-Quadrant (`+`) screen-battery body and the `90°`-bent-stem B module (`pafta/P13`).

---

## 1 · The `+` cross quadrant latch and reversible `90°` B module docking law

| Question | Answer | Proof |
| --- | --- | --- |
| How do the 4 screen-battery quadrants (`Q1..Q4`) join? | Across `x = 0` (`160 mm`) and `y = 0` (`80 mm`) via a **`(0,0)` Ti hub. `8` tapered Ti pins (`<2.5 µm` step), `24` bipolar `N52H` magnets, `64` gold leaves,. Also, a `<15 µm` (`n = 1.585`) optical lip**. | `pafta/P09`, `pafta/P13`, `pafta/P19` |
| How does the `90°`-bent-stem B module attach? | **Only the stem (`çubuk`) is bent `90°`** and clips onto **any of the 4 edges (`Top`, `Bottom`, `Left`, `Right`)**,. While the **round ring (`yuvarlak`) lies flat on the Front (`+Z`) or Back (`-Z`) screen**. | `pafta/P10`, `pafta/P14`, `pafta/P21` |
| Where is USB Type-C located? | **Exclusively inside the `90°`-bent stem of the B module**. The 4-quadrant screen body has **zero USB-C ports and zero buttons** and charges on any `Qi / Qi2.2` wireless pad. | `pafta/P10`, `pafta/P16` |
| How are all `64` `+` seam leaves and `12` B dock pins protected? | **Dead-Pad (`Ölü Pin`) security + `IP68` sealing**: every contact stays at `0 V` until the mate completes a **`3 ms` cryptographic handshake**. | `pafta/P10`, `pafta/P13` |

---

## 2 · Magnetic, mechanical, and Dead-Pad parameters (`pafta/P13`)

| Parameter | `+` Cross Quadrant Seam (`Q1..Q4`) | `90°`-Bent B Stem Edge Dock (`4` edges, `+Z / -Z`) |
| --- | --- | --- |
| Magnet array | **`24` bipolar `N52H` NdFeB (`6` per half-axis, `3.0 x 1.4 x 1.0 mm`)** | **`8` `N52H` NdFeB poles (`3.2 x 1.6 x 1.1 mm`)** in `90°` stem clip |
| Holding force | **`11.2 N` normal pull, `18.5 N` shear** per half-axis | **`7.2 N` normal hold, `4.5 N` shear** on any of the 4 outer edges |
| Precision registration | **`(0,0)` cruciform Ti hub + `8` tapered Ti pins (`<2.5 µm` Z-step)** | **reversible `±90°` Grade-5 Ti hinge + edge keyway (`±0.08 mm`)** |
| Optical / waterproof seal | **`12 µm` phenyl-fluorosilicone lip (`n = 1.585`, `R < 0.0001%`, `IP68`)** | **`0.40 mm` FKM fluoroelastomer gasket (`25%` compression, `IP68`)** |
| Electrical contact array | **`64` gold micro-leaf contacts (`16` per half-axis, `18 mΩ`)** | **`12` hard-gold pogo pins (`18 mΩ`, palindrome front/back pinout)** |
| Dead-Pad (`Ölü Pin`) switch | **`3 ms` cryptographic challenge-response** (`0 V` when detached) | **`3 ms` cryptographic challenge-response** before power/TCON enable |
| Stray magnetic field at eye | **`<0.08 µT` ELF / `<0.4 mT` DC** at `8 mm` (`Mu-metal` + bifilar cancellation) | **`SAR = 0.054 W/kg`** (`37x` below ICNIRP `2.0 W/kg` limit) |
