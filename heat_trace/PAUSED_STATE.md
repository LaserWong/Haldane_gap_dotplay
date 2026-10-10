# Paused at the user's request

Paused 2026-10-10 16:26 UTC. Do not resume research, benchmarks, or long runs
unless the user explicitly resumes the project. No automation was created.

## Completed spin-one work

- All nine Appendix A physical thermal inputs L6/L8/L10, I/P/C, beta21/2
  independently reconstructed, completing the six previously missing inputs.
- Exact streamed fixed-point Horner; no full diagonalization, dense column
  matrix, stochastic trace, or reuse of printed physical integer totals.
- Rigorous own Taylor, coefficient, floor, orbit-weighted Frobenius, and
  finite-exponential errors. Independent auditor passed implementation and
  all L6/L8/L10 interval arithmetic.
- Original L6 all-column implementation freshly run and bitwise matched.
- Exact magnetic-translation/antiunitary symmetry and orbit tests passed.
- Fresh D26 MPS reconstruction/GMP N120 anchor passed via the audit worker.
- Combined physical/scalar/analytic reconstruction establishes a unique
  ground state and gap >= 0.005908566393 for the spin-one isotropic periodic
  Heisenberg chain, bilinear coefficient1, every even L>=1920.
- Original PDF absent, not directly reviewed; Appendix B remaining inputs
  not claimed complete.
- Portable copy test passed without the upstream sibling directory; all
  L10 C cached chunks reused and exact interval unchanged.

Main deliverables: `appendix_a_replay.json`, `PROOF.md`, `results/`,
`audit_inputs/APPENDIX_A_BRIDGE.md`, `audit_inputs/streamed_heat_audit.json`,
`reference_validation.json`, `symmetry_validation.json`,
`portability_validation.json`, `MANIFEST.json`.

Recorded one-process L10 compute times I/P/C: 91.4/116.8/175.2 seconds.
Maximum recorded child RSS was <=12.6 MB. BLAS/OpenMP limits were one.

## Unfinished spin-two work

All files are under `spin2/`, kept separate from the completed spin-one
manifest. No complete new spin-two finite heat input or uniform gap exists.

- `verify_cluster.py` freshly checked 38,165 exact integer inequalities
  from the archived open-eight M0 positive vector. It confirms
  E8 >= -1066059959/31250000. SU2 multiplets imply this is the full open
  cluster lower bound; translated/gauged clusters give
  H_L/L >= -1066059959/218750000 > -39/8 for L>=8.
- `prepare_chebyshev.py` generated exact positive Chebyshev coefficients
  from a normalized finite Poisson convolution: mu256, lambda128,
  cutoff320, Q2^56, K141, final nonzero degree136. Its separately bounded
  polynomial truncation/normalization error is <1/Q; weighted recurrence
  error factor is approximately134.3799574615. These are preparation
  results, not a completed trace certificate.
- `chebyshev_columns.cpp` is an UNVALIDATED prototype over
  Z[sqrt(6),omega]. Its initial compile/one-column L9 I benchmark command
  was interrupted with exit130 on the pause request. Treat any executable
  or benchmark output as incomplete, not as a tested timing or certificate.
- No overnight/full spin-two run was launched. No benchmark-based total
  runtime or certified global error report has yet been produced.

## Resume only if authorized

1. Verify the completed spin-one manifest; no recomputation is necessary.
2. Independently audit the spin-two polynomial/error derivation and the
   quadratic/Eisenstein integer kernel, including every overflow bound.
3. Complete small-column tests and a bounded L9 I/C benchmark first.
4. Derive exact total work, memory, thermal-error, and tail-sector budgets.
   Obtain the root's resource allocation before any overnight run.

The planned forward Chebyshev recurrence has positive-weighted error
amplification controlled by the Bessel second moment, roughly mu+K rather
than K squared. This idea still needs a full implementation/certificate
audit. Existing high-magnetization tail certificates reduce L9/L10 squared
block work by only about14%/16%; do not infer a feasible total runtime
without the missing benchmark.
