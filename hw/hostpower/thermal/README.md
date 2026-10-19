# BUDLUM LEAF · HOST POWER · THERMAL · CONDITION 2 OF THE HOST LIFE LAW

**Revision L.6.1 (proposed) · 2026-10-19 · the Thermal team of `hw/hostpower`**. This directory answers one question. When the host feeds the Budlum Leaf 160, is always-on possible under the `36.2 °C` skin limit, and through which interface? Every number below comes from `python3 run_all.py`. Every material number is `[HYPOTHESIS]` unless a source is named.

## 1 · The verdict, thesis damage first

**Host power does not pass condition 2 in free air. No interface passes, and the battery baseline fails too.** The heat comes from the session. The interface only adds to it. `[HYPOTHESIS]` `out/thesis_check.txt`

1. **Free air fails everywhere**. A delta session of `2.5 W` on the fixed body reaches `41.3 °C` on the battery at `25 °C`. That is `5.1 K` over the limit. Contact fails by `5.9` to `8.4 K`. Qi fails by `5.8` to `6.0 K`. Zero of `72` free-air combinations pass.
2. **Host power gives no heat gain at session power**. The battery path loses only `0.04 W` at `2.5 W`. Contact with a `0.10` to `0.34 W` interface loss is hotter than the battery. Qi in float mode adds `0.2` to `0.8 W`.
3. **Qi weakens the thesis when the host charges the cell**. Qi2.2 at `25 W` received puts `9.2 W` of heat in the body with a delta session running. The skin reaches `37.3 °C` even on the dock cold plate, which is `1.1 K` over the limit. In free air the admitted load falls to `0 W`.
4. **Qi is harmless when the host only feeds the load**. In float mode the Qi class changes the heat by under `0.2 W`. The class sets the cap on the load, not the heat. BPP `5 W` carries at most `4.7 W` of load.
5. **The dock cold plate is the only path to always-on**. All `72` combinations pass with margins of `+3.1` to `+9.4 K`. The plate holds `22 °C`. The TEC takes `0.4` to `5.1 W` of electric power for the nominal sessions. `[HYPOTHESIS]` `out/dock_tec.txt`

**The sentence the program can keep**. Always-on needs the host to feed the load and the dock to pull the heat. The cell staying small is a mass and volume gain. It is not a heat gain.

## 2 · What is here

| The file | The content |
|---|---|
| `hostthermal.py` | the library: sessions, interfaces, environments, heat vectors, the sustained search, the throttle fixed point |
| `eyewear.py` | the bounded two-node study of a host-fed Leaf Frame |
| `run_all.py` | runs the self check and all items, writes `out/` |
| `out/selfcheck.txt` | five checks against `sim/thermal/README.md`, all pass |
| `out/item1_cases.{json,txt}` | the steady hottest point for each session and interface at `25` and `30 °C` |
| `out/item2_admission.{json,txt}` | the admitted load power for `20`, `25`, `30`, `35 °C`, wind, cold plate, and the Qi classes |
| `out/item3_feed_vs_charge.{json,txt}` | float against `+0.2 C`, `1 C` and charge at the cap |
| `out/eyewear.{json,txt}` | the face-side limit and the host budget of the Frame |
| `out/item5_throttle.{json,txt}` | the steady state of the throttle law at `30` and `25 °C` |
| `out/dock_tec.{json,txt}` | the TEC check of the `22 °C` cold plate |
| `out/thesis_check.{json,txt}` | the margin in kelvin of condition 2 for every interface |
| `out/plots/01` to `05` | cases, admission, feed against charge, eyewear, throttle |

**How to run it**.

1. Install `numpy`, `scipy` and `matplotlib` for `python3`.
2. Run `python3 run_all.py` in this directory. The run takes about `10 s`.
3. Read `out/thesis_check.txt` first, then the item files.
4. Check the prose with `python3 tools/check_prose.py hw/hostpower/thermal/README.md` from the repository root.

The scripts import `sim/thermal/leaf_thermal.py` and `hw/dock/budget.py` read only. They write nothing outside this directory.

## 3 · The model and the assumptions

**The body**. The fixed body F1 to F4 of `sim/thermal`: graphite hinge, graphite spreader layer, full-disc ring pad, ring strap. `[HYPOTHESIS]` The unfixed body reaches `61.3 °C` in the delta session, so it is not a candidate.

**The check**. The model reproduces `41.3 °C` for the delta session, `44.9 °C` for 5G, `1.73 W` sustained and `6.93 W` of Qi heat. `[TREE]` `out/selfcheck.txt`

**The gate quantity**. `T_skin` is the hottest touchable surface: front cap, ring shell, bar or back skin. The ring shell is the hottest point in nearly every case. The hottest front cap tile is `0.2` to `0.6 K` lower and is in the JSON as `T_cap`.

| The session | The map | The power at the loads |
|---|---|---|
| delta | map (a) of `sim/thermal`, called video there | `2.50 W`, body `1.25 W`, ring `1.25 W` |
| video Wi-Fi | `hw/energy` video session, ring split of map (a) | `3.27 W`, body `1.35 W`, ring `1.92 W` |
| 5G outdoor | map (c) of `sim/thermal`, with the light wind of `12 W/m²K` | `4.18 W` |

| The interface | The model |
|---|---|
| battery | cell `I²R` and the DC lattice of `sim/thermal`, as in `session_q` |
| contact `0.10`, `0.34 W` | the host feeds VBUS. The cell floats. The fixed loss sits on the seat tile pads. The two bounds come from `FINAL/11` and `hw/dock` |
| contact, I²R of a worn pad | the physics check: `5.7 mW` at `1.92 W` from `hw/energy` times `3.97` for a worn pad. It gives `0.04` to `0.11 W` |
| Qi BPP `5 W`, EPP `15 W`, MPP `25 W` | the charge loss chain of `sim/thermal` at the received power. Rectifier output `5`, `12`, `15 V` |

**The Qi chain**. The host input is the smallest received power that feeds the load. The cell current is zero in float mode. The coil, the shield, the lead, the rectifier, the charger and the lattice scale with the received power. The charger stays at `95 %` at every class. `[HYPOTHESIS]`

**The three supports**. Free air means both faces in air. The Qi rows lie on a passive puck of `Ø58 mm` at ambient plus `1` to `5 K`. The dock rows lie on the full-face `22 °C` plate of `hw/dock`. The row "battery, on a table" gives the Qi support with no host power. `[HYPOTHESIS]`

## 4 · Item 1: the cases at `25 °C`

Steady hottest skin point in °C. The margin is `36.2 °C` minus that value. Light wind applies to 5G only. `[HYPOTHESIS]`

| The case | Delta `2.5 W` | Video `3.3 W` | 5G `4.2 W` |
|---|---|---|---|
| battery, in air | `41.3` (`-5.1`) | `48.2` (`-12.0`) | `44.9` (`-8.7`) |
| battery, on a table | `40.1` (`-3.9`) | `46.7` (`-10.5`) | `46.1` (`-9.9`) |
| contact, `0.10 W` loss | `42.1` (`-5.9`) | `49.0` (`-12.8`) | `45.4` (`-9.2`) |
| contact, `0.34 W` loss | `44.6` (`-8.4`) | `51.0` (`-14.8`) | `46.9` (`-10.7`) |
| Qi BPP `5 W`, float | `42.2` (`-6.0`) | `49.6` (`-13.4`) | `49.4` (`-13.2`) |
| Qi EPP `15 W`, float | `42.0` (`-5.8`) | `49.1` (`-12.9`) | `48.8` (`-12.6`) |
| Qi MPP `25 W`, float | `42.0` (`-5.8`) | `49.1` (`-12.9`) | `48.8` (`-12.6`) |
| Qi MPP `25 W`, cell `+0.2 C` | `43.0` (`-6.8`) | `50.2` (`-14.0`) | `49.8` (`-13.6`) |
| any interface on the dock plate | `27.2` to `28.4` | `29.7` to `31.0` | `30.4` to `31.9` |

**The reading**. Against the same table support, Qi in float mode adds `1.9 K` in the delta session. The charge chain costs `0.2 W`. The contact bound of `0.34 W` costs `3.3 K` against the battery in air. `30 °C` rows are in `out/item1_cases.txt`.

## 5 · Item 2: the admission table

The largest sustained load that holds `36.2 °C`, in W at the loads, delta shape. The nominal delta load is `2.50 W`. `[HYPOTHESIS]` Full tables for the other two sessions are in `out/item2_admission.txt`.

| The case | `20 °C` | `25 °C` | `30 °C` | `35 °C` |
|---|---|---|---|---|
| battery, in air, still | `2.47` | `1.73` | `0.97` | `0.19` |
| battery, in air, light wind | `3.39` | `2.37` | `1.33` | `0.26` |
| contact `0.10 W`, still | `2.34` | `1.60` | `0.82` | `0.00` |
| contact `0.34 W`, still | `1.91` | `1.09` | `0.25` | `0.00` |
| Qi MPP, float, puck, still | `2.37` | `1.64` | `0.89` | `0.12` |
| Qi MPP, float, puck, light wind | `2.83` | `1.95` | `1.06` | `0.16` |
| Qi MPP, cell `+0.2 C`, still | `2.22` | `1.49` | `0.74` | `0.00` |
| Qi MPP, charge at the cap, still | `0.00` | `0.00` | `0.00` | `0.00` |
| dock plate, battery or contact `0.34 W` | `6.9` to `7.2` | `6.6` to `7.0` | `6.4` to `6.7` | `6.2` to `6.5` |
| dock plate, Qi MPP, float | `6.29` | `6.09` | `5.89` | `5.68` |
| dock plate, Qi BPP, float | `4.67` | `4.67` | `4.67` | `4.67` |
| dock plate, Qi MPP, charge at the cap | `2.15` | `1.91` | `1.67` | `1.42` |

**What makes always-on impossible**. The following combinations never carry a full session.

1. **Free air above `20 °C` in still air**. No interface holds the delta session of `2.5 W`. At `20 °C` the battery admits `2.47 W`, which is `0.03 W` short.
2. **Free air at `35 °C`**. Every interface admits `0.26 W` or less, with or without wind.
3. **Any Qi class that charges the cell at its cap, off the dock**. Qi EPP and MPP admit `0 W` at every ambient in still air. The BPP admits `0.97 W` at `25 °C`.
4. **Video Wi-Fi on a Qi MPP pad that charges at `25 W`**. Off the dock the admitted load is `0 W`. On the dock it is `1.2` to `1.9 W`, under the `3.27 W` of the session.
5. **Any session on a Qi MPP pad that charges at `25 W`, even on the dock**. The dock admits `1.2` to `2.2 W` at `20` to `35 °C`. Qi EPP at its cap also fails the 5G session on the dock at `30 °C` and above.
6. **Light wind at `20 °C` is the only free-air pass**. The delta session passes for all classes in float mode and on the battery. Nothing else in free air passes.

**The largest Qi class for an always-on delta session**. The Qi class is not the limit in float mode.

| The rule | Free air, `20 °C` wind | Free air, other | Dock, `20` to `35 °C` |
|---|---|---|---|
| A: the host feeds the load, the cell floats | all three classes | none | all three classes. BPP caps the load at `4.67 W` |
| B: the host charges the cell at its cap | none | none | BPP and EPP. EPP fails 5G at `30 °C` and above. MPP never passes |

## 6 · Item 3: feed the load or charge the cell

Heat inside the Leaf in W, delta session, Qi MPP, `25 °C`. The skin column is the puck row. `[HYPOTHESIS]` Full tables are in `out/item3_feed_vs_charge.txt`.

| The rule | The heat | The heat saved by float | The skin | The host wall draw |
|---|---|---|---|---|
| float: the host feeds the load | `2.75 W` | none | `42.0 °C` | `3.1 W` |
| the cell gains `0.2 C` (`1.14 W`) | `2.89 W` | `0.15 W`, `1.1 K` | `43.0 °C` | `4.5 W` |
| the cell charges at `1 C` | `3.74 W` | `1.0 W`, `6.6 K` | `48.6 °C` | `10.5 W` |
| the host input sits at `25 W` | `9.19 W` | `6.4 W`, `35 K` | `77.0 °C` | `31.0 W` |

**The same rule on the other classes**. Qi EPP at its cap gives `5.67 W`, so float saves `2.9 W`. Qi BPP is capped at `5 W`, so float saves `0.7 W`. A contact feed that charges at `25 W` gives `6.25 W`, so float saves `3.6 W`. `[HYPOTHESIS]`

**On the dock plate**. Charging at `1 C` during the delta session costs `2.1 K` and `1.0 W`. Charging at the Qi MPP cap costs `9.4 K` and reaches `37.3 °C`. The cold plate absorbs `1 C` but not `25 W`.

**What the rule buys in admitted power**. On a puck at `25 °C` the delta-shape load is `1.64 W` in float. It is `1.49 W` at `+0.2 C`, `0.76 W` at `1 C` and `0 W` at the cap. The float rule is worth `0.15 W` at the low top-up and `0.9 W` against `1 C`.

**The justification for the power-path team**. Feed the load from the host and keep the cell current at zero during a session. Allow the `+0.2 C` top-up only when the skin sits under `34.2 °C`, where the throttle law is still at full power. Charge the cell at a higher rate only off the session or on the dock plate. `[DECISION]` proposed

## 7 · Item 4: the eyewear case

A bounded two-node model of a host-fed Leaf Frame. The Frame is `30` to `40 g` and draws `0.4` to `1.2 W` with the display on (`FINAL/07` Section 7.5). The face-side limit is `36.2 °C` (`FINAL/04`, gate ENR-16). `[DECISION]`

**The assumptions**. All are `[HYPOTHESIS]`. They are listed in `out/eyewear.json`.

1. Skin at `34 °C` at the nose and temple. The skin is a fixed sink.
2. Exposed area `100 cm²`. Contact patches `8 cm²` with a `1 mm` cover and a light-pressure contact of `100 W/m²K`.
3. A hot spot of `60 %` of the heat behind a `3 K/W` spreading resistance. Both the outer surface and the contact surface must stay at or under `36.2 °C`.
4. The worn host feeds through a temple connector or a cable. The connector loss is `0.10` to `0.34 W`. Qi is not worn, because decision R-1 removes the coil.

| The ambient | The heat limit, still air | The heat limit, wind | The load that fits, still, loss `0.34 W` |
|---|---|---|---|
| `20 °C` | `1.47 W` | `2.09 W` | `1.13 W` |
| `25 °C` | `1.05 W` | `1.48 W` | `0.71 W` |
| `30 °C` | `0.63 W` | `0.86 W` | `0.29 W` |
| `35 °C` | `0.20 W` | `0.23 W` | `0.00 W` |

**The reading**. A Frame at `0.8 W` with a `0.34 W` connector loss holds the limit in still air up to about `24 °C`. A `1.2 W` Frame holds up to `19 °C`. A `0.4 W` Frame holds up to `28.7 °C`. The host budget is the heat limit and not the wall power. The skin at `34 °C` leaves only `2.2 K` of rise. `[HYPOTHESIS]`

**The sensitivity**. At `25 °C` the limit moves from `1.05 W` to `1.36 W` with an ideal spreader and to `0.86 W` at `6 K/W`. The skin temperature and the contact area move it by under `0.05 W`.

**What this means**. A host feed does not lower the Frame heat. It removes the cell and its mass. The face-side limit then caps the host budget at about `1 W` at room temperature. Always-on on the face is a `0.4 W` class function above `25 °C`. `[HYPOTHESIS]`

## 8 · Item 5: the throttle at `30 °C`

The law of `sim/thermal`: full to `34.2 °C`, `20 %` at `36.0 °C`, off at `36.2 °C`. The table gives the steady fixed point of the whole session, as the run of `sim/thermal` throttles it. Brightness comes from the display term by `FINAL/17` Section 17.13. `[HYPOTHESIS]`

| The case at `30 °C`, no cold plate | Delta held | Video held | 5G held |
|---|---|---|---|
| battery | `35 %` | `26 %` | `30 %` |
| contact `0.10 W` | `30 %` | `22 %` | `27 %` |
| contact `0.34 W` | `9 %` | `7 %` | `13 %` |
| Qi BPP, EPP, MPP, float | `32 %` | `23` to `24 %` | `24 %` |
| any interface on the dock plate | `100 %` | `100 %` | `100 %` |

**The picture level held**. The delta session on the battery holds `0.35` of its display term. That is about `147 nits` at a `35 %` picture level, or `21 %` at `250 nits`. On Qi it is `135 nits`. Video falls to `101` to `118 nits` on all but the `0.34 W` contact, below the `30 %` floor of the law. The dock plate holds `417 nits` for delta, `458` for video and `750` for 5G. At `25 °C` the battery and the Qi classes hold `0.59` to `0.62` of the delta session. That is `244` to `258 nits`.

**A display-only throttle holds nothing**. The ring alone dissipates `1.25 W` in the delta session. At `30 °C` in free air the ring is over the limit with the picture off. The throttle must reduce the hub and the radio too. `[HYPOTHESIS]`

## 9 · Condition 2 per interface

Margin in K at the nominal sessions, `25 °C`. A negative margin is a failure by that many degrees. `out/thesis_check.txt` holds `20`, `30` and `35 °C`.

| The interface | Delta | Video Wi-Fi | 5G outdoor | The verdict |
|---|---|---|---|---|
| battery, in air | `-5.1` | `-12.0` | `-8.7` | fails |
| contact, no plate | `-5.9` to `-8.4` | `-12.7` to `-14.8` | `-9.2` to `-10.7` | fails |
| Qi BPP, EPP, MPP, puck | `-5.8` to `-6.0` | `-12.9` to `-13.4` | `-12.6` to `-13.2` | fails |
| contact, dock plate | `+8.3` to `+8.8` | `+5.8` to `+6.3` | `+5.2` to `+5.7` | passes |
| Qi, dock plate | `+8.2` to `+8.3` | `+5.5` to `+5.6` | `+4.6` to `+4.7` | passes |

**The best free-air case**. Delta at `20 °C` on the battery fails by `0.2 K`. Delta at `20 °C` through contact `0.10 W` fails by `1.0 K`. Through Qi MPP it fails by `0.8 K`. `[HYPOTHESIS]`

## 10 · The open issues

1. **The body is the limit, not the host**. The fixed body sustains `1.73 W` at `25 °C`. An ideal isothermal body holds `2.62 W` (`sim/thermal`). A cooler ring or a larger radiating face is the only lever without a dock.
2. **The `36.2 °C` limit against ambient `35 °C`**. It is the open issue 1 of `sim/thermal` and it stays open. At `35 °C` free air no interface passes.
3. **Dew point on the cold plate**. A `22 °C` plate at `35 °C` and `60 %` humidity is under the dew point of about `26 °C`. The dock needs a sealed window or a warmer set-point. `[GENERAL]`
4. **The TEC cost at `35 °C`**. The delta session needs `3.8 W` of electric power for the plate. At `25 °C` it needs `0.4 W`. Gate with the power-path and dock teams. `out/dock_tec.txt`
5. **The 5G map is lighter than the energy table**. The thermal map has `4.18 W`. The `hw/energy` outdoor video has `6.66 W` at the loads. The thermal numbers for that session are optimistic. `[TREE]`
6. **The interface loss is a bound, not a measure**. `0.10` to `0.34 W` is fixed by the brief. The physics value is `0.04` to `0.11 W`. The gap is `0.5` to `3.1 K` in the delta session. A pad measurement closes it.
7. **The BPP chain**. The model keeps `95 %` for the charger at a `5 V` input. A 3:1 charger cannot run from `5 V`. A bypass or a buck costs more heat than this model carries. `[HYPOTHESIS]`
8. **The puck support**. The puck temperature rises `5 K` at `25 W` by assumption. A real puck needs a measurement, and so does the contact of `400 W/m²K`.
9. **The eyewear model has two nodes**. It is a bound. A face-worn thermal test with a head form replaces it.
10. **Steady state only**. The run uses no PCM and no transient. Bursts of `60 s` are not in this study. `[DECISION]` out of scope

## 11 · The proposed gates

| Gate | The test | The pass condition |
|---|---|---|
| HST-T1 | delta session, battery and each host interface, in air at `25 °C`, still, `60 min` | the hottest skin point is at or under `36.2 °C`. The model expects a failure of `5.1` to `8.4 K`, so the gate records the limit |
| HST-T2 | the same session on the dock plate at `20`, `25`, `30` and `35 °C` | the hottest skin point is at or under `36.2 °C` for `60 min`. The model predicts `28` to `31 °C`. |
| HST-T3 | the Qi float test: the host feeds the load, the cell current is under `20 mA` | the heat is within `0.3 W` of the battery run on the same support |
| HST-T4 | the charge-during-session test on the dock at `25 °C`, `1 C` and Qi `25 W` | `1 C` passes at or under `36.2 °C`. `25 W` is allowed only if the skin stays at or under `36.2 °C`. The model says it fails by `1.1 K`. |
| HST-T5 | the interface loss of the `12` pads, new and worn, at `1.9` and `3.3 W` | the loss is at or under `0.10 W`. A value over `0.34 W` is a stop. |
| HST-T6 | the throttle test at `30 °C` in free air, delta session | the session holds at least `30 %` of its power with the hottest point at or under `36.2 °C` |
| HST-T7 | the cold plate set-point with the TEC at `35 °C` and `60 %` humidity | the plate holds `22 °C` with no condensation, or the set-point rises above the dew point |
| HST-T8 | the Frame on a head form, `0.8 W` plus a `0.34 W` connector loss, at `25 °C` | the contact surface and the outer surface are at or under `36.2 °C` for `60 min` |
| HST-T9 | the power-path rule: a session start with the cell current at zero | the cell charges only below `34.2 °C` and only at `0.2 C` or less during a session |
