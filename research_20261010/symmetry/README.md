# Symmetry-compressed ordinary bilayer ground certificates

Updated 2026-10-10 13:28 EDT / 17:28 UTC. Stable completed subtask checkpoint.
Source: main commit `6be889a30f642bde77fb89af75b3a7379615bed1`. Baseline files were not edited. No GitHub push was performed by this worker.

## Main results

- Exact SU(2) and spatial symmetry compression on 4x4: 377 q<=2 Sz=0 configurations (361 in even parity) -> 121 singlet vectors -> **6 independent trial vectors**, in a full Hilbert space of dimension 4^16=4,294,967,296.
- Compressed q2 and old full-q2 Ritz minima are mathematically equal whenever the exact trial Rayleigh quotient is below the existing all-sector second-level bound. In all nine size/coupling checks, rounded rational Rayleigh quotients agree within 10^-20.
- One block-Krylov extension gives **11 trial vectors** on 4x4. At g=.01/.02/.03 the exact residual squared drops from 2.36025e-6 / 3.79837e-5 / 1.92855e-4 to 7.02822e-10 / 4.58375e-8 / 5.31537e-7. Corresponding optimized-bound Temple widths are 8.29827e-10 / 6.58230e-8 / 9.69152e-7.
- At g=.03 this 11D result improves the archived 3,769-dimensional selected-depth-two residual squared 1.11990e-6. Its larger leaked support also costs more: roughly 5.1 seconds and 226 MiB peak versus the archived 2.6 seconds and 118 MiB. These are same-session measurements, not hardware-normalized benchmarks.
- An exact analytic q4 leakage contraction eliminates physical q4 enumeration. It matches the explicit integer G/H/H^2 matrices entry-for-entry on 2x2,4x2,4x4 at g=.01,.02,.03. For 8x8 it uses **15 trial vectors**, about 0.9–1.4 seconds and <77 MiB peak in the recorded run, while the full Hilbert dimension is 4^64=340282366920938463463374607431768211456.
- Independent physical-spin action on the entire 2x2 Hilbert space verifies all exact G/H/H^2 matrices and full leaked support at all three couplings. These are internal independent-formulation checks; an independent-worker audit is still required before promoting new seed certificates.

## Larger seed tests

Ladder 4x4 -> 8x4 -> 8x8 uses 6/15/15 trial vectors.

- g=.01, beta20: exact lower purities A=.999854564212919, B=.999325128033404, C=.997264843627325. Existing exact scalar replay accepts after one round and returns gap >=.1558512172 for every integer square side L>=8, conditional on the existing transfer theorem. This is a **new candidate dimension/computation example**, not an improvement over the separately audited .16892 g=.01 result. Small-L bridging and independent review are not performed here.
- g=.02: the tested larger q2 seeds fail; the best minimum purity over integer beta=1..200 is about .914812 near beta25.
- g=.03: the tested larger q2 seeds fail; best minimum purity in that scan is about .133994 near beta40. The 8x8 Temple width .0217527 is the main loss. Hypothetically removing energy-interval width, while retaining the same q2 Rayleigh energy and full-space tail, raises the best scanned minimum purity to about .972070. This is a bottleneck diagnostic, not a valid replacement certificate.

Exact replay was applied to the best scanned beta and its two neighbors. These failures do not prove an all-beta or all-local-parameter obstruction for the larger ladder. They do not establish a physical gaplessness boundary.

## Dimensions, accuracy, and cost

The complete measurements, exact rational endpoints, and matrices are in `summary.json`, `symmetry_*_block*.json`, and `analytic_*.json`. The 11D space has 20,081 expanded trial configurations and 452,093 reached configurations. These support counts must not be confused with its 11 independent linear vectors, the one retained physical ground state, the exponential Hilbert dimension, or an MPS bond dimension. No MPS representation is used here.

For larger q2 cases at g=.03:

| Rung lattice | Full Hilbert dimension | q<=2 Sz0 | SU2 singlet | Space-invariant | Residual squared | Temple width |
|---|---:|---:|---:|---:|---:|---:|
| 4x4 | 4^16 | 377 | 121 | 6 | 1.92855e-4 | 3.51665e-4 |
| 8x4 | 4^32 | 1521 | 497 | 15 | 8.43714e-4 | 2.20235e-3 |
| 8x8 | 4^64 | 6113 | 2017 | 15 | 3.43836e-3 | 2.17527e-2 |

The q2 method solves memory and linear-dimension growth on these sizes; residual accuracy becomes limiting. Higher-depth orbit-only residual contraction is described as a proposal in `PROOF.md`, not a completed certificate. Its implementation is deferred pending the parallel complete-low-band/tail work.

## Reproduction

Run from the repository root. All numerical commands set one BLAS thread. The largest completed job was <230 MiB RSS, within the one-CPU/1.5 GiB worker budget.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python research_20261010/symmetry/verify_symmetry.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python research_20261010/symmetry/symmetric_ground.py --nx 4 --ny 4 --g 3/100 --depths 1
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python research_20261010/symmetry/analytic_q2.py --nx 8 --ny 8 --g 3/100
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python research_20261010/symmetry/check_large_seeds.py

The last command reads the nine existing analytic certificate files. Re-running a command replaces only its generated files in this directory. No command changes remote state. Depth >1 on 4x4 has not been costed and should not be launched without a support/memory estimate.

## Files and verification status

- `PROOF.md`: exact basis, equality of q2 Ritz minima, complete leakage contraction, interfaces, and scoped future suggestions
- `symmetric_ground.py`: explicit sparse integer basis, exact Gram/H/H^2, block Krylov, complete reached support
- `analytic_q2.py`: streamed four-rung pairing contraction and exact ground certificate
- `verify_symmetry.py`, `verification.json`: passed exact checks, including independent physical-spin action
- `check_large_seeds.py`, `larger_seed_diagnostics.json`: float beta scan and exact neighboring seed replay
- `*_basis.json.gz`: integer sparse trial vectors, each state packed with rung i at bits 2i, coefficients as decimal strings
- `summary.json`: coupling/size/depth/cost comparisons and archived baseline references
- `MANIFEST_SHA256.json`: checksums of this stable checkpoint

The scientific research authorization remains subject to the parent task's deadline, 2026-10-13 20:00 America/New_York / 2026-10-14 00:00 UTC. This worker has no active long calculation at the stable checkpoint.
