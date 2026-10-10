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
TMP=$(mktemp -d "$(dirname "$HERE")/chain_m8_numerator_replay_XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$TMP/"
cp -a "$HERE/snapshot" "$TMP/"
CPU=${REVIEW_CPU:-4}
for SCRIPT in provenance audit audit_nested structural_checks adversarial_tests; do
 taskset -c "$CPU" python -u "$TMP/$SCRIPT.py"
done
python - "$HERE" "$TMP" <<'PY'
from pathlib import Path
import json,sys
old,new=map(Path,sys.argv[1:])
for name in ['independent_moments.json','four_span_review.json','nested_span_review.json','overflow_and_structure.json']:
 assert json.loads((old/name).read_text())==json.loads((new/name).read_text()),name
for name in ['SUMMARY.json','adversarial_tests.json']:
 a=json.loads((old/name).read_text());b=json.loads((new/name).read_text())
 for k in ['seconds','cpu_seconds','peak_rss_kib']:a.pop(k,None);b.pop(k,None)
 assert a==b,name
print('CLEAN M8 NUMERATOR REPLAY PASS')
PY
