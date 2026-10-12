#!/usr/bin/env python3
"""bootsm.py - the dead-pad and safe-screen boot state machine of the Leaf.

Firmware-Integrity team, revision L.6.0. The executable model behind
STATE-MACHINE.md. It answers two questions:

  1. the time: when is the safe screen on the panel, when is the link up,
     when is the session offered (targets of FINAL/08, Section 8.2:
     20 ms, 60 ms, 150 ms, 300 ms)
  2. the law: for every set of faults, the Leaf ends in a stated, visible
     state, and every refused part is named. A Leaf is never a brick.

All step times are [HYPOTHESIS] until the bench (the boot matrix of FINAL/08,
Section 8.8, step 6) measures them. Change T and rerun.

Run: python3 bootsm.py            the nominal trace and the budgets
     python3 bootsm.py --sweep    every subset of 16 faults (65 536 runs)
"""
import itertools
import json
import os
import sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------ the step times, in ms ---
MiB = 1024 * 1024
T = {
    "aon": 1.0,            # U4 ROM up on the ring cell
    "u7_boot": 8.0,        # U7 ROM checks one internal U7 slot
    "manifest": 6.0,       # ed25519 check of the installed manifest + digest
    "pad": 3.0,            # one dead-pad handshake (FINAL/06, ENR-19)
    "u1_rom": 10.0,        # U1 ROM path and panel driver ready (ring power)
    "rdisp": 5.0,          # rear round AMOLED ready
    "tile_rail": 5.0,      # tile rails ramp after a pad closes
    "compose": 2.0,        # U1 ROM draws the safe screen
    "scan": 1000 / 240,    # one frame at 240 Hz
    "report": 1.0,         # one DICE or signed report to U7
    "radio_assoc": 30.0,   # Wi-Fi fast reconnect with a cached association
    "anchor": 5.0,         # U7 compares the trust anchor
    "offer": 40.0,         # the session offer to the nearest validator
    "u5_resume": 60.0,     # modem leaves standby, RRC resume, signed report
    "u7_spi_Bps": 6.0e6,   # U7 SPI read rate of the boot NOR
    "nor_load_Bps": 52.0e6,  # a chip loading its own image, quad SPI 104 MHz
    "nor_prog_Bps": 0.8e6,   # NOR program rate during an update
}
SIZES = {}   # filled from chips.json


def _load_sizes():
    with open(os.path.join(HERE, "chips.json"), encoding="utf-8") as f:
        for c in json.load(f)["chips"]:
            SIZES[c["id"]] = c["size_kib"] * 1024


_load_sizes()

# --------------------------------------------- the body: quadrant graph ---
SEAT = "Q1"                       # the quadrant under the B module seat
ADJ = {"Q1": ["Q2", "Q3"], "Q2": ["Q1", "Q4"],
       "Q3": ["Q1", "Q4"], "Q4": ["Q2", "Q3"]}

# ----------------------------------------------- the chips and the roles ---
DOMAIN = ["U1", "U6", "U2A", "U2B", "U5", "U3", "U8", "CAM"]   # A/B set
DIRECT_ORDER = ["U4", "U1", "U8", "CAM", "U3"]                  # U7 hashes
DICE = ["U6", "U2A", "U2B"]
LINK_RADIOS = ["U2A", "U5"]

FAULTS = [
    "U7_A", "U7_B",                 # U7 internal slots
    "PAD_B",                        # the 12 B pads to the seat tile
    "PAD_Q1", "PAD_Q2", "PAD_Q3", "PAD_Q4",   # quadrant authenticators
    "U1_HW",                        # U1 silicon dead (ROM path lost)
    "U4_PATCH",                     # U4 patch fails its hash
    "U1_A", "U1_B", "U6_A", "U6_B", "U2A_A", "U2A_B", "U2B_A", "U2B_B",
    "U5_A", "U5_B", "U3_A", "U3_B", "U8_A", "U8_B", "CAM_A", "CAM_B",
    "U5_COLD",                      # the modem was power-cycled
    "ANCHOR",                       # the trust anchor differs
    "STREAM_KEY",                   # the stream key is not an active validator
    "REVOKED",                      # the installed release is revoked
]

VISIBLE = {"SESSION", "SESSION_STATED", "RECOVERY", "UPDATE_REQUIRED",
           "ANCHOR_STATED", "STREAM_REFUSED", "SE_FAULT", "REAR_ONLY",
           "LED_CODE"}


@dataclass
class Result:
    final: str = "BLANK"
    surface: str = "none"             # face, rear, led
    t_safe: float = None              # safe screen visible
    t_link: float = None
    t_session: float = None
    slot: str = "A"
    reverted: bool = False
    wallet: bool = False
    powered: list = field(default_factory=list)      # quadrants at VSYS
    quarantined: list = field(default_factory=list)  # gates held closed
    lines: list = field(default_factory=list)        # the stated lines
    trace: list = field(default_factory=list)        # (t, state, note)

    def log(self, t, state, note=""):
        self.trace.append((round(t, 2), state, note))


def _load_ms(chip):
    return SIZES[chip] / T["nor_load_Bps"] * 1000


def _direct_ms(chip):
    return SIZES[chip] / T["u7_spi_Bps"] * 1000


def boot(faults=(), trial=False):
    f = set(faults)
    unknown = f - set(FAULTS)
    if unknown:
        raise ValueError(f"unknown faults {unknown}")
    r = Result()
    t = 0.0
    r.log(t, "DEAD", "all 64 seam leaves and 12 B pads at 0 V")

    # S1 WAKE: the ring cell powers the always-on domain (U4 ROM, U7)
    t += T["aon"]
    r.log(t, "WAKE", "U4 ROM up, rails of U7 and U1 on")
    t_u1 = t + T["u1_rom"]
    if "U1_HW" in f:
        t_u1 = None

    # S2 ROOT: U7 boots one of its own two slots
    u7_ok = True
    t += T["u7_boot"]
    if "U7_A" in f:
        r.log(t, "ROOT", "U7 slot A refused by U7 ROM")
        t += T["u7_boot"]
        if "U7_B" in f:
            u7_ok = False
            r.log(t, "ROOT", "U7 slot B refused by U7 ROM")
        else:
            r.lines.append("U7 runs its slot B: U7 repair queued")
    t_u7 = t
    if u7_ok:
        r.wallet = True
        r.log(t, "ROOT", "U7 up")

    # S3 SE_FAULT: with no root, no pad can close. Ring power only.
    if not u7_ok:
        r.lines.append("secure element fault: wallet locked, service recovery")
        return _floor(r, t, f, body=False, final="SE_FAULT")

    # S4 PAD_AUTH: B pads, then the quadrants by graph distance
    powered = {}
    if "PAD_B" in f or f"PAD_{SEAT}" in f:
        why = "B pads" if "PAD_B" in f else f"{SEAT} authenticator"
        r.lines.append(f"body refused at the seat ({why}): pads stay at 0 V")
        r.log(t + T["pad"], "PAD_AUTH", f"seat refused: {why}")
    else:
        powered[SEAT] = t + T["pad"]
        frontier = [SEAT]
        while frontier:
            nxt = []
            for q in frontier:
                for n in ADJ[q]:
                    if n in powered or f"PAD_{n}" in f:
                        continue
                    powered[n] = powered[q] + T["pad"]
                    nxt.append(n)
            frontier = nxt
        for q in sorted(ADJ):
            if q not in powered:
                r.lines.append(f"{q} refused by the dead-pad handshake: "
                               "it stays at 0 V")
        r.log(powered[SEAT], "PAD_AUTH",
              "powered " + ",".join(sorted(powered)))
    r.powered = sorted(powered)

    # S5 SAFE_SCREEN: U1 ROM on the seat quadrant, else on the rear panel
    if not powered:
        return _floor(r, t_u7, f, body=False, final="REAR_ONLY")
    if t_u1 is None:
        r.lines.append("U1 fault: LED code on the flash")
        return _floor(r, t_u7, f, body=True, final="LED_CODE")
    t_safe = max(t_u1, powered[SEAT] + T["tile_rail"]) + T["compose"] + T["scan"]
    r.t_safe, r.surface = t_safe, "face"
    r.log(t_safe, "SAFE_SCREEN", "battery, wallet, class line, part lines")

    # S6 VERIFY: U7 checks the installed manifest, then measures
    t_m = t_u7 + T["manifest"]
    r.log(t_m, "VERIFY", "installed manifest signature and digest")
    if "REVOKED" in f:
        r.lines.append("the installed release is revoked: update required")

    def run_domain(slot):
        """Measure the A/B domain in one slot. Returns (fails, times)."""
        fails = {c for c in DOMAIN if f"{c}_{slot}" in f}
        times = {}
        t_dom = powered[SEAT]                    # radio domain powers here
        for c in DICE:
            times[c] = t_dom + _load_ms(c) + T["report"]
        tt = t_m
        for c in DIRECT_ORDER:
            if c == "U4":
                tt += _direct_ms("U4")
                times["U4"] = tt
                continue
            tt += _direct_ms(c)
            times[c] = tt
        # the modem keeps its attach in standby; a cold modem is slow
        times["U5"] = (t_dom + SIZES["U5"] / 100e6 * 1000 + 1500.0
                       if "U5_COLD" in f else t_m + T["u5_resume"])
        return fails, times

    if "U4_PATCH" in f:
        r.lines.append("U4 patch refused: ROM defaults, charge limited")

    fails, times = run_domain("A")
    essential_ok = ("U6" not in fails and "U1" not in fails and
                    any(x not in fails for x in LINK_RADIOS))
    if trial and fails:
        r.reverted = True
        r.lines.append("trial release refused (" + ",".join(sorted(fails)) +
                       "): back to the previous release, floors unchanged")
        essential_ok = False
    if not essential_ok:
        r.slot = "B"
        shift = max(times[c] for c in DICE + ["U1"]) + 1.0
        r.log(shift, "SLOT_B", "radio and stream domain restarts on slot B")
        fails, times = run_domain("B")
        times = {c: v + shift - powered[SEAT] for c, v in times.items()}
        if not r.reverted:
            r.lines.append("running the previous release (slot B)")

    for c in sorted(fails):
        r.quarantined.append(c)
        r.lines.append(f"{c} refused: firmware not attested, held off")
    r.log(max(times.values()), "ATTEST",
          "quarantined " + (",".join(r.quarantined) or "none"))

    # S7 LINK: the first attested link radio
    radios = [c for c in LINK_RADIOS if c not in fails]
    if "U6" in fails or "U1" in fails or not radios:
        r.lines.append("no stream path: recovery through the port part or "
                       "the dock")
        r.final = "RECOVERY"
        return r
    t_link = min(times[c] + (T["radio_assoc"] if c == "U2A" else 0.0)
                 for c in radios)
    r.t_link = t_link
    r.log(t_link, "LINK", "path " + "/".join(radios))

    if "REVOKED" in f:
        r.final = "UPDATE_REQUIRED"
        r.log(t_link, r.final, "only the update class is carried")
        return r

    # S8 ANCHOR and the stream check (SW-22)
    t_a = t_link + T["anchor"]
    if "ANCHOR" in f:
        r.lines.append("trust anchor differs: re-anchor by a second channel")
        r.final = "ANCHOR_STATED"
        r.log(t_a, r.final)
        return r
    if "STREAM_KEY" in f:
        r.lines.append("stream key is not an active validator: refused")
        r.final = "STREAM_REFUSED"
        r.log(t_a, r.final)
        return r

    # S9 SESSION
    t_s = max(t_a, times["U6"], times["U1"]) + T["offer"]
    r.t_session = t_s
    stated = [x for x in r.lines]
    r.final = "SESSION_STATED" if stated else "SESSION"
    r.log(t_s, r.final)
    return r


def _floor(r, t, f, body, final):
    """The floor states that do not reach the radio domain."""
    if "U1_HW" in f:
        r.final, r.surface = "LED_CODE", "led"
        r.t_safe = t + 2.0
        r.log(r.t_safe, "LED_CODE", "U4 ROM blinks the flash LED code")
        return r
    r.final = final
    if final == "LED_CODE":
        return r
    r.surface = "rear"
    r.t_safe = max(t, T["aon"] + T["u1_rom"]) + T["rdisp"] + T["compose"] + T["scan"]
    r.log(r.t_safe, final, "U1 ROM draws the safe screen on the rear panel")
    return r


# ------------------------------------------------------------ budgets ---
def budgets():
    nor = ["U1", "U6", "U2A", "U2B", "U3", "U8", "CAM"]
    nor_bytes = sum(SIZES[c] for c in nor)
    direct_bytes = sum(SIZES[c] for c in DIRECT_ORDER)
    return {
        "boot_nor_one_slot_MiB": nor_bytes / MiB,
        "boot_nor_two_slots_MiB": 2 * nor_bytes / MiB,
        "u7_direct_hash_ms": direct_bytes / T["u7_spi_Bps"] * 1000,
        "u7_scrub_all_nor_s": nor_bytes / T["u7_spi_Bps"],
        "update_write_nor_s": nor_bytes / min(T["u7_spi_Bps"],
                                              T["nor_prog_Bps"]),
        "release_total_MiB": (nor_bytes + SIZES["U5"] + SIZES["U4"] +
                              4 * SIZES["QN"]) / MiB,
    }


def sweep(names=None):
    """Run every subset of `names`. Returns (count, violations)."""
    names = names or ["U7_A", "U7_B", "PAD_B", "PAD_Q2", "PAD_Q4", "U1_HW",
                      "U1_A", "U4_PATCH", "U6_A", "U6_B", "U2A_A", "U2A_B",
                      "U5_A", "U5_B", "U2B_A", "U3_A"]
    bad, n = [], 0
    for k in range(len(names) + 1):
        for combo in itertools.combinations(names, k):
            n += 1
            for trial in (False, True):
                r = boot(combo, trial=trial)
                v = check_law(r, combo)
                if v:
                    bad.append((combo, trial, v))
    return n, bad


def check_law(r, faults):
    """The invariants. Returns a list of broken ones."""
    v = []
    if r.final not in VISIBLE:
        v.append("I1 not a visible state")
    if r.t_safe is None or r.t_safe > 60.0:
        v.append(f"I2 safe screen at {r.t_safe} ms")
    if r.wallet != (not {"U7_A", "U7_B"} <= set(faults)):
        v.append("I3 wallet state wrong")
    for c in r.quarantined:
        if not any(c in line for line in r.lines):
            v.append(f"I4 {c} quarantined in silence")
    if r.final in ("SESSION", "SESSION_STATED"):
        if r.quarantined and r.final == "SESSION":
            v.append("I5 a session hides a refused part")
        for c in ("U6", "U1"):
            if c in r.quarantined:
                v.append(f"I6 session without {c}")
    if faults and r.final == "SESSION":
        fs = set(faults)
        # a fault in an unused B copy is latent: the rest-time scrub finds it
        latent = {x for x in fs if x.endswith("_B") and
                  x[:-2] + "_A" not in fs}
        harmless = {"U5_COLD"} | latent
        if not fs <= harmless:
            v.append("I7 a fault produced a silent session")
    return v


def main(argv):
    r = boot()
    for row in sorted(r.trace, key=lambda x: x[0]):
        print(f"{row[0]:8.2f} ms  {row[1]:13s} {row[2]}")
    print(f"safe screen {r.t_safe:.1f} ms (target 60), link {r.t_link:.1f} ms "
          f"(target 150), session {r.t_session:.1f} ms (target 300)")
    for k, v in budgets().items():
        print(f"{k:26s} {v:8.2f}")
    if "--sweep" in argv:
        n, bad = sweep()
        print(f"sweep: {n} fault sets x 2 modes, {len(bad)} violations")
        for b in bad[:10]:
            print(" ", b)
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
