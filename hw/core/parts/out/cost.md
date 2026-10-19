# The cost share of each group and what leaves the Leaf

Source: `program/budget.py`, base case, read only. USD per Leaf, no margin. `[HYPOTHESIS]` of the Program Office. MISSING groups carry a range of this seat.

## Volume 1,000,000 per year, unit cost 1575 USD

| Group | Source | USD | Share | Leaves C0 | Leaves C0R | Leaves C1 | Leaves C2 |
|---|---|---|---|---|---|---|---|
| micro-LED tiles x 128 | budget.py | 1204.71 | 76.5 % | 0.00 | 0.00 | 0.00 | 0.00 |
| micro cells x 128 | budget.py | 66.00 | 4.2 % | 66.00 | 66.00 | 0.00 | 0.00 |
| tile mechanics: PC caps, hinges, skin, seats, magnets, 128 t | budget.py | 32.00 | 2.0 % | 0.00 | 0.00 | 0.00 | 0.00 |
| TCM protection IC x 128 | budget.py | 9.60 | 0.6 % | 9.60 | 9.60 | 0.00 | 0.00 |
| Qi2.2 sector coils, shield, rectifier | budget.py | 5.00 | 0.3 % | 4.55 | 4.55 | 0.00 | 0.00 |
| touch grid, AgNW, on the caps | budget.py | 6.00 | 0.4 % | 0.00 | 0.00 | 0.00 | 0.00 |
| U1 and U6 ASICs with 16 MB store | budget.py | 20.00 | 1.3 % | 20.00 | 20.00 | 0.00 | 0.00 |
| U5 5G modem SiP with RF front end and eSIM | budget.py | 42.00 | 2.7 % | 42.00 | 0.00 | 0.00 | 0.00 |
| U2A Wi-Fi 7 and BT 6.0, U2B 60 GHz and UWB | budget.py | 12.00 | 0.8 % | 12.00 | 0.00 | 0.00 | 0.00 |
| U7 secure element, U8 IMU, U3 audio, U4 power, NOR | budget.py | 7.50 | 0.5 % | 2.65 | 2.65 | 0.00 | 0.00 |
| 50 MP camera column with sapphire L1 | budget.py | 18.00 | 1.1 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B module mechanics: LCP shells, LDS, windows, jack, speaker, | budget.py | 17.00 | 1.1 % | 0.00 | 0.00 | 0.00 | 0.00 |
| rear round AMOLED | budget.py | 5.00 | 0.3 % | 0.00 | 0.00 | 0.00 | 0.00 |
| ring PCBA, 8-layer HDI, assembly | budget.py | 8.50 | 0.5 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B cell 0.14 Wh | budget.py | 1.30 | 0.1 % | 1.30 | 1.30 | 0.00 | 0.00 |
| tile hub die x 128 (not in budget.py) | MISSING, range 5.0 to 19.0 | 10.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ocular NTCs, hinge sensors, seam strips, seat controllers (not in budg | MISSING, range 3.0 to 12.0 | 6.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ring small parts: flash, tuners, mux, magnets, gaskets, spreader, cans | MISSING, range 3.0 to 10.0 | 6.00 | n/a | 1.60 | 0.69 | 0.00 | 0.00 |
| cellular royalties | budget.py | 60.58 | 3.8 % | 60.58 | 0.00 | 0.00 | 0.00 |

The royalty row moves only if the royalty follows the modem. That is a legal question (candidate K-3 and gate HC-A10).

## Volume 100,000 per year, unit cost 3949 USD

| Group | Source | USD | Share | Leaves C0 | Leaves C0R | Leaves C1 | Leaves C2 |
|---|---|---|---|---|---|---|---|
| micro-LED tiles x 128 | budget.py | 3218.29 | 81.5 % | 0.00 | 0.00 | 0.00 | 0.00 |
| micro cells x 128 | budget.py | 139.20 | 3.5 % | 139.20 | 139.20 | 0.00 | 0.00 |
| tile mechanics: PC caps, hinges, skin, seats, magnets, 128 t | budget.py | 60.00 | 1.5 % | 0.00 | 0.00 | 0.00 | 0.00 |
| TCM protection IC x 128 | budget.py | 19.00 | 0.5 % | 19.00 | 19.00 | 0.00 | 0.00 |
| Qi2.2 sector coils, shield, rectifier | budget.py | 9.00 | 0.2 % | 8.18 | 8.18 | 0.00 | 0.00 |
| touch grid, AgNW, on the caps | budget.py | 12.00 | 0.3 % | 0.00 | 0.00 | 0.00 | 0.00 |
| U1 and U6 ASICs with 16 MB store | budget.py | 45.00 | 1.1 % | 45.00 | 45.00 | 0.00 | 0.00 |
| U5 5G modem SiP with RF front end and eSIM | budget.py | 60.00 | 1.5 % | 60.00 | 0.00 | 0.00 | 0.00 |
| U2A Wi-Fi 7 and BT 6.0, U2B 60 GHz and UWB | budget.py | 18.00 | 0.5 % | 18.00 | 0.00 | 0.00 | 0.00 |
| U7 secure element, U8 IMU, U3 audio, U4 power, NOR | budget.py | 12.00 | 0.3 % | 4.24 | 4.24 | 0.00 | 0.00 |
| 50 MP camera column with sapphire L1 | budget.py | 30.00 | 0.8 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B module mechanics: LCP shells, LDS, windows, jack, speaker, | budget.py | 30.00 | 0.8 % | 0.00 | 0.00 | 0.00 | 0.00 |
| rear round AMOLED | budget.py | 8.00 | 0.2 % | 0.00 | 0.00 | 0.00 | 0.00 |
| ring PCBA, 8-layer HDI, assembly | budget.py | 14.00 | 0.4 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B cell 0.14 Wh | budget.py | 2.20 | 0.1 % | 2.20 | 2.20 | 0.00 | 0.00 |
| tile hub die x 128 (not in budget.py) | MISSING, range 7.0 to 26.0 | 14.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ocular NTCs, hinge sensors, seam strips, seat controllers (not in budg | MISSING, range 5.0 to 20.0 | 10.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ring small parts: flash, tuners, mux, magnets, gaskets, spreader, cans | MISSING, range 5.0 to 15.0 | 9.00 | n/a | 2.40 | 1.03 | 0.00 | 0.00 |
| cellular royalties | budget.py | 151.87 | 3.8 % | 151.87 | 0.00 | 0.00 | 0.00 |

The royalty row moves only if the royalty follows the modem. That is a legal question (candidate K-3 and gate HC-A10).

## Volume 5,000,000 per year, unit cost 803 USD

| Group | Source | USD | Share | Leaves C0 | Leaves C0R | Leaves C1 | Leaves C2 |
|---|---|---|---|---|---|---|---|
| micro-LED tiles x 128 | budget.py | 553.74 | 68.9 % | 0.00 | 0.00 | 0.00 | 0.00 |
| micro cells x 128 | budget.py | 41.60 | 5.2 % | 41.60 | 41.60 | 0.00 | 0.00 |
| tile mechanics: PC caps, hinges, skin, seats, magnets, 128 t | budget.py | 22.00 | 2.7 % | 0.00 | 0.00 | 0.00 | 0.00 |
| TCM protection IC x 128 | budget.py | 6.40 | 0.8 % | 6.40 | 6.40 | 0.00 | 0.00 |
| Qi2.2 sector coils, shield, rectifier | budget.py | 3.50 | 0.4 % | 3.18 | 3.18 | 0.00 | 0.00 |
| touch grid, AgNW, on the caps | budget.py | 4.50 | 0.6 % | 0.00 | 0.00 | 0.00 | 0.00 |
| U1 and U6 ASICs with 16 MB store | budget.py | 13.00 | 1.6 % | 13.00 | 13.00 | 0.00 | 0.00 |
| U5 5G modem SiP with RF front end and eSIM | budget.py | 34.00 | 4.2 % | 34.00 | 0.00 | 0.00 | 0.00 |
| U2A Wi-Fi 7 and BT 6.0, U2B 60 GHz and UWB | budget.py | 9.50 | 1.2 % | 9.50 | 0.00 | 0.00 | 0.00 |
| U7 secure element, U8 IMU, U3 audio, U4 power, NOR | budget.py | 5.80 | 0.7 % | 2.05 | 2.05 | 0.00 | 0.00 |
| 50 MP camera column with sapphire L1 | budget.py | 14.00 | 1.7 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B module mechanics: LCP shells, LDS, windows, jack, speaker, | budget.py | 13.00 | 1.6 % | 0.00 | 0.00 | 0.00 | 0.00 |
| rear round AMOLED | budget.py | 4.00 | 0.5 % | 0.00 | 0.00 | 0.00 | 0.00 |
| ring PCBA, 8-layer HDI, assembly | budget.py | 6.50 | 0.8 % | 0.00 | 0.00 | 0.00 | 0.00 |
| B cell 0.14 Wh | budget.py | 1.00 | 0.1 % | 1.00 | 1.00 | 0.00 | 0.00 |
| tile hub die x 128 (not in budget.py) | MISSING, range 3.5 to 13.0 | 7.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ocular NTCs, hinge sensors, seam strips, seat controllers (not in budg | MISSING, range 2.0 to 8.0 | 4.00 | n/a | 0.00 | 0.00 | 0.00 | 0.00 |
| ring small parts: flash, tuners, mux, magnets, gaskets, spreader, cans | MISSING, range 2.2 to 7.5 | 4.50 | n/a | 1.20 | 0.51 | 0.00 | 0.00 |
| cellular royalties | budget.py | 30.90 | 3.8 % | 30.90 | 0.00 | 0.00 | 0.00 |

The royalty row moves only if the royalty follows the modem. That is a legal question (candidate K-3 and gate HC-A10).

