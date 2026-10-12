# BUDLUM LEAF · HARDWARE · 07 · THE 3D MODELS AND RENDERS

**Revision L.5.0 · 2026-10-12**.
All 13 3D STL models and 8 renders are generated programmatically. Also, Revision L.5.0 (`4 x 40.0 x 80.0 x 2.00 mm` `+` snap-together polycarbonate screen-battery quadrants, universal `Qi2.2` wireless charging, and `90°`-bent-stem B module). Every model is a closed, watertight 2-manifold triangle mesh.

---

## 1 · The generators in `cad/`

| The script | What it builds | How to run |
| --- | --- | --- |
| **`cad/leaf_v2.py`** | Revision L.5.0 assembly (`84` internal subparts): `4 x 40x80x2.00 mm` (`68 g`) `+` quadrants, `LLZO` battery, `Qi2.2` coils,. Also, `90°`-bent-stem B module (`20 g`) | `python3 cad/leaf_v2.py` |
| **`cad/monogram_letter.py`** | 1:1 analytical geometry of `uploads/b.png` and Revision L.5.0 `90°`-bent stem (`b_flat_ring_outline`, `b_bent_stem_profile`, `+` seam helpers) | imported by `leaf_v2.py`, `monogram_detail.py`, and `pafta/` |
| **`cad/monogram_detail.py`** | Standalone STLs (`monogram-ring.stl`, `monogram-letter.stl`) and engineering SVGs (`monogram-section.svg`, `monogram-exploded.svg`) of the `90°`-bent-stem B module | `python3 cad/monogram_detail.py` |
| **`cad/leaf_geom.py`** | Family geometry helpers (`quadrant_outline`, `stack`, `mesh_from_rings`) and class bodies (`leaf80-body.stl` `2.00 mm`, `leaf160-body.stl` `2.00 mm`, `leaf480-body.stl` `2.40 mm`) | `python3 cad/leaf_geom.py` |
| **`cad/leaf_classes.py`** | Builds the class bodies and plan SVGs/PNGs via `leaf_geom.main()` | `python3 cad/leaf_classes.py` |
| **`cad/rail_detail.py`** | Builds the `+` cross seam / Qi2.2 / `90°` B stem USB-C STLs and SVG (`rail-module.stl`, `rail-receiver.stl`, `rail-detail.svg`) | `python3 cad/rail_detail.py` |
| **`cad/render3d.py`** | Pure-Python perspective renderer with view-direction depth sorting and horizontal Y-strip bending triangulation | imported by `leaf_v2.py` |
| **`cad/heypcb_post.py`** | Composes the 6-panel Revision L.5.0 master visual sheet `heypcb-post.png` and `heypcb-post.txt` into `teslim/` | `python3 cad/heypcb_post.py` |

---

## 2 · The active 3D STL models in `cad/models/`

All bulky bottom-battery (`228 mm` tall) files are retired and replaced by the `80.0 x 160.0 x 2.00 mm` 4-Quadrant (`+`) body. Also, `90°`-bent-stem B module.

| The model | The file | Dimensions (`mm`) | Triangles | Description |
| --- | --- | --- | --- | --- |
| **Leaf 160 complete device** | `cad/models/leaf160-device.stl` | `80.0 x 172.0 x 6.70` | `155 968` | `4 x (40x80x2.00 mm)` (`68 g`) `+` quadrants + `90°`-bent-stem B module (`20 g`, ring flat on screen. Stem bent `90°` at top edge) |
| **90°-Bent-Stem B module** | `cad/models/monogram-module.stl` | `40.0 x 44.0 x 6.70` | `49 856` | `32` internal parts: `90°`-bent stem (`USB-C` + antenna) + flat `Ø32/Ø24 mm` ring (`50 MP` camera, rear AMOLED, Zero-CPU SiP) |
| **Leaf 160 4-Quadrant (+) frame & seam** | `cad/models/leaf160-frame.stl` | `80.0 x 160.0 x 2.20` | `73 792` | `4` `ISO 10993` polycarbonate shells (`Q1..Q4`), `<15 µm` (`n=1.585`) `+` lip, `(0,0)` Ti hub, `8` Ti pins, `24` N52H magnets. `64` gold leaves |
| **Leaf 160 T-OLED + PDLC + AgNW/ITO** | `cad/models/leaf160-screen.stl` | `77.8 x 157.8 x 1.96` | `21 088` | 4-quadrant flicker-free `T-OLED` + `PDLC` privacy film + `AgNW/ITO` mesh + graphene/Mu-metal shield |
| **4-Quadrant LLZO battery & Qi2.2** | `cad/models/leaf160-battery.stl` | `73.4 x 153.4 x 1.60` | `57 056` | `4 x 3.0 Wh = 12.0 Wh` `LLZO/PEO` solid-state cells, bifilar tabs, `36.2 C` NTCs, `Ø54 mm` `Qi2.2` coil. `4 x Ø22 mm` `Qi` coils, `U_QI` |
| **Bent 4-Quadrant (+) screen-battery** | `cad/models/leaf160-battery-bent.stl` | `80.0 x 137.4 x 59.7` | `21 568` | 3D flexed state (`R 25.5 mm`, `0.38%` strain) of the 4-Quadrant (`+`) polycarbonate + `LLZO` solid-state battery laminate |
| **B module ring + camera/panel** | `cad/models/monogram-ring.stl` | `40.0 x 44.0 x 6.70` | `22 176` | flat circular ring assembly + `90°` hinge, `50 MP` folded optics, rear round AMOLED, and 6L Zero-CPU PCBA |
| **B module complete letter** | `cad/models/monogram-letter.stl` | `40.0 x 44.0 x 6.70` | `49 856` | complete `90°`-bent-stem B module with all `32` internal components |
| **Leaf 80 / 160 / 480 bodies** | `leaf80/160/480-body.stl` | `40x80x2.20` / `80x160x2.20` / `320x480x2.40` | `2 916` each | single-quadrant eyewear tile (`Leaf 80`), 4-quadrant phone (`Leaf 160`), and multi-tile desk sheet (`Leaf 480`) |
| **Qi2.2 / `+` seam & B stem dock** | `rail-module.stl`, `rail-receiver.stl` | `76.8 x 35.6 x 3.00` | `4 032 / 656` | `+` seam / `Qi2.2` / `90°` B stem USB-C subassemblies |

---

## 3 · The rendered views in `teslim/`

| Render file | What it shows |
| --- | --- |
| `teslim/render-whole.png` | 3/4 view of the `80x160x2.00 mm` (`68 g`) 4-Quadrant (`+`) body (`Qi2.2`, zero USB-C on body). It uses the `90°`-bent-stem B module (`20 g`) on the screen |
| `teslim/render-face.png` | front view: seamless `<15 µm` (`n=1.585`) `+` cross, `4 x 3.0 Wh` `LLZO` cells, `Ø54 mm` `Qi2.2` coil,. Also, flat B ring on screen with `90°` stem at top edge |
| `teslim/render-back.png` | rear view: rear T-OLED across `Q1..Q4`, `Qi2.2` + `4 x Ø22 mm` wireless coils,. Also, reversible `90°`-bent-stem B module (`Ø22.4 mm` round AMOLED) |
| `teslim/render-battery.png` | `Q4` quadrant detached (`EU 2023/1542` Art. 11 `<3 s` swap) showing `(0,0)` Ti hub, `24` N52H magnets, `64` gold leaves, and `LLZO` + `Qi2.2` internals |
| `teslim/render-apart.png` | exploded view of all `84` internal parts across `Q1..Q4` (`2.00 mm` 11-layer stack, `LLZO` cells, `Qi2.2`) and the `90°`-bent-stem B module |
| `teslim/render-module.png` | close-up of the `90°`-bent-stem B module (`32` parts): `90°` stem (`USB-C` + LCP/60GHz antenna) and flat ring (`50 MP` camera, OIS. Prism, 6L PCBA) |
| `teslim/render-module-back.png` | rear close-up of the `90°`-bent-stem B module: `Ø22.4 mm` round LTPO AMOLED, `0.15 mm` Cu-graphite shield, `±90°` Ti hinge,. Also, `12` gold dock pins |
| `teslim/heypcb-post.png` | 6-panel Revision L.5.0 master visual sheet (`2400 x 1950 px`) combining all views and specifications |
