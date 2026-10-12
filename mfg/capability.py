#!/usr/bin/env python3
"""capability.py - the process-capability check of the critical dimensions.

Budlum Leaf L.6.0, Manufacturing and Test team, mfg/.
Gates: MON-23 (bar and module), DSP-19 (seam gap), MEC-40 (seat repeat),
MEC-37 and the soft edges of the team brief, section 4.

The CTQs
  1. the B bar, 1.00 +/- 0.05 mm: a five-layer stack, Monte Carlo and RSS
  2. the B module, 4.00 +/- 0.05 mm: a free stack against a press-to-height bond
  3. the seam: the tile pitch error sets the pixel gap (USL 50.0 um),
     the glass kerf must stay inside 0..10 um; the script finds the pitch
     target and the glass kerf that give the best device yield
  4. the laser chipping: a Weibull defect model per tile perimeter
  5. the PC cap kerf: no cap contact at +50 C
  6. the seat repeat: a Hertz and friction model of Si3N4 in WC vees
  7. the soft-edge radii: the tool replication model per edge

Every process sigma is [HYPOTHESIS] until the DVT data replace it.
Run:  python3 capability.py
"""
import math

import numpy as np
from scipy.stats import norm

import common as C

RNG = np.random.default_rng(21)
N_MC = 400_000
CPK_MIN = 1.33        # DVT exit, every CTQ                  [DECISION] mfg
CPK_CRIT = 1.67       # PVT exit, MON-23 and DSP-19 CTQs      [DECISION] mfg


def cpk(mu, sd, lsl=None, usl=None):
    vals = []
    if usl is not None:
        vals.append((usl - mu) / (3 * sd))
    if lsl is not None:
        vals.append((mu - lsl) / (3 * sd))
    return min(vals)


def ppm_out(mu, sd, lsl=None, usl=None):
    p = 0.0
    if usl is not None:
        p += norm.sf((usl - mu) / sd)
    if lsl is not None:
        p += norm.cdf((lsl - mu) / sd)
    return p * 1e6


# ------------------------------------------------------------------ 1. the bar
# layer, nominal mm, tolerance mm (3 sigma), mean bias mm, process  [HYPOTHESIS]
BAR_STACK = [
    ("top skin, LCP-GF40 over-mould", 0.20, 0.012, +0.003, "2nd shot, 0.20 mm cavity, steel +/-0.005"),
    ("antenna, LDS Cu/Ni/Au", 0.05, 0.006, 0.000, "plated 12 um in a 0.05 mm relief"),
    ("core, LCP-GF40 LDS grade", 0.40, 0.012, +0.002, "1st shot"),
    ("mmWave flex, 2-layer LCP", 0.10, 0.008, 0.000, "rolled LCP film, +/-8 um"),
    ("contact layer with 12 leaves", 0.25, 0.012, 0.000, "insert-moulded carrier"),
    ("two LCP fusion bond lines", 0.00, 0.006, -0.004, "fusion consumes about 2 um per line"),
]

# the module stack along the ring axis                           [HYPOTHESIS]
MOD_STACK_FREE = [
    ("sliding pad, PTFE-filled, laminated", 0.12, 0.010, 0.0),
    ("ring cup, LCP-GF40, moulded height", 3.40, 0.020, +0.004),
    ("rear PSA bond line, die-cut", 0.08, 0.015, 0.0),
    ("rear round AMOLED with cover", 0.40, 0.010, 0.0),
]
# press-to-height: a liquid OCA with hard stops fills the bond line,
# so the total is the fixture height plus the press and cure shrink
MOD_PTH = {"fixture_3s": 0.006, "cure_shrink_3s": 0.006, "pad_3s": 0.010, "bias": 0.001}


def stack_mc(stack, n=N_MC):
    tot = np.zeros(n)
    for row in stack:
        nom, tol, bias = row[1], row[2], row[3]
        tot += RNG.normal(nom + bias, tol / 3, n)
    return tot


def stack_report(name, stack, nom, tol):
    tot = stack_mc(stack)
    wc = sum(r[2] for r in stack)
    rss = math.sqrt(sum((r[2] / 3) ** 2 for r in stack))
    mu, sd = tot.mean(), tot.std()
    return {
        "ctq": name, "nominal": nom, "tol": tol,
        "worst_case_tol": wc, "worst_case_ok": wc <= tol,
        "rss_sigma": rss, "mc_mean": mu, "mc_sigma": sd,
        "cpk": cpk(mu, sd, nom - tol, nom + tol),
        "ppm": ppm_out(mu, sd, nom - tol, nom + tol),
        # gauge: P/T = 6 sigma_gauge / (USL - LSL) <= 0.10
        "gauge_sigma_max_um": 0.10 * 2 * tol / 6 * 1000,
    }


def module_pth():
    s = math.sqrt(sum(v ** 2 for k, v in MOD_PTH.items() if k != "bias")) / 3
    mu = C.MOD_T + MOD_PTH["bias"]
    return {"ctq": "module 4.00, press-to-height", "nominal": C.MOD_T, "tol": C.MOD_TOL,
            "mc_mean": mu, "mc_sigma": s,
            "cpk": cpk(mu, s, C.MOD_T - C.MOD_TOL, C.MOD_T + C.MOD_TOL),
            "ppm": ppm_out(mu, s, C.MOD_T - C.MOD_TOL, C.MOD_T + C.MOD_TOL)}


# ------------------------------------------------------------------ 3. the seam
# pixel gap at a seam = 50.0 um + pitch error e (display team, seam_lattice).
# The rest pitch of the lattice is L = a (cos t + sin |t|), so a residual tile
# angle t adds a * |t| = 10 um per mrad. The pitch error of one pair is
#     e = e_datum + a |t_res|,   e_datum ~ N(mu, sigma_datum)
# glass kerf = k0 + e - dL - dR, with dL and dR the cut-to-pattern errors.
SIG_DATUM = 0.50      # um, rest datum: stop width and lattice centring  [HYPOTHESIS]
SIG_CUT = 0.50        # um, laser cut to pixel pattern, vision-aligned   [HYPOTHESIS]
SIG_VEE = 0.35        # um, quadrant seam after the vee active bond      [HYPOTHESIS]
SIG_THETA = 0.02      # mrad, residual rest angle, half-normal, with a stop [HYPOTHESIS]
MU_E_MIN = -3.0       # um, the deepest pitch bias the seam can take unseen [HYPOTHESIS]


def _p_over(mu, s_d, s_t, limit=0.0):
    """P(e_datum + a|t| > limit), e_datum normal, t half-normal (mrad)."""
    if s_t <= 0:
        return norm.sf((limit - mu) / s_d)
    a = C.TILE  # um per mrad: 10 mm x 1e-3 = 10 um
    ts = np.linspace(0, 8 * s_t, 801)
    f = 2 * norm.pdf(ts / s_t) / s_t
    g = norm.sf((limit - mu - a * ts) / s_d)
    return float(np.trapezoid(f * g, ts))


def _p_under(mu, s_d, s_t, limit=0.0):
    """P(e_datum + a|t| < limit)."""
    return 1.0 - _p_over(mu, s_d, s_t, limit)


def seam_yield(k0, mu_e, sig_place=SIG_DATUM, sig_cut=SIG_CUT, sig_vee=SIG_VEE,
               sig_theta=SIG_THETA, counts=None):
    """Device yield of the seam over every tile pair, and the CTQ indices."""
    counts = counts or C.lattice_counts()
    out = {}
    for tag, n, s_e in (("tile", counts["fixed_hinges"], sig_place),
                        ("quadrant", counts["split_couplers"], sig_vee)):
        p_gap = _p_over(mu_e, s_e, sig_theta)                 # gap > 50.0 um
        s_k = math.sqrt(s_e ** 2 + 2 * sig_cut ** 2)
        p_kerf = (_p_under(mu_e + k0, s_k, sig_theta, 0.0)
                  + _p_over(mu_e + k0, s_k, sig_theta, C.KERF_MAX_UM))
        m_t = C.TILE * sig_theta * math.sqrt(2 / math.pi)      # mean of a|t|
        mu_k = k0 + mu_e + m_t
        out[tag] = {
            "pairs": n, "sigma_e": s_e, "p_gap_pair": p_gap, "p_kerf_pair": p_kerf,
            "cpk_gap": norm.isf(max(p_gap, 1e-300)) / 3,
            "cpk_kerf": norm.isf(max(p_kerf, 1e-300)) / 3,
            "kerf_mean": mu_k, "kerf_sigma": s_k,
            "yield": (1 - p_gap) ** n * (1 - p_kerf) ** n,
        }
    out["device_yield"] = out["tile"]["yield"] * out["quadrant"]["yield"]
    return out


def margin_um(k0):
    """Chip-to-cut margin against the glass kerf (display team table)."""
    return C.EDGE_MARGIN_RULE_UM + (C.KERF_NOM_UM - k0) / 2


# ------------------------------------------------------------------ 4. chipping
# chips per mm of cut edge and the Weibull of the chip depth        [HYPOTHESIS]
CHIP_DENSITY = 2.0        # chips per mm
CHIP_SCALE = 2.0          # um, Weibull scale, fs filamentation + cleave
CHIP_SHAPE = 2.0
TILE_EDGE_MM = 4 * (TILE_LEN := 10.0) - 4 * 2 * 0.55 + 4 * 0.55 * math.sqrt(2)


def chip_fail(limit, scale=CHIP_SCALE, shape=CHIP_SHAPE, dens=CHIP_DENSITY, edge=TILE_EDGE_MM):
    n = dens * edge
    p1 = math.exp(-(limit / scale) ** shape)
    return 1 - (1 - p1) ** n


# ------------------------------------------------------------------ 5. cap kerf
# The PC cap grows 27 um per 40 K (67.5 ppm/K). The gates run from -10 to
# +50 C, a span of 60 K, so the cap kerf swings 40.5 um, not 27 um.
# The window: no cap contact at +50 C (kerf > 0), and the kerf stays under
# the 50 um that the black face hides at -10 C.                [DECISION] 21.2.4
SIG_CAP_SIZE = 1.5     # um, UV-ps laser cut of PC, 1 sigma per cap    [HYPOTHESIS]
SIG_CAP_CENTRE = 1.5   # um, cap-to-glass centring at the OCA bond      [HYPOTHESIS]
CAP_CTE_UM_K = C.CAP_GROW_UM_40K / 40.0
T_HOT, T_COLD, T_ASM = 50.0, -10.0, 23.0
CAP_VISIBLE_UM = 50.0


OCA_SHEAR_UM = 3.0     # um of cap interference the 0.05 mm OCA takes in shear [HYPOTHESIS]


def cap_kerf(mu_e, k_hot=C.CAP_KERF_HOT_UM, s_size=SIG_CAP_SIZE, s_c=SIG_CAP_CENTRE, touch_lim=0.0):
    s = math.sqrt(2 * (s_size / 2) ** 2 + 2 * s_c ** 2 + SIG_DATUM ** 2)
    swing = (T_HOT - T_COLD) * CAP_CTE_UM_K
    mu_hot = k_hot + mu_e
    mu_cold = mu_hot + swing
    n = C.lattice_counts()["tile_pairs"]
    p_touch = norm.cdf((touch_lim - mu_hot) / s)
    p_show = norm.sf((CAP_VISIBLE_UM - mu_cold) / s)
    return {"sigma": s, "swing_60K": swing, "kerf_hot_mean": mu_hot, "kerf_cold_mean": mu_cold,
            "kerf_assembly_23C": mu_hot + (T_HOT - T_ASM) * CAP_CTE_UM_K,
            "cpk_touch": (mu_hot - touch_lim) / (3 * s), "cpk_show": (CAP_VISIBLE_UM - mu_cold) / (3 * s),
            "p_touch_pair": p_touch, "p_show_pair": p_show,
            "device_yield": (1 - p_touch) ** n * (1 - p_show) ** n}


def cap_kerf_best(mu_e, touch_lim=0.0):
    """The hot kerf that centres the window, and the sigma it needs."""
    swing = (T_HOT - T_COLD) * CAP_CTE_UM_K
    window = CAP_VISIBLE_UM - swing - touch_lim
    k_hot = touch_lim + window / 2 - mu_e
    best = cap_kerf(mu_e, k_hot, touch_lim=touch_lim)
    s_need = None
    for sc in np.arange(2.0, 0.09, -0.02):
        if cap_kerf(mu_e, k_hot, s_size=sc, s_c=sc, touch_lim=touch_lim)["device_yield"] >= 0.995:
            s_need = float(sc)
            break
    return {"window_um": window, "k_hot_um": k_hot, "at_best": best,
            "sigma_size_and_centre_for_995": s_need}


# ------------------------------------------------------------------ 6. the seat
def seat_repeat(F_n=1.0, mu=0.10, ball_d=0.60e-3, floor_um=0.05, film_um=0.0):
    """Non-repeat of the quadrant seat, um, 1 sigma.

    Hertz approach of a Si3N4 ball in a WC vee under the magnet preload, then a
    friction hysteresis of mu times the approach per contact. The six contacts
    of a three-ball seat average. A floor covers micro-slip and the surface
    finish. A film or a dust layer adds its own spread.
    [GENERAL] Slocum, Precision Engineering 10 (1988) 85-91, and 14 (1992) 67-76.
    """
    E1, v1 = 310e9, 0.27      # Si3N4
    E2, v2 = 620e9, 0.22      # WC
    Es = 1 / ((1 - v1 ** 2) / E1 + (1 - v2 ** 2) / E2)
    R = ball_d / 2
    delta = (9 * F_n ** 2 / (16 * R * Es ** 2)) ** (1 / 3)
    hyst = mu * delta * 1e6                     # um, full band per contact
    sig_h = (hyst / 4) / math.sqrt(6 / 2)       # band = +/-2 sigma; 6 contacts, 2 per axis
    sig = math.sqrt(sig_h ** 2 + floor_um ** 2 + film_um ** 2)
    return {"preload_N_per_ball": F_n, "hertz_approach_um": delta * 1e6,
            "hysteresis_um": hyst, "sigma_um": sig}


def seat_capability(sig):
    usl = C.SEAT_REPEAT_UM
    p1 = 2 * norm.sf(usl / sig)
    p_all = 1 - (1 - p1) ** C.SWAPS
    return {"sigma_um": sig, "cpk": usl / (3 * sig), "p_swap_over": p1,
            "p_any_over_in_10k": p_all,
            "sigma_needed_for_99pct": usl / norm.isf((1 - 0.99 ** (1 / C.SWAPS)) / 2)}


# ------------------------------------------------------------------ 7. radii
# nominal, proposed tolerance, process sigma, bias                 [HYPOTHESIS]
RADII = {
    "body perimeter, front and back face edges": (0.10, 0.025, +0.010),
    "tile PC-cap top edges and chamfer corners": (0.010, 0.003, 0.000),
    "B ring outer top and bottom edges": (0.05, 0.010, +0.008),
    "B ring inner bore edges": (0.05, 0.010, +0.008),
    "B bar long edges": (0.05, 0.010, +0.008),
    "B moulded 90 deg corner, outside edge": (0.05, 0.012, +0.008),
    "jack mouth": (0.05, 0.010, +0.006),
    "windows": (0.03, 0.007, 0.000),
}


def radii_report():
    rows = []
    for name, r, where, how in C.SOFT_EDGES:
        tol, sd, bias = RADII[name]
        mu = r + bias
        rows.append({"edge": name, "r": r, "tol": tol, "where": where, "process": how,
                     "mean": mu, "sigma": sd,
                     "cpk": cpk(mu, sd, r - tol, r + tol),
                     "ppm": ppm_out(mu, sd, r - tol, r + tol),
                     "flash_risk": "LCP" in how})
    return rows


# ------------------------------------------------------------------ run
def optimise_seam():
    """Pick the glass kerf and the pitch target.

    The key is the device yield, then the smallest Cpk of the seam CTQs.
    The pitch target stays at or above MU_E_MIN, so the seam never reads as a
    bright line.
    """
    best, grid = None, []
    for k0 in np.arange(5.0, 9.01, 0.5):
        m = margin_um(k0)
        y_chip = 1 - chip_fail(min(C.CHIPPING_MAX_UM, m))
        for mu_e in np.arange(MU_E_MIN, 0.01, 0.25):
            s = seam_yield(k0, mu_e)
            y = s["device_yield"] * y_chip ** 128
            cmin = min(s["tile"]["cpk_gap"], s["tile"]["cpk_kerf"],
                       s["quadrant"]["cpk_gap"], s["quadrant"]["cpk_kerf"])
            key = (round(y, 5), cmin)
            grid.append((float(k0), float(mu_e), y, cmin))
            if best is None or key > best[0]:
                best = (key, float(k0), float(mu_e), y, s, y_chip, cmin)
    return best[1:], grid


def run(verbose=True):
    res = {}
    bar = stack_report("bar 1.00", BAR_STACK, C.BAR_T, C.BAR_TOL)
    mod = stack_report("module 4.00, free stack", MOD_STACK_FREE, C.MOD_T, C.MOD_TOL)
    pth = module_pth()
    res["bar"], res["module_free"], res["module_pth"] = bar, mod, pth

    best, grid = optimise_seam()
    k0, mu_e, y, s, y_chip, cmin = best
    res["seam_opt"] = {"glass_kerf_nominal_um": float(k0), "pitch_target_um": float(mu_e),
                       "pitch_target_mm": C.TILE + mu_e / 1000,
                       "edge_margin_um": margin_um(k0),
                       "device_yield_seam_and_chip": y, "seam": s,
                       "tile_chip_yield": y_chip, "min_cpk": cmin}
    res["seam_display_nominal"] = seam_yield(C.KERF_NOM_UM, 0.0)
    # the sigma of placement that the seam needs for 99.5 % at the optimum
    need = None
    for sp in np.arange(1.2, 0.09, -0.02):
        if seam_yield(k0, mu_e, sig_place=sp)["tile"]["yield"] >= 0.995:
            need = sp
            break
    res["seam_sigma_place_for_995"] = need

    res["chipping"] = {
        "tile_edge_mm": TILE_EDGE_MM,
        "sweep": [{"scale_um": sc, "p_tile_over_10": chip_fail(10.0, scale=sc),
                   "device_yield_128": (1 - chip_fail(10.0, scale=sc)) ** 128}
                  for sc in (1.5, 2.0, 2.5, 3.0, 3.5, 4.0)],
    }
    res["cap_kerf_part21"] = cap_kerf(mu_e)
    res["cap_kerf_best"] = cap_kerf_best(mu_e)
    res["cap_kerf_oca"] = cap_kerf_best(mu_e, touch_lim=-OCA_SHEAR_UM)

    seat = seat_repeat(F_n=1.0, mu=0.10)
    res["seat_model"] = seat
    res["seat_cap"] = seat_capability(seat["sigma_um"])
    res["seat_cap_dirty"] = seat_capability(seat_repeat(film_um=0.15)["sigma_um"])
    res["seat_cap_particle"] = seat_capability(seat_repeat(film_um=0.30)["sigma_um"])
    res["radii"] = radii_report()

    if verbose:
        print("== 1. THE BAR 1.00 +/- 0.05 mm (MON-23) ==")
        for r in BAR_STACK:
            print(f"   {r[0]:34s} {r[1]:.3f} +/-{r[2]:.3f}  bias {r[3]:+.3f}  {r[4]}")
        print(f"   worst case +/-{bar['worst_case_tol']:.3f} mm -> {'inside' if bar['worst_case_ok'] else 'OUTSIDE'} +/-0.05")
        print(f"   Monte Carlo mean {bar['mc_mean']:.4f}, sigma {bar['mc_sigma']*1000:.2f} um, "
              f"Cpk {bar['cpk']:.2f}, {bar['ppm']:.1f} ppm out")
        print(f"   gauge sigma for P/T 10 %: {bar['gauge_sigma_max_um']:.2f} um or less")
        print()
        print("== 2. THE MODULE 4.00 +/- 0.05 mm (MON-23) ==")
        print(f"   free stack: worst case +/-{mod['worst_case_tol']:.3f}, sigma {mod['mc_sigma']*1000:.2f} um, "
              f"Cpk {mod['cpk']:.2f}, {mod['ppm']:.1f} ppm")
        print(f"   press-to-height: sigma {pth['mc_sigma']*1000:.2f} um, Cpk {pth['cpk']:.2f}, {pth['ppm']:.3f} ppm")
        print()
        print("== 3. THE SEAM (DSP-19): pixel gap <= 50.0 um, glass kerf 0..10 um ==")
        sd = res["seam_display_nominal"]
        print(f"   at the display nominal (kerf 6, pitch error 0): tile Cpk_gap {sd['tile']['cpk_gap']:.2f}, "
              f"device yield {sd['device_yield']*100:.3g} %")
        print(f"   optimum: glass kerf {k0:.1f} um, pitch target {mu_e:+.2f} um "
              f"({C.TILE + mu_e/1000:.5f} mm), margin {margin_um(k0):.1f} um")
        for tag in ("tile", "quadrant"):
            t = s[tag]
            print(f"     {tag:8s} pairs {t['pairs']:3d}  Cpk gap {t['cpk_gap']:.2f}  Cpk kerf {t['cpk_kerf']:.2f}  "
                  f"kerf {t['kerf_mean']:.2f} +/- {t['kerf_sigma']:.2f} um  yield {t['yield']*100:.3f} %")
        print(f"   device yield, seam and chipping: {y*100:.3f} %")
        print(f"   placement sigma for a 99.5 % tile-seam yield: {need:.2f} um")
        print()
        print("== 4. THE CHIPPING (Weibull, shape 2, 2 chips per mm) ==")
        for r in res["chipping"]["sweep"]:
            print(f"   scale {r['scale_um']:.1f} um: P(tile chip > 10 um) {r['p_tile_over_10']:.2e}, "
                  f"device {r['device_yield_128']*100:.3f} %")
        print()
        ck = res["cap_kerf_part21"]
        cb = res["cap_kerf_best"]
        print("== 5. THE PC CAP KERF ==")
        print(f"   the swing from -10 to +50 C is {ck['swing_60K']:.1f} um (Part 21 states 27 um over 40 K)")
        print(f"   Part 21 setting: kerf {ck['kerf_hot_mean']:.1f} um at +50 C, {ck['kerf_assembly_23C']:.1f} um at 23 C, "
              f"{ck['kerf_cold_mean']:.1f} um at -10 C, sigma {ck['sigma']:.2f} um")
        print(f"     Cpk no-touch {ck['cpk_touch']:.2f}, Cpk unseen {ck['cpk_show']:.2f}, device yield {ck['device_yield']*100:.3g} %")
        bb = cb["at_best"]
        print(f"   centred: window {cb['window_um']:.1f} um, hot kerf {cb['k_hot_um']:.2f} um (pitch target incl.), "
              f"Cpk {min(bb['cpk_touch'], bb['cpk_show']):.2f}, device yield {bb['device_yield']*100:.3g} %")
        print(f"   size and centring sigma for a 99.5 % device: {cb['sigma_size_and_centre_for_995']:.2f} um each")
        co = res["cap_kerf_oca"]
        bo = co["at_best"]
        print(f"   with {OCA_SHEAR_UM:.0f} um of OCA shear allowed at +50 C: window {co['window_um']:.1f} um, "
              f"hot kerf {co['k_hot_um']:.2f} um, Cpk {min(bo['cpk_touch'], bo['cpk_show']):.2f}, "
              f"sigma for 99.5 %: {co['sigma_size_and_centre_for_995']:.2f} um each")
        print()
        print("== 6. THE SEAT REPEAT (MEC-40) ==")
        print(f"   Hertz approach {seat['hertz_approach_um']:.2f} um at 1 N per ball, hysteresis {seat['hysteresis_um']:.3f} um")
        for tag, key in (("clean", "seat_cap"), ("0.15 um film", "seat_cap_dirty"), ("0.30 um particle", "seat_cap_particle")):
            sc = res[key]
            print(f"   {tag:16s} sigma {sc['sigma_um']:.3f} um, Cpk {sc['cpk']:.2f}, "
                  f"P(any of 10 000 swaps > 1 um) {sc['p_any_over_in_10k']:.2e}")
        print(f"   sigma needed for 99 % of seats to pass 10 000 swaps: {res['seat_cap']['sigma_needed_for_99pct']:.3f} um")
        print()
        print("== 7. THE SOFT-EDGE RADII (team brief, section 4) ==")
        for r in res["radii"]:
            print(f"   {r['edge']:42s} r {r['r']:.2f} +/-{r['tol']:.3f}  mean {r['mean']:.3f} sigma {r['sigma']:.3f}"
                  f"  Cpk {r['cpk']:.2f}{'' if r['cpk'] >= CPK_MIN else ' ACTION'}  {r['process']}")
    return res


if __name__ == "__main__":
    r = run()
    C.save_json("capability.json", r)
