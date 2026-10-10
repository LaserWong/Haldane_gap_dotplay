#!/usr/bin/env bash
# Replay under limits, preserving all sealed outputs. ~30 seconds on the original CPU.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
RES=$(cd "$HERE/../.." && pwd)
DEST=${1:-"$HERE/replay_$(date -u +%Y%m%dT%H%M%SZ)"}
mkdir -p "$DEST"
RUN=(python "$HERE/run_limited.py")
"${RUN[@]}" g++ -O3 -std=c++17 -Wall -Wextra "$HERE/contract_third.cpp" -o "$DEST/contract_third"
"${RUN[@]}" g++ -O3 -std=c++17 -Wall -Wextra "$HERE/test_physical.cpp" -o "$DEST/test_physical"
for shape in 2x2 4x2 4x4 8x4 8x8; do
  timeout 610 "${RUN[@]}" "$DEST/contract_third" "$RES/large_seed_moments/geometry_$shape.txt" "$DEST/geometry_${shape}_origin.json" origin
done
for shape in 2x2 4x2 4x4; do
  timeout 610 "${RUN[@]}" "$DEST/contract_third" "$RES/large_seed_moments/geometry_$shape.txt" "$DEST/geometry_${shape}_full.json" full
  timeout 610 "${RUN[@]}" "$DEST/test_physical" "$RES/large_seed_moments/geometry_$shape.txt" "$HERE/physical_local_A.txt" "$DEST/physical_$shape.json"
done
python - "$HERE" "$DEST" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:])
for path in new.glob('*.json'):
    saved=old/path.name
    if not saved.exists():continue
    a,b=json.loads(path.read_text()),json.loads(saved.read_text())
    for key in ('F','S','V','W','X','Y','Z','fixture'):
        if key in a:assert a[key]==b[key],(path.name,key)
print('PASS all replayed exact geometry and physical fixtures')
PY
for shape in 4x4 8x4 8x8; do
  input="$RES/low_band/frontier_g009/block1_${shape}_g9d100.json"
  geometry="$HERE/geometry_${shape}_origin.json"
  timeout 610 "${RUN[@]}" python "$HERE/exact_filter.py" "$input" "$geometry" "$DEST/filtered_${shape}_g9d100.json"
  timeout 610 "${RUN[@]}" python "$HERE/enlarged_numerator.py" "$input" "$geometry" "$DEST/enlarged_${shape}_g9d100.json"
done
python - "$HERE" "$DEST" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:])
for path in list(new.glob('filtered_*.json'))+list(new.glob('enlarged_*.json')):
    a,b=json.loads(path.read_text()),json.loads((old/path.name).read_text())
    for rec in (a,b):
        for key in ('seconds','peak_rss_kib'):rec.pop(key,None)
    assert a==b,path.name
print('PASS all rational trial outputs (excluding resource diagnostics)')
PY
printf 'Replay retained in %s\n' "$DEST"
