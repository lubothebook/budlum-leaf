#!/usr/bin/env python3
# BUDLUM LEAF · tools/add_standing.py · revision L.4.1 · 2026-10-07
# Adds the one standing note of revision L.4.1 to the historical MASTER volumes,
# so a reader never mistakes a revision log for the live state. One file per run,
# an exact match, and it prints the line it wrote.

import sys

NOTE = ("**The standing at revision L.4.1, of 2026-10-07**. The module is **the upright Budlum B module** of `HARDWARE/20` on the top edge of the screen. Its bar is the antenna, its ring holds the camera and round AMOLED, and the battery is a 4-layer flexible sheet. Live numbers are in `MASTER/STATE.md` and in the FINAL parts. `[DECISION]`\n")

TARGETS = {
    "MASTER/06-REVISION-A.md": "**Date:** 2026-10-05 · the answers of Ayaz to the first six questions · this log is the trace of every number that moved.",
    "MASTER/07-REVISION-B.md": "**Date:** 2026-10-05 · the answers of Ayaz to the second six questions · this log lists every change that the answers made.",
    "MASTER/08-REVISION-C.md": "**Date:** 2026-10-05 · the answers of Ayaz to the third six questions · and the Field mode, explained the way a product is sold.",
    "MASTER/15-REVISION-E.md": "**Date:** 2026-10-05 · the answers of Ayaz to the fifth six questions · and the two new doctrines that they produced.",
    "MASTER/16-REVISION-F.md": "**Date:** 2026-10-05 · the answers of Ayaz to the sixth six questions.",
}


def main():
    for path, anchor in TARGETS.items():
        s = open(path).read()
        if "The standing at revision L.4.1" in s:
            print(path, "already carries the note")
            continue
        if s.count(anchor) != 1:
            print("ABORT", path, "anchor count", s.count(anchor))
            return 1
        s = s.replace(anchor, anchor + "\n\n" + NOTE.strip())
        open(path, "w").write(s)
        print(path, "note added")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
