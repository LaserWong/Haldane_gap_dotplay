#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python verify_manifest.py
python plot_overview.py --check-only
python test_snapshot_guards.py
scratch=$(mktemp -d /tmp/haldane-overview-stage8-replay.XXXXXX)
trap 'rm -rf "$scratch"' EXIT
python plot_overview.py --output-dir "$scratch"
for stem in certified_bounds ordinary_interval_pieces trial_space_counts aklt_reference_scope recipe_upper_caps; do
  cmp "$stem.png" "$scratch/$stem.png"
  cmp "$stem.pdf" "$scratch/$stem.pdf"
done
python verify_manifest.py
printf 'PASS: all ten rendered files reproduce byte-for-byte; sealed artifacts are unchanged.\n'
