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
(ulimit -v 524288; ulimit -t 60; taskset -c 3 g++ -O2 -std=c++17 matrix_residual.cpp -lgmpxx -lgmp -o check/matrix_residual)
(ulimit -v 262144; ulimit -t 5; taskset -c 3 check/matrix_residual ../bilayer_16d_4x4_residual_g0105/geometry_4x4.txt check/matrix_4x4.json)
(ulimit -v 262144; ulimit -t 4; taskset -c 3 check/matrix_residual ../bilayer_complete_residual_8x4/geometry_4x2.txt check/matrix_4x2.json)
python check_fixture.py check
python - <<'PY'
import json
from pathlib import Path
for name in ['matrix_4x4.json','matrix_4x2.json','complete_H2_polynomial_4x4.json','complete_H2_polynomial_4x2.json','fixture_checks.json']:
 a=json.load(open(name));b=json.load(open(Path('check')/name))
 for k in ['cache_seconds','q4_seconds','q6_seconds','seconds','peak_rss_kib']:a.pop(k,None);b.pop(k,None)
 assert a==b,name
print('PASS fixture matrices and complete polynomial replay')
PY
