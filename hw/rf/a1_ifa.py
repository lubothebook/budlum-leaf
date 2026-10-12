#!/usr/bin/env python3
"""a1_ifa.py - A1, the 2.4 GHz inverted-F in the 32 x 4 x 1.00 mm LCP bar.

Gate RF-22 (A1 at -2.5 dB or better), RF-18 (tuner), RF-9.

Three models, one design:
 1. The transmission-line (TL) model. The arm over the edge ground is a line
    with Z0 and eps_eff from cs2d.py. The short leg, the feed leg, the tuner
    leg and the open end are lumped. The radiation is a conductance at the
    open end.
 2. The thin-wire method of moments (mom_wire.py). The arm, the legs and the
    80 x 160 mm body ground as a wire grid. In air it is the reference for the
    TL model. With capacitor legs that stand for the LCP it checks the
    dielectric case.
 3. The design: arm length, feed tap, tuner tap, matching network, tuner
    states, the bandwidth and the efficiency budget.

Run: python3 a1_ifa.py            (uses cached MoM sweeps in out/)
     python3 a1_ifa.py --fresh    (recomputes the MoM, about 15 min)
"""
import json
import os
import sys
import numpy as np
from scipy.optimize import least_squares, brentq
from rf_common import (C0, MU0, EPS0, SIGMA, surface_resistance, db, EPS_LCP_GF40,
                       TAN_LCP_GF40)
from mom_wire import Wires, solve_ports, far_field, radiated_power
import geom_body as G

MM = 1e-3
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FRESH = "--fresh" in sys.argv
CS = json.load(open(os.path.join(OUT, "cs2d.json")))["A1_overhang"]

# ------------------------------------------------------------ the layout [DECISION of this team]
# bar x = 19..51 mm on the top edge, seat tile x = 30..40 mm, A4 at x = 19.5..30
GEOM = dict(x_short=30.0 * MM, x_feed=32.0 * MM, x_tune=38.0 * MM, x_open=50.0 * MM)
W_STRIP = 1.6 * MM
WIFI24 = (2.400e9, 2.4835e9)
F0 = 2.442e9

# tuner: SP4T aperture switch with four fixed capacitors [HYPOTHESIS] part class of BGSA14GN10
RON, COFF = 1.0, 0.16e-12          # Ohm, F per off path [HYPOTHESIS] typical SP4T aperture switch
CAP_Q = 80.0                       # 0201 C0G at 2.4 GHz [GENERAL]
IND_Q = 45.0                       # 0201 thin-film inductor at 2.4 GHz [GENERAL]


# ======================================================================= TL model
def _line(Z0, g, l, V, I):
    """Move (V, I) from the far end to the near end of a line of length l."""
    ch, sh = np.cosh(g * l), np.sinh(g * l)
    return ch * V + Z0 * sh * I, sh / Z0 * V + ch * I


def line_params(f, Z0, ee, strip_w=W_STRIP, ground="SS304"):
    """Propagation constant with conductor and dielectric loss [GENERAL]."""
    f = np.asarray(f, float)
    beta = 2 * np.pi * f * np.sqrt(ee) / C0
    rs_cu = surface_resistance(f, SIGMA["Cu_LDS"])
    rs_g = surface_resistance(f, SIGMA[ground])
    Rp = 1.5 * rs_cu / (2 * strip_w) + rs_g / G.EDGE_W
    ac = Rp / (2 * Z0)
    er = EPS_LCP_GF40
    ad = 0.0
    if ee > 1.0001:
        ad = (2 * np.pi * f / C0) * er * (ee - 1) * TAN_LCP_GF40 / (2 * np.sqrt(ee) * (er - 1))
    return ac + ad + 1j * beta


def tl_ifa(f, prm, geom=GEOM, Zt=None, ground="SS304", lossless=False):
    """Input impedance and power split of the IFA for 1 A at the port.

    f may be an array. prm: Z0, ee, Ls (short leg), Lf (feed leg), Lt (tuner
    leg), Ce (open end), Gr0 (radiation conductance at F0, scales as f^2).
    Zt: the tuner branch impedance at f (None = no tuner leg).
    """
    f = np.asarray(f, float)
    w = 2 * np.pi * f
    g = line_params(f, prm["Z0"], prm["ee"], ground=ground)
    if lossless:
        g = 1j * g.imag
    Z0 = prm["Z0"]
    S = geom["x_feed"] - geom["x_short"]
    # left branch: short leg, then the line S to the feed
    Vs = 1j * w * prm["Ls"] + 0.02 * (not lossless)
    Vl, Il = _line(Z0, g, S, Vs, np.ones_like(Vs))
    Yleft = Il / Vl
    # right branch: open end, line l2, tuner tap, line l1
    Gr = prm["Gr0"] * (f / F0) ** 2
    Ye = Gr + 1j * w * prm["Ce"]
    if Zt is None:
        l1, l2 = geom["x_open"] - geom["x_feed"], 0.0
    else:
        l1, l2 = geom["x_tune"] - geom["x_feed"], geom["x_open"] - geom["x_tune"]
    Ve = np.ones_like(Ye)
    V2, I2 = _line(Z0, g, l2, Ve, Ye * Ve)
    It = 0.0
    if Zt is not None:
        It = V2 / (Zt + 1j * w * prm["Lt"])
        I2 = I2 + It
    Vj, Ij = _line(Z0, g, l1, V2, I2)
    Yj = Ij / Vj + Yleft
    Zin = 1j * w * prm["Lf"] + 1.0 / Yj
    k = (1.0 / Yj) / Vj
    Prad = 0.5 * Gr * np.abs(k) ** 2
    Ptun = 0.5 * np.real(Zt) * np.abs(It * k) ** 2 if Zt is not None else 0.0 * Prad
    Pin = 0.5 * np.real(Zin)
    return Zin, dict(Pin=Pin, Prad=Prad, Ptun=Ptun, eta=Prad / Pin)


def tuner_Z(f, C_on):
    """SP4T aperture switch to ground: the on path carries C_on, the rest are off."""
    w = 2 * np.pi * np.asarray(f, float)
    if C_on is None or C_on <= 0:
        return 1.0 / (1j * w * 4 * COFF)
    zon = RON + 1.0 / (1j * w * C_on) + 1.0 / (w * C_on * CAP_Q)
    zoff = 1.0 / (1j * w * 3 * COFF)
    return 1.0 / (1.0 / zon + 1.0 / zoff)


def f_parallel(prm, geom, Ct, lo=1.6e9, hi=3.6e9, n=4001, **kw):
    fg = np.linspace(lo, hi, n)
    z, _ = tl_ifa(fg, prm, geom, Zt=tuner_Z(fg, Ct), **kw)
    i = int(np.argmax(z.real))
    return fg[i] if 0 < i < n - 1 else np.nan


def c_for_freq(prm, geom, ftarget, cmax=8e-12):
    """Tuner capacitance that puts the parallel resonance at ftarget."""
    cs = np.geomspace(0.05e-12, cmax, 90)
    fr = np.array([f_parallel(prm, geom, c) for c in cs])
    ok = ~np.isnan(fr)
    cs, fr = cs[ok], fr[ok]
    # the resonance falls as C rises (capacitive tap); interpolate on the monotone part
    for a, b, fa, fb in zip(cs[:-1], cs[1:], fr[:-1], fr[1:]):
        if (fa - ftarget) * (fb - ftarget) <= 0 and fa != fb:
            lo, hi, flo = a, b, fa
            for _ in range(30):
                m = np.sqrt(lo * hi)
                fm = f_parallel(prm, geom, m)
                if np.isnan(fm):
                    break
                if (flo - ftarget) * (fm - ftarget) <= 0:
                    hi = m
                else:
                    lo, flo = m, fm
            return np.sqrt(lo * hi)
    return None


# ======================================================================= MoM runs
def build_mom(f, geom=GEOM, cload=0.0, lossy=True, metal="SS304", Ct=None):
    W = Wires()
    ye = G.plate(W, f, metal=metal)
    if not lossy:
        W.rloss = [0.0] * len(W.rloss)
    nodes = G.ifa(W, f, geom["x_short"], geom["x_feed"],
                  geom["x_tune"] if Ct is not False else None, geom["x_open"],
                  y_arm=ye + G.ARM_DY, ymin_ground=ye - 1e-6, cload_per_m=cload)
    if not lossy:
        W.rloss = [0.0] * len(W.rloss)
    if Ct is not False and "tune" in nodes:
        W.loads[nodes["tune"]] = (lambda C: (lambda ff: tuner_Z(ff, C)))(Ct)
    W.finish()
    return W, nodes


def mom_sweep(name, freqs, **kw):
    path = os.path.join(OUT, f"mom_{name}.npz")
    key = repr(sorted((k, (round(v, 9) if isinstance(v, float) else (sorted((a, round(b, 7)) for a, b in v.items()) if isinstance(v, dict) else v)))
                      for k, v in kw.items()))
    if os.path.exists(path) and not FRESH:
        d = np.load(path)
        if len(d["f"]) == len(freqs) and np.allclose(d["f"], freqs) and str(d["key"]) == key:
            return d["Z"], d["eta"]
    Z, eta = [], []
    for f in freqs:
        W, n = build_mom(f, **kw)
        Zp, I, Rl, pb = solve_ports(W, f, [n["feed"]])
        Iv = I[:, 0]
        Pin = 0.5 * np.real(np.conj(Iv[pb[0]]))
        Pl = 0.5 * np.real(np.conj(Iv) @ (Rl @ Iv))
        Z.append(Zp[0, 0]); eta.append((Pin - Pl) / Pin)
        print(f"    MoM {name}: {f/1e9:6.3f} GHz  Z = {Zp[0,0].real:8.2f} {Zp[0,0].imag:+8.2f}j  eta_rad = {eta[-1]:.3f}",
              flush=True)
    Z, eta = np.array(Z), np.array(eta)
    np.savez(path, f=freqs, Z=Z, eta=eta, key=key)
    return Z, eta


def parallel_res(freqs, Z):
    """Frequency of the peak of Re Z (the parallel resonance), by a parabola."""
    i = int(np.argmax(Z.real))
    i = min(max(i, 1), len(Z) - 2)
    y = Z.real[i - 1:i + 2]; x = freqs[i - 1:i + 2]
    a, b, c = np.polyfit(x, y, 2)
    return -b / (2 * a), c - b * b / (4 * a)


# ======================================================================= main
def main():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    print("A1 inverted-F, 2.4 GHz, in the 1.00 mm LCP bar")
    print(f"  cs2d line: Z0 = {CS['Z0']:.1f} Ohm, eps_eff = {CS['eps_eff']:.2f}; air Z0 = {CS['Z0_air']:.1f} Ohm")
    print(f"  layout: short x = 30, feed x = 32, tuner x = 38, open end x = 50 mm (arm 20.0 mm)")

    # ---------------------------------------------------------------- 1. air, no tuner, lossless
    fa = np.linspace(2.7e9, 3.3e9, 7)
    print("  [1] MoM in air, no tuner leg, lossless (the TL reference)")
    Za, _ = mom_sweep("air", fa, cload=0.0, lossy=False, Ct=False)
    fr_a, R_a = parallel_res(fa, Za)

    # unfitted analytic TL in air: leg inductance of a 2.6 mm wire [GENERAL]
    lleg = 2.6 * MM
    Lleg = MU0 * lleg / (2 * np.pi) * (np.log(2 * lleg / (0.2 * MM)) - 1)
    Ce0 = 0.5 * MM * CS["Ca"]          # open-end fringe = 0.5 mm of line [GENERAL]
    pr0 = dict(Z0=CS["Z0_air"], ee=1.0, Ls=Lleg, Lf=Lleg, Lt=Lleg, Ce=Ce0, Gr0=1e-4)
    fgrid = np.linspace(2.5e9, 3.6e9, 1101)
    Z0tl = np.array([tl_ifa(f, pr0, Zt=None)[0] for f in fgrid])
    fr_tl0 = fgrid[np.argmax(Z0tl.real)]
    print(f"      MoM air parallel resonance {fr_a/1e9:.3f} GHz, R = {R_a:.0f} Ohm")
    print(f"      TL air, analytic legs ({Lleg*1e9:.2f} nH), unfitted: {fr_tl0/1e9:.3f} GHz"
          f"  -> error {100*(fr_tl0/fr_a-1):+.1f} %")

    # fit the lumped parts of the TL to the MoM
    def resid(x):
        p = dict(Z0=CS["Z0_air"] * x[0], ee=1.0, Ls=x[1] * 1e-9, Lf=x[2] * 1e-9, Lt=0,
                 Ce=x[3] * 1e-12, Gr0=x[4] * 1e-4)
        r = []
        for f, zm in zip(fa, Za):
            zt = tl_ifa(f, p, Zt=None)[0]
            ym, yt = 1 / zm, 1 / zt
            r += [(ym - yt).real * 100, (ym - yt).imag * 100]
        return r
    x0 = [1.0, Lleg * 1e9, Lleg * 1e9, Ce0 * 1e12, 1.0]
    fit = least_squares(resid, x0, bounds=([0.6, 0, 0, 0, 0.01], [3.0, 5, 5, 1, 100]))
    kz, Ls, Lf, Ce, Gr0 = fit.x
    prm_air = dict(Z0=CS["Z0_air"] * kz, ee=1.0, Ls=Ls * 1e-9, Lf=Lf * 1e-9, Lt=Ls * 1e-9,
                   Ce=Ce * 1e-12, Gr0=Gr0 * 1e-4)
    Zfit = np.array([tl_ifa(f, prm_air, Zt=None)[0] for f in fa])
    rms = np.sqrt(np.mean(np.abs(1 / Zfit - 1 / Za) ** 2)) / np.sqrt(np.mean(np.abs(1 / Za) ** 2))
    print(f"      TL fitted to MoM: Z0 x {kz:.2f}, Ls = {Ls:.2f} nH, Lf = {Lf:.2f} nH, Ce = {Ce*1e3:.1f} fF,"
          f" Gr = {Gr0*1e-4*1e3:.3f} mS. Relative rms error of Y: {100*rms:.1f} %")
    res["air"] = dict(f_mom=fr_a, R_mom=R_a, f_tl_unfitted=fr_tl0, fit=list(fit.x), rms_Y=rms)

    # ---------------------------------------------------------------- 2. LCP loading
    cextra = CS["C"] - CS["Ca"]
    fd = np.linspace(2.0e9, 2.6e9, 7)
    print(f"  [2] MoM with capacitor legs for the LCP ({cextra*1e12:.1f} pF/m every 2 mm), lossless")
    Zd, _ = mom_sweep("lcp", fd, cload=cextra, lossy=False, Ct=False)
    fr_d, R_d = parallel_res(fd, Zd)
    # the cap legs add a line of Z0 / sqrt(ee) with the same legs; open end gains the LCP fringe
    prm = dict(prm_air)
    prm.update(Z0=prm_air["Z0"] / np.sqrt(CS["eps_eff"]), ee=CS["eps_eff"], Ce=prm_air["Ce"] * CS["eps_eff"])
    fg = np.linspace(1.9e9, 2.9e9, 2001)
    Ztl = np.array([tl_ifa(f, prm, Zt=None)[0] for f in fg])
    fr_tld = fg[np.argmax(Ztl.real)]
    print(f"      MoM: {fr_d/1e9:.3f} GHz (R = {R_d:.0f} Ohm).  TL with cs2d eps_eff, no refit: {fr_tld/1e9:.3f} GHz"
          f"  -> error {100*(fr_tld/fr_d-1):+.1f} %")
    res["lcp"] = dict(f_mom=fr_d, R_mom=R_d, f_tl=fr_tld)

    # ---------------------------------------------------------------- 3. the design search (TL)
    print("  [3] design search: arm length, feed tap, tuner tap (SP4T + C0G caps, Ron 1.0 Ohm, Coff 0.16 pF/path)")
    best = None
    for xo in (42.0, 44.0, 46.0, 48.0, 50.0):
        for sf in (1.5, 2.5, 3.5):
            for xt in (35.0, 37.5, 39.5):
                geom = dict(x_short=30.0 * MM, x_feed=(30.0 + sf) * MM, x_tune=xt * MM, x_open=xo * MM)
                if geom["x_tune"] <= geom["x_feed"] + 0.5 * MM:
                    continue
                ev = evaluate(prm, geom)
                if ev is None:
                    continue
                if best is None or ev["worst_dB"] > best["worst_dB"]:
                    best = dict(ev, geom=geom)
    geom = best["geom"]
    print(f"      best: open end x = {geom['x_open']/MM:.1f} mm (arm {(geom['x_open']-geom['x_short'])/MM:.1f} mm),"
          f" feed x = {geom['x_feed']/MM:.1f}, tuner x = {geom['x_tune']/MM:.1f} mm")
    print(f"      off-state resonance {best['f_off']/1e9:.3f} GHz; mid-state feed Z {best['Zmid'].real:.1f} {best['Zmid'].imag:+.1f}j Ohm")
    print(f"      matching: {best['net']['desc']}")
    for k, v in best["states"].items():
        print(f"      state {k:4s}: C_on = {v['C']*1e12:5.2f} pF; over {v['span'][0]/1e9:.3f}-{v['span'][1]/1e9:.4f} GHz"
              f" worst S11 {v['s11_worst']:+.1f} dB, radiation eff {v['eta_rad_dB']:+.2f} dB,"
              f" total eff worst {v['tot_worst_dB']:+.2f} dB, mean {v['tot_mean_dB']:+.2f} dB")
    print(f"      RF-22 A1 target -2.5 dB: worst total efficiency in band {best['worst_dB']:+.2f} dB"
          f" -> {'PASS' if best['worst_dB'] >= -2.5 else 'NOT YET'}")
    res["design"] = dict(geom_mm={k: v / MM for k, v in geom.items()}, f_off=best["f_off"],
                         Zmid=[best["Zmid"].real, best["Zmid"].imag], match=best["net"]["desc"],
                         states={k: dict(C_pF=v["C"] * 1e12, s11_worst=v["s11_worst"], eta_rad_dB=v["eta_rad_dB"],
                                         tot_worst_dB=v["tot_worst_dB"], tot_mean_dB=v["tot_mean_dB"])
                                 for k, v in best["states"].items()},
                         worst_dB=best["worst_dB"])
    # with a copper-flashed can ground
    evc = evaluate(prm, geom, ground="Cu")
    print(f"      the same with a 2 um copper flash on the can edge: worst total {evc['worst_dB']:+.2f} dB")
    res["design"]["worst_dB_Cu"] = evc["worst_dB"]

    # Q and bandwidth of the mid state [GENERAL] Yaghjian-Best
    Cmid = best["states"]["mid"]["C"]
    fb = np.linspace(2.30e9, 2.60e9, 3001)
    zz, _ = tl_ifa(fb, prm, geom, Zt=tuner_Z(fb, Cmid))
    y = 1 / zz
    i0 = int(np.argmax(zz.real))
    dB_ = np.gradient(y.imag, fb)[i0]
    Q = fb[i0] * abs(dB_) / (2 * y.real[i0])
    fbw = (3 - 1) / (np.sqrt(3) * Q)
    print(f"  [4] antenna Q at the mid state = {Q:.0f}: VSWR-3 bandwidth {100*fbw:.2f} % = {fbw*F0/1e6:.0f} MHz per state;"
          f" the band needs {(WIFI24[1]-WIFI24[0])/1e6:.1f} MHz")
    res["Q_mid"] = Q

    # n78 reach of the same aperture tuner (time-shared outdoors) [HYPOTHESIS] use case
    fr_off = f_parallel(prm, geom, None, hi=5e9)
    print(f"      tuner off: parallel resonance {fr_off/1e9:.2f} GHz (reach for 5G n78 3.3-3.8 GHz:"
          f" {'yes' if fr_off >= 3.3e9 else 'no, needs an inductive state'})")
    res["f_off_wide"] = fr_off

    # ---------------------------------------------------------------- 4. MoM check of the final design, with losses
    print("  [5] MoM check of the design, mid state, with conductor loss (LCP as capacitor legs)")
    fchk = np.array([2.40e9, 2.42e9, 2.44e9, 2.46e9, 2.48e9])
    out = {}
    for metal in ("SS304", "Cu"):
        Zc, ec = mom_sweep(f"final_{metal}", fchk, geom=geom, cload=cextra, lossy=True, metal=metal, Ct=Cmid)
        zt, pw = tl_ifa(fchk, prm, geom, Zt=tuner_Z(fchk, Cmid), ground=metal)
        out[metal] = dict(Z=[(z.real, z.imag) for z in Zc], eta_dB=[db(e) for e in ec],
                          Z_tl=[(z.real, z.imag) for z in zt], eta_tl_dB=[db(e) for e in pw["eta"]])
        for f, zm, em, zl, el in zip(fchk, Zc, ec, zt, pw["eta"]):
            print(f"      {metal:5s} {f/1e9:.2f} GHz  MoM Z {zm.real:6.1f}{zm.imag:+7.1f}j  eta {db(em):+.2f} dB"
                  f"   |  TL Z {zl.real:6.1f}{zl.imag:+7.1f}j  eta {db(el):+.2f} dB")
    res["mom_final"] = out
    res["prm"] = {k: float(v) for k, v in prm.items()}
    json.dump(res, open(os.path.join(OUT, "a1_ifa.json"), "w"), indent=1, default=float)
    print("  wrote out/a1_ifa.json")


GROUPS = {"low": (2.401e9, 2.428e9), "mid": (2.428e9, 2.453e9), "high": (2.453e9, 2.4835e9)}


def tot_eff(fs, prm, geom, c, net, ground="SS304"):
    z, pw = tl_ifa(fs, prm, geom, Zt=tuner_Z(fs, c), ground=ground)
    zl, lossnet = net_apply(net, z, fs)
    g = (zl - 50) / (zl + 50)
    return pw["eta"] * (1 - np.abs(g) ** 2) * lossnet, pw["eta"], 20 * np.log10(np.abs(g))


def evaluate(prm, geom, ground="SS304"):
    """Tune the mid state to 2.442 GHz, match it, then optimise each group state."""
    from scipy.optimize import minimize_scalar
    Cmid = c_for_freq(prm, geom, F0)
    if Cmid is None:
        return None
    Zmid = tl_ifa(np.array([F0]), prm, geom, Zt=tuner_Z(F0, Cmid), ground=ground)[0][0]
    net = l_match(Zmid, F0)
    states = {}
    worst = 0.0
    for name, (a, b) in GROUPS.items():
        fs = np.linspace(a, b, 9)
        def neg(lc):
            return -tot_eff(fs, prm, geom, np.exp(lc), net, ground)[0].min()
        r = minimize_scalar(neg, bounds=(np.log(0.05e-12), np.log(8e-12)), method="bounded")
        c = float(np.exp(r.x))
        te, er, s11 = tot_eff(fs, prm, geom, c, net, ground)
        states[name] = dict(C=c, span=(a, b), s11_worst=float(s11.max()), eta_rad_dB=float(db(er.mean())),
                            tot_worst_dB=float(db(te.min())), tot_mean_dB=float(db(te.mean())))
        worst = min(worst, db(te.min()))
    return dict(states=states, worst_dB=float(worst), net=net, Zmid=Zmid,
                f_off=f_parallel(prm, geom, None))


def l_match(Z, f):
    """Two-element L match to 50 Ohm; picks the shunt-first or series-first form."""
    w = 2 * np.pi * f
    R, X = Z.real, Z.imag
    Z0 = 50.0
    if R > Z0:
        # shunt element at the antenna, series towards the 50 Ohm port
        Q = np.sqrt(R / Z0 - 1)
        G = 1 / Z
        B_need = -G.imag + np.sqrt(G.real * (1 / Z0 - G.real) + 0j).real  # choose + root
        Bsh = B_need
        Yt = G + 1j * Bsh
        Zt = 1 / Yt
        Xse = -Zt.imag
        kind = "shunt-series"
    else:
        Xse = -X + np.sqrt(R * (Z0 - R))
        Zt = Z + 1j * Xse
        Yt = 1 / Zt
        Bsh = -Yt.imag
        kind = "series-shunt"
    def part(x, series):
        if series:
            return ("L", x / w) if x > 0 else ("C", -1 / (w * x))
        return ("C", x / w) if x > 0 else ("L", -1 / (w * x))
    se = part(Xse, True); sh = part(Bsh, False)
    def txt(p):
        return f"{p[1]*1e9:.2f} nH" if p[0] == "L" else f"{p[1]*1e12:.2f} pF"
    desc = (f"{kind}: shunt {sh[0]} {txt(sh)} at the antenna, series {se[0]} {txt(se)} to the port"
            if kind == "shunt-series" else
            f"{kind}: series {se[0]} {txt(se)} at the antenna, shunt {sh[0]} {txt(sh)} at the port")
    return dict(kind=kind, se=se, sh=sh, desc=desc)


def net_apply(net, Zant, f):
    """Impedance seen from the 50 Ohm port, and the network power efficiency."""
    w = 2 * np.pi * f
    def z_of(p, series):
        typ, v = p
        if typ == "L":
            return 1j * w * v + w * v / IND_Q
        return 1 / (1j * w * v) + 1 / (w * v * CAP_Q)
    zse = z_of(net["se"], True); zsh = z_of(net["sh"], False)
    if net["kind"] == "shunt-series":
        Za = 1 / (1 / Zant + 1 / zsh)
        Zp = Za + zse
        # power: current I through zse, then the shunt split
        I = 1.0
        Pin = 0.5 * Zp.real
        V = I * Za
        Pant = 0.5 * abs(V) ** 2 * (1 / Zant).real
    else:
        Zb = Zant + zse
        Zp = 1 / (1 / Zb + 1 / zsh)
        V = 1.0
        Pin = 0.5 * (1 / Zp).real
        I = V / Zb
        Pant = 0.5 * abs(I) ** 2 * Zant.real
    return Zp, Pant / Pin


if __name__ == "__main__":
    main()
