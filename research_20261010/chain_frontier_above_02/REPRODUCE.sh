#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - "$HERE" <<'PY'
import json,hashlib,sys
from pathlib import Path
p=Path(sys.argv[1]);root=p.parents[1]
for name,h in json.loads((p/'FROZEN_MANIFEST.json').read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
for name,h in json.loads((p/'EXTERNAL_INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,name
print('Frozen and inherited inputs verified')
PY
TMP="$(mktemp -d "$HERE/../chain_frontier_replay.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$HERE"/*.json "$HERE"/*.npz "$TMP/"
python "$TMP/explore.py"
python "$TMP/optimize_comparison.py"
python "$TMP/expand_reference.py"
python "$TMP/certify.py"
python "$TMP/obstruction.py"
python "$TMP/diagnose.py"
python "$TMP/verify.py"
python - "$HERE" "$TMP" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:])
a=json.loads((old/'summary.json').read_text())['results'];b=json.loads((new/'summary.json').read_text())['results']
assert a==b,(a,b)
print('Clean replay reproduced all certified gaps, paths and onset sizes.')
PY
