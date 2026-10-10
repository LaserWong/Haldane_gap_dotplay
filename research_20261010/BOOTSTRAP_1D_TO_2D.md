# From one to two spatial dimensions: bootstrap and required inputs

Updated 2026-10-10 17:26 EDT / 21:26 UTC.

This note answers the user's question about the structural difficulty of the two-dimensional extension and whether it requires full-spectrum diagonalization. The accepted model and boundary conventions are in [MODELS_AND_NORMALIZATION.md](MODELS_AND_NORMALIZATION.md).

## 1. The same scalar mechanism with one additional axis

A one-dimensional ladder doubles spatial length and inverse temperature. A two-dimensional ladder doubles two spatial lengths and inverse temperature. Each edge is a partition-function ratio with the denominator squared. If the edges form one consistently ordered ladder from a common initial basepoint, cancellation gives

$$
S^2T=\frac{Z(2n,2\beta)}{Z(n,\beta)^4}
$$

in one dimension, and

$$
A^4B^2C=\frac{Z(2n,2m,2\beta)}{Z(n,m,\beta)^8}
$$

in two dimensions. The variables on the left are the successive spatial/thermal purity ratios along the stated ladders. They are not all evaluated at the initial geometry. More explicitly, let v=(n,m,β), let D_i double coordinate i, and define P_i(v)=Z(D_i v)/Z(v)^2. Then A=P_x(v), B=P_y(D_x v), and C=P_t(D_y D_x v). A full cycle reaches the common base (2n,2m,2β).

The purification function is

$$
G(z)=1-\frac{(1-z)^2}{2z^2}.
$$

One-dimensional canonical updates are

$$
S'=G(S^2T),\qquad T'=G(T^2S').
$$

Two-dimensional canonical updates are

$$
A'=G(A^4B^2C),\qquad B'=G(B^4C^2A'),\qquad C'=G(C^4(A')^2B').
$$

These are sufficient lower-bound updates. Positive first output requires the corresponding argument to exceed sqrt(2)-1. This is only the first necessary gate for this update, not a complete startup or all-size criterion. For illustration, setting every input to 0.85 gives 0.85^3=0.614125 in one dimension and 0.85^7=0.32057708828125 in two dimensions. The extra axis makes comparable input uncertainty more costly.

Once certified inputs enter the contracting regime, the larger-size continuation is scalar. No new many-body diagonalization is needed at each doubling. Retaining separately certified joint ratios improves over multiplying independently weakened edge bounds. See [the independent joint-ratio lemma](joint_ratio_review/GENERAL_LEMMA.md).

## 2. Model-specific work remains essential

The spatial ratios must have a valid self-adjoint transfer representation. For the ordinary antiferromagnetic bilayer, the rung basis makes the local column evolution real and the continuous-time bond-history kernel symmetric. An absolutely convergent expansion gives the physical partition function as the trace of the spatial transfer operator raised to the circumference. This is verified in both spatial directions in [the physical transfer proof](bilayer_audit/PROOF.md).

The transfer operator itself need not be positive. Even seed lengths make its even powers positive and allow the purity bounds. Odd target sizes require the separately proved signed-transfer interpolation. Two-dimensional all-size certificates also need interpolation in both directions, all finite windows before asymptotic contraction, and the smallest-size bridge. A successful dyadic or asymptotic sequence alone is insufficient.

The scalar extension is therefore relatively direct for this verified model class. Its transfer hypotheses and startup estimates do not automatically hold for arbitrary two-dimensional Hamiltonians. No general efficient algorithm for all two-dimensional gap problems is claimed.

## 3. Partial spectral data suffice when the omitted spectrum is controlled

For an orthonormal family of trial vectors with Rayleigh quotients R_j, spectral Jensen gives

$$
Z(\beta)\geq\sum_j e^{-\beta R_j}.
$$

A single normalized vector therefore supplies a valid partition-function lower bound. No residual or certified ground-state identification is required for this particular lower bound.

Upper bounds are more demanding. If certified lower spectral endpoints are l_j and the remaining eigenvalues are covered by bins with lower endpoints b_q and valid multiplicities m_q, then

$$
Z(\beta)\leq\sum_j e^{-\beta l_j}+\sum_q m_qe^{-\beta b_q}.
$$

Every omitted eigenvalue must be accounted for, with correct multiplicity and index bookkeeping. In the present bilayer certificates, trial matrices, residual/Temple or moment bounds, and analytic counted spectral comparisons supply these data. A list of approximate low eigenvalues without an omitted-spectrum bound would not suffice.

## 4. Actual inputs at g=0.09

The accepted point certificate uses the following seed geometries:

| Rung patch | Physical spins | Full Hilbert dimension | Information used |
|---|---:|---:|---|
| 4×4 | 32 | 2^32 | Certified low band of 49 states plus a complete omitted-spectrum bound |
| 8×4 | 64 | 2^64 | Certified low band of 97 states plus a complete omitted-spectrum bound |
| 8×8 | 128 | 2^128 | One Rayleigh trial contribution, found in a 43-dimensional search |

The smaller denominator ground searches remain 11 and 29 dimensional. Their total trial dimensions including the odd low-band directions are 59 and 125. The 49/97 counts are not dimensions of the full physical spaces, nor a requirement to obtain exact eigenvalues. The largest numerator requires only one retained state; 43 is its search dimension, not its number of retained levels.

Exact moment construction still has a computational cost. In this implementation symmetry and local spin contractions avoid enumerating the full 2^128 physical basis. The independent reviewer also checked many intermediate support configurations, so small search dimension should not be equated with zero preparation cost or a general polynomial complexity guarantee.

The resulting independently accepted bound is gap ≥0.027330086079 for all integer square side lengths L≥2, with a unique finite-volume ground state. See [the exact-third-moment review](third_moment_review/REVIEW.md). The continuous interval [0,.09] is separately covered by [the interval review](interval_range_009_review/REVIEW.md).
