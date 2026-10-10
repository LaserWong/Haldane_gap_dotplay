# Final symmetry-ground variant: independent acceptance

Updated 2026-10-10 13:42 America/New_York / 17:42 UTC.

## Result

The frozen beta_initial=909/100 variant passes all independent checks and yields gap≥0.009195338283, with a unique ground state, for every integer periodic square side L≥2 in the ordinary spin-1/2 bilayer at unit rung exchange and in-layer exchange g=.03.

The final rational gap is 9195338283/1000000000000. After the correlated first cycle and five further complete cycles, the asymptotic base is L=128 and beta=14544/25. Required earlier finite windows have gap lower bounds at least .013513267909, and L=2,3 have the elementary lower bound .19. Therefore neither bridge lowers the asymptotic certificate value.

## Physical reconstruction and exact moments

`symmetric_ground_audit.py` reads the stored sparse integer basis vectors and rebuilds every Hamiltonian-applied vector using the separately derived physical-spin local kernel. It imports no producer symmetry code. It compares every entry of the compressed matrices G, K, and J, with T=400(H−E00), against the supplied source matrices.

All entries agree exactly on 2×2, 4×2, and 4×4. The respective linear dimensions are 4, 11, 11; expanded supports are 34, 1,101, 20,081; reached supports are 38, 4,067, 452,093. The Gram matrices are independently certified positive definite. The entire 2×2 calculation is additionally checked in the computational-spin basis with an exact integer Hamiltonian.

For the stored coefficient vector c, the independent reconstruction gives norm n=c*Gc, ha=c*Kc, hb=c*Jc. It verifies rho=ha/(den·n) and residual²=hb/(den²·n)−rho². The replacement scalar Gram data are G=[n], A=[ha], E=[n·hb−ha²], with residual denominator den²·n. This is the exact full residual Gram in the one-dimensional trial space. The rounded residual bound is explicitly checked against the exact rational residual squared.

The old excited-trial blocks and number-sector bins are unchanged. Their identity is checked before use. The updated global residual bound, complement lower bound, and every new Schur-polynomial endpoint are recomputed independently. The new trial has even triplet parity and Sz=0, so the previously proved full-band count continues to apply without a missing sector.

This validates the chosen physical trial and its entire leakage. It does not require treating a tiny residual as a completeness argument, nor rely on the numerical accuracy of the symmetry eigensolver.

## Independent exponentials and exact scalar replay

The recommended `symmetric_correlated_fast_audit.py` uses a separately implemented 256-bit directed dyadic enclosure. It reduces |x| to at most 1/4, propagates lower and upper Taylor terms with directed rounding, adds a geometric remainder bound after 70 terms, then squares outward to undo range reduction. Negative exponents use outward-rounded reciprocals. Every operation is rational; 256 bits denotes an arithmetic enclosure precision, not an assumed floating accuracy.

The independently enclosed trace ratios reproduce the exact downward-rounded J1, J2, and C in the frozen final source, and consequently all first purities and every recurrence update agree. The independent logarithmic endpoint also reproduces the final rational gap. The optional direct unbounded-Fraction Taylor replay completed successfully and gives identical final results.

## All-integer bridge and provenance

The independent bridge audit checks each square-root-dependent lower bound by squaring rational endpoints. It verifies each claimed finite-window gap with a separate Taylor exponential enclosure. Every size, temperature, recurrence state, and source SHA-256 is checked. The frozen source is `symmetric_correlated_beta909d100_FINAL.json`; the root bridge is `finite_window_symmetric_correlated_beta909d100_FINAL.json`.

The bridge uses the analytic lemma proved in NUMBER_AND_BRIDGE_REVIEW.md. Both inverse-purity preconditions are checked at every application. It covers every integer side length, including odd sizes. No density-of-even-sizes argument, ED extrapolation, or interchange of infinite-size and zero-temperature limits is used.

## Scope boundary

Only the three g=.03 block-depth-one symmetry sources and their frozen final low-band/seed chain are promoted by this review. The larger analytic-q2 contractions, other couplings, higher depth, and a future improved scalar bootstrap constant remain outside this completed scope.
