# An enlarged two-dimensional all-integer acceptance domain

Date 10 October 2026. Root independent review of the previously audited one-dimensional domain extension and the two-dimensional interpolation proof.

## Statement

Under the exact real self-adjoint Hilbert–Schmidt thermal-transfer hypotheses of `two_d_theory/THEORY.md`, the two-dimensional theorem remains valid with the common seed defect threshold enlarged from 1/500 to **1/200**. The contraction constant remains 32, the all-integer finite-scale purity-loss constant remains 20, and the uniform gap bound remains

$$
\Delta \ge \beta_*^{-1}\log\frac{1}{32u_*}.
$$

The logarithmic statement assumes 0<u_*≤1/200. Zero defect is the rank-one limiting case and is handled directly.

The scope is unchanged and covers rectangles in the same dyadic scale boxes and, for a square seed, every integer square side at least the seed side. This does not establish a uniform statement for arbitrary aspect ratios.

## One-dimensional domain

The independent review in `audit/NEW_RESULT_REVIEWS.md`, section 4, already establishes the one-dimensional interpolation for common defect v≤1/40. For completeness, the endpoint checks used there are independently recomputed using exact fractions in `interpolation_domain.py`.

The first contraction coefficient is

$$
\frac{(3-3v+v^2)^2}{2(1-v)^6}\le5.
$$

Its square-root factor increases because differentiating (3−3v+v²)/(1−v)³ leaves the positive numerator 6−4v+v². The thermal coefficient obtained after the first update is bounded by

$$
\frac{(2+5v)^2}{2(1-2v-5v^2)^2}\le5.
$$

This is increasing while its denominator is positive, so the endpoint suffices. The interpolation proof requires

$$
\frac32+5v+\frac{2}{1-2v}<4,
$$

which is increasing and equals 567/152 at v=1/40. The inverse-purity step has positive margin v−5v²−v³ for 0<v≤1/40. These are analytic interval arguments with exact endpoint arithmetic, not a numerical grid argument.

## Two-dimensional extension

For 0≤u≤1/200, the same three-purity sequential recursion gives

$$
f(7u)\le\frac{49}{2(1-7u)^2}u^2\le32u^2\le u.
$$

The coefficient is increasing and equals 980000/37249<32 at the endpoint. Each updated defect remains at most u, so the same bound applies at the next sequential step.

The transverse signed-transfer interpolation in the existing proof gives the longitudinal spatial purity at arbitrary intermediate transverse integer length at least 1−5u. The thermal purity at twice the longitudinal seed length is at least 1−4u. The second one-dimensional interpolation is now legal because 5u≤1/40. Hence every intermediate integer rectangle has thermal purity at least 1−20u.

Its largest Gibbs weight is at least this purity and exceeds 1/2, giving a unique ground state and

$$
e^{-\beta\Delta}\le\frac{20u}{1-20u}\le32u.
$$

The last coefficient is increasing and equals 200/9<32 at u=1/200. Iterating u_j≤(32u_*)^{2^j}/32 and β_j=2^jβ_* yields the stated scale-independent gap.

## Verification and use

Run `python research_20261010/root_review/interpolation_domain.py` from the repository root. The JSON records exact endpoint fractions and hypothesis/scope. It checks arithmetic only. The analytic arguments above and the archived transfer/interpolation proof supply the continuous-domain reasoning.

No frozen checkpoint verifier is modified. New candidate replays may use this larger domain only when they explicitly record that they use this extension. Existing certificates with u≤1/500 remain unchanged.

In an independent second review, the ordinary-bilayer auditor checked this proof and its exact endpoint script on 10 October 2026 and confirmed the continuous-domain extension through 1/200.
