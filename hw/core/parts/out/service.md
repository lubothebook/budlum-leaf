# The service story of the Split

Law L9: a part is renewable and carries a record. Article 11 of 2023/1542: the user removes the battery. Quadrant swap in under 3 s (F21 21.2.4). Module swap in under 10 s (FINAL/03 3.8). `[HYPOTHESIS]`

## Mass of each swap unit, by class

| Swap unit | Today g | C0 | C0R | C1 | C2 |
|---|---|---|---|---|---|
| quadrant | 39.76 | 20.83 | 20.83 | 39.76 | 39.76 |
| module | 10.87 | 9.02 | 10.02 | 10.87 | 10.87 |
| fixed | 0.84 | 0.84 | 0.84 | 0.84 | 0.84 |
| core | 0.00 | 20.85 | 19.84 | 0.00 | 0.00 |

The quadrant row counts the derived body masses. The module row counts HARDWARE/13 and the placement-only parts. The core row is what the Core holds of today's Leaf mass.

## Which parts become swappable in the Core, by class

| ID | Part | Today | C0 | C1 | C2 |
|---|---|---|---|---|---|
| BD06 | Qi2.2 sector coils x4, ferrite and Mu-metal shield, NP0 bank | quadrant | core | quadrant | quadrant |
| BD07 | U_Q x4 rectifier and 3:1 charger | quadrant | core | quadrant | quadrant |
| BD08 | hermetic micro cells, 9.25 x 9.25 x 0.90 mm, 30 um can | quadrant | core | quadrant | quadrant |
| BD09 | TCM protection IC, fuse and balance channel per cell | quadrant | core | quadrant | quadrant |
| BD23 | Qi alignment magnets (16 N52 in tile corners) and QI2_AC_RING seam leaves | quadrant | core | quadrant | quadrant |
| M16 | U1 TCON and local compositor (safe-screen ROM inside) | module | core | module | module |
| M17 | U2A Wi-Fi 7 and BT 6.0 combo | module | core | module | module |
| M18 | U2B 60 GHz and UWB | module | core | module | module |
| M19 | U5 5G standalone modem with RF front end and eSIM | module | core | module | module |
| M20 | U6 slice decoder, camera encoder block and 16 MB frame store | module | core | module | module |
| M21 | U7 secure element: wallet keys, validator set, receipts | module | core | module | module |
| M27 | cell multiplexer, 4 x 32 channels | module | core | module | module |
| M29 | B cell, 0.14 Wh, 20 x 8 x 1.50 mm | module | core | module | module |
| M32 | shield cans, nickel silver, over U2A, U2B, U5 | module | core | module | module |
| X03 | Y1 TCXO | module | core | module | module |

Parts not listed stay in the swap unit of the first column at every class.

## What the record law gives the Core

| Question | Answer |
|---|---|
| who holds the record of a moved part | the Core part itself, in its own secure element, as law L9 asks |
| who holds the record of the Skin | the Skin identity chip N01, which verifies and holds the part lines of the quadrants and the tile hubs |
| what a Core part swap needs from the Skin | nothing: the Skin sees a new Core certificate and pairs again by the chain record |
| the Article 11 unit at C0 | the Core cells, readily removable in the Core. The Skin quadrants keep only 20 Buffer cells |
| the Article 11 unit at C1 and C2 | unchanged: the quadrant, with 32 cells, TCMs and U_Q |
| the module swap at C0 | the module shrinks to the ring stub. Radio, decoder and wallet upgrades leave the module |
| what stays fixed in the Leaf at every class | the hinges, caps, emitters, seat, bar antennas and the touch grid. A failure there is a quadrant or a Leaf swap |
