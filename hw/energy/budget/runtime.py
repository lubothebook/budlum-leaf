#!/usr/bin/env python3
"""runtime.py - the energy budget per use case, the run times, the B cell
and the dock pack. Energy and BMS team, hw/energy/.

Gates ENR-22, ENR-24, SW-20.

Run:  python3 hw/energy/budget/runtime.py   (after cell/microcell.py)
Out:  hw/energy/out/budget.json, hw/energy/out/budget.txt
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
with open(os.path.join(OUT, "cell_spec.json")) as f:
    CELL = json.load(f)

V_BUS = 3.80

# ------------------------------------------------------------------ loads
# W at the load. Body = display + address drivers + hinge sense (in the tiles).
# B = hub (U1, U6), radio (U2A, U2B, U5), authority (U7, U8, U4 housekeeping),
#     camera, audio, rear display (in the ring).
# Sources: FINAL/04 Section 4.6 rows [DECISION]; FINAL/17 Section 17.13
# display at 800 nits [DECISION]; the rest [HYPOTHESIS], marked "h".
DOMAINS = ["display", "address", "hinge", "hub", "radio", "authority",
           "camera", "audio", "rear"]
BODY = {"display", "address", "hinge"}
CASES = [
    # name, source, display, address, hinge, hub, radio, authority, camera, audio, rear
    ("wallet standby, screen off, Wi-Fi TWT", "h", 0, 0, 0, 0.005, 0.030, 0.020, 0, 0, 0),
    ("rear display glance, body dark", "h", 0, 0, 0, 0.005, 0.030, 0.030, 0, 0, 0.040),
    ("safe screen, no link", "F04", 0.10, 0.02, 0, 0.05, 0.00, 0.03, 0, 0, 0),
    ("static page at 10 Hz", "F04", 0.15, 0.02, 0, 0.10, 0.05, 0.03, 0, 0, 0),
    ("music on the 3.5 mm jack, screen off", "h", 0, 0, 0, 0.06, 0.10, 0.03, 0, 0.04, 0),
    ("voice call on 5G, screen off", "h", 0, 0, 0, 0.05, 0.55, 0.05, 0, 0.08, 0),
    ("delta session, 250 nits, Wi-Fi", "F04", 0.60, 0.20, 0, 0.70, 0.40, 0.12, 0, 0, 0),
    ("delta session at 41 % stretch", "h", 0.60, 0.20, 0.01, 0.75, 0.40, 0.12, 0, 0, 0),
    ("50 MP camera, viewfinder and upload", "h", 0.60, 0.20, 0, 0.70, 1.00, 0.12, 0.35, 0, 0),
    ("video session, Wi-Fi", "F04", 1.10, 0.25, 0, 1.20, 0.60, 0.12, 0, 0, 0),
    ("video outdoors, 800 nits, 5G", "F17+h", 3.84, 0.40, 0, 1.20, 1.10, 0.12, 0, 0, 0),
]
ETA_BODY = 0.92     # tile drivers from VBUS  [HYPOTHESIS]
ETA_B = 0.90        # U4 bucks in the ring  [HYPOTHESIS]
R_PATH = 0.050      # ohm: pack (DCIR/128) + bus + bar, from pack/network.py
USABLE = 0.96       # fraction of nominal above the 3.40 V seat cut-off, network.py

B_CELL = dict(L=20.0, W=8.0, H=1.50, whl=600.0, v=3.87)   # FINAL/21 21.2.5
B_CELL["vol_mm3"] = B_CELL["L"] * B_CELL["W"] * B_CELL["H"]
B_CELL["Wh"] = B_CELL["vol_mm3"] * 1e-6 * B_CELL["whl"]
B_CELL["mAh"] = B_CELL["Wh"] / B_CELL["v"] * 1000
ETA_BCELL = 0.95    # U4 path from the B cell to the B rails


def pack_wh(variant, which):
    vol = CELL["geometry"]["cell_volume_mm3"]
    if which == "target":
        return 128 * vol * 1e-6 * CELL["variants"][variant]["target_whl"]
    return 128 * CELL["variants"][variant]["energy_Wh"]


def battery_power(row):
    vals = dict(zip(DOMAINS, row[2:]))
    pb = sum(v for k, v in vals.items() if k in BODY)
    pB = sum(v for k, v in vals.items() if k not in BODY)
    p = pb / ETA_BODY + pB / ETA_B
    i = p / V_BUS
    p += i * i * R_PATH
    return pb, pB, p


def main():
    L = []
    p = L.append
    res = {"cases": [], "stores": {}, "b_cell": {}, "dock": {}, "charge": {}}
    stores = {
        "G target 600 Wh/L": pack_wh("G", "target"),
        "G model": pack_wh("G", "model"),
        "S target 750 Wh/L": pack_wh("S", "target"),
        "S model": pack_wh("S", "model"),
    }
    res["stores"] = stores
    p("stores (Wh, nominal): " + ", ".join("%s %.2f" % kv for kv in stores.items())
      + ", B cell %.3f" % B_CELL["Wh"])
    p("")
    head = "%-40s %6s %6s %6s | " % ("use case", "body", "B", "batt") + \
        " ".join("%9s" % k.split()[0] + k.split()[1][0] for k in stores) + "  (h, body + B cell)"
    p(head)
    for row in CASES:
        pb, pB, pbat = battery_power(row)
        hrs = {}
        for k, e in stores.items():
            e_use = e * USABLE + B_CELL["Wh"] * USABLE * ETA_BCELL
            hrs[k] = e_use / pbat
        res["cases"].append(dict(name=row[0], source=row[1], body_W=pb, b_W=pB,
                                 battery_W=pbat, hours=hrs))
        p("%-40s %6.3f %6.3f %6.3f | " % (row[0], pb, pB, pbat) +
          " ".join("%10.2f" % h for h in hrs.values()))
    p("")
    # the FINAL/21 statement: 2 to 3 W video, 1.9 to 3.7 h
    for load in (2.0, 3.0):
        pbat = load / ((ETA_BODY + ETA_B) / 2)
        pbat += (pbat / V_BUS) ** 2 * R_PATH
        for k, e in stores.items():
            h = (e * USABLE + B_CELL["Wh"] * USABLE * ETA_BCELL) / pbat
            res.setdefault("final21_check", {})[f"{load} W {k}"] = h
        p("FINAL/21 check, %.1f W at the loads (%.2f W at the cells): " % (load, pbat) +
          ", ".join("%s %.2f h" % (k, (e * USABLE + B_CELL["Wh"] * USABLE * ETA_BCELL) / pbat)
                    for k, e in stores.items()))
    # the path to the full 3.7 h: S at model density, better converters
    pbat = 0.8 / 0.95 + 1.2 / 0.93
    pbat += (pbat / V_BUS) ** 2 * R_PATH
    h = (stores["S model"] * USABLE + B_CELL["Wh"] * USABLE * ETA_BCELL) / pbat
    res["path_to_3p7h"] = dict(battery_W=pbat, hours=h)
    p("path to 3.7 h: 2.0 W (0.8 body at 0.95, 1.2 ring at 0.93) on S model: %.2f W at the cells, %.2f h" % (pbat, h))
    p("")
    # ------------------------------------------------------------- B cell
    b = B_CELL
    p("B cell: %.0f x %.0f x %.2f mm = %.0f mm3, %.3f Wh, %.1f mAh at %.2f V"
      % (b["L"], b["W"], b["H"], b["vol_mm3"], b["Wh"], b["mAh"], b["v"]))
    b_cases = {
        "swap holdover (radios kept, decoder idle) 0.40 W": 0.40,
        "B alone, rear glance 0.105 W": 0.105,
        "B alone, wallet standby 0.055 W": 0.055,
        "B alone, voice call on 5G 0.73 W": 0.73,
    }
    for k, w in b_cases.items():
        e = b["Wh"] * USABLE * ETA_BCELL
        cr = (w / ETA_BCELL / b["v"]) / (b["mAh"] / 1000)
        res["b_cell"][k] = dict(minutes=e / w * 60, c_rate=cr)
        p("  %-48s %6.1f min at %.1f C" % (k, e / w * 60, cr))
    # the fit of a 20 x 8 mm cell beside the camera column in the ring
    r_in = 15.0           # mm, inner radius of the Ø32 ring shell, 1.0 mm wall
    cam_half = 3.0        # mm, half of the 6.0 mm camera column side
    a_max = (r_in ** 2 - (b["L"] / 2) ** 2) ** 0.5 - b["W"]
    res["b_cell"]["fit_clearance_mm"] = a_max - cam_half
    p("  fit: inner edge of the cell at most %.2f mm from the centre; camera edge at %.2f mm; clearance %.2f mm"
      % (a_max, cam_half, a_max - cam_half))
    hb = CELL.get("b_cell", {})
    for k, d in hb.items():
        p("  same cell in the hermetic can build [%s]: %.3f Wh at %.0f Wh/L" % (k, d["energy_Wh"], d["whl_cell"]))
    pk = 4.50
    p("  B peak %.2f W from the cell alone would be %.0f C: the body bus carries peaks, the cell does not"
      % (pk, pk / ETA_BCELL / b["v"] / (b["mAh"] / 1000)))
    p("")
    # --------------------------------------------------------------- dock
    dock_cell = dict(L=70.0, W=60.0, H=3.7, whl=650.0, n=2, v=3.87)
    e_cell = dock_cell["L"] * dock_cell["W"] * dock_cell["H"] * 1e-6 * dock_cell["whl"]
    res["dock_cell"] = dict(dock_cell, Wh_each=e_cell, Wh_pack=dock_cell["n"] * e_cell,
                            mAh_pack=dock_cell["n"] * e_cell / dock_cell["v"] * 1000)
    p("dock pack: %d x pouch %.0f x %.0f x %.1f mm at %.0f Wh/L = %.2f Wh, 1S%dP, %.0f mAh"
      % (dock_cell["n"], dock_cell["L"], dock_cell["W"], dock_cell["H"], dock_cell["whl"],
         dock_cell["n"] * e_cell, dock_cell["n"], dock_cell["n"] * e_cell / dock_cell["v"] * 1000))
    dock = dict(Wh=20.0, usable=0.95, eta_boost=0.94, eta_qi=0.72, eta_contact_dock=0.95,
                eta_contact_leaf=0.96 * 0.99)
    e_qi = dock["Wh"] * dock["usable"] * dock["eta_boost"] * dock["eta_qi"]
    e_ct = dock["Wh"] * dock["usable"] * dock["eta_contact_dock"] * dock["eta_contact_leaf"]
    res["dock"] = dict(dock, delivered_qi_Wh=e_qi, delivered_contact_Wh=e_ct, refills={})
    p("dock pack 20 Wh: delivered to the cells by Qi %.1f Wh, by the 12 pads %.1f Wh" % (e_qi, e_ct))
    for k, e in stores.items():
        full = e + B_CELL["Wh"]
        res["dock"]["refills"][k] = dict(qi=e_qi / full, contact=e_ct / full)
        p("  %-20s refills: Qi %.2f, pads %.2f" % (k, e_qi / full, e_ct / full))
    need = 3 * (stores["S target 750 Wh/L"] + B_CELL["Wh"]) / (dock["usable"] * dock["eta_contact_dock"] * dock["eta_contact_leaf"])
    res["dock"]["wh_for_3_refills_S_pads"] = need
    p("  three pad refills of the 750 Wh/L body need a %.1f Wh dock pack" % need)
    p("")
    # ------------------------------------------------------------- charge
    for k in ("G target 600 Wh/L", "S target 750 Wh/L"):
        e = stores[k]
        p_cells = 25.0 * 0.85 * 0.96
        t50 = 0.5 * e / p_cells * 60
        # CC to 70 %, then a CV tail modelled as an exponential to 100 %
        t70 = 0.7 * e / p_cells * 60
        t_cv = 0.3 * e / (p_cells * 0.35) * 60
        res["charge"][k] = dict(t50_min=t50, t70_min=t70, t100_min=t70 + t_cv)
        p("Qi2.2 25 W into %s: 50 %% in %.1f min, 70 %% in %.1f min, full in about %.0f min (thermal permitting, ENR-24)"
          % (k, t50, t70, t70 + t_cv))
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(OUT, "budget.json"), "w") as f:
        json.dump(res, f, indent=1)
    with open(os.path.join(OUT, "budget.txt"), "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
