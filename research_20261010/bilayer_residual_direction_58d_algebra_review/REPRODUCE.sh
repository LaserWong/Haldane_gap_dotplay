#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -f MANIFEST_SHA256.json ]; then /usr/bin/python3 - <<'PY'
import hashlib,json
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
PY
fi
mkdir -p check
/usr/bin/python3 measure.py check/witness_metrics.json 256 6 /usr/bin/python3 audit.py --witness-only check/witness.json
/usr/bin/python3 - <<'PY'
import json,sys
from fractions import Fraction as F
sys.set_int_max_str_digits(0)
x=json.load(open('audit.json'));y=json.load(open('check/witness.json'));assert x['results']==y['results']
for t in x['targets']:
 c=t['fraction_free_certificate'];d=int(c['scale']);assert d>0;prev=1
 for p,m in zip(t['pivots'],c['positive_leading_minors']):
  m=int(m);assert m>0 and F(p)==F(m,prev*d)>0;prev=m
assert json.load(open('integration.json'))['all_nine_producer_LDL_results_independently_accounted_for']
print('PASS fresh rational witnesses/count gates and sealed exact target certificates')
PY
