# Completed independent low-band review

Updated: 2026-10-10 13:42 America/New_York / 17:42 UTC.
The review is complete, with no scientific computation still running.

## Strongest independently checked result

For the **ordinary spin-1/2 square bilayer**, with **unit antiferromagnetic rung coupling** and **g=0.03 in both in-layer directions**, every periodic square of **integer side L≥2** has a **unique ground state** and

**gap ≥ 0.009195338283.**

The periodic Hamiltonian retains both positive-direction bonds at side length two. There are no crossed exchanges. This is an exact certificate lower bound, not an estimate of the physical gap. The proof combines independently reviewed analytic arguments with exact rational arithmetic. It is not formalized in a proof assistant.

The frozen final seed is `../low_band/symmetric_correlated_beta909d100_FINAL.json`, beta_initial=909/100. Its x→y→temperature bootstrap establishes the stated bound at L≥128. Independently checked finite-window interpolation and an elementary L=2,3 estimate extend the same bound to all L≥2.

## Evidence

- [Original low-band review](REVIEW.md): complete-band count, principal-angle complement, Gram residuals, Schur inertia, and affine trace bounds
- [Shell-tail and bridge review](NUMBER_AND_BRIDGE_REVIEW.md): both parity Jacobi chains, correlated first cycle, and all-integer interpolation
- [Final symmetry variant](SYMMETRY_VARIANT_REVIEW.md): independent complete physical reconstruction and final exact scalar checks
- [Ground moment results](symmetric_ground_results.json): every G/K/J entry rebuilt on all three patches
- [Final correlated replay](symmetric_correlated_fast_results.json): independent directed-rational exponential bounds, exact inputs, recurrence, and asymptotic gap
- [Final all-integer bridge](symmetric_finite_window_results.json): exact square-root endpoint and separate exponential gap checks
- [Aggregate finite-window results](finite_window_results.json): all eight reviewed successful original, refined, and final seeds

The unbounded-rational Taylor replay also completed and produced the same final result as the bounded-denominator directed-rational replay. Its evidence is `symmetric_correlated_results.json`. The fast version is the recommended reproduction route.

## Verification

1. Physical spin-1/2 local Hamiltonians and all leaked trial configurations, with no producer modules imported.
2. Exact local comparison matrices, every original G/A/B/E entry, and all endpoint inertias, using an independent Fraction-based elimination.
3. Global no-missed-low-state counting from the full triplet-number multiplicities and exact Sz/parity sectors.
4. Number-sector diagonal and creation bounds, independent occupancy dynamic programming, both parity chains, and every rational LDL pivot.
5. Every symmetry-compressed G/K/J entry at g=.03 and block depth one on 2×2, 4×2, and 4×4. The largest has 11 independent proposal vectors, 20,081 expanded configurations, and 452,093 reached configurations.
6. The chosen ground state plus 48 excited states on the largest patch form a 49-dimensional retained band in a 4,294,967,296-dimensional Hilbert space. These dimensions are different from expanded support and are not MPS bond dimensions.
7. Exact heat-trace interval construction, correlated cancellation, every accepted scalar update, final logarithmic gap, and full-integer size bridge.
8. Separate physical-spin ED/residual diagnostics on the tiny patches. No ED calculation supplies any rigorous acceptance condition.

Every calculation is constrained to one CPU and one BLAS thread. Audit programs enforce a one-GiB address-space limit. The largest original audit RSS was about 298 MiB. The new 4×4 symmetry moment reconstruction took about 12.2 seconds and 147 MiB peak RSS.

## Scope

This review does not independently certify the larger 8×8 analytic-q2 symmetry contraction or its g=.01 seed, higher block-Krylov depth, g=.04/.05 frontier work, later scalar continuations beyond the frozen stopping state, or a future improved bootstrap constant such as K=26. Those are separate tasks. It does not claim a larger physical phase region, an infinite-volume uniqueness result, or that the certificate lower bound approximates the actual gap.

## Reproduction

From the repository root, in sequence:

    python research_20261010/low_band_review/independent_review.py
    python research_20261010/low_band_review/complement_diagnostic.py
    python research_20261010/low_band_review/trace_audit.py
    python research_20261010/low_band_review/number_tail_audit.py
    python research_20261010/low_band_review/correlated_audit.py
    python research_20261010/low_band_review/refined_correlated_audit.py
    python research_20261010/low_band_review/symmetric_ground_audit.py
    python research_20261010/low_band_review/symmetric_correlated_fast_audit.py
    python research_20261010/low_band_review/finite_window_audit.py
    python research_20261010/low_band_review/symmetric_finite_window_audit.py

All scripts write only this review directory. Producer inputs are left unchanged. `SOURCE_MANIFEST_SHA256.json` records reviewed producer/bridge inputs. `MANIFEST_SHA256.json` records this review's artifacts. Hashes identify the checked versions and do not replace the mathematical or arithmetic checks.
