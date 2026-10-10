#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_manifest.py
python audit.py | tee logs/audit.log
python test_adversarial.py | tee logs/adversarial.log
python test_bivariate.py | tee logs/bivariate.log
