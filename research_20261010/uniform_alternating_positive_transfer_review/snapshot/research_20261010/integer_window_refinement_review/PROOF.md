# Independent audit: direct time-first integer windows

Updated 2026-10-10 18:12 EDT (America/New_York) / 22:12 UTC.

## Acceptance and scope

The new direct interpolation is proved below without a space/time relabeling or an assumption that physical purity is monotone in chain size. Independent exact scalar replay accepts all integer M>=2 for the periodic alternating spin-one chain at these discrete couplings:

| g | certified gap | initial beta | extra time-first cycles | asymptotic onset M | asymptotic beta |
|---|---:|---:|---:|---:|---:|
| .21 | .107424972 | 8.19 | 4 | 128 | 262.08 |
| .22 | .071581253 | 8.1 | 4 | 128 | 259.2 |
| .225 | .051807500 | 8.25 | 5 | 256 | 528 |

These are pointwise certificates, not a continuous interval. They inherit the physical input certification in `chain_frontier_above_02_review`; no Hamiltonian or full physical spectrum was recomputed here. The source input hash is independently matched against that review's frozen producer manifest. The rank-195 g=.25 inputs similarly match `chain_frontier_rank195_review`.

At g=.25, beta=1884/125 at the window, the new lemma certifies gap >=1/100 on the new 8<=M<=16 window. Together with the independently replayed initial [4,8] window at beta=942/125 and local M=2,3 bounds, every integer 2<=M<=16 has gap >=1/100. Its next time-first update has argument approximately .3870258342574809 and b_next approximately -.25422206217257126. This is not an all-size gap result. The earlier exact all-beta obstruction continues to concern only its specifically defined old canonical transport and first-window recipe; the present lemma escapes that first-window obstruction. A failed bounded scan of the new route is not a global impossibility theorem.

## 1. Physical and operator hypotheses

The Hamiltonian is H_M=sum_j [S_(2j-1) dot S_(2j)+g S_(2j) dot S_(2j+1)], with 2M spin-one sites, M>=2, periodic bonds and strong exchange one. Gap units are this exchange. The finite-size convention, physical dimensions 9^4=6561 and 9^8=43,046,721, and energy shifts H'_M=H_M+2M I are exactly those of the inherited reviews. Additive shifts linear in M do not change T or S.

Use the established homogeneous, exchange-invariant, cell-time-reversal-invariant history transfer for this model, grouping weak bonds inside cells and unit strong bonds between cells. At each fixed finite beta>0 it is a real self-adjoint Hilbert–Schmidt operator X_beta, with Z_M(beta)=Tr X_beta^M for every integer M>=2. The bounded kernel and finite history-measure mass prove the Hilbert–Schmidt property for every finite g,beta in question; the old width(v)<=.03 requirement belonged to the analytic seed, not to existence of the transfer. This is the construction described in `audit/AUDIT_REPORT.md` and `chain_audit/CHAIN_CERTIFICATE_PROOF.md`.

A Hilbert–Schmidt operator is compact. Its real eigenvalues form an l2 sequence, with multiplicities, and its Mth power is trace class for every integer M>=2. Thus each trace equals an absolutely convergent sum of Mth eigenvalue powers. All norm inequalities below apply to countable sequences; none requires Tr X_beta to exist. The physical finite-dimensional thermal trace is strictly positive for every integer M>=2. Positivity only at even sizes would be insufficient.

No positivity of all transfer eigenvalues, positive-entry kernel, or Perron–Frobenius theorem is required. The Hilbert spaces at beta and 2beta need not be identified.

## 2. Direct lemma and proof

Fix even n>=2 and beta>0. Write exact values

A=T(n,beta)=Z_n(2beta)/Z_n(beta)^2,
B=S(n,2beta)=Z_(2n)(2beta)/Z_n(2beta)^2>1/2.

Let certified endpoints satisfy 0<a<=A<=1 and 1/2<b<=B<=1, and put w=(1+sqrt(2b-1))/2. For every integer n<=M<=2n, p=M/n:

- odd M: T(M,beta)>=a^p [w^p-(1-w)^p];
- even M: T(M,beta)>=(a w)^p.

Let mu_j be eigenvalues of Y=X_(2beta). Since n is even, q_j=|mu_j|^n/Z_n(2beta) is a probability distribution with purity B. If q_* is its largest weight, B<=q_* implies q_*>1/2. Also B<=q_*^2+(1-q_*)^2, hence q_*>=w. It is unique, so the corresponding mu_* is the unique largest-modulus eigenvalue.

That eigenvalue is positive. Indeed, compactness and uniqueness give r=max_(j != *) |mu_j/mu_*|<1. For m>=n the absolute relative tail is bounded by r^(m-n) sum_(j != *) |mu_j/mu_*|^n, which tends to zero. If mu_*<0, all sufficiently large odd traces would therefore be negative, contradicting physical Z_m(2beta)>0.

For p>=1, sum_(j != *) q_j^p <= (sum_(j != *) q_j)^p=(1-q_*)^p. Thus the normalized numerator is at least q_*^p for even M, and at least q_*^p-(1-q_*)^p for odd M. Both expressions increase with q_* on [1/2,1].

Independently, if lambda_j are eigenvalues of X_beta, absolute-spectrum norm monotonicity gives

0<Z_M(beta)<=sum_j |lambda_j|^M<=(sum_j |lambda_j|^n)^(M/n)=Z_n(beta)^p.

Divide the numerator estimate by the squared denominator estimate. This proves the claim, with A^p replaced safely by a^p. This step relates two trace ratios by their definitions; it does not identify thermal and spatial operators or interchange their roles.

## 3. Uniform simplification and endpoint directions

For p in [1,2], define f_p(w)=w^p-(1-w)^p-(2w-1). It vanishes at w=1/2 and w=1. For 1<p<2 its second derivative is p(p-1)[w^(p-2)-(1-w)^(p-2)]<=0 on (1/2,1). Hence f_p>=0 by concavity. At p=1,2 the identity is exact; endpoint continuity handles w=1. For even M, w^p>=w^2>=2w-1. Since 0<a<=1 implies a^p>=a^2,

T(M,beta)>=a^2 sqrt(2b-1)

uniformly on the entire integer window. Only this simplification requires the upper restriction p<=2; the length-resolved inequalities remain valid for all integer M>=n.

All expressions increase in a and in b, so replacing them by certified lower endpoints is safe. In exact implementation, a lower square-root endpoint gives a lower w; positive powers of w are rounded down, while the subtracted (1-w)^p is rounded up. Multiplication by a lower a^p is safe because the resulting bracket is nonnegative. The implementation explicitly rejects odd base n, b<=1/2, b>1, a>1, and sizes outside its advertised interval.

## 4. Actual basepoints, seed identities, and closure

Define J_actual=Z8(2beta)/Z4(beta)^4 and C_actual=S(4,2beta). Exact cancellation gives

J_actual=T(4,beta)^2 C_actual=S(4,beta)^2 T(8,beta).

All three relevant purities are <=1. A lower endpoint J therefore supplies T(4,beta)>=sqrt(J), S(4,beta)>=sqrt(J), T(8,beta)>=J and the retained canonical joint lower endpoint J. This does not need any sign assumption on rho8-2rho4. The direct initial [4,8] window uses (sqrt(J),C) at beta, while the previously audited canonical window can be used separately; their maximum remains valid.

The one-term variational numerator and complete small-seed trace upper bounds give J>=exp[-2beta(rho8-2rho4)]/Q4(beta)^4 and C>=exp[-2beta(rho8-2rho4)]/Q4(2beta)^2, where Q4(t)=exp(t rho4) Z4(t). The complete counted reference tail sums to 6561 states and the shifted low endpoints use rho4+8. The rational exponential bounds are always directed outward.

The previously reviewed purification G(x)=1-(1-x)^2/(2x^2), increasing on (0,1], gives a=G(J), b=G(C^2 a), at precisely (n,beta_current)=(8,2beta_initial). There a<=T(n,beta_current), b<=S(n,2beta_current). Every extra full time-first cycle uses P=a^2 b, a_next=G(P), b_next=G(b^2 a_next), and doubles both coordinates. Domain positivity is checked before use.

At each such state the canonical exchange identity supplies S(n,beta_current)>=sqrt(P), T(2n,beta_current)>=P, and their joint lower endpoint P. This allows the established old canonical integer-window bound, separately from the new direct bound. The checker uses whichever lower bound is larger, with its actual fixed beta_current.

All M=2,3 use the inherited local-form lower gaps 1-2a_local-M b_local. Every next dyadic window beginning at n=4 is checked before advancing, with exp(beta_current*d)<I/(1-I). Once u=max(1-sqrt(P),1-P)<=1/100, the inherited all-integer asymptotic theorem closes every M>=n provided exp(beta_current*d)<1/(5u). No physical purity monotonicity is used to move a window between temperatures.

For completeness, a thermal purity I>1/2 implies its largest Gibbs weight is at least I, hence unique. Its second-to-first weight ratio is at most (1-I)/I. Therefore the certified positive d implies both unique finite-volume ground state and gap >=d.

## 5. Independent arithmetic and adversarial checks

`audit.py` imports no producer code. It uses 176-bit directed rational rounding, a 100-term positive Taylor exponential at argument <=1/2, an explicit geometric remainder, reciprocal bounds and repeated squaring. Rational power enclosures use exact integer root bisection; square roots use integer isqrt. These settings differ from the producer's 128-bit, 64-term, <=1/16 routine. Every saved accepted purity, step coordinate, short-size bound, terminal defect, and final exponential inequality is independently checked. The weaker saved g=.225 decimal .051807500 is accepted; the optimistic floating scan display is not promoted.

9,282 exact finite-spectrum comparisons include 7,655 signed-subleading-spectrum cases. The negative dominant spectrum [-10,1] demonstrates why even purity alone cannot establish the odd-size result. Twelve adversarial changes are rejected: oversized gap, wrong temperature, wrong spatial base, missing window, inflated endpoint, wrong onset, false terminal defect, odd base, b=1/2, b>1, a>1 and size outside the advertised window.

The audit uses CPU8, one process, a 1GiB address-space limit; measured peak RSS is about 12MiB. This is scalar work only. Source JSON and predecessor acceptance/manifests are frozen in `snapshot`, with explicit SHA256 provenance. The original active directory is an extracted working tree, not a Git checkout; no branch or commit changes were made. No producer, parent root, or GitHub files were modified.
