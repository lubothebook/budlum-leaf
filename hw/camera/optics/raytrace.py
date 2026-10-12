#!/usr/bin/env python3
"""raytrace.py: a small sequential ray tracer for rotationally symmetric
even-asphere lenses, written for the Budlum Leaf camera column (gate CAM-21).

Units: mm for length, um for wavelength. Surface vertices sit on the z axis.
Object at infinity. All tracing is vectorised with numpy.

Contents
  materials       n(material, wavelength)
  Lens            prescription container (surfaces, thicknesses, media, stop)
  trace()         exact real-ray trace with Newton intersection on aspheres
  paraxial()      y-nu trace: EFL, BFL, exit pupil
  rays_for_field  ray aiming onto a stop surface, hexapolar or square pupil
  psf/MTF         wavefront (OPD to a reference sphere) and OTF by pupil
                  autocorrelation in image-space direction-cosine space
"""
import json
import numpy as np

# --------------------------------------------------------------------------
# materials
# --------------------------------------------------------------------------
WL_F, WL_D, WL_C = 0.4861327, 0.5875618, 0.6562725
WAVES = np.array([WL_F, WL_D, WL_C])
WEIGHTS = np.array([1.0, 2.0, 1.0])


def _sapphire_o(wl):
    """Sapphire, ordinary ray. Malitson and Dodge 1972 Sellmeier [PUBLICATION]."""
    l2 = wl * wl
    n2 = (1 + 1.4313493 * l2 / (l2 - 0.0726631 ** 2)
          + 0.65054713 * l2 / (l2 - 0.1193242 ** 2)
          + 5.3414021 * l2 / (l2 - 18.028251 ** 2))
    return np.sqrt(n2)


def _cauchy_from_nd_vd(nd, vd, pgf=0.70):
    """Three-term Cauchy n = A + B/l^2 + C/l^4 through nF, nd, nC.
    nF - nC = (nd - 1)/vd, and nF - nd = pgf (nF - nC). [GENERAL]"""
    dFC = (nd - 1.0) / vd
    nF = nd + pgf * dFC
    nC = nF - dFC
    M = np.array([[1, WL_F ** -2, WL_F ** -4],
                  [1, WL_D ** -2, WL_D ** -4],
                  [1, WL_C ** -2, WL_C ** -4]])
    A, B, C = np.linalg.solve(M, [nF, nd, nC])
    return lambda wl: A + B / wl ** 2 + C / wl ** 4


# nd, vd of moulded optical polymers, maker data-sheet class [PUBLICATION]
POLYMERS = {
    "APEL5514ML": (1.5445, 55.9),   # Mitsui cyclo-olefin copolymer
    "E48R":       (1.5310, 56.0),   # Zeon cyclo-olefin polymer
    "OKP-A2":     (1.6320, 23.4),   # Osaka Gas Chemicals polyester
    "EP-9000":    (1.6700, 19.2),   # Mitsubishi Gas Chemical polycarbonate class
    "EP-10000":   (1.6800, 18.3),   # Mitsubishi Gas Chemical high-index class
    "PC":         (1.5855, 29.9),   # polycarbonate
}
_MAT = {"AIR": lambda wl: np.ones_like(np.asarray(wl, float)),
        "SAPPHIRE": _sapphire_o}
for _k, (_nd, _vd) in POLYMERS.items():
    _MAT[_k] = _cauchy_from_nd_vd(_nd, _vd)


def n_of(mat, wl):
    return float(_MAT[mat.upper() if mat.upper() in _MAT else mat](wl))


# --------------------------------------------------------------------------
# lens container
# --------------------------------------------------------------------------
class Lens:
    """Surfaces 0..S-1. Surface i: curvature c[i], conic k[i], even asphere
    terms a[i, j] in normalised form  a_j (r / rn[i])^(2j+4), j = 0..NA-1.
    t[i] is the axial distance from surface i to surface i+1 (last: to image).
    mat[i] is the medium after surface i. stop is the index of the stop."""

    def __init__(self, c, k, a, rn, t, mat, stop, epd, names=None):
        self.c = np.asarray(c, float)
        self.k = np.asarray(k, float)
        self.a = np.asarray(a, float)
        self.rn = np.asarray(rn, float)
        self.t = np.asarray(t, float)
        self.mat = list(mat)
        self.stop = int(stop)
        self.epd = float(epd)
        self.names = names or [f"S{i+1}" for i in range(len(c))]

    @property
    def S(self):
        return len(self.c)

    def z_vertex(self):
        return np.concatenate([[0.0], np.cumsum(self.t[:-1])])

    def ttl(self):
        return float(np.sum(self.t))

    def copy(self):
        return Lens(self.c.copy(), self.k.copy(), self.a.copy(), self.rn.copy(),
                    self.t.copy(), list(self.mat), self.stop, self.epd, list(self.names))

    def to_dict(self):
        return dict(c=self.c.tolist(), k=self.k.tolist(), a=self.a.tolist(),
                    rn=self.rn.tolist(), t=self.t.tolist(), mat=self.mat,
                    stop=self.stop, epd=self.epd, names=self.names)

    @staticmethod
    def from_dict(d):
        return Lens(d["c"], d["k"], d["a"], d["rn"], d["t"], d["mat"],
                    d["stop"], d["epd"], d.get("names"))

    def save(self, path, extra=None):
        d = self.to_dict()
        if extra:
            d.update(extra)
        with open(path, "w") as f:
            json.dump(d, f, indent=1)

    @staticmethod
    def load(path):
        with open(path) as f:
            return Lens.from_dict(json.load(f))

    def standard_coeffs(self):
        """Even asphere coefficients A4, A6, ... in the standard form
        sum A_2m r^2m (mm units)."""
        out = np.zeros_like(self.a)
        for i in range(self.S):
            for j in range(self.a.shape[1]):
                p = 2 * j + 4
                out[i, j] = self.a[i, j] / self.rn[i] ** p
        return out

    # ---- surface shape ---------------------------------------------------
    def sag(self, i, r):
        r = np.asarray(r, float)
        c, k = self.c[i], self.k[i]
        r2 = r * r
        arg = 1.0 - (1.0 + k) * c * c * r2
        arg = np.maximum(arg, 1e-12)
        z = c * r2 / (1.0 + np.sqrt(arg))
        u2 = r2 / self.rn[i] ** 2
        up = u2 * u2
        for j in range(self.a.shape[1]):
            z = z + self.a[i, j] * up
            up = up * u2
        return z

    def dsag_dr(self, i, r):
        r = np.asarray(r, float)
        c, k = self.c[i], self.k[i]
        arg = 1.0 - (1.0 + k) * c * c * r * r
        arg = np.maximum(arg, 1e-12)
        d = c * r / np.sqrt(arg)
        rn = self.rn[i]
        u = r / rn
        for j in range(self.a.shape[1]):
            p = 2 * j + 4
            d = d + self.a[i, j] * p * u ** (p - 1) / rn
        return d

    def sag_valid(self, i, r):
        c, k = self.c[i], self.k[i]
        return 1.0 - (1.0 + k) * c * c * np.asarray(r) ** 2 > 0


# --------------------------------------------------------------------------
# real ray trace
# --------------------------------------------------------------------------
def trace(lens, P, D, wl, upto=None, z_image=None, keep=False):
    """Trace rays. P, D: (N,3) start points (in air, before surface 0) and
    unit directions. Returns dict with final P, D, OPL, valid, and per-surface
    hit heights if keep. upto: trace only through surface index upto
    (inclusive), no image plane."""
    P = P.copy()
    D = D.copy()
    N = P.shape[0]
    valid = np.ones(N, bool)
    opl = np.zeros(N)
    zv = lens.z_vertex()
    n1 = 1.0
    last = lens.S - 1 if upto is None else upto
    hits = []
    for i in range(last + 1):
        n2 = n_of(lens.mat[i], wl)
        # Newton intersection
        z0 = zv[i]
        t = (z0 - P[:, 2]) / D[:, 2]
        for _ in range(12):
            X = P + t[:, None] * D
            r = np.hypot(X[:, 0], X[:, 1])
            s = lens.sag(i, r)
            f = (X[:, 2] - z0) - s
            dsr = lens.dsag_dr(i, r)
            with np.errstate(invalid="ignore", divide="ignore"):
                drdt = np.where(r > 1e-12, (X[:, 0] * D[:, 0] + X[:, 1] * D[:, 1]) / r, 0.0)
            fp = D[:, 2] - dsr * drdt
            fp = np.where(np.abs(fp) < 1e-9, 1e-9, fp)
            t = t - f / fp
        X = P + t[:, None] * D
        r = np.hypot(X[:, 0], X[:, 1])
        valid &= lens.sag_valid(i, r) & np.isfinite(t) & (np.abs(f) < 1e-7)
        dsr = lens.dsag_dr(i, r)
        with np.errstate(invalid="ignore", divide="ignore"):
            cx = np.where(r > 1e-12, X[:, 0] / r, 0.0)
            cy = np.where(r > 1e-12, X[:, 1] / r, 0.0)
        Nrm = np.stack([-dsr * cx, -dsr * cy, np.ones(N)], 1)
        Nrm /= np.linalg.norm(Nrm, axis=1)[:, None]
        opl += n1 * t
        valid &= t > -1e-9
        mu = n1 / n2
        cosi = np.sum(Nrm * D, 1)
        rad = 1.0 - mu * mu * (1.0 - cosi * cosi)
        valid &= rad > 0
        rad = np.maximum(rad, 0.0)
        D = mu * D + (np.sqrt(rad) - mu * cosi)[:, None] * Nrm
        D /= np.linalg.norm(D, axis=1)[:, None]
        P = X
        if keep:
            hits.append(dict(r=r.copy(), cosi=cosi.copy(), X=X.copy()))
        n1 = n2
    out = dict(P=P, D=D, opl=opl, valid=valid, n=n1, hits=hits)
    if upto is None:
        zi = zv[-1] + lens.t[-1] if z_image is None else z_image
        t = (zi - P[:, 2]) / D[:, 2]
        out["P"] = P + t[:, None] * D
        out["opl"] = opl + n1 * t
        out["D"] = D
    return out


# --------------------------------------------------------------------------
# paraxial trace
# --------------------------------------------------------------------------
def paraxial(lens, wl=WL_D):
    """Marginal ray (y=1, u=0) gives EFL and BFL. Chief ray from the stop
    centre gives the exit pupil."""
    ns = [1.0] + [n_of(m, wl) for m in lens.mat]
    y, nu = 1.0, 0.0
    for i in range(lens.S):
        nu = nu - y * lens.c[i] * (ns[i + 1] - ns[i])
        if i < lens.S - 1:
            y = y + lens.t[i] * nu / ns[i + 1]
    efl = -1.0 / nu
    bfl = -y / (nu / ns[-1])
    # exit pupil: chief ray starting at the stop centre with unit angle
    y, nu = 0.0, ns[lens.stop + 1] * 1.0
    for i in range(lens.stop + 1, lens.S):
        y = y + lens.t[i - 1] * nu / ns[i]
        nu = nu - y * lens.c[i] * (ns[i + 1] - ns[i])
    if lens.stop == lens.S - 1:
        y_last, u_last = 0.0, 1.0
    else:
        y_last, u_last = y, nu / ns[-1]
    # exit pupil distance measured from the last surface vertex (negative = before)
    xp_from_last = -y_last / u_last if abs(u_last) > 1e-12 else np.inf
    return dict(efl=efl, bfl=bfl, xp_from_last=xp_from_last)


# --------------------------------------------------------------------------
# ray aiming and pupil samplings
# --------------------------------------------------------------------------
def hexapolar(rings):
    pts = [(0.0, 0.0)]
    for k in range(1, rings + 1):
        rr = k / rings
        n = 6 * k
        a = 2 * np.pi * np.arange(n) / n
        pts += list(zip(rr * np.cos(a), rr * np.sin(a)))
    return np.array(pts)


def square_pupil(n):
    g = (np.arange(n) + 0.5) / n * 2 - 1
    X, Y = np.meshgrid(g, g)
    m = X ** 2 + Y ** 2 <= 1.0
    return np.stack([X[m], Y[m]], 1), (X, Y, m)


def _stop_hit(lens, P, D, wl):
    if lens.stop == 0 and lens.c[0] == 0 and not np.any(lens.a[0]):
        t = -P[:, 2] / D[:, 2]
        X = P + t[:, None] * D
        return X[:, :2], np.ones(len(P), bool)
    o = trace(lens, P, D, wl, upto=lens.stop)
    return o["P"][:, :2], o["valid"]


def rays_for_field(lens, theta_deg, pupil_xy, wl, z0=-1.0, iters=4):
    """Rays from infinity at field angle theta (in y), aimed so that they cross
    the stop surface at pupil_xy * (stop semi-aperture). The stop semi-aperture
    is set by the paraxial EPD scaled to the stop surface on axis."""
    th = np.radians(theta_deg)
    Dd = np.array([0.0, np.sin(th), np.cos(th)])
    N = len(pupil_xy)
    D = np.tile(Dd, (N, 1))
    # stop semi-aperture: aim the on-axis marginal ray of the entrance pupil
    sa = stop_semi_aperture(lens, wl)
    target = pupil_xy * sa
    # initial guess: start points on plane z0 shifted back along the field
    base = np.zeros((N, 3))
    base[:, 2] = z0
    base[:, 1] = z0 * np.tan(th)  # passes near vertex
    base[:, :2] += pupil_xy * lens.epd / 2
    P = base.copy()
    h = 1e-4
    for _ in range(iters):
        hit, v = _stop_hit(lens, P, D, wl)
        err = target - hit
        if np.max(np.abs(err)) < 1e-7:
            break
        Px = P.copy(); Px[:, 0] += h
        Py = P.copy(); Py[:, 1] += h
        hx, _ = _stop_hit(lens, Px, D, wl)
        hy, _ = _stop_hit(lens, Py, D, wl)
        J11 = (hx[:, 0] - hit[:, 0]) / h; J21 = (hx[:, 1] - hit[:, 1]) / h
        J12 = (hy[:, 0] - hit[:, 0]) / h; J22 = (hy[:, 1] - hit[:, 1]) / h
        det = J11 * J22 - J12 * J21
        det = np.where(np.abs(det) < 1e-12, 1e-12, det)
        dx = (J22 * err[:, 0] - J12 * err[:, 1]) / det
        dy = (-J21 * err[:, 0] + J11 * err[:, 1]) / det
        P[:, 0] += dx
        P[:, 1] += dy
    return P, D


_SA_CACHE = {}


def stop_semi_aperture(lens, wl=WL_D):
    """Semi-aperture of the stop that gives the design EPD (paraxially)."""
    if lens.stop == 0:
        return lens.epd / 2
    ns = [1.0] + [n_of(m, WL_D) for m in lens.mat]
    y, nu = lens.epd / 2, 0.0
    for i in range(lens.stop):
        nu = nu - y * lens.c[i] * (ns[i + 1] - ns[i])
        y = y + lens.t[i] * nu / ns[i + 1]
    return abs(y)


# --------------------------------------------------------------------------
# image quality helpers
# --------------------------------------------------------------------------
def chief_height(lens, theta_deg, wl=WL_D, z_image=None):
    P, D = rays_for_field(lens, theta_deg, np.zeros((1, 2)), wl)
    o = trace(lens, P, D, wl, z_image=z_image)
    return o["P"][0, 1], o["D"][0], o["valid"][0]


def field_angle_for_height(lens, h_target, wl=WL_D, guess=44.0):
    """Secant search for the field angle whose chief ray lands at h_target."""
    a0, a1 = guess * 0.9, guess
    h0 = chief_height(lens, a0, wl)[0]
    h1 = chief_height(lens, a1, wl)[0]
    for _ in range(25):
        if abs(h1 - h0) < 1e-12:
            break
        a2 = a1 + (h_target - h1) * (a1 - a0) / (h1 - h0)
        a2 = float(np.clip(a2, 1.0, 70.0))
        a0, h0 = a1, h1
        a1 = a2
        h1 = chief_height(lens, a1, wl)[0]
        if abs(h1 - h_target) < 1e-7:
            break
    return a1


def opd_and_cosines(lens, theta, pupil, wl, ref_point=None, z_image=None):
    """OPD (waves) of each ray against a reference sphere centred on
    ref_point (x,y on the image plane), passing through the exit pupil centre
    of the chief ray. Returns (opd_waves, l, m, valid, image xy)."""
    P, D = rays_for_field(lens, theta, pupil, wl)
    o = trace(lens, P, D, wl, z_image=z_image)
    Pc, Dc = rays_for_field(lens, theta, np.zeros((1, 2)), wl)
    oc = trace(lens, Pc, Dc, wl, z_image=z_image)
    zi = o["P"][0, 2]
    if ref_point is None:
        ref_point = oc["P"][0, :2]
    Pref = np.array([ref_point[0], ref_point[1], zi])
    par = paraxial(lens, wl)
    zlast = lens.z_vertex()[-1]
    zxp = zlast + par["xp_from_last"]
    # exit pupil point of the chief ray
    tc = (zxp - oc["P"][0, 2]) / oc["D"][0, 2]
    E = oc["P"][0] + tc * oc["D"][0]
    R = np.linalg.norm(E - Pref)

    def to_sphere(Pi, Di, opl_i):
        # go back from the image plane along the ray to the reference sphere
        # |Pi - s Di - Pref| = R, take the root on the pupil side (s > 0)
        w = Pi - Pref
        b = np.sum(w * Di, 1)
        cc = np.sum(w * w, 1) - R * R
        disc = np.maximum(b * b - cc, 0)
        s = b + np.sqrt(disc)
        return opl_i - s

    L = to_sphere(o["P"], o["D"], o["opl"])
    Lc = to_sphere(oc["P"], oc["D"], oc["opl"])[0]
    # plane-wave start offset: rays start on different planes; correct to a
    # common wavefront plane normal to the field direction through origin
    Dd = Dc[0]
    start_off = P @ Dd  # projection of start point on field direction
    start_off_c = Pc[0] @ Dd
    L = L + start_off
    Lc = Lc + start_off_c
    opd = (L - Lc) / (wl * 1e-3)
    return opd, o["D"][:, 0], o["D"][:, 1], o["valid"], o["P"][:, :2]


def mtf_wave(lens, theta, freqs, waves=WAVES, weights=WEIGHTS, n_pupil=48,
             grid=256, z_image=None):
    """Polychromatic diffraction MTF, tangential (y) and sagittal (x).
    The pupil function is resampled on a uniform grid in image-space direction
    cosines (l, m); the OTF is its autocorrelation. A shift of dl in l
    corresponds to dl / wavelength cycles per mm on the image plane."""
    from scipy.interpolate import griddata
    pup, _ = square_pupil(n_pupil)
    # common polychromatic reference: centroid at d
    data = []
    cents = []
    for wl in waves:
        opd, l, m, v, xy = opd_and_cosines(lens, theta, pup, wl, z_image=z_image)
        data.append((wl, l, m, v))
        cents.append(xy[v].mean(0))
    ref = np.average(np.array(cents), axis=0, weights=weights)
    lm_all = np.concatenate([np.stack([d[1][d[3]], d[2][d[3]]], 1) for d in data])
    lc = lm_all.mean(0)
    span = np.max(np.abs(lm_all - lc)) * 1.02
    dl = 2 * span / (grid / 2)  # pupil occupies half the grid (2x padding)
    ax = (np.arange(grid) - grid / 2) * dl
    Lg, Mg = np.meshgrid(ax + lc[0], ax + lc[1])
    otf_t = np.zeros(len(freqs), complex)
    otf_s = np.zeros(len(freqs), complex)
    wsum = 0.0
    from scipy.spatial import ConvexHull
    from matplotlib.path import Path
    for (wl, l, m, v), w in zip(data, weights):
        opd, l, m, v, xy = opd_and_cosines(lens, theta, pup, wl, ref_point=ref, z_image=z_image)
        pts = np.stack([l[v], m[v]], 1)
        W = griddata(pts, opd[v], (Lg, Mg), method="linear")
        hull = Path(pts[ConvexHull(pts).vertices])
        inside = hull.contains_points(np.stack([Lg.ravel(), Mg.ravel()], 1)).reshape(Lg.shape)
        inside &= np.isfinite(W)
        # amplitude: uniform in entrance pupil maps to non-uniform in (l,m);
        # use the local Jacobian via ray density. First order: uniform.
        Pf = np.where(inside, np.exp(2j * np.pi * np.nan_to_num(W)), 0)
        F = np.fft.fft2(Pf)
        ac = np.fft.ifft2(np.abs(F) ** 2)
        ac0 = ac[0, 0]
        wlmm = wl * 1e-3
        for q, nu in enumerate(freqs):
            s = nu * wlmm / dl  # shift in grid cells
            i0 = int(np.floor(s)); fr = s - i0
            # tangential: shift in m (rows); sagittal: shift in l (cols)
            def at(idx_r, idx_c):
                return ac[idx_r % grid, idx_c % grid]
            vt = (1 - fr) * at(i0, 0) + fr * at(i0 + 1, 0)
            vs = (1 - fr) * at(0, i0) + fr * at(0, i0 + 1)
            otf_t[q] += w * vt / ac0
            otf_s[q] += w * vs / ac0
        wsum += w
    return np.abs(otf_t / wsum), np.abs(otf_s / wsum), ref


def diffraction_limit_mtf(nu, wl_um, fnum):
    nc = 1.0 / (wl_um * 1e-3 * fnum)
    x = np.clip(np.asarray(nu, float) / nc, 0, 1)
    return 2 / np.pi * (np.arccos(x) - x * np.sqrt(1 - x * x))
