# The collisions of the Split with the designs and the gates

Each row names the gate or section, what collides, and the way out in each distance class. `[HYPOTHESIS]` for every resolution.

## X1. the 50 MP camera column and the Core taking camera processing

| Item | Text |
|---|---|
| gate or section | CAM-21, MON-23, F21 21.3.5, M09 sections 3.1 and 3.2, CAM-3 |
| the collision | The lens and sensor must stay. The sentinel (remosaic, compression, encode) needs an uplink. The leaves hold a 0.4 Gbit/s back channel, and 12.5 MP at 30 fps needs 3.75 Gbit/s. |
| resolve at C0 | Zone 1 stays. Move the sentinel only if a display pair is switched to camera uplink in capture mode (HC-A5), or keep the encoder in U6. |
| resolve at C1 | No change. The sentinel stays, because the uplink carries 30 to 80 Mbit/s of compressed video and 12 to 30 MB stills. |
| resolve at C2 | No change. A weak uplink under SAR forbids raw video. |
| parts | M11, M20, N03 |

## X2. the 4.00 mm module is set by the camera column

| Item | Text |
|---|---|
| gate or section | F21 21.3.5 (3.90 mm column), MON-23 (4.00 +- 0.05 mm), CAM-21 |
| the collision | Moving silicon frees area and volume in the ring. It does not thin the module, because the column stands 3.90 mm. |
| resolve at C0 | Module stays 4.00 mm. Freed volume is room, not thickness. |
| resolve at C1 | Nothing leaves the ring. Module stays 4.00 mm. |
| resolve at C2 | Nothing leaves the ring. Module stays 4.00 mm. |
| parts | M11, M06 |

## X3. camera state declaration and hardware indicator

| Item | Text |
|---|---|
| gate or section | M09 section 5 item 2 (RG-5), CAM-5 |
| the collision | A hardware indicator and a signed sensor declaration stop software from hiding camera use. U7 signs today. The Skin signs nothing. |
| resolve at C0 | Wire the indicator to the sensor supply rail on the Skin. The Core signs the declaration and names the Skin identity (HC-A5). |
| resolve at C1 | No change. U7 stays on the Leaf. |
| resolve at C2 | No change. |
| parts | M11, M21, N01 |

## X4. the 12 gold leaves and the one wired seat

| Item | Text |
|---|---|
| gate or section | MON-23, MON-18, MON-21, F21 21.3.2 and 21.3.3, E03 section 2 |
| the collision | The leaves carry two display pairs, a 0.4 Gbit/s back channel, VBUS, VHV, sideband and ground. The ring slides on a stretching face and a cable pulls on the bar. |
| resolve at C0 | A Core plug takes the leaves in place of the ring chips, or a port-part clip-on takes another edge. Test a 30 N pull on a seat (HC-A4). |
| resolve at C1 | No change. The leaves carry the ring only. |
| resolve at C2 | No change. |
| parts | M04, BD14, PP01, PP03, N03 |

## X5. the dead-pad law

| Item | Text |
|---|---|
| gate or section | ENR-19, MON-16, FS state PAD_AUTH, RL-7, RL-14 |
| the collision | Every pad holds 0 V until a 3 ms challenge. The challenger verifies a signed answer. At C0 the answer comes from the Core, and the Skin holds no signing key. |
| resolve at C0 | The Skin identity chip verifies the Core certificate in 3 ms. First break opens the FET in under 0.8 ms (HC-A4). |
| resolve at C1 | Not used. No pad touches a Core. The pairing key of the trust seat replaces the challenge. |
| resolve at C2 | Not used. The law holds on the bar and the port part as designed. |
| parts | BD14, BD15, M04, M21, M23, N01 |

## X6. the Zero CPU definition

| Item | Text |
|---|---|
| gate or section | F21 21.5.1, F21 21.4.2, FZ section 4, naming law of BR section 7 |
| the collision | Part 21 gives the Leaf no general-purpose processor and no operating system. The Core holds the validator role, which needs both. |
| resolve at C0 | Relocated silicon stays fixed-function. Claim Zero CPU for the Skin and the relocated block. Name the validator role as a separate node (HC-A10). |
| resolve at C1 | Same. A room validator is a node, as the dock validator is today. |
| resolve at C2 | No change. The Core is a validator, not part of the Leaf. |
| parts | M16, M20, DK05 |

## X7. the local compositor, the stretch warp and the Part 21 interaction budget

| Item | Text |
|---|---|
| gate or section | F21 21.5.6, SW-21, SW-23, DSP-17 |
| the collision | U1 moves cursor, scroll, glyph echo and the per-tile warp in under 10 ms. SW-23 needs a predicted action with the network cut. |
| resolve at C0 | The Core runs the compositor. The tether round trip is well under 1 ms. SW-23 cuts the Core uplink, not the tether. |
| resolve at C1 | Compositor stays on the Leaf, as the ruling of Ayaz says. |
| resolve at C2 | No change. The far round trip is 80 ms, so the Leaf compositor and speculative frames are essential. |
| parts | M16 |

## X8. the stream check and the wallet on the Leaf

| Item | Text |
|---|---|
| gate or section | F21 21.5.4, F21 21.5.8, SW-22, BR section 4 item 4 |
| the collision | U7 accepts a stream only from an active validator key. With U7 on the Core, the Skin trusts the paired Core key and nothing else. |
| resolve at C0 | SW-22 moves to the Core. The Skin refuses an unpaired Core key. The rogue Skin reads every pixel (HC-A11). |
| resolve at C1 | No change. U7 stays as the hardened identity element. |
| resolve at C2 | No change. U7 stays. |
| parts | M21, M20, N01 |

## X9. the safe-screen ROM lives in U1

| Item | Text |
|---|---|
| gate or section | FS (U1 ROM path), FINAL/08 section 8.2 safe-screen law, I2 (60 ms) |
| the collision | Every fault ends in a visible state. If U1 leaves and the link fails, the Skin is dark and the law is broken. |
| resolve at C0 | Keep a ROM-only safe-screen die on the Skin (N02). Show it within 60 ms of a link loss (HC-A3). |
| resolve at C1 | No change. U1 stays. |
| resolve at C2 | No change. |
| parts | M16, N02 |

## X10. the seam loop and the 3 ms recalibration after a swap

| Item | Text |
|---|---|
| gate or section | F21 21.2.4 items 4 and 5, MEC-40, DSP-17 |
| the collision | U1 shifts the image in 3.125 um steps and recalibrates in the 3 ms window. The calibration of 32 tiles is about 154 KB, so the back channel needs 3.1 ms. |
| resolve at C0 | Read the calibration over a pair (0.2 ms), or keep the closed loop in the tile hubs (HC-A6). |
| resolve at C1 | No change. U1 stays. |
| resolve at C2 | No change. |
| parts | M16, BD19, BD04 |

## X11. frame store, decoder and compositor at C1 and C2

| Item | Text |
|---|---|
| gate or section | F21 21.5.1, BR section 8 item 2, DSC link of DI |
| the collision | Slices of tens to 150 Mbit/s cross a room. The raw stream of 6 to 12 Gbit/s needs the 60 GHz array, and Wi-Fi 7 2 x 2 tops out at 5.76 Gbit/s PHY. |
| resolve at C0 | Not needed. The tether carries 13.43 Gbit/s over two pairs. |
| resolve at C1 | U6, the frame store and the compositor stay. The ruling of Ayaz keeps them at C1 and C2. HC-A9 measures the link and confirms the necessity. |
| resolve at C2 | U6 stays. No raw stream crosses a kilometre. |
| parts | M20, M16 |

## X12. the radios and the antennas are one design

| Item | Text |
|---|---|
| gate or section | RF-9, RF-17, RF-19, RF-22, RF-23, F21 21.4 |
| the collision | A1 to A4 are tuned to U2A and U2B with the tuners. A SiP holds the front end and the baseband together. Ayaz keeps the antennas and the 5G modem on the Leaf. |
| resolve at C0 | The rule keeps the front end and moves the baseband, which no part list splits. C0 moves the SiPs whole. C0R keeps them. The truth lies between. |
| resolve at C1 | All three radios stay. They are the Leaf end of the link. |
| resolve at C2 | All three radios stay. |
| parts | M17, M18, M19, M25 |

## X13. dormant antennas and a Leaf that cannot roam at C0

| Item | Text |
|---|---|
| gate or section | BR section 8, F21 21.4.1, RF-21 to RF-23 |
| the collision | If the radios move, the bar antennas and the corner flex lines end in no radio. A Skin off its tether is then dark. An RF cable of 2 m loses many dB at 60 GHz. |
| resolve at C0 | Choose C0R (radios stay), or accept a tether-only Skin. The choice is for Ayaz (candidate K-3). |
| resolve at C1 | No change. The antennas feed the radios on the Leaf. |
| resolve at C2 | No change. |
| parts | M01, M02, M03, M05, M17, M18, M19, M24, M25, M32, X03 |

## X14. Qi2.2 on a Skin with no cell behind it

| Item | Text |
|---|---|
| gate or section | F21 21.2.6, ENR-24, F22 D-10 |
| the collision | At C0 the tether carries power, so the rule omits the coil, the rectifier and the alignment magnets. A Skin that must charge off its tether needs them. |
| resolve at C0 | The Skin omits the Qi path (3.9 g). The Core charges its own cells. Candidate K-2 puts it back. |
| resolve at C1 | No change. Energy is local, so the coil stays. |
| resolve at C2 | No change. |
| parts | BD06, BD07, BD23 |

## X15. Article 11, the removable quadrant and the Buffer rule

| Item | Text |
|---|---|
| gate or section | FINAL/17 17.6, F22 22.12, E06 section 2, ENR-13, ENR-22 |
| the collision | The quadrant is the user battery today: 32 cells, TCMs, U_Q and bonded tiles. With all cells in the Core, Article 11 applies to the Core battery. |
| resolve at C0 | The Core cells need tool-free removal. The Skin quadrant holds no cell and is display only (HC-A6). |
| resolve at C1 | No change. Cells stay in the quadrants. |
| resolve at C2 | No change. |
| parts | BD08, BD09, M27, DK04 |

## X16. the legal class of the Leaf

| Item | Text |
|---|---|
| gate or section | E06 section 1 (2023/1670 class with modem and voice path) |
| the collision | The Leaf sits in a regulation class because it has a 5G modem and a voice path. A Skin with no modem can fall outside it, and the Core can enter it. |
| resolve at C0 | Ask a lawyer which box is the product. Hypothesis only. |
| resolve at C1 | No change. |
| resolve at C2 | No change. |
| parts | M19, BD08 |

## X17. the mass figures of the catalogues

| Item | Text |
|---|---|
| gate or section | FINAL/03 3.1, MEC-2, H03, H17, F21 21.1 |
| the collision | The stated 68 g body counts 34.4 g of withdrawn LLZO cells. The L.6.0 body has no mass list. The 88 g total counts a withdrawn 20 g module. |
| resolve at C0 | State the mass of Skin, Core and tether as three configurations (the mass rule of FINAL/03 3.1). |
| resolve at C1 | State Leaf and Core mass as two configurations. |
| resolve at C2 | No change. |
| parts | W01, W06, BD08 |

## X18. the rear display and wallet standby with no Core

| Item | Text |
|---|---|
| gate or section | E04 section 3 (rear glance 75 min, wallet standby 143 min on the B cell), E05 section 1.3 rule 5 |
| the collision | At C0 the rear glance, the clock and the wallet standby need the Core, because U1, U7 and the B cell leave. |
| resolve at C0 | The Skin alone shows the safe screen only. State it in the product text. |
| resolve at C1 | No change. The B cell, U1 and U7 stay. |
| resolve at C2 | No change. |
| parts | M09, M21, M29 |

## X19. the Host Life Law and a Skin with no store

| Item | Text |
|---|---|
| gate or section | F22 22.2 condition 4, F22 D-9, HST-1, HST-2, HST-5 |
| the collision | Part 22 asks for a bridge store, so a host swap loses no session. The rule of necessity sends all cells to the Core at C0. |
| resolve at C0 | Line item L2. Keep 20 Buffer cells (2.4 g) or accept a dark Skin for 3 s at a host swap. Ayaz decides (K-7). |
| resolve at C1 | No change. The cells stay. |
| resolve at C2 | No change. The cells stay. |
| parts | BD08, BD09, M29 |

