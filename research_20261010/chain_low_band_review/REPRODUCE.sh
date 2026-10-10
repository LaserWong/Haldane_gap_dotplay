#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# Recompute in a sibling scratch directory, preserving the sealed review bytes.
python - "$HERE" <<'PY'
import hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1]);m=p/'MANIFEST_SHA256.json'
if m.exists():
 for n,h in json.loads(m.read_text()).items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
 print('Original independent-review seal verified')
PY
REPLAY=$(mktemp -d "$ROOT/research_20261010/.chain_low_band_replay.XXXXXX")
trap 'rm -rf "$REPLAY"' EXIT
cp "$HERE"/*.py "$REPLAY/"
python "$REPLAY/verify_blocks.py"
python "$REPLAY/audit_certificate.py"
python "$REPLAY/rejection_guards.py"
python "$REPLAY/physical_diagnostic.py"
python - "$HERE" "$REPLAY" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:]);a=json.loads((old/'SUMMARY.json').read_text());b=json.loads((new/'SUMMARY.json').read_text())
assert a['status']==b['status'] and a['results']==b['results'] and a['moment_review']==b['moment_review'] and a['provenance']==b['provenance']
print('Exact results and accepted scope reproduce; frozen review unchanged')
PY
