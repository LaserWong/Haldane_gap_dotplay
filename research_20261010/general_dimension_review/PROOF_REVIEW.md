# Independent review of the general-dimensional purity bootstrap

Review date: 10 October 2026, 13:42 EDT / 17:42 UTC.

## Verdict and evidence

The theorem in `two_d_theory/GENERAL_DIMENSION.md` is correct under its exact transfer and Gibbs assumptions. Its sequential recursion, all-integer interpolation, constants, and stated finite-volume gap scope pass this independent review. No correction to its numerical constants is required. The proof below supplies the basepoint bookkeeping and spectral details that are compressed in the original exposition.

The following qualifications are essential.

- The partition function is that of a finite-dimensional Hamiltonian which is independent of inverse temperature. Positivity of an otherwise arbitrary function called `Z` would not establish thermal purity or thermal squaring.
- Each spatial transfer is self-adjoint and Hilbert–Schmidt, and the exact trace identity holds for every integer length at least two at every fixed transverse geometry used in the proof. The transverse lengths may be odd after interpolation.
- All staircase spatial base lengths are even. A spatial ratio at an odd base length need not be a purity and can exceed one.
- Reordering the coordinates changes the basepoints. One cannot reorder previously measured numbers without transporting their bounds.
- The finite-volume result covers the stated union of common dyadic boxes. It does not cover all aspect ratios, all rectangles with a prescribed bounded aspect ratio, or all infinite-volume ground states.

`verify_general_dimension.py` imports no project proof or certificate routines. It uses integer matrix products and Python `Fraction`. The exact results are in `exact_checks.json`. The tests include all 118 cyclic rotation steps for every permutation in dimensions one through three, a genuinely interacting two-dimensional commuting model on every rectangle in `[2,4]^2`, independent full-basis enumeration on three small tori, and signed-transfer examples. These finite checks test formulas and implementation. The proof for arbitrary dimension is the analytic argument below.

Input SHA-256 values are recorded in the JSON. The working directory is an extracted snapshot with no `.git` metadata. `CURRENT_STATUS.json` identifies its source commit as `6be889a30f642bde77fb89af75b3a7379615bed1`, but this review does not independently assert a local Git checkout or remote publication. No baseline files were changed.

## 1. Spectral facts and their domains

Let `p_a` be a probability distribution and let its purity be `S=sum_a p_a^2=1-u`. Its maximum weight satisfies `p_max >= S`. If `S>1/2`, the maximum weight is unique.

After squaring the weights and normalizing, the new defect is

\[
1-\frac{\sum_a p_a^4}{S^2}
=\frac{2\sum_{a<b}(p_a p_b)^2}{S^2}
\le\frac{2(\sum_{a<b}p_a p_b)^2}{S^2}
=\frac{u^2}{2(1-u)^2}=f(u).
\]

This holds for `0<=u<1`. The function `f` is increasing on this domain. For a spatial transfer `X`, the probability weights are `|lambda_a|^n / Tr X^n`, where `n>=2` is even. Self-adjoint Hilbert–Schmidt operators are compact, and these powers are summable. For time doubling, the weights are the eigenvalues of the Gibbs density matrix. Thus the same squaring estimate applies in every coordinate.

Suppose a spatial even-power purity exceeds one half. There is a unique eigenvalue of largest absolute value. Call it `lambda_0`. It is positive. Indeed, if it were negative, the relative absolute tail at the even length `n` would be

\[
r_n=\sum_{a\ne0}|\lambda_a/\lambda_0|^n
=\frac{1-p_{\max}}{p_{\max}}<1.
\]

For any odd `L>=n`, the tail at `L` is at most `r_n`, so `Tr X^L` would be negative. This contradicts the exact positive physical partition function. This argument is valid for an infinite-rank Hilbert–Schmidt transfer because the tail is absolutely summable. No positivity-preserving kernel or positive-semidefinite transfer is assumed.

The relevant monotonicity statements have different domains.

- At fixed `X`, the absolute-spectrum purity `sum |lambda|^(2p)/(sum |lambda|^p)^2` is increasing with `p>=2`. For a signed spectrum, its identification with the physical spatial ratio is valid at even integer base lengths. It does not imply monotonicity of physical ratios through odd lengths.
- At fixed finite-dimensional Hamiltonian, Gibbs purity is increasing for `beta>=0`. Differentiating its logarithm gives `2(U_beta-U_(2 beta))>=0`.
- Spatial purity need not increase with inverse temperature, since the spatial transfer itself changes with temperature. The bootstrap uses the exact exchange identity instead of such a monotonicity claim.
- The function `w^2+(1-w)^2` used to invert a high purity is increasing only on `w>=1/2`. This domain is established before that estimate is used below.

For the first statement, logarithmic differentiation at `p>2` gives twice the difference of the expectations of `log|lambda|` under the `2p` and `p` weights. That difference is nonnegative by log-convexity of the moment sum. The endpoint `p=2` follows by dominated continuity. Zero eigenvalues contribute zero and can be omitted.

## 2. Staircase coordinates and sequential cycling

Write `k=d+1`, with inverse temperature as one coordinate. For a basepoint `v`, define

\[
P_i(v)=\frac{Z(D_i v)}{Z(v)^2}.
\]

At every basepoint used before interpolation, spatial base lengths are even. Hence `0<P_i(v)<=1`, including when `i` denotes time. Commuting the coordinate doublings gives

\[
P_i(D_jv)P_j(v)^2=P_j(D_iv)P_i(v)^2.
\]

For an ordered list `(i_1,...,i_k)`, let

\[
v_j=D_{i_j}\cdots D_{i_1}v,\qquad
Q_j=P_{i_j}(v_{j-1}),\qquad v_0=v.
\]

All intermediate partition functions cancel in the weighted product,

\[
\prod_{j=1}^k Q_j^{2^{k-j}}=\frac{Z(v_k)}{Z(v)^{2^k}}.
\]

Let `w=D_(i_k)...D_(i_2)v`. Repeatedly using purity at most one along the path from `v` to `w` gives `Z(w)<=Z(v)^(2^(k-1))`. Consequently,

\[
P_{i_1}(w)=\frac{Z(v_k)}{Z(w)^2}
\ge\prod_{j=1}^k Q_j^{2^{k-j}}.
\]

Now double coordinate `i_1` itself. Its purity at `D_(i_1)w=v_k` has defect bounded by applying `f` to the product loss. Use the new basepoint `D_(i_1)v` and rotate the order to `(i_2,...,i_k,i_1)`. The first `k-1` staircase values are exactly the old `Q_2,...,Q_k`. The last is the newly squared purity just bounded. Repeating this operation `k` times restores the original ordering and changes the basepoint to `D_(i_k)...D_(i_1)v`. Every spatial length and inverse temperature has doubled exactly once.

Thus the sequential update is justified for every coordinate permutation. Later updates must use the transported current queue. A common invariant bound `u` may be reused once invariance is proved, but this does not justify treating the original measured entries as values at the new basepoints.

Let `c_k=2^k-1`. If all current defects are at most `u`, the product loss is at most `c_k u`. If `K>=c_k^2` and `Ku<=1/4`, then

\[
c_k u\le\frac1{4c_k}\le\frac1{12},\qquad
\frac{f(c_k u)}{c_k^2u^2}
=\frac1{2(1-c_k u)^2}\le\frac{72}{121}<1,
\]

where `d>=1` gives `c_k>=3`. The new defect is at most `Ku^2<=u/4`, so the common bound is valid at the next sequential step. After a complete cycle,

\[
u_{j+1}\le K u_j^2,\qquad
u_j\le\frac{(Ku_*)^{2^j}}K.
\]

This is an analytic proof for every dimension. The finite list of exact dimension endpoints in the executable is an additional arithmetic check.

## 3. Reordering bounds without losing their basepoints

For two adjacent staircase values `a=P_i(v)` and `b=P_j(D_i v)`, denote the swapped values by `c=P_j(v)` and `e=P_i(D_j v)`. Their exact relation is `e c^2=b a^2`. Since both swapped values are at most one,

\[
c\ge a\sqrt b\ge ab,\qquad e\ge a^2b.
\]

The rational conservative transport is therefore `(a,b) -> (ab,a^2 b)`, with the axis labels and basepoints transported at the same time. At most `k(k-1)/2` adjacent swaps suffice to put any permutation in standard order. If a common defect bound is used, each such conservative swap increases that bound by at most a factor of three while it remains meaningful. This is a conversion bound, not equality of permuted measurements.

For the interpolation proof, use the sharper square-root bound. Move the last spatial direction left through the preceding spatial directions, keeping time last. Every not-yet-crossed stationary edge still has its original lower bound `1-u`. After `ell` crossings, the moving edge is at least

\[
(1-u)^{r_\ell},\qquad
r_0=1,\quad r_{\ell+1}=1+r_\ell/2,\quad
r_\ell=2-2^{-\ell}<2.
\]

Hence the last-direction purity is at least `(1-u)^2>=1-2u` at every needed prefix. This explicitly justifies the prefix assertion in `GENERAL_DIMENSION.md`.

## 4. All-integer one-dimensional lemma

Assume `S(n,beta)>=1-v` and `T(2n,beta)>=1-v`, with even `n>=2` and `0<v<=1/100`. The exchange identity and `T(n,beta)<=1` give `S(n,2 beta)>=(1-v)^3>1/2`.

The maximum normalized weight `w` of `X_(2 beta)^n` is therefore at least one half. If `w<=1-2v`, then

\[
S(n,2\beta)\le w^2+(1-w)^2
\le1-4v+8v^2<(1-v)^3,
\]

because the final positive difference is `v(1-5v-v^2)`. Therefore `w>1-2v`, and the absolute tail ratio is at most `2v/(1-2v)`. The dominant eigenvalue is positive by Section 1.

The squaring estimate also gives `S(2n,2 beta)>=1-5v^2`. Indeed,

\[
\frac{f(1-(1-v)^3)}{v^2}
=\frac{(3-3v+v^2)^2}{2(1-v)^6}.
\]

The positive square-root factor is increasing, since the derivative of `(3-3v+v^2)/(1-v)^3` has numerator `6-4v+v^2>0`. At `v=1/100`, the coefficient is exactly `4410747005000/941480149401<5`.

For any integer `n<=L<=2n`, put `t=L/(2n)` in `[1/2,1]`. The positive dominant eigenvalue and its relative tail give

\[
Z_L(2\beta)\ge[(1-5v^2)Z_{2n}(2\beta)]^t
\left(1-\frac{2v}{1-2v}\right).
\]

Absolute-spectrum Hölder interpolation gives, also for odd `L`,

\[
Z_L(\beta)\le\sum_a|\lambda_a|^L
\le Z_n(\beta)^{2-2t}Z_{2n}(\beta)^{2t-1}.
\]

Dividing yields

\[
T(L,\beta)\ge S(n,\beta)^{2-2t}T(2n,\beta)^t
(1-5v^2)^t\left(1-\frac{2v}{1-2v}\right).
\]

The first two factors are at least `(1-v)^(2-t)>=1-(3/2)v`. The third is at least `1-5v^2`. All factors are nonnegative. Their product is at least one minus the sum of losses, and

\[
\frac32+5v+\frac2{1-2v}
\le\frac{3519}{980}<4.
\]

It follows that `T(L,beta)>=1-4v`. The case `v=0` follows directly from rank-one transfer and Gibbs spectra. No limiting operation in system size or temperature has been exchanged.

## 5. Induction over spatial dimension

Assume a standard staircase `(x_1,...,x_d,beta)` whose defects are at most `u`. Fix an arbitrary integer `W` in `[n_d,2n_d]` and write `t=W/n_d` in `[1,2]`. For a preceding spatial edge `i`, its numerator has the first `i` spatial coordinates doubled. At that prefix, Section 3 bounds the last-direction purity below by `1-2u`.

The dominant eigenvalue of this last-direction transfer is positive. Its normalized `n_d`-power weight is at least `1-2u`, and its absolute tail ratio is at most `2u/(1-2u)`. Therefore the numerator at length `W` is at least its value at `n_d` raised to `t`, multiplied by

\[
(1-2u)^t\left(1-\frac{2u}{1-2u}\right).
\]

For the denominator transfer, no high-purity hypothesis is required. Absolute-spectrum norm monotonicity gives

\[
Z(W)\le\sum_a|\lambda_a|^W
\le\left(\sum_a|\lambda_a|^{n_d}\right)^{W/n_d}
=Z(n_d)^t.
\]

After dividing the partition functions, the altered spatial purity satisfies

\[
P_i^{(W)}\ge(1-u)^t(1-2u)^t
\left(1-\frac{2u}{1-2u}\right)
\ge(1-u)^2(1-2u)(1-4u)\ge1-8u.
\]

All factors are nonnegative in the stated domain. The final polynomial remainder is

\[
(1-u)^2(1-2u)(1-4u)-(1-8u)
=u^2(21-22u+8u^2)\ge0.
\]

At the terminal spatial prefix, the original last-space and time purities directly supply the one-dimensional lemma. Thus the terminal thermal purity after replacing `n_d` by `W` is at least `1-4u`. The reduced `(d-1)`-dimensional staircase therefore has all defects at most `8u`.

For

\[
U_d=\frac1{100\,8^{d-1}},\qquad F_d=4\,8^{d-1},
\]

one has `8U_d=U_(d-1)`. The one-dimensional base case and induction establish

\[
T(L_1,\ldots,L_d;\beta)\ge1-F_du
\]

for all integer `n_i<=L_i<=2n_i` whenever `u<=U_d`. An odd fixed `W` is legitimate because the transfer assumption includes every transverse integer geometry. This is the point where an assumption limited to even transverse widths would be insufficient.

## 6. Uniform gap and exact geometric scope

Take

\[
K_d=\max\{(2^{d+1}-1)^2,2F_d\},\qquad
0<u_*\le\min\{1/(4K_d),U_d\}.
\]

The recursion preserves this domain. In fact, interpolation gives `F_d u_j<=1/25`, stronger than the one-half condition used in the original argument. The largest Gibbs weight is at least the purity and therefore exceeds one half. The ground state is unique, and

\[
e^{-\beta_j\Delta_{L_1,\ldots,L_d}}
\le\frac{F_du_j}{1-F_du_j}
\le2F_du_j\le K_du_j\le(K_du_*)^{2^j}.
\]

Since `beta_j=2^j beta_*`,

\[
\Delta_{L_1,\ldots,L_d}\ge\frac{\log(1/(K_du_*))}{\beta_*}
\]

on every common dyadic box specified in the original statement. The scale cancellation uses inverse temperature, not physical volume.

For an equal-sided seed, every integer cube side `L>=n_*` lies in at least one such interval. For an unequal-sided seed, the exact scope remains the union of the boxes. Even bounded aspect ratio alone does not characterize that union. For instance, normalized coordinates three and five have ratio less than two but do not occupy a common interval `[2^j,2^(j+1)]`.

A corresponding GNS gap for a local weak limit would additionally use a consistent finite-range interaction and the local finite-volume gap inequality. This theorem alone does not prove uniqueness across all infinite-volume ground states or boundary conditions.

## 7. Exact diagnostic models and counterexamples

The interacting two-dimensional test is the diagonal Hamiltonian

\[
H=4\sum_r n_r+2\sum_{r,e\in\{x,y\}}n_r n_{r+e},\qquad n_r\in\{0,1\}.
\]

At `beta=log(16)`, all Boltzmann weights are rational. A symmetric row transfer uses half of each row energy on either side of its cross-row coupling. For transverse width two, its principal minor on row states `00` and `01` is `q^4(q^2-1)<0`, where `q=1/16`. Thus its spectrum is genuinely signed, despite positive matrix entries. All nine rectangles in `[2,4]^2` satisfy the certified interpolation bounds. Direct enumeration at `2x2`, `2x3`, and `3x3` agrees exactly with the independently constructed transfer trace and verifies the periodic doubled-edge convention. The unique vacuum ground state has exact gap four.

The higher-dimensional tests are independent stacks of interacting chains,

\[
H=2\sum_r n_r+2\sum_r n_r n_{r+e_1}.
\]

Their chain transfer is `[[1,q],[q,q^4]]` with `q=1/2048`, and determinant `q^4-q^2<0`. They have exact gap two. These models test every permutation and all integer box sides in dimensions one through three. They are not offered as genuinely coupled three-dimensional applications.

Two exact counterexamples delimit the proof's monotonicity and basepoint assertions.

1. For `X=diag(1,-1/16)`, all integer traces are positive, but

   \[
   S(2)=65537/66049<1,\qquad S(3)=16777217/16769025>1.
   \]

   Thus physical spatial ratios cannot be treated as purities at odd bases, even though their partition functions are positive. A real orthogonal conjugate of this transfer has strictly positive entries, so an entrywise-positive kernel does not fix the error.

2. For the zero-field ferromagnetic Ising chain at `beta=log(2)` and even base length two, the transfer eigenvalues are `5/2,3/2`. At `2 beta` they are `17/4,15/4`. Consequently,

   \[
   S(2,\beta)=353/578,\qquad S(2,2\beta)=67073/132098<353/578.
   \]

   Cooling lowers this spatial purity. The `x,beta` staircase is `(353/578,67073/249218)`, whereas the `beta,x` staircase is `(257/578,67073/132098)`. Merely swapping the former pair supplies a false lower bound for the latter spatial entry.

These are counterexamples to unlicensed extensions of the argument, not to the theorem under review.

## 8. Reproduction and additional improvement

Run from the repository root:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research_20261010/general_dimension_review/verify_general_dimension.py
```

The script has no third-party dependency and uses one process. It writes only within this new review directory. Its runtime field is a diagnostic float. All acceptance comparisons use exact rational or integer arithmetic.

`CONSTANT_IMPROVEMENTS.md` separately records a sharper dimension-dependent interpolation factor and the two-dimensional contraction/gap constant `26` on the already-reviewed domain `u<=1/200`. These are improvements, not repairs required by the general-dimensional theorem.
