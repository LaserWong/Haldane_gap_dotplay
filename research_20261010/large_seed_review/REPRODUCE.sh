#!/bin/sh
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_snapshot.py
c++ -std=c++17 -O2 -Wall -Wextra -fsanitize=undefined -fno-sanitize-recover=all rebuild_geometry.cpp -o rebuild_geometry
python rebuild_geometry.py > logs/geometry.log 2>&1
python audit_large.py --part ground > logs/ground.log 2>&1
python audit_large.py --part translation > logs/translation.log 2>&1
python audit_tail_trace.py --part local > logs/local.log 2>&1
python audit_tail_trace.py --part patch > logs/patch.log 2>&1
python audit_tail_trace.py --part trace > logs/trace.log 2>&1
python audit_bridges.py > logs/bridges.log 2>&1
