# Fixed-vector intermediate coupling points with square symmetry

Updated 2026-10-11 00:42 UTC / 2026-10-10 20:42 EDT.

## Exact point candidate

At ordinary bilayer g=53/500=.106, beta0=47/5, the new square-symmetry recurrence and direct finite windows give the exact candidate

 gap >= 10472755223/500000000000 = .020945510446

for every integer periodic square L>=2, with a unique finite-volume ground state, pending separate independent numerical review. This is a POINT result and does not certify the intervening coupling interval by gap monotonicity.

Finite windows: [8,16] .093800446778; [16,32] .060178164912; [32,64] .043053333712; [64,128] .035405649093. At side128, the canonical small-common-defect theorem applies, giving the stated .020945510446. The independently accepted short theorem on 0<=g<=.15 gives >.050426624396 for every L2,...,7 and therefore exceeds the final target.

candidate_g0106.json saves the point's complete exact physical scalar data, new-coupling gates, trace ratios, all recurrence states and final exponential witness. result.json preserves all four point assessments. The stronger square-window and recurrence theorems are independently sealed separately.

## Fixed vectors and complete matrix provenance

The first exploratory pass held only the already accepted g=.11 endpoint vectors fixed; it missed all four sampled intermediate couplings. Those results are preserved as fixed011_*. These misses are not no-go theorems. The second pass also reused the already accepted g=.105 vectors and took the stronger physically valid lower endpoint at each new point. No eigensolver, trial-vector optimization, support extension or full-space physical contraction was run.

For the accepted .106 candidate, both chosen ground-lower vectors are the .105 vectors, of dimensions16 and43. Their complete moment polynomials were recomputed by finite matrix contractions of the independently accepted21D and57D split G/H/H² arrays, embedding the old tied R+M coefficients exactly. Complete q8 image contributions remain in H². At .105 their norm/mean/variance reproduce the previously independently accepted physical witnesses exactly; the alternate .11 vectors similarly reproduce their .11 endpoints. The largest numerator selects the saved43D upper-energy vector. It retains one state in the full2^128 Hilbert space; denominator low-band counts remain49 and97. Ambient split matrix dimension57 is not the dimension of the selected43D vector.

At each newly tested coupling, the full mean, complete variance, global r1 ground-identification margin, even-sector r2 cutoff and every fixed-z=.1 odd Gram/mean/variance/cutoff margin are recalculated exactly. The r2 sector interpretation is justified by the same complete count: one even ground plus3N positive-Gram odd directions below r2, while the global reference count permits at most1+3N. Odd lower endpoints include the valid global r1 floor. The entire q>=2 reference tail remains in every trace upper bound. No interpolation of certified gaps or unverified monotonicity in g is used.

Denominator pivots are normalization choices and do not change spectral counts. source matrices and every external input are pinned in INPUT_SHA256.json; source independent-review seals are also saved in fixed_moment_polynomials.json. produce.py verifies the major complete reviews before calculation.

## Arithmetic and bounded misses

A finite beta grid8,...,13 in steps.05 proposed temperatures. At .106 it found53 successful candidates; the exact best selected temperature is47/5. The same grid found no candidate at .107,.108,.109 with these fixed-vector choices. This does not exclude a different temperature, scalar schedule or fixed vector.

All acceptance uses exact rationals, integer-square-root enclosures, and directed384-bit exponentials. In this program, the positive Taylor terms are themselves rounded outward at384 bits; interval induction encloses every term and the final geometric remainder, then directed squaring and inversion preserve containment. No floating eigenvalue or logarithm accepts a certificate.

The final replay uses CPU2, single-thread libraries,256MiB and a65-CPU-second hard limit; observed runtime was about3CPU seconds/18MiB. Together with the preceding .11 pilot and initial fixed-.11 diagnostic, work remains below the originally assigned120-CPU-second cumulative budget. No GitHub or predecessor files were changed. The separately authorized closed-interval extension belongs in a new directory.
