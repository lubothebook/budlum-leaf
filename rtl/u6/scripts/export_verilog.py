"""Export hdl/slice_auth.py to build/slice_auth.v and run a generic yosys
synthesis for a cell count. Run: python3 scripts/export_verilog.py"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "hdl"))
from amaranth.back import rtlil, verilog
from slice_auth import SliceAuth

out = os.path.join(HERE, "..", "build")
os.makedirs(out, exist_ok=True)
v = verilog.convert(SliceAuth(), name="u6_slice_auth")
path = os.path.join(out, "slice_auth.v")
open(path, "w").write(v)
print(f"wrote {path}: {len(v.splitlines())} lines")

# Generic gate mapping with the yosys build that amaranth ships. It has no
# Verilog frontend and no synth/abc, so it reads the RTLIL of the same design
# and maps to simple gates with simplemap. No logic minimisation: an upper bound.
il = os.path.join(out, "slice_auth.il")
open(il, "w").write(rtlil.convert(SliceAuth(), name="u6_slice_auth"))
script = ("read_rtlil slice_auth.il; proc; flatten; opt; wreduce; opt; "
          "simplemap; opt; opt_clean; write_json slice_auth_gates.json")
r = subprocess.run([sys.executable, "-m", "amaranth_yosys", "-q", "-p", script],
                   capture_output=True, text=True, cwd=out)
if r.returncode:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
import json
from collections import Counter
mods = json.load(open(os.path.join(out, "slice_auth_gates.json")))["modules"]
cnt = Counter(c["type"] for mdl in mods.values() for c in mdl["cells"].values())
os.remove(os.path.join(out, "slice_auth_gates.json"))
# NAND2-equivalent weights of a generic standard-cell library [HYPOTHESIS]
W = {"$_NOT_": 0.67, "$_AND_": 1.33, "$_OR_": 1.33, "$_NAND_": 1.0, "$_NOR_": 1.0,
     "$_XOR_": 2.33, "$_XNOR_": 2.33, "$_MUX_": 2.33, "$_ANDNOT_": 1.33, "$_ORNOT_": 1.33}
ge = 0.0
lines = []
for k, n in sorted(cnt.items(), key=lambda kv: -kv[1]):
    w = 5.0 if "DFF" in k else W.get(k, 2.0)
    ge += w * n
    lines.append(f"{k:<16}{n:>8}")
flops = sum(n for k, n in cnt.items() if "DFF" in k)
rep = "\n".join(lines) + f"\nflip-flops      {flops:>8}\nNAND2-eq (unminimised) {ge/1000:.0f} kGE\n"
open(os.path.join(out, "gate_count.txt"), "w").write(rep)
print(rep)
