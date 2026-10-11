# Independent58D endpoint and selected-target review

## Accepted scope
PASS for exact finite-patch ground-energy witnesses atg=217/2000 and11/100, complete matrix integration, and four strictly positive-definite target pencils. No new all-size gap or continuous coupling interval is certified. The prior all-size frontier is unaffected.

The exact new8×4 ground lower bounds are recorded as rational numbers in audit.json. Their approximations are−0.29970312163017 and−0.30833747799085. Gains over freshly checked57D witnesses are approximately5.774831924×10⁻⁶ and6.438571918×10⁻⁶. The rational inequalities, not rounded displays or optimizer convergence, are the certificates.

Producer scientific seal1bdec7a19aa4f7c8aa586fbb6b66bda65035e99fd86871c4952e134cf88f301b and its resource addendumecb288368cfc2d2f21a2f0d2ec21974ec203d7481fab8aae4e28d6a2bb23d119 are preserved. The complete58D physical matrix was independently accepted under13e12855678f844ce419319908087ad05a7de6d5dd547ee2060d4db7ccee1887 before this review.

## Fresh physical witness verification
Every saved energy and pencil proposal for the21D4×4,57D8×4 and58D8×4 spaces is an exact integer coefficient vector with a common2^96 scale. The reviewer recomputes its norm, affine Rayleigh polynomial, full quadratic second-moment polynomial and quadratic variance directly from accepted complete matrices. Every coefficient and every evaluated moment agrees. Variances are nonnegative, and both rho<r1<r2 and ell<r2 hold. Each normalized pencil expectation is strictly negative; every saved Temple lower and strict endpoint is independently checked. Selection of the energy or pencil proposal and all gains are compared exactly. The43D8×8 numerator Rayleigh data are also independently contracted from its accepted matrix.

Let a=r2 bound the second eigenvalue in the full untruncated even-singlet sector. For ell<a, a negative expectation of P(ell)=H²−(a+ell)H+a ell G implies the sector ground E0>ell: every eigenvalue other than the ground is≥a, and a ground≤ell would make every polynomial factor nonnegative. The stronger Temple lower rho−variance/(a−rho) is checked directly. This uses complete H², not the square of a projected H.

## Global ground and sector completeness
The directed reference cutoff is recomputed with a certified60-decimal lower enclosure of sqrt(1−4g). The full-Hilbert r1 comparison and rho<r1 identify a unique global ground, which is even and a singlet because the trial basis lies in that invariant sector.

Independently rebuild the fixedz=.1 odd family from accepted structural polynomials in Q(sqrt2). Every momentum Gram symbol is positive. Means, complete variances, directed enclosures, Temple lower bounds, cutoff margins and tail endpoints are recomputed at each coupling for both patches. All N distinct momenta and their spin-three multiplicity are counted, with no duplicate or missing mode. Each odd trial energy lies below r2. Thus the ground plus3N odd states exhaust the1+3N reference count below r2:49 on4×4 and97 on8×4. The next state in the even-singlet sector is≥r2. The review never treats r2 as the second eigenvalue of the full Hilbert space.

## Complete integration checks
The producer58D polynomial agrees entry-by-entry with the independently accepted matrix. All old57D principal blocks remain unchanged. The exact Gram is rank58. Fresh fraction-free elimination checks A² positive definite and H² positive definite at both couplings, with all pivots agreeing with the producer's GMP elimination.

For the operator Gram[[G,A],[A,A²]], use the exact triangular change of image vectors Aψ=(2/g)(Hψ−Qψ), with Q preserving each basis occupation. Its first58 LDL pivots equal those of G, and the second58 equal4/g² times the independently computed H-moment block pivots atg=.11. All116 predicted pivots equal the producer's saved pivots, giving PSD and rank87. This independently accounts for all nine producer LDL jobs without reusing its elimination implementation.

## Selected-target exclusions
An independent fraction-free Bareiss/LDL calculation proves every pivot strictly positive for four matrices J−(a+ell)H+a ell G. Its exact positive leading principal minors and common denominator scale are saved. All pivots agree with the independently reconstructed rational matrix and producer values.

Two targets are the previously accepted sufficient .11 ground32 targets for beta47/5 and10. Their exact values are checked against that source. Two further targets are explicitly chosen near the proposed endpoint and are not asserted scalar-sufficient. These positive-definite pencils exclude a negative-pencil/Temple witness reaching those particular ell values within the current58D basis and fixedr2 cutoff. They do not exclude a different cutoff, trial space, physical bound or bootstrap route. Sufficient target failure is not a universal no-go.

## Scalar diagnostics and resource caveat
The producer's saved-vector grid beta7…14 in increments.05 reported no all-size candidate. This review does not repeat the floating grid and gives it no no-go interpretation. No actual all-size certificate was supplied, and none is promoted here.

Producer resource compliance remains UNVERIFIED. Its initial LDL call timed out after six completed jobs; the resumed child reported33.13448 CPU seconds despite a configured25-second cap, and a trustworthy whole-task upper bound was not retained. Mathematical acceptance does not certify, repair or reinterpret that runtime record. The resource addendum remains a separate engineering limitation.

The independent full endpoint/count/target audit used48.34 process CPU seconds and28,992KiB; supplementary integration used1.10 CPU seconds and17,828KiB. These were separately bounded and measured under the authorized60-total-CPU-second/256MiB lane. A short witness-only replay verifies the rational physics/count gates again without repeating the costly four-target elimination. No physical contractions or producer optimizer runs were performed.

## Reproduction
Default REPRODUCE.sh checks seals, reruns fresh rational witness/count gates under6CPU seconds/256MiB, and checks the saved fraction-free pivot/minor relations. The expensive fresh target elimination is preserved as an independently computed sealed result. FULL_CACHED_REPLAY.sh requires a new budget authorization before another complete60-second cached batch. The default never starts a physical pass or optimizer.
