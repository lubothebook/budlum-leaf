# BUDLUM LEAF · HARDWARE · 14 · THE PORTLESS QI2.2 BODY AND 90° BENT B STEM USB-C INTERFACE, PART BY PART (42 PARTS)

**Revision L.5.0 · 2026-10-12**.
`04-PORT-RAIL.md` states the portless `Qi2.2` wireless charging body and the sole `USB Type-C` receptacle inside the `90°`-bent B stem. **This file states all 42 parts** of the wireless receiver network (`14` body parts across `Q1..Q4`) and the `90°` B stem `USB-C`. Also, optional side-rail I/O assembly (`28` parts) (`pafta/P10`, `pafta/P16`). `[DECISION]`

---

## 1 · The two halves of the Revision L.5.0 charging and I/O architecture

| The quantity | The portless 4-Quadrant (`+`) body receiver (`14` parts) | The `90°` B stem USB-C & I/O assembly (`28` parts) |
| --- | --- | --- |
| **USB-C ports & buttons** | **`0` USB-C ports, `0` buttons on the screen body** | **1 sole `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68) in `90°` B stem** |
| **Wireless charging** | **Central `Ø54.0 mm` 4-sector `Qi2.2` (`15-25 W`) + `4 x Ø22.0 mm` (`5-10 W`) `Qi` coils** | feeds `40 W` wired USB-C power into `+` bus via `12` gold pogo pins |
| **Edge docking** | 4-edge reversible magnetic (`7.2 N`) + `12`-pad (`3 ms` Dead-Pad) tracks | clips onto Top, Bottom, Left, or Right edge on Front (`+Z`) or Back (`-Z`) |
| **Mass contribution** | `4.80 g` total across `Q1..Q4` (included in `68.0 g` body) | `4.60 g` inside the `20.0 g` B module (`+ 9.0 g` optional side rail) |

---

## 2 · The portless 4-Quadrant (`+`) wireless charging & edge receiver, part by part (Parts 1 to 14)

| No | The part | The material | The size | The tolerance | The mass | The function | The gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Qi2.2` central `90°` coil sector (`x 4`) | multi-strand Litz copper (`0.18 mm`) | `R = 16..27 mm` (`Ø54.0 mm` assembled) | `±0.05 mm` | `1.40 g` | forms unified `15-25 W` `Qi2.2` MPP receiver across `(0,0)` | ENR-12, RL-2 |
| 2 | Per-quadrant local `Qi` coil (`x 4`) | planar copper spiral (`120-200 kHz`) | `Ø22.0 x 0.16 mm` in each tile center | `±0.05 mm` | `1.00 g` | charges any single detached `3.0 Wh` tile (`5-10 W`) on any pad | ENR-12, RL-2 |
| 3 | Nanocrystalline ferrite + `Mu-metal` shield (`x 4`) | `FeSiB` + `Mu-metal` (`µ_r > 25 000`) | `34.0 x 74.0 x 0.09 mm` per tile | `±0.02 mm` | `0.80 g` | guides `Qi2.2` flux (`86%` eff.) and blocks ELF (`<0.08 µT`) toward eye | ENR-16 |
| 4 | `Qi2.2` MPP alignment magnet ring (`x 4` arcs) | `N52H` flux-guided quadrant arc segments | `Ø56.0 mm` ring (`4 x 90°` arcs) | `±0.03 mm` | `0.52 g` | self-centers assembled screen body on any `Qi2 / MagSafe` charger | ENR-12 |
| 5 | `U_QI` dual-input wireless rectifier & BMS (`x 4`) | `Qi2.2` (`25 W`) + local `Qi` (`10 W`) IC | `3.2 x 2.8 x 0.38 mm` per tile | `±0.02 mm` | `0.24 g` | rectifies wireless AC and balances `3.0 Wh` `LLZO` cell | ENR-12, RL-2 |
| 6 | `+` seam `QI2_AC_RING` gold micro-leaves (`x 8` pairs) | hard Au over Ni on BeCu spring leaves | `1.4 x 0.9 x 0.35 mm` (`18 mΩ`) | `±0.02 mm` | `0.16 g` | bridges the `4 x 90°` `Qi2.2` coil sectors across `x = 0` and `y = 0` | RL-8 |
| 7 | `NP0` resonant tuning capacitor bank (`x 4`) | high-Q `C0G/NP0` ceramic capacitors | `8 x (0.6 x 0.3 mm)` per tile | `±1%` | `0.08 g` | tunes `127.7 kHz` / `360 kHz` `Qi2.2` MPP resonance | RL-2 |
| 8 | Hardware `36.2 °C` ocular NTC sensor (`x 4`) | `0.1 °C` precision NTC + hardware comparator | `2 x (1.0 x 0.5 mm)` per tile | `±0.1 °C` | `0.06 g` | throttles wireless/wired current if periocular skin reaches `36.2 °C` | ENR-16 |
| 9 | 4-edge reversible B dock gold lands (`12` per edge) | flush hard-gold over Ni lands (`0.15 mm` recess) | `22.0 x 2.8 x 0.20 mm` on 4 edges | `±0.02 mm` | `0.20 g` | accepts `90°`-bent B stem in Front (`+Z`) or Back (`-Z`) orientation | MON-5, RL-8 |
| 10 | 4-edge ferromagnetic `N52H` keeper strips | 430F stainless + `N52H` pole seats | `24.0 x 1.8 x 0.35 mm` | `±0.03 mm` | `0.16 g` | provides `7.2 N` magnetic hold for the `90°` B stem on all 4 edges | RL-13 |
| 11 | `1-Wire` Dead-Pad challenge pad (`x 4` edges) | gold identity pad (`3 ms` auth) | `Ø1.4 mm` center pad | `±0.02 mm` | `0.04 g` | keeps all `12` edge pads at `0 V` until `3 ms` cryptographic auth | RL-14 |
| 12 | First-break presence pad (`x 4` edges) | recessed detection land (`1.2 ms` early break) | `Ø1.0 mm` | `±0.02 mm` | `0.04 g` | opens power FET in `<0.8 ms` before B stem unclips | RL-7 |
| 13 | Edge gasket sealing land (`x 4` edges) | precision molded `ISO 10993` PC groove | `26.0 x 3.2 x 0.35 mm` | `±0.02 mm` | `0.06 g` | mates against the `90°` B stem FKM skirt for `IP68` sealing | RL-9 |
| 14 | Moisture interdigitated detector (`x 4` edges) | 2-pad impedance sensor on `AgNW/ITO` | `2.0 x 1.0 mm` | `±0.02 mm` | `0.04 g` | inhibits power enable if conductive liquid bridges an open seat | RL-10 |

---

## 3 · The `90°`-bent B stem sole `USB Type-C` & optional studio I/O parts (Parts 15 to 42)

| No | The part | The material | The size | The tolerance | The mass | The function | The gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 15 | `90°` B stem upper Ti/LCP shell | Grade-5 Ti + LCP (`r = 0.55 mm` soft) | `8.0 x 32.0 x 2.25 mm` | `±0.03 mm` | `1.20 g` | structural outer shell of the `90°`-bent stem | RL-15, MON-9 |
| 16 | `90°` B stem lower edge-clip saddle | Grade-5 Ti precision edge saddle | `8.0 x 32.0 x 2.25 mm` | `±0.03 mm` | `1.15 g` | hooks onto Top, Bottom, Left, or Right edge (`+Z` or `-Z`) | RL-15, MON-5 |
| 17 | **Sole `USB Type-C` receptacle (`IP68`)** | stainless shell, 24 gold pins (`10 000` mates) | `8.9 x 7.3 x 3.10 mm` | `±0.05 mm` | `0.85 g` | **the ONLY USB-C port on the device (`40 W PD 3.1 + DP 2.1`)** | RL-1 |
| 18 | Reversible `±90°` Ti micro-hinge barrel | Grade-5 Ti twin-cam detented hinge | `Ø2.2 x 18.0 mm` (`50 000` cycles) | `±0.01 mm` | `0.95 g` | bends ONLY the stem at `90°` while ring lies flat on screen | MON-1, MON-5 |
| 19 | 20-line LCP coaxial hinge flex | 4-layer LCP RF & power ribbon | `16.0 x 6.5 x 0.18 mm` | `±0.02 mm` | `0.20 g` | carries `40 W` USB-C power, `DP 2.1`, and `60 GHz` across `90°` hinge | RL-2 |
| 20 | Stem 6-layer HDI USB-C & RF board | rigid-flex HDI board inside `90°` stem | `7.2 x 30.4 x 0.35 mm` | `±0.03 mm` | `0.35 g` | mounts USB-C receptacle, `U_PD`, ESD array, and RF feeds | RL-16 |
| 21 | `USB 3.2 Gen 2` & `DP 2.1` mux/redriver | 4-lane `10 Gbit/s` linear redriver | `2.4 x 2.4 x 0.35 mm` | `±0.02 mm` | `0.05 g` | routes DisplayPort Alt-Mode and USB 3.2 to `U1` Master TCON | RL-1, RL-5 |
| 22 | `U_PD` `USB-PD 3.1` (`40 W`) controller | bidirectional `20 V / 2.0 A` sink/source IC | `3.5 x 3.5 x 0.40 mm` | `±0.02 mm` | `0.10 g` | negotiates `40 W` wired charging and `15 W` OTG reverse output | RL-2 |
| 23 | Digital audio & headset codec (`U3` link) | `32-bit / 384 kHz`, `120 dB` DNR | `3.2 x 3.2 x 0.40 mm` | `±0.02 mm` | `0.05 g` | drives USB-C digital/analog audio and optional `PORT-CJ` `3.5 mm` jack | RL-11 |
| 24 | Direct-drive headphone amp stage | Class-AB/H `2 x 30 mW` into `32 Ω` | `2.0 x 2.0 x 0.35 mm` | `±0.02 mm` | `0.04 g` | `<3 µV` noise floor for wired studio monitoring | RL-11 |
| 25 | `1-Wire` cryptographic Dead-Pad IC | EAL6+ secure authenticator (`3 ms`) | `1.5 x 1.5 x 0.30 mm` | `±0.02 mm` | `0.02 g` | completes `3 ms` challenge-response before closing `VSYS_HV` FET | RL-14 |
| 26 | High-speed differential eye redriver | `10 Gbit/s` equalizer | `2.0 x 2.0 x 0.30 mm` | `±0.02 mm` | `0.03 g` | preserves signal eye across reversible front/back pin mux | RL-1 |
| 27 | `4-channel` TVS ESD protection (`x 2`) | `0.25 pF` ultra-low-capacitance TVS (`±15 kV`) | `2 x (1.0 x 0.6 mm)` | `±0.02 mm` | `0.03 g` | protects sole USB-C port and `12` pogo pins against ESD | RL-1 |
| 28 | Buck-boost inductor & input filter | `1.2 µH` shielded alloy inductor + `2 x 22 µF` | `2.5 x 2.0 x 1.0 mm` | `±0.03 mm` | `0.20 g` | filters `20 V / 2.0 A` USB-C rail into `VSYS_HV` | RL-2 |
| 29 | High-frequency decoupling array | `20 x (0.1 to 4.7 µF)` `0201` MLCCs | `0.6 x 0.3 mm` | `±0.02 mm` | `0.05 g` | local rail impedance `<15 mΩ` | RL-15 |
| 30 | Symmetric gold pogo pins (`x 12`) | hard Au over Ni over BeCu (`0.35 N` each) | `12 x (Ø1.0 x 2.2 mm)` | `±0.02 mm` | `0.45 g` | `18 mΩ` contact resistance; palindrome layout works on `+Z` and `-Z` | RL-8, RL-16 |
| 31 | Individual pin O-ring seals (`x 12`) | 40 Shore A fluoro-silicone micro-rings | `Ø1.6 x 0.25 mm` | `±0.02 mm` | `0.05 g` | isolates each pogo pin against salt fog and water | RL-9 |
| 32 | Multi-edge latch magnets (`8 x N52H`) | bipolar `N52H` NdFeB (`7.2 N` total hold) | `8 x (3.2 x 1.6 x 1.1 mm)` | `±0.02 mm` | `1.55 g` | locks `90°` B stem onto Top, Bottom, Left, or Right screen edge | RL-13, MON-5 |
| 33 | Perimeter `IP68` FKM gasket skirt | 60 Shore A fluoroelastomer (`25%` compression) | `30.0 x 3.6 x 0.40 mm` | `±0.02 mm` | `0.25 g` | seals the `12`-pin dock and USB-C barrel to `IP68` | RL-9, MON-12 |
| 34 | Reversible front/back orientation Hall sensor | dual-axis TMR magnetic polarity sensor | `1.2 x 1.2 x 0.30 mm` | `±0.02 mm` | `0.02 g` | detects which edge (`Top/Bottom/Left/Right`) and face (`+Z/-Z`) is docked | RL-18, MON-5 |
| 35 | Edge alignment keyway & chamfer | `0.65 mm` radiused self-centering lip | `24.0 x 2.2 mm` | `±0.02 mm` | *(in 16)* | centers the `90°` stem on the `2.00 mm` polycarbonate edge within `±0.08 mm` | RL-16, RL-18 |
| 36 | Cu-ferrite RF/power isolation shield | `0.12 mm` copper over nanocrystalline ferrite | `26.0 x 6.8 x 0.12 mm` | `±0.03 mm` | `0.17 g` | isolates `40 W` USB-C switching from the `Wi-Fi 7 / UWB / 60 GHz` stem antennas | RF-9 |
| 37 | USB-C mouth TPU strain relief | 55 Shore A molded elastomer collar | `8.9 x 4.5 mm` | `±0.05 mm` | `0.10 g` | absorbs `30 N` cable side-pull without unseating the `90°` stem | RL-17 |
| 38 | Internal snap-lock ribs (`x 4`) | CNC undercut interlocks inside Ti shell | `0.5 mm` undercut | `±0.02 mm` | *(in 15/16)* | screwless closure of the `90°` stem shell | MEC-5 |
| 39 | Laser-etched regulatory & `EU 2022/2380` plate | micro-etched Grade-5 Ti inner spine | `18.0 x 2.5 mm` | `±0.02 mm` | `0.05 g` | permanent `USB-C PD 40 W` and `CE / EU 2023/1542` markings | RL-9 |
| 40 | Optional `PORT-CJ` `3.5 mm` TRRS studio adapter | detachable side-rail / USB-C studio jack module | `Ø5.0 x 11.5 mm` (optional accessory) | `±0.05 mm` | *(optional)* | provides `3.5 mm` TRRS studio headphone/mic jack when required | RL-4, RL-11 |
| 41 | Optional `PORT-CA` `USB-A` / `microSD` adapter | detachable side-rail host adapter | `13.6 x 5.8 mm` (optional accessory) | `±0.05 mm` | *(optional)* | provides legacy `USB-A` or `UHS-II` card slot off the main body | RL-3, RL-5 |
| 42 | Thermal potting & structural adhesive set | `3.5 W/m·K` silicone potting + PSA | internal fill | `±0.02 mm` | `0.16 g` | conducts USB-C heat into the Ti stem (`<4.2 K` rise at `40 W`) | RL-15 |
