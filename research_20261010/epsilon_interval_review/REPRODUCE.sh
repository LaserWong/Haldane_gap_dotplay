#!/bin/sh
# Run from the repository root. Writes only into epsilon_interval_review.
set -eu
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/epsilon_interval_review/audit_interval.py \
  > research_20261010/epsilon_interval_review/audit.log 2>&1
cat research_20261010/epsilon_interval_review/audit.log
