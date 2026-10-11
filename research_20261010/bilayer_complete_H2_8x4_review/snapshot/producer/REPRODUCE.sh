#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('INPUT_SHA256.json',Path('..'))]:
 for f,h in json.load(open(file)).items():assert hashlib.sha256((base/f).read_bytes()).hexdigest()==h,f
print('Seals verified')
PY
mkdir -p check
(ulimit -v 524288; ulimit -t 60; taskset -c 3 g++ -O2 -std=c++17 ../bilayer_residual_pencil_fixture/matrix_residual.cpp -lgmpxx -lgmp -o check/matrix_residual)
(ulimit -v 102400; ulimit -t 40; timeout 45 taskset -c 3 check/matrix_residual ../bilayer_complete_residual_8x4/geometry_8x4.txt check/matrix_8x4.json)
python assemble.py check
python - <<'PY'
import json
from pathlib import Path
for name in ['matrix_8x4.json','complete_H2_polynomial_8x4.json','fixture_checks.json']:
 a=json.load(open(name));b=json.load(open(Path('check')/name))
 for k in ['cache_seconds','q4_seconds','q6_seconds','seconds','peak_rss_kib']:a.pop(k,None);b.pop(k,None)
 assert a==b,name
print('PASS complete 8x4 matrix and polynomial replay')
PY
