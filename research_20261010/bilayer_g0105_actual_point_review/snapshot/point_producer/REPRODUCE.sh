#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('SCALAR_INPUT_SHA256.json',Path('../../..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
taskset -c 3 python certify.py
python - <<'PY'
import json
x=json.load(open('candidate.json'));y=json.load(open('candidate_check.json'));x.pop('seconds');y.pop('seconds');assert x==y
print('PASS actual-input all-size scalar replay agrees')
PY
