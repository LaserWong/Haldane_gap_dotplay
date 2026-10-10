#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python verify_manifest.py
python audit.py > logs/full_replay.log 2>&1
cat logs/full_replay.log
python test_adversarial.py > logs/adversarial.log 2>&1
cat logs/adversarial.log
