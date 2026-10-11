#!/bin/sh
set -eu
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib,pathlib
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()==h,f
PY
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp audit.py "$tmp/"
cp -r snapshot "$tmp/"
python "$tmp/audit.py"
python - "$tmp/audit.json" <<'PY'
import json,sys
a=json.load(open('audit.json'));b=json.load(open(sys.argv[1]))
for x in (a,b):
 for k in ('cpu_seconds','peak_rss_kib'):x.pop(k,None)
assert a==b
print('CLEAN NEW-COUPLING PHYSICAL AND SCALAR REPLAY PASS')
PY
