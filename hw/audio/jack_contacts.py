#!/usr/bin/env python3
"""jack_contacts.py - contact springs, retention, wear and the sealed pocket.

1. Spring fingers for T, R1, R2 (pre-loaded cantilevers in the inboard pocket)
   and the sleeve C-clip. A grid search picks t, b, L and preload inside the
   pocket limits.
2. Insertion and withdrawal force from the tip detent and the friction.
3. Contact resistance (Holm, gold on brass).
4. Wear over 5 000 cycles (Archard, sphere on cylinder, worn cap model) and
   the plating stack that survives it.
5. The gasketed contact pocket: FKM squeeze, contact stress against the
   IP68 head, clamp force and the heat stakes.

Run:  python3 jack_contacts.py   -> out/contacts.json
"""
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

# ------------------------------------------------------------------ materials
CUTI = dict(name="Cu-Ti C1990 HP", E=127e3, Sy=1000.0)   # [GENERAL] mill data class
MU = 0.20                                             # Au on Au/Ni, lubricated [GENERAL]
H_AU = 1.7e3      # MPa, hard gold AuCo 170 HV         [GENERAL]
H_PDNI = 4.5e3    # MPa, PdNi 80/20 450 HV             [GENERAL]
H_INLAY = 2.3e3   # MPa, AuAgCu hard clad inlay 230 HV  [GENERAL]
RHO = {"Au": 2.2e-8, "brass": 7.0e-8, "Ni": 7.0e-8}   # ohm m

# ------------------------------------------------------------------ 1 fingers
# each contact: stroke = radial travel from the free stop to the plug surface
R_PLUG = P.PLUG_D / 2
R_NECK = P.NECK_D / 2
POCKET = dict(L_max=5.0, t_set=(0.08, 0.10, 0.12, 0.15, 0.18))


def finger(t, b, L, preload_def, stroke, taper=1.5):
    """Tapered cantilever. taper: deflection gain of a linear width taper
    at the same root stress (1.5 for a triangle-like plan)."""
    k = CUTI["E"] * b * t**3 / (4 * L**3) * (1 / taper)
    d_tot = preload_def + stroke
    F_pre = k * preload_def
    F_max = k * d_tot
    sig = 6 * F_max * L / (b * t**2)
    return k, F_pre, F_max, sig


def design(name, stroke_work, stroke_max, F_min, F_cap, widths=(0.8, 1.0, 1.2, 1.4, 1.6)):
    """stroke_work: travel at the working point; stroke_max: worst travel.
    widths: total width; a tip pair is two 1.5 mm fingers side by side."""
    best = None
    for t, b, L, pre in itertools.product(POCKET["t_set"], widths,
                                          [2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                                          [0.01 * i for i in range(1, 61)]):
        k, Fp, Fm, sig = finger(t, b, L, pre, stroke_max)
        F_work = k * (pre + stroke_work)
        if F_work < F_min or Fm > F_cap or sig > 0.75 * CUTI["Sy"]:
            continue
        score = (sig / CUTI["Sy"]) + 0.02 * L          # low stress, short finger
        if best is None or score < best[0]:
            best = (score, dict(contact=name, t=t, b=b, L=L, preload_def=round(pre, 2),
                                k=round(k, 3), F_work=round(F_work, 2), F_max=round(Fm, 2),
                                sigma=round(sig), sigma_over_Sy=round(sig / CUTI["Sy"], 2)))
    return best[1] if best else dict(contact=name, result="no design in the pocket")


def main():
    res = {}
    print("JACK CONTACTS, RETENTION, WEAR AND SEAL (MON-22)")
    # the tip finger rests in the neck: working travel to the neck radius,
    # worst travel to the full shank radius plus the plug tolerance.
    clr = 0.05
    # free stop at r = R_NECK - clr: travel 0.05 in the neck, 0.53 on the shank
    T = design("T tip pair (detent)", stroke_work=clr,
               stroke_max=P.PLUG_D_TOL[1] / 2 - (R_NECK - clr), F_min=1.0, F_cap=3.0,
               widths=(2.4, 2.8, 3.2))
    R1 = design("R1 ring 1", stroke_work=0.20, stroke_max=0.25, F_min=0.6, F_cap=1.2)
    R2 = design("R2 ring 2 (x2 Kelvin)", stroke_work=0.20, stroke_max=0.25, F_min=0.6, F_cap=1.2)
    res["fingers"] = [T, R1, R2]
    print(f" 1 fingers, {CUTI['name']}, tapered, stress limit 0.75 Sy")
    for f in res["fingers"]:
        print("   ", f)
    # detect leaf: normally closed on the back of T; T lifts it by its full stroke
    res["detect"] = dict(type="NC leaf on the back of T, opens at 0.15 mm of T travel",
                         contact_force_N=0.3, travel_mm=round(T.get("preload_def", 0), 2))
    # sleeve C-clip: grips the sleeve over 240 deg in the captured zone
    clip = dict(material="Cu-Ti C1990, Au over Ni", t=0.10, wrap_deg=240, length=1.9,
                grip_N=2.0, note="also the structural liner in CR-AUD-1 when made in 17-4PH")
    res["clip"] = clip

    # ------------------------------------------------------------------ 2 forces
    alpha_in, alpha_out = math.radians(30), math.radians(60)  # tip ball and neck flanks
    N_T = T["F_max"]
    N_neck = T["F_work"]

    def ramp(N, a):
        return N * (math.tan(a) + MU) / (1 - MU * math.tan(a))
    F_ins = ramp(N_T, alpha_in) + MU * (R1["F_max"] + 2 * R2["F_max"] + clip["grip_N"] * 2)
    F_out = ramp(N_neck, alpha_out) + MU * (R1["F_work"] + 2 * R2["F_work"] + clip["grip_N"] * 2)
    res["insertion_N"] = round(F_ins, 2)
    res["withdrawal_N"] = round(F_out, 2)
    ok_force = 3.0 <= F_out <= 15.0 and F_ins <= 15.0
    print(f" 2 insertion {F_ins:.1f} N, withdrawal {F_out:.1f} N "
          f"(targets: withdrawal 3..15 N, insertion <= 15 N) {'PASS' if ok_force else 'FAIL'}")

    # ------------------------------------------------------------------ 3 resistance
    rows = []
    for f in (T, R1, R2):
        F = f["F_work"]
        a = math.sqrt(F / (math.pi * H_AU * 1e6))
        Rc = (RHO["Au"] + RHO["brass"]) / (4 * a)
        rows.append(dict(contact=f["contact"], a_um=round(a * 1e6, 1), Rc_mohm=round(Rc * 1e3, 2)))
    res["resistance"] = rows
    print(" 3 constriction resistance (clean, gold on brass):",
          ", ".join(f"{r['contact'].split()[0]} {r['Rc_mohm']} mOhm" for r in rows))

    # ------------------------------------------------------------------ 4 wear
    cycles = 5000
    R_dimple = 1.0e-3                      # m, dimple radius across the slide
    wear = []
    for f, s_contact in ((T, 2.4), (R1, 5.4), (R2, 8.2)):
        slide = 2 * (P.PLUG_L - s_contact) * 1e-3     # m per cycle, in and out
        Fm = f["F_max"] / (2 if "pair" in f["contact"] else 1)   # per dimple
        for K, Kname in ((1e-7, "lubricated, mild"), (1e-6, "lubricated, typical"),
                         (1e-5, "dry, severe")):
            for H, Hn in ((H_AU, "hard Au"), (H_INLAY, "AuAgCu inlay"), (H_PDNI, "PdNi")):
                V = K * Fm * slide * cycles / (H * 1e6)
                h = math.sqrt(V / (math.pi * R_dimple))      # worn cap depth
                wear.append(dict(contact=f["contact"].split()[0], K=K, case=Kname, surface=Hn,
                                 slide_m=round(slide * cycles, 1), depth_um=round(h * 1e6, 2)))
    res["wear"] = wear
    worst_typ = max(w["depth_um"] for w in wear if w["K"] == 1e-6 and w["surface"] == "AuAgCu inlay")
    worst_sev = max(w["depth_um"] for w in wear if w["K"] == 1e-5 and w["surface"] == "AuAgCu inlay")
    stack = dict(inlay="AuAgCu clad inlay 6.0 um over PdNi 1.0 um over Ni 2.0 um on Cu-Ti, PFPE lube",
                 wearable_um=7.0)
    res["plating"] = stack
    ok_wear = stack["wearable_um"] >= 1.5 * worst_typ
    print(f" 4 wear over {cycles} cycles, worst finger, AuAgCu inlay: "
          f"{worst_typ:.2f} um typical, {worst_sev:.2f} um severe")
    for w in wear:
        if w["surface"] == "AuAgCu inlay" and w["K"] == 1e-6:
            print(f"    {w['contact']:3s} slide {w['slide_m']:6.1f} m  depth {w['depth_um']:.2f} um")
    print(f"   plating: {stack['inlay']}, {stack['wearable_um']} um wearable: "
          f"{'PASS' if ok_wear else 'FAIL'} at 1.5x typical. Severe case needs the MON-22 test.")

    # ------------------------------------------------------------------ 5 seal
    g = dict(section=0.40, squeeze=0.25, E_fkm=4.5, perimeter=2 * (14.0 + 3.0))
    contact_stress = g["E_fkm"] * g["squeeze"] * 1.3           # shape factor of a square cord
    line_force = contact_stress * g["section"]
    clamp = line_force * g["perimeter"]
    p_ip68 = 1000 * 9.81 * P.WATER_DEPTH_M / 1e6               # MPa
    p_test = 1000 * 9.81 * 3.0 / 1e6                           # 3 m proof, twice the depth
    stake_d, stake_tau = 0.5, 40.0                             # LCP heat stake, MPa shear
    n_stakes = math.ceil(1.5 * clamp / (stake_tau * math.pi * stake_d**2 / 4))
    res["seal"] = dict(contact_stress_MPa=round(contact_stress, 2), clamp_N=round(clamp, 1),
                       p_ip68_MPa=round(p_ip68, 4), p_proof_MPa=round(p_test, 4),
                       ratio=round(contact_stress / p_test, 1), heat_stakes=n_stakes)
    print(f" 5 pocket gasket: FKM 60A cord 0.40 at 25 % squeeze, perimeter {g['perimeter']:.0f} mm")
    print(f"   contact stress {contact_stress:.2f} MPa against {p_test:.3f} MPa proof head "
          f"(ratio {contact_stress/p_test:.0f}), clamp {clamp:.1f} N, {n_stakes} heat stakes O0.5")
    ok_seal = contact_stress / p_test >= 10
    res["pass"] = dict(forces=ok_force, wear=ok_wear, seal=ok_seal,
                       fingers=all("result" not in f for f in (T, R1, R2)))
    print("RESULT:", res["pass"])
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "contacts.json"), "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
