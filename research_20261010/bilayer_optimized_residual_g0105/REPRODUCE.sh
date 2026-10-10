#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('INPUT_SHA256.json',Path('..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
(ulimit -v 102400; ulimit -t 40; timeout 45 taskset -c 3 ../bilayer_complete_residual_8x4/residual_scalar ../bilayer_complete_residual_8x4/geometry_8x4.txt raw_residual_check.json coefficients.txt origin)
taskset -c 3 python assemble.py raw_residual_check.json physical_result_check.json
python - <<'PY'
import json
x=json.load(open('physical_result.json'));y=json.load(open('physical_result_check.json'))
for k in ['contraction_seconds','peak_rss_kib']:x.pop(k);y.pop(k)
assert x==y
print('PASS complete physical residual replay agrees')
PY
