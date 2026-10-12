#!/usr/bin/env python3
"""check_prose.py — the writing check of the Budlum Leaf directive.

Gate PRG-12. The rules come from the writing standard of the directive
(ASD-STE100, simplified technical English):

  1. no em dash (U+2014). The en dash (U+2013) is reported and not failed.
  2. a descriptive sentence: 25 words or less.
  3. a procedural sentence: 20 words or less. A line is procedural when it
     starts with a step marker (a digit, a bullet, "Step", "Do", "Turn",
     "Put", "Fit", "Run", "Measure", "Write", "Set", "Hold", "Read").
  4. a rule uses "must" or "can". "should", "may", "might" and "could" are
     reported as a warning, because a rule must not use them.
  5. a table row is not a sentence. A line that starts with "|" is measured
     cell by cell, and only cells longer than 25 words are reported.

Usage:
    python3 check_prose.py FILE [FILE ...]
    python3 check_prose.py --summary DIR [DIR ...]
    python3 check_prose.py --top DIR            # worst 40 sentences of a tree

Exit code: 1 when an em dash is found or a sentence is too long.
          0 when the file passes.

The tool reads only. It never writes to the files it measures.
"""
import glob
import os
import re
import sys

EM = "\u2014"
EN = "\u2013"
STEP_WORDS = ("step", "do", "turn", "put", "fit", "run", "measure",
              "write", "set", "hold", "read", "open", "press", "check")
WARN_WORDS = ("should", "may", "might", "could")


def sentences(text):
    """Split a text into (line number, sentence) pairs.

    A sentence ends at a full stop, a question mark or an exclamation mark
    that is followed by a space, a closing quote or the end of the line.
    """
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            for c in cells:
                if not c:
                    continue
                for part in re.split(r"(?<=[.!?])\s+", c):
                    part = part.strip()
                    if part:
                        out.append((n, part, "cell"))
            continue
        if not stripped or stripped.startswith("#"):
            continue
        body = stripped.lstrip("0123456789.*- \t")
        kind = "prose"
        low = body.lower()
        if stripped[:1].isdigit() or stripped.startswith(("- ", "* ", "| ")):
            kind = "step"
        elif low.startswith(STEP_WORDS):
            kind = "step"
        parts = re.split(r"(?<=[.!?])\s+", stripped)
        for p in parts:
            p = p.strip()
            if p:
                out.append((n, p, kind))
    return out


def words(s):
    return [w for w in re.split(r"\s+", s) if w]


def check(path, listing=False):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    n_em = sum(l.count(EM) for l in lines)
    n_en = sum(l.count(EN) for l in lines)
    long_list, warn_list, long_cells = [], [], []
    total = 0
    for n, s, kind in sentences(text):
        total += 1
        w = len(words(s))
        limit = 20 if kind == "step" else 25
        if w > limit:
            if kind == "cell":
                # a table cell is a label set, and not a sentence. The rule of
                # simplified technical English measures sentences, so a long
                # cell is counted and reported apart, and it does not fail.
                long_cells.append((n, w, s))
            else:
                long_list.append((n, w, limit, kind, s))
    for n, line in enumerate(lines, 1):
        low = line.lower()
        if "uses **must** or **can**" in line:
            continue            # the rule of Part 19.4 names the words it bans
        for w in WARN_WORDS:
            if re.search(r"\b" + w + r"\b", low):
                warn_list.append((n, w, line.strip()[:70]))
    if listing:
        for n, w, limit, kind, s in long_list:
            print(f"  LONG  {path}:{n}  {w} words (limit {limit}, {kind}): {s[:90]}")
        for n, w, line in warn_list:
            print(f"  WARN  {path}:{n}  '{w}': {line}")
    return dict(path=path, em=n_em, en=n_en, sentences=total,
                long=len(long_list), warn=len(warn_list),
                long_cells=len(long_cells), long_list=long_list,
                cell_list=long_cells)


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    leaf = os.path.dirname(here)
    default_dirs = [os.path.join(leaf, d) for d in ("FINAL", "MASTER", "HARDWARE")]
    if len(argv) == 1 or (len(argv) > 1 and argv[1] == "--summary"):
        targets = argv[2:] if len(argv) > 2 else default_dirs
        rows, tot = [], dict(files=0, em=0, en=0, sentences=0, long=0,
                             warn=0, cells=0)
        for d in targets:
            files = sorted(glob.glob(os.path.join(d, "*.md"))) if os.path.isdir(d) else ([d] if os.path.isfile(d) else [])
            for f in files:
                r = check(f)
                rows.append(r)
                tot["files"] += 1
                for k in ("em", "en", "sentences", "long", "warn"):
                    tot[k] += r[k]
                tot["cells"] += r["long_cells"]
        print(f"{'file':50s} {'em':>3s} {'sent':>5s} {'>25':>4s} {'cells':>6s} {'warn':>4s}")
        for r in rows:
            pct = 100.0 * r["long"] / max(r["sentences"], 1)
            print(f"{os.path.basename(r['path']):50s} {r['em']:3d} {r['sentences']:5d} "
                  f"{r['long']:4d} {r['long_cells']:6d} {r['warn']:4d}   {pct:4.1f}% long")
        pct = 100.0 * tot["long"] / max(tot["sentences"], 1)
        print(f"{'TOTAL ' + str(tot['files']) + ' files':50s} {tot['em']:3d} "
              f"{tot['sentences']:5d} {tot['long']:4d} {tot['cells']:6d} {tot['warn']:4d}"
              f"   {pct:4.1f}% of the sentences are long")
        return 1 if (tot["em"] or tot["long"]) else 0

    if len(argv) > 1 and argv[1] == "--top":
        rows = []
        for d in argv[2:]:
            for f in sorted(glob.glob(os.path.join(d, "*.md"))):
                rows += check(f)["long_list"]
        rows.sort(key=lambda r: -r[1])
        print("the worst sentences of the tree, by word count:")
        for n, w, limit, kind, s in rows[:40]:
            print(f"  {w:3d} words (limit {limit}, {kind}): {s[:110]}")
        return 0

    fail = 0
    for f in argv[1:]:
        if os.path.isdir(f):
            for g in sorted(glob.glob(os.path.join(f, "*.md"))):
                r = check(g, listing=True)
                print(f"{os.path.basename(g):50s} em {r['em']:3d}  sentences {r['sentences']:5d}  "
                      f"long {r['long']:4d}  long cells {r['long_cells']:5d}  warn {r['warn']:4d}")
                fail |= 1 if (r["em"] or r["long"]) else 0
        else:
            r = check(f, listing=True)
            print(f"{os.path.basename(f):50s} em {r['em']:3d}  sentences {r['sentences']:5d}  "
                  f"long {r['long']:4d}  long cells {r['long_cells']:5d}  warn {r['warn']:4d}")
            fail |= 1 if (r["em"] or r["long"]) else 0
    return fail


if __name__ == "__main__":
    sys.exit(main(sys.argv))
