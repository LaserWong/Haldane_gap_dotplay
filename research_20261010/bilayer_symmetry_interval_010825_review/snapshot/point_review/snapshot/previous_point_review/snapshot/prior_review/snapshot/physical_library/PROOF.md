# Independent physical pencil endpoints and scoped target exclusions

Scope: four physical ground-energy lower bounds at the POINT couplings g=.11 and.12, on4x4 and8x4 patches, using the unchanged16D/43D even-singlet bases; and two exact positive-definite43D target pencils at g=.11. No all-size gap, continuous coupling range, or universal bootstrap obstruction is claimed. Floating scalar temperature diagnostics and the proposed conditional target scalar paths are not promoted by this review.

## Complete physical moments

The independently accepted full4x4 and8x4 matrix review manifests are pinned. Every first-moment matrix and Gram is rebuilt from accepted independent geometry. Every full second moment uses the independently checked coupling polynomial, including q8, signed commutator and M-zero image contributions. No projected square of a finite Hamiltonian matrix is used. The omitted-image Gram is explicitly nonzero.

Each producer rational vector is read exactly. Norm, mean, complete variance, cutoff, pencil expectation, resulting Temple bound, baseline energy-optimized-vector variance and endpoint improvement are independently recomputed as rational numbers. Floating generalized eigensolvers and their root brackets are ignored: they proposed these vectors and endpoints but do not certify them.

For cutoff a and saved ell<a, all four normalized quadratic values
 <(H'-a)(H'-ell)>=variance-(rho-ell)(a-rho)
are strictly negative. The exact Temple bound rho-variance/(a-rho) is strictly larger than ell and matches the saved rational endpoint. The four physical lower endpoints, safely rounded DOWN to12 decimal places, are:

 g=.11,4x4: E0(H')>=−.154352817352;
 g=.11,8x4: E0(H')>=−.308345263165;
 g=.12,4x4: E0(H')>=−.184847038308;
 g=.12,8x4: E0(H')>=−.369360273562.

These are shifted energies H'=H+3N/4, not gaps. Exact stronger rational bounds are in audit.json. The improvement over freshly energy-optimized vectors is positive in all four cases, but no global finite-basis optimum is asserted.

## New-coupling global identification and sector cutoff

The reference values r1 and r2 are recomputed at each exact coupling using directed60-decimal square-root lower endpoints. All new even-singlet means lie strictly below the FULL-HILBERT r1. Ordered min-max therefore identifies a unique global ground below r1, and the trial's nonzero projection onto that level places the ground in the even-singlet sector.

This review independently reconstructs the fixed z=.1 odd trial family from the accepted literal bivariate physical operator polynomials. For every momentum on4x4 and8x4, exact Q(sqrt2) Fourier symbols prove strictly positive Gram and mean below the new r2. This is96 mode/coupling checks in total. Each mode has three SU(2)-related spin components. Different momenta and spin projections give orthogonal invariant symmetry blocks, so the Rayleigh form on the entire3N-dimensional odd span lies below r2. The exact global reference count allows at most1+3N eigenvalues below r2. Together with the identified ground these odd levels exhaust the available count. Thus the second level of the FULL untruncated even-singlet sector is at least r2.

This distinction is essential: r2 is not the full-Hilbert second eigenvalue. Every rational ground-basis vector is exactly even and SU(2) singlet, because the pair-singlet basis and all defining creation/preserving operators have those symmetries. Coefficient rounding does not break them. With the sector cutoff justified, negativity of the complete pencil proves the physical lower endpoint. Merely checking a negative finite matrix without this counting argument would be insufficient.

## Two chosen fixed-cutoff target limitations

At g=.11 the scalar-assessment package supplies two proposed ground32 thresholds, associated with beta47/5 and10. The reviewer takes their exact rational values as specified targets; this acceptance does not rely on floating searches for those targets or assert that they are necessary for startup.

For each specified target ell, the reviewer reconstructs the COMPLETE43x43 matrix
 M(ell)=J-(a+ell)K+a ell G,
using the independently accepted physical J and the fixed sector cutoff a=r2(.11). Exact rational elimination yields43 strictly positive pivots, all agreeing with the stored LDL sequence. Hence M(ell) is positive definite. No nonzero vector in this CURRENT43-dimensional space can have the negative pencil required to certify that target using THIS cutoff and criterion. The saved endpoint vector's variance budget and the requested improvement from the accepted physical endpoint are independently checked.

This is a finite-space, fixed-cutoff limitation. It does not prove that the physical ground lies below the target, that a larger or differently split basis fails, that a better sector cutoff fails, or that every all-size bootstrap is impossible. It also does not turn failed floating temperature samples into a no-go theorem. The accompanying conditional scalar paths and sensitivity scenarios remain outside this review's accepted scope.

## Reproduction and dependencies

No physical contractions are performed here. The checker uses only previously independently accepted complete matrices and exact physical odd-family identities. Source and producer snapshots, including their immutable manifests, are preserved. The4x4 matrix review is a4eec814..., the8x4 matrix review a7733091..., producer pencil witnesses b7182fdb..., and target assessment0ffd7b5d.... Exact full hashes are verified in audit.py.

REPRODUCE.sh checks the seal, reruns all rational contractions,96 odd-mode tests and both43-pivot eliminations in a fresh directory, and compares scientific output. Typical cost25CPU seconds and31MiB peak RSS; no root, producer or remote files are changed.
