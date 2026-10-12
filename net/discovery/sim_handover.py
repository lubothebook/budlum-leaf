#!/usr/bin/env python3
"""sim_handover.py: a discrete-event simulation of one Leaf moving through a city.

FINAL/21 Section 21.5.4. Gates DST-12 (zero-frame handover) and SW-24
(the Leaf serves from the lowest round trip). Uses netmodel.py.

The world
  * a city of city_km x city_km, n_val validators. A share sits at 5G edge
    sites (the L1 cell layer), the rest at metro sites (the L1 metro layer);
  * 5G everywhere, with local breakout at the nearest edge site;
  * Wi-Fi in venue zones, with breakout at the nearest ISP PoP;
  * validator brownouts (queue and loss) and crashes, as Poisson processes.

The Leaf
  * bootstraps 3 to 5 candidates from the anycast reply (latency map);
  * probes each candidate once per second (PathProbe), keeps an EWMA score;
  * keeps a primary P and a shadow S, and multipath QUIC on Wi-Fi and 5G;
  * switches on a soft trigger (RTT or loss) or a hard one (P silent).

The four policies
  A  no shadow: a new validator needs a handshake, a state sync and a key frame;
  B  state-hot shadow, cut at the next frame (HandoverCommand, no lead);
  C  state-hot shadow, scheduled switch_frame with a lead, plus K frames of
     overlap from P (make before break). The proposed default;
  D  render-hot shadow that streams every frame all the time (2x downlink).

Output: results/handover.json and results/handover_latency_cdf.png.
    python3 sim_handover.py            # full run, about 3 minutes
    python3 sim_handover.py --quick    # smoke run
"""
import argparse
import heapq
import json
import math
import os
import random
from dataclasses import dataclass, field, asdict

import netmodel as nm

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


@dataclass
class Params:
    seed: int = 1
    policy: str = "C"
    duration_s: float = 600.0
    city_km: float = 40.0
    city_h_km: float = 0.0           # 0 = square
    layout: str = "city"             # "city" or "corridor"
    n_val: int = 24
    frac_cell: float = 0.33          # share of validators at 5G edge sites
    edge_km: float = 8.0             # spacing of 5G breakout (UPF) sites
    n_pops: int = 3                  # ISP PoPs for Wi-Fi breakout
    n_wifi_zones: int = 120
    wifi_r_km: float = 0.10
    drive_frac: float = 0.5
    v_drive_mps: float = 12.0
    v_walk_mps: float = 1.4
    cell_km: float = 0.4             # 5G cell size: one radio handover per cell
    radio_ho_ms: float = 0.0         # 0 = DAPS (Rel-16), 20-40 = legacy
    brownout_per_h: float = 2.0      # per validator
    brownout_s: float = 20.0
    brownout_q_ms: float = 3.0
    brownout_loss: float = 0.03
    crash_per_h: float = 0.5         # per validator, a stressed fleet
    crash_down_s: float = 120.0
    q_ms: float = 0.05               # normal queue mean, one way
    loss_wifi: float = 0.001         # residual after MAC retries
    loss_cell: float = 0.0005        # residual after HARQ and RLC
    loss_val: float = 0.0002
    d_dl_ms: float = 8.0             # a frame later than this is lost
    probe_s: float = 1.0
    n_cand: int = 5
    boot_s: float = 30.0
    probe_win: int = 5               # the score uses the last 5 probes
    score_mode: str = "mix"          # min + half of (median - min)
    burst: bool = True               # all probes of a round in one burst
    hyst_rel: float = 0.0
    hyst_abs_ms: float = 0.25
    n_consec: int = 3
    loss_trig: float = 0.01
    detect_frames: int = 2
    warm_ms: float = 5.8             # render the reference frame + encode
    lead_margin_ms: float = 2.0
    overlap_frames: int = 4
    sync_ms: float = 60.0            # new shadow: state copy from P and announce
    se_check_ms: float = 20.0        # U7 active-set check on a new key
    keyframe_ms: float = 8.0         # policy A: the key frame and the reload


# ------------------------------------------------------------------ world ---

class World:
    def __init__(self, p: Params):
        r = random.Random(p.seed * 7919)
        L = p.city_km
        Ly = p.city_h_km or L
        self.p = p
        # edge sites on a grid
        nx = max(1, int(round(L / p.edge_km)))
        ny = max(1, int(round(Ly / p.edge_km)))
        self.edges = [((i + 0.5) * L / nx, (j + 0.5) * Ly / ny)
                      for i in range(nx) for j in range(ny)]
        if p.layout == "corridor":   # one PoP per 40 km along the corridor
            self.pops = [((k + 0.5) * 40.0, Ly / 2) for k in range(max(1, int(L // 40)))]
        else:
            self.pops = [(L / 2 + r.gauss(0, L / 8), Ly / 2 + r.gauss(0, Ly / 8))
                         for _ in range(p.n_pops)]
        # validators
        n_cell = int(round(p.frac_cell * p.n_val))
        sites = r.sample(range(len(self.edges)), min(n_cell, len(self.edges)))
        self.vals = []
        for s in sites:
            self.vals.append(dict(pos=self.edges[s], kind="cell", edge=s))
        while len(self.vals) < p.n_val:
            if p.layout == "corridor":
                pos = (r.uniform(0, L), r.uniform(0, Ly))
            else:
                pos = (min(L, max(0, r.gauss(L / 2, L / 4))),
                       min(Ly, max(0, r.gauss(Ly / 2, Ly / 4))))
            self.vals.append(dict(pos=pos, kind="metro", edge=None))
        for v in self.vals:
            v["stretch"] = r.uniform(1.3, 2.0)
        # Wi-Fi venue zones
        self.zones = [(r.uniform(0, L), r.uniform(0, Ly)) for _ in range(p.n_wifi_zones)]
        # validator events
        T = p.duration_s
        self.brown = [[] for _ in self.vals]
        self.crash = [[] for _ in self.vals]
        for i in range(len(self.vals)):
            t = 0.0
            while True:
                t += r.expovariate(p.brownout_per_h / 3600.0)
                if t > T:
                    break
                self.brown[i].append((t, t + r.expovariate(1.0 / p.brownout_s)))
            t = 0.0
            while p.crash_per_h > 0:
                t += r.expovariate(p.crash_per_h / 3600.0)
                if t > T:
                    break
                self.crash[i].append((t, t + p.crash_down_s))
                t += p.crash_down_s
        # trajectory: waypoints, each leg on foot or by car
        self.legs = []
        t = 0.0
        if p.layout == "corridor":   # drive end to end and back
            pos = (0.0, Ly / 2)
        else:
            pos = (r.uniform(0, L), r.uniform(0, Ly))
        while t < T:
            if p.layout == "corridor":
                nxt = (L if pos[0] < L / 2 else 0.0, r.uniform(0.3 * Ly, 0.7 * Ly))
            else:
                nxt = (r.uniform(0, L), r.uniform(0, Ly))
            v = p.v_drive_mps if r.random() < p.drive_frac else p.v_walk_mps
            d = nm.dist(pos, nxt) * 1000.0
            dur = max(1.0, d / v)
            self.legs.append((t, t + dur, pos, nxt))
            t += dur
            pos = nxt

    def user_pos(self, t):
        for a, b, p0, p1 in self.legs:
            if a <= t <= b:
                f = (t - a) / (b - a)
                return (p0[0] + f * (p1[0] - p0[0]), p0[1] + f * (p1[1] - p0[1]))
        return self.legs[-1][3]

    def v_state(self, i, t):
        """(up, extra queue mean, extra loss) of validator i at time t (s)."""
        for a, b in self.crash[i]:
            if a <= t < b:
                return False, 0.0, 1.0
        for a, b in self.brown[i]:
            if a <= t < b:
                return True, self.p.brownout_q_ms, self.p.brownout_loss
        return True, 0.0, 0.0

    def first_crash_after(self, i, t):
        for a, b in self.crash[i]:
            if a >= t:
                return a
        return None


# --------------------------------------------------------------- the sim ---

class Sim:
    def __init__(self, p: Params):
        self.p = p
        self.w = World(p)
        self.r = random.Random(p.seed * 104729 + ord(p.policy))
        self.q = []
        self.seq = 0
        self.t = 0.0                 # ms
        self.pos = self.w.user_pos(0)
        self.base = {}               # (path, v) -> one-way wired ms
        self.paths = [nm.CELL]
        self.edge_idx = None
        self.cell_count = 0
        self.radio_gap_until = -1.0
        self.score = {}
        self.win = {}
        self.why = {}
        self.regret = []
        self.cands = []
        self.P = None
        self.S = None                # (v, ready_at_ms)
        self.S_sync = None           # (v, done_at_ms) a shadow being synced
        self.switch = None           # dict of the switch in progress
        self.bad_consec = 0
        self.lossP_win = []          # (t, lost) frames from P in the last second
        self.stats = dict(frames=0, lost=0, lost_network=0, lost_handover=0,
                          lost_failover=0, reloads=0, ho_planned=0,
                          ho_failover=0, dual_frames=0, frames_sent=0)
        self.ho_losses = []          # frames lost per handover
        self.lat = []
        self.rtt_P = []
        self.served_layer = {"cell": 0, "metro": 0}
        self.best_pick = 0
        self.picks = 0
        self.down_since = None

    # ---- the event queue ----
    def at(self, t, kind, data=None):
        self.seq += 1
        heapq.heappush(self.q, (t, self.seq, kind, data))

    # ---- network geometry ----
    def update_geometry(self):
        w, p = self.w, self.p
        self.pos = w.user_pos(self.t / 1000.0)
        e = min(range(len(w.edges)), key=lambda k: nm.dist(self.pos, w.edges[k]))
        if self.edge_idx is not None and e != self.edge_idx:
            self.at(self.t, "bootstrap")
        self.edge_idx = e
        epos = w.edges[e]
        in_wifi = any(nm.dist(self.pos, z) < p.wifi_r_km for z in w.zones)
        self.paths = [nm.CELL] + ([nm.WIFI] if in_wifi else [])
        pop = min(w.pops, key=lambda q: nm.dist(self.pos, q))
        for i, v in enumerate(w.vals):
            if v["edge"] == e:
                cell = nm.UPF_MS + nm.wired_ow_ms(nm.dist(self.pos, epos), 0, hops=1)
            else:
                cell = nm.UPF_MS + nm.wired_ow_ms(nm.dist(self.pos, epos),
                                                  nm.dist(epos, v["pos"]),
                                                  stretch_core=v["stretch"])
            self.base[(nm.CELL, i)] = cell
            self.base[(nm.WIFI, i)] = nm.wired_ow_ms(nm.dist(self.pos, pop),
                                                     nm.dist(pop, v["pos"]),
                                                     stretch_core=v["stretch"],
                                                     fixed=nm.OLT_MS)

    def radio_tick(self, dist_m):
        """Count 5G cell changes along the path; each costs radio_ho_ms."""
        if self.p.radio_ho_ms <= 0:
            return
        self.cell_count += dist_m
        if self.cell_count >= self.p.cell_km * 1000:
            self.cell_count = 0
            self.radio_gap_until = self.t + self.p.radio_ho_ms

    def best_path(self, v):
        ps = [k for k in self.paths if not (k == nm.CELL and self.t < self.radio_gap_until)]
        if not ps:
            return None
        return min(ps, key=lambda k: self.base[(k, v)] + nm.AIR_DL_MEAN[k])

    def ow_dl(self, v, send_ms):
        """Downlink one-way delay of one frame from v, or None when lost."""
        up, xq, xl = self.w.v_state(v, send_ms / 1000.0)
        if not up:
            return None
        path = self.best_path(v)
        if path is None:
            return None
        r = self.r
        d = self.base[(path, v)] + nm.queue_ms(r, self.p.q_ms + xq) + nm.air_dl_ms(r, path)
        loss = (self.p.loss_wifi if path == nm.WIFI else self.p.loss_cell) + self.p.loss_val + xl
        if r.random() < loss:
            alts = [k for k in self.paths if k != path]
            if alts:   # multipath QUIC: resend on the other path after one slice
                k = alts[0]
                d = d + nm.FRAME_MS / 4 + self.base[(k, v)] + nm.air_dl_ms(r, k)
            else:      # one path: QUIC loss detection after about 1.125 RTT
                d = d + 1.125 * 2 * d + self.base[(path, v)] + nm.air_dl_ms(r, path)
            if r.random() < xl:   # the brownout drops the resend too
                return None
        return d

    def ow_up(self, v):
        path = self.best_path(v) or nm.CELL
        return (nm.air_up_ms(self.r, path) + self.base[(path, v)]
                + nm.queue_ms(self.r, self.p.q_ms + self.w.v_state(v, self.t / 1000)[1]))

    def true_rtt(self, v):
        path = self.best_path(v) or nm.CELL
        return 2 * self.base[(path, v)] + nm.AIR_DL_MEAN[path] + nm.AIR_UP_MEAN[path]

    # ---- the control plane ----
    def bootstrap(self):
        """The anycast reply: the n_cand lowest round trips on the latency map."""
        live = [i for i in range(len(self.w.vals)) if self.w.v_state(i, self.t / 1000)[0]]
        ranked = sorted(live, key=self.true_rtt)
        keep = [x for x in (self.P, self.S and self.S[0]) if x is not None]
        self.cands = list(dict.fromkeys(ranked[: self.p.n_cand] + keep))

    def probe(self):
        """One probe round. The Leaf sends the probes of a round in one burst
        on one path, so the air delay is common to all candidates and cancels
        in the comparison (SPEC.md Section 3.4). Each candidate adds its wired
        leg, its queue and a small independent jitter."""
        r = self.r
        air = {k: nm.air_up_ms(r, k) + nm.air_dl_ms(r, k) for k in (nm.CELL, nm.WIFI)}
        for c in self.cands:
            up, xq, xl = self.w.v_state(c, self.t / 1000)
            path = self.best_path(c) or nm.CELL
            if not up or r.random() < xl + self.p.loss_val:
                rtt = 1e3                          # a timeout
            elif self.p.burst:
                rtt = (air[path] + 2 * self.base[(path, c)]
                       + nm.queue_ms(r, self.p.q_ms + xq) + nm.queue_ms(r, self.p.q_ms + xq)
                       + r.expovariate(1 / 0.05))
            else:
                rtt = self.ow_up(c) + (self.ow_dl(c, self.t) or 1e3)
            w = self.win.setdefault(c, [])
            w.append(rtt)
            del w[:-self.p.probe_win]
            ws = sorted(w)
            if self.p.score_mode == "median":
                self.score[c] = ws[len(ws) // 2]
            else:   # "mix": the min filters the air jitter, the median catches queues
                self.score[c] = ws[0] + 0.5 * (ws[len(ws) // 2] - ws[0])
            if c == self.P:
                self.rtt_P.append(rtt)

    def pick_shadow(self):
        if self.p.policy == "A" or self.P is None:
            return
        if self.S is not None or self.S_sync is not None:
            return
        others = [c for c in self.cands if c != self.P and self.w.v_state(c, self.t / 1000)[0]]
        if not others:
            return
        c = min(others, key=lambda x: self.score.get(x, self.true_rtt(x)))
        self.start_sync(c)

    def start_sync(self, c):
        done = self.t + self.p.sync_ms + 2 * self.ow_up(c)
        self.S_sync = (c, done)
        self.at(done, "sync_done", c)

    def evaluate(self):
        """The soft trigger, once per probe round."""
        if self.P is None or self.switch is not None:
            return
        now = self.t
        self.lossP_win = [(a, b) for a, b in self.lossP_win if a > now - 1000]
        n = len(self.lossP_win)
        loss = sum(b for _, b in self.lossP_win) / n if n else 0.0
        sP = self.score.get(self.P, 1e3)
        others = [c for c in self.cands if c != self.P]
        if not others:
            return
        best = min(others, key=lambda x: self.score.get(x, 1e3))
        sB = self.score.get(best, 1e3)
        bad = sP > sB * (1 + self.p.hyst_rel) + self.p.hyst_abs_ms
        self.bad_consec = self.bad_consec + 1 if bad else 0
        if not (self.bad_consec >= self.p.n_consec or loss > self.p.loss_trig):
            return
        why = "rtt" if self.bad_consec >= self.p.n_consec else "loss"
        self.why[why] = self.why.get(why, 0) + 1
        if self.p.policy == "A":
            self.begin_reload(best, planned=True)
            return
        if self.S is not None and self.S[0] == best:
            self.begin_switch(planned=True)
        elif self.S_sync is None or self.S_sync[0] != best:
            self.start_sync(best)    # make the target the shadow first

    def begin_reload(self, target, planned):
        """Policy A, and any policy with no shadow: a full new session."""
        rtt = self.true_rtt(target)
        ready = self.t + 2 * rtt + self.p.se_check_ms + self.p.sync_ms + self.p.keyframe_ms
        self.switch = dict(kind="reload", to=target, ready=ready, t0=self.t,
                           planned=planned, lost=0)
        self.stats["reloads"] += 1
        self.at(ready, "switch_done")

    def begin_switch(self, planned):
        v = self.S[0]
        p = self.p
        lead_up = self.ow_up(v)
        ready = self.t + lead_up + p.warm_ms
        if p.policy == "B" or not planned:
            sf_time = self.t           # cut at the next frame
        else:                          # C and D: scheduled switch_frame
            sf_time = self.t + lead_up + p.warm_ms + p.lead_margin_ms
        if p.policy == "D":            # the shadow already streams every frame
            ready = self.t
            sf_time = self.t
        self.switch = dict(kind="shadow", to=v, ready=ready, sf_time=sf_time,
                           t0=self.t, planned=planned, lost=0,
                           end=sf_time + p.overlap_frames * nm.FRAME_MS)
        self.at(max(ready, sf_time) + (p.overlap_frames + 1) * nm.FRAME_MS, "switch_done")

    def switch_done(self):
        sw = self.switch
        if sw is None:
            return
        self.ho_losses.append(sw["lost"])
        self.stats["ho_planned" if sw["planned"] else "ho_failover"] += 1
        self.P = sw["to"]
        if self.S is not None and self.S[0] == self.P:
            self.S = None
        self.switch = None
        self.bad_consec = 0
        self.down_since = None
        self.pick_shadow()

    # ---- the frame ----
    def frame(self, f_ms):
        p = self.p
        self.stats["frames"] += 1
        sources = []                   # (validator, send time)
        sw = self.switch
        if self.P is not None:
            if sw is None:
                sources.append((self.P, f_ms))
                if p.policy == "D" and self.S is not None:
                    sources.append((self.S[0], f_ms))
            elif sw["kind"] == "reload":
                if f_ms >= sw["ready"]:
                    sources.append((sw["to"], f_ms))
                else:
                    sources.append((self.P, f_ms))
            else:
                if f_ms < sw["sf_time"]:
                    sources.append((self.P, f_ms))
                    if p.policy == "D":
                        sources.append((sw["to"], f_ms))
                else:
                    sources.append((sw["to"], max(f_ms, sw["ready"])))
                    if f_ms < sw["end"] and p.policy in ("C", "D"):
                        sources.append((self.P, f_ms))
        best = None
        for v, send in sources:
            self.stats["frames_sent"] += 1
            d = self.ow_dl(v, send)
            if d is None:
                continue
            late = send - f_ms + d
            if best is None or late < best[1]:
                best = (v, late)
        if len(sources) > 1:
            self.stats["dual_frames"] += 1
        fromP = self.P
        lost = best is None or best[1] > p.d_dl_ms
        if fromP is not None and sw is None:
            self.lossP_win.append((f_ms, 1 if lost else 0))
        if lost:
            self.stats["lost"] += 1
            new_side = sw is not None and f_ms >= (sw["sf_time"] if sw["kind"] == "shadow" else sw["ready"])
            if sw is not None and not sw["planned"]:
                sw["lost"] += 1
                self.stats["lost_failover"] += 1
            elif new_side:           # a frame the new validator owed: the switch lost it
                sw["lost"] += 1
                self.stats["lost_handover"] += 1
            elif sw is not None:     # the old primary was failing: that is why we switch
                self.stats["lost_network"] += 1
            elif self.P is not None and not self.w.v_state(self.P, f_ms / 1000)[0]:
                self.stats["lost_failover"] += 1
                if self.down_since is None:
                    self.down_since = f_ms
                    self.at(f_ms + p.detect_frames * nm.FRAME_MS, "detect")
            else:
                self.stats["lost_network"] += 1
            return
        v, late = best
        r = self.r
        e2e = (nm.touch_ms(r) + self.ow_up(v) + nm.render_ms(r) + nm.encode_ms(r)
               + late + nm.decode_ms(r) + nm.scanout_ms(r))
        self.lat.append(e2e)
        self.served_layer[self.w.vals[v]["kind"]] += 1

    def detect(self):
        """P is silent for detect_frames: fail over to the shadow or reload."""
        if self.switch is not None:
            return
        if self.S is not None and self.w.v_state(self.S[0], self.t / 1000)[0]:
            self.begin_switch(planned=False)
        else:
            live = [c for c in self.cands if c != self.P and self.w.v_state(c, self.t / 1000)[0]]
            if not live:
                self.bootstrap()
                live = [c for c in self.cands if c != self.P]
            tgt = min(live, key=self.true_rtt)
            self.begin_reload(tgt, planned=False)
        self.down_since = None

    # ---- the main loop ----
    def run(self):
        p = self.p
        T = p.duration_s * 1000.0
        self.update_geometry()
        self.bootstrap()
        self.probe()
        self.P = min(self.cands, key=lambda c: self.score[c])
        self.pick_shadow()
        self.at(100.0, "move")
        self.at(p.probe_s * 1000, "probe")
        self.at(p.boot_s * 1000, "boot_timer")
        f = 0
        next_frame = 0.0
        last_pos = self.pos
        while True:
            t_ev = self.q[0][0] if self.q else math.inf
            if next_frame <= t_ev:
                if next_frame > T:
                    break
                self.t = next_frame
                self.frame(next_frame)
                f += 1
                next_frame = f * nm.FRAME_MS
                continue
            t, _, kind, data = heapq.heappop(self.q)
            if t > T:
                break
            self.t = t
            if kind == "move":
                self.update_geometry()
                self.radio_tick(nm.dist(last_pos, self.pos) * 1000)
                last_pos = self.pos
                self.at(t + 100.0, "move")
            elif kind == "probe":
                self.probe()
                self.evaluate()
                if self.S is not None and not self.w.v_state(self.S[0], t / 1000)[0]:
                    self.S = None
                self.pick_shadow()
                self.picks += 1
                live = [c for c in self.cands if self.w.v_state(c, t / 1000)[0]]
                if live and self.P is not None:
                    b = min(live, key=self.true_rtt)
                    self.best_pick += self.P == b
                    self.regret.append(self.true_rtt(self.P) - self.true_rtt(b))
                self.at(t + p.probe_s * 1000, "probe")
            elif kind in ("bootstrap", "boot_timer"):
                self.bootstrap()
                if kind == "boot_timer":
                    self.at(t + p.boot_s * 1000, "boot_timer")
            elif kind == "sync_done":
                if self.S_sync is not None and self.S_sync[0] == data:
                    if self.w.v_state(data, t / 1000)[0] and data != self.P:
                        self.S = (data, t)
                    self.S_sync = None
            elif kind == "detect":
                if self.P is not None and not self.w.v_state(self.P, t / 1000)[0]:
                    self.detect()
                else:
                    self.down_since = None
            elif kind == "switch_done":
                self.switch_done()
        return self.report()

    def report(self):
        s = dict(self.stats)
        lat = sorted(self.lat)
        n = len(lat)
        rt = sorted(x for x in self.rtt_P if x < 1e3)
        q = lambda xs, a: xs[min(len(xs) - 1, int(a * (len(xs) - 1)))] if xs else float("nan")
        s.update(p50_ms=q(lat, 0.50), p99_ms=q(lat, 0.99), p999_ms=q(lat, 0.999),
                 mean_ms=sum(lat) / n if n else float("nan"),
                 rtt_p50_ms=q(rt, 0.5), rtt_p99_ms=q(rt, 0.99),
                 ho_losses=self.ho_losses,
                 best_pick_share=self.best_pick / max(1, self.picks),
                 regret=self.regret, why=self.why,
                 cell_layer_share=self.served_layer["cell"] / max(1, n),
                 lat_sample=lat[:: max(1, n // 4000)])
        return s


# ---------------------------------------------------------- experiments ---

def aggregate(runs):
    keys = ["frames", "lost", "lost_network", "lost_handover", "lost_failover",
            "reloads", "ho_planned", "ho_failover", "dual_frames", "frames_sent"]
    a = {k: sum(r[k] for r in runs) for k in keys}
    lat = sorted(x for r in runs for x in r["lat_sample"])
    q = lambda xs, f: xs[min(len(xs) - 1, int(f * (len(xs) - 1)))]
    hours = a["frames"] / nm.FRAME_HZ / 3600
    ho_planned = [x for r in runs for x in r["ho_losses"]]
    a.update(
        hours=round(hours, 2),
        p50_ms=round(q(lat, 0.5), 2), p99_ms=round(q(lat, 0.99), 2),
        p999_ms=round(q(lat, 0.999), 2),
        rtt_p50_ms=round(sum(r["rtt_p50_ms"] for r in runs) / len(runs), 3),
        rtt_p99_ms=round(sum(r["rtt_p99_ms"] for r in runs) / len(runs), 3),
        loss_ppm=round(1e6 * a["lost"] / a["frames"], 1),
        handover_loss_ppm=round(1e6 * a["lost_handover"] / a["frames"], 2),
        failover_loss_ppm=round(1e6 * a["lost_failover"] / a["frames"], 1),
        handovers_per_h=round((a["ho_planned"] + a["ho_failover"]) / hours, 1),
        frames_lost_per_planned_ho=round(a["lost_handover"] / max(1, a["ho_planned"]), 3),
        frames_lost_per_failover=round(a["lost_failover"] / max(1, a["ho_failover"]), 2),
        zero_loss_handover_share=round(sum(1 for x in ho_planned if x == 0) / max(1, len(ho_planned)), 4),
        downlink_overhead=round(a["frames_sent"] / a["frames"] - 1, 4),
        best_pick_share=round(sum(r["best_pick_share"] for r in runs) / len(runs), 3),
        regret_mean_ms=round(sum(x for r in runs for x in r["regret"]) / max(1, sum(len(r["regret"]) for r in runs)), 3),
        regret_p99_ms=round(q(sorted(x for r in runs for x in r["regret"]), 0.99), 3),
        cell_layer_share=round(sum(r["cell_layer_share"] for r in runs) / len(runs), 3),
    )
    return a, lat


def run_policy(policy, seeds, **kw):
    runs = [Sim(Params(seed=s, policy=policy, **kw)).run() for s in seeds]
    return aggregate(runs)


SCENARIOS = {
    # name: (Params overrides, seeds, duration s)
    "city": (dict(), 8, 600.0),
    "stress": (dict(brownout_per_h=20.0, crash_per_h=3.0), 8, 600.0),
    "intercity": (dict(layout="corridor", city_km=160.0, city_h_km=20.0, n_val=40,
                       drive_frac=1.0, v_drive_mps=30.0, n_wifi_zones=40), 6, 1800.0),
}
KEYS = ("hours", "p50_ms", "p99_ms", "p999_ms", "rtt_p50_ms", "rtt_p99_ms", "loss_ppm",
        "handover_loss_ppm", "failover_loss_ppm", "handovers_per_h", "ho_planned",
        "ho_failover", "frames_lost_per_planned_ho", "frames_lost_per_failover",
        "zero_loss_handover_share", "reloads", "downlink_overhead", "regret_mean_ms",
        "regret_p99_ms", "cell_layer_share")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    os.makedirs(RES, exist_ok=True)
    out = dict(params=asdict(Params()), scenarios={}, sweep_n_val={}, legacy_radio_ho={})
    cdfs = {}
    for name, (kw, n_seeds, dur) in SCENARIOS.items():
        if args.quick:
            n_seeds, dur = 2, min(dur, 150.0)
        out["scenarios"][name] = dict(overrides=kw, seeds=n_seeds, duration_s=dur, policies={})
        for pol in "ABCD":
            a, lat = run_policy(pol, range(1, n_seeds + 1), duration_s=dur, **kw)
            out["scenarios"][name]["policies"][pol] = {k: a[k] for k in KEYS}
            if name == "city":
                cdfs[pol] = lat
            print(name, pol, json.dumps({k: a[k] for k in KEYS}), flush=True)
    seeds = range(1, 3) if args.quick else range(1, 7)
    dur = 150.0 if args.quick else 600.0
    for n in (6, 12, 24, 48):
        a, _ = run_policy("C", seeds, duration_s=dur, n_val=n)
        out["sweep_n_val"][n] = {k: a[k] for k in (
            "p50_ms", "p99_ms", "rtt_p50_ms", "rtt_p99_ms", "loss_ppm",
            "handover_loss_ppm", "handovers_per_h", "regret_mean_ms", "cell_layer_share")}
        print("n_val", n, out["sweep_n_val"][n], flush=True)
    for pol in "CD":
        a, _ = run_policy(pol, seeds, duration_s=dur, radio_ho_ms=30.0, drive_frac=1.0)
        out["legacy_radio_ho"][pol] = {k: a[k] for k in ("p99_ms", "loss_ppm", "handover_loss_ppm")}
        print("legacy radio HO, driving", pol, out["legacy_radio_ho"][pol], flush=True)
    with open(os.path.join(RES, "handover.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        names = {"A": "A no shadow", "B": "B shadow, cut", "C": "C shadow, scheduled + overlap",
                 "D": "D render-hot dual stream"}
        for pol, lat in cdfs.items():
            ys = [1 - (i + 0.5) / len(lat) for i in range(len(lat))]
            ax.semilogy(lat, ys, label=names[pol])
        ax.axvline(30, ls="--", c="k", lw=0.8)
        ax.set_xlabel("input to photon, ms")
        ax.set_ylabel("1 - CDF")
        ax.set_xlim(8, 40)
        ax.set_ylim(1e-4, 1)
        ax.legend()
        ax.set_title("Leaf moving through a 40 km city, 24 validators")
        fig.tight_layout()
        fig.savefig(os.path.join(RES, "handover_latency_ccdf.png"), dpi=120)
    except Exception as e:  # the plot is optional
        print("plot skipped:", e)


if __name__ == "__main__":
    main()
