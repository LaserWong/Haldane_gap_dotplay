#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python verify_manifest.py
out=$(mktemp -d "$PWD/replay_unsealed_XXXXXX")
export REVIEW_OUTPUT="$out/results"
mkdir "$REVIEW_OUTPUT"
python audit.py > "$out/audit.log" 2>&1
python test_adversarial.py > "$out/adversarial.log" 2>&1
python verify_manifest.py
cat "$out/audit.log" "$out/adversarial.log"
printf '\nFresh output: %s\n' "$out"
