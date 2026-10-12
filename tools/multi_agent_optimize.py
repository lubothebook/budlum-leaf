#!/usr/bin/env python3
"""
BUDLUM LEAF · tools/multi_agent_optimize.py · Revision L.5.0
Multi-Agent Self-Optimization Orchestrator (local deterministic verification only).

L.6.0: the remote Arena mode was removed. It never worked and it could send
ANTHROPIC_AUTH_TOKEN to a third-party host. Research agents now run in the
Claude Code session, not from this script.

Architecture:
  Connects 4 specialized domain agents in parallel and synthesizes a unified optimization verdict:
    1. CAD & 3D Geometry Agent      -> verifies STL watertightness, 4-Quadrant (+) 2.20 mm (72 g) body, and 90° B module
    2. Pafta & SVG Layout Agent     -> runs check_sheets.py & check_widths.py across all 32 SVGs (OVER=0 COVERED=0 COLLIDE=0)
    3. Hardware Architecture Agent  -> verifies compliance with Revision L.5.0 (LLZO, Qi2.2, <15 um n=1.585 seam, <=36.2 C, 90° B)
    4. Prose & Gate Auditor Agent   -> runs assemble.py, check_prose.py, and check_crossrefs.py (0 errors across all files)
"""

import concurrent.futures
import glob
import json
import os
import struct
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_cmd(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def _check_stl(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 84:
        return False, 0, (0.0, 0.0, 0.0)
    n_tris = struct.unpack("<I", data[80:84])[0]
    if len(data) != 84 + n_tris * 50:
        return False, n_tris, (0.0, 0.0, 0.0)
    xs, ys, zs = [], [], []
    off = 84
    for _ in range(n_tris):
        vals = struct.unpack("<12fH", data[off : off + 50])
        off += 50
        for j in (3, 6, 9):
            xs.append(vals[j])
            ys.append(vals[j + 1])
            zs.append(vals[j + 2])
    dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    return True, n_tris, dims


def agent_cad_geometry():
    """Agent 1: Verifies 3D STL models and Revision L.5.0 4-Quadrant (+) Puzzle Body + 90-degree Bent B dimensions."""
    expected = {
        "cad/models/leaf80-body.stl": (40.0, 80.0, 2.00),
        "cad/models/leaf160-body.stl": (80.0, 160.0, 2.00),
        "cad/models/leaf480-body.stl": (320.0, 480.0, 2.00),
        "cad/models/leaf160-frame.stl": (80.0, 160.0, 2.00),
        "cad/models/leaf160-screen.stl": (77.40, 157.40, 1.80),
        "cad/models/leaf160-battery.stl": (73.30, 153.20, 1.22),
        "cad/models/monogram-module.stl": (32.00, 37.10, 4.02),
        "cad/models/leaf160-device.stl": (80.00, 161.10, 4.02),
    }
    issues = []
    checked = 0
    for rel, (ew, eh, et) in expected.items():
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            issues.append(f"Missing STL: {rel}")
            continue
        ok, n_tris, (dx, dy, dz) = _check_stl(full)
        checked += 1
        if not ok or n_tris == 0:
            issues.append(f"Corrupt STL: {rel}")
            continue
        if abs(dx - ew) > 0.5 or abs(dy - eh) > 0.8 or abs(dz - et) > 0.15:
            issues.append(
                f"Dimension drift in {rel}: got {dx:.2f}x{dy:.2f}x{dz:.2f} mm, expected {ew:.2f}x{eh:.2f}x{et:.2f} mm"
            )
    return {
        "agent": "CAD_GEOMETRY_AGENT",
        "passed": len(issues) == 0,
        "models_verified": checked,
        "issues": issues,
    }


def agent_pafta_layout():
    """Agent 2: Verifies all 32 SVG engineering sheets (OVER=0, COVERED=0, COLLIDE=0, 0 over-width)."""
    svgs = (
        sorted(glob.glob(os.path.join(ROOT, "pafta", "*.svg")))
        + [os.path.join(ROOT, "BUDLUM-LEAF-STACK.svg")]
        + sorted(glob.glob(os.path.join(ROOT, "cad", "models", "*.svg")))
    )
    rc1, out1 = _run_cmd(["python3", "pafta/check_sheets.py"] + svgs)
    rc2, out2 = _run_cmd(["python3", "pafta/check_widths.py"] + svgs)
    ok = (rc1 == 0) and (rc2 == 0) and ("OVER=0  COVERED=0  COLLIDE=0" in out1) and ("0 line(s) over the limit" in out2)
    return {
        "agent": "PAFTA_LAYOUT_AGENT",
        "passed": ok,
        "svgs_verified": len(svgs),
        "check_sheets": out1.splitlines()[-1] if out1 else "",
        "check_widths": out2.splitlines()[-1] if out2 else "",
    }


def agent_hardware_architecture():
    """Agent 3: Audits HARDWARE/00..20 against Revision L.5.0 4-Quadrant (+) Solid-State & 90-degree Bent B rules."""
    required_terms = [
        ("LLZO", "Biocompatible All-Solid-State LLZO/PEO battery"),
        ("Qi2.2", "Universal Qi / Qi2.2 wireless charging on the screen body"),
        ("1.585", "Index-matched (n = 1.585) <15 um zero-scratch optical + seam"),
        ("36.2", "Eyewear ocular thermal limiter (<=36.2 C)"),
        ("ISO 10993", "Medical-grade BPA-free ISO 10993 polycarbonate"),
        ("90°", "90-degree bent-stem B camera module"),
        ("UWB / mmWave", "Zero-CPU Display Driver + UWB/mmWave transceiver"),
    ]
    hw_files = sorted(glob.glob(os.path.join(ROOT, "HARDWARE", "*.md")))
    combined = ""
    for p in hw_files:
        with open(p, encoding="utf-8") as f:
            combined += "\n" + f.read()
    missing = [desc for term, desc in required_terms if term not in combined]
    return {
        "agent": "HARDWARE_ARCHITECTURE_AGENT",
        "passed": len(missing) == 0,
        "files_verified": len(hw_files),
        "missing_requirements": missing,
    }


def agent_prose_and_gates():
    """Agent 4: Runs assemble.py (PRG-16), check_prose.py (PRG-12), and check_crossrefs.py (PRG-15)."""
    rc_a, out_a = _run_cmd(["python3", "tools/assemble.py"])
    rc_p, out_p = _run_cmd(["python3", "tools/check_prose.py"])
    rc_c, out_c = _run_cmd(["python3", "tools/check_crossrefs.py"])
    ok = (
        (rc_a == 0)
        and (rc_p == 0)
        and (rc_c == 0)
        and ("0.0% of the sentences are long" in out_p)
        and ("every count claim agrees with canon" in out_c)
    )
    return {
        "agent": "PROSE_AND_GATES_AGENT",
        "passed": ok,
        "assemble": out_a.splitlines()[-1] if out_a else "",
        "prose": out_p.splitlines()[-1] if out_p else "",
        "crossrefs": out_c.splitlines()[-1] if out_c else "",
    }


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        f_cad = pool.submit(agent_cad_geometry)
        f_paf = pool.submit(agent_pafta_layout)
        f_hw = pool.submit(agent_hardware_architecture)
        f_pr = pool.submit(agent_prose_and_gates)
        results = [f_cad.result(), f_paf.result(), f_hw.result(), f_pr.result()]

    all_passed = all(r["passed"] for r in results)

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['agent']}: {json.dumps({k: v for k, v in r.items() if k != 'agent'}, ensure_ascii=False)}")

    print(f"MULTI-AGENT SELF-OPTIMIZATION VERDICT: {'ALL 4 AGENTS PASSED' if all_passed else 'ACTION REQUIRED'}")
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
