# Continuous ordinary-bilayer interval extension

Updated 2026-10-10 15:14 America/New_York (EDT, UTC−4) / 19:14 UTC.

Exact candidate, pending independent interval review. Fifteen new adjoining
closed intervals cover .07≤g≤.078 for every integer square side L≥2, with gap
at least .002006633957. Together with the sealed earlier result, this gives
0≤g≤.078 with the unchanged uniform lower bound .001945771244.

- [Full proof and exact partition](PROOF.md)
- [Extension ledger](coverage_summary.json)
- [Exact replay and combined union](replay_result.json)
- [Reconstructed source provenance](source_validation.json)
- [Filter algebra tests](test_results.json)

Only one ground contribution is retained on each patch. Largest full Hilbert
space: 2^128. Original trial dimensions: 11/29/29. The single implicit filtered
largest vector has q≤6 and lies in an enlarged space of dimension at most 30.
The extension uses the existing largest full second moment; it does not retain
the older first-moment-only input restriction. No higher moments, large state
expansion, new geometry contraction, or full diagonalization were computed.

Reproduce from the repository root:

    bash research_20261010/interval_extension/REPRODUCE.sh

Every old sealed file remains untouched. This is a local candidate package;
no remote publication or claim of completed independent audit is made here.
