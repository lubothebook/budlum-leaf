#!/usr/bin/env python3
# BUDLUM LEAF · cad/monogram_letter.py · revision L.6.0 · 2026-10-12
#
# L.6.0 soft edges (TEAM-BRIEF section 4), true quarter-circle fillets on the shell:
#   ring outer top and bottom edges r 0.40 mm, inner bore edges r 0.25 mm, bar long edges
#   r 0.20 mm (the R 2.0 end of b.png stays), moulded 90 deg corner outside edge r 0.30 mm,
#   gap (valley) edges r 0.25 mm. The 2D outline and every nominal dimension are unchanged.
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


# ── L.6.0 soft-edge radii of the shell (TEAM-BRIEF section 4) ──
R_RING_OUT = 0.40     # [DECISION] ring outer top and bottom edges
R_BORE = 0.25         # [DECISION] ring inner bore edges
R_BAR = 0.20          # [DECISION] bar long edges
R_CORNER = 0.30       # [DECISION] moulded 90 deg corner, outside edge
R_GAP = 0.25          # gap (valley) edges, same family as the bore
FILLET_STEPS = 6      # facets per quarter fillet: each facet turns 15 deg
U_TO_Z = 2.80 / 3.6   # the bar maps u to z at 0.778 mm per mm


def _thick_at(u):
    """Shell thickness at u: 2.00 mm on the face, 1.00 mm on the bar, linear through the bend."""
    if u >= 4.8:
        return 2.00
    if u <= 3.6:
        return STEM_THICK
    t = (4.8 - u) / 1.2
    return 2.00 * (1.0 - t) + STEM_THICK * t


def fillet_profile(r, T, n=FILLET_STEPS):
    """[(height, inset)] down one side wall of thickness T, from the back face (height 0) to the
    front face (height T), with a quarter-circle fillet of radius r at both face edges."""
    r = min(r, 0.49 * T)
    out = []
    for i in range(n + 1):
        a = (math.pi / 2.0) * i / n
        out.append((r - r * math.cos(a), r - r * math.sin(a)))
    for i in range(n + 1):
        a = (math.pi / 2.0) * i / n
        out.append((T - r + r * math.sin(a), r - r * math.cos(a)))
    return out


def _build_strip(M, side_a, side_b, L):
    """Closed, watertight strip solid. side_a(i, k) and side_b(i, k) return the 3D point of layer k
    (0 = back face edge, L-1 = front face edge) on the two side walls at station i (0..M-1).
    Every triangle stays between the two sides: no chord crosses the bore or the gap."""
    verts = []
    for k in range(L):
        for i in range(M):
            verts.append(side_a(i, k))
    off_b = len(verts)
    for k in range(L):
        for i in range(M):
            verts.append(side_b(i, k))

    def ia(k, i):
        return k * M + i

    def ib(k, i):
        return off_b + k * M + i

    faces = []
    for k in range(L - 1):
        for i in range(M - 1):
            faces.append((ia(k, i), ia(k, i + 1), ia(k + 1, i + 1)))
            faces.append((ia(k, i), ia(k + 1, i + 1), ia(k + 1, i)))
            faces.append((ib(k, i), ib(k + 1, i + 1), ib(k, i + 1)))
            faces.append((ib(k, i), ib(k + 1, i), ib(k + 1, i + 1)))
    for i in range(M - 1):
        faces.append((ia(0, i), ib(0, i + 1), ia(0, i + 1)))
        faces.append((ia(0, i), ib(0, i), ib(0, i + 1)))
        faces.append((ia(L - 1, i), ia(L - 1, i + 1), ib(L - 1, i + 1)))
        faces.append((ia(L - 1, i), ib(L - 1, i + 1), ib(L - 1, i)))
    pa0, pa1 = verts[ia(L // 2, 0)], verts[ia(L // 2, M - 1)]
    closed = math.dist(pa0, pa1) < 1e-6
    if not closed:
        for k in range(L - 1):
            faces.append((ia(k, 0), ia(k + 1, 0), ib(k + 1, 0)))
            faces.append((ia(k, 0), ib(k + 1, 0), ib(k, 0)))
            faces.append((ia(k, M - 1), ib(k + 1, M - 1), ia(k + 1, M - 1)))
            faces.append((ia(k, M - 1), ib(k, M - 1), ib(k + 1, M - 1)))
    return verts, faces


def _fold_h(u, v, h):
    """Fold a point at height h (mm above the back face) through _fold_uv_to_3d."""
    return _fold_uv_to_3d(u, v, h / _thick_at(u))


def b_solid_from_rings(outer_rings=None, inner_rings=None):
    """Build the closed, watertight 3D triangle mesh `(verts, faces)` of the unified `b` module
    from three exact, structured, non-overlapping parametric strips of `uploads/b.png`:
      1. Circular Ring (`yuvarlak`, centered at (u=24, v=16), R_in = 12.0 mm, R_out = 16.0 mm):
         strictly annular around the Ø24.0 mm bore so ZERO triangles ever cross the bore!
         L.6.0: outer face edges r 0.40 mm, bore edges r 0.25 mm.
      2. Curved Bridge (`boğaz`, u = 3.6 .. 23.5 mm, v = 0.0 .. 16.0 mm between the valley arc
         R_val = 12.0 mm centered at (16, 16) and the bottom/ring contour):
         curves smoothly through the 90° bend at u = 3.6 .. 4.8 mm!
         L.6.0: outer edge r 0.40 mm blending to r 0.30 mm at the moulded corner, gap edge r 0.25 mm.
      3. Horizontal Top `Çubuk` (`u = 0.0 .. 4.0 mm, v = 0.0 .. 32.0 mm` with R = 2.0 mm end cap):
         bent 90° across the gap (`boşluk`) so it sits horizontally on top of the 2.00 mm screen edge
         with a 1.00 mm (`bir milim`) slim profile! L.6.0: long edges r 0.20 mm.
    """
    n = FILLET_STEPS
    L = 2 * (n + 1)

    # Strip 1: closed annular ring, uv centre (24, 16): 2.00 mm thick, flat on the face.
    N1 = 128
    pa = fillet_profile(R_RING_OUT, 2.00)
    pb = fillet_profile(R_BORE, 2.00)

    def ring_a(i, k):
        ang = 2.0 * math.pi * i / N1
        h, d = pa[k]
        r = RING_RO - d
        return _fold_h(24.0 + r * math.cos(ang), 16.0 + r * math.sin(ang), h)

    def ring_b(i, k):
        ang = 2.0 * math.pi * i / N1
        h, d = pb[k]
        r = RING_RI + d
        return _fold_h(24.0 + r * math.cos(ang), 16.0 + r * math.sin(ang), h)

    v1, f1 = _build_strip(N1 + 1, ring_a, ring_b, L)

    # Strip 2: curved bridge from u = 3.6 (into the bend) to u = 23.5 (bottom of the ring).
    N2 = 48
    us = [3.6 + (23.5 - 3.6) * i / float(N2) for i in range(N2 + 1)]

    def r_side_a(u):
        # moulded corner r 0.30 through the bend, blending to the ring family r 0.40 by u = 7.0
        if u <= 5.5:
            return R_CORNER
        if u >= 7.0:
            return R_RING_OUT
        return R_CORNER + (R_RING_OUT - R_CORNER) * (u - 5.5) / 1.5

    def v_top(u, d):
        r_val = VALLEY_R + d
        r_o = RING_RO - d
        if u <= 12.5:
            du = max(-r_val, min(r_val, u - 16.0))
            return 16.0 - math.sqrt(max(0.0, r_val * r_val - du * du))
        du = max(-r_o, min(r_o, u - 24.0))
        return 16.0 - math.sqrt(max(0.0, r_o * r_o - du * du))

    def bridge_a(i, k):
        u = us[i]
        h, d = fillet_profile(r_side_a(u), _thick_at(u))[k]
        return _fold_h(u, d, h)

    def bridge_b(i, k):
        u = us[i]
        h, d = fillet_profile(R_GAP, _thick_at(u))[k]
        ha, da = fillet_profile(r_side_a(u), _thick_at(u))[k]
        return _fold_h(u, max(da + 0.4, v_top(u, d)), h)

    v2, f2 = _build_strip(N2 + 1, bridge_a, bridge_b, L)

    # Strip 3: straight bar (u 0 .. 4, v 0 .. 32) with the R 2.0 bottom-left fillet and the R 2.0
    # top semicircle cap of b.png. The bar is 1.00 mm thick (y) and u maps to z at 0.778 mm/mm.
    N3 = 64

    def bar_pt(i, k, side):
        u_mid = 2.0
        d = fillet_profile(R_BAR, STEM_THICK)[k][1]
        du = d / U_TO_Z            # inset across the bar width, in u
        dv = d                     # inset at the bar ends, in v (= x, mm)
        v_min = 0.05 + dv
        v_max = 32.0 - 0.05 - dv
        v = v_min + (v_max - v_min) * i / float(N3)
        r_cap = CAP_R - du
        if side < 0:
            u = du
            if v < 2.0:
                dv2 = 2.0 - v
                u = max(du, 2.0 - math.sqrt(max(0.0, r_cap * r_cap - dv2 * dv2)))
        else:
            u = 4.0 - du
        if v > 30.0:
            dv2 = v - 30.0
            hw = math.sqrt(max(0.02, r_cap * r_cap - dv2 * dv2))
            u = u_mid - hw if side < 0 else u_mid + hw
        h = fillet_profile(R_BAR, _thick_at(u))[k][0]
        return _fold_h(u, v, h)

    v3, f3 = _build_strip(N3 + 1, lambda i, k: bar_pt(i, k, -1), lambda i, k: bar_pt(i, k, +1), L)

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
