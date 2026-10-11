#!/usr/bin/env bash
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
: "${1:?Provide a fresh output directory and an approved 30 CPU second local budget}"
mkdir "$1"; out="$(cd "$1" && pwd)"; mkdir "$out/rules" "$out/validation"
(ulimit -v 524288; taskset -c 6 g++ -std=c++17 -O2 "$src/compiler.cpp" -o "$out/compiler"; taskset -c 6 g++ -std=c++17 -O2 "$src/validate.cpp" -o "$out/validate")
(ulimit -t 7; ulimit -v 262144; taskset -c 6 "$out/compiler" "$out/rules") 2>"$out/rules/run.log"
(ulimit -t 23; ulimit -v 262144; taskset -c 6 "$out/validate" "$out/validation") 2>"$out/validation/run.log"
python - "$src" "$out" <<'CHECK'
import json,sys
from pathlib import Path
src,out=map(Path,sys.argv[1:])
for fam in ('N','F','L'):
 assert (src/'run'/f'rules_{fam}.bin').read_bytes()==(out/'rules'/f'rules_{fam}.bin').read_bytes()
for name in ('fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json'):
 assert json.loads((src/'validation'/name).read_text())==json.loads((out/'validation'/name).read_text())
assert json.loads((out/'validation'/'validation.json').read_text())['complete']
print('Exact local rules and all fifteen fixture terms reproduced.')
CHECK
