#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
import json,hashlib
from pathlib import Path
for file,base in [('MANIFEST_SHA256.json',Path('.')),('INPUT_SHA256.json',Path('..'))]:
 for p,h in json.load(open(file)).items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p
print('Seals verified')
PY
taskset -c 3 python replay.py
python - <<'PY'
import json
x=json.load(open('result.json'));y=json.load(open('result_check.json'))
for k in ['seconds','peak_rss_kib']:x.pop(k);y.pop(k)
assert x==y
print('PASS exact short-size interval/moment/root replay agrees')
PY
