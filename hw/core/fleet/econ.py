#!/usr/bin/env python3
"""econ.py - the economics of a shared Core, its power, its failure and its replicas. Question 3.

The cost of a large Core (array, silicon, validator hardware, site), the cost per Leaf served at
several fleet sizes, the unit costs that gate SW-19 asks for (H-15 of Part 15), and the failure and
power of a Core site. The price of a session is deferred by Ayaz (FINAL/17 17.14), so this file gives
costs and break-even prices, never a price.

Read only: program/budget.py (the Leaf unit cost), hw/dock (the validator module cost and power),
hw/hostpower/continuity (shadow takeover, the dock pair), fleet.py of this seat (the capacity).
Every cost is a [HYPOTHESIS] with a low, a base and a high value, except where a line says [PUBLICATION].

Run:   python3 econ.py        Out: out/econ.txt, out/econ.json
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

ROOT, OUT = F.ROOT, F.OUT
PB = F.load_module("program_budget", os.path.join(ROOT, "program", "budget.py"))

# --------------------------------------------------------------------------- the cost parameters, USD
# name: (low, base, high, note)
COST = dict(
    elem_usd=(100.0, 170.0, 300.0, "per array element with PA, filter, antenna, calibration. A 64T64R AAU is about USD 10 to 20 k: no public price"),
    radio_other=(15e3, 30e3, 60e3, "precoder and fronthaul processing of a large array, per sector"),
    server=(30e3, 45e3, 70e3, "two 96-core CPUs, 1 TB RAM, 100 GbE"),
    engine_card=(3e3, 5.2e3, 9e3, "a KU15P-class frame engine card; the chip alone is USD 2600 [TREE] hw/dock"),
    ma35d=(1200.0, 1595.0, 2500.0, "[PUBLICATION] AMD Alveo MA35D launch price USD 1595; 8 x 4Kp60 per card"),
    hsm=(4e3, 8e3, 15e3, "a PKCS#11 signer for the validator key"),
    site_build=(30e3, 60e3, 120e3, "mast or roof, install, permits, cabling, cooling"),
    backhaul_capex=(5e3, 15e3, 40e3, "a fibre drop"),
    ups_usd_kwh=(300.0, 450.0, 700.0, "Li-ion storage with inverter"),
    rent=(6e3, 12e3, 30e3, "per site-year"),
    backhaul_opex=(5e3, 15e3, 40e3, "per site-year"),
    noc=(3e3, 8e3, 20e3, "network operations per site-year"),
    kwh=(0.08, 0.12, 0.20, "USD per kWh"),
    maint=(0.05, 0.08, 0.12, "share of capex per year"),
    spectrum=(0.0, 0.0, 100e3, "per site-year. UNKNOWN: the base case excludes it. A licence or a private band changes the answer"),
)
WACC = 0.10
LIFE_PASSIVE, LIFE_COMPUTE = 7, 4
HOURS_YEAR = 8760.0


def crf(n, r=WACC):
    return r / (1 - (1 + r) ** -n)


def pick(k, which):
    lo, ba, hi, _ = COST[k]
    return {"low": lo, "base": ba, "high": hi}[which] if isinstance(which, str) else which[k]


def compute_bill(p, n_reg, radius_m=1000.0):
    """Right-size the compute for n_reg registered Leafs at the peak mix. The reference box of fleet.py is one server, four frame
    engines, four MA35D encoders and one signer. Each device type is bought on its own limit."""
    m = F.mix_by_limit(dict(p, c2_radius_m=radius_m), "C2")
    per_server = min(m["compute.cpu"], m["compute.dram"], m["memnet.ram"], m["memnet.nic"], m["memnet.wan"])
    per_engine = m["compute.engine"] / 4.0
    per_enc = min(m["compute.enc"], m["compute.dec"]) / 4.0
    per_hsm = m["compute.sign"]
    bill = dict(servers=max(1, math.ceil(n_reg / per_server)), engines=max(1, math.ceil(n_reg / per_engine)),
                encoders=max(1, math.ceil(n_reg / per_enc)), hsms=max(1, math.ceil(n_reg / per_hsm)))
    bill["wall"] = min((("cpu/ram/net", per_server), ("engine", per_engine), ("encoder", per_enc), ("signer", per_hsm)), key=lambda kv: kv[1])[0]
    return bill


def site_cost(c, sectors=3, bill=None, n_elem=256, p_rf_w=100.0, ups_h=4.0, load_factor=0.7):
    """Capex, annual cost and power of one C2 site: `sectors` arrays, a compute bill, a UPS of `ups_h` hours."""
    bill = bill or dict(servers=1, engines=4, encoders=4, hsms=1)
    array = sectors * (n_elem * c["elem_usd"] + c["radio_other"])
    box = c["server"] + 4 * c["engine_card"] + 4 * c["ma35d"] + c["hsm"]
    compute = bill["servers"] * c["server"] + bill["engines"] * c["engine_card"] + bill["encoders"] * c["ma35d"] + bill["hsms"] * c["hsm"]
    # power, watts: arrays = PA at 35 % plus 2 W per element of digital and LNA; devices from fleet.CORES and the MA35D
    p_array = sectors * (p_rf_w / 0.35 + 2.0 * n_elem)
    p_box = bill["servers"] * 900.0 + bill["engines"] * 40.0 + bill["encoders"] * 35.0 + bill["hsms"] * 20.0
    p_site_peak = p_array + p_box
    p_site_avg = p_site_peak * load_factor
    ups = ups_h * p_site_peak / 1000.0 * c["ups_usd_kwh"] + 5e3
    capex_compute = compute
    capex_passive = array + c["site_build"] + c["backhaul_capex"] + ups
    ann_capex = capex_compute * crf(LIFE_COMPUTE) + capex_passive * crf(LIFE_PASSIVE)
    energy = p_site_avg * 1.3 / 1000.0 * HOURS_YEAR * c["kwh"]            # PUE 1.3 on the average
    opex = c["rent"] + c["backhaul_opex"] + c["noc"] + c["spectrum"] + energy + c["maint"] * (capex_compute + capex_passive)
    return dict(array=array, box=box, bill=bill, capex_compute=capex_compute, capex_passive=capex_passive,
                capex=capex_compute + capex_passive, ups=ups, ann_capex=ann_capex, energy_usd=energy, opex=opex,
                annual=ann_capex + opex, p_peak_kw=p_site_peak / 1000.0, p_avg_kw=p_site_peak * load_factor / 1000.0,
                p_array_kw=p_array / 1000.0, p_box_kw=p_box / 1000.0)


def capacity_at(p, radius_m, sectors, cost_c):
    """Registered Leafs one site carries at the peak mix: the radio of `sectors` arrays, the compute right-sized to it."""
    q = dict(p, c2_radius_m=radius_m)
    m = F.n_mix(q, "C2")
    radio = m["groups"]["radio"]
    n_site = sectors * radio
    bill = compute_bill(p, n_site, radius_m)
    delta = F.n_for(q, "delta", "C2")
    video = F.n_for(q, "video", "C2")
    return dict(n=n_site, radio_sector=radio, bill=bill, radio_bind=m["group_bind"]["radio"],
                delta_sessions=sectors * delta["groups"]["radio"], video_sessions=sectors * video["groups"]["radio"],
                delta_cov=F.covered(delta["detail"]))


def main():
    L = []

    def pr(s=""):
        L.append(s)
        print(s)

    p = dict(F.BASE)
    out = {}
    pr("FLEET seat · economics of a shared Core · every figure is a [HYPOTHESIS] unless tagged. Spectrum and stake are excluded (UNKNOWN).")
    pr("")
    # ------------------------------------------------------------------ 1 the site
    pr("1 · the cost of a C2 site: 3 sectors of 256 elements, 100 W each, one reference compute box, a 4 h UPS")
    pr("  %-26s %12s %12s %12s" % ("line", "low", "base", "high"))
    sites = {w: site_cost({k: pick(k, w) for k in COST}) for w in ("low", "base", "high")}
    out["site"] = sites
    for k, lab in (("array", "arrays"), ("capex_compute", "compute box (server, 4 engines, 4 MA35D, HSM)"),
                   ("capex_passive", "arrays, build, backhaul, UPS"), ("capex", "capex"),
                   ("ann_capex", "annualised capex"), ("opex", "opex per year"), ("annual", "annual cost")):
        pr("  %-26s %12s %12s %12s" % (lab[:26], *["%.0f" % sites[w][k] for w in ("low", "base", "high")]))
    pr("  the reference box alone: %.0f / %.0f / %.0f USD. The silicon that the Leaf also carries is not in this table." % (
        sites["low"]["box"], sites["base"]["box"], sites["high"]["box"]))
    pr("  power: arrays %.2f kW, compute box %.2f kW, peak %.2f kW, average %.2f kW; energy %.0f USD per year at the base." % (
        sites["base"]["p_array_kw"], sites["base"]["p_box_kw"], sites["base"]["p_peak_kw"], sites["base"]["p_avg_kw"],
        sites["base"]["energy_usd"]))
    pr("  a 64T64R AAU draws about 1 kW [PUBLICATION, inferred from a 3 kW three-sector site of China Mobile]; this model gives %.2f kW per 256-element sector." % (
        sites["base"]["p_array_kw"] / 3))
    pr("")

    # ------------------------------------------------------------------ 2 leafs per site
    cb = {k: pick(k, "base") for k in COST}
    pr("2 · registered Leafs per site at the peak mix, and the cost per Leaf, capacity bound (a city dense enough that capacity, not coverage, sets the sites)")
    pr("  The compute is right-sized: each device type is bought on its own limit (servers, frame engines, MA35D encoders, signers).")
    pr("  %6s %7s %10s %8s %26s %9s %10s %10s" % ("radius", "sectors", "Leafs/site", "radio", "servers/engines/enc/hsm", "delta ses", "USD/Leaf-yr", "USD/Leaf-mo"))
    cap = {}
    for rkm in (0.5, 1.0, 2.0):
        for sec in (1, 3):
            cp = capacity_at(p, rkm * 1000.0, sec, cb)
            sc = site_cost(cb, sectors=sec, bill=cp["bill"])
            per_leaf = sc["annual"] / cp["n"]
            cap["r%.1f_s%d" % (rkm, sec)] = dict(cp, annual=sc["annual"], p_peak_kw=sc["p_peak_kw"], usd_leaf_year=per_leaf, usd_leaf_month=per_leaf / 12)
            b_ = cp["bill"]
            pr("  %6.1f %7d %10.0f %8s %26s %9.0f %10.1f %10.2f" % (
                rkm, sec, cp["n"], cp["radio_bind"][6:], "%d / %d / %d / %d" % (b_["servers"], b_["engines"], b_["encoders"], b_["hsms"]),
                cp["delta_sessions"], per_leaf, per_leaf / 12))
    out["capacity"] = cap
    pr("  Leafs per site count the registered Leafs at the 15 percent session peak of net/discovery/density.py.")
    pr("")

    # ------------------------------------------------------------------ 3 fleet sizes
    pr("3 · the cost per Leaf by fleet size. A metro of 400 km2 (20 x 20 km), the Leafs spread evenly. Sector radius 1 km, 3 sectors.")
    pr("  A site must cover the area (coverage) and carry the Leafs (capacity). Replicas: R sites reach every point, none above (R-1)/R of its capacity.")
    cp1 = capacity_at(p, 1000.0, 3, cb)
    area = 400.0
    cov_km2 = math.pi * 1.0 ** 2                      # one site, 3 sectors of 1 km radius
    pr("  one site covers %.1f km2 and carries %.0f registered Leafs; the capacity at the peak is %.0f Leafs per km2 of cover." % (
        cov_km2, cp1["n"], cp1["n"] / cov_km2))
    pr("  A coverage-bound site below the capacity bound holds the smallest compute (1 server, 1 engine, 1 encoder, 1 signer): the cost per Leaf then falls with the fleet.")
    pr("  %10s %9s | %-33s | %-33s" % ("Leafs", "per km2", "R = 1: sites, USD/Leaf-month", "R = 2: sites, USD/Leaf-month"))
    sweep = {}
    sc1 = site_cost(cb, sectors=3, bill=cp1["bill"])
    for n in (1e3, 1e4, 1e5, 1e6, 1e7):
        row = {}
        cells = []
        for r in (1, 2):
            cover = r * 1.2 * area / cov_km2
            capn = n / (cp1["n"] * (r - 1) / r if r > 1 else cp1["n"])
            sites_n = max(cover, capn)
            # sites below the capacity bound still hold a compute box each
            sc_small = site_cost(cb, sectors=3, bill=compute_bill(p, min(n / sites_n, cp1["n"]), 1000.0))
            usd = sites_n * (sc1["annual"] if capn >= cover else sc_small["annual"]) / n / 12
            row["R%d" % r] = dict(sites=sites_n, usd_leaf_month=usd, bound="coverage" if cover >= capn else "capacity")
            cells.append("%7.0f sites, %10.2f  %s" % (sites_n, usd, "cov" if cover >= capn else "cap"))
        sweep["%d" % n] = row
        pr("  %10.0f %9.1f | %-33s | %-33s" % (n, n / area, cells[0], cells[1]))
    out["fleet_sizes"] = sweep
    pr("  cov = coverage bound, cap = capacity bound. Below about %.0f Leafs in the metro the coverage sets the cost." % (
        1.2 * area / cov_km2 * cp1["n"]))
    pr("")

    # ------------------------------------------------------------------ 4 the unit costs of SW-19
    pr("4 · the unit cost of each network function, per session-hour, capacity bound, base case (gate SW-19)")
    pr("  one site of 3 sectors at 1 km, compute right-sized: %d servers, %d engines, %d encoders, %d signers." % (
        cp1["bill"]["servers"], cp1["bill"]["engines"], cp1["bill"]["encoders"], cp1["bill"]["hsms"]))
    sc = sc1
    cp = cp1
    cat = dict(
        array=3 * (256 * cb["elem_usd"] + cb["radio_other"]) * crf(LIFE_PASSIVE) * (1 + cb["maint"] / crf(LIFE_PASSIVE)),
        compute=sc["capex_compute"] * crf(LIFE_COMPUTE) + cb["maint"] * sc["capex_compute"],
        site=(cb["site_build"] + cb["backhaul_capex"] + sc["ups"]) * crf(LIFE_PASSIVE) + cb["maint"] * (cb["site_build"] + cb["backhaul_capex"] + sc["ups"])
        + cb["rent"] + cb["noc"],
        backhaul=cb["backhaul_opex"], power=sc["energy_usd"])
    tot = sum(cat.values())
    pr("  annual cost %.0f USD per site (the categories sum to %.0f; the table above adds a spectrum line of 0)" % (sc["annual"], tot))
    sessions = {"delta": cp["delta_sessions"], "video": cp["video_sessions"]}
    pr("  %-10s %9s | %s" % ("function", "USD/year", "USD per delta session-hour at 10 / 25 / 50 % utilisation"))
    unit = {}
    for k, v in cat.items():
        vals = [v / (sessions["delta"] * HOURS_YEAR * u) for u in (0.10, 0.25, 0.50)]
        unit[k] = dict(usd_year=v, delta=vals)
        pr("  %-10s %9.0f | %8.4f %8.4f %8.4f" % (k, v, *vals))
    allv = [sc["annual"] / (sessions["delta"] * HOURS_YEAR * u) for u in (0.10, 0.25, 0.50)]
    allvv = [sc["annual"] / (sessions["video"] * HOURS_YEAR * u) for u in (0.10, 0.25, 0.50)]
    pr("  %-10s %9.0f | %8.4f %8.4f %8.4f" % ("all, delta", sc["annual"], *allv))
    pr("  %-10s %9.0f | %8.4f %8.4f %8.4f   (%.0f video sessions per site)" % ("all, video", sc["annual"], *allvv, sessions["video"]))
    unit["all_delta"] = allv
    unit["all_video"] = allvv
    out["unit"] = unit
    gb_delta, gb_video = 2.0e6 / 8 * 3600 / 1e9, 30.0e6 / 8 * 3600 / 1e9
    pr("  The meter of H-15 counts bytes of the class: a delta session hour is %.2f GB down, a video session hour %.1f GB." % (gb_delta, gb_video))
    pr("  Cost per GB at 25 %% utilisation: delta %.3f USD, video %.3f USD. Per session minute: delta %.4f USD, video %.4f USD." % (
        allv[1] / gb_delta, allvv[1] / gb_video, allv[1] / 60, allvv[1] / 60))
    unit["gb"] = dict(delta_usd_gb=allv[1] / gb_delta, video_usd_gb=allvv[1] / gb_video)
    pr("  The session price is deferred by Ayaz. These are the costs the price must cover. A 20 percent margin raises each by 25 percent.")
    pr("")

    # ------------------------------------------------------------------ 5 the three classes
    pr("5 · the cost per Leaf-year at C0, C1 and C2 (the Core part only; the Leaf is the same Leaf)")
    leaf_unit = PB.unit_cost()[1_000_000]["base"]["total"]
    pr("  the L.6.0 Leaf, unit cost at 1 M a year, base: %.0f USD; over 4 years %.0f USD per year [TREE] program/budget.py" % (leaf_unit, leaf_unit / 4))
    room_core = 1000 + 2600 + 150 + 200 + 50          # AGX Orin, KU15P chip, Wi-Fi 7 AP, enclosure and PSU, HSM [HYPOTHESIS]
    dock_core = 700 + 2600 + 100 + 150 + 50           # Orin NX, KU15P chip: the hw/dock pick
    pr("  %-34s %9s %9s %9s" % ("case", "Core USD", "Leafs", "USD/Leaf-yr"))
    cls = {}
    for lab, usd, n, life in (("C0 dock Core, 1 Leaf on the pad", dock_core, 1, 5), ("C0 dock Core, 2 pads", dock_core, 2, 5),
                              ("C1 room Core, 1 Leaf", room_core, 1, 5), ("C1 room Core, 3 Leafs", room_core, 3, 5),
                              ("C1 room Core, 6 Leafs", room_core, 6, 5)):
        y = usd * crf(life) / n
        cls[lab] = dict(usd=usd, leafs=n, usd_leaf_year=y)
        pr("  %-34s %9.0f %9d %9.1f" % (lab, usd, n, y))
    c2 = cap["r1.0_s3"]
    pr("  %-34s %9.0f %9.0f %9.1f   (annual cost incl. opex, capacity bound)" % (
        "C2 site, 3 sectors at 1 km", sc1["capex"], c2["n"], c2["usd_leaf_year"]))
    cls["C2 site"] = dict(usd=sc1["capex"], leafs=c2["n"], usd_leaf_year=c2["usd_leaf_year"])
    out["classes"] = cls
    pr("  The Core part of a room costs %.0f to %.0f USD per Leaf-year; a shared site costs %.0f. The Leaf keeps its silicon in all three." % (
        cls["C1 room Core, 6 Leafs"]["usd_leaf_year"], cls["C1 room Core, 1 Leaf"]["usd_leaf_year"], c2["usd_leaf_year"]))
    pr("")

    # ------------------------------------------------------------------ 6 Monte Carlo of the cost per Leaf
    pr("6 · the Monte Carlo: cost per registered Leaf-month at the capacity bound, 3 sectors, 1 km. 300 draws over the cost and the capacity ranges.")
    rng = np.random.default_rng(11)
    vals, bind = [], {}
    for _ in range(300):
        c = {k: float(rng.uniform(COST[k][0], COST[k][2])) for k in COST if k != "spectrum"}
        c["spectrum"] = 0.0
        q = F.draw(rng, F.BASE)
        cp_ = capacity_at(q, 1000.0, 3, c)
        sc_ = site_cost(c, sectors=3, bill=cp_["bill"])
        vals.append(sc_["annual"] / cp_["n"] / 12)
        bind[cp_["radio_bind"]] = bind.get(cp_["radio_bind"], 0) + 1
    v = np.array(vals)
    mc = dict(p10=float(np.percentile(v, 10)), p50=float(np.percentile(v, 50)), p90=float(np.percentile(v, 90)))
    out["mc_cost_leaf_month"] = mc
    pr("  USD per Leaf-month: p10 %.2f, p50 %.2f, p90 %.2f. Binding radio limit: %s" % (
        mc["p10"], mc["p50"], mc["p90"], ", ".join("%s %.0f%%" % (k, 100 * n / 300) for k, n in sorted(bind.items(), key=lambda kv: -kv[1]))))
    pr("")

    # ------------------------------------------------------------------ 7 failure, power, replicas
    pr("7 · the failure and the power of a Core site, and the replica count")
    pr("  rates [HYPOTHESIS]: radio and array 1 per 80 000 h, compute box 1 per 40 000 h, site power 1 per 100 000 h, repair 6 h by a truck.")
    lam_hw = 1 / 80000 + 1 / 40000 + 1 / 100000
    repair_h = 6.0
    q_hw = lam_hw * repair_h / (1 + lam_hw * repair_h)
    pr("  hardware: %.2f failures per year, %.2f h dark per year, availability %.5f" % (lam_hw * HOURS_YEAR, q_hw * HOURS_YEAR, 1 - q_hw))
    pr("  grid: outages per year and mean length are the unknown. Rows: the UPS hours that survive the outage law.")
    pr("  %-26s %9s %9s %9s %9s" % ("grid (per year, mean h)", "UPS 1 h", "UPS 4 h", "UPS 8 h", "UPS 24 h"))
    grid = {}
    for lab, n, tau in (("good, 0.5 per year, 1 h", 0.5, 1.0), ("fair, 3 per year, 1.5 h", 3.0, 1.5), ("poor, 12 per year, 3 h", 12.0, 3.0)):
        row = []
        for u in (1, 4, 8, 24):
            dark_events = n * math.exp(-u / tau)
            dark_h = dark_events * tau                  # memoryless: the mean excess after the UPS ends is tau
            row.append((dark_events, dark_h))
        grid[lab] = row
        pr("  %-26s " % lab + " ".join("%4.2f ev %4.1fh" % r for r in row))
    pr("  cells: dark events per year and dark hours per year of the site. UPS cost at 4 h: %.0f USD, 8 h: %.0f USD at the base." % (
        site_cost(cb, ups_h=4.0)["ups"], site_cost(cb, ups_h=8.0)["ups"]))
    out["grid"] = {k: [list(x) for x in v_] for k, v_ in grid.items()}
    pr("  Replicas. q is the share of time that one site is dark; R sites reach the same Leaf; beta is the common cause (one feeder, one firmware).")
    q_site = q_hw + 3.0 * math.exp(-4.0 / 1.5) * 1.5 / HOURS_YEAR      # hardware plus the fair grid with a 4 h UPS
    pr("  q of one site, fair grid, 4 h UPS: %.2e (%.1f min per year)" % (q_site, q_site * 525600))
    pr("  %-3s %-9s %12s %12s %10s %14s" % ("R", "beta", "dark min/yr", "events/yr", "capacity", "USD/Leaf-mo x"))
    rep = {}
    for r in (1, 2, 3):
        for beta in (0.02, 0.3):
            u_all = q_site ** r + beta * q_site if r > 1 else q_site
            mins = u_all * 525600
            cap_f = (r - 1) / r if r > 1 else 1.0
            mult = 1.0 / cap_f if r > 1 else 1.0
            ev = r * (lam_hw * HOURS_YEAR + 3.0 * math.exp(-4.0 / 1.5)) * (q_site ** (r - 1)) * 0.0 + (
                (lam_hw * HOURS_YEAR + 3.0 * math.exp(-4.0 / 1.5)) * (beta if r > 1 else 1.0))
            rep["R%d_b%.2f" % (r, beta)] = dict(dark_min_year=mins, events_year=ev, usable_capacity=cap_f, cost_multiplier=mult)
            if r == 1 and beta != 0.02:
                continue
            pr("  %-3d %-9.2f %12.2f %12.3f %10.2f %14.2f" % (r, beta, mins, ev, cap_f, mult))
    out["replicas"] = rep
    pr("  The grid is a common cause for sites that share a feeder. With beta 0.3 a second site gains little: put the second site on another feeder.")
    pr("  What a failure does to the Leaf: the shadow takes over, 4 to 5 frames covered by U1 at p50 and p99 [TREE] hw/dock dockpair;")
    pr("  a cold start is 133 ms at p50 and 152 ms at p99. Without any Core in reach the Leaf falls back to a far validator, 93 ms RTT: the delta class holds, video does not.")
    pr("  A dock pair in one box makes the joint loss of power and primary 60 times more frequent [TREE] hw/dock: never put the shadow in the primary site.")
    pr("  Recommended: R = 2 sites reach every Leaf, on two feeders; each site holds at most 50 to 60 percent of its sessions; one spare compute box per site;")
    pr("  a UPS of 4 h on the fair grid, 8 h on the poor grid; the shadow of a session lives in the other site. The site cost rises by 2 times for the same Leafs.")
    pr("  Blast radius: one site holds %.0f registered Leafs, up to %.0f live delta sessions. One event touches all of them. [HYPOTHESIS]" % (
        cp1["n"], cp1["delta_sessions"]))
    pr("  Power of the site at capacity: %.1f kW peak, %.1f kW average. Per registered Leaf %.2f W; per live delta session %.1f W against %.2f W in the Leaf." % (
        sc1["p_peak_kw"], sc1["p_avg_kw"], sc1["p_avg_kw"] * 1000 / cp1["n"], sc1["p_peak_kw"] * 1000 / cp1["delta_sessions"], 2.19))
    out["site_power"] = dict(peak_kw=sc1["p_peak_kw"], avg_kw=sc1["p_avg_kw"], w_per_registered=sc1["p_avg_kw"] * 1000 / cp1["n"],
                             w_per_delta_session=sc1["p_peak_kw"] * 1000 / cp1["delta_sessions"])
    # ------------------------------------------------------------------ 8 the receipts: the Core as the unit of settlement
    pr("")
    pr("8 · the receipts. Part 21 has one receipt per session and second; the Core can settle them in one transaction per slot.")
    n_site = cp1["n"]
    active = n_site * (F.MIX["delta"] + F.MIX["video"])
    idle_r = n_site * F.MIX["idle"] * 0.1
    rec_s = active * 1.0 + idle_r
    naive_b = F.SIG87 + F.PK87 + 2420 + 100 + 300           # the Core wallet signature, its key, the identity attestation
    naive_ref = F.SIG87 + 2420 + 100 + 300                  # key by reference
    agg_b = F.SIG65 + 200                                   # one validator signature over the Merkle root, per slot of 6 s
    pr("  one site, %d registered Leafs at the peak mix: %.0f receipts per second (%.0f live, %.0f idle)." % (n_site, rec_s, active, idle_r))
    pr("  naive on chain: %.1f MB/s with the key inline (%d B each), %.1f MB/s with the key by reference (%d B)." % (
        rec_s * naive_b / 1e6, naive_b, rec_s * naive_ref / 1e6, naive_ref))
    pr("  aggregated by the Core: one transaction per 6 s slot of %d B, %.2f kB/s. The receipts stay with the Core and each Leaf holds its Merkle path." % (
        agg_b, agg_b / 6 / 1e3))
    pr("  the ratio is %.0f times (key inline). For 1 000 000 registered Leafs at %d per site: %.0f sites, naive %.0f GB/s, aggregated %.2f MB/s." % (
        rec_s * naive_b / (agg_b / 6), n_site, 1e6 / n_site, 1e6 / n_site * rec_s * naive_b / 1e9, 1e6 / n_site * agg_b / 6 / 1e6))
    out["receipts"] = dict(receipts_per_s=rec_s, naive_mb_s=rec_s * naive_b / 1e6, agg_kb_s=agg_b / 6 / 1e3,
                           ratio=rec_s * naive_b / (agg_b / 6))
    pr("  the aggregate needs a rule: the Leaf attestation of each second stays checkable by a challenger for the challenge period. Gate HC-C9.")
    with open(os.path.join(OUT, "econ.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    with open(os.path.join(OUT, "econ.txt"), "w") as f:
        f.write("\n".join(L) + "\n")
    return out


if __name__ == "__main__":
    main()
