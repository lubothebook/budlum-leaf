# BUDLUM LEAF · HOST POWER · STUDY · 01 · THE PRIOR ART

**Revision L.6.1 (proposed) · 2026-10-19 · Study team**. This is a prior art survey by web search. It is not a patent search and not legal advice. Gate HPS-1 asks for the professional search.

## 1 · The verdict first

**Ayaz asked if a device that works as long as its host works is a world first. The honest answer is no.** The parts of the Host Life Law that exist today are many. A full combination matching the Leaf was not found in this survey. That is a weaker statement than "first". `[HYPOTHESIS]`

| The part of the law | Is it new? | The closest prior art |
|---|---|---|
| a display that has no cell and lives on a host cable | no | XREAL Air 2, row 1 |
| a secure wallet with a screen and no cell | no | Ledger Nano S, row 15 |
| a full computer that runs with the cell removed, on a dock or a vehicle supply | no | Samsung No Battery Mode, row 8 |
| a capacitor that ends a session cleanly when power drops | no | dash cams, row 12 |
| a small cell that bridges the swap of a large cell | no | patent WO2013054164A2, row 14 |
| a heat reason for running on the host and not on the cell | no | Samsung No Battery Mode and bypass charging, rows 8 and 9 |

## 2 · How to read the status column

| The status | The meaning |
|---|---|
| Opened | the study team read the page with WebFetch on 2026-10-19. A `[PUBLICATION]` tag is allowed |
| Search | the fact came from a search result summary only. The page was not read. It is a `[HYPOTHESIS]` until opened |
| Recall | the fact comes from memory. It is a `[HYPOTHESIS]` |

**Several pages refused or failed to load.** They include Zebra docs, Plugable, the EUR-Lex text and the Commission notice. Rows that rest on them say Search.

## 3 · The table

| No. | Product or class | What it does, and the power path | When the host goes away | Source | Status |
|---|---|---|---|---|---|
| 1 | XREAL Air 2, tethered glasses | no cell, no processor. Power and picture pass through one cable. GSMArena measured 1.5 to 1.8 W static and 1.5 to 1.6 W in video | dark. The cable is the only source of power and picture | https://www.gsmarena.com/xreal_air_2_review-news-60451.php | Opened |
| 2 | Viture adapter for XR glasses | passes up to 45 W so the host charges while the glasses run. The page does not state that the glasses have no cell | not stated on the page | https://www.viture.com/product/usb-c-to-glasses-and-charging-adapter | Opened |
| 3 | Rokid Max glasses and Rokid Station | glasses run from USB-C. The Station is a box with a 5 000 mAh cell, about 5 h | the Station cell carries the glasses. The Max alone is not stated | https://www.xda-developers.com/rokid-max-review/ | Search |
| 4 | Apple Vision Pro | an external pack feeds the headset. Apple says all-day use when plugged in. The pack also powers it off the head | Apple says save work before you detach the pack. The page does not say what follows | https://support.apple.com/en-us/117740 | Opened |
| 5 | Meta Quest with a Link cable | the headset has its own cell. A PC port without PD at 18 W or more slows charging. Heat limits charging during use | the headset runs on its own cell | https://www.meta.com/help/quest/3482884435359892/ | Opened |
| 6 | USB-C portable monitors | bus powered by DisplayPort Alt Mode. Search summaries give 4 to 15 W by size. No cell | dark | https://us.ktcplay.com/blogs/support-tips/portable-monitor-wattage-usb-c | Search |
| 7 | Samsung DeX | the phone is the host. A PC port gives 2.5 W at 5 V 0.5 A or 4.5 W at 5 V 0.9 A. The battery can still fall | not stated. Samsung advises against battery packs | https://www.samsung.com/us/support/answer/ANS10001972/ | Opened |
| 8 | Samsung Galaxy Tab Active5 No Battery Mode | runs Android with the cell removed on a PD 2.0 supply of 9 V and 2.3 A or more. Names kiosks and vehicles. Cuts CPU, volume and brightness | no host, no power. The cell is removable, so a user can refit it | https://news.samsung.com/global/introducing-the-galaxy-xcover7-galaxy-tab-active5-the-perfect-blend-of-durability-work-continuity-and-productivity-for-todays-enterprises | Opened |
| 9 | Bypass charging (Samsung, ASUS ROG, Sony) | the charger feeds the system and the cell sits idle, to cut heat and wear. Samsung and ASUS only inside a game. Not with wireless chargers | the cell is still in the circuit and carries on | https://www.makeuseof.com/bypass-charging-on-android/ | Opened |
| 10 | NFC e-paper (Waveshare, Good Display, Ynvisible) | no cell. A phone field powers one refresh, 2 s on the Waveshare page. Ynvisible needs about 1 mJ per cm2 | the image stays. Ynvisible holds it 5 to 15 minutes. Bistable e-paper holds longer (Search) | https://www.waveshare.com/2.9inch-nfc-powered-e-paper.htm and https://www.eetimes.com/powering-e-paper-displays-with-nfc-energy-harvesting/ | Opened |
| 11 | Qi powered cell-free display | no product found in the search. The Qi results were ordinary devices with a cell | not applicable | search "Qi wireless powered e-paper display" | Search |
| 12 | Dash cams with a supercapacitor | a capacitor replaces the cell. It saves the clip and shuts down when the 12 V supply falls | runs 30 s to 2 min, for a clean shutdown only | https://www.dashcaminsight.com/supercapacitor-vs-battery-dash-cam/ | Opened |
| 13 | Zebra TC52x-HC true hot swap | a super capacitor keeps the system alive while a nurse swaps the cell. Search summaries give 30 to 60 s | memory is kept for a short time, then the device can reboot | https://docs.zebra.com/us/en/mobile-computers/handheld/tc5-series/tc53-tc58-prg/using-the-device/battery-management/battery-true-hot-swap.html | Search |
| 14 | Patent WO2013054164A2 | a small main cell, under about 10 % of the size of the swap cell, keeps power while the large cell is replaced | the small cell alone runs the device for a short time | https://patents.google.com/patent/WO2013054164A2/en | Opened |
| 15 | Ledger Nano S and Nano S Plus | a hardware wallet with a screen and no cell. It takes power over USB from the phone or computer | dark. Keys stay in the secure element | https://www.professionalcryptorecovery.com/blog/ledger-nano-s-not-turning-on/ | Opened |
| 16 | Trezor Model T | search summaries say no cell and USB-C power. The Trezor page itself did not state it | dark | https://trezor.io/trezor-model-t | Search |
| 17 | Lenovo ThinkPad Power Bridge | an internal cell keeps the laptop on while the user swaps the external cell | the internal cell carries the load | https://www.upgrade-my-laptop.com/guides/laptop-battery-replacement/lenovo-laptop-battery-replacement/lenovo-thinkpad-t480-doesnt-switch-to-secondary-battery-shuts-down-unexpectedly-power-bridge-fix-guide/ | Search |
| 18 | Medical cart hot swap (Ergotron, Anton Bauer) | a battery system with a swap bridge. A reseller says two minutes of continuous power during a swap | the cart carries on during the swap | https://www.pagec.com/about/blog/780-emr-carts-with-hot-swap-battery-system-2 | Search |
| 19 | Portable CarPlay displays | run from a 12 V socket, some on 12 V to 24 V. Cell content is not stated in the results | not stated | https://cybernews.com/reviews/best-portable-carplay-display/ | Search |
| 20 | Magic Leap 1 Lightpack | a hip pack holds the compute and the cell, about 3 h. The headset is tethered to it | the pack is the host. Product is end of life | https://www.skillsive.com/tools/xr-devices/magic-leap-1 | Opened |
| 21 | Battery free wearable sensors | research tags and sweat sensors harvest body motion or RF. They show no wallet and no large surface | no energy, no work | https://www.science.org/doi/10.1126/sciadv.aay9842 | Search |

## 4 · What the table shows

1. **The host-only display is a product category.** Tethered glasses sell today. Their draw is about `1.5` to `1.8 W`, far below the Leaf peak of `8.7 W`. `[PUBLICATION]` row 1.
2. **A wallet that lives on a host exists.** The Ledger Nano S has a screen and no cell. That part of the idea is old.
3. **Samsung is the closest neighbour.** No Battery Mode runs a full computer with the cell removed. Samsung names heat and cell health. `[PUBLICATION]` row 8.
4. **Samsung also shows the price.** The mode cuts CPU speed, volume and brightness. The Leaf must expect a peak limit on weak hosts. See `STANDARDS.md` Section 5.
5. **The bridge cell is old.** It appears in a patent, in laptops and in nurse devices. Rows 13, 14, 17, 18.
6. **The capacitor ride-through is old.** Dash cams use it to end a session cleanly. This is the Bare tier job in the BRIEF. Row 12.
7. **The host is trusted in every row.** No source above treats the power host as a hostile party. The Leaf trust rule is outside this table. See Section 6.

## 5 · What is not new in the Host Life Law

| The statement of the law | The verdict |
|---|---|
| a Leaf lives as long as the host lives | not new for glasses, monitors and a wallet. New only for the Leaf surface |
| the cell stops being the source of life | not new. Samsung No Battery Mode and dash cams show it |
| the cell becomes the bridge between hosts | not new in kind. Laptops, nurse devices and a patent bridge a swap |
| capacity moves from the body to the place | not new. Every tethered display moves it |
| the heat of the body falls when the host carries the load | not new. Samsung and bypass charging state the heat reason |

## 6 · The combination that remains open

**No source in this survey joins all of these in one product.** `[HYPOTHESIS]` Absence from a web search is not proof. Gate HPS-1 tests it.

| The element | The state of the art | The Leaf element |
|---|---|---|
| 1. the surface | glasses, monitors, e-paper, a small wallet screen | a flexible `160 x 80 mm` surface that is also a wallet |
| 2. the session | none of the rows keeps a chain session | a chain session that survives a power gap |
| 3. the bridge | a bridge saves a clip or a swap of a cell | a bridge that walks a wallet session between two hosts |
| 4. the tiers | one product has one energy design | one family with Bare, Buffer and Full stores |
| 5. the door | rows trust the power host | a host with power has no authority over the secure rail |
| 6. the heat law | heat appears as a mode switch | a skin limit of `36.2 °C` that sets the host class |

**The claim that survives is the join of elements 2, 3 and 5.** A chain session, a bridge between hosts and a power door. The next file words it.

## 7 · The searches that were not made

| The gap | Why it matters | The owner |
|---|---|---|
| patent databases by class: `H02J7`, `H02J9`, `G06F1/26`, `G06F1/30`, `G06Q20` | the web search found one patent. A professional search finds the rest | patent searcher, gate HPS-1 |
| a freedom to operate review of Qi, USB PD and Zebra style claims | the bridge and the ride-through are old, and old patents expire | patent attorney, gate HPS-2 |
| Apple, Samsung and Ledger patents on host power and wallets | the three closest neighbours are large filers | patent searcher, gate HPS-1 |
| unopened pages in rows 3, 6, 11, 13, 16 to 19 and 21 | a Search row is not a `[PUBLICATION]` | the study team, next cycle |
| products from Turkey, China and Korea in the local language | a web search in English misses them | a Turkish speaking searcher |

## 8 · The sources

Each URL above is a source. The status column says which pages the team read. The team read no source as legal advice.
