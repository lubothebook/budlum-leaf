#!/usr/bin/env python3
"""validator_sizing.py - the compute of the optional dock validator module.

Dock team, hw/dock/. Gates SW-20, DST-12, RG-18.

The dock validator renders Leaf frames at 1600 x 3200 and 240 Hz,
deterministically in fixed point, and runs the Budlum chain duty.

1. It runs bench/ (the leaf-duty rasteriser of validator/leaf-duty, mounted
   read only) and takes the best of five runs. The bench renders the demo
   wallet scene with Q16.16 arithmetic and hashes 16 slices with SHA-256.
2. It turns the measured cost into a per-session need at 240 Hz.
3. It checks four candidate modules against two sessions (one served and
   one hot shadow, DST-12) plus the chain duty.

Run:  python3 hw/dock/validator_sizing.py        (cargo builds bench/ once)
Out:  hw/dock/out/validator_sizing.json, hw/dock/out/validator_sizing.txt
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BENCH = os.path.join(HERE, "bench")
os.makedirs(OUT, exist_ok=True)

W, H, HZ = 1600, 3200, 240
FRAME_BYTES = W * H * 4
SLICES = 16                       # T validator/leaf-duty/src/raster.rs
SPEC_COUNT = 2                    # H: speculative frames per frame (render_spec)
SESSIONS = 2                      # D dock team: one served, one hot shadow (DST-12)
CHAIN_CORES = 1.0                 # H: consensus, BLS12-381 + ML-DSA-65, 6 s slot
NET_CORES = 0.5                   # H: QUIC, 2 x 2 paths, the stream packer
CHAIN_RAM_GB = 6.0                # H: state cache, mempool, peers
GPU_OPS_PER_PX = 40.0             # H: integer ops per touched pixel (blend, coverage)
SIMD_SPEEDUP = 4.0                # H: integer NEON/AVX2 port of the scalar raster

lines = []


def p(s=""):
    lines.append(s)
    print(s)


def run_bench():
    exe = os.path.join(BENCH, "target", "release", "dock-render-bench")
    if not os.path.exists(exe):
        subprocess.run(["cargo", "build", "--release", "--offline"], cwd=BENCH, check=True)
    runs = []
    for _ in range(5):
        r = subprocess.run([exe, "1", "30"], capture_output=True, text=True, check=True)
        runs.append(json.loads(r.stdout.strip().replace("[", "\"").replace("]", "\"")
                               .replace("\"\"", "\"")))
    best = min(runs, key=lambda d: d["ms_per_frame"])
    best_hash = min(d["hash_ms_per_frame"] for d in runs)
    return best, best_hash, runs


# The candidates. Every figure is [HYPOTHESIS] unless the source says
# [PUBLICATION]. core_vs_ref: scalar integer speed of one big core against
# the reference core of this sandbox (Xeon at 2.1 GHz). sha_gbps: SHA-256 per
# core with the SHA-2 instructions.
CANDIDATES = [
    dict(name="NVIDIA Jetson Orin NX 16 GB", big_cores=8, core_vs_ref=0.85, sha_gbps=1.3,
         mem_gbps=102.4, gpu_tops_int=0.94, ram_gb=16, w_typ=18, w_max=25, size="69.6 x 45 mm SO-DIMM",
         cost_usd=700, src="P NVIDIA Jetson Orin NX datasheet: 8 x A78AE, 1024 CUDA cores, 102.4 GB/s"),
    dict(name="NVIDIA Jetson AGX Orin 32 GB", big_cores=8, core_vs_ref=0.95, sha_gbps=1.4,
         mem_gbps=204.8, gpu_tops_int=1.7, ram_gb=32, w_typ=25, w_max=40, size="100 x 87 mm",
         cost_usd=1000, src="P NVIDIA Jetson AGX Orin datasheet"),
    dict(name="Rockchip RK3588 SoM", big_cores=4, core_vs_ref=0.80, sha_gbps=1.4,
         mem_gbps=34.0, gpu_tops_int=0.0, ram_gb=16, w_typ=8, w_max=12, size="about 70 x 50 mm",
         cost_usd=180, src="P Rockchip RK3588 brief: 4 x A76 + 4 x A55, LPDDR4x/5"),
    dict(name="AMD Ryzen 7 8845HS COM", big_cores=8, core_vs_ref=1.6, sha_gbps=2.2,
         mem_gbps=120.0, gpu_tops_int=0.0, ram_gb=32, w_typ=28, w_max=54, size="COM Express Mini, 84 x 55 mm",
         cost_usd=650, src="P AMD product page: 8 x Zen 4, LPDDR5x-7500"),
]


def size(bench, hash_ms):
    renders = 1 + SPEC_COUNT
    raster_ms = max(bench["ms_per_frame"] - bench["hash_ms_per_frame"], 1e-3)
    od = bench["overdraw"]
    ref_hash_gbps = FRAME_BYTES / (hash_ms * 1e-3) / 1e9
    need = dict(
        renders_per_frame=renders,
        hash_GBps=renders * FRAME_BYTES * HZ / 1e9,
        hash_streams=renders * SLICES,
        raster_ref_core_s_per_s=renders * raster_ms * 1e-3 * HZ,
        touched_Gpx_per_s=renders * od * W * H * HZ / 1e9,
    )
    need["gpu_Gops"] = need["touched_Gpx_per_s"] * GPU_OPS_PER_PX
    need["mem_GBps"] = need["touched_Gpx_per_s"] * 8.0 + need["hash_GBps"] + 0.1
    need["frame_ring_MB"] = (renders + 2) * FRAME_BYTES / 1e6
    p("1 · the measured reference (best of 5 runs, one core of this sandbox)")
    p("  %.1f ms per 1600 x 3200 frame, of which SHA-256 of 16 slices %.1f ms (%.2f GB/s)"
      % (bench["ms_per_frame"], bench["hash_ms_per_frame"], ref_hash_gbps))
    p("  %d primitives per frame, overdraw %.2f, frame hash prefix %s"
      % (bench["prims_per_frame"], od, bench["frame_hash"]))
    p("  the scalar reference reaches %.1f frames/s on one core. 240 Hz needs %.0f x that"
      % (1000.0 / bench["ms_per_frame"], HZ * bench["ms_per_frame"] / 1000.0))
    p("")
    p("2 · one session at 240 Hz with %d speculative frames, so %d renders per frame" % (SPEC_COUNT, renders))
    p("  SHA-256: %.1f GB/s in %d sequential streams of 1.28 MB" % (need["hash_GBps"], need["hash_streams"]))
    p("  raster: %.1f reference-core-seconds per second (scalar), %.2f Gpx/s touched, %.0f Gops/s on a GPU"
      % (need["raster_ref_core_s_per_s"], need["touched_Gpx_per_s"], need["gpu_Gops"]))
    p("  memory traffic %.1f GB/s, frame ring %.0f MB" % (need["mem_GBps"], need["frame_ring_MB"]))
    p("")
    out = []
    p("3 · the candidates, %d sessions + the chain duty" % SESSIONS)
    p("  %-30s %6s %6s %6s %6s %6s %7s  %s" % ("module", "hashC", "rastC", "needC", "haveC", "memBW", "GPU", "verdict"))
    for c in CANDIDATES:
        hash_cores = SESSIONS * need["hash_GBps"] / c["sha_gbps"]
        if c["gpu_tops_int"] > 0:
            raster_cores = 0.25 * SESSIONS          # H: the scene build and the GPU feed
            gpu_util = SESSIONS * need["gpu_Gops"] / (c["gpu_tops_int"] * 1000.0)
        else:
            raster_cores = SESSIONS * need["raster_ref_core_s_per_s"] / c["core_vs_ref"] / SIMD_SPEEDUP
            gpu_util = 0.0
        need_cores = hash_cores + raster_cores + CHAIN_CORES + NET_CORES
        mem_util = SESSIONS * need["mem_GBps"] / c["mem_gbps"]
        ok = need_cores <= 0.85 * c["big_cores"] and mem_util <= 0.6 and gpu_util <= 0.7
        verdict = "meets 2 sessions" if ok else "short"
        sess_max = 0
        for s in range(1, 9):
            hc = s * need["hash_GBps"] / c["sha_gbps"]
            rc = (0.25 * s) if c["gpu_tops_int"] > 0 else s * need["raster_ref_core_s_per_s"] / c["core_vs_ref"] / SIMD_SPEEDUP
            gu = s * need["gpu_Gops"] / (c["gpu_tops_int"] * 1000.0) if c["gpu_tops_int"] > 0 else 0
            if (hc + rc + CHAIN_CORES + NET_CORES <= 0.85 * c["big_cores"]
                    and s * need["mem_GBps"] / c["mem_gbps"] <= 0.6 and gu <= 0.7):
                sess_max = s
        p("  %-30s %6.1f %6.1f %6.1f %6d %5.0f%% %6.0f%%  %s, %d sessions max"
          % (c["name"], hash_cores, raster_cores, need_cores, c["big_cores"], 100 * mem_util,
             100 * gpu_util, verdict, sess_max))
        out.append(dict(c, hash_cores=hash_cores, raster_cores=raster_cores, need_cores=need_cores,
                        mem_util=mem_util, gpu_util=gpu_util, meets=ok, sessions_max=sess_max))
    p("")
    p("4 · no SoC alone serves %d sessions with %d renders per frame. The SHA-256 streams" % (SESSIONS, renders))
    p("  and the DRAM traffic of the overdraw are the walls. Without speculation (1 render):")
    need0 = dict(need)
    for k in ("hash_GBps", "raster_ref_core_s_per_s", "touched_Gpx_per_s", "gpu_Gops", "mem_GBps"):
        need0[k] = need[k] / renders
    need0["hash_streams"] = SLICES
    for c in out:
        hc = need0["hash_GBps"] / c["sha_gbps"]
        rc = 0.25 if c["gpu_tops_int"] > 0 else need0["raster_ref_core_s_per_s"] / c["core_vs_ref"] / SIMD_SPEEDUP
        nc = hc + rc + CHAIN_CORES + NET_CORES
        mu = need0["mem_GBps"] / c["mem_gbps"]
        c["one_session_no_spec"] = dict(need_cores=nc, mem_util=mu, meets=nc <= 0.85 * c["big_cores"] and mu <= 0.6)
        p("  %-30s needs %4.1f of %d cores, memory %3.0f %%: %s" % (c["name"], nc, c["big_cores"], 100 * mu,
          "1 session" if c["one_session_no_spec"]["meets"] else "short"))
    p("")
    fe = frame_engine(need, SESSIONS)
    p("5 · the frame engine (the U6 twin), %d sessions x %d renders at 240 Hz" % (SESSIONS, renders))
    p("  SHA-256 core %.2f GB/s at %.0f MHz, %d slice(s) per core, %d cores"
      % (fe["sha_gbps_core"], FE_CLK_MHZ, fe["slices_per_core"], fe["sha_cores"]))
    p("  %d pixel engines of %d px/clock, %d LUT, %.1f MB on-chip band RAM, DRAM %.1f GB/s"
      % (fe["px_engines"], PX_PER_CLK, fe["lut"], fe["onchip_MB"], fe["dram_GBps"]))
    p("  fits: %s, about %s W, about %s USD" % (fe["fpga"], fe["fpga_w"], fe["fpga_usd"]))
    pick = next(c for c in out if "Orin NX" in c["name"])
    pick = dict(pick, frame_engine=fe)
    p("")
    p("6 · the pick: %s as the host (chain, scene build, QUIC, PKCS#11 in the TEE)" % pick["name"])
    p("  plus the %s frame engine on PCIe Gen3 x4." % fe["fpga"])
    p("  module power %d to %d W + %s W, cost about %d + %s USD"
      % (pick["w_typ"], pick["w_max"], fe["fpga_w"], pick["cost_usd"], fe["fpga_usd"]))
    p("  the ASIC path: the same engine as a U6-class die, about 3 W  [HYPOTHESIS]")
    p("  the rule of determinism: integer and Q16.16 only, on the CPU and on the GPU alike.")
    p("  Integer GPU arithmetic is bit-exact, so two validators on two kinds of silicon agree.")
    p("  The SHA-256 slice hash is sequential inside a slice. It, not the raster, sets the CPU count.")
    p("  chain duty: RAM %.0f GB + frame rings %.0f MB, NVMe 1 TB, a PKCS#11 signer (README s4)"
      % (CHAIN_RAM_GB, SESSIONS * need["frame_ring_MB"]))
    return need, out, pick


# ------------------------------------------------------------------ the frame engine
# The ambitious real path: a fixed-function frame engine beside the host SoC.
# It renders each slice in bands of rows in on-chip RAM and feeds the band to
# a SHA-256 core as it lands, so the overdraw never reaches DRAM. It is the
# twin of U6 in the Leaf. FPGA first, ASIC later.  [HYPOTHESIS]
FE_CLK_MHZ = 300.0
SHA_ROUNDS_PER_CLK = 2            # H: two unrolled rounds per clock
SHA_LUT = 2200                    # H: one SHA-256 core with its band FIFO
PX_PER_CLK = 16                   # H: one pixel engine, Q16.16 blend lanes
PX_ENGINE_LUT = 28000             # H
INFRA_LUT = 45000                 # H: PCIe Gen3 x4, DMA, scene parser, AXI
BAND_ROWS = 4                     # rows per band, double-buffered per hash core
FPGAS = [
    dict(name="AMD Kintex UltraScale+ KU5P", lut=216960, ram_mb=(16.9 + 18.0) / 8, w=10, usd=1100),
    dict(name="AMD Kintex UltraScale+ KU11P", lut=298560, ram_mb=(21.1 + 22.5) / 8, w=13, usd=1700),
    dict(name="AMD Kintex UltraScale+ KU15P", lut=522720, ram_mb=(34.6 + 36.0) / 8, w=18, usd=2600),
]


def frame_engine(need, sessions):
    sha_gbps_core = 64.0 / (64.0 / SHA_ROUNDS_PER_CLK) * FE_CLK_MHZ * 1e6 / 1e9
    per_stream = need["hash_GBps"] / need["hash_streams"]
    slices_per_core = max(1, int(sha_gbps_core / per_stream))
    sha_cores = -(-sessions * need["hash_streams"] // slices_per_core)
    px_engines = -(-int(sessions * need["touched_Gpx_per_s"] * 1e9) // int(PX_PER_CLK * FE_CLK_MHZ * 1e6 * 0.8))
    lut = sha_cores * SHA_LUT + px_engines * PX_ENGINE_LUT + INFRA_LUT
    ram_mb = sha_cores * 2 * BAND_ROWS * W * 4 / 1e6
    dram = sessions * (need["hash_GBps"] / 3.0 * 0 + 0.6)   # H: scenes, images, the out stream
    fit = next((f for f in FPGAS if lut <= 0.8 * f["lut"] and ram_mb <= 0.8 * f["ram_mb"]), None)
    return dict(sha_gbps_core=sha_gbps_core, slices_per_core=slices_per_core, sha_cores=sha_cores,
                px_engines=px_engines, lut=lut, onchip_MB=ram_mb, dram_GBps=dram,
                fpga=fit["name"] if fit else None, fpga_w=fit["w"] if fit else None,
                fpga_usd=fit["usd"] if fit else None)


def main():
    p("BUDLUM LEAF DOCK L.6.0 · the validator module sizing · gates SW-20, DST-12, RG-18")
    p("")
    try:
        bench, hash_ms, runs = run_bench()
        src = "measured now"
    except Exception as e:  # no cargo: the recorded run of 2026-10-12
        bench = dict(ms_per_frame=57.3, hash_ms_per_frame=18.5, overdraw=2.254,
                     prims_per_frame=42, frame_hash="9a 6b 5a be")
        hash_ms, runs, src = 18.5, [], "recorded 2026-10-12 (%s)" % e
    p("bench: %s" % src)
    need, cands, pick = size(bench, hash_ms)
    with open(os.path.join(OUT, "validator_sizing.json"), "w") as f:
        json.dump(dict(bench=bench, runs=runs, need_per_session=need, sessions=SESSIONS,
                       spec_count=SPEC_COUNT, candidates=cands,
                       pick=pick), f, indent=1)
    with open(os.path.join(OUT, "validator_sizing.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
