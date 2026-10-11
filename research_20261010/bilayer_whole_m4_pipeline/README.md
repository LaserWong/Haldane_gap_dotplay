# Bounded whole-moment pipeline: producer handoff

2026-10-11 03:14 UTC / 2026-10-10 23:14 EDT. This package is a producer correctness/sample gate, not a full 8×4 moment result or production-ready checkpoint implementation.

## Result

All six strengthened complete physical fixtures pass: localized, translation-symmetrized, and generic B/L/R/M sources on 4×2 and 5×2 periodic rungs. Every one of the fifteen signed high-sector terms agrees with independently assembled physical operator-vector expressions, and m0 through m4 agree with direct physical H and H² vectors. The entire low-sector ψ, χ and z vectors agree; Cm and E†m agree as full q4 vectors. Exact occupied-anchor/permutation and reduced/full normalization checks pass for invariant sources. The physical edge matrix is reconstructed from the spin-half convention by the inherited, reviewed Cartesian fixture. Independent review of this new integration remains separate.

Eight disjoint dispersed batches cover exactly 512 q6 and 128 q4 targets, plus 64 q2 targets and vacuum in the first batch. Every batch repeats its targets and compares all 22 exact scalar accumulators, including all fifteen named terms. No 8×4 complete support sweep or complete cache was performed. Sample scalar values labeled moments in JSON are partial, mixed-sector sample sums: `moments_are_full_physical_fixture_only=false` explicitly forbids treating these as physical moments.

Guarded computation totals: 26.904021 CPU seconds (wait4), 27.612707469 wall seconds; maximum RSS 41,604 KiB. Conservative reservation charge is 257/300 CPU seconds, including a failed 35-second reservation and one second reserved for metadata summarization. Admission soft stop is 270 seconds. The compilation cap was separately 512 MiB, affinity CPU6; compile CPU was not recorded by wait4 and is not included in these numerical runtime totals. No further computation is requested by this report.

## Geometry and units correction

The 8×4 torus has 32 rungs. There are 64 spatial nearest-neighbor edges in each layer, hence 128 physical intralayer spin bonds. Each spatial edge supplies one two-rung bilayer interaction. The old sealed design's phrase “64 rung edges” is superseded by this explicit convention; its immutable file is not changed. H′=Q+(g/2)(C+C†+D), g=11/100; T=200H′=200Q+11(C+C†+D). Full Hilbert dimension is 4^32. All fixture moments are unnormalized exact T moments.

## Contents and entry points

- whole.cpp: integration, general occupation/pairing action, source/χ/v builders, full fixtures, bounded sample.
- brauer_snapshot.cpp and reference/: snapshots of the accepted direct Cartesian/Brauer derivations. Original seals remain untouched.
- geometry_8x4.txt, witness57.txt, reference_coefficients.txt: fixed accepted 57D source inputs. witness order is vacuum,B14,L14,R14,M14. cR and cM are distinct.
- run_guarded.py, BUDGET_LEDGER.json: monotone pre-reservation, external CPU/wall guard, process-group kill and wait4 accounting. Each attempted numerical batch remains charged its entire reservation.
- runs/checked_*: strengthened complete fixtures and mutation checks.
- runs/sample_offset0_fixed and sample_offset1 through sample_offset7: successful cold/repeated samples.
- runs/sample_offset0: retained failed target-generator attempt, never aggregated into successful sample.
- SUMMARY.json and COST_AND_LIMITS.md: empirical counters, costs and production limitations.
- PROOF.md: identities, convention, bounds and normalization.

Rebuilding uses g++ -O2 -std=c++17 whole.cpp -lgmpxx -lgmp -o whole under the separately authorized compiler resource cap. Replay requires its own authorization and should use a new output/ledger directory; do not run the producer guard against this frozen directory. Executable arguments: `whole fixture generic OUTPUT INPUT RULEDIR CAP 5`; or `whole sample sample OUTPUT INPUT RULEDIR CAP OFFSET 64 16`. INPUT is this package, RULEDIR is ../bilayer_brauer_rule_compiler/run. The code's internal deadline is CAP−2 seconds; the external guard is still required.

## Failure history and provenance

The first six fixtures preceded added full-vector/normalization/permutation diagnostics; `whole_initial_fixture.cpp` preserves that source. The six checked fixtures passed with those stronger diagnostics. Thereafter only the large sample q4 cache cap was tightened to 4096 and the large-sample generator corrected. Small fixture logic was unchanged. Early numerical records did not hash their executable/source at launch; they must not be represented as cryptographically bound replay records. Successful large samples bind both source and executable SHA256 at launch.

The first large sample completed its q6/q4 steps but aborted on its first q2 target because the q2 unranking wrote target[k] rather than target[k−1]. `whole_failed_low_sampler.cpp` and the failed logs remain. This was not a physical identity mismatch. The corrected generator exhaustively checks all 496 q2 ranks for ordering, unique coverage and rank/unrank equality before each successful sample. The failed 35-second reservation was not refunded although its wait4 CPU was 0.698591 seconds. The final source change and final sample executable are hash-bound in the eight successful records.

## Explicit remaining work

No serialization/restart round-trip or exactly-once resumed accumulation proof exists here. Checkpoint JSON is diagnostic, not a production resume format. No full accepted 8×4 m0/m1/m2 replay was performed; it is mandatory in eventual production. Per-operator timing and per-term GMP counters are not separately recorded; counters are aggregate, builder timers are nested/inclusive. No F/L left-m skip optimization was used. No independent 8×4 whole-action comparison is claimed by the cold/repeated equality. The independent reviewer has a separately authorized physical dense-reference fixture gate.
