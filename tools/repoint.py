#!/usr/bin/env python3
"""repoint.py — the one repoint step after an edit, in the order the rules demand.

It does four things and it never guesses:

  1. runs tools/assemble.py and reads the line and character counts of v5,
  2. measures the prose of FINAL and MASTER with tools/check_prose.py,
  3. writes the prose numbers into tools/canon.json,
  4. repoints the mirrors: FINAL/00-front-and-map.md and MASTER/STATE.md.

Usage:
    python3 tools/repoint.py            # measure, write, repoint
    python3 tools/repoint.py --dry      # measure and print, write nothing

Gate PRG-15 owns the counts, so this script is a convenience, not a second
authority: it writes exactly the numbers that check_prose and assemble print.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEAF = os.path.dirname(HERE)


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=LEAF, capture_output=True, text=True)
    return p.stdout + p.stderr


def main():
    dry = "--dry" in sys.argv
    out = run(["tools/assemble.py"])
    lines = re.search(r"lines: (\d+), characters: (\d+)", out)
    gates = re.search(r"canon: (\d+) gates, (\d+) device and network, (\d+) program, (\d+) research, (\d+) gaps", out)
    prose = run(["tools/check_prose.py", "--summary", "FINAL", "MASTER"])
    tot = re.search(r"TOTAL (\d+) files\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s", prose)
    if not (lines and gates and tot):
        print("measurement failed")
        print(out[-800:], prose[-800:])
        return 1
    ln, ch = int(lines.group(1)), int(lines.group(2))
    gtot, gdev, gprg, grg, gaps = (int(g) for g in gates.groups())
    files, em, sent, lng, cells, warn = (int(v) for v in tot.groups())
    pct = 100.0 * lng / sent
    print("v5 %d lines, %d characters" % (ln, ch))
    print("gates %d (%d device, %d program, %d research), gaps %d" % (gtot, gdev, gprg, grg, gaps))
    print("prose %d sentences, %d long, %d long cells, %d warning words, %d em dashes, %.1f percent long"
          % (sent, lng, cells, warn, em, pct))
    if dry:
        return 0

    # 1 · canon.json
    p = os.path.join(HERE, "canon.json")
    s = open(p).read()
    s = re.sub(r'"device_and_network_gates": \d+', '"device_and_network_gates": %d' % gdev, s)
    s = re.sub(r'"program_gates": \d+', '"program_gates": %d' % gprg, s)
    s = re.sub(r'"research_gates": \d+', '"research_gates": %d' % grg, s)
    s = re.sub(r'"gates_total": \d+', '"gates_total": %d' % gtot, s)
    s = re.sub(r'"gap_items": \d+', '"gap_items": %d' % gaps, s)
    s = re.sub(r'"sentences_total": \d+', '"sentences_total": %d' % sent, s)
    s = re.sub(r'"long_sentences": \d+', '"long_sentences": %d' % lng, s)
    s = re.sub(r'"long_cells": \d+', '"long_cells": %d' % cells, s)
    s = re.sub(r'"warn_words": \d+', '"warn_words": %d' % warn, s)
    s = re.sub(r'"em_dashes": \d+', '"em_dashes": %d' % em, s)
    open(p, "w").write(s)
    print("canon.json written")

    # 2 · FINAL/00 mirror
    p = os.path.join(LEAF, "FINAL", "00-front-and-map.md")
    s = open(p).read()
    s = re.sub(r"\*\*\d+ gates: \d+ device and network, \d+ program and \d+ research\*\*",
               "**%d gates: %d device and network, %d program and %d research**" % (gtot, gdev, gprg, grg), s)
    s = re.sub(r"\*\*\d+ sentences over the limit of [\d ]+, at \d\.\d percent\*\*",
               "**%d sentences over the limit of %s, at %.1f percent**" % (lng, "{:,}".format(sent).replace(",", " "), pct), s)
    s = re.sub(r"with \d+ long table cells", "with %d long table cells" % cells, s)
    s = re.sub(r"\d+ gates of \d+ device and network, \d+ program and \d+ research",
               "%d gates of %d device and network, %d program and %d research" % (gtot, gdev, gprg, grg), s)
    s = re.sub(r"\*\*The [a-z-]+ drawing sheets\*\*", "**The twenty-five drawing sheets**", s)
    open(p, "w").write(s)
    print("FINAL/00 repointed")

    # 3 · FINAL/16 mirror
    p = os.path.join(LEAF, "FINAL", "16-gap-register.md")
    s = open(p).read()
    s = re.sub(r"written, with \d+ gates and one record format",
               "written, with %d gates and one record format" % gtot, s)
    open(p, "w").write(s)
    print("FINAL/16 repointed")

    # 4 · MASTER/STATE mirror
    p = os.path.join(LEAF, "MASTER", "STATE.md")
    s = open(p).read()
    s = re.sub(r"\*\*\d+ gates\*\* \(\d+ device and net", "**%d gates** (%d device and net" % (gtot, gdev), s)
    s = re.sub(r"is \*\*[\d ]+ lines and [\d ]+ characters\*\*",
               "is **%s lines and %s characters**" % ("{:,}".format(ln).replace(",", " "), "{:,}".format(ch).replace(",", " ")), s)
    open(p, "w").write(s)
    print("MASTER/STATE repointed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
