# BUDLUM LEAF · HOST POWER · THE INDEX

**Revision L.6.1 (proposed) · 2026-10-19 · the Program Lead**. This directory holds the work of block `HP-1`. The result is Part 22 of the directive: `FINAL/22-host-power-and-the-living-leaf.md`.

## 1 · What is here

| The directory | The seat | The question | The check |
|---|---|---|---|
| `BRIEF.md` | the Lead | the thesis, the rules and the corrections | read it first |
| `powerpath/` | power path | the tiers, the power path, the cell life, the host classes | `run_all.py` |
| `thermal/` | thermal | which interface holds `36.2 °C` | `run_all.py` |
| `trust/` | trust | a host must never gain authority | `python3 -m unittest discover -s tests` |
| `continuity/` | continuity | a session across a power gap, and RG-19 | `python3 -m unittest discover -s tests` |
| `study/` | study | prior art, the law, the standards and the claim | `python3 tools/check_prose.py` |

## 2 · How to run it

1. Install `numpy`, `scipy` and `matplotlib`. The seats `powerpath` and `thermal` need them.
2. Run the script named in the table, from the directory of the seat.
3. Read the `README.md` of the seat for the results and the open issues.

The `trust` and `continuity` tests use the standard library only.

## 3 · The standing

Every number is `[HYPOTHESIS]` until its gate runs. The seats ran models and tests, not hardware. The gate names inside a seat are its own proposals. Part 22 merges them into `HST-1` to `HST-29`.
