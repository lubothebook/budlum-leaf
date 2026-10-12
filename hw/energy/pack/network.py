#!/usr/bin/env python3
"""network.py - the 128-cell 1S128P body bus, solved as a resistor network.

Energy and BMS team, hw/energy/. Gates ENR-22, ENR-23, ENR-24, MON-16.

The body is 8 x 16 tiles. Each tile holds one micro cell behind its own
fuse and its own cell switch (the TCM, tile cell monitor). The tiles join
their four neighbours through the corner hinges. Each hinge carries one
VBUS and one GND copper line. Inside a quadrant every hinge carries power.
Across a quadrant seam only the four couplers round the (+) crossing carry
power, each through the U_Q quadrant switch on both sides.

The script solves the DC network for the use cases and the fault cases,
and sizes the thin-film fuse.

Run:  python3 hw/energy/pack/network.py
Out:  hw/energy/out/network.json, hw/energy/out/network.txt
"""
import json
import math
import os

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(OUT, "cell_spec.json")) as f:
    CELL = json.load(f)

NX, NY = 8, 16
N = NX * NY

# ---------------------------------------------------------------- copper
RHO_CU = 1.68e-8      # ohm m, 20 C
RHO_EGAIN = 29.4e-8   # ohm m  [PUBLICATION] Dickey, Adv. Funct. Mater. 18, 1097 (2008)
T_CU = 2e-6           # m, hinge copper on the neutral plane  [DECISION] FINAL/21 21.2.2
W_PWR = 0.45e-3       # m, VBUS line width along the ribbon height (1.2-1.5 mm ribbon)
L_HINGE = 1.0e-3      # m, 0.8 mm ribbon + 0.2 mm landing
R_HINGE_CU = RHO_CU * L_HINGE / (T_CU * W_PWR)
# EGaIn channel in parallel, 50 um x 0.40 mm, for the 41 % mode
R_HINGE_LM = RHO_EGAIN * L_HINGE / (50e-6 * 0.40e-3)
R_HINGE = 1.0 / (1.0 / R_HINGE_CU + 1.0 / R_HINGE_LM)
R_LOOP = 2 * R_HINGE_CU          # worst case: copper only, VBUS + GND
R_QSW = 0.010                    # ohm, U_Q quadrant switch, each side
R_TCM = 0.030                    # ohm, cell switch, back-to-back NFET
R_TILE = 0.004                   # ohm, tile routing loop

# --------------------------------------------------------------- fuse
FUSE = dict(t=2e-6, w=20e-6, l=200e-6)            # thin-film copper neck
R_FUSE = RHO_CU * FUSE["l"] / (FUSE["t"] * FUSE["w"])


def idx(x, y):
    return y * NX + x


def quadrant(x, y):
    return (1 if x < 4 else 2) if y < 8 else (3 if x < 4 else 4)


CROSS = {1: (3, 7), 2: (4, 7), 3: (3, 8), 4: (4, 8)}


def edges(seam_mode="crossing", removed=()):
    out = []
    for y in range(NY):
        for x in range(NX):
            for dx, dy in ((1, 0), (0, 1)):
                x2, y2 = x + dx, y + dy
                if x2 >= NX or y2 >= NY:
                    continue
                q1, q2 = quadrant(x, y), quadrant(x2, y2)
                if q1 in removed or q2 in removed:
                    continue
                if q1 == q2:
                    out.append((idx(x, y), idx(x2, y2), R_LOOP + R_TILE, "hinge"))
                else:
                    is_cross = (x, y) in CROSS.values() and (x2, y2) in CROSS.values()
                    if seam_mode == "all" or is_cross:
                        out.append((idx(x, y), idx(x2, y2),
                                    R_LOOP + R_TILE + 2 * R_QSW, "seam"))
    return out


def solve(case):
    """case: dict with ocv (array), r_branch (array), i_load (array, A out of
    node), edges. Returns node voltages, cell currents (A, + = discharge),
    edge currents."""
    E = case["edges"]
    alive = case.get("alive", np.ones(N, bool))
    G = lil_matrix((N, N))
    b = np.zeros(N)
    for i, j, r, _ in E:
        g = 1.0 / r
        G[i, i] += g
        G[j, j] += g
        G[i, j] -= g
        G[j, i] -= g
    for k in range(N):
        if not alive[k]:
            G[k, k] += 1.0     # pin dead nodes to 0 V, isolated
            continue
        g = 1.0 / case["r_branch"][k]
        G[k, k] += g
        b[k] += g * case["ocv"][k] - case["i_load"][k]
    V = spsolve(G.tocsr(), b)
    Icell = np.where(alive, (case["ocv"] - V) / case["r_branch"], 0.0)
    Iedge = [(i, j, (V[i] - V[j]) / r, kind) for i, j, r, kind in E]
    return V, Icell, Iedge


def base_case(variant, ocv=3.87, seam_mode="crossing", removed=()):
    rc = CELL["variants"][variant]["dcir_ohm"]
    alive = np.array([quadrant(i % NX, i // NX) not in removed for i in range(N)])
    return dict(ocv=np.full(N, ocv), r_branch=np.full(N, rc + R_TCM + R_FUSE + R_TILE),
                i_load=np.zeros(N), edges=edges(seam_mode, removed), alive=alive)


def run_load(variant, p_body, p_b, seat, eta_b=0.90, eta_body=0.92,
             seam_mode="crossing", removed=()):
    c = base_case(variant, seam_mode=seam_mode, removed=removed)
    alive = c["alive"]
    V = np.full(N, 3.8)
    for _ in range(8):   # constant-power loads: iterate on the node voltage
        il = np.zeros(N)
        il[alive] = p_body / eta_body / alive.sum() / V[alive]
        il[idx(*seat)] += p_b / eta_b / V[idx(*seat)]
        c["i_load"] = il
        V, Ic, Ie = solve(c)
    loss_net = sum(i * i * r for (a, bb, r, _), (_, _, i, _) in zip(c["edges"], Ie))
    loss_cell = float(np.sum(Ic ** 2 * c["r_branch"]))
    ic = Ic[alive]
    return dict(seat=seat, v_min=float(V[alive].min()), v_max=float(V[alive].max()),
                v_seat=float(V[idx(*seat)]),
                i_cell_min_mA=1e3 * float(ic.min()), i_cell_max_mA=1e3 * float(ic.max()),
                imbalance=float(ic.max() / max(ic.min(), 1e-9)),
                i_hinge_max_A=float(max(abs(e[2]) for e in Ie)),
                i_seam_max_A=float(max([abs(e[2]) for e in Ie if e[3] == "seam"] or [0])),
                loss_net_mW=1e3 * loss_net, loss_cell_mW=1e3 * loss_cell,
                p_out_W=float(np.sum(ic) * 0 + p_body / eta_body + p_b / eta_b))


def run_charge(variant, p_in=25.0, eta_qi=0.85, eta_q=0.96, ocv=3.90):
    """Qi2.2 25 W in; the master U_Q rectifies to VHV; each U_Q charges its
    quadrant from VHV at its crossing tile."""
    c = base_case(variant, ocv=ocv)
    p_cells = p_in * eta_qi * eta_q
    V = np.full(N, 4.1)
    for _ in range(8):
        il = np.zeros(N)
        for q, (x, y) in CROSS.items():
            il[idx(x, y)] -= p_cells / 4 / V[idx(x, y)]
        c["i_load"] = il
        V, Ic, Ie = solve(c)
    cap = CELL["variants"][variant]["capacity_mAh"] / 1000.0
    loss_cell = float(np.sum(Ic ** 2 * c["r_branch"]))
    loss_net = sum(i * i * r for (a, bb, r, _), (_, _, i, _) in zip(c["edges"], Ie))
    return dict(p_in_W=p_in, p_to_cells_W=p_cells,
                i_cell_min_mA=-1e3 * float(Ic.max()), i_cell_max_mA=-1e3 * float(Ic.min()),
                c_rate_max=float(-Ic.min() / cap), c_rate_mean=float(-Ic.mean() / cap),
                v_max=float(V.max()),
                i_hinge_max_A=float(max(abs(e[2]) for e in Ie)),
                i_seam_max_A=float(max(abs(e[2]) for e in Ie if e[3] == "seam")),
                heat_W=p_in * (1 - eta_qi * eta_q) + loss_cell + loss_net,
                loss_cell_W=loss_cell, loss_net_W=loss_net)


def run_cell_short(variant, at, r_short=0.010):
    """internal short inside one cell: its OCV branch becomes r_short to 0 V
    behind its fuse and its cell switch. Before the fuse opens."""
    c = base_case(variant)
    k = idx(*at)
    c["ocv"][k] = 0.0
    c["r_branch"][k] = r_short + R_TCM + R_FUSE + R_TILE
    V, Ic, Ie = solve(c)
    i_fault = -Ic[k]
    others = np.delete(Ic, k)
    return dict(at=at, i_fault_A=float(i_fault), v_node=float(V[k]),
                i_other_cell_max_A=float(others.max()),
                i_hinge_max_A=float(max(abs(e[2]) for e in Ie)))


def run_bus_short(variant, at, r_short=0.005):
    """hard short of the VBUS copper of one tile to GND, before any switch
    acts: every cell of the quadrant feeds it."""
    c = base_case(variant)
    k = idx(*at)
    c["i_load"] = np.zeros(N)
    # add a conductance to ground at node k
    E = c["edges"]
    G = lil_matrix((N, N))
    b = np.zeros(N)
    for i, j, r, _ in E:
        g = 1.0 / r
        G[i, i] += g; G[j, j] += g; G[i, j] -= g; G[j, i] -= g
    for m in range(N):
        g = 1.0 / c["r_branch"][m]
        G[m, m] += g
        b[m] += g * c["ocv"][m]
    G[k, k] += 1.0 / r_short
    V = spsolve(G.tocsr(), b)
    Ic = (c["ocv"] - V) / c["r_branch"]
    Ie = [abs((V[i] - V[j]) / r) for i, j, r, _ in E]
    return dict(at=at, i_short_A=float(V[k] / r_short), i_cell_max_A=float(Ic.max()),
                i_hinge_max_A=float(max(Ie)))


OCV_SOC = np.array([0.0, 0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00])
OCV_V = np.array([3.30, 3.55, 3.65, 3.72, 3.79, 3.89, 4.06, 4.38])  # [GENERAL] graphite/LCO shape


def run_soc(variant, p_body, p_b, seat, dt=30.0, eta_b=0.90, eta_body=0.92, k_bal=0.0):
    """discharge to empty at constant power: does the parallel bus keep the
    cells together? The OCV slope pulls the cells back to one SOC."""
    cap_As = CELL["variants"][variant]["capacity_mAh"] * 3.6
    soc = np.ones(N)
    c = base_case(variant)
    r0 = c["r_branch"].copy()
    V = np.full(N, 3.9)
    t, spread_max, e_out = 0.0, 0.0, 0.0
    while True:
        c["ocv"] = np.interp(soc, OCV_SOC, OCV_V)
        c["alive"] = soc > 0.005
        # balance: the TCM runs its switch in the linear region and adds
        # resistance to a cell that is behind the mean (k_bal per 1 % SOC)
        deficit = np.clip(soc.mean() - soc, 0, None) / 0.01
        c["r_branch"] = r0 * (1.0 + k_bal * deficit)
        if c["alive"].sum() < N or V[idx(*seat)] < 3.40:
            break
        for _ in range(3):
            il = np.zeros(N)
            il[:] = p_body / eta_body / N / V
            il[idx(*seat)] += p_b / eta_b / V[idx(*seat)]
            c["i_load"] = il
            V, Ic, Ie = solve(c)
        soc -= Ic * dt / cap_As
        spread_max = max(spread_max, float(soc.max() - soc.min()))
        e_out += (p_body + p_b) * dt
        t += dt
    e_nom = CELL["variants"][variant]["energy_Wh"] * N * 3600
    return dict(hours=t / 3600, spread_max=spread_max, soc_left_mean=float(soc.mean()),
                load_energy_Wh=e_out / 3600, battery_fraction=float(1 - soc.mean()))


def fuse_design():
    """adiabatic melt I2t of the fuse neck and of a hinge line, and the
    steady-state temperature rise of the neck on 12.5 um polyimide."""
    rho_cu, cp, lat, t_melt = 8.96e6, 0.385, 205.0, 1085.0  # g/m3, J/gK, J/g, C
    e_vol = rho_cu * (cp * (t_melt - 25) + lat)              # J/m3
    rho_avg = 5.0e-8                                         # ohm m, averaged to melt
    a_fuse = FUSE["t"] * FUSE["w"]
    a_hinge = T_CU * W_PWR
    i2t_fuse = e_vol * a_fuse ** 2 / rho_avg
    i2t_hinge = e_vol * a_hinge ** 2 / rho_avg
    # steady state: substrate path through 12.5 um PI plus two copper leads
    r_sub = 12.5e-6 / (0.12 * FUSE["w"] * FUSE["l"])
    r_lead = 0.5e-3 / (400 * T_CU * 60e-6)
    r_th = 1.0 / (1.0 / r_sub + 2.0 / r_lead)
    rise = {f"{i:.2f} A": i * i * R_FUSE * r_th for i in (0.06, 0.10, 0.30, 1.00)}
    i_fuse_ss = math.sqrt((t_melt - 40) / (r_th * R_FUSE))
    return dict(neck_um=[FUSE["t"] * 1e6, FUSE["w"] * 1e6, FUSE["l"] * 1e6],
                r_fuse_mohm=1e3 * R_FUSE, i2t_melt_A2s=i2t_fuse,
                i2t_hinge_melt_A2s=i2t_hinge, selectivity=i2t_hinge / i2t_fuse,
                r_th_K_per_W=r_th, rise_K=rise, i_fuse_steady_A=i_fuse_ss)


def main():
    res = dict(r_hinge_cu_mohm=1e3 * R_HINGE_CU, r_hinge_lm_mohm=1e3 * R_HINGE_LM,
               r_hinge_both_mohm=1e3 * R_HINGE, r_fuse_mohm=1e3 * R_FUSE)
    L = []
    p = L.append
    p("1S128P body bus, 8 x 16 tiles")
    p("hinge line: Cu %.1f mOhm, EGaIn %.1f mOhm, both %.1f mOhm; fuse neck %.0f mOhm"
      % (1e3 * R_HINGE_CU, 1e3 * R_HINGE_LM, 1e3 * R_HINGE, 1e3 * R_FUSE))
    fz = fuse_design()
    res["fuse"] = fz
    p("fuse: melt I2t %.2e A2s, hinge melt I2t %.2e A2s, selectivity x%.0f"
      % (fz["i2t_melt_A2s"], fz["i2t_hinge_melt_A2s"], fz["selectivity"]))
    p("fuse: Rth %.0f K/W, steady fusing current %.2f A, rise %s"
      % (fz["r_th_K_per_W"], fz["i_fuse_steady_A"],
         ", ".join("%s %.1f K" % kv for kv in fz["rise_K"].items())))
    seats = [(x, 0) for x in range(NX)] + [(0, y) for y in range(NY)] + \
            [(x, NY - 1) for x in range(NX)] + [(NX - 1, y) for y in range(NY)]
    res["load"] = {}
    cases = {
        "video 3.27 W (body 1.35, B 1.92)": (1.35, 1.92),
        "outdoor video 5G (body 4.24, B 2.42)": (4.24, 2.42),
        "peak (body 4.24, B 4.50)": (4.24, 4.50),
    }
    for v in ("G", "S"):
        for name, (pb, pB) in cases.items():
            worst = None
            for s in seats:
                r = run_load(v, pb, pB, s)
                if worst is None or r["v_seat"] < worst["v_seat"]:
                    worst = r
            res["load"][f"{v} {name}"] = worst
            p("[%s] %-38s worst seat %s: Vseat %.3f V, cell %.1f..%.1f mA (x%.2f), hinge max %.3f A, seam max %.3f A, net loss %.1f mW, cell loss %.0f mW"
              % (v, name, worst["seat"], worst["v_seat"], worst["i_cell_min_mA"], worst["i_cell_max_mA"],
                 worst["imbalance"], worst["i_hinge_max_A"], worst["i_seam_max_A"],
                 worst["loss_net_mW"], worst["loss_cell_mW"]))
    # all seam couplers carrying power, for comparison
    r = run_load("G", 4.24, 4.50, (0, 0), seam_mode="all")
    res["load"]["G peak, all seam couplers powered"] = r
    p("[G] peak with every seam coupler powered, seat (0,0): hinge max %.3f A, seam %.3f A"
      % (r["i_hinge_max_A"], r["i_seam_max_A"]))
    # quadrant removed: Q1 out, B seated on Q2 top edge
    r = run_load("G", 1.35 * 0.75, 1.92, (7, 0), removed=(1,))
    res["load"]["G video, Q1 removed, seat (7,0)"] = r
    p("[G] video, Q1 removed, seat (7,0): Vseat %.3f V, cell max %.1f mA, seam max %.3f A"
      % (r["v_seat"], r["i_cell_max_mA"], r["i_seam_max_A"]))
    r = run_load("G", 1.35 * 0.75, 1.92, (0, 15), removed=(2,))
    res["load"]["G video, Q2 removed, seat (0,15)"] = r
    p("[G] video, Q2 removed, seat (0,15): Vseat %.3f V, cell max %.1f mA, seam max %.3f A"
      % (r["v_seat"], r["i_cell_max_mA"], r["i_seam_max_A"]))
    res["soc"] = {}
    for v in ("G", "S"):
        for kb in (0.0, 2.0):
            r = run_soc(v, 1.35, 1.92, (0, 15), k_bal=kb)
            res["soc"][f"{v} k_bal={kb}"] = r
            p("[%s] video to empty, seat (0,15), balance k=%.1f: %.2f h, largest SOC spread %.1f %%, SOC left %.1f %%, load energy %.2f Wh"
              % (v, kb, r["hours"], 100 * r["spread_max"], 100 * r["soc_left_mean"], r["load_energy_Wh"]))
    res["charge"] = {}
    for v in ("G", "S"):
        r = run_charge(v)
        res["charge"][v] = r
        p("[%s] Qi2.2 25 W: %.1f W to cells, cell %.1f..%.1f mA, %.2f C max (%.2f C mean), hinge %.3f A, seam %.3f A, heat %.2f W"
          % (v, r["p_to_cells_W"], r["i_cell_min_mA"], r["i_cell_max_mA"], r["c_rate_max"],
             r["c_rate_mean"], r["i_hinge_max_A"], r["i_seam_max_A"], r["heat_W"]))
    res["cell_short"] = []
    for at in ((0, 0), (3, 7), (4, 12), (7, 15)):
        r = run_cell_short("G", at)
        res["cell_short"].append(r)
        t_open = fz["i2t_melt_A2s"] / r["i_fault_A"] ** 2
        r["t_fuse_open_us"] = 1e6 * t_open
        p("cell short at %s: fault %.1f A through its fuse, opens in %.2f us; other cells max %.3f A; hinge max %.2f A"
          % (at, r["i_fault_A"], 1e6 * t_open, r["i_other_cell_max_A"], r["i_hinge_max_A"]))
    res["bus_short"] = []
    for at in ((0, 0), (3, 7)):
        r = run_bus_short("G", at)
        res["bus_short"].append(r)
        t_hinge = fz["i2t_hinge_melt_A2s"] / r["i_hinge_max_A"] ** 2
        r["t_hinge_melt_ms"] = 1e3 * t_hinge
        p("bus short at %s: %.1f A, cell max %.2f A, hinge max %.2f A, hinge melts after %.2f ms (TCM trips in 0.02 ms)"
          % (at, r["i_short_A"], r["i_cell_max_A"], r["i_hinge_max_A"], 1e3 * t_hinge))
    # one cell's own stored energy, deposited in its tile, adiabatic
    for v in ("G", "S"):
        e = CELL["variants"][v]["energy_J"]
        m_tile = 68.0 / 128   # g, body mass share per tile  [DECISION] HARDWARE/15 body 68 g
        dT = e / (m_tile * 1.0)
        res[f"tile_adiabatic_rise_{v}_K"] = dT
        p("[%s] one cell holds %.0f J; adiabatic tile rise %.0f K: a contained event needs the vent and the spread of ENR-15"
          % (v, e, dT))
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(OUT, "network.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    with open(os.path.join(OUT, "network.txt"), "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
