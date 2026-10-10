#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python - <<'PY'
from pathlib import Path
import hashlib,json
for p,h in json.loads(Path('INPUT_SHA256.json').read_text()).items():
 assert hashlib.sha256((Path('snapshot')/p).read_bytes()).hexdigest()==h,p
print('Frozen input hashes PASS')
PY
python audit.py
