#!/bin/sh
# Proposal only. Requires root-created, reviewed authority and prepaid ledger.
set -eu
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
exec /usr/bin/taskset -c 6 /usr/bin/prlimit --cpu=99:100 --as=67108864:134217728 -- /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 /workspace/shared/haldane_active/research_20261010/bilayer_streaming_hash_revision/outer.py
