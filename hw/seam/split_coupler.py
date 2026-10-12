#!/usr/bin/env python3
"""split_coupler.py - the 24 split hinge couplers of the + crossing.

Deliverable 2 of the seam team. A split coupler is the standard edge-on
polyimide hinge of the lattice. Its far end is bonded to a WC-Ni key. The key
sits in a socket in the corner of the neighbour tile. A Ti-6Al-4V gate pin drops
through a hole in the key flange and locks it in every direction. A 25 um NiTi
wire lifts the gate pin. So the lattice stays one mechanism in every stretch
state, and the quadrant separates only when U4 opens its 12 gates.

The script proves: the load path against the ribbon break load, the gate in
double shear, the shock rating of the gate, the SMA stroke, force, heating
time, hold power and cooling, the insertion force, the seat misfit force, the
contact resistance and the data lanes that cross a seam.
Gates: MEC-40 (swap under 3 s), MEC-42 (the hinge), DSP-19 (seam data path).
"""
import json
import math
import os
import seam_params as P


def ribbon():
    r = P.RIBBON
    A = r["t_um"] * 1e-6 * r["h_mm"] * 1e-3
    k_ax = r["E"] * A / (r["L_mm"] * 1e-3)
    return dict(area_mm2=A * 1e6, break_N=r["sigma_u"] * A, k_axial_N_per_um=k_ax * 1e-6)


def gate_pin():
    d = P.GATE_PIN_D_mm
    area = math.pi / 4 * d * d                        # mm^2
    double_shear = 2 * area * P.GATE_PIN_TAU * 1e-6   # N
    bearing_Ti = d * P.KEY["flange_mm"] * 1.1e9 * 1e-6
    m = 4430 * area * 1e-6 * 0.40e-3                  # kg, 0.40 mm pin
    g_hold = P.GATE_SPRING_N / (m * 9.81)
    return dict(double_shear_N=double_shear, bearing_N=bearing_Ti, mass_ug=m * 1e9,
                spring_g_rating=g_hold)


def sma(T_amb=P.T_MIN_C):
    s = P.SMA
    R = s["rho_e"] * s["L_mm"] * 1e-3
    vol = math.pi / 4 * (s["d_um"] * 1e-6) ** 2 * s["L_mm"] * 1e-3
    m = s["dens"] * vol
    E_heat = m * (s["cp"] * (s["Af_C"] + 10 - T_amb) + s["latent"])
    P_pulse = s["I_pulse"] ** 2 * R
    t_heat = 1.5 * E_heat / P_pulse          # 1.5: conduction into the pin and the bed
    P_hold = s["I_hold"] ** 2 * R
    stroke = s["strain"] * s["L_mm"]
    return dict(R_ohm=R, mass_ug=m * 1e9, E_heat_uJ=E_heat * 1e6, t_heat_ms=t_heat * 1e3,
                P_pulse_mW=P_pulse * 1e3, P_hold_mW=P_hold * 1e3, stroke_mm=stroke,
                stroke_margin=stroke / P.GATE_LIFT_mm, force_margin=s["force_N"] / (P.GATE_SPRING_N + 0.01),
                cool_ms=s["cool_s"] * 1e3, V_pulse=s["I_pulse"] * R)


def insertion_force(alpha_deg=30.0, mu=0.2):
    a = math.radians(alpha_deg)
    per = P.GATE_SPRING_N * (math.tan(a) + mu) / (1 - mu * math.tan(a))
    return per


def holm_resistance(F=0.03, H=0.7e9, rho=2.2e-8, film_mohm=10.0):
    a = math.sqrt(F / (math.pi * H))
    return rho / (2 * a) * 1e3 + film_mohm


def main():
    res = {}
    rb = ribbon()
    res["ribbon"] = rb
    design = 2 * rb["break_N"]
    gp = gate_pin()
    res["gate_pin"] = gp
    res["design_load_N"] = design
    print(f"ribbon break {rb['break_N']:.2f} N -> coupler design load {design:.2f} N (2 x ribbon)")
    print(f"gate pin D{P.GATE_PIN_D_mm} Ti-6Al-4V double shear {gp['double_shear_N']:.1f} N "
          f"(SF {gp['double_shear_N']/design:.2f}), bearing {gp['bearing_N']:.1f} N; "
          f"spring holds the pin shut to {gp['spring_g_rating']:.0f} g")
    # key flange in z: WC-Ni flange 0.10 mm under a 0.08 mm Ti lip, shear area = perimeter x thickness
    lip_shear = 2 * (P.KEY["w_mm"] + P.KEY["l_mm"]) * 0.08 * 550e6 * 1e-6 * 0.5
    res["z_capture_N"] = lip_shear
    print(f"key z capture (Ti lip, half the perimeter engaged): {lip_shear:.1f} N")

    for T in (P.T_MIN_C, P.T_REF_C, P.T_MAX_C):
        s = sma(T)
        res[f"sma_{T:+.0f}C"] = s
    s = res[f"sma_{P.T_MIN_C:+.0f}C"]
    print(f"SMA 25 um x {P.SMA['L_mm']} mm: R {s['R_ohm']:.2f} ohm, stroke {s['stroke_mm']*1e3:.0f} um "
          f"(x{s['stroke_margin']:.2f} of the {P.GATE_LIFT_mm*1e3:.0f} um lift), force x{s['force_margin']:.2f}")
    print(f"  heat to Af+10 from -10 C: {s['E_heat_uJ']:.2f} uJ, {s['t_heat_ms']:.1f} ms at "
          f"{P.SMA['I_pulse']*1e3:.0f} mA ({s['V_pulse']:.2f} V), hold {s['P_hold_mW']:.1f} mW, cool {s['cool_ms']:.0f} ms")
    n_gates = 12
    hold_s = 2.0
    E_q = n_gates * (s["P_pulse_mW"] * 1e-3 * s["t_heat_ms"] * 1e-3 + s["P_hold_mW"] * 1e-3 * hold_s)
    res["release_energy_J"] = E_q
    res["release_peak_W"] = n_gates * s["P_pulse_mW"] * 1e-3
    print(f"one quadrant release: 12 gates, peak {res['release_peak_W']:.2f} W, energy {E_q*1e3:.0f} mJ for a {hold_s} s window")

    fi = insertion_force()
    res["insertion_per_gate_N"] = fi
    res["insertion_quadrant_N"] = 12 * fi
    print(f"insertion: ramp 30 deg lifts each gate with {fi*1e3:.0f} mN, the quadrant with {12*fi:.2f} N")

    # misfit of the ribbon at rest, thermal plus assembly
    misfit_asm = 0.5e-6
    dalpha = P.MAT["PI"][2] - 4.0e-6
    misfit_T = dalpha * P.RIBBON["L_mm"] * 1e-3 * max(P.T_MAX_C - P.T_REF_C, P.T_REF_C - P.T_MIN_C)
    k = rb["k_axial_N_per_um"] * 1e6
    F_mis = k * (misfit_asm + misfit_T)
    res["misfit"] = dict(assembly_um=misfit_asm * 1e6, thermal_um=misfit_T * 1e6, force_N=F_mis)
    print(f"ribbon misfit at rest: {misfit_asm*1e6:.1f} um assembly + {misfit_T*1e6:.2f} um thermal "
          f"-> {F_mis*1e3:.0f} mN (budgeted 50 mN in the magnet sizing)")

    # shock: the share of one coupler when a quadrant decelerates in plane
    m_q = 32 * 0.424e-3
    a_ribbon = rb["break_N"] * 12 / m_q / 9.81
    a_coupler = design * 12 / m_q / 9.81
    res["shock"] = dict(quadrant_g=m_q * 1e3, ribbon_limit_g=a_ribbon, coupler_limit_g=a_coupler)
    print(f"in-plane shock of a {m_q*1e3:.1f} g quadrant shared by 12 couplers: ribbon limit {a_ribbon:.0f} g, "
          f"coupler limit {a_coupler:.0f} g")

    # electrical: 4 gold flank contacts per key (VBUS, GND, D+, D-)
    Rc = holm_resistance()
    res["contact_mohm"] = Rc
    bits = (P.TILES_X // 2 * 200) * (P.TILES_Y // 2 * 200) * 240 * 24
    lanes_long = 8
    res["data"] = dict(quadrant_Gbps=bits / 1e9, lanes_long_edge=lanes_long,
                       per_lane_Gbps=bits / 1e9 / lanes_long * 1.25)
    print(f"key contacts: about {Rc:.0f} mOhm each; one quadrant needs {bits/1e9:.2f} Gb/s, "
          f"{bits/1e9/lanes_long*1.25:.2f} Gb/s per lane on 8 long-edge couplers with 8b10b")
    res["pass"] = dict(gate_vs_design=gp["double_shear_N"] >= design,
                       sma_stroke=s["stroke_margin"] >= 1.0, sma_force=s["force_margin"] >= 1.5,
                       heat_under_50ms=s["t_heat_ms"] < 50, misfit_in_budget=F_mis < 0.05)
    print("checks:", res["pass"])
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/split_coupler.json", "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    main()
