#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo 'Run in a disposable sibling copy; relies on verified momentum inputs.'
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python verify_singlet.py > singlet_verify.log
python verify_scalar.py > scalar_verify.log
