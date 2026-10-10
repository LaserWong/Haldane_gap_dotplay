# Independent review: cooled uniform-chain seeds

2026-10-10 18:27 EDT / 22:27 UTC. Independent acceptance completed.

## Accepted results

For the periodic uniform spin-1 Heisenberg chain H_L=sum_j S_j dot S_(j+1), with bilinear coefficient one, the following bounds and unique ground states are certified:

| Certified gap lower bound | Every integer length | Seed inverse temperature | Small-defect entry |
|---|---:|---:|---:|
| 51/5000 = 0.0102 | L >= 60 | 105/4 | 960 |
| 17/2500 = 0.0068 | L >= 56 | 609/25 | 1792 |
| 1/400 = 0.0025 | L >= 54 | 2373/100 | 3456 |

PASS. This review independently rebuilds the physical D26 matrices and insertion, contracts the new lengths with sequential powers rather than the producer's binary powers, verifies all exact scalar inequalities, and supplies the analytic arguments below. No substantive defect was found. These results inherit the archived, independently audited nine physical thermal enclosures and the exact self-adjoint thermal-history representation; they do not constitute fresh recomputation of those heat traces.

The producer manifest SHA-256 is `13c41cfac38c43a6199bfceebc98be4379773c733d1c59dfdb93af03881a037c`. All 17 entries match, as do its input hashes, the six entries in the moment assessment, and the seven entries in its independent moment review. The original producer and prior seals remain unchanged. No root or GitHub changes were made. The snapshot has no Git metadata.

The three bounds should remain separate: n60 improves the prior route without reducing its physical seed; n56 is a smaller seed using the original quadratic-tail structure; n54 additionally uses generalized sector powers. The combined interpretation is the corresponding stronger bound on each nested range. No claim is made below L54, no smallest-possible seed is proved, and a failed floating proposal at n52 is not a no-go theorem.

## 1. Physical dependencies and fresh MPS reconstruction

All thermal inputs refer to beta0=21/2, shift a=700741/500000, and lengths 6,8,10. I/P/C are seam rotations by 0,pi,2pi/3, not three temperatures. The physical dimensions are 3^6,3^8,3^10. The inherited real self-adjoint Hilbert-Schmidt history transfer satisfies Z_L(beta)=Tr X_beta^L for every integer L>=2, with the same operator at all lengths and positive physical partition functions. Its eigenvalues may be negative.

The audited A4 decomposition gives multiplicity-space lists I,O,N with physical trace I+2O+3N. Complex sectors occur in an identical conjugate pair; the vector sector has three identical copies. Ordinary spectral eigenvalue multiplicities in each list are positive integers. None of the following arguments supposes finite thermal-transfer rank.

The independently reviewed moment package yields rigorous upper even moments at beta0, using unit-atom residual Hankel constraints and directed convex packing. Its refinement and global support exclusion are not rederived here; their sealed review is checked and remains an explicit dependency. The present checker independently reevaluates all needed moment powers at finer precision before accepting the producer's outward envelopes.

`rebuild_d26.py` reuses the earlier independent entrywise reconstruction, not the producer contraction engine. It reconstructs three 26x26 local matrices from the archived integer parameter table, forms the physical spin-1 two-site Heisenberg insertion, and rebuilds all 11 difference blocks. Those blocks are byte-identical to audit/mps/mps_blocks.txt. Direct product-basis amplitudes at lengths 2 and 3 check physical norm and total energy, including the doubled periodic bond at length 2.

The MPS norm transfer has dimension 26^2=676 and block dimensions 1,8,32,80,136,162,136,80,32,8,1. This is one trial state's norm transfer, not the thermal transfer, a retained spectral count, or the exponentially large physical Hilbert space.

For each length L, the fresh sequential contraction computes

    N0_L = Tr T^L,
    H0_L = L Tr(T^(L-2) O).

The periodic state's total Rayleigh quotient is H0_L/N0_L. All integers at 104,108,112,120 match the producer; at 120 they also satisfy H0_120=120 U120 and N0_120=V120 from the earlier audited contraction. Thus a per-bond quantity was not accidentally used as a total energy. Every N0_L is positive, and

    500000 H0_L + 700741 L N0_L < 0

is checked as an integer inequality. This proves a shifted Rayleigh quotient below zero, hence an actual ground energy below zero, at each anchor. No uniqueness assumption is involved.

The 48-site benchmark matched exactly and took 9.212 CPU seconds with 10.6 MiB RSS. The separate sequential run through 120 took 30.591 CPU seconds and 18.7 MiB RSS. Both ran on CPU5, under 600 CPU-second/700 MiB limits. An initial benchmark comparison command used an incorrect relative path; the benchmark computation had already completed, and the corrected comparison immediately passed. The final reproduction script uses fail-fast ordering and requires the comparison before the longer run.

## 2. Cooling seam traces and the sector mass polygon

At an even base length ell let the certified beta0 sector upper moments be A,B,C. Then

    Z_ell(beta0) <= z=A+2B+3C,
    every nonidentity seam trace <= p=A+2B.

The two nonidentity character expressions are I+2O-N and I-O. Their positivity as physical partition functions is important; a signed parity insertion into an untwisted Gibbs trace would not justify the cooling step.

For positive Boltzmann weights and r>=1, sum w_i^r <= (sum w_i)^r. Apply this separately to each physical seam Hamiltonian. At beta=r beta0 we obtain upper bounds D>=z^r and E>=p^r. No beta=21 physical input or interpretation of spatial transfer powers as temperature doubling is introduced.

Character projection then gives

    I_ell <= tau=(D+11E)/12,
    I_ell+2O_ell <= tau0=(D+3E)/4,
    Z_ell <= D.

The checker verifies D>=tau0>=tau>0. With w_i=|lambda_i|^ell and leading weight t, the anchor length 2n has exponent p0=2n/ell. Since its shifted ground energy is negative, Z_2n(beta)>1. Therefore

    1 < sum w_i^p0 <= t^(p0-1) D.

The selected initial t0=4/5 satisfies D t0^(p0-1)<1. Consequently t>t0. Because 2t0>D, a repeated leading eigenvalue is impossible and the leading atom must belong to the trivial sector: nontrivial sectors require at least two copies. This is uniqueness of the largest transfer modulus, not an assumed uniqueness of the many-body ground state.

Remove that one trivial atom. Write x for residual trivial mass, y for the combined two complex copies, and zeta for the three vector copies. Then

    x>=0, y>=0, zeta>=0,
    x<=tau-t, x+y<=tau0-t, x+y+zeta<=D-t.

For every real exponent q>=1, positivity and the lq mass inequality on each multiplicity list give

    tail_q <= x^q + 2(y/2)^q + 3(zeta/3)^q.

This inequality also holds for countably infinite lists by finite partial sums and monotone convergence. Replacing zeta by D-t-x-y only increases the right side. The resulting function of x,y is convex on its compact polygon. Its maximum is attained at one of the vertices

    (0,0), (tau-t,0),
    (tau-t,tau0-tau), (0,tau0-t).

The independent checker finds these as intersections of active constraints, rather than copying the producer's vertex list. Each vertex objective is nonincreasing in t on 0<=t<=tau: every varying nonnegative component decreases, while other components are constant. Their maximum R_q(t) is therefore nonincreasing. This proves the generalized lemma, including q=27/14 and p0=27/7 at n54; it is not an extrapolation from integer powers.

For a known lower t0, the direct anchor estimate is

    1 < Z_2n <= t^p0 + R_p0(t0).

Thus a proposed larger t1 is valid whenever t1^p0+R_p0(t0)<1. In the original n60/n56 mode p0=4, the weaker but valid tail_4 <= (tail_2)^2 <= R_2(t0)^2 is used. The checker independently evaluates and validates every recorded strict contradiction, not merely the final inferred root. No moment-feasibility test is treated as sufficient for an actual spectrum.

## 3. Initial purities and their exact coordinates

The canonical state is staggered:

    S = S(n,beta) = Z_2n(beta)/Z_n(beta)^2,
    T = T(2n,beta) = Z_2n(2beta)/Z_2n(beta)^2.

It is essential that the thermal seed has length 2n, not n. Here n,ell are even. Put q=n/ell. With the final strict lower mass bound t0,

    Z_n <= t^q + R_q(t0),
    Z_2n >= t^(2q),
    S(n,beta) >= [1+R_q(t0)/t0^q]^(-2).

Signs cause no problem because these lengths are even. The argument is valid for fractional q; n54 uses ell28, so q=27/14, without changing the temperature or the seed geometry.

For the thermal input, let Q bound Z_2n(beta0). Select one actual ground Boltzmann weight w0>1, established by the negative shifted trial energy. All other weights, including any other ground weights if degeneracy existed, sum to at most Q-w0<Q-1. At the cooled beta their ratio to the selected ground weight is bounded by (Q-1)^r, since sum_i (w_i/w0)^r <= ((Q-w0)/w0)^r <= (Q-1)^r. Its normalized weight is therefore at least [1+(Q-1)^r]^-1, and the Gibbs purity is at least its square. Hence

    T(2n,beta) >= [1+(Q-1)^r]^-2.

This ground-plus-tail cooling proves the needed thermal purity without first assuming uniqueness and without a separately computed 2beta trace. The checker independently encloses all rational powers and proves the selected rational S,T are conservative.

## 4. Sequential recurrence with staggering preserved

For any probability distribution with purity a, its normalized square has purity at least

    G(a)=1-(1-a)^2/(2a^2).

Indeed, 2 sum_(i<j) p_i^2 p_j^2 <= (1-sum_i p_i^2)^2/2; divide the corresponding fourth-moment inequality by a^2. G is increasing on 0<a<=1.

The exact exchange identities are

    S(n,2beta) T(n,beta)^2 = S(n,beta)^2 T(2n,beta),
    T(4n,beta) S(2n,beta)^2 = S(2n,2beta) T(2n,beta)^2.

Since the omitted purity factors are at most one, the first identity and spatial normalized squaring give

    S' = S(2n,2beta) >= G(S^2 T).

The second identity then uses this newly updated S', followed by Gibbs normalized squaring, to give

    T' = T(4n,2beta) >= G(T^2 S').

Thus the next canonical state is precisely (n',beta')=(2n,2beta), with thermal length 2n'=4n. Using old S in the second update, or treating T as T(n,beta), would be wrong. The independent replay verifies every state, its n/beta doubling, exact 10^-24 downward rounding, positivity, and the sequential dependence on the new S'.

## 5. Signed-transfer interpolation covers every integer window

Fix a canonical state with lower bounds S,T and p=S^2 T>1/2. The first exchange identity gives S(n,2beta)>=p. Since n is even, the normalized n-th powers of the eigenvalues of Y=X_(2beta) form a probability list. Its largest weight is at least

    w=(1+sqrt(2p-1))/2 > 1/2.

The inverse-purity statement follows from sum p_i^2 <= w_max^2+(1-w_max)^2 and w_max>=purity>1/2. Hence Y has a unique largest-modulus eigenvalue. This eigenvalue is positive: if it were negative, its normalized signed contribution would dominate all sufficiently large odd traces, which would be negative, contradicting positive physical Z_L(2beta). The absolute remainder tends to zero by dominated convergence using a finite even trace-class moment. A finite thermal rank is unnecessary.

This positivity statement concerns X_(2beta), the operator used for the window numerator, not an unproved assumption about every eigenvalue of X_beta. With rho=(1-w)/w,

    sum_(j>0) |mu_j/mu0|^n <= rho < 1.

At 2n the tail is at most rho^2; at every integer L>=n it is at most rho^(L/n)<=rho. For a=L/(2n) in [1/2,1], this yields

    Z_L(2beta) >= [Z_2n(2beta)/(1+rho^2)]^a (1-rho).

At beta, even endpoint moments and absolute-spectrum Hölder give

    Z_L(beta) <= Z_n(beta)^(2-2a) Z_2n(beta)^(2a-1).

The left side is positive even at odd L; it is bounded above by the absolute spectral sum. Combining these inequalities gives

    T(L,beta) >= (1-rho) S^(2-2a) d^a,
    d=T/(1+rho^2).

The logarithm of the a-dependent product is affine, so its minimum over the full interval is attained at an endpoint. Therefore every integer n<=L<=2n has thermal purity at least

    C=(1-rho) min(S sqrt(d),d).

All dependence on supplied S,T lower bounds is monotone. A downward root for sqrt(2p-1) gives a lower w, an upper rho, and lower d,C. This is the direction implemented and independently checked.

If C>1/2, the largest Gibbs probability is at least C, so it is unique and represents a unique ground state. The first excited-to-ground probability ratio is at most (1-C)/C. Consequently the rational test

    exp(beta gap) (1-C) < C

certifies the claimed gap. A 70-term positive Taylor enclosure with explicit remainder and directed squaring independently verifies every window's strict margin. No floating logarithm certifies any gap.

## 6. Infinite dyadic continuation and coverage

For 0<u<=1/100 with S,T>=1-u, the spatial defect update is at most

    u^2 (3-3u+u^2)^2/[2(1-u)^6] <= 5u^2.

Using the newly improved spatial input, the thermal defect is at most

    u^2 (2+5u)^2/[2(1-2u-5u^2)^2] <= 5u^2.

Both coefficients are increasing on this interval and are checked at its rational endpoint. The spatial monotonicity follows by differentiating (3-3u+u^2)/(1-u)^3; its numerator is 6-4u+u^2>0. Thermal monotonicity follows because its positive numerator increases and positive denominator decreases.

For completeness, the finite-window formula above directly gives T(L,beta)>=1-4u in this regime. The inverse-purity lower bound gives w>=1-2u because

    (1-u)^3 - [(1-2u)^2+(2u)^2] = u-5u^2-u^3 > 0.

Thus rho<=2u/(1-2u). The inequality 4u(1-u)<=(1-2u)^2 implies rho^2<=u/(1-u), so d>=(1-u)^2 and sqrt(d)>=1-u. Both terms in min(S sqrt(d),d) are at least (1-u)^2. It follows that

    C >= [(1-4u)/(1-2u)] (1-u)^2 >= 1-4u.

Hence the excited/ground ratio is at most 4u/(1-4u)<=5u. Exact dyadic iteration gives u_j<=(5u0)^(2^j)/5 and beta_j=2^j beta0. The certificate's strict test exp(beta0 gap)5u0<1 therefore proves the same gap at every later integer length. There is no repeated numerical-rounding floor and no limit interchange.

The initial finite windows are contiguous, with shared endpoints, and overlap the asymptotic region:

- n60: 60–120, 120–240, 240–480, 480–960; asymptotic L>=960.
- n56: 56–112, 112–224, 224–448, 448–896, 896–1792; asymptotic L>=1792.
- n54: 54–108, 108–216, 216–432, 432–864, 864–1728, 1728–3456; asymptotic L>=3456.

One additional finite window inside each asymptotic region is checked as an overlap test. Thus every integer length in each stated range, including odd lengths, is covered.

## 7. Exactness, adversarial checks, and limits

`check_scalar.py` independently verifies all seals, fresh contractions, shifted-energy signs, cooling envelopes, dominant-mass iterations, seed bounds, sequential recurrence, finite windows, and asymptotic margins. It uses integer root comparisons on a 10^-36 grid and a separate exponential enclosure. It neither imports nor executes producer scalar code. All exact rational powers, including denominators 14,7,25,50, are enclosed before comparison.

`adversarial.py` checks fractional polygon powers at rational interior points, perfect-power spectral examples, infinite geometric tails, a counterexample to dropping the complex multiplicity factor, degenerate-ground cooling, negative-leading odd traces, exact staggered exchange identities, and normalized-square purity bounds. These regression tests complement, rather than replace, the analytic proofs.

The physical heat computations and the all-length transfer construction remain inherited, named premises. No new many-body eigensolver, thermal input campaign, full-spectrum calculation, or conjectured infinite-volume energy was used. The MPS104 anchor is valid, but its absence from an accepted n52 certificate is not a proof that n52 cannot succeed. Other cooling ratios, richer numerators, alternative initializations, or tighter moments remain outside this bounded scan.

Reproduce in a disposable copy with `bash REPRODUCE.sh`; it writes only review artifacts. CPU5 is preferred, one CPU and 700 MiB limits apply, and measured scientific CPU usage is well below the initial 600-second budget. INPUT_SHA256.json records consumed provenance; CLAIM_VERDICTS.json, MANIFEST_SHA256.json, and SEAL.json freeze this review.
