#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
ulimit -v 1048576
ulimit -t 300
CPU=$(python -c 'import os;print(min(os.sched_getaffinity(0)))')
taskset -cp "$CPU" $$ >/dev/null
python verify_provenance.py > provenance.log
python independent_trials.py > independent_trials.log
python independent_d26.py > independent_d26.log
g++ -O2 contract_d26.cpp -lgmpxx -lgmp -o contract_d26
./contract_d26 d26_blocks.txt > d26_contractions.out 2> d26_contractions.log
cmp d26_contractions.out ../uniform_seed_size_diagnostics/mps_lengths.out
python independent_scalar.py > independent_scalar.log
python regressions.py > regressions.log
python verify_provenance.py > provenance_after.log
echo 'PASS: independent integer trials, D26, scalar half-line coverage, regressions, and frozen-source provenance.'
