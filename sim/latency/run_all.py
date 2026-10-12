#!/usr/bin/env python3
"""run_all.py: every result of the latency team. Gate DST-11.

    python3 run_all.py            # full run, 2 M samples per main path (about 2 min)
    python3 run_all.py --quick    # 200 k samples, for a smoke test

Writes results/results.json, results/summary.txt and plots/*.png.
"""
import argparse
import json
import os
import time
from dataclasses import replace

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
PLOTS = os.path.join(HERE, "plots")

# dataviz reference palette, light mode, fixed order
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK, INK2, GRID = "#1f1f1e", "#5f5e58", "#e4e3dd"
GATE = 30.0

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "legend.frameon": False, "lines.linewidth": 2,
    "figure.dpi": 130, "savefig.bbox": "tight",
})


def run(path, n, seed=1):
    x, st = M.simulate(path, n, seed)
    return x, st, M.stats(x)


def nr_path(**kw):
    p = M.paths()["nr_cell"]
    netkw = {k[4:]: v for k, v in kw.items() if k.startswith("net_")}
    nrkw = {k: v for k, v in kw.items() if not k.startswith(("net_", "scan_", "render_"))}
    scankw = {k[5:]: v for k, v in kw.items() if k.startswith("scan_")}
    renkw = {k[7:]: v for k, v in kw.items() if k.startswith("render_")}
    return replace(p, nr=replace(p.nr, **nrkw), net=replace(p.net, **netkw),
                   scan=replace(p.scan, **scankw), render=replace(p.render, **renkw))


def gate_line(ax, horizontal=True):
    if horizontal:
        ax.axhline(GATE, color=INK2, lw=1, ls="--")
    else:
        ax.axvline(GATE, color=INK2, lw=1, ls="--")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    N = 200_000 if a.quick else 2_000_000      # main paths
    NS = 200_000 if a.quick else 1_000_000     # sweeps
    NH = 100_000 if a.quick else 400_000       # heat map cells
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PLOTS, exist_ok=True)
    R = {"samples": dict(main=N, sweep=NS, heatmap=NH)}
    t_start = time.time()

    # ---------------------------------------------------------------- 1 paths
    P = M.paths()
    R["paths"] = {}
    xs = {}
    for k, p in P.items():
        x, st, s = run(p, N)
        xs[k] = x
        s["stages_mean"] = {g: float(st[g].mean()) for g in M.STAGES}
        s["stages_p99"] = {g: float(np.percentile(st[g], 99)) for g in M.STAGES}
        s["sum_of_stage_p99"] = float(sum(s["stages_p99"].values()))
        s["part21"] = M.PART21[k]
        R["paths"][k] = s
    xp = M.predicted_action(np.random.default_rng(7), N, P["wifi_room"])
    R["predicted"] = M.stats(xp)
    xs["predicted"] = xp

    # ---------------------------------------------------------------- 2 BLER
    blers = [0.0, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]
    R["bler"] = [dict(bler=b, **run(nr_path(bler_ul=b, bler_dl=b), NS)[2]) for b in blers]
    R["bler_dl_only"] = [dict(bler=b, **run(nr_path(bler_ul=0.01, bler_dl=b), NS)[2]) for b in blers]

    # ---------------------------------------------------------------- 3 TDD
    pats = [("DDDSU", {}), ("DDSUU", {}), ("DSUUU", {}), ("DDDDDDDSUU", {}),
            ("DDDSUDDSUU", {}), ("DDDDDDDDSU", {}),
            ("DDDSU + S-slot PUSCH", dict(pattern="DDDSU", s_cfg=(6, 2, 6), s_pusch=True)),
            ("DDDSU + mini-slots", dict(pattern="DDDSU", ul_minislot=2, dl_minislot=7)),
            ("DDDDDDDSUU + mini-slots", dict(pattern="DDDDDDDSUU", ul_minislot=2, dl_minislot=7))]
    R["tdd"] = []
    for name, kw in pats:
        kw = kw or dict(pattern=name)
        R["tdd"].append(dict(pattern=name, **run(nr_path(**kw), NS)[2]))
    R["tdd_bler20"] = []
    for name, kw in pats:
        kw = dict(kw or dict(pattern=name), bler_ul=0.2, bler_dl=0.2)
        R["tdd_bler20"].append(dict(pattern=name, **run(nr_path(**kw), NS)[2]))

    # ---------------------------------------------------------------- 4 load
    loads = [0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95]
    R["load"] = {"priority": [], "best_effort": [], "public": []}
    for L in loads:
        R["load"]["priority"].append(dict(load=L, **run(nr_path(load=L), NS)[2]))
        R["load"]["best_effort"].append(dict(load=L, **run(nr_path(load=L, priority_qos=False), NS)[2]))
        # public cell: no configured grant, no priority, central UPF and regional validator
        R["load"]["public"].append(dict(load=L, **run(nr_path(
            load=L, priority_qos=False, configured_grant=False, sr_period=2,
            net_rtt_ms=12.0, net_cv=0.4), NS)[2]))

    # ---------------------------------------------------------------- 5 handover
    hos = {
        "Rel-15 hard HO": dict(ho_int_ms=(30.0, 60.0), ho_rlf_p=0.01),
        "Rel-16 CHO": dict(ho_int_ms=(30.0, 60.0), ho_rlf_p=0.002),
        "Rel-18 LTM": dict(ho_int_ms=(2.0, 5.0), ho_rlf_p=0.002),
        "Rel-16 DAPS": dict(ho_int_ms=(0.0, 1.0), ho_rlf_p=0.002),
    }
    rates = [0.0, 1 / 60, 1 / 30, 1 / 10, 1 / 5, 1 / 2]
    R["handover"] = {}
    for name, kw in hos.items():
        R["handover"][name] = [dict(rate_hz=r, **run(nr_path(ho_rate_hz=r, **kw), NS)[2]) for r in rates]

    # ---------------------------------------------------------------- 6 gate map
    rtts = [0.3, 1, 2, 4, 6, 8, 10, 12, 14, 16]
    bl = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]
    H = np.zeros((len(bl), len(rtts)))
    for i, b in enumerate(bl):
        for j, r in enumerate(rtts):
            H[i, j] = run(nr_path(bler_ul=b, bler_dl=b, net_rtt_ms=r), NH, seed=3)[2]["p99"]
    R["gate_map"] = dict(rtt_ms=rtts, bler=bl, p99=H.tolist())
    # largest network RTT at p99 <= 30 for each BLER (linear interpolation)
    R["gate_map"]["max_rtt_ms"] = [float(np.interp(GATE, H[i], rtts)) if H[i, 0] < GATE else 0.0
                                   for i in range(len(bl))]

    # ---------------------------------------------------------------- 7 Wi-Fi
    R["wifi"] = []
    for busy in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        for mlo in (True, False):
            p = P["wifi_room"]
            coll = 0.02 + 0.2 * busy
            links = (M.WifiLink(busy=busy, coll=coll), M.WifiLink(busy=busy / 2, coll=coll / 2))
            p = replace(p, wifi=replace(p.wifi, links=links, mlo=mlo,
                                        ap_queue_p=min(0.1 + busy, 0.9)))
            R["wifi"].append(dict(busy=busy, mlo=mlo, **run(p, NS)[2]))

    # ---------------------------------------------------------------- 8 other
    R["frame_locked_render"] = run(nr_path(render_frame_locked=True), NS)[2]
    R["capability2"] = run(nr_path(n1_ms=4.5 / 28, n2_ms=5.5 / 28, gnb_ms=0.15), NS)[2]
    R["dynamic_grant_unloaded"] = run(nr_path(configured_grant=False), NS)[2]
    R["operator_edge_rtt2"] = run(nr_path(net_rtt_ms=2.0), NS)[2]

    # ---------------------------------------------------------------- 9 mitigations
    worst = dict(bler_ul=0.30, bler_dl=0.30, load=0.8, priority_qos=True,
                 ho_rate_hz=0.1, ho_int_ms=(30.0, 60.0), ho_rlf_p=0.01, net_rtt_ms=2.0)
    ladder = [
        ("worst case outdoors", {}),
        ("+ robust MCS: BLER 1 %", dict(bler_ul=0.01, bler_dl=0.01)),
        ("+ mini-slot PUSCH / PDSCH", dict(ul_minislot=2, dl_minislot=7)),
        ("+ DAPS or LTM handover", dict(ho_int_ms=(0.0, 1.0), ho_rlf_p=0.002, mig_rtt_ms=0.0)),
        ("+ capability-2 timing", dict(n1_ms=4.5 / 28, n2_ms=5.5 / 28, gnb_ms=0.15)),
        ("+ tile-local scan restart", dict(scan_tile_restart=True)),
    ]
    kw = dict(worst)
    R["mitigation"] = []
    xs_mit = {}
    for name, d in ladder:
        kw.update(d)
        x, _, s = run(nr_path(**kw), N, seed=11)
        xs_mit[name] = x
        R["mitigation"].append(dict(step=name, **s))
    # the same ladder without the network faults: pure baseline gains
    kw = {}
    R["mitigation_baseline"] = []
    for name, d in ladder[1:]:
        kw.update(d)
        R["mitigation_baseline"].append(dict(step=name, **run(nr_path(**kw), NS, seed=12)[2]))
    # Wi-Fi room with tile-local scan restart
    p = P["wifi_room"]
    R["wifi_room_tile_restart"] = run(replace(p, scan=replace(p.scan, tile_restart=True)), NS)[2]
    xpt = M.predicted_action(np.random.default_rng(8), NS,
                             replace(p, scan=replace(p.scan, tile_restart=True)))
    R["predicted_tile_restart"] = M.stats(xpt)

    R["runtime_s"] = time.time() - t_start
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(R, f, indent=1)

    plots(R, xs, xs_mit)
    summary(R)


# ============================================================================ plots

def plots(R, xs, xs_mit):
    names = {"wifi_room": "Wi-Fi, room validator", "wifi_city": "Wi-Fi, city validator",
             "nr_cell": "5G SA, cell-site validator", "far": "Far validator",
             "predicted": "Predicted action (U1)"}
    order = ["predicted", "wifi_room", "wifi_city", "nr_cell", "far"]

    # 1 CCDF of the paths
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for i, k in enumerate(order):
        x = np.sort(xs[k])
        n = x.size
        idx = np.unique(np.r_[np.linspace(0, n - 1, 3000).astype(int), np.arange(n - 2000, n)])
        ax.semilogy(x[idx], 1 - (idx + 0.5) / n, color=C[i], label=names[k])
    gate_line(ax, horizontal=False)
    for q, lab in [(1e-2, "p99"), (1e-3, "p99.9")]:
        ax.axhline(q, color=GRID, lw=1)
        ax.text(60, q * 1.15, lab, color=INK2, ha="center", fontsize=8)
    ax.text(GATE + 1, 0.3, "DST-11: 30 ms", color=INK2, fontsize=8)
    ax.set_xlim(0, 120)
    ax.set_ylim(1e-6, 1.2)
    ax.set_xlabel("input to photon (ms)")
    ax.set_ylabel("fraction of actions slower than x")
    ax.set_title("Input-to-photon latency, four paths and the predicted action (2 M samples each)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.55, 0.02))
    fig.savefig(os.path.join(PLOTS, "01_ccdf_paths.png"))
    plt.close(fig)

    # 2 stage means: model vs Part 21
    labels = ["touch", "air up", "network", "render", "encode", "air down", "decode", "scan-out"]
    keys = ["wifi_room", "wifi_city", "nr_cell"]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    y = []
    ticks = []
    for i, k in enumerate(keys):
        for j, src in enumerate(["Part 21", "model"]):
            vals = M.PART21[k]["stages"] if src == "Part 21" else [R["paths"][k]["stages_mean"][g] for g in M.STAGES]
            left = 0
            yy = i * 2.6 + j
            for s, v in enumerate(vals):
                ax.barh(yy, v, left=left, color=plt.cm.tab10.colors[s] if False else
                        ["#2a78d6", "#7fb0ea", "#a7a69d", "#eb6834", "#f3a37f", "#1baf7a", "#8fd7bd", "#eda100"][s],
                        edgecolor="white", linewidth=1.5, height=0.8, label=labels[s] if (i == 0 and j == 0) else None)
                left += v
            ax.text(left + 0.2, yy, f"{left:.1f} ms", va="center", color=INK, fontsize=8)
            ticks.append((yy, f"{names[k]}\n{src}"))
    ax.set_yticks([t[0] for t in ticks])
    ax.set_yticklabels([t[1] for t in ticks], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("mean (ms)")
    ax.set_xlim(0, 21)
    ax.set_title("Stage means: the Part 21 table against the model")
    ax.legend(ncol=4, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.42))
    ax.grid(axis="y", visible=False)
    fig.savefig(os.path.join(PLOTS, "02_stage_means.png"))
    plt.close(fig)

    # 3 BLER
    fig, ax = plt.subplots(figsize=(7, 4))
    b = [r["bler"] * 100 for r in R["bler"]]
    for i, (q, lab) in enumerate([("p50", "p50"), ("p99", "p99"), ("p999", "p99.9")]):
        ax.plot(b, [r[q] for r in R["bler"]], color=C[i], marker="o", ms=4, label=f"{lab}, UL and DL")
    ax.plot(b, [r["p99"] for r in R["bler_dl_only"]], color=C[3], ls=":", marker="o", ms=4,
            label="p99, DL only (UL at 1 %)")
    gate_line(ax)
    ax.set_xlabel("first-transmission BLER (%)")
    ax.set_ylabel("input to photon (ms)")
    ax.set_title("5G cell-site path: sensitivity to HARQ BLER (DDDSU, 30 kHz)")
    ax.legend(fontsize=8)
    fig.savefig(os.path.join(PLOTS, "03_sens_bler.png"))
    plt.close(fig)

    # 4 TDD
    fig, ax = plt.subplots(figsize=(8, 4.2))
    pats = [r["pattern"] for r in R["tdd"]]
    yv = np.arange(len(pats))
    ax.barh(yv - 0.2, [r["p99"] for r in R["tdd"]], height=0.38, color=C[0], label="p99, BLER 10 %")
    ax.barh(yv + 0.2, [r["p99"] for r in R["tdd_bler20"]], height=0.38, color=C[1], label="p99, BLER 20 %")
    ax.scatter([r["mean"] for r in R["tdd"]], yv - 0.2, color=INK, s=12, zorder=3, label="mean, BLER 10 %")
    gate_line(ax, horizontal=False)
    ax.set_yticks(yv)
    ax.set_yticklabels(pats, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("input to photon (ms)")
    ax.set_title("5G cell-site path: sensitivity to the TDD pattern (slot 0.5 ms)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", visible=False)
    fig.savefig(os.path.join(PLOTS, "04_sens_tdd.png"))
    plt.close(fig)

    # 5 load
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, (k, lab) in enumerate([("priority", "CG + delay-critical QoS flow"),
                                  ("best_effort", "CG, best-effort scheduling"),
                                  ("public", "public cell: no CG, no QoS, central UPF")]):
        L = [r["load"] * 100 for r in R["load"][k]]
        ax.plot(L, [r["p99"] for r in R["load"][k]], color=C[i], marker="o", ms=4, label=lab + ", p99")
        ax.plot(L, [r["mean"] for r in R["load"][k]], color=C[i], ls=":", lw=1.5)
    gate_line(ax)
    ax.set_xlabel("cell load (%)")
    ax.set_ylabel("input to photon (ms)")
    ax.set_title("5G: sensitivity to cell load (dotted: mean)")
    ax.set_yscale("log")
    ax.set_yticks([15, 20, 30, 50, 100, 200])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.legend(fontsize=8)
    fig.savefig(os.path.join(PLOTS, "05_sens_load.png"))
    plt.close(fig)

    # 6 handover
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for i, (name, rows) in enumerate(R["handover"].items()):
        r = [x["rate_hz"] for x in rows]
        rx = [1 / v if v > 0 else np.nan for v in r]
        axs[0].plot(r, [x["p99"] for x in rows], color=C[i], marker="o", ms=4, label=name)
        axs[1].plot(r, [x["p999"] for x in rows], color=C[i], marker="o", ms=4, label=name)
    for axx, t in zip(axs, ["p99", "p99.9"]):
        gate_line(axx)
        axx.set_xlabel("handovers per second")
        axx.set_ylabel(f"{t} input to photon (ms)")
        axx.set_title(f"5G handover: {t}")
        axx.set_yscale("log")
        axx.set_yticks([20, 30, 50, 100])
        axx.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axs[0].legend(fontsize=8)
    fig.savefig(os.path.join(PLOTS, "06_sens_handover.png"))
    plt.close(fig)

    # 7 gate map
    g = R["gate_map"]
    H = np.array(g["p99"])
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    im = ax.imshow(H, origin="lower", aspect="auto", cmap="Blues",
                   extent=[-0.5, len(g["rtt_ms"]) - 0.5, -0.5, len(g["bler"]) - 0.5])
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            ax.text(j, i, f"{H[i, j]:.0f}", ha="center", va="center", fontsize=7,
                    color="white" if H[i, j] > 0.6 * H.max() + 0.4 * H.min() else INK,
                    fontweight="bold" if H[i, j] > GATE else "normal")
    ax.contour(np.arange(H.shape[1]), np.arange(H.shape[0]), H, levels=[GATE], colors=[C[1]], linewidths=2)
    ax.set_xticks(range(len(g["rtt_ms"])))
    ax.set_xticklabels(g["rtt_ms"])
    ax.set_yticks(range(len(g["bler"])))
    ax.set_yticklabels([f"{b*100:.0f}" for b in g["bler"]])
    ax.set_xlabel("network RTT, gNB to validator and back (ms)")
    ax.set_ylabel("BLER, UL and DL (%)")
    ax.set_title("5G p99 (ms). Orange line: the DST-11 gate at 30 ms")
    ax.grid(False)
    fig.colorbar(im, ax=ax, label="p99 (ms)")
    fig.savefig(os.path.join(PLOTS, "07_gate_map.png"))
    plt.close(fig)

    # 8 mitigation ladder
    fig, ax = plt.subplots(figsize=(8, 4.2))
    st = [r["step"] for r in R["mitigation"]]
    yv = np.arange(len(st))
    ax.barh(yv - 0.2, [r["p99"] for r in R["mitigation"]], height=0.38, color=C[0], label="p99")
    ax.barh(yv + 0.2, [min(r["p999"], 150) for r in R["mitigation"]], height=0.38, color=C[1], label="p99.9")
    for i, r in enumerate(R["mitigation"]):
        ax.text(r["p99"] + 1, i - 0.2, f"{r['p99']:.1f}", va="center", fontsize=8, color=INK)
        ax.text(min(r["p999"], 150) + 1, i + 0.2, f"{r['p999']:.1f}", va="center", fontsize=8, color=INK)
    gate_line(ax, horizontal=False)
    ax.set_yticks(yv)
    ax.set_yticklabels(st, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("input to photon (ms)")
    ax.set_title("5G outdoors: worst case and the mitigations, applied in order")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", visible=False)
    fig.savefig(os.path.join(PLOTS, "08_mitigations.png"))
    plt.close(fig)

    # 9 Wi-Fi contention
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, mlo in enumerate([True, False]):
        rows = [r for r in R["wifi"] if r["mlo"] == mlo]
        lab = "MLO, 5 + 6 GHz" if mlo else "single link, 5 GHz"
        ax.plot([r["busy"] * 100 for r in rows], [r["p99"] for r in rows], color=C[i], marker="o", ms=4, label=lab + ", p99")
        ax.plot([r["busy"] * 100 for r in rows], [r["p999"] for r in rows], color=C[i], ls=":", lw=1.5, label=lab + ", p99.9")
    gate_line(ax)
    ax.set_xlabel("5 GHz channel occupancy (%)")
    ax.set_ylabel("input to photon (ms)")
    ax.set_title("Wi-Fi room path: sensitivity to contention")
    ax.legend(fontsize=8)
    fig.savefig(os.path.join(PLOTS, "09_sens_wifi.png"))
    plt.close(fig)


# ============================================================================ summary

def summary(R):
    L = []
    w = L.append
    w("PATHS (mean / p50 / p99 / p99.9 ms; Part 21 mean, p99)")
    for k, s in R["paths"].items():
        w(f"  {k:10s} {s['mean']:6.2f} {s['p50']:6.2f} {s['p99']:6.2f} {s['p999']:6.2f}"
          f"   | P21 {s['part21']['mean']}, {s['part21']['p99']}   sum of stage p99 = {s['sum_of_stage_p99']:.1f}")
        w("      stages: " + ", ".join(f"{g} {v:.2f}" for g, v in s["stages_mean"].items()))
    s = R["predicted"]
    w(f"  predicted  {s['mean']:6.2f} {s['p50']:6.2f} {s['p99']:6.2f} {s['p999']:6.2f}")
    s = R["predicted_tile_restart"]
    w(f"  predicted + tile restart {s['mean']:6.2f} p99 {s['p99']:6.2f}")
    w("BLER (UL=DL): " + ", ".join(f"{r['bler']:.2f}:{r['p99']:.1f}/{r['p999']:.1f}" for r in R["bler"]))
    w("BLER DL only: " + ", ".join(f"{r['bler']:.2f}:{r['p99']:.1f}" for r in R["bler_dl_only"]))
    w("TDD (BLER10): " + ", ".join(f"{r['pattern']}:{r['mean']:.1f}/{r['p99']:.1f}" for r in R["tdd"]))
    w("TDD (BLER20): " + ", ".join(f"{r['pattern']}:{r['p99']:.1f}" for r in R["tdd_bler20"]))
    for k, rows in R["load"].items():
        w(f"LOAD {k}: " + ", ".join(f"{r['load']:.2f}:{r['mean']:.1f}/{r['p99']:.1f}" for r in rows))
    for k, rows in R["handover"].items():
        w(f"HO {k}: " + ", ".join(f"{r['rate_hz']:.3f}:{r['p99']:.1f}/{r['p999']:.1f}/{r['frac_over_30']*100:.2f}%" for r in rows))
    g = R["gate_map"]
    w("GATE max RTT per BLER: " + ", ".join(f"{b:.2f}:{m:.1f}" for b, m in zip(g["bler"], g["max_rtt_ms"])))
    w("WIFI: " + ", ".join(f"{r['busy']:.1f}{'M' if r['mlo'] else 'S'}:{r['p99']:.1f}/{r['p999']:.1f}" for r in R["wifi"]))
    for k in ["frame_locked_render", "capability2", "dynamic_grant_unloaded", "operator_edge_rtt2", "wifi_room_tile_restart"]:
        s = R[k]
        w(f"{k}: mean {s['mean']:.2f} p99 {s['p99']:.2f} p99.9 {s['p999']:.2f}")
    w("MITIGATION ladder (worst case):")
    for r in R["mitigation"]:
        w(f"  {r['step']:32s} mean {r['mean']:6.2f} p99 {r['p99']:6.2f} p99.9 {r['p999']:7.2f} >30ms {r['frac_over_30']*100:.3f}%")
    w("MITIGATION ladder (baseline cell):")
    for r in R["mitigation_baseline"]:
        w(f"  {r['step']:32s} mean {r['mean']:6.2f} p99 {r['p99']:6.2f} p99.9 {r['p999']:7.2f}")
    w(f"runtime {R['runtime_s']:.0f} s")
    txt = "\n".join(L)
    open(os.path.join(OUT, "summary.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
