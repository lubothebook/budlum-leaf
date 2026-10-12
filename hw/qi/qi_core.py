#!/usr/bin/env python3
"""qi_core.py - the shared physics of the Budlum Leaf Qi2.2 receiver (team hw/qi).

Everything the numbered scripts compute rests on this file:

  * the tile grid and the rotating-square hinge rule of FINAL/21 21.2.1-21.2.2,
  * the four-sector receiver coil drawn on the 10 mm tiles round the + crossing,
  * a Qi MPP-class transmitter coil (A11-like proxy, see TX below),
  * the Neumann integral: closed form for parallel straight filaments
    (Grover), Maxwell's formula for coaxial circles, the vector potential of a
    circular loop (elliptic integrals) and a general numeric Neumann sum,
  * a layered half-space model (transfer-matrix surface impedance) for the
    Tx ferrite, the Rx nanocrystalline shield and the cell metal behind it,
    folded into the Neumann sums by discrete complex images (DCIM),
  * Biot-Savart fields for the proximity (AC) loss of the pseudo-litz strands.

Units: geometry in mm, physics in SI. Angles in degrees unless named *_rad.
Tags used in the comments follow the Leaf rules: [DECISION] [HYPOTHESIS]
[PUBLICATION] [GENERAL].
"""
import math
import numpy as np
from scipy.special import ellipk, ellipe

MU0 = 4e-7 * math.pi
F_OP = 360e3                      # Qi2 MPP operating frequency [PUBLICATION] WPC Qi v2.0 MPP
OMEGA = 2 * math.pi * F_OP
RHO_CU = 1.72e-8                  # copper at 20 C [GENERAL]
SIG_CU = 1 / RHO_CU
DELTA_CU = math.sqrt(RHO_CU / (math.pi * F_OP * MU0))   # skin depth at 360 kHz

# --------------------------------------------------------------------------
# 1. the body grid (FINAL/21 21.2.1)
# --------------------------------------------------------------------------
TILE = 10.0                       # mm [DECISION]
BODY_W, BODY_H = 80.0, 160.0      # mm [DECISION]
CROSS = (40.0, 80.0)              # the + crossing in body coordinates [DECISION]


def hinge_pairs_at_node(p, q):
    """The two tile pairs a node (p, q) joins (local integer node coords).

    The rotating-square rule: tile (i, j) turns +theta when i + j is even.
    A counter-clockwise tile's top-right corner meets its top neighbour, so an
    even node joins the two vertical pairs and an odd node joins the two
    horizontal pairs. Tile (i, j) spans [10i, 10i+10] x [10j, 10j+10] in mm
    from the + crossing. Returned as ((tile, tile), (tile, tile)).
    """
    if (p + q) % 2 == 0:
        return (((p - 1, q - 1), (p - 1, q)), ((p, q - 1), (p, q)))
    return (((p - 1, q - 1), (p, q - 1)), ((p - 1, q), (p, q)))


def hinge_node_between(t1, t2):
    """Node (p, q) where the hinge of two edge-neighbour tiles sits."""
    (i1, j1), (i2, j2) = sorted([t1, t2])
    if i1 == i2:                       # vertical pair, shared edge y = 10*j2
        cands = [(i1, j2), (i1 + 1, j2)]
    else:                              # horizontal pair, shared edge x = 10*i2
        cands = [(i2, j1), (i2, j1 + 1)]
    for (p, q) in cands:
        for pair in hinge_pairs_at_node(p, q):
            if set(pair) == {t1, t2}:
                return (p, q)
    raise ValueError("no hinge")


def tile_rot_sign(t):
    i, j = t
    return 1 if (i + j) % 2 == 0 else -1


# --------------------------------------------------------------------------
# 2. the stack (FINAL/21 21.2.7 with the team proposal of README section 2)
# --------------------------------------------------------------------------
class Stack:
    """z positions in mm, z = 0 at the Tx coil filament plane, +z to the Leaf."""

    def __init__(self, gap_tx_surface=2.0, skin=0.08, cu_t=0.050, pi_core=0.0125,
                 coverlay=0.0125, sh_layers=2, sh_ribbon=0.018, sh_glue=0.005,
                 mu_ribbon=800 - 100j, kerf=0.020, can_t=0.030, can_sigma=1.39e6,
                 cell_G=7680.0, cell_t=0.90, tx_ferrite_gap=1.05,
                 tx_ferrite_t=1.0, mu_tx_ferrite=1500 - 15j, with_cell=True,
                 with_shield=True):
        self.__dict__.update(locals())
        del self.__dict__["self"]
        self.tx_surface = tx_ferrite_gap + gap_tx_surface - tx_ferrite_gap + 1.05
        # Tx coil filament plane z = 0, ferrite top z = -tx_ferrite_gap.
        # the Tx interface surface sits gap_tx_surface above the Tx coil top
        # of a 2.1 mm litz layer, so 1.05 + gap above the filament plane.
        self.tx_surface = 1.05 + gap_tx_surface
        self.rx_fpc_bottom = self.tx_surface + skin
        self.fpc_t = 2 * cu_t + pi_core + 2 * coverlay
        self.z_rx = self.rx_fpc_bottom + coverlay + cu_t + pi_core / 2
        self.sh_t = sh_layers * (sh_ribbon + sh_glue)
        self.z_shield = self.rx_fpc_bottom + self.fpc_t + 0.005
        self.z_cell = self.z_shield + self.sh_t + (0.200 - self.fpc_t - 0.005 - self.sh_t)
        self.coil_shield_total = self.z_cell - self.rx_fpc_bottom

    def mu_shield_eff(self):
        fill = self.sh_layers * self.sh_ribbon / self.sh_t
        mu_stack = 1 + fill * (self.mu_ribbon - 1)
        g = self.kerf / TILE
        return 1.0 / ((1 - g) / mu_stack + g)

    def upper_layers(self):
        """Layers above the Rx coil, from the shield bottom outward (SI)."""
        L = []
        if self.with_shield:
            L.append((self.sh_t * 1e-3, self.mu_shield_eff(), 0.0))
        gap = (self.z_cell - self.z_shield - (self.sh_t if self.with_shield else 0)) * 1e-3
        if self.with_cell:
            if gap > 0:
                L.append((gap, 1.0, 0.0))
            inner = self.cell_t - 2 * self.can_t
            L.append((self.can_t * 1e-3, 1.0, self.can_sigma))
            L.append((inner * 1e-3, 1.0, self.cell_G / (inner * 1e-3)))
            L.append((self.can_t * 1e-3, 1.0, self.can_sigma))
        return L

    def lower_layers(self):
        return [(self.tx_ferrite_t * 1e-3, self.mu_tx_ferrite, 0.0)]


def surface_R(k, layers, omega=OMEGA):
    """TE reflection coefficient of a planar stack seen from air.

    layers: [(thickness_m, mu_r, sigma)] from the interface outward; air beyond.
    Convention exp(+j omega t), mu = mu' - j mu''. A magnetic half-space gives
    (mu-1)/(mu+1); a perfect conductor gives -1.
    """
    k = np.asarray(k, dtype=float)
    zeta = k.astype(complex)                      # air half-space beyond
    for (d, mu, sig) in reversed(layers):
        eta = np.sqrt(k ** 2 + 1j * omega * MU0 * mu * sig + 0j)
        y = eta / mu
        th = np.tanh(eta * d)
        zeta = y * (zeta + y * th) / (y + zeta * th)
    return (k - zeta) / (k + zeta)


def g_refl_fn(stack, zs, zo):
    """Reflected part of the two-stack spectral Green's function (zs, zo in mm)."""
    z1 = -stack.tx_ferrite_gap * 1e-3
    z0 = stack.z_shield * 1e-3 if stack.with_shield else stack.z_cell * 1e-3
    zs_, zo_ = zs * 1e-3, zo * 1e-3
    up, lo = stack.upper_layers(), stack.lower_layers()

    def g(k):
        R0 = surface_R(k, up) if up else np.zeros_like(k, dtype=complex)
        R1 = surface_R(k, lo) if lo else np.zeros_like(k, dtype=complex)
        D = z0 - z1
        E = np.exp(-k * D)
        s1 = np.exp(-k * (zs_ - z1))
        s0 = np.exp(-k * (z0 - zs_))
        den = 1 - R0 * R1 * E * E
        alpha = (R1 * s1 + R0 * R1 * E * s0) / den
        beta = (R0 * s0 + R0 * R1 * E * s1) / den
        return alpha * np.exp(-k * (zo_ - z1)) + beta * np.exp(-k * (z0 - zo_))
    zmin = min(zs_ + zo_ - 2 * z1, 2 * z0 - zs_ - zo_)
    return g, zmin


def dcim(gfun, zmin, n=28, kmin=5.0, kmax=None):
    """Fit g(k) ~ sum a_m exp(-k c_m), c_m >= zmin. Returns (a, c[m]), rms error."""
    if kmax is None:
        kmax = 25.0 / zmin
    k = np.logspace(math.log10(kmin), math.log10(kmax), 500)
    g = gfun(k)
    c = zmin * np.logspace(0, math.log10(0.4 / zmin), n)
    A = np.exp(-np.outer(k, c))
    w = np.sqrt(k / k.max()) + 0.05            # emphasise the mid band
    Aw = A * w[:, None]
    gw = g * w
    lam = 1e-9 * np.linalg.norm(Aw) ** 2
    lhs = Aw.T @ Aw + lam * np.eye(n)
    a = np.linalg.solve(lhs, Aw.T @ gw)
    err = np.sqrt(np.mean(np.abs(A @ a - g) ** 2)) / (np.sqrt(np.mean(np.abs(g) ** 2)) + 1e-30)
    return a, c * 1e3, err          # c back to mm


# --------------------------------------------------------------------------
# 3. Neumann kernels
# --------------------------------------------------------------------------
def _H(x, d):
    return x * np.arcsinh(x / d) - np.sqrt(x * x + d * d)


def mutual_parallel_sets(A0, A1, B0, B1, dz=0.0, gmd_self=None, same=False):
    """Sum of Neumann mutual inductances between two sets of straight segments.

    Only parallel or antiparallel pairs contribute (perpendicular pairs give
    zero; this routine is for rectilinear coils). Points in mm, result in H.
    dz: extra vertical separation (image distance). same: the sets are the same
    list, so the self pair uses gmd_self (mm) and every pair counts both ways.
    """
    A0, A1, B0, B1 = (np.asarray(v, float) for v in (A0, A1, B0, B1))
    ua = A1 - A0
    la = np.linalg.norm(ua, axis=1)
    ua = ua / la[:, None]
    ub = B1 - B0
    lb = np.linalg.norm(ub, axis=1)
    ub = ub / lb[:, None]
    total = 0.0 + 0j
    nb = len(B0)
    chunk = max(1, 2_000_000 // max(nb, 1))
    for s in range(0, len(A0), chunk):
        e = min(len(A0), s + chunk)
        dot = ua[s:e] @ ub.T
        par = np.abs(np.abs(dot) - 1) < 1e-9
        ii, jj = np.nonzero(par)
        if len(ii) == 0:
            continue
        gi = ii + s
        u = ua[gi]
        rel_a = B0[jj] - A0[gi]
        rel_b = B1[jj] - A0[gi]
        sa = np.einsum("ij,ij->i", rel_a, u)
        sb = np.einsum("ij,ij->i", rel_b, u)
        perp = rel_a - sa[:, None] * u
        d2 = np.einsum("ij,ij->i", perp, perp) + dz * dz
        if same:
            selfm = gi == jj
            d2 = np.where(selfm, gmd_self ** 2 + dz * dz, d2)
        d = np.sqrt(np.maximum(d2, 1e-18))
        l = la[gi]
        val = _H(sb, d) - _H(sa, d) - _H(sb - l, d) + _H(sa - l, d)
        total += val.sum()
    return MU0 / (4 * math.pi) * total * 1e-3       # mm -> m


def maxwell_M(a, b, d):
    """Mutual inductance of coaxial circles, radii a, b, separation d (mm) [H]."""
    a, b, d = (np.asarray(v, float) * 1e-3 for v in (a, b, d))
    m = 4 * a * b / ((a + b) ** 2 + d ** 2)
    k = np.sqrt(m)
    return MU0 * np.sqrt(a * b) * ((2 / k - k) * ellipk(m) - 2 / k * ellipe(m))


def loop_Aphi(a, rho, z):
    """A_phi of a unit-current circular loop radius a at (rho, z), all mm, SI out."""
    a = a * 1e-3
    rho = np.maximum(np.asarray(rho, float) * 1e-3, 1e-9)
    z = np.asarray(z, float) * 1e-3
    m = 4 * a * rho / ((a + rho) ** 2 + z ** 2)
    m = np.minimum(m, 1 - 1e-12)
    k = np.sqrt(m)
    return MU0 / (math.pi * k) * np.sqrt(a / rho) * ((1 - m / 2) * ellipk(m) - ellipe(m))


def gauss_points(P0, P1, h=0.5, n=2):
    """Gauss-Legendre points (mm) and weighted direction vectors (mm) of segments."""
    P0, P1 = np.asarray(P0, float), np.asarray(P1, float)
    L = np.linalg.norm(P1 - P0, axis=1)
    nsub = np.maximum(1, np.ceil(L / h)).astype(int)
    xg, wg = np.polynomial.legendre.leggauss(n)
    pts, vecs, owner = [], [], []
    for s in range(len(P0)):
        t_edges = np.linspace(0, 1, nsub[s] + 1)
        for q in range(nsub[s]):
            ta, tb = t_edges[q], t_edges[q + 1]
            for xx, ww in zip(xg, wg):
                t = ta + (tb - ta) * (xx + 1) / 2
                pts.append(P0[s] + t * (P1[s] - P0[s]))
                vecs.append((P1[s] - P0[s]) * (tb - ta) * ww / 2)
                owner.append(s)
    return np.array(pts), np.array(vecs), np.array(owner)


def M_segments_to_loops(pts, vecs, loops_r, center, z_sep_list, weights=None):
    """Mutual (H) between a path given by Gauss points and coaxial Tx circles.

    loops_r: radii (mm) of the Tx loops centred at `center` (x, y) mm.
    z_sep_list: list of (weight, vertical separation mm) image terms.
    """
    dx = pts[:, 0] - center[0]
    dy = pts[:, 1] - center[1]
    rho = np.hypot(dx, dy)
    phx, phy = -dy / np.maximum(rho, 1e-12), dx / np.maximum(rho, 1e-12)
    proj = (phx * vecs[:, 0] + phy * vecs[:, 1]) * 1e-3
    tot = 0j
    for (w, zs) in z_sep_list:
        for a in loops_r:
            tot += w * np.sum(loop_Aphi(a, rho, zs) * proj)
    return tot


def numeric_L(pts, vecs, reg):
    """General numeric Neumann double sum with kernel 1/sqrt(r^2+reg^2) (mm)."""
    n = len(pts)
    tot = 0.0
    chunk = max(1, 6_000_000 // n)
    for s in range(0, n, chunk):
        e = min(n, s + chunk)
        d = pts[s:e, None, :] - pts[None, :, :]
        r = np.sqrt(np.einsum("ijk,ijk->ij", d, d) + reg * reg)
        dots = vecs[s:e] @ vecs.T
        tot += np.sum(dots / r)
    return MU0 / (4 * math.pi) * tot * 1e-3


# --------------------------------------------------------------------------
# 4. Biot-Savart for straight segments (for the proximity loss)
# --------------------------------------------------------------------------
def B_segments(P, A0, A1, I, dz=0.0):
    """B (T) at points P (mm) from segments A0->A1 carrying complex I (A).

    dz shifts the sources down by dz mm (image term). Returns complex (n, 3).
    """
    P = np.asarray(P, float)
    A0 = np.asarray(A0, float).copy()
    A1 = np.asarray(A1, float).copy()
    A0[:, 2] -= dz
    A1[:, 2] -= dz
    I = np.broadcast_to(np.asarray(I, complex), (len(A0),))
    out = np.zeros((len(P), 3), complex)
    L = A1 - A0
    ln = np.linalg.norm(L, axis=1)
    u = L / ln[:, None]
    chunk = max(1, 3_000_000 // max(len(A0), 1))
    for s in range(0, len(P), chunk):
        e = min(len(P), s + chunk)
        a = P[s:e, None, :] - A0[None]
        b = P[s:e, None, :] - A1[None]
        an = np.linalg.norm(a, axis=2)
        bn = np.linalg.norm(b, axis=2)
        cr = np.cross(u[None], a)
        c2 = np.einsum("ijk,ijk->ij", cr, cr)
        c2 = np.maximum(c2, 1e-10)
        fac = (np.einsum("jk,ijk->ij", u, a) / np.maximum(an, 1e-9)
               - np.einsum("jk,ijk->ij", u, b) / np.maximum(bn, 1e-9)) / c2
        mask = c2 < 1e-6            # on the line: skip (self handled apart)
        fac = np.where(mask, 0.0, fac)
        out[s:e] = np.einsum("ij,ijk->ik", fac * I[None, :], cr)
    return out * MU0 / (4 * math.pi) * 1e3     # 1/mm -> 1/m


def circle_polyline(r, n=128, center=(0.0, 0.0), z=0.0):
    t = np.linspace(0, 2 * math.pi, n + 1)
    pts = np.stack([center[0] + r * np.cos(t), center[1] + r * np.sin(t), np.full_like(t, z)], 1)
    return pts[:-1], pts[1:]


# --------------------------------------------------------------------------
# 5. the transmitter: a Qi MPP-class coil (A11-like proxy)
# --------------------------------------------------------------------------
# [PUBLICATION] WPC Qi type A11 Tx coil: 10 turns litz, outer 43 mm, inner
# 20.5 mm, single layer, about 6.3 uH on a ferrite plate. The Qi2 MPP Tx coil
# is of the same class (MagSafe-style, about 43-45 mm). It is used here as the
# reference transmitter. [HYPOTHESIS] that the class matches within 15 %.
TX = dict(n=10, r_in=10.25, r_out=21.5, wire_r=0.55, Q=120.0, L_spec=6.3e-6)


def tx_radii():
    p = (TX["r_out"] - TX["r_in"]) / TX["n"]
    return TX["r_in"] + p * (np.arange(TX["n"]) + 0.5)


def tx_L(stack, dc=None):
    r = tx_radii()
    gmd = TX["wire_r"] * math.exp(-0.25)
    a, b = np.meshgrid(r, r)
    terms = [(1.0, 0.0)] if dc is None else [(1.0, 0.0)] + list(zip(dc[0], dc[1]))
    tot = 0j
    for (w, c) in terms:
        d = np.where(a == b, math.hypot(gmd, c), c)
        tot += w * np.sum(maxwell_M(a, b, d))
    return tot


# --------------------------------------------------------------------------
# 6. the receiver: the four-sector coil on the tiles round the + crossing
# --------------------------------------------------------------------------
class SectorCoil:
    """The four-sector series receiver coil of FINAL/21 21.2.6, item 1-3.

    Each quadrant carries one sector: N nested turns over the 2 x 2 tile block
    next to the + crossing (tiles A=(0,0) B=(1,0) C=(1,1) D=(0,1) in Q1 local
    indices). A turn crosses four hinges (A-B, B-C, C-D, D-A) on the neutral
    plane and is drawn rectilinear, so the closed-form Neumann sum is exact for
    filaments. The four sectors run in series; one link crosses each seam.
    """

    def __init__(self, N=6, w_turn=0.80, s_turn=0.10, n_strand=4, g_strand=0.05,
                 edge=0.35, seam_edge=0.45, hinge_half=0.50, hinge_line=0.30,
                 fan=0.12, rib_h=1.5, z=0.0, block=2):
        self.__dict__.update(locals())
        del self.__dict__["self"]
        self.pitch = w_turn + s_turn
        self.segs = []          # (P0, P1, kind, tile0, tile1, turn, sector)
        self._build()

    # offsets of turn i from the tile block edges
    def o(self, i):
        return self.edge + self.w_turn / 2 + i * self.pitch

    def _sector_q1(self, i):
        """Vertex list of turn i in Q1 local mm, CCW, with tile labels."""
        N, c, yb, df = self.N, self.hinge_half, self.hinge_line, self.fan
        o = self.o(i)
        os = self.seam_edge + self.w_turn / 2 + i * self.pitch   # along the seams
        T = TILE * self.block / 2           # 10 mm, the block half
        S = TILE * self.block               # 20 mm, the block size
        f = (N - 1 - i) * df                # funnel offset: inner turns nearest the node
        q = i * df                          # hinge-line offset: inner turns farthest from edge
        hb = yb + q                         # bottom hinge line (node (10,0)), on the seam side
        A, B, C, D = (0, 0), (1, 0), (1, 1), (0, 1)
        v = []
        # A bottom (seam y=0 side uses seam_edge offset)
        v += [((os, os), A), ((T - c - f, os), A), ((T - c - f, hb), A),
              ((T - c, hb), A), ((T + c, hb), B), ((T + c + f, hb), B), ((T + c + f, os), B),
              ((S - o, os), B), ((S - o, T - o), B)]
        # B top heading -x to the node (10,10), right-hand vertical pair B-C
        xr = T + yb + (N - 1 - i) * df
        v += [((xr, T - o), B), ((xr, T - c), B), ((xr, T + c), C), ((xr, T + o), C),
              ((S - o, T + o), C), ((S - o, S - o), C)]
        # C top heading -x to node (10,20): hinge C-D on the outer edge
        ht = S - yb - q
        v += [((T + c + f, S - o), C), ((T + c + f, ht), C), ((T + c, ht), C),
              ((T - c, ht), D), ((T - c - f, ht), D), ((T - c - f, S - o), D),
              ((os, S - o), D), ((os, T + o), D)]
        # D bottom heading +x to node (10,10), left-hand vertical pair D-A
        xl = T - yb - (N - 1 - i) * df
        v += [((xl, T + o), D), ((xl, T + c), D), ((xl, T - c), A), ((xl, T - o), A),
              ((os, T - o), A), ((os, os), A)]
        return v

    def _build(self):
        mirrors = [(1, 1, False), (-1, 1, True), (-1, -1, False), (1, -1, True)]
        for sec, (sx, sy, rev) in enumerate(mirrors):
            for i in range(self.N):
                v = self._sector_q1(i)
                pts = [(sx * x, sy * y) for (x, y), _ in v]
                tiles = []
                for _, (ti, tj) in v:
                    tiles.append((ti if sx > 0 else -1 - ti, tj if sy > 0 else -1 - tj))
                if rev:
                    pts, tiles = pts[::-1], tiles[::-1]
                for k in range(len(pts) - 1):
                    p0, p1 = pts[k], pts[k + 1]
                    if abs(p0[0] - p1[0]) < 1e-12 and abs(p0[1] - p1[1]) < 1e-12:
                        continue
                    t0, t1 = tiles[k], tiles[k + 1]
                    kind = "hinge" if t0 != t1 else "tile"
                    self.segs.append((p0, p1, kind, t0, t1, i, sec))
        # funnel: the short pieces next to a hinge (within fan * N of the node)
        out = []
        for (p0, p1, kind, t0, t1, i, sec) in self.segs:
            if kind == "tile":
                L = math.dist(p0, p1)
                near = self._near_node(p0, p1)
                if near and L < self.N * self.fan + self.hinge_half + 0.6:
                    kind = "funnel"
            out.append((p0, p1, kind, t0, t1, i, sec))
        self.segs = out

    def _near_node(self, p0, p1):
        for p in (p0, p1):
            gx, gy = p[0] / TILE, p[1] / TILE
            if abs(gx - round(gx)) * TILE < 1.2 + self.N * self.fan and \
               abs(gy - round(gy)) * TILE < 1.2 + self.N * self.fan:
                return True
        return False

    # -- arrays -----------------------------------------------------------
    def arrays(self, theta_deg=0.0, scale_center=True):
        """Segment endpoints (n, 3) in mm, after the rotating-square motion."""
        P0, P1 = [], []
        th = math.radians(theta_deg)
        for idx, (p0, p1, kind, t0, t1, i, sec) in enumerate(self.segs):
            zoff = 0.0
            if kind == "hinge":
                # the turns stack on the edge-on ribbon: separate them in z
                zoff = (i - (self.N - 1) / 2) * (self.rib_h / max(self.N, 1)) * 0.0
            P0.append(self._move(p0, t0, th) + (self.z + zoff,))
            P1.append(self._move(p1, t1, th) + (self.z + zoff,))
        return np.array(P0), np.array(P1)

    @staticmethod
    def _move(p, t, th):
        if th == 0.0:
            return (p[0], p[1])
        i, j = t
        cx, cy = (i + 0.5) * TILE, (j + 0.5) * TILE
        s = tile_rot_sign(t)
        a = s * th
        dx, dy = p[0] - cx, p[1] - cy
        f = math.cos(th) + math.sin(th)
        nx = cx * f + dx * math.cos(a) - dy * math.sin(a)
        ny = cy * f + dx * math.sin(a) + dy * math.cos(a)
        return (nx, ny)

    def gmd(self):
        return 0.2235 * (self.w_turn + 2 * 0.050 + 0.0125)

    def lengths_by_kind(self):
        d = {}
        for (p0, p1, kind, *_r) in self.segs:
            d[kind] = d.get(kind, 0.0) + math.dist(p0, p1)
        return d

    def hinge_crossings(self):
        return sum(1 for s in self.segs if s[2] == "hinge")

    def check_hinge_rule(self):
        """Every tile change happens at the hinge node the lattice allows."""
        bad = 0
        for (p0, p1, kind, t0, t1, i, sec) in self.segs:
            if kind != "hinge":
                continue
            node = hinge_node_between(t0, t1)
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            if math.dist(mid, (node[0] * TILE, node[1] * TILE)) > 1.0 + self.N * self.fan:
                bad += 1
        return bad

    def area_turns(self):
        """Signed enclosed area of each closed turn (mm^2) by the shoelace."""
        areas = {}
        for (p0, p1, kind, t0, t1, i, sec) in self.segs:
            areas[(sec, i)] = areas.get((sec, i), 0.0) + 0.5 * (p0[0] * p1[1] - p1[0] * p0[1])
        return areas


# --------------------------------------------------------------------------
# 7. inductance helpers for the sector coil and the Tx
# --------------------------------------------------------------------------
def rx_L(coil, dc=None, theta=0.0):
    P0, P1 = coil.arrays(theta)
    L = mutual_parallel_sets(P0, P1, P0, P1, 0.0, coil.gmd(), same=True)
    if dc is not None:
        for (w, c) in zip(*dc):
            L += w * mutual_parallel_sets(P0, P1, P0, P1, c, coil.gmd(), same=True)
    return L


def rx_tx_M(coil, stack, dc_tx_rx=None, dx=0.0, dy=0.0, theta=0.0, h=1.0):
    P0, P1 = coil.arrays(theta)
    pts, vecs, _ = gauss_points(P0, P1, h=h, n=2)
    zsep = [(1.0, stack.z_rx)]
    if dc_tx_rx is not None:
        zsep += list(zip(dc_tx_rx[0], dc_tx_rx[1]))
    return M_segments_to_loops(pts, vecs, tx_radii(), (dx, dy), zsep)


def round_coil_L(radii, wire_gmd, dc=None):
    a, b = np.meshgrid(radii, radii)
    terms = [(1.0, 0.0)] + (list(zip(dc[0], dc[1])) if dc is not None else [])
    tot = 0j
    for (w, c) in terms:
        d = np.where(a == b, math.hypot(wire_gmd, c), c)
        tot += w * np.sum(maxwell_M(a, b, d))
    return tot


def round_coil_M(radii, stack, dc=None, dx=0.0):
    """Round reference Rx coil to the Tx (polygon points, offset dx)."""
    tot = 0j
    for r in radii:
        A0, A1 = circle_polyline(r, 256, (dx, 0.0), 0.0)
        pts, vecs, _ = gauss_points(A0, A1, h=2.0, n=2)
        zsep = [(1.0, stack.z_rx)] + (list(zip(dc[0], dc[1])) if dc is not None else [])
        tot += M_segments_to_loops(pts, vecs, tx_radii(), (0.0, 0.0), zsep)
    return tot


def images(stack, which):
    """DCIM image sets for 'rx' (Rx self), 'tx' (Tx self), 'tr' (Tx to Rx)."""
    zz = {"rx": (stack.z_rx, stack.z_rx), "tx": (0.0, 0.0), "tr": (0.0, stack.z_rx)}[which]
    g, zmin = g_refl_fn(stack, *zz)
    a, c, err = dcim(g, zmin)
    return (a, c), err


def bessel_check(stack, a_mm, b_mm, zs, zo):
    """Coaxial circles in the layered model by the direct Bessel integral (H)."""
    from scipy.special import j1
    g, zmin = g_refl_fn(stack, zs, zo)
    k = np.linspace(1e-3, 60.0 / (zmin), 400000)
    a, b = a_mm * 1e-3, b_mm * 1e-3
    f = j1(k * a) * j1(k * b) * g(k)
    return MU0 * math.pi * a * b * np.trapezoid(f, k)


# --------------------------------------------------------------------------
# 8. the circuit: series-series resonant link at 360 kHz
# --------------------------------------------------------------------------
def solve_link(L1, L2, M, R1, R2, RL, P_out=25.0, omega=OMEGA):
    """Both sides tuned to resonance on the real part of L. Phasors are peak.

    Returns a dict with currents, voltages and the loss split.
    """
    C1 = 1 / (omega ** 2 * L1.real)
    C2 = 1 / (omega ** 2 * L2.real)
    Z11 = R1 + 1j * omega * L1 + 1 / (1j * omega * C1)
    Z22 = R2 + 1j * omega * L2 + 1 / (1j * omega * C2) + RL
    Z12 = 1j * omega * M
    # unit I1
    I2 = -Z12 / Z22
    PL = 0.5 * abs(I2) ** 2 * RL
    s = math.sqrt(P_out / PL)
    I1 = 1.0 * s
    I2 = I2 * s
    V1 = Z11 * I1 + Z12 * I2
    Pin = 0.5 * (V1 * np.conj(I1)).real
    P_tx_cu = 0.5 * abs(I1) ** 2 * R1
    P_rx_cu = 0.5 * abs(I2) ** 2 * R2
    P_mag = Pin - P_out - P_tx_cu - P_rx_cu
    return dict(I1=abs(I1), I2=abs(I2), I1_rms=abs(I1) / math.sqrt(2), I2_rms=abs(I2) / math.sqrt(2),
                V1=abs(V1), Pin=Pin, eta=P_out / Pin, P_tx_cu=P_tx_cu, P_rx_cu=P_rx_cu,
                P_mag=P_mag, C2=C2, C1=C1, V2_load=abs(I2) * RL)


def eta_max(k, Q1, Q2):
    x = k * k * Q1 * Q2
    return x / (1 + math.sqrt(1 + x)) ** 2
