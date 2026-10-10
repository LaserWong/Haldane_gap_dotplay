#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_inputs.py
python audit_physical.py --part ground > logs/ground.log 2>&1
python audit_physical.py --part translation > logs/translation.log 2>&1
python audit_frontier.py > logs/scalar.log 2>&1
python check_bounded_grid.py > logs/grid.log 2>&1
python finalize_review.py
