#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python - "$HERE" <<'PY'
from pathlib import Path
import hashlib,json,sys
p=Path(sys.argv[1]);root=p.parents[1]
for name,h in json.loads((p/'FROZEN_MANIFEST.json').read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
for name,h in json.loads((p/'EXTERNAL_INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,name
print('All frozen inputs preserved')
PY
TMP="$(mktemp -d "$HERE/../chain_rank195_replay.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
cp "$HERE"/*.py "$TMP/"
python "$TMP/build_reference.py"
python "$TMP/diagnose_initial.py"
python "$TMP/triplet_witness.py"
python "$TMP/obstruction.py"
python "$TMP/denominator_obstruction.py"
python "$TMP/necessary_numerator_target.py"
python "$TMP/verify.py"
python "$TMP/verify_target.py"
python - "$HERE" "$TMP" <<'PY'
from pathlib import Path
import json,sys
old,new=map(Path,sys.argv[1:])
def read(p,n):return json.loads((p/n).read_text())
assert read(old,'expanded_moments.json')==read(new,'expanded_moments.json')
a,b=read(old,'expanded_inputs.json')[0],read(new,'expanded_inputs.json')[0]
for k in ['comparison_endpoints','alpha','B','omitted_cutoff','complete_reference_bins','remaining_count']:
 assert a['small']['expanded_band'][k]==b['small']['expanded_band'][k],k
assert read(old,'triplet_witness.json')==read(new,'triplet_witness.json')
for name in ['obstruction_g1d4.json','denominator_obstruction_g1d4.json','necessary_numerator_target_g1d4.json']:
 a,b=read(old,name),read(new,name)
 for k in ['intervals','maximum_postcycle_joint_upper','beta_ge12_second_argument_upper']:
  assert a[k]==b[k],(name,k)
print('Clean replay reproduced all exact endpoints, triplet witnesses and obstruction intervals')
PY
