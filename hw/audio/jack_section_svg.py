#!/usr/bin/env python3
"""jack_section_svg.py - draws jack_section.svg from the same numbers as the scripts.

View A: the ring from the face, with the jack, the speaker and the mics.
View B: section A-A across the bore at the closed end (x = 0).
View C: the mid-plane section along the bore, with the plug, the contacts
        and the gasketed pocket.

Run:  python3 jack_section_svg.py   -> jack_section.svg
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
geo_path = os.path.join(HERE, "out", "geometry.json")
if not os.path.exists(geo_path):
    sys.exit("run jack_geometry.py first")
G = json.load(open(geo_path))
R, RI, d, rb, t = P.RING_RO, P.RING_RI, P.CHORD_D, P.BORE_D / 2, P.WALL_T
xb = G["x_bottom"]

INK, MUTE, BORE, WALL, PLUG, CONT, GASK, ACC = (
    "#1d2433", "#7a8496", "#ffffff", "#c9d3e3", "#d9b45a", "#b5452f", "#2f7d5b", "#2a5db0")
out = []


def add(s):
    out.append(s)


def txt(x, y, s, size=11, anchor="start", color=INK, weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
        f'fill="{color}" font-weight="{weight}" font-family="Helvetica, Arial, sans-serif">{s}</text>')


W, H = 1500, 1080
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add(f'<rect width="{W}" height="{H}" fill="#fbfaf7"/>')
txt(30, 40, "BUDLUM LEAF L.6.0 . B RING . THE 3.5 mm JACK IN THE RIM", 20, weight="bold")
txt(30, 62, "hw/audio . FINAL/21 21.3.6 . HARDWARE/13 part 26 . gate MON-22 . drawn by jack_section_svg.py "
            "from out/geometry.json . all dimensions in mm", 12, color=MUTE)

# ---------------------------------------------------------------- view A
sa, cx, cy = 12.0, 270, 375
def A(x, y):
    return cx + x * sa, cy - y * sa
txt(30, 100, "VIEW A . the ring from the face (+y toward the bar edge)", 14, weight="bold")
add(f'<circle cx="{cx}" cy="{cy}" r="{R*sa}" fill="{WALL}" stroke="{INK}" stroke-width="1.5"/>')
add(f'<circle cx="{cx}" cy="{cy}" r="{RI*sa}" fill="#eef2f8" stroke="{INK}" stroke-width="1" stroke-dasharray="5 3"/>')
txt(cx, cy + 4, "O24.0 windows", 11, "middle", MUTE)
# A3 loop
add(f'<circle cx="{cx}" cy="{cy}" r="{15.5*sa}" fill="none" stroke="{ACC}" stroke-width="1" stroke-dasharray="2 3"/>')
# bore strip (clip to ring + boss)
x_end = G["shoulder_seat"]["14.0"]["x_shoulder"]
x0, y0 = A(xb, d + rb)
x1, y1 = A(x_end, d - rb)
add(f'<clipPath id="ringclip"><circle cx="{cx}" cy="{cy}" r="{(R+0.75)*sa}"/></clipPath>')
add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" fill="{PLUG}" '
    f'stroke="{INK}" stroke-width="0.8" clip-path="url(#ringclip)"/>')
# closed end hatch
xc0, _ = A(xb, 0)
xc1, _ = A(G["closed_outer_halfspan"], 0)
add(f'<rect x="{xc0:.1f}" y="{y0:.1f}" width="{xc1-xc0:.1f}" height="{y1-y0:.1f}" fill="none" '
    f'stroke="{CONT}" stroke-width="1.6"/>')
# boss
bx, by = A(G["x_capture_ends_r16"] + 0.6, d - 0.6)
add(f'<path d="M {A(9.0, 12.4)[0]:.1f} {A(9.0, 12.4)[1]:.1f} A {(R+0.75)*sa:.1f} {(R+0.75)*sa:.1f} 0 0 1 '
    f'{A(12.2, 10.4)[0]:.1f} {A(12.2, 10.4)[1]:.1f}" fill="none" stroke="{INK}" stroke-width="3"/>')
txt(A(12.6, 11.4)[0] + 6, A(12.6, 11.4)[1], "rim boss 0.74", 10)
txt(30, 122, "jack: chord 13.8, bore O3.6, walls 0.20", 11)
txt(30, 138, "red box: closed end 5.04 (bore 4.84)", 11, color=CONT)
txt(30, 154, "gold: bore and trough, 9.16 to the 14.0 shoulder", 11)
# speaker
def arcbox(a0, a1, r0, r1, fill, label):
    p0 = (cx + r0 * sa * math.cos(math.radians(a0)), cy - r0 * sa * math.sin(math.radians(a0)))
    p1 = (cx + r1 * sa * math.cos(math.radians(a0)), cy - r1 * sa * math.sin(math.radians(a0)))
    p2 = (cx + r1 * sa * math.cos(math.radians(a1)), cy - r1 * sa * math.sin(math.radians(a1)))
    p3 = (cx + r0 * sa * math.cos(math.radians(a1)), cy - r0 * sa * math.sin(math.radians(a1)))
    add(f'<path d="M {p0[0]:.1f} {p0[1]:.1f} L {p1[0]:.1f} {p1[1]:.1f} A {r1*sa:.1f} {r1*sa:.1f} 0 0 0 '
        f'{p2[0]:.1f} {p2[1]:.1f} L {p3[0]:.1f} {p3[1]:.1f} A {r0*sa:.1f} {r0*sa:.1f} 0 0 1 {p0[0]:.1f} {p0[1]:.1f} Z" '
        f'fill="{fill}" stroke="{INK}" stroke-width="0.8" fill-opacity="0.75"/>')
    am = math.radians((a0 + a1) / 2)
    txt(cx + (R + 2.6) * sa * math.cos(am), cy - (R + 2.6) * sa * math.sin(am) + 4, label, 10, "middle")
arcbox(298, 332, 12.3, 15.6, "#9db7d9", "speaker 9.0x3.2x2.2")
arcbox(250, 298, 12.3, 15.6, "#dfe8f3", "back volume 100 mm3")
arcbox(110, 135, 12.3, 15.6, "#e7e1d3", "bar joint")
phi = math.degrees(math.asin(10 / R))
for nm, a in (("M1", 180 - phi), ("M2", 180 + phi)):
    mx, my = cx + (R - 0.6) * sa * math.cos(math.radians(a)), cy - (R - 0.6) * sa * math.sin(math.radians(a))
    add(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="5" fill="{GASK}"/>')
    txt(mx - 10, my + 4, nm, 11, "end", GASK, "bold")
m1 = A(-12.49, 10); m2 = A(-12.49, -10)
add(f'<line x1="{m1[0]-24:.1f}" y1="{m1[1]:.1f}" x2="{m2[0]-24:.1f}" y2="{m2[1]:.1f}" stroke="{GASK}" '
    f'stroke-width="1" marker-end="url(#arr)"/>')
txt(m1[0] - 30, cy, "endfire 20 mm", 10, "end", GASK)
add('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
    f'<path d="M0,0 L6,3 L0,6 Z" fill="{GASK}"/></marker></defs>')
# section line A-A
ax0, ay0 = A(0, d + rb + 1.2); ax1, ay1 = A(0, d - rb - 1.2)
add(f'<line x1="{ax0:.1f}" y1="{ay0:.1f}" x2="{ax1:.1f}" y2="{ay1:.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="8 3 2 3"/>')
txt(ax0 + 4, ay0 - 2, "A", 12, weight="bold"); txt(ax1 + 4, ay1 + 10, "A", 12, weight="bold")
add(f'<line x1="{cx-6}" y1="{cy}" x2="{cx+6}" y2="{cy}" stroke="{INK}"/>'
    f'<line x1="{cx}" y1="{cy-6}" x2="{cx}" y2="{cy+6}" stroke="{INK}"/>')
txt(30, 615, "A3 loop O31.0 (dotted) detours inboard of the jack, r <= 11.6, over 49.6..100.4 deg. RF-22.", 11, color=ACC)
txt(30, 631, "Mic axis is fixed in the module frame: from the bar into the body, on all eight seats.", 11, color=GASK)

# ---------------------------------------------------------------- view B
sb, bx0, by0 = 52.0, 650, 330      # y horizontal (right = outboard), z vertical
def B(y, z):
    return bx0 + (y - 13.8) * sb, by0 - z * sb
txt(560, 100, "SECTION A-A . across the bore at the closed end (x = 0)", 14, weight="bold")
yl, yr = 10.8, 16.0
p, q = B(yl, 2.0), B(yr, -2.0)
add(f'<rect x="{p[0]:.1f}" y="{p[1]:.1f}" width="{q[0]-p[0]:.1f}" height="{q[1]-p[1]:.1f}" fill="{WALL}" stroke="{INK}"/>')
c0 = B(d, 0)
add(f'<circle cx="{c0[0]:.1f}" cy="{c0[1]:.1f}" r="{(rb+t)*sb:.1f}" fill="#8e7cc3" fill-opacity="0.55" stroke="{INK}" stroke-width="0.8"/>')
add(f'<circle cx="{c0[0]:.1f}" cy="{c0[1]:.1f}" r="{rb*sb:.1f}" fill="{BORE}" stroke="{INK}"/>')
add(f'<circle cx="{c0[0]:.1f}" cy="{c0[1]:.1f}" r="{P.PLUG_D/2*sb:.1f}" fill="{PLUG}" fill-opacity="0.6" stroke="{INK}" stroke-dasharray="3 2"/>')
# saddle and pocket
s0, s1 = B(10.8, 1.5), B(11.75, -1.5)
add(f'<rect x="{s0[0]:.1f}" y="{s0[1]:.1f}" width="{s1[0]-s0[0]:.1f}" height="{s1[1]-s0[1]:.1f}" fill="#f3e6c8" stroke="{INK}" stroke-width="0.8"/>')
g0 = B(10.95, 1.65); g1 = B(10.95, -1.65)
add(f'<line x1="{g0[0]:.1f}" y1="{g0[1]:.1f}" x2="{g1[0]:.1f}" y2="{g1[1]:.1f}" stroke="{GASK}" stroke-width="6"/>')
f0 = B(11.5, 0.6); f1 = B(d - rb + 0.05, 0.0)
add(f'<path d="M {f0[0]:.1f} {f0[1]:.1f} Q {f1[0]-10:.1f} {f0[1]:.1f} {f1[0]:.1f} {f1[1]:.1f}" stroke="{CONT}" stroke-width="3" fill="none"/>')
# labels
txt(B(16.1, 2.0)[0] + 6, B(0, 1.9)[1] + 4, "4.00 module", 10)
txt(B(d, 2.25)[0], B(d, 2.25)[1], "crown 0.20 (stress peak, +-z)", 10, "middle", CONT)
txt(B(15.9, -2.35)[0], B(0, -2.35)[1] + 6, "rim wall 0.40", 10, "end")
txt(B(10.8, -2.3)[0], B(0, -2.3)[1] + 8, "saddle root", 10)
txt(B(10.8, 0)[0], 160, "green: FKM pocket cord 0.40 at 25 % squeeze", 10, color=GASK)
txt(B(10.8, 0)[0], 176, "red: contact finger from the PEEK carrier in the saddle", 10, color=CONT)
txt(c0[0], c0[1] + 4, "plug O3.5", 10, "middle")
txt(c0[0], c0[1] + 18, "bore O3.6", 10, "middle", MUTE)
txt(560, 470, "Violet band: the 0.20 mm wall. LCP-GF40 as decided; Y-TZP cup or metal liner in the", 11)
txt(560, 486, "team design. FE stress per 1 N/mm: crown 34 (LCP), 50 (stiff band); rim side 14 / 23.", 11)
txt(560, 502, "The inboard wall rests on the saddle: under 1 MPa per N/mm.", 11)

# ---------------------------------------------------------------- view C
sc, cx0, cy0 = 46.0, 120, 850     # x horizontal, y vertical (up = outboard)
def C(x, y):
    return cx0 + (x - xb + 0.6) * sc, cy0 - (y - 13.8) * sc
txt(30, 662, "SECTION B-B . mid-plane along the bore, z = 0 (up = outboard, toward the rim)", 14, weight="bold")
# ring material polygon (mid-plane): between y = 10.6 and the rim arc, minus the bore
pts = []
xs = [xb - 0.6 + i * 0.1 for i in range(0, int((x_end + 1.2 - xb) / 0.1) + 1)]
top = [(x, math.sqrt(max(R**2 - x * x, 0))) for x in xs if R**2 - x * x > 10.6**2]
poly = [(xs[0], 10.6)] + top + [(top[-1][0], 10.6)]
add('<path d="M ' + " L ".join(f"{C(x,y)[0]:.1f} {C(x,y)[1]:.1f}" for x, y in poly) +
    f' Z" fill="{WALL}" stroke="{INK}" stroke-width="1"/>')
# boss arc
boss = [(x, math.sqrt(max((R + 0.75) ** 2 - x * x, 0))) for x in xs if 8.6 <= x <= x_end + 0.1]
add('<path d="M ' + " L ".join(f"{C(x,y)[0]:.1f} {C(x,y)[1]:.1f}" for x, y in boss) +
    f'" fill="none" stroke="{INK}" stroke-width="3"/>')
# bore
b0, b1 = C(xb, d + rb), C(x_end + 0.6, d - rb)
add(f'<rect x="{b0[0]:.1f}" y="{b0[1]:.1f}" width="{b1[0]-b0[0]:.1f}" height="{b1[1]-b0[1]:.1f}" fill="{BORE}"/>')
# sleeve band in the closed end
k0, k1 = C(xb - t, d + rb + t), C(G["closed_outer_halfspan"], d - rb - t)
add(f'<rect x="{k0[0]:.1f}" y="{k0[1]:.1f}" width="{k1[0]-k0[0]:.1f}" height="{k1[1]-k0[1]:.1f}" '
    f'fill="none" stroke="#8e7cc3" stroke-width="5" stroke-opacity="0.6"/>')
# plug zones
for name, s0_, s1_, sig in P.PLUG_ZONES:
    rr = P.NECK_D / 2 if name == "tip neck" else P.PLUG_D / 2
    col = PLUG if sig != "-" else "#333333"
    z0, z1 = C(xb + s0_, d + rr), C(xb + s1_, d - rr)
    add(f'<rect x="{z0[0]:.1f}" y="{z0[1]:.1f}" width="{z1[0]-z0[0]:.1f}" height="{z1[1]-z0[1]:.1f}" '
        f'fill="{col}" stroke="{INK}" stroke-width="0.5"/>')
    if sig != "-":
        txt((z0[0] + z1[0]) / 2, z0[1] - 6, sig.split()[0], 10, "middle")
om0, om1 = C(xb + P.PLUG_L, d + 2.6), C(xb + P.PLUG_L + 4.5, d - 2.6)
add(f'<rect x="{om0[0]:.1f}" y="{om0[1]:.1f}" width="{om1[0]-om0[0]:.1f}" height="{om1[1]-om0[1]:.1f}" rx="6" fill="#55606f"/>')
txt((om0[0] + om1[0]) / 2, om0[1] - 6, "plug body", 10, "middle")
# contacts in the inboard pocket
for c in G["contacts"]:
    if c["contact"].startswith("D"):
        continue
    cxp = C(c["x"], d - rb)
    cyp = cxp
    root = C(c["x"] + (3.0 if c["contact"].startswith(("T", "R")) else 0.9), 11.15)
    add(f'<path d="M {root[0]:.1f} {root[1]:.1f} Q {cxp[0]+20:.1f} {root[1]:.1f} {cxp[0]:.1f} {cyp[1]+1:.1f}" '
        f'stroke="{CONT}" stroke-width="3" fill="none"/>')
    add(f'<circle cx="{cxp[0]:.1f}" cy="{cyp[1]:.1f}" r="3.5" fill="{CONT}"/>')
    txt(cxp[0], C(0, 10.35)[1] + 6, c["contact"].split()[0] + f" s={c['s']}", 10, "middle", CONT, "bold")
# detect leaf
dl = C(xb + 2.4, 11.2)
add(f'<line x1="{dl[0]-14:.1f}" y1="{dl[1]+8:.1f}" x2="{dl[0]+14:.1f}" y2="{dl[1]+8:.1f}" stroke="{ACC}" stroke-width="3"/>')
txt(dl[0] - 18, dl[1] + 12, "D (NC)", 10, "end", ACC)
# gasket line along the pocket
gp0, gp1 = C(xb, 10.75), C(10.6, 10.75)
add(f'<line x1="{gp0[0]:.1f}" y1="{gp0[1]:.1f}" x2="{gp1[0]:.1f}" y2="{gp1[1]:.1f}" stroke="{GASK}" stroke-width="5"/>')
txt(gp1[0] + 6, gp1[1] + 4, "FKM pocket gasket, PEEK contact carrier, 4 heat stakes", 10, color=GASK)
# dimension marks
for i, (xv, lab) in enumerate(((xb, "blind end"), (G["closed_outer_halfspan"], "closed wall ends"),
                (G["x_bore_breaks_rim"], "bore breaks the rim"), (G["x_capture_ends_r16"], "capture < 180 deg"),
                (x_end, "shoulder, 14.0"))):
    pa = C(xv, 17.0 + 0.35 * (i % 2))
    add(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pa[0]:.1f}" y2="{C(xv, d+rb)[1]:.1f}" stroke="{MUTE}" stroke-dasharray="2 2"/>')
    txt(pa[0], pa[1] - 4, f"{lab} x={xv:.2f}", 9, "middle", MUTE)
txt(30, 1040, "Change request CR-AUD-1: chord 13.2 in place of 13.8 grows the closed tube to 9.78 mm. With a 0.20 mm "
              "Ti-6Al-4V, 17-4PH or Zr-BMG liner it holds 10 N at 15 mm in every direction.", 11, color=CONT)
txt(30, 1058, "As decided (13.8, LCP walls) it holds 0.5 N outboard and 1.1 N face-normal. jack_sideload.py.", 11, color=CONT)
add("</svg>")
with open(os.path.join(HERE, "jack_section.svg"), "w") as f:
    f.write("\n".join(out))
print("wrote jack_section.svg")
