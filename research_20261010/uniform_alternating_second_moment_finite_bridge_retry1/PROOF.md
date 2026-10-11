# Certified finite-prefix gaps remove the coarse Weyl bottleneck

2026-10-11 04:27 UTC. Exact producer interval proof, pending independent composition review. The contracted physical32/64 observables and Gibbs second-moment bounds are independently accepted in uniform_alternating_b2_fixture_review, manifest8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee. This package performs only scalar arithmetic.

## 1. New exact intervals and unchanged model

For spin-one exchange h_j=S_j dot S_(j+1), use the periodic Hamiltonian

    H_M(g)=sum_j[h_(2j−1)+g h_(2j)], L=2M, M>=2,
    c=(1+g)/2, eta=(1−g)/(1+g), H_M(g)=c(H0+eta B),
    H0=sum_j h_j, B=sum_odd h_j−sum_even h_j.

The designated coupling is one. The four closed intervals and physical-unit gaps are listed exactly in README.md and certificate.json. They cover every integer M>=2 and claim a unique finite-volume ground state. They do not cover alternating odd-physical rings or assert optimality.

The earlier coarse-bridge package uniform_alternating_second_moment_robustness is frozen under manifest bcc9601beaaf7c76557df759a0166a5f3eede1aa5287936b7bd7effaf6d222fb. Its four radii remain valid lower anchors. The present extension preserves that seal and all earlier accepted structural and numerical results.

## 2. Accepted finite Gibbs purities and a stronger gap implication

For a finite Hamiltonian at inverse temperature beta, let C>1/2 lower-bound Gibbs purity and let p0 be its largest Gibbs weight. Purity>1/2 implies p0>1/2 and uniqueness of the maximal weight. Since

    C<=sum_i p_i²<=p0²+(1−p0)²,

one obtains

    p0>=w(C)=(1+sqrt(2C−1))/2.

For each excited state, p_i/p0<= (1−p0)/p0 <= (1−w)/w. Hence

    gap >= beta^(-1) log[w/(1−w)]
         = beta^(-1) log[(1+sqrt(2C−1))/(1−sqrt(2C−1))].   (1)

The implementation does not certify a floating logarithm. It rounds the square root downward, then selects a rational delta by a directed strict test

    w−upper_exp(beta delta)(1−w)>0.                       (2)

Every finite input here has beta0=49/4. The exact rational purities are read directly from the already accepted uniform_gap_0248_all_sizes_review/results.json, whose manifest is5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf. The relevant arrays are cached_prefix_4_to25 and new_direct26_to33. This source review checks each cached endpoint against its original accepted certificate and records the physical temperature. No neighboring-size purity, temperature rescaling, or physical gap monotonicity is assumed.

Only the14 even physical lengths4..30 are needed. The exact chosen finite gaps are:

| Physical L | Certified uniform delta_L |
|---|---|
|4|907/1000|
|6|511/1000|
|8|427/1000|
|10|51/125|
|12|97/250|
|14|147/500|
|16|49/200|
|18|221/1000|
|20|21/100|
|22|207/1000|
|24|113/1000|
|26|21/100|
|28|107/500|
|30|217/1000|

These are conservative rational milligap lower endpoints, not rounded-up logarithm displays. Equation(2) is independently recorded with a strict positive rational margin for each length. Physical24 uses its accepted parity-resolved purity and MPS48 construction; it is not replaced by an invented own24 trial. The other listed finite purities have their accepted own-length trial provenance. Analytic physical2/3 are unnecessary because the alternating model here starts at physical4 (M2).

## 3. Length-resolved finite Weyl bridge and physical normalization

Centering the local exchange by1/2 gives norm at most3/2. Because L is even, the centering terms cancel in B, and ||B_L||<=3L/2. Weyl gives at each fixed finite length

    gap(H0+eta B)>=delta_L−3L|eta|.

For |eta|<=r and positive right side, physical c=1/(1+eta) is at least1/(1+r), so

    gap(H_M(g))>=(delta_L−3Lr)/(1+r).                    (3)

The checker verifies(3)>=D separately for all14 lengths in each row. As a redundant direct test against the actual accepted Gibbs weight, it also verifies

    w_L−exp{beta0[(1+r)D+3Lr]}(1−w_L)>0.                (4)

All56 such checks pass strictly; none relies on an interpolated or all-size monotone finite gap. The smallest(3) occurs at physical24. Its values in the four rows are approximately.1036914134,.0999066570,.0974341640,.0959276843, respectively, all well above their targets.

This is a finite-prefix norm comparison only. The estimate proportional to L is never applied at unbounded length. Unlike the prior global .0248 bridge, it leaves substantial radius slack at all four accepted rows.

## 4. Finite seed comparison and all-size continuation

The remaining proof is unchanged from the separately frozen second-moment robustness package, but is replayed at each new radius. The actual untwisted uniform Gibbs state at beta0 is invariant under one-site translation, which reverses B. Gibbs variational convexity gives Z_eta>=Z0; Golden–Thompson gives Z_eta/Z0<=Tr(rho0 exp(−beta0 eta B)). The spectral distribution is symmetric. The pointwise bound

    cosh(tx)−1<=(x²/b²)[cosh(tb)−1], |x|<=b,

therefore yields

    Z_eta,L/Z0,L<=A_L=1+kappa_L[cosh(beta0*(3L/2)*r)−1],
    kappa32<=17/125, kappa64<=157/1000.                   (5)

Both kappa bounds have independent observable/fidelity acceptance. Equation(5) is not asserted for a twisted trace. The original18 uniform I/P thermal inputs at lengths4..12 remain unchanged sources of the accepted uniform physical32 seed. Its own physical64 MPS anchor remains unchanged.

The MPS has zero staggered mean exactly by translation. With actual tau0=beta0/c and shifted per-site energy ca, a=700741/500000, its Boltzmann numerator is unchanged. Thus

    s0>=S0/A32², t0>=T0/A64²,
    cell base n0=16, normalized beta0=49/4.              (6)

The accepted positive cell transfer is A_g A_g* between the distinct nonnegative-history measure spaces, positive trace class for g>=0, with the physical trace identity at every integer cell count M>=2. Positivity permits all integer windows. For n<=M<=2n, positive l^p numerator monotonicity and Holder denominator interpolation give

    T(M,tau)>=s^(2−M/n)t^(M/(2n))>=min(s sqrt(t),t)=C.

Every window passes C−exp[beta(1+r)D](1−C)>0. The sequential recurrence is

    G(x)=1−(1−x)²/(2x²),
    s_new=G(s²t), t_new=G(t² s_new),
    (n,beta)->(2n,2beta), actual tau=beta/c.

All legal positive endpoints are checked. When u=max(1−s,1−t)<=.01, the next defect is at most5u². The exact terminal condition5u exp[beta(1+r)D]<1 closes every remaining integer-cell window. This is the same independently accepted all-size continuation; changing the finite input radius does not alter its hypotheses.

The final four rows use10,9,10,10 finite windows, closing at cell8192,4096,8192,8192. Terminal defects are about2.74546e−56,6.59534e−22,7.31510e−29,2.41445e−15, with strictly positive terminal margins about.580707,.106429,.357281,.493606. The exact rational values, not these displays, certify the tails. Together with the14 finite bridges, every integer M>=2 is covered without a size hole.

## 5. Exact search, preserved failed attempt and finite precision

The preceding unsealed finite-bridge attempt used a floating proposal search with an optimistic branch when a tiny defect rounded to zero. All10 planned nearby exact candidates failed its sufficient check; the script stopped at its explicit no-candidate assertion without an accepted interval. It used3.569925 child+.052848613 parent CPU seconds. That folder is preserved and separately sealed as0d06089ab17528acf94b8912662f93fdced8ec72bbe971311aa8674dd040ec5d. A failure of these sufficient tests is not a no-go theorem for the physical model.

Root authorized exactly one corrected attempt, with23 child CPU seconds plus one parent reserve from the remaining scalar budget. This package entirely removes floating proposal logic. It first exactly rechecks all four previously certified radii, then tries the rational upper bracket1/2500 and performs bounded rational bisection. Every candidate has an exclusive numbered file, including all rejected exact recurrences and their failure stage. The process budget stops search cycles before finalization, rather than accepting an unverified numerical proposal.

Five complete bisection cycles were completed. Final radii are rounded downward to a1e−7 rational grid and independently rechecked; each target has its own final checkpoint. The run saves32 planned candidates,15 of them rejected, and four accepted final rows. Search upper brackets are merely next candidate bounds, not proofs that larger radii are impossible.

The directed arithmetic uses400 decimal places, exact integer-root brackets,220-term positive Taylor exponentials after argument reduction below1/16, a geometric next-term remainder, and outward repeated squaring. All exponentials/cosh losses round upward where required; s,t,C round downward. This greatly exceeds the precision needed for the final defects through1e−56. No successful result relies on a defect rounding to zero.

## 6. Guards, cumulative budget and immutable sources

The corrected child is pinned to CPU4 with hard23CPU-second and256MiB limits. An independent guard actively polls process CPU, kills above22seconds, enforces a90-second wall watchdog, and records wait4. Postexec checks verify all hard limits, sole affinity, default/unblocked SIGXCPU and parent-death SIGKILL. The parent has a one-second CPU cap; its measured cost is recorded separately.

Corrected attempt:18.508296 child CPU seconds, .315003745 parent CPU seconds,15628KiB wait4 peak,19.031991810seconds wall,904 active polls. No watchdog fired and no further retry occurred.

The complete separately authorized30-second scalar gate comprises:

    first successful coarse bridge: .452154+.006521998,
    preserved failed extension:    3.569925+.052848613,
    corrected successful retry:   18.508296+.315003745,
    measured cumulative total:    22.904749356 CPU seconds.

Charging a full one-second reserve for each of the three parent launchers instead of their measured costs gives25.530375CPU seconds, still below30. This budget is separate from previously authorized physical observable contraction and compilation budgets; none is reset or hidden.

The original observable, first-interval, positive-cell, uniform-gap and seed manifests are verified unchanged. The failed attempt is also pinned. No physical contraction, root-document change, remote action or sealed-file modification occurs. The final mathematical result remains producer-only until independently reviewed. Replaying the guard requires a disposable output directory; its exclusive files prevent an automatic retry.
