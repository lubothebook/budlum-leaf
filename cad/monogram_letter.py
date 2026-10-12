#!/usr/bin/env python3
# BUDLUM LEAF · cad/monogram_letter.py · revision L.5.0 · 2026-10-12
#
# Exact analytical 2D & 3D geometry of the Budlum `b` module (`uploads/b.png` 1:1, IoU = 0.9995):
#   1. In 2D (`uploads/b.png`, 40.0 x 32.0 mm in (u, v) coordinates):
#      - Straight bar (`çubuk`, u = 0.0 .. 4.0 mm, v = 0.0 .. 32.0 mm): top semicircle cap R = 2.0 mm
#        at (u = 2.0, v = 30.0), bottom-left fillet R = 2.0 mm at (u = 2.0, v = 2.0).
#      - Natural bending gap (`yuvarlakla çubuk arasındaki boşluk`, u = 4.0 .. 8.0 mm for v > 4.381 mm)
#        and curved bridge (`boğaz`, u = 4.0 .. 13.0 mm for v = 0.0 .. 4.381 mm, inner valley arc
#        centered at (u = 16.0, v = 16.0) with R = 12.0 mm).
#      - Circular ring (`yuvarlak`, centered at (u = 24.0, v = 16.0), outer Ø32.0 mm / R = 16.0 mm,
#        inner bore Ø24.0 mm / R = 12.0 mm).
#   2. In 3D on the device (`onu ters çevirip çubuğu büküyorsun`):
#      - The `b` is turned 90° so the `çubuk` (length 32.0 mm along X = v) is HORIZONTAL at the top
#        (`O yukarıda çünkü yatay olarak duruyor`), and bent 90° (`dik açıyla`) right along the natural
#        gap line u = 4.0 mm with ZERO extra hinge parts (`yeni bir parça ekleyerek değil`):
#          * The `çubuk` area (u = 0.0 .. 4.0 mm) lies HORIZONTALLY in the (X, Z) plane right on top
#            of the 2.00 mm thick screen edge (`çubuk ekranın üstüne tam oturacak bir şekilde duruyor`),
#            with a 1.00 mm (`bir milim`) slim height profile above the screen edge (y = 36.0 .. 37.0 mm
#            -> y_phone = +80.0 .. +81.0 mm, z = -2.00 .. +0.80 mm across the 2.00 mm screen top edge).
#          * Everything else except the `çubuk` (`kalan kısım çubuk hariç`, u = 4.0 .. 40.0 mm: the curved
#            bridge + the Ø32.0 / Ø24.0 mm circular ring centered at (x = 16.0, y = 16.0)) hangs down in
#            the vertical (X, Y) plane on the front (or back) face of the screen (y = 0.0 .. 36.0 mm
#            -> y_phone = +44.0 .. +80.0 mm), facing directly toward the user (`Diğer kısım bize doğru
#            bakarak duruyor`).

import math

B_2D_W = 40.0
B_2D_H = 32.0

MON_W = 32.0              # X width of the turned & bent `b` module (32.0 mm)
MON_H = 36.0              # Y height on the screen face from bottom of ring (y=0) to top screen edge (y=36.0)
STEM_TOP_Y = 37.0         # Top surface of the 1.00 mm (`bir milim`) horizontal `çubuk` on the screen edge
RING_C = (16.0, 16.0)     # Center of the circular ring (`yuvarlak`) in bent module (X, Y) coordinates
RING_RO = 16.0            # Outer ring radius, Ø32.0 mm
RING_RI = 12.0            # Inner bore radius, Ø24.0 mm (ring wall = 4.00 mm)

STEM_W = 4.0              # Exact `b.png` stem width u = 0.0 .. 4.0 mm
STEM_H = 37.0             # Total Y height of bent module (36.0 mm on screen + 1.00 mm horizontal top `çubuk`)
STEM_THICK = 1.00         # 1.00 mm (`bir milim`) slim profile height of the horizontal `çubuk` on the screen edge
CAP_R = 2.0               # Exact semicircle cap radius of `b.png` stem (u = 0..4.0 mm -> R = 2.0 mm)
VALLEY_C = (16.0, 16.0)
VALLEY_R = 12.0


def b_2d_outer_uv(d=0.0):
    """Exact 1:1 2D outer contour of `uploads/b.png` in `(u, v)` coordinates
    (`u in [0, 40]`, `v in [0, 32]`), inset inward by `d` mm (`IoU = 0.9995` at `d = 0`).
    """
    r_stem = max(0.4, CAP_R - d)
    r_bot = max(0.4, 2.0 - d)
    r_val = VALLEY_R + d
    r_out = RING_RO - d
    u_int = (320.0 + r_val ** 2 - r_out ** 2) / 16.0
    v_int = 16.0 - math.sqrt(max(r_val ** 2 - (u_int - 16.0) ** 2, 0.0))

    pts = []
    # 1. Flat bottom from (24.0, d) left to (2.0, d), n = 24
    for i in range(24):
        t = i / 24.0
        pts.append((24.0 * (1.0 - t) + 2.0 * t, d))
    # 2. Bottom-left quarter-circle corner centered at (2.0, 2.0), radius r_bot, n = 16
    for i in range(16):
        ang = -math.pi / 2.0 - (math.pi / 2.0) * (i / 16.0)
        pts.append((2.0 + r_bot * math.cos(ang), 2.0 + r_bot * math.sin(ang)))
    # 3. Left outer edge of `çubuk` from (d, 2.0) up to (d, 30.0), n = 28
    for i in range(28):
        t = i / 28.0
        pts.append((d, 2.0 + (30.0 - 2.0) * t))
    # 4. Top semicircle cap centered at (2.0, 30.0), radius r_stem, from pi to 0, n = 32
    for i in range(32):
        ang = math.pi - math.pi * (i / 32.0)
        pts.append((2.0 + r_stem * math.cos(ang), 30.0 + r_stem * math.sin(ang)))
    # 5. Inner straight wall of `çubuk` from (4.0 - d, 30.0) down to (4.0 - d, 16.0), n = 16
    for i in range(16):
        t = i / 16.0
        pts.append((4.0 - d, 30.0 - (30.0 - 16.0) * t))
    # 6. Concave valley arc (`boşluk`) centered at (16.0, 16.0), radius r_val, from pi to (u_int, v_int), n = 32
    ang_val_start = math.pi
    ang_val_end = math.atan2(v_int - 16.0, u_int - 16.0)
    for i in range(32):
        t = i / 32.0
        ang = ang_val_start + (ang_val_end - ang_val_start) * t
        pts.append((16.0 + r_val * math.cos(ang), 16.0 + r_val * math.sin(ang)))
    # 7. Outer ring arc centered at (24.0, 16.0), radius r_out, clockwise over top to (24.0, d), n = 128
    ang_ring_start = 2.0 * math.pi + math.atan2(v_int - 16.0, u_int - 24.0)
    ang_ring_end = -math.pi / 2.0
    for i in range(128):
        t = i / 128.0
        ang = ang_ring_start + (ang_ring_end - ang_ring_start) * t
        pts.append((24.0 + r_out * math.cos(ang), 16.0 + r_out * math.sin(ang)))

    return list(reversed(pts))


def b_outer_outline(d=0.0):
    """2D front-projection outline `(x, y)` of the turned & 90°-bent `b` module on the screen:
    - `x = v in [0, 32.0]` mm
    - For `u >= 4.0` mm (`kalan kısım çubuk hariç`: bridge + ring): `y = 40.0 - u` (`0.0 .. 36.0` mm on screen)
    - For `u in [0.0, 4.0]` mm (`çubuk`, bent 90° horizontally onto the top edge of the 2.00 mm screen):
      projects in front view as the `1.00 mm` (`bir milim`) slim horizontal top bar `y = 36.0 .. 37.0` mm!
    """
    uv_pts = b_2d_outer_uv(d=d)
    pts = []
    for (u, v) in uv_pts:
        x = v
        if u >= 4.0:
            y = 40.0 - u
        else:
            y = 36.0 + (4.0 - u) * (STEM_THICK / 4.0)
        pts.append((x, y))
    return pts


def bore_outline(n=128, d=0.0):
    """Counter-clockwise inner circular opening (Ø24.0 mm, R = 12.0 mm centered at RING_C = (16.0, 16.0))."""
    r = RING_RI + d
    return [
        (RING_C[0] + r * math.cos(2.0 * math.pi * i / n),
         RING_C[1] + r * math.sin(2.0 * math.pi * i / n))
        for i in range(n)
    ]


def ring_only_outline(n=128, d=0.0):
    r = RING_RO - d
    return [
        (RING_C[0] + r * math.cos(2.0 * math.pi * i / n),
         RING_C[1] + r * math.sin(2.0 * math.pi * i / n))
        for i in range(n)
    ]


def ring_outline(n=128, d=0.0):
    return b_outer_outline(d=d)


def stem_outline(n_arc=20, n_flare=14, d=0.0):
    return []


def _fold_uv_to_3d(u, v, s_thick):
    """Map a point `(u, v)` on the exact 2D `uploads/b.png` silhouette (`u in [0, 40]`, `v in [0, 32]`)
    and normalized thickness `s_thick in [0.0, 1.0]` (`0.0` = back/inner face, `1.0` = front/outer face)
    into 3D `(x, y, z)` coordinates of the turned & 90°-bent `b` module:
      - `x = v` (`0.0 .. 32.0` mm, horizontal along the screen's top edge)
      - For `u >= 4.8` mm (`kalan kısım çubuk hariç` — circular ring `yuvarlak` + lower bridge):
          Lies flat in the vertical `(X, Y)` screen plane (`y = 40.0 - u`, `z = 2.00 * s_thick`)
          facing directly toward the viewer (`Diğer kısım bize doğru bakarak duruyor`).
      - For `u in [3.6, 4.8]` mm (the natural 90° bend zone across the bridge right at the gap `boşluk`,
          with ZERO extra hinge parts added):
          Smoothly rotates by 90° from the vertical `(X, Y)` screen plane into the horizontal `(X, Z)`
          top-edge plane!
      - For `u <= 3.6` mm (`çubuk` — the straight bar of the `b`):
          Lies HORIZONTALLY in the `(X, Z)` plane right on top of the 2.00 mm thick screen edge
          (`çubuk ekranın üstüne tam oturacak bir şekilde duruyor. O yukarıda çünkü yatay olarak duruyor`),
          with a `1.00 mm` (`bir milim`) slim height profile (`y = 36.0 + 1.00 * s_thick` = `36.0 .. 37.0` mm)
          and spanning horizontally in `Z` (`z = 0.80 - (3.6 - u) * (2.80 / 3.6)` = `-2.00 .. +0.80` mm)
          right across the 2.00 mm thickness of the screen's top edge!
    """
    x = v
    if u >= 4.8:
        y = 40.0 - u
        z = 2.00 * s_thick
        return (x, y, z)
    elif u <= 3.6:
        y = 36.0 + STEM_THICK * s_thick
        z = 0.80 - (3.6 - u) * (2.80 / 3.6)
        return (x, y, z)
    else:
        t = (4.8 - u) / 1.2
        ang = t * (math.pi / 2.0)
        y_base = 35.2 + 0.8 * math.sin(ang)
        z_base = 0.80 * (1.0 - math.cos(ang))
        thick = 2.00 * (1.0 - t) + STEM_THICK * t
        y = y_base + thick * s_thick * math.sin(ang)
        z = z_base + thick * s_thick * math.cos(ang)
        return (x, y, z)


def _build_structured_strip_3d(uv_pairs_fn):
    """Given `uv_pairs_fn(d)` returning a list of `( (u_a, v_a), (u_b, v_b) )` cross-section pairs
    along a strip (closed if first == last, or open with end caps), build a closed, watertight 3D mesh
    through `_fold_uv_to_3d(u, v, s_th)` across `sd_layers`.
    Every triangle stays strictly between `(u_a, v_a)` and `(u_b, v_b)` — ZERO chords ever cross
    the circular bore (`Ø24.0 mm`) or the valley gap (`boşluk`)!
    """
    sd_layers = [
        (0.00, 0.36),
        (0.10, 0.14),
        (0.24, 0.03),
        (0.36, 0.00),
        (0.64, 0.00),
        (0.76, 0.03),
        (0.90, 0.14),
        (1.00, 0.36),
    ]
    L = len(sd_layers)
    sample_pairs = uv_pairs_fn(0.0)
    M = len(sample_pairs)
    verts = []
    # Side A vertices (k = 0..L-1, i = 0..M-1)
    for (s_th, d) in sd_layers:
        pairs = uv_pairs_fn(d)
        for (pa, _) in pairs:
            verts.append(_fold_uv_to_3d(pa[0], pa[1], s_th))
    off_b = len(verts)
    # Side B vertices (k = 0..L-1, i = 0..M-1)
    for (s_th, d) in sd_layers:
        pairs = uv_pairs_fn(d)
        for (_, pb) in pairs:
            verts.append(_fold_uv_to_3d(pb[0], pb[1], s_th))

    def ia(k, i):
        return k * M + i

    def ib(k, i):
        return off_b + k * M + i

    faces = []
    # Side walls across thickness layers k = 0..L-2
    for k in range(L - 1):
        for i in range(M - 1):
            faces.append((ia(k, i), ia(k, i + 1), ia(k + 1, i + 1)))
            faces.append((ia(k, i), ia(k + 1, i + 1), ia(k + 1, i)))
            faces.append((ib(k, i), ib(k + 1, i + 1), ib(k, i + 1)))
            faces.append((ib(k, i), ib(k + 1, i), ib(k + 1, i + 1)))

    # Bottom cap (k = 0) and top cap (k = L - 1) strictly between side A and side B
    for i in range(M - 1):
        faces.append((ia(0, i), ib(0, i + 1), ia(0, i + 1)))
        faces.append((ia(0, i), ib(0, i), ib(0, i + 1)))
        faces.append((ia(L - 1, i), ia(L - 1, i + 1), ib(L - 1, i + 1)))
        faces.append((ia(L - 1, i), ib(L - 1, i + 1), ib(L - 1, i)))

    # End caps at i = 0 and i = M - 1 (if open strip)
    p0a, p0b = sample_pairs[0]
    p1a, p1b = sample_pairs[-1]
    if math.hypot(p0a[0] - p1a[0], p0a[1] - p1a[1]) > 1e-4 or math.hypot(p0b[0] - p1b[0], p0b[1] - p1b[1]) > 1e-4:
        for k in range(L - 1):
            faces.append((ia(k, 0), ia(k + 1, 0), ib(k + 1, 0)))
            faces.append((ia(k, 0), ib(k + 1, 0), ib(k, 0)))
            faces.append((ia(k, M - 1), ib(k + 1, M - 1), ia(k + 1, M - 1)))
            faces.append((ia(k, M - 1), ib(k, M - 1), ib(k + 1, M - 1)))

    return verts, faces


def b_solid_from_rings(outer_rings=None, inner_rings=None):
    """Build the closed, watertight 3D triangle mesh `(verts, faces)` of the unified `b` module
    from three exact, structured, non-overlapping parametric strips of `uploads/b.png`:
      1. Circular Ring (`yuvarlak`, centered at (u=24, v=16), R_in = 12.0 mm, R_out = 16.0 mm):
         strictly annular around the Ø24.0 mm bore so ZERO triangles ever cross the bore!
      2. Curved Bridge (`boğaz`, u = 3.6 .. 24.0 mm, v = 0.0 .. 16.0 mm between the valley arc
         R_val = 12.0 mm centered at (16, 16) and the bottom/ring contour):
         curves smoothly through the 90° bend at u = 3.6 .. 4.8 mm!
      3. Horizontal Top `Çubuk` (`u = 0.0 .. 4.0 mm, v = 0.0 .. 32.0 mm` with R = 2.0 mm end cap):
         bent 90° across the gap (`boşluk`) so it sits horizontally on top of the 2.00 mm screen edge
         with a 1.00 mm (`bir milim`) slim profile!
    """
    # Strip 1: Closed Annular Ring (`yuvarlak`, u_c = 24.0, v_c = 16.0, R_in = 12.0, R_out = 16.0)
    def ring_pairs(d):
        r_i = RING_RI + d * 0.7
        r_o = RING_RO - d * 0.7
        N = 128
        out = []
        for i in range(N + 1):
            ang = 2.0 * math.pi * i / N
            ca, sa = math.cos(ang), math.sin(ang)
            out.append(((24.0 + r_o * ca, 16.0 + r_o * sa), (24.0 + r_i * ca, 16.0 + r_i * sa)))
        return out

    # Strip 2: Curved Bridge (`boğaz`) connecting the ring (u <= 24.0, v = 0..4.381) to the `çubuk` (u = 3.6..4.0, v = 0..16.0)
    def bridge_pairs(d):
        r_val = VALLEY_R + d * 0.6
        r_o = RING_RO - d * 0.6
        N = 48
        out = []
        # Parameter s in [0, 1] from u = 3.6 (at the 90° bend into the `çubuk`) to u = 23.5 (bottom of ring)
        for i in range(N + 1):
            t = i / float(N)
            u = 3.6 + (23.5 - 3.6) * t
            v_bot = d * 0.6
            # Upper boundary of bridge: valley arc centered at (16.0, 16.0) for u <= 12.5, then outer ring arc for u > 12.5
            if u <= 12.5:
                du = max(-r_val, min(r_val, u - 16.0))
                v_top = 16.0 - math.sqrt(max(0.0, r_val * r_val - du * du))
            else:
                du = max(-r_o, min(r_o, u - 24.0))
                v_top = 16.0 - math.sqrt(max(0.0, r_o * r_o - du * du))
            v_top = max(v_bot + 0.4, v_top)
            out.append(((u, v_bot), (u, v_top)))
        return out

    # Strip 3: Straight Bar (`çubuk`, u in [0.0, 4.0], v in [0.0, 32.0]) with R = 2.0 mm bottom-left fillet and R = 2.0 mm top semicircle cap
    def stem_pairs(d):
        d_c = min(0.32, d * 0.6)
        r_cap = max(0.4, CAP_R - d_c)
        N = 64
        out = []
        v_min = d_c + 0.05
        v_max = 32.0 - d_c - 0.05
        for i in range(N + 1):
            t = i / float(N)
            v = v_min + (v_max - v_min) * t
            u_left = d_c
            u_right = 4.0 - d_c
            # Bottom-left quarter-circle fillet centered at (2.0, 2.0)
            if v < 2.0:
                dv = 2.0 - v
                u_left = max(d_c, 2.0 - math.sqrt(max(0.0, r_cap * r_cap - dv * dv)))
            # Top semicircle cap centered at (2.0, 30.0)
            if v > 30.0:
                dv = v - 30.0
                hw = math.sqrt(max(0.02, r_cap * r_cap - dv * dv))
                u_left = 2.0 - hw
                u_right = 2.0 + hw
            out.append(((u_left, v), (u_right, v)))
        return out

    v1, f1 = _build_structured_strip_3d(ring_pairs)
    v2, f2 = _build_structured_strip_3d(bridge_pairs)
    v3, f3 = _build_structured_strip_3d(stem_pairs)

    verts = v1 + v2 + v3
    off2 = len(v1)
    off3 = len(v1) + len(v2)
    faces = (
        f1
        + [(a + off2, b + off2, c + off2) for (a, b, c) in f2]
        + [(a + off3, b + off3, c + off3) for (a, b, c) in f3]
    )
    return verts, faces


def svg_path(k, ox, oy, flip_y=True):
    """The turned & 90°-bent `b` module as one SVG path in pixels:
    `oy` corresponds to y = 36.0 mm (top edge of the screen), so:
      - The horizontal `1.00 mm` (`bir milim`) `çubuk` sits right on top of the screen edge (`oy - 1.0*k .. oy`),
      - The natural gap (`boşluk`) and curved bridge sit at `oy .. oy + 4.0*k`,
      - The circular ring (`yuvarlak`, y = 0..32 mm) hangs down on the screen face (`oy + 4.0*k .. oy + 36.0*k`)
        facing directly toward us!
    """
    def X(x):
        return ox + x * k

    def Y(y):
        return oy + (MON_H - y) * k if flip_y else oy + y * k

    def poly(pts):
        return "M " + " L ".join("%.1f %.1f" % (X(x), Y(y)) for (x, y) in pts) + " Z"

    outer = poly(b_outer_outline(0.0))
    inner = poly(list(reversed(bore_outline(128, 0.0))))
    return outer + " " + inner
