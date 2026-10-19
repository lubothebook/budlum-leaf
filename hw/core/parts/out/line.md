# The parts on the line, under the rule of necessity

Rule: Ayaz, 2026-10-19. A part stays in the B module only if physics forces it at the distance class. The body keeps the emitters and the tile drivers. Everything else is Core.

A part is on the line when the rule disagrees with a law, a gate or a physical fact. It is also on the line when no part list can split it. `[HYPOTHESIS]`

| No. | The group | What the rule says | What the table holds | Why |
|---|---|---|---|---|
| L1 | energy at C1 and C2 | The ruling lists no energy part, so the rule says Core. | Cells, TCMs, mux, B cell, coil and rectifier stay at C1 and C2. They move at C0. | Physics: watts do not cross 30 m or a kilometre. Brief section 8 item 4 says energy is local at C2. |
| L2 | the Buffer store at C0 | All 128 cells are Core at C0. | The table sends all 128 cells to the Core. The sensitivity keeps 20 cells: 2.4 g with their TCMs and the mux, about 12 USD at 1 M. | Law, not physics: the Host Life Law (Part 22, condition 4) asks for a bridge store at a host swap. Without it the Skin goes dark for 3 s. |
| L3 | the radio SiPs at C0 | The antennas and the radio front end stay. The baseband is Core. | U2A, U2B and U5 hold front end and baseband in one SiP. C0 moves them whole (upper bound). C0R keeps them whole (lower bound). | Physics keeps the front end at the antenna. No part list splits the SiP, so the truth lies between C0 and C0R. |
| L4 | the safe-screen ROM | The compositor U1 is Core at C0, and its ROM with it. | A ROM-only die N02 stays on the Skin. | Law, not physics: every fault ends in a visible state (FINAL/08 8.2). Without it a link loss gives a dark Skin. |
| L5 | identity | A hardened identity element stays at C1 and C2. | U7 stays at C1 and C2. At C0 the small chip N01 holds the identity and the part records, and the wallet moves to the Core. | The identity must stay (BRIEF section 4 item 4). The dead-pad law needs a verifier on the Skin. |
| L6 | touch front end, hinge and seam sensors, tile hubs | The body keeps the emitters and the tile drivers only. | The touch front ends and the sensors stay. The tile hubs and seat controllers stay as tile drivers and link end. | Physics: an electrode or a strain sensor is read at the tile, because a long trace adds noise and delay. Scan logic can move. |
| L7 | the 36.2 C hardware cut-off | Not an emitter or a tile driver, so Core. | The NTCs and the comparator stay in the body. | Physics and law: a surface temperature is measured at the surface, and the cut-off acts with the link lost (ENR-16). |
| L8 | the IMU | Not in the list of the ruling, so Core. | U8 stays in the module. | Physics: it senses the seat, the face and the grip of the Leaf. A Core IMU senses the Core. |
| L9 | audio codec, power chip, boot NOR, rail parts | Not in the list, so Core. | U3, U4, U9, U4B and the rail inductors stay in the module. | Physics: the DAC and amplifier sit at the speaker and jack, and the camera, panel and flash rails are local. U4 also answers the dead-pad law. U9 holds the firmware of the stayers. |
| L10 | heat parts of the camera | Not in the list, so Core. | The spreader, phase change buffer, Cu-graphite shield and graphite shield stay. | Physics: the camera and the emitters make heat where they are. The buffer was sized for the camera sentinel, so it can shrink after the move (candidate K-1). |
| L11 | the seat interface and the dead-pad law | Not an emitter or a tile driver, so Core. | The seat fields, seam leaves, 12 bar leaves and the ring serdes stay. | Law and physics: the 12 leaves are the only wired seat and the tether interface at C0. The dead-pad responder must sit at the pads (ENR-19). |
| L12 | the camera encoder and the uplink | Sentinel work is processing, so Core. | At C1 and C2 the encoder in U6 stays. At C0 it moves if a display pair is switched to uplink. | Physics: the uplink under SAR is weak, and 12.5 MP at 30 fps needs 3.75 Gbit/s. Only compressed video crosses a room or a kilometre. |

## The parts of each line item

| No. | Parts |
|---|---|
| L1 | BD06, BD07, BD08, BD09, BD23, M27, M29 |
| L2 | BD08, BD09 |
| L3 | M17, M18, M19, M32, X03, M25 |
| L4 | N02, M16 |
| L5 | M21, N01 |
| L6 | BD18, BD19, BD04, BD20 |
| L7 | BD17 |
| L8 | M22 |
| L9 | M23, X01, X05, X02 |
| L10 | M31, M10, BD16 |
| L11 | BD14, BD15, M04, N03 |
| L12 | M20 |
