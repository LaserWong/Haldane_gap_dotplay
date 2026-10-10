#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
python - "$HERE" <<'PY'
from pathlib import Path
import sys,json,hashlib
p=Path(sys.argv[1]);f=p/'MANIFEST_SHA256.json'
if f.exists():
 for n,h in json.loads(f.read_text()).items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
 print('REVIEW SEAL PASS')
PY
TMP=$(mktemp -d "$(dirname "$HERE")/chain_expanded_replay_XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$TMP"/
cp -a "$HERE/snapshot" "$TMP/"
CPU=${REVIEW_CPU:-4}
taskset -c "$CPU" python -u "$TMP/provenance.py"
taskset -c "$CPU" python -u "$TMP/audit.py"
taskset -c "$CPU" python -u "$TMP/adversarial_tests.py"
taskset -c "$CPU" python -u "$TMP/audit_obstruction.py"
python - "$HERE" "$TMP" <<'PY'
from pathlib import Path
import json,sys
old,new=map(Path,sys.argv[1:]);a=json.loads((old/'SUMMARY.json').read_text());b=json.loads((new/'SUMMARY.json').read_text())
assert a['results']==b['results'];assert a['status']==b['status']
assert json.loads((old/'physical_premises.json').read_text())==json.loads((new/'physical_premises.json').read_text())
print('CLEAN REPLAY PASS', b['results'])
PY
