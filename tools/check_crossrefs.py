#!/usr/bin/env python3
"""check_crossrefs.py — the count check (PRG-15) and the assembly check (PRG-16).

Two duties:

  PRG-15  one count. The gate rows of FINAL/*.md are counted, the counts are
          compared with tools/canon.json, and every "<n> gates" or "<n> items"
          claim in the tree is checked against the canonical set. A number that
          is not canonical is a defect, because two counts is a defect.

  PRG-16  the assembly. The assembled directive must carry each part once, in
          ascending order, and every FINAL file must carry one H1 header.

Usage:
    python3 check_crossrefs.py            # from the LEAF directory
    python3 check_crossrefs.py --fix-canon   # write the counted gate numbers
                                             # into canon.json after a review

Exit code 0 when the tree agrees with canon.json, 1 on a defect.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEAF = os.path.dirname(HERE)
FINAL = os.path.join(LEAF, "FINAL")
CANON = os.path.join(HERE, "canon.json")
ASSEMBLED = os.path.join(LEAF, "BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md")

DEVICE_PREFIXES = ("MEC", "ENR", "DSP", "RF", "CAM", "CLR", "FLD", "SW", "DST",
                    "DUO", "SZ", "B", "EY", "RL", "MON", "HST")
PROGRAM_PREFIX = "PRG"
RESEARCH_PREFIX = "RG"

DEF_RE = re.compile(r"^\|\s*\*{0,2}([A-Z]{2,4}|B)-(\d{1,3})\*{0,2}\s*\|")
CLAIM_RE = re.compile(r"\b(\d{1,3})\s+(gates|items)\b")
PART_RE = re.compile(r"^# BUDLUM LEAF .* PART (\d+)")


def gate_rows():
    seen = {}
    for f in sorted(glob.glob(os.path.join(FINAL, "*.md"))):
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            m = DEF_RE.match(line)
            if m:
                seen.setdefault(f"{m.group(1)}-{m.group(2)}", []).append(
                    os.path.basename(f) + ":" + str(n))
    return seen


def counts(seen):
    d = sum(1 for k in seen if k.split("-")[0] in DEVICE_PREFIXES)
    p = sum(1 for k in seen if k.split("-")[0] == PROGRAM_PREFIX)
    r = sum(1 for k in seen if k.split("-")[0] == RESEARCH_PREFIX)
    return d, p, r, d + p + r


def claims(canon):
    ok = {canon["device_and_network_gates"], canon["program_gates"],
          canon["research_gates"], canon["gates_total"],
          canon["gap_items"], canon["gap_blockers"], canon["gap_major"],
          canon["gap_minor"]}
    hits = []
    for f in sorted(glob.glob(os.path.join(FINAL, "*.md"))) + [ASSEMBLED]:
        if not os.path.exists(f):
            continue
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            for num, word in CLAIM_RE.findall(line):
                n_i = int(num)
                if n_i < 10:            # a small number is not a count claim
                    continue
                hits.append((os.path.basename(f), n, n_i, word,
                             n_i in ok, line.strip()[:90]))
    return hits


def assembly_check():
    if not os.path.exists(ASSEMBLED):
        print("PRG-16  no assembled file yet")
        return 0
    parts, dup = [], []
    for line in open(ASSEMBLED, encoding="utf-8"):
        m = PART_RE.match(line)
        if m:
            p = int(m.group(1))
            if p in parts:
                dup.append(p)
            parts.append(p)
    bad = [a for a, b in zip(parts, parts[1:]) if b <= a]
    print(f"PRG-16  parts in the assembled file: {len(parts)}"
          f"  first {parts[:3]}  last {parts[-3:] if parts else []}")
    if dup:
        print("PRG-16  FAIL duplicate part numbers:", sorted(set(dup)))
    if bad:
        print("PRG-16  FAIL the order breaks at:", bad)
    files = sorted(glob.glob(os.path.join(FINAL, "*.md")))
    miss = []
    for f in files:
        h1 = [l for l in open(f, encoding="utf-8") if l.startswith("# ")]
        if len(h1) != 1:
            miss.append((os.path.basename(f), len(h1)))
    if miss:
        print("PRG-16  FAIL a file must carry one H1 header:", miss)
    print(f"PRG-16  FINAL files: {len(files)}, each with one H1 header"
          if not miss else "")
    return 1 if (dup or bad or miss) else 0


def main(argv):
    canon = json.load(open(CANON))
    seen = gate_rows()
    d, p, r, t = counts(seen)
    print(f"PRG-15  gate rows: device and network {d}, program {p}, "
          f"research {r}, total {t}")
    if "--fix-canon" in argv:
        canon.update(device_and_network_gates=d, program_gates=p,
                     research_gates=r, gates_total=t)
        json.dump(canon, open(CANON, "w"), indent=2)
        print("PRG-15  canon.json written")
        return 0
    fail = 0
    for key, val in (("device_and_network_gates", d), ("program_gates", p),
                     ("research_gates", r), ("gates_total", t)):
        if key in canon and canon[key] != val:
            print(f"PRG-15  FAIL canon says {key} = {canon[key]}, "
                  f"the tree counts {val}")
            fail = 1
    hits = claims(canon)
    wrong = [h for h in hits if not h[4]]
    for f, n, num, word, ok, text in hits:
        mark = "ok  " if ok else "FAIL"
        print(f"PRG-15  {mark} {f}:{n}  '{num} {word}'  {text}")
    if wrong:
        print(f"PRG-15  FAIL {len(wrong)} count claim(s) disagree with canon")
        fail = 1
    else:
        print(f"PRG-15  every count claim agrees with canon ({len(hits)} claims)")
    fail |= assembly_check()
    return fail


if __name__ == "__main__":
    sys.exit(main(sys.argv))
