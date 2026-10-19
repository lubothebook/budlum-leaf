#!/usr/bin/env python3
"""ringfit.py - does the B ring board fit after the Split? (gate HC-A2)

PARTS seat of hw/core. Reads hw/electronics/placement.py (imported, read only)
and parts_data.json. Two checks:

  1. AREA. The demand of the parts that stay (area with skirt, courtyard and
     can, the formula of placement.py) against the free board area that
     placement_results.txt reports. Deterministic. Needs no extra package.
  2. PACKING (option --pack). The raster packer of placement.py runs on the
     reduced part list. It needs shapely. The packer is greedy and its result
     moves with the numpy and shapely versions, so the baseline is run in the
     same session and printed next to the Split result.

If shapely is missing, the area check still runs. The part list of
placement.py is read through stub modules, which hold no geometry.

Run: python3 ringfit.py            (area check)
     python3 ringfit.py --pack     (adds the packer, about 20 s per run)
"""
import json
import os
import re
import sys
import types

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
CLASSES = ("C0", "C0R", "C1", "C2")


def import_placement():
    """Import hw/electronics/placement.py. Use stub shapely if it is missing."""
    real = True
    try:
        import shapely  # noqa: F401
    except ImportError:
        real = False
        sg = types.ModuleType("shapely.geometry")
        sg.Point = sg.box = None
        sa = types.ModuleType("shapely.affinity")
        sa.rotate = sa.translate = None
        so = types.ModuleType("shapely.ops")
        so.unary_union = None
        top = types.ModuleType("shapely")
        top.geometry, top.affinity, top.ops = sg, sa, so
        sys.modules.update({"shapely": top, "shapely.geometry": sg, "shapely.affinity": sa, "shapely.ops": so})
    sys.path.insert(0, os.path.join(ROOT, "hw", "electronics"))
    import placement as PL  # read only
    return PL, real


def read_areas():
    """Free top and bottom area per scenario from placement_results.txt."""
    res = {}
    path = os.path.join(ROOT, "hw", "electronics", "placement_results.txt")
    for line in open(path):
        m = re.match(r"^(S\d)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)%\s+([\d.]+)\s+(\d+)", line)
        if m:
            res[m.group(1)] = dict(placed=int(m.group(2)), failed=int(m.group(3)), demand=float(m.group(4)),
                                   top=float(m.group(5)), bottom=float(m.group(7)))
    return res


def staying_names(D, cls):
    gone = set()
    for r in D["parts"]:
        if r["g"] not in ("module", "placement") or not r.get("pl"):
            continue
        a, f = (r["a0"], r["f0"]) if cls in ("C0", "C0R") else (r["a1"], r["f1"])
        if cls == "C0R" and r.get("radio"):
            a, f = "S", 0
        if cls == "C2":
            a, f = r["a2"], r["f2"]
        if a == "M" and f >= 0.999:
            gone.update(r["pl"])
    return gone


def added_parts(D, cls):
    """Skin additions as placement-style dicts (w, h, z, kind)."""
    sizes = {"N01": (2.0, 2.0, 0.40), "N02": (2.0, 2.0, 0.40), "N03": (3.0, 3.0, 0.50)}
    out = []
    for r in D["parts"]:
        if r["g"] != "split":
            continue
        if cls in ("C0", "C0R"):
            on = True
        else:
            on = False
        if on:
            w, h, z = sizes[r["id"]]
            out.append(dict(name=r["id"] + " " + r["n"][:24], w=w, h=h, z=z, kind="ic", hot=False, rmin=0.0, rmax=99.0))
    return out


def demand(PL, plist):
    return sum((p["w"] + 2 * PL.inflate(p)) * (p["h"] + 2 * PL.inflate(p)) for p in plist)


def main():
    pack = "--pack" in sys.argv
    D = json.load(open(os.path.join(HERE, "parts_data.json")))
    PL, real = import_placement()
    areas = read_areas()
    L = []
    P = L.append
    P("RING FIT AFTER THE SPLIT (ringfit.py, gate HC-A2). Area in mm2, skirt, courtyard and can included.")
    P("free board area from placement_results.txt: S2 top %.1f, S4 top %.1f plus bottom rim %.1f" % (
        areas["S2"]["top"], areas["S4"]["top"], areas["S4"]["bottom"]))
    P("the packer of placement.py fails 3 parts in every baseline scenario S0 to S5 (placement_results.txt)")
    P("")
    P("%-5s %-9s %8s %8s %8s %6s  %s" % ("class", "scenario", "demand", "free", "fill", "parts", "parts removed or added"))
    summary = {}
    for sc, free in (("S2", areas["S2"]["top"]), ("S3", areas["S3"]["top"]), ("S4", areas["S4"]["top"] + areas["S4"]["bottom"])):
        base_parts = PL.parts(sc)
        for cls in ("BASE",) + CLASSES:
            if cls == "BASE":
                plist = base_parts
                note = "baseline, the parts of placement.py"
            else:
                gone = staying_names(D, cls)
                plist = [p for p in base_parts if p["name"] not in gone] + added_parts(D, cls)
                note = "removed %d, added %d" % (len([p for p in base_parts if p["name"] in gone]), len(added_parts(D, cls)))
            dem = demand(PL, [p for p in plist if not (sc in ("S3", "S4") and p["kind"] == "cell")])
            fill = dem / free
            P("%-5s %-9s %8.1f %8.1f %7.0f%% %6d  %s" % (cls, sc, dem, free, 100 * fill, len(plist), note))
            summary["%s/%s" % (cls, sc)] = dict(demand=dem, free=free, fill=fill, parts=len(plist))
    P("")
    P("reading: fill above 100 percent cannot be packed. The baseline S2 demand exceeds the board. The Split at C0 leaves a board far under full.")
    gate = summary["C0/S3"]["fill"] <= 0.60 and summary["C0/S2"]["fill"] <= 0.60
    P("gate HC-A2 area test at C0 (fill 60 percent or less in S2 and S3): %s" % ("PASS" if gate else "FAIL"))
    P("C0R: S2 %.0f %%, S3 %.0f %%; C1 and C2 equal the baseline." % (100 * summary["C0R/S2"]["fill"], 100 * summary["C0R/S3"]["fill"]))

    if pack:
        P("")
        if not real:
            P("PACKING SKIPPED: shapely is not installed. Install shapely in user space and run again.")
        else:
            P("PACKING with the raster packer of placement.py (same session for the baseline)")
            orig = PL.parts
            for sc in ("S2", "S4"):
                for cls in ("BASE", "C0", "C0R"):
                    if cls == "BASE":
                        PL.parts = orig
                    else:
                        gone = staying_names(D, cls)
                        add = added_parts(D, cls)
                        PL.parts = (lambda s, g=gone, a=add: [p for p in orig(s) if p["name"] not in g] + a)
                    r = PL.run(sc)
                    P("  %-5s %-3s placed %2d failed %d errors %d  %s" % (
                        cls, sc, len(r["placed"]), len(r["failed"]), len(r["errors"]),
                        ", ".join(p["name"] for p, _ in r["failed"]) or "-"))
                    summary["pack %s/%s" % (cls, sc)] = dict(placed=len(r["placed"]), failed=len(r["failed"]), errors=len(r["errors"]))
            PL.parts = orig
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "ringfit.txt"), "w").write("\n".join(L) + "\n")
    json.dump(summary, open(os.path.join(OUT, "ringfit.json"), "w"), indent=1)
    print("\n".join(L))
    return 0 if gate else 1


if __name__ == "__main__":
    sys.exit(main())
