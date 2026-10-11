#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -f MANIFEST_SHA256.json ]; then python - <<'PY'
import hashlib,json
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
PY
fi
mkdir -p check/snapshot
cp independent.py audit.py base_kernel.inc init_kernel.inc instrumented.cpp check/
cp -a snapshot/. check/snapshot/
python measure.py check/compile_metrics.json 512 40 g++ -O2 -std=c++17 check/instrumented.cpp -lgmpxx -lgmp -o check/instrumented
python measure.py check/small_metrics.json 100 10 check/instrumented snapshot/geometry_4x2.txt check/small 4 2 fixture > check/small.json
mv check/small.vectors.txt check/small.vectors.txt.tmp
mv check/small.vectors.txt.tmp check/small.vectors.txt
python measure.py check/sample_metrics.json 100 10 check/instrumented snapshot/geometry_8x4.txt snapshot/producer/reference_coefficients.txt 8 4 benchmark > check/sample.json
python measure.py check/python_metrics.json 100 30 python check/independent.py
python - <<'PY'
import json
for f in ['independent.json','small.json','sample.json']:
 def strip(d):return {k:v for k,v in d.items() if 'seconds' not in k and k!='peak_rss_kib'}
 assert strip(json.load(open(f)))==strip(json.load(open('check/'+f))),f
print('PASS: independent physical replay and deterministic sample')
PY
python audit.py check/audit.json
cmp audit.json check/audit.json
