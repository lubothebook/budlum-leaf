#!/usr/bin/env python3
"""Export the U1 lane to Verilog and count its logic gates with Yosys.

    pip install yowasp-yosys     # once, the WebAssembly build of Yosys
    python3 export_verilog.py

Writes u1_lane.v and results/gates.json. The SRAM arrays stay as $mem cells
(they become compiled SRAM macros); the logic maps to 2-input CMOS gates and
flip-flops. The NAND2 equivalent is the CMOS transistor count / 4.
"""
import json
import os
import re
import subprocess

from amaranth.back import verilog

from u1_rtl import U1Lane

HERE = os.path.dirname(os.path.abspath(__file__))

YS = """
read_verilog -sv {v}
hierarchy -top u1_lane
proc; flatten; opt -full; wreduce; alumacc; share; opt
memory -nomap; opt_clean
techmap; opt -fast
abc -g AND,NAND,OR,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
opt_clean
stat
stat -tech cmos
"""


def main():
    dut = U1Lane()
    v = verilog.convert(dut, name="u1_lane", ports=dut.ports())
    vp = os.path.join(HERE, "u1_lane.v")
    with open(vp, "w") as f:
        f.write(v)
    print("wrote", vp, len(v.splitlines()), "lines")
    ys = os.path.join(HERE, "results", "synth.ys")
    os.makedirs(os.path.dirname(ys), exist_ok=True)
    with open(ys, "w") as f:
        f.write(YS.format(v=vp))
    r = subprocess.run(["yowasp-yosys", "-q", "-l", os.path.join(HERE, "results", "synth.log"),
                        "-s", ys], capture_output=True, text=True)
    log = open(os.path.join(HERE, "results", "synth.log")).read()
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(1)
    cells = {}
    blocks = log.split("Printing statistics.")
    last_plain = blocks[-2]
    for m_ in re.finditer(r"^\s+(\d+)\s+.*?\$_(\w+)_", last_plain, re.M):
        cells[m_.group(2)] = cells.get(m_.group(2), 0) + int(m_.group(1))
    for m_ in re.finditer(r"^\s+\$_(\w+)_\s+(\d+)", last_plain, re.M):
        cells[m_.group(1)] = cells.get(m_.group(1), 0) + int(m_.group(2))
    mems = re.findall(r"\$mem\w*\s+(\d+)|(\d+)\s+.*\$mem", last_plain)
    tr = re.findall(r"Estimated number of transistors:\s+(\d+)", log)
    transistors = int(tr[-1]) if tr else None
    ff = sum(n for k, n in cells.items() if "DFF" in k)
    res = dict(cells=cells, flip_flops=ff, cmos_transistors=transistors,
               nand2_eq=(transistors / 4 if transistors else None))
    with open(os.path.join(HERE, "results", "gates.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
