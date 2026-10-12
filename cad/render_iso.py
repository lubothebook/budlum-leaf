#!/usr/bin/env python3
# BUDLUM LEAF · cad/render_iso.py · revision L.4.1 · 2026-10-07
#
# Orthographic SVG mesh helpers and primitive builders (`box`, `cylinder`,
# `rounded_plate`, `read_stl`, `transform`, `render`) used by `rail_detail.py`.

import math, os, struct
from leaf_geom import mesh_from_rings, rounded_rect

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")


def box(dx, dy, dz, cx=0.0, cy=0.0, cz=0.0):
    ring = [
        (cx - dx / 2.0, cy - dy / 2.0),
        (cx + dx / 2.0, cy - dy / 2.0),
        (cx + dx / 2.0, cy + dy / 2.0),
        (cx - dx / 2.0, cy + dy / 2.0),
    ]
    z0, z1 = cz - dz / 2.0, cz + dz / 2.0
    return mesh_from_rings([(z0, ring), (z1, ring)])


def cylinder(r, h, n=24, cx=0.0, cy=0.0, cz=0.0):
    ring = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    z0, z1 = cz - h / 2.0, cz + h / 2.0
    return mesh_from_rings([(z0, ring), (z1, ring)])


def rounded_plate(w, h, r, dz, z0=0.0):
    ring = rounded_rect(w, h, r, n_corner=8)
    return mesh_from_rings([(z0, ring), (z0 + dz, ring)])


def read_stl(path):
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[80:84])[0]
    tris = []
    off = 84
    for i in range(n):
        vals = struct.unpack("<12fH", data[off:off + 50])
        v = [(vals[3], vals[4], vals[5]), (vals[6], vals[7], vals[8]), (vals[9], vals[10], vals[11])]
        tris.append(v)
        off += 50
    return tris


def disc(radius, z, n=48, cx=0.0, cy=0.0):
    """A flat disc as triangles, for the camera window."""
    pts = [(cx + radius * math.cos(2 * math.pi * i / n), cy + radius * math.sin(2 * math.pi * i / n), z) for i in range(n)]
    tris = []
    for i in range(n):
        tris.append([(cx, cy, z), pts[i], pts[(i + 1) % n]])
    return tris


def transform(tris, move=(0, 0, 0), scale=1.0):
    out = []
    for t in tris:
        out.append([((p[0] * scale + move[0]), (p[1] * scale + move[1]), (p[2] * scale + move[2])) for p in t])
    return out


def normal(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return (nx / ln, ny / ln, nz / ln)


def render(tris, path, az_deg=38.0, el_deg=26.0, width=1100, margin=40, palette=None, y_up=False, title=None, subtitle=None, layers=None):
    az, el = math.radians(az_deg), math.radians(el_deg)
    ca, sa, ce, se = math.cos(az), math.sin(az), math.cos(el), math.sin(el)
    if y_up:
        # +Y is upright vertical; azimuth rotates in (X, Z) around +Y; elevation tilts from +Z toward +Y
        right = (ca, 0.0, sa)
        up = (-se * sa, ce, se * ca)
        view = (-ce * sa, se, ce * ca)
        light = (-0.38, 0.62, 0.68)
    else:
        right = (-sa, ca, 0.0)
        up = (-ce * ca, -ce * sa, se)
        view = (se * ca, se * sa, ce)
        light = (0.42, -0.55, 0.72)
    proj, depth, front = [], [], []
    for t in tris:
        p2 = []
        for p in t:
            p2.append((p[0] * right[0] + p[1] * right[1] + p[2] * right[2],
                       p[0] * up[0] + p[1] * up[1] + p[2] * up[2]))
        d = sum((p[0] * view[0] + p[1] * view[1] + p[2] * view[2]) for p in t) / 3.0
        n = normal(t)
        nv = n[0] * view[0] + n[1] * view[1] + n[2] * view[2]
        proj.append(p2)
        depth.append(d)
        front.append(0 if nv < -1e-5 else (1 if nv < 0.15 else 2))
    xs = [p[0] for t in proj for p in t]
    ys = [p[1] for t in proj for p in t]
    top_pad = 90 if title else 0
    sx = (width - 2 * margin) / max(max(xs) - min(xs), 1e-6)
    sy = (width - 2 * margin) / max(max(ys) - min(ys), 1e-6)
    s = min(sx, sy)
    ox = margin - min(xs) * s
    oy = margin - min(ys) * s
    height = int((max(ys) - min(ys)) * s + 2 * margin + top_pad)
    if layers is not None:
        order = sorted(range(len(proj)), key=lambda i: (layers[i], front[i], depth[i]))
    else:
        order = sorted(range(len(proj)), key=lambda i: (front[i], depth[i]))
    o = ["<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>"
         % (width, height, width, height),
         "<defs><linearGradient id='bg' x1='0' y1='0' x2='0' y2='1'>"
         "<stop offset='0' stop-color='#10151d'/><stop offset='1' stop-color='#070a0e'/>"
         "</linearGradient></defs>",
         "<rect width='%d' height='%d' fill='url(#bg)'/>" % (width, height)]
    if title:
        o.append("<text x='%d' y='42' fill='#e8edf2' font-family='DejaVu Sans,Helvetica,Arial,sans-serif' font-size='22' font-weight='700'>%s</text>"
                 % (margin, title))
    if subtitle:
        o.append("<text x='%d' y='68' fill='#9fb0bf' font-family='DejaVu Sans,Helvetica,Arial,sans-serif' font-size='14'>%s</text>"
                 % (margin, subtitle))
    for i in order:
        t = tris[i]
        n = normal(t)
        lam = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        base = 0.20 + 0.80 * lam
        key = palette[i] if palette else (196, 205, 218)
        col = (min(255, int(key[0] * base) + 14), min(255, int(key[1] * base) + 16), min(255, int(key[2] * base) + 18))
        pts = " ".join("%.1f,%.1f" % (p[0] * s + ox, height - (p[1] * s + oy)) for p in proj[i])
        o.append("<polygon points='%s' fill='#%02x%02x%02x' stroke='#%02x%02x%02x' stroke-width='0.45' stroke-linejoin='round'/>"
                 % (pts, col[0], col[1], col[2], col[0], col[1], col[2]))
    o.append("</svg>")
    open(path, "w").write("\n".join(o))
    return path
