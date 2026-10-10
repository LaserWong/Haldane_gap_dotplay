# Complete low-band and number-sector certificates

Updated 2026-10-10 13:32 America/New_York / 17:32 UTC.

## Current status

The new exact-arithmetic method passes the ordinary spin-1/2 bilayer g=3/100 test on the 2×2, 4×2 and 4×4 periodic seed patches. These are new research certificates, distinct from the unchanged paused baseline. Independent review is in progress. No GitHub push has been made by this worker.

The complete ground-plus-first-band ranks are 13, 25 and 49, respectively. The largest full Hilbert space has dimension 4,294,967,296. Its retained variational supports are 361 even M=0 configurations, 3,936 odd M=0 configurations, and 3,376 odd M=+1 configurations. Spin reversal supplies the M=−1 block. These support sizes are neither full Hilbert dimensions nor MPS bond dimensions. The largest reached support has 168,368 configurations and the observed peak RSS was 208.4 MiB. All calculation processes used one BLAS thread, with a 2 GiB address-space cap on the larger runs.

The original affine dimer tail still fails at this coupling even after certifying the complete low band. The new triplet-number Jacobi comparison raises the full-space lower bound for the 50th shifted eigenvalue of the 4×4 patch from 1.3300393706848 to 1.844298248746. This sharper entire-spectrum tail, together with the complete band and correlated trace cancellation, passes the exact three-purity bootstrap.

The best completed basic-ground certificate uses initial β=911/100 and gives gap at least 0.004333053946 for integer square L≥256 under the already audited transfer/interpolation theorem. Its exact inputs and replay are the first entry in `refined_correlated_number_g003.json`.

The parent has also constructed a sharper finite-window interpolation bridge covering the missing sizes. See `../root_review/finite_window_2d.py` and `../root_review/finite_window_refined_correlated_number_g003.json`. Combined with that independently checked bridge, the same gap is a candidate for all integer square L≥2. This extension remains conditional on completion of the independent review of the new low-band/tail calculations and the bridge. Do not silently upgrade its status from this summary alone.

Symmetry-compressed block-Krylov ground trials have now been integrated from `../symmetry/`. Their exact scalar moment contractions are in `integrate_symmetric_ground.py`, and the resulting stronger seed computation is running separately. The previous accepted certificates remain unchanged.

## Proof and audit boundaries

`PROOF.md` gives complete derivations of

1. A residual-angle bound using an external full-space count, followed by a lower bound on the trial complement.
2. Rational Gram and residual-surrogate certification without algebraic orthonormalization.
3. Schur-polynomial inertia bounds for every retained eigenvalue.
4. The all-sector rank count and exact symmetry multiplicities.
5. Complete-low-band trace numerators and rigorous tail sums.
6. Number-sector Jacobi comparison, exact graph counts and rational LDL certificates.
7. Correlated first-step cancellation.

The independent reviewer has confirmed the abstract theorem and reconstructed every G/A/B/E entry for 2×2 and 4×2, with independently implemented exact inertia. Its 4×4 and number-tail checks should be read from `../low_band_review/`, not inferred from this file.

The physical-basis and random tests in `validation_diagnostics.json` and `number_tail_validation.json` are floating diagnostics only. They neither replace the exact certificates nor constitute a proof of completeness.

## Files and reproduction

- `low_band_certificate.py`: sparse trial proposals, complete leaked residual, exact Gram and Schur bounds, original affine-tail baseline.
- `number_sector_tail.py`: exact local PSD, occupancy maxima, Jacobi LDL bins, improved band cutoff and full tail.
- `correlated_low_band.py`: correlated full-band trace ratios and exact scalar replay.
- `integrate_symmetric_ground.py`: exact contraction of the independent symmetry trial moments into the ground block.
- `bilayer_*_low_band.json`: baseline full-band certificate.
- `bilayer_*_number_low_band.json`: full band with sharper number-sector count and tail.
- `bilayer_*_symmetric_number_low_band.json`: deeper symmetry-ground variant.
- `*_gram.json`, `*_trial.npz`: replayable exact input moments and dyadic trial vectors.
- `number_bins_*.json`: complete weighted graph, exact occupancy counts and all positive rational LDL pivots.
- `refined_correlated_number_g003.json`: improved exact accepted basic-ground seeds.

From the repository root, use single-thread BLAS and suppress bytecode creation in the baseline directories.

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/low_band_certificate.py --shapes 2x2,4x2,4x4
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/number_sector_tail.py
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/correlated_low_band.py --number
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/integrate_symmetric_ground.py

The first command reuses saved Gram files unless `--no-reuse` is given. Floating eigensolvers propose vectors and endpoints. Every accepted endpoint is checked with exact arithmetic. No full finite-system diagonalization enters the certificates.

## Remaining work

- Finish independent review of the new number-sector tail, 4×4 moment maps and complete trace/replay chain.
- Finish and independently review the deeper-ground candidate.
- Preserve the finite-window interpolation scope explicitly.
- Explore translated dressed-triplet trials for larger seed patches without expanding the complete q≤3 Hilbert support.
- A failed temperature grid is not an all-temperature exclusion, and a largest successful tested coupling is not a physical critical coupling.
