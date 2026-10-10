#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ -e MANIFEST_SHA256.json ]]; then python verify_manifest.py; fi
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
ulimit -v 1048576
ulimit -t 600
python verify_dependencies.py
if [[ -e INPUT_SHA256.json ]]; then python verify_inputs.py; fi
taskset -c 6 python audit_local.py > local.log
taskset -c 6 g++ -std=c++17 -O3 -UNDEBUG audit_residual.cpp -lgmpxx -lgmp -o audit_residual
for mode in full origin; do
 taskset -c 6 ./audit_residual ../third_moment_review/results/geometry_4x2.txt independent_fixture_coefficients.txt independent_fixture_${mode}.json "$mode"
 for shape in 2x2 3x2; do
  taskset -c 6 ./audit_residual geometry_${shape}.txt coeff_${shape}.txt independent_${shape}_${mode}.json "$mode"
 done
done
if [[ -e snapshot/PHYSICAL_MANIFEST.json ]]; then
 taskset -c 6 ./audit_residual snapshot/geometry_8x4.txt snapshot/ground_8x4_coefficients.txt independent_8x4.json origin > independent_8x4.log 2>&1
 taskset -c 6 python audit_assembly.py > assembly.log
fi
python verify_results.py
if [[ -e snapshot_scalar/SCALAR_MANIFEST.json ]]; then taskset -c 6 python audit_scalar.py > scalar.log; fi
if [[ -e snapshot_polynomial/POLYNOMIAL_MANIFEST.json ]]; then taskset -c 6 python audit_polynomial.py > polynomial.log; fi
python verify_inputs.py
