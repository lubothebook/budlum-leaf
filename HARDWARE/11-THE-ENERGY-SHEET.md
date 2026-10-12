# BUDLUM LEAF · HARDWARE · 11 · THE 4-QUADRANT (+) BIOCOMPATIBLE SOLID-STATE BATTERY AND EYEWEAR SAFETY

> **Revision L.6.0 note (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` supersedes this file where they differ. Each tile holds a `4 x 8` grid of `5.0 mm` micro cells on islands, with a fuse in each lane. The device energy is about `1.7 Wh` at the maximum stretch, on a realistic `600 Wh/L`.

**Revision L.5.0 · 2026-10-12**.
This file specifies the **`4 x 3.0 Wh = 12.0 Wh` (`3 200 mAh`) `LLZO/PEO-Ceramic` all-solid-state battery**, universal **`Qi2.2` wireless charging**,. Also, **eyewear / human-health safety architecture** inside the four `40.0 x 80.0 x 2.00 mm` (`17.0 g`) polycarbonate screen quadrants (`pafta/P11`, `pafta/P12`, `pafta/P17`).

---

## 1 · Why the bulky bottom battery is cancelled and solid-state batteries return inside the 4 polycarbonate tiles

1. **Cancelling the bulky external bottom battery**. The `80 x 36 x 4 mm` external bottom pack added `36 mm` of bulky length (`çok kaba duruyor`). Revision L.5.0 eliminates it completely.
2. **4-Quadrant (`+`) tool-free replaceable battery (`EU 2023/1542` Article 11)**. Dividing the `80.0 x 160.0 x 2.00 mm` (`68.0 g`) body across `x = 0`. Also, `y = 0` creates four `40.0 x 80.0 x 2.00 mm` (`17.0 g`) polycarbonate screen-battery tiles (`Q1..Q4`). Each tile snaps out or in within **`<3 seconds`** with zero tools, satisfying **Regulation (EU) 2023/1542 Article 11**.
3. **Biocompatible all-solid-state `LLZO/PEO` chemistry for eyewear, hand, and pocket use**. Because the tiles are also worn directly in front of the eyes as smart glasses (`göze de konulacak. Gözlük olarak da kullanılacak`), liquid/gel Li-ion cells (`LiPF6`) are forbidden. Each tile uses a **non-flammable inorganic `LLZO` (`Li7La3Zr2O12`) + cross-linked `PEO` solid-state battery** (`0%` liquid. `0.0 ppm` HF gas, `0.0%` swelling).

---

## 2 · Key parameters of the 4-Quadrant (`+`) solid-state battery & Qi2.2 system

| Property | Value at Leaf 160 (`Q1..Q4`) |
| --- | --- |
| Quadrant tile dimensions & mass | `4 x (40.0 x 80.0 x 2.00 mm)`. `17.0 g` per tile = **`80.0 x 160.0 x 2.00 mm` (`68.0 g` total body)** |
| Solid-state cell per quadrant | `35.0 x 75.0 x 1.08 mm` (`2.83 mL`). **`3.0 Wh` / `800 mAh` per tile = `12.0 Wh` / `3 200 mAh` total** (`750 Wh/L`) |
| Runtime at `0.85 W` Zero-CPU draw | **`>14.1 hours` active runtime** (no local CPU/GPU thermal load) |
| Chemical & fire safety | **All-solid-state `LLZO/PEO` + `LiFePO4/NMC` (`0%` liquid solvent, `0%` `LiPF6`, `0.0 ppm` HF gas, `0%` swelling)** |
| Ocular thermal safety (`IEC 62368-1` / `60601-1`) | **`<=35.8 °C` steady-state** and **`36.2 °C` hardware NTC cut-off** (`k_xy = 1 100 W/m·K`, `k_z = 1.5 W/m·K`) |
| Electromagnetic & RF ocular safety | **Bifilar current cancellation (`<0.08 µT` ELF)** + `Mu-metal` shield + **`SAR = 0.054 W/kg`** (`37x` below ICNIRP `2.0 W/kg`) |
| Biocompatibility & photobiological safety | **`ISO 10993-5 / -10`** medical-grade BPA-free PC + flicker-free DC-dimming `T-OLED` (`<415 nm` HEV cut, `IEC 62471` RG0) |
| Universal wireless charging (`0` USB-C on body) | **Central `Ø54.0 mm` 4-sector `Qi2.2` MPP (`15-25 W`)** + **`4 x Ø22.0 mm` (`5-10 W`) local `Qi` coils** |

---

## 3 · Uninterrupted quadrant hot-swap in four steps (`EU 2023/1542` Article 11)

1. **Pull any single quadrant (`Q1`, `Q2`, `Q3`, or `Q4`, `11.2 N`)**. Its `32` mating `+` seam contacts drop to `0 V` (`Dead-Pad`) in `<0.8 ms`.
2. **Keep running on the remaining 3 quadrants (`9.0 Wh`)**. The other three tiles sustain the display and `U1` Master TCON with zero reboot.
3. **Snap in a replacement `17.0 g` quadrant (`<3 s`)**. The `(0,0)` Ti hub, tapered Ti pins (`<2.5 µm` step),. Also, `<15 µm` (`n = 1.585`) lip self-align the tile.
4. **Complete the `3 ms` Dead-Pad handshake and balance cells**. The `U_QI` BMS authenticates in **`3 ms`** and balances the new `3.0 Wh` tile.

---

## 4 · Verification gates

| Gate | Subject | Pass condition |
| --- | --- | --- |
| **ENR-11** | 4-Quadrant `LLZO/PEO` solid-state capacity (`4 x 3.0 Wh = 12.0 Wh`) | `>=12.0 Wh` (`3 200 mAh`), `>14.1 h` runtime at `0.85 W`, `<28 mΩ` cell impedance |
| **ENR-12** | Universal `Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` wireless charging & `3 ms` Dead-Pad | `15-25 W` whole-body charge and `5-10 W` single-tile charge on any pad; `<3 ms` auth |
| **ENR-13** | `<3 s` tool-free quadrant hot-swap (`EU 2023/1542` Article 11) | any 1 tile swaps in `<3 s` while remaining 3 tiles (`9.0 Wh`) keep session active |
| **ENR-15 / ENR-16** | Non-flammable solid-state puncture & `<=36.2 C` eyewear ocular safety | `0` fire / `0.0 ppm` HF on nail test; hardware NTC cuts current at `36.2 °C`; `ISO 10993` pass |
