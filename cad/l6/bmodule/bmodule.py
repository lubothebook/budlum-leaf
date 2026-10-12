#!/usr/bin/env python3
# BUDLUM LEAF · cad/l6/bmodule/bmodule.py · revision L.6.0 · 2026-10-12
#
# Parametric generator of the L.6.0 B module (Part 21.3, HARDWARE/13, 32 parts).
#
# Frame (module frame, mm):
#   x : along the bar, 0 .. 32 (x = v of uploads/b.png)
#   y : up the face; the body top edge is y = 36, the bar is y = 36 .. 37 (y = 40 - u)
#   z : out of the face; the body front face is z = 0, the body is z = -2 .. 0,
#       the ring is z = 0 .. 4.00, the bar lies across the edge at z = -2 .. +2
#   ring centre RC = (16, 16); "local" X, Y are measured from RC.
#   jack: chord at X = +13.8, axis parallel to Y, axis height z = 2.0, mouth toward -Y.
#
# Seated on the 80 x 160 x 2 body: translate by (+24, +124, 0) (see seat_check.py).
#
# Run:  python3 bmodule.py          -> stl/*.stl, stl/parts.json
# Needs numpy, shapely, trimesh and manifold3d (the boolean kernel; pip install manifold3d).

import json
import math
import os
import sys
import time

import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
import trimesh
import manifold3d as mf

M = mf.Manifold
CS = mf.CrossSection

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")

# ---------------------------------------------------------------------------
# 1. Parameters. Every number of Part 21.3 and HARDWARE/13 lives here.
# ---------------------------------------------------------------------------
P = dict(
    # module envelope
    module_t=4.00,          # ring thickness, z = 0 .. 4.00
    body_t=2.00,            # body thickness (seat), z = -2 .. 0
    edge_y=36.0,            # body top edge in the module frame
    # b.png / monogram_letter.py
    bar_len=32.0, bar_w=4.0, bar_h=1.00, cap_r=2.0,
    ring_c=(16.0, 16.0), ring_ro=16.0, ring_ri=12.0,
    valley_c=(16.0, 24.0), valley_r=12.0,
    neck_t=2.00,            # bridge plate thickness on the face
    # shell walls
    skin=0.30, wall=0.60,   # ring skins (front/rear) and outer wall
    # bar stack (bottom to top): contact 0.25, mmWave 0.10, core 0.40, antenna 0.05, skin 0.20
    bar_layers=(0.25, 0.10, 0.40, 0.05, 0.20),
    # fillets (Ayaz order, L.6.0 touch edges)
    f_ring_out=0.40, f_ring_bore=0.25, f_bar=0.20, f_corner=0.30, f_jack=0.20,
    f_window=0.10, f_neck_top=0.25, f_neck_bot=0.20,
    # camera
    cam_c=(0.0, 0.5), cam_xy=(7.0, 6.0), cam_h=3.90, l1_d=3.0,
    cam_nose_xy=(6.3, 5.1), disp_hole=(6.5, 5.3), rear_pocket_d=0.20,
    # jack
    jack_off=13.8, jack_bore=3.6, jack_wall=0.20, jack_closed=5.0, jack_trough=9.0,
    # z stack inside the ring
    z_amoled=(0.30, 0.70), z_shield=(0.70, 0.85), z_pcba=(0.90, 1.45),
    z_chip0=1.46, z_cell=(1.50, 3.00), z_spk=(0.90, 3.10), z_spreader=(2.47, 3.27),
    z_gasket=(3.30, 3.70), z_mag=(0.30, 1.40), z_flex=(1.45, 1.55), z_a3=(1.60, 2.40),
    keep_x=11.4,            # internal parts stay at local X <= keep_x where Y < keep_y (jack)
    keep_y=3.0,
)

RC = np.array(P["ring_c"])
T = P["module_t"]
SEG = 360                  # revolve segments (chord sag 0.6 um at r = 16)


# ---------------------------------------------------------------------------
# 2. Geometry helpers
# ---------------------------------------------------------------------------
def boxm(x0, x1, y0, y1, z0, z1):
    return M.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def lbox(X0, X1, Y0, Y1, z0, z1):
    """Box in ring-local X, Y."""
    return boxm(X0 + RC[0], X1 + RC[0], Y0 + RC[1], Y1 + RC[1], z0, z1)


def poly_to_cs(shp):
    geoms = getattr(shp, "geoms", [shp])
    contours = []
    for g in geoms:
        g = orient(g, 1.0)
        contours.append(shapely.get_coordinates(g.exterior)[:-1].copy())
        for h in g.interiors:
            contours.append(shapely.get_coordinates(h)[:-1].copy())
    return CS(contours, mf.FillRule.EvenOdd)


def prism(shp, z0, z1):
    return poly_to_cs(shp).extrude(z1 - z0).translate((0, 0, z0))


def lpoly(shp):
    """Shapely geometry in local X, Y -> module x, y."""
    return shapely.affinity.translate(shp, RC[0], RC[1])


def rounded_polygon(pts, radii, n_arc=12):
    """2D polygon with a tangent fillet of radius radii[i] at vertex i."""
    pts = [np.asarray(p, float) for p in pts]
    n = len(pts)
    out = []
    for i in range(n):
        p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
        r = radii[i]
        if r <= 0:
            out.append(p)
            continue
        u1 = (a - p) / np.linalg.norm(a - p)
        u2 = (b - p) / np.linalg.norm(b - p)
        ang = math.acos(max(-1.0, min(1.0, float(u1 @ u2))))
        t = r / math.tan(ang / 2)
        c = p + (u1 + u2) / np.linalg.norm(u1 + u2) * (r / math.sin(ang / 2))
        t1, t2 = p + u1 * t, p + u2 * t
        a1 = math.atan2(*(t1 - c)[::-1])
        a2 = math.atan2(*(t2 - c)[::-1])
        d = a2 - a1
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        for k in range(n_arc + 1):
            th = a1 + d * k / n_arc
            out.append(c + r * np.array([math.cos(th), math.sin(th)]))
    return np.array(out)


def revolve_profile(pts, radii, centre=RC, seg=SEG):
    prof = rounded_polygon(pts, radii)
    if Polygon(prof).exterior.is_ccw is False:
        prof = prof[::-1]
    return CS([prof]).revolve(seg).translate((centre[0], centre[1], 0))


def mesh_to_manifold(V, F):
    V = np.asarray(V, np.float64)
    F = np.asarray(F, np.int64)
    tm = trimesh.Trimesh(V, F, process=False)
    if tm.volume < 0:
        F = F[:, ::-1]
    m = M(mf.Mesh(vert_properties=V.astype(np.float32), tri_verts=F.astype(np.uint32)))
    if m.status() != mf.Error.NoError:
        raise RuntimeError("bad mesh: %s" % m.status())
    return m


def loft(sections, caps2d):
    """Closed solid through planar-capped sections of equal vertex count.
    sections: list of (N,3); caps2d: (first, last) 2D CCW coordinates of the end caps."""
    S, N = len(sections), len(sections[0])
    V = np.concatenate(sections)
    F = []
    for k in range(S - 1):
        a, b = k * N, (k + 1) * N
        for i in range(N):
            j = (i + 1) % N
            F.append((a + i, a + j, b + j))
            F.append((a + i, b + j, b + i))
    t0 = mf.triangulate([np.asarray(caps2d[0], float)])
    F += [tuple(t[::-1]) for t in t0]
    t1 = mf.triangulate([np.asarray(caps2d[1], float)])
    F += [tuple(t + (S - 1) * N) for t in t1]
    return mesh_to_manifold(V, np.array(F))


def rounded_prism(poly, h0, h1, rb, rt, frame=None, nf=8, seg=0.06):
    """Extrude a plan polygon from h0 to h1 with a fillet of radius rb on the bottom
    perimeter and rt on the top perimeter. Convex plan corners need a radius >= max(rb, rt).
    frame maps (a, b, h) arrays to (x, y, z); it must be a proper rotation."""
    poly = orient(poly, 1.0)
    ext = poly.exterior
    n = max(64, int(ext.length / seg))
    d = np.linspace(0, ext.length, n, endpoint=False)
    Pt = shapely.get_coordinates(shapely.line_interpolate_point(ext, d))
    tng = np.roll(Pt, -1, 0) - np.roll(Pt, 1, 0)
    tng /= np.linalg.norm(tng, axis=1)[:, None]
    nin = np.stack([-tng[:, 1], tng[:, 0]], 1)
    layers = []
    if rb > 0:
        for k in range(nf + 1):
            ph = 0.5 * math.pi * k / nf
            layers.append((rb * (1 - math.sin(ph)), h0 + rb * (1 - math.cos(ph))))
    else:
        layers.append((0.0, h0))
    if rt > 0:
        for k in range(nf + 1):
            ph = 0.5 * math.pi * k / nf
            layers.append((rt * (1 - math.cos(ph)), h1 - rt + rt * math.sin(ph)))
    else:
        layers.append((0.0, h1))
    secs, c2 = [], []
    for dl, h in layers:
        q = Pt + nin * dl
        a, b, hh = q[:, 0], q[:, 1], np.full(len(q), h)
        xyz = np.stack(frame(a, b, hh) if frame else (a, b, hh), 1)
        secs.append(xyz)
        c2.append(q)
    return loft(secs, (c2[0], c2[-1]))


def cyl_y(r, y0, y1, X, z, seg=128):
    """Cylinder along +y, axis at module (X, z)."""
    return (M.cylinder(y1 - y0, r, r, seg).rotate((-90, 0, 0)).translate((X, y0, z)))


def union_all(ms):
    ms = [m for m in ms if m is not None]
    return M.batch_boolean(ms, mf.OpType.Add) if len(ms) > 1 else ms[0]


# ---------------------------------------------------------------------------
# 3. Signed distance of the jack trough block (moulded into the ring shell)
# ---------------------------------------------------------------------------
def _round_box2(px, py, bx, by, r):
    qx, qy = abs(px) - bx + r, abs(py) - by + r
    return min(max(qx, qy), 0.0) + math.hypot(max(qx, 0.0), max(qy, 0.0)) - r


def _rint(a, b, r):
    """Round intersection of two SDFs (negative inside), fillet radius r."""
    return min(-r, max(a, b)) + math.hypot(max(a + r, 0.0), max(b + r, 0.0))


def jack_sdf_factory():
    ro, ri = P["ring_ro"], P["ring_ri"]
    fo, fb, fj = P["f_ring_out"], P["f_ring_bore"], P["f_jack"]
    xo, rb = P["jack_off"], P["jack_bore"] / 2
    ro_t = rb + P["jack_wall"]                      # 2.0, tube outer radius
    s_closed0 = -(math.sqrt(ro ** 2 - (xo + ro_t) ** 2))   # -2.52: sleeve fully inside
    s_mouth = s_closed0 - P["jack_trough"]          # -11.52
    sc, hl = (s_mouth + (-9.5)) / 2, ((-9.5) - s_mouth) / 2
    cz = T / 2

    def d_env(X, Y, z):
        rho = math.hypot(X, Y)
        px, py = rho - (ri + ro) / 2, z - cz
        r = fo if px > 0 else fb
        return _round_box2(px, py, (ro - ri) / 2, T / 2, r)

    def sdf(x, y, z):
        X, Y = x - RC[0], y - RC[1]
        p, q = X - xo, z - cz
        rho_b = math.hypot(p, q)
        a = d_env(X, Y, z)
        # rim boss: inner half collar, rounded 0.2
        dx, dy = rho_b - ro_t + fj, abs(Y - sc) - hl + fj
        boss = min(max(dx, dy), 0.0) + math.hypot(max(dx, 0.0), max(dy, 0.0)) - fj
        boss = _rint(boss, p - 0.3, fj)
        env = min(a, boss)
        d = _rint(env, rb - rho_b, fj)              # minus the bore, mouth and lips rounded
        # generous clip box (the exact JB box trims it afterwards)
        bxs = max(11.65 - X, X - 16.75, -11.95 - Y, Y + 2.35)
        d = max(d, bxs)
        return -d
    return sdf, s_closed0, s_mouth


# ---------------------------------------------------------------------------
# 4. The parts
# ---------------------------------------------------------------------------
def build(verbose=True):
    t0 = time.time()
    parts = {}

    def add(name, no, m, material, rho, group, note=""):
        parts[name] = dict(m=m, no=no, material=material, rho=rho, group=group, note=note)

    ro, ri, sk, wl = P["ring_ro"], P["ring_ri"], P["skin"], P["wall"]
    fo, fb, fw = P["f_ring_out"], P["f_ring_bore"], P["f_window"]
    rin = ro - wl                                    # cavity radius 15.4
    ey = P["edge_y"]
    xo = P["jack_off"]
    jx = RC[0] + xo                                  # jack axis x (module)
    cz = T / 2

    # 4.1 ring envelope (full disc, outer fillets) and ring shell
    E = revolve_profile([(0, 0), (ro, 0), (ro, T), (0, T)], [0, fo, fo, 0])
    shell_rev = revolve_profile(
        [(ri, 0), (ro, 0), (ro, T), (ri, T), (ri, T - sk), (rin, T - sk), (rin, sk), (ri, sk)],
        [fb, fo, fo, fb, 0, 0, 0, 0])

    # 4.2 windows (0.10 edge break) and the camera
    cam_X, cam_Y = P["cam_c"]
    cx, cy = RC[0] + cam_X, RC[1] + cam_Y
    l1 = M.cylinder(sk, P["l1_d"] / 2, P["l1_d"] / 2, 96).translate((cx, cy, T - sk))
    front = revolve_profile([(0, T - sk), (ri, T - sk), (ri, T), (0, T)], [0, 0, fw, 0]) - l1
    nx, ny = P["cam_nose_xy"]
    hx, hy = P["disp_hole"]
    pocket = boxm(cx - hx / 2, cx + hx / 2, cy - hy / 2, cy + hy / 2, sk - P["rear_pocket_d"], sk + 0.01)
    rear = revolve_profile([(0, 0), (ri, 0), (ri, sk), (0, sk)], [0, fw, 0, 0]) - pocket
    z_cam0 = T - P["cam_h"]                          # 0.10
    cwx, cwy = P["cam_xy"]
    camera = union_all([
        boxm(cx - nx / 2, cx + nx / 2, cy - ny / 2, cy + ny / 2, z_cam0, 0.90),
        boxm(cx - cwx / 2, cx + cwx / 2, cy - cwy / 2, cy + cwy / 2, 0.90, T - sk),
        l1])
    add("front_window", 7, front, "sapphire, AR coat, L1 seat", 3.98, "ring")
    add("rear_window", 8, rear, "sapphire, oleophobic, 0.20 camera pocket", 3.98, "ring")
    add("camera_column", 11, camera, "50 MP column, L1 in the window", 2.6, "ring",
        "3.60 body + 0.30 L1 = 3.90")

    # 4.3 jack: closed-end sleeve (exact) + trough block (SDF, moulded in the shell)
    sdf, s_c0, s_mouth = jack_sdf_factory()
    s_c1 = s_c0 + P["jack_closed"]                   # +2.48 ... blind end
    rb, rt = P["jack_bore"] / 2, P["jack_bore"] / 2 + P["jack_wall"]
    y_c0, y_c1 = RC[1] + s_c0, RC[1] + s_c1
    tube_env = cyl_y(rt, y_c0, y_c1 + P["jack_wall"], jx, cz)
    sleeve = (tube_env - cyl_y(rb, y_c0 - 0.01, y_c1, jx, cz)) ^ E
    JB = lbox(11.75, 16.7, -11.9, s_c0, -0.2, T + 0.2)
    if verbose:
        print("  meshing jack trough SDF ...", flush=True)
    blk = M.level_set(sdf, [RC[0] + 11.6, RC[1] - 12.0, -0.15, RC[0] + 16.8, RC[1] - 2.3, T + 0.15],
                      0.05, 0.0, 0.002)
    blk = blk ^ JB
    add("jack_sleeve", 26, sleeve, "3.5 mm sleeve, Ø3.6 bore, 0.20 wall, blind end", 8.5, "ring",
        "closed end s = %.2f .. %.2f" % (s_c0, s_c1))

    # 4.4 corner flex path (bar -> corner -> neck -> ring), Part 5
    zf0, zf1 = P["z_flex"]
    flex_line = LineString([(2.15, 36.55), (2.15, 25.5), (5.5, 25.5)])
    flex_poly = flex_line.buffer(1.75, cap_style="flat", join_style="round", quad_segs=16)
    flex = union_all([boxm(0.40, 3.90, 36.45, 36.55, -0.10, zf1), prism(flex_poly, zf0, zf1)])
    flex_len = 1.65 + flex_line.length
    add("corner_flex", 5, flex, "20-line LCP flex, 0.10", 2.2, "bar", "length %.2f" % flex_len)

    # 4.5 ring shell, Part 6
    shell = shell_rev - tube_env - JB - flex
    shell = shell + blk
    add("ring_shell", 6, shell, "LCP-GF40, no metal", 1.70, "ring")

    # 4.6 bar + neck + moulded corner, Part 1
    L, W, H = P["bar_len"], P["bar_w"], P["bar_h"]
    cr = P["cap_r"]
    # plan in (a, b) = (x, -z): z = +2 is the front (face side), z = -2 the back
    semi = [(L - cr + cr * math.cos(t), cr * math.sin(t)) for t in np.linspace(math.pi / 2, -math.pi / 2, 65)]
    frc = [(0.25 + 0.25 * math.cos(t), -1.75 + 0.25 * math.sin(t)) for t in np.linspace(-math.pi / 2, -math.pi, 13)]
    bkc = [(cr + cr * math.cos(t), cr * math.sin(t)) for t in np.linspace(math.pi, math.pi / 2, 33)]
    plan = Polygon(semi + frc + bkc)
    plan = plan.buffer(0)
    fb_bar = P["f_bar"]
    bar = rounded_prism(plan, ey, ey + H, fb_bar, fb_bar,
                        frame=lambda a, b, h: (a, h, -b))
    # neck (bridge) on the face, z = 0 .. 2, overlapping the ring wall and the bar
    raw = (sbox(0, 16, 16, ey) - Point(P["valley_c"]).buffer(P["valley_r"], 256)
           - Point(RC).buffer(15.6, 256))
    strip = sbox(0, 14.45, ey - 0.1, ey + 0.8)
    neck_plan = unary_union([raw, strip]).buffer(-0.3, 64).buffer(0.3, 64).buffer(0.1, 64).buffer(-0.1, 64)
    if neck_plan.geom_type != "Polygon":
        neck_plan = max(neck_plan.geoms, key=lambda g: g.area)
    neck = rounded_prism(neck_plan, 0.0, P["neck_t"], P["f_neck_bot"], P["f_neck_top"])
    neck = neck - E
    # corner cutter: r 0.30 on the outside edge (y = 37, z = 2) along the bend, taper to 0.19
    xs = np.concatenate([np.linspace(-0.1, 14.0, 3), np.linspace(14.0, 15.0, 12)[1:]])
    rr = np.where(xs <= 14.0, P["f_corner"], P["f_corner"] - (P["f_corner"] - 0.19) * (xs - 14.0))
    e = 0.05
    yt, zt = ey + H, P["bar_w"] / 2
    secs, caps = [], []
    for x, r in zip(xs, rr):
        th = np.linspace(math.pi / 2, 0, 16)
        yz = [(yt + e, zt - r), (yt + e, zt + e), (yt - r, zt + e), (yt - r, zt)]
        yz += [(yt - r + r * math.cos(t), zt - r + r * math.sin(t)) for t in th[1:-1]]
        yz += [(yt, zt - r)]
        yz = np.array(yz)
        if Polygon(yz).exterior.is_ccw is False:
            yz = yz[::-1]
        secs.append(np.column_stack([np.full(len(yz), x), yz]))
        caps.append(yz)
    cutter = loft(secs, (caps[0], caps[-1]))
    part1 = (bar + neck) - cutter

    # 4.7 bar internals: A1/A2 copper, A4 array, 12 leaves (Parts 2, 3, 4)
    lay = np.cumsum((0,) + P["bar_layers"]) + ey      # 36.00 36.25 36.35 36.75 36.80 37.00
    a1 = boxm(1.3, 30.7, lay[3], lay[4], -1.8, 1.8)
    a4 = boxm(16.5, 30.5, lay[1], lay[2], -1.6, 1.6)
    seat_x0 = 6.2                                     # seat tile body x 30..40 -> module 6..16
    leaves = union_all([boxm(seat_x0 + 0.8 * i + 0.15, seat_x0 + 0.8 * i + 0.65, lay[0], lay[1], -1.75, 1.25)
                        for i in range(12)])
    part1 = part1 - a1 - a4 - leaves - flex
    add("bar_shell", 1, part1, "LCP-GF40 bar, bridge and moulded 90° corner", 1.70, "bar")
    add("a1_a2_copper", 2, a1, "LDS copper", 8.96, "bar")
    add("a4_array", 3, a4, "2-layer LCP flex, 1 x 4 patches", 2.4, "bar")
    add("body_leaves", 4, leaves, "12 hard-gold spring leaves, field 9.6", 8.8, "bar",
        "x %.2f .. %.2f" % (seat_x0, seat_x0 + 9.6))

    # 4.8 ring internals
    kx, ky = P["keep_x"], P["keep_y"]
    keep = lpoly(sbox(kx, 20, -20, ky))                # jack keep-out (local X >= 11.4, Y < 3)
    camc = lpoly(Point(cam_X, cam_Y))

    def lrect(X0, X1, Y0, Y1):
        return lpoly(sbox(X0, X1, Y0, Y1))

    def crect(w, h, grow=0.0):
        return lpoly(sbox(cam_X - w / 2 - grow, cam_X + w / 2 + grow, cam_Y - h / 2 - grow, cam_Y + h / 2 + grow))

    disc = lambda r: lpoly(Point(0, 0).buffer(r, 256))
    amoled = prism(disc(11.6) - crect(hx, hy), *P["z_amoled"])
    shield = prism(disc(11.8) - crect(hx + 0.2, hy + 0.2), *P["z_shield"])
    add("rear_amoled", 9, amoled, "round LTPO AMOLED Ø23.2, 6.5 x 5.3 hole", 2.6, "ring")
    add("cu_graphite_shield", 10, shield, "Cu-graphite, Ø23.6", 3.5, "ring")

    # magnets: 8 x (3.2 tangential x 1.6 radial x 1.1), r 13.4 .. 15.0
    mag_ang = [25, 65, 115, 150, 185, 215, 240, 300]
    mags, notches = [], []
    for a in mag_ang:
        rect = sbox(13.4, 15.0, -1.6, 1.6)
        g = shapely.affinity.rotate(rect, a, origin=(0, 0))
        mags.append(prism(lpoly(g), *P["z_mag"]))
        notches.append(lpoly(shapely.affinity.rotate(sbox(13.3, 16, -1.7, 1.7), a, origin=(0, 0))))
    add("seat_magnets", 28, union_all(mags), "8 x N52H in the sliding pad", 7.5, "ring")

    spk = lrect(-4.5, 4.5, -14.6, -11.4)
    add("micro_speaker", 13, prism(spk, *P["z_spk"]), "balanced micro-speaker 9.0 x 3.2 x 2.2", 4.0, "ring")

    pcba_plan = disc(15.0) - keep - crect(7.2, 6.2) - spk.buffer(0.1, join_style="mitre") - unary_union(notches)
    add("ring_pcba", 15, prism(pcba_plan, *P["z_pcba"]), "8-layer HDI, Ø30.0 x 0.55", 2.8, "ring")

    z0 = P["z_chip0"]
    chips = {  # name: (no, X0, X1, Y0, Y1, h, can)
        "u5_modem": (19, -12.2, -4.2, -2.5, 7.5, 0.80, True),
        "u2b_60ghz_uwb": (18, -2.5, 2.5, 3.85, 8.35, 0.60, True),
        "u1_tcon": (16, -2.6, 2.6, 8.8, 14.0, 0.45, False),
        "u2a_wifi7": (17, 4.5, 9.5, 3.7, 8.7, 0.60, True),
        "u6_decoder": (20, 5.35, 11.35, -2.6, 3.4, 0.70, False),
        "u7_secure": (21, 6.3, 8.3, 9.0, 11.0, 0.40, False),
        "u8_imu": (22, -4.7, -2.7, 9.0, 11.0, 0.70, False),
        "u3_audio": (23, -13.4, -10.2, -6.0, -2.8, 0.40, False),
        "u4_power": (23, 9.8, 13.0, 3.6, 6.8, 0.40, False),
        "cell_mux": (27, 3.0, 6.0, 9.0, 12.0, 0.40, False),
    }
    cans = []
    for name, (no, X0, X1, Y0, Y1, h, can) in chips.items():
        add(name, no, lbox(X0, X1, Y0, Y1, z0, z0 + h), "die / package", 2.4, "ring")
        if can:
            o = lbox(X0 - 0.15, X1 + 0.15, Y0 - 0.15, Y1 + 0.15, z0, z0 + h + 0.15)
            i = lbox(X0 - 0.05, X1 + 0.05, Y0 - 0.05, Y1 + 0.05, z0 - 0.01, z0 + h + 0.05)
            cans.append(o - i)
    add("shield_cans", 32, union_all(cans), "nickel silver over U2A, U2B, U5", 8.7, "ring")
    tun = [(5.0, 6.5, -12.5, -11.5), (-6.5, -5.0, -12.5, -11.5), (9.8, 11.3, 7.0, 8.0)]
    add("aperture_tuners", 25, union_all([lbox(*t, z0, z0 + 0.4) for t in tun]), "3 switched networks", 2.4, "ring")
    mics = [(-7.5, -4.8, 10.0, 11.8), (-12.0, -10.2, -8.8, -6.1)]
    add("mems_mics", 14, union_all([lbox(*m_, z0, z0 + 0.9) for m_ in mics]), "2 x MEMS, ePTFE", 2.5, "ring")
    add("led_flash", 12, lbox(3.65, 5.25, -1.0, 1.4, z0, z0 + 0.65), "2700K + 5600K CSP", 3.0, "ring")
    cell = lrect(-10.0, 10.0, -10.8, -2.8)
    add("b_cell", 29, prism(cell, *P["z_cell"]), "Li-ion 20 x 8 x 1.5, 0.14 Wh", 2.6, "ring")

    spr_plan = (disc(14.0) - keep - crect(7.4, 6.4) - cell.buffer(0.1, join_style="mitre")
                - spk.buffer(0.1, join_style="mitre") - lrect(3.45, 5.45, -1.2, 1.6))
    add("spreader_pcm", 31, prism(spr_plan, *P["z_spreader"]), "graphite + PCM, Ø28 x 0.80", 1.2, "ring")
    gsk_plan = disc(15.0) - disc(11.4) - keep.buffer(0.2, join_style="mitre")
    add("gaskets", 30, prism(gsk_plan, *P["z_gasket"]), "FKM 60A, Ø30.0 x 3.6 x 0.40", 1.85, "ring")
    # A3 loop: LDS band on the inner wall, routed around the jack groove
    a3_plan = disc(rin) - disc(rin - 0.05) - lrect(11.0, 17, -13, ky + 0.2)
    add("a3_loop", 24, prism(a3_plan, *P["z_a3"]), "LDS loop Ø31 class", 8.96, "ring")

    if verbose:
        print("  built %d parts in %.1f s" % (len(parts), time.time() - t0))
    info = dict(s_closed0=s_c0, s_closed1=s_c1, s_mouth=s_mouth, flex_len=flex_len,
                neck_plan_area=neck_plan.area)
    return parts, info


def to_trimesh(m):
    mesh = m.to_mesh()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)


def export(parts, info):
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    allm = []
    for name, d in sorted(parts.items(), key=lambda kv: (kv[1]["no"], kv[0])):
        m = d["m"]
        tm = to_trimesh(m)
        fn = "bmodule-p%02d-%s.stl" % (d["no"], name.replace("_", "-"))
        tm.export(os.path.join(OUT, fn))
        bb = m.bounding_box()
        meta[name] = dict(no=d["no"], file=fn, material=d["material"], density=d["rho"],
                          group=d["group"], note=d["note"], volume_mm3=round(m.volume(), 4),
                          bounds=[round(v, 4) for v in bb])
        allm.append(m)
    asm = M.compose(allm)
    to_trimesh(asm).export(os.path.join(OUT, "bmodule-assembly.stl"))
    with open(os.path.join(OUT, "parts.json"), "w") as f:
        json.dump(dict(params={k: v for k, v in P.items()}, info=info, parts=meta), f, indent=1)
    return meta


if __name__ == "__main__":
    parts, info = build()
    meta = export(parts, info)
    for k, v in sorted(meta.items(), key=lambda kv: kv[1]["no"]):
        print("  p%02d %-22s %9.3f mm3" % (v["no"], k, v["volume_mm3"]))
    print("  info:", info)
