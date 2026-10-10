#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_manifest.py
python -u audit_recombinations.py | tee logs/replay.log
python check_grid_diagnostic.py | tee -a logs/replay.log
python verify_manifest.py
