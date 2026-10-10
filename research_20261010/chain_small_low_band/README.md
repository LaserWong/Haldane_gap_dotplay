# Count the chain's small-patch triplet contribution

Updated 2026-10-10 15:30 America/New_York / 19:30 UTC.

Exact candidates for every integer M>=2:

- g=.18: gap >= .112949677804
- g=.185: gap >= .096048414952
- g=.19: gap >= .078956697835
- g=.195: gap >= .061526095375
- g=.2: gap >= .043446395688

External independent review is pending. These are discrete parameter points.

The new denominator data comprise thirteen bare vacuum/triplet vectors and full shifted-Hamiltonian images on 172 configurations. A counted Schur comparison improves the twelve triplet lower endpoints without requiring the full band below the omitted-state cutoff. All 6,561 physical states remain counted. Largest M=8 data are reused without a new support reconstruction.

Read `PROOF.md`, `summary.json`, and `verification.json`. Reproduce with `REPRODUCE.sh`. `benchmark.json` is floating diagnostics only. The previous frozen chain extension remains unchanged.
