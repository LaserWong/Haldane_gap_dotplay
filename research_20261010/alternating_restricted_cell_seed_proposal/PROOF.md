# Exact restricted-input construction and scoped obstruction

2026-10-11 00:05 EDT / 04:05 UTC. Producer mathematical checks; independent review pending. Resource compliance NOT ACCEPTED; see RESOURCE_REPORT.md.

## 1. Model, temperature and restricted data

H_M(g)=sum_j [S_(2j−1)·S_(2j)+g S_(2j)·S_(2j+1)], periodic M≥2, spin one. At the feasibility point g=1, beta=49/4 and the shift per physical site is a=700741/500000. The corresponding scalar cell shift is2a. The positive history transfer K=A A* represents Z_M=Tr K^M. We use only physical L=2M in {4,6,8,10,12}; their cell orders are M=2,...,6.

The integer-spin pi rotations form a Klein four-group. Equivariance permits its orthogonal character projectors to commute with positive K. Each projected restriction is positive. Rotational equivalence of the three nontrivial characters gives the sector power sums

    J_k=(Z_I,2k+3 Z_P,2k)/4,
    N_k=(Z_I,2k−Z_P,2k)/4,
    Z_2k=J_k+3N_k.

Each eigenvalue occurrence in a multiplicity sector has unit mass. Physical P is the spatial pi seam from the accepted input, not an arbitrary temporal insertion. The g=1 cell eigenvalues are squares of the single-site eigenvalues, but NO odd physical moments of that single-site transfer are imported.

verify.py parses the published integer table without executing its code, selects precisely the ten even-length I/P rows, and reconstructs their exact rational enclosures. It rounds outward at1e−18 before the character combination. The independent complete heat review states exact matching of each selected published integer; diagnose.py checks these ten matches and pins the source members. No physical kernel, matrix, contraction or thermal calculation is executed.

## 2. Unit-atom Hankel support bounds

For positive sector eigenvalues x_i and moments m2,...,m6, write

    H_ij=m_(2+i+j), 0≤i,j≤2, v(t)=(1,t,t²).

Removing an eigenvalue occurrence t gives H−t²v(t)v(t)^T≥0. Thus every quadratic q obeys

    t² q(t)² ≤ sum_i x_i² q(x_i)².

For rational q, the right side is bounded by the moment upper endpoint for each nonnegative coefficient of q² and the lower endpoint for each negative coefficient. The search only proposes q; all checks are rational. At each rational cap U the checker verifies U²q(U)² exceeds this upper bound, and every coefficient of q(U+y) is strictly positive. Consequently t²q(t)² increases for t≥U and the whole exterior ray is excluded.

The exact caps are

    J: 0≤x<501577563/500000000 =1.003155126,
    N: 0≤x<189745179/250000000 =.758980716.

The full q coefficients, moment bounds, ray margins and shifted coefficients are in certificate.json. Infinite transfer rank causes no problem: finite m2 and m6 make these square sums finite, and finite-subfamily limits give the inequality.

## 3. Exact long-moment upper envelopes

For each sector and k in {15,16,17,30,32,34}, choose two positive rational nodes a<b<U. Construct the exact quartic p interpolating f(x)=x^(k−2) and f'(x) at a,b and f(U) at U. The checker solves the five interpolation equations over rational numbers and checks them exactly.

The Hermite remainder is

    f(x)−p(x)=f^(5)(xi)/5! (x−a)²(x−b)²(x−U)≤0, 0≤x≤U.

All k here exceed6, hence f^(5)≥0. This is a whole-interval analytic envelope, not a sampled-grid certificate. Multiplying by x² and summing gives m_k≤sum_(j=0)^4 p_j m_(2+j), evaluated outward with coefficient signs. The rational coefficients and bounds are recorded. At k34 the full trace upper bound is

    Q34=J34_upper+3N34_upper≈1.1133056350335735.

## 4. Own-length trial numerator and unit-multiplicity forcing

For cell seed n, its doubled cell volume is2n and the physical anchor length is4n:60,64 or68. The independent anchor output is checked bytewise against its source manifest, and its N0_L,H0_L integers are compared with the consumed producer integers. N0_L>0 and

    R_L=H0_L/N0_L+aL<0.

H0_L is already the TOTAL periodic energy numerator; no extra L factor is inserted. Jensen gives Z_(2n cells)(beta)≥exp(−beta R_L), and at doubled temperature the lower numerator is exp(−2 beta R_L).

For a proposed ell, supposing every J eigenvalue≤ell gives either the quartic Hermite bound with cap ell, or the stronger convex-packing bound from m6. If y_i=x_i^6≤h=ell^6 and sum y_i≤m6_upper, then

    sum y_i^r≤floor(m/h)h^r+(m−floor(m/h)h)^r, r≥1.

Use r=2n/6, add3N_(2n)_upper, and compare against exp(−beta R_L). A strict deficit forces at least one unit J atom above ell. The final rational forced ell values are .999979272, .999989753 and .999995519 for n15,16,17. Since K is positive, no negative-ray exclusion is needed.

After removing that atom, the J sixth moment is at most m6_upper−ell^6. Hence the remaining J n-th mass is at most(m6_upper−ell^6)^(n/6). Adding3N_n_upper gives the tail. The final endpoints are

    S≥[1+tail/ell^n]^(−2),
    T≥exp(−2 beta R_(4n))/Q_(2n)^2.

Rational root brackets and positive Taylor exponential bounds with geometric remainders are rounded outward at90 decimal places. Original Hermite-only forcing is retained in baseline_certificate.json; final certificate.json uses the minimum of Hermite and packing. This is genuine unit-mass forcing, not an assumption that a relaxed weighted moment measure is an integer spectrum.

## 5. Positive windows and failure of this recurrence recipe

For each positive endpoint pair, the accepted cell positivity lemma supplies

    T(M,beta)≥min(S sqrt(T),T), n≤M≤2n.

The exact scalar update is sequential:

    S_new=G(S²T), T_new=G(T² S_new), G(z)=1−(1−z)²/(2z²).

The thermal update uses the NEW S. All stored calculations are downward rounded. Although the first three windows have positive purity bounds, the next recurrence fails its positive-domain gate:

- cell15: S_new≈−.0293348447958;
- cell16: S_new≈.524253038337, T_new≈−4.40585226687;
- cell17: S_new≈.485357004107, T_new≈−7.14804017747.

These exact rational values appear in diagnostics.json. No negative quantity is promoted to a purity endpoint. The failure is independent of the trial gap target, since the recurrence does not depend on that target. A finite positive-window result cannot be promoted to an all-size bootstrap.

## 6. Counterfactual sufficient improvement

diagnose.py separately keeps the final cell17 S endpoint and substitutes the UNACHIEVED thermal endpoint167/200=.835. Exact positive windows at gap1/200=.005 and the usual small-defect closure then succeed at round4. This is a conditional design target only. With the same physical68 anchor, a sufficient denominator target is

    Q34≤sqrt(exp(−2 beta R68)/(.835)),

with the downward enclosed right side1.0944628815077482. The present Q34 is about1.7% larger. This comparison does not prove that lowering Q alone is necessary, that .835 is the optimal threshold, or that a new trial numerator cannot help.

The package proves no new gap, no g=.9 statement, no minimal seed, and no universal insufficiency of m2,...,m6. Its precise output is a valid tested construction that fails, a conditional repair target, and a bounded design proposal.
