#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo 'Run only in a disposable copy; exact raw outputs reproduce, resource metadata changes.'
ulimit -v 716800
ulimit -t 600
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
CPU=$(python -c 'import os;print(min(os.sched_getaffinity(0)))')
taskset -pc "$CPU" $$ >/dev/null
python build_displacement_sources.py plus > source_checks_plus.log
g++ -O3 -std=c++17 contract_displacements.cpp -lgmpxx -lgmp -o contract_displacements
./contract_displacements sources_plus.txt 2 0 1 > fixtures_plus.out 2> fixtures_plus.log
./contract_displacements sources_plus.txt 4 0 1 2 3 >> fixtures_plus.out 2>> fixtures_plus.log
./contract_displacements sources_plus.txt 6 0 1 2 3 4 5 >> fixtures_plus.out 2>> fixtures_plus.log
./contract_displacements sources_plus.txt 24 0 1 12 > benchmark_n24_plus.out 2> benchmark_n24_plus.log
./contract_displacements sources_plus.txt 24 2 3 4 5 6 7 8 9 10 11 > remaining_n24_plus.out 2> remaining_n24_plus.log
python verify_fourier.py > fourier_verify.log
python verify_scalar.py > scalar_verify.log
echo 'PASS exact displacements, Fourier intervals, and recipe-specific scalar screen.'
