#!/usr/bin/env python3
"""powerpath.py - question 2: the power path and its time-stepped simulator.

TOPOLOGY (rail names of hw/energy/03). See README section 3 for the drawing.

  host --> VHV (leaves 5, 8, or the Q1 rectifier) --> U_Q input OR-ing diode (new) --> U_Q x4, 3:1 SC, 6.25 W each
        --> VBUS (the 1S128P grid, the "bridge cell" = the enabled micro cells, TCM switches) --> tile nodes
        --> S_SEAT (leaves 2, 11) --> U4 --> VSYS_B = max(VBUS, B cell) by ideal diodes --> ring rails
  B cell --> U7 always-on 1.8 V (the ISLAND rail: secure element and U4 ROM)
  U4 charges the B cell from VBUS; the body never takes energy back from the B cell (no back-feed).

MODES  HOST_FEED, HOST_TOPUP, BRIDGE, ISLAND. Thresholds in TH below.

The simulator steps an adaptive dt (0.2 ms near an event, up to 0.5 s in steady state), solves the VBUS node
(parallel cell groups, constant-power load, host current injection), and tracks the SOC of the pack and of the B cell.

Run:  python3 hw/hostpower/powerpath/powerpath.py
Out:  out/powerpath.json, out/powerpath.txt, out/pp_*.png
"""
import math

import numpy as np
from scipy.optimize import brentq

import common as C

# ------------------------------------------------------------------ thresholds, the contract of the controller
TH = dict(
    V_HOST_OK_RISE=9.0,     # V on VHV: the host counts as present at or above this [H]
    V_HOST_OK_FALL=8.0,     # V on VHV: the host counts as lost below this [H]
    T_HOST_QUAL=0.020,      # s a rising host must hold before U_Q takes it [H]
    T_MATE=0.003,           # s mating challenge, hw/energy/03 s3.2 [D] gate ENR-19
    T_UNMATE=0.0008,        # s S_SEAT opens, hw/energy/03 s3.3 [D]
    SOC_TOP_LO=0.45,        # enter HOST_TOPUP below this pack SOC [D] this team
    SOC_TOP_HI=0.55,        # leave HOST_TOPUP at this SOC: the float band is 45 to 55 % [D] this team
    SOC_CLASS_DELTA=0.30,   # BRIDGE: below this the session is capped to the delta class [D]
    SOC_CLASS_SAFE=0.18,    # BRIDGE: below this only the safe screen runs [D]
    SOC_CLOSE=0.12,         # BRIDGE: below this the session closes and the state is saved [D]
    SOC_FLOOR=0.10,         # BRIDGE to ISLAND: the pack reserve [D]
    B_SOC_TARGET=0.60,      # the B cell float target [D]
    B_SOC_RING_MIN=0.15,    # below this the B cell serves U7 and U4 ROM only [D]
    C_TOPUP=0.5,            # C, the top-up current of the enabled cells [D]
    CMAX=3.0,               # C, discharge cap of the micro cell [H]
    V_SEAT_FLOOR=3.40,      # V, display classes [D]
    ETA_UQ=0.97,            # U_Q 3:1 SC at its ratio [H]
    ETA_U4=0.95,            # U4 from the B cell, runtime.py [T]
    ETA_AON=0.80,           # always-on 1.8 V regulator [H]
    P_UQ_EACH=6.25,         # W per U_Q [T]
    I_JOIN=0.38,            # A, a joining quadrant, hw/energy/03 s4 [D]
    V_AON_MIN=2.30,         # V, the B cell voltage under which the 1.8 V island rail drops (LDO dropout 0.5 V) [H]
)
F_RING = {"standby": 1.0, "safe screen": 0.40, "delta session": 0.60, "video": 0.59,
          "outdoor": 0.36, "peak": 0.52}     # share of the load in the ring, from hw/energy/04 s3.1 and 03 s1.2 [T]
B_CELL = dict(E_Wh=C.B_CELL_WH, dcir=1.84)    # G can model DCIR of the 20 x 8 x 1.5 mm cell [T]


class Host:
    """A host segment: a source that is present from t0 to t1."""

    def __init__(self, t0, t1, V=12.0, P=25.0, t_pd=0.0, dips=(), name="host"):
        self.t0, self.t1, self.V, self.P, self.t_pd = t0, t1, V, P, t_pd
        self.dips = list(dips)       # (ta, tb, V)
        self.name = name

    def vhv(self, t):
        if t < self.t0 + TH["T_MATE"] or t >= self.t1:
            return 0.0
        for ta, tb, vd in self.dips:
            if ta <= t < tb:
                return vd
        if t < self.t0 + TH["T_MATE"] + self.t_pd:
            return 5.0                     # vSafe5V before the contract: below the U_Q input threshold
        return self.V

    def pcap(self, t):
        return self.P if self.vhv(t) >= TH["V_HOST_OK_RISE"] else 0.0

    def edges(self):
        e = [self.t0, self.t0 + TH["T_MATE"], self.t0 + TH["T_MATE"] + self.t_pd, self.t1]
        for ta, tb, _ in self.dips:
            e += [ta, tb]
        return e


class Pack:
    """Parallel cell groups, one per quadrant."""

    def __init__(self, n_q, E_cell, dcir, soc0):
        self.E = E_cell
        self.q_ah = C.cell_q_Ah(E_cell)
        self.dcir = dcir
        self.n = list(n_q)
        self.soc = [soc0] * 4
        self.joining = [False] * 4

    def n_on(self):
        return sum(self.n)

    def q_total(self):
        return self.n_on() * self.q_ah

    def groups(self):
        out = []
        for k in range(4):
            if self.n[k] > 0:
                out.append((k, self.dcir * C.r_factor(self.soc[k]) / self.n[k], float(C.ocv(self.soc[k]))))
        return out

    def currents(self, v):
        """Discharge current of each group at bus voltage v (A, positive out of the cell)."""
        res = {}
        for k, r, o in self.groups():
            i = (o - v) / r
            if self.joining[k]:
                i = max(-TH["I_JOIN"], i)       # the limit holds the inrush into the joining cells only
            res[k] = i
        return res

    def mean_soc(self):
        tot = sum(self.n)
        return sum(self.soc[k] * self.n[k] for k in range(4)) / tot if tot else 0.0

    def voc_eff(self):
        gs = self.groups()
        if not gs:
            return 0.0
        g = sum(1 / r for _, r, _ in gs)
        return sum(o / r for _, r, o in gs) / g


class CapStore:
    """Bare tier: a capacitor store behind a converter."""

    def __init__(self, C_F, esr, vmax, vmin, eta=0.90):
        self.C, self.esr, self.vmax, self.vmin, self.eta = C_F, esr, vmax, vmin, eta
        self.v = vmax

    def soc(self):
        return max(0.0, (self.v ** 2 - self.vmin ** 2) / (self.vmax ** 2 - self.vmin ** 2))


def bus_solve(pack, p_load, i_host):
    """Bus voltage for a constant-power load and an injected host current. Returns V or None (collapse)."""
    gs = pack.groups()
    if not gs:
        return None

    def f(v):
        ibat = sum(pack.currents(v).values())
        return ibat + i_host - p_load / v

    # the physical operating point is the highest root: scan down from above the open-circuit voltage
    hi = 5.2
    fhi = f(hi)
    v = hi
    while v > 0.6:
        v2 = v - 0.05
        f2 = f(v2)
        if (fhi < 0) != (f2 < 0):
            return brentq(f, v2, v, xtol=1e-7)
        v, fhi = v2, f2
    return None


def run(name, tier, hosts, session, events=(), t_end=60.0, pack=None, cap=None, soc0=0.5, b_soc0=0.6,
        n_q=(5, 5, 5, 5), E_cell=None, dcir=None, close_s=None, record_dt=0.05, verbose=False):
    """session: list of (t, class name). events: list of (t, kind, arg). Kinds:
       quad_out q | quad_in q (arg=(q, n, soc)) | b_off | b_on"""
    cell = C.CELLS["S"]
    E_cell = E_cell or cell["E_target_Wh"]
    dcir = dcir or cell["dcir"]
    if tier == "bare":
        pk = None
        store = cap
    else:
        pk = pack or Pack(n_q, E_cell, dcir, soc0)
        store = None
    soc_b = b_soc0
    quad_present = [True] * 4
    mode = "ISLAND" if (tier == "bare" and False) else "BRIDGE"
    host_ok = False
    host_rise_t = None
    b_seated = True
    sess = sorted(session)
    evs = sorted(events, key=lambda e: e[0])
    edge_times = sorted({0.0, t_end} | {e[0] for e in evs} | {s[0] for s in sess} |
                        {x for h in hosts for x in h.edges()})
    t = 0.0
    log = dict(t=[], mode=[], vhv=[], vbus=[], vsys_b=[], vbcell=[], vaon=[], soc=[], soc_b=[], p_load=[], p_host=[],
               i_host=[])
    ev_log = []
    stats = dict(vaon_min=9.0, vaon_dropped=False, vbus_min=9.0, brownout_s=0.0, c_max=0.0, collapse=0,
                 e_host_Wh=0.0, e_pack_Wh=0.0, e_b_Wh=0.0, mode_s={}, closed_clean=None, bus_floor_s=0.0)
    cls = "standby"
    last_mode = mode
    next_rec = 0.0
    close_t0 = None
    session_closed = False
    ev_i = 0
    sess_i = 0
    while t < t_end - 1e-12:
        # ---- discrete events
        while ev_i < len(evs) and evs[ev_i][0] <= t + 1e-12:
            _, kind, arg = evs[ev_i]
            ev_i += 1
            if kind == "quad_out":
                if pk:
                    pk.n[arg] = 0
                quad_present[arg] = False
                ev_log.append((t, "quadrant Q%d removed, U_Q opens, its cells leave the bus" % (arg + 1)))
            elif kind == "quad_in":
                q, n, s = arg
                if pk:
                    pk.n[q], pk.soc[q], pk.joining[q] = n, s, True
                quad_present[q] = True
                ev_log.append((t, "quadrant Q%d joins in current limit %.2f A, %d cells at SOC %.2f" % (q + 1, TH["I_JOIN"], n, s)))
            elif kind == "b_off":
                b_seated = False
                ev_log.append((t, "B module unseated: S_SEAT opens, VSYS_B on the B cell"))
            elif kind == "b_on":
                b_seated = True
                ev_log.append((t, "B module seated: S_SEAT closes after the 3 ms challenge"))
        while sess_i < len(sess) and sess[sess_i][0] <= t + 1e-12:
            cls = sess[sess_i][1]
            sess_i += 1
            session_closed = False
            close_t0 = None
            ev_log.append((t, "session class -> %s" % cls))
        # ---- host
        vhv = max((h.vhv(t) for h in hosts), default=0.0)
        hobj = next((h for h in hosts if h.vhv(t) == vhv and vhv > 0), None)
        if vhv >= TH["V_HOST_OK_RISE"]:
            if host_rise_t is None:
                host_rise_t = t
            if not host_ok and t - host_rise_t >= TH["T_HOST_QUAL"]:
                host_ok = True
                ev_log.append((t, "host qualified at %.1f V after %.0f ms" % (vhv, 1000 * TH["T_HOST_QUAL"])))
        else:
            host_rise_t = None
            if host_ok and vhv < TH["V_HOST_OK_FALL"]:
                host_ok = False
                ev_log.append((t, "host lost, VHV %.1f V" % vhv))
        n_uq = sum(quad_present)
        p_host_cap = 0.0
        if host_ok and hobj is not None:
            p_host_cap = min(hobj.P, TH["P_UQ_EACH"] * n_uq) * TH["ETA_UQ"]       # W into the bus
        # ---- soc of the store
        soc_pack = pk.mean_soc() if pk else store.soc()
        have_store = (pk.n_on() > 0) if pk else store.v > store.vmin
        # ---- mode
        new = mode
        if host_ok and p_host_cap > 0:
            if mode in ("BRIDGE", "ISLAND"):
                new = "HOST_TOPUP" if soc_pack < TH["SOC_TOP_HI"] else "HOST_FEED"
            elif mode == "HOST_FEED" and soc_pack < TH["SOC_TOP_LO"]:
                new = "HOST_TOPUP"
            elif mode == "HOST_TOPUP" and soc_pack >= TH["SOC_TOP_HI"]:
                new = "HOST_FEED"
            if tier == "bare":
                new = "HOST_TOPUP" if (store.v < store.vmax - 0.02) else "HOST_FEED"
        else:
            if mode in ("HOST_FEED", "HOST_TOPUP"):
                new = "BRIDGE"
            if mode == "BRIDGE" and (not have_store or soc_pack <= TH["SOC_FLOOR"] or session_closed):
                new = "ISLAND"
            if mode == "ISLAND":
                # a pack that is back and above the floor by 5 points returns the body to BRIDGE
                new = "BRIDGE" if (have_store and soc_pack > TH["SOC_FLOOR"] + 0.05 and not session_closed) else "ISLAND"
        if new != mode:
            if new != "BRIDGE":
                close_t0 = None
            if new in ("HOST_FEED", "HOST_TOPUP", "BRIDGE"):
                session_closed = False if new != "BRIDGE" or mode == "ISLAND" else session_closed
            ev_log.append((t, "mode %s -> %s (SOC %.3f, host %s)" % (mode, new, soc_pack, "ok" if host_ok else "no")))
            mode = new
        # ---- the load the controller allows
        p_req = C.LOADS[cls]
        f_ring = F_RING[cls]
        cap_cells = 0.0
        if pk and pk.n_on():
            cap_cells = TH["CMAX"] * pk.q_total() * float(C.ocv(max(soc_pack, 0.1))) * 0.90
        if mode in ("HOST_FEED", "HOST_TOPUP"):
            p_allowed = p_req
            assist = cap_cells if soc_pack > TH["SOC_CLASS_SAFE"] else 0.0     # no pack assist at the safe class
            if p_req > p_host_cap + assist:
                p_allowed = p_host_cap + assist
            if tier == "bare":
                p_allowed = min(p_req, p_host_cap)
        elif mode == "BRIDGE":
            if tier == "bare":
                # the Bare tier closes the session: the safe screen for close_s, then dark
                if close_s is not None:
                    if close_t0 is None:
                        close_t0 = t
                    p_allowed = C.LOADS["safe screen"] if t - close_t0 < close_s else 0.0
                    if t - close_t0 >= close_s and not session_closed:
                        session_closed = True
                        stats["closed_clean"] = t
                        ev_log.append((t, "Bare tier: session closed and the state saved, body dark"))
                else:
                    p_allowed = min(p_req, C.LOADS["safe screen"])
            else:
                if soc_pack > TH["SOC_CLASS_DELTA"]:
                    p_allowed = min(p_req, cap_cells)
                elif soc_pack > TH["SOC_CLASS_SAFE"]:
                    p_allowed = min(p_req, C.LOADS["delta session"], cap_cells)
                elif soc_pack > TH["SOC_CLOSE"]:
                    p_allowed = min(p_req, C.LOADS["safe screen"])
                else:
                    p_allowed = 0.0
                    if not session_closed:
                        session_closed = True
                        stats["closed_clean"] = t
                        ev_log.append((t, "pack at %.2f: session closed, state saved, body goes dark at the floor" % soc_pack))
        else:  # ISLAND
            p_allowed = 0.0
        if cls in ("standby",) and mode != "ISLAND":
            p_allowed = min(p_req, p_allowed) if p_allowed else p_req
        # ---- ring and body split
        ring_on_vbus = b_seated and mode != "ISLAND"
        p_ring = p_allowed * f_ring
        p_body = p_allowed - p_ring
        p_b_from_cell = 0.0       # W drawn from the B cell
        if not ring_on_vbus:
            # the ring runs from the B cell, capped by U4
            if soc_b > TH["B_SOC_RING_MIN"]:
                p_ring_b = min(p_ring, C.P_RING_CAP)
            else:
                p_ring_b = 0.0
            p_b_from_cell += p_ring_b / TH["ETA_U4"]
            p_vbus_load = p_body if mode != "ISLAND" else 0.0
        else:
            p_vbus_load = p_allowed
        # the B cell charger takes power from VBUS when seated, host present or pack above the float floor
        b_chg = 0.0
        if ring_on_vbus and soc_b < TH["B_SOC_TARGET"] and (mode in ("HOST_FEED", "HOST_TOPUP") or soc_pack > 0.3):
            b_chg = 0.037 * 3.9 / TH["ETA_U4"]
            p_vbus_load += b_chg
        # island rail: U7 and U4 ROM always from the B cell
        p_b_from_cell += C.P_ISLAND / TH["ETA_AON"]
        # ---- solve the bus
        vbus = None
        i_host = 0.0
        i_chg_cmd = 0.0
        if tier == "bare":
            vbus = 3.8 if (store.v > store.vmin and mode != "ISLAND") else 0.0
            p_store_out = (p_vbus_load / store.eta) if vbus else 0.0
            if mode in ("HOST_FEED", "HOST_TOPUP") and vbus:
                # host carries the load; top-up current into the store at most 1 A and 5 W
                p_chg = min(1.0 * store.v, max(p_host_cap - p_vbus_load, 0.0), 5.0) if mode == "HOST_TOPUP" else 0.0
                i_store = -p_chg / max(store.v, 0.1)
                p_store_out = 0.0
                i_host = (p_vbus_load + p_chg) / max(vbus, 1.0)
            elif vbus:
                disc = store.v ** 2 - 4 * store.esr * p_store_out
                if disc < 0:
                    store.v = 0.0
                    i_store = 0.0
                else:
                    i_store = (store.v - math.sqrt(disc)) / (2 * store.esr)
                    if store.v - i_store * store.esr < store.vmin:
                        i_store = 0.0
                        store.v = 0.0
                        vbus = 0.0
            else:
                i_store = 0.0
        else:
            if mode == "ISLAND" or not have_store and not host_ok:
                vbus = 0.0 if not host_ok else None
            if mode in ("HOST_FEED", "HOST_TOPUP"):
                if mode == "HOST_TOPUP":
                    i_chg_cmd = TH["C_TOPUP"] * pk.q_total()
                # fixed point: the host current is limited by the power it can offer into the bus
                v_guess = pk.voc_eff() if pk.n_on() else 3.86
                if pk.n_on() == 0:
                    v_guess = 3.86
                for _ in range(8):
                    i_want = p_vbus_load / max(v_guess, 1.0) + i_chg_cmd
                    i_host = min(i_want, p_host_cap / max(v_guess, 1.0))
                    if pk.n_on() == 0:
                        vbus = 3.86 if i_host * 3.86 >= p_vbus_load * 0.999 else None
                        break
                    vbus = bus_solve(pk, p_vbus_load, i_host)
                    if vbus is None:
                        break
                    if abs(vbus - v_guess) < 1e-4:
                        break
                    v_guess = vbus
            elif mode == "BRIDGE":
                i_host = 0.0
                vbus = bus_solve(pk, p_vbus_load, 0.0) if pk.n_on() else None
                if vbus is None and p_vbus_load > 0:
                    stats["collapse"] += 1
        # ---- the step
        d = min(abs(t - e) for e in edge_times)
        dt = min(max(0.05 * d, 2e-4), 0.5, t_end - t)
        # keep an event inside the step from being jumped over
        nxt = min((e for e in edge_times if e > t + 1e-12), default=t_end)
        dt = min(dt, nxt - t) if nxt - t > 1e-9 else dt
        if tier == "bare":
            if mode in ("HOST_FEED", "HOST_TOPUP") and vbus:
                if mode == "HOST_TOPUP":
                    store.v = min(store.vmax, store.v + (-i_store) * dt / store.C)
            elif vbus and store.v > 0:
                store.v -= i_store * dt / store.C
            if store.v < store.vmin and vbus:
                store.v = 0.0
            stats["e_pack_Wh"] += (store.v * i_store * dt) / 3600.0 if mode == "BRIDGE" else 0.0
            ibat_tot = i_store
        else:
            ibat_tot = 0.0
            if vbus and pk.n_on():
                cur = pk.currents(vbus)
                for k, i in cur.items():
                    pk.soc[k] = min(1.0, max(0.0, pk.soc[k] - i * dt / (3600.0 * pk.n[k] * pk.q_ah)))
                    cr = abs(i) / (pk.n[k] * pk.q_ah)
                    if cr > stats["c_max"] and not pk.joining[k]:
                        stats["c_max"] = cr
                    if pk.joining[k] and abs(vbus - float(C.ocv(pk.soc[k]))) < 0.02:
                        pk.joining[k] = False
                ibat_tot = sum(cur.values())
                stats["e_pack_Wh"] += vbus * ibat_tot * dt / 3600.0
        # ---- the B cell
        p_b_net = p_b_from_cell - (b_chg * TH["ETA_U4"] if b_chg else 0.0)
        soc_b -= p_b_net * dt / (3600.0 * B_CELL["E_Wh"])
        soc_b = min(1.0, max(0.0, soc_b))
        stats["e_b_Wh"] += p_b_net * dt / 3600.0
        i_b = (p_b_from_cell / 3.8)
        v_b = float(C.ocv(soc_b)) - i_b * B_CELL["dcir"]
        v_aon = 1.8 if v_b >= TH["V_AON_MIN"] and soc_b > 0.0 else 0.0
        vsys_b = max(vbus or 0.0, v_b) if b_seated else v_b
        if v_aon < 1.75:
            stats["vaon_dropped"] = True
        stats["vaon_min"] = min(stats["vaon_min"], v_aon)
        if vbus is not None and p_allowed > 0.1:
            stats["vbus_min"] = min(stats["vbus_min"], vbus)
            if vbus < TH["V_SEAT_FLOOR"] and mode != "ISLAND":
                stats["bus_floor_s"] += dt
        if vbus is None and p_vbus_load > 0 and mode != "ISLAND":
            stats["brownout_s"] += dt
        stats["e_host_Wh"] += (min(p_host_cap, (i_host * (vbus or 0.0))) / TH["ETA_UQ"]) * dt / 3600.0 if host_ok else 0.0
        stats["mode_s"][mode] = stats["mode_s"].get(mode, 0.0) + dt
        # ---- the record
        if t >= next_rec - 1e-12 or mode != last_mode:
            log["t"].append(t)
            log["mode"].append(mode)
            log["vhv"].append(vhv)
            log["vbus"].append(vbus if vbus is not None else 0.0)
            log["vsys_b"].append(vsys_b)
            log["vbcell"].append(v_b)
            log["vaon"].append(v_aon)
            log["soc"].append(soc_pack)
            log["soc_b"].append(soc_b)
            log["p_load"].append(p_allowed)
            log["p_host"].append(i_host * (vbus or 0.0))
            log["i_host"].append(i_host)
            next_rec = t + record_dt
            last_mode = mode
        t += dt
    stats["n_events"] = len(ev_log)
    return dict(name=name, tier=tier, log=log, events=ev_log, stats=stats, final_soc=(pk.mean_soc() if pk else store.soc()))


# ------------------------------------------------------------------ the scenarios
def scenarios():
    S = []
    # S1 desk dock -> walk 4 min -> vehicle. 12 V host from the dock pads, then a vehicle cradle with a PD contract of 350 ms,
    # and a cranking dropout of 0.9 s inside the vehicle segment.
    t_dock, t_lift, t_veh = 60.0, 60.0, 300.0
    hosts = [Host(0.0, t_lift, 12.0, 25.0, 0.0, name="H0 desk dock pads"),
             Host(t_veh, 480.0, 12.0, 25.0, 0.35, dips=[(t_veh + 60.0, t_veh + 61.25, 0.0)], name="H3 vehicle cradle")]
    sess = [(0.0, "delta session")]
    S.append(dict(id="S1", title="desk dock, 60 s, walk 4 min with a delta session, vehicle with a cranking dropout of 0.9 s and a 0.35 s PD re-contract",
                  hosts=hosts, session=sess, t_end=480.0, soc0=0.35, kwargs={}))
    # S2 host brownout, 12 V pad, delta session; a short dip of 150 ms to 6 V and a long dip of 2 s to 0 V
    hosts = [Host(0.0, 60.0, 12.0, 25.0, 0.0, dips=[(20.0, 20.15, 6.0), (40.0, 42.0, 0.0)], name="host with brownouts")]
    S.append(dict(id="S2", title="host brownout: 150 ms to 6 V at 20 s, 2 s to 0 V at 40 s, delta session",
                  hosts=hosts, session=[(0.0, "delta session")], t_end=60.0, soc0=0.50, kwargs={}))
    # S3 host vanishes mid-session: video session, pad host vanishes at 30 s, nobody returns
    hosts = [Host(0.0, 30.0, 12.0, 25.0, 0.0, name="host that vanishes")]
    S.append(dict(id="S3", title="host vanishes at 30 s in a video session, no new host: graceful close and the island",
                  hosts=hosts, session=[(0.0, "video")], t_end=9000.0, soc0=0.55, kwargs=dict(record_dt=10.0)))
    # S4 quadrant hot swap, B seated on the removed quadrant, host feeding through another seat
    hosts = [Host(0.0, 60.0, 12.0, 25.0, 0.0, name="host through the Q1 seat")]
    ev = [(20.0, "quad_out", 2), (20.0, "b_off", None), (23.0, "quad_in", (2, 5, 0.30)), (23.0, "b_on", None)]
    S.append(dict(id="S4", title="hot swap of Q3 at 20 s, B module on the Q3 seat, host on Q1, 3 s swap",
                  hosts=hosts, session=[(0.0, "delta session")], events=ev, t_end=60.0, soc0=0.50, kwargs={}))
    # S5 quadrant swap with no host: cells evenly spread against all cells in the removed quadrant
    hosts = []
    ev = [(20.0, "quad_out", 2), (23.0, "quad_in", (2, 5, 0.30))]
    S.append(dict(id="S5a", title="no host, quadrant swap, Buffer cells spread evenly (5 per quadrant)",
                  hosts=hosts, session=[(0.0, "delta session")], events=ev, t_end=60.0, soc0=0.60,
                  kwargs=dict(n_q=(5, 5, 5, 5))))
    ev = [(20.0, "quad_out", 2), (23.0, "quad_in", (2, 20, 0.30))]
    S.append(dict(id="S5b", title="no host, quadrant swap, all 20 Buffer cells in the removed quadrant",
                  hosts=hosts, session=[(0.0, "delta session")], events=ev, t_end=60.0, soc0=0.60,
                  kwargs=dict(n_q=(0, 0, 20, 0))))
    # S6 a weak host: a 5 W low-power pad (H6) against the outdoor video session of 7.5 W
    hosts = [Host(0.0, 900.0, 12.0, 5.0, 0.0, name="H6 5 W pad")]
    S.append(dict(id="S6", title="weak host: 5 W pad at the rectifier, outdoor video 7.5 W for 15 min, pack assists",
                  hosts=hosts, session=[(0.0, "outdoor")], t_end=900.0, soc0=0.55, kwargs=dict(record_dt=2.0)))
    return S


def summarize(res):
    s = res["stats"]
    return dict(
        name=res["name"], tier=res["tier"], vaon_min=s["vaon_min"], vaon_dropped=s["vaon_dropped"],
        vbus_min=s["vbus_min"], bus_below_seat_floor_s=s["bus_floor_s"], brownout_s=s["brownout_s"],
        collapse_steps=s["collapse"], c_rate_max=s["c_max"], e_from_host_Wh=s["e_host_Wh"],
        e_pack_Wh=s["e_pack_Wh"], e_bcell_Wh=s["e_b_Wh"], mode_seconds=s["mode_s"], closed_clean_at_s=s["closed_clean"],
        final_soc=res["final_soc"], soc_b_final=res["log"]["soc_b"][-1])


def main():
    L = []

    def p(s=""):
        L.append(s)
        print(s)

    p("POWER-PATH · question 2 · power path simulator")
    p("thresholds: " + ", ".join("%s=%s" % kv for kv in TH.items()))
    p("")
    out = {"thresholds": TH, "scenarios": {}}
    runs = []
    for sc in scenarios():
        variants = []
        kw = sc["kwargs"]
        variants.append(("Buffer 20 cells S, float 60 %", "buffer", dict(kw)))
        if sc["id"] in ("S1", "S3", "S6"):
            variants.append(("Full 128 cells S", "buffer", dict(kw, n_q=(32, 32, 32, 32))))
        for vname, tier, k2 in variants:
            r = run(sc["id"] + " " + vname, tier, sc["hosts"], sc["session"], events=sc.get("events", ()), t_end=sc["t_end"],
                    soc0=sc["soc0"], **k2)
            runs.append((sc, vname, r))
        if sc["id"] in ("S1", "S2", "S3"):
            # Bare: 0.23 cm3 of the large-cell EDLC density (3 tiles), session closes after 3 s
            tech_c = 6.3  # F/cm3
            vol = 0.23
            capst = CapStore(C_F=tech_c * vol, esr=0.109 / vol, vmax=2.7, vmin=1.35)
            r = run(sc["id"] + " Bare, 0.23 cm3 EDLC, close in 3 s", "bare", sc["hosts"], sc["session"],
                    events=sc.get("events", ()), t_end=sc["t_end"], soc0=sc["soc0"], cap=capst, close_s=3.0,
                    **{k: v for k, v in sc["kwargs"].items() if k == "record_dt"})
            runs.append((sc, "Bare, 0.23 cm3 EDLC, close in 3 s", r))

    cur = None
    for sc, vname, r in runs:
        if cur != sc["id"]:
            cur = sc["id"]
            p("=" * 100)
            p("%s  %s" % (sc["id"], sc["title"]))
        sm = summarize(r)
        out["scenarios"][r["name"]] = dict(summary=sm, events=r["events"])
        p("-" * 100)
        p("%s" % vname)
        for t, msg in r["events"]:
            if len(r["events"]) > 40 and t > 0 and "mode" not in msg and "close" not in msg:
                continue
            p("  t=%8.3f s  %s" % (t, msg))
        lg = r["log"]
        vb = [v for v in lg["vbus"] if v > 0]
        p("  rails: VHV %.1f..%.1f V | VBUS %.3f..%.3f V | VSYS_B min %.3f V | V_BCELL min %.3f V | 1V8_AON min %.2f V"
          % (min(lg["vhv"]), max(lg["vhv"]), min(vb) if vb else 0, max(vb) if vb else 0, min(lg["vsys_b"]), min(lg["vbcell"]), sm["vaon_min"]))
        p("  pack SOC %.3f -> %.3f (min %.3f) | B cell SOC %.3f -> %.3f (min %.3f) | peak cell C-rate %.2f C"
          % (lg["soc"][0], lg["soc"][-1], min(lg["soc"]), lg["soc_b"][0], lg["soc_b"][-1], min(lg["soc_b"]), sm["c_rate_max"]))
        p("  mode seconds: " + ", ".join("%s %.1f" % kv for kv in sm["mode_seconds"].items()))
        p("  energy: from host %.3f Wh, net from pack %.3f Wh (negative = charged), net from B cell %.4f Wh | bus below the 3.40 V seat floor %.3f s, bus collapse %.3f s"
          % (sm["e_from_host_Wh"], sm["e_pack_Wh"], sm["e_bcell_Wh"], sm["bus_below_seat_floor_s"], sm["brownout_s"]))
        p("  ISLAND RAIL (secure element and U4 ROM): %s, minimum %.2f V" % ("DROPPED" if sm["vaon_dropped"] else "never dropped", sm["vaon_min"]))
    out["island_never_dropped"] = all(not r["stats"]["vaon_dropped"] for _, _, r in runs)
    p("")
    p("ISLAND RAIL OVER ALL %d RUNS: %s" % (len(runs), "never dropped" if out["island_never_dropped"] else "DROPPED in at least one run"))
    C.dump("powerpath", out, L)
    plots(runs)


def plots(runs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def pick(sid, vname):
        for sc, v, r in runs:
            if sc["id"] == sid and v.startswith(vname):
                return r
        return None

    for sid, vnames, fn in (("S1", ["Buffer", "Bare"], "pp_S1.png"), ("S3", ["Buffer", "Full"], "pp_S3.png"),
                            ("S4", ["Buffer"], "pp_S4.png"), ("S6", ["Buffer", "Full"], "pp_S6.png"), ("S2", ["Buffer"], "pp_S2.png"),
                            ("S5a", ["Buffer"], "pp_S5a.png"), ("S5b", ["Buffer"], "pp_S5b.png")):
        fig, ax = plt.subplots(4, 1, figsize=(9, 8), sharex=True)
        for j, vn in enumerate(vnames):
            r = pick(sid, vn)
            if r is None:
                continue
            lg = r["log"]
            t = np.array(lg["t"])
            col = C.PAL[j]
            ax[0].plot(t, lg["vhv"], color=col, lw=1.2, label=vn)
            ax[1].plot(t, lg["vbus"], color=col, lw=1.2, label="VBUS " + vn)
            if j == 0:
                ax[1].plot(t, lg["vsys_b"], color="#888", lw=0.9, ls="--", label="VSYS_B")
                ax[1].plot(t, lg["vaon"], color="#222", lw=0.9, ls=":", label="1V8_AON")
            ax[2].plot(t, lg["soc"], color=col, lw=1.2, label="pack SOC " + vn)
            ax[2].plot(t, lg["soc_b"], color=col, lw=0.9, ls="--", label="B cell SOC " + vn)
            ax[3].plot(t, lg["p_load"], color=col, lw=1.2, label="allowed load " + vn)
        C.style(ax[0], "", "VHV, V")
        C.style(ax[1], "", "rails, V")
        C.style(ax[2], "", "SOC")
        C.style(ax[3], "time, s", "load, W")
        ax[1].legend(fontsize=7, ncol=4, frameon=False, loc="lower left")
        ax[2].legend(fontsize=7, ncol=2, frameon=False)
        ax[0].legend(fontsize=7, frameon=False)
        sc = next(s for s, v, r in runs if s["id"] == sid)
        ax[0].set_title("%s  %s" % (sid, sc["title"]), fontsize=9, loc="left")
        fig.tight_layout()
        fig.savefig(C.OUT + "/" + fn, dpi=110)
        plt.close(fig)


if __name__ == "__main__":
    main()
