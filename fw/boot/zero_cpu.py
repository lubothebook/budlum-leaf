#!/usr/bin/env python3
"""zero_cpu.py - the Zero-CPU compliance check, chip by chip.

The rule (FINAL/21, Section 21.5.1, Ayaz's decision):
  Leaf has no general-purpose application processor and no operating
  system. It runs no third-party code. Fixed-function silicon with signed
  firmware is allowed: the radios, the modem, the video decoder, the TCON,
  the ISP, the power chip and the secure element. A frame store is allowed.

The six tests, applied to every entry of chips.json:
  Z1 bounded job   the part does a fixed list of jobs (at most 6) and no
                   network input carries instructions
  Z2 no OS shown   nothing outside the part sees a process model, an API or
                   a scheduler; a scheduler inside a part is firmware
  Z3 no third-party code
                   no path loads user, application or validator code; the
                   signers are the chip vendor and Budlum only
  Z4 data only     no interpreter, no script, no JIT, no applet loader
  Z5 signed and measured
                   every updatable code store has a measure method that U7
                   checks, and a vendor signature
  Z6 gated         an updatable part has a hardware gate held closed until
                   U7 passes it (U7 itself is the gate)

Verdicts: PASS, CONDITIONAL (passes, with supplier conditions to buy),
OPEN (a ruling by Ayaz is needed), FAIL (breaks the rule).
The "interfaces" field lists work owed by other teams; it does not change
the verdict.

Run: python3 zero_cpu.py [--markdown]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OK_SIGNERS = {"vendor", "budlum-owner", "budlum-release"}
OK_MEASURE = {"self-rom", "direct", "dice", "owner-key+scrub", "handshake"}
MAX_JOBS = 6


def load(path=os.path.join(HERE, "chips.json")):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["chips"]


def tests(c):
    """Return {Z: (ok, note)} for one chip."""
    t = {}
    t["Z1"] = (len(c["jobs"]) <= MAX_JOBS and not c["instruction_input"],
               f"{len(c['jobs'])} jobs")
    t["Z2"] = (not c["app_visible_os"], c["internal_scheduler"])
    foreign = set(c["signers"]) - OK_SIGNERS
    t["Z3"] = (not c["loads_user_code"] and not foreign,
               "signers " + "+".join(c["signers"]))
    t["Z4"] = (not c["interpreter"] and not c["instruction_input"],
               "interpreter" if c["interpreter"] else "data only")
    has_code = c["size_kib"] > 0
    if has_code or c["updatable"]:
        t["Z5"] = (c["measure"] in OK_MEASURE and "vendor" in c["signers"],
                   c["measure"])
    else:
        t["Z5"] = (True, "no code")
    if c["updatable"] and c["id"] != "U7":
        t["Z6"] = (bool(c["gate"]) and not c["gate"].startswith("none"),
                   "gated")
    else:
        t["Z6"] = (True, "root" if c["id"] == "U7" else "fixed")
    return t


def verdict(c):
    t = tests(c)
    failed = [z for z, (ok, _) in t.items() if not ok]
    if c["open"]:
        return "OPEN", failed
    if failed:
        return "FAIL", failed
    if c["conditions"]:
        return "CONDITIONAL", failed
    return "PASS", failed


def table(chips):
    rows = ["| Part | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 | Verdict |",
            "|---|---|---|---|---|---|---|---|"]
    for c in chips:
        t = tests(c)
        v, _ = verdict(c)
        cells = ["ok" if t[z][0] else "**no**" for z in
                 ("Z1", "Z2", "Z3", "Z4", "Z5", "Z6")]
        rows.append(f"| `{c['id']}` {c['name']} | " + " | ".join(cells) +
                    f" | {v} |")
    return "\n".join(rows)


def main(argv):
    chips = load()
    if "--markdown" in argv:
        print(table(chips))
    bad = 0
    for c in chips:
        v, failed = verdict(c)
        if "--markdown" not in argv:
            print(f"{c['id']:6s} {v:12s} failed={failed} "
                  f"open={len(c['open'])} cond={len(c['conditions'])}")
        if v == "FAIL":
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
