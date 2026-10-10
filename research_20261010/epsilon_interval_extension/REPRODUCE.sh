#!/bin/sh
# Run from repository root. New output is confined to epsilon_interval_extension.
set -eu
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/epsilon_interval_extension/extend_interval.py
python research_20261010/epsilon_interval_extension/extend_interval.py --name frontier --segments \
 '1/125:33/4000:1/125' '33/4000:17/2000:17/2000' \
 '17/2000:171/20000:17/2000' '171/20000:43/5000:17/2000' \
 '43/5000:173/20000:17/2000' '173/20000:87/10000:17/2000' \
 '87/10000:7/800:9/1000' '7/800:11/1250:9/1000'
