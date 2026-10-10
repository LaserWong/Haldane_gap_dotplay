#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('POINT_MANIFEST_SHA256.json',Path('.')),('INTERVAL_MANIFEST_SHA256.json',Path('.')),('POINT_DEPENDENCIES.json',Path('../..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
taskset -c 3 python certify_points.py
taskset -c 3 python extend_interval.py
python - <<'PY'
import json
from pathlib import Path
x=json.load(open('points.json'));y=json.load(open('points_check.json'));assert x['results']==y['results']
x=json.load(open('extension_summary.json'));y=json.load(open('extension_summary_check.json'))
for k in ['seconds','peak_rss_kib']:x.pop(k);y.pop(k)
assert x==y
for p in Path('extension').glob('*.json'):assert json.load(open(p))==json.load(open(Path('extension_check')/p.name))
print('PASS exact point and closed-interval replay agrees')
PY
