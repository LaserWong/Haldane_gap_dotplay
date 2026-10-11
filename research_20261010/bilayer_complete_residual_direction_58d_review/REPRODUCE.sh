#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -f MANIFEST_SHA256.json ]; then /usr/bin/python3 - <<'PY'
import hashlib,json
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
PY
fi
/usr/bin/python3 check_fixture.py
mkdir -p check
/usr/bin/python3 measure.py check/algebra_metrics.json 256 60 /usr/bin/python3 assemble.py check/audit.json
/usr/bin/python3 - <<'PY'
import json
x=json.load(open('audit.json'));y=json.load(open('check/audit.json'))
for a in [x,y]:
 for k in ['cpu_seconds','peak_rss_kib']:a.pop(k,None)
assert x==y
print('PASS sealed physical inputs and cached58D exact replay; no physical rerun')
PY
