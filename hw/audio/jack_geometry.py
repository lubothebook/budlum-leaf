#!/usr/bin/env python3
"""jack_geometry.py - the 3.5 mm jack groove in the B ring rim (FINAL/21 21.3.6).

Frame: ring centre at the origin, +y toward the bar edge, z = 0 at mid-thickness.
The bore axis is the line y = CHORD_D, z = 0, running along +x. The plug enters
from +x. s is the distance along the bore from the blind end (the tip datum).

Run:  python3 jack_geometry.py      -> prints the checks, writes out/geometry.json
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

R, RI, T = P.RING_RO, P.RING_RI, P.RING_T
d, rb, t = P.CHORD_D, P.BORE_D / 2, P.WALL_T


def x_at(r, y):
    """x where the line y meets the circle of radius r (positive root)."""
    return math.sqrt(r * r - y * y) if r > abs(y) else 0.0


def wrap_deg(x, r_out):
    """Angle of bore wall material around the axis at station x (deg)."""
    ymax = x_at(r_out, 0) if False else math.sqrt(max(r_out**2 - x * x, 0))
    if ymax >= d + rb:
        return 360.0
    if ymax <= d - rb:
        return 0.0
    # material where y < ymax: the arc below the chord of the circle
    c = (ymax - d) / rb
    return 360.0 - 2 * math.degrees(math.acos(c))


def main():
    res = {}
    # 1 radial span
    res["bore_r_span"] = [d - rb, d + rb]
    res["wall_r_span"] = [d - rb - t, d + rb + t]
    res["outer_wall_at_x0"] = R - (d + rb)
    # 2 window clearance: windows sit at |z| >= T/2 - WINDOW_T
    z_w = T / 2 - P.WINDOW_T
    y_min_at_window_plane = d - math.sqrt((rb + t) ** 2 - z_w**2)
    res["window_plane_clearance"] = y_min_at_window_plane - RI
    res["inner_wall_intrusion_midplane"] = RI - (d - rb - t)
    res["inner_wall_intrusion_halfspan_x"] = x_at(RI, d - rb - t)

    # 3 closed end: the outer wall line y = d + rb + t stays inside r = R
    x_closed = x_at(R, d + rb + t)
    x_bottom = -(x_closed - t)                 # inner face of the 0.2 end wall
    res["closed_outer_halfspan"] = x_closed
    res["closed_outer_length"] = 2 * x_closed
    res["closed_bore_length"] = x_closed - x_bottom
    res["x_bottom"] = x_bottom
    # 4 trough stations
    res["x_bore_breaks_rim"] = x_at(R, d + rb)
    res["x_capture_ends_r16"] = x_at(R, d)       # wrap falls to 180 deg
    res["x_cradle_ends_r16"] = x_at(R, d - rb)   # inboard bore line leaves the ring
    res["x_inboard_wall_ends_r16"] = x_at(R, d - rb - t)
    # 5 plug seat with the tip datum
    seats = {}
    for L in (P.PLUG_L_RANGE[0], P.PLUG_L, P.PLUG_L_RANGE[1]):
        x_sh = x_bottom + L
        r_need = math.hypot(x_sh, d - rb)          # cradle floor reaches the shoulder
        seats[f"{L:.1f}"] = dict(x_shoulder=round(x_sh, 3),
                                 boss_needed=round(max(r_need - R, 0), 3))
    res["shoulder_seat"] = seats
    res["trough_length_to_shoulder"] = x_bottom + P.PLUG_L - x_closed
    for b in P.BOSS_H:
        res[f"x_capture_ends_boss{b}"] = x_at(R + b, d)
    # 6 entry angle of the plug to the rim tangent at the centre-line exit
    xe = res["x_capture_ends_r16"]
    res["entry_angle_to_rim_tangent_deg"] = 90 - math.degrees(math.acos(xe / R))
    # 7 wrap angle table
    res["wrap_table"] = [
        dict(x=round(x, 2), s=round(x - x_bottom, 2),
             wrap_r16=round(wrap_deg(x, R), 1),
             wrap_boss1=round(wrap_deg(x, R + 1.0), 1))
        for x in [x_bottom, 0, 2.5, 3.56, 5, 6, 7, 8.1, 9, 9.93, 10.5, 11.68]
    ]
    # 8 contacts: s from the blind end, the plug tip bottoms on it
    contacts = [
        ("T  tip, detent in the neck", 2.40, "L"),
        ("D  detect leaf behind T", 2.40, "DET"),
        ("R1 ring 1", 5.40, "R"),
        ("R2 ring 2", 8.20, "GND, Kelvin pair"),
        ("S  sleeve C-clip", 11.20, "MIC"),
    ]
    # plug-to-plug zone scatter grows with the distance from the tip datum,
    # because the detent in the neck sets the axial place.     [HYPOTHESIS]
    def zone_shift(s):
        return 0.10 + 0.025 * s
    patch = 0.10                 # half-length of the contact patch
    rows = []
    for name, s, sig in contacts:
        x = x_bottom + s
        zone = next(z for z in P.PLUG_ZONES if z[1] <= s < z[2])
        if name.startswith("T"):
            zone = ("tip neck", 2.0, 2.8, "L")
        margin = min(s - zone[1], zone[2] - s) - patch
        if x <= x_closed:
            region = "closed end"
        elif x <= res["x_bore_breaks_rim"]:
            region = "closed, rim wall thinning"
        elif x <= res["x_capture_ends_r16"]:
            region = "trough, captured"
        else:
            region = "trough, cradle and boss"
        wall_ok = x <= res["x_inboard_wall_ends_r16"]
        rows.append(dict(contact=name, signal=sig, s=s, x=round(x, 2),
                         plug_zone=zone[0], margin=round(margin, 2),
                         margin_after_scatter=round(margin - zone_shift(s), 2),
                         region=region, inboard_wall=wall_ok))
    res["contacts"] = rows
    # 9 PCBA notch: keep 0.2 mm off the inboard wall
    y_notch = d - rb - t - 0.2
    x0, x1 = x_bottom - t, x_at(15.0, y_notch)
    res["pcba_notch"] = dict(y_from=y_notch, x_from=round(x0, 2), x_to=round(x1, 2))
    # 10 A3 loop at r = 15.5 meets the wall band
    r_a3 = 31.0 / 2
    a_lo = math.degrees(math.atan2(d - rb - t, x_at(r_a3, d - rb - t)))
    a_hi = math.degrees(math.atan2(d, x_bottom - t))
    res["a3_conflict_arc_deg"] = [round(a_lo, 1), round(a_hi, 1)]
    res["a3_detour_inboard_r"] = d - rb - t - 0.2
    # 11 overmold of the plug against the screen face (ring on the face)
    om = {}
    for D in (4.0, 5.0, 6.0, 7.0):
        om[f"{D:.0f}"] = round(max(D / 2 - T / 2, 0), 2)
    res["overmold_below_ring_underside"] = om
    # 12 sector used by the jack, for the layout of the other parts
    pts = [(x_bottom - t, d + rb + t), (x_bottom - t, d - rb - t),
           (res["x_inboard_wall_ends_r16"], d - rb - t)]
    angs = [math.degrees(math.atan2(y, x)) for x, y in pts]
    res["jack_sector_deg"] = [round(min(angs), 1), round(max(angs), 1)]

    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "geometry.json"), "w") as f:
        json.dump(res, f, indent=1)

    # ---- print
    print("JACK GROOVE GEOMETRY CHECK (FINAL/21 21.3.6)")
    print(f" bore r span {res['bore_r_span']}, wall r span {res['wall_r_span']}")
    print(f" outer wall at the chord mid-point {res['outer_wall_at_x0']:.2f} mm")
    print(f" window plane clearance {res['window_plane_clearance']:.2f} mm "
          f"(mid-plane wall reaches r={d-rb-t:.1f}, {res['inner_wall_intrusion_midplane']:.2f} mm "
          f"inside r=12 over |x|<{res['inner_wall_intrusion_halfspan_x']:.2f})")
    print(f" closed end: outer {res['closed_outer_length']:.2f} mm, bore {res['closed_bore_length']:.2f} mm"
          f" + 0.20 end wall, blind end at x={x_bottom:.2f}")
    print(f" trough: bore breaks the rim at x={res['x_bore_breaks_rim']:.2f}, capture >180 deg to "
          f"x={res['x_capture_ends_r16']:.2f}, cradle to x={res['x_cradle_ends_r16']:.2f}")
    print(f" trough length to a 14.0 mm shoulder {res['trough_length_to_shoulder']:.2f} mm")
    for L, v in seats.items():
        print(f" plug {L} mm: shoulder x={v['x_shoulder']}, boss to cradle it {v['boss_needed']} mm")
    for b in P.BOSS_H:
        print(f" capture with a {b} mm boss ends at x={res[f'x_capture_ends_boss{b}']:.2f}")
    print(f" plug entry angle to the rim tangent {res['entry_angle_to_rim_tangent_deg']:.1f} deg")
    print(" wrap table (x, s, wrap r16, wrap boss 1.0):")
    for w in res["wrap_table"]:
        print(f"   {w['x']:6.2f} {w['s']:6.2f} {w['wrap_r16']:6.1f} {w['wrap_boss1']:6.1f}")
    print(" contacts:")
    for c in rows:
        print(f"   {c['contact']:28s} s={c['s']:5.2f} x={c['x']:6.2f} {c['plug_zone']:10s} "
              f"margin {c['margin']:.2f} ({c['margin_after_scatter']:+.2f} after scatter) "
              f"{c['region']}, inboard wall {c['inboard_wall']}")
    print(f" PCBA notch: y > {y_notch:.1f} for x {x0:.2f}..{x1:.2f}")
    print(f" A3 loop r=15.5 meets the jack over {res['a3_conflict_arc_deg']} deg; detour at r<={res['a3_detour_inboard_r']:.1f}")
    print(f" overmold below the ring underside (D: mm): {om}")
    print(f" jack sector {res['jack_sector_deg']} deg")
    ok = (abs(res["closed_outer_length"] - P.CLOSED_L) < 0.2 and
          abs(res["trough_length_to_shoulder"] - P.TROUGH_L) < 0.3 and
          res["window_plane_clearance"] > 0 and
          all(c["margin_after_scatter"] > 0 for c in rows) and
          P.BOSS_H[0] <= seats["14.0"]["boss_needed"] <= P.BOSS_H[1])
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
