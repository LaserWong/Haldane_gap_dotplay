#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
ulimit -v 1048576
python - <<'PY'
import json,hashlib
from pathlib import Path
for p,h in json.loads(Path('FROZEN_MANIFEST.json').read_text())['files'].items():
 assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
for p,h in json.loads(Path('INPUT_SHA256.json').read_text()).items():
 assert hashlib.sha256((Path('..')/p).read_bytes()).hexdigest()==h,p
print('Own freeze and input pins pass.')
PY
python verify_inputs.py
python replay.py
python weight_class.py
python numerator_floor.py
