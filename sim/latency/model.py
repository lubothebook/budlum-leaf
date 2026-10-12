#!/usr/bin/env python3
"""model.py: input-to-photon latency model of the Budlum Leaf L.6.0.

Part 21, Section 21.5.7. Gate DST-11.

Every sample is one new action. The chain runs in absolute time (ms):
touch -> air uplink -> network up -> execute and render -> first-slice
encode -> network down -> air downlink -> first-slice decode -> beam-raced
scan-out and micro-LED response. Absolute time matters: the phase of the
5G TDD frame at the downlink is set by the real delays before it, and the
scan-out phase is free-running against everything else.

All times are in milliseconds. All parameters are [HYPOTHESIS] values from
the 3GPP and IEEE timing rules quoted in README.md, unless marked.
"""
from dataclasses import dataclass, field, replace
import numpy as np

# ----------------------------------------------------------------------------
# distributions
# ----------------------------------------------------------------------------

def gamma_mc(rng, mean, cv, n):
    """Gamma with a mean and a coefficient of variation. cv = 0 is a constant."""
    if mean <= 0:
        return np.zeros(n)
    if cv <= 0:
        return np.full(n, float(mean))
    k = 1.0 / cv ** 2
    return rng.gamma(k, mean / k, n)


def lognorm_mc(rng, mean, cv, n, size_biased=False):
    """Lognormal with a mean and a cv. size_biased returns the length-biased law."""
    s2 = np.log(1.0 + cv ** 2)
    mu = np.log(mean) - s2 / 2.0
    if size_biased:  # the interval you land in is length-biased: mu + s2
        mu = mu + s2
    return rng.lognormal(mu, np.sqrt(s2), n)


# ----------------------------------------------------------------------------
# stage parameters
# ----------------------------------------------------------------------------

@dataclass
class Touch:
    hz: float = 480.0          # [DECISION] Part 21 touch scan
    proc_ms: float = 0.75      # controller: AFE settle, centroid, filter, report to U1
    proc_cv: float = 0.15
    u1_ms: float = 0.05        # U1 packs the event for U2A or U5


@dataclass
class WifiLink:
    busy: float = 0.30         # probability the link is busy when the frame arrives
    other_ppdu_ms: float = 1.0 # mean airtime of the frame that holds the medium
    other_ppdu_cv: float = 1.0
    other_ppdu_max: float = 5.484  # 802.11 aPPDUMaxTime
    aifs_ms: float = 0.034     # AC_VO: SIFS 16 us + 2 x 9 us
    cwmin: int = 3             # AC_VO
    cwmax: int = 7
    slot_ms: float = 0.009
    refreeze: float = 0.10     # chance another station seizes the medium during backoff
    coll: float = 0.05         # collision probability per attempt
    per: float = 0.03          # frame error after a clean access
    max_tries: int = 7


@dataclass
class Wifi:
    links: tuple = (WifiLink(busy=0.30), WifiLink(busy=0.15))  # 5 GHz + 6 GHz MLO
    mlo: bool = True
    ul_ppdu_ms: float = 0.08   # tiny input frame: preamble + data + SIFS + BlockAck
    dl_ppdu_ms: float = 0.12   # first slice ~60 kbit at ~2 Gb/s + preamble + BA
    sta_stack_ms: float = 0.15 # U2A MAC firmware
    ap_fwd_ms: float = 0.25    # AP bridge / switch, each way
    ap_fwd_cv: float = 0.4
    ap_queue_p: float = 0.10   # AP holds other traffic in the same AC
    ap_queue_ms: float = 0.30  # mean of that queue (exponential)


@dataclass
class Nr:
    pattern: str = "DDDSU"     # [DECISION] Part 21 operator pattern, 2.5 ms
    scs_khz: float = 30.0
    s_cfg: tuple = (10, 2, 2)  # special slot: DL, gap, UL symbols
    s_pusch: bool = False      # PUSCH allowed in the UL symbols of S
    ul_minislot: int = 0       # 0 = slot PUSCH, else PUSCH length in symbols (type B)
    dl_minislot: int = 0       # 0 = slot PDSCH, else PDSCH length in symbols (type B)
    configured_grant: bool = True
    bler_ul: float = 0.10
    bler_dl: float = 0.10
    retx_factor: float = 0.2   # BLER of a retransmission = factor x first BLER (soft combining)
    max_harq: int = 4
    arq_penalty_ms: float = 8.0  # residual loss after HARQ: RLC or next-frame recovery
    n1_ms: float = 10 / 28.0   # PDSCH processing, capability 1 at 30 kHz: 10 symbols
    n2_ms: float = 12 / 28.0   # PUSCH preparation, capability 1 at 30 kHz: 12 symbols
    gnb_ms: float = 0.30       # gNB decode, schedule and encode
    gnb_cv: float = 0.2
    ue_l2_ms: float = 0.10     # U5 L2 each way
    load: float = 0.0          # cell load 0..1
    priority_qos: bool = True  # delay-critical 5QI flow
    sr_period: int = 1         # SR occasions every N PUCCH occasions (dynamic grant only)
    # handover
    ho_rate_hz: float = 0.0
    ho_int_ms: tuple = (30.0, 60.0)  # interruption range (Rel-15 hard handover)
    ho_rlf_p: float = 0.0            # handover failure -> radio link failure
    ho_rlf_ms: tuple = (100.0, 400.0)
    air_window_ms: float = 4.0       # time the action spends in the air stages
    mig_s: float = 0.5               # validator migration window after a handover
    mig_rtt_ms: float = 1.0          # extra RTT while the old validator still serves


@dataclass
class Net:
    """The network both ways, between the air and the validator."""
    kind: str = "lan"          # lan | metro_gpon | far | upf
    rtt_ms: float = 0.1
    cv: float = 0.3
    gpon_cycle_ms: float = 1.0  # GPON upstream DBA cycle (uniform wait)
    tail_ms: float = 0.1        # exponential queueing tail, mean


@dataclass
class Render:
    mean_ms: float = 4.3       # execute + render at the validator
    cv: float = 0.12
    frame_locked: bool = False # True: render waits for the validator's own 240 Hz tick
    enc_ms: float = 1.5        # first-slice encode + hash
    enc_cv: float = 0.10
    dec_ms: float = 1.5        # U6 first-slice check + decode
    dec_cv: float = 0.10


@dataclass
class Scan:
    hz: float = 240.0          # [DECISION]
    u1_compose_ms: float = 0.20  # U1 line buffer and compose
    led_ms: float = 0.05       # micro-LED rise and first PWM sub-frame
    tile_restart: bool = False # mitigation: U1 restarts the scan of the target tile
    tile_rows: int = 200
    rows: int = 3200


@dataclass
class Path:
    name: str
    air: str                   # wifi | nr
    net: Net
    wifi: Wifi = field(default_factory=Wifi)
    nr: Nr = field(default_factory=Nr)
    touch: Touch = field(default_factory=Touch)
    render: Render = field(default_factory=Render)
    scan: Scan = field(default_factory=Scan)


# ----------------------------------------------------------------------------
# touch and scan-out
# ----------------------------------------------------------------------------

def touch_stage(rng, n, p: Touch):
    T = 1000.0 / p.hz
    return rng.uniform(0, T, n) + gamma_mc(rng, p.proc_ms, p.proc_cv, n) + p.u1_ms


def scan_stage(rng, n, p: Scan):
    T = 1000.0 / p.hz
    if p.tile_restart:
        # the slice lands; U1 restarts the scan of that tile row; the changed row
        # is somewhere inside the 200 rows of the tile.
        wait = rng.uniform(0, T * p.tile_rows / p.rows, n)
    else:
        # beam-raced: the changed row is shown when the free-running beam reaches it
        wait = rng.uniform(0, T, n)
    return p.u1_compose_ms + wait + p.led_ms


def predicted_action(rng, n, path: Path):
    """U1 picks a speculative frame already in the frame store. No network."""
    pick = gamma_mc(rng, 0.20, 0.2, n)
    return touch_stage(rng, n, path.touch) + pick + scan_stage(rng, n, path.scan)


# ----------------------------------------------------------------------------
# Wi-Fi 7 MLO
# ----------------------------------------------------------------------------

def wifi_link_access(rng, n, L: WifiLink, own_ppdu_ms):
    """Channel access + own PPDU on one link, EDCA AC_VO, with retries."""
    t = np.zeros(n)
    busy = rng.random(n) < L.busy
    resid = rng.random(n) * np.minimum(
        lognorm_mc(rng, L.other_ppdu_ms, L.other_ppdu_cv, n, size_biased=True),
        L.other_ppdu_max)
    t += busy * resid
    active = np.ones(n, bool)
    cw = L.cwmin
    for k in range(L.max_tries):
        m = active.sum()
        if m == 0:
            break
        idx = np.nonzero(active)[0]
        bo = rng.integers(0, cw + 1, m) * L.slot_ms + L.aifs_ms
        frz = rng.random(m) < L.refreeze
        bo += frz * (rng.random(m) * np.minimum(
            lognorm_mc(rng, L.other_ppdu_ms, L.other_ppdu_cv, m, True), L.other_ppdu_max))
        t[idx] += bo + own_ppdu_ms
        fail = rng.random(m) < 1 - (1 - L.coll) * (1 - L.per)
        t[idx[fail]] += 0.05  # BlockAck timeout
        active[idx[~fail]] = False
        cw = min(2 * cw + 1, L.cwmax)
    return t


def wifi_air(rng, n, w: Wifi, uplink: bool):
    own = w.ul_ppdu_ms if uplink else w.dl_ppdu_ms
    links = w.links if w.mlo else w.links[:1]
    acc = np.min(np.vstack([wifi_link_access(rng, n, L, own) for L in links]), axis=0)
    fwd = lognorm_mc(rng, w.ap_fwd_ms, w.ap_fwd_cv, n)
    if uplink:
        return w.sta_stack_ms + acc + fwd
    q = (rng.random(n) < w.ap_queue_p) * rng.exponential(w.ap_queue_ms, n)
    return fwd + q + acc + w.sta_stack_ms


# ----------------------------------------------------------------------------
# 5G NR TDD
# ----------------------------------------------------------------------------

class Ops:
    """Periodic transmission opportunities: next start >= t, and its length."""

    def __init__(self, items, P):
        items = sorted(items)
        if not items:
            raise ValueError("no opportunities in the pattern")
        s = np.array([a for a, _ in items])
        d = np.array([b for _, b in items])
        self.s = np.r_[s, s[0] + P]
        self.d = np.r_[d, d[0]]
        self.P = P

    def next(self, t):
        ph = np.mod(t, self.P)
        i = np.searchsorted(self.s, ph - 1e-9, "left")
        return t - ph + self.s[i], self.d[i]


def tdd_ops(nr: Nr):
    slot = 15.0 / nr.scs_khz
    sym = slot / 14.0
    P = len(nr.pattern) * slot
    sdl, sgap, sul = nr.s_cfg
    dl, ul, pdcch, pucch = [], [], [], []
    for i, c in enumerate(nr.pattern):
        t0 = i * slot
        if c == "D":
            if nr.dl_minislot:
                L = nr.dl_minislot
                for k in range(2, 14 - L + 1, 2):  # after the 2-symbol CORESET
                    dl.append((t0 + k * sym, L * sym))
            else:
                dl.append((t0, slot))
            pdcch.append((t0, 2 * sym))
        elif c == "U":
            if nr.ul_minislot:
                L = nr.ul_minislot
                for k in range(0, 12 - L + 1, L):
                    ul.append((t0 + k * sym, L * sym))
            else:
                ul.append((t0, slot))
            pucch.append((t0 + 12 * sym, 2 * sym))
        elif c == "S":
            dl.append((t0, sdl * sym))
            pdcch.append((t0, 2 * sym))
            if sul > 0:
                pucch.append((t0 + (14 - sul) * sym, sul * sym))
                if nr.s_pusch:
                    ul.append((t0 + (14 - sul) * sym, sul * sym))
    return dict(P=P, slot=slot, dl=Ops(dl, P), ul=Ops(ul, P),
                pdcch=Ops(pdcch, P), pucch=Ops(pucch, P))


def _defer(rng, ops, s, d, p):
    """Skip a geometric number of opportunities (load). p = chance an op is taken."""
    if p <= 0:
        return s, d
    k = rng.geometric(1 - p, s.size) - 1
    k = np.minimum(k, 200)
    for j in range(int(k.max()) if k.size else 0):
        m = k > j
        s2, d2 = ops.next(s[m] + 1e-6)
        s[m], d[m] = s2, d2
    return s, d


def _harq(rng, n, first_bler, nr: Nr):
    """Number of transmissions per sample (1..max_harq) and residual failure."""
    ntx = np.ones(n, int)
    alive = rng.random(n) < first_bler
    b = first_bler * nr.retx_factor
    for k in range(1, nr.max_harq):
        ntx[alive] += 1
        alive = alive & (rng.random(n) < b)
    return ntx, alive


def nr_uplink(rng, t, nr: Nr, ops):
    """t: absolute time the event is ready in U5. Returns time it leaves the gNB."""
    n = t.size
    load = nr.load * (0.1 if nr.priority_qos else 1.0)
    t = t + nr.ue_l2_ms
    if nr.configured_grant:
        s, d = ops["ul"].next(t + nr.n2_ms)
    else:
        # scheduling request -> grant -> PUSCH
        s, d = ops["pucch"].next(t)
        for _ in range(nr.sr_period - 1):
            m = rng.random(n) < 0.5
            s2, d2 = ops["pucch"].next(s[m] + 1e-6)
            s[m], d[m] = s2, d2
        rx = s + d + gamma_mc(rng, nr.gnb_ms, nr.gnb_cv, n)
        gs, gd = ops["pdcch"].next(rx)
        gs, gd = _defer(rng, ops["pdcch"], gs, gd, load)
        # a BSR round follows when the first grant is too small (loaded cells)
        s, d = ops["ul"].next(gs + gd + nr.n2_ms)
    end = s + d
    ntx, lost = _harq(rng, n, nr.bler_ul, nr)
    for k in range(1, nr.max_harq):
        m = ntx > k
        if not m.any():
            break
        rx = end[m] + gamma_mc(rng, nr.gnb_ms, nr.gnb_cv, m.sum())
        gs, gd = ops["pdcch"].next(rx)
        s, d = ops["ul"].next(gs + gd + nr.n2_ms)
        end[m] = s + d
    end = end + lost * nr.arq_penalty_ms
    return end + gamma_mc(rng, nr.gnb_ms, nr.gnb_cv, n)


def nr_downlink(rng, t, nr: Nr, ops):
    """t: absolute time the slice reaches the gNB. Returns time U5 hands it to U6."""
    n = t.size
    load = nr.load * (0.1 if nr.priority_qos else 1.0)
    ready = t + gamma_mc(rng, nr.gnb_ms, nr.gnb_cv, n)
    s, d = ops["dl"].next(ready)
    s, d = _defer(rng, ops["dl"], s, d, load)
    end = s + d
    ntx, lost = _harq(rng, n, nr.bler_dl, nr)
    for k in range(1, nr.max_harq):
        m = ntx > k
        if not m.any():
            break
        ack_s, ack_d = ops["pucch"].next(end[m] + nr.n1_ms)
        rx = ack_s + ack_d + gamma_mc(rng, nr.gnb_ms, nr.gnb_cv, m.sum())
        s, d = ops["dl"].next(rx)
        end[m] = s + d
    end = end + lost * nr.arq_penalty_ms
    return end + nr.n1_ms + nr.ue_l2_ms


def handover_extra(rng, n, nr: Nr):
    """Extra delay from handover interruptions and validator migration."""
    extra = np.zeros(n)
    rnet = np.zeros(n)
    if nr.ho_rate_hz <= 0:
        return extra, rnet
    lam = nr.ho_rate_hz / 1000.0  # per ms
    D = rng.uniform(*nr.ho_int_ms, n)
    rlf = rng.random(n) < nr.ho_rlf_p
    D = np.where(rlf, rng.uniform(*nr.ho_rlf_ms, n), D)
    u = rng.random(n)
    p_before = lam * D               # the action starts inside a gap
    p_during = lam * nr.air_window_ms  # a gap opens while it is in the air
    hit_b = u < p_before
    hit_d = (u >= p_before) & (u < p_before + p_during)
    extra += hit_b * rng.uniform(0, 1, n) * D + hit_d * D
    mig = rng.random(n) < nr.ho_rate_hz * nr.mig_s
    rnet += mig * nr.mig_rtt_ms
    return extra, rnet


# ----------------------------------------------------------------------------
# network
# ----------------------------------------------------------------------------

def net_oneway(rng, n, net: Net, up: bool):
    half = net.rtt_ms / 2.0
    if net.kind == "metro_gpon":
        # fixed fibre + routers each way, GPON upstream DBA wait on the way up,
        # an exponential queueing tail each way. Mean RTT = net.rtt_ms.
        fixed = max(net.rtt_ms - net.gpon_cycle_ms / 2.0 - 2 * net.tail_ms, 0.0) / 2.0
        x = gamma_mc(rng, fixed, net.cv, n) + rng.exponential(net.tail_ms, n)
        if up:
            x += rng.uniform(0, net.gpon_cycle_ms, n)
        return x
    if net.kind == "far":
        # long-haul: fixed propagation + exponential-like jitter, mean RTT = net.rtt_ms
        return half - 1.0 - net.tail_ms + gamma_mc(rng, 1.0, 1.0, n) + rng.exponential(net.tail_ms, n)
    return gamma_mc(rng, half, net.cv, n)


# ----------------------------------------------------------------------------
# the chain
# ----------------------------------------------------------------------------

STAGES = ["touch", "air_up", "net", "render", "encode", "air_down", "decode", "scan"]


def simulate(path: Path, n: int, seed: int = 1):
    rng = np.random.default_rng(seed)
    st = {}
    t0 = rng.uniform(0, 1000.0, n)  # absolute time of the touch
    t = t0 + touch_stage(rng, n, path.touch)
    st["touch"] = t - t0
    if path.air == "nr":
        ops = tdd_ops(path.nr)
        ho, rnet = handover_extra(rng, n, path.nr)
        a = t + ho
        t = nr_uplink(rng, a, path.nr, ops)
        st["air_up"] = t - (a - ho)
    else:
        rnet = np.zeros(n)
        a = t
        t = t + wifi_air(rng, n, path.wifi, True)
        st["air_up"] = t - a
    up = net_oneway(rng, n, path.net, True) + rnet / 2
    t = t + up
    a = t
    r = path.render
    if r.frame_locked:
        T = 1000.0 / 240.0
        t = t + (T - np.mod(t + rng.uniform(0, T), T))  # random validator tick phase
    t = t + lognorm_mc(rng, r.mean_ms, r.cv, n)
    st["render"] = t - a
    a = t
    t = t + gamma_mc(rng, r.enc_ms, r.enc_cv, n)
    st["encode"] = t - a
    dn = net_oneway(rng, n, path.net, False) + rnet / 2
    st["net"] = up + dn
    t = t + dn
    a = t
    if path.air == "nr":
        t = nr_downlink(rng, t, path.nr, ops)
    else:
        t = t + wifi_air(rng, n, path.wifi, False)
    st["air_down"] = t - a
    a = t
    t = t + gamma_mc(rng, r.dec_ms, r.dec_cv, n)
    st["decode"] = t - a
    a = t
    t = t + scan_stage(rng, n, path.scan)
    st["scan"] = t - a
    return t - t0, st


def stats(x):
    q = np.percentile(x, [50, 90, 99, 99.9])
    return dict(mean=float(x.mean()), p50=float(q[0]), p90=float(q[1]),
                p99=float(q[2]), p999=float(q[3]), max=float(x.max()),
                frac_over_30=float((x > 30).mean()))


# ----------------------------------------------------------------------------
# the four paths of Part 21
# ----------------------------------------------------------------------------

def paths():
    return {
        "wifi_room": Path("Wi-Fi, room validator", "wifi", Net("lan", 0.1, 0.3)),
        "wifi_city": Path("Wi-Fi, city validator", "wifi",
                          Net("metro_gpon", 1.2, 0.3, gpon_cycle_ms=1.0, tail_ms=0.1)),
        "nr_cell": Path("5G SA, cell-site validator", "nr", Net("upf", 0.3, 0.3)),
        "far": Path("Far validator", "wifi", Net("far", 80.0, 0.0, tail_ms=2.0)),
    }


PART21 = {  # Section 21.5.7 table, mean of a new action and the p99 claim
    "wifi_room": dict(mean=13.6, p99=20.0, stages=[1.8, 1.0, 0.1, 4.3, 1.5, 1.0, 1.5, 2.4]),
    "wifi_city": dict(mean=14.7, p99=21.0, stages=[1.8, 1.0, 1.2, 4.3, 1.5, 1.0, 1.5, 2.4]),
    "nr_cell": dict(mean=15.4, p99=21.0, stages=[1.8, 2.3, 0.3, 4.3, 1.5, 1.3, 1.5, 2.4]),
    "far": dict(mean=93.5, p99=100.0, stages=[1.8, 1.0, 80.0, 4.3, 1.5, 1.0, 1.5, 2.4]),
}
