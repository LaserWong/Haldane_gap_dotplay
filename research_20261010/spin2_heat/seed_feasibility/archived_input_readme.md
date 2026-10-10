# Higher spatial moments for the spin-2 Heisenberg chain

**No size-uniform gap is proved in this bundle.**

This continues the previous finite-certificate attempt for

    H_L = sum_j S_j . S_(j+1), spin 2, periodic, J=1.
    Z_L(beta,g) = Tr exp[-beta(H_L(g) + (5951/1250)L)].

## New completed calculations

* Full physical spectra, including all multiplicities, are computed and validated
  at L=4,5,6,7,8, for twists I, P (pi), C (2pi/3). Auxiliary L=2,3 spectra are also
  included, with the two parallel bonds counted at L=2. No low-energy spectral
  truncation is used for these validated spectra.
* The verifier constructs a real form of each translation block, freezes the full
  eigenvector matrix on a dyadic grid, checks its Gram matrix using exact integer
  dot products implemented in BLAS, and encloses all eigenvalues from the full
  residual and orthogonality bounds. Matrix-entry, basis-change, remaining BLAS,
  and scalar-exponential errors are included. See VALIDATION.md for assumptions.
* `trace_intervals.json` contains rational thermal enclosures at beta=6,8,12,16,24.
  Finite spectral enclosures can be reused at other temperatures. High-energy
  weights dropped from the thermal sum have an explicit dimension-weighted tail.
* Exact rational interval Hankel matrices and exterior Sturm root counts produce
  certified spatial support caps from moments through order 8.
* The existing exact MPS contractions are rechecked at the improved common energy
  shift a=11902211/2500000=4.7608844. This is a recheck of existing integer totals,
  not a new optimization or a new full tensor contraction.
* An exact three-site angular-momentum argument bounds the uncomputed |M|>=8
  part of the L=10, beta=8 thermal trace, for either twist, by

      1.06081e-7.

  This is NOT a bound on all omitted low-energy Ritz states.

## Selected numerical results (a=4.7608, beta=8)

Validated L=8 thermal intervals, rounded outward:

    I: 33.8254653453 <= Z8(I) <= 33.8254738643
    P:  0.1987346855 <= Z8(P) <=  0.1987347358
    C:  0.6267925313 <= Z8(C) <=  0.6267926901

The largest translation block has dimension 4783, compared with the physical
Hilbert space dimension 390625. All dimension counts include symmetry factors.

For the J=D2-invariant and N=one nontrivial D2 spatial list:

    maximum moment   J cap       N cap          status
    6                1.767199    1.764766       validated
    8                1.275821    1.262312       validated
    10               1.1147646   1.0886770      exploratory ONLY

With moments through order 8, the finer I/O decomposition also gives

    I cap 1.133830, O cap 1.098512.

The order-10 data substantially improve the candidate caps but do not give a
successful initialization in the tested family. They are not certified inputs.
The code tests beta=6,8,10,12,16,20,24,32 and the previously certified trial lengths
128,256,512, at two allowed shifts; none passes this particular search.
Failure of this sufficient test is not evidence for a gapless chain and does not
rule out other filters or initializations.

As a by-product, the validated complete L=8 spectrum proves a finite-ring gap
larger than 0.5455692490. This is explicitly NOT a uniform-in-L gap statement.

## What remains unverified at orders 9 and 10

The L=9 data are the previously computed truncated numerical spectra. L=10 I/P
spectra were freshly recomputed with 16 Ritz values in each M=0,...,7 sector.
Their small residuals do NOT certify that no eigenvalues were missed, and do not
provide complete-spectrum enclosures. They are labeled exploratory throughout.
No L=10 C data are used or claimed.

`higher_order_tail_analysis.json` distinguishes a genuinely bounded high-magnetic-
sector tail from a CONDITIONAL in-sector tail estimate. The latter would become
usable only after validating eigenvalue counts below suitable energy cutoffs and
outward enclosures for all included eigenvalues (including degeneracies).
Such inertia/counting checks have not been performed.

## Files and reproduction

Python dependencies: NumPy, SciPy, mpmath, SymPy, threadpoolctl. The verifier assumes
standard IEEE binary64 arithmetic as described in VALIDATION.md. It is not a Lean
formalization and has not undergone an independent full code audit.

Run from this directory:

    python test_verifier.py
    python validated_real.py --ns 2 3 4 5 6 7 8 --twists I P C
    python enclose_traces.py --ns 2 3 4 5 6 7 8 --betas 6 8 12 16 24
    python moment_filters.py
    python explore10.py --twists I P
    python exploratory_higher_filters.py
    python tail_analysis.py

Completed spectral blocks are cached. To recompute all eigensystems and residual
checks, move `verified_real` aside before running `validated_real.py`; retaining
that directory reuses its previously computed blocks and bounds. The full dense
eigenvector arrays are not stored, so a fresh verification reruns eigensolvers.
The exact moment filters and postprocessors can be rerun directly from the stored
spectral/thermal intervals. `verifier_unit_tests.json` records independent Python-
integer checks of the dyadic Gram routine, and `spectrum_crosscheck.json` records
comparisons with the earlier independent full-basis implementation.

`previous/spin2_heisenberg_attempt` contains the prior attempt, clearly separated
from this run. The mathematical source framework is the uploaded paper
*The periodic spin-one Haldane gap*, especially Sections 3--5. The present spin-two
thermal inputs and robust matrix-filter extension are new calculations, not claims
that the source paper itself proves the spin-two result. For general full-spectrum
validation methods, see Rump and Lange, JCAM 434 (2023), article 115332.
