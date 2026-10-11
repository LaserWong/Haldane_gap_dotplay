#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p check
(ulimit -v 524288; ulimit -t 40; taskset -c 3 g++ -O2 -std=c++17 fixture.cpp -lgmpxx -lgmp -o check/fixture)
(ulimit -v 102400; ulimit -t 2; taskset -c 3 check/fixture ../bilayer_complete_residual_8x4/geometry_4x2.txt ignored 4 2 fixture) > check/fixture_4x2.json
(ulimit -v 102400; ulimit -t 3; taskset -c 3 check/fixture ../bilayer_complete_residual_8x4/geometry_8x4.txt reference_coefficients.txt 8 4 benchmark) > check/sample_8x4.json
python - <<'PY'
import json
for f in ['fixture_4x2.json','sample_8x4.json']:
 a=json.load(open(f));b=json.load(open('check/'+f))
 for x in (a,b):
  for k in list(x):
   if 'seconds' in k or k=='peak_rss_kib': x.pop(k)
 assert a==b,f
print('PASS: exact fixture and deterministic partial sample reproduced')
PY
