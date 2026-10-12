# BUDLUM LEAF · HW · DISPLAY · THE STATE OF THE ART AND THE PARTNERS

**Revision L.6.0 · 2026-10-12 · Display team**. Each entry names its tag. An entry marked "verify" is from memory and gets a source check before it enters `FINAL/`.

## 1 · Where the art stands

| No. | The fact | What it means for the Leaf | The tag |
|---|---|---|---|
| R1 | Garmin fēnix 8 Pro MicroLED, AUO panel, 2025: about `326 ppi` | the best shipping micro-LED face; `508 ppi` is `1.56` times it | `[PUBLICATION]` as cited in Part 21.2.3 |
| R2 | Sony Crystal LED (CLEDIS): tiled micro-LED modules, each pixel driven by a micro IC | the uIC drive scheme ships in tiled micro-LED | `[PUBLICATION]` Sony, 2016 on |
| R3 | Samsung The Wall: modular micro-LED tiles with no visible seam at TV pitch | the seamless tile principle ships, at a coarse pitch | `[PUBLICATION]` Samsung, 2018 on |
| R4 | Bower et al., transfer-printed `8 x 15 µm` inorganic LEDs with micro ICs, Photonics Research 5(2), 2017 | micro-transfer printing of LEDs and CMOS ICs on glass | `[PUBLICATION]` verify |
| R5 | Shin et al., vertical full-colour micro-LEDs by 2D-material layer transfer, Nature 614, 81, 2023 | a stacked RGB pixel of a few µm, the long-term path past the quad | `[PUBLICATION]` verify |
| R6 | JBD micro-LED microdisplays on silicon, `2.5 µm` pitch class | InGaN chips far under `5 µm` work at high current density | `[PUBLICATION]` verify |
| R7 | Wong et al., size-independent peak efficiency of III-nitride micro-LEDs, Appl. Phys. Express 12, 097004, 2019 | sidewall passivation holds the EQE at small chips | `[PUBLICATION]` verify |
| R8 | Porotech porous-GaN InGaN red micro-LEDs | the native red of option A | `[PUBLICATION]` verify |
| R9 | PlayNitride micro-LED with quantum-dot colour conversion | the colour path of option B | `[PUBLICATION]` verify |
| R10 | LPKF LIDE laser-induced deep etching of glass | TGVs of about `10 µm` at high aspect ratio | `[PUBLICATION]` LPKF |
| R11 | Intel glass core substrate, announced 2023 | glass with fine vias and RDL is a volume path | `[PUBLICATION]` Intel, 2023 |
| R12 | VESA DSC 1.2b and VDC-M 1.2 | the `3:1` and `5:1` visually lossless link codecs | `[PUBLICATION]` VESA |
| R13 | Wyman, Sloan and Shirley, analytic CIE 1931 fits, JCGT 2(2), 2013 | the colour matching functions in `tile_spec.py` | `[PUBLICATION]` |
| R14 | rotating-square stretchable displays, npj Flexible Electronics, 2024 | the body kinematics checked in `warp.py` | `[PUBLICATION]` as cited in Part 21.2.1 |
| R15 | LG Display stretchable micro-LED panels, 2022 and 2024, about `100 ppi` | stretchable micro-LED ships at about a fifth of the Leaf density | `[PUBLICATION]` verify |
| R16 | display driver ICs on `28 nm` high-voltage CMOS | the uIC node of Section 1.4 | `[GENERAL]` |

**The honest distance**. No one ships `508 ppi` micro-LED on glass. R1 is the nearest face. R6 shows the chips, and R2 and R4 show the drive. The Leaf joins these in one tile. Gap G-40 stays open until DSP-19 passes.

## 2 · The candidate partners

| The block | The candidates | The ask |
|---|---|---|
| blue chips, `5 µm`, passivated | PlayNitride, Porotech, Aledia, JBD | `5 µm` blue chips on a release layer, fault rate `≤ 1e-5` |
| QD colour conversion | PlayNitride, a QD photoresist supplier | `5 µm` QD pattern, `≤ 6 µm` thick, blue-cut filter |
| carrier glass and TGVs | Corning, Schott, AGC, LPKF | `9.994 mm` tiles, `Ø12 µm` TGVs, two Cu RDL layers |
| uIC foundry | TSMC, UMC or Samsung `28 nm` HV | a `20 x 85 µm` die, thinned to `≤ 10 µm`, on a release layer |
| uIC transfer | X Display Company | micro-transfer printing of uICs and chips |
| laser transfer and repair | Kulicke & Soffa, Coherent, Toray Engineering | laser lift-off and re-place, `≤ 2 s` per site |
| inspection | KLA, InZiv | PL and EL of `20 M` chips per device |
| panel integration | AUO | the tile line, after the R1 face |
| link IP | VESA DSC licensees | a DSC encoder for `128` slices and a small decoder per hub |

Each candidate is `[HYPOTHESIS]` until a quote or a sample exists.
