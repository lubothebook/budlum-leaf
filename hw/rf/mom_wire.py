#!/usr/bin/env python3
"""mom_wire.py - a thin-wire method-of-moments solver in numpy.

Budlum Leaf, RF and antenna team, L.6.0. Gate RF-22, RF-21, RF-23 cross-check.

The method
----------
* Electric field integral equation in mixed-potential form, Galerkin testing.
* Triangle (rooftop) basis across every node; a node of degree d carries d-1
  basis functions, so wire junctions and wire grids are handled.
* Reduced thin-wire kernel G = exp(-jkR) / (4 pi R), R = sqrt(d^2 + a^2).
  The static part 1/R is integrated in closed form over the source segment,
  the smooth part (exp(-jkR) - 1)/R by Gauss quadrature. This keeps the
  self term and close wires (1 mm IFA over a ground edge) accurate.
* Optional infinite PEC plane z = 0 by image theory. A wire end on the plane
  carries a half basis whose image completes it (a monopole base).
* Distributed series loss per segment (Ohm/m) and lumped series loads at a
  basis node (tuner capacitors, matching parts, hinge impedance).
* Delta-gap ports at nodes, an N-port impedance matrix, port efficiencies,
  far fields (E_theta, E_phi) and the radiated power by sphere integration.

Run `python3 mom_wire.py` for the validation set: a half-wave dipole and a
quarter-wave monopole against their textbook impedances, and an energy check.
"""
import numpy as np
import scipy.sparse as sp

C0 = 299792458.0
MU0 = 4e-7 * np.pi
EPS0 = 1.0 / (MU0 * C0 ** 2)
ETA0 = MU0 * C0


class Wires:
    """A wire structure: nodes, straight segments, radii and losses."""

    def __init__(self, tol=1e-7):
        self.tol = tol
        self._key = {}
        self.nodes = []
        self.segs = []
        self.radius = []
        self.rloss = []          # series resistance per metre, Ohm/m
        self.tag = []
        self.loads = {}          # node index -> complex series impedance
        self.image = False

    def node(self, p):
        p = np.asarray(p, float)
        k = tuple(np.round(p / self.tol).astype(np.int64))
        if k not in self._key:
            self._key[k] = len(self.nodes)
            self.nodes.append(p)
        return self._key[k]

    def line(self, p0, p1, nseg, radius, rloss=0.0, tag=""):
        """Add a straight wire from p0 to p1 cut into nseg segments."""
        p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
        ids = [self.node(p0 + (p1 - p0) * i / nseg) for i in range(nseg + 1)]
        for a, b in zip(ids[:-1], ids[1:]):
            if a != b:
                self.segs.append((a, b))
                self.radius.append(radius)
                self.rloss.append(rloss)
                self.tag.append(tag)
        return ids

    def polyline(self, pts, dmax, radius, rloss=0.0, tag=""):
        out = []
        for p0, p1 in zip(pts[:-1], pts[1:]):
            n = max(1, int(np.ceil(np.linalg.norm(np.subtract(p1, p0)) / dmax)))
            out += self.line(p0, p1, n, radius, rloss, tag)
        return out

    def finish(self):
        self.N = np.array(self.nodes)
        self.S = np.array(self.segs, int)
        self.a = np.array(self.radius)
        self.rl = np.array(self.rloss)
        r0 = self.N[self.S[:, 0]]
        r1 = self.N[self.S[:, 1]]
        d = r1 - r0
        self.L = np.linalg.norm(d, axis=1)
        self.t = d / self.L[:, None]
        self.r0 = r0
        self._bases()
        return self

    # ---------------------------------------------------------------- bases
    def _bases(self):
        inc = {}
        for s, (a, b) in enumerate(self.S):
            inc.setdefault(a, []).append((s, 0))   # node is the start of s
            inc.setdefault(b, []).append((s, 1))   # node is the end of s
        rows, segs, al, be = [], [], [], []
        self.bnode = []
        nb = 0
        for n in range(len(self.N)):
            lst = inc.get(n, [])
            onplane = self.image and abs(self.N[n][2]) < 1e-9
            if len(lst) == 1 and onplane:
                pairs = [(lst[0], None)]
            elif len(lst) >= 2:
                pairs = [(lst[0], o) for o in lst[1:]]
            else:
                pairs = []
            for (sa, ea), other in pairs:
                La = self.L[sa]
                # incoming half on sa
                if ea == 1:
                    rows.append(nb); segs.append(sa); al.append(0.0); be.append(1.0 / La)
                else:
                    rows.append(nb); segs.append(sa); al.append(-1.0); be.append(1.0 / La)
                if other is not None:
                    sb, eb = other
                    Lb = self.L[sb]
                    if eb == 0:
                        rows.append(nb); segs.append(sb); al.append(1.0); be.append(-1.0 / Lb)
                    else:
                        rows.append(nb); segs.append(sb); al.append(0.0); be.append(-1.0 / Lb)
                self.bnode.append(n)
                nb += 1
        self.nb = nb
        ns = len(self.S)
        self.Pa = sp.csr_matrix((al, (rows, segs)), shape=(nb, ns))
        self.Pb = sp.csr_matrix((be, (rows, segs)), shape=(nb, ns))
        self.bnode = np.array(self.bnode)

    def basis_at(self, node_index, which=0):
        idx = np.where(self.bnode == node_index)[0]
        if len(idx) == 0:
            raise ValueError("no basis at node %d" % node_index)
        return int(idx[which])


def _gauss(n):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (x + 1.0), 0.5 * w


def _kernel_blocks(W, k, ng=4, ngs=3, image=False, chunk=1200):
    """Return A0, A1, B0, B1 (segment x segment) for free space or the image."""
    ns = len(W.S)
    xg, wg = _gauss(ng)
    xs, ws = _gauss(ngs)
    sgn = 1.0
    r0s, ts = W.r0.copy(), W.t.copy()
    if image:
        r0s[:, 2] *= -1.0
        ts[:, 2] *= -1.0
        sgn = -1.0
    # observation points
    so = (W.L[:, None] * xg[None, :])                     # ns x ng
    P = W.r0[:, None, :] + so[..., None] * W.t[:, None, :]
    P = P.reshape(-1, 3)
    wo = (W.L[:, None] * wg[None, :]).reshape(-1)
    so = so.reshape(-1)
    # source quadrature for the smooth part
    ss = W.L[:, None] * xs[None, :]
    Q = r0s[:, None, :] + ss[..., None] * ts[:, None, :]
    Q = Q.reshape(-1, 3)
    wq = (W.L[:, None] * ws[None, :]).reshape(-1)
    sq = ss.reshape(-1)
    aq = np.repeat(W.a, ngs)
    A0 = np.zeros((ns, ns), complex); A1 = np.zeros_like(A0)
    B0 = np.zeros_like(A0); B1 = np.zeros_like(A0)
    npnt = len(P)
    chunk = max(ng, (chunk // ng) * ng)
    for c0 in range(0, npnt, chunk):
        c1 = min(npnt, c0 + chunk)
        p = P[c0:c1]
        # static, analytic over each source segment
        d = p[:, None, :] - r0s[None, :, :]
        u = np.einsum("psk,sk->ps", d, ts)
        rho2 = np.einsum("psk,psk->ps", d, d) - u * u
        rho2 = np.maximum(rho2, 0.0) + W.a[None, :] ** 2
        rho = np.sqrt(rho2)
        Ls = W.L[None, :]
        I0 = np.arcsinh((Ls - u) / rho) + np.arcsinh(u / rho)
        I1 = np.sqrt((Ls - u) ** 2 + rho2) - np.sqrt(u * u + rho2)
        K0 = I0 / (4 * np.pi)
        K1 = (I1 + u * I0) / (4 * np.pi)
        # smooth part
        R2 = (p * p).sum(1)[:, None] + (Q * Q).sum(1)[None, :] - 2.0 * (p @ Q.T)
        R = np.sqrt(np.maximum(R2, 0.0) + aq[None, :] ** 2)
        kR = k * R
        g = np.where(kR > 1e-4, (np.cos(kR) - 1.0 - 1j * np.sin(kR)) / (4 * np.pi * R),
                     -1j * k / (4 * np.pi))
        gw = g * wq[None, :]
        K0 = K0 + gw.reshape(c1 - c0, ns, ngs).sum(-1)
        K1 = K1 + (gw * sq[None, :]).reshape(c1 - c0, ns, ngs).sum(-1)
        # reduce over observation points of each segment
        s0, s1 = c0 // ng, c1 // ng
        wv = wo[c0:c1][:, None]
        sv = so[c0:c1][:, None]
        m = s1 - s0
        A0[s0:s1] = (wv * K0).reshape(m, ng, ns).sum(1)
        A1[s0:s1] = (wv * sv * K0).reshape(m, ng, ns).sum(1)
        B0[s0:s1] = (wv * K1).reshape(m, ng, ns).sum(1)
        B1[s0:s1] = (wv * sv * K1).reshape(m, ng, ns).sum(1)
    T = W.t @ ts.T
    return sgn * A0, sgn * A1, sgn * B0, sgn * B1, T


def impedance_matrix(W, f, ng=4, ngs=3):
    k = 2 * np.pi * f / C0
    w = 2 * np.pi * f
    Pa, Pb = W.Pa, W.Pb
    Z = np.zeros((W.nb, W.nb), complex)
    for img in ([False, True] if W.image else [False]):
        A0, A1, B0, B1, T = _kernel_blocks(W, k, ng, ngs, image=img)
        vec = (Pa @ (Pa @ (T * A0).T).T + Pb @ (Pa @ (T * A1).T).T
               + Pa @ (Pb @ (T * B0).T).T + Pb @ (Pb @ (T * B1).T).T)
        sca = Pb @ (Pb @ A0.T).T
        Z += 1j * w * MU0 * vec - 1j / (w * EPS0) * sca
    # distributed loss: integral of R' c_m c_n over each segment
    L = W.L
    rl = W.rl
    if np.any(rl != 0):
        D00 = sp.diags(rl * L); D01 = sp.diags(rl * L ** 2 / 2); D11 = sp.diags(rl * L ** 3 / 3)
        Zl = (Pa @ D00 @ Pa.T + Pa @ D01 @ Pb.T + Pb @ D01 @ Pa.T + Pb @ D11 @ Pb.T).toarray()
    else:
        Zl = np.zeros_like(Z, dtype=float)
    Z = Z + Zl
    Zload = np.zeros(W.nb, complex)
    for n, zl in W.loads.items():
        zv = zl(f) if callable(zl) else zl
        Zload[W.basis_at(n)] += zv
    Z[np.diag_indices(W.nb)] += Zload
    return Z, np.real(Zl) + np.diag(np.real(Zload))


def solve_ports(W, f, port_nodes, ng=4, ngs=3):
    """Return Zport (N x N), currents per port drive, the loss matrix."""
    Z, Rl = impedance_matrix(W, f, ng, ngs)
    pb = [W.basis_at(n) for n in port_nodes]
    V = np.zeros((W.nb, len(pb)), complex)
    for i, b in enumerate(pb):
        V[b, i] = 1.0
    I = np.linalg.solve(Z, V)
    Y = I[pb, :]
    Zp = np.linalg.inv(Y)
    return Zp, I, Rl, pb


def port_powers(Zp, I, Rl, pb, drive):
    """Input, loss and radiated power for a port voltage drive vector."""
    Iv = I @ drive
    Vp = drive
    Ip = Iv[pb]
    Pin = 0.5 * np.real(np.sum(Vp * np.conj(Ip)))
    Ploss = 0.5 * np.real(np.conj(Iv) @ (Rl @ Iv))
    return Pin, Ploss, Pin - Ploss


def far_field(W, f, Ib, th, ph, ngs=4):
    """E_theta, E_phi at r = 1 m (phase reference at origin), grid th x ph."""
    k = 2 * np.pi * f / C0
    w = 2 * np.pi * f
    ca = W.Pa.T @ Ib
    cb = W.Pb.T @ Ib
    xs, ws = _gauss(ngs)
    s = W.L[:, None] * xs[None, :]
    wq = W.L[:, None] * ws[None, :]
    cur = (ca[:, None] + cb[:, None] * s) * wq          # ns x ngs
    pos = W.r0[:, None, :] + s[..., None] * W.t[:, None, :]
    srcs = [(pos.reshape(-1, 3), (cur[..., None] * W.t[:, None, :]).reshape(-1, 3))]
    if W.image:
        pi = pos.copy(); pi[..., 2] *= -1
        ti = W.t.copy(); ti[:, 2] *= -1
        srcs.append((pi.reshape(-1, 3), (-cur[..., None] * ti[:, None, :]).reshape(-1, 3)))
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    rh = np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)], -1)
    thv = np.stack([np.cos(TH) * np.cos(PH), np.cos(TH) * np.sin(PH), -np.sin(TH)], -1)
    phv = np.stack([-np.sin(PH), np.cos(PH), np.zeros_like(PH)], -1)
    A = np.zeros(TH.shape + (3,), complex)
    for p, j in srcs:
        ph_ = np.exp(1j * k * (rh.reshape(-1, 3) @ p.T))   # npts x nsrc
        A += (ph_ @ j).reshape(TH.shape + (3,))
    A *= MU0 / (4 * np.pi)
    Eth = -1j * w * (A * thv).sum(-1)
    Eph = -1j * w * (A * phv).sum(-1)
    return Eth, Eph


def radiated_power(Eth, Eph, th, ph):
    U = (np.abs(Eth) ** 2 + np.abs(Eph) ** 2) / (2 * ETA0)
    TH = th[:, None]
    integrand = U * np.sin(TH)
    return np.trapezoid(np.trapezoid(integrand, ph, axis=1), th)


def ecc_patterns(E1, E2, th, ph):
    """Envelope correlation from two complex far fields (isotropic, XPR = 1)."""
    (t1, p1), (t2, p2) = E1, E2
    w = np.sin(th)[:, None]
    def integ(x):
        return np.trapezoid(np.trapezoid(x * w, ph, axis=1), th)
    c12 = integ(t1 * np.conj(t2) + p1 * np.conj(p2))
    c11 = integ(np.abs(t1) ** 2 + np.abs(p1) ** 2)
    c22 = integ(np.abs(t2) ** 2 + np.abs(p2) ** 2)
    return float(np.abs(c12) ** 2 / (c11 * c22))


# ------------------------------------------------------------- validation
def _validate():
    f = 300e6
    lam = C0 / f
    print("mom_wire validation (f = 300 MHz, lambda = 1 m)")
    # half-wave dipole, a = 0.001 lambda
    for Lrel in (0.47, 0.50):
        W = Wires()
        n = 41
        ids = W.line((0, 0, -Lrel / 2 * lam), (0, 0, Lrel / 2 * lam), n, 1e-3 * lam)
        W.finish()
        Zp, I, Rl, pb = solve_ports(W, f, [ids[n // 2]])
        print(f"  dipole L = {Lrel:.2f} lambda, a = 0.001 lambda:  Zin = {Zp[0,0].real:6.1f} {Zp[0,0].imag:+6.1f}j Ohm"
              f"   (0.50 ref: 73+42j thin-wire EMF limit; 80-86 +42..46j thick-wire MoM at a=0.001 lambda)")
    # energy check on the 0.5 lambda dipole
    th = np.linspace(0, np.pi, 91); ph = np.linspace(0, 2 * np.pi, 121)
    Eth, Eph = far_field(W, f, I[:, 0], th, ph)
    Prad = radiated_power(Eth, Eph, th, ph)
    Pin = 0.5 * np.real(1.0 * np.conj(I[pb[0], 0]))
    print(f"  energy check: P_in = {Pin*1e3:.3f} mW, P_rad (far field) = {Prad*1e3:.3f} mW, ratio {Prad/Pin:.3f}")
    # quarter-wave monopole over the image plane
    W = Wires(); W.image = True
    ids = W.line((0, 0, 0), (0, 0, 0.25 * lam), 20, 1e-3 * lam)
    W.finish()
    Zp, I, Rl, pb = solve_ports(W, f, [ids[0]])
    print(f"  monopole 0.25 lambda over PEC plane: Zin = {Zp[0,0].real:6.1f} {Zp[0,0].imag:+6.1f}j Ohm"
          f"   (half the dipole: ref 36.5+21j thin limit)")
    th = np.linspace(0, np.pi / 2, 61)
    Eth, Eph = far_field(W, f, I[:, 0], th, ph)
    Prad = radiated_power(Eth, Eph, th, ph)
    Pin = 0.5 * np.real(np.conj(I[pb[0], 0]))
    print(f"  energy check (upper half space): ratio {Prad/Pin:.3f}")


if __name__ == "__main__":
    _validate()
