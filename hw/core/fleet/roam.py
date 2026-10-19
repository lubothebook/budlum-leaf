#!/usr/bin/env python3
"""roam.py - the roaming fleet. Question 4 of the order of Ayaz.

A fleet of Leafs moves through a city of 20 x 20 km on a simple day: sleep, home, a walk, a vehicle,
a walk, the desk, lunch, the desk, a walk, a vehicle, a walk, home. Between them stand the Cores:
C2 site Cores on a hexagonal grid, C1 room Cores at some homes and desks, C0 docks at some beds and
desks. The simulation (10 s steps, 24 h) counts

  * the share of the day on C0, C1 and C2, and the share of the sessions on each;
  * the hand-over rate between C2 sites, and the class changes (compute host changes);
  * the energy host changes (a dock, a desk, a cradle, the cell);
  * the energy drawn from the Leaf cell, and the time above the free-air heat limit;
  * the C2 sessions per site by the hour, against the capacity of fleet.py;
  * the share of C2 session time where the link does not close.

The Leaf is the ruled B module of fleet.py: wallet signer in the Core, ACK 1.5 %.
All assumptions are in PARAMS and in DAY. Every one is a [HYPOTHESIS].

Run:   python3 roam.py        (about 40 s)    Out: out/roam.txt, out/roam.json
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fleet as F  # noqa: E402
import twohosts as T  # noqa: E402

OUT = F.OUT
CITY_KM = 20.0
DT = 10.0
STEPS = int(24 * 3600 / DT)
ACTS = ("idle", "delta", "video")

PARAMS = dict(
    n_leafs=1500, site_r_km=1.0,                     # sector radius; paths are straight lines, real paths add about 30 % of crossings
    v_walk=1.4, v_veh=10.0,                          # m/s, the vehicle speed is the mean including stops
    p_dock_home=0.5, p_dock_office=0.5, p_room_home=0.6, p_room_office=0.6, p_public_c1=0.10,
    dock_share_desk=0.6, dock_share_home=0.25,       # of the time at the desk or at home that the Leaf sits on its dock
    p_host_desk=0.8, p_cradle=0.5, p_pad_home=0.3, p_bank_walk=0.10, p_host_sleep=0.95,
    hyst_frac=0.05, free_air_w=1.73, plate_w=5.7,
)
# activity mix by segment type: idle, delta, video. [HYPOTHESIS]
MIXSEG = {
    "sleep": (1.00, 0.00, 0.00), "home": (0.60, 0.28, 0.12), "desk": (0.45, 0.52, 0.03),
    "walk": (0.80, 0.18, 0.02), "vehicle": (0.60, 0.28, 0.12), "cafe": (0.50, 0.35, 0.15),
}
SEGS = ["sleep", "home", "walk", "vehicle", "walk", "desk", "cafe", "desk", "walk", "vehicle", "walk", "home", "sleep"]


# --------------------------------------------------------------------------- the grid
def nearest_site(xy, isd):
    """The nearest site of a hexagonal lattice with inter-site distance isd. xy in metres, shape (N, 2)."""
    h = isd * math.sqrt(3) / 2
    j = xy[:, 1] / h
    i = xy[:, 0] / isd - j / 2
    best = None
    for di in (0, 1):
        for dj in (0, 1):
            ii, jj = np.floor(i) + di, np.floor(j) + dj
            sx = isd * (ii + jj / 2)
            sy = h * jj
            d = np.hypot(xy[:, 0] - sx, xy[:, 1] - sy)
            if best is None:
                best = [d, ii, jj, sx, sy]
            else:
                m = d < best[0]
                for k, v in enumerate((d, ii, jj, sx, sy)):
                    best[k] = np.where(m, v, best[k])
    return best[0], best[1].astype(np.int64) * 100003 + best[2].astype(np.int64), best[3], best[4]


def hashu(a, b):
    """A reproducible uniform number in [0, 1) from two integer arrays."""
    x = (a.astype(np.uint64) * np.uint64(0x9E3779B97F4A7C15)) ^ (b.astype(np.uint64) * np.uint64(0xC2B2AE3D27D4EB4F))
    x ^= x >> np.uint64(29)
    x *= np.uint64(0xBF58476D1CE4E5B9)
    x ^= x >> np.uint64(32)
    return (x >> np.uint64(11)).astype(np.float64) / float(1 << 53)


# --------------------------------------------------------------------------- the radio power table for C2
_TABLE = {}


def radio_table(env, ack=0.015):
    """Leaf radio W by ground distance, 100 m steps, for each activity: NaN where the link does not close."""
    key = (env, ack)
    if key in _TABLE:
        return _TABLE[key]
    p = dict(F.BASE, env_db=env, ul_mode=3, ack_share=ack)
    ds = np.arange(50.0, 8001.0, 50.0)
    tab = {}
    for act in ACTS:
        w = []
        for d in ds:
            q = dict(p, urban=1 if d <= 4000 else 0)
            r = T.radio_w_at(q, act, d) if act != "idle" else dict(radio_w=T.LOADS["idle"]["radio_5g_near"])
            w.append(np.nan if (r is None or "fail" in r) else r["radio_w"])
        tab[act] = np.array(w)
    _TABLE[key] = (ds, tab)
    return _TABLE[key]


def leaf_power(act_i, env_i, dist_m, cls):
    """W at the cells for N Leafs. act_i 0 idle 1 delta 2 video. cls 0 C0, 1 C1, 2 C2. NaN: no link at C2."""
    n = act_i.size
    out = np.zeros(n)
    names = ("idle", "delta", "video")
    for k, a in enumerate(names):
        wifi = T.battery_w(T.LOADS[a], T.LOADS[a]["radio_wifi"])
        m0 = (act_i == k) & (cls < 2)
        out[m0] = wifi
        m2 = (act_i == k) & (cls == 2)
        if m2.any():
            for env in (0.0, 8.0, 15.0):
                mm = m2 & (env_i == env)
                if mm.any():
                    ds, tab = radio_table(env)
                    rw = np.interp(dist_m[mm], ds, tab[a], right=np.nan)
                    # np.interp does not propagate NaN safely at an edge: mark a NaN neighbour as no link
                    idx = np.clip(np.searchsorted(ds, dist_m[mm]), 0, ds.size - 1)
                    rw = np.where(np.isnan(tab[a][idx]) | np.isnan(tab[a][np.clip(idx - 1, 0, ds.size - 1)]), np.nan, rw)
                    base = T.LOADS[a]
                    out[mm] = base["body"] / T.ETA_BODY + (base["ring_other"] + rw) / T.ETA_B
                    i = out[mm] / T.V_BUS
                    out[mm] = out[mm] + i * i * T.R_PATH
    return out


# --------------------------------------------------------------------------- one run
def simulate(pr_, seed=5):
    P = dict(PARAMS, **pr_)
    rng = np.random.default_rng(seed)
    N = P["n_leafs"]
    city = CITY_KM * 1000.0
    isd = math.sqrt(3) * P["site_r_km"] * 1000.0            # hex cells of circumradius R
    ns = len(SEGS)
    home = rng.uniform(0, city, (N, 2))
    office = rng.uniform(0, city, (N, 2))
    cafe = office + rng.normal(0, 150.0, (N, 2))
    ang1, ang2 = rng.uniform(0, 2 * math.pi, N), rng.uniform(0, 2 * math.pi, N)
    walk1 = home + np.stack([np.cos(ang1), np.sin(ang1)], 1) * (900.0 * P["v_walk"])     # a 15 min walk
    walk2 = office + np.stack([np.cos(ang2), np.sin(ang2)], 1) * (600.0 * P["v_walk"])   # a 10 min walk
    attr = lambda p_: rng.random(N) < p_
    dock_home, dock_off = attr(P["p_dock_home"]), attr(P["p_dock_office"])
    room_home, room_off, public_c1 = attr(P["p_room_home"]), attr(P["p_room_office"]), attr(P["p_public_c1"])
    host_desk, cradle, pad_home = attr(P["p_host_desk"]), attr(P["p_cradle"]), attr(P["p_pad_home"])
    bank, host_sleep = attr(P["p_bank_walk"]), attr(P["p_host_sleep"])
    # the timeline: t[:, s] is the start of segment s
    shift = rng.normal(0, 1800.0, N)
    veh = np.clip(np.hypot(*(walk2 - walk1).T) / P["v_veh"], 300, 5400)
    t = np.zeros((N, ns + 1))
    t[:, 1] = 7 * 3600 + shift
    t[:, 2] = t[:, 1] + 2700 + rng.normal(0, 300, N)
    t[:, 3] = t[:, 2] + 900
    t[:, 4] = t[:, 3] + veh
    t[:, 5] = t[:, 4] + 600
    t[:, 6] = 12.5 * 3600 + shift * 0.5
    t[:, 7] = t[:, 6] + 2700
    leave = 17.5 * 3600 + rng.normal(0, 1800.0, N)
    t[:, 8] = leave
    t[:, 9] = t[:, 8] + 600
    t[:, 10] = t[:, 9] + veh
    t[:, 11] = t[:, 10] + 900
    t[:, 12] = 23 * 3600 + rng.normal(0, 2400.0, N)
    t[:, 13] = 24 * 3600 + 1.0
    t[:, 1:] = np.maximum.accumulate(np.minimum(t[:, 1:], 24 * 3600 + 1.0), axis=1)
    # start and end position of each segment
    START = np.stack([home, home, home, walk1, walk2, office, cafe, office, office, walk2, walk1, home, home], axis=1)
    END = np.stack([home, home, walk1, walk2, office, office, cafe, office, walk2, walk1, home, home, home], axis=1)
    mixp = np.array([MIXSEG[k] for k in SEGS])
    kind_names = np.array(SEGS)
    idx = np.arange(N)
    hy = P["hyst_frac"] * isd
    # serving C2 site
    sxs = np.zeros(N)
    sys_ = np.zeros(N)
    have_serv = np.zeros(N, dtype=bool)
    cls_time = np.zeros((N, 3))
    sess_time = np.zeros((3, 3))
    seg_cls = np.zeros((ns, 3))
    ho_c2 = np.zeros(N)
    ho_move = {"walk": [0.0, 0.0], "vehicle": [0.0, 0.0]}
    cls_changes = np.zeros(N)
    host_changes = np.zeros(N)
    cell_wh, host_wh, load_wh, hot_s = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    wh_cls, cell_cls, hot_cls = np.zeros(3), np.zeros(3), np.zeros(3)
    out_s, c2_s = np.zeros(3), np.zeros(3)
    hour_sessions = np.zeros((24, 3))
    hour_steps = np.zeros(24)
    site_load = {}
    prev_cls, prev_host = np.full(N, -1), np.full(N, -1)
    for step in range(STEPS):
        tt = step * DT
        s = np.clip((tt >= t[:, 1:-1]).sum(axis=1), 0, ns - 1)
        t0, t1 = t[idx, s], t[idx, s + 1]
        fr = np.clip((tt - t0) / np.maximum(t1 - t0, 1.0), 0, 1)
        a_, b_ = START[idx, s], END[idx, s]
        pos = a_ + fr[:, None] * (b_ - a_)
        kname = kind_names[s]
        blk = np.full(N, int(tt // 3600), dtype=np.int64)       # on the dock or off it, by the hour
        u = hashu(idx + 7, blk)
        is_sleep, is_home, is_desk = kname == "sleep", kname == "home", kname == "desk"
        is_cafe, is_walk, is_veh = kname == "cafe", kname == "walk", kname == "vehicle"
        cls = np.full(N, 2)
        env = np.full(N, 15.0)
        host = np.zeros(N, dtype=np.int64)         # 0 the cell, 1 dock, 2 a host without a heat path, 3 cradle
        cls = np.where(is_sleep, np.where(dock_home, 0, np.where(room_home, 1, 2)), cls)
        host = np.where(is_sleep, np.where(dock_home, 1, np.where(host_sleep, 2, 0)), host)
        dk = dock_home & (u < P["dock_share_home"])
        cls = np.where(is_home, np.where(dk, 0, np.where(room_home, 1, 2)), cls)
        host = np.where(is_home, np.where(dk, 1, np.where(pad_home, 2, 0)), host)
        dk = dock_off & (u < P["dock_share_desk"])
        cls = np.where(is_desk, np.where(dk, 0, np.where(room_off, 1, 2)), cls)
        host = np.where(is_desk, np.where(dk, 1, np.where(host_desk, 2, 0)), host)
        cls = np.where(is_cafe, np.where(public_c1, 1, 2), cls)
        cls = np.where(is_walk | is_veh, 2, cls)
        env = np.where(is_walk, 0.0, np.where(is_veh, 8.0, env))
        host = np.where(is_walk, np.where(bank, 2, 0), host)
        host = np.where(is_veh, np.where(cradle, 3, 0), host)
        ub = hashu(idx + 31, np.full(N, int(tt // 600), dtype=np.int64))
        act = (ub[:, None] >= np.cumsum(mixp[s], axis=1)).sum(axis=1).clip(0, 2)
        # the C2 serving site with a hysteresis
        d, sid, sx, sy = nearest_site(pos, isd)
        d_serv = np.hypot(pos[:, 0] - sxs, pos[:, 1] - sys_)
        change = ~have_serv | ((d + hy) < d_serv)
        ho = change & have_serv & (cls == 2)
        ho_c2 += ho
        for nm in ("walk", "vehicle"):
            mm = kname == nm
            ho_move[nm][0] += float((ho & mm).sum())
            ho_move[nm][1] += float(mm.sum()) * DT
        sxs = np.where(change, sx, sxs)
        sys_ = np.where(change, sy, sys_)
        sid_serv = np.where(change, sid, np.zeros(N, dtype=np.int64)) if False else sid
        have_serv |= change
        dist_c2 = np.hypot(pos[:, 0] - sxs, pos[:, 1] - sys_)
        cls_changes += (prev_cls >= 0) & (cls != prev_cls)
        host_changes += (prev_host >= 0) & ((host > 0) != (prev_host > 0))
        prev_cls, prev_host = cls.copy(), host.copy()
        for c_ in range(3):
            mc = cls == c_
            cls_time[:, c_] += mc * DT
            seg_cls[:, c_] += np.bincount(s[mc], minlength=ns) * DT
            for a2 in range(3):
                sess_time[c_, a2] += float((mc & (act == a2)).sum()) * DT
        w = leaf_power(act, env, np.maximum(dist_c2, 35.0), cls)
        nolink = np.isnan(w)
        m2 = cls == 2
        for a2 in range(3):
            c2_s[a2] += float((m2 & (act == a2)).sum()) * DT
            out_s[a2] += float((m2 & (act == a2) & nolink).sum()) * DT
        w2 = np.where(nolink, T.battery_w(T.LOADS["idle"], T.LOADS["idle"]["radio_5g_near"]), w)   # no link: local only
        wh = w2 * DT / 3600.0
        load_wh += wh
        feed = host > 0
        host_wh += np.where(feed, wh, 0.0)
        cell_wh += np.where(feed, 0.0, wh)
        heatpath = (host == 1) | (host == 3)
        hot = (w2 > P["free_air_w"]) & ~heatpath
        hot_s += hot * DT
        for c_ in range(3):
            mc = cls == c_
            wh_cls[c_] += float(wh[mc].sum())
            cell_cls[c_] += float(np.where(feed, 0.0, wh)[mc].sum())
            hot_cls[c_] += float(hot[mc].sum()) * DT
        hr = int(tt // 3600)
        hour_steps[hr] += 1
        for a2 in range(3):
            hour_sessions[hr, a2] += float((m2 & (act == a2)).sum())
        if step % 30 == 0:
            m_ = m2 & (act > 0)
            if m_.any():
                uids, inv = np.unique(sid[m_], return_inverse=True)
                cd = np.bincount(inv, weights=(act[m_] == 1).astype(float))
                cv = np.bincount(inv, weights=(act[m_] == 2).astype(float))
                site_load.setdefault(hr, []).append((float(cd.max()), float(cv.max())))
    tot = cls_time.sum(axis=0)
    return dict(
        params=P, isd_m=isd, hours_per_day=(tot / N / 3600.0).tolist(), share=(tot / tot.sum()).tolist(),
        sessions_by_class=(sess_time / sess_time.sum(axis=1, keepdims=True).clip(1)).tolist(),
        session_hours=(sess_time.sum(axis=0) / N / 3600.0).tolist(),
        ho_per_hour_walk=ho_move["walk"][0] / max(ho_move["walk"][1], 1) * 3600.0,
        ho_per_hour_vehicle=ho_move["vehicle"][0] / max(ho_move["vehicle"][1], 1) * 3600.0,
        c2_handovers_per_leaf_day=float(ho_c2.mean()), class_changes_per_leaf_day=float(cls_changes.mean()),
        host_changes_per_leaf_day=float(host_changes.mean()),
        wh_day=float(load_wh.mean()), cell_wh_day=float(cell_wh.mean()), host_wh_day=float(host_wh.mean()),
        hot_hours_day=float(hot_s.mean() / 3600.0),
        wh_day_cls=(wh_cls / N).tolist(), cell_wh_day_cls=(cell_cls / N).tolist(), hot_hours_cls=(hot_cls / N / 3600.0).tolist(),
        outage_share=(out_s / np.maximum(c2_s, 1)).tolist(), c2_session_hours=(c2_s / N / 3600.0).tolist(),
        hourly_c2=(hour_sessions / hour_steps[:, None].clip(1) / N).tolist(),
        seg_hours={"%02d %s" % (i, SEGS[i]): (seg_cls[i] / N / 3600.0).tolist() for i in range(ns)},
        site_peak={h: (max(v_[0] for v_ in v), max(v_[1] for v_ in v)) for h, v in site_load.items()},
        n_leafs=N,
    )


# --------------------------------------------------------------------------- the report
def main():
    L = []

    def pr(s=""):
        L.append(s)
        print(s)

    out = {}
    pr("FLEET seat · the roaming fleet · a simulated day in a city of %d x %d km, %d Leafs, steps of %d s" % (CITY_KM, CITY_KM, PARAMS["n_leafs"], DT))
    pr("The Leaf is the ruled B module of fleet.py. Cores: C2 sites on a hexagonal grid, C1 room Cores, C0 docks. Every assumption is a [HYPOTHESIS].")
    pr("")
    base = simulate({})
    out["base"] = base
    pr("1 · the base day. Sector radius %.1f km (inter-site distance %.2f km), room Cores at %.0f %% of homes and desks, docks at %.0f %%." % (
        PARAMS["site_r_km"], base["isd_m"] / 1000, 100 * PARAMS["p_room_home"], 100 * PARAMS["p_dock_home"]))
    hrs = base["hours_per_day"]
    pr("  hours per Leaf and day: C0 %.1f, C1 %.1f, C2 %.1f  (shares %.0f %%, %.0f %%, %.0f %%)" % (
        hrs[0], hrs[1], hrs[2], *(100 * x for x in base["share"])))
    sh = base["session_hours"]
    pr("  session hours per Leaf and day: idle %.1f, delta %.1f, video %.1f" % tuple(sh))
    sbc = np.array(base["sessions_by_class"])
    pr("  activity share inside each class (rows C0, C1, C2; columns idle, delta, video):")
    for i, c in enumerate(("C0", "C1", "C2")):
        pr("    %s  %.2f  %.2f  %.2f" % (c, *sbc[i]))
    pr("  time by segment (hours on C0, C1, C2):")
    for k, v in base["seg_hours"].items():
        pr("    %-10s %5.2f %5.2f %5.2f" % (k, *v))
    pr("")
    pr("2 · the hand-overs")
    pr("  C2 to C2 hand-overs while walking: %.1f per hour; in a vehicle: %.1f per hour [net/discovery city run: 4.5 per hour, mixed]" % (
        base["ho_per_hour_walk"], base["ho_per_hour_vehicle"]))
    pr("  per Leaf and day: %.1f C2 hand-overs, %.1f class changes (a compute host change each), %.1f energy host changes" % (
        base["c2_handovers_per_leaf_day"], base["class_changes_per_leaf_day"], base["host_changes_per_leaf_day"]))
    pr("  Each compute host change is a hot-shadow switch: 0 frames lost in the planned case [TREE] net/discovery policy C, 4 to 5 covered on a failure.")
    pr("")
    pr("3 · the energy and the heat of the day")
    pr("  load energy %.1f Wh per Leaf and day; from a host %.1f Wh; from the cell %.1f Wh" % (base["wh_day"], base["host_wh_day"], base["cell_wh_day"]))
    full_s = 7.38 * 0.96
    pr("  the cell alone: %.2f cycles per day on Full S (%.1f Wh usable); the cell floats on a host (Part 22.4)" % (base["cell_wh_day"] / full_s, full_s))
    pr("  time above the free-air limit of 1.73 W with no heat path: %.1f h per Leaf and day (a dock plate or a cradle is a heat path)" % base["hot_hours_day"])
    pr("  by class, per Leaf and day:  %-10s %8s %8s %8s" % ("", "C0", "C1", "C2"))
    pr("    load energy, Wh             %-10s %8.1f %8.1f %8.1f" % ("", *base["wh_day_cls"]))
    pr("    from the cell, Wh           %-10s %8.1f %8.1f %8.1f" % ("", *base["cell_wh_day_cls"]))
    pr("    hours above 1.73 W, no plate %-9s %8.1f %8.1f %8.1f" % ("", *base["hot_hours_cls"]))
    pr("    mean load per hour on the class, W: %s" % ", ".join("%s %.2f" % (c, w / max(h, 1e-9)) for c, w, h in zip(("C0", "C1", "C2"), base["wh_day_cls"], base["hours_per_day"])))
    ow = base["outage_share"]
    pr("  C2 session time with no link at this site spacing: idle %.1f %%, delta %.1f %%, video %.1f %%; C2 session hours per day: %s" % (
        100 * ow[0], 100 * ow[1], 100 * ow[2], ", ".join("%.2f" % x for x in base["c2_session_hours"])))
    pr("")
    pr("4 · the C2 sessions by the hour (share of all Leafs in a C2 session of that kind, mean of the hour)")
    hc = np.array(base["hourly_c2"])
    pr("  hour   delta  video   busiest site: delta, video (5 min peaks of the %d-Leaf city)" % base["n_leafs"])
    for h in range(24):
        sp = base["site_peak"].get(h) or base["site_peak"].get(str(h))
        pr("  %02d   %6.3f %6.3f   %s" % (h, hc[h, 1], hc[h, 2], "%d, %d" % (sp[0], sp[1]) if sp else "-"))
    peak_h = int(np.argmax(hc[:, 1] + hc[:, 2] * 3))
    out["peak_hour"] = peak_h
    pr("  The peak hour is %02d:00. C2 delta share %.1f %%, C2 video share %.1f %% of all Leafs." % (peak_h, 100 * hc[peak_h, 1], 100 * hc[peak_h, 2]))
    cap_d, cap_v = 3 * F.n_for(dict(F.BASE, c2_radius_m=1000.0), "delta", "C2")["groups"]["radio"], 3 * F.n_for(dict(F.BASE, c2_radius_m=1000.0), "video", "C2")["groups"]["radio"]
    area = 2.598 * PARAMS["site_r_km"] ** 2
    dens = 1.0 / (area * (hc[peak_h, 1] / cap_d + hc[peak_h, 2] / cap_v))
    out["leafs_per_km2_at_peak"] = dens
    pr("  A site of 3 sectors at R = 1 km (%.1f km2) has radio capacity for %.0f delta or %.0f video sessions." % (area, cap_d, cap_v))
    pr("  At the real peak this carries %.0f registered Leafs per km2. The mix of fleet.py (15 %% in a session) would give %.0f." % (
        dens, 1.0 / (area * (0.12 / cap_d + 0.03 / cap_v))))
    pr("")

    # --------------------------------------------------------------- the deployment sweep
    pr("5 · the deployment of room Cores and docks changes the C2 share (sector radius 1 km)")
    pr("  %-26s %6s %6s %6s %9s %8s %8s %8s" % ("deployment", "C0 h", "C1 h", "C2 h", "cell Wh", "hot h", "HO/day", "cls/day"))
    dep = {}
    for lab, kw in (("no room Core, no dock", dict(p_room_home=0, p_room_office=0, p_dock_home=0, p_dock_office=0, p_public_c1=0)),
                    ("docks only", dict(p_room_home=0, p_room_office=0, p_dock_home=0.5, p_dock_office=0.5, p_public_c1=0)),
                    ("base: 60 % room, 50 % dock", {}),
                    ("everyone has both", dict(p_room_home=1, p_room_office=1, p_dock_home=1, p_dock_office=1, p_public_c1=0.3))):
        r = base if not kw else simulate(kw, seed=6)
        dep[lab] = r
        pr("  %-26s %6.1f %6.1f %6.1f %9.1f %8.1f %8.1f %8.1f" % (
            lab, *r["hours_per_day"], r["cell_wh_day"], r["hot_hours_day"], r["c2_handovers_per_leaf_day"], r["class_changes_per_leaf_day"]))
    out["deployment"] = {k: {kk: vv for kk, vv in v.items() if kk in ("hours_per_day", "cell_wh_day", "hot_hours_day", "c2_handovers_per_leaf_day", "class_changes_per_leaf_day", "outage_share")} for k, v in dep.items()}
    pr("")
    pr("6 · the sector radius of the C2 grid changes the hand-over rate and the outage (deployment: base)")
    pr("  %8s %8s %10s %10s %9s %9s %9s" % ("R km", "ISD km", "HO/h walk", "HO/h veh", "out dlt %", "out vid %", "HO/day"))
    rr = {}
    for rk in (0.5, 1.0, 1.5, 2.0, 3.0):
        r = base if rk == 1.0 else simulate(dict(site_r_km=rk), seed=7)
        rr[str(rk)] = r
        pr("  %8.1f %8.2f %10.1f %10.1f %9.1f %9.1f %9.1f" % (
            rk, r["isd_m"] / 1000, r["ho_per_hour_walk"], r["ho_per_hour_vehicle"], 100 * r["outage_share"][1],
            100 * r["outage_share"][2], r["c2_handovers_per_leaf_day"]))
    out["radius"] = {k: {kk: vv for kk, vv in v.items() if kk in ("isd_m", "ho_per_hour_walk", "ho_per_hour_vehicle", "outage_share", "c2_handovers_per_leaf_day")} for k, v in rr.items()}
    pr("  The outage is the share of C2 session minutes where the SAR uplink or the downlink does not close at the base case of fleet.py.")
    with open(os.path.join(OUT, "roam.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    with open(os.path.join(OUT, "roam.txt"), "w") as f:
        f.write("\n".join(L) + "\n")
    return out


if __name__ == "__main__":
    main()
