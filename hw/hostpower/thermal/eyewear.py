#!/usr/bin/env python3
"""eyewear.py - a bounded study of a host-fed Leaf Frame worn on the face.

Team THERMAL of hw/hostpower. The Frame (FINAL/07 Section 7.5) is a worn Leaf:
30 to 40 g, a 2 to 3 Wh cell in the temple, 0.4 to 1.2 W with the display on.
The face-side surface limit is 36.2 C (ENR-16, FINAL/04 Section 4.6 and 4.7, [DECISION]).

The model is two nodes, in steady state. Every number is [HYPOTHESIS].

  body   one node at T_b. It holds the lens, the rim and the two temples.
         It sheds heat to air (convection and radiation, area A_AIR)
         and to the skin through the contact patches (area A_CONTACT).
  skin   34 C at the temple and the nose, held by the body (blood flow). It is a fixed sink.

The contact patch is a cover (silicone or PC, 1 mm) in series with the pressure contact of
a light-pressure fit against skin and hair. The contact surface is the face-side surface.
The temple electronics sit in a hot spot: a fraction F_LOCAL of the heat flows through a
spreading resistance R_SP above the body node. Both the outer surface over the hot spot and
the contact surface under it must stay at or under 36.2 C.

Run: python3 eyewear.py   (run_all.py calls it)
"""
import json
import os
import sys

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

T_LIM = 36.2
A_AIR = 100e-4            # m2, lens both faces 63 cm2 plus temples 39 cm2 [HYPOTHESIS]
A_CONTACT = 8e-4          # m2, two temple patches 6 cm2 plus two nose pads 2 cm2
H_CONTACT = 100.0         # W/m2K, a light-pressure fit on skin and hair
COVER_T, COVER_K = 1.0e-3, 0.20      # m, W/mK
F_LOCAL = 0.60            # share of the heat in the temple electronics (SoC, radio, regulator)
EPS = 0.90
SIGMA = 5.670374e-8


def h_rad(t_amb, t_surf=33.0):
    tm = (t_amb + t_surf) / 2 + 273.15
    return 4 * EPS * SIGMA * tm ** 3


def model(t_amb, wind, t_skin=34.0, r_sp=3.0, a_contact=A_CONTACT, h_contact=H_CONTACT):
    """Return G_air, G_ser, G_c: the three conductances of the two node model."""
    h_conv = 12.0 if wind else 5.5
    g_air = (h_conv + h_rad(t_amb)) * A_AIR
    g_cov = COVER_K * a_contact / COVER_T
    g_c = h_contact * a_contact
    g_ser = 1.0 / (1.0 / g_cov + 1.0 / g_c)
    return g_air, g_ser, g_c


def temps(P, t_amb, wind, t_skin=34.0, r_sp=3.0, **kw):
    g_air, g_ser, g_c = model(t_amb, wind, t_skin, r_sp, **kw)
    t_b = (P + g_air * t_amb + g_ser * t_skin) / (g_air + g_ser)
    t_hot = t_b + F_LOCAL * P * r_sp                 # the outer surface over the hot spot
    t_contact = t_skin + (g_ser / g_c) * (t_hot - t_skin)   # the face-side surface
    return dict(T_body=t_b, T_outer_hot=t_hot, T_contact=t_contact, T_peak=max(t_hot, t_contact))


def p_max(t_amb, wind, t_skin=34.0, r_sp=3.0, **kw):
    """Largest heat in the Frame that holds both surfaces at 36.2 C."""
    if temps(0.0, t_amb, wind, t_skin, r_sp, **kw)["T_peak"] > T_LIM:
        return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(50):
        m = 0.5 * (lo + hi)
        if temps(m, t_amb, wind, t_skin, r_sp, **kw)["T_peak"] <= T_LIM:
            lo = m
        else:
            hi = m
    return lo


def run():
    os.makedirs(OUT, exist_ok=True)
    res = dict(assumptions=dict(A_AIR_cm2=A_AIR * 1e4, A_CONTACT_cm2=A_CONTACT * 1e4,
                                h_contact=H_CONTACT, cover_mm=COVER_T * 1e3, cover_k=COVER_K,
                                F_LOCAL=F_LOCAL, T_skin_nominal=34.0, R_SP_nominal=3.0,
                                limit=T_LIM, tag="HYPOTHESIS"))
    g_air, g_ser, g_c = model(25.0, False)
    res["conductances_25C_still_W_per_K"] = dict(air=g_air, contact_series=g_ser, contact_surface_to_skin=g_c)
    lines = ["EYEWEAR STUDY, host-fed Leaf Frame, face-side limit %.1f C" % T_LIM,
             "two-node model, steady, all numbers [HYPOTHESIS]",
             "G_air %.3f W/K, G_contact(series) %.3f W/K at 25 C still air" % (g_air, g_ser), ""]
    # 1. the nominal table
    nominal = {}
    lines.append("1. heat limit P_heat,max in the Frame (W), skin 34 C, R_SP 3 K/W")
    lines.append("   %-8s %12s %12s" % ("T_amb", "still air", "light wind"))
    for ta in (20, 25, 30, 35):
        a, b = p_max(ta, False), p_max(ta, True)
        nominal[ta] = dict(still=a, wind=b)
        lines.append("   %-8s %12.2f %12.2f" % ("%d C" % ta, a, b))
    res["pmax_nominal"] = nominal
    # 2. host budget: heat limit minus the connector loss
    lines.append("")
    lines.append("2. host power budget: the load that fits is P_heat,max minus the interface loss")
    lines.append("   The worn host feeds through a temple connector or a cable. Loss 0.10 to 0.34 W.")
    host = {}
    for ta in (20, 25, 30, 35):
        row = {}
        for tag, wind in (("still", False), ("wind", True)):
            pm = nominal[ta][tag]
            row[tag] = dict(P_heat_max=pm, load_lo_loss=max(0.0, pm - 0.10),
                            load_hi_loss=max(0.0, pm - 0.34))
        host[ta] = row
        lines.append("   %2d C still: load %.2f W at 0.10 W loss, %.2f W at 0.34 W loss; wind: %.2f and %.2f W"
                     % (ta, row["still"]["load_lo_loss"], row["still"]["load_hi_loss"],
                        row["wind"]["load_lo_loss"], row["wind"]["load_hi_loss"]))
    res["host_budget"] = host
    # 3. the Frame loads of FINAL/07: 0.4 to 1.2 W, display on, nominal 0.8 W
    lines.append("")
    lines.append("3. the Frame loads (FINAL/07 Section 7.5: 0.4 W, 0.8 W, 1.2 W, display on), peak surface C")
    verdict = {}
    for ta in (20, 25, 30, 35):
        for tag, wind in (("still", False), ("wind", True)):
            for P_load in (0.4, 0.8, 1.2):
                for loss in (0.10, 0.34):
                    t = temps(P_load + loss, ta, wind)
                    verdict[f"{ta}C|{tag}|{P_load}W|loss{loss}"] = dict(T_peak=t["T_peak"],
                                                                         margin=T_LIM - t["T_peak"])
    res["frame_loads"] = verdict
    for ta in (20, 25, 30, 35):
        s = []
        for P_load in (0.4, 0.8, 1.2):
            t = temps(P_load + 0.34, ta, False)
            s.append("%.1f W: %.1f C (%+.1f K)" % (P_load, t["T_peak"], T_LIM - t["T_peak"]))
        lines.append("   %2d C still, loss 0.34 W: " % ta + "; ".join(s))
    # 4. sensitivity
    lines.append("")
    lines.append("4. sensitivity of P_heat,max at 25 C still air")
    sens = {}
    for name, kw in (("nominal", {}),
                     ("skin 33 C", dict(t_skin=33.0)), ("skin 35 C", dict(t_skin=35.0)),
                     ("R_SP 0 K/W (ideal spreader)", dict(r_sp=0.0)),
                     ("R_SP 6 K/W", dict(r_sp=6.0)),
                     ("contact area x2", dict(a_contact=2 * A_CONTACT)),
                     ("contact area x0.5", dict(a_contact=0.5 * A_CONTACT)),
                     ("loose fit, h_contact 30", dict(h_contact=30.0))):
        sens[name] = p_max(25.0, False, **kw)
        lines.append("   %-34s %.2f W" % (name, sens[name]))
    res["sensitivity_25C_still"] = sens
    # 5. the limit with no host: what does the skin sink give
    lines.append("")
    zero = {ta: temps(0.0, ta, False) for ta in (20, 25, 30, 35)}
    res["zero_power_T_peak"] = {ta: z["T_peak"] for ta, z in zero.items()}
    lines.append("5. idle surface with no power: " + ", ".join("%d C -> %.1f C" % (ta, z["T_peak"])
                                                              for ta, z in zero.items()))
    # which ambient does a 0.8 W Frame with 0.34 W loss stop to be always-on
    lo = None
    for ta in np.arange(10, 40.01, 0.25):
        if temps(0.8 + 0.34, ta, False)["T_peak"] > T_LIM:
            lo = float(ta)
            break
    res["ambient_limit_0p8W_0p34W_still"] = lo
    lines.append("6. a 0.8 W Frame with a 0.34 W connector loss holds 36.2 C in still air up to %s C ambient"
                 % ("%.2f" % (lo - 0.25) if lo else ">40"))
    with open(os.path.join(OUT, "eyewear.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    with open(os.path.join(OUT, "eyewear.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return res, lines


if __name__ == "__main__":
    r, l = run()
    print("\n".join(l))
