# Independent review of the ordinary-bilayer continuous extension

Updated 2026-10-10 15:16 America/New_York (EDT, UTC−4) / 19:16 UTC.

## Verdict and exact scope

The frozen extension passes independent exact-arithmetic and analytical review. For the ordinary spin-1/2 square bilayer,

Δ_L(g) ≥ 2006633957/1000000000000 = 0.002006633957,

simultaneously for every real 7/100 ≤ g ≤ 39/500 and every integer square side L≥2. Together with the sealed prior interval certificate, this gives

Δ_L(g) ≥ 486442811/250000000000 = 0.001945771244,

for the entire closed interval 0≤g≤0.078 and every integer L≥2. Each indicated finite periodic Hamiltonian has a unique ground state. The extension uses fifteen closed intervals, and the combined coverage uses thirty-one. These are uniform interval certificates, not interpolation of isolated gap values.

The model has unit antiferromagnetic rung exchange, the same nonnegative straight intralayer coupling g in both layers and directions, and no crossed exchange. Positive-direction periodic bonds retain multiplicity at length two. No conclusion is asserted for arbitrary aspect ratios, all infinite-volume ground states, the true physical gap, or the optimal coupling frontier. This is exact computation plus analytic proof, not proof-assistant formalization.

The seed patches have 16, 32, and 64 rungs, hence 32, 64, and 128 physical spins and full Hilbert dimensions 2^32, 2^64, and 2^128. Their original linear trial dimensions are 11, 29, and 29. Exactly one ground level is retained in each smaller denominator, and one filtered trial contribution is used in the largest numerator. Its augmented space has dimension at most 30 and support at triplet number q≤6. No excited-state trial family is needed. None of these dimensions is an MPS bond dimension.

The largest full second moment is now required, although it was unnecessary in the earlier unfiltered first-moment-only certificate. Existing G/H/H² inputs suffice: no H³ or H⁴, new physical contraction, new geometry, filtered-state residual certificate, or maximum-patch diagonalization is used.

## Frozen provenance and independence

The producer freeze contains 28 files and has SHA-256:

3b1f4f32cea6b844fffe2f56ef23a13b437fcf9cf3f2a1f24c44b4afe0bdc8a0.

It is preserved as `PRODUCER_FREEZE.json`, with every listed file copied byte-for-byte to `snapshot/`. `INPUT_SHA256.json` binds 105 local inputs, including all three exact polynomial exports, all 21 original physical moment files, all 21 original negative-witness files, all 21 auxiliary exports, and the prior physical geometry. All auxiliary export manifest entries and every external dependency listed by the producer are checked too.

Seven earlier review manifests, totaling 656 files, are verified in full: ordinary_interval_review, variational_filter_review, ground_moment_review, large_seed_review, quadratic_boson_review, alternative_order_review, and bosonic_tail_review. Their exact manifest hashes and file counts are in `INHERITED_REVIEWS.json`. The source moments and negative-witness files are also matched by hash to the sealed ground_moment_review inputs.

No producer module is imported or executed by the independent acceptance program, and no eigensolver is used. The program explicitly reuses the sealed earlier independent interval auditor's physical assembly, directed exponential arithmetic, and scalar/finite-window replay. New code checks the auxiliary exports, complete largest-patch second moment, uniform filter, and expanded coverage. Reuse is disclosed rather than represented as a fresh implementation of every inherited component.

Previously exhaustively reconstructed F/S/V/W geometry is reused by verified hash; no new 8×8 six-site enumeration is claimed. Both previous theory and reviewed physical contractions remain explicit dependencies. The extracted shared tree has no local Git metadata; these filesystem results do not imply a new commit or remote publication. Producer and older reviewed files were left unchanged.

## 1. Physical polynomial inputs and auxiliary witnesses

Let H′(g)=H(g)+3N/4=Q+gV and W be the fixed physical basis formed from the vacuum, invariant pair-singlet orbit sums, and their fixed four-triplet A42 images. All columns have even triplet parity and definite q=0,2,4. With the common factor 2^N removed,

G=W*W/2^N,
K(g)=W*H′(g)W/2^N=K0+gK1,
J(g)=(H′(g)W)*(H′(g)W)/2^N=J0+gJ1+g²J2.

The degree statements are analytic consequences of fixed W and affine H′, independent of sampled data. The full image includes q=6; J is not K G^−1 K.

The auditor reconstructs periodic graphs, pair orbits, Gram matrices, first moments, and full second moments for all three patches from the sealed physical geometry. Exact formal evaluations at g=0,1,−1 recover the known-degree coefficients. These formal values only extract polynomial coefficients; no stability or spectral theorem is applied at those couplings. Every coefficient equals the auxiliary export exactly, and independent-column selections give dimensions 11/29/29.

A second consistency check evaluates those reconstructed polynomials at every available physical source coupling .03,.04,.05,.06,.07,.08,.10, checking all 21 G/K/J files entry by entry. Integer denominators are exactly d=4 denominator(g), first moments are divided by d, second moments by d², and the common norm factor is exactly 2^N. Thus the required three distinct points for a quadratic identity are exceeded, while the analytic degree bound is supplied separately.

Every auxiliary vector equals its original negative-direction witness. Its exact norm, two Rayleigh coefficients, three full second-moment coefficients, and three residual coefficients are recomputed. The center identity

[(ρ−a)(ρ−l)+v] = c*M(l)c/(c*Gc) < 0

and the corresponding Temple center endpoint are checked for all 21 exports. This provenance does not turn different witnesses into different levels. For this extension each chosen auxiliary vector is simply one nonzero fixed even trial, and the required spectral-count statement is re-established over the interval below. The inverse-moment method that proposed it is not a needed hypothesis.

For each embedded integer vector c, n=c*Gc>0,

ρ(g)=c*K(g)c/n,
v(g)=c*J(g)c/n−ρ(g)²=v0+v1g+v2g².

All coefficients and normalization values agree exactly. The checks v0≥0, v2≥0 and 4v0v2≥v1² verify the underlying two-operator covariance positivity. Thus v is a nonnegative convex quadratic; its maximum is the endpoint maximum and its minimum is attained at an endpoint or at the rational vertex −v1/(2v2), when that vertex lies inside the interval.

## 2. Uniform largest-patch filter

Let ψ be the normalized fixed base trial, r(g)=(H′(g)−ρ(g))ψ, and v=||r||². Exact orthogonality gives <ψ,r>=0 and <ψ,H′r>=v. For fixed t≥0 the normalized filtered state is

φ_g=(ψ−t r(g))/sqrt(1+t²v(g)).

If <r,H′r>≤R v, then

<φ_g,H′φ_g> ≤ ρ(g)+v(g)[−2t+(R−ρ(g))t²]/[1+t²v(g)].

The auditor independently reconstructs the four-spin local exchange in rational dimer coordinates. It verifies parity, maximum number change two, and positivity of (Qi+Qj)/2−V_pres by exact rational Schur complements. The latter has rank 12 and nullity 4; the nonorthogonal coordinate calculation is a congruence with its explicit Gram metric. The three normalized vacuum-creation amplitudes each have square 1/4, giving total square 3/4.

Consequently the weighted degree-four graph gives Pq H′Pq≤(1+2g)q. The inherited hard-core boson creation bound gives

||P(q+2)H′Pq||²≤bq(g),
bq=(floor(q/2)+1)v_b+4g² floor((q+1)²/4),
v_b=(3g²/4)Σe we².

For the 8×8 patch Σe we²=128. Since r has q=0,2,4,6, Cauchy–Schwarz bounds its expectation by the four-by-four Jacobi form with diagonal (1+2g)q and positive off-diagonals sqrt(bq). All entries are nondecreasing for g≥0; the form evaluated on xq=||Pq r|| at any g∈[a,b] is therefore bounded by the same form at b.

The saved rational Rmax has strictly positive exact LDL pivots for Rmax I−Jplus(b). Every pivot is recomputed, and the preceding 10^−16 grid point fails positivity. This proves a uniform upper bound without a floating eigenvalue or approximate square root. Although H′r may reach q=8, those components are orthogonal to r and do not enter the expectation. This does not prove a full residual bound for φ_g.

Set Cmax=Rmax−min(ρ(a),ρ(b))>0, vmin=min_[a,b] v≥0, and t=1/Cmax. Then C(g)=Rmax−ρ(g)≤Cmax, so

−2t+C(g)t²≤−1/Cmax.

Since v/(1+t²v) is increasing on v≥0, the correct uniform gain is

d=vmin Cmax/(Cmax²+vmin),

and <φ_g,H′φ_g>≤ρ(g)−d throughout the interval. Normalization and the negative numerator are treated together; replacing their extrema separately could reverse the desired bound. The saved gains range approximately from .001019354696 to .001749519390, and every exact gain is positive.

The filtered upper endpoint remains affine in the same g because d is fixed on the interval. Q preserves the original pure-q trial space, so the entire interval family r(g) lies in W+span{Vψ}; the augmented dimension bound 30 holds for the whole family on each interval, not merely at one g. The family remains even, spin zero, and supported at q≤6. Jensen's inequality gives the single trace contribution Z′64(2β,g)≥exp[−2β(ρ(g)−d)].

## 3. Ground identification, even Temple denominator and full trace tail

The inherited stable quadratic-boson comparison, with δ=sqrt(1−4g), gives ordered reference energies

E_b+qδ=C(2g−1)+(C+q)sqrt(1−4g), C=3N/8

for the main patches. The physical Hamiltonian, hard-core projection, bosonic mode rotation, and coordinate squeezing preserve parity. Restricting min–max to the even sector gives λ2,even≥E_b+2δ, while the full-space bound is λ2≥E_b+δ. The squeezing parity statement follows because both mode rotation and each positive coordinate dilation commute with total coordinate inversion; it is not inferred from low-state samples.

For each denominator trial, E_b+qδ−ρ is concave in g, with second derivative −4(C+q)/(1−4g)^(3/2). Its lesser endpoint value is a uniform lower bound. Every endpoint square root is rounded downward by exact integer-square inequalities at 60 decimal places. The least saved ground-identification margin m1 exceeds .805364005416; the least even Temple denominator m2 exceeds 1.634821659549.

Because the trial Rayleigh quotient is below the full second-level cutoff, it identifies the unique global ground in the even sector. Rank-one Temple in that sector therefore gives

ρ(g)−w≤λ1(H′(g))≤ρ(g), w=vmax/m2.

No excited trial family or assumed complete triplet band is involved.

Bosonic reference multiplicities are dq=binom(3N+q−1,q), not hard-core shell counts binom(N,q)3^q. The sorted reference list through q=N has binom(4N,N)≥4^N entries. After replacing only its single q=0 ground entry, all remaining physical indices are bounded by the ordered positive q≥1 list. Adding excess positive terms is safe. Hence

exp(βρ(g)) Z′N(β,g)≤exp(βw)+Σ(q=1…N) dq exp(−βmq)=U_N(β).

This dimension argument does not assert that the squeezed physical subspace lies in reference sectors q≤N. All counts, tail terms, and q=1 starting indices are explicitly checked.

## 4. Shared-parameter correlation and transport

Let ρS,ρT be the two auxiliary affine Rayleigh normalizers and ρM the filtered affine upper endpoint. The exact correlated combinations are

h1=8ρS−2ρM, h2=16ρS−4ρM, h0=4ρT−2ρM.

Their minima are computed jointly at the common interval endpoints. The physical −3N/4 shifts cancel exactly in each combination. Independent extrema of separate extensive energies are not substituted.

The accepted lower ratios are exp(β min h1)/U16(β)^8, exp(β min h2)/U16(2β)^8, and exp(β min h0)/U32(2β)^2. The independent exponential routine uses 112 Taylor terms, reduction to |x|≤1/16, a geometric remainder, and 512-bit directed arithmetic. It is distinct from the producer's exponential implementation. All saved trace upper bounds enclose the independent tighter bounds; every 18-decimal lower ratio is reproduced.

For F(z)=1−(1−z)²/(2z²), the time–x–y route gives a=F(J1), b=F(J2a), c=F(C0^4 a²b). Adjacent-direction partition-function cancellation gives e c²=b a² and transports a lower pair to (a sqrt(b),a²b). Applying the two swaps yields canonical inputs

(A,B,C)=(a sqrt(b), a²b sqrt(c), a^4 b²c)

at base (8,8,2β). Every directed square root, basepoint, and downward rounding is checked. The inherited comparison and interpolation theorems retain their hypotheses. No spatial coordinate is identified with inverse temperature.

## 5. Every finite size and the exact union

All 66 complete three-direction recurrence rounds are independently replayed with sequential updates. At accepted defect u≤1/500, the inherited all-integer theorem supplies an asymptotic gap witness d whenever exp(β_final d)32u<1. This inequality is checked using directed exponentials, so no floating logarithm enters acceptance. The scalar contraction and interpolation constants are rechecked exactly at the threshold.

All 81 finite-window records are independently reconstructed, including both signed-transfer one-dimensional steps, principal-weight square roots, normalization ratios, and the final exponential gap inequality. The 90 short-size rows cover L=2,…,7 for each interval; their separately rebuilt edge-square sums are 16,18,32,50,72,98. The singlet-product Rayleigh upper is zero, and the decreasing comparison E_b+δ at the upper coupling endpoint gives the uniform short-size gap. Physical-gap monotonicity is not assumed.

The weakest new interval is [77/1000,31/400]=[.077,.0775], with β_initial=231/20 and asymptotic onset L=1024. Its required consecutive finite-window gap lower bounds, starting at L=8,16,32,64,128,256,512, are .057487070155, .026295859244, .012641810029, .006692741119, .004161322975, .003163798793, .002754271846. Each exceeds the accepted uniform extension bound .002006633957. An extra [1024,2048] window is checked but not needed.

The fifteen closed intervals meet by exact rational equality from 7/100 to 39/500. They join the earlier sealed sixteen-interval certificate at exactly 7/100. The older bound is smaller, so its value remains the combined uniform bound. Short sizes, consecutive finite windows, and the asymptotic tail cover every integer L≥2 without an omitted range.

## Reproduction and audit limits

Run `bash REPRODUCE.sh` from this review directory, or invoke it by its full path. This writes only review results and logs. The main audit and regression tests pin one CPU, set numeric thread counts to one, and cap address space at 1 GiB. The independent certificate replay takes approximately 16 seconds with about 26 MiB peak RSS in this environment.

Twenty-one targeted in-memory corruptions are rejected, including altered normalization, second moments, residual extrema, compression pivots, filter parameters, dimensions, tail counting, correlated exponents, transport, finite windows, period-two multiplicity and inflated gaps. Four further exact algebra fixtures cover an interior residual minimum, both endpoint vertices, and zero variance. The interior-minimum fixture specifically rejects the unsafe endpoint-only minimum; that branch is not visited by the actual fifteen certificates.

`results/SUMMARY.json` records the exact accepted union and per-interval results. `results/matrix_reconstruction.json`, `auxiliary_exports.json`, `local_parity.json`, `rejection_guards.json`, and `filter_edgecases.json` expose the individual checks. `MANIFEST_SHA256.json` seals the finished review. Verify it before reproduction, because timing-bearing logs/results may change on a repeated run.

The remaining continuous region above .078 is outside this review. A successful discrete certificate at .08 would not certify the intervening couplings. Bounded proposal-search failures likewise do not prove gaplessness or exclude all temperatures or methods.
