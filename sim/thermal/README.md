# BUDLUM LEAF · SIM · THERMAL · THE TILE BODY AND THE B MODULE

**Revision L.6.0 · 2026-10-12 · the Thermal team**. This directory holds a runnable lumped RC model of the `128` tile body and the B module. It checks the `36.2 °C` cut-off and the cell limits for three cases. It links each result to gates ENR-24 and MEC-11 of Part 21 and Part 11.

## 1 · What is here

| The file | The content |
|---|---|
| `leaf_thermal.py` | the network, the power maps, the charge loss chain, the throttle law, the solvers |
| `run_all.py` | runs every case, writes `results.json` and the plots |
| `results.json` | every number of this README, written by the last run |
| `plots/01_power_maps.png` | the heat per tile and in the ring for cases (a), (b) and (c) |
| `plots/02_session_fields.png` | the steady front surface field, video and 5G, baseline and fixed |
| `plots/03_charge_steady.png` | the steady hottest temperature against the Qi2.2 power |
| `plots/04_charge_transient.png` | the charge from `0` to `80 %` with the throttle law |
| `plots/05_throttle.png` | the throttle law and the throttled video session |
| `plots/06_ambient_sweep.png` | the sustained video power and charge power against the ambient |
| `plots/07_loss_budget.png` | the device heat at `25 W` received |

**How to run it**.

1. Run `python3 run_all.py` in this directory.
2. Read `results.json` and the plots. The run takes about `25 s`.

## 2 · The model

**The network**. Each tile is a stack of five nodes: cap surface, glass and micro-LED, coil or spreader layer, cell, back skin. The layers follow Part 21, Section 21.2.7. `[DECISION]` The B module adds four nodes: ring PCBA, ring shell, B cell and bar. The network has `644` nodes. `[TREE]` `leaf_thermal.py`

**The islands**. A tile joins its neighbours only through the corner hinge and the floating back skin. `[DECISION]` Part 21, Section 21.2.2.

| The path | The conductance per tile pair | The source |
|---|---|---|
| polyimide hinge, `12.5 µm`, `1.3 mm` tall, `0.8 mm` long, with `2 µm` copper | `4.9e-4 W/K` | `[HYPOTHESIS]` geometry of Part 21 |
| floating TPU skin, `80 µm`, `k = 0.2` | `1.6e-5 W/K` | `[HYPOTHESIS]` |
| air in the face kerf at rest | `8.7e-3 W/K` | sensitivity only, off by default |

**The boundaries**. Natural convection of `5.5 W/m²K` per face, and `12 W/m²K` outdoors in a light wind. Radiation is linearised at `ε = 0.90`. The ring is a `Ø32 x 4.0 mm` disc on the face, centred `18 mm` below the top edge. The pad is a fixed temperature under its footprint, with a contact of `400 W/m²K`. `[HYPOTHESIS]`

**The power maps**. Plot `01_power_maps.png` shows them. `[HYPOTHESIS]` Part 4, Section 4.6, sets the split.

| The case | On the tiles | In the B ring | The total |
|---|---|---|---|
| (a) video, Wi-Fi | display `1.00 W`, address `0.25 W` | `U1 0.35`, `U2A 0.40`, `U6 0.30`, `U5 0.05`, `U3/U4 0.12`, `U7/U8 0.03` | `2.50 W` |
| (b) Qi2.2 charge, `25 W` received | coil, shield, AC lead, DC lattice, cells | rectifier, charger, idle | `6.93 W` of heat |
| (c) 5G outdoor | display `1.80 W`, address `0.30 W` | `U5 1.20`, `U1 0.35`, `U6 0.30`, `U3/U4 0.15`, others `0.08` | `4.18 W` |

**The charge loss chain at `25 W` received**. The coil current is `1.85 A` RMS at a `15 V` rectifier. The pad draws `27.7 W`. The cells store `20.8 W`, which is `3.84 C`. `[HYPOTHESIS]`

| The loss | The heat | Where it lands |
|---|---|---|
| receiver coil, `0.30 Ω` with four seam links | `1.03 W` | the `24` coil tiles |
| shield core and can eddy current | `0.40 W` | the coil tiles |
| AC lead, coil to the ring, `0.19 Ω` through the hinges | `0.64 W` | the lead tiles |
| synchronous rectifier, `97.5 %` | `0.64 W` | the ring |
| charger, `95 %` | `1.25 W` | the ring |
| DC lattice at `3.85 V`, solved on the hinge resistor lattice | `1.54 W` | the tiles near the seat tile |
| the `12` bar leaves | `0.34 W` | the bar |
| cells, `50 Ω·mAh` | `1.09 W` | every cell |

## 3 · The fixes

Every fix keeps the `25 W` class and the islanded tiles. Each fix is `[HYPOTHESIS]` until its gate measures it.

| No. | The fix | The number | The gate |
|---|---|---|---|
| F1 | three edge-on hinge leaves of `17 µm` pyrolytic graphite beside the polyimide | `0.048 W/K` per leaf, `k = 1850 W/mK` `[PUBLICATION]` Panasonic PGS | MEC-42 re-run with the laminate |
| F2 | a graphite spreader of `0.14 W/K` per square in the `0.20 mm` layer, with a `1.5 mm` hinge landing | link `0.042 W/K`, `86` times the baseline | MEC-11 |
| F3 | the whole ring underside is a sliding contact pad of `3000 W/m²K` | Part 11 mechanism 3, under `3 K/W` | MEC-11, MON-21 |
| F4 | a graphite strap through the moulded bend and a gel strip under the bar | `0.08 W/K` and `3000 W/m²K` | MEC-11 |
| F5 | the Leaf pad: a full-face pad, fan-cooled to ambient plus `1 K`, or regulated at `22 °C` | `80 x 160 mm` contact | ENR-24, ENR-6 |
| F6 | the throttle law on the hottest surface or NTC | full to `34.2 °C`, `20 %` at `36.0 °C`, off at `36.2 °C` | MEC-6, MEC-12 |
| F7 | `3 g` of encapsulated PCM in the ring, melting at `33 °C` | `600 J` of latent buffer | MEC-11 |

**A rejected fix**. A per-quadrant charger next to the `+` crossing cuts the DC lattice loss from `1.54` to `0.54 W`. It concentrates `1.25 W` in four coil tiles, so the sustained rate on a `22 °C` pad falls. The charger stays in the ring.

## 4 · The results at `25 °C` ambient

### 4.1 Case (a), video, and case (c), 5G outdoor

| The case | The hottest surface | The hottest cell | The sustained power under `36.2 °C` |
|---|---|---|---|
| (a) video `2.50 W`, baseline | `61.3 °C`, the ring | `59.4 °C` | `0.78 W` |
| (a) video `2.50 W`, fixed | `41.3 °C`, the ring | `40.2 °C` | **`1.73 W`** |
| (a) video `2.00 W`, fixed | `38.0 °C` | `37.1 °C` | fails |
| (a) video, an ideal isothermal body | n.a. | n.a. | `2.62 W` |
| (c) 5G `4.18 W`, shade, baseline | `66.0 °C` | `62.9 °C` | `1.15 W` |
| (c) 5G `4.18 W`, shade, fixed | `44.9 °C` | `43.0 °C` | **`2.38 W`** |
| (c) 5G in sun, `600 W/m²` absorbed, fixed | `60.8 °C` | `58.3 °C` | `0 W` |

**The finding**. The B ring is the hot spot in every case. The fixes cut the ring by `20 K`. The cells stay under the `60 °C` discharge limit only with the fixes. `[HYPOTHESIS]`

**The physics floor**. The body and the ring shed `0.31 W/K` to air. At `25 °C` ambient, even an isothermal body holds only `2.62 W` under `36.2 °C`. So a `2` to `3 W` video session at `25 °C` passes only below `22.5 °C` ambient with the fixes. Plot `06_ambient_sweep.png`.

**The throttle**. The fixed body runs `2.50 W` for `2.5 min`, then the law settles it at `1.55 W`. With F7 it runs full power for `15 min`. Plot `05_throttle.png`.

**The palm**. A palm at `34 °C` on the back lowers the sustained video power to `1.60 W`. The hand is warmer than the body, so it adds heat. `[HYPOTHESIS]`

### 4.2 Case (b), Qi2.2 at `25 W`

| The set-up | The steady hottest at `25 W` | The sustained `P_rx` | The time to `80 %` |
|---|---|---|---|
| baseline, Qi2.2 puck at `30 °C` | `137.8 °C` | `3.0 W` | `93 min` |
| fixed, Qi2.2 puck at `30 °C` | `65.0 °C` | `8.5 W` | `36 min` |
| fixed, Leaf pad with fan at `26 °C` | `36.5 °C` | `24.4 W` | `15.6 min` |
| fixed, Leaf pad regulated at `22 °C` | `32.9 °C` | **`30.7 W`**, so `25 W` holds | **`14.0 min`** |

**The verdict for `25 W`**. The `25 W` class holds as a sustained rate only on the regulated Leaf pad. It holds from `15` to `35 °C` ambient. On a third-party puck the body takes `25 W` for under `1 min`, then `8.5 W`. Plot `04_charge_transient.png`.

**The cells while charging**. The hottest cell stays under `34 °C` on both Leaf pads. The `45 °C` charge limit never binds. The coolest cell stays above `22 °C` on the regulated pad. That keeps the `4.4 C` rate clear of lithium plating. `[HYPOTHESIS]` A pad set below `22 °C` is refused for that reason.

## 5 · The gates

| Gate | What this model says | The standing |
|---|---|---|
| **ENR-24** | `25 W` certification needs the full power path. The tile body holds `25 W` sustained on the regulated Leaf pad. On a test puck it throttles to `8.5 W` within `1 min`. | passes with F1 to F6 and the Leaf pad. Open on a puck |
| **MEC-11** | at `35 °C` ambient a surface limit of `36.2 °C` leaves `1.2 K`. The fixed body sustains `0.19 W` of video and `0.26 W` of 5G. | fails for every design. A ruling is needed, Section 6 |
| ENR-6, MEC-6 | the throttle law of F6 replaces the `38 / 45 / 48 °C` curve of Part 11 under the `36.2 °C` cut-off | the law is in `leaf_thermal.py` |
| MEC-42 | F1 adds pyrolytic graphite to the hinge ribbon | the bend test must re-run with the laminate |

## 6 · The open issues

1. **The `36.2 °C` cut-off against the `35 °C` test ambient**. No passive body sheds `2` W through `1.2 K`. Part 4 and Part 11 conflict. The program must rule on one rise-based limit for MEC-11.
2. **The `2` to `3 W` video session at `25 °C`**. It sustains `1.73 W` with the fixes. The gap closes only with a cooler room, a Leaf stand with a fan, or a lower ring power.
3. **The sun**. At `600 W/m²` absorbed, the face exceeds `36.2 °C` with the power off. The policy shows the safe screen and says why.
4. **The rectifier in the ring**. The AC lead loses `0.64 W` in the hinges. A rectifier next to the coil saves it. This team names it and does not move it.
5. **The material numbers**. The cell resistance, the coil resistance, the contact conductances and the chip powers are `[HYPOTHESIS]`. Each is one field of `Config` in `leaf_thermal.py`.
6. **The stretched state**. The model runs at rest. A stretched body opens `6 mm` gaps and adds edge area, so the rest state is the conservative case. Charging runs only at rest. `[DECISION]` Part 21, Section 21.2.6.
7. **The standard limit for context**. IEC 62368-1 sets `43 °C` for a part touched for more than `8 h`. `[PUBLICATION]` At `25 °C` the fixed body passes it for video at `41.3 °C`. The 5G case reaches `44.9 °C` and fails it.
