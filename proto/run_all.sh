#!/bin/sh
# Runs every script of the Wire-Protocol team and the prose check.
set -e
cd "$(dirname "$0")"
python3 tools/kmac.py
python3 tests/test_roundtrip.py > /dev/null && echo "round trip: ok (out/sizes.md)"
python3 model/bitrate.py > /dev/null && echo "bitrate: ok (out/bitrate.md)"
python3 model/handover.py > /dev/null && echo "handover: ok (out/handover.md)"
python3 ../tools/check_prose.py README.md TRANSPORT.md VERSIONING.md
