#!/bin/sh
set -eu
cd "$(dirname "$0")"
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python criteria.py > exclusions.log
python examples.py > examples.log
python entropy_rank.py > entropy_rank.log
python residual_obstruction.py > residual_obstructions.log
cat exclusions.log examples.log entropy_rank.log residual_obstructions.log
