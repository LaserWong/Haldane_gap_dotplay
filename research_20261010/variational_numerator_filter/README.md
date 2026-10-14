# Variational numerator filter

Updated 2026-10-10 15:00 America/New_York (EDT, UTC−4) / 19:00 UTC.

Exact producer candidates. Independent review pending. The proof is in `PROOF.md`.

This optional route lowers an existing ground trial's Rayleigh upper endpoint using G/H/H² and a rigorous upper expectation on its residual. It constructs no production physical residual and does not use H³/H⁴. The existing first-moment-only route is untouched.

The sharper variant resolves the residual norm among q=0,2,4,6 using existing F/S/V/W geometry. All 21 residual norm sums equal the stored complete variance exactly.

The table gives results for the largest 8×8 rung patch.

| g | Global-upper gain | Sector-resolved gain |
|---|---:|---:|
| 0.03 | 0.00000810164917 | 0.00000822360666 |
| 0.04 | 0.00004333230048 | 0.00004447590235 |
| 0.05 | 0.00015531950211 | 0.00016145319743 |
| 0.06 | 0.00043029483044 | 0.00045338941553 |
| 0.07 | 0.00099439875883 | 0.00106241475672 |
| 0.08 | 0.00200680758131 | 0.00217391024282 |
| 0.10 | 0.00608024794650 | 0.00676318139512 |

These are energy-upper-endpoint improvements, not gap lower bounds. Input trial dimensions are 11/29/29 on 4×4/8×4/8×8. The filter uses an at-most-two-dimensional plane and retains one implicit normalized state with q≤6 support. Adjoining its residual direction to the original space would give dimension at most 12/30/30. The largest physical Hilbert dimension is 4^64=2^128. No new residual claim is made for the filtered state.

For the consumer interface, read `filtered_<nx>x<ny>_g<p>d<q>.json`, use `shifted_rayleigh_upper` (H′=H+3N/4) or `energy_rayleigh_upper` (H). `filter` is the sharper certified variant. `global_upper_filter` preserves the simpler variant. Both have exact rational data. Treat status as candidate until independent review and complete scalar/bridge replay.

Reproduce with `bash REPRODUCE.sh`. The scope is ≤1 CPU and 1 GiB address space, with BLAS/OpenMP threads set to one. Run time is seconds. Files are only written in this directory. Upstream inputs are referenced by exact hashes. No physical-state computation or external publication is performed.

The next action is independent review of local upper normalization, residual-sector formulas, and all exact endpoints. Then combine with independently reviewed denominator lower endpoints and complete thermal/finite-size checks. Parent owns updates to the main README and final publication.
