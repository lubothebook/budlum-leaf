#!/bin/sh
# Run every U6 script in order. Stops at the first failure.
set -e
cd "$(dirname "$0")"
python3 ref/keccak.py
python3 ref/gen_vectors.py
python3 sim/test_slice_auth.py
python3 scripts/throughput.py
python3 scripts/framestore_budget.py
python3 scripts/export_verilog.py
