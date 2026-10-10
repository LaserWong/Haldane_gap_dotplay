#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
ulimit -v 1048576
ulimit -t 600
python verify_point.py
out="replay_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir "$out"
taskset -c 5 g++ -O3 -std=c++17 residual_scalar.cpp -o "$out/residual_scalar" -lgmpxx -lgmp
timeout 610 taskset -c 5 "$out/residual_scalar" geometry_8x4.txt "$out/residual_8x4.json" ground_8x4_coefficients.txt origin 2>"$out/run.log"
python verify_point.py "$out/residual_8x4.json"
