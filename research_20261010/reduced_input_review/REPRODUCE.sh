#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
ulimit -v 1048576
CPU=$(python -c 'import os; print(min(os.sched_getaffinity(0)))')
taskset -cp "$CPU" $$ >/dev/null
g++ -O2 -std=c++17 rebuild_fs_only.cpp -o rebuild_fs_only
python audit_dataflow.py | tee logs/dataflow.log
python audit_reduced.py | tee logs/replay.log
python test_read_boundary.py | tee logs/read_boundary.log
