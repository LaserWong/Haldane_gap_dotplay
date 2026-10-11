#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 ../../reproducibility/stage11_exact_evidence/materialize.py --repo-root ../..
python verify_manifest.py
python ../overview_stage15/plot_overview.py --check-only
python check_transport.py --check-only
python plot_overview.py --check-only
python test_snapshot_guards.py
scratch=$(mktemp -d /tmp/haldane-overview-stage16-replay.XXXXXX)
trap 'rm -rf "$scratch"' EXIT
python plot_overview.py --output-dir "$scratch"
for stem in certified_bounds ordinary_interval_pieces trial_space_counts aklt_reference_scope recipe_upper_caps mps_recipe_windows chain_window_refinement accepted_recipe_scope uniform_gap_frontier uniform_theorem_comparison bilayer_frontier stage13_trial_dimensions conditional_uniform_bounds bilayer_short_size_bounds bilayer_ground_endpoints bilayer_complete_matrix_dimensions stage16_scope_comparison; do
  cmp "$stem.png" "$scratch/$stem.png"
  cmp "$stem.pdf" "$scratch/$stem.pdf"
done
python verify_manifest.py
printf 'PASS: all thirty-four rendered files reproduce byte-for-byte; sealed artifacts are unchanged.\n'
