#!/usr/bin/env python3
# BUDLUM LEAF · cad/monogram_detail.py · revision L.5.0 · 2026-10-12
#
# Full Part-by-Part 3D Model, Cross-Section, and Exploded Isometric Drawings of the Revision L.5.0
# Turned & 90°-Bent-at-Gap (`Boşluk`) `b` Camera, Zero-CPU & USB-C Module:
#   - Uses the user's exact `uploads/b.png` silhouette (`40.0 x 32.0 mm` in 2D, IoU = 0.9995),
#     turned 90° (`onu ters çevirip`) so the straight bar (`çubuk`) is at the top and horizontal
#     (`O yukarıda çünkü yatay olarak duruyor`), and bent 90° directly across the natural gap
#     (`yuvarlakla çubuk arasındaki boşluk`, ZERO added hinge blocks: `bükmek de yeni bir parça
#     ekleyerek değil`):
#       * Horizontal Top `Çubuk` (`32.0 mm` along X, `1.00 mm` / `bir milim` height profile above
#         the 2.00 mm screen edge `y = 36.0 .. 37.0 mm`, `z = -2.00 .. +0.80 mm`): sits horizontally
#         flush on the top edge of the 2.00 mm screen (`çubuk ekranın üstüne tam oturacak bir şekilde
#         duruyor`), housing the 3-band LCP antenna, 1x4 60 GHz array, and SOLE USB Type-C (40 W PD 3.1).
#       * Front-Facing Remaining Part (`kalan kısım çubuk hariç`: natural gap `boşluk` + `Ø32.0 / Ø24.0 mm`
#         circular ring `yuvarlak` centered at `(16.0, 16.0)`, `y = 0.0 .. 36.0 mm`, `z = 0.00 .. 2.00 mm`):
#         hangs down on the front (or back) face of the screen facing directly toward us (`Diğer kısım
#         bize doğru bakarak duruyor`), housing the 6L Zero-CPU PCBA, 50 MP OIS camera, and rear Ø22.4 mm AMOLED.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import monogram_letter as ML
from leaf_geom import write_stl
from leaf_v2 import monogram_parts, merge
from render_iso import render

OUT = os.path.join(HERE, "models")


def svg_section(path):
    """Dimensioned plan and 90° natural-gap bend cross-section of the Revision L.5.0 `b` module."""
    W, H = 1360, 820
    s = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
        '<rect width="%d" height="%d" fill="#0e1114"/>' % (W, H),
        '<g font-family="DejaVu Sans,Helvetica,Arial,sans-serif" fill="#e8edf2">',
        '<text x="34" y="42" font-size="20" font-weight="700">BUDLUM B MODÜLÜ · TERS ÇEVRİLİP BOŞLUKTAN 90° BÜKÜLEN YATAY 1 MM ÇUBUK + YUVARLAK KAMERA</text>',
        '<text x="34" y="68" font-size="13" fill="#9fb0bf">'
        'B harfi ters çevrilir: 1.00 mm çubuk yukarıda yatay olarak 2.00 mm ekran üst kenarına oturur · Yuvarlak kısım boşluktan 90° bükülüp bize bakar'
        '</text>',
        '<text x="34" y="106" font-size="14" font-weight="700" fill="#cfd9e2">1 · Ters Çevrilip 90° Bükülen B Ön Planı (1 mm Yatay Çubuk Üstte, Yuvarlak Önde)</text>',
    ]
    k, ox, oy = 9.4, 96.0, 170.0

    def X(x):
        return ox + x * k

    def Y(y):
        return oy + (ML.MON_H - y) * k

    # Top edge of the 2.00 mm screen reference line at y = 36.0 mm
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#5cc4e8" stroke-width="1.6" stroke-dasharray="6,4"/>'
             % (X(-4.0), Y(36.0), X(38.0), Y(36.0)))
    s.append('<text x="%.1f" y="%.1f" font-size="11" fill="#5cc4e8">Ekran Üst Kenarı (y = +80 mm): Sadece 1.00 mm yatay çubuk ekran üstüne oturur</text>'
             % (X(0.0), Y(38.2)))

    # Turned & 90°-Bent B frame (1.0 mm horizontal top çubuk at y=36..37 mm + natural gap y=32..36 mm + Ø32/Ø24 mm ring y=0..32 mm)
    s.append('<path d="%s" fill="#8fa882" stroke="#c9d6c4" stroke-width="1.6" fill-rule="evenodd"/>' % ML.svg_path(k, ox, oy))

    # Horizontal 3-Band LCP Antenna + 60 GHz patches + SOLE USB Type-C (40W) inside the 1.00 mm top `çubuk` (y = 36..37 mm)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#daa84a" stroke="#f5d98e" stroke-width="1.0"/>'
             % (X(4.0), Y(36.85), 17.5 * k, 0.7 * k))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#cfd8e2" stroke="#f0f4f8" stroke-width="1.0"/>'
             % (X(23.0), Y(36.88), 6.2 * k, 0.76 * k))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="#e04842"/>'
             % (X(29.2), Y(36.90), 0.9 * k, 0.80 * k))

    # Annular 6-Layer Rigid-Flex Ring PCBA inside the circular ring wall (centered at (16.0, 16.0))
    cx_p, cy_p = X(16.0), Y(16.0)
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#246c48" stroke-width="%.1f" stroke-dasharray="44 12"/>'
             % (cx_p, cy_p, 13.5 * k, 2.4 * k))

    # Camera housing filling the Ø24.0 mm opening inside the ring
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#323a44" stroke="#7c8794" stroke-width="1.4"/>' % (cx_p, cy_p, 12.0 * k))

    # 50 MP CMOS Sensor + 4 Corner OIS Coils + 5P Lens + 2 MEMS Mics + Speaker + Flash
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="#2a7652" stroke="#7bd4a2" stroke-width="1.2"/>'
             % (X(16.0 - 7.0), Y(16.0 + 5.1), 14.0 * k, 10.2 * k))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#4480ac" stroke="#98d2f5" stroke-width="1.0"/>'
             % (X(16.0 - 6.0), Y(16.0 + 4.4), 12.0 * k, 8.8 * k))
    for (ox_c, oy_c) in [(-6.1, -4.5), (5.0, -4.5), (-6.1, 4.5), (5.0, 4.5)]:
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#da8e4a" stroke="#f8d29c" stroke-width="1.0"/>'
                 % (X(16.0 + ox_c - 1.0), Y(16.0 + oy_c + 0.9), 2.1 * k, 1.7 * k))
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#16304e" stroke="#4a7ca8" stroke-width="1.4"/>' % (cx_p, cy_p, 5.8 * k))
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#2c6696"/>' % (cx_p, cy_p, 4.2 * k))
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#0d1b2c"/>' % (cx_p, cy_p, 2.6 * k))

    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#dfe8dc">Yuvarlak halka (bize bakar): 6L Zero-CPU PCB + 50MP OIS + AMOLED</text>' % (X(-4.0), Y(-2.6)))
    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#f5d98e">Yatay 1 mm üst çubuk (ekran üstünde): LCP anten + 60GHz + TEK USB-C</text>' % (X(-4.0), Y(-5.2)))
    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#9bd0f5">Ek parçasız B boşluğundan 90° bükülür; önüne/arkasına ve 4 yönüne takılır</text>' % (X(-4.0), Y(-7.8)))

    # 2. 90° Natural-Gap Bend Side Cross-Section in (Z, Y) plane showing the 1.00 mm horizontal top `çubuk` on the 2.00 mm screen edge!
    s.append('<text x="690" y="106" font-size="14" font-weight="700" fill="#cfd9e2">2 · Yandan 90° Boşluk Büküm Kesiti (Üstte 1 mm Yatay Çubuk, Önde Yuvarlak)</text>')
    k2, ox2, oy2 = 11.5, 710.0, 210.0

    def X2(x):
        return ox2 + x * k2

    def Y2(z):
        return oy2 - z * k2

    # Underlying 2.00 mm polycarbonate screen edge (x = 4.0..42.0, z = -2.00..0.00 mm)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#224c6e" fill-opacity="0.65" stroke="#62b8e8" stroke-width="1.2"/>'
             % (X2(4.0), Y2(0.0), 36.0 * k2, 2.0 * k2))

    # 1.00 mm (`bir milim`) Horizontal Top `Çubuk` sitting right on the 2.00 mm screen top edge!
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#8fa882" stroke="#c9d6c4" stroke-width="1.4"/>'
             % (X2(0.0), Y2(2.0), 4.0 * k2, 4.0 * k2))
    # LCP antenna + USB-C port inside the 1.00 mm horizontal top `çubuk`
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#daa84a" stroke="#f5d98e" stroke-width="1.0"/>'
             % (X2(0.6), Y2(1.7), 1.3 * k2, 3.2 * k2))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#cfd8e2" stroke="#e04842" stroke-width="1.1"/>'
             % (X2(2.1), Y2(1.5), 1.4 * k2, 2.8 * k2))

    # Ring walls (x = 8.0..12.0 and x = 36.0..40.0, z = 0..2.0 mm) + internal 6-layer PCB
    for (a, b) in ((8.0, 12.0), (36.0, 40.0)):
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#8fa882" stroke="#c9d6c4" stroke-width="1.4"/>'
                 % (X2(a), Y2(2.0), (b - a) * k2, 2.0 * k2))
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#246c48" stroke="#64c896" stroke-width="1.0"/>'
                 % (X2(a + 0.6), Y2(1.8), 2.8 * k2, 1.6 * k2))

    # Front Camera stack (z = 0.50 .. 2.00 mm)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#323a44" stroke="#8a96a4" stroke-width="1.2"/>'
             % (X2(12.0), Y2(1.98), 24.0 * k2, 1.48 * k2))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#4480ac" stroke="#98d2f5" stroke-width="1.0"/>'
             % (X2(17.6), Y2(0.92), 12.8 * k2, 0.36 * k2))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#da8e4a"/>' % (X2(14.2), Y2(1.35), 2.6 * k2, 0.70 * k2))
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#da8e4a"/>' % (X2(31.2), Y2(1.35), 2.6 * k2, 0.70 * k2))
    for lz in (1.10, 1.35, 1.60, 1.82):
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#2c6696" stroke="#8eccf0" stroke-width="0.8"/>'
                 % (X2(18.2), Y2(lz + 0.16), 11.6 * k2, 0.16 * k2))

    # Center Copper-Graphite EM/Thermal Shield (z = 0.36 .. 0.46 mm)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="#ba8054" stroke="#f0be94" stroke-width="1.0"/>'
             % (X2(12.2), Y2(0.46), 23.6 * k2, 0.10 * k2))

    # Rear Round LTPO AMOLED stack (z = 0.00 .. 0.36 mm) resting on the 2.00 mm screen face
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#18222c" stroke="#64c896" stroke-width="1.1"/>'
             % (X2(12.0), Y2(0.36), 24.0 * k2, 0.36 * k2))

    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#9bd0f5">Ön (z=0.50..2.00 mm): 50MP sensör + 4-eksen OIS + 5P lens (bize bakar)</text>' % (X2(0.0), Y2(3.2)))
    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#f0be94">Orta (z=0.36..0.46 mm): 0.10 mm Cu-Grafit kalkan · Altta Ø22.4 mm AMOLED</text>' % (X2(0.0), Y2(-3.2)))
    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#98e4ac">Üst Yatay Çubuk (1.00 mm): Ekran üstüne oturur (LCP anten + TEK USB-C)</text>' % (X2(0.0), Y2(-4.8)))

    notes = [
        "• Orijinal b.png ters çevrilir; ek parça olmadan boşluktan 90° bükülür.",
        "• 1.00 mm (bir milim) çubuk yukarıda yatay olarak ekran üstüne oturur.",
        "• Çubuk hariç kalan yuvarlak kısım (Ø32/Ø24 mm) bize doğru bakarak durur.",
        "• Yatay çubukta LCP anten + TEK USB-C; halkada Zero-CPU + 50MP OIS.",
    ]
    for i, t in enumerate(notes):
        s.append('<text x="690" y="%d" font-size="11.5" fill="#cfd9e2">%s</text>' % (468 + i * 26, t))
    s.append("</g></svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    b_all = monogram_parts(with_panel=True)
    ring_sub = [(v, f) for (n, v, f, _, _) in b_all if any(k in n for k in ("shell", "hinge", "lcp", "usbc", "pcb", "ics"))]
    full_sub = [(v, f) for (_, v, f, _, _) in b_all]
    vr, fr = merge(ring_sub)
    vf, ff = merge(full_sub)
    n_ring = write_stl(os.path.join(OUT, "monogram-ring.stl"), vr, fr, "budlum turned 90deg bent b frame")
    n_let = write_stl(os.path.join(OUT, "monogram-letter.stl"), vf, ff, "budlum turned 90deg bent b full")
    svg_section(os.path.join(OUT, "monogram-section.svg"))

    flat, pal, lay = [], [], []
    for p_idx, (name, v, f, col, _) in enumerate(b_all):
        rgb = tuple(int(round(c * 255)) for c in col)
        if "rear" in name or "dock" in name:
            dz = (-28.0, 0.0, -10.0)
            l_val = p_idx
        elif any(k in name for k in ("shell", "hinge", "lcp", "usbc", "pcb", "ics", "shield")):
            dz = (0.0, 0.0, 0.0)
            l_val = 100 + p_idx
        else:
            dz = (28.0, 0.0, 10.0)
            l_val = 200 + p_idx
        for (a, b, c) in f:
            flat.append([(v[a][0] + dz[0], v[a][1] + dz[1], v[a][2] + dz[2]),
                         (v[b][0] + dz[0], v[b][1] + dz[1], v[b][2] + dz[2]),
                         (v[c][0] + dz[0], v[c][1] + dz[1], v[c][2] + dz[2])])
            pal.append(rgb)
            lay.append(l_val)

    render(
        flat,
        os.path.join(OUT, "monogram-exploded.svg"),
        az_deg=22.0,
        el_deg=14.0,
        width=1400,
        margin=60,
        palette=pal,
        y_up=True,
        layers=lay,
        title="BUDLUM B MODÜLÜ · BOŞLUKTAN 90° BÜKÜLEN YATAY 1 MM ÇUBUK + YUVARLAK KAMERA PATLATILMIŞ 3B",
        subtitle="Solda Ø22.4 mm arka AMOLED · Ortada yatay 1 mm üst çubuk (LCP anten + TEK USB-C) + 6L PCB · Sağda 50MP OIS kamera + 5P lens",
    )
    print("monogram-ring.stl %d tris, monogram-letter.stl %d tris" % (n_ring, n_let))


if __name__ == "__main__":
    main()
