#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python rebuild_d26.py > rebuild.log
python limited_run.py 48 > benchmark48.out 2> benchmark48.log
python - <<'PY'
from pathlib import Path
p=Path('.').resolve()
def ints(f):return {k:int(v) for line in f.read_text().splitlines() for k,v in [line.split('=')]}
a=ints(p/'benchmark48.out');b=ints(p.parent/'mps_excited_seed_witnesses/ground_lengths.out')
assert all(a[k]==b[k] for k in a)
PY
python limited_run.py 96 100 > anchors.out 2> anchors.log
python check.py > check.log
