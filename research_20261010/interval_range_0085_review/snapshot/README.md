# Extend the complete ordinary-bilayer range to .085

Updated 2026-10-10 15:35 America/New_York (EDT, UTC−4) / 19:35 UTC.

Exact producer candidate, pending independent review. Sixteen new closed
intervals cover every real g∈[.08,.085] and every integer square side L≥2 at
uniform gap ≥.003365750386. Together with the preserved earlier 33 pieces,
the complete 49-piece [0,.085] union retains gap ≥.001945771244.

- Seven ground-only intervals cover [.08,.082], gap ≥.005978179134.
- Nine intervals add the existing odd-band denominator inputs for [.082,.085],
  gap ≥.003365750386.
- The largest 128-spin seed retains one filtered numerator contribution,
  augmented ground search dimension ≤30, full Hilbert dimension 2^128.
- Added denominator retained-state counts are 49/97; odd subspaces are 48/96
  dimensional, combined ground-search/odd spaces 59/125 dimensional.
- No largest-patch odd inputs, new sparse support, H³/H⁴, or new geometry.

[PROOF.md](PROOF.md) supplies the analytic fixed-center polynomial reconstruction,
all-real-g bounds, no-missed-state argument, all-size bridges, and input tradeoff.
[coverage_summary.json](coverage_summary.json) lists the pieces;
[replay_result.json](replay_result.json) records exact saved-vector replay with
no eigensolver calls. All 100 finite windows and 96 short-size rows passed.

Reproduce with:

    bash research_20261010/interval_range_0085/REPRODUCE.sh

The extracted workspace has no Git metadata. No publication is implied.

Final reproduction passed in 19.05 seconds, about 83.3 MiB peak RSS. The package
binds 96 direct inputs and ten prior review seals (1,165 files); polynomial,
filter, joint arithmetic, and 19 corruption guards passed. See
[reproduce.log](reproduce.log) and [reproduce_cost.json](reproduce_cost.json).
