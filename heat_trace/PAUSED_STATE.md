# Results at the October 10 pause

This record describes the October 10, 2026 pause.
The project resumed on October 14, 2026, at 17:36:22 UTC.
The current repository README and AGENTS.md determine the authorized work.
The completed checks and pending tasks below retain their status at the earlier pause.

Paused 2026-10-10 16:26 UTC. The pause prohibited further research, benchmarks, and long runs until an explicit resumption. No automation was created.

## Completed spin-1 work

- All nine Appendix A physical thermal inputs L6/L8/L10, I/P/C, beta = 21/2 independently reconstructed, completing the six previously missing inputs.
- Exact streamed fixed-point Horner calculations, without full diagonalization, a dense column matrix, stochastic trace, or reuse of printed physical integer totals.
- Independent bounds control the Taylor, coefficient, floor, orbit-weighted Frobenius, and finite-exponential errors. The implementation and all L6/L8/L10 interval calculations passed independent review.
- The original L6 all-column implementation was rerun and matched bit for bit.
- Exact magnetic-translation/antiunitary symmetry and orbit tests passed.
- Fresh D = 26 MPS reconstruction/GMP N = 120 anchor passed via the independent audit.
- Combined physical/scalar/analytic reconstruction establishes a unique ground state and gap >= 0.005908566393 for the spin-1 isotropic periodic Heisenberg chain, bilinear coefficient 1, every even L>=1920.
- The original PDF was unavailable for direct review. The remaining Appendix B inputs were not claimed complete.
- Portable copy test passed without the upstream sibling directory. All L10 C cached chunks were reused, and the exact interval was unchanged.

Main deliverables: `appendix_a_replay.json`, `PROOF.md`, `results/`, `audit_inputs/APPENDIX_A_BRIDGE.md`, `audit_inputs/streamed_heat_audit.json`, `reference_validation.json`, `symmetry_validation.json`, `portability_validation.json`, `MANIFEST.json`.

Recorded single-process L10 compute times I/P/C: 91.4/116.8/175.2 seconds. Maximum recorded child RSS was <=12.6 MB. BLAS/OpenMP limits were one.

## Unfinished spin-2 work

All files are under `spin2/`, kept separate from the completed spin-1 manifest. No complete new spin-2 finite heat input or uniform gap exists.

- `verify_cluster.py` freshly checked 38,165 exact integer inequalities from the archived open-eight M0 positive vector. It confirms E8 >= -1066059959/31250000. SU2 multiplets imply this is the full open cluster lower bound. Translated/gauged clusters give H_L/L >= -1066059959/218750000 > -39/8 for L>=8.
- `prepare_chebyshev.py` generated exact positive Chebyshev coefficients from a normalized finite Poisson convolution: mu = 256, lambda = 128, cutoff = 320, Q = 2^56, K = 141, and final nonzero degree 136. Its separately bounded polynomial truncation/normalization error is <1/Q. Weighted recurrence error factor is approximately 134.3799574615. These are preparation results, not a completed trace certificate.
- `chebyshev_columns.cpp` is an unvalidated prototype over Z[sqrt(6),omega]. Its initial compile/one-column L9 I benchmark command was interrupted with exit code 130 on the pause request. Treat any executable or benchmark output as incomplete, not as a tested timing or certificate.
- No overnight/full spin-2 run was launched. No benchmark-based total runtime or certified global error report has yet been produced.

## Tasks recorded for a later resumption

1. Verify the completed spin-1 manifest. No recomputation is necessary.
2. Independently audit the spin-2 polynomial/error derivation and the
quadratic/Eisenstein integer kernel, including every overflow bound.
3. Complete small-column tests and a bounded L9 I/C benchmark first.
4. Derive exact total work, memory, thermal-error, and tail-sector budgets.
Obtain an approved resource allocation before any overnight run.

The planned forward Chebyshev recurrence has positive-weighted error amplification controlled by the Bessel second moment, roughly mu+K rather than K squared. This idea still needs a full implementation/certificate audit. Existing high-magnetization tail certificates reduce L9/L10 squared block work by only about 14%/16%. Do not infer a feasible total runtime without the missing benchmark.
