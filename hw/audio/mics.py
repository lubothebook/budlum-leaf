#!/usr/bin/env python3
"""mics.py - the two MEMS microphones of the B ring (MON-7): place and spacing.

Frame of jack_geometry.py: ring centre at the origin, +y toward the bar edge.
The bar always lies on a body edge, and the ring always lies inward of it.
So the axis "from the bar into the body" is fixed in the module frame on
every one of the eight seats. That axis is the endfire axis of the pair.

1. Annulus allocation: jack, bar joint, mics, speaker, back volume.
2. Spacing sweep: spatial alias limit, first-order differential white noise
   gain (WNG), delay in samples, null depth under a sensitivity mismatch.
3. The acoustic port: Helmholtz resonance of the rim hole and mesh.

Run:  python3 mics.py   -> out/mics.json
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402

c = P.C_AIR
R = P.RING_RO
FS = 48000

ALLOC = [  # name, from deg, to deg, owner, tag
    ("speaker back volume", 250, 298, "audio", "HYPOTHESIS"),
    ("speaker 9.0 x 3.2", 298, 332, "audio", "HYPOTHESIS"),
    ("jack (closed end to rim)", 47.5, 102.1, "audio", "DECISION 13.8 chord"),
    ("bar joint and corner flex", 110, 135, "module integrator", "HYPOTHESIS"),
]
D_PICK = 20.0                      # mm, the chosen spacing
PHI = math.degrees(math.asin(D_PICK / 2 / R))
ALLOC += [("M1 rim port", 180 - PHI - 2, 180 - PHI + 2, "audio", "this team"),
          ("M2 rim port", 180 + PHI - 2, 180 + PHI + 2, "audio", "this team")]
F_X = 500.0                        # Hz, crossover: below it the pair runs as a sum


def rim(theta_deg):
    t = math.radians(theta_deg)
    return np.array([R * math.cos(t), R * math.sin(t)])


def overlaps():
    bad = []
    for i in range(len(ALLOC)):
        for j in range(i + 1, len(ALLOC)):
            a, b = ALLOC[i], ALLOC[j]
            if a[1] < b[2] and b[1] < a[2]:
                bad.append((a[0], b[0]))
    return bad


def wng_db(d, f):
    """Delay-and-subtract cardioid, equalised to unity on axis."""
    kd = 2 * math.pi * f * d / c
    H = abs(1 - np.exp(-2j * kd))
    return 10 * math.log10(H**2 / 2)


def null_depth_db(mismatch_db, f, d):
    """Rear null of the cardioid when one mic is mismatch_db hotter."""
    g = 10 ** (mismatch_db / 20)
    kd = 2 * math.pi * f * d / c
    rear = abs(1 - g)                      # delays cancel at the rear
    front = abs(1 - g * np.exp(-2j * kd))
    return 20 * math.log10(max(rear, 1e-9) / front)


def main():
    res = {}
    print("TWO MEMS MICROPHONES (MON-7)")
    ov = overlaps()
    res["allocation"] = ALLOC
    res["overlaps"] = ov
    print(" annulus allocation (deg, CCW from +x):")
    for a in ALLOC:
        print(f"   {a[0]:28s} {a[1]:6.1f} .. {a[2]:6.1f}  {a[3]} [{a[4]}]")
    print("   overlaps:", ov if ov else "none")
    m1, m2 = rim(180 - PHI), rim(180 + PHI)
    d = float(np.linalg.norm(m1 - m2))
    spk = rim(315)
    res["positions"] = dict(M1=m1.round(2).tolist(), M2=m2.round(2).tolist(), spacing_mm=round(d, 2),
                            axis="along -y, from the bar into the body",
                            spk_to_M1=round(float(np.linalg.norm(spk - m1)), 1),
                            spk_to_M2=round(float(np.linalg.norm(spk - m2)), 1))
    print(f" M1 {m1.round(2)}, M2 {m2.round(2)}, spacing {d:.2f} mm, endfire axis along -y")
    print(f" speaker port to M1 {res['positions']['spk_to_M1']} mm, to M2 {res['positions']['spk_to_M2']} mm")

    print(" spacing sweep (alias = c/2d; WNG of an equalised cardioid; self-noise 26 dBA):")
    sweep = []
    noise_dba = 94 - P.MIC["snr_db"]
    for dmm in (8, 10, 12, 16, 20, 24, 28):
        dd = dmm * 1e-3
        fa = c / (2 * dd)
        w300, w1k, wx = wng_db(dd, 300), wng_db(dd, 1000), wng_db(dd, F_X)
        nd = null_depth_db(1.0, 1000, dd)
        row = dict(d_mm=dmm, f_alias_kHz=round(fa / 1e3, 2), wng300=round(w300, 1),
                   wng1k=round(w1k, 1), wng_x=round(wx, 1), eq_noise_300=round(noise_dba - w300, 1),
                   delay_samples=round(dd / c * FS, 2), null_1dB_mismatch=round(nd, 1))
        sweep.append(row)
        print(f"   d {dmm:2d} mm: alias {fa/1e3:5.2f} kHz, WNG300 {w300:6.1f} dB, WNG500 {wx:6.1f} dB, WNG1k {w1k:6.1f} dB, "
              f"noise@300 {noise_dba - w300:5.1f} dB, delay {dd/c*FS:4.2f} smp, null(1 dB) {nd:5.1f} dB")
    res["sweep"] = sweep
    pick = next(r for r in sweep if r["d_mm"] == D_PICK)
    ok = pick["f_alias_kHz"] >= 8.0 and pick["wng_x"] >= -12.0 and not ov
    print(f" choice d = {D_PICK:.0f} mm, rim angles {180-PHI:.1f} and {180+PHI:.1f} deg: alias "
          f"{pick['f_alias_kHz']} kHz >= 8 kHz (16 kHz wideband), WNG at the {F_X:.0f} Hz crossover "
          f"{pick['wng_x']} dB >= -12 dB -> {'PASS' if ok else 'FAIL'}")
    print("   below the crossover the pair sums (WNG +3 dB); the validator runs the adaptive stage.")

    # port Helmholtz: O0.5 rim hole, 0.6 mm long with the mesh, 0.5 mm3 front volume
    a = 0.25e-3
    S = math.pi * a**2
    L = 0.6e-3 + 1.7 * a
    V = 0.5e-9
    fH = c / (2 * math.pi) * math.sqrt(S / (V * L))
    res["port_helmholtz_kHz"] = round(fH / 1e3, 1)
    print(f" mic port Helmholtz {fH/1e3:.1f} kHz (must be > 20 kHz): {'PASS' if fH > 20e3 else 'FAIL'}")
    res["pass"] = bool(ok and fH > 20e3)
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "mics.json"), "w") as fo:
        json.dump(res, fo, indent=1)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
