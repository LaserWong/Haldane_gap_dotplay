#!/bin/sh
set -eu
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib,pathlib
p=pathlib.Path('.')
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,f
PY
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
cp audit.py "$scratch/"
cp -r snapshot "$scratch/"
python "$scratch/audit.py"
python - "$scratch/audit.json" <<'PY'
import json,sys
x=json.load(open('audit.json'));y=json.load(open(sys.argv[1]))
for a in (x,y):
 for k in ('seconds','peak_rss_kib'):a.pop(k,None)
assert x==y
print('CLEAN EXACT REPLAY PASS')
PY
