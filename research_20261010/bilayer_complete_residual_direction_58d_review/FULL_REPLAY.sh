#!/bin/bash
# This script documents a new physical run. The flag does not itself grant authorization.
set -euo pipefail
[ "${SEPARATELY_AUTHORIZED_FULL_REPLAY:-}" = YES ] || { echo 'A new explicit full-physical-run authorization is required.' >&2; exit 2; }
cd "$(dirname "$0")"
out=$(mktemp -d "$PWD/physical_replay.XXXXXX")
/usr/bin/python3 measure.py "$out/compile.json" 512 40 g++ -O2 -std=c++17 independent.cpp -lgmpxx -lgmp -o "$out/independent"
/usr/bin/python3 measure.py "$out/runtime.json" 100 500 "$out/independent" ../bilayer_complete_residual_8x4/geometry_8x4.txt ../bilayer_residual_direction_outer_gate/reference_coefficients.txt 8 4 full_authorized 0 0 "$out/progress.json" > "$out/full.json"
/usr/bin/python3 - "$out/full.json" <<'PY'
import json,sys
x=json.load(open('full.json'));y=json.load(open(sys.argv[1]))
for a in [x,y]:
 for k in list(a):
  if 'seconds' in k or k=='peak_rss_kib':a.pop(k)
assert x==y
print('PASS separately authorized full independent replay')
PY
