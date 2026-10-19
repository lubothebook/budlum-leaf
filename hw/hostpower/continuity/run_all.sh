#!/bin/sh
# Runs every script of the continuity team, then the tests and the prose check.
# Usage: sh hw/hostpower/continuity/run_all.sh
set -e
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 powersm.py --fuzz
python3 handover_sim.py > /dev/null
python3 dockpair.py > /dev/null
python3 protodraft.py > /dev/null
python3 sessionchain.py
python3 -m unittest discover -s tests 2>&1 | tail -4
python3 ../../../tools/check_prose.py README.md POWER-STATES.md RG-19-session-pause-resume.md
