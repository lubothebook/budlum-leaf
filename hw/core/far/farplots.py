#!/usr/bin/env python3
"""farplots.py - the plots of the far link seat. Run after farlink.py and farlatency.py.

Palette: the validated categorical default of the dataviz skill (blue, orange, aqua, yellow, violet).
The aqua and yellow are under 3:1 on the surface, so every series also has its own marker and the
legend is always present. The numbers of every plot are in out/*.json and out/*.txt.
Out: out/plots/01_rate_vs_distance.png ... 05_aperture.png
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import farlink as F  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PLOTS = os.path.join(OUT, "plots")
os.makedirs(PLOTS, exist_ok=True)

SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
COL = {"wifi24": "#2a78d6", "wifi5": "#eb6834", "wifi6": "#1baf7a", "nr35": "#eda100", "nr07": "#6250d6"}
MARK = {"wifi24": "o", "wifi5": "s", "wifi6": "^", "nr35": "D", "nr07": "v"}
NAME = {"wifi24": "Wi-Fi 2.4 GHz", "wifi5": "Wi-Fi 5 GHz", "wifi6": "Wi-Fi 6 GHz", "nr35": "5G 3.5 GHz", "nr07": "5G 700 MHz"}
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "axes.spines.top": False, "axes.spines.right": False, "grid.color": GRID,
                     "grid.linewidth": 0.6, "legend.frameon": False})


def dgrid(n=120):
    return [10 ** (math.log10(30) + (math.log10(12000) - math.log10(30)) * i / (n - 1)) for i in range(n)]


def fig1():
    fig, axs = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
    for j, scen in enumerate(["UMa-LOS", "UMa-NLOS"]):
        for i, (key, title) in enumerate((("dl_bps", "downlink per Leaf"), ("ul_bps", "uplink per Leaf"))):
            ax = axs[i][j]
            for tech in ["wifi24", "wifi5", "wifi6", "nr35", "nr07"]:
                ds = dgrid()
                ys = [max(F.link(tech, scen, d, 18, "TR")[key] / 1e6, 1e-3) for d in ds]
                ax.plot(ds, ys, color=COL[tech], lw=1.8, label=NAME[tech], marker=MARK[tech], markevery=15, ms=5)
            if i == 0:
                ax.axhline(150.2, color=INK2, lw=1, ls="--")
                ax.axhline(25, color=INK2, lw=1, ls=":")
                ax.text(32, 165, "slice 150 Mbit/s", color=INK2, fontsize=8)
                ax.text(32, 27.5, "slice 25 Mbit/s", color=INK2, fontsize=8)
            else:
                ax.axhline(F.UL_CORE_BPS / 1e6, color=INK2, lw=1, ls="--")
                ax.text(32, F.UL_CORE_BPS / 1e6 * 1.12, "touch, IMU, voice, signed batch 2 Mbit/s", color=INK2, fontsize=8)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_ylim(1e-1, 2e3)
            ax.grid(True, which="major")
            ax.set_title("%s, %s, Core 18 dBi" % (title, scen), loc="left", fontsize=10)
            if i == 1:
                ax.set_xlabel("distance, m")
            if j == 0:
                ax.set_ylabel("Mbit/s")
            for d in (100, 300, 1000, 3000, 10000):
                ax.axvline(d, color=GRID, lw=0.5, zorder=0)
    axs[0][0].legend(loc="lower left", ncol=1, fontsize=8)
    fig.suptitle("Rate per Leaf against distance (BTK rules, Leaf as designed, 90 % shadow margin)", x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "01_rate_vs_distance.png"), dpi=130)
    plt.close(fig)


def fig2():
    fig, axs = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    reqs = [("DL 25 Mbit/s", "#2a78d6"), ("DL 150 Mbit/s", "#eb6834"), ("UL 2 Mbit/s", "#1baf7a")]
    gs = [4 + 0.5 * i for i in range(0, 43)]
    for ax, tech in zip(axs, ["nr35", "nr07", "wifi5"]):
        for scen, ls in (("UMa-NLOS", "-"), ("UMa-LOS", "--")):
            for (nm, col), kind in zip(reqs, ("dl25", "dl150", "ul")):
                ys = []
                for g in gs:
                    if kind == "ul":
                        f = lambda d, g=g: F.link(tech, scen, d, g, "TR")["ul_bps"]
                        r = F.reach(f, F.UL_CORE_BPS)
                    else:
                        f = lambda d, g=g: F.link(tech, scen, d, g, "TR")["dl_bps"]
                        r = F.reach(f, F.SLICE_LO_BPS if kind == "dl25" else F.SLICE_HI_BPS)
                    ys.append(max(r, 20.0) / 1000.0)
                ax.plot(gs, ys, color=col, ls=ls, lw=1.8, label="%s, %s" % (nm, scen) if tech == "nr35" else None)
        for g in F.CORE_G:
            ax.axvline(g, color=GRID, lw=0.6, zorder=0)
        ax.set_yscale("log")
        ax.set_ylim(0.02, 70)
        ax.set_xlabel("Core antenna gain, dBi")
        ax.set_title(NAME[tech], loc="left", fontsize=10)
        ax.grid(True, which="major", axis="y")
    axs[0].set_ylabel("range, km (drawn from 20 m up)")
    axs[0].legend(fontsize=7, loc="lower right")
    fig.suptitle("What a bigger Core antenna buys: range for the slice stream (solid urban NLOS, dashed LOS)", x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "02_range_vs_core_gain.png"), dpi=130)
    plt.close(fig)


def fig3():
    arch = json.load(open(os.path.join(OUT, "arch.json")))["reach_m"]
    names = ["raw pixel stream", "compressed pixel stream 3:1", "compressed pixel stream 6:1",
             "slice stream, upper (full screen, 2 speculative frames)", "slice stream, lower (video class)"]
    short = ["raw 36.9 Gbit/s", "compressed 3:1, 12.3 Gbit/s", "compressed 6:1, 6.1 Gbit/s", "slice 150 Mbit/s", "slice 25 Mbit/s"]
    scens = [("FS", "#1baf7a"), ("UMa-LOS", "#2a78d6"), ("UMa-NLOS", "#eb6834"), ("UMa-NLOS+O2I-low", "#6250d6")]
    fig, ax = plt.subplots(figsize=(9.5, 5))
    h = 0.17
    for k, (sc, col) in enumerate(scens):
        for i, nm in enumerate(names):
            r = arch[sc][nm]["range_m"]
            v = max(r, 3.0)
            y = i + (k - 1.5) * (h + 0.03)
            ax.barh(y, v, height=h, color=col, label=("free space, 60 GHz allowed" if sc == "FS" else sc) if i == 0 else None, edgecolor=SURF, linewidth=1)
            ax.text(v * 1.15, y, ("<3 m" if r < 3 else ("%.0f m" % r if r < 1000 else "%.1f km" % (r / 1000))), va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(short)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(2, 300000)
    ax.set_xlabel("distance where the architecture stops, m (best radio, Core 25 dBi, BTK rules)")
    ax.grid(True, axis="x")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=4, fontsize=8)
    ax.set_title("Where each architecture stops (FS is free space and the only line where 60 GHz works)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "03_architecture_reach.png"), dpi=130)
    plt.close(fig)


def fig4():
    lat = json.load(open(os.path.join(OUT, "latency.json")))
    key = [k for k in lat if k.startswith("input 200")][0]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    cols = {"Core at the radio": "#2a78d6", "metro, 20 km of fibre": "#eb6834", "regional, 100 km": "#1baf7a",
            "national, 500 km": "#6250d6"}
    mk = {"Core at the radio": "o", "metro, 20 km of fibre": "s", "regional, 100 km": "^", "national, 500 km": "D"}
    for ax, cfg in zip(axs, ["5G 3.5 GHz, LOS, Core 25 dBi", "5G 700 MHz, LOS, Core 25 dBi"]):
        for b, col in cols.items():
            ds = sorted(int(d) for d in lat[key][cfg][b])
            ax.plot(ds, [lat[key][cfg][b][str(d)]["p99"] for d in ds], color=col, marker=mk[b], lw=1.8, label=b)
        ax.axhline(30, color=INK2, lw=1, ls="--")
        ax.text(3000, 30.6, "gate 30 ms", color=INK2, fontsize=8)
        ax.set_xscale("log")
        ax.set_ylim(15, 36)
        ax.set_xlabel("distance, m")
        ax.set_title(cfg, loc="left", fontsize=10)
        ax.grid(True, which="major")
    axs[0].set_ylabel("input to photon p99, ms")
    axs[0].legend(fontsize=8, loc="center left")
    fig.suptitle("Latency p99 against distance: air distance costs microseconds, the backhaul costs milliseconds", x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "04_latency_p99.png"), dpi=130)
    plt.close(fig)


def fig5():
    ant = json.load(open(os.path.join(OUT, "antenna.json")))["aperture"]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    cols = {"nr07": "#6250d6", "wifi24": "#2a78d6", "nr35": "#eda100", "wifi5": "#eb6834", "wifi6": "#1baf7a"}
    for tech in ["nr07", "wifi24", "nr35", "wifi5", "wifi6"]:
        gs = [int(g) for g in ant[tech]]
        ax.plot(gs, [ant[tech][str(g)]["side_m"] for g in gs], color=cols[tech], marker=MARK[tech], lw=1.8, label=NAME[tech])
    ax.set_yscale("log")
    ax.set_xticks(F.CORE_G)
    ax.set_xlabel("Core antenna gain, dBi")
    ax.set_ylabel("side of a square aperture, m")
    ax.grid(True, which="major")
    ax.legend(fontsize=8)
    ax.set_title("The Core antenna as an object (aperture efficiency 0.6)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "05_aperture.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("plots written to", PLOTS)
