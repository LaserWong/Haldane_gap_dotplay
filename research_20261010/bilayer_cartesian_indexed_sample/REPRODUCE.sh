#!/usr/bin/env bash
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
: "${1:?A fresh output directory and approved 60 CPU second budget are required}"
mkdir "$1"; out="$(cd "$1" && pwd)"
cp "$src/geometry_8x4.txt" "$src/reference_coefficients.txt" "$out/"
mkdir "$out/run"
(ulimit -v 524288; taskset -c 6 g++ -O2 -std=c++17 "$src/benchmark.cpp" -lgmpxx -lgmp -o "$out/benchmark")
(ulimit -t 60; ulimit -v 262144; taskset -c 6 "$out/benchmark" "$out/run") 2>"$out/run/run.log"
python - "$src" "$out" <<'PY'
from pathlib import Path
import json,sys
src,out=map(Path,sys.argv[1:])
for family in ('N','F','L'):
 assert (src/'run'/f'rules_{family}.bin').read_bytes()==(out/'run'/f'rules_{family}.bin').read_bytes()
for name in ('fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json'):
 assert json.loads((src/'run'/name).read_text())==json.loads((out/'run'/name).read_text())
a=json.loads((src/'run/summary.json').read_text());b=json.loads((out/'run/summary.json').read_text())
assert len(b['families'])==3
for x,y in zip(a['families'],b['families']):
 for key in ('name','rules','blocks','embeddings','fourfold_stabilized_blocks','samples','rule_hits','maximum_rule_hits','lookup_calls','lookup_misses','checksum_exact_Gram_bilinear','sample_occupied_edge_classes'):
  assert x[key]==y[key],key
print('Exact rules, fixtures and sampled bilinear checksums reproduced.')
PY
