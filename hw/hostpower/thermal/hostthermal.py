#!/usr/bin/env python3
"""hostthermal.py - the host-power layer on top of sim/thermal/leaf_thermal.py.

Team THERMAL of hw/hostpower. Condition 2 of the Host Life Law (BRIEF Section 5):
the hottest face point stays at or under 36.2 C for the whole session.

This file imports the L.6.0 thermal network read only. It adds
  * the three session maps (delta, video Wi-Fi, 5G outdoor),
  * the host interfaces: battery, contact (bar pads or dock pads), Qi BPP, EPP, MPP,
  * the heat vector of each interface with the cell floating or topping up,
  * the three environments: free air, Qi puck, dock cold plate,
  * the sustained-power search and the throttle fixed point.

Every material number is [HYPOTHESIS] unless the README names a source.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True          # never write __pycache__ next to read-only sources

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sim", "thermal"))
import leaf_thermal as LT                                   # noqa: E402
from leaf_thermal import (Config, Network, NT, NL, LAYERS, derate,       # noqa: E402
                          charge_losses, dist_alpha, coil_map, lead_tiles, tid)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


DOCK_DIR = os.path.join(ROOT, "hw", "dock")
sys.path.insert(0, DOCK_DIR)
DB = _load("dock_budget", os.path.join(DOCK_DIR, "budget.py"))   # read only, main() not run
DP = DB.P                                                         # hw/dock/params.py

T_LIM = 36.2

# --------------------------------------------------------------------------
# the body: the L.6.0 fixed body F1 to F4 of sim/thermal/run_all.py
# --------------------------------------------------------------------------
BASE = Config(name="baseline")
FIX = BASE.copy(name="fixed", hinge_kind="graphite", hinge_leaves=3, landing=1.5e-3,
                spreader_kt=0.14, ring_pad_full=True, h_ring_pad=3000.0,
                G_ring_bar=0.08, h_bar=3000.0)
WIND = dict(h_front=12.0, h_back=12.0, h_ring=12.0)       # light wind, as the 5G case

# --------------------------------------------------------------------------
# the sessions
# --------------------------------------------------------------------------
_V = LT.SESSIONS["video"]
_G = LT.SESSIONS["5g_outdoor"]
_ring_video_scale = 1.92 / sum(_V["ring"].values())       # hw/energy: video Wi-Fi ring 1.92 W

SESS = {
    # the thermal team map (a) of 2.50 W, called delta here (FINAL/21 "2 to 3 W" session)
    "delta": dict(tiles=sum(_V["tiles"].values()),
                  ring=dict(_V["ring"]), nits_note="map (a) of sim/thermal"),
    # hw/energy video session, Wi-Fi: body 1.35 W, ring 1.92 W, ring split of map (a)
    "video_wifi": dict(tiles=1.10 + 0.25,
                       ring={k: v * _ring_video_scale for k, v in _V["ring"].items()},
                       nits_note="hw/energy video session"),
    # the thermal team map (c) of 4.18 W, with the light wind
    "5g_outdoor": dict(tiles=sum(_G["tiles"].values()), ring=dict(_G["ring"]),
                       nits_note="map (c) of sim/thermal"),
}
DISPLAY_W = {"delta": 1.00, "video_wifi": 1.10, "5g_outdoor": 1.80}   # display term of each map
SESS_WIND = {"delta": False, "video_wifi": False, "5g_outdoor": True}


def sess_total(name):
    s = SESS[name]
    return s["tiles"] + sum(s["ring"].values())


# FINAL/17 Section 17.13: P_display = 0.60 W * (nits / 250) * (APL / 35 %)
def nits_at_apl35(p_display):
    return 250.0 * p_display / 0.60


def apl_at_250nits(p_display):
    return 35.0 * p_display / 0.60


# --------------------------------------------------------------------------
# the interfaces
# --------------------------------------------------------------------------
# kind: battery | contact | qi.  cap = highest received power after the Leaf rectifier.
IFACES = {
    "battery": dict(kind="battery", label="battery only"),
    # the same battery Leaf lying on a table: the support of the Qi case, with no host power
    "battery_table": dict(kind="battery", pad="puck", label="battery, on a table"),
    "contact_lo": dict(kind="contact", loss=0.10, cap=25.0, label="contact, 0.10 W loss"),
    "contact_hi": dict(kind="contact", loss=0.34, cap=25.0, label="contact, 0.34 W loss"),
    # physics check of the two bounds: hw/energy bar_pins 5.7 mW at 1.92 W, worn pad x3.97 (0.31/0.078)
    "contact_i2r": dict(kind="contact", loss=0.0, loss_k=3.97 * 5.7e-3 / 1.92 ** 2, cap=25.0,
                        label="contact, I2R of a worn pad"),
    "qi_bpp": dict(kind="qi", cap=5.0, V_rect=5.0, label="Qi BPP 5 W"),
    "qi_epp": dict(kind="qi", cap=15.0, V_rect=12.0, label="Qi EPP 15 W"),
    "qi_mpp": dict(kind="qi", cap=25.0, V_rect=15.0, label="Qi2.2 MPP 25 W"),
}
QI_NAMES = ("qi_bpp", "qi_epp", "qi_mpp")
PUCK_DT_AT_25W = 5.0          # K above ambient of a passive puck at 25 W received (sim/thermal ambient sweep)
C_TOPUP_LOW = 0.2             # C-rate of the low top-up, on E_body
E_BODY = FIX.E_body_Wh


def R_cell(cfg):
    return cfg.cell_ohm_mAh / (cfg.E_body_Wh / NT / cfg.V_cell * 1000)


def cell_heat(cfg, P_net):
    """I2R of all cells at a net cell power P_net (W, either sign)."""
    I_cell = abs(P_net) / cfg.V_cell / NT
    return NT * I_cell ** 2 * R_cell(cfg)


# --------------------------------------------------------------------------
# index helpers (vectorised heat vector)
# --------------------------------------------------------------------------
_net0 = Network(FIX)
IDX = {L: np.array([_net0.nid(t, L) for t in range(NT)]) for L in LAYERS}
I_PCB, I_SHELL, I_BAR = _net0.rid("ring_pcb"), _net0.rid("ring_shell"), _net0.rid("bar")
CM = coil_map()
W_COIL = CM / CM.sum()
LEAD = lead_tiles(FIX)
SEAT = tid(*FIX.seat_tile)


# --------------------------------------------------------------------------
# the heat vector
# --------------------------------------------------------------------------
def load_q(name, st=1.0, sr=1.0):
    """Heat of the session loads only. Tiles scale st, ring chips scale sr."""
    s = SESS[name]
    q = np.zeros(_net0.n)
    q[IDX["F"]] += st * s["tiles"] / NT
    q[I_PCB] += sr * sum(s["ring"].values())
    return q, st * s["tiles"] + sr * sum(s["ring"].values())


def _solve_input(cfg, P_L, target, cap, chain):
    """Find the host input P_in <= cap whose chain puts P_L + target at the cells.

    chain(P_in) -> P_out at the charger output. The lattice and leaves take
    alpha * P_out^2. net = P_out - lattice - leaves - P_L is the cell power.
    Returns P_in, P_out, net, host_limited (the cap binds before the load is met).
    """
    tot, per, leaves, _ = dist_alpha(cfg)
    a = float(tot + leaves)

    def net(P_in):
        P_out = chain(P_in)
        return P_out - a * P_out ** 2 - P_L, P_out

    if net(cap)[0] <= target:
        n, Po = net(cap)
        return cap, Po, n, bool(n < -1e-9)       # host limited: the cap cannot feed the load
    lo, hi = 0.0, cap
    for _ in range(50):
        m = 0.5 * (lo + hi)
        if net(m)[0] < target:
            lo = m
        else:
            hi = m
    P_in = 0.5 * (lo + hi)
    n, Po = net(P_in)
    return P_in, Po, n, False


def heat(name, iface, mode="float", st=1.0, sr=1.0, cfg=FIX, dock=False):
    """Heat vector and bookkeeping of one operating point.

    mode: float            the host feeds the load, the cell current is zero
          topup            the cell gains C_TOPUP_LOW * E_body in addition
          charge           the host input sits at its cap, the cell takes the rest
          c<number>        the cell charges at that C-rate (for example c1.0)
    """
    spec = IFACES[iface]
    q, P_L = load_q(name, st, sr)
    info = dict(P_L=P_L, iface=iface, mode=mode)
    tot, per, leaves, _ = dist_alpha(cfg)
    if spec["kind"] == "battery":
        P_net = -P_L
        q[IDX["C"]] += cell_heat(cfg, P_L) / NT
        q[IDX["C"]] += per * P_L ** 2
        q[I_BAR] += leaves * P_L ** 2
        info.update(P_in=0.0, P_out=P_L, P_net=P_net, host_limited=False,
                    P_host=0.0, P_wall=0.0, heat_path=float(cell_heat(cfg, P_L) + (tot + leaves) * P_L ** 2),
                    tx_coil_loss=0.0, P_rx=0.0)
        info["Q_leaf"] = float(q.sum())
        return q, info

    target = {"float": 0.0, "topup": C_TOPUP_LOW * E_BODY}.get(mode)
    if mode == "charge":
        target = 1e9
    elif mode.startswith("c"):
        target = float(mode[1:]) * E_BODY
    cap = spec["cap"]

    if spec["kind"] == "contact":
        if mode == "float":
            # the host regulates the VBUS leaves; the Leaf takes the load only.
            P_out = P_L + (tot + leaves) * P_L ** 2
            P_in, P_net, lim = P_L, 0.0, False
            chg_loss = 0.0
        else:
            # VHV at 12 V through the 3:1 charger of the ring (eta_chg), cell charges
            chain = lambda Pi: Pi * cfg.eta_chg
            P_in, P_out, P_net, lim = _solve_input(cfg, P_L, target, cap, chain)
            chg_loss = P_in * (1 - cfg.eta_chg)
        q[I_PCB] += chg_loss
        q[IDX["C"]] += per * P_out ** 2
        # the interface loss replaces the leaves term: it sits at the 12 pads of the seat tile
        loss_if = spec["loss"] + spec.get("loss_k", 0.0) * P_out ** 2
        q[IDX["C"][SEAT]] += loss_if
        if mode != "float":
            q[IDX["C"]] += cell_heat(cfg, P_net) / NT
        host_in = (P_in if mode != "float" else P_out) + loss_if
        info.update(P_in=P_in, P_out=P_out, P_net=P_net, host_limited=bool(lim),
                    P_host=host_in, P_wall=host_in / DP.ETA_CONTACT_BB, tx_coil_loss=0.0,
                    P_rx=P_in, heat_path=float(q.sum() - P_L))
        info["Q_leaf"] = float(q.sum())
        return q, info

    # Qi
    ccfg = cfg.copy(V_rect=spec["V_rect"])

    def chain(Prx):
        return Prx * ccfg.eta_chg

    P_rx, P_out, P_net, lim = _solve_input(ccfg, P_L, target, cap, chain)
    L = charge_losses(ccfg, P_rx)
    q[IDX["S"]] += (L["coil"] + L["shield_eddy"]) * W_COIL
    q[IDX["S"][LEAD]] += L["ac_lead"] / len(LEAD)
    q[I_PCB] += L["rectifier"] + L["charger"]
    q[IDX["C"]] += per * P_out ** 2
    q[I_BAR] += leaves * P_out ** 2
    q[IDX["C"]] += cell_heat(ccfg, P_net) / NT
    P_pad = P_rx + L["coil"] + L["shield_eddy"] + L["ac_lead"] + L["rectifier"]   # into the Leaf coil
    tx_coil = P_pad * (1 / DP.ETA_TX_COIL - 1)
    P_dc = P_pad / DP.ETA_TX_COIL / DP.ETA_INVERTER / DP.ETA_TX_FRONT
    info.update(P_in=P_rx, P_out=P_out, P_net=P_net, host_limited=bool(lim), P_rx=P_rx,
                P_host=P_pad, P_wall=P_dc, tx_coil_loss=tx_coil,
                heat_path=float(q.sum() - P_L), losses={k: float(v) for k, v in L.items()
                                                       if not k.startswith("_") and k != "cells_I2R"})
    info["Q_leaf"] = float(q.sum())
    return q, info


# --------------------------------------------------------------------------
# the environments
# --------------------------------------------------------------------------
_TEC_QMAX = {}


def tec_qmax(amb):
    """Highest heat the dock TEC pumps at the 22 C set-point, by bisection (hw/dock/budget.py)."""
    key = round(amb, 3)
    if key not in _TEC_QMAX:
        lo, hi = 0.0, 32.0
        if DB.solve_tec(amb, hi) is not None:
            _TEC_QMAX[key] = hi
        else:
            for _ in range(10):
                m = 0.5 * (lo + hi)
                if DB.solve_tec(amb, m) is not None:
                    lo = m
                else:
                    hi = m
            _TEC_QMAX[key] = lo
    return _TEC_QMAX[key]


class Env:
    """One thermal environment: ambient, wind, and the surface under the Leaf.

    pad: free   the Leaf hangs in air or lies on a bad conductor (a bar pad host, a hand-held host)
         puck   a passive Qi puck, Ø58 mm, at ambient plus a rise that follows P_rx
         dock   the full-face dock cold plate, regulated at 22 C (hw/dock), TEC checked
    """

    def __init__(self, amb, wind, pad, body=FIX):
        self.amb, self.wind, self.pad = amb, wind, pad
        c = body.copy(T_amb=amb, **(WIND if wind else {}))
        if pad == "puck":
            c = c.copy(pad="puck", T_pad=20.0)
        elif pad == "dock":
            c = c.copy(pad="leafpad", T_pad=20.0)
        self.cfg = c
        self.net = Network(c)
        if pad != "free":
            c2 = c.copy(T_pad=30.0)
            n2 = Network(c2)
            self.gpad = (n2.GbT - self.net.GbT) / 10.0
        else:
            self.gpad = np.zeros(self.net.n)
        self.lu = spla.splu((self.net.G + sp.diags(self.net.Gb)).tocsc())

    def pad_temp(self, info):
        if self.pad == "puck":
            return self.amb + max(1.0, PUCK_DT_AT_25W * info["P_rx"] / 25.0)
        if self.pad == "dock":
            return DP.PAD_SETPOINT
        return 20.0

    def tec_ok(self, info):
        if self.pad != "dock":
            return True
        q_need = (info["Q_leaf"] * DP.F_DEVICE_HEAT_TO_PAD + info["tx_coil_loss"]
                  + DP.UA_PAD_LEAK * (self.amb - DP.PAD_SETPOINT))
        return q_need <= tec_qmax(self.amb)

    def solve(self, q, info):
        Tp = self.pad_temp(info)
        rhs = q + self.net.q_fixed + self.net.GbT + (Tp - 20.0) * self.gpad
        return self.lu.solve(rhs)

    def read(self, q, info):
        T = self.solve(q, info)
        r = self.net.readout(T)
        n = self.net
        cands = {
            "front tile cap": max(T[n.nid(t, "FS")] for t in range(NT)),
            "back skin": r["T_back_max"],
            "ring shell": r["T_ring_shell"],
            "bar": r["T_bar"],
        }
        where = max(cands, key=cands.get)
        r["where"] = where
        r["T_gate"] = r["T_surface_max"]
        r["T_pad"] = self.pad_temp(info)
        return r


_ENV = {}


def env(amb, wind, pad, body="fixed"):
    key = (amb, wind, pad, body)
    if key not in _ENV:
        _ENV[key] = Env(amb, wind, pad, FIX if body == "fixed" else BASE)
    return _ENV[key]


def iface_pad(iface, plate):
    if plate:
        return "dock"
    if IFACES[iface].get("pad"):
        return IFACES[iface]["pad"]
    return "puck" if IFACES[iface]["kind"] == "qi" else "free"


def point(name, iface, mode, amb, wind, plate, st=1.0, sr=1.0, body="fixed"):
    """One steady operating point. Returns the readout merged with the heat bookkeeping."""
    e = env(amb, wind, iface_pad(iface, plate), body)
    cfg = e.cfg
    q, info = heat(name, iface, mode, st, sr, cfg=FIX if body == "fixed" else BASE,
                   dock=(plate and IFACES[iface]["kind"] == "contact"))
    r = e.read(q, info)
    r.update({k: v for k, v in info.items() if k != "losses"})
    r["losses"] = info.get("losses", {})
    r["tec_ok"] = e.tec_ok(info)
    charging = info["P_net"] > 0.05
    r["cell_ok"] = r["T_cell_max"] <= (FIX.T_cell_chg_lim if charging else FIX.T_cell_dis_lim)
    r["skin_ok"] = r["T_gate"] <= T_LIM
    return r


def ok_point(r):
    return r["skin_ok"] and r["cell_ok"] and r["tec_ok"]


# --------------------------------------------------------------------------
# the sustained power
# --------------------------------------------------------------------------
def sustained(name, iface, mode, amb, wind, plate, hi=4.0, iters=26):
    """Largest session scale that holds 36.2 C, and the largest the host input carries.

    Returns dict(s_thermal, s_cap, s_adm, P_thermal, P_cap, P_adm, limit).
    """
    def thermal_ok(s):
        return ok_point(point(name, iface, mode, amb, wind, plate, s, s))

    def cap_ok(s):
        _, info = heat(name, iface, mode, s, s, cfg=FIX)
        return not info["host_limited"]

    def search(f):
        if not f(0.0):
            return 0.0
        if f(hi):
            return hi
        lo_, hi_ = 0.0, hi
        for _ in range(iters):
            m = 0.5 * (lo_ + hi_)
            if f(m):
                lo_ = m
            else:
                hi_ = m
        return lo_

    st_ = search(thermal_ok)
    kind = IFACES[iface]["kind"]
    if kind == "battery":
        sc = hi
    else:
        sc = search(cap_ok)
    sa = min(st_, sc)
    P = sess_total(name)
    return dict(s_thermal=st_, s_cap=sc, s_adm=sa, P_thermal=st_ * P, P_cap=sc * P, P_adm=sa * P,
                limit=("thermal" if st_ <= sc else "host cap"), always_on=bool(sa >= 1.0 - 1e-6))


# --------------------------------------------------------------------------
# the throttle: steady fixed point of the existing law
# --------------------------------------------------------------------------
def throttle_steady(name, iface, mode, amb, wind, plate, display_only=False, iters=30):
    """Steady state of the throttle law of sim/thermal (derate on the hottest surface).

    whole session: the display, the stream and the radio scale together (the law of run_all.py).
    display only:  the tiles scale, the ring chips stay at their power (a picture-level throttle).
    Returns the held scale s = derate(T(s)). The existing floor is 0.30.
    """
    def T_of(s):
        st, sr = (s, 1.0) if display_only else (s, s)
        r = point(name, iface, mode, amb, wind, plate, st, sr)
        return r

    def holds(s):
        r = T_of(s)
        return (s <= derate(r["T_gate"], T_LIM) + 1e-12) and r["tec_ok"] and not r["host_limited"]

    if holds(1.0):
        return dict(s=1.0, T=T_of(1.0)["T_gate"], state="full")
    if not holds(0.0):
        return dict(s=0.0, T=T_of(0.0)["T_gate"], state="off")
    lo, hi = 0.0, 1.0
    for _ in range(iters):
        m = 0.5 * (lo + hi)
        if holds(m):
            lo = m
        else:
            hi = m
    r = T_of(lo)
    state = "throttled" if lo >= 0.30 else "below the 30 % floor"
    return dict(s=lo, T=r["T_gate"], state=state)
