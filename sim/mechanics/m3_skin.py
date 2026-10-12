"""(3) The floating back skin: strain, pad torque and pad peel. Gate MEC-41.

A neo-Hookean (incompressible, plane stress) membrane FE on a 4a x 4a patch
with 5 x 5 rigid pads at the tile centres. The pad centres follow the
rotating-square lattice (pitch a(cos t + sin t)). Two pad bonds:
  bonded : the pad turns with its tile, +/- theta (the FINAL/21 design)
  swivel : the pad centre follows the tile, the pad turn is free (the fix)
With displacement control the solution does not depend on mu, so the energy
and the forces scale with mu * t. The representative cell is the one tile
cell around the central pad (2, 2).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from matplotlib.collections import PolyCollection

from common import A_TILE, DEG, PLOTS, mm, um, save, verdict

SKINS = {  # name: (mu [Pa], E [Pa], thickness [m], elongation at break) [GENERAL]
    "TPU 80A, 80 um": (3.3e6, 10e6, 80 * um, 5.0),
    "TPU 80A, 50 um": (3.3e6, 10e6, 50 * um, 5.0),
    "silicone 30A, 80 um": (0.5e6, 1.5e6, 80 * um, 4.0),
}
H = 0.25 * mm
NP = 5


def mesh(h=H):
    n = int(round(4 * A_TILE / h)) + 1
    xs = np.linspace(0, 4 * A_TILE, n)
    X, Y = np.meshgrid(xs, xs)
    P = np.c_[X.ravel(), Y.ravel()]
    idx = np.arange(n * n).reshape(n, n)
    a, b, c, d = idx[:-1, :-1].ravel(), idx[:-1, 1:].ravel(), idx[1:, 1:].ravel(), idx[1:, :-1].ravel()
    # alternate the diagonal to avoid a mesh bias
    flip = ((np.arange(n - 1)[:, None] + np.arange(n - 1)[None, :]) % 2).ravel().astype(bool)
    t1 = np.where(flip[:, None], np.c_[a, b, c], np.c_[a, b, d])
    t2 = np.where(flip[:, None], np.c_[a, c, d], np.c_[b, c, d])
    return P, np.r_[t1, t2]


class Skin:
    def __init__(self, r_pad, h=H):
        self.P, self.T = mesh(h)
        self.r = r_pad
        self.centres = np.array([(i * A_TILE, j * A_TILE) for j in range(NP) for i in range(NP)])
        self.sign = np.array([(-1) ** (i + j) for j in range(NP) for i in range(NP)])
        d = np.linalg.norm(self.P[:, None, :] - self.centres[None], axis=2)
        self.owner = np.where(d.min(1) <= r_pad + 1e-12, d.argmin(1), -1)
        self.free = np.where(self.owner < 0)[0]
        X0 = self.P[self.T]
        Dm = np.stack([X0[:, 1] - X0[:, 0], X0[:, 2] - X0[:, 0]], axis=2)
        self.A0 = 0.5 * np.abs(np.linalg.det(Dm))
        self.Dmi = np.linalg.inv(Dm)
        cen = X0.mean(1)
        c = 2 * A_TILE
        self.central = (np.abs(cen[:, 0] - c) <= A_TILE / 2) & (np.abs(cen[:, 1] - c) <= A_TILE / 2)
        self.k_mid = 2 * NP + 2

    def place(self, theta, beta):
        """Positions of the pad nodes: centre on the lattice, pad turn beta."""
        s = np.cos(theta) + np.sin(theta)
        x = np.zeros_like(self.P)
        m = self.owner >= 0
        k = self.owner[m]
        dX = self.P[m] - self.centres[k]
        cb, sb = np.cos(beta[k]), np.sin(beta[k])
        x[m] = s * self.centres[k] + np.c_[cb * dX[:, 0] - sb * dX[:, 1], sb * dX[:, 0] + cb * dX[:, 1]]
        return x

    def energy(self, x, mu=1.0, per_elem=False):
        """Return W (per unit thickness, mu = 1), gradient on all nodes."""
        xe = x[self.T]
        Ds = np.stack([xe[:, 1] - xe[:, 0], xe[:, 2] - xe[:, 0]], axis=2)
        F = Ds @ self.Dmi
        J = np.linalg.det(F)
        I1 = np.einsum("eij,eij->e", F, F) + 1 / J ** 2
        w = mu / 2 * (I1 - 3)
        Finv_T = np.transpose(np.linalg.inv(F), (0, 2, 1))
        Pst = mu * (F - Finv_T / J[:, None, None] ** 2)
        H_ = self.A0[:, None, None] * Pst @ np.transpose(self.Dmi, (0, 2, 1))
        g = np.zeros_like(x)
        np.add.at(g, self.T[:, 1], H_[:, :, 0])
        np.add.at(g, self.T[:, 2], H_[:, :, 1])
        np.add.at(g, self.T[:, 0], -H_[:, :, 0] - H_[:, :, 1])
        if per_elem:
            return w, F, Pst, J
        return float((w * self.A0).sum()), g

    def solve(self, theta, mode):
        s = np.cos(theta) + np.sin(theta)
        beta0 = self.sign * theta if mode == "bonded" else np.zeros(NP * NP)
        x = s * self.P
        x[self.owner >= 0] = self.place(theta, beta0)[self.owner >= 0]
        nf = len(self.free)

        def fun(z):
            xx = x.copy()
            xx[self.free] = z[:2 * nf].reshape(-1, 2)
            if mode == "swivel":
                beta = z[2 * nf:]
                pm = self.owner >= 0
                xx[pm] = self.place(theta, beta)[pm]
            E, g = self.energy(xx)
            gz = g[self.free].ravel()
            if mode == "swivel":
                pm = np.where(self.owner >= 0)[0]
                k = self.owner[pm]
                r = xx[pm] - s * self.centres[k]
                tq = r[:, 0] * g[pm, 1] - r[:, 1] * g[pm, 0]
                gb = np.bincount(k, weights=tq, minlength=NP * NP)
                gz = np.r_[gz, gb]
            return E / A_TILE ** 2, gz / A_TILE ** 2
        z0 = x[self.free].ravel()
        if mode == "swivel":
            z0 = np.r_[z0, beta0]
        sol = minimize(fun, z0, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=20000, maxcor=30, gtol=1e-11, ftol=1e-15))
        xx = x.copy()
        xx[self.free] = sol.x[:2 * nf].reshape(-1, 2)
        beta = sol.x[2 * nf:] if mode == "swivel" else beta0
        if mode == "swivel":
            pm = self.owner >= 0
            xx[pm] = self.place(theta, beta)[pm]
        return xx, beta, sol

    def post(self, x, theta, beta):
        """Per mu = 1 and unit thickness: cell energy, max stretch, pad torque, pad edge force."""
        s = np.cos(theta) + np.sin(theta)
        w, F, Pst, J = self.energy(x, per_elem=True)
        _, g = self.energy(x)
        c = self.central
        C = np.transpose(F, (0, 2, 1)) @ F
        ev = np.linalg.eigvalsh(C)
        lam_max = np.sqrt(ev[:, 1])
        cell_W = float((w * self.A0)[c].sum())
        pm = np.where(self.owner == self.k_mid)[0]
        r = x[pm] - s * self.centres[self.k_mid]
        torque = float(np.sum(r[:, 0] * g[pm, 1] - r[:, 1] * g[pm, 0]))
        # line force at the pad edge: nominal traction on the ring of elements outside the pad
        cen = self.P[self.T].mean(1)
        dc = np.linalg.norm(cen - self.centres[self.k_mid], axis=1)
        ring = (dc > self.r) & (dc < self.r + 1.5 * H)
        nrm = (cen[ring] - self.centres[self.k_mid]) / dc[ring][:, None]
        trac = np.linalg.norm(np.einsum("eij,ej->ei", Pst[ring], nrm), axis=1)
        lam_ring = lam_max[ring]
        return dict(cell_W=cell_W, lam_max=float(lam_max[c].max()),
                    lam_p99=float(np.percentile(lam_max[c], 99)),
                    torque=torque, edge_trac_max=float(trac.max()), edge_trac_mean=float(trac.mean()),
                    lam_ring_max=float(lam_ring.max()), J_min=float(J.min()))


def peel(N, lam, W_t, E, t, alpha):
    """Energy release rate at the pad edge [J/m2].

    N: nominal line force, lam: stretch of the free skin at the edge, W_t: strain
    energy per area of that skin. alpha: the angle at which the skin leaves.
    Kendall peel, written for a large-strain film.
    """
    return N * (lam - np.cos(alpha)) - W_t


def main():
    thetas = np.array([5, 10, 17.5, 25, 35, 45]) * DEG
    out = {}
    fields = {}
    for r_pad in (1.0 * mm, 1.5 * mm):
        sk = Skin(r_pad)
        for mode in ("bonded", "swivel"):
            rows = []
            for th in thetas:
                x, beta, sol = sk.solve(th, mode)
                p = sk.post(x, th, beta)
                p.update(theta_deg=th / DEG, iters=int(sol.nit), converged=bool(sol.success),
                         beta_mid_deg=float(beta[sk.k_mid] / DEG))
                rows.append(p)
                if abs(th / DEG - 45) < 1e-9:
                    fields[(r_pad, mode)] = (sk, x)
                print(f"pad {2*r_pad/mm:.0f} mm {mode:6s} theta {th/DEG:5.1f} lam_max {p['lam_max']:.3f} "
                      f"torque/mu t {p['torque']:.3e} trac {p['edge_trac_max']:.3f} J_min {p['J_min']:.3f} it {sol.nit}")
            out[f"pad {2*r_pad/mm:.0f} mm, {mode}"] = rows

    # ---- scale to the skins, peel and the gate
    res = dict(fe=out, skins={})
    G_TH = 50.0   # [HYPOTHESIS] cyclic debond threshold of a fused TPU pad bond, J/m2
    ALPHA = 2 * DEG   # [HYPOTHESIS] skin take-off angle from tile height tolerance
    for name, (mu, E, t, eb) in SKINS.items():
        d = {}
        for key, rows in out.items():
            r = rows[-1]   # theta = 45 deg, 41.4 %
            r25 = rows[2]  # theta = 17.5 deg
            N = r["edge_trac_max"] * mu * t
            lam = r["lam_ring_max"]
            W_t = mu / 2 * (2 * lam ** 2 + lam ** -4 - 3) * t / 2   # free skin, between uniaxial and biaxial
            G = peel(N, lam, W_t, E, t, ALPHA)
            strain_max = r["lam_max"] - 1
            d[key] = dict(
                strain_max_41=strain_max, strain_max_25=r25["lam_max"] - 1,
                strain_p99_41=r["lam_p99"] - 1,
                energy_per_tile_41_J=r["cell_W"] * mu * t, energy_per_tile_25_J=r25["cell_W"] * mu * t,
                pad_torque_41_Nm=r["torque"] * mu * t, pad_torque_25_Nm=r25["torque"] * mu * t,
                edge_line_force_41_N_per_m=N, G_peel_41=G,
                skin_ok=strain_max <= min(1.0, eb / 3),
                peel_ok=G <= G_TH / 2)
            d[key]["MEC-41"] = verdict(d[key]["skin_ok"] and d[key]["peel_ok"])
        res["skins"][name] = d
    res["criteria"] = dict(G_threshold=G_TH, G_allow=G_TH / 2, alpha_deg=ALPHA / DEG,
                           skin_strain_allow="min(100 %, elongation at break / 3)")
    save("m3_skin", res)

    # ---- plots
    fig, ax = plt.subplots(1, 2, figsize=(11, 5.4))
    for a_, mode in zip(ax, ("bonded", "swivel")):
        sk, x = fields[(1.0 * mm, mode)]
        w, F, _, _ = sk.energy(x, per_elem=True)
        C = np.transpose(F, (0, 2, 1)) @ F
        lam = np.sqrt(np.linalg.eigvalsh(C)[:, 1])
        pc = PolyCollection(x[sk.T] / mm, array=100 * (lam - 1), cmap="viridis", edgecolors="none")
        pc.set_clim(0, 150)
        a_.add_collection(pc); a_.autoscale(); a_.set_aspect("equal")
        a_.set_title(f"skin at 41 %, Ø2 mm pads, {mode}")
        fig.colorbar(pc, ax=a_, label="max principal strain %", shrink=0.8)
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m3_skin_field.png", dpi=120); plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for key, rows in out.items():
        th = [r["theta_deg"] for r in rows]
        ax[0].plot(th, [100 * (r["lam_max"] - 1) for r in rows], "o-", label=key)
        ax[1].plot(th, [abs(r["torque"]) * 3.3e6 * 80e-6 * 1e3 for r in rows], "o-", label=key)
    ax[0].set_ylabel("max skin strain %"); ax[1].set_ylabel("pad torque, TPU 80 um [mN m]")
    for a_ in ax:
        a_.set_xlabel("theta deg"); a_.grid(alpha=.3); a_.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{PLOTS}/m3_skin.png", dpi=130); plt.close(fig)
    return res


if __name__ == "__main__":
    r = main()
    for n, d in r["skins"].items():
        for k, v in d.items():
            print(n, "|", k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
