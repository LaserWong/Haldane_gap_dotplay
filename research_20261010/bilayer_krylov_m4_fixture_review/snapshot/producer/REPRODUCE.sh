#!/usr/bin/env bash
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
: "${1:?Provide a fresh output directory}"
mkdir "$1"
out="$(cd "$1" && pwd)"
(ulimit -v 524288; taskset -c 3 g++ -std=c++17 -O2 "$src/fixture.cpp" -o "$out/fixture")
(ulimit -t 5; ulimit -v 102400; taskset -c 3 "$out/fixture" "$out") 2>"$out/run.log"
python - "$src" "$out" <<'CHECK'
from pathlib import Path
import json,sys
src,out=map(Path,sys.argv[1:])
for name in ('fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json'):
    assert json.loads((src/name).read_text())==json.loads((out/name).read_text()),name
print('All exact fixture data reproduced.')
CHECK
