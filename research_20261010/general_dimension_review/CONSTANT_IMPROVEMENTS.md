# Sharper constants from the same purity proof

Date: 10 October 2026, 13:44 EDT / 17:44 UTC.

The improvements below retain the exact transfer hypotheses, periodic conventions, and common-scale geometric scope of `PROOF_REVIEW.md`. They do not enlarge the class of physical models. No frozen verifier or baseline certificate has been changed.

The two-dimensional constant `26` was rederived by the independent reviewer during this audit. The additional general-dimensional refinement below has a complete analytic proof and exact endpoint checks in this directory, but has not yet received a second independent review.

## 1. Two-dimensional constant 26

For a standard two-dimensional seed with all three defects at most

$$
0<u_*\le\frac1{200},
$$

the all-integer uniform gap bound improves to

$$
\boxed{\displaystyle
\Delta\ge\frac{\log(1/(26u_*))}{\beta_*}.}
$$

The finite-scale interpolation remains `T(L,W;beta)>=1-20u`. The recursion and scope are unchanged. The improvement is obtained by keeping the actual product loss in the common-defect estimate.

At every sequential step, three current purities at least `1-u` give a pre-square purity at least `(1-u)^7`. Define

$$
R_7(u)=\frac{f(1-(1-u)^7)}{u^2}
=\frac12\left[\sum_{r=1}^7(1-u)^{-r}\right]^2.
$$

Each summand is increasing for `0<=u<1`, so the coefficient is increasing. At the exact endpoint,

$$
R_7(1/200)
=\frac{3895544369762551059173832744020000}
       {152736582765019941952958691637201}
<26.
$$

The strict rational margin is

$$
26-R_7(1/200)
=\frac{75606782127967431603093238547226}
       {152736582765019941952958691637201}>0.
$$

Consequently each updated defect is at most `26u^2`. Since `26u<=13/100<1`, the updated entry stays within the same common bound `u`. This proves that the same estimate may be used at the next sequential step. After a complete cycle,

$$
u_{j+1}\le26u_j^2,\qquad
u_j\le\frac{(26u_*)^{2^j}}{26}.
$$

The already reviewed extension of the one-dimensional interpolation to `v<=1/40` justifies two-dimensional interpolation at `u<=1/200`, since the second application has `v=5u`. For completeness, its required endpoint checks are independently reproduced here:

$$
\frac{f(1-(1-v)^3)}{v^2}\bigg|_{v=1/40}
=\frac{17529408800}{3518743761}<5,
$$

$$
\frac32+5v+\frac2{1-2v}\bigg|_{v=1/40}
=\frac{567}{152}<4,
\qquad
1-5v-v^2\bigg|_{v=1/40}=\frac{1399}{1600}>0.
$$

The monotonicity and inverse-weight arguments are those proved in Section 4 of the review, and remain valid on this interval. The terminal probability ratio satisfies

$$
\frac{20u}{1-20u}
\le\frac{200}{9}u<26u.
$$

The same cancellation of `2^j` against `beta_j=2^j beta_*` now gives the boxed gap bound. The improvement over constant `32` at the same accepted seed is exactly `log(32/26)/beta_*`. This improves a certified lower bound, not the model's actual spectral gap.

## 2. Refined induction factor in dimension d

The general-dimensional proof bounded every transported last-axis purity by `(1-u)^2`. That limit is approached only after many swaps. For a preceding spatial edge with index `i>=1`, the numerator prefix requires at most `d-1-i` swaps. Its last-axis purity is therefore at least

$$
p\ge(1-u)^r,\qquad
1\le r\le r_d=2-2^{-(d-2)},\qquad d\ge2.
$$

For a changed last length `W/n_d=t` in `[1,2]`, the same signed-transfer estimates give

$$
P_i^{(W)}\ge(1-u)^t p^{t-1}(2p-1)
\ge(1-u)^2p(2p-1).
$$

The factors are nonnegative in the domain used below. Bernoulli's inequality gives `p>=(1-u)^r>=1-ru`. Hence

$$
P_i^{(W)}\ge(1-2u)(1-ru)(1-2ru)
\ge1-(2+3r)u\ge1-C_du,
$$

where

$$
C_d=8-\frac3{2^{d-2}}\quad(d\ge2).
$$

The terminal thermal edge still has defect at most `4u`, which is no greater than `C_du` because `C_d>=5`. Define

$$
P_1=1,\qquad P_d=\prod_{s=2}^d C_s,\qquad
\widehat F_d=4P_d,\qquad U_d=\frac1{40P_d}.
$$

Induction using the one-dimensional domain `1/40` proves

$$
T(L_1,\ldots,L_d;\beta)\ge1-\widehat F_du,
\qquad 0\le u\le U_d,
$$

for all integer intermediate box sizes. The identity `C_d U_d=U_(d-1)` checks the induction domain exactly. Also `widehat F_d U_d=1/10`, independent of dimension.

The first values of the new interpolation loss are `4`, `20`, `130`, `1885/2`, and `114985/16`. The corresponding original general loss factors are `4`, `32`, `256`, `2048`, and `16384`. The new `d=2` value recovers the specialized loss factor `20`.

## 3. A valid integer contraction and gap constant in every dimension

Let

$$
c_d=2^{d+1}-1,
$$

and define the exact endpoint coefficients

$$
A_d=\frac12\left[\sum_{r=1}^{c_d}(1-U_d)^{-r}\right]^2,
\qquad B_d=\frac{\widehat F_d}{1-\widehat F_dU_d}
=\frac{10}{9}\widehat F_d.
$$

A convenient valid integer is

$$
\widehat K_d=\left\lceil\max\{A_d,B_d\}\right\rceil.
$$

The improved theorem is then

$$
0<u_*\le U_d
\quad\Longrightarrow\quad
\Delta\ge\frac{\log(1/(\widehat K_du_*))}{\beta_*}
$$

on the same common dyadic boxes. In particular, the first six valid integer constants are

| Spatial dimension | Interpolation loss `widehat F_d` | Input threshold `U_d` | Valid integer `widehat K_d` |
| --- | --- | --- | --- |
| 1 | 4 | 1/40 | 5 |
| 2 | 20 | 1/200 | 26 |
| 3 | 130 | 1/1300 | 145 |
| 4 | 1885/2 | 1/9425 | 1048 |
| 5 | 114985/16 | 8/574925 | 7986 |
| 6 | 14373125/256 | 128/71865625 | 62384 |

These are valid sufficient constants. This argument does not establish optimality.

To prove the statement in all dimensions rather than infer it from the table, first note

$$
\frac{c_d^2}{P_d}\le\frac{49}{5}.
$$

At dimensions one and two, the ratios are `9` and `49/5`. For `d>=2`, the next ratio is divided by `C_(d+1)>=13/2` and multiplied by

$$
\frac{c_{d+1}^2}{c_d^2}=(2+1/c_d)^2
\le(2+1/7)^2=225/49<13/2.
$$

Thus it decreases after dimension two. It follows that

$$
c_d^2U_d\le49/200<1/4,
\qquad 2\widehat F_dU_d=1/5.
$$

The original contraction argument consequently bounds `A_d<=c_d^2`. Since `c_d^2` is an integer and `widehat F_d>=4`,

$$
\lceil A_d\rceil\le c_d^2,
\qquad \lceil B_d\rceil\le B_d+1\le2\widehat F_d.
$$

Therefore

$$
\widehat K_dU_d\le
\max\{c_d^2U_d,2\widehat F_dU_d\}\le49/200<1.
$$

This establishes the invariant small-defect domain for every dimension. The exact product-loss coefficient is increasing with `u`, so every sequential update is at most `A_du^2<=widehat K_du^2`. The thermal probability ratio is at most `B_du<=widehat K_du`. The recursion and gap extraction now proceed as in the reviewed theorem.

The all-dimensional proof is analytic. `exact_checks.json` separately records exact values through dimension six and the rational endpoint comparisons. No floating-point number is used to select these integers.

## Review status and adoption

The baseline general-dimensional theorem passes the independent audit without relying on these improvements. The independent reviewer separately confirmed the two-dimensional `K=26` algebra on 10 October 2026. The refined all-dimensional family should receive its own second review before project summaries label it independently verified.

Existing stored gap certificates remain unmodified. A new replay using these constants should state its accepted seed, common defect, inverse temperature, exact constant, short-size bridge, and geometric scope. The new constants alone do not validate uncertified heat traces or enlarge a seed's size coverage.
