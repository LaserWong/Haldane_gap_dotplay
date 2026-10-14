# Certifying low energies without assuming ground degeneracy

The generic problem begins with unknown ground multiplicity. A group of close numerical Ritz values does not establish exact degeneracy. The exact routines in `gapflow/low_band.py` separate an isolated bottom spectral cluster from an exactly degenerate ground eigenspace.

## Exact cluster certificate

The caller proposes rational bounds a < b < t. Floating candidates may suggest these bounds, but cannot certify them. Exact full-matrix pencil inertia, or the sum of exact inertia over every conserved magnetization sector, must establish all three conditions.

- No eigenvalue lies below a.
- Exactly r eigenvalues lie below b, none equals b, and r is positive.
- Exactly r eigenvalues lie below t.

These facts place the complete bottom cluster inside [a,b), establish its rank r and bound its width by b-a. If r is smaller than the full dimension, the gap between the top of that cluster and the omitted spectrum is at least t-b. An eigenvalue exactly at t is permitted. An eigenvalue exactly at a is also permitted.

The result fields `low_band_rank`, `low_band_width_upper` and `gap_above_cluster_lower` refer to this cluster. They do not imply that its r energies coincide. `true_ground_multiplicity` and `true_ground_gap_lower` remain absent as mathematical conclusions, represented by null values, until equality has been proved separately. A cluster containing the whole spectrum is labeled `NO_SPECTRUM_ABOVE_CLUSTER`. Only an additional single-energy proof justifies `NO_EXCITED_SPACE`.

`certify_low_band(A, lower, upper, threshold, Wdiag=None)` treats a rational symmetric matrix or a positive-metric rational pencil. `certify_sector_low_band(model, lower, upper, threshold)` checks every conserved total-Sz sector. Incomplete coverage cannot establish a full-space cluster. The earlier exact-ground-energy APIs remain explicit specialized verification paths. They are not an assumption required by these generic routines.

## Automatic multiplicity from exact distinct-root counts

With `infer_multiplicity=True`, sufficiently small inputs can prove whether all cluster energies coincide. The method forms the exact rational characteristic polynomial of W^(-1) A, takes its squarefree part and uses an exact Sturm root count on [a,b]. It never evaluates approximate polynomial roots or computes the full eigenspectrum.

For an exhaustive sector decomposition, the method forms the least common multiple of the squarefree sector polynomials. This counts distinct energies across sectors without counting the same energy again in each block. If the interval contains exactly one distinct root, the inertia count r is its full ground multiplicity. The true gap above that ground eigenspace is then at least t-b. If it contains more than one root, the result remains a low-cluster certificate with unknown ground multiplicity.

The distinct-root calculation has a default full-Hilbert-dimension cap of 16, including for the sector path. Above the cap the cluster result remains valid while multiplicity remains unknown unless a structural argument applies. Exact polynomial arithmetic can have substantial coefficient growth. External process limits must enforce hard time and memory bounds.

Tests include two copies of the rational symmetric block [[-1,1],[1,1]]. Its ground energy is the irrational number -sqrt(2), with multiplicity two. An interval [-2,-1) and cutoff 0 establish that multiplicity without supplying the ground energy or degeneracy. A distinct test with levels 0 and 1/1000 confirms that close unequal energies remain a two-state cluster, not a degenerate ground.

## Structural Kramers inference

The exhaustive-sector path can infer multiplicity two without a characteristic polynomial. The implemented sufficient conditions are an odd sum of the local doubled spins, real supported interactions invariant term by term under time reversal, and an already certified complete bottom cluster of rank two. The odd doubled-spin sum gives Theta squared equal to -1. Kramers degeneracy forces every full-space energy to occur an even number of times. Therefore the two states in that isolated bottom cluster must have the same energy, proving exact ground multiplicity two.

The termwise check accepts the supported real Heisenberg and XXZ interactions, single-ion Sz squared, and real products of an even number of distinct-site spin components. Nonzero longitudinal fields, odd products and unsupported terms fail this sufficient check. It does not attempt to recognize cancellations between symmetry-breaking terms.

This inference is integrated only where the model itself generates every sector. It is not attached to an arbitrary caller-provided matrix or a single magnetization block. Time reversal usually maps one nonzero magnetization sector to another, so a single-sector rank-two observation would be insufficient.

The open three-site spin-1/2 Heisenberg chain passes this inference with the polynomial dimension cap set to one. Adding a small longitudinal field breaks the time-reversal check and leaves the two close low energies as a cluster with unknown degeneracy. An integer-spin ferromagnetic dimer instead uses the exact sector root-union method to infer a five-dimensional ground eigenspace automatically.

## Reproduction

Run from the workflow root.

    python -m unittest discover -s tests -p test_low_band.py -v

All statements concern the supplied finite matrix or fully covered finite model. None establishes a thermodynamic gap or assumes a ground multiplicity from numerical near-equality.
