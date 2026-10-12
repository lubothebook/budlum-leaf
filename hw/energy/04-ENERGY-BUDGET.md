# BUDLUM LEAF · ENERGY · 04 · THE ENERGY BUDGET AND THE RUN TIMES

**Revision L.6.0 · 2026-10-12 · Energy and BMS team**. Script: `budget/runtime.py`. Output: `out/budget.txt`, `out/budget.json`. Gates ENR-22, ENR-24, SW-20.

## 1 · The method

1. Split each use case into nine load domains. Three live in the body, six in the ring.
2. Divide the body loads by `0.92` for the tile drivers. Divide the ring loads by `0.90` for U4. `[HYPOTHESIS]`
3. Add the `I²R` loss of the pack, the bus and the bar, `50 mΩ` in all. `[TREE]` `pack/network.py`
4. Use `96 %` of the nominal energy. The network solve leaves about `4 %` above the `3.40 V` seat floor. `[TREE]`
5. Add the B cell at `96 %` through the U4 path at `95 %`.

**The claim rule of FINAL/17 Section 17.13 holds**. Each run time names the brightness, the picture level, the session and the radio. `[DECISION]`

## 2 · The stores

| The store | Nominal | The tag |
|---|---|---|
| body, G at `600 Wh/L`, the target | `5.90 Wh` | `[TREE]` |
| body, G at the model `694 Wh/L` | `6.83 Wh` | `[TREE]` |
| body, S at `750 Wh/L`, the target | `7.38 Wh` | `[TREE]` |
| body, S at the model `850 Wh/L` | `8.36 Wh` | `[TREE]` |
| B cell, `20.0 x 8.0 x 1.50 mm` at `600 Wh/L` | `0.144 Wh` | `[TREE]` |

## 3 · The budget per use case

Loads in watts. "Battery" is the power drawn from the cells. Hours run on the body plus the B cell.

| The use case | Load source | Body | Ring | Battery | G `600` | G model | S `750` | S model |
|---|---|---|---|---|---|---|---|---|
| wallet standby, screen off, Wi-Fi target wake time | `[HYPOTHESIS]` | `0.000` | `0.055` | `0.061` | `94.9 h` | `109.4 h` | `118.1 h` | `133.5 h` |
| rear display glance, body dark | `[HYPOTHESIS]` | `0.000` | `0.105` | `0.117` | `49.7 h` | `57.3 h` | `61.8 h` | `69.9 h` |
| safe screen, no link | FINAL/04 4.6 | `0.120` | `0.080` | `0.219` | `26.4 h` | `30.5 h` | `32.9 h` | `37.2 h` |
| static page at `10 Hz` | FINAL/04 4.6 | `0.170` | `0.180` | `0.385` | `15.1 h` | `17.4 h` | `18.7 h` | `21.2 h` |
| music on the `3.5 mm` jack, screen off | `[HYPOTHESIS]` | `0.000` | `0.230` | `0.256` | `22.7 h` | `26.1 h` | `28.2 h` | `31.9 h` |
| voice call on 5G, screen off | `[HYPOTHESIS]` | `0.000` | `0.730` | `0.813` | `7.1 h` | `8.2 h` | `8.9 h` | `10.0 h` |
| delta session, `250 nits`, `35 %` picture level, Wi-Fi | FINAL/04 4.6 | `0.800` | `1.220` | `2.242` | `2.6 h` | `3.0 h` | `3.2 h` | `3.6 h` |
| delta session at `41 %` stretch | `[HYPOTHESIS]` | `0.810` | `1.270` | `2.310` | `2.5 h` | `2.9 h` | `3.1 h` | `3.5 h` |
| `50 MP` camera, viewfinder and upload | `[HYPOTHESIS]` | `0.800` | `2.170` | `3.318` | `1.8 h` | `2.0 h` | `2.2 h` | `2.5 h` |
| video session, Wi-Fi | FINAL/04 4.6 | `1.350` | `1.920` | `3.646` | `1.6 h` | `1.8 h` | `2.0 h` | `2.2 h` |
| video outdoors, `800 nits`, `70 %` picture level, 5G | FINAL/17 17.13 and `[HYPOTHESIS]` | `4.240` | `2.420` | `7.482` | `0.8 h` | `0.9 h` | `1.0 h` | `1.1 h` |

All hours are `[TREE]` outputs of `budget/runtime.py`.

### 3.1 The domain split behind the table

| The use case | Display | Address | Hinge | Hub | Radio | Authority | Camera | Audio | Rear |
|---|---|---|---|---|---|---|---|---|---|
| wallet standby | `0` | `0` | `0` | `0.005` | `0.030` | `0.020` | `0` | `0` | `0` |
| delta session | `0.60` | `0.20` | `0` | `0.70` | `0.40` | `0.12` | `0` | `0` | `0` |
| `50 MP` camera | `0.60` | `0.20` | `0` | `0.70` | `1.00` | `0.12` | `0.35` | `0` | `0` |
| video, Wi-Fi | `1.10` | `0.25` | `0` | `1.20` | `0.60` | `0.12` | `0` | `0` | `0` |
| video outdoors, 5G | `3.84` | `0.40` | `0` | `1.20` | `1.10` | `0.12` | `0` | `0` | `0` |

The full split for every row lives in `budget/runtime.py`, list `CASES`.

## 4 · The check against FINAL/21

FINAL/21 Section 21.2.5 states: a video session of `2-3 W` runs `1.9-3.7 h` on the body and the B cell. `[HYPOTHESIS]`

| Load at the loads | Battery power | G `600` | G model | S `750` | S model |
|---|---|---|---|---|---|
| `2.0 W` | `2.21 W` | `2.62 h` | `3.02 h` | `3.26 h` | `3.68 h` |
| `3.0 W` | `3.33 W` | `1.74 h` | `2.01 h` | `2.16 h` | `2.45 h` |

**The reading**. FINAL/21 divided the energy by the load with no conversion loss. With the `0.90-0.92` converters, the band at the targets is `1.74-3.26 h`. The S cell at its model density reaches `3.68 h` at `2 W`. `[TREE]`

**The path to the full `3.7 h` band, with no target lowered**.

1. Build the S variant to its model density of `850 Wh/L`. That alone gives `3.68 h` at `2 W`.
2. Raise the tile drivers from `0.92` to `0.95`. Feed the micro-LED sinks straight from VBUS, with no buck.
3. Raise U4 from `0.90` to `0.93`. Use a `0.75 V` core buck with a light-load mode.
4. Together these give `3.80 h` at `2 W`, split `0.8 W` body and `1.2 W` ring. Gate ENR-22. `[TREE]` `budget/runtime.py`

## 5 · The charge plan, Qi2.2 `25 W`

| The store | To `50 %` | To `70 %` | To full, CV tail | Mean rate | The tag |
|---|---|---|---|---|---|
| G at `600 Wh/L` | `8.7 min` | `12.2 min` | about `27 min` | `2.8 C`, `3.5 C` peak | `[TREE]` |
| S at `750 Wh/L` | `10.9 min` | `15.2 min` | about `34 min` | `2.3 C`, `2.9 C` peak | `[TREE]` |

**The rules of the charge**. `[DECISION]` this team, gate ENR-24.

1. The receiver takes `25 W`. That is the Qi2.2 power profile, and it stays.
2. The full `25 W` runs from `0` to `50 %` SOC above `25 °C` cell temperature.
3. Below `25 °C`, U_Q holds the G cell at `1.5 C` to avoid lithium plating.
4. The skin limit of `36.2 °C` overrides every rate. A cooled pad keeps `25 W` longer.
5. Above `70 %` the charge goes to constant voltage.
6. The body charges at rest only, every hinge at `θ = 0`. FINAL/21 21.2.6.

**The heat of a full-rate charge** is `5.8 W` in the body. The coil and converters make `4.6 W`, and the cells and the bus make `1.2 W`. That is the real limit of a `2.00 mm` body. Gate ENR-24 measures it. `[TREE]`

## 6 · The open items of the budget

1. The 5G radio powers of `0.55-1.10 W` need the radio team's numbers.
2. The `50 MP` upload path needs an encoder in the ring. No such block is in `HARDWARE/13`. That is a question for the B team.
3. The micro-LED anchor of `0.60 W` at `250 nits` comes from the OLED-era gate DSP-5. Gate DSP-19 must measure the micro-LED tile.
