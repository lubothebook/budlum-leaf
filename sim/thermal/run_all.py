#!/usr/bin/env python3
"""run_all.py  --  run every Thermal case of the Leaf L.6.0 and write
results.json plus the PNG plots in ./plots.

    python3 run_all.py          # about 1 to 3 minutes
"""
import json
import os
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import leaf_thermal as LT
from leaf_thermal import (Config, Network, NX, NY, NT, session_q, session_total,
                          charge_q, charge_losses, sustained_charge,
                          sustained_session, simulate_charge, derate, coil_map)

HERE = os.path.dirname(os.path.abspath(__file__))
PLOTS = os.path.join(HERE, "plots")
os.makedirs(PLOTS, exist_ok=True)

# validated default palette (dataviz skill, references/palette.md)
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
CRIT = "#d03b3b"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SEQ = LinearSegmentedColormap.from_list(
    "blue_seq", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 2.0, "font.size": 9, "legend.frameon": False,
})

# --------------------------------------------------------------------------
# configurations
# --------------------------------------------------------------------------
BASE = Config(name="baseline")
FIX = BASE.copy(
    name="fixed",
    hinge_kind="graphite", hinge_leaves=3, landing=1.5e-3,   # F1 graphite hinge
    spreader_kt=0.14,                                         # F2 0.20 mm graphite S layer
    ring_pad_full=True, h_ring_pad=3000.0,                    # F3 full-disc ring pad
    G_ring_bar=0.08, h_bar=3000.0,                            # F4 ring-bar strap, edge gel
)
OUTDOOR = dict(h_front=12.0, h_back=12.0, h_ring=12.0)
PAD_FAN = dict(pad="leafpad", T_pad=26.0)       # fan-cooled Leaf pad, ambient + 1 K
PAD_TEC = dict(pad="leafpad", T_pad=22.0)       # regulated Leaf pad, 22 C
PUCK = dict(pad="puck", T_pad=30.0)             # a passive Qi2.2 MPP puck

R = {"generated": time.strftime("%Y-%m-%d %H:%M"), "limits": dict(
    skin=BASE.T_skin_lim, cell_charge=BASE.T_cell_chg_lim, cell_discharge=BASE.T_cell_dis_lim)}


def rd(d, n=2):
    return {k: (round(float(v), n) if isinstance(v, (int, float, np.floating)) else v)
            for k, v in d.items()}


# --------------------------------------------------------------------------
# 1. power maps
# --------------------------------------------------------------------------
def tile_power(net, q):
    m = np.zeros(NT)
    for t in range(NT):
        for L in LT.LAYERS:
            m[t] += q[net.nid(t, L)]
    ring = sum(q[net.rid(x)] for x in Network.RING)
    return m.reshape(NY, NX), ring


def plot_power_maps():
    cases = []
    n = Network(BASE)
    cases.append(("(a) video session, 2.50 W", *tile_power(n, session_q(n, "video"))))
    q, L = charge_q(n, 25.0)
    cases.append(("(b) Qi2.2 charge, 25 W received", *tile_power(n, q)))
    no = Network(BASE.copy(**OUTDOOR))
    cases.append(("(c) 5G outdoor session, 4.18 W", *tile_power(no, session_q(no, "5g_outdoor"))))
    fig, axs = plt.subplots(1, 3, figsize=(10, 5.6))
    vmax = max(c[1].max() for c in cases) * 1000
    for ax, (title, m, ring) in zip(axs, cases):
        im = ax.imshow(m * 1000, cmap=SEQ, vmin=0, vmax=vmax, extent=(0, 80, 160, 0))
        ax.add_patch(plt.Circle((40, 18), 16, fill=False, ec=CRIT, lw=1.5))
        ax.text(40, 18, f"B ring\n{ring:.2f} W", ha="center", va="center", color=INK, fontsize=8)
        ax.set_title(title, fontsize=9, color=INK)
        ax.set_xlabel("x, mm")
        ax.grid(False)
    axs[0].set_ylabel("y from the top edge, mm")
    cb = fig.colorbar(im, ax=axs, shrink=0.8)
    cb.set_label("heat per tile, mW (ring shown as a number)")
    fig.suptitle("Power maps of the three cases, baseline electrics", color=INK)
    fig.savefig(os.path.join(PLOTS, "01_power_maps.png"), dpi=130)
    plt.close(fig)
    R["loss_budget_25W"] = rd(L, 3)
    R["loss_budget_25W_quadrant_charger"] = rd(charge_losses(BASE.copy(charger_site="quadrant"), 25.0), 3)


# --------------------------------------------------------------------------
# 2. steady states of the sessions, baseline and fixed
# --------------------------------------------------------------------------
def steady_sessions():
    out = {}
    fields = {}
    for amb in (25.0, 35.0):
        for cfgname, cfg in (("baseline", BASE), ("fixed", FIX)):
            for sess, extra in (("video", {}), ("5g_outdoor", OUTDOOR)):
                for sun in ((0.0, 600.0) if sess == "5g_outdoor" else (0.0,)):
                    c = cfg.copy(T_amb=amb, solar=sun, **extra)
                    n = Network(c)
                    T = n.steady(session_q(n, sess))
                    r = n.readout(T)
                    key = f"{sess}{'_sun' if sun else ''}|{cfgname}|{amb:.0f}C"
                    r["P_total_W"] = session_total(sess)
                    r["skin_pass"] = r["T_surface_max"] <= c.T_skin_lim
                    r["cell_pass"] = r["T_cell_max"] <= c.T_cell_dis_lim
                    r["sustained_scale"] = sustained_session(c, sess)
                    r["sustained_W"] = r["sustained_scale"] * session_total(sess)
                    out[key] = rd(r)
                    if amb == 25.0 and not sun:
                        fields[(sess, cfgname)] = (n.field(T, "FS"), r)
    # video at 2.0 and 3.0 W, and the sensitivities
    for cfgname, cfg in (("baseline", BASE), ("fixed", FIX)):
        for P in (2.0, 2.5, 3.0):
            n = Network(cfg)
            r = n.readout(n.steady(session_q(n, "video", P / session_total("video"))))
            out[f"video_{P:.1f}W|{cfgname}|25C"] = rd(r)
    sens = {}
    for name, c in (("fixed + kerf air at rest", FIX.copy(kerf_air=True)),
                    ("fixed + palm at 34 C on the back", FIX.copy(hand=True)),
                    ("fixed, one graphite leaf", FIX.copy(hinge_leaves=1, landing=0.7e-3)),
                    ("ideal body, link 1 W/K", None)):
        if c is None:
            orig = LT.hinge_G
            LT.hinge_G = lambda k: 1.0
            c = FIX.copy(spreader_kt=100.0, coil_kt=100.0)
            s = sustained_session(c, "video")
            LT.hinge_G = orig
        else:
            s = sustained_session(c, "video")
        sens[name] = round(s * session_total("video"), 3)
    out["video_sustained_sensitivity_W"] = sens
    R["sessions"] = out
    # plot temperature fields
    fig, axs = plt.subplots(1, 4, figsize=(12, 5.6))
    keys = [("video", "baseline"), ("video", "fixed"), ("5g_outdoor", "baseline"), ("5g_outdoor", "fixed")]
    vmin, vmax = 25, max(fields[k][0].max() for k in keys)
    for ax, k in zip(axs, keys):
        f, r = fields[k]
        im = ax.imshow(f, cmap=SEQ, vmin=vmin, vmax=vmax, extent=(0, 80, 160, 0))
        ax.contour(np.linspace(5, 75, NX), np.linspace(5, 155, NY), f, levels=[36.2],
                   colors=[CRIT], linewidths=1.5)
        ax.add_patch(plt.Circle((40, 18), 16, fill=False, ec=INK, lw=1.0, ls="--"))
        ax.set_title(f"{k[0]}, {k[1]}\nring shell {r['T_ring_shell']:.1f} C, "
                     f"cells {r['T_cell_min']:.1f}-{r['T_cell_max']:.1f} C", fontsize=8)
        ax.grid(False)
    cb = fig.colorbar(im, ax=axs, shrink=0.8)
    cb.set_label("front cap surface, C (red line = 36.2 C)")
    fig.suptitle("Steady state at 25 C ambient, free air (5G: 12 W/m2K wind, shade)", color=INK)
    fig.savefig(os.path.join(PLOTS, "02_session_fields.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# 3. charging: steady T vs P, sustained rate, transient to 80 %
# --------------------------------------------------------------------------
CHG = [
    ("baseline, Qi2.2 puck", BASE.copy(**PUCK), S2),
    ("fixed, Qi2.2 puck", FIX.copy(**PUCK), S4),
    ("fixed, Leaf pad fan (26 C)", FIX.copy(**PAD_FAN), S1),
    ("fixed, Leaf pad regulated (22 C)", FIX.copy(**PAD_TEC), S3),
]


def charging():
    out = {}
    Ps = np.linspace(0, 30, 16)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, c, col in CHG:
        n = Network(c)
        tmax = []
        for P in Ps:
            r = n.readout(n.steady(charge_q(n, P)[0]))
            tmax.append(max(r["T_surface_max"], r["T_ntc_max"]))
        ax.plot(Ps, tmax, color=col, label=name)
        Psus, rs = sustained_charge(c)
        r25 = n.readout(n.steady(charge_q(n, 25.0)[0]))
        out[name] = dict(sustained_P_rx_W=round(Psus, 2),
                         sustained_C_rate=round(charge_losses(c, Psus)["_C_rate"], 2),
                         at_25W=rd(r25), at_sustained=rd(rs))
    ax.axhline(36.2, color=CRIT, lw=1.2)
    ax.text(0.5, 37.2, "36.2 C cut-off", color=INK2)
    ax.axvline(25, color=INK2, lw=0.8, ls=":")
    ax.set_ylim(20, 80)
    ax.set_xlabel("Qi2.2 received power P_rx, W")
    ax.set_ylabel("hottest surface or NTC, steady, C")
    ax.set_title("Steady charge temperature at 25 C ambient", color=INK)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "03_charge_steady.png"), dpi=130)
    plt.close(fig)

    # transients
    fig, axs = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
    for name, c, col in CHG:
        net, rec = simulate_charge(c, soc0=0.0, soc_end=0.80, t_max=5 * 3600)
        t = np.array([x[0] for x in rec]) / 60
        P = [x[2]["P_rx"] for x in rec]
        soc = [x[2]["soc"] * 100 for x in rec]
        hot = [max(x[2]["T_surface_max"], x[2]["T_ntc_max"]) for x in rec]
        axs[0].plot(t, P, color=col, label=name)
        axs[1].plot(t, hot, color=col)
        axs[2].plot(t, soc, color=col)
        reached = rec[-1][2]["soc"] >= 0.799
        out[name]["t80_min"] = round(t[-1], 1) if reached else None
        out[name]["soc_at_end"] = round(rec[-1][2]["soc"], 3)
        out[name]["T_cell_max_run"] = round(max(x[2]["T_cell_max"] for x in rec), 2)
        out[name]["T_cell_min_run"] = round(min(x[2]["T_cell_min"] for x in rec[3:]), 2)
        out[name]["mean_P_rx_W"] = round(float(np.mean(P)), 2)
    axs[0].set_ylabel("P_rx, W")
    axs[0].legend(loc="upper right", fontsize=7)
    axs[1].axhline(36.2, color=CRIT, lw=1.2)
    axs[1].set_ylabel("hottest surface/NTC, C")
    axs[2].axhline(80, color=INK2, lw=0.8, ls=":")
    axs[2].set_ylabel("state of charge, %")
    axs[2].set_xlabel("time, min")
    axs[0].set_title("Charge from 0 to 80 % with the throttle law, 25 C ambient", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "04_charge_transient.png"), dpi=130)
    plt.close(fig)
    R["charging"] = out


# --------------------------------------------------------------------------
# 4. throttle law and video throttling
# --------------------------------------------------------------------------
def throttle():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    Th = np.linspace(30, 37, 300)
    axs[0].plot(Th, [derate(x, 36.2) * 100 for x in Th], color=S1)
    axs[0].axvline(36.2, color=CRIT, lw=1.2)
    axs[0].set_xlabel("hottest surface or NTC, C")
    axs[0].set_ylabel("allowed power, % of the class")
    axs[0].set_title("Throttle law: full to 34.2 C, 20 % at 36.0 C, off at 36.2 C", fontsize=9)
    out = {}
    for name, c, col in (("baseline", BASE, S2), ("fixed", FIX, S1),
                         ("fixed + 3 g PCM at 33 C", FIX.copy(pcm_g=3.0), S3)):
        net = Network(c)
        st = {}

        def qf(t, T, net=net):
            r = net.readout(T)
            f = derate(r["T_surface_max"], 36.2)
            # the display and the stream degrade together: 30 % is the floor
            s = max(0.3, f)
            return session_q(net, "video", s), dict(scale=s, **r)

        rec = net.transient(qf, 3600, dt=2.0, record_every=15)
        t = np.array([x[0] for x in rec]) / 60
        P = np.array([x[2]["scale"] for x in rec]) * session_total("video")
        axs[1].plot(t, P, color=col, label=name)
        # time to the first derate step
        first = next((x[0] for x in rec if x[2]["scale"] < 1.0), None)
        out[name] = dict(full_power_min=None if first is None else round(first / 60, 1),
                         P_after_60min_W=round(float(P[-1]), 2))
    axs[1].set_xlabel("time, min")
    axs[1].set_ylabel("video session power, W")
    axs[1].set_title("Video at 2.50 W from a 25 C start, throttled", fontsize=9)
    axs[1].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "05_throttle.png"), dpi=130)
    plt.close(fig)
    R["video_throttle"] = out


# --------------------------------------------------------------------------
# 5. ambient sweep
# --------------------------------------------------------------------------
def ambient_sweep():
    ambs = np.arange(15, 36, 2.5)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    out = {"T_amb": ambs.tolist()}
    for name, cfg, col in (("video, baseline", BASE, S2), ("video, fixed", FIX, S1)):
        v = [sustained_session(cfg.copy(T_amb=a), "video") * session_total("video") for a in ambs]
        axs[0].plot(ambs, v, color=col, label=name, marker="o", ms=4)
        out[name] = [round(x, 3) for x in v]
    axs[0].set_xlabel("ambient, C")
    axs[0].set_ylabel("sustained session power, W")
    axs[0].set_title("Sustained video power under 36.2 C, free air", fontsize=9)
    axs[0].legend()
    for name, mk, col in (("charge, fixed, pad fan (amb + 1 K)", lambda a: FIX.copy(T_amb=a, pad="leafpad", T_pad=a + 1), S1),
                          ("charge, fixed, pad regulated 22 C", lambda a: FIX.copy(T_amb=a, **PAD_TEC), S3),
                          ("charge, fixed, Qi2.2 puck (amb + 5 K)", lambda a: FIX.copy(T_amb=a, pad="puck", T_pad=a + 5), S4)):
        v = [min(25.0, sustained_charge(mk(a))[0]) for a in ambs]
        axs[1].plot(ambs, v, color=col, label=name, marker="o", ms=4)
        out[name] = [round(x, 2) for x in v]
    axs[1].set_xlabel("ambient, C")
    axs[1].set_ylabel("sustained P_rx, W (capped at 25)")
    axs[1].set_title("Sustained Qi2.2 charge under 36.2 C", fontsize=9)
    axs[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "06_ambient_sweep.png"), dpi=130)
    plt.close(fig)
    R["ambient_sweep"] = out


# --------------------------------------------------------------------------
# 6. loss budget bar
# --------------------------------------------------------------------------
def loss_bar():
    L = charge_losses(BASE, 25.0)
    keys = ["coil", "shield_eddy", "ac_lead", "rectifier", "charger", "dc_lattice", "leaves", "cells_I2R"]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(keys[::-1], [L[k] for k in keys[::-1]], color=S1, height=0.6)
    for i, k in enumerate(keys[::-1]):
        ax.text(L[k] + 0.03, i, f"{L[k]:.2f} W", va="center", color=INK, fontsize=8)
    tot = sum(L[k] for k in keys)
    ax.set_title(f"Device heat at 25 W received: {tot:.2f} W "
                 f"(ring {L['rectifier'] + L['charger']:.2f} W)", color=INK, fontsize=9)
    ax.set_xlabel("W")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "07_loss_budget.png"), dpi=130)
    plt.close(fig)
    R["device_heat_25W_total"] = round(tot, 3)


if __name__ == "__main__":
    t0 = time.time()
    n = Network(BASE)
    nf = Network(FIX)
    R["network"] = dict(nodes=n.n, hinge_G_baseline_W_per_K=LT.hinge_G("copper"),
                        link_G_baseline=float(np.mean(n.g_link)),
                        link_G_fixed=float(np.mean(nf.g_link)),
                        skin_G_W_per_K=n.g_skin, R_lead_ohm=LT.R_lead(BASE),
                        coil_tiles=int((coil_map() > 0).sum()))
    for f in (plot_power_maps, steady_sessions, charging, throttle, ambient_sweep, loss_bar):
        print("running", f.__name__, flush=True)
        f()
    R["runtime_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(R, fh, indent=1, default=float)
    print(json.dumps(R, indent=1, default=float))
