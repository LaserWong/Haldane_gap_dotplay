#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
python - "$HERE" <<'PY'
import sys,json,hashlib
from pathlib import Path
p=Path(sys.argv[1])
for name,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():
 assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
print('Review seal verified')
PY
OUT="$(mktemp -d /tmp/bilayer-g010-review-XXXXXX)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python "$HERE/review_exact.py" "$OUT/exact_result.json"
python "$HERE/review_scan.py" "$OUT/scan_result.json"
printf 'Independent replay outputs: %s\n' "$OUT"
