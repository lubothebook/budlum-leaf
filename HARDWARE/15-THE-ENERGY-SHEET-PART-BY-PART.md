# BUDLUM LEAF · HARDWARE · 15 · THE 4-QUADRANT (+) SOLID-STATE BATTERY AND QI2.2 WIRELESS SYSTEM, PART BY PART (25 PARTS)

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. The four pouch cells are replaced by `128` hermetic micro cells, one per rotating tile. The body holds `5.7 Wh` at `600 Wh/L` and `7.2 Wh` at `750 Wh/L`.

**Revision L.5.0 · 2026-10-12**.
`11-THE-ENERGY-SHEET.md` states the operation of the 4-Quadrant (`+`) biocompatible `LLZO/PEO` solid-state battery (`4 x 3.0 Wh = 12.0 Wh` / `3 200 mAh`). Universal `Qi2.2` wireless charging, and eyewear safety (`<=36.2 C`, `ISO 10993`). This file lists all **25 part groups** of the energy and `+` seam system across `Q1..Q4` (`pafta/P11`, `pafta/P12`, `pafta/P17`).

---

## 1 · Complete 25-part bill of materials (`72.00 g` total across `4 x 18.00 g` quadrants `Q1..Q4`)

| No | Part name | Material and construction | Dimensions (`mm`, per tile / set) | Mass (`g`, 4 tiles) | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | Quadrant `Q1` (Top-Left) `LLZO/PEO` solid-state cell | non-flammable `LLZO` garnet + cross-linked `PEO` (`3.0 Wh`, `800 mAh`) | `35.0 x 75.0 x 1.08` | `8.60` | ENR-11, ENR-15 |
| 2 | Quadrant `Q2` (Top-Right) `LLZO/PEO` solid-state cell | non-flammable `LLZO` garnet + cross-linked `PEO` (`3.0 Wh`, `800 mAh`) | `35.0 x 75.0 x 1.08` | `8.60` | ENR-11, ENR-15 |
| 3 | Quadrant `Q3` (Bottom-Left) `LLZO/PEO` solid-state cell | non-flammable `LLZO` garnet + cross-linked `PEO` (`3.0 Wh`, `800 mAh`) | `35.0 x 75.0 x 1.08` | `8.60` | ENR-11, ENR-15 |
| 4 | Quadrant `Q4` (Bottom-Right) `LLZO/PEO` solid-state cell | non-flammable `LLZO` garnet + cross-linked `PEO` (`3.0 Wh`, `800 mAh`) | `35.0 x 75.0 x 1.08` | `8.60` | ENR-11, ENR-15 |
| 5 | Aluminum-laminated ceramic hermetic pouch (`x 4`) | `45 µm` Al-polymer-SiOx zero-outgassing barrier (`0.0 ppm` HF) | `35.4 x 75.4 x 0.09` | `1.40` | ENR-15, ENR-16 |
| 6 | Bifilar current-canceling anode/cathode foil tabs (`x 4` pairs) | counter-flowing Cu/Ni foil pairs (`ELF < 0.08 µT` at eye) | `12.0 x 2.4 x 0.08` | `0.40` | ENR-16 |
| 7 | Central `Ø54.0 mm` `Qi2.2` MPP `90°` coil sectors (`x 4`) | Litz copper `90°` sectors around `(0,0)` (`15 to 25 W` wireless) | `R = 16..27 x 0.18` | `1.40` | ENR-12, RL-2 |
| 8 | Per-quadrant `Ø22.0 mm` local `Qi` coils (`x 4`) | planar spiral `Qi` receivers (`5 to 10 W` standalone tile charge) | `Ø22.0 x 0.16` | `1.00` | ENR-12, RL-2 |
| 9 | Nanocrystalline ferrite + `Mu-metal` ocular shield (`x 8`) | `FeSiB` + `Mu-metal` (`µ_r > 25 000`, blocks wireless/battery flux) | `34.0 x 74.0 x 0.09` | `1.80` | ENR-16 |
| 10 | Orthotropic pyrolytic graphene thermal spreaders (`x 8`) | `k_xy = 1 100 W/m·K` in-plane, `k_z = 1.5 W/m·K` aerogel insulator | `36.0 x 76.0 x 0.05` | `1.60` | ENR-16, MEC-38 |
| 11 | `U_QI` dual-coil wireless rectifier & BMS ASICs (`x 4`) | rectifies `Qi2.2` (`25 W`) & local `Qi` (`10 W`) + active cell balancing | `3.2 x 2.8 x 0.38` | `0.24` | ENR-12, ENR-14 |
| 12 | Hardware `36.2 °C` ocular NTC thermal limiters (`x 8`) | `2` precision NTCs per tile + hardware comparator cut-off at `36.2 °C` | `8 x (1.0 x 0.5 x 0.3)` | `0.12` | ENR-16 |
| 13 | Dead-Pad (`Ölü Pin`) `3 ms` cryptographic switches (`x 4`) | keeps all `64` `+` seam leaves at `0 V` when a quadrant is detached | `2.0 x 2.0 x 0.32` | `0.16` | ENR-19, MON-10 |
| 14 | Solid-state thin-film holdover capacitors (`x 4`) | `180 mF` ceramic/polymer capacitor per tile for glitch-free `<3 s` swap | `14.0 x 4.0 x 0.25` | `0.48` | ENR-13 |
| 15 | Center `(0,0)` cruciform Grade-5 Titanium hub | 4-way interlocking corner keystone at `(x=0, y=0)` | `6.0 x 6.0 x 1.40` | `0.60` | F-01, ENR-13 |
| 16 | Tapered Grade-5 Ti micro-dovetail alignment pins (`x 8`) | `2` pins per internal half-axis locking Z-step to `<2.5 µm` | `8 x (Ø0.70 x 2.40)` | `0.48` | DSP-15, ENR-13 |
| 17 | Bipolar `N52H` `+` seam latch magnets (`x 24`) | `6` alternating `N-S-N-S` poles per half-axis (`11.2 N` pull, `<3 s` swap) | `24 x (3.0 x 1.4 x 1.0)` | `1.80` | ENR-12, ENR-13 |
| 18 | Gold-plated BeCu `+` seam micro-leaf contacts (`x 64`) | `16` recessed wiping contacts per half-axis (`18 mΩ`, `VSYS + QI2 + MIPI`) | `64 x (1.4 x 0.9 x 0.35)` | `0.72` | ENR-12, RL-8 |
| 19 | `<15 µm` (`n = 1.585`) self-healing optical `+` seam lip | phenyl-fluorosilicone elastomer (`R < 0.0001%`, zero scratch, `IP68`) | `160 + 80 x 0.012 x 2.20` | `0.20` | DSP-16, F-07 |
| 20 | `Qi2.2` MPP magnetic alignment ring (`4 x 90°` arcs) | flux-guided `N52H` arc segments around `(0,0)` | `Ø56.0 x 0.45` | `0.52` | ENR-12 |
| 21 | `ISO 10993-5/-10` medical-grade BPA-free PC shells (`x 8`) | front & back `0.20 mm` optical polycarbonate (`R = 3.20`, `r = 0.65 mm`) | `8 x (40.0 x 80.0 x 0.20)` | `12.80` | DSP-16, ENR-16 |
| 22 | Silicone OCA shear-decoupling slip layers (`x 8`) | `G = 0.08 MPa` optical silicone (`0.38%` strain at `R 25.5 mm`) | `8 x (39.6 x 79.6 x 0.05)` | `1.60` | B-6, DSP-16 |
| 23 | Flicker-free DC-dimming `T-OLED` panels (`x 8`) | dual-face transparent OLED (`508 ppi`, `<415 nm` HEV cut, `IEC 62471` RG0) | `8 x (39.8 x 79.8 x 0.14)` | `6.80` | DSP-15 |
| 24 | Invisible `AgNW / ITO` mesh & Corning edge-wrap (`x 8`) | `12 Ω/sq` transparent mesh + side-wall edge-wrapped electrodes | `8 x (39.8 x 79.8 x 0.04)` | `1.60` | MEC-34 |
| 25 | Switchable `PDLC` privacy film cores (`x 4`) | low-voltage matte privacy lock / `0 V` clear glass (`0.09 mm` center) | `4 x (39.6 x 79.6 x 0.09)` | `1.88` | CLR-1..11 |
| **Total** | **25 part groups (`52` physical body subparts)** | **`4 x 3.0 Wh = 12.0 Wh` `LLZO` + `Qi2.2` + `<15 µm` `+` seam** | **`80.0 x 160.0 x 2.00 mm`** | **`72.00 g` (`4 x 17 g`)** | **ENR-11..21** |
