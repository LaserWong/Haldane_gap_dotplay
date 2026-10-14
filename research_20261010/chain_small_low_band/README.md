# Small-patch triplet contributions in the alternating chain

Updated 2026-10-10 15:30 America/New_York / 19:30 UTC.

The producer calculation gives the following exact candidate bounds for every integer M>=2.

- g=.18: gap >= .112949677804
- g=.185: gap >= .096048414952
- g=.19: gap >= .078956697835
- g=.195: gap >= .061526095375
- g=.2: gap >= .043446395688

Independent review is pending. The bounds apply at the listed coupling points.

The new denominator data comprise thirteen bare vacuum/triplet vectors and full shifted-Hamiltonian images on 172 configurations. A counted Schur comparison improves the twelve triplet lower endpoints without requiring the full band below the omitted-state cutoff. All 6,561 physical states remain counted. The largest M=8 inputs are reused without reconstructing their support.

Read `PROOF.md`, `summary.json`, and `verification.json`. Reproduce with `REPRODUCE.sh`. `benchmark.json` is floating diagnostics only. The previous frozen chain extension remains unchanged.
