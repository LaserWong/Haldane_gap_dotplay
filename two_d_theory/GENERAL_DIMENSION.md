# Staircase purities and integer hypercube interpolation in arbitrary dimension

October 10, 2026.
This note extends `THEORY.md` to general dimension.
The two-dimensional applications retain the sharper constant 32 proved there.
The constants below provide a conservative general theorem.

## 1. Transfer assumptions and staircase purities

Consider a finite periodic d-dimensional model with Z(L₁,…,L_d;β)>0.
For each spatial direction and every fixed choice of the other integer side lengths at least 2, assume an exact real selfadjoint Hilbert–Schmidt transfer representation valid for every integer length at least 2 in that direction.
Each seed length n_i is even.
Inverse temperature is the k=d+1 coordinate.

Let D_i double coordinate i and define P_i(v)=Z(D_iv)/Z(v)².
The spatial powers at every required base point are even, so 0<P_i≤1.
The temporal ratio is the Gibbs purity.
Doubling a coordinate in its own direction obeys the defect-squaring bound f(u)=u²/[2(1−u)²].
For a coordinate ordering (π₁,…,π_k), define the staircase inputs by

$$
Q_j=P_{\pi_j}(D_{\pi_{j-1}}\cdots D_{\pi_1}v).
$$

## 2. Sequential recurrence

The exchange identity

$$
P_i(D_jv)P_j(v)^2=P_j(D_iv)P_i(v)^2
$$

allows the first step to pass successively through the remaining k−1 steps.
The resulting lower bound is

$$
P_{\pi_1}(D_{\pi_k}\cdots D_{\pi_2}v)
\ge\prod_{j=1}^{k}Q_j^{2^{k-j}}.
$$

The product also reduces to a single corner ratio,

$$
\prod_{j=1}^{k}Q_j^{2^{k-j}}
=\frac{Z(D_{\pi_k}\cdots D_{\pi_1}v)}{Z(v)^{2^k}}.
$$

We then square in direction π₁, move the updated Q₁ to the end of the queue, and repeat for the remaining directions.
A complete cycle doubles all spatial lengths and β.
Each step uses the current queue, so the updates cannot be performed in parallel using the old values.

Set c_k=2^k−1.
If every input defect is at most u, the product loses at most c_k u.
For u≤1/(4c_k²),

$$
f(c_k u)\le c_k^2 u^2.
$$

Thus K≥c_k² and Ku≤1/4 give u'≤Ku² and

$$
u_j\le\frac{(Ku_*)^{2^j}}{K}.
$$

This recurrence holds for every coordinate ordering.
The base point of Q_j depends on its position, however, so reordering the coordinates requires new staircase inputs rather than a permutation of existing numerical values.

## 3. Interpolation to every integer side length

Fix the standard order (x₁,…,x_d,β) and define

$$
F_d=4\,8^{d-1}.
$$

If every staircase purity defect is at most u and u≤1/[100·8^(d−1)], then every integer L_i∈[n_i,2n_i] satisfies

$$
T(L_1,\ldots,L_d;\beta)\ge1-F_du.
$$

We prove this by induction on d.
For d=1, the statement is the all-integer interpolation lemma in Section 4 of `THEORY.md`.
For d≥2, first replace the final spatial length by an arbitrary W∈[n_d,2n_d].
The last-direction transfer purity must be controlled at each spatial staircase prefix.
When adjacent steps with purities (a,b) are exchanged, the new first edge has purity at least a√b.
Move the dth spatial direction successively to the left.
Each spatial edge not yet crossed is an original staircase edge and has purity at least 1−u.
If the moving edge has lower bound (1−u)^r, its bound after the next exchange is (1−u)^(1+r/2).
Starting from r=1 gives r<2 throughout.
The last-direction purity is therefore at least (1−u)²≥1−2u at every required prefix.

For each earlier spatial edge, the positive dominant eigenvalue and the spectral tail bound the numerator after the final length is changed.
Monotonicity of the absolute-spectrum ℓ^p norm bounds the denominator from above.
With t=W/n_d∈[1,2], these estimates give

$$
P_i^{(W)}\ge(1-u)^t(1-2u)^t
\left(1-\frac{2u}{1-2u}\right)
\ge(1-u)^2(1-2u)(1-4u)\ge1-8u.
$$

The final inequality follows from the Bernoulli product bound for finitely many nonnegative loss factors.
The one-dimensional lemma applied to the original dth spatial purity and temporal purity gives the terminal physical purity T≥1−4u.
At fixed W, the remaining d−1 dimensional staircase thus has all defects bounded by 8u.
The induction hypothesis yields T≥1−8F_(d−1)u, which gives F_d=8F_(d−1).
The condition u≤1/[100·8^(d−1)] keeps every induction step within the domain of the one-dimensional lemma.

The same proof includes odd side lengths.
Positivity of the dominant eigenvalue in absolute value follows from the exact transfer identity and the positive partition function at arbitrarily large odd powers.
No positive-kernel assumption is used.

## 4. Uniform gap in general dimension

Define

$$
K_d=\max\{(2^{d+1}-1)^2,\,2F_d\}.
$$

Suppose a standard staircase seed satisfies

$$
0<u_*\le\min\left\{\frac1{4K_d},\frac1{100\,8^{d-1}}\right\}.
$$

Every integer periodic Hamiltonian in each common-scale box 2^j n_i≤L_i≤2^(j+1)n_i then has a unique ground state and obeys

$$
\Delta_{L_1,\ldots,L_d}
\ge\frac{\log[1/(K_du_*)]}{\beta_*}.
$$

Indeed, F_du_j≤1/2, so the ratio of excited-state to ground-state Gibbs probabilities is at most

$$
\frac{F_du_j}{1-F_du_j}\le2F_du_j\le K_du_j
\le(K_du_*)^{2^j}.
$$

Using β_j=2^jβ_* gives the stated gap.
If all n_i are equal, the boxes cover every sufficiently large integer hypercube.
A single such seed does not establish a uniform gap for rectangles of arbitrary aspect ratio.

For d=2, the conservative general constant is K₂=64.
The dedicated two-dimensional proof gives K₂=32 and the wider interpolation domain u≤1/500.
The general result therefore leaves the numerical constants of the existing two-dimensional certificates unchanged.

## 5. Scope of the transfer assumptions

The exact transfer structure is a hypothesis of the theorem.
Finite-range interactions may be converted to nearest-neighbor interactions by finite blocking, but the real structure and an appropriate identical-factor or exchange-symmetric decomposition must still be checked after blocking.
General PEPS boundary transfers, nonselfadjoint transfers, approximate Trotter expansions, and uncontrolled tensor truncations do not automatically satisfy these assumptions.

All spatial recurrences share the same doubling of β.
The defect contracts with an exponent proportional to the linear scale 2^j, while the physical volume grows as 2^(dj).
The gap is extracted using inverse temperature, not volume.
