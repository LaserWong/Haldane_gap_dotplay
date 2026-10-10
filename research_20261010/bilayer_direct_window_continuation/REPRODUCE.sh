#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('DEPENDENCIES.json',Path('..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
taskset -c 3 python replay_intervals.py
python - <<'PY'
import json
x=json.load(open('interval_results.json'));y=json.load(open('interval_results_check.json'))
for k in ['seconds','peak_rss_kib']:x.pop(k);y.pop(k)
assert x==y
print('PASS exact66-interval replay agrees')
PY
