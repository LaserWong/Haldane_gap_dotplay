# Independent review: uniform-chain n52 Hermite seed

2026-10-10 18:36 EDT / 22:36 UTC. Independent scoped acceptance.

## Verdict

PASS: for the periodic uniform spin-1 Heisenberg chain with bilinear coefficient one,

    gap(H_L) >= 19/5000 = 0.0038 for every integer L>=52,

and the ground state is unique throughout this range. The canonical seed is n52 at beta=567/25, with the small-defect regime starting at n*=3328, beta*=36288/25. Every preceding integer window is independently verified, including odd lengths. No result below52 or minimum-seed theorem is claimed.

The frozen producer manifest is `9c4e7a8b78a88920582cfdea1318c71a1c4557c25213d490277325ab3b78c8c9`. All eight producer entries match. The checker also verifies the complete moment assessment/review and cooled-seed producer/review manifests. Original inputs, producer files, previous seals, root state, and GitHub were not modified.

This is a new scalar/analytic consequence of the same nine certified thermal inputs and accepted MPS104. It is not a new heat-trace computation or MPS contraction. The thermal-input certification, all-integer self-adjoint transfer construction, and physical MPS reconstruction remain inherited independently audited premises. The new Hermite identity and the complete numerical certificate are independently checked here.

## 1. Inherited physical premises and exact input directions

The model is H_L=sum_j S_j dot S_(j+1), periodic, unit bilinear coupling, with spin one at each site. The extensive shift is a=700741/500000. The nine physical inputs use beta0=21/2 and lengths6,8,10, with I/P/C seam rotations0,pi,2pi/3. These are not three temperatures. The supplied physical dimensions are3^6,3^8,3^10.

The exact thermal-history transfer is real self-adjoint Hilbert-Schmidt, with Z_L(beta)=Tr X_beta^L for every integer L>=2. Its spectrum can be signed; all physical partition functions, including odd lengths, are positive. A4 multiplicity-space lists give the physical trace I+2O+3N. O is one of two identical complex-sector lists; N is one of three identical vector copies. Thermal-transfer rank is not identified with physical Hilbert dimension or MPS bond dimension.

The prior independent moment review certifies support caps for x=lambda^2 and outward moment intervals m3,m4,m5, corresponding to transfer lengths6,8,10. This review checks its immutable manifest and uses exactly those rationals. Unit spectral multiplicities are inherited; the new polynomial bound itself also works for any positive spectral measure, but does not weaken the premises used to obtain the support caps.

The accepted MPS104 has physical bond dimension26, norm-transfer dimension676, and one normalized physical trial state. Its total Rayleigh quotient is H0_104/N0_104, not a per-bond quotient. The previous independent review rebuilt all local matrices and insertion and freshly contracted104 using sequential powers. This review checks that sealed output against the producer and verifies again

    N0_104>0,
    500000 H0_104 + 104*700741 N0_104 < 0.

No additional contraction was necessary. The shifted total quotient is approximately -0.00001093891643013882; exact integers, rather than this display, are the premise.

## 2. Hermite majorant: independent global polynomial certificate

For an even length L>=10, write k=L/2-3>=2. Let the certified squared-transfer support be0<=x<=h and select any rational node0<t<h. The producer's quadratic Q(x)=a0+b x+c x^2 interpolates x^k at t and h and its first derivative at t. The checker verifies all three interpolation equations exactly, checks the support and node against the sealed cap, and verifies the midpoint-based proposed node arithmetic. The way the node was proposed is not needed for validity: any verified interior node suffices.

The independent proof does not depend only on a quoted remainder theorem. For k>=3 define

    P_(k-3)(x) = sum_(j=0)^(k-3) p_j x^j,
    p_j = sum_(a=0)^(k-3-j) (a+1) t^a h^(k-3-j-a).

Every coefficient is strictly positive. Direct polynomial multiplication gives the exact identity

    Q(x)-x^k = (h-x)(x-t)^2 P_(k-3)(x).

This is the monomial divided-difference formula: P is the complete homogeneous polynomial of degree k-3 in the four variables t,t,h,x. It can also be established directly by polynomial division and the three interpolation conditions. The checker constructs the displayed coefficients and verifies the full coefficient vector, with no sampled-domain inference. At L26 the degree k is10; at L104 it is49. All six sector/length polynomial identities pass.

On the entire closed interval0<=x<=h, all factors have nonnegative sign. Thus Q(x)>=x^k, including x=0, t, and h. For k=2, Q(x)=x^2 exactly. This agrees with the producer's Hermite remainder sign f'''(xi)(x-t)^2(x-h)/6<=0, and supplies an independent algebraic certificate.

Multiplication by x^3, never division, yields

    x^(L/2) <= a0 x^3+b x^4+c x^5.

At x=0 both sides vanish even when Q(0)>0. Summing over a finite or countable spectrum is legitimate: m3,m4,m5 are finite, so the polynomial terms are absolutely summable. The resulting sector upper bound is a0 m3+b m4+c m5. The coefficient b is negative in the actual degree10/49 polynomials, so its lower moment endpoint must be used. The checker enumerates all eight moment-box corners and confirms that the signed endpoint choice equals the exact maximum. Upper endpoints for all three terms would be invalid.

Each Hermite upper bound is independently checked against its 10^-24 upward rounding. The previously accepted convex-packing bound is separately reevaluated with finer directed roots. Taking the smaller of two certified upper bounds is safe. No quadrature existence theorem, integral atom realization, or sufficiency of a moment screen is assumed.

The physical trace bounds improve as follows; these are floating displays of verified rational upper bounds:

| Length | Prior packing | Hermite/packing minimum |
|---|---:|---:|
| 26 | 1.2031383868561591 | 1.1951234970824767 |
| 104 | 1.2838789094348110 | 1.2838789091259710 |

The meaningful gain is the base-length envelope. The104 denominator change is much smaller. This is a new use of the same third/fourth/fifth squared-spectrum moments, not new physical data.

## 3. Cooled sector seed with actual anchor magnitude

At ell26 let A,B,C be the selected sector upper bounds. Then z=A+2B+3C bounds the identity trace and p=A+2B bounds every nonidentity tetrahedral seam. Separate Gibbs cooling of each physical seam gives D>=z^r and E>=p^r at r=54/25. Character projection implies

    tau=(D+11E)/12,
    tau0=(D+3E)/4,
    I_ell<=tau, I_ell+2O_ell<=tau0, Z_ell<=D.

These are the same sector conventions and temperature as the earlier reviewed construction. All cooling powers are enclosed upward.

Let R be the negative shifted MPS104 total Rayleigh quotient. Since E0<=R,

    ground weight at beta0 >= exp(-beta0 R),
    Z104(r beta0) >= exp(-r beta0 R).

The independently verified rational lower endpoints are v>1 and W>1, displayed as approximately1.0001148652190206 and1.000248125402652. A separately implemented positive Taylor expansion with geometric remainder and directed squaring proves each lower direction. No presumed ground-state uniqueness is used.

For transfer weights w_i=|lambda_i|^26, let t be the largest weight. The anchor exponent is4, so W<=Z104<=D t^3. The initial t0=4/5 satisfies D t0^3<W and2t0>D. Thus t>t0, the leading atom is unique, and it belongs to the trivial sector. The residual masses x,y,zeta obey the same polygon constraints as the accepted cooled-sector proof:

    x,y,zeta>=0,
    x<=tau-t, x+y<=tau0-t, x+y+zeta<=D-t.

For any j>=1 their power tail is bounded by the maximum of x^j+2(y/2)^j+3(zeta/3)^j over the four polygon vertices. Denote it R_j(t). Convexity and the preserved2/3-copy multiplicities prove this bound; each vertex expression decreases with t. The independent checker reconstructs polygon vertices by active-constraint intersections.

Every proposed increased lower t1 is certified by the exact strict contradiction

    t1^4+R_4(t0)<W.

Thus if t<=t1, the upper bound on Z104 would contradict its lower anchor W. The checker verifies all recorded iterations using W, not a silently substituted unit anchor. It then verifies the spatial lower bound

    S(52,beta) >= [1+R_2(t0)/t0^2]^-2.

For the thermal seed take Q>=Z104(beta0) and select one ground weight w0>=v. Other weights may include degenerate ground weights; their total relative mass is at most(Q-w0)/w0<=Q/v-1. Its rth-power sum after cooling is at most(Q/v-1)^r. Hence

    T(104,beta) >= [1+(Q/v-1)^r]^-2.

The code verifies Q>v, and using a lower v increases the residual ratio and therefore conservatively decreases the purity bound. An upper anchor would have the wrong direction. The resulting accepted lower seeds are approximately S>=0.867427750539740 and T>=0.880322631774115. The actual anchor magnitude is a small additional improvement; the main advance is the base26 Hermite envelope.

## 4. Correct staggered recurrence and all-integer bridges

The canonical state retains its physical coordinates:

    S=S(n,beta), T=T(2n,beta).

The exact exchange identities give S(n,2beta)>=S^2 T and T(4n,beta)>=S(2n,2beta) T^2. Normalized squaring of a probability distribution with purity z has purity at least G(z)=1-(1-z)^2/(2z^2). Consequently the sequential update is

    S_new=G(S^2 T), T_new=G(T^2 S_new),
    (n_new,beta_new)=(2n,2beta).

Its new thermal coordinate is4n=2n_new. The new S, not the old S, belongs in the second update. The independent checker verifies every physical coordinate, exact downward rounding, positive domain, and next state.

At each canonical state p=S^2 T>1/2. The normalized nth eigenvalue powers of X_(2beta) have purity at least p and leading weight at least w=(1+sqrt(2p-1))/2. Since n is even, these are nonnegative weights even if the transfer spectrum is signed. The leading modulus is unique, and its eigenvalue is positive because a unique negative leading eigenvalue would make all sufficiently large odd traces negative. The all-integer physical trace identity and positive odd partition functions are essential inherited hypotheses here.

With rho=(1-w)/w and d=T/(1+rho^2), the signed-tail estimate at2beta and absolute-spectrum Hölder estimate atbeta yield

    T(L,beta) >= C=(1-rho) min(S sqrt(d),d)

for every integer n<=L<=2n. This is the previously accepted lemma, whose full countable-spectrum proof appears in uniform_cooled_seed_review/REVIEW.md. A lower root for w gives upper rho and lower d,C, so all numerical directions are conservative. The checker independently redoes every root and comparison.

For C>1/2, the largest Gibbs probability is at least C, so the ground state is unique. The excited/ground ratio is at most(1-C)/C. Each rational exponential test

    exp(beta*19/5000)(1-C)<C

therefore certifies the gap throughout the corresponding integer window. The contiguous windows are52–104,104–208,208–416,416–832,832–1664,1664–3328. The initial C is approximately0.5698806054510107. An extra3328–6656 window is verified inside the asymptotic region.

At n*=3328,beta*=36288/25, the common defect is exactly

    u=13538523147385201077/25000000000000000000000,

approximately0.0005415409258954081. The previously reviewed small-defect proof gives u_next<=5u^2 for0<u<=1/100 and signed all-integer window purity>=1-4u. The independently rechecked test exp(beta*19/5000)5u<1 has positive margin approximately0.32691119438471. Exact dyadic continuation then covers every integer L>=3328 at the same uniform gap. No finite-precision iteration beyond the stopping state, extrapolated limit, or physical gap fit is used.

Together the early windows and asymptotic theorem prove the claimed scope beginning at52, with no omitted odd lengths or earlier dyadic windows.

## 5. Direct time-first comparison has the correct basepoint

The independently reviewed direct lemma takes a<=T(m,beta) and b<=S(m,2beta), b>1/2, and gives T(L,beta)>=a^2 sqrt(2b-1) for every integer m<=L<=2m. Its sign justification is again the positive unique leading eigenvalue of X_(2beta).

At initial base52 the canonical inputs cannot simply be renamed a,b. Their exchange identity only supplies a>=sqrt(K), b>=K with K=S^2 T. These inferred endpoints yield the reported lower expression K sqrt(2K-1), approximately0.3774786279792793. Its being below1/2 is a failure of that particular lower bound, not an upper bound on physical purity or an impossibility theorem.

After the spatial G update, the compatible pair is genuinely available at base104 and the original physical beta567/25:

    a=T(104,beta)>=T,
    b=S(104,2beta)>=G(S^2 T).

The direct window lower bound is approximately0.6667440063707969 on104–208, and its gap inequality passes. The checker verifies base104, interval104–208, and beta567/25 explicitly; beta is not doubled prematurely. This optional bridge is valid but unnecessary for the already complete canonical certificate.

## 6. Reproduction and scientific limits

Run `python independent_check.py > replay.log` and `python adversarial.py > adversarial.log` in a disposable copy to preserve this sealed snapshot. The independent replay uses exact integer-root comparisons at10^-36 resolution, a separate70-term exponential enclosure, and the exact nonnegative-factor polynomial identity. It imports no producer code and runs no contractions or eigensolver. Measured replay cost is about2.7CPU seconds,12.5MiB RSS, CPU5, under700MiB/600CPU-second limits.

The independent tests include495 closed-support polynomial evaluations across degrees2–12, exact k2 behavior, zero/repeated/end nodes, signed endpoint corners, and counterexamples to extending the support or using an upper ground anchor. They also check the direct halfstep basepoint and complete window coverage. These tests supplement the exact global proof; the proof does not rest on a grid.

Exploratory floating searches below52 remain proposal generators. Their failures cannot establish minimum size, an all-temperature obstruction, or an exclusion of other moment constructions, richer numerator spaces, or bootstrap orders. Accepted n54/56/60 certificates remain unchanged and continue to give stronger bounds on their respective ranges. No additional physical input campaign was launched.
