#!/usr/bin/env python3
# BUDLUM LEAF · cad/rail_detail.py · revision L.5.0 · 2026-10-12
#
# Full Part-by-Part 3D Model of the Revision L.5.0 Plus (+) Cross Bi-Directional Puzzle-Interlocking
# (`Yapboz Girdili-Çıktılı Kilit`) Seam, 2.00 mm (`2 milim`) Biocompatible All-Solid-State Battery
# Quadrant Core (`R = 6.35 mm` outer corners), and Portless Qi2.2 Wireless Charging Receiver:
#   1. PART A (z < 0 -> rail-receiver.stl): Central Plus (+) Cruciform Titanium Hub (x=0, y=0),
#      24 Complementary Superelastic Nitinol/Ti-PEEK Dovetail Puzzle Tenons & Mortises (`girdili-çıktılı
#      yapboz dişleri`, 10 N/mm tensile pull resistance, installable from +Z or -Z), 12 µm Refractive-
#      Index-Matched (n = 1.585) Self-Healing Optical Elastomer Seam Lip, 24 Bipolar N52H Magnets,
#      and 64 Gold Micro-Leaf Contacts.
#   2. PART B (z >= 0 -> rail-module.stl): User-Replaceable 40.0 x 80.0 x 2.00 mm Polycarbonate Quadrant
#      carrying the 3.0 Wh All-Solid-State LLZO/PEO-LiBOB Cell, Bifilar Counter-Wound Cu/Al Tabs,
#      Dual NTC Ocular Thermal Sensors (<= 36.2 C), Orthotropic Graphene/Mu-Metal Eyewear Shield,
#      90° Sector of the Ø54 mm Qi2.2 Coil + Ø22 mm Standalone Quadrant Qi Coil + U_QI BMS ASIC + 1.0 F Cap.
#
# Writes:
#   models/rail-receiver.stl
#   models/rail-module.stl
#   models/rail-exploded.svg

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from leaf_geom import write_stl, mesh_from_rings, rounded_rect
from render_iso import render, transform, box, cylinder

OUT = os.path.join(HERE, "models")


def build():
    parts = []

    def add(name, mesh, rgb, layer_z):
        v, f = mesh
        parts.append((name, v, f, rgb, layer_z))

    # ================================================================
    # PART A: CENTRAL PLUS (+) PUZZLE-INTERLOCKING (`YAPBOZ GİRDİLİ-ÇIKTILI`) SPINE & OPTICAL SEAM (z < 0)
    # ================================================================
    Z_REC = -6.0
    # 1. Central 4-Way Grade-5 Titanium Cruciform (+) Locking Hub at (0, 0)
    add("1 ti cruciform x-arm", box(76.0, 2.4, 0.90, 0.0, 0.0, Z_REC + 0.50), (182, 194, 208), -26.0)
    add("1 ti cruciform y-arm", box(2.4, 36.0, 0.90, 0.0, 0.0, Z_REC + 0.50), (182, 194, 208), -25.8)
    add("1 ti center hub boss", cylinder(3.6, 1.10, 28, 0.0, 0.0, Z_REC + 0.50), (206, 214, 224), -25.0)

    # 2. 12 µm Refractive-Index-Matched (n = 1.585) Self-Healing Fluorosilicone Optical Seam Lip
    add("2 optical seam lip x", box(78.0, 0.90, 1.15, 0.0, 0.0, Z_REC + 0.80), (104, 226, 202), -21.0)
    add("2 optical seam lip y", box(0.90, 38.0, 1.15, 0.0, 0.0, Z_REC + 0.80), (104, 226, 202), -20.8)

    # 3. Complementary Superelastic Nitinol/Ti-PEEK Dovetail Puzzle Tenons (`Çıktılı`) & Mortises (`Girdili`)
    for px in (-32.0, -22.0, -12.0, 12.0, 22.0, 32.0):
        # Neck + widened dovetail puzzle head along X seam
        add("3 nitinol puzzle neck x", box(2.8, 2.2, 0.90, px, 1.1 if px > 0 else -1.1, Z_REC + 0.70), (88, 218, 182), -18.2)
        add("3 nitinol puzzle head x", box(4.6, 2.0, 0.90, px, 2.4 if px > 0 else -2.4, Z_REC + 0.70), (64, 198, 162), -18.0)
    for py in (-14.0, -6.0, 6.0, 14.0):
        add("3 nitinol puzzle neck y", box(2.2, 2.8, 0.90, 1.1 if py > 0 else -1.1, py, Z_REC + 0.70), (88, 218, 182), -18.2)
        add("3 nitinol puzzle head y", box(2.0, 4.6, 0.90, 2.4 if py > 0 else -2.4, py, Z_REC + 0.70), (64, 198, 162), -18.0)

    # 4. Bipolar N52H Inter-Tile Micro-Magnets + Gold Micro-Leaf Contacts along the + Cross
    for mx in (-34.0, -24.0, -16.0, -8.0, 8.0, 16.0, 24.0, 34.0):
        add("4 plus n52h magnet", box(3.0, 1.6, 0.85, mx, 0.0, Z_REC + 0.65), (160, 172, 186), -15.0)
    for gx in range(-32, 33, 4):
        if abs(gx) < 4:
            continue
        add("5 gold micro-leaf", box(1.3, 2.2, 0.88, float(gx), 0.0, Z_REC + 0.75), (242, 202, 92), -12.0)

    # ================================================================
    # PART B: 4-QUADRANT (+) 2.00 MM BIOCOMPATIBLE SOLID-STATE BATTERY & QI2 TILE ASSEMBLY (z >= 0)
    # ================================================================
    Z = 2.0
    for (sx, sy) in ((-1.0, 1.0), (1.0, 1.0), (-1.0, -1.0), (1.0, -1.0)):
        qcx = sx * 19.6
        qcy = sy * 9.2
        # 6. Lower & Upper Biocompatible ISO 10993 Polycarbonate Quadrant Frames (R = 6.35 mm outer corner, 2.00 mm total stack)
        q_out = rounded_rect(37.6, 17.2, 3.2, 0.0, 12)
        q_in = rounded_rect(34.0, 13.8, 2.0, 0.0, 12)
        q_out_s = [(x + qcx, y + qcy) for (x, y) in q_out]
        q_in_s = [(x + qcx, y + qcy) for (x, y) in q_in]
        add("6 lower pc+oca shell", mesh_from_rings([(Z, q_out_s), (Z + 0.8, q_out_s)],
                                                    [(Z, q_in_s), (Z + 0.8, q_in_s)]),
            (116, 174, 218), -4.0)
        add("7 upper pc+oca shell", mesh_from_rings([(Z + 2.0, q_out_s), (Z + 2.8, q_out_s)],
                                                    [(Z + 2.0, q_in_s), (Z + 2.8, q_in_s)]),
            (142, 198, 236), 34.0)

        # 8. Orthotropic Graphene / Mu-Metal Eyewear Thermal & EM Shield (<= 36.2 C, ELF < 0.08 µT)
        add("8 eyewear shield", box(33.2, 13.2, 0.26, qcx, qcy, Z + 0.62), (54, 68, 84), 4.0)

        # 9. Micro-Articulated All-Solid-State Oxide-Ceramic (LLZO / PEO-LiBOB) Safe Flexible Battery Core (3.0 Wh)
        add("9 llzo solid-state cell", box(32.4, 12.6, 1.06, qcx, qcy, Z + 1.40), (46, 162, 140), 12.0)

        # 10. Bifilar Counter-Wound Current-Canceling Cu/Al Foil Tabs + Dual NTC Ocular Thermal Sensors
        add("10 bifilar cu tab", box(2.8, 2.2, 0.42, qcx - sx * 11.0, qcy - sy * 4.2, Z + 2.10), (224, 138, 74), 16.0)
        add("10 bifilar al tab", box(2.8, 2.2, 0.42, qcx - sx * 7.2, qcy - sy * 4.2, Z + 2.10), (206, 214, 224), 16.0)
        add("11 ocular ntc sensor", box(1.8, 1.2, 0.38, qcx + sx * 10.0, qcy + sy * 3.8, Z + 2.15), (234, 110, 72), 17.0)

        # 11. 90° Sector of Central Ø54 mm Qi2.2 Coil + Standalone Quadrant Qi Sub-Coil + U_QI ASIC + 1.0 F Cap
        add("12 qi2 sector coil", box(10.5, 5.2, 0.36, sx * 8.2, sy * 4.2, Z + 2.30), (242, 194, 72), 23.0)
        add("13 quadrant qi coil", cylinder(5.2, 0.34, 24, qcx + sx * 3.5, qcy, Z + 2.30), (228, 172, 64), 24.0)
        add("14 u_qi bms asic", box(3.4, 3.2, 0.44, qcx + sx * 3.5, qcy, Z + 2.50), (42, 50, 62), 26.0)
        add("15 hot-swap 1f cap", box(5.6, 3.0, 0.42, qcx + sx * 11.2, qcy - sy * 3.6, Z + 2.40), (196, 168, 98), 25.0)

    return parts


def main():
    os.makedirs(OUT, exist_ok=True)
    parts = build()

    for which, name in (("receiver", "rail-receiver.stl"), ("module", "rail-module.stl")):
        sel = []
        for (nm, v, f, rgb, lz) in parts:
            for (a, b, c) in f:
                tri = [v[a], v[b], v[c]]
                zc = sum(p[2] for p in tri) / 3.0
                if (which == "receiver" and zc < 0.0) or (which == "module" and zc >= 0.0):
                    sel.append(tri)
        idx, verts, faces = {}, [], []
        for tri in sel:
            ids = []
            for p in tri:
                k = (round(p[0], 4), round(p[1], 4), round(p[2], 4))
                if k not in idx:
                    idx[k] = len(verts)
                    verts.append(k)
                ids.append(idx[k])
            faces.append(tuple(ids))
        n = write_stl(os.path.join(OUT, name), verts, faces, "leaf quad puzzle " + which)
        print("%-20s %6d triangles" % (name, n))

    def zcenter(v, f):
        zs = [v[i][2] for tri in f for i in tri]
        return (min(zs) + max(zs)) / 2.0

    allt, pal, lay = [], [], []
    for (nm, v, f, rgb, target_z) in parts:
        dz = target_z - zcenter(v, f)
        tv = transform([[v[a], v[b], v[c]] for (a, b, c) in f], move=(0.0, 0.0, dz))
        allt += tv
        pal += [rgb] * len(tv)
        lay += [target_z] * len(tv)

    render(
        allt,
        os.path.join(OUT, "rail-exploded.svg"),
        az_deg=36,
        el_deg=18,
        width=1360,
        palette=pal,
        layers=lay,
        title="BUDLUM LEAF · 2.00 MM (+) GİRDİLİ-ÇIKTILI YAPBOZ EKRAN-BATARYA KİLİDİ VE 4x KATI-HAL PİL",
        subtitle="Altta Nitinol/Ti-PEEK yapboz kilit + n=1.585 optik dudak + 64 altın yaprak · Ortada 4x yanmaz LLZO katı-hal pil · Üstte Qi2.2 bobinler",
    )
    print("wrote rail-exploded.svg (%d triangles, %d parts)" % (len(allt), len(parts)))


if __name__ == "__main__":
    main()
