"""Replay vectors/rtl_events.json into the RTL with amaranth.sim.

Checks every verdict, digest and seq against the Python reference, and
records the cycles per slice. Writes build/sim_cycles.json.
Run: python3 sim/test_slice_auth.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "hdl"))
from amaranth.sim import Simulator
from slice_auth import SliceAuth

events = json.load(open(os.path.join(HERE, "..", "vectors", "rtl_events.json")))
dut = SliceAuth()
log = []


async def tb(ctx):
    first_load = True
    for e in events:
        if e["op"] in ("load", "clear"):
            writes = []
            s = e["slot"] << 5
            if e["op"] == "load":
                writes += [(s | i, int(v, 16)) for i, v in enumerate(e["prefix"])]
                sid = bytes.fromhex(e["sid"])
                writes += [(25, int.from_bytes(sid[:8], "little")),
                           (26, int.from_bytes(sid[8:], "little")), (s | 27, 1)]
                if first_load:
                    writes.append((28, 0))
                    first_load = False
            else:
                writes.append((s | 27, 0))
            for a, d in writes:
                ctx.set(dut.cfg_we, 1); ctx.set(dut.cfg_addr, a); ctx.set(dut.cfg_data, d)
                await ctx.tick()
            ctx.set(dut.cfg_we, 0)
            continue
        words = [int(w, 16) for w in e["words"]]
        cycles = 0
        for k, wv in enumerate(words):
            ctx.set(dut.in_data, wv); ctx.set(dut.in_valid, 1)
            ctx.set(dut.in_last, int(k == len(words) - 1))
            while not ctx.get(dut.in_ready):
                await ctx.tick(); cycles += 1
            await ctx.tick(); cycles += 1
        ctx.set(dut.in_valid, 0); ctx.set(dut.in_last, 0)
        while not ctx.get(dut.res_valid):
            await ctx.tick(); cycles += 1
            assert cycles < 100000, "no verdict"
        err = ctx.get(dut.res_err)
        ok = err == e["err"]
        if "digest" in e and e["err_name"] not in ("LENGTH", "BAD_VERSION"):
            dg = ctx.get(dut.res_digest).to_bytes(32, "little").hex()
            ok &= dg == e["digest"]
            ok &= ctx.get(dut.res_seq) == e["seq"]
        log.append(dict(name=e["name"], words=len(words), cycles=cycles, err=err,
                        expect=e["err"], pass_=bool(ok)))
        await ctx.tick()


sim = Simulator(dut)
sim.add_clock(5e-9)          # 200 MHz
sim.add_testbench(tb)
sim.run()

bad = [l for l in log if not l["pass_"]]
for l in log:
    print(f"{'PASS' if l['pass_'] else 'FAIL'}  {l['name']:<48} words {l['words']:>5}  cycles {l['cycles']:>6}  err {l['err']}")
os.makedirs(os.path.join(HERE, "..", "build"), exist_ok=True)
json.dump(log, open(os.path.join(HERE, "..", "build", "sim_cycles.json"), "w"), indent=1)
print(f"\n{len(log) - len(bad)}/{len(log)} slices match the reference")
sys.exit(1 if bad else 0)
