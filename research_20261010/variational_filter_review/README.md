# Independent review of the variational numerator filter

Updated October 10, 2026, at 15:03 America/New_York / 19:03 UTC.

All 21 global-compression improvements and all 21 q-resolved Rayleigh improvements passed independent exact-arithmetic checks.
Six direct physical tests on 2×2, 3×2, and 4×2 patches also passed.

- [REVIEW.md](REVIEW.md) gives the proof, scope, and independently reused inputs.
- [results/point_replay.json](results/point_replay.json) records the exact endpoints and checks at all parameter points.
- [results/local_upper.json](results/local_upper.json) gives the local normalized upper matrix.
- [results/small_physical_crosschecks.json](results/small_physical_crosschecks.json) records the finite-system checks.
- [REPRODUCE.sh](REPRODUCE.sh) runs the replay.
- [INPUT_SHA256.json](INPUT_SHA256.json) records the frozen input hashes.

The result improves the ground-state trial-energy upper bound and the lower contribution to the heat trace.
It supplies neither a new filtered-state residual nor a complete gap certificate.
The proof distinguishes the initial 11/29/29-dimensional trial spaces from the enlarged implicit spaces of dimension ≤12/30/30.
