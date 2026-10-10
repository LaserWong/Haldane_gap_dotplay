# Independent signed-moment optimization review

Updated 2026-10-10 19:36 EDT (America/New_York) / 23:36 UTC.

## Verdict and precise condition

CONDITIONALLY ACCEPTED: for the uniform periodic spin-one Heisenberg Hamiltonian with unit bilinear exchange, the gap is at least 107/5000 = .0214 and the ground state is unique for every integer physical length L >= 36. No claim below 36, minimum initialization claim, finite transfer-rank assumption, or new thermal-matrix validation is made.

The condition is validity of all eighteen published beta=49/4 physical integer W totals together with their stated Frobenius/rounding error bounds and the inherited exact self-adjoint history-transfer identification. This distinction is material: the optimization reconstructs tighter rational enclosures from those W certificates; the coarser center +/-30e-6 table alone is not the precise input used. These eighteen physical certificates have NOT all been rerun locally. The beta=21/2 nine-input certification and small thermal-kernel fixtures do not discharge these separate premises.

The producer package is frozen at manifest dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85. The accepted baseline review is pinned at 3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b. This review verifies both complete manifests, all producer input hashes, and the continuation dependencies. No producer module or search code is imported or executed. A local frozen producer snapshot is supplied.

## 1. Published inputs and signed sectors

We independently parse W from unchanged official thermal72.tex and compare all eighteen integers to the literal archived Python B table, parsed with ast.literal_eval only. For n=4,...,12, compute x=(49/4)n(3/2-a), a=700741/500000, the degree-100 positive Taylor sum s, last term t, integer r=floor(sqrt(W)), d=floor(sqrt(3^n))+1, and error E=d[281(d+1)+1]. Since 0<x<15, the omitted exponential tail is at most 15t/86<t. Thus the published physical certificate yields

L=s max(0,r-E)^2/2^110, U=(s+t)(r+1+E)^2/2^110.

Each endpoint is rounded outwards to a 10^-18 grid. All exact endpoints independently agree with the producer. This is an exact reconstruction of the conversion from published totals; it does not regenerate physical columns.

At the common temperature, J_n=(Z_n+3P_n)/4 and N_n=(Z_n-P_n)/4. The full trace is J_n+3N_n. In particular N_lower=(Z_lower-P_upper)/4 and N_upper=(Z_upper-P_lower)/4. These are powers lambda^n, for orders 4 through 12. All four odd N intervals are strictly negative. Replacing odd moments by absolute values or replacing lambda by lambda squared is invalid.

For a coefficient c, an upper linear bound uses the upper moment endpoint when c>=0 and the lower endpoint when c<0. Enlarging the joint physical constraints to these interval boxes is conservative, despite shared Z,P correlations. No attainability of all adverse endpoints, independent sectors, or global physical sharpness is claimed.

## 2. Unit-atom exclusion and both entire exterior rays

For any real degree-four q, define F(x)=x^4 q(x)^2>=0. Absolute convergence follows from the finite fourth and twelfth moments: intermediate absolute powers are bounded by |lambda|^4+|lambda|^12. Thus the sum of F over each sector is a valid linear combination of moments 4,...,12. Every eigenvalue occurrence has unit mass, including multiplicities, so a single occurrence t contributes F(t) and cannot exceed the full nonnegative sum.

Equivalently, H_ij=m_(4+i+j), v(t)=(1,t,...,t^4), obey H-t^4 v(t)v(t)^T>=0 after removing one occurrence. This is necessary for a spectral list, and is not valid for arbitrary fractional masses. When H>0, maximizing the squared evaluation functional gives the necessary Christoffel condition t^4 v(t)^T H^-1 v(t)<=1. No inverse is needed for the actual accepted exclusion: the supplied rational q is tested directly.

For every one of J+, J-, N+, N-, the reviewer independently squares q, computes its sign-directed upper sum B, and verifies r^4 q(sign*r)^2>B. Crucially, it also expands q(sign*(r+y)) exactly in y and finds all five coefficients strictly positive. Hence q and (r+y)^4 are positive and nondecreasing for every y>=0. The filter is strictly beyond B throughout that ENTIRE exterior ray. No root scan, isolated endpoint check, or ignored disconnected component is used.

The accepted open supports are

- J: -0.6501774659 < lambda < 1.0013390453
- N: -0.8710299903 < lambda < 0.7502278231

All exact coefficients, shifts and margins are pinned in the producer certificate and independently checked. For each stated midpoint nonexclusion point, a separately implemented rational LDL factorization gives positive pivots for H_mid-t^4 vv^T. Therefore no degree-four square filter can exclude that point for these midpoint moments. The midpoint comes from the simultaneous Z,P box midpoint. This only brackets the robust square-filter method on that enlarged data set; it does not establish a physical or integer-atom realization, global optimality, or an obstruction to other methods.

## 3. Long-moment majorants on closed signed supports

For each of ten proposals (J and N at k=24,36,48,72,120), write the supplied degree-eight rational polynomial p and form the full polynomial p(x)-x^(k-4). On the entire CLOSED signed support interval [a,b], convert exactly to Bernstein coefficients after x=a+(b-a)t. If every coefficient is nonnegative, the polynomial is nonnegative because the Bernstein basis is nonnegative and sums to one. Otherwise split exactly at the midpoint using de Casteljau and repeat. Every terminal leaf is checked; all leaf counts and depths agree. The largest degree here is 116, and no grid, floating optimizer, or library numerical polynomial routine contributes to acceptance.

This proves x^4 p(x)>=x^k throughout support, including x=0. In particular the proof never divides by x, presumes a lower nonzero support bound, or ignores the negative half-line. Summing is justified by absolute convergence of powers 4 through 12. Its upper bound uses each coefficient's correct interval direction. All ten bounds are independently reproduced. Only the N36 majorant is needed by the improved seed; checking the other nine validates the additional advertised moment results rather than silently narrowing the review.

## 4. Full multiplicities, dominant atom, and physical anchor

For y_i in [0,h], sum y_i<=m, and r>=1, convex transfer of mass between two unsaturated coordinates increases sum y_i^r. Finite families therefore obey C(m,h,r)=floor(m/h)h^r+(m-floor(m/h)h)^r. This expression is nondecreasing in m; finite-subfamily limits extend the bound to countable lists. Without a cap, sum y_i^r<=m^r.

Use y=lambda^12, mJ and mN equal to their refined upper endpoints, and U=max(J caps), V=max(N caps). The original exact D26 periodic MPS72 contraction has V72>0 and -700741 V72-500000 U72>0. U72 is a ONE-BOND insertion. Consequently the total shifted Rayleigh quotient is 72(U72/V72+a)<0, and Z72(b)>1 at every b>0 by the variational principle. This is an inherited physically reviewed contraction, checked again by exact signs, not a new contraction or a uniqueness premise. D=26 is its bond dimension, not the full physical Hilbert dimension 3^72 and not a thermal transfer rank.

At ell=.9999979746, the exact inequality C(mJ,ell^12,6)+3C(mN,V^12,6)<1 contradicts Z72>1 if every J atom has modulus<=ell. Hence at least one J atom exceeds ell in modulus. Since ell exceeds the negative-J cap, that atom is positive. Removing one occurrence leaves residual twelfth mass R=mJ-ell^12>0. The verified R<ell^12 also excludes a second J occurrence of that size. Multiplicity three is retained in every N contribution.

For k=36,72, the old-refined packing tail is RA(k)=R^(k/12)+3C(mN,V^12,k/12). Its thermal bound is

T(72,49/4)>=[U^72+RA(72)]^-2,

using Z72(49/2)>1. For the spatial seed improve the tail to R^3+3 B_N36, where B_N36 is the certified long-polynomial upper bound on ONE N list. Keeping the dominant lambda^72 term in the numerator gives

S(36,49/4)>=[1+(R^3+3 B_N36)/ell^36]^-2.

The resulting defects are approximately .040903345383812 and .175483695027402. All expressions are independently reconstructed as exact fractions. The unchanged cap-only spatial defect was approximately .04467006818632. Dropping the N multiplicity would falsely improve the bound; an adversarial fixture explicitly detects that difference.

## 5. Canonical recurrence and every integer window

At state (n,beta), the variables are S(n,beta) and T(2n,beta). These cannot be relabeled as an unstaggered pair. The accepted purification theorem gives the sequential updates

S_new=G(S^2 T), T_new=G(T^2 S_new), G(z)=1-(1-z)^2/(2z^2),

then doubles both n and beta. G is increasing on (0,1]. The independent checker verifies every saved downward-rounded output against its unrounded exact expression, uses the NEW spatial endpoint in the thermal update, and checks all domains and coordinates.

For completeness, the finite-window argument is reconstructed here. At beta and 2beta the exact exchange identity gives S(n,2beta)>=K=S^2 T because T(n,beta)<=1. For even n, the normalized n-th absolute transfer weights at 2beta have purity>=K>1/2, hence a unique largest weight at least w=(1+sqrt(2K-1))/2. Compactness and the finite n-th absolute moment imply a strict modulus ratio below one for the remaining spectrum. If the leading transfer eigenvalue were negative, all sufficiently large odd traces would be negative. The all-integer physical trace identity and positive physical traces exclude that. This step concerns the leading eigenvalue only, not positivity of subleading eigenvalues.

Set rho=(1-w)/w and d=T/(1+rho^2). Relative absolute tail at 2n is at most rho^2 and at every L>=n is at most rho. For a=L/(2n), n<=L<=2n, the dominant positive eigenvalue therefore gives

Z_L(2beta)>=[Z_2n(2beta)/(1+rho^2)]^a(1-rho).

Absolute-spectrum Holder interpolation between the even powers n and 2n gives

Z_L(beta)<=Z_n(beta)^(2-2a) Z_2n(beta)^(2a-1).

Dividing these estimates yields T(L,beta)>=(1-rho) S^(2-2a) d^a. Its logarithm is affine in a, so the uniform bound is C=(1-rho)min(S sqrt(d),d). Lower square-root endpoints increase rho and decrease d,C in the safe direction. The proof applies to every integer L in the interval, including odd L, without physical purity monotonicity in L.

The reviewer uses a 200-decimal rational grid, integer-isqrt brackets and a separately implemented 220-term positive Taylor exponential at reduced argument<=1/4. This differs from the producer's 160-decimal root bisection and 180-term exact Taylor routine. Every saved C and margin is verified against these tighter independent enclosures. All eleven windows [36*2^j,72*2^j], j=0,...,10, satisfy C>exp(beta*.0214)(1-C)>0 at their actual temperature. The smallest displayed margin is about .06526, so no marginal floating comparison is involved.

A Gibbs purity C>1/2 forces its largest normalized weight to be at least C and unique. The second-to-first ratio is at most (1-C)/C. The stated exponential inequality therefore proves the gap and unique ground state throughout each window.

## 6. Infinite closure, with an independent elementary window estimate

At n*=36864, beta*=12544, let u=max(1-S,1-T). The exact check gives 0<u<=.01 and 5u exp(beta*.0214)<1. The first recurrence defect is at most

u^2 (3-3u+u^2)^2/[2(1-u)^6] <= 9u^2/[2(.99)^6] < 5u^2.

Using that new spatial bound, the second defect is at most

u^2 (2+5u)^2/[2(1-2u-5u^2)^2] <= 5u^2.

The numerical constants are verified rationally at u=.01, with monotonic numerator/denominator bounds. For the first expression one may bound its numerator by 9 and denominator by 2(.99)^6, also below 5; the recorded sharper endpoint comparison is compatible with the decreasing numerator and increasing full ratio.

A direct independent proof of C>=1-4u uses K>=(1-u)^3>=1-3u. For u<=.01, sqrt(2K-1)>=1-(7/2)u (since u<=4/49), hence rho<=9u/5 (since u<=1/63). Thus d>=(1-u)(1-rho^2)>=1-u-(81/25)u^2>=1-(26/25)u. Since sqrt(d)>=d, both entries of the minimum are at least 1-(51/25)u. Therefore C>=(1-9u/5)(1-51u/25)>=1-(96/25)u>=1-4u. Its excited-to-ground ratio is at most 4u/(1-4u)<=5u.

Iteration gives u_j<=(5u)^(2^j)/5 while beta_j=2^j beta*. Consequently 5u_j exp(beta_j*.0214)<=[5u exp(beta*.0214)]^(2^j)<1 for every j. No finite decimal rounding floor is used in this analytic closure. The early dyadic windows have shared endpoints and no holes, and the terminal theorem covers every later one. Together they establish precisely all integers L>=36.

## 7. Provenance, adversarial tests, and reproducibility

The unchanged official initialization.tex, thermal72.tex, and trials.tex snapshots are retained with their exact Git blob and SHA256 pins in SOURCE_PROVENANCE.json. Apache-2.0 LICENSE, attribution, and the prior relevant-ancestor NOTICE checks accompany them. The audit independently verifies both SHA256 and Git blob hashes. These sources are read locally; no source code from the external paper is executed.

Twenty adversarial mutations are rejected, including wrong odd signs/interval direction, unsupported cap, false shift, false nonexclusion point, endpoint-only polynomial positivity, omission of zero, missing window, wrong temperature/coordinate, unstaggered thermal input, inflated recurrence/window values or gap, false onset/defect, and fractional mass substituted for one spectral occurrence. Separate exact witnesses cover multiplicity three and the necessity of positive odd physical traces. Exhaustive evaluation of 1,024 moment-box corners validates the adverse coefficient directions.

Run `python audit.py` and `python adversarial_tests.py` from this folder. Both use only the Python standard library, CPU2, at most 600 CPU seconds and 700 MiB address space. First independent full replay consumed 37.99 CPU seconds and 29,080 KiB peak RSS; final replay resources are in results.json. No thermal job, root status, remote repository, or frozen producer artifact was modified. The active tree is extracted and has no Git metadata. This review's local manifest seals its proof, checker, results, negative fixtures, source copies, and frozen producer snapshot.
