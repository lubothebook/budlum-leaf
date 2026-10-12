#!/usr/bin/env python3
"""budget.py - the power and thermal budget of the L.6.0 Leaf Dock.

Dock team, hw/dock/. Gates SW-20, ENR-24, ENR-6.

It reads the charge loss chain of sim/thermal/results.json (read only) and
the Leaf energy stores of hw/energy/out/budget.json (read only), then:

  1. sizes the regulated full-face pad: the heat it must pump, the TEC
     current, the TEC power and the hot-side heat, from 15 to 35 deg C;
  2. shows why a fan-only pad misses the 22 deg C set-point;
  3. sizes the blower air flow for the whole box, with and without the
     validator module;
  4. checks the 140 W wall feed in every operating mode;
  5. counts the Leaf refills from the 20 Wh pack, away from a wall.

Run:  python3 hw/dock/budget.py
Out:  hw/dock/out/budget.json, hw/dock/out/budget.txt, hw/dock/out/tec_sweep.png
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
K0 = 273.15
RHO_CP_AIR = 1.18 * 1006.0      # J/m3K at 25 deg C

lines = []


def p(s=""):
    lines.append(s)
    print(s)


# ------------------------------------------------------------------ inputs
def load_json(rel):
    path = os.path.join(ROOT, rel)
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


TH = load_json("sim/thermal/results.json")
EN = load_json("hw/energy/out/budget.json")

if TH and "loss_budget_25W" in TH:
    LB = TH["loss_budget_25W"]
    src_th = "sim/thermal/results.json"
else:  # the README numbers of the thermal team, as a fallback
    LB = dict(coil=1.027, shield_eddy=0.40, ac_lead=0.635, rectifier=0.641,
              charger=1.25, dc_lattice=1.542, leaves=0.342, cells_I2R=1.089,
              _P_stored=20.776, _P_pad_draw=27.703)
    src_th = "sim/thermal/README.md (fallback)"

QI_DEVICE_HEAT = sum(v for k, v in LB.items() if not k.startswith("_"))
CONTACT_DEVICE_HEAT = LB["charger"] + LB["dc_lattice"] + LB["leaves"] + LB["cells_I2R"]
P_STORED = LB["_P_stored"]
P_COUPLED = LB["_P_pad_draw"]            # into the Leaf coil, W

STORES = {}
if EN and "stores" in EN:
    for k, v in EN["stores"].items():
        wh = v.get("Wh") if isinstance(v, dict) else v
        if isinstance(wh, (int, float)):
            STORES[k] = float(wh)
if not STORES:
    STORES = {"G target 600 Wh/L": 5.90, "S target 750 Wh/L": 7.38}

# ------------------------------------------------------------------ the Qi transmitter chain
TX_COIL_LOSS = P_COUPLED * (1.0 / P.ETA_TX_COIL - 1.0)
P_BRIDGE_OUT = P_COUPLED / P.ETA_TX_COIL
P_TX_DC = P_BRIDGE_OUT / P.ETA_INVERTER / P.ETA_TX_FRONT
TX_BOARD_LOSS = P_TX_DC - P_BRIDGE_OUT          # on the board, not under the pad
P_CONTACT_DC = P.CONTACT_P_RX / P.ETA_CONTACT_BB


# ------------------------------------------------------------------ the TEC model
def tec_coeffs(t=P.TEC):
    th = t["Th_rated"] + K0
    S = t["Vmax"] / th
    R = t["Vmax"] * (th - t["dTmax"]) / (t["Imax"] * th)
    K = t["Imax"] * t["Vmax"] * (th - t["dTmax"]) / (2.0 * th * t["dTmax"])
    return S, R, K


S_M, R_M, K_M = tec_coeffs()
N_TEC = P.TEC["n_modules"]


def tec_point(I, Tc, Th):
    """Per module: cold-side heat, electric power, hot-side heat (W)."""
    dT = Th - Tc
    qc = S_M * I * Tc - 0.5 * I * I * R_M - K_M * dT
    pe = S_M * I * dT + I * I * R_M
    return qc, pe, qc + pe


def pad_demand(t_amb, path):
    """Heat the TEC cold side must pump to hold the pad at the set-point."""
    dev = QI_DEVICE_HEAT if path == "qi" else CONTACT_DEVICE_HEAT
    q = dev * P.F_DEVICE_HEAT_TO_PAD + P.UA_PAD_LEAK * (t_amb - P.PAD_SETPOINT)
    if path == "qi":
        q += TX_COIL_LOSS
    return q


def solve_tec(t_amb, q_need):
    """Lowest-power current that pumps q_need with the sink in the loop."""
    tc = P.PAD_SETPOINT - q_need * P.R_COLD + K0
    best = None
    for I in np.linspace(0.05, P.TEC["Imax"], 600):
        th = t_amb + K0 + 5.0
        for _ in range(60):
            qc, pe, qh = tec_point(I, tc, th)
            th_new = t_amb + K0 + N_TEC * qh * P.R_SINK_TEC
            if abs(th_new - th) < 1e-4:
                break
            th = 0.5 * th + 0.5 * th_new
        if N_TEC * qc >= q_need:
            if best is None or N_TEC * pe < best["P_tec"]:
                best = dict(I=float(I), P_tec=float(N_TEC * pe), Q_hot=float(N_TEC * qh),
                            T_hot=float(th - K0), T_cold=float(tc - K0),
                            COP=float(q_need / (N_TEC * pe)) if pe > 0 else float("inf"))
    return best


def fan_only_pad(t_amb, path):
    """Pad temperature with the TEC unpowered, heat conducted through it."""
    dev = QI_DEVICE_HEAT if path == "qi" else CONTACT_DEVICE_HEAT
    q = dev * P.F_DEVICE_HEAT_TO_PAD + (TX_COIL_LOSS if path == "qi" else 0.0)
    r = P.R_COLD + 1.0 / (N_TEC * K_M) + P.R_SINK_TEC
    return t_amb + q * r


def load_sum(table, col):
    i = {"idle": 0, "typ": 1, "peak": 2}[col]
    return sum(v[i] for v in table.values())


def main():
    p("BUDLUM LEAF DOCK L.6.0 · power and thermal budget · gate SW-20")
    p("inputs: %s, hw/energy/out/budget.json" % src_th)
    p("")
    p("1 · the charge paths at 25 W received")
    p("  Qi: coupled into the Leaf %.2f W, Tx coil loss %.2f W (under the pad), "
      "bridge+front loss %.2f W (board)" % (P_COUPLED, TX_COIL_LOSS, TX_BOARD_LOSS))
    p("  Qi: dock DC draw %.2f W, Leaf heat %.2f W, stored %.2f W, wall-to-cell %.1f %%"
      % (P_TX_DC, QI_DEVICE_HEAT, P_STORED, 100 * P_STORED / P_TX_DC))
    p("  contact (12 leaves, VHV at %.0f V): dock DC draw %.2f W, Leaf heat %.2f W, "
      "stored %.2f W, %.1f %%" % (P.CONTACT_V, P_CONTACT_DC, CONTACT_DEVICE_HEAT,
                                   P_STORED, 100 * P_STORED / P_CONTACT_DC))
    p("  rule: contact first when the leaves mate, Qi otherwise, never both  [DECISION] dock team")
    p("")

    p("2 · the TEC: %d x 127-couple 40 x 40 mm, S %.4f V/K, R %.2f ohm, K %.3f W/K per module"
      % (N_TEC, S_M, R_M, K_M))
    ambs = np.arange(15.0, 35.01, 2.5)
    sweep = {"qi": [], "contact": []}
    p("  %-8s %-7s %8s %7s %8s %8s %8s %6s %10s" % ("path", "T_amb", "Q_pump", "I", "P_tec",
                                                  "Q_hot", "T_hot", "COP", "fan-only"))
    for path in ("qi", "contact"):
        for ta in ambs:
            q = pad_demand(ta, path)
            fo = fan_only_pad(ta, path)
            row = dict(T_amb=float(ta), Q_pump=float(q), fan_only_pad=float(fo))
            if fo <= P.PAD_SETPOINT:
                # the room alone holds the pad cold: the TEC is off and the
                # blower slows until the pad rises to 22 C (plating floor)
                row.update(I=0.0, P_tec=0.0, Q_hot=float(q), T_hot=float(fo), COP=0.0,
                           mode="TEC off, blower throttled to hold 22 C")
                p("  %-8s %5.1f C %6.2f W   TEC off, the blower slows to hold 22 C" % (path, ta, q))
                sweep[path].append(row)
                continue
            s = solve_tec(ta, q)
            if s:
                s["P_tec"] = max(s["P_tec"], 0.0)
                s["mode"] = "TEC cooling"
                row.update(s)
                p("  %-8s %5.1f C %6.2f W %5.2f A %6.2f W %6.2f W %6.1f C %6.2f %8.1f C"
                  % (path, ta, q, s["I"], s["P_tec"], s["Q_hot"], s["T_hot"], s["COP"], fo))
            else:
                row["fail"] = True
                p("  %-8s %5.1f C %6.2f W   no current holds the set-point" % (path, ta, q))
            sweep[path].append(row)
    worst = max(sweep["qi"], key=lambda r: r.get("P_tec", 1e9))
    p("  worst case: Qi at %.0f C, TEC %.1f W electric, %.1f W to the fins"
      % (worst["T_amb"], worst["P_tec"], worst["Q_hot"]))
    p("  fan only: the pad sits %.1f K above the room at 25 C. Fan-only cannot reach 22 C "
      "above 22 C ambient, so the TEC is the design  [HYPOTHESIS]"
      % (fan_only_pad(25.0, "qi") - 25.0))
    p("")

    # ---------------------------------------------------------- the air
    base_typ = load_sum(P.LOADS, "typ")
    base_peak = load_sum(P.LOADS, "peak")
    val_typ = load_sum(P.VALIDATOR, "typ")
    val_peak = load_sum(P.VALIDATOR, "peak")
    pack_loss = P.PACK_CHARGE_W * 0.06
    heat_box_base = worst["Q_hot"] + TX_BOARD_LOSS + base_peak + pack_loss + 0.04 * P.WALL_FEED_W * 0.5
    heat_box_val = heat_box_base + val_peak
    dT_air_max = 10.0
    flow_base = heat_box_base / (RHO_CP_AIR * dT_air_max) * 1000.0
    flow_val = heat_box_val / (RHO_CP_AIR * dT_air_max) * 1000.0
    p("3 · the blower, air rise held at %.0f K at 35 C ambient" % dT_air_max)
    p("  box heat, no validator: %.1f W, needs %.2f L/s (%.1f CFM)"
      % (heat_box_base, flow_base, flow_base * 2.119))
    p("  box heat, with validator: %.1f W, needs %.2f L/s (%.1f CFM)"
      % (heat_box_val, flow_val, flow_val * 2.119))
    p("  the TEC fins sit first in the air path. The validator fins sit downstream  [DECISION] dock team")
    p("")

    # ---------------------------------------------------------- the wall
    modes = {}
    tec_qi = worst["P_tec"]
    tec_ct = max(r["P_tec"] for r in sweep["contact"] if "P_tec" in r)
    modes["idle, AP on"] = load_sum(P.LOADS, "idle") + 1.5
    modes["Qi 25 W + AP + TEC + pack 1 C"] = base_typ + P_TX_DC + tec_qi + P.PACK_CHARGE_W / 0.94
    modes["contact 25 W + AP + TEC + pack 1 C"] = base_typ + P_CONTACT_DC + tec_ct + P.PACK_CHARGE_W / 0.94
    modes["Qi 25 W + AP peak + TEC + validator peak"] = base_peak + P_TX_DC + tec_qi + val_peak
    modes["all at peak, pack 1 C (shed by priority)"] = (base_peak + P_TX_DC + tec_qi + val_peak
                                                          + P.PACK_CHARGE_W / 0.94)
    p("4 · the wall feed: USB-C PD 3.1 EPR, %.0f W" % P.WALL_FEED_W)
    for k, v in modes.items():
        p("  %-48s %6.1f W  %s" % (k, v, "fits" if v <= P.WALL_FEED_W else "over: pack charge pauses"))
    p("  priority: Leaf charge, TEC, radios, validator, pack charge last  [DECISION] dock team")
    p("")

    # ---------------------------------------------------------- the pack
    wh_nom = P.PACK_S * P.PACK_P * P.CELL_V_NOM * P.CELL_AH
    wh_use = wh_nom * P.PACK_USABLE
    eta_pack_out = 0.97
    p("5 · the pack: %dS%dP, %.2f Wh nominal, %.2f Wh usable" % (P.PACK_S, P.PACK_P, wh_nom, wh_use))
    refills = {}
    # energy per stored Wh in the Leaf, from the pack, at 25 C ambient
    tec25_ct = next(r for r in sweep["contact"] if abs(r["T_amb"] - 25.0) < 1e-6)["P_tec"]
    tec25_qi = next(r for r in sweep["qi"] if abs(r["T_amb"] - 25.0) < 1e-6)["P_tec"]
    paths = {
        "contact, TEC on, AP off": (P_CONTACT_DC + tec25_ct + 0.8 + 0.6) / P_STORED,
        "contact, TEC on, AP on": (P_CONTACT_DC + tec25_ct + 0.8 + 0.6 + base_typ - 1.4) / P_STORED,
        "Qi, TEC on, AP off": (P_TX_DC + tec25_qi + 0.8 + 0.6) / P_STORED,
    }
    for name, wh_per_wh in paths.items():
        delivered = wh_use * eta_pack_out / wh_per_wh
        refills[name] = {"delivered_to_cells_Wh": delivered}
        p("  %-26s delivers %5.2f Wh to the Leaf cells" % (name, delivered))
        for sname, swh in STORES.items():
            n80 = delivered / (0.8 * swh)
            nfull = delivered / swh
            refills[name][sname] = {"0_to_80": n80, "0_to_100": nfull}
            p("      %-22s %4.2f refills 0-80 %%, %4.2f full" % (sname, n80, nfull))
    k = paths["contact, TEC on, AP off"] / eta_pack_out / P.PACK_USABLE
    need80 = 3 * 0.8 * STORES.get("S target 750 Wh/L", 7.38) * k
    needfull = 3 * STORES.get("S target 750 Wh/L", 7.38) * k
    p("  FINAL/21 says 'about three times'. The contact path gives %.1f refills 0-80 %% of the"
      % refills["contact, TEC on, AP off"].get("G target 600 Wh/L", {}).get("0_to_80", 0))
    p("  600 Wh/L body, AP off. Three 0-80 %% refills of the 750 Wh/L body need %.1f Wh." % need80)
    p("  Three full refills of the 750 Wh/L body need %.1f Wh in the pack." % needfull)
    refills["Wh_for_3x_0_80_S"] = need80
    refills["Wh_for_3x_full_S"] = needfull
    p("")

    res = dict(
        inputs=dict(thermal=src_th, loss_budget=LB, stores=STORES),
        qi=dict(P_coupled=P_COUPLED, tx_coil_loss=TX_COIL_LOSS, board_loss=TX_BOARD_LOSS,
                P_dc=P_TX_DC, leaf_heat=QI_DEVICE_HEAT),
        contact=dict(P_dc=P_CONTACT_DC, leaf_heat=CONTACT_DEVICE_HEAT, V=P.CONTACT_V),
        tec=dict(S=S_M, R=R_M, K=K_M, n=N_TEC, sweep=sweep, worst=worst),
        air=dict(heat_base=heat_box_base, heat_val=heat_box_val, flow_base_lps=flow_base,
                 flow_val_lps=flow_val),
        wall=dict(feed=P.WALL_FEED_W, modes=modes),
        pack=dict(Wh_nom=wh_nom, Wh_usable=wh_use, refills=refills),
    )
    with open(os.path.join(OUT, "budget.json"), "w") as f:
        json.dump(res, f, indent=1)
    with open(os.path.join(OUT, "budget.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        for path, c in (("qi", "#2a6fdb"), ("contact", "#1b9e77")):
            ta = [r["T_amb"] for r in sweep[path]]
            ax[0].plot(ta, [r["P_tec"] for r in sweep[path]], "-o", color=c, label=path + ", TEC power")
            ax[0].plot(ta, [r["Q_pump"] for r in sweep[path]], "--", color=c, label=path + ", heat pumped")
            ax[1].plot(ta, [r["fan_only_pad"] for r in sweep[path]], "-o", color=c, label=path + ", fan only")
        ax[1].axhline(P.PAD_SETPOINT, color="k", lw=1, label="22 C set-point, TEC")
        ax[0].set_xlabel("ambient, C")
        ax[0].set_ylabel("W")
        ax[0].legend(fontsize=8)
        ax[0].set_title("regulated pad at 22 C")
        ax[1].set_xlabel("ambient, C")
        ax[1].set_ylabel("pad top, C")
        ax[1].legend(fontsize=8)
        ax[1].set_title("fan-only pad")
        fig.tight_layout()
        fig.savefig(os.path.join(OUT, "tec_sweep.png"), dpi=110)
    except Exception as e:  # plotting is optional
        p("plot skipped: %s" % e)


if __name__ == "__main__":
    main()
