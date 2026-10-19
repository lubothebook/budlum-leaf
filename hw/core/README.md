# BUDLUM LEAF · CORE AND SKIN · THE INDEX

**Revision L.7 candidate · 2026-10-19 · the Program Lead**. This directory holds blocks `HP-2` to `HP-4`. The result is Part 23 of the directive: `FINAL/23-core-skin-and-the-heartbeat.md`.

## 1 · What is here

| The directory | The seat | The question | The check |
|---|---|---|---|
| `BRIEF.md` | the Lead | the Split, the distance order, and the standing after the studies | read it first |
| `link/` | link | the pixel link and the smallest Skin | `python3 linkmodel.py` |
| `power/` | power | the Skin power tree, the Core energy, the mass | `python3 run_all.py` |
| `heat/` | heat | the Skin alone and the Core alone | `python3 run_all.py` |
| `trust/` | trust | the zero-key Skin and the lying Skin | `python3 -m unittest discover -s tests` |
| `session/` | continuity | many Skins on one Core, roaming | `python3 -m unittest discover -s tests` |
| `study/` | study | prior art, cost and the break-even | `python3 cost.py` |
| `far/` | far link | the link budget at kilometres | `python3 farlink.py` |
| `parts/` | parts | every part by distance class | `python3 parts.py` |
| `fleet/` | fleet | Leafs per Core and the two hosts law | `python3 fleet.py` |
| `invent/` | the Lead | the search for an unlimited battery | `python3 explore.py` |

## 2 · How to run it

1. Install `numpy`, `scipy` and `matplotlib`. The seats `power`, `heat`, `link` and `far` need them.
2. Run the command in the table, from the directory of the seat.
3. Read the `README.md` of the seat for the results and the open issues.

The seats `parts` and `fleet` can need `shapely` for the geometry checks. Without it only the area check runs.

## 3 · The standing

Every number is `[HYPOTHESIS]` until its gate runs. The seats ran models and tests, not hardware. The gate names inside a seat are its own proposals. Part 23 merges them into `CSK-1` to `CSK-29`.
