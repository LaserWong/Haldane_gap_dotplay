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
TMP=$(mktemp -d "$(dirname "$HERE")/chain_pair_block_replay_XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$TMP/"
cp -a "$HERE/pair_snapshot" "$HERE/block_snapshot" "$TMP/"
CPU=${REVIEW_CPU:-4}
for SCRIPT in provenance audit adversarial_tests check_inherited_quantum; do
 taskset -c "$CPU" python -u "$TMP/$SCRIPT.py"
done
python - "$HERE" "$TMP" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:])
for n in ['certified_numerator.json','exact_reviews.json','inherited_quantum_diagnostic.json']:
 assert json.loads((old/n).read_text())==json.loads((new/n).read_text()),n
for n in ['SUMMARY.json','adversarial_tests.json']:
 a=json.loads((old/n).read_text());b=json.loads((new/n).read_text())
 for k in ['seconds','cpu_seconds','peak_rss_kib']:a.pop(k,None);b.pop(k,None)
 assert a==b,n
print('CLEAN PAIR/BLOCK REPLAY PASS')
PY
