#!/usr/bin/env python3
# BUDLUM LEAF · cad/render3d.py · revision L.4.1 · 2026-10-07
#
# Pure-Python + NumPy + PIL 3D renderer for Budlum Leaf CAD assemblies.
# Combines view-direction-aware layer ordering with back-to-front painter's
# depth sorting (-zc) and centroid-capped/annular-strip meshes so there is
# zero Z-fighting on thin coplanar layers and zero concave fan artifacts.

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

__all__ = [
    "part",
    "render",
    "render_scene",
    "read_stl",
    "transform",
    "scale_rot",
    "mat4_apply",
    "fit_camera",
    "rounded_rect",
    "circle",
    "prism",
    "annular_arc",
]


def part(verts, faces, colour, alpha=255, spec=0.35, shine=28.0, name="", bias=0.0, order=0.0):
    return dict(
        v=np.asarray(verts, float),
        f=[tuple(t) for t in faces],
        c=tuple(colour),
        a=alpha,
        spec=spec,
        shine=shine,
        name=name,
        bias=bias,
        order=order,
    )


def read_stl(path, colour=(200, 205, 212), alpha=255, spec=0.35):
    data = open(path, "rb").read()
    n = int(np.frombuffer(data[80:84], "<u4")[0])
    arr = np.frombuffer(data[84 : 84 + n * 50], dtype=np.uint8).reshape(n, 50)
    tri = arr[:, 12:48].copy().view("<f4").reshape(n, 3, 3).astype(float)
    return part(tri.reshape(-1, 3), np.arange(n * 3).reshape(n, 3), colour, alpha, spec)


def mat4_apply(v, m):
    h = np.c_[v, np.ones(len(v))]
    return (h @ np.asarray(m, float).T)[:, :3]


def scale_rot(scale=1.0, rot=None, move=(0.0, 0.0, 0.0)):
    if rot is None:
        rot = (0.0, 0.0, 0.0)
    rx, ry, rz = (math.radians(a) for a in rot)
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    R = Rz @ Ry @ Rx * scale
    m = np.eye(4)
    m[:3, :3] = R
    m[:3, 3] = move
    return m


def transform(p, m):
    return part(
        mat4_apply(p["v"], m),
        p["f"],
        p["c"],
        p["a"],
        p["spec"],
        p["shine"],
        p["name"],
        p["bias"],
        p["order"],
    )


def _cam(eye, target, up):
    eye = np.asarray(eye, float)
    f = np.asarray(target, float) - eye
    f /= np.linalg.norm(f)
    u = np.asarray(up, float)
    r = np.cross(f, u)
    if np.linalg.norm(r) < 1e-8:
        u = np.array([0.0, 1.0, 0.0])
        r = np.cross(f, u)
    r /= np.linalg.norm(r)
    u2 = np.cross(r, f)
    return eye, f, r, u2


def render(
    parts,
    path,
    eye,
    target=(0, 0, 0),
    up=(0, 1, 0),
    fov=28.0,
    width=1600,
    height=None,
    ss=2,
    bg=((16, 20, 25), (38, 46, 54)),
    ground=None,
    light=((-0.42, 0.55, 0.72), (0.58, -0.25, 0.45)),
    ambient=0.32,
    shadow=True,
    label=None,
):
    eye, f, r, u = _cam(eye, target, up)
    if height is None:
        height = width
    aspect = width / float(height)
    W, H = width * ss, height * ss
    img = Image.new("RGB", (W, H), bg[0])
    dr = ImageDraw.Draw(img, "RGBA")

    for y in range(H):
        t = y / float(H - 1)
        col = tuple(int(bg[0][i] + (bg[1][i] - bg[0][i]) * t) for i in range(3))
        dr.line([(0, y), (W, y)], fill=col)

    tan = math.tan(math.radians(fov) / 2.0)
    l1_cam = np.asarray(light[0], float)
    l1_cam /= np.linalg.norm(l1_cam)
    l2_cam = np.asarray(light[1], float)
    l2_cam /= np.linalg.norm(l2_cam)
    l1 = l1_cam[0] * r + l1_cam[1] * u + l1_cam[2] * (-f)
    l1 /= np.linalg.norm(l1)
    l2 = l2_cam[0] * r + l2_cam[1] * u + l2_cam[2] * (-f)
    l2 /= np.linalg.norm(l2)
    view = -f

    if shadow and ground is not None:
        blob = Image.new("L", (W, H), 0)
        bd = ImageDraw.Draw(blob)
        for p in parts:
            v = p["v"]
            if len(v) == 0:
                continue
            cam = (v - eye) @ np.column_stack([r, u, f])
            keep = cam[:, 2] > 0.1
            if not keep.any():
                continue
            z = cam[keep, 2][:, None]
            proj = np.c_[
                cam[keep, 0] / (z[:, 0] * tan * aspect),
                cam[keep, 1] / (z[:, 0] * tan),
            ]
            px = (proj[:, 0] + 1) / 2.0 * W
            py = (1 - proj[:, 1]) / 2.0 * H
            x0, x1, y0, y1 = px.min(), px.max(), py.min(), py.max()
            if x1 - x0 < 2 and y1 - y0 < 2:
                continue
            bd.ellipse([x0, y0, x1, y1], fill=55)
        blob = blob.filter(ImageFilter.GaussianBlur(W / 38.0))
        img = Image.composite(Image.new("RGB", (W, H), (6, 8, 10)), img, blob)
        dr = ImageDraw.Draw(img, "RGBA")

    # Determine whether the camera looks from the front (+Z) or back (-Z)
    front_view = (eye[2] >= target[2])
    basis = np.column_stack([r, u, f])

    draw = []
    for p in parts:
        v = p["v"]
        if len(v) == 0:
            continue
        cam = (v - eye) @ basis
        ord_val = float(p.get("order", 0.0))
        # Flip layer order automatically when viewing from the back (-Z)
        eff_order = ord_val if front_view else -ord_val
        bias = float(p.get("bias", 0.0))
        for t in p["f"]:
            i0, i1, i2 = t[0], t[1], t[2]
            c0, c1, c2 = cam[i0], cam[i1], cam[i2]
            if c0[2] <= 0.1 or c1[2] <= 0.1 or c2[2] <= 0.1:
                continue
            v0, v1, v2 = v[i0], v[i1], v[i2]
            n = np.cross(v1 - v0, v2 - v0)
            ln = np.linalg.norm(n)
            if ln < 1e-12:
                continue
            n = n / ln
            centroid = (v0 + v1 + v2) / 3.0
            to_tri = centroid - eye
            if n @ to_tri > 0.0:
                n = -n
            zc = (c0[2] + c1[2] + c2[2]) / 3.0 + bias
            px0 = c0[0] / (c0[2] * tan * aspect)
            py0 = c0[1] / (c0[2] * tan)
            px1 = c1[0] / (c1[2] * tan * aspect)
            py1 = c1[1] / (c1[2] * tan)
            px2 = c2[0] / (c2[2] * tan * aspect)
            py2 = c2[1] / (c2[2] * tan)
            pts2d = [
                ((px0 + 1) * 0.5 * W, (1 - py0) * 0.5 * H),
                ((px1 + 1) * 0.5 * W, (1 - py1) * 0.5 * H),
                ((px2 + 1) * 0.5 * W, (1 - py2) * 0.5 * H),
            ]
            draw.append((eff_order, -zc, pts2d, n, p))

    # Sort by effective layer order first, then back-to-front (-zc ascending = farthest first)
    draw.sort(key=lambda item: (item[0], item[1]))

    for (_, _, pts2d, n, p) in draw:
        lam1 = max(0.0, float(n @ l1))
        lam2 = max(0.0, float(n @ l2))
        half = l1 + view
        half = half / (np.linalg.norm(half) + 1e-9)
        sp = (max(0.0, float(n @ half)) ** p["shine"]) * p["spec"] * lam1
        shade = ambient + 0.68 * lam1 + 0.25 * lam2
        col = tuple(min(255, int(p["c"][i] * shade + 255 * sp)) for i in range(3))
        dr.polygon(pts2d, fill=col + (p["a"],))

    if ss != 1:
        img = img.resize((width, height), Image.LANCZOS)
    dr = ImageDraw.Draw(img, "RGBA")
    if label:
        fpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        bpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        for (txt, x, y, size, col) in label:
            bold = size >= 24
            try:
                fnt = ImageFont.truetype(bpath if bold else fpath, int(size))
            except Exception:
                fnt = None
            dr.text((x, y), txt, fill=col, font=fnt)
    img.save(path)
    return path


def fit_camera(parts, direction, fov=28.0, width=1800, height=1350, margin=0.84, up=(0, 1, 0)):
    v = np.vstack([p["v"] for p in parts if len(p["v"])])
    lo, hi = v.min(axis=0), v.max(axis(0)) if hasattr(v.max, "axis") else (v.min(axis=0), v.max(axis=0))
    lo, hi = v.min(axis=0), v.max(axis=0)
    center = (lo + hi) / 2.0
    corners = np.array(
        [[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    )
    d = np.asarray(direction, float)
    d = d / np.linalg.norm(d)
    cz = -d
    u_vec = np.asarray(up, float)
    right = np.cross(cz, u_vec)
    if np.linalg.norm(right) < 1e-8:
        u_vec = np.array([0.0, 0.0, 1.0])
        right = np.cross(cz, u_vec)
    right = right / np.linalg.norm(right)
    u2 = np.cross(right, cz)
    tan = math.tan(math.radians(fov) / 2.0)
    tt = tan * (width / float(height))
    rel = corners - center
    x = rel @ right
    y = rel @ u2
    zf = rel @ cz
    t = 0.0
    for i in range(len(rel)):
        t = max(t, abs(x[i]) / (margin * tt) - zf[i], abs(y[i]) / (margin * tan) - zf[i])
    t *= 1.04
    eye = center + d * t
    return tuple(eye), tuple(center)


def rounded_rect(w, h, r, d=0.0, n=16):
    w2, h2, r2 = w - 2 * d, h - 2 * d, max(r - d, 0.05)
    cx, cy = w2 / 2 - r2, h2 / 2 - r2
    pts = []
    for (px, py, a0) in ((cx, cy, 0), (-cx, cy, 90), (-cx, -cy, 180), (cx, -cy, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((px + r2 * math.cos(a), py + r2 * math.sin(a)))
    return pts


def circle(r, n=64, cx=0.0, cy=0.0):
    return [
        (cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


def prism(rings, inner=None):
    """Builds a closed mesh from [(z, pts), ...].
    Uses a centroid vertex for top and bottom caps so radial triangles are symmetric
    and never create diagonal fan artifacts across circles or rectangles.
    """
    n = len(rings[0][1])
    verts = []
    tri = []
    for (z, pts) in rings:
        verts += [(x, y, z) for (x, y) in pts]
    m = len(rings)
    for k in range(m - 1):
        a0 = k * n
        b0 = (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            tri.append((a0 + i, a0 + j, b0 + j))
            tri.append((a0 + i, b0 + j, b0 + i))
    if inner is None:
        # Bottom cap (ring 0) via centroid
        z_bot, pts_bot = rings[0]
        cx_b = sum(p[0] for p in pts_bot) / n
        cy_b = sum(p[1] for p in pts_bot) / n
        c_bot = len(verts)
        verts.append((cx_b, cy_b, z_bot))
        for i in range(n):
            j = (i + 1) % n
            tri.append((c_bot, j, i))
        # Top cap (ring m-1) via centroid
        z_top, pts_top = rings[m - 1]
        cx_t = sum(p[0] for p in pts_top) / n
        cy_t = sum(p[1] for p in pts_top) / n
        c_top = len(verts)
        verts.append((cx_t, cy_t, z_top))
        top_off = (m - 1) * n
        for i in range(n):
            j = (i + 1) % n
            tri.append((c_top, top_off + i, top_off + j))
    else:
        for (z, pts) in inner:
            verts += [(x, y, z) for (x, y) in pts]
        off = m * n
        for k in range(m - 1):
            a0 = off + k * n
            b0 = off + (k + 1) * n
            for i in range(n):
                j = (i + 1) % n
                tri.append((a0 + j, a0 + i, b0 + i))
                tri.append((a0 + j, b0 + i, b0 + j))
        for i in range(n):
            j = (i + 1) % n
            tri.append((i, j, off + j))
            tri.append((i, off + j, off + i))
            top = (m - 1) * n
            tri.append((top + j, top + i, off + top + i))
            tri.append((top + j, off + top + i, off + top + j))
    return np.array(verts, float), tri


def annular_arc(cx, cy, r_in, r_out, deg0, deg1, z0, z1, steps=24):
    """Builds a clean curved annular ribbon between angles deg0 and deg1 without
    concave chord-fan distortion.
    """
    verts = []
    tri = []
    for k in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * k / steps)
        ca, sa = math.cos(a), math.sin(a)
        verts.append((cx + r_in * ca, cy + r_in * sa, z0))
        verts.append((cx + r_out * ca, cy + r_out * sa, z0))
        verts.append((cx + r_in * ca, cy + r_in * sa, z1))
        verts.append((cx + r_out * ca, cy + r_out * sa, z1))
    for k in range(steps):
        b = 4 * k
        # bottom quad (b+0, b+1, b+5, b+4)
        tri.append((b + 0, b + 5, b + 1))
        tri.append((b + 0, b + 4, b + 5))
        # top quad (b+2, b+3, b+7, b+6)
        tri.append((b + 2, b + 3, b + 7))
        tri.append((b + 2, b + 7, b + 6))
        # inner wall (b+0, b+2, b+6, b+4)
        tri.append((b + 0, b + 2, b + 6))
        tri.append((b + 0, b + 6, b + 4))
        # outer wall (b+1, b+5, b+7, b+3)
        tri.append((b + 1, b + 5, b + 7))
        tri.append((b + 1, b + 7, b + 3))
    # end caps
    tri.append((0, 1, 3))
    tri.append((0, 3, 2))
    e = 4 * steps
    tri.append((e + 0, e + 2, e + 3))
    tri.append((e + 0, e + 3, e + 1))
    return np.array(verts, float), tri


def render_scene(
    scene_list,
    path,
    size=(1300, 1150),
    angles=(26.0, -26.0, 0.0),
    zoom=5.0,
    pan=(0.0, 0.0),
    bg_top=(14, 20, 28),
    bg_bot=(24, 34, 46),
    title=None,
    subtitle=None,
):
    """High-level scene wrapper converting (verts, faces, rgb_01, alpha_01) tuples into
    `render3d.part(...)` meshes, fitting camera to `angles=(el_deg, az_deg, roll_deg)`,
    and writing the rendered PNG with optional header title/subtitle.
    """
    W, H = int(size[0]), int(size[1])
    p_list = []
    for item in scene_list:
        v, f, col, a = item[0], item[1], item[2], item[3]
        ord_val = float(item[4]) if len(item) > 4 else 0.0
        c255 = (
            max(0, min(255, int(round(col[0] * 255)))),
            max(0, min(255, int(round(col[1] * 255)))),
            max(0, min(255, int(round(col[2] * 255)))),
        )
        a255 = max(12, min(255, int(round(a * 255))))
        p_list.append(part(v, f, c255, alpha=a255, spec=0.38, shine=28.0, order=ord_val))

    el_deg, az_deg = float(angles[0]), float(angles[1])
    el = math.radians(el_deg)
    az = math.radians(az_deg)
    direction = (
        -math.cos(el) * math.sin(az),
        math.sin(el),
        math.cos(el) * math.cos(az),
    )
    eye, target = fit_camera(p_list, direction, fov=28.0, width=W, height=H, margin=0.78)
    labels = []
    if title:
        labels.append((title, 32, 20, 20, (236, 243, 250, 255)))
    if subtitle:
        labels.append((subtitle, 32, 50, 14, (156, 182, 160, 255)))
    return render(
        p_list,
        path,
        eye=eye,
        target=target,
        up=(0, 1, 0),
        fov=28.0,
        width=W,
        height=H,
        ss=2,
        bg=(bg_top, bg_bot),
        label=labels,
    )

