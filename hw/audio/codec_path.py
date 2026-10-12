#!/usr/bin/env python3
"""codec_path.py - the U3 audio path, the HiFi option and the jack detection.

1. Output: power and voltage into 16, 32 and 300 ohm for the base codec
   and the HiFi DAC option.
2. Ground crosstalk: the shared ground return, with and without a Kelvin
   ground sense on the R2 contact pair.
3. Microphone bias and the CTIA / Android headset button bands.
4. Detection state machine, run against test vectors (plug types, water).
5. The stream from the validator: PCM bit rate and the jitter buffer.

The silicon figures are [HYPOTHESIS] targets for the U3 choice, not a part.
Run:  python3 codec_path.py   -> out/codec.json
"""
import json
import math
import os
import sys

OPTIONS = {
    "base U3": dict(vout_rms=1.0, dnr_db=112, thdn_db=-95, rails="+-1.8 V charge pump"),
    "HiFi DAC": dict(vout_rms=2.0, dnr_db=128, thdn_db=-112, rails="+-2.9 V charge pump"),
}
LOADS = (16.0, 32.0, 300.0)

# Android 3.5 mm headset spec: button bands as resistance on the mic line
BUTTONS = [("A play/pause/hook", 0, 70), ("D voice command", 110, 180),
           ("B volume up", 210, 290), ("C volume down", 360, 680)]
MICBIAS_V, MICBIAS_R = 2.7, 2200.0


def out_power():
    rows = []
    for name, o in OPTIONS.items():
        for RL in LOADS:
            # the amplifier current limit caps the low-impedance power
            i_lim = 0.10 if name == "base U3" else 0.14          # A peak
            v = min(o["vout_rms"], i_lim / math.sqrt(2) * RL)
            p_mw = v**2 / RL * 1e3
            spl = 100 + 10 * math.log10(p_mw)   # a 100 dB/mW headphone
            rows.append(dict(option=name, RL=RL, v_rms=round(v, 3), p_mw=round(p_mw, 1),
                             spl_100dB_per_mW=round(spl, 1)))
    return rows


def crosstalk():
    rows = []
    for RL in (16.0, 32.0):
        for label, Rg in (("device side, no sense", 0.030), ("Kelvin sense on R2", 0.002)):
            xt = 20 * math.log10(Rg / (RL + Rg))
            rows.append(dict(RL=RL, case=label, R_gnd_ohm=Rg, xtalk_db=round(xt, 1)))
    return rows


def button_thresholds():
    rows = []
    for name, lo, hi in BUTTONS:
        v_lo = MICBIAS_V * lo / (lo + MICBIAS_R)
        v_hi = MICBIAS_V * hi / (hi + MICBIAS_R)
        rows.append(dict(button=name, R_lo=lo, R_hi=hi, V_lo=round(v_lo, 3), V_hi=round(v_hi, 3)))
    # gaps between the bands must hold the ADC error (12 bit, 2 % divider)
    gaps = [rows[i + 1]["V_lo"] - rows[i]["V_hi"] for i in range(len(rows) - 1)]
    return rows, min(gaps)


def classify(sw_open, z_tip, z_ring, z_sleeve_r2, z_mic_gnd_leak):
    """Return the state. Impedances in ohm, measured by the codec.
    sw_open: the NC detect leaf is open (a plug lifts T)."""
    if not sw_open:
        return "EMPTY"
    if z_tip > 50e3 and z_ring > 50e3:
        return "MOISTURE OR FOREIGN BODY: bias off, retry in 10 s"
    if z_tip >= 50e3 or z_ring >= 50e3:
        return "MOISTURE OR FOREIGN BODY: bias off, retry in 10 s"
    if z_tip > 1e3:
        # water leaks DC between every pin; a line input leaks none to MIC
        if z_mic_gnd_leak < 50e3:
            return "MOISTURE (ionic leak): bias off, retry in 10 s"
        return "LINE IN of an amplifier"
    if z_sleeve_r2 < 5:
        return "3-POLE headphone"
    if 600 < z_sleeve_r2 < 5e3 and z_mic_gnd_leak > 50e3:
        return "4-POLE CTIA headset"
    if z_sleeve_r2 < 600:
        return "4-POLE, button held at plug-in: wait"
    return "4-POLE OMTP: swap MIC and GND in the codec, then re-measure"


VECTORS = [
    ("no plug", (False, 0, 0, 0, 1e9), "EMPTY"),
    ("32 ohm 3-pole", (True, 32, 32, 0.2, 1e9), "3-POLE headphone"),
    ("CTIA headset", (True, 32, 32, 1800, 1e9), "4-POLE CTIA headset"),
    ("OMTP headset", (True, 32, 32, 1e5, 1e9), "4-POLE OMTP: swap MIC and GND in the codec, then re-measure"),
    ("300 ohm 3-pole", (True, 300, 300, 0.2, 1e9), "3-POLE headphone"),
    ("line in, 10 k", (True, 10e3, 10e3, 0.2, 1e9), "LINE IN of an amplifier"),
    ("salt water, no plug", (True, 4e3, 4e3, 3e3, 3e3), "MOISTURE (ionic leak): bias off, retry in 10 s"),
    ("dry foreign body", (True, 1e8, 1e8, 1e8, 1e9), "MOISTURE OR FOREIGN BODY: bias off, retry in 10 s"),
]


def stream():
    rows = []
    for label, fs, bits, ch in (("default 48 kHz 24 bit stereo", 48000, 24, 2),
                                ("HiFi 96 kHz 24 bit stereo", 96000, 24, 2),
                                ("HiFi 192 kHz 24 bit stereo", 192000, 24, 2),
                                ("uplink 2 mics 48 kHz 24 bit", 48000, 24, 2)):
        mbps = fs * bits * ch / 1e6
        rows.append(dict(stream=label, raw_mbps=round(mbps, 2), packet_10ms_bytes=int(fs * bits * ch / 8 / 100)))
    return rows


def main():
    res = {}
    print("U3 AUDIO PATH, HIFI OPTION, JACK DETECTION")
    res["power"] = out_power()
    print(" 1 output (100 dB/mW headphone for the SPL column)")
    for r in res["power"]:
        print(f"   {r['option']:8s} {r['RL']:5.0f} ohm  {r['v_rms']:.2f} Vrms  {r['p_mw']:6.1f} mW  "
              f"{r['spl_100dB_per_mW']:5.1f} dB SPL")
    res["crosstalk"] = crosstalk()
    print(" 2 ground crosstalk (the cable ground adds its own share)")
    for r in res["crosstalk"]:
        print(f"   {r['RL']:3.0f} ohm {r['case']:22s} {r['xtalk_db']:6.1f} dB")
    rows, gap = button_thresholds()
    res["buttons"] = rows
    res["button_min_gap_V"] = gap
    # ratiometric read: the ADC uses the bias as reference, so the bias error
    # cancels; 2 % divider error at the band edge plus 2 LSB of a 12-bit ADC
    adc_err = max(0.02 * rows[i]["V_hi"] + 2 * MICBIAS_V / 4096 for i in range(len(rows) - 1))
    print(f" 3 buttons on a {MICBIAS_V} V / {MICBIAS_R:.0f} ohm bias; smallest band gap {gap*1e3:.0f} mV, "
          f"ADC and divider error {adc_err*1e3:.0f} mV -> {'PASS' if gap > 2 * adc_err else 'FAIL'}")
    for r in rows:
        print(f"   {r['button']:20s} {r['R_lo']:4d}..{r['R_hi']:4d} ohm  {r['V_lo']:.3f}..{r['V_hi']:.3f} V")
    print(" 4 detection vectors")
    okv = True
    out = []
    for name, v, want in VECTORS:
        got = classify(*v)
        ok = got == want
        okv &= ok
        out.append(dict(vector=name, state=got, ok=ok))
        print(f"   {name:22s} -> {got:58s} {'ok' if ok else 'MISMATCH'}")
    res["detection"] = out
    res["stream"] = stream()
    print(" 5 stream from the validator (raw PCM, no decoder on the Leaf)")
    for r in res["stream"]:
        print(f"   {r['stream']:30s} {r['raw_mbps']:5.2f} Mbit/s, {r['packet_10ms_bytes']} B per 10 ms")
    res["pass"] = bool(okv and gap > 2 * adc_err)
    print("RESULT:", "PASS" if res["pass"] else "FAIL")
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "out", "codec.json"), "w") as fo:
        json.dump(res, fo, indent=1)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
