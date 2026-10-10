#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - "$HERE" <<'PY'
import json,hashlib,sys
from pathlib import Path
p=Path(sys.argv[1]);root=p.parents[1]
for n,h in json.loads((p/'FROZEN_MANIFEST.json').read_text()).items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
for n,h in json.loads((p/'EXTERNAL_INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==h,n
PY
TMP="$(mktemp -d "$HERE/../chain_numerator_replay.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$HERE/contract.cpp" "$TMP/"
(ulimit -v 716800; ulimit -t 600; g++ -O2 -std=c++17 "$TMP/contract.cpp" -lgmpxx -lgmp -o "$TMP/contract")
python "$TMP/probe.py"
python "$TMP/prepare.py"
"$TMP/contract" "$TMP/packed_input.txt" "$TMP/cpp_probe" probe
"$TMP/contract" "$TMP/packed_input.txt" "$TMP/full" full
python "$TMP/evaluate.py"
python "$TMP/prepare_image_input.py" full packed_image_input.txt
"$TMP/contract" "$TMP/packed_image_input.txt" "$TMP/second_support" support
"$TMP/contract" "$TMP/packed_image_input.txt" "$TMP/second_probe" probe
"$TMP/contract" "$TMP/packed_image_input.txt" "$TMP/second" full
python "$TMP/evaluate_three.py"
python "$TMP/prepare_old_direction.py"
"$TMP/contract" "$TMP/packed_old_direction.txt" "$TMP/old_direction" full
python "$TMP/evaluate_four.py"
python "$TMP/prepare_image_input.py" second packed_second_image.txt
"$TMP/contract" "$TMP/packed_second_image.txt" "$TMP/energy_replay" energy
python "$TMP/replay_images.py"
python "$TMP/verify_certificates.py"
python - "$HERE" "$TMP" <<'PY'
import json,sys
from pathlib import Path
old,new=map(Path,sys.argv[1:])
for name in ['rayleigh.json','rayleigh_three.json','rayleigh_four.json']:
 a=json.loads((old/name).read_text());b=json.loads((new/name).read_text())
 for k in ['exact_rayleigh','new_delta','span_target_LDL_pivots']:
  assert a[k]==b[k],(name,k)
print('Clean replay reproduces all exact Rayleigh values and whole-span exclusions.')
PY
