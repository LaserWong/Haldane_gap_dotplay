# Independent joint-aware ordinary-bilayer interval audit

Updated 2026-10-10 15:25 America/New_York (EDT, UTC−4) / 19:25 UTC.

## Accepted result

Both new closed coupling intervals pass independent exact-arithmetic application review, after the producer was frozen and the new scalar lemma received its separate independent acceptance:

| Coupling interval | Initial β | Gap lower bound for every integer L≥2 |
| --- | --- | --- |
| [39/500,79/1000] | 103/10 | 20733752457/10^12 = 0.020733752457 |
| [79/1000,2/25] | 207/20 | 4107651847/(5·10^11) = 0.008215303694 |

Thus the entire real interval 0.078≤g≤0.08 has gap at least 0.008215303694. Combining it with the unchanged, independently sealed 31-piece certificate gives a 33-piece exact cover of

**0≤g≤0.08, every integer square side L≥2, with gap at least 486442811/250000000000 = 0.001945771244 and a unique finite-volume ground state.**

The model is the ordinary spin-1/2 square bilayer, with unit rung exchange, equal nonnegative straight intralayer exchange g, no crossed bonds, and periodic positive-direction bond multiplicity retained at L=2. There is no conclusion about arbitrary aspect ratios, infinite-volume ground-state uniqueness, a physical transition, optimality of g=0.08, or the actual gap. This is an analytic proof with exact arithmetic, not proof-assistant verification.

## Frozen provenance and independence

The following are hard gates in `ACCEPTANCE_GATES.json`, checked before acceptance:

- Prior independent interval review, `interval_extension_review/MANIFEST_SHA256.json`: `1af6c2142aa6a3649fd50275a8582add9cfe0a72ff8f21556195185c495eb956`, 123 sealed files.
- New producer freeze, `interval_joint_extension/FROZEN_MANIFEST.json`: `bc90f03bf6e2b0abf0e3694e957e3a0a2b7482f3fdf56a396bddffd5a5c5380c`, 17 files. All were copied byte-for-byte into `snapshot/`; the original manifest is preserved as `PRODUCER_FREEZE.json`.
- Independent scalar-lemma review, `joint_ratio_review/LEMMA_REVIEW_MANIFEST.json`: `18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91`, 13 files. Its accepted theorem and full domain are pinned verbatim in the gate record. The lemma's producer seal is `905a55c3419a08082c05f8fe011116e2655035c23cb9040e4e92ad856ce4e9bc`.

`INPUT_SHA256.json` additionally pins 74 external files. Every external dependency declared by the frozen producer is checked. The seven physical/theoretical reviews inherited by the earlier interval auditor are verified in full, totaling 656 files; their manifest hashes are recorded in `results/SUMMARY.json`.

The application audit imports no producer module and invokes no eigensolver. Its new joint recursion, route merger, joint-aware finite windows, tail witness and complete coverage checks are independently written. It explicitly reuses the pinned earlier independent auditor's physical matrix assembler, fixed-vector/filter checks, and directed exponential arithmetic. This is disclosed reuse of accepted components, not a claim of reimplementing every earlier theorem.

The three physical polynomial matrices are assembled afresh in exact arithmetic from the previously exhaustively reconstructed and hash-sealed F/S/V/W geometry. No new six-site enumeration or geometry contraction is claimed. The frozen prior review already checked that geometry and all 21 original physical moment files. No frozen source or prior result was edited. The shared extracted tree has no Git metadata; this review does not imply a new commit or remote publication.

## 1. Exact physical polynomial inputs and interval scope

Write H′(g)=H(g)+3N/4=Q+gV. The fixed even trial basis contains q=0,2,4 triplet sectors. With its known common norm factor removed,

G=W*W, K(g)=K0+gK1, J(g)=(H′(g)W)*(H′(g)W)=J0+gJ1+g²J2.

J is the full second moment, including the q=6 image. It is not the compressed square K G^−1 K. The degree statements follow from fixed W and affine H′. Exact evaluations of the assembler at formal g=0,1,−1 recover these coefficients and agree entrywise with all three previously accepted polynomial exports. Those formal points extract coefficients only; no stability theorem is applied there.

For every saved integer vector c, the audit verifies its geometry, dimension, positive metric norm n=c*Gc, affine Rayleigh coefficients ρ=c*Kc/n, quadratic full second moment, and complete residual v=c*Jc/n−ρ². The covariance inequalities v0≥0, v2≥0 and 4v0v2≥v1² are checked exactly. Therefore v is a nonnegative convex quadratic on the real line. Its maximum on each interval is an endpoint maximum; its minimum is the lesser endpoint or its rational interior vertex. A fixed vector is used throughout each entire interval, not selected separately at unsampled interior couplings.

The denominator vectors are checked against the accepted auxiliary exports at g=0.08. Their derivation as inverse-moment witnesses is not used to identify additional levels. Only their concrete fixed-vector moments enter this certificate.

## 2. Uniform filter, ground identification and trace bounds

For the largest patch, r(g)=(H′(g)−ρ(g))ψ is orthogonal to ψ, has norm squared v(g), and has q≤6. The accepted local number-preserving inequality and bosonic creation comparison give a 4×4 upper Jacobi form on q=0,2,4,6. Every coefficient is nondecreasing for g≥0. At the upper endpoint b, the auditor reconstructs its rational diagonal/off-diagonal-squared entries and every exact positive LDL pivot for Rmax I−Jplus(b). Thus <r,H′r>≤Rmax v uniformly on [a,b].

Let Cmax=Rmax−min(ρ(a),ρ(b))>0, vmin=min_[a,b]v, and t=1/Cmax. The normalized filtered trial obeys

<φ_g,H′φ_g>≤ρ(g)+v(g)[−2t+(Rmax−ρ(g))t²]/[1+t²v(g)]
                 ≤ρ(g)−vmin Cmax/(Cmax²+vmin).

The second inequality uses the negative numerator and monotonicity of v/(1+t²v) together; it does not separate incompatible extrema. Every constant and improvement is recomputed. The two gains are approximately 0.00179555947215 and 0.00191736224234. The resulting upper endpoint remains affine in g. Since Q preserves the original pure-q space, the whole interval family lies in the original space plus at most the one direction Vψ, dimension at most 30. No filtered-state residual, H³ or H⁴ is asserted or required.

For N=16 and 32, the inherited stable quadratic-boson comparison gives

Eref(q,g)=C(2g−1)+(C+q)√(1−4g), C=3N/8.

Its difference from affine ρ(g) is concave, so its smaller endpoint value is a lower bound at every real interior g. Every endpoint square root is enclosed downward by an exact integer-square inequality at 60 decimal places. The full second level uses q=1; the second even-sector level uses q=2, by the inherited parity-preserving comparison. Positive q=1 margins identify the unique global ground as the even trial's ground. Even-sector Temple gives λ1≥ρ−vmax/m2. Across both intervals the minimum q=1 margin exceeds 0.797862075803 and the minimum q=2 denominator exceeds 1.622483200927.

The full trace, including both parities, is bounded using one retained ground level and bosonic reference multiplicities dq=binom(3N+q−1,q), q=1,…,N. Their list including q=0 has binom(4N,N)≥4^N entries, enough for physical min–max counting; positive excess terms are safe. This uses no odd/triplet trial band and does not equate bosonic multiplicities to hard-core shell multiplicities.

The exact correlated affine energies are 8ρ16−2ρ64, 16ρ16−4ρ64 and 4ρ32−2ρ64, with the filtered largest endpoint. The shifts −3N/4 cancel, and each combination is minimized jointly at its common g endpoints. All normalized trace upper bounds enclose the auditor's independent tighter 512-bit dyadic exponential bounds. Every final 18-decimal ratio and initial purity is reproduced exactly. The exponential algorithm uses 112 Taylor terms with an explicit geometric remainder and argument reduction to |x|≤1/16.

## 3. Preserved product and every canonical update

The new scalar theorem is used only within its independently accepted reflected even-base domain. At a common base, actual purities are in (0,1], and telescoping gives

A⁴B²C=a⁴b²c=Z(final)/Z(initial)^8.

Initial lower txy values a,b,c give K=floor18(a⁴b²c), retained separately. Adjacent-order conversion gives canonical component lowers

A=floor18(a√b), B=floor18(a²b√c), C=floor18(a⁴b²c)

at the same base (8,8,2β). K can exceed the product of those transported component lowers without inconsistency; the lower values are simultaneous inequalities, not simultaneously attained physical values.

Dropping actual factors≤1 gives B²C≥K, A²B≥√K and C≥K. The auditor independently checks each sequential canonical argument and downward output:

D=G(max(A_l⁴B_l²C_l,K)),
E=G(max(B_l⁴C_l²,K²)D),
F=G(max(C_l,K)⁴D²E),
G(z)=1−(1−z)²/(2z²).

Arguments and positive outputs are all checked in (0,1]. Independently, the txy triple undergoes three ordinary rotating-order updates. Both routes end at exactly the same doubled base and β; only then is the new txy triple transported and merged componentwise with canonical bounds. The next K is reconstructed from valid new-base canonical and txy products. The old K is never silently carried to a different base. A nonpositive route is discarded, never clipped upward.

All nine full coupled transitions pass, including each scalar update argument, both order-specific triples, route merger, explicit base and temperature. The two records contain five and six saved states, ending at n=128 and n=256. Every reflected base is even. This does not posit spatial purity≤1 on arbitrary odd base geometries.

## 4. Every finite-size bridge and asymptotic tail

Each saved state is given its own joint-aware finite window. Define

I(s,t;K)=(1−r)min(s√d,d),
p=max(s²t,K), w=(1+√(2p−1))/2, r=(1−w)/w, d=t/(1+r²).

Both inverse-purity arguments must exceed 1/2. In two dimensions, with B_l>1/2,

sx=max(A_l²√(2B_l−1),√K√(2B_l−1)/B_l),
ty=I(B_l,C_l;K), thermal=I(sx,ty;0).

The whole quotient √(2B−1)/B is monotone on [1/2,1]; numerator and denominator are not bounded independently. No unproved outer joint constraint is introduced. All 40-decimal directed roots, subordinate values and saved details are independently reconstructed. Every reported rational window gap d satisfies the rigorous exponential test exp(βd)(1−thermal)<thermal. The accepted signed-transfer theorem supplies all integer target sizes, including odd target sizes, within each window.

For [.078,.079], successive required windows start at L=8,16,32,64 and have gap lower bounds .047492735480, .036947456381, .031358741848 and .028941865765. For [.079,.08], required windows start at L=8,16,32,64,128 and give .036099386632, .022320500910, .015257051867, .012954347563 and .012158966123. The two extra windows at the asymptotic onsets are also validated, though not needed for coverage.

At n=128 or 256, the common component defect is already ≤1/500, so the unchanged analytic scalar-tail theorem applies with zero additional recorded rounds. Its constants are checked exactly at the threshold. Each rational asymptotic gap satisfies exp(βd)32u<1 using directed exponentials, with no floating logarithm in acceptance.

The twelve independent short-size rows cover L=2,…,7. Their periodic edge-square sums are reconstructed as 16,18,32,50,72,98, preserving doubled bonds at L=2. The product-singlet upper endpoint is zero. The decreasing second-level comparison at the upper g endpoint supplies the uniform positive short-size gaps; monotonicity of the physical gap is not assumed.

Short sizes, consecutive closed windows and the tail together cover every integer L≥2. The coupling pieces meet at exact rational .079 and join the prior accepted [0,.078] cover at exact .078. The old cover includes g=0 with exact dimer gap 1. Its smaller lower bound controls the full 33-piece union.

## Validation, resources and reproducibility

`test_adversarial.py` rejects 41 targeted certificate corruptions: physical normalization/moments, Temple and filter constants, omitted shells, temperature or geometry mismatches, altered joint values, stale cross-base constraints, nonsequential updates, missing states/windows, outer/inner bridge data, short-size multiplicity and inflated gaps. Four exact filter fixtures exercise an interior variance minimum, both endpoint vertices and zero variance. Eight scalar guards reject values outside the purity domain and discard nonpositive updates. These finite tests supplement the analytic proof.

Run `bash REPRODUCE.sh` here. It verifies the finished review manifest before running, writes only this review's results/logs, then performs the independent acceptance replay and adversarial tests. Timing-bearing results can change on rerun, so the original manifest is meant to be verified before reproduction. The main replay uses about 26 MiB RSS and a few seconds here. Both programs set numeric threads to one, pin one CPU and cap address space at 1 GiB.

`results/SUMMARY.json` is the accepted machine-readable result; `results/physical_polynomials.json` pins the inherited geometry and reconstructed matrices. `MANIFEST_SHA256.json` seals the finished package. The earlier `results/PRELIMINARY.json` is intentionally preserved and explicitly marked unaccepted; final acceptance is solely in `results/SUMMARY.json` and `REVIEW_STATUS.json`.
