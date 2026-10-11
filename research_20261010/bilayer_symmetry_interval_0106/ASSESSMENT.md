# Closed coupling interval [.105,.106] with square symmetry

Updated 2026-10-11 00:46 UTC / 2026-10-10 20:46 EDT.

The entire closed interval **21/200<=g<=53/500** has the exact candidate gap

 **20881493369/10^12 = .020881493369**

for every integer periodic square L>=2, with a unique finite-volume ground state, pending separate independent review. No gap-monotonicity assumption is made. One interval sufficed; no subdivision or uncovered endpoint was used. Joining it to the already accepted [0,.105] theorem would extend the continuous range to [0,.106] while retaining the old smaller uniform lower bound, only after this interval's independent acceptance.

Initial beta is189/20=9.45. Exact finite windows cover [8,16],[16,32],[32,64],[64,128]; at side128, the canonical small-common-defect theorem applies with its independently checked exponential gap witness. The previously accepted short theorem on[0,.15] gives gap>.050426624396 for L2,...,7 and covers the remaining finite sizes uniformly. All exact trace components, physical margins, interval enclosures, states and witnesses are saved in result.json.

The denominator vectors remain the accepted g=.10516D and43D fixed vectors, evaluated through their complete coupling polynomials. The numerator is the accepted g=.10543D fixed vector, retaining one state. Retained trace counts are49/97/1; the largest full Hilbert dimension remains2^128. This job contracts no physical supports or matrices, runs no eigensolver, and changes no trial vector.

DERIVATION.md proves the enclosure directions before the computation: means are affine, complete residual squares are nonnegative convex quadratics, and each reference energy minus an affine mean is concave. Exact endpoint and Q(sqrt(2)) quadratic-form checks establish uniform global ground identification, even-sector cutoff and all odd counting margins. Uniform Temple widths, odd reference floors and every q>=2 tail term are included. The correlated numerator energies are enclosed as complete affine combinations before exponentiation, preserving the cancellation.

The source point package is sealedf0964e98022793c1f200e63c290acd340539e59833a6ecffc1610b4ef08132e3; its complete input hash list is checked before execution, in addition to its own manifest. INPUT_SHA256.json pins this interval's direct dependencies and the two independent square-symmetry proofs. All numerics are exact rationals or directed384-bit exponentials and60-decimal square roots. Floating beta scans only propose temperatures.

The separately authorized interval budget was120CPU seconds,256MiB and CPU2. Both initial computation and final provenance-checked replay together used under2CPU seconds and about14MiB. No predecessor or GitHub files changed. A bounded future optimized-vector test belongs to a separate package and must not modify this interval freeze.
