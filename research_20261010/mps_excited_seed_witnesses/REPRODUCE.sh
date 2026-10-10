#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo 'Run in a disposable sibling copy: timing/metadata outputs will be replaced.'
ulimit -v 1048576
ulimit -t 600
CPU=$(python -c 'import os;print(max(os.sched_getaffinity(0)))')
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
taskset -pc "$CPU" $$ >/dev/null
python build_sources.py > source_checks.log
g++ -O3 -std=c++17 contract_sources.cpp -lgmpxx -lgmp -o contract_sources
./contract_sources sources.txt 24 > contractions_n24.out 2> contractions_n24.log
g++ -O3 -std=c++17 contract_ground.cpp -lgmpxx -lgmp -o contract_ground
./contract_ground ../../audit/mps/mps_blocks.txt > ground_lengths.out 2> ground_lengths.log
python verify_witnesses.py > witness_verify.log
python verify_scalar.py > scalar_verify.log
(
 cd longitudinal_extension
 python build_longitudinal.py > source_checks.log
 g++ -O3 -std=c++17 contract_longitudinal.cpp -lgmpxx -lgmp -o contract_longitudinal
 ./contract_longitudinal sources.txt 24 > contractions_n24.out 2> contractions_n24.log
 python verify_longitudinal.py > verify_longitudinal.log
 python verify_scalar.py > scalar_verify.log
 python conditional_trace_budget.py > conditional_trace_budget.log
)
(
 cd momentum_extension
 bash REPRODUCE.sh
)
(
 cd singlet_completion
 python verify_singlet.py > singlet_verify.log
 python verify_scalar.py > scalar_verify.log
)
echo 'PASS physical and scalar reproductions. See preserved manifests for frozen identities.'
