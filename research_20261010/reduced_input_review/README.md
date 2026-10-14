# Reduced input requirements for the largest seed

See [REVIEW.md](REVIEW.md) for the proof, exact accepted bounds, dataflow and
scope. Run `REPRODUCE.sh` for all checks.

- `results/all_size_replay.json`: eight exact, all-integer-square certificates
- `results/physical_first_moments.json`: independent largest G/K and G/A checks
- `results/fs_reconstruction.json`: q4-only F/S construction, no q6 contraction
- `results/read_boundary.json`: isolated absent/poisoned-file acceptance tests
- `results/path_ledger.json`: correlated cancellation and exact basepoints
- `INPUT_SHA256.json`: immutable producer and smaller-patch inputs
- `INHERITED_REVIEWS.json`: accepted upper-trace and short-size proof provenance

The checked construction obtains nearly the same bound from one largest-seed trial as from 193 trial directions. Full residual and complete-tail certification are needed only through the 8×4 rung patch, while the physical numerator patch remains 8×8.
