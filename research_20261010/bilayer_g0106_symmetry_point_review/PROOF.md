# Independent g=.106 all-integer point certificate

## Result and exact scope

For the ordinary isotropic bilayer with unit rung exchange and intralayer g=53/500=.106, every integer periodic square sideL≥2 has a unique full-Hilbert ground and gap at least

10472755223/500000000000 = .020945510446.

This certifies one coupling point. It does not interpolate a continuous interval between.105 and.106. The previously accepted[0,.105] interval remains a separate theorem. No physical support contraction, eigensolver, optimization or large simulation is performed here.

## Complete physical inputs, freshly evaluated at the new coupling

Producer package seal f0964e98022793c1f200e63c290acd340539e59833a6ecffc1610b4ef08132e3 is pinned. Both candidate_g0106.json and its result.json copy are compared exactly. The independent review recursively pins its prior physical/scalar library and the accepted21D4×4 and57D8×4 complete H′² matrix reviews.

The checker contracts the exact Gram, affine first-H and quadratic complete second-H matrices with two fixed candidates for each denominator: the saved.105 vector and the saved.11 vector. It derives the entire affine mean and quadratic full variance polynomials using exact rational arithmetic. Every quadratic variance is PSD, and its value is nonnegative at the new coupling. The polynomial contractions reproduce the independently accepted.105 physical moments and.11 endpoint lower values at their reference couplings. This guards coefficient ordering, normalization, and the R/M embedding.

The saved16D4×4 and43D8×4 vectors embed into the accepted21D/57D split bases by duplicating each old U coefficient into R and M, since U=R+M. This is an identity of physical vectors, not a new optimization or truncation. Atg=.106 both selected denominator lower vectors are the.105 vectors. Their original search dimensions are16 and43; the ambient exact matrix dimensions are21 and57.

The complete second moment includes the physical q8 image and all mixed terms, as certified by the independent complete-matrix reviews. No projected H squared is substituted. The selected full variance and mean are reevaluated atg=.106 before applying the sector Temple formula.

## Cutoffs, odd count, and global ground

The checker freshly evaluates the oscillator comparison r_q=(3N/8)(2g−1)+(3N/8+q)sqrt(1−4g), with a downward rational square-root witness, for N=16,32. Every chosen mean lies strictly below the global first-excited reference r1, identifying a unique global ground below r1.

The fixedz=.1 odd family is recomputed from the accepted structural operator polynomials, rather than trusting saved new-coupling lower values. Each momentum Gram is strictly positive. All mean and complete residual polynomial coefficients are independently reconstructed; values atg=.106 are handled in Q(sqrt2), with exact sign tests and directed rational enclosures. Every odd mean lies below r2. There are N distinct momentum modes with spin multiplicity3, hence48/96 odd states below r2. Together with the identified ground and the full-Hilbert reference count, this gives the second level of the full untruncated even-singlet sector at least r2. The sector Temple lower rho−variance/(r2−rho) therefore bounds the actual global ground. It is not a claim that full-Hilbert λ2≥r2.

Every odd retained energy lower is max(r1, theta_lower−variance_upper/(r2−theta_upper)). The trace keeps49/97 states including the ground. The complete omitted tail includes q=2,…,N with oscillator multiplicity binomial(3N+q−1,q); the total reference count covers at least4^N states. All cutoffs, mode counts, positivity gates and new-coupling lower energies are checked afresh.

## Rayleigh upper energies and trace normalization

For each shape4×4,8×4,8×8 the checker independently reconstructs the weighted physical pair graph and pair-orbit first-H action, assembles split Gram/first-H blocks from the accepted cached geometry, and contracts the saved.11 split vectors. The old43D numerator vector is also embedded and its affine energy coefficients reconstructed exactly. The selected numerator atg=.106 is that saved43D vector. Only one numerator state is retained; no numerator residual is required for a Rayleigh upper. Its full physical dimension is2^128, unrelated to its43D search dimension.

The denominator trace pivot is the minimum of verified trial upper energies. The ground width equals pivot minus the newly evaluated ground lower; all odd and tail energies are measured relative to that same pivot. Changing a pivot does not move absolute odd or tail energies. The correlated combinations are explicitly rebuilt as8e16−2u64,16e16−4u64,4e32−2u64. The reviewer independently sums ground, odd and complete tail exponentials atβ0,2β0,2β0 and obtains the three exact ratio lower bounds. The selectedβ0=47/5.

## Every size window and the terminal theorem

The first raw txy state has common physical base(8,8,94/5). The independently accepted square-isotropic recurrence and window theorem are used with their exact edge/temperature labels. Every saved raw entry, transported canonical entry, common defect and window lower is recomputed with directed rational rounding.

The four finite windows are[8,16],[16,32],[32,64],[64,128]. Their certified gaps are respectively .093800446778, .060178164912, .043053333712 and .035405649093. For each purityp>1/2, the reviewer checks exp(βγ)(1−p)<p exactly, giving uniqueness and the stated finite-window gap, including odd integer sides.

At side128 andβ=1504/5, the canonical common defect satisfies0<u≤1/500. The independently accepted asymptotic theorem applies, and the reviewer checks exp(βγ)*32u<1 atγ=.020945510446. The accepted continuous short theorem on[0,.15] coversL=2,…,7 withgap≥.050426624396, larger thanγ. Overlapping finite windows and the terminal theorem cover every integerL≥2 without a size gap.

The reviewer uses its independent544-bit directed exponential enclosure; producer384-bit enclosures are not trusted as arithmetic results. Initial ratios agree exactly at the60-decimal saved grid. Every selected displayed gap passes its rational exponential inequality. There is no floating optimization in the reviewer.

## Reproduction and limits

Run REPRODUCE.sh to check seals, copy to a fresh directory, and repeat all exact matrix-polynomial, new-coupling odd/count, trace and scalar checks. The observed audit uses under3CPU seconds and21MiB RSS, within the assigned120CPU-second/256MiB bound onCPU4. The other sampled coupling failures in the producer package are not promoted to impossibility claims or independently reviewed here. A continuous-coupling extension requires a separate closed-interval physical and scalar audit.
