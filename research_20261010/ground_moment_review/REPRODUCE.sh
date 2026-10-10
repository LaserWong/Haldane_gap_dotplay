#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python verify_manifest.py
python verify_inputs.py
python audit_direct.py | tee logs/direct_witnesses.log
python audit_ground.py | tee logs/ground.log
python audit_scalars.py | tee logs/scalars.log
python audit_dominance.py | tee logs/dominance.log
python independent_grid.py | tee logs/grid.log
python verify_inputs.py
