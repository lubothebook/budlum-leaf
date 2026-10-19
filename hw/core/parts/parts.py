#!/usr/bin/env python3
"""parts.py - the allocation of every Leaf part under the Split, by distance class.

PARTS seat of hw/core, block HP-3. Study of revision L.7 candidate. It changes
no L.6.0 or L.6.1 decision. Every result is [HYPOTHESIS] until a gate runs.

Input : parts_data.json (authored, with a citation on every row)
        program/budget.py (read only, imported)
Output: parts_table.csv, out/parts_table.md, out/summary.txt, out/summary.json,
        out/cost.txt, out/cost.json, out/cost.md, out/service.md,
        out/collisions.md, out/gates.md, out/lanes.txt

The classes
  C0   contact or tether, up to 2 m (the maximum Split)
  C0R  C0 with the three radios kept (Ayaz named antennas and the 5G modem)
  C1   a room, up to 30 m, with the compressed stream of Part 21
  C2   far: the Skin is the L.6.0 Leaf

Run: python3 parts.py
"""
import csv
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CLASSES = ("C0", "C0R", "C1", "C2")
COUNTED = ("body", "module", "placement")      # parts that make the L.6.0 Leaf
VOLS = ("100000", "1000000", "5000000")
LMH = ("low", "base", "high")


# ------------------------------------------------------------------ load
def load():
    with open(os.path.join(HERE, "parts_data.json")) as f:
        return json.load(f)


def resolve(row, cls):
    """Return (code, fraction) of a row in a class."""
    a0, a1, a2 = row["a0"], row["a1"], row["a2"]
    f0, f1, f2 = row["f0"], row["f1"], row["f2"]
    if cls == "C0":
        return a0, f0
    if cls == "C0R":
        if row.get("radio"):
            return "S", 0.0
        return a0, f0
    if cls == "C1":
        return a1, f1
    if cls == "C2":
        return a2, f2
    raise KeyError(cls)


def moved(row, cls):
    code, f = resolve(row, cls)
    return f if code == "M" else 0.0


def verdict(row, cls, star=True):
    """The home of a part under the rule of necessity: Body, Module or Core."""
    code, f = resolve(row, cls)
    if row["g"] in ("port", "dock", "withdrawn"):
        return {"port": "port part", "dock": "dock", "withdrawn": "withdrawn"}[row["g"]]
    if code == "M" and f >= 0.999:
        v = "Core"
    elif code == "M":
        v = "Core %.0f%%" % (100 * f)
    elif code == "A":
        v = "Module (new)"
    elif code == "-":
        v = "none"
    elif row["g"] == "body":
        v = "Body"
    else:
        v = "Module"
    if star and row.get("line") and v not in ("none",):
        v += "*"
    return v


def vol_mm3(row):
    d = row.get("dim")
    if not d:
        return None
    v = d[0] * d[1] * d[2]
    return v * (row["cnt"] if row.get("dpp") else 1)


# ------------------------------------------------------------------ checks
def validate(D):
    errs = []
    ids = [r["id"] for r in D["parts"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    codes = set(D["meta"]["codes"])
    for r in D["parts"]:
        for k in ("a0", "a1", "a2"):
            if r[k] not in codes and r[k] != "-":
                errs.append("%s bad code %s" % (r["id"], r[k]))
        if not r.get("ms"):
            errs.append("%s has no citation" % r["id"])
        if r["cg"] not in D["cost_groups"]:
            errs.append("%s unknown cost group %s" % (r["id"], r["cg"]))
        if r["mb"] == "derived" and not ("lo" in r and "hi" in r):
            errs.append("%s derived mass has no range" % r["id"])
    idset = set(ids)
    cids = {c["id"] for c in D["collisions"]}
    for r in D["parts"]:
        for c in r.get("col", []):
            if c not in cids:
                errs.append("%s names unknown collision %s" % (r["id"], c))
    for c in D["collisions"]:
        for p in c["parts"]:
            if p not in idset:
                errs.append("collision %s names unknown part %s" % (c["id"], p))
    mods = [r for r in D["parts"] if r["g"] == "module" and r["id"].startswith("M")]
    if len(mods) != 32:
        errs.append("module rows: %d, expected 32 (HARDWARE/13)" % len(mods))
    msum = sum(r["m"] for r in mods)
    if abs(msum - 10.80) > 0.01:
        errs.append("module stated sum %.3f g, HARDWARE/13 states 10.80 g" % msum)
    return errs, msum


# ------------------------------------------------------------------ mass
def mass_tables(D):
    P = D["parts"]
    cnt = [r for r in P if r["g"] in COUNTED]
    body = [r for r in P if r["g"] == "body"]
    mod = [r for r in P if r["g"] in ("module", "placement")]
    res = {}
    t_body = sum(r["m"] for r in body)
    t_body_lo = sum(r.get("lo", r["m"]) for r in body)
    t_body_hi = sum(r.get("hi", r["m"]) for r in body)
    t_mod_h13 = sum(r["m"] for r in P if r["g"] == "module")
    t_mod_all = sum(r["m"] for r in mod)
    res["today"] = dict(body_derived=t_body, body_lo=t_body_lo, body_hi=t_body_hi,
                        module_H13=t_mod_h13, module_with_placement_parts=t_mod_all,
                        leaf_derived=t_body + t_mod_all, leaf_lo=t_body_lo + t_mod_all,
                        leaf_hi=t_body_hi + t_mod_all,
                        leaf_stated_68_plus_H13=68.0 + t_mod_h13,
                        leaf_stated_88=88.0)
    cells_stated = 34.4
    for cls in CLASSES:
        leave = sum(r["m"] * moved(r, cls) for r in cnt)
        leave_lo = sum(r.get("lo", r["m"]) * moved(r, cls) for r in cnt)
        leave_hi = sum(r.get("hi", r["m"]) * moved(r, cls) for r in cnt)
        added = sum(r["m"] for r in P if r["g"] == "split" and resolve(r, cls)[0] == "A")
        fcell = moved(next(r for r in P if r["id"] == "BD08"), cls)
        leave_A = sum(r["m"] * moved(r, cls) for r in mod) + cells_stated * fcell
        today = res["today"]["leaf_derived"]
        res[cls] = dict(leaves_g=leave, leaves_lo=leave_lo, leaves_hi=leave_hi, added_g=added,
                        skin_g=today - leave + added, share_leaving=leave / today,
                        stays_g=today - leave,
                        basis_A_leaves_g=leave_A,
                        basis_A_skin_g=68.0 + t_mod_h13 - leave_A + added,
                        basis_A_share=leave_A / (68.0 + t_mod_h13))
    # module only
    for cls in CLASSES:
        m_leave = sum(r["m"] * moved(r, cls) for r in P if r["g"] in ("module", "placement"))
        m_add = sum(r["m"] for r in P if r["g"] == "split" and resolve(r, cls)[0] == "A")
        res[cls]["module_leaves_g"] = m_leave
        res[cls]["module_after_g"] = t_mod_all - m_leave + m_add
    return res


# ------------------------------------------------------------------ volume
def volume_tables(D):
    P = D["parts"]
    r = {}
    ring_env = 3.141592653589793 * 16.0 ** 2 * 4.00
    layer_env = 3.141592653589793 * 14.75 ** 2 * 2.30      # above the board, PL STACK
    cell_vol_body = 9.25 * 9.25 * 0.90                       # mm3 per cell, CS
    r["ring_envelope_mm3"] = ring_env
    r["ring_layer_above_board_mm3"] = layer_env
    r["b_cell_mm3"] = 20.0 * 8.0 * 1.5
    r["bar_envelope_mm3"] = 32.0 * 4.0 * 1.0
    r["body_cell_layer_mm3_each"] = cell_vol_body
    r["body_cell_layer_mm3_all"] = 128 * cell_vol_body
    r["classes"] = {}
    for cls in CLASSES:
        v = 0.0
        items = []
        for row in P:
            if row["g"] not in ("module", "placement"):
                continue
            f = moved(row, cls)
            vv = vol_mm3(row)
            if f > 0 and vv is not None:
                v += vv * f
                items.append((row["id"], vv * f))
        fcell = moved(next(x for x in P if x["id"] == "BD08"), cls)
        r["classes"][cls] = dict(ring_volume_freed_mm3=v, items=items,
                                 share_of_layer=v / layer_env,
                                 times_b_cell=v / r["b_cell_mm3"],
                                 body_cell_volume_freed_mm3=fcell * 128 * cell_vol_body,
                                 body_cells_leaving=round(fcell * 128))
    return r


# ------------------------------------------------------------------ energy
def energy_tables(D):
    n = D["meta"]["n_cells"]
    nb = D["meta"]["buffer_cells"]
    # CS: 128-cell roll-up at the targets
    wh = dict(G_target=5.90, S_target=7.38, G_model=6.83, S_model=8.36)
    return dict(per_cell={k: v / n for k, v in wh.items()},
                buffer_wh={k: v / n * nb for k, v in wh.items()},
                leaving_wh={k: v / n * (n - nb) for k, v in wh.items()},
                body_wh=wh)


# ------------------------------------------------------------------ cost
def cost_tables(D):
    sys.path.insert(0, os.path.join(ROOT, "program"))
    import budget as B  # read only
    unit = B.unit_cost()
    P = D["parts"]
    G = D["cost_groups"]
    out = {"volumes": {}}
    for vi, vol in enumerate(VOLS):
        v = int(vol)
        out["volumes"][vol] = {}
        for ii, lmh in enumerate(LMH):
            lines = dict(unit[v][lmh]["lines"])
            total = unit[v][lmh]["total"]
            roy = lines["cellular SEP royalties"]
            # group cost
            gcost = {}
            for gid, g in G.items():
                if g["budget"]:
                    gcost[gid] = lines[g["budget"]]
                else:
                    gcost[gid] = g["usd"][vol][ii]
            # row cost: share of its group by weight, over the rows allowed in that group
            def allowed(row, gid):
                if gid == "splitadd":
                    return row["g"] == "split"
                if gid == "portpart":
                    return row["g"] == "port"
                if gid == "none":
                    return False
                return row["g"] in COUNTED
            wsum = {}
            for row in P:
                if allowed(row, row["cg"]):
                    wsum[row["cg"]] = wsum.get(row["cg"], 0.0) + row["cw"]
            rowcost = {}
            for row in P:
                if allowed(row, row["cg"]):
                    rowcost[row["id"]] = gcost[row["cg"]] * row["cw"] / wsum[row["cg"]]
                else:
                    rowcost[row["id"]] = 0.0
            budget_ids = {gid for gid, g in G.items() if g["budget"]}
            res = {"total_budget": total, "royalty": roy, "group_cost": gcost, "classes": {}}
            for cls in CLASSES:
                leave_b = sum(rowcost[r["id"]] * moved(r, cls) for r in P
                              if r["g"] in COUNTED and r["cg"] in budget_ids)
                leave_m = sum(rowcost[r["id"]] * moved(r, cls) for r in P
                              if r["g"] in COUNTED and r["cg"] not in budget_ids)
                add = sum(rowcost[r["id"]] for r in P if r["g"] == "split" and resolve(r, cls)[0] == "A")
                f_u5 = moved(next(x for x in P if x["id"] == "M19"), cls)
                res["classes"][cls] = dict(leaves_budget=leave_b, leaves_missing=leave_m,
                                           added=add, royalty_follows_modem=roy * f_u5,
                                           share_leaving=leave_b / total,
                                           net_skin_change=-(leave_b + leave_m) + add)
            res["rowcost"] = rowcost
            out["volumes"][vol][lmh] = res
    return out


# ------------------------------------------------------------------ lanes
def lane_tables():
    L = []
    P = L.append
    BC = 0.400             # Gbit/s back channel, DI section B
    PAIR = 19.39 / 2       # Gbit/s payload of one 10 Gbit/s pair, DI section B
    DISP_NEED = 13.85      # Gbit/s, DI section B
    P("THE LEAVES AT C0: what the twelve gold leaves must carry once the ring chips are in the Core")
    P("sources: hw/display/out/interface.txt section B (pairs, back channel), F21 21.3.5 and 21.5.5, M09 section 3")
    P("")
    P("capacity: back channel %.3f Gbit/s, one display pair %.2f Gbit/s payload, two pairs %.2f" % (BC, PAIR, 2 * PAIR))
    P("display need (DSC 10 bpp, 240 Hz): %.2f Gbit/s, margin of two pairs %.0f %%" % (DISP_NEED, 100 * (2 * PAIR / DISP_NEED - 1)))
    P("")
    streams = [
        ("rear panel 480 x 480, 24 bit, 120 Hz, raw", 480 * 480 * 24 * 120 / 1e9),
        ("rear panel 480 x 480, 24 bit, 120 Hz, DSC 3:1", 480 * 480 * 24 * 120 / 3 / 1e9),
        ("rear panel clock at 10 Hz, raw", 480 * 480 * 24 * 10 / 1e9),
        ("audio: 2 mics and stereo out, 48 kHz, 24 bit", 4 * 48e3 * 24 / 1e9),
        ("IMU, 6 axes, 16 bit, 1 kHz", 6 * 16 * 1e3 / 1e9),
        ("camera still 50 MP, 12 bit, per frame (Gbit, not Gbit/s)", 50e6 * 12 / 1e9),
        ("camera 12.5 MP binned, 10 bit, 30 fps", 12.5e6 * 10 * 30 / 1e9),
        ("camera 12.5 MP binned, 10 bit, 60 fps", 12.5e6 * 10 * 60 / 1e9),
        ("camera 4K, 10 bit, 120 fps raw", 3840 * 2160 * 10 * 120 / 1e9),
    ]
    P("%-62s %10s  %-12s %-12s" % ("stream", "Gbit/s", "on the BC", "on a pair"))
    res = {}
    for name, g in streams:
        bc = "fits" if g <= BC * 0.5 else ("tight" if g <= BC else "NO")
        pr = "fits" if g <= PAIR else "NO"
        if "per frame" in name:
            bc = "%.1f s" % (g / BC)
            pr = "%.2f s" % (g / PAIR)
        P("%-62s %10.4f  %-12s %-12s" % (name, g, bc, pr))
        res[name] = g
    P("(fits on the BC means at most half of it, because touch at 480 Hz, hinge angles and telemetry share it)")
    P("")
    kb = 4.8
    cal_bits = 32 * kb * 1024 * 8
    P("calibration of a swapped quadrant: 32 tiles x %.1f KB [HYPOTHESIS, range 1 to 8 KB] = %.0f KB = %.2f Mbit" % (kb, 32 * kb, cal_bits / 1e6))
    P("  over the back channel : %.2f ms against the 3 ms window of F21 21.2.4" % (cal_bits / (BC * 1e9) * 1e3))
    P("  over one display pair : %.2f ms" % (cal_bits / (PAIR * 1e9) * 1e3))
    for k in (1.0, 8.0):
        b = 32 * k * 1024 * 8
        P("  at %.0f KB per tile      : %.2f ms on the BC, %.2f ms on a pair" % (k, b / (BC * 1e9) * 1e3, b / (PAIR * 1e9) * 1e3))
    res["cal_ms_bc"] = cal_bits / (BC * 1e9) * 1e3
    res["cal_ms_pair"] = cal_bits / (PAIR * 1e9) * 1e3
    P("")
    P("THE PIXEL STREAM AT C1 AND C2 against the radios the Leaf keeps")
    sub, bits, code = 3920, 12, 5.0 / 6.0
    sym = 13.6e-6
    per = sub * bits * code / sym
    wifi_phy = 2 * per / 1e9
    P("Wi-Fi 7 (802.11be) 2 x 2, 320 MHz, 4096-QAM 5/6, 0.8 us GI [GENERAL]: %.2f Gbit/s PHY, about %.1f Gbit/s real at 60 %%" % (wifi_phy, 0.6 * wifi_phy))
    for name, g in (("raw 10 bit, 240 Hz", 36.9), ("DSC 3:1", 12.3), ("4:1", 9.2), ("6:1", 6.1),
                    ("DSC 10 bpp as designed, wire", 13.43), ("compressed slices of Part 21, upper end", 0.15)):
        verdict = "fits PHY" if g <= wifi_phy else "does not fit PHY"
        if g <= 0.6 * wifi_phy:
            verdict = "fits real"
        P("  %-45s %6.2f Gbit/s  -> %s" % (name, g, verdict))
    res["wifi_phy"] = wifi_phy
    P("A 60 GHz link of 13.43 Gbit/s at 30 m is the question of the link seat (hw/core/link). Gate HC-A9.")
    return L, res


# ------------------------------------------------------------------ write
def fmt_alloc(row, cls):
    code, f = resolve(row, cls)
    if code == "M" and f < 0.999:
        return "M %.2f" % f
    return code


def write_csv(D):
    path = os.path.join(HERE, "parts_table.csv")
    cols = ["id", "group", "part", "count", "mass_g", "mass_basis", "mass_low_g", "mass_high_g", "mass_cite",
            "stated_reference_g", "stated_reference_cite", "place_today",
            "C0", "C0R", "C1", "C2", "rule_C0", "rule_C0R", "rule_C1", "rule_C2", "line_items", "volume_mm3", "reason", "cost_group", "service_today", "service_C0", "gates", "collisions"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in D["parts"]:
            code0, f0 = resolve(r, "C0")
            svc0 = "core" if (code0 == "M" and f0 >= 0.999) else ("core and quadrant" if code0 == "M" else r["svc"])
            v = vol_mm3(r)
            w.writerow([r["id"], r["g"], r["n"], r["cnt"], "" if r["m"] is None else r["m"], r["mb"],
                        r.get("lo", ""), r.get("hi", ""), r["ms"], r.get("ref", ""), r.get("refs", ""), r["today"]] +
                       [fmt_alloc(r, c) for c in CLASSES] + [verdict(r, c, star=False) for c in CLASSES] + [" ".join(r.get("line", []))] +
                       ["" if v is None else round(v, 2), r["why"], r["cg"], r["svc"], svc0, r["gates"], " ".join(r.get("col", []))])
    return path


def md_cell(s):
    return str(s).replace("|", "/")


def write_table_md(D, msum):
    path = os.path.join(OUT, "parts_table.md")
    L = []
    P = L.append
    P("# The allocation table of the Split, part by part")
    P("")
    P("Generated by `parts.py` from `parts_data.json`. Every row cites its file. `[HYPOTHESIS]` for every derived mass.")
    P("")
    P("**The rule of necessity (Ayaz, 2026-10-19).** " + D["meta"]["rule"] + " A star marks a part on the line. The line items L1 to L12 give the reason.")
    P("")
    P("**The verdict.** Body keeps the emitters, the tile drivers and the carrier of the tiles. Module is the B module. Core is the separate hardware.")
    P("")
    P("**The codes after the verdict.** P must stay: physics, law or an order of Ayaz. S stays by design. M can move to a Core, with the fraction. A is added by the Split.")
    P("")
    P("**The classes.** C0 is contact or tether, up to 2 m, with the radio SiPs moved whole. C0R is C0 with the radio SiPs kept. C1 is a room up to about 30 m. C2 is far.")
    P("")
    groups = [("body", "The body: 128 tiles, their layers, the hinges, the seat, the coils and the cells"),
              ("module", "The B module: the 32 parts of HARDWARE/13 (stated sum %.2f g)" % msum),
              ("placement", "Ring parts that the placement study lists and HARDWARE/13 does not"),
              ("split", "Parts the Split adds to the Skin at C0"),
              ("port", "The port part (L.5.0 values reused, [HYPOTHESIS])"),
              ("dock", "The dock, a host and not a Leaf part"),
              ("withdrawn", "Older catalogue parts that L.6.0 withdrew, kept so the catalogues are covered")]
    for g, title in groups:
        P("## " + title)
        P("")
        P("| ID | Part | Count | Mass g | Basis | C0 | C0R | C1 | C2 | Line | Why |")
        P("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in D["parts"]:
            if r["g"] != g:
                continue
            m = "none" if r["m"] is None else ("%.3g" % r["m"])
            if r["g"] == "withdrawn":
                m = "ref %.3g" % r.get("ref", 0)
            cells = []
            for c in CLASSES:
                v = verdict(r, c)
                if r["g"] in ("port", "dock", "withdrawn") or v == "none":
                    cells.append("-" if v == "none" else v)
                else:
                    cells.append("%s %s" % (v, fmt_alloc(r, c)))
            P("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                r["id"], md_cell(r["n"]), r["cnt"], m, r["mb"], " | ".join(cells), " ".join(r.get("line", [])) or "-", md_cell(r["why"])))
        P("")
    open(path, "w").write("\n".join(L) + "\n")
    return path


def write_line_md(D):
    path = os.path.join(OUT, "line.md")
    L = ["# The parts on the line, under the rule of necessity", "",
         "Rule: " + D["meta"]["rule"], "",
         "A part is on the line when the rule disagrees with a law, a gate or a physical fact. It is also on the line when no part list can split it. `[HYPOTHESIS]`", "",
         "| No. | The group | What the rule says | What the table holds | Why |", "|---|---|---|---|---|"]
    for x in D["line_items"]:
        L.append("| %s | %s | %s | %s | %s |" % (x["id"], md_cell(x["title"]), md_cell(x["rule"]), md_cell(x["held"]), md_cell(x["why"])))
    L.append("")
    L.append("## The parts of each line item")
    L.append("")
    L.append("| No. | Parts |")
    L.append("|---|---|")
    for x in D["line_items"]:
        L.append("| %s | %s |" % (x["id"], ", ".join(x["parts"])))
    open(path, "w").write("\n".join(L) + "\n")
    return path


def write_collisions_md(D):
    path = os.path.join(OUT, "collisions.md")
    L = ["# The collisions of the Split with the designs and the gates", "",
         "Each row names the gate or section, what collides, and the way out in each distance class. `[HYPOTHESIS]` for every resolution.", ""]
    for c in D["collisions"]:
        L.append("## %s. %s" % (c["id"], c["title"]))
        L.append("")
        L.append("| Item | Text |")
        L.append("|---|---|")
        L.append("| gate or section | %s |" % md_cell(c["where"]))
        L.append("| the collision | %s |" % md_cell(c["what"]))
        L.append("| resolve at C0 | %s |" % md_cell(c["C0"]))
        L.append("| resolve at C1 | %s |" % md_cell(c["C1"]))
        L.append("| resolve at C2 | %s |" % md_cell(c["C2"]))
        L.append("| parts | %s |" % ", ".join(c["parts"]))
        L.append("")
    open(path, "w").write("\n".join(L) + "\n")
    return path


def write_gates_md(D):
    path = os.path.join(OUT, "gates.md")
    L = ["# The proposed gates HC-A1 to HC-A12", "",
         "Proposed by the parts seat. The Lead merges them into the series of Part 21 if Ayaz rules for the Split.", "",
         "| Gate | The test | The pass condition |", "|---|---|---|"]
    for g in D["gates"]:
        L.append("| %s | %s | %s |" % (g["id"], md_cell(g["test"]), md_cell(g["pass"])))
    L += ["", "## The candidates for Ayaz", "", "| No. | The candidate | The decision it touches |", "|---|---|---|"]
    for k in D["candidates"]:
        L.append("| %s | %s | %s |" % (k["id"], md_cell(k["text"]), md_cell(k["touches"])))
    open(path, "w").write("\n".join(L) + "\n")
    return path


def write_service_md(D, M):
    P = D["parts"]
    path = os.path.join(OUT, "service.md")
    L = ["# The service story of the Split", "",
         "Law L9: a part is renewable and carries a record. Article 11 of 2023/1542: the user removes the battery. Quadrant swap in under 3 s (F21 21.2.4). Module swap in under 10 s (FINAL/03 3.8). `[HYPOTHESIS]`", ""]
    # swap units
    def unit_of(r, cls):
        code, f = resolve(r, cls)
        if code == "M" and f >= 0.999:
            return "core"
        if code == "M":
            return "split: core and " + r["svc"]
        if code == "A":
            return "added: " + r["svc"]
        return r["svc"]
    L.append("## Mass of each swap unit, by class")
    L.append("")
    L.append("| Swap unit | Today g | C0 | C0R | C1 | C2 |")
    L.append("|---|---|---|---|---|---|")
    units = ["quadrant", "module", "fixed", "core"]
    for u in units:
        row = [u]
        for cls in ("TODAY",) + CLASSES:
            tot = 0.0
            for r in P:
                if r["g"] not in COUNTED + ("split",) or r["m"] is None:
                    continue
                if cls == "TODAY":
                    if r["g"] == "split":
                        continue
                    if r["svc"] == u:
                        tot += r["m"]
                    continue
                code, f = resolve(r, cls)
                if code == "A":
                    if r["svc"] == u:
                        tot += r["m"]
                    continue
                if r["g"] == "split":
                    continue
                if code == "M":
                    if u == "core":
                        tot += r["m"] * f
                    if r["svc"] == u:
                        tot += r["m"] * (1 - f)
                elif r["svc"] == u:
                    tot += r["m"]
            row.append("%.2f" % tot)
        L.append("| " + " | ".join(row) + " |")
    L.append("")
    L.append("The quadrant row counts the derived body masses. The module row counts HARDWARE/13 and the placement-only parts. The core row is what the Core holds of today's Leaf mass.")
    L.append("")
    L.append("## Which parts become swappable in the Core, by class")
    L.append("")
    L.append("| ID | Part | Today | C0 | C1 | C2 |")
    L.append("|---|---|---|---|---|---|")
    for r in P:
        if r["g"] not in COUNTED + ("split",):
            continue
        us = [unit_of(r, c) for c in ("C0", "C1", "C2")]
        if r["g"] == "split":
            continue
        if all(u == r["svc"] for u in us):
            continue
        L.append("| %s | %s | %s | %s |" % (r["id"], md_cell(r["n"]), r["svc"], " | ".join(us)))
    L.append("")
    L.append("Parts not listed stay in the swap unit of the first column at every class.")
    L.append("")
    L.append("## What the record law gives the Core")
    L.append("")
    L.append("| Question | Answer |")
    L.append("|---|---|")
    L.append("| who holds the record of a moved part | the Core part itself, in its own secure element, as law L9 asks |")
    L.append("| who holds the record of the Skin | the Skin identity chip N01, which verifies and holds the part lines of the quadrants and the tile hubs |")
    L.append("| what a Core part swap needs from the Skin | nothing: the Skin sees a new Core certificate and pairs again by the chain record |")
    L.append("| the Article 11 unit at C0 | the Core cells, readily removable in the Core. The Skin quadrants keep only 20 Buffer cells |")
    L.append("| the Article 11 unit at C1 and C2 | unchanged: the quadrant, with 32 cells, TCMs and U_Q |")
    L.append("| the module swap at C0 | the module shrinks to the ring stub. Radio, decoder and wallet upgrades leave the module |")
    L.append("| what stays fixed in the Leaf at every class | the hinges, caps, emitters, seat, bar antennas and the touch grid. A failure there is a quadrant or a Leaf swap |")
    open(path, "w").write("\n".join(L) + "\n")
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    D = load()
    errs, msum = validate(D)
    if errs:
        print("VALIDATION FAILED")
        for e in errs:
            print("  " + e)
        return 1
    M = mass_tables(D)
    V = volume_tables(D)
    E = energy_tables(D)
    C = cost_tables(D)
    lanes, LR = lane_tables()

    write_csv(D)
    write_table_md(D, msum)
    write_collisions_md(D)
    write_line_md(D)
    write_gates_md(D)
    write_service_md(D, M)
    open(os.path.join(OUT, "lanes.txt"), "w").write("\n".join(lanes) + "\n")

    S = []
    p = S.append
    p("THE MASS AND VOLUME SUMMARY OF THE SPLIT (parts.py, all [HYPOTHESIS])")
    p("rows: %d, module stated sum %.2f g (HARDWARE/13 states 10.80 g), validation passed" % (len(D["parts"]), msum))
    t = M["today"]
    p("")
    p("THE LEAF TODAY")
    p("  body, derived L.6.0 sum        %6.2f g  (range %.1f to %.1f)" % (t["body_derived"], t["body_lo"], t["body_hi"]))
    p("  module, HARDWARE/13 stated     %6.2f g" % t["module_H13"])
    p("  module plus placement-only     %6.2f g" % t["module_with_placement_parts"])
    p("  Leaf, derived                  %6.2f g  (range %.1f to %.1f)" % (t["leaf_derived"], t["leaf_lo"], t["leaf_hi"]))
    p("  Leaf, stated 68.0 body plus H13 module  %6.2f g ; the stated total is 88.0 g (it counts a withdrawn 20 g module)" % t["leaf_stated_68_plus_H13"])
    p("  the stated 68 g body counts 34.4 g of withdrawn LLZO cells; the L.6.0 cells weigh 14.72 g (128 x 0.115 g, cell_spec.txt)")
    p("")
    p("THE MASS THAT LEAVES THE LEAF, by class (derived basis, then the stated 68 g basis)")
    p("  %-5s %9s %8s %9s %9s %9s | %9s %9s" % ("class", "leaves g", "share", "added g", "Skin g", "range lo-hi", "A leaves", "A share"))
    for cls in CLASSES:
        m = M[cls]
        p("  %-5s %9.2f %7.1f%% %9.2f %9.2f %5.1f-%-5.1f | %9.2f %8.1f%%" % (
            cls, m["leaves_g"], 100 * m["share_leaving"], m["added_g"], m["skin_g"],
            t["leaf_derived"] - m["leaves_hi"] + m["added_g"], t["leaf_derived"] - m["leaves_lo"] + m["added_g"],
            m["basis_A_leaves_g"], 100 * m["basis_A_share"]))
    p("  module alone: mass today %.2f g; after the Split:" % t["module_with_placement_parts"] + ", ".join(
        "%s %.2f g (leaves %.2f)" % (c, M[c]["module_after_g"], M[c]["module_leaves_g"]) for c in CLASSES))
    p("")
    p("MASS BY CODE (counted rows: body, module, placement-only; derived basis; M counts the moving fraction)")
    p("  %-5s %8s %8s %8s %8s | row counts" % ("class", "P g", "S g", "M g", "M stays"))
    cnt_rows = [r for r in D["parts"] if r["g"] in COUNTED]
    for cls in CLASSES:
        gp = sum(r["m"] for r in cnt_rows if resolve(r, cls)[0] == "P")
        gs = sum(r["m"] for r in cnt_rows if resolve(r, cls)[0] == "S")
        gm = sum(r["m"] * resolve(r, cls)[1] for r in cnt_rows if resolve(r, cls)[0] == "M")
        gms = sum(r["m"] * (1 - resolve(r, cls)[1]) for r in cnt_rows if resolve(r, cls)[0] == "M")
        npp = sum(1 for r in cnt_rows if resolve(r, cls)[0] == "P")
        nss = sum(1 for r in cnt_rows if resolve(r, cls)[0] == "S")
        nmm = sum(1 for r in cnt_rows if resolve(r, cls)[0] == "M")
        p("  %-5s %8.2f %8.2f %8.2f %8.2f | rows P %3d S %3d M %3d" % (cls, gp, gs, gm, gms, npp, nss, nmm))
    p("")
    p("VERDICT BY CLASS under the rule of necessity (counted rows, derived basis, grams and rows; a star row is on the line)")
    p("  %-5s %9s %9s %9s %9s | row counts" % ("class", "Body g", "Module g", "Core g", "Skin add"))
    for cls in CLASSES:
        acc = {"Body": [0.0, 0], "Module": [0.0, 0], "Core": [0.0, 0]}
        nline = 0
        for r in cnt_rows:
            v = verdict(r, cls, star=False)
            if v not in acc:
                continue
            acc[v][0] += r["m"]
            acc[v][1] += 1
            if r.get("line"):
                nline += 1
        add = sum(r["m"] for r in D["parts"] if r["g"] == "split" and resolve(r, cls)[0] == "A")
        p("  %-5s %9.2f %9.2f %9.2f %9.2f | rows Body %3d Module %3d Core %3d, on the line %3d" % (
            cls, acc["Body"][0], acc["Module"][0], acc["Core"][0], add, acc["Body"][1], acc["Module"][1], acc["Core"][1], nline))
    p("")
    nb = D["meta"]["buffer_cells"]
    p("THE ENERGY THAT LEAVES (C0: all 128 cells move, because the rule keeps no energy part at C0)")
    p("  body energy G target %.2f Wh, S target %.2f Wh, so %.2f to %.2f Wh leave the Leaf" % (
        E["body_wh"]["G_target"], E["body_wh"]["S_target"], E["body_wh"]["G_target"], E["body_wh"]["S_target"]))
    cellrow = next(r for r in D["parts"] if r["id"] == "BD08")
    tcmrow = next(r for r in D["parts"] if r["id"] == "BD09")
    muxrow = next(r for r in D["parts"] if r["id"] == "M27")
    buf_g = nb / 128 * (cellrow["m"] + tcmrow["m"]) + muxrow["m"]
    p("  LINE ITEM L2, the Buffer of Part 22: if %d cells stay on the Skin, %.2f g stay (cells, TCMs and the mux)," % (nb, buf_g))
    p("  the Skin keeps %.2f to %.2f Wh, and the cost that leaves falls by %s USD at 100 k, 1 M and 5 M (base)" % (
        E["buffer_wh"]["G_target"], E["buffer_wh"]["S_target"],
        " / ".join("%.1f" % (nb / 128 * (C["volumes"][v]["base"]["group_cost"]["cells"] + C["volumes"][v]["base"]["group_cost"]["tcm"])) for v in VOLS)))
    p("  C0 with the Buffer: leaves %.2f g, Skin %.2f g" % (M["C0"]["leaves_g"] - buf_g, M["C0"]["skin_g"] + buf_g))
    p("")
    p("THE VOLUME OF THE B RING THAT BECOMES FREE")
    p("  ring envelope %.0f mm3 (pi x 16^2 x 4.00); electronics layer above the board %.0f mm3 (r 14.75 x 2.30)" % (
        V["ring_envelope_mm3"], V["ring_layer_above_board_mm3"]))
    p("  B cell %.0f mm3, bar %.0f mm3, one body cell %.1f mm3, all 128 body cells %.0f mm3" % (
        V["b_cell_mm3"], V["bar_envelope_mm3"], V["body_cell_layer_mm3_each"], V["body_cell_layer_mm3_all"]))
    for cls in CLASSES:
        c = V["classes"][cls]
        p("  %-4s ring volume freed %7.1f mm3 = %4.1f %% of the layer = %.1f B cells ; body cell volume freed %7.0f mm3 (%d cells)" % (
            cls, c["ring_volume_freed_mm3"], 100 * c["share_of_layer"], c["times_b_cell"], c["body_cell_volume_freed_mm3"], c["body_cells_leaving"]))
        p("        parts: " + ", ".join("%s %.1f" % (i, v) for i, v in c["items"]))
    p("")
    p("WHAT IT DOES TO THE 4.00 MM, THE 1.00 MM AND THE 0.14 WH")
    p("  4.00 mm module : the camera column stands 3.90 mm (F21 21.3.5). No class thins the module. The freed volume is room.")
    p("  1.00 mm bar    : the bar holds A1, A2, A4 and the 12 leaves. All are P. No class changes the bar.")
    p("  0.14 Wh B cell : C0 and C0R move it with U7. C1 and C2 keep it (island rail of the wallet).")
    p("  body 2.00 mm   : the cell layer is 0.90 mm of 2.00 mm (45 %). At C0 all 128 tiles lose their cell: 1.10 mm (candidate K-6)")
    open(os.path.join(OUT, "summary.txt"), "w").write("\n".join(S) + "\n")

    # cost output
    CT = []
    q = CT.append
    q("THE COST SHARE OF EACH GROUP AND WHAT LEAVES (parts.py, program/budget.py read only, USD per Leaf, no margin)")
    q("All inputs are [HYPOTHESIS] of the Program Office. Groups marked MISSING are not in budget.py and carry a range of this seat.")
    q("")
    cmd = {}
    for vol in VOLS:
        b = C["volumes"][vol]
        tot_b = b["base"]["total_budget"]
        q("== volume %s per year" % format(int(vol), ","))
        q("unit cost today (budget.py): low %.0f, base %.0f, high %.0f USD" % (b["low"]["total_budget"], tot_b, b["high"]["total_budget"]))
        q("  %-12s %-9s %9s %7s   %s" % ("group", "source", "base USD", "share", "leaves base USD at C0 / C0R / C1 / C2"))
        G = D["cost_groups"]
        for gid, g in G.items():
            if gid in ("none", "splitadd", "portpart"):
                continue
            usd = b["base"]["group_cost"][gid]
            leave = []
            for cls in CLASSES:
                s = sum(b["base"]["rowcost"][r["id"]] * moved(r, cls) for r in D["parts"]
                        if r["g"] in COUNTED and r["cg"] == gid)
                leave.append(s)
            src = "budget.py" if g["budget"] else "MISSING"
            share = "%5.1f%%" % (100 * usd / tot_b) if g["budget"] else "  n/a "
            q("  %-12s %-9s %9.2f %7s   %s" % (gid, src, usd, share, " / ".join("%.2f" % x for x in leave)))
        roy = b["base"]["royalty"]
        q("  %-12s %-9s %9.2f %5.1f%%   follows the modem: %s" % ("royalty", "budget.py", roy, 100 * roy / tot_b,
                                                                   " / ".join("%.2f" % b["base"]["classes"][c]["royalty_follows_modem"] for c in CLASSES)))
        q("  other budget lines (assembly, packaging) stay: not allocated to a part, counted as staying")
        q("")
        q("  LEAVING THE LEAF, budget lines only (USD, low / base / high) and share of the unit cost (base)")
        for cls in CLASSES:
            lv = [b[k]["classes"][cls]["leaves_budget"] for k in LMH]
            ms = [b[k]["classes"][cls]["leaves_missing"] for k in LMH]
            ad = [b[k]["classes"][cls]["added"] for k in LMH]
            ry = b["base"]["classes"][cls]["royalty_follows_modem"]
            q("  %-4s leaves %7.1f / %7.1f / %7.1f  = %4.1f%% ; plus MISSING-group parts %5.2f / %5.2f / %5.2f ; royalty if it follows the modem %6.1f ; added to the Skin %5.2f / %5.2f / %5.2f" % (
                cls, lv[0], lv[1], lv[2], 100 * lv[1] / tot_b, ms[0], ms[1], ms[2], ry, ad[0], ad[1], ad[2]))
        q("")
        cmd[vol] = {cls: dict(leaves_low=b["low"]["classes"][cls]["leaves_budget"],
                              leaves_base=b["base"]["classes"][cls]["leaves_budget"],
                              leaves_high=b["high"]["classes"][cls]["leaves_budget"],
                              share_base=b["base"]["classes"][cls]["share_leaving"],
                              missing_base=b["base"]["classes"][cls]["leaves_missing"],
                              royalty_base=b["base"]["classes"][cls]["royalty_follows_modem"],
                              added_base=b["base"]["classes"][cls]["added"]) for cls in CLASSES}
    q("THE CEILING: the display (micro-LED tiles x 128) is a share of the unit cost that no class moves.")
    for vol in VOLS:
        b = C["volumes"][vol]["base"]
        share = b["group_cost"]["display"] / b["total_budget"]
        q("  %s per year: display %.0f USD = %.1f %%; so at most %.1f %% of the unit cost is movable, before assembly and packaging" % (
            format(int(vol), ","), b["group_cost"]["display"], 100 * share, 100 * (1 - share)))
    open(os.path.join(OUT, "cost.txt"), "w").write("\n".join(CT) + "\n")

    # cost md
    CM = ["# The cost share of each group and what leaves the Leaf", "",
          "Source: `program/budget.py`, base case, read only. USD per Leaf, no margin. `[HYPOTHESIS]` of the Program Office. MISSING groups carry a range of this seat.", ""]
    for vol in ("1000000", "100000", "5000000"):
        b = C["volumes"][vol]["base"]
        tot = b["total_budget"]
        CM.append("## Volume %s per year, unit cost %.0f USD" % (format(int(vol), ","), tot))
        CM.append("")
        CM.append("| Group | Source | USD | Share | Leaves C0 | Leaves C0R | Leaves C1 | Leaves C2 |")
        CM.append("|---|---|---|---|---|---|---|---|")
        for gid, g in D["cost_groups"].items():
            if gid in ("none", "splitadd", "portpart"):
                continue
            usd = b["group_cost"][gid]
            lv = []
            for cls in CLASSES:
                s = sum(b["rowcost"][r["id"]] * moved(r, cls) for r in D["parts"] if r["g"] in COUNTED and r["cg"] == gid)
                lv.append("%.2f" % s)
            if g["budget"]:
                CM.append("| %s | budget.py | %.2f | %.1f %% | %s |" % (g["budget"][:60], usd, 100 * usd / tot, " | ".join(lv)))
            else:
                lo, ba, hi = (C["volumes"][vol][k]["group_cost"][gid] for k in LMH)
                CM.append("| %s | MISSING, range %.1f to %.1f | %.2f | n/a | %s |" % (md_cell(g["label"])[:70], lo, hi, usd, " | ".join(lv)))
        roy = b["royalty"]
        CM.append("| cellular royalties | budget.py | %.2f | %.1f %% | %s |" % (
            roy, 100 * roy / tot, " | ".join("%.2f" % b["classes"][c]["royalty_follows_modem"] for c in CLASSES)))
        CM.append("")
        CM.append("The royalty row moves only if the royalty follows the modem. That is a legal question (candidate K-3 and gate HC-A10).")
        CM.append("")
    open(os.path.join(OUT, "cost.md"), "w").write("\n".join(CM) + "\n")

    # json
    js = dict(validation="ok", module_stated_sum_g=msum, mass=M, volume=V, energy=E, cost_summary=cmd, lanes=LR)
    json.dump(js, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=str)
    json.dump({vol: {k: dict(total_budget=C["volumes"][vol][k]["total_budget"], classes=C["volumes"][vol][k]["classes"],
                              group_cost=C["volumes"][vol][k]["group_cost"]) for k in LMH} for vol in VOLS},
              open(os.path.join(OUT, "cost.json"), "w"), indent=1)
    print("\n".join(S))
    print()
    print("\n".join(CT[:48]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
