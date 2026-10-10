# Independent continuous ordinary-bilayer review through g = 0.085

Updated 2026-10-10 17:05 America/New_York (EDT, UTC−4) / 21:05 UTC.

## Accepted conclusion and scope

The frozen candidate passes independent exact mathematical replay and the additional fixed-center polynomial review. For the ordinary periodic spin-1/2 square bilayer, with rung exchange 1 and equal straight intralayer exchange g, no crossed bonds, and positive-direction periodic bond multiplicity retained, the new sixteen adjoining closed intervals cover

    2/25 ≤ g ≤ 17/200,
    gap(H_L(g)) ≥ 1682875193/500000000000 = 0.003365750386,
    for every integer square side L ≥ 2.

Every finite system in that scope has a unique ground state. Joining the already independently sealed 33-piece certificate gives **49 closed pieces covering every real g in [0,0.085]**, with the common all-integer-size lower bound

    gap(H_L(g)) ≥ 486442811/250000000000 = 0.001945771244.

This is an analytic proof supported by exact-arithmetic certificates, not a proof-assistant formalization. The bound is sufficient, not an estimate of the actual gap or a critical coupling. No claim is made for arbitrary aspect ratios, infinite-volume ground-state uniqueness, or a larger continuous interval.

The first seven new pieces cover [0.08,0.082] with ground-only denominators; their minimum is 0.005978179134. The following nine pieces cover [0.082,0.085] using the complete translated spin-one band on the two smaller denominator patches. Their minimum is 0.003365750386. The largest 8×8-rung numerator uses one filtered ground contribution throughout.

## 1. Freeze, provenance and independence

The candidate's FROZEN_MANIFEST.json has SHA-256

    cd21cbf09698816bf8cb096fe1680c89dff47ba5a895b1bedc1693ed2bec56dc.

All 52 frozen files are copied byte-for-byte to snapshot/ and checked against PRODUCER_FREEZE.json. All 96 direct external input hashes are checked. Eleven independent review seals, totaling 1,328 sealed files, are verified in full before helper imports. Three mandatory acceptance gates are:

- interval_joint_review/MANIFEST_SHA256.json: cc57b7779f77d91164ec68d612979817846a1ec91a66ab45c86b243becdabc8d
- joint_ratio_review/LEMMA_REVIEW_MANIFEST.json: 18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91
- bilayer_polynomial_frontier_review/MANIFEST_SHA256.json: 9cb0484af6d424e74e5520d8d995c88d63ab2c6396938634b98acf3927684930

The last review's explicit PHYSICAL_ACCEPTANCE.json is checked, including its normalized polynomial degrees, integer scaling and coefficient-file hash. Its discrete g=.085 gap is not substituted for a continuous-interval proof.

No producer module is imported or executed. Ground matrix assembly, exact exponential/root arithmetic, filter checks and scalar recurrences are disclosed reuse from the pinned independent interval auditors. The joint audit_record logic is reused with only the audited coupling range and physical trial/trace callbacks changed. The new denominator polynomial extraction, bivariate reconstruction, quadratic-field Fourier analysis and uniform odd Temple checks are independently implemented here. The executable module-boundary check rejects a project-local mathematical import outside this review and those two accepted interval reviews.

The original literal source is read and AST-checked, never imported. No eigensolver runs; proposed integer vectors are accepted only by their exact moments. No new large sparse support, H³/H⁴ moment, or full many-body spectrum is constructed. All writes are confined to this review directory. The extracted project has no Git metadata; no commit or remote publication is implied.

## 2. Physical Hamiltonian and complete ground moments

For N rungs, write H′(p)=H(p)+3N/4=Q+pV. A direct 16-dimensional four-spin reconstruction separately verifies the unit rung exchange, the two straight intralayer exchanges, and absence of crossed bonds. In the fixed rational rung metric the shifted rung spectrum is 0,1; V changes total triplet number by 0 or ±2. The normalized vacuum pair-creation norm squared is 3/4. Both signs of the local number-preserving comparison are positive semidefinite.

The fixed ground basis occupies q=0,2,4. The previously exhaustively reconstructed geometry contractions are hash-pinned. Fresh exact assembly at formal p=0,1,−1 recovers

    G = W*W,
    K(p) = K0+p K1,
    J(p) = J0+p J1+p² J2 = (H′(p)W)*(H′(p)W).

These formal points extract coefficients; no stability theorem is applied there. All entries and selected indices agree with the accepted polynomial exports. J includes the complete q=6 leakage; it is not K G⁻¹ K. Every saved integer trial vector is checked for dimension, positive metric norm, affine Rayleigh quotient ρ(p), complete second moment, and the exact full variance polynomial v(p). The exact covariance conditions v0≥0, v2≥0 and 4v0v2≥v1² establish nonnegative convex variance for all real p.

The ground-only pieces reuse the .08 auxiliary witnesses. The low-band pieces use newly proposed rational coefficient vectors, but no proposal eigenvalue is consumed: each vector is evaluated from G/K/J and certified by the same Temple argument.

For N=16,32 the accepted quadratic-boson comparison gives

    Eref(q,p)=C(2p−1)+(C+q)√(1−4p),  C=3N/8.

Its difference from affine ρ is concave. The smaller endpoint gives a uniform lower bound, using square roots enclosed downward by exact 60-decimal integer-square inequalities. The q=1 margin identifies the unique global even ground; the even-sector q=2 margin supplies its Temple denominator. The maximum variance occurs at an endpoint. Thus λground(p)≥ρ(p)−vmax/m2 uniformly. Across the sixteen pieces, the minimum full-ground identification margin exceeds .779489388792 and the minimum even Temple denominator exceeds 1.591893229256.

For the largest patch, the full residual has q≤6. The auditor reconstructs the 4×4 upper Jacobi comparison at the upper interval endpoint and every positive rational LDL pivot. Its monotone coefficients give a uniform residual compression upper R. Let Cmax=R−min ρ, t=1/Cmax, and vmin be the quadratic minimum, including any interior rational vertex. The normalized filter has Rayleigh upper

    ρ(p) − vmin Cmax/(Cmax²+vmin).

The negative numerator and the increasing fraction v/(1+t²v) are bounded together. Every saved improvement, fixed t, extremum and normalization is checked. No residual of the filtered vector is asserted. Because Q preserves the original basis, the family lies in that basis plus at most one Vψ direction, so the largest augmented dimension is at most 30.

## 3. Literal odd family and integer normalization

The literal construction forms T=dH′(z), d=4 denominator(z), begins with the bare q=1 triplet e_r, and constructs

    W_r = 2d e_r − P3 T e_r = 2d w_r(z),
    w_r(z)=u_r+z v_r,
    u_r=e_r,  v_r=−P3 V e_r/2.

Therefore Qu_r=u_r and Qv_r=3v_r exactly; v_r has no q=1 component. The metric and translations are independent of z. This is a stronger structural statement than merely placing w in q=1⊕q=3. The Hamiltonian, projectors and translations commute with total spin, so each w_r is a spin-one highest-weight vector. Its unchanged q=1 part ensures N independent translations. Three spin components give 3N directions. A complete H′ image occupies q=1,3,5, including all leakage to q=5.

For every cross-displacement matrix element, affine w and affine H′ prove the degrees

    G(z)=<w_0,w_r>: degree ≤2,
    A(z)=<w_0,H′(z)w_r>: degree ≤3,
    B(z)=<H′(z)w_0,H′(z)w_r>: degree ≤4.

These bounds are operator identities, not conclusions from sampled agreement. Since the stored moments contract W=2d w and TW=dH′W, their exact physical divisors are respectively **4d², 4d³ and 4d⁴**, with each source's own d. The fixed geometry-dependent metric factor is preserved.

For the 4×4 and 8×4 patches, reversed seven-point Newton divided differences independently recover each coefficient at z=.03,.04,.05,.06,.07,.08,.10. All above-degree coefficients vanish. A separate degree+1 fit agrees, as do the coefficients sealed by the earlier independent polynomial review. There are 1,008 exact source evaluations, including 432 values beyond the degree+1 defining samples. Every displacement satisfies inversion/Hermitian symmetry coefficientwise. Twelve deliberate physical normalization errors, using either raw stored arrays or an off-by-one denominator exponent, are rejected.

## 4. Bivariate reconstruction, including complex cross terms

Write G(z)=G0+z²G2. Q-eigenspace orthogonality implies no linear Gram term. Define

    Qmom(z)=G0+3z²G2,
    Q2mom(z)=G0+9z²G2,
    Vmom(z)=[A(z)−Qmom(z)]/z=v0+z v1+z²v2.

The quotient is an exact polynomial identity, including its continuous value at z=0. In the complete second moment the mixed polynomial is

    C(z)=<Qw_0,Vw_r>+<Vw_0,Qw_r>
        =2v0+4z v1+6z²v2.

For a term with left/right Q eigenvalues qi,qj, Hermiticity moves Q and V to give the weight qi+qj. Hence the weights 2,4,6 apply separately to every cross-displacement term. They do not assume that <Qw_0,Vw_r> equals <Vw_0,Qw_r>, or that either term is real. This closes the principal new analytic issue in the fixed-center construction.

The constant and linear terms of B−Q2mom−zC vanish identically, and

    D(z)=[B(z)−Q2mom(z)−zC(z)]/z²

is a degree≤2 polynomial. At fixed trial center z and arbitrary physical p,

    Gfixed=G(z),
    Afixed(p)=Qmom(z)+p Vmom(z),
    Bfixed(p)=Q2mom(z)+p C(z)+p² D(z).

The auditor checks 720 exact diagonal recoveries and every structural cancellation. Sixty independent exact complex-Hermitian fixtures use distinct left/right columns, unequal mixed QV and VQ terms, non-real cross moments, a separate q=5 leakage coordinate, z=0, negative z, and p≠z. They verify the full identity without any reality assumption. A polynomial vanishing at all seven source points explicitly demonstrates why finite samples alone would not establish the degree theorem.

## 5. All fixed-center Fourier modes and omitted states

Circulant translation moments diagonalize in momentum. Each Fourier symbol is reconstructed independently in Q(√2); the sides divide eight. All Gram symbols are strictly positive. Division gives affine θ_k(p), quadratic full second moment and quadratic full variance v_k(p). The exact quadratic-field signs of the two diagonal variance coefficients and covariance determinant establish nonnegative convex variance globally.

For each mode and interval [a,b], concavity of Eref(2,p)−θ_k(p) and convexity of v_k(p) give

    m_k=min_endpoint(Eref(2,p)−θ_k(p))>0,
    V_k=max_endpoint v_k(p),  w_k=V_k/m_k,
    ell_k=min_endpoint(θ_k(p)−ρground(p))−w_k.

All √2 bounds use exact 160-bit directed enclosures with the sign branch of the irrational coefficient handled correctly. Every saved endpoint enclosure, Temple denominator, width and correlated relative endpoint is reproduced exactly. The 432 mode certificates pass; the minimum uniform odd Temple denominator exceeds .410010420037. Another 3,888 within-interval evaluations supplement the concavity/convexity proof; they are not the justification for unsampled couplings.

Every odd Ritz mode is below the global q=2 cutoff throughout its interval. The even ground and 3N odd trial directions are orthogonal and span 1+3N directions below that cutoff. The complete bosonic comparison places ordered level 3N+2 at or above it. Consequently there are exactly 1+3N levels below the cutoff: the unique even ground and one level in each of the N momentum spin-one sectors, with spin multiplicity three. No omitted sector or additional low state is assumed away. Rank-one Temple within each sector now gives λ_k(p)−ρground(p)≥ell_k.

The oscillator reference multiplicities are dq=binom(3N+q−1,q), not physical hard-core shell multiplicities. Counts q=0 and q=1 are exactly 1 and 3N. Removing precisely those entries and retaining q=2,…,N leaves enough reference entries for all omitted physical eigenvalues, because

    Σ(q=0,…,N) dq = binom(4N,N) ≥ 4^N.

Any excess reference terms are positive and safe. Every multiplicity, total count and first omitted index is independently checked.

## 6. Directed traces, joint scalar states and all integer sizes

The denominator normalized trace is bounded by

    exp(βρground) Z′ ≤ exp(βwground)
        + 3 Σ_k exp(−βell_k)
        + Σ(q=2,…,N) dq exp(−βm_q).

Ground-only pieces instead keep the original q≥1 tail. Independent 512-bit dyadic Taylor exponentials, explicit geometric remainders and directed squaring verify each supplied ground/band/tail upper. No band multiplicity or omitted shell is dropped. The three affine energy combinations 8ρ16−2ρ64, 16ρ16−4ρ64 and 4ρ32−2ρ64 are minimized at common coupling endpoints; the physical energy shifts cancel exactly. All initial 18-decimal downward ratios and purities match.

The accepted same-base joint lemma supplies K=a⁴b²c=A⁴B²C. A formal partition-function exponent ledger verifies the common base and telescoping identity for both txy and xyt at every one of the 100 states. The scalar replay independently verifies all 84 transitions, including sequential canonical update arguments, three rotating-order updates, transport, route merger, doubled geometry/temperature, and recomputation of K at the new base. An old-base K is never carried over. Nonpositive routes are discarded, never clipped upward.

Each of the 100 states has a checked joint-aware finite window. The complete monotone quotient √(2B−1)/B is retained; the outer interpolation uses no unproved joint constraint. Both inverse-purity margins, all directed roots, every detail field and each rational gap's strict exponential witness are verified. The 84 pre-asymptotic windows are consecutive from L=8; the remaining sixteen windows at the asymptotic onsets are also checked. The final common defect is ≤1/500 at L≤1024, so the inherited analytic small-defect theorem covers all larger integers. Odd target sizes are included by the accepted signed-transfer interpolation, without assuming spatial purity bounds at odd bases.

All 96 short-size rows, L=2,…,7 for each interval, are independently reconstructed. Periodic edge-square sums are [16,18,32,50,72,98]; L=2 parallel bonds are not deduplicated. The singlet-product Rayleigh upper is zero and the decreasing q=1 comparison at the upper coupling endpoint gives each positive short-size bound. Physical-gap monotonicity is not assumed.

The final bound on each coupling piece is the minimum of the short-size, required finite-window and asymptotic bounds. Exact rational shared endpoints ensure the sixteen new intervals join each other and the previous [0,.08] certificate without gaps.

## 7. Dimensions, tests and reproduction

The physical patches remain 4×4, 8×4 and 8×8 rungs, containing 32,64,128 spins, with complete Hilbert dimensions 2^32,2^64,2^128. Ground search dimensions are 11,29,29. On the nine low-band pieces the two denominator traces retain 49 and 97 levels; their odd linear spaces have dimensions 48 and 96. The ground search plus odd spaces have dimensions 59 and 125. The actual fixed ground/odd witnesses span 49 and 97 directions. The largest numerator retains one filtered state in an augmented space of dimension at most 30. These numbers are not MPS bond dimensions. No largest-patch odd moment enters the mathematical replay, although provenance verification hashes entire earlier review seals.

The adversarial suite rejects 61 corruptions covering physical normalization, full residuals, filter minima/pivots, odd centers, Gram/Fourier moments, mixed coefficients, Temple bounds, band and tail counts, initial ratios, joint state/base mismatches, omitted windows and inflated gaps. Four exact filter fixtures test interior/boundary minima and zero variance; eight scalar guards test invalid domains and discarded nonpositive outputs. The separate bivariate suite has 60 complex fixtures, 12 normalization rejection tests and exact quadratic-field guards.

Run `bash REPRODUCE.sh` from this directory. It verifies the final review manifest before running, executes the independent replay and tests sequentially, and writes only review results/logs. Every Python process enforces one CPU, one numerical-library thread and a 1-GiB address-space limit. The complete sequential reproduction passed in 42.94 seconds with 33,388 KiB peak child RSS (about 32.6 MiB). The main mathematical replay took 27.23 seconds in that run. Timing-bearing outputs may change on reproduction, so preserve or verify the sealed package before rerunning.

The authoritative machine-readable result is results/SUMMARY.json together with REVIEW_STATUS.json. The final MANIFEST_SHA256.json seals the complete review package. Original producer files, prior review files, root project files and GitHub are unchanged.

## Interval results

| Closed coupling interval | Initial beta | All-integer-L≥2 gap lower |
|---|---:|---:|
| [2/25, 161/2000] | 52/5 | 0.012803905637 |
| [161/2000, 81/1000] | 209/20 | 0.007839659402 |
| [81/1000, 13/160] | 101/10 | 0.012042649244 |
| [13/160, 163/2000] | 209/20 | 0.009925833451 |
| [163/2000, 327/4000] | 41/4 | 0.005978179134 |
| [327/4000, 131/1600] | 21/2 | 0.009304607579 |
| [131/1600, 41/500] | 21/2 | 0.006992836884 |
| [41/500, 33/400] | 44/5 | 0.022177736183 |
| [33/400, 83/1000] | 44/5 | 0.015615550369 |
| [83/1000, 167/2000] | 44/5 | 0.012467078143 |
| [167/2000, 21/250] | 177/20 | 0.005705272078 |
| [21/250, 337/4000] | 177/20 | 0.010600821716 |
| [337/4000, 169/2000] | 173/20 | 0.006958866515 |
| [169/2000, 339/4000] | 35/4 | 0.003365750386 |
| [339/4000, 679/8000] | 177/20 | 0.006937745488 |
| [679/8000, 17/200] | 177/20 | 0.004135722317 |
