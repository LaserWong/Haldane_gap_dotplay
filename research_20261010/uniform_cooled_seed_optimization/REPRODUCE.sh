#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
g++ -O2 contract_ground.cpp -lgmpxx -lgmp -o contract_ground
taskset -c 0 ./contract_ground ../../audit/mps/mps_blocks.txt 48 > benchmark48.out 2> benchmark48.log
python - <<'PY'
from pathlib import Path
d={l.split('=')[0]:l for l in Path('../mps_excited_seed_witnesses/ground_lengths.out').read_text().splitlines()}
assert all(d[l.split('=')[0]]==l for l in Path('benchmark48.out').read_text().splitlines())
PY
taskset -c 0 ./contract_ground ../../audit/mps/mps_blocks.txt 104 108 112 120 > new_lengths.out 2> new_lengths.log
python certify.py > certify.log
python scan.py > scan.log
