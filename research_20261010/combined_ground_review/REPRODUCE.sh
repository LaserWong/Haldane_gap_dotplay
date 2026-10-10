#!/bin/sh
set -eu
cd "$(dirname "$0")"
ulimit -v 1048576
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_seals.py
export COMBINED_REVIEW_OUTPUT="$(mktemp -d /tmp/combined-ground-review.XXXXXX)"
python audit_combination.py
python audit_grid.py
python audit_comparison.py
printf 'Replayed outputs: %s\n' "$COMBINED_REVIEW_OUTPUT"
