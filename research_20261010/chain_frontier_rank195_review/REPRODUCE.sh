#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
python - "$HERE" <<'PY'
import sys,json,hashlib
from pathlib import Path
p=Path(sys.argv[1]);f=p/'MANIFEST_SHA256.json'
if f.exists():
 for n,h in json.loads(f.read_text()).items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
 print('REVIEW SEAL PASS')
PY
TMP=$(mktemp -d "$(dirname "$HERE")/chain_rank195_replay_XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$TMP/"
cp -a "$HERE/snapshot" "$TMP/"
CPU=${REVIEW_CPU:-4}
taskset -c "$CPU" python -u "$TMP/provenance.py"
taskset -c "$CPU" python -u "$TMP/audit.py"
taskset -c "$CPU" python -u "$TMP/audit_obstructions.py"
taskset -c "$CPU" python -u "$TMP/adversarial_tests.py"
python - "$HERE" "$TMP" <<'PY'
from pathlib import Path
import json,sys
old,new=map(Path,sys.argv[1:])
for name in ['physical_premises.json','triplet_review.json','physical_endpoint_review.json']:
 assert json.loads((old/name).read_text())==json.loads((new/name).read_text()),name
for name in ['obstruction_review.json','adversarial_tests.json']:
 a=json.loads((old/name).read_text());b=json.loads((new/name).read_text())
 for k in ['seconds','peak_rss_kib']:a.pop(k,None);b.pop(k,None)
 assert a==b,name
print('CLEAN RANK195 REPLAY PASS')
PY
