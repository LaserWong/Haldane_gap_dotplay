#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
# 1 GiB virtual-address limit; each Python verifier also pins one permitted CPU.
ulimit -v 1048576
CPU=$(python -c 'import os; print(min(os.sched_getaffinity(0)))')
g++ -O2 mps_small.cpp -lgmpxx -lgmp -o mps_small
taskset -c "$CPU" ./mps_small ../../audit/mps/mps_blocks.txt > mps_small.out 2> mps_small.log
# Trial vectors are fixed data. No eigensolver is needed for certificate replay.
python verify_uniform_screen.py
python verify_aklt.py
