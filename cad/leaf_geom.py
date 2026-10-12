#!/usr/bin/env python3
# BUDLUM LEAF · cad/leaf_geom.py · revision L.6.0 · 2026-10-12
#
# L.6.0 soft edges (TEAM-BRIEF section 4): the body perimeter face edges carry a true r 0.65 mm
# quarter-circle fillet (stack() profile fixed: the top roll was inverted and left the front edge
# sharp), the plan corners stay R 6.35 mm, the + seam sides keep a 0.03 mm edge break only.
#
# Shared parametric geometry for the Budlum Leaf family:
#   - 4-Quadrant Plus (+) Seamless Snap-Together Polycarbonate Screen-Battery Tiles:
#       4 x (40.0 x 80.0 x 2.00 mm) = 80.0 x 160.0 x 2.00 mm body (68.0 g = 4 x 17.0 g)
#   - Outer screen corner radius R = 6.35 mm (`63.5 px` on `800 x 1600 px`, IoU = 0.999987
#       against the user's `uploads/Group 911.png` screen design)
#   - Internal Bi-Directional Puzzle-Like Interlocking (`yapboz parçaları gibi iç içe girmiş
#       girdili-çıktılı kilit`) inside the 2.00 mm screen core (z = -0.45 .. +0.45 mm) so the
#       4 tiles bend together at R = 25.5 mm without separating, while the outer polycarbonate
#       surfaces meet at a < 15 µm index-matched (n = 1.585) zero-scratch optical seam
#   - Turned & 90°-Bent-at-Gap (`boşluk`) `b` Camera, Zero-CPU & USB-C Module (`uploads/b.png`
#       1:1 silhouette, 1.00 mm horizontal top `çubuk` on screen edge + front-facing circular ring)

import math
import os
import struct


def corner_radius(short_side):
    """Exact screen corner radius matching `uploads/Group 911.png`:
    6.35 mm (`63.5 px` at 10 px/mm, IoU = 0.999987) for the 80 x 160 mm phone body.
    """
    if abs(short_side - 80.0) < 1e-3:
        return 6.35
    if abs(short_side - 40.0) < 1e-3:
        return 6.35
    return round(max(3.2, min(14.0, short_side * (6.35 / 80.0))), 2)


corner_cut = corner_radius


BODY_EDGE_R = 0.65     # [DECISION] TEAM-BRIEF 4: body outer perimeter, front and back face edges
SEAM_EDGE_BREAK = 0.03 # [DECISION] TEAM-BRIEF 4: interior tile cap top edges, kerf unchanged


def edge_fillet(thickness):
    """Soft tactile edge fillet of the body face edges: r 0.65 mm (TEAM-BRIEF 4), never more than
    0.49 of the thickness so a flat side land always remains."""
    return round(min(BODY_EDGE_R, thickness * 0.49), 2)


def _arc(cx, cy, r, a0, a1, n):
    return [
        (cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n))
        for i in range(n + 1)
    ]


def rounded_rect(w, h, R, d=0.0, n=16):
    """Counter-clockwise perimeter of a w x h rounded rectangle inset by d."""
    r = max(R - d, 0.05)
    hw, hh = w / 2.0 - d, h / 2.0 - d
    cx, cy = hw - r, hh - r
    corners = [
        (+cx, +cy, 0.0),
        (-cx, +cy, math.pi / 2.0),
        (-cx, -cy, math.pi),
        (+cx, -cy, 3.0 * math.pi / 2.0),
    ]
    pts = []
    for (x0, y0, a0) in corners:
        seg = _arc(x0, y0, r, a0, a0 + math.pi / 2.0, n)
        pts += seg[:-1] if pts else seg
    return pts


outline = rounded_rect


def quadrant_outline(qx, qy, qw=40.0, qh=80.0, r_outer=6.35, r_inner=0.18, d=0.0, n=12, d_seam=None):
    """Counter-clockwise outer perimeter of one quadrant tile (qw x qh = 40 x 80 mm)
    centered at its local origin (0, 0):
      - The ONE outer phone corner `(qx, qy)` (`qx, qy in {-1, +1}`) uses the user's exact
        `Group 911.png` screen radius `r_outer = 6.35 mm` (`IoU = 0.999987`),
      - The THREE internal seams meeting along the `+` cross (`x = 0` and `y = 0`) use an
        ultra-tight optical half-lap radius `r_inner = 0.18 mm` so all 4 tiles mate with zero
        gap (`< 15 µm` index-matched `n = 1.585` fluorosilicone boundary).
    L.6.0: `d` insets the two outer body sides (the r 0.65 face-edge fillet), `d_seam` insets the
    two + seam sides (the 0.03 mm edge break); `d_seam = None` insets every side by `d`.
    """
    if d_seam is None:
        d_seam = d
    xr = qw / 2.0 - (d if qx == +1 else d_seam)
    xl = -qw / 2.0 + (d if qx == -1 else d_seam)
    yt = qh / 2.0 - (d if qy == +1 else d_seam)
    yb = -qh / 2.0 + (d if qy == -1 else d_seam)
    corner_specs = [
        (+1, +1, 0.0),
        (-1, +1, 90.0),
        (-1, -1, 180.0),
        (+1, -1, 270.0),
    ]
    raw_corners = []
    for (sx, sy, a0) in corner_specs:
        outer = (sx == qx and sy == qy)
        r_c = max((r_outer - d) if outer else (r_inner - d_seam), 0.04)
        cx = (xr if sx > 0 else xl) - sx * r_c
        cy = (yt if sy > 0 else yb) - sy * r_c
        seg = _arc(cx, cy, r_c, math.radians(a0), math.radians(a0 + 90.0), n)
        raw_corners.append(seg)
    pts = []
    edge_steps = 16
    for idx in range(4):
        seg = raw_corners[idx]
        nxt_start = raw_corners[(idx + 1) % 4][0]
        pts += seg[:-1]
        p0 = seg[-1]
        for k in range(edge_steps):
            u = k / float(edge_steps)
            pts.append((p0[0] + (nxt_start[0] - p0[0]) * u, p0[1] + (nxt_start[1] - p0[1]) * u))
    return pts


def _puzzle_lobe_1d(s0, s1, n_lobes, sign_dir, amp=2.2):
    """Generate a smooth complementary dovetail puzzle wave (`yapboz girdili-çıktılı kilit`)
    along coordinate `s` from `s0` to `s1` with `n_lobes` full male+female pairs:
    each lobe has a neck-to-head dovetail widening (`omega = sin(theta) + 0.28*sin(3*theta)`)
    so adjacent tiles lock in both tension and shear while remaining installable from +Z or -Z!
    """
    pts = []
    margin = 4.5
    s_start = s0 + (margin if s1 > s0 else -margin)
    s_end = s1 - (margin if s1 > s0 else -margin)
    pts.append((s0, 0.0))
    pts.append((s_start, 0.0))
    steps = n_lobes * 28
    for i in range(steps + 1):
        u = i / float(steps)
        s = s_start + (s_end - s_start) * u
        theta = u * n_lobes * 2.0 * math.pi
        # Dovetail-shaped puzzle profile: wider rounded head, narrower neck
        off = sign_dir * amp * (math.sin(theta) + 0.28 * math.sin(3.0 * theta)) / 1.12
        pts.append((s, off))
    pts.append((s1, 0.0))
    return pts


def quadrant_puzzle_outline(qx, qy, qw=40.0, qh=80.0, r_outer=6.35, inset=0.55):
    """Counter-clockwise perimeter of the internal bi-directional puzzle-interlocking structural core
    (`z = -0.45 .. +0.45 mm`, `t = 0.90 mm` inside the `2.00 mm` screen) of Quadrant `(qx, qy)`.
    """
    p_out, _ = quadrant_puzzle_pair(qx, qy, qw=qw, qh=qh, r_outer=r_outer, inset=inset)
    return p_out


def quadrant_puzzle_pair(qx, qy, qw=40.0, qh=80.0, r_outer=6.35, inset=0.45, wall=2.10):
    """Return `(puz_outer, puz_inner)` with 1-to-1 matched perimeter vertices so every triangle
    of the puzzle-interlock frame stays strictly within the `wall` mm perimeter rim and NEVER
    crosses the interior of the quadrant!
    """
    hw = qw / 2.0 - inset
    hh = qh / 2.0 - inset
    hw_in = qw / 2.0 - wall
    hh_in = qh / 2.0 - wall
    r_in = max(0.8, r_outer - (wall - inset))

    p_out = []
    p_in = []

    def clamp(val, lo, hi):
        return max(lo, min(hi, val))

    # 1. Right edge (x near +hw, y from -hh to +hh)
    if qx == -1:
        for (sy, dx) in _puzzle_lobe_1d(-hh + 2.2, +hh - 2.2, n_lobes=4, sign_dir=+1.0, amp=1.95):
            p_out.append((hw + inset + dx, sy))
            p_in.append((hw_in, clamp(sy, -hh_in, +hh_in)))
    else:
        y0 = (-hh + r_outer) if qy == -1 else (-hh + 0.8)
        y1 = (+hh - r_outer) if qy == +1 else (+hh - 0.8)
        for k in range(17):
            t = k / 16.0
            yy = y0 + (y1 - y0) * t
            p_out.append((+hw, yy))
            p_in.append((+hw_in, clamp(yy, -hh_in, +hh_in)))
        if qy == +1:
            o_arc = _arc(+hw - r_outer, +hh - r_outer, r_outer, 0.0, math.pi / 2.0, 10)[1:]
            i_arc = _arc(+hw_in - r_in, +hh_in - r_in, r_in, 0.0, math.pi / 2.0, 10)[1:]
            p_out += o_arc
            p_in += i_arc

    # 2. Top edge (y near +hh, x from +hw to -hw)
    if qy == -1:
        for (sx_c, dy) in _puzzle_lobe_1d(+hw - 2.2, -hw + 2.2, n_lobes=2, sign_dir=-1.0, amp=1.95):
            p_out.append((sx_c, hh + inset + dy))
            p_in.append((clamp(sx_c, -hw_in, +hw_in), +hh_in))
    else:
        x0 = (+hw - r_outer) if qx == +1 else (+hw - 0.8)
        x1 = (-hw + r_outer) if qx == -1 else (-hw + 0.8)
        for k in range(13):
            t = k / 12.0
            xx = x0 + (x1 - x0) * t
            p_out.append((xx, +hh))
            p_in.append((clamp(xx, -hw_in, +hw_in), +hh_in))
        if qx == -1:
            o_arc = _arc(-hw + r_outer, +hh - r_outer, r_outer, math.pi / 2.0, math.pi, 10)[1:]
            i_arc = _arc(-hw_in + r_in, +hh_in - r_in, r_in, math.pi / 2.0, math.pi, 10)[1:]
            p_out += o_arc
            p_in += i_arc

    # 3. Left edge (x near -hw, y from +hh to -hh)
    if qx == +1:
        for (sy, dx) in reversed(_puzzle_lobe_1d(-hh + 2.2, +hh - 2.2, n_lobes=4, sign_dir=+1.0, amp=1.95)):
            p_out.append((-hw - inset + dx, sy))
            p_in.append((-hw_in, clamp(sy, -hh_in, +hh_in)))
    else:
        y0 = (+hh - r_outer) if qy == +1 else (+hh - 0.8)
        y1 = (-hh + r_outer) if qy == -1 else (-hh + 0.8)
        for k in range(17):
            t = k / 16.0
            yy = y0 + (y1 - y0) * t
            p_out.append((-hw, yy))
            p_in.append((-hw_in, clamp(yy, -hh_in, +hh_in)))
        if qy == -1:
            o_arc = _arc(-hw + r_outer, -hh + r_outer, r_outer, math.pi, 3.0 * math.pi / 2.0, 10)[1:]
            i_arc = _arc(-hw_in + r_in, -hh_in + r_in, r_in, math.pi, 3.0 * math.pi / 2.0, 10)[1:]
            p_out += o_arc
            p_in += i_arc

    # 4. Bottom edge (y near -hh, x from -hw to +hw)
    if qy == +1:
        for (sx_c, dy) in reversed(_puzzle_lobe_1d(+hw - 2.2, -hw + 2.2, n_lobes=2, sign_dir=-1.0, amp=1.95)):
            p_out.append((sx_c, -hh - inset + dy))
            p_in.append((clamp(sx_c, -hw_in, +hw_in), -hh_in))
    else:
        x0 = (-hw + r_outer) if qx == -1 else (-hw + 0.8)
        x1 = (+hw - r_outer) if qx == +1 else (+hw - 0.8)
        for k in range(13):
            t = k / 12.0
            xx = x0 + (x1 - x0) * t
            p_out.append((xx, -hh))
            p_in.append((clamp(xx, -hw_in, +hw_in), -hh_in))
        if qx == +1:
            o_arc = _arc(+hw - r_outer, -hh + r_outer, r_outer, 3.0 * math.pi / 2.0, 2.0 * math.pi, 10)[1:]
            i_arc = _arc(+hw_in - r_in, -hh_in + r_in, r_in, 3.0 * math.pi / 2.0, 2.0 * math.pi, 10)[1:]
            p_out += o_arc
            p_in += i_arc

    return p_out, p_in


def circle(r, n, d=0.0, phase=0.0):
    return [
        (
            (r - d) * math.cos(phase + 2.0 * math.pi * i / n),
            (r - d) * math.sin(phase + 2.0 * math.pi * i / n),
        )
        for i in range(n)
    ]


def mesh_from_rings(rings, inner_rings=None):
    """Build a closed triangle mesh from [(z, [pts]), ...] with optional inner bore rings."""
    n = len(rings[0][1])
    verts, faces = [], []
    for (z, pts) in rings:
        verts += [(x, y, z) for (x, y) in pts]
    if inner_rings:
        off_in = len(verts)
        for (z, pts) in inner_rings:
            verts += [(x, y, z) for (x, y) in pts]
    L = len(rings)

    def o(layer, i):
        return (layer % L) * n + (i % n)

    def q(layer, i):
        return off_in + (layer % L) * n + (i % n)

    for k in range(L - 1):
        for i in range(n):
            faces.append((o(k, i), o(k, i + 1), o(k + 1, i + 1)))
            faces.append((o(k, i), o(k + 1, i + 1), o(k + 1, i)))
            if inner_rings:
                faces.append((q(k, i), q(k + 1, i + 1), q(k, i + 1)))
                faces.append((q(k, i), q(k + 1, i), q(k + 1, i + 1)))
    if inner_rings:
        for i in range(n):
            faces.append((o(L - 1, i), o(L - 1, i + 1), q(L - 1, i + 1)))
            faces.append((o(L - 1, i), q(L - 1, i + 1), q(L - 1, i)))
            faces.append((o(0, i), q(0, i + 1), o(0, i + 1)))
            faces.append((o(0, i), q(0, i), q(0, i + 1)))
    else:
        zmin, zmax = rings[0][0], rings[-1][0]
        for (z, top) in ((zmin, False), (zmax, True)):
            k = L - 1 if top else 0
            cx = sum(verts[o(k, i)][0] for i in range(n)) / n
            cy = sum(verts[o(k, i)][1] for i in range(n)) / n
            ci = len(verts)
            verts.append((cx, cy, z))
            for i in range(n):
                if top:
                    faces.append((ci, o(k, i), o(k, i + 1)))
                else:
                    faces.append((ci, o(k, i + 1), o(k, i)))
    vol = 0.0
    for (a, b, cc) in faces:
        p, r, s = verts[a], verts[b], verts[cc]
        vol += (
            p[0] * (r[1] * s[2] - r[2] * s[1])
            - p[1] * (r[0] * s[2] - r[2] * s[0])
            + p[2] * (r[0] * s[1] - r[1] * s[0])
        ) / 6.0
    if vol < 0:
        faces = [(a, cc, b) for (a, b, cc) in faces]
    return verts, faces


def fillet_inset(z, z0, z1, r):
    """Inset of a quarter-circle edge fillet of radius r at height z on a side wall from z0 to z1."""
    if r <= 0.0:
        return 0.0
    e = None
    if z < z0 + r:
        e = (z0 + r) - z
    elif z > z1 - r:
        e = z - (z1 - r)
    if e is None:
        return 0.0
    e = min(e, r)
    return r - math.sqrt(max(r * r - e * e, 0.0))


def fillet_heights(z0, z1, r, steps):
    """Heights of a side wall that carries a quarter-circle fillet of radius r at both face edges,
    sampled at equal angle steps (steps segments per fillet, so each facet turns 90/steps deg)."""
    zs = []
    for i in range(steps + 1):
        a = (math.pi / 2.0) * i / steps
        zs.append(z0 + r - r * math.cos(a))
    for i in range(steps + 1):
        a = (math.pi / 2.0) * i / steps
        zs.append(z1 - r + r * math.sin(a))
    if z1 - z0 <= 2.0 * r + 1e-9:
        zs = zs[: steps + 1] + zs[steps + 2:]
    return zs


def stack(pts_fn, z0, z1, edge_round, steps=8):
    """A prism whose top and bottom perimeter edges are softened by a true quarter-circle fillet of
    radius edge_round (equal-angle facets). L.6.0: the top roll used to run inverted (inset r just
    under the face, 0 at the face) and left the face edge sharp; it is now the mirror of the bottom."""
    r = min(edge_round, (z1 - z0) / 2.0)
    return [(z, pts_fn(fillet_inset(z, z0, z1, r))) for z in fillet_heights(z0, z1, r, steps)]


def stack_multi(pts_fn, z0, z1, radii, steps=8):
    """Like stack(), but pts_fn takes one inset per radius in `radii`, so different sides of the
    same outline carry different fillets (body r 0.65 outside, 0.03 break on the seam sides).
    The heights are the union of the fillet heights of every radius."""
    zs = set()
    for r in radii:
        r = min(r, (z1 - z0) / 2.0)
        for z in fillet_heights(z0, z1, r, steps):
            zs.add(round(z, 9))
    zs = sorted(zs)
    out = []
    for z in zs:
        ds = [fillet_inset(z, z0, z1, min(r, (z1 - z0) / 2.0)) for r in radii]
        out.append((z, pts_fn(*ds)))
    return out


def write_stl(path, verts, faces, name="budlum"):
    with open(path, "wb") as f:
        f.write(name.encode()[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(faces)))
        for (a, b, c) in faces:
            p, q, r = verts[a], verts[b], verts[c]
            ux, uy, uz = q[0] - p[0], q[1] - p[1], q[2] - p[2]
            vx, vy, vz = r[0] - p[0], r[1] - p[1], r[2] - p[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<3f", nx / ln, ny / ln, nz / ln))
            for pt in (p, q, r):
                f.write(struct.pack("<3f", pt[0], pt[1], pt[2]))
            f.write(struct.pack("<H", 0))
    return len(faces)


def plan_svg(path, w, h, th, title):
    """Write an annotated upright plan SVG and PNG of the 4-Quadrant (+) Puzzle-Interlocking
    Polycarbonate Screen-Battery Body (`R = 6.35 mm`, `2.00 mm` thickness), Universal Qi2 Wireless
    Charging Coils, and Turned & 90°-Bent-at-Gap (`boşluk`) `b` Module (`1.0 mm` horizontal top `çubuk`
    on screen edge + circular ring facing us on the screen).
    """
    from monogram_letter import b_outer_outline, RING_C, RING_RI, MON_H
    from PIL import Image, ImageDraw, ImageFont

    R = corner_radius(min(w, h))
    pts = rounded_rect(w, h, R, 0.0, 20)
    m, W = 50.0, 900.0
    s = min((W - 2 * m) / max(w, h + 30.0), 3.4)
    top_pad = int(18.0 * s + 70)
    H = int(h * s + top_pad + 160)
    X = lambda x: W / 2.0 + x * s
    Y = lambda y: top_pad + (h / 2.0 - y) * s
    d_outer = "M " + " L ".join("%.2f %.2f" % (X(x), Y(y)) for (x, y) in pts) + " Z"
    bezel = 1.40
    scr_pts = rounded_rect(w - 2 * bezel, h - 2 * bezel, max(R - bezel, 1.2), 0.0, 20)
    d_scr = "M " + " L ".join("%.2f %.2f" % (X(x), Y(y)) for (x, y) in scr_pts) + " Z"

    # Puzzle-interlocking (+) wave path along x = 0 and y = 0
    puz_v = [(dx, sy) for (sy, dx) in _puzzle_lobe_1d(-h / 2.0 + 4.0, h / 2.0 - 4.0, n_lobes=8, sign_dir=1.0, amp=2.0)]
    puz_h = [(sx_c, dy) for (sx_c, dy) in _puzzle_lobe_1d(-w / 2.0 + 4.0, w / 2.0 - 4.0, n_lobes=4, sign_dir=1.0, amp=2.0)]
    d_puz_v = "M " + " L ".join("%.2f %.2f" % (X(x), Y(y)) for (x, y) in puz_v)
    d_puz_h = "M " + " L ".join("%.2f %.2f" % (X(x), Y(y)) for (x, y) in puz_h)

    # Turned & 90°-bent `b` Module:
    # Horizontal 1.00 mm `çubuk` sits right on top of the screen edge (y_phone = h/2 .. h/2 + 1.0 mm),
    # while the natural gap (`boşluk`) and Ø32/Ø24 mm circular ring (`yuvarlak`) hang down on the screen face!
    x0_b = -w / 2.0
    y0_b = h / 2.0 - MON_H
    b_outer = [(x0_b + x, y0_b + y) for (x, y) in b_outer_outline(0.0)]
    d_b_outer = "M " + " L ".join("%.2f %.2f" % (X(x), Y(y)) for (x, y) in b_outer) + " Z"
    rcx, rcy = X(x0_b + RING_C[0]), Y(y0_b + RING_C[1])
    r_bore = RING_RI * s

    sub = "4-Parçalı (+) Yapboz Ekran-Pil (%.2f mm, R=%.2f mm, Katı-Hal Pil, Qi2) · Yatay 1 mm Çubuklu B" % (th, R)
    o = [
        "<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>" % (W, H, W, H),
        "<rect width='%d' height='%d' fill='#0d1117'/>" % (W, H),
        "<text x='40' y='32' fill='#eaf1f8' font-family='DejaVu Sans,Helvetica,Arial' font-size='17' font-weight='bold'>%s</text>" % title,
        "<text x='40' y='54' fill='#93a68c' font-family='DejaVu Sans,Helvetica,Arial' font-size='12.5'>%s</text>" % sub,
        "<path d='%s' fill='#bad6ec' fill-opacity='0.35' stroke='#7ec2ee' stroke-width='2.0'/>" % d_outer,
        "<path d='%s' fill='#15324c' fill-opacity='0.60' stroke='#62b2e6' stroke-width='1.2'/>" % d_scr,
        # Internal puzzle-interlock (yapboz girdili-çıktılı) + optical seam
        "<path d='%s' fill='none' stroke='#5ce0b8' stroke-width='1.5'/>" % d_puz_v,
        "<path d='%s' fill='none' stroke='#5ce0b8' stroke-width='1.5'/>" % d_puz_h,
        "<line x1='%.2f' y1='%.2f' x2='%.2f' y2='%.2f' stroke='#7ee0c6' stroke-width='1.0' stroke-dasharray='4,3'/>" % (X(0), Y(h/2), X(0), Y(-h/2)),
        "<line x1='%.2f' y1='%.2f' x2='%.2f' y2='%.2f' stroke='#7ee0c6' stroke-width='1.0' stroke-dasharray='4,3'/>" % (X(-w/2), Y(0), X(w/2), Y(0)),
        # Central Ø54 mm Qi2.2 wireless charging coil + 4 quadrant Ø22 mm Qi coils
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='none' stroke='#f0c05a' stroke-width='2.0' stroke-dasharray='4,2'/>" % (X(0), Y(0), min(w, h) * 0.33 * s),
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='none' stroke='#d8a848' stroke-width='1.2'/>" % (X(-w/4), Y(h/4), min(w, h) * 0.14 * s),
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='none' stroke='#d8a848' stroke-width='1.2'/>" % (X(w/4), Y(h/4), min(w, h) * 0.14 * s),
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='none' stroke='#d8a848' stroke-width='1.2'/>" % (X(-w/4), Y(-h/4), min(w, h) * 0.14 * s),
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='none' stroke='#d8a848' stroke-width='1.2'/>" % (X(w/4), Y(-h/4), min(w, h) * 0.14 * s),
        # Turned & 90°-Bent-at-Gap b module ON the screen (1.0 mm horizontal top çubuk + front-facing yuvarlak)
        "<path d='%s' fill='#8fa882' fill-opacity='0.96' stroke='#c9d6c4' stroke-width='1.6'/>" % d_b_outer,
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='#16283c' stroke='#557896' stroke-width='1.3'/>" % (rcx, rcy, r_bore),
        "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='#285888'/>" % (rcx, rcy, r_bore * 0.52),
    ]
    rows = [
        ("4-Parçalı (+) Yapboz Ekran", "4x (%.0fx%.0fx%.2f mm) · R=%.2f mm · Girdili-çıktılı yapboz kilit" % (w/2, h/2, th, R)),
        ("Katı-Hal Pil ve Göz Sağlığı", "LLZO/PEO pil (12 Wh, 0 HF) · &lt;=36.2 C · SAR 0.054 W/kg"),
        ("Portsuz Qi2 Kablosuz Gövde", "Gövdede Type-C yok · Qi/Qi2.2 (15-25 W) merkez + 4 bobin"),
        ("Boşluktan 90° Bükülen B", "1 mm yatay çubuk ekran üstünde · Yuvarlak kısım bize bakar"),
    ]
    y0 = H - 108
    for (k, v) in rows:
        o.append("<text x='40' y='%d' fill='#8ea2b4' font-family='DejaVu Sans,Helvetica,Arial' font-size='12'>%s</text>" % (y0, k))
        o.append("<text x='340' y='%d' fill='#eaf1f8' font-family='DejaVu Sans,Helvetica,Arial' font-size='12' font-weight='bold'>%s</text>" % (y0, v))
        y0 += 24
    o.append("</svg>\n")
    with open(path, "w") as f:
        f.write("\n".join(o))

    png_path = os.path.splitext(path)[0] + ".png"
    im = Image.new("RGB", (int(W), int(H)), (13, 17, 23))
    dr = ImageDraw.Draw(im)
    fp_b = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fp_r = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    f_title = ImageFont.truetype(fp_b, 17) if os.path.exists(fp_b) else ImageFont.load_default()
    f_sub = ImageFont.truetype(fp_r, 12) if os.path.exists(fp_r) else ImageFont.load_default()
    f_row_k = ImageFont.truetype(fp_r, 12) if os.path.exists(fp_r) else ImageFont.load_default()
    f_row_v = ImageFont.truetype(fp_b, 12) if os.path.exists(fp_b) else ImageFont.load_default()

    dr.text((40, 16), title, fill=(234, 241, 248), font=f_title)
    dr.text((40, 40), sub, fill=(147, 166, 140), font=f_sub)
    dr.polygon([(X(x), Y(y)) for (x, y) in pts], fill=(42, 78, 108), outline=(126, 194, 238))
    dr.polygon([(X(x), Y(y)) for (x, y) in scr_pts], fill=(22, 52, 78), outline=(98, 178, 230))
    dr.line([(X(x), Y(y)) for (x, y) in puz_v], fill=(92, 224, 184), width=2)
    dr.line([(X(x), Y(y)) for (x, y) in puz_h], fill=(92, 224, 184), width=2)
    rq = min(w, h) * 0.33 * s
    dr.ellipse((X(0) - rq, Y(0) - rq, X(0) + rq, Y(0) + rq), outline=(240, 192, 90), width=2)
    dr.polygon([(X(x), Y(y)) for (x, y) in b_outer], fill=(143, 168, 130), outline=(201, 214, 196))
    dr.ellipse((rcx - r_bore, rcy - r_bore, rcx + r_bore, rcy + r_bore), fill=(22, 40, 60), outline=(85, 120, 150))
    rb2 = r_bore * 0.52
    dr.ellipse((rcx - rb2, rcy - rb2, rcx + rb2, rcy + rb2), fill=(40, 88, 136))
    y0 = int(H) - 120
    for (k, v) in rows:
        dr.text((40, y0), k, fill=(142, 162, 180), font=f_row_k)
        dr.text((360, y0), v.replace("&lt;", "<"), fill=(234, 241, 248), font=f_row_v)
        y0 += 24
    im.save(png_path)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "models")
    os.makedirs(out, exist_ok=True)
    specs = [
        ("leaf80", 40.0, 80.0, 2.00, "BUDLUM LEAF 80 · 40 x 80 x 2.00 MM TEKİL KARO / GÖZLÜK MODÜLÜ"),
        ("leaf160", 80.0, 160.0, 2.00, "BUDLUM LEAF 160 · 4-PARÇALI (+) YAPBOZ EKRAN-PİL + 90° BÜKÜMLÜ B MODÜLÜ"),
        ("leaf480", 320.0, 480.0, 2.00, "BUDLUM LEAF 480 · ÇOKLU (+) YAPBOZ EKRAN-PİL + 90° BÜKÜMLÜ B MODÜLÜ"),
    ]
    for (tag, w, h, th, title) in specs:
        R = corner_radius(min(w, h))
        er = edge_fillet(th)
        v, f = mesh_from_rings(stack(lambda d, w=w, h=h, R=R: rounded_rect(w, h, R, d, 20), 0.0, th, er, steps=10))
        n = write_stl(os.path.join(out, "%s-body.stl" % tag), v, f, "budlum %s quad" % tag)
        plan_svg(os.path.join(out, "%s-plan.svg" % tag), w, h, th, title)
        print("%-10s  %6.1f x %6.1f x %.2f mm  R=%.2f  edge_r=%.2f  %6d tris" % (tag, w, h, th, R, er, n))


if __name__ == "__main__":
    main()
