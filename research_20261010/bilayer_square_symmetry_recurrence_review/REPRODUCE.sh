#!/bin/sh
set -eu
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib,pathlib
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()==h,f
PY
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp check.py "$tmp/"
cp -r snapshot "$tmp/"
python "$tmp/check.py"
cmp checks.json "$tmp/checks.json"
echo 'CLEAN EXACT REPLAY PASS'
