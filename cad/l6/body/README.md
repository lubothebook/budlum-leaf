# CAD-Body · the L.6.0 rotating-square body

**Revision L.6.0 · 2026-10-12**. This directory holds the parametric model of the stretch body of FINAL/21, Sections 21.2.1 to 21.2.6. Units are millimetres. The body centre is the origin.

## 1 · What is here

| The file | The content |
|---|---|
| `body_gen.py` | the parametric generator (numpy, trimesh, shapely, matplotlib) |
| `verify_body.py` | the checks, read from the exported STL files |
| `body-rest.stl` | `θ = 0°`, `80 x 160 mm`, 390 watertight bodies |
| `body-default.stl` | `θ = 17.5°`, the default stretch |
| `body-max.stl` | `θ = 45°`, the maximum stretch |
| `plan-rest`, `plan-default`, `plan-max` | top-view plans, `.svg` and `.png` |
| `plan-three-states.png` | the three states side by side, at one scale |
| `plan-hinge-detail.png` | `3.2 mm` windows on a seam hinge and a plain hinge |
| `body-geometry.json` | the parameters, the face counts and the seat ball positions per state |
| `verify-results.json`, `verify-log.txt` | the results of the last check run |

## 2 · How to run it

1. Run `python3 body_gen.py`. It writes the STL files, the plans and the JSON in about 6 s.
2. Run `python3 verify_body.py`. It exits with `0` when every check passes.
3. Change a value in `BodyParams` to make a variant. Run both scripts again.

## 3 · The model

| The part | The model | The tag |
|---|---|---|
| tiles | `8 x 16 = 128`, `32` per quadrant, `2.00 mm` thick | `[DECISION]` 21.2.1 |
| cell and cut | `10.000 mm` cell pitch, `10 µm` kerf, so a `9.990 mm` tile | `[DECISION]` 21.2.4 |
| kinematics | tile `(i, j)` turns by `(-1)^(i+j) θ`, pitch `a (cos θ + sin θ)` | `[GENERAL]` |
| chamfer | `0.55 mm` leg at all four corners | `[DECISION]` of this team, Section 5 |
| hinge ribbon | PI, `12.5 µm`, `1.20 mm` tall at `z = 0.68` to `1.88`, `0.80 mm` arc | `[DECISION]` 21.2.2 |
| ribbon anchor | the two chamfer midpoints, `30 µm` bond into each tile | `[HYPOTHESIS]` |
| split couplers | the `24` hinges that cross a quadrant line, cut `20 µm` at the middle | `[DECISION]` 21.2.4 |
| seat balls | `6` Si3N4 balls, `Ø0.60 mm`, centre `z = 0.36`, at split-coupler pivots | `[HYPOTHESIS]` |
| Qi zone | annulus `Ø45 / Ø20 mm` at the `+` crossing, cut per tile at rest | `[DECISION]` OD, `[HYPOTHESIS]` ID |

**Why the ball sits on the pivot**. Two seam tiles counter-rotate about their shared pivot. The pivot is the only point fixed to both tiles at every `θ`. So a ball there seats at every state. It lies under the ribbon layer, with a `20 µm` gap in `z`.

**The seat**. Each quadrant sees three balls, a Maxwell seat. Each ball sits in one vee on each side of its seam. The balls of Q1 are at `(0, 10)`, `(0, 70)` and `(20, 0)` at rest.

**The ribbon arc**. The arc has a fixed length of `0.80 mm`. It bulges toward the pivot at rest. It straightens as the chord grows from `0.56` to `0.792 mm` at `45°`.

## 4 · The edge softening (order of Ayaz, 2026-10-12)

The order softens only the sharp touch edges. No whole face is rounded. The fillets are in the STL meshes, not only in this text.

| The edge | The radius | The measured radius |
|---|---|---|
| outer perimeter, front face edge | `r = 0.65 mm` (HARDWARE/06) | `0.650 mm` |
| outer perimeter, back face edge | `r = 0.65 mm` | `0.650 mm` |
| the four outer plan corners | `R = 6.35 mm` | `6.350 mm` |
| PC cap top edge of every tile side | `0.03 mm` break | `0.030 mm` |
| back edge of every tile side | `0.03 mm` break | `0.030 mm` |
| the vertical edges of each chamfered corner | `0.03 mm` break | `0.030 mm` |

**How the mesh holds the fillets**. Each plan vertex carries its own fillet radius. Its column traces an exact quarter circle at the front and the back. The checker fits circles to the STL vertices.

**The run-out**. A hinge chamfer on the outline carries a ribbon bond from `z = 0.68` to `1.88`. A `0.65 mm` fillet there would cut the bond away. So the perimeter fillet runs out from `0.65` to `0.03 mm` over `2.0 mm` before each hinge chamfer. The run-out is a smoothstep, so no crease forms. `[DECISION]` of this team, for review by Ayaz.

**The kerf and the edge pixel stay untouched**. The break reaches only `30 µm` below the cap face. The glass and pixel layer lies at `z = 1.45` to `1.70`. There the tile is the full `9.990 mm`. So the `10 µm` cut and the `20 µm` edge-pixel rule hold: `199 x 50 µm + 2 x 20 µm = 9.990 mm`.

**The facet audit**. No two adjacent facets of a tile turn more than `46.3°`. A `90°` edge split into two facets turns `45°`. So no tile edge is an unrounded crease.

## 5 · The results

All checks pass. Run `verify_body.py` to repeat them.

| The check | `θ = 0°` | `θ = 17.5°` | `θ = 45°` | The gate |
|---|---|---|---|---|
| stretch factor `cos θ + sin θ` | `1.00000` | `1.25442` | `1.41421` | MEC-39 |
| lattice envelope, mm | `80.000 x 160.000` | `100.354 x 200.708` | `113.137 x 226.274` | MEC-39 |
| STL bounding box, mm | `79.990 x 159.990` | `100.006 x 200.359` | `112.345 x 225.482` | MEC-39 |
| area ratio | `1.000` | `1.574` | `2.000` | MEC-39 |
| tiles, per quadrant | `128`, `32` | `128`, `32` | `128`, `32` | MEC-39 |
| largest tile overlap | `0 mm²` | `0 mm²` | `0 mm²` | MEC-39 |
| hinges, largest pivot gap | `232`, `0` | `232`, `1.4e-14 mm` | `232`, `1.4e-14 mm` | MEC-42 |
| ribbon clash with a foreign tile or ribbon | `0` | `0` | `0` | MEC-42 |
| watertight bodies | `390 / 390` | `390 / 390` | `390 / 390` | MEC-39 |
| void diagonals, mm | closed | `6.014` and `19.074` | `14.142` and `14.142` | MEC-41 |
| largest ribbon chord, mm | `0.560` | `0.703` | `0.792` | MEC-42 |
| tile cover of the face | `98.9 %` | `62.9 %` | `49.5 %` | DSP-17 |

**The notes on the table**.

1. The lattice envelope is the hinge-pivot lattice. It equals `(cos θ + sin θ) x 80 x 160` to `1e-9 mm`.
2. The STL box is smaller by the chamfers and the kerf: `0.35 mm` at `17.5°` and `0.79 mm` at `45°`.
3. The `6.01 mm` void diagonal confirms the `6.0 mm` gap of Section 21.2.2.
4. The STL files total `14.7 MB`, under the `15 MB` limit.
5. The Qi zone covers parts of `24` tiles at rest, `1 264 mm²` of coil area.

## 6 · The open issues

| No. | The issue | The owner | The gate |
|---|---|---|---|
| 1 | The `R 6.35 mm` corner clips the `9.25 mm` cell of each corner tile by `5.80 mm²`. That is `0.21 %` of the cell area. The four corner cells need a notched can. | Energy | ENR-22 |
| 2 | The tile covers `62.9 %` and `49.5 %` of the stretched face. Section 21.2.3 states `61 %` and `47.5 %`. That matches a `9.8 mm` active area, which no file defines. | Display | DSP-17 |
| 3 | The ribbon has only `1 %` slack at `45°`: chord `0.792` against `0.800 mm`. A `0.85 mm` ribbon or a `0.50 mm` chamfer gives more margin. | Hinge | MEC-42 |
| 4 | The perimeter fillet runs out to `0.03 mm` over `2.0 mm` at each hinge chamfer. Ayaz must accept this run-out. | Ayaz | MEC-41 |
| 5 | The cap break leaves a `70 µm` V groove at a closed seam: `2 x 30 + 10 µm`. The pixel layer is untouched, but the cap face shows the groove. | Display | DSP-19 |
| 6 | Two balls of each seat lie below its centroid. Their vee axes are only `48°` apart, so the seat is soft in rotation. A ball nearer the outer seam end fixes it. | Seat | MEC-40 |
| 7 | The vees, the N52H preload magnets and the `16` Qi magnets are not modelled. The ball diameter `Ø0.60 mm` is a hypothesis. | Seat, Qi | MEC-40, ENR-24 |
| 8 | The ball clears the ribbon by only `20 µm` in `z`. | Seat, Hinge | MEC-40 |
| 9 | The ribbon ends sink `30 µm` into the tiles, so the STL shells overlap there. A slicer must union them. Each shell is watertight. | CAD | MEC-39 |
| 10 | The ribbon edges are `12.5 µm` sheet edges. They sit `0.12 mm` below the cap face, so the edge check excludes them. | Hinge | MEC-42 |
| 11 | The Qi coil inner diameter of `20 mm` is a hypothesis. | Qi | ENR-24 |
