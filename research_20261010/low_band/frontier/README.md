# Ordinary bilayer coupling frontier at g=0.04 and 0.05

Updated 2026-10-10 13:42 America/New_York / 17:42 UTC.

This directory is separate from the frozen, independently reviewed g=0.03 certificates.

## Exact finite-patch results

Complete low bands were certified on the same 2×2, 4×2 and 4×4 periodic patches at both g=1/25 and g=1/20. The band ranks remain 13, 25 and 49. The number-sector cutoff still separates the complete trial band from all omitted states. These new coupling-specific numerical certificates have not been independently audited.

The symmetry-compressed ground sources use one block-Krylov extension and have at most 11 trial vectors. Their full expanded support and full residual outside the trial space are retained. Ground source artifacts are under `symmetry/` and the additional exact check residual_squared_bound >= exact r² is enforced when integrating them.

The exact shifted 50th-eigenvalue cutoffs on 4×4 are

- g=0.04, 1.775456374051
- g=0.05, 1.697559811076

## Scalar acceptance and bottleneck diagnostics

Neither coupling passed the floating proposal grid β=4,4.05,…,20, across the three placements of the temperature axis. This is a bounded numerical search, not an all-temperature exclusion.

At g=0.04, the smallest canonical first-cycle maximum defect was about 0.224820. Removing the omitted tail alone improved it to about 0.222693. Setting both the entire omitted tail and every retained-band width to zero improved it only to about 0.222075. These deliberately optimistic ablations are diagnostics, not physical heat traces or certified upper bounds. They indicate that the small spatial seed curvature dominates after the band and tail errors have been controlled.

At g=0.05, no full positive first bootstrap cycle remained on the tested grid, even under the same optimistic ablation. A larger seed family is therefore the next targeted experiment. This does not imply a physical phase boundary or a proof that every temperature fails.

## Rejected numerical proposal and safe retry

For the 4×4, M=1 block at g=0.05, a single-start ARPACK proposal returned only 14 of the 16 low modes and two higher modes around 2.7. The exact global cutoff check rejected it. No low-band or purity certificate was accepted from those data.

The rejected vector and Gram files are retained with `rejected_arpack_missing_modes` in their names. A block LOBPCG proposal initialized by all 16 bare triplets recovered the full band. Its largest Ritz value is below 1.07, and it passed the same exact Gram/residual/count checks. The exact residual-squared bound is about 0.001483877280.

This event reinforces why the numerical eigensolver is only a proposal generator and cannot supply the spectral-completeness proof.

## Reproduction

- `build_symmetric_sources.py` generates the coupling-specific ground trial sources.
- `run_frontier.py` generates/reuses the complete low-band certificates and runs the finite-grid ablations.
- `retry_degenerate_proposal.py` preserves the rejected proposal and performs the documented block-solver retry.
- `frontier_summary.json` contains both final diagnostic scans.
- `frontier_g1d25_q2_diagnostic.json` preserves the earlier shallower-ground comparison.

Use PYTHONDONTWRITEBYTECODE=1, one BLAS thread, and a 2 GiB address-space cap. The retry script should not be rerun blindly after acceptance because it is a record of a particular rejected proposal and recovery.
