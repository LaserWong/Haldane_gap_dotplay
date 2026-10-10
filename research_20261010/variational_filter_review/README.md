# Variational numerator filter review

Updated 2026-10-10 15:03 America/New_York / 19:03 UTC.

PASS. All 21 global-compression and all 21 q-resolved Rayleigh improvements are independently checked with exact arithmetic. Six direct physical probes on 2×2, 3×2, and 4×2 also pass.

- [Proof, scope, and independent-reuse details](REVIEW.md)
- [Exact endpoints and all-point checks](results/point_replay.json)
- [Local normalized upper matrix](results/local_upper.json)
- [Finite physical checks](results/small_physical_crosschecks.json)
- [Reproduction](REPRODUCE.sh)
- [Frozen input hashes](INPUT_SHA256.json)

The result supplies a better ground-trial energy upper bound and heat-trace lower contribution. It supplies no new filtered-state residual or complete gap certificate. The initial 11/29/29-dimensional trial and the enlarged implicit ≤12/30/30-dimensional space are distinguished in the proof.
