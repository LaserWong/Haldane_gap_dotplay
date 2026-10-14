# Haldane bootstrap results at the October 10 pause

This document describes the snapshot saved on October 10, 2026.
The user requested a pause at 12:24 New York time that day, and all research and numerical tasks stopped.
The snapshot preserved the results available at the pause and did not automatically resume the calculations previously scheduled to continue through October 13.
The user subsequently resumed the project on October 14, 2026, at 17:36:22 UTC, or 13:36:22 EDT.
See [README.md](README.md) for current results, evidence availability, and tasks.
The results and completion statements below describe the October 10 snapshot.
Paths identify materials in that snapshot and do not by themselves establish that every file is currently recoverable.

## Completed results with independent checks

1. **Low-energy seed for the spin-1 dimer chain.** The alternating chain has strong coupling 1 and weak coupling 0.05. A single lowest-energy trial state, its exact residual, and a full spectral-tail bound give a gap lower bound of 0.116303868802 for every periodic cell count M ≥ 2. The supporting materials are `low_energy/` and `audit/independent/certificate_s1_W1_g1d20_k0_audit.json`.

2. **Ordinary two-dimensional bilayer.** The spin-1/2 square bilayer has vertical coupling 1 and in-plane coupling 0.01 in both directions. Its gap is at least 0.072950533962 for every periodic square of side length L ≥ 2. The largest seed contains 32 spins, with full Hilbert-space dimension 4,294,967,296 and linear trial-space dimension 377. The independent check is recorded in `audit/independent/bilayer_g001_audit.json`.

3. **Two-dimensional spin-1 large-D model.** For D = 1 and Heisenberg coupling 0.01 in both directions, the gap is at least 0.086452285325 on every square torus of integer side length L ≥ 2. The largest seed contains 16 spin-1 sites, with full Hilbert-space dimension 43,046,721 and linear trial-space dimension 241. The independent check is recorded in `audit/independent/largeD_g001_audit.json`.

4. **A nonperturbative one-state example.** The fully frustrated bilayer has vertical coupling 1 and equal direct and crossed couplings J. Its exact singlet product state requires one trial state and has zero residual. For all periodic rectangles with nx, ny ≥ 2 and 0 ≤ J < 1/3, the optimal gap bound uniform over this family is min(1, 4 − 12J). At J = 0.3, this bound is 0.4, while the actual gap on squares with L ≥ 3 is 1. The analytic argument and independent small-system checks were completed. A reproducible certificate also implements the same three-purity bootstrap. The supporting materials are `two_d_theory/NONPERTURBATIVE_MODELS.md` and `two_d_numerics/results/fully_frustrated_checks.json`. The crossed couplings distinguish this model from the ordinary bilayer in item 2.

5. **Reproduction and computational optimization of the uniform spin-1 calculation.** All nine finite heat-trace inputs in Appendix A were completed and recertified. Exact integer contractions of the D = 26 MPS were reconstructed, and the moments, filtering, cooling, and bootstrap were checked. The resulting gap lower bound is 0.005908566393 for periodic chains of every integer length L ≥ 1920. The standard replay retains the original even-size statement, while the independent audit supplies interpolation to all integer lengths. This work reproduces the calculation and extensions in the supplied archive. It does not claim direct access to the missing original PDF. The supporting materials are `heat_trace/appendix_a_replay.json`, `heat_trace/PROOF.md`, and `audit/APPENDIX_A_BRIDGE.md`.

6. **A rigorous limitation of the current certification method.** For the ordinary spin-1/2 bilayer at g = 0.03, the specified ground-only numerator combined with the independent-dimer spectral-tail bound fails the current recurrence at every temperature and every local comparison parameter. Tightening the existing ground-state interval cannot remove this obstruction. The result limits this certification method and does not locate a physical phase transition. The independent check is recorded in `audit/independent/majorant_g003_audit.json`.

## Progress on three additional questions

The upper coupling limit depends on several distinct issues, including the physical phase transition, trial-state accuracy, the full spectral-tail estimate, and the spatial purity of the seed.
The fully frustrated model gives a nonperturbative parameter interval that can be treated exactly.
The ordinary-bilayer result at g = 0.03 identifies a limitation of the current spectral-tail certificate.

The linear dimension of the complete excitation-shell space is

$$
\sum_{j=0}^{q}\binom{M}{j}\left[(2s+1)^2-1\right]^j.
$$

Comparisons of adaptive support depth, residuals, and certification accuracy were saved.
The exact binomial-truncation example in `root_review/trial_dimension_toy.json` concerns a solvable model.
It illustrates representation complexity and supplies no evidence for the interacting models.

The linear trial-space dimension, MPS bond dimension, and full Hilbert-space dimension measure different resources.
The D = 26 MPS used for the uniform spin-1 chain is a compact variational state.
Its energy certificate must still be combined with the full heat-trace certificate.

## Saved work awaiting complete independent verification

- Candidate spin-1 dimer-chain certificates at larger weak couplings, including g = 0.1, 0.125, and 0.15, with several support depths. The status files in `low_energy/` specify their size ranges and the arguments covering short chains.
- Stronger optimized numerical lower bounds for the ordinary bilayer and candidate certificates at g = 0.02. These candidates remain distinct from the independently checked value in item 2.
- Robustness tests near J = 0.3 in the fully frustrated bilayer, with direct coupling J + ε and crossed coupling J. Floating-point benchmarks and new exact candidate certificates were saved separately.
- Extensions to general dimension d, some improved constants, SU(2)-compressed bases, certification of entire low-energy bands, and spin-2 Chebyshev heat-trace optimization.
- A separately recorded spin-2 benchmark interrupted at the pause. No overnight run or complete large-system calculation was started.

The `PAUSE` and `PAUSED` files in individual directories give more detailed results, unverified work, and restart instructions.
After the October 10 pause, work on this snapshot was limited to archive organization and verification.
Parameter scans did not continue during that pause.

## Snapshot contents

- `audit/` contains independent checks, physical assumptions, complete proof connections, and exact verification outputs.
- `heat_trace/` contains streaming integer heat-trace code, checkpoints, the nine heat-trace inputs, and the replay of the original calculation.
- `low_energy/` contains sparse trial states, exact residuals, local comparisons, spectral-tail bounds, and candidate certificates.
- `two_d_theory/` contains two-dimensional theorems, interpolation between integer sizes, nonperturbative models, and references.
- `two_d_numerics/` contains independent Hamiltonian implementations, exact cross-checks, and floating-point benchmarks.
- `seed_size/` contains seed exclusions, temperature windows, parameter optimization, and spectral-tail limits.
- `root_review/` contains additional independent local-matrix checks and examples of trial-space complexity.
- `original/` and `input/` contain the initially uploaded extension package and its unchanged extracted contents.
- `upstream/extracted/` contains the original reference code, scalar programs, and spin-2 local-certificate dependencies needed to reproduce this snapshot.

The snapshot did not duplicate the approximately 196 MB historical `HaldaneConjecture.zip` archive or its unrelated historical server logs.
Its new results, source code, checkpoints, and required reference dependencies were saved.
The original ZIP has SHA-256 `f55ab851502759d863673f627bce28de1d040750f18f747a7814e866153425c8`.

## Reproducing the snapshot

Run `python verify_archive.py` first to check the archive file hashes.
`COMPUTE_ENVIRONMENT.json` records the Python environment.
The numerical code generally uses numpy, scipy, and sympy.
The integer C++ programs require a C++ compiler and GMP.
The supplied Linux binaries record the original environment and should be rebuilt from source on other platforms.

From the snapshot root, run `python heat_trace/replay_appendix_a.py` to replay the saved certificate for the original calculation.
Directory READMEs give the commands for recomputation and individual checks.
Some audit scripts were changed from absolute paths in the original execution environment to package-relative paths.
`PORTABILITY_PATCHES.json` records those changes, which did not alter the mathematical logic.

The restart priorities recorded at the pause were to read the directory status files, then choose among larger couplings, improved low-energy-band or spectral-tail certification, and long spin-2 calculations.
No automatic restart was scheduled for this snapshot.
Current work follows the later instructions recorded in `README.md` and `AGENTS.md`.
