#!/usr/bin/env python3
"""coreheat.py - the heat of the Split: the Skin alone and the Core alone.

Seat HEAT of hw/core (block HP-2). The Split moves the silicon, the radios and the energy
off the surface. The Skin keeps the emitters, the tile drivers, a link PHY and a minimal
decoder. The Core keeps the rest.

This file imports hw/hostpower/thermal/hostthermal.py (and through it sim/thermal and hw/dock)
read only. Every number is [HYPOTHESIS] unless the README names a source.
"""
import math
import os
import sys

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "hw", "hostpower", "thermal"))
import hostthermal as H                       # noqa: E402
import eyewear as EW                          # noqa: E402
from leaf_thermal import NT, derate, dist_alpha, tid    # noqa: E402

LIM = 36.2
IDX = H.IDX
SEAT = tid(*H.FIX.seat_tile)

# --------------------------------------------------------------------------
# the Skin: the fixed L.6.0 body with no B ring and no bar load
# --------------------------------------------------------------------------
# The ring footprint is taken out by a ring radius of 1 nm: no cover on the face, no pad, no ring heat.
SKIN_CFG = H.FIX.copy(name="skin", ring_ro=1e-9, ring_ri=0.0)
SKIN_BASELINE = H.BASE.copy(name="skin_unfixed", ring_ro=1e-9, ring_ri=0.0)

# display plus address loads of the Skin, W (display, address). Sources named in the README.
LOADS = {
    "delta_energy": (0.60, 0.20),      # hw/energy body column, 0.80 W
    "delta_thermal": (1.00, 0.25),     # sim/thermal map (a) tiles, 1.25 W
    "video": (1.10, 0.25),             # hw/energy body column, 1.35 W
    "5g_like": (1.80, 0.30),           # sim/thermal map (c) tiles, 2.10 W
    "outdoor_800nit": (3.84, 0.40),    # hw/energy outdoor video, 4.24 W
}
LABEL = {"delta_energy": "delta 0.80 W", "delta_thermal": "delta 1.25 W (map a)", "video": "video 1.35 W",
         "5g_like": "5G-like 2.10 W", "outdoor_800nit": "outdoor 800 nit 4.24 W"}
PHY_SWEEP = (0.15, 0.25, 0.35)
FEEDS = {"cells": "own cells, no host", "feed010": "contact feed, 0.10 W loss", "feed034": "contact feed, 0.34 W loss"}

_ENV = {}


def env(amb, wind, pad="free", body="fixed"):
    key = (amb, wind, pad, body)
    if key not in _ENV:
        _ENV[key] = H.Env(amb, wind, pad, SKIN_CFG if body == "fixed" else SKIN_BASELINE)
    return _ENV[key]


def solve_T(e, q, T_pad=20.0):
    rhs = q + e.net.q_fixed + e.net.GbT + (T_pad - 20.0) * e.gpad
    return e.lu.solve(rhs)


def skin_q(load, s=1.0, phy=0.25, place="dist", feed="cells", extra=0.0, extra_place="seat", cfg=SKIN_CFG):
    """Heat vector of the Skin.

    load   key of LOADS. s scales the display and address loads. phy is the link PHY and decoder, W.
    place  dist: the PHY and decoder load spreads over all tiles in the driver layer.
           seat: the PHY and decoder sit on the seat tile.
    feed   cells: own cells, I2R and the lattice. feed010 / feed034: a contact feed, the cell floats.
    extra  an additional power-path loss at the Skin end, W, on the seat tile.
    """
    d, a = LOADS[load]
    q = np.zeros(H._net0.n)
    p_disp = s * (d + a)
    q[IDX["F"]] += p_disp / NT
    if place == "dist":
        q[IDX["F"]] += phy / NT
    else:
        q[IDX["F"][SEAT]] += phy
    if extra:
        if extra_place == "seat":
            q[IDX["C"][SEAT]] += extra
        else:
            q[IDX["C"]] += extra / NT
    P_el = p_disp + phy + extra           # electric power through the lattice
    tot, per, leaves, _ = dist_alpha(cfg)
    q[IDX["C"]] += per * P_el ** 2
    if feed == "cells":
        q[IDX["C"]] += H.cell_heat(cfg, P_el) / NT
    elif feed in ("feed010", "feed034"):
        q[IDX["C"][SEAT]] += 0.10 if feed == "feed010" else 0.34
    # feed "none": the power path loss is the argument extra, and the cell is absent
    return q, dict(P_disp=p_disp, P_el=P_el, Q=float(q.sum()))


def skin_T(q, amb, wind, pad="free", T_pad=20.0, body="fixed"):
    e = env(amb, wind, pad, body)
    T = solve_T(e, q, T_pad)
    n = e.net
    fs = T[IDX["FS"]]
    kk = T[IDX["K"]]
    t_fs, t_k = float(fs.max()), float(kk.max())
    if t_fs >= t_k:
        t = int(np.argmax(fs)); layer = "front cap"
    else:
        t = int(np.argmax(kk)); layer = "back skin"
    hot = dict(T=max(t_fs, t_k), layer=layer, tile=(t % 8, t // 8), T_front=t_fs, T_back=t_k,
               T_cell_max=float(T[IDX["C"]].max()), T_ring_shell=float(T[H.I_SHELL]),
               T_mean_front=float(fs.mean()))
    return hot


def sustained_skin(load, amb, wind, phy=0.25, place="dist", feed="cells", extra=0.0, pad="free",
                   T_pad=20.0, T_lim=LIM, hi=None, iters=34, extra_place="seat"):
    """Largest scale of the display and address load that holds T_lim, and the powers at that scale."""
    if hi is None:
        hi = 30.0 / sum(LOADS[load])           # up to 30 W of display and address power

    def ok(s):
        q, _ = skin_q(load, s, phy, place, feed, extra, extra_place)
        return skin_T(q, amb, wind, pad, T_pad)["T"] <= T_lim
    if not ok(0.0):
        return dict(s=0.0, P_disp_addr=0.0, P_display=0.0, ok0=False)
    if ok(hi):
        s = hi
    else:
        lo, h = 0.0, hi
        for _ in range(iters):
            m = 0.5 * (lo + h)
            if ok(m):
                lo = m
            else:
                h = m
        s = lo
    d, a = LOADS[load]
    return dict(s=s, P_disp_addr=s * (d + a), P_display=s * d, ok0=True)


def picture(p_display):
    """FINAL/17 Section 17.13: P_display = 0.60 W x (nits / 250) x (APL / 35 %)."""
    return dict(nits_at_apl35=250.0 * p_display / 0.60, apl_at_250=35.0 * p_display / 0.60,
                nits_full_white=250.0 * p_display / 0.60 * 35.0 / 100.0,
                apl_at_800=35.0 * p_display / (0.60 * 800 / 250))


# --------------------------------------------------------------------------
# the Core: a sealed box
# --------------------------------------------------------------------------
SIGMA = 5.670374e-8
BOXES = {
    "S 90x60x18": (0.090, 0.060, 0.018),
    "M 140x90x30": (0.140, 0.090, 0.030),
    "L 200x130x45": (0.200, 0.130, 0.045),
    "XL 300x200x70": (0.300, 0.200, 0.070),
}


def _h_nat(dT, L, kind):
    dT = max(dT, 1e-6)
    if kind == "vert":
        return max(1.42 * (dT / L) ** 0.25, 1.31 * dT ** (1 / 3))
    if kind == "up":
        return max(1.32 * (dT / L) ** 0.25, 1.52 * dT ** (1 / 3))
    return 0.59 * (dT / L) ** 0.25          # facing down


def box_T(Q, dims, amb, mode="free", eps=0.90, fins=1.0, v_fan=2.0, T_plate=22.0, h_foot=400.0):
    """Mean case surface temperature of a sealed box that dissipates Q watts.

    mode free:  natural convection and radiation, the box stands on a desk (the bottom is half blocked).
    mode fan:   forced air at v_fan m/s over all faces, area multiplied by fins.
    mode plate: the footprint lies on a plate at T_plate with h_foot, the rest in natural air.
    The relations are the textbook simple forms for air at room temperature [GENERAL].
    """
    L, Wd, Hh = dims
    A_top = L * Wd
    A_side = 2 * (L + Wd) * Hh
    Lc_top = L * Wd / (2 * (L + Wd))

    def balance(T):
        """Heat leaving the box at case temperature T, W."""
        dT = T - amb
        adT = max(abs(dT), 1e-6)
        Tk, Ak = T + 273.15, amb + 273.15
        h_rad = eps * SIGMA * (Tk ** 4 - Ak ** 4) / dT if abs(dT) > 1e-6 else 4 * eps * SIGMA * Ak ** 3
        if mode == "fan":
            hc = 5.7 + 3.8 * v_fan
            return (hc + h_rad) * (A_top * 2 + A_side) * fins * dT
        g = (_h_nat(adT, Hh, "vert") + h_rad) * A_side
        g += (_h_nat(adT, Lc_top, "up") + h_rad) * A_top
        if mode == "plate":
            return g * dT + h_foot * A_top * (T - T_plate)
        g += (_h_nat(adT, Lc_top, "down") + 0.5 * h_rad) * A_top * 0.5
        return g * dT

    lo, hi = min(amb, T_plate) - 5.0, amb + 300.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if balance(m) < Q:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def box_Qmax(T_lim, dims, amb, **kw):
    """Largest heat that holds the mean surface at T_lim."""
    if box_T(0.0, dims, amb, **kw) > T_lim:
        return 0.0
    lo, hi = 0.0, 400.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if box_T(m, dims, amb, **kw) <= T_lim:
            lo = m
        else:
            hi = m
    return lo


PEAK_FACTOR = 1.25      # peak case rise over the mean rise, a metal case with one spreader [HYPOTHESIS]

# loads of the Core per Skin: hw/energy domains, delta and video (hub, radio, authority), W at the rails
DOMAINS = {"delta": dict(hub=0.70, radio=0.40, authority=0.12),
           "video": dict(hub=1.20, radio=0.60, authority=0.12)}
SKIN_ELEC = {"delta": 0.80, "video": 1.35}        # W the Skin draws for display and address
ETA_RAIL = 0.90         # Core rail converters, hw/energy ETA_B
ETA_CORE_OUT = 0.94     # Core-end supply of the Skin power [HYPOTHESIS]
PHY_CORE = 0.25         # link PHY at the Core end, per Skin, W [HYPOTHESIS]
MODEM_5G = 1.20         # 5G modem active, U5 of map (c) in sim/thermal
VALIDATOR_TYP = sum(v[1] for v in H.DP.VALIDATOR.values())
VALIDATOR_IDLE = sum(v[0] for v in H.DP.VALIDATOR.values())
VALIDATOR_PEAK = sum(v[2] for v in H.DP.VALIDATOR.values())


def core_heat(N, session="delta", shared=True, modem=False, validator=None, skin_phy=0.25, skin_end_loss=0.0):
    """Heat of a Core that serves N Skins, W.

    shared True:  the radio and the authority chips run once, the hub chips run per Skin.
    shared False: every Skin brings the whole ring load of the Leaf (1.22 W delta, 1.92 W video).
    The Skin supply loses (1 - ETA_CORE_OUT) at the Core end.
    """
    d = DOMAINS[session]
    if shared:
        rails = N * d["hub"] + d["radio"] + d["authority"]
    else:
        rails = N * (d["hub"] + d["radio"] + d["authority"])
    q = rails / ETA_RAIL
    p_skin = N * (SKIN_ELEC[session] + skin_phy + skin_end_loss)
    q += p_skin * (1 / ETA_CORE_OUT - 1) + N * PHY_CORE
    if modem:
        q += MODEM_5G
    if validator:
        q += {"idle": VALIDATOR_IDLE, "typ": VALIDATOR_TYP, "peak": VALIDATOR_PEAK}[validator]
    return q


# --------------------------------------------------------------------------
# the worn Skin: the Frame
# --------------------------------------------------------------------------
def frame_temps(P_display, P_temple, amb, wind=False, t_skin=34.0, r_sp=3.0, a_contact=None):
    """The two node model of eyewear.py with the hot spot share set by the loads.

    P_display spreads over the lens and the rim (no hot spot). P_temple is the link PHY, the decoder,
    the connector and the power path, in the temple: it sits behind the spreading resistance r_sp.
    """
    kw = {} if a_contact is None else dict(a_contact=a_contact)
    g_air, g_ser, g_c = EW.model(amb, wind, t_skin, r_sp, **kw)
    P = P_display + P_temple
    t_b = (P + g_air * amb + g_ser * t_skin) / (g_air + g_ser)
    t_hot = t_b + P_temple * r_sp
    t_contact = t_skin + (g_ser / g_c) * (t_hot - t_skin)
    return dict(T_body=t_b, T_hot=t_hot, T_contact=t_contact, T_peak=max(t_hot, t_contact, t_b))


def frame_pmax(P_temple, amb, wind=False, **kw):
    """Largest display power with a fixed temple load that holds 36.2 C."""
    if frame_temps(0.0, P_temple, amb, wind, **kw)["T_peak"] > LIM:
        return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(50):
        m = 0.5 * (lo + hi)
        if frame_temps(m, P_temple, amb, wind, **kw)["T_peak"] <= LIM:
            lo = m
        else:
            hi = m
    return lo


def peak_T(tm, amb, mode, T_plate=22.0):
    """Peak case temperature from the mean: the peak rise is PEAK_FACTOR times the mean rise over the cold reference."""
    ref = T_plate if mode == "plate" else amb
    return ref + PEAK_FACTOR * (tm - ref)


# --------------------------------------------------------------------------
# class C2: the Leaf keeps the radio, the 5G modem, the decoder and the compositor
# --------------------------------------------------------------------------
# The Leaf of L.6.0: the ring takes the hub (decoder, compositor, frame store), the radio and the authority chips.
# hw/energy domains, W: delta hub 0.70, authority 0.12; video hub 1.20, authority 0.12.
C2_RING = {"delta": dict(hub=0.70, auth=0.12), "video": dict(hub=1.20, auth=0.12)}
C2_TILES = {"delta": (0.60, 0.20), "video": (1.10, 0.25)}
R_SWEEP = (0.4, 0.8, 1.2, 1.6)      # the radio domain at the Leaf, W; 0.4 W is the L.6.0 delta radio


def c2_q(session, radio, s=1.0, feed="cells", ring_scale=1.0):
    """Heat vector of the L.6.0 body with the ring at class C2.

    The tiles carry display and address (scaled by s). The ring carries hub + authority + radio.
    feed cells: the Leaf cells supply (cell I2R, lattice, bar leaves, as session_q). feed010, feed034: a contact feed.
    """
    d, a = C2_TILES[session]
    ring = C2_RING[session]["hub"] + C2_RING[session]["auth"] + radio
    cfg = H.FIX
    q = np.zeros(H._net0.n)
    q[IDX["F"]] += s * (d + a) / NT
    q[H.I_PCB] += ring
    P = s * (d + a) + ring
    tot, per, leaves, _ = dist_alpha(cfg)
    q[IDX["C"]] += per * P ** 2
    if feed == "cells":
        q[IDX["C"]] += H.cell_heat(cfg, P) / NT
        q[H.I_BAR] += leaves * P ** 2
    else:
        q[IDX["C"][SEAT]] += 0.10 if feed == "feed010" else 0.34
    return q, dict(P_L=P, ring=ring, Q=float(q.sum()))


def c2_T(q, amb, wind, pad="free", T_pad=20.0):
    e = H.env(amb, wind, pad)
    rhs = q + e.net.q_fixed + e.net.GbT + (T_pad - 20.0) * e.gpad
    T = e.lu.solve(rhs)
    r = e.net.readout(T)
    cands = {"ring shell": r["T_ring_shell"], "bar": r["T_bar"], "back skin": r["T_back_max"],
             "front cap": r["T_front_max"]}
    where = max(cands, key=cands.get)
    return dict(T=r["T_surface_max"], where=where, T_ring_shell=r["T_ring_shell"], T_ring_pcb=r["T_ring_pcb"],
                T_front=r["T_front_max"], T_cell_max=r["T_cell_max"])


def c2_sustained(session, radio, amb, wind, feed="cells", pad="free", T_pad=20.0, T_lim=LIM):
    """Largest scale of display and address power that holds T_lim with the ring fixed. Zero if the ring alone is too hot."""
    def ok(s):
        q, _ = c2_q(session, radio, s, feed)
        return c2_T(q, amb, wind, pad, T_pad)["T"] <= T_lim
    if not ok(0.0):
        return 0.0
    hi = 10.0
    if ok(hi):
        return hi
    lo = 0.0
    for _ in range(34):
        m = 0.5 * (lo + hi)
        if ok(m):
            lo = m
        else:
            hi = m
    return lo
