# Bilayer polynomial frontier. Independent review

Updated 2026-10-10 15:38 EDT / 19:38 UTC.

The g=.085 ordinary periodic spin-1/2 square bilayer candidate passes independent polynomial-input, full physical, exact scalar and all-integer-size review, with the following results.

- Every integer L>=2 has gap >= .027887084487 and a unique finite-volume ground state
- beta_initial=177/20. Eight additional txy cycles after the seed cycle
- Final canonical base L=2048 and beta=22656/5
- All eight earlier finite windows and L=2,...,7 checked
- New .085 and .09 physical inputs accepted on all three geometries
- .09 has no new all-size gap certificate. Selected failures are bounded diagnostics

See PROOF.md and results/SUMMARY.json. This is a discrete coupling result, not a continuous interval extension. No new physical support or higher moments are constructed, no eigensolver is called, and no full many-body spectrum is computed. The largest seed has 128 physical spins, full Hilbert dimension 2^128, ground search dimension 29, retained ground-plus-triplet band dimension 193.

Run bash REPRODUCE.sh under the enforced one-CPU/1-GiB cap. INPUT_SHA256.json, PRODUCER_FREEZES.json and PRIOR_REVIEW_SHA256.json pin the source chain. MANIFEST_SHA256.json seals this completed review. Replaying changes timing outputs, so verify or preserve the sealed copy first.
