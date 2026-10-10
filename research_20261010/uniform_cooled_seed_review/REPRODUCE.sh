#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python rebuild_d26.py > rebuild.log
g++ -O2 contract_sequential.cpp -lgmpxx -lgmp -o contract_sequential
./contract_sequential d26_blocks.txt 48 > benchmark48.out 2> benchmark48.log
python - <<'PY'
from pathlib import Path
p=Path('.').resolve()
assert (p/'benchmark48.out').read_bytes()==(p.parent/'uniform_cooled_seed_optimization/benchmark48.out').read_bytes()
PY
./contract_sequential d26_blocks.txt 104 108 112 120 > new_lengths.out 2> new_lengths.log
python check_scalar.py > scalar.log
python adversarial.py > adversarial.log
