#!/usr/bin/env python3
"""pathloss.py - the published path loss models of the far link seat.

Every function returns the median path loss in dB and the shadow fading
sigma in dB. d is the 2D ground distance in metres, f the carrier in GHz.

Sources (all [PUBLICATION], formulas typed from the documents, not fetched):
  FSPL     Friis, ITU-R P.525
  UMa, UMi 3GPP TR 38.901 V16, Table 7.4.1-1 (path loss) and 7.4.3 (O2I)
  RMa      3GPP TR 38.901 V16, Table 7.4.1-1
  Indoor   ITU-R P.1238 (indoor, N coefficients of Table 2)
  O2       ITU-R P.676, about 15 dB/km at 60 GHz, sea level
  Rain     ITU-R P.838 order of magnitude, about 10 dB/km at 25 mm/h and 60 GHz [HYPOTHESIS]
  Hata     Okumura-Hata, only as a cross-check of UMa at 0.7 GHz
Validity ranges of 38.901: UMa and UMi 10 m to 5 km, RMa 10 m to 10 km (LOS) and
5 km (NLOS). Beyond them the formula is an extrapolation: valid() says so.
"""
import math

C = 299792458.0


def lg(x):
    return math.log10(x)


def fspl(d3d, f_ghz):
    return 20 * lg(4 * math.pi * d3d * f_ghz * 1e9 / C)


def _d3d(d2d, hbs, hut):
    return math.hypot(d2d, hbs - hut)


# ------------------------------------------------------------------ UMa
def uma_los(d2d, f, hbs=25.0, hut=1.5):
    d3 = _d3d(d2d, hbs, hut)
    dbp = 4 * (hbs - 1.0) * (hut - 1.0) * f * 1e9 / C
    if d2d <= dbp:
        pl = 28.0 + 22 * lg(d3) + 20 * lg(f)
    else:
        pl = 28.0 + 40 * lg(d3) + 20 * lg(f) - 9 * lg(dbp ** 2 + (hbs - hut) ** 2)
    return pl, 4.0


def uma_nlos(d2d, f, hbs=25.0, hut=1.5):
    d3 = _d3d(d2d, hbs, hut)
    pl_n = 13.54 + 39.08 * lg(d3) + 20 * lg(f) - 0.6 * (hut - 1.5)
    return max(uma_los(d2d, f, hbs, hut)[0], pl_n), 6.0


# ------------------------------------------------------------------ UMi street canyon
def umi_los(d2d, f, hbs=10.0, hut=1.5):
    d3 = _d3d(d2d, hbs, hut)
    dbp = 4 * (hbs - 1.0) * (hut - 1.0) * f * 1e9 / C
    if d2d <= dbp:
        pl = 32.4 + 21 * lg(d3) + 20 * lg(f)
    else:
        pl = 32.4 + 40 * lg(d3) + 20 * lg(f) - 9.5 * lg(dbp ** 2 + (hbs - hut) ** 2)
    return pl, 4.0


def umi_nlos(d2d, f, hbs=10.0, hut=1.5):
    d3 = _d3d(d2d, hbs, hut)
    pl_n = 35.3 * lg(d3) + 22.4 + 21.3 * lg(f) - 0.3 * (hut - 1.5)
    return max(umi_los(d2d, f, hbs, hut)[0], pl_n), 7.82


# ------------------------------------------------------------------ RMa
def _rma_pl1(d3, f, h):
    return (20 * lg(40 * math.pi * d3 * f / 3.0) + min(0.03 * h ** 1.72, 10) * lg(d3)
            - min(0.044 * h ** 1.72, 14.77) + 0.002 * lg(h) * d3)


def rma_los(d2d, f, hbs=35.0, hut=1.5, h=5.0):
    d3 = _d3d(d2d, hbs, hut)
    dbp = 2 * math.pi * hbs * hut * f * 1e9 / C
    if d2d <= dbp:
        return _rma_pl1(d3, f, h), 4.0
    d3b = _d3d(dbp, hbs, hut)
    return _rma_pl1(d3b, f, h) + 40 * lg(d3 / d3b), 6.0


def rma_nlos(d2d, f, hbs=35.0, hut=1.5, h=5.0, w=20.0):
    d3 = _d3d(d2d, hbs, hut)
    pl_n = (161.04 - 7.1 * lg(w) + 7.5 * lg(h) - (24.37 - 3.7 * (h / hbs) ** 2) * lg(hbs)
            + (43.42 - 3.1 * lg(hbs)) * (lg(d3) - 3) + 20 * lg(f)
            - (3.2 * lg(11.75 * hut) ** 2 - 4.97))
    return max(rma_los(d2d, f, hbs, hut, h)[0], pl_n), 8.0


# ------------------------------------------------------------------ O2I, 38.901 7.4.3
def o2i_loss(f, kind="low", d_in=12.5):
    """Building entry loss PL_tw + PL_in, dB. d_in: depth inside, mean of U(0,25) = 12.5 m."""
    l_glass = 2 + 0.2 * f
    l_iir = 23 + 0.3 * f
    l_conc = 5 + 4 * f
    if kind == "low":
        tw = 5 - 10 * lg(0.3 * 10 ** (-l_glass / 10) + 0.7 * 10 ** (-l_conc / 10))
    else:
        tw = 5 - 10 * lg(0.7 * 10 ** (-l_iir / 10) + 0.3 * 10 ** (-l_conc / 10))
    return tw + 0.5 * d_in, 4.4


# ------------------------------------------------------------------ ITU-R P.1238 indoor (office)
_P1238_N = [(0.9, 33), (1.25, 32), (1.9, 30), (4.0, 28), (5.2, 31), (60.0, 22)]


def p1238_n(f):
    pts = _P1238_N
    if f <= pts[0][0]:
        return pts[0][1]
    for (f0, n0), (f1, n1) in zip(pts, pts[1:]):
        if f <= f1:
            t = (lg(f) - lg(f0)) / (lg(f1) - lg(f0))
            return n0 + t * (n1 - n0)
    return pts[-1][1]


def p1238(d, f, floors=0):
    """L = 20 log f(MHz) + N log d + Lf - 28 ; Lf = 15 + 4(n-1) dB per floor count (office, P.1238)."""
    lf = 0.0 if floors == 0 else 15 + 4 * (floors - 1)
    return 20 * lg(f * 1e3) + p1238_n(f) * lg(max(d, 1.0)) + lf - 28, 3.0


# ------------------------------------------------------------------ gas, rain
def o2_db(d, f, rain_mm_h=0.0):
    """Atmospheric extra loss: oxygen at 60 GHz and an optional rain term. Zero below 20 GHz."""
    if f < 20:
        return 0.0
    gam = 15.0 if 55 <= f <= 66 else 0.1
    gam += 0.9 * rain_mm_h ** 0.75 if rain_mm_h else 0.0   # 25 mm/h gives about 10 dB/km: HYPOTHESIS
    return gam * d / 1000.0


def hata_urban(d, f_mhz, hb=30.0, hm=1.5):
    """Okumura-Hata, large city, valid 150-1500 MHz, 1-20 km."""
    a = 3.2 * lg(11.75 * hm) ** 2 - 4.97
    return (69.55 + 26.16 * lg(f_mhz) - 13.82 * lg(hb) - a
            + (44.9 - 6.55 * lg(hb)) * lg(d / 1000.0)), 8.0


# ------------------------------------------------------------------ the scenario table
# each: name -> function (d2d, f) -> (median PL dB, sigma dB), valid range m (lo, hi)
def scenarios(f):
    def with_o2(fn, kind=None):
        def g(d, ff):
            pl, s = fn(d, ff)
            return pl + o2_db(d, ff), s
        return g

    def o2i(kind):
        def g(d, ff):
            pl, s = uma_nlos(d, ff)
            ol, so = o2i_loss(ff, kind)
            return pl + ol, math.hypot(s, so)
        return g

    def fs(d, ff):
        return fspl(max(d, 1.0), ff) + o2_db(d, ff), 0.0

    def indoor(floors):
        def g(d, ff):
            return p1238(d, ff, floors)
        return g

    return {
        "IN": (indoor(0), (1, 100)),
        "IN-1F": (indoor(1), (1, 100)),
        "FS": (fs, (1, 1e9)),
        "UMa-LOS": (with_o2(uma_los), (10, 5000)),
        "UMa-NLOS": (with_o2(uma_nlos), (10, 5000)),
        "UMa-NLOS+O2I-low": (o2i("low"), (10, 5000)),
        "UMa-NLOS+O2I-high": (o2i("high"), (10, 5000)),
        "UMi-NLOS": (with_o2(umi_nlos), (10, 5000)),
        "RMa-LOS": (with_o2(rma_los), (10, 10000)),
        "RMa-NLOS": (with_o2(rma_nlos), (10, 5000)),
    }


def selftest():
    """Known values: FSPL 2.4 GHz at 1 km, 38.901 UMa NLOS at 3.5 GHz, Hata and UMa near 0.7 GHz."""
    out = {}
    out["fspl_2.44GHz_1km_dB"] = round(fspl(1000, 2.44), 2)           # 100.2 (textbook 100.2)
    out["uma_nlos_3.5GHz_1km_dB"] = round(uma_nlos(1000, 3.5)[0], 1)  # about 141
    out["uma_los_3.5GHz_1km_dB"] = round(uma_los(1000, 3.5)[0], 1)    # about 117
    out["hata_0.73GHz_1km_dB"] = round(hata_urban(1000, 730)[0], 1)
    out["uma_nlos_0.73GHz_1km_dB"] = round(uma_nlos(1000, 0.73)[0], 1)
    out["rma_nlos_0.73GHz_5km_dB"] = round(rma_nlos(5000, 0.73)[0], 1)
    out["o2i_low_3.5GHz_dB"] = round(o2i_loss(3.5, "low")[0], 1)
    out["o2i_high_3.5GHz_dB"] = round(o2i_loss(3.5, "high")[0], 1)
    out["p1238_5.2GHz_30m_dB"] = round(p1238(30, 5.2)[0], 1)
    out["o2_60GHz_1km_dB"] = o2_db(1000, 62.0)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(), indent=1))
