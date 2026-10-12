#!/usr/bin/env python3
"""speaker.py - the 9.0 x 3.2 x 2.2 mm speaker of the B ring (MON-6).

1. Fit: a 9.0 x 3.2 box as a chord in the annulus r = 12..16 mm.
2. Lumped model (acoustic impedance analogy, voltage drive):
     source p = e Bl / (Sd Ze), series Bl^2/(Sd^2 Ze), driver Zm/Sd^2,
     back volume 1/(jw Cab), then the front: cavity Cf in shunt, and the
     rim slot, the IP68 membrane and the radiation load in series.
   SPL in half space at 100 mm. Excursion and power set the voltage.
3. Back volume sweep, with and without a zeolite fill.

The driver figures are [HYPOTHESIS]: scaled from published 1511-class
micro-speakers to a 8.0 x 2.4 mm racetrack diaphragm.

Run:  python3 speaker.py   -> out/speaker.json
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

rho, c = P.RHO_AIR, P.C_AIR
mu_air = 1.81e-5

DRV = dict(Sd=13.5e-6, Mms=8.0e-6, fs=900.0, Qms=2.0, Re=8.0, Le=20e-6, Bl=0.45,
           xmax=0.20e-3, P_rated=0.7)          # [HYPOTHESIS]
DRV["Cms"] = 1 / ((2 * math.pi * DRV["fs"]) ** 2 * DRV["Mms"])
DRV["Rms"] = 2 * math.pi * DRV["fs"] * DRV["Mms"] / DRV["Qms"]

FRONT = dict(Vf=9.0 * 3.2 * 0.30 * 1e-9,       # 0.30 mm front cavity
             slot_w=6.0e-3, slot_h=0.45e-3, slot_L=0.80e-3,
             mem_R=1.5e7, mem_M=600.0)        # ePTFE IP68 membrane, Pa s/m3 and kg/m4 [HYPOTHESIS]


def fit():
    # inner edge of the box at radial distance a, outer corners must stay
    # inside r = 15.8 (0.2 mm wall); inner mid-point may pass under the window ledge
    a_max = math.sqrt(15.8**2 - (P.SPEAKER["L"] / 2) ** 2) - P.SPEAKER["W"]
    return dict(inner_edge_r=round(a_max, 3), under_window_mm=round(max(12.0 - a_max, 0), 3),
                arc_deg=round(math.degrees(2 * math.asin(P.SPEAKER["L"] / 2 / 15.8)), 1))


def response(Vb, f, e=1.0, zeolite=1.0):
    w = 2 * math.pi * f
    Ze = DRV["Re"] + 1j * w * DRV["Le"]
    Sd = DRV["Sd"]
    ps = e * DRV["Bl"] / (Sd * Ze)
    Zeb = DRV["Bl"] ** 2 / (Sd**2 * Ze)
    Zm = (DRV["Rms"] + 1j * w * DRV["Mms"] + 1 / (1j * w * DRV["Cms"])) / Sd**2
    Cab = Vb * zeolite / (rho * c**2)
    Zb = 1 / (1j * w * Cab)
    Cf = FRONT["Vf"] / (rho * c**2)
    S = FRONT["slot_w"] * FRONT["slot_h"]
    a_eq = math.sqrt(S / math.pi)
    Lp = FRONT["slot_L"] + 1.2 * a_eq                     # end corrections
    Mp = rho * Lp / S
    Rp = 12 * mu_air * FRONT["slot_L"] / (FRONT["slot_w"] * FRONT["slot_h"] ** 3)
    Rr = rho * w**2 / (2 * math.pi * c)
    Zbr = Rp + 1j * w * Mp + FRONT["mem_R"] + 1j * w * FRONT["mem_M"] + Rr
    Zcf = 1 / (1j * w * Cf)
    Zf = Zcf * Zbr / (Zcf + Zbr)
    Ud = ps / (Zeb + Zm + Zb + Zf)
    Up = Ud * Zcf / (Zcf + Zbr)
    p = rho * w * abs(Up) / (2 * math.pi * P.SPL_TARGET_R)
    x = abs(Ud) / (w * Sd)
    return 20 * math.log10(p / 20e-6), x


def spl_at_limits(Vb, f, zeolite=1.0):
    e_pow = math.sqrt(DRV["P_rated"] * DRV["Re"])
    spl1, x1 = response(Vb, f, 1.0, zeolite)
    e_x = DRV["xmax"] / x1
    e = min(e_pow, e_x)
    return spl1 + 20 * math.log10(e), e, "xmax" if e_x < e_pow else "power"


def main():
    res = {"driver": {k: v for k, v in DRV.items()}, "fit": fit()}
    print("SPEAKER 9.0 x 3.2 x 2.2 (MON-6: 78 dB SPL at 100 mm)")
    print(" fit:", res["fit"])
    Cas = DRV["Cms"] * DRV["Sd"] ** 2
    print(f" driver: Sd {DRV['Sd']*1e6:.1f} mm2, Mms {DRV['Mms']*1e6:.1f} mg, fs {DRV['fs']:.0f} Hz, "
          f"Vas {Cas*rho*c**2*1e9:.0f} mm3, Bl {DRV['Bl']}, xmax {DRV['xmax']*1e3:.2f} mm")
    # front resonance
    S = FRONT["slot_w"] * FRONT["slot_h"]
    Lp = FRONT["slot_L"] + 1.2 * math.sqrt(S / math.pi)
    fH = c / (2 * math.pi) * math.sqrt(S / (FRONT["Vf"] * Lp))
    res["front_helmholtz_Hz"] = fH
    print(f" front Helmholtz (slot only) {fH/1e3:.1f} kHz")
    f_band = np.geomspace(800, 4000, 25)
    sweep = []
    print(" back volume sweep, rated power or xmax, mean SPL 0.8..4 kHz at 100 mm:")
    for Vb_mm3 in (60, 100, 150, 200, 300):
        for z in (1.0, 1.8):
            Vb = Vb_mm3 * 1e-9
            vals = [spl_at_limits(Vb, f, z) for f in f_band]
            spl = np.array([v[0] for v in vals])
            p_mean = np.sqrt(np.mean((10 ** (spl / 20)) ** 2))
            spl_mean = 20 * math.log10(p_mean)
            s1k, e1k, lim1k = spl_at_limits(Vb, 1000.0, z)
            Cab = Vb * z / (rho * c**2)
            fc = DRV["fs"] * math.sqrt(1 + Cas / Cab)
            sweep.append(dict(Vb_mm3=Vb_mm3, zeolite=z, fc=round(fc), spl_1k=round(s1k, 1),
                              lim_1k=lim1k, spl_mean=round(spl_mean, 1)))
            print(f"   Vb {Vb_mm3:3d} mm3 x{z:.1f}: fc {fc:5.0f} Hz  SPL@1k {s1k:5.1f} dB ({lim1k})"
                  f"  mean {spl_mean:5.1f} dB")
    res["sweep"] = sweep
    # the design point
    Vb_design, z_design = 100, 1.8
    d = next(s for s in sweep if s["Vb_mm3"] == Vb_design and s["zeolite"] == z_design)
    res["design"] = d
    # MON-6 is judged at 1 kHz, the excursion-limited worst point of the band
    ok = d["spl_1k"] >= P.SPL_TARGET_DB and d["spl_mean"] >= P.SPL_TARGET_DB
    sector = Vb_design / (math.pi * (15.8**2 - 12.2**2) * 3.6 / 360 * 0.7)
    res["back_volume_sector_deg"] = round(sector, 1)
    print(f" back volume {Vb_design} mm3 needs about {sector:.0f} deg of annulus at 70 % fill")
    print(f" design point: {Vb_design} mm3 with zeolite x{z_design}: 1 kHz {d['spl_1k']} dB, mean {d['spl_mean']} dB, "
          f"target {P.SPL_TARGET_DB} dB -> {'PASS' if ok else 'FAIL'}")
    # spectrum at the design point for the record
    spec = []
    for f in np.geomspace(200, 12000, 40):
        s_, e_, lim = spl_at_limits(Vb_design * 1e-9, f, z_design)
        spec.append([round(float(f)), round(s_, 1), lim])
    res["spectrum"] = spec
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "speaker.json"), "w") as fo:
        json.dump(res, fo, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
