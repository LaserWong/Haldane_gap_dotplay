#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
ulimit -v 1048576
CPU=$(python -c 'import os; print(min(os.sched_getaffinity(0)))')
taskset -pc "$CPU" "$$" >/dev/null
python rebuild_d26.py >d26_build.log 2>&1
g++ -O2 contract_d26.cpp -lgmpxx -lgmp -o contract_d26
./contract_d26 d26_rebuilt_blocks.txt >d26_fresh.out 2>d26_contract.log
python independent_aklt.py >aklt_run.log 2>&1
python independent_uniform.py >uniform_run.log 2>&1
python - <<'PY'
import json
for f in ['d26_rebuild_results.json','aklt_independent_results.json','uniform_independent_results.json']:
 x=json.load(open(f)); assert x['status']=='PASS'
 print(f,x['status'],f"{x['seconds']:.3f}s",x['peak_kb'],'KiB')
PY
