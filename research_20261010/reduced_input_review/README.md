# Reduced largest-seed input: independent PASS

See [REVIEW.md](REVIEW.md) for the proof, exact accepted bounds, dataflow and
scope. Run `REPRODUCE.sh` for all checks.

- `results/all_size_replay.json`: eight exact, all-integer-square certificates
- `results/physical_first_moments.json`: independent largest G/K and G/A checks
- `results/fs_reconstruction.json`: q4-only F/S construction, no q6 contraction
- `results/read_boundary.json`: isolated absent/poisoned-file acceptance tests
- `results/path_ledger.json`: correlated cancellation and exact basepoints
- `INPUT_SHA256.json`: immutable producer and smaller-patch inputs
- `INHERITED_REVIEWS.json`: accepted upper-trace and short-size proof provenance

One largest trial has practically the same strength as 193 trial directions.
The maximum patch requiring full residual and complete-tail certification is
8×4 rungs instead of 8×8; the physical largest numerator patch remains 8×8.
