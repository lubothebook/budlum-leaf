#!/usr/bin/env python3
"""leaf_thermal.py  --  lumped RC thermal network of the Budlum Leaf L.6.0 body
plus the B module.

Team: Thermal.  Gates: ENR-24 (Qi2.2 25 W on the tile body), MEC-11 (module
path at 35 C ambient), with ENR-6 / MEC-6 (charge heat, derating) as context.

The model
---------
* 128 rigid tiles (8 x 16, 10 x 10 mm).  Each tile is a vertical stack of five
  nodes, following FINAL/21 Section 21.2.7:

      FS  front surface (PC cap top)          0.25 PC + 0.05 OCA
      F   glass / micro-LED / glass           0.25
      S   Qi coil + shield or graphite layer  0.20  (+ 0.03 slip OCA above)
      C   hermetic micro cell in its can      0.90
      K   floating back skin (+ routing)      0.08 + 0.24

* Tiles are thermal islands.  Tile to tile heat moves ONLY through
    - the corner hinge ribbons (one per edge-neighbour pair), joined to S and C
    - the floating back skin (K to K, in-plane)
  An optional sensitivity adds air conduction across the 10-20 um face kerf at
  rest (`kerf_air=True`); it is OFF in every result unless named.
* The B module: ring PCBA node (all silicon + rectifier + charger),
  ring shell node (convection, radiation, sliding pad onto the face tiles),
  B cell node, bar node (contact to the top-edge tiles through 12 leaves).
* Boundaries: convection + linearised radiation to air, optional solar load,
  optional pad contact (a fixed pad temperature under the pad footprint).
* Electrical heat: Qi2.2 receiver coil, shield/can eddy loss, AC lead loss from
  the coil to the rectifier in the ring, rectifier, charger, DC lattice
  distribution (solved on the hinge resistor lattice), cell I^2 R.

Every material number is [HYPOTHESIS] unless the README names its source.
Run:  python3 run_all.py   (this file is a library)
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

SIGMA = 5.670374e-8
NX, NY = 8, 16                  # tiles across x (80 mm) and y (160 mm)
NT = NX * NY
PITCH = 10e-3                   # m
A_TILE = PITCH * PITCH * 0.985  # chamfered corners remove about 1.5 %
LAYERS = ("FS", "F", "S", "C", "K")
NL = len(LAYERS)

# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------


@dataclass
class Config:
    name: str = "baseline"
    # ---- environment
    T_amb: float = 25.0
    h_front: float = 5.5           # W/m2K natural convection, front face
    h_back: float = 5.5            # back face where it sees air
    h_ring: float = 5.5
    eps: float = 0.90              # PC cap, TPU skin, matte LCP shell
    solar: float = 0.0             # W/m2 absorbed on the front face (after alpha)
    # ---- pad
    pad: str = "none"              # none | puck | leafpad
    T_pad: float = 30.0            # pad top temperature under contact
    h_pad: float = 400.0           # skin to pad contact, W/m2K
    puck_d: float = 58e-3          # Qi2.2 MPP puck diameter
    h_back_on_pad_air: float = 2.5  # back area that hovers over the table
    # ---- hinge and skin
    hinge_kind: str = "copper"     # copper | graphite
    skin_k: float = 0.20           # W/mK TPU / silicone
    skin_t: float = 80e-6
    kerf_air: bool = False
    hinge_leaves: int = 1          # parallel edge-on ribbons per corner hinge
    landing: float = 0.7e-3        # hinge landing size on the tile corner, m
    hand: bool = False             # a hand on the lower back half at T_hand
    T_hand: float = 34.0
    h_hand: float = 150.0
    spreader_kt: float = 0.010     # W/K per square, S layer in-plane, non-coil tiles
    coil_kt: float = 0.028         # W/K per square, S layer in-plane, coil tiles
    # ---- B module
    ring_xy: tuple = (40e-3, 18e-3)   # ring centre from the top-left corner
    ring_ro: float = 16e-3
    ring_ri: float = 12e-3
    ring_h: float = 4.0e-3
    seat_tile: tuple = (3, 0)
    h_ring_pad: float = 600.0      # annulus sliding pad onto the caps, W/m2K
    G_pcb_shell: float = 0.40      # W/K inside the ring (module spreader)
    ring_pad_full: bool = False    # True: the whole ring underside is a contact pad
    G_ring_bar: float = 0.004      # W/K through the moulded 90 deg bend
    h_bar: float = 800.0           # W/m2K bar onto the top edge of the tiles
    pcm_g: float = 0.0             # g of encapsulated PCM in the ring
    pcm_Tm: float = 33.0
    pcm_L: float = 200.0           # J/g
    # ---- charge electrics
    V_rect: float = 15.0
    R_coil: float = 0.30           # ohm AC, coil + 4 seam links
    P_shield_25: float = 0.40      # W at 25 W, shield core + can eddy
    R_lead: float | None = None    # ohm AC coil to ring; None = from geometry
    lead_cu_hinge_w: float = 1.0e-3  # copper width per lead on a hinge ribbon
    eta_rect: float = 0.975
    eta_chg: float = 0.950
    charger_site: str = "ring"     # ring | quadrant (per-quadrant buck in 4 tiles)
    V_bus_ring: float = 3.85       # DC bus out of the ring
    V_cell: float = 3.85
    R_rail_hinge: float = 20e-3    # ohm per rail per tile-to-tile link
    R_leaves: float = 9e-3         # ohm loop through the 12 bar leaves
    cell_ohm_mAh: float = 50.0     # cell DC resistance x capacity
    E_body_Wh: float = 5.7
    # ---- limits
    T_skin_lim: float = 36.2
    T_cell_chg_lim: float = 45.0
    T_cell_dis_lim: float = 60.0

    def copy(self, **kw):
        c = copy.deepcopy(self)
        for k, v in kw.items():
            if not hasattr(c, k):
                raise KeyError(k)
            setattr(c, k, v)
        return c


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def tid(i, j):
    return j * NX + i


def tile_centre(i, j):
    return ((i + 0.5) * PITCH, (j + 0.5) * PITCH)


def _frac_in(pred, n=24):
    """Fraction of each tile area where pred(x, y) is true (sampled)."""
    out = np.zeros(NT)
    s = (np.arange(n) + 0.5) / n * PITCH
    X0, Y0 = np.meshgrid(s, s)
    for j in range(NY):
        for i in range(NX):
            X = X0 + i * PITCH
            Y = Y0 + j * PITCH
            out[tid(i, j)] = pred(X, Y).mean()
    return out


def coil_overlap(r_in=8e-3, r_out=22.5e-3, c=(40e-3, 80e-3)):
    f = _frac_in(lambda X, Y: ((X - c[0]) ** 2 + (Y - c[1]) ** 2 >= r_in ** 2)
                 & ((X - c[0]) ** 2 + (Y - c[1]) ** 2 <= r_out ** 2))
    return f


def disc_overlap(c, r_out, r_in=0.0):
    return _frac_in(lambda X, Y: ((X - c[0]) ** 2 + (Y - c[1]) ** 2 <= r_out ** 2)
                    & ((X - c[0]) ** 2 + (Y - c[1]) ** 2 >= r_in ** 2))


def neighbours():
    """Edge-neighbour pairs: one corner hinge joins each pair (rotating squares)."""
    pairs = []
    for j in range(NY):
        for i in range(NX):
            if i + 1 < NX:
                pairs.append((tid(i, j), tid(i + 1, j)))
            if j + 1 < NY:
                pairs.append((tid(i, j), tid(i, j + 1)))
    return pairs


PAIRS = neighbours()


def quadrant(t):
    i, j = t % NX, t // NX
    return (0 if i < NX // 2 else 1) + (0 if j < NY // 2 else 2)


# --------------------------------------------------------------------------
# hinge conductance
# --------------------------------------------------------------------------

def hinge_G(kind):
    """Thermal conductance of one edge-on hinge ribbon, W/K.

    copper:   12.5 um polyimide, 1.3 mm tall, 0.8 mm long, k = 0.12, plus
              about 1e-9 m2 of 2 um copper on the neutral plane (k = 390).
    graphite: the same ribbon laminated with 17 um pyrolytic graphite sheet
              (k_in-plane = 1850 W/mK [PUBLICATION] Panasonic PGS 17 um), plus
              the copper.  The PGS sits on the neutral plane next to the copper.
    """
    L = 0.8e-3
    g_pi = 0.12 * 12.5e-6 * 1.3e-3 / L
    g_cu = 390.0 * 1.0e-9 / L
    if kind == "copper":
        return g_pi + g_cu
    if kind == "graphite":
        g_pgs = 1850.0 * 17e-6 * 1.2e-3 / L
        return g_pi + g_cu + g_pgs
    raise ValueError(kind)


# --------------------------------------------------------------------------
# DC lattice distribution
# --------------------------------------------------------------------------

def lattice_loss(src_tiles, src_I, sink_I, R_link, members=None):
    """Solve a resistor lattice. Return (total loss W, per-tile loss W).

    src_tiles / src_I: current injected at given tiles (A).
    sink_I: current drawn at each member tile (array NT, A).
    R_link: loop resistance of one tile-to-tile link (both rails).
    members: tiles that take part (None = all). Links leave no member set.
    """
    mem = np.ones(NT, bool) if members is None else members
    idx = -np.ones(NT, int)
    ids = np.where(mem)[0]
    idx[ids] = np.arange(len(ids))
    n = len(ids)
    rows, cols, vals = [], [], []
    links = []
    g = 1.0 / R_link
    for a, b in PAIRS:
        if mem[a] and mem[b]:
            ia, ib = idx[a], idx[b]
            rows += [ia, ib, ia, ib]
            cols += [ia, ib, ib, ia]
            vals += [g, g, -g, -g]
            links.append((a, b))
    Lm = sp.csr_matrix((vals, (rows, cols)), shape=(n, n)).tolil()
    b_vec = -sink_I[ids].copy()
    for t, I in zip(src_tiles, src_I):
        b_vec[idx[t]] += I
    # ground the first source node
    ref = idx[src_tiles[0]]
    Lm[ref, :] = 0
    Lm[ref, ref] = 1
    b_vec[ref] = 0
    V = spla.spsolve(Lm.tocsr(), b_vec)
    per = np.zeros(NT)
    tot = 0.0
    for a, b in links:
        I = (V[idx[a]] - V[idx[b]]) * g
        p = I * I * R_link
        tot += p
        per[a] += p / 2
        per[b] += p / 2
    return tot, per


# --------------------------------------------------------------------------
# the network
# --------------------------------------------------------------------------

class Network:
    """Builds the conductance matrix, the capacities and the boundary terms."""

    RING = ("ring_pcb", "ring_shell", "ring_cell", "bar")

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.n = NT * NL + len(self.RING)
        self.rows, self.cols, self.vals = [], [], []
        self.Gb = np.zeros(self.n)      # conductance to a boundary
        self.GbT = np.zeros(self.n)     # sum G_b * T_b
        self.C = np.zeros(self.n)
        self.q_fixed = np.zeros(self.n)  # solar
        self.surface_nodes = []
        self._build()

    # node index helpers
    def nid(self, t, layer):
        return t * NL + LAYERS.index(layer)

    def rid(self, name):
        return NT * NL + self.RING.index(name)

    def link(self, a, b, g):
        if g <= 0:
            return
        self.rows += [a, b, a, b]
        self.cols += [a, b, b, a]
        self.vals += [g, g, -g, -g]

    def bnd(self, a, g, T):
        self.Gb[a] += g
        self.GbT[a] += g * T

    def h_rad(self):
        Tm = (self.cfg.T_amb + 33.0) / 2 + 273.15
        return 4 * self.cfg.eps * SIGMA * Tm ** 3

    def _build(self):
        c = self.cfg
        A = A_TILE
        hr = self.h_rad()
        # --- geometry of the ring and pad
        disc = disc_overlap(c.ring_xy, c.ring_ro)
        ann = disc_overlap(c.ring_xy, c.ring_ro, c.ring_ri)
        inner = disc - ann
        self.disc, self.ann = disc, ann
        if c.pad == "puck":
            padf = disc_overlap((40e-3, 80e-3), c.puck_d / 2)
        elif c.pad == "leafpad":
            padf = np.ones(NT)
        else:
            padf = np.zeros(NT)
        self.padf = padf
        # --- per-tile vertical stack
        R = {  # K/W per tile area, m2K/W divided by A
            ("FS", "F"): (0.25e-3 / 0.20 + 0.05e-3 / 0.20 + 0.125e-3 / 1.0) / A,
            ("F", "S"): (0.125e-3 / 1.0 + 0.03e-3 / 0.20 + 0.10e-3 / 1.0) / A,
            ("S", "C"): (0.10e-3 / 1.0 + 10e-6 / 0.2 + 0.45e-3 / 0.8) / A,
            ("C", "K"): (0.45e-3 / 0.8 + 0.24e-3 / 0.30 + c.skin_t / 2 / c.skin_k) / A,
        }
        cap = {  # J/K per tile
            "FS": 0.25e-3 * A * 1.44e6,
            "F": 0.30e-3 * A * 2.0e6,
            "S": 0.20e-3 * A * 2.6e6,
            "C": 0.90e-3 * (9.25e-3 ** 2) * 2.2e6,
            "K": (0.24e-3 * 1.6e6 + c.skin_t * 1.8e6) * A,
        }
        for t in range(NT):
            i, j = t % NX, t // NX
            for (a, b), r in R.items():
                self.link(self.nid(t, a), self.nid(t, b), 1.0 / r)
            for L_ in LAYERS:
                self.C[self.nid(t, L_)] = cap[L_]
            # front surface: exposed part convects and radiates
            a_front = A * (1 - disc[t])
            self.bnd(self.nid(t, "FS"), (c.h_front + hr) * a_front, c.T_amb)
            self.q_fixed[self.nid(t, "FS")] += c.solar * a_front
            # back skin: pad contact or air
            a_pad = A * padf[t]
            a_air = A - a_pad
            hb = c.h_back if c.pad == "none" else c.h_back_on_pad_air
            hrb = hr if c.pad == "none" else hr * 0.5  # sees the table
            if c.hand and j >= NY // 2 and 1 <= i <= NX - 2 and c.pad == "none":
                # a palm on 6 x 8 tiles of the lower back: 48 cm2
                self.bnd(self.nid(t, "K"), c.h_hand * a_air, c.T_hand)
            else:
                self.bnd(self.nid(t, "K"), (hb + hrb) * a_air, c.T_amb)
            if a_pad > 0:
                g_pad = 1.0 / (1.0 / (c.h_pad * a_pad) + (c.skin_t / 2 / c.skin_k) / a_pad)
                self.bnd(self.nid(t, "K"), g_pad, c.T_pad)
            # perimeter tile edges
            n_edge = (i == 0) + (i == NX - 1) + (j == 0) + (j == NY - 1)
            if n_edge:
                a_e = n_edge * PITCH * 2.0e-3
                self.bnd(self.nid(t, "C"), (c.h_front + hr) * a_e, c.T_amb)
            self.surface_nodes += [self.nid(t, "FS"), self.nid(t, "K")]
        # --- tile to tile: hinges and skin only
        gh = hinge_G(c.hinge_kind) * c.hinge_leaves
        gskin = c.skin_k * c.skin_t * PITCH / PITCH
        gkerf = 0.026 * 0.50e-3 * PITCH / 15e-6 if c.kerf_air else 0.0
        # corner-to-centre spreading inside a tile: a 90 deg wedge from a
        # 0.7 mm landing to the 7 mm half-diagonal
        cm = coil_map()
        kt = np.where(cm > 0.3, c.coil_kt, c.spreader_kt)
        g_int = kt * (math.pi / 2) / math.log(7.0e-3 / c.landing)
        self.g_hinge, self.g_skin = gh, gskin
        self.g_link = []
        for a, b in PAIRS:
            g = 1.0 / (1.0 / gh + 1.0 / g_int[a] + 1.0 / g_int[b])
            self.g_link.append(g)
            self.link(self.nid(a, "S"), self.nid(b, "S"), g)
            self.link(self.nid(a, "K"), self.nid(b, "K"), gskin)
            if gkerf:
                self.link(self.nid(a, "F"), self.nid(b, "F"), gkerf)
        # --- B module
        pcb, sh, rc, bar = (self.rid(x) for x in self.RING)
        self.C[pcb] = 2.5
        self.C[sh] = 4.5
        self.C[rc] = 0.6
        self.C[bar] = 0.3
        self.link(pcb, sh, c.G_pcb_shell)
        self.link(pcb, rc, 0.03)       # thermal wall, Part 11 mechanism 5
        self.link(rc, sh, 0.08)
        self.link(sh, bar, c.G_ring_bar)
        self.link(pcb, bar, 0.002)
        a_top = math.pi * c.ring_ro ** 2
        a_side = 2 * math.pi * c.ring_ro * c.ring_h
        self.bnd(sh, (c.h_ring + hr) * (a_top + a_side), c.T_amb)
        self.q_fixed[sh] += c.solar * a_top
        a_bar = 32e-3 * (4e-3 + 2e-3)  # top + outer side of the bar
        self.bnd(bar, (c.h_ring + hr) * a_bar, c.T_amb)
        self.q_fixed[bar] += c.solar * 32e-3 * 1e-3
        # ring onto tiles: annulus pad and inner air gap of 0.1 mm
        for t in range(NT):
            if ann[t] > 0:
                self.link(sh, self.nid(t, "FS"), c.h_ring_pad * ann[t] * A)
            if inner[t] > 0:
                h_in = c.h_ring_pad * 0.9 if c.ring_pad_full else 0.026 / 0.1e-3
                self.link(sh, self.nid(t, "FS"), h_in * inner[t] * A)
        # bar onto the top-edge tiles through leaves and LCP face
        for i in range(NX):
            x0, x1 = i * PITCH, (i + 1) * PITCH
            ov = max(0.0, min(x1, c.ring_xy[0] + 16e-3) - max(x0, c.ring_xy[0] - 16e-3))
            if ov > 0:
                g = c.h_bar * ov * 2.0e-3
                if (i, 0) == tuple(c.seat_tile):
                    g += 12 * 0.02     # 12 gold leaves, 0.02 W/K each
                self.link(bar, self.nid(tid(i, 0), "C"), g)
        self.surface_nodes += [sh, bar]
        self.surface_nodes = np.array(self.surface_nodes)
        self.cell_nodes = np.array([self.nid(t, "C") for t in range(NT)] + [rc])
        self.ntc_nodes = np.array([self.nid(t, "S") for t in range(NT)])
        self.G = sp.csr_matrix((self.vals, (self.rows, self.cols)), shape=(self.n, self.n))

    # ---------------------------------------------------------------- solvers
    def pcm_C(self, T):
        """Apparent heat capacity of the PCM in the ring shell (1 K band)."""
        c = self.cfg
        Cx = np.zeros(self.n)
        if c.pcm_g > 0:
            sh = self.rid("ring_shell")
            Cx[sh] = c.pcm_g * 2.0  # sensible, about 2 J/gK
            if abs(T[sh] - c.pcm_Tm) <= 0.5:
                Cx[sh] += c.pcm_g * c.pcm_L / 1.0
        return Cx

    def steady(self, q):
        A = (self.G + sp.diags(self.Gb)).tocsc()
        return spla.spsolve(A, q + self.q_fixed + self.GbT)

    def transient(self, q_fun, t_end, dt=2.0, T0=None, record_every=10):
        """Implicit Euler. q_fun(t, T) -> (q vector, info dict)."""
        T = np.full(self.n, self.cfg.T_amb) if T0 is None else T0.copy()
        base = (self.G + sp.diags(self.Gb)).tocsc()
        lu_cache = {}
        out = []
        steps = int(round(t_end / dt))
        for k in range(steps + 1):
            q, info = q_fun(k * dt, T)
            if k % record_every == 0 or info.get("stop"):
                out.append((k * dt, T.copy(), info))
            if info.get("stop"):
                break
            Ctot = self.C + self.pcm_C(T)
            key = round(float(Ctot.sum()), 6)
            if key not in lu_cache:
                lu_cache[key] = spla.splu((base + sp.diags(Ctot / dt)).tocsc())
            T = lu_cache[key].solve(Ctot / dt * T + q + self.q_fixed + self.GbT)
        return out

    # --------------------------------------------------------------- readouts
    def readout(self, T):
        return dict(
            T_surface_max=float(T[self.surface_nodes].max()),
            T_front_max=float(max(T[self.nid(t, "FS")] for t in range(NT))),
            T_back_max=float(max(T[self.nid(t, "K")] for t in range(NT))),
            T_ring_shell=float(T[self.rid("ring_shell")]),
            T_ring_pcb=float(T[self.rid("ring_pcb")]),
            T_bar=float(T[self.rid("bar")]),
            T_cell_max=float(T[self.cell_nodes[:NT]].max()),
            T_cell_min=float(T[self.cell_nodes[:NT]].min()),
            T_Bcell=float(T[self.rid("ring_cell")]),
            T_ntc_max=float(T[self.ntc_nodes].max()),
        )

    def field(self, T, layer):
        return np.array([T[self.nid(t, layer)] for t in range(NT)]).reshape(NY, NX)


# --------------------------------------------------------------------------
# power maps
# --------------------------------------------------------------------------

SESSIONS = {
    # W on the tiles (display + address) and W per ring chip
    "video": dict(tiles=dict(display=1.00, address=0.25),
                  ring=dict(U1=0.35, U2A=0.40, U5=0.05, U6=0.30, U3U4=0.12, U7U8=0.03)),
    "5g_outdoor": dict(tiles=dict(display=1.80, address=0.30),
                       ring=dict(U1=0.35, U2A=0.05, U5=1.20, U6=0.30, U3U4=0.15, U7U8=0.03)),
    "charge_idle": dict(tiles=dict(display=0.0, address=0.0),
                        ring=dict(U1=0.02, U2A=0.03, U5=0.0, U6=0.0, U3U4=0.05, U7U8=0.01)),
}


def session_total(name, scale=1.0):
    s = SESSIONS[name]
    return scale * (sum(s["tiles"].values()) + sum(s["ring"].values()))


def session_q(net: Network, name, scale=1.0, display_map=None):
    """Heat vector of a use session (no charging). Discharge losses included."""
    c = net.cfg
    s = SESSIONS[name]
    q = np.zeros(net.n)
    disp = scale * sum(s["tiles"].values())
    w = np.ones(NT) / NT if display_map is None else display_map / display_map.sum()
    for t in range(NT):
        q[net.nid(t, "F")] += disp * w[t]
    ring = scale * sum(s["ring"].values())
    q[net.rid("ring_pcb")] += ring
    # discharge: cell I2R and DC lattice from all cells to the seat tile
    P = disp + ring
    I_cell = P / c.V_cell / NT
    R_cell = c.cell_ohm_mAh / (c.E_body_Wh / NT / c.V_cell * 1000)
    for t in range(NT):
        q[net.nid(t, "C")] += I_cell ** 2 * R_cell
    I_tot = P / c.V_cell
    seat = tid(*c.seat_tile)
    _, per = lattice_loss([seat], [I_tot], np.full(NT, I_tot / NT), 2 * c.R_rail_hinge)
    for t in range(NT):
        q[net.nid(t, "C")] += per[t]
    q[net.rid("bar")] += I_tot ** 2 * c.R_leaves
    return q


# ---- charging -------------------------------------------------------------

_COIL = None
_LEAD_TILES = None


def coil_map():
    global _COIL
    if _COIL is None:
        _COIL = coil_overlap()
    return _COIL


def lead_tiles(cfg):
    """Tiles that carry the two AC leads from the coil to the ring."""
    j_ring = int(cfg.ring_xy[1] // PITCH)
    tiles = [tid(3, j) for j in range(j_ring + 1, 8)]
    return tiles


def R_lead(cfg):
    """AC resistance of both leads from the coil to the rectifier in the ring."""
    if cfg.R_lead is not None:
        return cfg.R_lead
    n_h = len(lead_tiles(cfg)) + 1                      # hinge crossings per lead
    r_h = 1.72e-8 * 0.8e-3 / (2e-6 * cfg.lead_cu_hinge_w)
    L_tile = n_h * PITCH                                 # routed in the tile layer
    r_t = 1.72e-8 * L_tile / (18e-6 * 1.5e-3)
    return 2 * (n_h * r_h + r_t)


_DIST_CACHE = {}


def dist_alpha(cfg):
    """Distribution loss coefficient: P_loss = alpha * P_cells_out^2, per tile map."""
    key = (cfg.charger_site, cfg.V_bus_ring, cfg.V_cell, cfg.R_rail_hinge, cfg.seat_tile)
    if key in _DIST_CACHE:
        return _DIST_CACHE[key]
    P = 1.0
    seat = tid(*cfg.seat_tile)
    R = 2 * cfg.R_rail_hinge
    if cfg.charger_site == "ring":
        I = P / cfg.V_bus_ring
        tot, per = lattice_loss([seat], [I], np.full(NT, I / NT), R)
        leaves = I * I * cfg.R_leaves
        chg_tiles = []
    else:
        # 15 V bus from the seat to four charger tiles next to the + crossing,
        # then the cell-voltage lattice inside each quadrant.
        chg_tiles = [tid(3, 7), tid(4, 7), tid(3, 8), tid(4, 8)]
        Ib = P / cfg.V_rect
        sink = np.zeros(NT)
        for t in chg_tiles:
            sink[t] = Ib / 4
        tot1, per1 = lattice_loss([seat], [Ib], sink, R)
        tot, per = tot1, per1.copy()
        for qd, ct in zip((0, 1, 2, 3), chg_tiles):
            mem = np.array([quadrant(t) == qd for t in range(NT)])
            Iq = P / 4 / cfg.V_cell
            sink = np.where(mem, Iq / mem.sum(), 0.0)
            t2, p2 = lattice_loss([ct], [Iq], sink, R, members=mem)
            tot += t2
            per += p2
        leaves = Ib * Ib * cfg.R_leaves
    _DIST_CACHE[key] = (tot, per, leaves, chg_tiles)
    return _DIST_CACHE[key]


def charge_losses(cfg, P_rx):
    """Loss budget at a Qi2.2 received DC power P_rx (W, rectifier output)."""
    I_ac = 1.11 * P_rx / cfg.V_rect
    out = {}
    out["coil"] = I_ac ** 2 * cfg.R_coil
    out["shield_eddy"] = cfg.P_shield_25 * (P_rx / 25.0) ** 2
    out["ac_lead"] = I_ac ** 2 * R_lead(cfg)
    out["rectifier"] = P_rx * (1 / cfg.eta_rect - 1)
    out["charger"] = P_rx * (1 - cfg.eta_chg)
    P_chg_out = P_rx * cfg.eta_chg
    tot, per, leaves, _ = dist_alpha(cfg)
    out["dc_lattice"] = tot * P_chg_out ** 2
    out["leaves"] = leaves * P_chg_out ** 2
    P_cells_in = P_chg_out - out["dc_lattice"] - out["leaves"]
    I_cell = P_cells_in / cfg.V_cell / NT
    R_cell = cfg.cell_ohm_mAh / (cfg.E_body_Wh / NT / cfg.V_cell * 1000)
    out["cells_I2R"] = NT * I_cell ** 2 * R_cell
    P_stored = P_cells_in - out["cells_I2R"]
    out["_P_stored"] = P_stored
    out["_C_rate"] = P_cells_in / cfg.E_body_Wh
    out["_I_ac"] = I_ac
    out["_P_pad_draw"] = P_rx + out["coil"] + out["shield_eddy"] + out["ac_lead"] + out["rectifier"]
    return out


def charge_q(net: Network, P_rx, idle=True):
    """Heat vector while charging at P_rx."""
    c = net.cfg
    L = charge_losses(c, P_rx)
    q = np.zeros(net.n)
    cm = coil_map()
    w = cm / cm.sum()
    for t in range(NT):
        q[net.nid(t, "S")] += (L["coil"] + L["shield_eddy"]) * w[t]
    lt = lead_tiles(c)
    for t in lt:
        q[net.nid(t, "S")] += L["ac_lead"] / len(lt)
    q[net.rid("ring_pcb")] += L["rectifier"]
    tot, per, leaves, chg_tiles = dist_alpha(c)
    P_chg_out = P_rx * c.eta_chg
    if c.charger_site == "ring":
        q[net.rid("ring_pcb")] += L["charger"]
    else:
        for t in chg_tiles:
            q[net.nid(t, "S")] += L["charger"] / 4
    for t in range(NT):
        q[net.nid(t, "C")] += per[t] * P_chg_out ** 2 + L["cells_I2R"] / NT
    q[net.rid("bar")] += L["leaves"]
    if idle:
        q[net.rid("ring_pcb")] += sum(SESSIONS["charge_idle"]["ring"].values())
    return q, L


# --------------------------------------------------------------------------
# charge controller and acceptance
# --------------------------------------------------------------------------

def cell_accept_C(soc):
    """Cell charge acceptance in C (of the body energy): CC 4.4 C, then taper.
    [HYPOTHESIS] silicon-anode fast-charge micro cell."""
    if soc < 0.60:
        return 4.4
    if soc < 0.80:
        return 4.4 - (4.4 - 2.0) * (soc - 0.60) / 0.20
    return max(0.3, 2.0 - (2.0 - 0.3) * (soc - 0.80) / 0.15)


def derate(T_hot, T_lim, band=2.0):
    """Throttle law on the hottest surface (or NTC):
    full power below T_lim - band, linear to 20 % at T_lim - 0.2 K, zero at T_lim.
    The shape follows Part 11 Section 11.4 moved under the 36.2 C cut-off."""
    a = T_lim - band
    b = T_lim - 0.2
    if T_hot <= a:
        return 1.0
    if T_hot < b:
        return 1.0 - 0.8 * (T_hot - a) / (b - a)
    if T_hot < T_lim:
        return 0.2 * (T_lim - T_hot) / 0.2
    return 0.0


def P_rx_for_cells(cfg, P_cells_target):
    """Invert the loss chain: P_rx that delivers P_cells_target into the cells."""
    lo, hi = 0.0, 40.0
    for _ in range(50):
        m = (lo + hi) / 2
        L = charge_losses(cfg, m)
        pin = m * cfg.eta_chg - L["dc_lattice"] - L["leaves"]
        if pin < P_cells_target:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def simulate_charge(cfg, soc0=0.0, soc_end=0.80, t_max=4 * 3600, dt=2.0,
                    P_class=25.0, T_lim=None, band=2.0, T0=None):
    net = Network(cfg)
    T_lim = cfg.T_skin_lim if T_lim is None else T_lim
    st = dict(soc=soc0, P=P_class)
    E_J = cfg.E_body_Wh * 3600
    hist = []

    def q_fun(t, T):
        r = net.readout(T)
        hot = max(r["T_surface_max"], r["T_ntc_max"])
        f = derate(hot, T_lim, band)
        if r["T_cell_max"] >= cfg.T_cell_chg_lim:
            f = 0.0
        P_acc = P_rx_for_cells(cfg, cell_accept_C(st["soc"]) * cfg.E_body_Wh)
        P = min(P_class, P_acc) * f
        q, L = charge_q(net, P)
        st["soc"] += L["_P_stored"] * dt / E_J
        info = dict(P_rx=P, soc=st["soc"], f=f, **r)
        hist.append((t, info))
        if st["soc"] >= soc_end:
            info["stop"] = True
        return q, info

    out = net.transient(q_fun, t_max, dt=dt, T0=T0, record_every=15)
    return net, out


def sustained_charge(cfg, T_lim=None):
    """Highest steady P_rx (<= 40 W) with surface, NTC <= T_lim and cells <= limit."""
    net = Network(cfg)
    T_lim = cfg.T_skin_lim if T_lim is None else T_lim

    def ok(P):
        T = net.steady(charge_q(net, P)[0])
        r = net.readout(T)
        return (max(r["T_surface_max"], r["T_ntc_max"]) <= T_lim
                and r["T_cell_max"] <= cfg.T_cell_chg_lim), r

    if not ok(0.0)[0]:
        return 0.0, ok(0.0)[1]
    lo, hi = 0.0, 40.0
    if ok(hi)[0]:
        return hi, ok(hi)[1]
    for _ in range(40):
        m = (lo + hi) / 2
        if ok(m)[0]:
            lo = m
        else:
            hi = m
    return lo, ok(lo)[1]


def sustained_session(cfg, name, T_lim=None):
    """Highest session power scale (x nominal) that holds every surface <= T_lim."""
    net = Network(cfg)
    T_lim = cfg.T_skin_lim if T_lim is None else T_lim

    def hot(s):
        r = net.readout(net.steady(session_q(net, name, s)))
        return r["T_surface_max"], r

    if hot(0.0)[0] > T_lim:
        return 0.0
    lo, hi = 0.0, 4.0
    if hot(hi)[0] <= T_lim:
        return hi
    for _ in range(40):
        m = (lo + hi) / 2
        if hot(m)[0] <= T_lim:
            lo = m
        else:
            hi = m
    return lo
