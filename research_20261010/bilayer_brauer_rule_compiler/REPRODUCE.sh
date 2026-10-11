#!/usr/bin/env bash
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
: "${1:?Fresh destination and approved 60 CPU second budget required}"
: "${2:?Verified sealed Cartesian run directory required}"
mkdir "$1"; out="$(cd "$1" && pwd)"; ref="$(cd "$2" && pwd)"
cp "$src/geometry_8x4.txt" "$src/reference_coefficients.txt" "$out/"; mkdir "$out/run"
(ulimit -v 524288; taskset -c 6 g++ -O2 -std=c++17 "$src/brauer.cpp" -lgmpxx -lgmp -o "$out/brauer")
(ulimit -t 60; ulimit -v 262144; taskset -c 6 "$out/brauer" "$out/run" "$ref") 2>"$out/run/run.log"
python - "$src" "$out" <<'PY'
from pathlib import Path
import sys,json
src,out=map(Path,sys.argv[1:])
for fam in ('N','F','L'):
 assert (src/'run'/f'diagrams_{fam}.bin').read_bytes()==(out/'run'/f'diagrams_{fam}.bin').read_bytes()
for name in ('fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json'):
 assert json.loads((src/'run'/name).read_text())==json.loads((out/'run'/name).read_text())
s=json.loads((out/'run/summary.json').read_text());assert len(s['families'])==3 and all(x['samples']==512 for x in s['families'])
print('Exact diagrams, physical fixtures and all sampled channels reproduced.')
PY
