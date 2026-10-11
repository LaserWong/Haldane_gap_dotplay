#!/bin/sh
set -eu
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import json,hashlib
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h,f
PY
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp independent.py compare.py "$tmp/"
cp -r snapshot "$tmp/"
python "$tmp/independent.py"
python "$tmp/compare.py"
python - "$tmp" <<'PY'
from pathlib import Path
import json,sys
for f in ('independent.json','comparison.json'):
 a=json.load(open(f));b=json.load(open(Path(sys.argv[1])/f))
 for x in (a,b):
  for k in ('seconds','cpu_seconds','peak_rss_kib'):x.pop(k,None)
 assert a==b,f
print('CLEAN INDEPENDENT REPLAY PASS')
PY
