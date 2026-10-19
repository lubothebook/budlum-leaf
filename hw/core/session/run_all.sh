#!/bin/sh
# Runs every script of the session seat, then the tests and the prose check.
# Usage: sh hw/core/session/run_all.sh
set -e
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 -W ignore skinsession.py
python3 -W ignore roam_sim.py > /dev/null
python3 -W ignore corefail.py > /dev/null
python3 -W ignore skinproto.py > /dev/null
python3 -W ignore -m unittest discover -s tests 2>&1 | tail -4
python3 ../../../tools/check_prose.py README.md RG-19A-skins.md
