# BUDLUM LEAF · BATTERY-FREE PANEL DECISIONS

**Revision L.8 · 2026-10-20**. This ledger records decisions under the battery-free panel directive. The directive takes priority over every earlier Leaf file on these topics. `[DECISION]`

| No. | Task | Status | Decision | Alternative and reason | Gate |
|---|---|---|---|---|---|
| BP-00 | Authority | **DECIDED** | The panel is passive without the attached Core. It contains no cell, no capacitor used as an energy store, and no user data. The Core carries the energy, identity, radios and computing. | L.7 Heartbeat and L.6.1 Buffer/Full put cells in the panel. They are retired. | BFP-1 |
| BP-01 | Authority | **DECIDED** | `FINAL/24-battery-free-panel.md` is the active battery-free section. It overrides battery, module placement, thickness, charging, pairing and distance claims in Parts 0 to 23. | Editing only the latest part leaves conflicting rules alive. H12 must rewrite or retire each conflict. | BFP-2 |
| BP-02 | Authority | **DECIDED** | The panel has no fixed thickness target. `2.00 mm` is an upper limit. A thinner stack is the design goal. | A fixed `2.00 mm` body spends flex margin for a battery that no longer exists. | BFP-3 |
| BP-03 | Authority | **DECIDED** | Polycarbonate is the carrier and the exterior. Glass is not a candidate in the panel stack or the Frame lens panel. | The glass micro-LED carrier of Part 21 conflicts with the material rule. | BFP-4 |
| BP-04 | Authority | **DECIDED** | The Core is the camera module. It attaches at qualified zones on an edge, front face, rear face or glasses frame. Every qualified zone supplies panel power and data. | A distant Core cannot feed an attached passive panel without a separate local power host. Part 23 C1/C2 is retired. | BFP-5 |
| BP-05 | Authority | **DECIDED** | The Core contains the charging receiver and the battery. The Budlum base transmits wireless power to the Core. The panel contains no charging receiver. | Qi2.2 sector coils in panel tiles are retired. | BFP-6 |
| BP-06 | Authority | **DECIDED** | Auxiliary magnetic battery modules attach to the Core only. No cell enters the panel or an add-on panel face. | A rear battery mounted on the panel violates the passive panel rule. | BFP-7 |
| BP-07 | Authority | **DECIDED** | The second face is an independent emissive face. One attached Core powers both faces within its output budget. | A shared image on both faces fails privacy. | BFP-8 |
| BP-08 | Authority | **DECIDED** | Linux and free software, hardware openness, the patent policy, B.U.D. storage and the wallet security rules remain requirements. | A remote wallet signer conflicts with the Core identity rule. The signer moves to the Core. | BFP-9 |

**The record rule**. H1 to H12 add rows in order. Each row gives a result, an alternative and a gate. A numerical claim needs a calculation or a source. `[DECISION]`
