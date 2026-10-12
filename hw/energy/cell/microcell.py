#!/usr/bin/env python3
"""microcell.py - the Budlum Leaf hermetic micro cell, L.6.0.

Energy and BMS team, hw/energy/. Gates ENR-22, ENR-23.

The cell is fixed by FINAL/21 Section 21.2.5:
    outside 9.25 x 9.25 x 0.90 mm, laser-welded 30 um can, own fuse.

This script designs the electrode stack inside that can for two
chemistries and prints capacity (mAh), energy (Wh) and density (Wh/L)
at the stack level and at the cell level.

    G : graphite anode / high-voltage LiCoO2 (4.45 V)   target 600 Wh/L
    S : silicon-carbon composite anode / LiCoO2 (4.48 V) target 750 Wh/L

Run:  python3 hw/energy/cell/microcell.py
Out:  hw/energy/out/cell_spec.json, hw/energy/out/cell_spec.txt
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)

UM = 1e-3  # micrometre in millimetres

# --------------------------------------------------------------------------
# 1. the can  [DECISION] from FINAL/21 Section 21.2.5
# --------------------------------------------------------------------------
CAN = dict(
    L=9.25, W=9.25, H=0.90,          # mm, outside
    r_corner=0.40,                    # mm, outside corner radius (deep draw)
    t_wall=30 * UM,                   # mm, side walls and both faces
    material="316L stainless (Ti Gr.1 option), case negative",
    rho_316L=7.99,                    # g/cm3
)

# lateral margins, per side, from the inner wall inward  [HYPOTHESIS]
LAT = dict(
    weld_clear=0.100,   # laser seam heat zone kept free of polymer
    frame=0.050,        # PEEK insulating locator frame
    sep_over=0.100,     # separator overhang beyond the anode edge
    an_over=0.100,      # anode overhang beyond the cathode edge
    edge_dead=0.020,    # laser-cut edge damage, inactive cathode rim
)
# corner notches (mm, square) cut out of the electrodes
NOTCH_FT = 1.40   # positive feedthrough corner: 1.10 mm HTCC insert + clearance
NOTCH_TAB = 0.70  # negative tab-bundle weld corner, opposite diagonal
R_EL = 0.30       # electrode corner radius

# thickness reserves, total  [HYPOTHESIS]
T_LINER = 2 * 5 * UM     # 5 um polyimide liner on each face
T_TOL = 20 * UM          # stack-up tolerance reserve

# --------------------------------------------------------------------------
# 2. the chemistries
# --------------------------------------------------------------------------
# Sources, tagged in hw/energy/01-MICRO-CELL.md:
#  [PUBLICATION] Zhang J.-N. et al., Nature Energy 4, 594 (2019): doped LiCoO2
#     cycles at 4.6 V; 4.45-4.48 V LiCoO2 is the shipping phone cathode.
#  [PUBLICATION] Schweidler S. et al., J. Phys. Chem. C 122, 8829 (2018):
#     graphite expands about 10 % in volume on full lithiation.
#  [PUBLICATION] Obrovac M. N., Chevrier V. L., Chem. Rev. 114, 11444 (2014):
#     silicon alloys expand up to about 280 %; composites limit electrode swell.
#  [PUBLICATION] Enovix AI-1, 935 Wh/L, Polaris Battery Labs, 13 Jan 2026.
VARIANTS = {
    "G": dict(
        name="graphite / LiCoO2 4.45 V",
        target_whl=600.0,
        v_nom=3.87, v_max=4.45, v_min=3.00,
        # cathode
        q_c=182.0, f_c=0.97, rho_c=4.10, t_al=9 * UM,
        # anode
        q_a=350.0, f_a=0.96, rho_a=1.70, t_cu=6 * UM, np=1.08,
        # separator: 5 um PE + 2 um Al2O3 coat
        t_sep=7 * UM,
        # electrode thickness swell: reversible + end of life
        sw_a=0.06 + 0.04, sw_c=0.02,
        pad_comp=0.70,          # compliance pad compresses 70 % at end of life
        L_max=4.5,              # mAh/cm2 per side, phone-class ceiling
        asi=20.0,               # ohm cm2, DC 10 s, energy design
        can="316L",
    ),
    "S": dict(
        name="Si-C composite / LiCoO2 4.48 V",
        target_whl=750.0,
        v_nom=3.80, v_max=4.48, v_min=2.80,
        q_c=188.0, f_c=0.97, rho_c=4.10, t_al=9 * UM,
        # silicon-carbon composite blended with graphite, prelithiated
        q_a=1000.0, f_a=0.92, rho_a=1.05, t_cu=6 * UM, np=1.10,
        t_sep=7 * UM,
        sw_a=0.15 + 0.07, sw_c=0.02,
        pad_comp=0.70,
        L_max=4.5,
        asi=18.0,
        can="316L",
    ),
}


def rounded_rect_area(a, b, r):
    return a * b - (4 - math.pi) * r * r


def geometry():
    inner = CAN["L"] - 2 * CAN["t_wall"]
    inner_w = CAN["W"] - 2 * CAN["t_wall"]
    inner_h = CAN["H"] - 2 * CAN["t_wall"]
    edge = LAT["weld_clear"] + LAT["frame"] + LAT["sep_over"]
    an_l, an_w = inner - 2 * edge, inner_w - 2 * edge
    ca_l, ca_w = an_l - 2 * LAT["an_over"], an_w - 2 * LAT["an_over"]
    cath_area_geo = rounded_rect_area(ca_l, ca_w, R_EL) \
        - NOTCH_FT ** 2 - NOTCH_TAB ** 2
    perim = 2 * (ca_l + ca_w)
    cath_area = cath_area_geo - perim * LAT["edge_dead"]
    v_cell = rounded_rect_area(CAN["L"], CAN["W"], CAN["r_corner"]) * CAN["H"]
    return dict(inner_side=inner, inner_h=inner_h,
                anode_side=math.sqrt(an_l * an_w),
                cath_side=math.sqrt(ca_l * ca_w), cath_area_mm2=cath_area,
                cell_volume_mm3=v_cell)


def design_box(key, L, W, H):
    """the same build in another can, for the B cell. Restores the can."""
    saved = dict(CAN)
    CAN.update(L=L, W=W, H=H)
    try:
        d = design(key)
        d["can_mm"] = [L, W, H]
        return d
    finally:
        CAN.clear()
        CAN.update(saved)


def per_side_um(v):
    """coating thickness per side per 1 mAh/cm2, in mm."""
    tc = 1.0 / (v["q_c"] * v["f_c"] * v["rho_c"]) * 10.0      # cm -> mm
    ta = v["np"] / (v["q_a"] * v["f_a"] * v["rho_a"]) * 10.0
    return tc, ta


def stack(v, n, L):
    """n double-sided cathodes, n-1 double-sided anodes, 2 single-sided
    outer anodes against the case-negative can, 2n separators."""
    tc, ta = per_side_um(v)
    c = n * (v["t_al"] + 2 * tc * L)
    a = (n - 1) * (v["t_cu"] + 2 * ta * L) + 2 * (v["t_cu"] + ta * L)
    s = 2 * n * v["t_sep"]
    swell = (2 * n * ta * L * v["sw_a"] + 2 * n * tc * L * v["sw_c"])
    pad = swell / v["pad_comp"]
    return dict(cathodes=c, anodes=a, separators=s, active_stack=c + a + s,
                swell=swell, pad=pad,
                total=c + a + s + pad + T_LINER + T_TOL,
                t_cath_side=tc * L, t_an_side=ta * L)


def design(key):
    v = VARIANTS[key]
    g = geometry()
    best = None
    for n in range(1, 8):
        # thickness is linear in L: solve for the largest L that fits
        s0 = stack(v, n, 0.0)["total"]
        s1 = stack(v, n, 1.0)["total"] - s0
        L = min(v["L_max"], (g["inner_h"] - s0) / s1)
        if L <= 0:
            continue
        cap = 2 * n * L * g["cath_area_mm2"] / 100.0          # mAh
        if best is None or cap > best["cap_mAh"] + 1e-9:
            best = dict(n=n, L=L, cap_mAh=cap)
    n, L = best["n"], best["L"]
    st = stack(v, n, L)
    cap = best["cap_mAh"]
    e_wh = cap * v["v_nom"] / 1000.0
    v_stack_mm3 = g["cath_area_mm2"] * st["active_stack"]
    # stack level: the cathode footprint times the active stack height
    whl_stack = e_wh / (v_stack_mm3 * 1e-6)
    whl_cell = e_wh / (g["cell_volume_mm3"] * 1e-6)
    el_area_cm2 = 2 * n * g["cath_area_mm2"] / 100.0
    r_dc = v["asi"] / el_area_cm2
    # mass estimate (g)
    can_mass = (2 * rounded_rect_area(CAN["L"], CAN["W"], CAN["r_corner"])
                + 4 * CAN["L"] * CAN["H"]) * CAN["t_wall"] * CAN["rho_316L"] / 1000
    tc, ta = per_side_um(v)
    m_cath = 2 * n * L / (v["q_c"] * v["f_c"]) * g["cath_area_mm2"] / 100 / 1000 * 1000
    m_an = 2 * n * L * v["np"] / (v["q_a"] * v["f_a"]) * g["anode_side"] ** 2 / 100
    m_foil = (n * v["t_al"] * 2.70 + (n + 1) * v["t_cu"] * 8.96) * g["anode_side"] ** 2 / 1000
    m_sep = 2 * n * v["t_sep"] * 1.4 * (g["anode_side"] + 0.2) ** 2 / 1000
    pore = 0.25 * (st["active_stack"] * g["cath_area_mm2"]) / 1000   # cm3
    m_ely = 1.25 * pore * 1.2
    m_misc = 0.020  # HTCC feedthrough, frame, tabs, pad
    mass = can_mass + m_cath / 1000 + m_an / 1000 + m_foil + m_sep + m_ely + m_misc
    # the stored chemical energy for the single-cell fault case
    return dict(
        variant=key, name=v["name"], n_cathodes=n, n_anodes=n + 1,
        loading_mAh_cm2=round(L, 3),
        t_cathode_coat_um=round(st["t_cath_side"] / UM, 1),
        t_anode_coat_um=round(st["t_an_side"] / UM, 1),
        t_al_um=v["t_al"] / UM, t_cu_um=v["t_cu"] / UM, t_sep_um=v["t_sep"] / UM,
        stack_um=dict(cathodes=round(st["cathodes"] / UM, 1),
                      anodes=round(st["anodes"] / UM, 1),
                      separators=round(st["separators"] / UM, 1),
                      swell_allowance=round(st["swell"] / UM, 1),
                      compliance_pad=round(st["pad"] / UM, 1),
                      liners=round(T_LINER / UM, 1),
                      tolerance=round(T_TOL / UM, 1),
                      total=round(st["total"] / UM, 1),
                      inner_height=round(g["inner_h"] / UM, 1)),
        cathode_area_mm2=round(g["cath_area_mm2"], 2),
        capacity_mAh=round(cap, 2),
        v_nom=v["v_nom"], v_max=v["v_max"], v_min=v["v_min"],
        energy_Wh=round(e_wh, 5),
        energy_J=round(e_wh * 3600, 1),
        whl_stack=round(whl_stack, 0),
        whl_cell=round(whl_cell, 0),
        target_whl=v["target_whl"],
        margin_vs_target=round(whl_cell / v["target_whl"] - 1, 3),
        dcir_ohm=round(r_dc, 2),
        mass_g=round(mass, 3),
        wh_kg=round(e_wh / mass * 1000, 0),
    )


def sensitivity(key):
    """how cell Wh/L moves with the lateral margin and the loading cap."""
    rows = []
    base = dict(LAT)
    for d in (-0.05, 0.0, +0.05, +0.10):
        for k in ("weld_clear", "sep_over", "an_over"):
            LAT[k] = base[k] + d / 3.0
        r = design(key)
        rows.append(("lateral margin %+0.2f mm/side" % d, r["whl_cell"]))
    LAT.update(base)
    v = VARIANTS[key]
    lm = v["L_max"]
    for L in (3.0, 3.5, 4.0, lm):
        v["L_max"] = L
        rows.append(("loading cap %.1f mAh/cm2" % L, design(key)["whl_cell"]))
    v["L_max"] = lm
    sw = v["sw_a"]
    for x in (0.10, 0.22, 0.35, 0.50):
        v["sw_a"] = x
        rows.append(("anode swell %.0f %% (rev + EOL)" % (100 * x), design(key)["whl_cell"]))
    v["sw_a"] = sw
    return rows


def main():
    g = geometry()
    res = {"geometry": {k: round(x, 4) for k, x in g.items()},
           "can": {k: CAN[k] for k in ("L", "W", "H", "r_corner", "t_wall", "material")},
           "lateral_margins_mm": LAT,
           "variants": {}}
    lines = []
    p = lines.append
    p("BUDLUM LEAF  hermetic micro cell  9.25 x 9.25 x 0.90 mm  (ENR-22)")
    p("cell envelope volume  %.2f mm3" % g["cell_volume_mm3"])
    p("inner cavity          %.3f x %.3f x %.3f mm" % (g["inner_side"], g["inner_side"], g["inner_h"]))
    p("anode side %.3f mm, cathode side %.3f mm, net cathode area %.2f mm2"
      % (g["anode_side"], g["cath_side"], g["cath_area_mm2"]))
    p("")
    for k in VARIANTS:
        d = design(k)
        res["variants"][k] = d
        res["variants"][k]["sensitivity"] = sensitivity(k)
        p("[%s] %s" % (k, d["name"]))
        p("  cathodes %d (2-sided), anodes %d (2 outer single-sided)" % (d["n_cathodes"], d["n_anodes"]))
        p("  loading %.2f mAh/cm2/side, cathode coat %.1f um, anode coat %.1f um"
          % (d["loading_mAh_cm2"], d["t_cathode_coat_um"], d["t_anode_coat_um"]))
        s = d["stack_um"]
        p("  height um: cath %.1f + anode %.1f + sep %.1f + pad %.1f + liners %.1f + tol %.1f = %.1f of %.1f"
          % (s["cathodes"], s["anodes"], s["separators"], s["compliance_pad"],
             s["liners"], s["tolerance"], s["total"], s["inner_height"]))
        p("  swell allowance %.1f um (taken by the pad at %d %% compression)"
          % (s["swell_allowance"], round(VARIANTS[k]["pad_comp"] * 100)))
        p("  capacity %.2f mAh  energy %.4f Wh (%.0f J)  at %.2f V nominal"
          % (d["capacity_mAh"], d["energy_Wh"], d["energy_J"], d["v_nom"]))
        p("  stack %.0f Wh/L   cell %.0f Wh/L   target %.0f   margin %+.1f %%"
          % (d["whl_stack"], d["whl_cell"], d["target_whl"], 100 * d["margin_vs_target"]))
        p("  DCIR about %.1f ohm, mass about %.3f g, %.0f Wh/kg"
          % (d["dcir_ohm"], d["mass_g"], d["wh_kg"]))
        for name, w in res["variants"][k]["sensitivity"]:
            p("    sens: %-32s %5.0f Wh/L" % (name, w))
        p("")
    # pack roll-up at the target density and at the model density
    p("128-cell roll-up")
    v128 = 128 * g["cell_volume_mm3"] / 1000
    p("  cell volume x 128 = %.3f cm3 (FINAL/21 used 9.56 cm3)" % v128)
    for k, d in res["variants"].items():
        p("  [%s] at target %.0f Wh/L: %.2f Wh, per quadrant %.3f Wh;  at model: %.2f Wh, per quadrant %.3f Wh"
          % (k, d["target_whl"], v128 * d["target_whl"] / 1000, v128 * d["target_whl"] / 4000,
             128 * d["energy_Wh"], 32 * d["energy_Wh"]))
    res["pack_cell_volume_cm3"] = round(v128, 4)
    # the B cell of FINAL/21, 20.0 x 8.0 x 1.50 mm, built the same way
    p("")
    p("B cell, 20.0 x 8.0 x 1.50 mm, in the same 30 um can build")
    res["b_cell"] = {}
    for k in VARIANTS:
        d = design_box(k, 20.0, 8.0, 1.50)
        res["b_cell"][k] = d
        p("  [%s] %d cathodes, %.2f mAh/cm2, %.1f mAh, %.4f Wh, %.0f Wh/L (target 0.14 Wh at 600 Wh/L)"
          % (k, d["n_cathodes"], d["loading_mAh_cm2"], d["capacity_mAh"], d["energy_Wh"], d["whl_cell"]))
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(OUT, "cell_spec.json"), "w") as f:
        json.dump(res, f, indent=1)
    with open(os.path.join(OUT, "cell_spec.txt"), "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
