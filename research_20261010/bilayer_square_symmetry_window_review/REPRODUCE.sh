#!/bin/sh
set -eu
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib,pathlib
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()==h,f
PY
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp check.py INPUT_SHA256.json "$tmp/"
cp -r snapshot "$tmp/"
python "$tmp/check.py"
python - "$tmp/checks.json" <<'PY'
import json,sys
a=json.load(open('checks.json'));b=json.load(open(sys.argv[1]))
for x in (a,b):x.pop('cpu_seconds')
assert a==b
print('CLEAN REPLAY PASS')
PY
