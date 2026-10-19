#!/usr/bin/env python3
"""host_margin.py - host power classes H0..H6 against the Leaf worst peak.

Study team, Host Power program. Reads no other file. Every input carries its
source tag in the table below. The output goes to stdout and to out/host_margin.txt.

Margin = P_avail x eta - P_PEAK. A negative margin means the host alone cannot
carry the worst peak, and the Buffer tier must carry the difference.
"""
import os

P_PEAK = 8.7          # W, worst peak, BRIEF Section 5 [TREE]
SESSION_H = (2.0, 3.7)    # h, delta or video session, BRIEF Section 2 [TREE]
E_BODY_WH = (5.9, 7.4)    # Wh, Full tier body, BRIEF Section 2 [TREE]

# (class, host, P_avail W, eta, source tag, note)
HOSTS = [
    ("H0", "wall dock, USB-C 40 W", 40.0, 0.90,
     "[TREE] FINAL/00 answer 11 for 40 W; eta [HYPOTHESIS]", "port part, VHV rail"),
    ("H2a", "desk PC port, USB 2.0 5 V 0.5 A", 2.5, 0.90,
     "[PUBLICATION] Samsung DeX support page; eta [HYPOTHESIS]", "no PD contract"),
    ("H2b", "desk PC port, USB 3.0 5 V 0.9 A", 4.5, 0.90,
     "[PUBLICATION] Samsung DeX support page; eta [HYPOTHESIS]", "no PD contract"),
    ("H2c", "desk USB-C PD 9 V 2.3 A", 20.7, 0.90,
     "[PUBLICATION] Samsung Tab Active5 page for 9 V 2.3 A; eta [HYPOTHESIS]", "PD contract"),
    ("H4a", "PoE class 1, PD 3.84 W", 3.84, 0.85,
     "[PUBLICATION] Ethernet Alliance 802.3bt overview; eta [HYPOTHESIS]", "802.3af"),
    ("H4b", "PoE class 2, PD 6.49 W", 6.49, 0.85,
     "[PUBLICATION] Ethernet Alliance 802.3bt overview; eta [HYPOTHESIS]", "802.3af"),
    ("H4c", "PoE class 3, PD 13 W", 13.0, 0.85,
     "[PUBLICATION] Ethernet Alliance 802.3bt overview; eta [HYPOTHESIS]", "802.3af"),
    ("H4d", "PoE class 4, PD 25.5 W", 25.5, 0.85,
     "[PUBLICATION] Ethernet Alliance 802.3bt overview; eta [HYPOTHESIS]", "802.3at"),
    ("H6a", "Qi basic power profile, 5 W", 5.0, 0.75,
     "[PUBLICATION] Granite River Labs Qi2 authentication note; eta from BRIEF heat", "before authentication"),
    ("H6b", "Qi2 15 W", 15.0, 0.75,
     "[PUBLICATION] WPC Qi page; eta from BRIEF heat", "after authentication"),
    ("H6c", "Qi2 25 W", 25.0, 0.75,
     "[PUBLICATION] WPC Qi page; eta from BRIEF heat", "after authentication"),
]


def main():
    lines = []
    out = lines.append
    out("HOST MARGIN against the worst peak of %.1f W" % P_PEAK)
    out("%-4s %-34s %7s %5s %9s  %s" % ("cls", "host", "P_avail", "eta", "margin W", "verdict"))
    for c, h, p, eta, tag, note in HOSTS:
        m = p * eta - P_PEAK
        verdict = "carries the peak" if m >= 0 else "needs the Buffer tier"
        out("%-4s %-34s %7.2f %5.2f %9.2f  %s" % (c, h, p, eta, m, verdict))
    out("")
    # Qi efficiency from the BRIEF heat figures: 25 W in, 5.8 to 6.9 W of heat.
    lo = (25.0 - 6.9) / 25.0
    hi = (25.0 - 5.8) / 25.0
    out("Qi2 25 W receive efficiency from the BRIEF heat: %.2f to %.2f" % (lo, hi))
    # Mean power of the Full tier session from the BRIEF figures.
    pmin = E_BODY_WH[0] / SESSION_H[1]
    pmax = E_BODY_WH[1] / SESSION_H[0]
    out("Mean session power bracket (5.9 Wh over 3.7 h to 7.4 Wh over 2 h): %.2f to %.2f W" % (pmin, pmax))
    out("")
    out("Buffer energy to carry the peak gap for a hand-over of t seconds, 8.7 W peak:")
    for t in (2, 10, 30, 60):
        out("  t = %3d s: %.1f J = %.4f Wh" % (t, P_PEAK * t, P_PEAK * t / 3600.0))
    out("")
    out("Source and tag of each row")
    for c, h, p, eta, tag, note in HOSTS:
        out("  %-4s %s (%s)" % (c, tag, note))
    text = "\n".join(lines)
    print(text)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "out", "host_margin.txt"), "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
