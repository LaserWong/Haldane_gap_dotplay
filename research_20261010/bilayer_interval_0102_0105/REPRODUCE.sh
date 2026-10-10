#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('INPUT_SHA256.json',Path('../..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
taskset -c 3 python export.py
taskset -c 3 python certify_interval.py
python - <<'PY'
import json
from pathlib import Path
for shape in ['4x4','8x4']:assert json.load(open(f'ground_polynomial_{shape}.json'))==json.load(open(f'ground_polynomial_{shape}_check.json'))
x=json.load(open('summary.json'));y=json.load(open('summary_check.json'))
for k in ['seconds','peak_rss_kib']:x.pop(k);y.pop(k)
assert x==y
for p in Path('coverage').glob('*.json'):assert json.load(open(p))==json.load(open(Path('coverage_check')/p.name))
print('PASS exact polynomials and all closed intervals agree')
PY
