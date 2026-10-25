# BUDLUM LEAF · THE BEND THAT STAYS AND THE BATTERY-FREE GAPS · WORKING NOTES

**Revision L.8 notes · 2026-10-25 · the Program Lead**. These notes record a read of the repository and a first design pass. No model, script or directive part changed. Every number without a script is `[HYPOTHESIS]` and needs a seat script before it enters `FINAL/`. `[DECISION]`

## 1 · The order

**The order of the founder, 2026-10-25**. *Read Budlum Leaf and code the systems that fix it. Budlum Leaf can be a screen that bends and stays as it is.* `[DECISION]`

The second sentence is a new product order. Part 18 Section 18.7.3 says the panel "holds the curve while you hold it, and it comes back flat". The new order asks the panel to keep the curve after the hand lets go. `[TREE]`

## 2 · Defects found in the tree

| Where | The defect | The fix |
|---|---|---|
| `FINAL/00` line 5 and `DECISIONS.md` BP-01 | both name Part 24 as the battery-free authority, and `FINAL/24-battery-free-panel.md` does not exist | write Part 24 from the seat results and add it to `tools/assemble.py` |
| `hw/panelfree/` | only `BRIEF.md` exists. The seat directories of S1 to S5 are empty | run the seats H1 to H11 |
| `tools/check_crossrefs.py` | the prefixes `BFP` and a hold prefix are not in `DEVICE_PREFIXES`, so their gate rows go uncounted | add the prefixes with the first gate table |
| `DECISIONS.md` | the gates `BFP-1` to `BFP-9` have no gate table in `FINAL/` | define them in Part 24 |

## 3 · The bend that stays: five mechanisms

The rule of the battery-free panel decides the field. The panel is passive without the Core, so a hold that needs panel energy is refused (BP-00). `[DECISION]`

| The mechanism | How it holds | The result | The mark |
|---|---|---|---|
| a ductile metal core, `0.20 mm` annealed aluminium | the metal yields and keeps the set | after a press onto a table the panel keeps a bow of about `16 mm` over `160 mm`. The flat rule of Part 18 allows `0.15 mm` | **NOT FEASIBLE** |
| a sealed vacuum pack of sliding films | the air pressure clamps the films, and friction holds the shape | a closed envelope ties the two faces into a stiff sandwich. At `R 30 mm` the free end relaxes over about `110` of `160 mm` | **NOT FEASIBLE** as a closed envelope |
| a shape memory polymer layer | the Core heats it soft, it cools rigid | about `260 J` per reshape and about `26 s` at `10 W`. A hot day returns it flat | **NOT FEASIBLE** as the main hold |
| a segmented friction spine on the rear | friction hinges hold each angle | the joints exceed the `2.00 mm` limit, and the display sees a tight local radius at each joint | **NOT FEASIBLE** under `2.00 mm` |
| **electrostatic layer jamming** | thin films slide while the voltage is off and lock while the Core applies a voltage | the shape holds with the Core attached, and the panel returns flat when the Core lets go | **NEEDS TEST** |

All values in the table are hand calculations. `[HYPOTHESIS]`

### 3.1 The pick: electrostatic layer jamming

**The principle**. A laminate of compliant strips couples by friction when a pressure presses the strips together. `[PUBLICATION]` Narang, Vlassak and Howe, *Mechanically Versatile Soft Machines through Laminar Jamming*, Advanced Functional Materials 28 (17), 2018, https://dash.harvard.edu/entities/publication/f4730fd6-09ae-442c-bb2e-f482bea7f02c

**The clamp**. An electrostatic clutch reaches about `20 N/cm²` of shear stress at `300 V`, with a release time under `15 ms`. `[PUBLICATION]` EPFL LMTS, Hinchet and Shea, https://www.epfl.ch/labs/lmts/lmts-research/haptics/textile-clutch

**The first sizing**. These are the values of the first pass. `[HYPOTHESIS]`

| The quantity | The value |
|---|---|
| the design shear stress | `50 kPa` at `120 V`, half of the published values |
| the film pack | about `20` films of `14 µm`, `0.30 mm` thick, about `5.4 g` on a Leaf 160 |
| the anchor | all layers join at one short edge, the Core edge. The other edges slide free |
| the springback stiffness | about `9 x 10⁻⁴ N·m`, with no closed envelope |
| the relaxed end at `R 30 mm` | about `3 mm` at the free end |
| the touch press that the hold resists | about `1.6 N`, `65 mm` from a grip at the Core edge |
| the reshape moment | about `0.13 N·m`, a firm two-hand bend |

**The behaviour**. The Core locks the shape. It releases the films when it senses a two-hand bend grip, and locks again after the hand stops. With the Core removed, the panel relaxes flat. `[HYPOTHESIS]`

**The open points**.

1. The charge on the films is a capacitor, and BP-00 refuses a capacitor used as an energy store. The Core discharges the films at detach.
2. The voltage class is open. A design at `60 V` gives about a quarter of the clamp at `120 V`.
3. Water between the films lowers the clamp. The seal class needs a gate.
4. A prior art search is open. Published patents already show a jamming laminate, for example US 11112827. `[PUBLICATION]` https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11112827

**The shape sensing**. The jamming electrodes can measure the slip between two films. The slip gives the turning angle along the panel, so the Core reads the shape for the image and the touch map. `[HYPOTHESIS]`

## 4 · The battery-free findings of the first pass

| Task | The finding | The mark |
|---|---|---|
| H8 Core heat | the `70 x 30 x 10 mm` reference Core reaches `47.6 °C` mean case at `1.6 W` and `25 °C` ambient. It holds `43 °C` up to `1.22 W` | **NEEDS TEST** |
| H8 charging | `60 W` into a Core cell of about `7.5 Wh` is about `8C`, above a fast-charge cell | **NOT FEASIBLE** at the reference size |
| H3 runtime | a Leaf 160 delta session draws about `2.4 W` at the Core. About `3 h` on `7.5 Wh` | **NEEDS TEST** |
| H1 panel silicon | about `1 600` source lines with a `1:6` demux need a `25 µm` pitch. A detachable contact needs about `0.4 mm`. The source driver stays on the panel | **NEEDS TEST** |
| H2 attach zones | at `6 Gbit/s` a stub over about `6 mm` reflects. Each zone needs its own receiver port, or zones share one pad stack | **NEEDS TEST** |
| H4 and H7 stack | a bonded PC carrier pulls the inorganic layers by about `0.24 %` from `23` to `60 °C`. The design limit is `0.3 %` | **NEEDS TEST** |

The heat figures come from `hw/core/heat/coreheat.py` `box_T` and `box_Qmax`, run read only. The other figures are hand calculations. `[HYPOTHESIS]`

**The touch limit**. IEC 62368-1 sets a TS1 limit of `48 °C` for a plastic surface held in normal use for more than one minute. `[PUBLICATION]` https://www.advancedenergy.com/en-us/about/news/blog/design-considerations-for-maximum-temperature-per-iec-safety-standards/

## 5 · The next moves

1. Write the seat scripts of S1, S2 and S3 under `hw/panelfree/`, with outputs in `out/`.
2. Write the hold seat `hw/panelfree/hold/`: the friction capacity, the poses, the touch press and the slip sensing.
3. Write Part 24 and Part 25 with their gates, and run PRG-12, PRG-15 and PRG-16.
