#!/bin/bash
# one block: optional eigensolver stage, then certification stage (separate processes)
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python3 run.py eig "$@" && python3 run.py "$@"
