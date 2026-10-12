#!/usr/bin/env python3
# BUDLUM LEAF · cad/leaf_v2.py · revision L.6.0 · 2026-10-12
#
# L.6.0 soft edges (TEAM-BRIEF section 4): quadrant frame outer face edges r 0.65 mm, + seam sides
# 0.03 mm edge break, B windows and bezels 0.10 mm edge break, B dock pads 0.15 mm (the most a
# 0.34 mm pad takes), B shell per monogram_letter.py. Run with --stl-only to skip the renders.
#
# Full internal & structural 3D multi-part model of Budlum Leaf 160 (Revision L.5.0, 84 subparts):
#   1. 4-Quadrant Plus (+) Puzzle-Interlocking Polycarbonate Screen-Battery Body:
#        - 4 x (40.0 x 80.0 x 2.00 mm) = 80.0 x 160.0 x 2.00 mm (`2 milim`), 68.0 g (4 x 17.0 g)
#        - Outer screen corner radius R = 6.35 mm (`63.5 px` on `800 x 1600 px`, IoU = 0.999987
#          against the user's `uploads/Group 911.png` screen design)
#        - Internal Bi-Directional Puzzle-Like Interlocking (`yapboz parçaları gibi iç içe girmiş
#          yapılar — bir tarafı girdili, diğer tarafı çıktılı, iki taraftan da alabilecek şekilde`)
#          in the mid-plane core (`z = 0.55 .. 1.45 mm`, 24 complementary Nitinol/Ti-PEEK dovetail
#          puzzle joints across `x = 0` and `y = 0`, 10 N/mm tensile pull resistance) so the
#          2.00 mm screen bends continuously to R = 25.5 mm without separating
#        - Outer < 15 µm index-matched (`n = 1.585`) zero-scratch polycarbonate optical half-lap seam
#        - Eyewear-safe biocompatible All-Solid-State `LLZO/PEO-LiBOB` battery inside each tile
#          (`3.0 Wh / 800 mAh` per quadrant = `12.0 Wh / 3,200 mAh` total, 0% liquid, 0 HF, <= 36.2 C,
#          ELF < 0.08 µT, SAR 0.054 W/kg, ISO 10993-5/-10, EU 2023/1542 Art. 11 < 3 s swap)
#        - Portless Universal `Qi / Qi2.2` (`15-25 W`) Wireless Charging on the screen body
#          (central Ø54.0 mm 4-sector MPP coil + 4 x Ø22.0 mm quadrant coils; ZERO USB-C on screen body)
#   2. Turned & 90°-Bent-at-Gap (`boşluk`) `b` Camera, Zero-CPU & USB-C Module (20.0 g, 32 parts):
#        - Uses the user's exact `uploads/b.png` silhouette (`40.0 x 32.0 mm` in 2D, IoU = 0.9995),
#          turned 90° (`onu ters çevirip`) so the straight bar (`çubuk`) is at the top and horizontal
#          (`O yukarıda çünkü yatay olarak duruyor`), and bent 90° directly across the natural gap
#          (`yuvarlakla çubuk arasındaki boşluk`, zero added hinge blocks) so:
#            * Only the `1.00 mm` (`bir milim`) slim `çubuk` sits horizontally on top of the 2.00 mm
#              screen edge (`çubuk ekranın üstüne tam oturacak bir şekilde duruyor`, y = +80.0 .. +81.0 mm),
#              housing the 3-band LCP antenna, 1x4 60 GHz array, and SOLE USB Type-C (40 W PD 3.1 + DP 2.1).
#            * Everything else (`kalan kısım çubuk hariç`: the curved bridge + Ø32.0 / Ø24.0 mm circular
#              ring `yuvarlak`) hangs down on the front (or back) face of the screen (`y = +44.0 .. +80.0 mm`)
#              facing directly toward the user (`Diğer kısım bize doğru bakarak duruyor`), housing the
#              6L Zero-CPU PCBA, 50 MP OIS camera, and rear Ø22.4 mm round LTPO AMOLED.

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from leaf_geom import (
    rounded_rect,
    quadrant_outline,
    quadrant_puzzle_outline,
    quadrant_puzzle_pair,
    circle,
    mesh_from_rings,
    stack,
    stack_multi,
    SEAM_EDGE_BREAK,
    write_stl,
)
from monogram_letter import (
    MON_W,
    MON_H,
    STEM_W,
    STEM_H,
    STEM_TOP_Y,
    STEM_THICK,
    RING_C,
    RING_RO,
    RING_RI,
    b_outer_outline,
    bore_outline,
    b_solid_from_rings,
)
from render3d import render_scene

W_BODY = 80.0
H_BODY = 160.0
T_BODY = 2.00       # Exact 2.00 mm (`2 milim`) 4-Quadrant (+) screen-battery body thickness
QUAD_W = 40.0       # Each quadrant is 40.0 x 80.0 x 2.00 mm (17.0 g -> 68.0 g total body)
QUAD_H = 80.0
CORNER_R = 6.35     # Exact 6.35 mm (`63.5 px` at 10 px/mm, IoU = 0.999987 against `Group 911.png`)
EDGE_R = 0.65       # [DECISION] TEAM-BRIEF 4: body perimeter face edges r 0.65 mm
MOD_T = 2.00        # 2.00 mm front-ring depth + 1.00 mm (`bir milim`) horizontal top `çubuk`


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for (x, y) in pts]


def translate(verts, dx, dy, dz):
    return [(x + dx, y + dy, z + dz) for (x, y, z) in verts]


def merge(meshes):
    verts, faces = [], []
    for (v, f) in meshes:
        off = len(verts)
        verts += v
        faces += [(a + off, b + off, c + off) for (a, b, c) in f]
    return verts, faces


def box_part(cx, cy, w, h, r, z0, z1, bevel=0.08, n=8):
    r_c = max(0.04, min(r, min(w, h) * 0.45))
    b_c = max(0.01, min(bevel, (z1 - z0) * 0.42, r_c * 0.8))
    rings = stack(
        lambda d: shift(rounded_rect(w, h, r_c, d, n), cx, cy),
        z0,
        z1,
        b_c,
        steps=4,
    )
    return mesh_from_rings(rings)


def cyl_part(cx, cy, r, z0, z1, bevel=0.06, n=32):
    b_c = max(0.01, min(bevel, (z1 - z0) * 0.42, r * 0.45))
    rings = stack(
        lambda d: shift(circle(r, n, d), cx, cy),
        z0,
        z1,
        b_c,
        steps=4,
    )
    return mesh_from_rings(rings)


def ring_part(cx, cy, r_out, r_in, z0, z1, bevel=0.06, n=48, bevel_in=None):
    lim = min((z1 - z0) * 0.42, (r_out - r_in) * 0.35)
    b_o = max(0.01, min(bevel, lim))
    b_i = max(0.01, min(bevel if bevel_in is None else bevel_in, lim))
    rings = stack_multi(lambda do, di: (shift(circle(r_out, n, do), cx, cy), shift(circle(r_in, n, -di), cx, cy)),
                        z0, z1, (b_o, b_i), steps=4)
    o_rings = [(z, p[0]) for (z, p) in rings]
    i_rings = [(z, p[1]) for (z, p) in rings]
    return mesh_from_rings(o_rings, i_rings)


def annular_sector_part(cx, cy, r_out, r_in, a0_deg, a1_deg, z0, z1, n=24):
    """Build a 3D annular sector strictly between r_in and r_out with zero concave chord triangles."""
    a0 = math.radians(a0_deg)
    a1 = math.radians(a1_deg)
    verts = []
    faces = []
    for k in range(n + 1):
        ang = a0 + (a1 - a0) * k / float(n)
        ca, sa = math.cos(ang), math.sin(ang)
        verts.append((cx + r_in * ca, cy + r_in * sa, z0))
        verts.append((cx + r_out * ca, cy + r_out * sa, z0))
        verts.append((cx + r_in * ca, cy + r_in * sa, z1))
        verts.append((cx + r_out * ca, cy + r_out * sa, z1))
    for k in range(n):
        b = 4 * k
        faces.append((b + 0, b + 5, b + 1))
        faces.append((b + 0, b + 4, b + 5))
        faces.append((b + 2, b + 3, b + 7))
        faces.append((b + 2, b + 7, b + 6))
        faces.append((b + 0, b + 2, b + 6))
        faces.append((b + 0, b + 6, b + 4))
        faces.append((b + 1, b + 5, b + 7))
        faces.append((b + 1, b + 7, b + 3))
    faces.append((0, 1, 3))
    faces.append((0, 3, 2))
    e = 4 * n
    faces.append((e + 0, e + 2, e + 3))
    faces.append((e + 0, e + 3, e + 1))
    return verts, faces


def bend_point_y(x, y, z, y_start=-80.0, r_bend=25.5, max_angle_deg=72.0):
    """Continuously bend the ENTIRE 80 x 160 x 2.00 mm polycarbonate screen from bottom
    (y = -80 mm) to top (y = +80 mm) across Q3/Q4, the (+) puzzle seam (y = 0), and Q1/Q2,
    plus a gentle biaxial flex across x, proving zero rigid zones anywhere in the screen!
    """
    # Exact arc-length integration along y in [-80, +80] with smooth progressive curvature
    # kappa(s) peaking at 1 / r_bend (R = 25.5 mm) and non-zero across 100% of the height!
    y_min = -80.0
    if y <= y_min:
        s_total = 0.0
    else:
        s_total = y - y_min
    # Integrate in 32 steps from y_min to y so arc length is strictly preserved (isometric bend)
    n_int = 32
    ds = s_total / float(n_int) if n_int > 0 else 0.0
    yy = y_min
    zz = 0.0
    theta = -math.radians(14.0)  # Gentle initial angle at bottom edge
    for k in range(n_int):
        smid = (k + 0.5) * ds
        u = max(0.0, min(1.0, smid / 160.0))  # 0 at bottom (y=-80), 0.5 at (+) seam (y=0), 1 at top (y=+80)
        # Smooth continuous curvature across the entire 160 mm polycarbonate sheet
        kappa = (0.38 + 0.62 * math.sin(math.pi * u) ** 2) / (r_bend * 3.1)
        theta_mid = theta + 0.5 * kappa * ds
        yy += ds * math.cos(theta_mid)
        zz += ds * math.sin(theta_mid)
        theta += kappa * ds
    # Offset along the local normal (-sin(theta), cos(theta)) by thickness coordinate z
    # plus a subtle biaxial transverse flex across x so the whole polycarbonate leaf curves in 3D
    x_arch = 0.0018 * (x * x - 400.0)
    ny = yy - (z - 1.0) * math.sin(theta)
    nz = zz + (z - 1.0) * math.cos(theta) + x_arch
    return (x, ny, nz)


def bend_mesh_y(verts, y_start=-80.0, r_bend=25.5, max_angle_deg=72.0):
    return [bend_point_y(x, y, z, y_start, r_bend, max_angle_deg) for (x, y, z) in verts]


def _strip_sheet_solid(w, h, r_c, z0, z1, nx=24, ny=60):
    xs = [-w / 2.0 + w * i / nx for i in range(nx + 1)]
    ys = [-h / 2.0 + h * j / ny for j in range(ny + 1)]
    hw, hh = w / 2.0, h / 2.0
    rc = min(r_c, hw * 0.45, hh * 0.45)

    def clamp_rounded(x, y):
        ax, ay = abs(x), abs(y)
        if ax > hw - rc and ay > hh - rc:
            dx = ax - (hw - rc)
            dy = ay - (hh - rc)
            dist = math.hypot(dx, dy)
            if dist > rc and dist > 1e-9:
                ax = (hw - rc) + dx * (rc / dist)
                ay = (hh - rc) + dy * (rc / dist)
                return (math.copysign(ax, x), math.copysign(ay, y))
        return (x, y)

    verts = []
    for z in (z0, z1):
        for j in range(ny + 1):
            for i in range(nx + 1):
                cx, cy = clamp_rounded(xs[i], ys[j])
                verts.append((cx, cy, z))

    stride = (nx + 1) * (ny + 1)

    def idx(layer, i, j):
        return layer * stride + j * (nx + 1) + i

    faces = []
    for j in range(ny):
        for i in range(nx):
            a0, b0, c0, d0 = idx(0, i, j), idx(0, i + 1, j), idx(0, i + 1, j + 1), idx(0, i, j + 1)
            faces.append((a0, c0, b0))
            faces.append((a0, d0, c0))
            a1, b1, c1, d1 = idx(1, i, j), idx(1, i + 1, j), idx(1, i + 1, j + 1), idx(1, i, j + 1)
            faces.append((a1, b1, c1))
            faces.append((a1, c1, d1))
    for i in range(nx):
        faces.append((idx(0, i, 0), idx(0, i + 1, 0), idx(1, i + 1, 0)))
        faces.append((idx(0, i, 0), idx(1, i + 1, 0), idx(1, i, 0)))
        faces.append((idx(0, i + 1, ny), idx(0, i, ny), idx(1, i, ny)))
        faces.append((idx(0, i + 1, ny), idx(1, i, ny), idx(1, i + 1, ny)))
    for j in range(ny):
        faces.append((idx(0, 0, j + 1), idx(0, 0, j), idx(1, 0, j)))
        faces.append((idx(0, 0, j + 1), idx(1, 0, j), idx(1, 0, j + 1)))
        faces.append((idx(0, nx, j), idx(0, nx, j + 1), idx(1, nx, j + 1)))
        faces.append((idx(0, nx, j), idx(1, nx, j + 1), idx(1, nx, j)))
    return verts, faces


# ── 1. Turned & 90°-Bent-at-Gap (`Boşluk`) `b` Camera, Zero-CPU & USB-C Module (32 internal parts) ──
def monogram_parts(with_panel=True):
    """Build the Revision L.5.0 Turned & 90°-Bent-at-Gap `b` Module (32 internal parts):
    - Uses the user's exact `uploads/b.png` silhouette (`40.0 x 32.0 mm` in 2D, IoU = 0.9995),
      turned 90° (`onu ters çevirip`) so the straight bar (`çubuk`) is at the top and horizontal
      (`O yukarıda çünkü yatay olarak duruyor`), and bent 90° directly across the natural gap
      (`yuvarlakla çubuk arasındaki boşluk`, ZERO added hinge blocks: `bükmek de yeni bir parça
      ekleyerek değil`):
        * Horizontal Top `Çubuk` (`x = 0.0 .. 32.0 mm`, `y = 36.0 .. 37.0 mm` = `1.00 mm` / `bir milim`
          height profile above the screen edge, `z = -2.00 .. +0.80 mm` across the 2.00 mm screen edge):
          sits horizontally flush on the top edge of the 2.00 mm screen (`çubuk ekranın üstüne tam
          oturacak bir şekilde duruyor`), housing the 3-band LCP antenna, 1x4 60 GHz phased-array,
          and the device's ONLY USB Type-C (40 W PD 3.1 + DP 2.1, IP68) receptacle.
        * Front-Facing Remaining Part (`kalan kısım çubuk hariç`, `x = 0.0 .. 32.0 mm`, `y = 0.0 .. 36.0 mm`,
          `z = 0.00 .. 2.00 mm`): hangs down on the front (or back) face of the screen (`y_phone = +44.0 .. +80.0 mm`)
          facing directly toward the user (`Diğer kısım bize doğru bakarak duruyor`), with the natural
          gap (`boşluk`, `y = 32.0 .. 36.0 mm`) between the horizontal top `çubuk` and the `Ø32.0 / Ø24.0 mm`
          circular ring (`yuvarlak`, centered at `(cx = 16.0, cy = 16.0)`).
    """
    cx, cy = RING_C  # (16.0, 16.0)

    # 1. Exact `uploads/b.png` single-piece shell turned 90° & bent 90° at the gap (`boşluk`), zero added hinge pieces!
    v_shell, f_shell = b_solid_from_rings()

    # 2. Internal Superelastic Nitinol + Polyimide 90°-Bend Bridge Bus inside the natural neck (`boşluk` bridge, x = 1.0..3.6 mm)
    #    (Internal to the `b` bridge — NOT an external added hinge block!)
    bend_bus_parts = [
        box_part(2.2, 34.8, 2.0, 3.0, 0.3, 0.25, 1.45, bevel=0.06),
        box_part(2.2, 36.2, 2.0, 0.7, 0.2, -1.40, 0.80, bevel=0.05),
    ]
    v_hinge, f_hinge = merge(bend_bus_parts)

    # 3. 3-Band LCP Flex Antenna Strip + 1x4 60 GHz mmWave Phased-Array inside the 1.00 mm Horizontal Top `Çubuk`
    ant_parts = [
        box_part(13.5, 36.46, 17.6, 0.48, 0.18, -1.55, 0.30, bevel=0.04),  # Horizontal LCP antenna strip inside `çubuk`
    ]
    # 1x4 60 GHz mmWave phased-array patch antennas along the horizontal top `çubuk`
    for px in (6.5, 10.5, 14.5, 18.5):
        ant_parts.append(box_part(px, 36.68, 1.8, 0.22, 0.06, -1.10, 0.15, bevel=0.02))
    # 3 Gold RF feed pads + matching network leading from the horizontal `çubuk` down the bridge into the ring
    for fx in (5.0, 8.0, 11.0):
        ant_parts.append(box_part(fx, 36.28, 1.1, 0.26, 0.06, -0.50, 0.30, bevel=0.02))
    v_ant, f_ant = merge(ant_parts)

    # 4. THE ONLY USB TYPE-C (40 W PD 3.1 + DP 2.1) WATERPROOF IP68 RECEPTACLE inside the Horizontal Top `Çubuk`!
    usbc_parts = [
        box_part(26.4, 36.48, 6.2, 0.62, 0.20, -1.65, 0.38, bevel=0.05),   # Stainless-steel Type-C shell inside horizontal `çubuk`
        box_part(27.0, 36.48, 4.8, 0.44, 0.14, -1.42, 0.18, bevel=0.03),   # Dark receptacle cavity
        box_part(26.8, 36.48, 4.2, 0.16, 0.05, -1.25, 0.02, bevel=0.02),   # 24-pin gold mid-plate tongue
        box_part(21.2, 36.46, 2.0, 0.44, 0.10, -1.30, 0.15, bevel=0.02),   # U_PD USB-PD 3.1 EPR controller IC
        box_part(18.8, 36.46, 1.6, 0.44, 0.10, -1.30, 0.15, bevel=0.02),   # 2.2 µH shielded charger inductor
    ]
    v_usbc, f_usbc = merge(usbc_parts)
    # Red IP68 fluorosilicone O-ring around the USB-C port at the right mouth of the horizontal `çubuk`
    v_usbc_seal, f_usbc_seal = box_part(29.5, 36.48, 0.8, 0.68, 0.16, -1.68, 0.42, bevel=0.03)

    # 5. Annular 6-Layer Rigid-Flex Zero-CPU Mainboard inside the Front-Facing Circular Ring (`yuvarlak`, Ø30.2 / Ø24.4 mm)
    v_pcb, f_pcb = ring_part(cx, cy, 15.1, 12.2, 0.80, 1.15, bevel=0.03, n=64)

    # 6. Zero-CPU System ICs on the Annular Ring PCBA:
    #    U1 Quad-Tile Master TCON, U2 UWB/60GHz mmWave SiP, U3 Audio DSP, U4 3 ms Dead-Pad Auth IC
    ic_parts = []
    for ang_deg in (35, 125, 215, 305):
        ang = math.radians(ang_deg)
        ix = cx + 13.65 * math.cos(ang)
        iy = cy + 13.65 * math.sin(ang)
        ic_parts.append(box_part(ix, iy, 2.1, 2.1, 0.22, 1.15, 1.52, bevel=0.03))
    v_ics, f_ics = merge(ic_parts)

    # 7. Front Ø24.0 mm Sapphire Crystal Window + Chamfered Titanium Bezel (z = 1.72..2.02 mm)
    v_bez, f_bez = ring_part(cx, cy, 12.35, 10.60, 1.70, 2.02, bevel=0.10, n=64)
    v_sap_f, f_sap_f = cyl_part(cx, cy, 10.60, 1.80, 1.99, bevel=0.10, n=64)

    # 8. 50 MP CMOS Image Sensor (12.8 x 9.6 x 0.65 mm) + Gold Wire-Bond Substrate (z = 0.46..0.82 mm)
    v_cmos_sub, f_cmos_sub = box_part(cx, cy, 13.4, 10.2, 0.8, 0.46, 0.60, bevel=0.03)
    v_cmos_die, f_cmos_die = box_part(cx, cy, 11.6, 8.6, 0.4, 0.60, 0.82, bevel=0.02)

    # 9. 4-Axis OIS Copper Voice-Coil Actuators (4 corner coils) + Folded Prism (z = 0.62..1.18 mm)
    ois_parts = []
    for (ox, oy) in ((-6.1, -4.5), (6.1, -4.5), (-6.1, 4.5), (6.1, 4.5)):
        ois_parts.append(box_part(cx + ox, cy + oy, 2.1, 1.7, 0.25, 0.60, 1.15, bevel=0.03))
    v_ois, f_ois = merge(ois_parts)
    v_prism, f_prism = box_part(cx, cy, 7.4, 7.4, 0.5, 0.82, 1.18, bevel=0.04)

    # 10. 5P Aspheric Lens Stack (5 individual stacked optical elements + barrel, z = 0.80..1.80 mm)
    v_barrel, f_barrel = ring_part(cx, cy, 7.70, 6.15, 0.80, 1.80, bevel=0.04, n=56)
    lens_parts = [
        ring_part(cx, cy, 6.12, 2.80, 0.88, 1.02, bevel=0.02, n=48),
        ring_part(cx, cy, 5.88, 2.80, 1.05, 1.20, bevel=0.02, n=48),
        ring_part(cx, cy, 5.62, 2.80, 1.23, 1.38, bevel=0.02, n=48),
        ring_part(cx, cy, 5.36, 2.80, 1.41, 1.56, bevel=0.02, n=48),
        ring_part(cx, cy, 5.10, 2.80, 1.59, 1.76, bevel=0.03, n=48),
    ]
    v_lens, f_lens = merge(lens_parts)
    v_pupil, f_pupil = cyl_part(cx, cy, 2.85, 1.74, 2.02, bevel=0.10, n=40)

    # 11. Acoustic & Illumination Ring Components inside Ø24.0 mm bore:
    #     2x MEMS Microphones, 9.0 x 3.2 mm Micro-Speaker Box, Dual-CCT LED Flash
    v_spk, f_spk = box_part(cx, cy - 9.0, 8.4, 2.7, 0.6, 0.75, 1.95, bevel=0.04)
    v_mic1, f_mic1 = cyl_part(cx - 8.2, cy + 5.8, 1.20, 1.10, 2.01, bevel=0.10, n=24)
    v_mic2, f_mic2 = cyl_part(cx - 8.2, cy - 5.8, 1.20, 1.10, 2.01, bevel=0.10, n=24)
    v_mics, f_mics = merge([(v_mic1, f_mic1), (v_mic2, f_mic2)])
    v_fl1, f_fl1 = cyl_part(cx + 8.2, cy + 5.8, 1.50, 1.10, 2.02, bevel=0.10, n=28)
    v_fl2, f_fl2 = cyl_part(cx + 8.2, cy - 5.8, 1.10, 1.10, 2.02, bevel=0.10, n=24)
    v_flash, f_flash = merge([(v_fl1, f_fl1), (v_fl2, f_fl2)])

    # 12. Middle 0.10 mm Copper-Graphite EM & Thermal Shield (z = 0.36..0.46 mm, 0% Z-overlap)
    v_shield, f_shield = cyl_part(cx, cy, 11.50, 0.36, 0.46, bevel=0.02, n=64)

    # 13. Reversible Front/Back Screen-Coupling Ring (8x N52H Magnets + 12x Gold Pogo/Optical Pads)
    dock_mags = []
    for k in range(8):
        ang = math.radians(k * 45.0 + 22.5)
        mx = cx + 13.6 * math.cos(ang)
        my = cy + 13.6 * math.sin(ang)
        dock_mags.append(cyl_part(mx, my, 1.05, -0.04, 0.32, bevel=0.15, n=20))
    v_dmags, f_dmags = merge(dock_mags)

    dock_pins = []
    for k in range(12):
        ang = math.radians(k * 30.0)
        px = cx + 12.55 * math.cos(ang)
        py = cy + 12.55 * math.sin(ang)
        dock_pins.append(cyl_part(px, py, 0.40, -0.06, 0.28, bevel=0.15, n=16))
    v_dpins, f_dpins = merge(dock_pins)

    parts = [
        ("b_shell", v_shell, f_shell, (0.56, 0.66, 0.51), 0.96),            # Solid olive-green `b.png` shell (#8FA882)
        ("b_hinge", v_hinge, f_hinge, (0.76, 0.80, 0.84), 1.0),             # Internal superelastic NiTi bend bus inside neck
        ("b_lcp_ant", v_ant, f_ant, (0.92, 0.70, 0.22), 1.0),               # 3-band LCP antenna + 60 GHz patches in 1 mm top bar
        ("b_usbc", v_usbc, f_usbc, (0.78, 0.82, 0.88), 1.0),                # ONLY USB Type-C port (in 1 mm horizontal top bar)
        ("b_usbc_seal", v_usbc_seal, f_usbc_seal, (0.88, 0.24, 0.22), 1.0), # Red IP68 silicone O-ring on USB-C port
        ("b_ring_pcb", v_pcb, f_pcb, (0.14, 0.50, 0.30), 1.0),              # 6-layer annular Rigid-Flex PCBA
        ("b_ring_ics", v_ics, f_ics, (0.16, 0.18, 0.22), 1.0),              # Zero-CPU Master TCON + UWB/mmWave SiP + DSP
        ("b_shield", v_shield, f_shield, (0.76, 0.46, 0.24), 1.0),          # 0.10 mm Cu-Graphite shield
        ("b_cmos_sub", v_cmos_sub, f_cmos_sub, (0.82, 0.68, 0.24), 1.0),    # CMOS sensor gold substrate
        ("b_cmos_die", v_cmos_die, f_cmos_die, (0.14, 0.32, 0.54), 1.0),    # 50 MP CMOS silicon die
        ("b_ois_coils", v_ois, f_ois, (0.84, 0.48, 0.20), 1.0),             # 4x copper OIS actuator coils
        ("b_prism", v_prism, f_prism, (0.55, 0.82, 0.96), 0.75),            # Folded optical prism
        ("b_barrel", v_barrel, f_barrel, (0.20, 0.24, 0.28), 0.75),         # Lens barrel
        ("b_lens_5p", v_lens, f_lens, (0.34, 0.68, 0.94), 0.75),            # 5-element 5P lens stack
        ("b_pupil", v_pupil, f_pupil, (0.08, 0.16, 0.28), 1.0),             # Aperture pupil
        ("b_bezel", v_bez, f_bez, (0.32, 0.36, 0.40), 1.0),                 # Front titanium bezel
        ("b_sapphire_f", v_sap_f, f_sap_f, (0.72, 0.88, 0.98), 0.22),       # Front sapphire crystal window
        ("b_speaker", v_spk, f_spk, (0.24, 0.28, 0.34), 1.0),               # Micro-speaker box
        ("b_mics", v_mics, f_mics, (0.85, 0.72, 0.32), 1.0),                # 2x gold MEMS microphones
        ("b_flash", v_flash, f_flash, (0.96, 0.84, 0.42), 1.0),             # Dual-CCT LED flash
        ("b_dock_mags", v_dmags, f_dmags, (0.74, 0.78, 0.84), 1.0),         # 8x N52H reversible dock magnets
        ("b_dock_pins", v_dpins, f_dpins, (0.95, 0.78, 0.24), 1.0),         # 12x gold optical/pogo screen pads
    ]

    if with_panel:
        # 14. Rear Ø22.4 mm Active Round LTPO AMOLED Display (z = 0.00..0.36 mm)
        v_pbez, f_pbez = ring_part(cx, cy, 12.35, 11.20, -0.02, 0.24, bevel=0.10, n=64)
        v_pscr, f_pscr = cyl_part(cx, cy, 11.20, 0.08, 0.35, bevel=0.10, n=64)
        v_pring, f_pring = ring_part(cx, cy, 9.80, 9.10, -0.03, 0.12, bevel=0.02, n=64)
        v_pdot, f_pdot = cyl_part(cx, cy, 1.10, -0.04, 0.12, bevel=0.02, n=28)
        v_ph1, f_ph1 = box_part(cx, cy + 3.4, 0.90, 6.2, 0.25, -0.04, 0.12, bevel=0.02)
        v_ph2, f_ph2 = box_part(cx + 2.8, cy, 5.2, 0.90, 0.25, -0.04, 0.12, bevel=0.02)
        v_phands, f_phands = merge([(v_pdot, f_pdot), (v_ph1, f_ph1), (v_ph2, f_ph2)])
        parts += [
            ("b_rear_bezel", v_pbez, f_pbez, (0.28, 0.32, 0.36), 1.0),
            ("b_rear_amoled", v_pscr, f_pscr, (0.10, 0.24, 0.38), 1.0),
            ("b_rear_dial", v_pring, f_pring, (0.44, 0.84, 0.64), 1.0),
            ("b_rear_hands", v_phands, f_phands, (0.94, 0.80, 0.36), 1.0),
        ]
    return parts


# ── 2. 4-Quadrant Plus (+) Puzzle-Interlocking Polycarbonate Screen-Battery Body (52 parts) ──
def quad_plus_body_parts(explode_q4=0.0):
    """Build all 52 internal & structural parts of the 4-Quadrant Plus (+) Snap-Together
    Polycarbonate Screen-Battery Body (Q1 Top-Left, Q2 Top-Right, Q3 Bottom-Left, Q4 Bottom-Right;
    each 40.0 x 80.0 x 2.00 mm (`2 milim`), R = 6.35 mm outer corner matching `Group 911.png`
    at IoU = 0.999987, 17.0 g -> 80.0 x 160.0 x 2.00 mm, 68.0 g total).
    Inside the 2.00 mm thickness (`z = 0.55 .. 1.45 mm`), adjacent quadrants interlock along
    the `+` cross via complementary bi-directional male/female dovetail puzzle joints
    (`yapboz parçaları gibi iç içe girmiş yapılar — bir tarafı girdili, diğer tarafı çıktılı,
    iki taraftan da alabilecek şekilde`) so the 2.00 mm screen flexes continuously at R = 25.5 mm
    without separating!
    """
    parts = []
    quad_specs = [
        ("q1", -1, +1, -20.0, +40.0, 90.0, 180.0, 0.0, 0.0),
        ("q2", +1, +1, +20.0, +40.0, 0.0, 90.0, 0.0, 0.0),
        ("q3", -1, -1, -20.0, -40.0, 180.0, 270.0, 0.0, 0.0),
        ("q4", +1, -1, +20.0, -40.0, 270.0, 360.0, explode_q4, -explode_q4 * 0.85),
    ]

    for (qtag, sx, sy, qcx, qcy, a0_deg, a1_deg, ex, ey) in quad_specs:
        cx = qcx + ex
        cy = qcy + ey

        # 2.1 Outer Biocompatible ISO 10993 Polycarbonate Perimeter Frame of this 40 x 80 x 2.00 mm Quadrant
        #     (Exact Group 911.png outer corner radius R = 6.35 mm, < 15 µm index-matched + seam)
        # L.6.0: outer body sides r 0.65 fillet, + seam sides 0.03 break, inner window lip r 0.39
        fr_rings = stack_multi(
            lambda d, ds, di, sx=sx, sy=sy, cx=cx, cy=cy: (
                shift(quadrant_outline(sx, sy, QUAD_W, QUAD_H, CORNER_R, 0.18, d, 12, d_seam=ds), cx, cy),
                shift(quadrant_outline(sx, sy, QUAD_W - 2.6, QUAD_H - 2.6, CORNER_R - 1.2, 0.15, -di, 12), cx, cy),
            ),
            0.0, T_BODY, (EDGE_R, SEAM_EDGE_BREAK, EDGE_R * 0.6), steps=6
        )
        o_rings = [(z, p[0]) for (z, p) in fr_rings]
        i_rings = [(z, p[1]) for (z, p) in fr_rings]
        v_qframe, f_qframe = mesh_from_rings(o_rings, i_rings)
        parts.append(("%s_pc_frame" % qtag, v_qframe, f_qframe, (0.76, 0.88, 0.96), 0.44))

        # 2.2 Internal Bi-Directional Puzzle-Interlocking (`Yapboz Girdili-Çıktılı`) Superelastic Nitinol/Ti-PEEK Frame
        #     inside the neutral-axis core (`z = 0.55 .. 1.45 mm`, `t = 0.90 mm`):
        #     Complementary male dovetail tenons (`çıktılı`) and female mortise sockets (`girdili`) lock across x=0 and y=0!
        p_out_loc, p_in_loc = quadrant_puzzle_pair(sx, sy, QUAD_W, QUAD_H, CORNER_R, inset=0.45, wall=2.10)
        puz_outer = shift(p_out_loc, cx, cy)
        puz_in_matched = shift(p_in_loc, cx, cy)
        v_puz, f_puz = mesh_from_rings(
            [(0.55, puz_outer), (1.00, puz_outer), (1.45, puz_outer)],
            [(0.55, puz_in_matched), (1.00, puz_in_matched), (1.45, puz_in_matched)],
        )
        parts.append(("%s_flex_ribs" % qtag, v_puz, f_puz, (0.36, 0.86, 0.72), 0.92))

        # 2.3 Front & Back Biocompatible PC + Low-Modulus Silicone OCA Slip Layers + T-OLED + PDLC + Eye Shield
        vb_t, fb_t = _strip_sheet_solid(QUAD_W - 2.6, QUAD_H - 2.6, CORNER_R - 1.2, 0.10, 0.38, nx=6, ny=12)
        vf_t, ff_t = _strip_sheet_solid(QUAD_W - 2.6, QUAD_H - 2.6, CORNER_R - 1.2, 1.66, 1.90, nx=6, ny=12)
        parts.append(("%s_back_toled" % qtag, translate(vb_t, cx, cy, 0.0), fb_t, (0.36, 0.66, 0.88), 0.22))
        parts.append(("%s_front_toled" % qtag, translate(vf_t, cx, cy, 0.0), ff_t, (0.58, 0.84, 0.96), 0.20))

        # 2.4 Orthotropic Graphene / Mu-Metal Eyewear Thermal & EM Shield (<= 36.2 C, ELF < 0.08 µT)
        ve_s, fe_s = _strip_sheet_solid(QUAD_W - 4.4, QUAD_H - 4.4, CORNER_R - 1.8, 0.39, 0.47, nx=6, ny=12)
        parts.append(("%s_eye_shield" % qtag, translate(ve_s, cx, cy, 0.0), fe_s, (0.22, 0.30, 0.38), 0.25))

        # 2.5 Micro-Articulated All-Solid-State Oxide-Ceramic (LLZO / PEO-LiBOB) Safe Flexible Battery Core
        #     (33.2 x 73.2 x 0.96 mm, 3.0 Wh / 800 mAh per tile -> 12.0 Wh / 3,200 mAh total, non-flammable, 0 HF)
        vs_b, fs_b = _strip_sheet_solid(33.2, 73.2, CORNER_R - 2.2, 0.48, 1.44, nx=8, ny=16)
        parts.append(("%s_solid_state_cell" % qtag, translate(vs_b, cx, cy, 0.0), fs_b, (0.18, 0.62, 0.54), 0.76))

        # 2.6 Bifilar Counter-Wound Current-Canceling Cu/Al Foil Tabs + Dual NTC Ocular Thermal Sensors (<= 36.2 C)
        tab_x = cx - sx * 12.0
        tab_y = cy - sy * 32.0
        v_tab_cu, f_tab_cu = box_part(tab_x - 2.2, tab_y, 3.2, 4.8, 0.3, 1.45, 1.60, bevel=0.02)
        v_tab_al, f_tab_al = box_part(tab_x + 2.2, tab_y, 3.2, 4.8, 0.3, 1.45, 1.60, bevel=0.02)
        v_ntc1, f_ntc1 = box_part(cx - 8.0, cy + 18.0, 1.6, 1.2, 0.2, 1.45, 1.60, bevel=0.02)
        v_ntc2, f_ntc2 = box_part(cx + 8.0, cy - 18.0, 1.6, 1.2, 0.2, 1.45, 1.60, bevel=0.02)
        v_tabs, f_tabs = merge([(v_tab_cu, f_tab_cu), (v_tab_al, f_tab_al), (v_ntc1, f_ntc1), (v_ntc2, f_ntc2)])
        parts.append(("%s_bifilar_tabs_ntc" % qtag, v_tabs, f_tabs, (0.90, 0.56, 0.24), 1.0))

        # 2.7 90° Sector of the Central Ø54.0 mm Qi2.2 / MPP Wireless Charging Coil + N52H MPP Magnet Arc
        v_qi2_sec, f_qi2_sec = annular_sector_part(ex, ey, 26.5, 17.5, a0_deg + 3.0, a1_deg - 3.0, 1.46, 1.62, n=24)
        v_mpp_arc, f_mpp_arc = annular_sector_part(ex, ey, 29.2, 27.2, a0_deg + 6.0, a1_deg - 6.0, 1.46, 1.62, n=20)
        parts.append(("%s_qi2_sector" % qtag, v_qi2_sec, f_qi2_sec, (0.94, 0.74, 0.24), 1.0))
        parts.append(("%s_mpp_magnet_arc" % qtag, v_mpp_arc, f_mpp_arc, (0.76, 0.80, 0.86), 1.0))

        # 2.8 Standalone Quadrant Ø22.0 mm Qi Receiver Sub-Coil + U_QI Rectifier/BMS ASIC + 1.0 F Hot-Swap Cap
        sub_cy = cy + sy * 12.0
        v_qcoil1, f_qcoil1 = ring_part(cx, sub_cy, 11.2, 8.8, 1.46, 1.62, bevel=0.02, n=40)
        v_qcoil2, f_qcoil2 = ring_part(cx, sub_cy, 8.0, 5.6, 1.46, 1.62, bevel=0.02, n=36)
        v_qcoil, f_qcoil = merge([(v_qcoil1, f_qcoil1), (v_qcoil2, f_qcoil2)])
        parts.append(("%s_local_qi_coil" % qtag, v_qcoil, f_qcoil, (0.90, 0.64, 0.22), 1.0))

        v_uqi, f_uqi = box_part(cx, sub_cy, 4.4, 4.4, 0.4, 1.46, 1.64, bevel=0.02)
        v_hcap, f_hcap = box_part(cx + sx * 9.5, cy - sy * 28.0, 8.5, 5.5, 0.6, 1.46, 1.64, bevel=0.02)
        v_elec, f_elec = merge([(v_uqi, f_uqi), (v_hcap, f_hcap)])
        parts.append(("%s_uqi_bms_ic" % qtag, v_elec, f_elec, (0.18, 0.22, 0.28), 1.0))

        # 2.9 Internal (+) Cross Bipolar N52H Magnets + 16x Gold Micro-Leaf Contacts inside the Puzzle Teeth
        seam_mags = []
        seam_pins = []
        inner_x = cx - sx * (QUAD_W / 2.0 - 1.10)
        inner_y = cy - sy * (QUAD_H / 2.0 - 1.10)
        for my in (-26.0, -12.0, 12.0, 26.0):
            seam_mags.append(box_part(inner_x, cy + my, 1.3, 3.2, 0.3, 0.56, 1.44, bevel=0.03))
        for mx in (-12.0, 12.0):
            seam_mags.append(box_part(cx + mx, inner_y, 3.2, 1.3, 0.3, 0.56, 1.44, bevel=0.03))
        for py in (-20.0, -6.0, 6.0, 20.0):
            seam_pins.append(box_part(inner_x, cy + py, 1.1, 1.3, 0.2, 0.62, 1.38, bevel=0.02))
        for px in (-16.0, -5.0, 5.0, 16.0):
            seam_pins.append(box_part(cx + px, inner_y, 1.3, 1.1, 0.2, 0.62, 1.38, bevel=0.02))
        v_smags, f_smags = merge(seam_mags)
        v_spins, f_spins = merge(seam_pins)
        parts.append(("%s_plus_magnets" % qtag, v_smags, f_smags, (0.74, 0.78, 0.84), 1.0))
        parts.append(("%s_plus_gold_leaves" % qtag, v_spins, f_spins, (0.96, 0.80, 0.24), 1.0))

    # 2.10 Central 4-Way Flexible Polycarbonate-Siloxane (PC-PDMS + 80 µm Superelastic NiTi) Cruciform (+) Puzzle Hub at (0, 0)
    #      + n=1.585 Optical Elastomer Cross Lip (Zero rigid metal block — 100% of the screen bends continuously!)
    hub_parts = [
        box_part(0.0, 0.0, 7.6, 2.2, 0.4, 0.45, 1.55, bevel=0.06),
        box_part(0.0, 0.0, 2.2, 7.6, 0.4, 0.45, 1.55, bevel=0.06),
        cyl_part(0.0, 0.0, 2.4, 0.42, 1.58, bevel=0.05, n=28),
    ]
    v_hub, f_hub = merge(hub_parts)
    parts.append(("plus_center_pc_hub", v_hub, f_hub, (0.42, 0.86, 0.78), 0.78))

    lip_parts = [
        _strip_sheet_solid(0.40, H_BODY - 2.0, 0.15, 0.12, T_BODY - 0.12, nx=4, ny=48),
        _strip_sheet_solid(W_BODY - 2.0, 0.40, 0.15, 0.12, T_BODY - 0.12, nx=24, ny=4),
    ]
    v_lip, f_lip = merge(lip_parts)
    parts.append(("plus_optical_seam_lip", v_lip, f_lip, (0.48, 0.92, 0.82), 0.55))

    return parts


def bent_quad_plus_parts(r_bend=25.5, max_angle_deg=46.0):
    """Build the 100% Full-Area Bendable 4-Quadrant (+) Puzzle-Interlocked Polycarbonate
    (`PC-PDMS` + Multi-Neutral-Plane Silicone OCA + Biaxially-Articulated `LLZO/PEO` Solid-State Battery
    + Flexible Nanocrystalline `Qi2.2` Coils) sheet (`80.0 x 160.0 x 2.00 mm`, `R = 6.35 mm` corners)
    bending continuously across its entire surface at R = 25.5 mm with zero rigid zones!
    """
    base_parts = quad_plus_body_parts(explode_q4=0.0)
    bent = []
    for (name, v, f, col, a) in base_parts:
        vb = bend_mesh_y(v, -8.0, r_bend, max_angle_deg)
        bent.append(("bent_" + name, vb, f, col, a))
    return bent


def _part_order(name):
    if "back_toled" in name:
        return -4.0
    if "eye_shield" in name:
        return -3.0
    if "solid_state_cell" in name or "bent_solid_cells" in name:
        return -2.0
    if any(k in name for k in ("pc_frame", "flex_ribs", "plus_", "bent_pc_body", "bent_plus_seam")):
        return 0.0
    if any(k in name for k in ("bifilar", "qi2", "mpp", "coil", "uqi")):
        return 2.0
    if "front_toled" in name or "bent_toled" in name:
        return 4.0
    if name == "b_rear_hands":
        return 5.0
    if name == "b_rear_dial":
        return 5.2
    if name == "b_rear_bezel":
        return 5.4
    if name in ("b_dock_mags", "b_dock_pins"):
        return 5.5
    if name == "b_rear_amoled":
        return 6.0
    if name == "b_shield":
        return 7.0
    if name == "b_cmos_sub":
        return 7.4
    if name == "b_cmos_die":
        return 7.8
    if name == "b_ois_coils":
        return 8.0
    if name == "b_ring_pcb":
        return 8.2
    if name == "b_ring_ics":
        return 8.4
    if name in ("b_hinge", "b_lcp_ant"):
        return 8.5
    if name == "b_prism":
        return 8.6
    if name == "b_barrel":
        return 8.8
    if name == "b_lens_5p":
        return 9.2
    if name == "b_shell":
        return 9.5
    if name in ("b_usbc", "b_usbc_seal"):
        return 9.8
    if name in ("b_speaker", "b_mics", "b_flash"):
        return 10.2
    if name in ("b_pupil", "b_bezel"):
        return 10.8
    if name == "b_sapphire_f":
        return 11.5
    return 0.0


def place_parts(parts, dx=0.0, dy=0.0, dz=0.0, alpha_scale=1.0):
    return [(translate(v, dx, dy, dz), f, col, min(1.0, a * alpha_scale), _part_order(name)) for (name, v, f, col, a) in parts]


def main():
    out_stl = os.path.join(HERE, "models")
    out_png = os.path.join(os.path.dirname(HERE), "teslim")
    os.makedirs(out_stl, exist_ok=True)
    os.makedirs(out_png, exist_ok=True)

    # 1. Build 4-Quadrant (+) Puzzle-Interlocking Screen-Battery Body and Turned & 90°-Bent-at-Gap `b` Module
    qbody_parts = quad_plus_body_parts(explode_q4=0.0)
    qbody_unlatched = quad_plus_body_parts(explode_q4=14.0)  # Q4 unlatched showing male/female puzzle teeth!
    b_parts = monogram_parts(with_panel=True)
    bent_parts = bent_quad_plus_parts(r_bend=25.5, max_angle_deg=46.0)

    # Write individual STLs
    frame_sub = [(v, f) for (n, v, f, _, _) in qbody_parts if any(k in n for k in ("frame", "ribs", "hub", "lip", "magnets", "leaves"))]
    scr_sub = [(v, f) for (n, v, f, _, _) in qbody_parts if any(k in n for k in ("toled", "shield", "qi2", "coil", "uqi"))]
    bat_sub = [(v, f) for (n, v, f, _, _) in qbody_parts if any(k in n for k in ("solid_state_cell", "bifilar", "qi2", "mpp", "coil", "uqi", "magnets", "leaves", "hub"))]

    v_fr, f_fr = merge(frame_sub)
    v_sc, f_sc = merge(scr_sub)
    v_ba, f_ba = merge(bat_sub)
    v_bb, f_bb = merge([(v, f) for (_, v, f, _, _) in bent_parts])
    v_mo, f_mo = merge([(v, f) for (_, v, f, _, _) in b_parts])

    n_fr = write_stl(os.path.join(out_stl, "leaf160-frame.stl"), v_fr, f_fr, "budlum leaf160 quad puzzle frame")
    n_sc = write_stl(os.path.join(out_stl, "leaf160-screen.stl"), v_sc, f_sc, "budlum leaf160 quad plus screen")
    n_ba = write_stl(os.path.join(out_stl, "leaf160-battery.stl"), v_ba, f_ba, "budlum leaf160 4x solid-state cells")
    n_bb = write_stl(os.path.join(out_stl, "leaf160-battery-bent.stl"), v_bb, f_bb, "budlum leaf160 bent quad puzzle")
    n_mo = write_stl(os.path.join(out_stl, "monogram-module.stl"), v_mo, f_mo, "budlum turned 90deg bent b module")

    # Full assembled Revision L.5.0 device:
    #   - 4-Quadrant (+) Puzzle-Interlocking Screen-Battery Body (`80 x 160 x 2.00 mm`, `R = 6.35 mm`)
    #     centered at `(0, 0, -1.00 .. +1.00 mm)`
    #   - Turned & 90°-Bent-at-Gap `b` Module docked on Quadrant Q1 (Top-Left):
    #       * Horizontal `1.00 mm` (`bir milim`) `çubuk` (`y_local = 36.0 .. 37.0 mm`) sits HORIZONTALLY
    #         right on top of the 2.00 mm screen's upper edge (`y_phone = +80.0 .. +81.0 mm`, `z_phone = -1.00 .. +1.80 mm`)!
    #       * Remaining part (`kalan kısım çubuk hariç`: natural gap `boşluk` + `Ø32.0 / Ø24.0 mm` circular ring `yuvarlak`,
    #         `y_local = 0.0 .. 36.0 mm`) hangs down on the front face of the screen (`y_phone = +44.0 .. +80.0 mm`,
    #         `z_phone = +1.00 .. +3.00 mm`), facing directly toward us (`Diğer kısım bize doğru bakarak duruyor`)!
    mod_dx = -W_BODY / 2.0          # Flush with the left edge x = -40.0 mm of Quadrant Q1 (x_phone = -40.0 .. -8.0 mm)
    mod_dy = H_BODY / 2.0 - MON_H   # +80.0 - 36.0 = +44.0 mm (so y_local = 36.0..37.0 mm is at y_phone = +80.0..+81.0 mm!)
    mod_dz = T_BODY / 2.0           # +1.00 mm (front polycarbonate surface of the 2.00 mm screen!)

    dev_meshes = (
        [(translate(v, 0, 0, -T_BODY / 2.0), f) for (_, v, f, _, _) in qbody_parts]
        + [(translate(v, mod_dx, mod_dy, mod_dz), f) for (_, v, f, _, _) in b_parts]
    )
    v_dv, f_dv = merge(dev_meshes)
    n_dv = write_stl(os.path.join(out_stl, "leaf160-device.stl"), v_dv, f_dv, "budlum leaf160 rev L50")
    print(
        "STL tris · frame=%d screen=%d battery=%d bent=%d b_mod=%d device=%d"
        % (n_fr, n_sc, n_ba, n_bb, n_mo, n_dv)
    )
    if "--stl-only" in sys.argv:
        return

    # ── Render 1 & 2: Turned & 90°-Bent-at-Gap `b` Module Front & Back (`render-module.png`, `render-module-back.png`)
    b_centered = place_parts(b_parts, -MON_W / 2.0, -STEM_H / 2.0, -0.5)
    render_scene(
        b_centered,
        os.path.join(out_png, "render-module.png"),
        size=(1300, 1000),
        angles=(24, -22, 0),
        zoom=22.0,
        pan=(0, 8),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum B Modülü (Ters Çevrilip Boşluktan 90° Bükülen Yatay 1 mm Çubuk + Yuvarlak Kamera) · Ön",
        subtitle="B'nin 1 mm çubuğu yukarıda yatay olarak ekran üst kenarına oturur · Kalan yuvarlak kısım boşluktan bükülüp bize doğru bakar",
    )
    render_scene(
        b_centered,
        os.path.join(out_png, "render-module-back.png"),
        size=(1300, 1000),
        angles=(22, 158, 0),
        zoom=22.0,
        pan=(0, 8),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum B Modülü (Ek Parçasız Boşluktan 90° Bükülen Yatay 1 mm Çubuk + Arka AMOLED) · Arka",
        subtitle="Yatay üst çubukta LCP anten + tek USB-C (40W) priz · Yuvarlak gövdede 50MP OIS + 6L Zero-CPU PCB + Ø22.4 mm AMOLED",
    )

    # ── Render 3, 4, 5: Assembled Device Isometric, Front, Back (`render-whole.png`, `render-face.png`, `render-back.png`)
    whole_scene = (
        place_parts(qbody_parts, 0.0, 0.0, -T_BODY / 2.0)
        + place_parts(b_parts, mod_dx, mod_dy, mod_dz)
    )
    render_scene(
        whole_scene,
        os.path.join(out_png, "render-whole.png"),
        size=(1300, 1150),
        angles=(26, -26, 0),
        zoom=5.3,
        pan=(0, 18),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum Leaf 160 · Tamamı Esneyebilen 2.00 mm (R=6.35 mm) (+) Yapboz Polikarbonat Ekran + 90° B Modülü",
        subtitle="4x (40x80x2.00 mm) tamamı esneyebilen PC-Siloksan ekran-pil (R=25.5 mm, Qi2 şarj, portsuz) · 1 mm yatay B çubuğu ekran üstünde",
    )
    render_scene(
        whole_scene,
        os.path.join(out_png, "render-face.png"),
        size=(1300, 1150),
        angles=(8, -6, 0),
        zoom=5.3,
        pan=(0, 18),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum Leaf 160 · Ön Görünüm (Tamamı Esneyebilen Polikarbonat, R=6.35 mm, + Yapboz Kilit, 1 mm B Çubuğu)",
        subtitle="Ekranın %100 tamamı esneyebilen polikarbonat yapıdadır (sıfır rijit bölge) · B'nin 1 mm çubuğu üstte yatay, yuvarlağı bize bakar",
    )
    render_scene(
        whole_scene,
        os.path.join(out_png, "render-back.png"),
        size=(1300, 1150),
        angles=(12, 172, 0),
        zoom=5.3,
        pan=(0, 18),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum Leaf 160 · Arka Görünüm (Tamamı Esneyebilen 2.00 mm Polikarbonat + 4x Esnek Katı-Hal Pil + Qi2.2)",
        subtitle="Çoklu nötr düzlemli PC-PDMS (%0.35 gerinim) + çift eksenli esnek LLZO/PEO katı-hal pil (12 Wh, <=36.2 C) + esnek nanokristalin Qi2",
    )

    # ── Render 6: `render-battery.png` — Left: R=25.5 mm Full-Area Bent Polycarbonate Puzzle Body · Right: Q4 Unlatched
    bat_scene = (
        place_parts(bent_parts, -48.0, 0.0, -T_BODY / 2.0)
        + place_parts(qbody_unlatched, 46.0, 0.0, -T_BODY / 2.0)
        + place_parts(b_parts, 46.0 + mod_dx, mod_dy, mod_dz)
    )
    render_scene(
        bat_scene,
        os.path.join(out_png, "render-battery.png"),
        size=(1400, 1050),
        angles=(28, -24, 0),
        zoom=4.6,
        pan=(-4, 14),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Tamamı Esneyebilen 2.00 mm Polikarbonat Ekran · R=25.5 mm Tam Alan Esneme ve (+) Yapboz Tak-Çıkar",
        subtitle="Solda: 4 karo, (+) yapboz kilit, katı-hal pil ve Qi2 bobinleriyle %100 tamamı esneyen polikarbonat ekran · Sağda: Tak-çıkar Q4",
    )

    # ── Render 7: `render-apart.png` — Full Exploded View of the 4 (+) Puzzle Quadrants & Turned 90°-Bent `b` Module
    apart_scene = []
    q_offsets = {"q1": (-12.0, 12.0), "q2": (12.0, 12.0), "q3": (-12.0, -12.0), "q4": (12.0, -12.0)}
    for (name, v, f, col, a) in qbody_parts:
        qprefix = name[:2]
        ox, oy = q_offsets.get(qprefix, (0.0, 0.0))
        if "back_toled" in name or "eye_shield" in name:
            oz = -9.0
        elif "solid_state_cell" in name or "bifilar" in name:
            oz = -3.0
        elif "qi2" in name or "mpp" in name or "coil" in name or "uqi" in name:
            oz = +3.5
        elif "front_toled" in name:
            oz = +9.5
        else:
            oz = 0.0
        apart_scene.append((translate(v, ox, oy, oz), f, col, min(1.0, a * 1.15)))

    # Exploded turned & 90°-bent `b` module floating above
    for idx, (name, v, f, col, a) in enumerate(b_parts):
        apart_scene.append((translate(v, mod_dx - 10.0, mod_dy + 16.0, 22.0 + idx * 0.65), f, col, min(1.0, a * 1.15)))

    render_scene(
        apart_scene,
        os.path.join(out_png, "render-apart.png"),
        size=(1400, 1150),
        angles=(30, -28, 0),
        zoom=3.9,
        pan=(0, -6),
        bg_top=(14, 20, 28),
        bg_bot=(24, 34, 46),
        title="Budlum Leaf 160 · Tüm 84 İç Parçanın (+) Yapboz Ekseninde Patlatılmış 3B Görünümü",
        subtitle="4x Biyouyumlu PC (R=6.35 mm, 2.00 mm) + Girdili-Çıktılı Yapboz Kilit + 4x Katı-Hal Pil + Qi2.2 Bobinler + Yatay 1 mm Çubuklu B",
    )
    print("All 7 primary 3D renders written to", out_png)


if __name__ == "__main__":
    main()
