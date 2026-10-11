#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
exec /usr/bin/taskset -c 7 /usr/bin/prlimit --cpu=20:22 --as=67108864:134217728 -- /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 /workspace/shared/haldane_active/research_20261010/bilayer_full_m4_launch_review/check_startup.py
