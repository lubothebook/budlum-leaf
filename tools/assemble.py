#!/usr/bin/env python3
"""assemble.py — the assembly of the single source of truth (gate PRG-16).

The directive is edited as parts in FINAL/. This tool builds the one file that
is handed to a coding AI, a partner or a factory.

The order is fixed here, and it is ascending, so that Part 14 cannot drift to
the end of the file again (the audit F-10).

Usage:
    python3 assemble.py            # build and report
    python3 assemble.py --check    # report only, and refuse a defective tree
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEAF = os.path.dirname(HERE)
FINAL = os.path.join(LEAF, "FINAL")
OUT = os.path.join(LEAF, "BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md")
OUT_ROOT = os.path.join(LEAF, "BUDLUM-LEAF-DIRECTIVE.md")

ORDER = [
    "00-front-and-map.md",
    "01-product.md",
    "02-panel.md",
    "03-body.md",
    "04-energy.md",
    "05-radio-link.md",
    "06-module.md",
    "07-frame-field.md",
    "08-firmware.md",
    "09-network.md",
    "10-distance.md",
    "11-heat.md",
    "12-verification.md",
    "13-build-and-program.md",
    "14-appendices.md",
    "15-hardening.md",
    "16-gap-register.md",
    "17-energy-architecture.md",
    "18-screen-fold-seal.md",
    "19-duo-shape-ip-and-ledger.md",
    "20-charge-path-and-both-face-module.md",
    "21-stretch-stem-and-projection.md",
    "22-host-power-and-the-living-leaf.md",
    "23-core-skin-and-the-heartbeat.md",
]

HEAD = ("# BUDLUM LEAF · THE DIRECTIVE · FINAL EDITION v5.0 · "
        "REVISION L.7 candidate · 2026-10-19 · the assembled single source of truth\n\n"
        "*This file is the concatenation of the twenty-four parts of `LEAF/FINAL/`, "
        "built by `LEAF/tools/assemble.py`. Edit the parts, never this file. "
        "The counts of the gates and of the gaps live in "
        "`LEAF/tools/canon.json` and are checked by gate PRG-15.*\n\n"
        "---\n\n")


def main(argv):
    missing = [f for f in ORDER if not os.path.exists(os.path.join(FINAL, f))]
    if missing:
        print("PRG-16  FAIL missing parts:", missing)
        return 1
    extra = [os.path.basename(f) for f in sorted(os.listdir(FINAL))
             if f.endswith(".md") and f not in ORDER]
    if extra:
        print("PRG-16  FAIL parts that are not in the order list:", extra)
        return 1
    chunks = []
    for f in ORDER:
        text = open(os.path.join(FINAL, f), encoding="utf-8").read().strip()
        chunks.append(text)
    body = "\n\n---\n\n".join(chunks) + "\n"
    lines = body.splitlines()
    parts = [l for l in lines if re.match(r"^# BUDLUM LEAF .* PART \d+", l)]
    heads = [l for l in lines if l.startswith("# BUDLUM LEAF")]
    canon = json.load(open(os.path.join(HERE, "canon.json")))
    print(f"PRG-16  parts in the file: {len(parts)}")
    print(f"PRG-16  H1 headers: {len(heads)} (one front matter and {len(parts)} parts)")
    print(f"PRG-16  lines: {len(lines)}, characters: {len(body)}")
    print(f"PRG-16  canon: {canon['gates_total']} gates, "
          f"{canon['device_and_network_gates']} device and network, "
          f"{canon['program_gates']} program, "
          f"{canon['research_gates']} research, {canon['gap_items']} gaps")
    if "--check" in argv:
        return 0
    open(OUT, "w", encoding="utf-8").write(HEAD + body)
    open(OUT_ROOT, "w", encoding="utf-8").write(HEAD + body)
    print(f"PRG-16  written: {OUT}")
    print(f"PRG-16  written: {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
