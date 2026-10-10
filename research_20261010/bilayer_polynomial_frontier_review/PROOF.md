# Independent polynomial frontier review

Updated 2026-10-10 15:38 America/New_York (EDT) / 19:38 UTC.

## Verdict and exact scope

PASS: for the ordinary spin-1/2 square bilayer at g=17/200=.085, every integer periodic square side L>=2 has a unique finite-volume ground state and spectral gap at least

    27887084487 / 10^12 = .027887084487.

Rung exchange is one, both straight intralayer directions in both layers have exchange g, and there are no crossed bonds. Positive-direction periodic edges retain multiplicity, including length-two parallel edges. Energy endpoints below use H'=H+3N/4 for N rungs; the energy shift does not change a gap.

This accepts one discrete new coupling. It does not extend a continuous coupling interval to .085, prove optimality, identify the actual physical gap or a phase boundary, or assert infinite-volume uniqueness or arbitrary-aspect-ratio uniformity.

The six new finite-seed physical input packages, at .085 and .09 on 4x4, 8x4 and 8x8 rungs, independently pass. The .09 package does not supply a new all-size gap certificate. Its three saved exact failed paths are verified as failures of those particular sufficient-bound paths. Its finite floating grid is neither an all-temperature exclusion nor evidence of physical gaplessness.

## 1. Frozen provenance and independence

The .085 producer freeze is low_band/frontier_bracket/FROZEN_MANIFEST_1928.json, SHA-256

    052d5c3a2c773a522484ba63c48f7f66ee029f32b27e22f5dc5458f7c6e23b94.

The selected record is g17d200/extra_cycles_exact.json, cycles_before_transport=8. That counter means eight additional complete time-x-y cycles after the initial correlated seed cycle. The latter already reaches (8,8,2 beta_initial). Thus nine complete cycles including the seed lead to the final base (2048,2048,22656/5).

The separate reusable joint-ratio proof is accepted only through joint_ratio_review/LEMMA_REVIEW_MANIFEST.json, pinned to

    18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91.

Its acceptance is not treated as acceptance of physical data. The present physical, exponential, basepoint and finite-window gates are separate.

PRODUCER_FREEZES.json pins both producer packages. INPUT_SHA256.json preserves all 139 snapshot files. PRIOR_REVIEW_SHA256.json records the complete accepted-review manifests for large-seed physics, the .06 order extension, the .07/.08/.10 frontier, the quadratic-boson comparison, the ground moment pencil, the residual filter, interval matrix assembly, the combined scalar review, and the separate joint lemma. All their sealed bytes, the producer's external dependencies, and this snapshot are checked before and after replay.

No producer module is executed. Independently reviewed assembly, exact Schur-inertia, Q(sqrt(2)) and filter functions are extracted unchanged from hash-pinned independent sources. Their entire source files remain in the snapshot. The point-specific acceptance driver and polynomial reconstruction are new. No physical sparse W/HW family is regenerated, no new high-q support is expanded, no eigensolver is called, and no full many-body spectrum is computed.

The shared workspace is an extracted snapshot without Git metadata. This review changes only its own directory and claims neither a commit nor publication. The review is exact-arithmetic plus analytic verification, not formal proof-assistant verification.

## 2. Literal physical family proves the polynomial degree

Fix a geometry and the rational orthogonal rung basis once and for all. A rung has unnormalized singlet, triplet-, triplet0 and triplet+ basis vectors, with metric diag(2,1,2,1). The N-rung product metric is independent of g. Q counts triplets, and the shifted physical Hamiltonian is

    H'(g)=Q+g V.

Let e_r be the bare localized magnetization +1 triplet. With P_3 projecting onto three triplets, put c_r=P_3 V e_r. The producer's literal trial family is

    w_r(g)=e_r-(g/2)c_r.

Indeed the source code constructs T=d H' with d=4q for reduced g=p/q, sets the bare coefficient of W_r to 2d, and subtracts every q=3 coefficient of T e_r. Since Q e_r=e_r has q=1, that q=3 piece is precisely d g c_r. Hence W_r=2d w_r; this is a g-dependent affine vector, not a fixed nearby-coupling vector.

The Hamiltonian, triplet-number projectors and translations commute with total spin. Thus w_r has total spin one and highest weight +1 for all real g. Its q=1 component remains e_r, so all N translated columns remain independent. The three spin components provide three orthogonal copies. One full H' image has only q=1,3,5 and includes every leaked q=5 component.

For an explicitly g-independent inner product, write w=e+g f with f=-c/2. Then

    G_rs(g)=<e_r,e_s>
            +g(<f_r,e_s>+<e_r,f_s>)+g^2<f_r,f_s>.

Also H'w=Qe+g(Qf+Ve)+g^2 Vf. Therefore

    G_rs(g)                              has degree <=2,
    A_rs(g)=<w_r,H'w_s>                  has degree <=3,
    B_rs(g)=<H'w_r,H'w_s>                has degree <=4.

The last expression is the complete physical second moment. Replacing it with the square of the compressed first moment would omit leakage and would not supply this certificate. Translation of either column preserves these degree statements for every displacement.

This is a proof from literal vector/operator definitions. Matching finitely many data points alone would not prove a degree bound: adding a multiple of the polynomial vanishing at all seven source couplings would evade such a test. The adversarial suite records that counterexample explicitly.

### Integer-denominator normalization

The stored displacement arrays contract W=2d w and TW=d H'W. Consequently

    G_stored=4 d^2 G_physical,
    A_stored=4 d^3 A_physical,
    B_stored=4 d^4 B_physical.

All source records must be divided by their own d before interpolation. The common physical metric, including its geometry-dependent factor, stays unchanged. At .085, d=800; at .09, d=400. The corresponding evaluated moments are multiplied by the appropriate 4 d^power and independently checked to be integers. The adversarial suite confirms that the raw unnormalized stored G arrays do not fit the claimed degree-two family.

### Independent reconstruction and extra checkpoints

For each of 112 displacements across the three geometries, the seven source couplings are .03,.04,.05,.06,.07,.08,.10. The 21 source JSON hashes occur in the accepted large_seed_review, alternative_order_review and bilayer_frontier_review seals. These reviews independently reconstructed the literal sparse columns, the complete H action, the metric and all displacement moments.

The producer fits the first degree+1 points by Lagrange evaluation. This audit instead fits the last degree+1 points in reverse order using Newton divided differences, converts to monomial coefficients, and checks every other coupling. It additionally constructs the full seven-point Newton polynomial and verifies every coefficient above degree 2/3/4 is exactly zero. The independent fits produce all new .085 and .09 arrays exactly.

There are 112*(4+3+2)=1008 extra-point checks. The exact reusable coefficients are saved in results/polynomial_coefficients.json. They describe physical moment identities for this affine family; they do not themselves certify a gap at every coupling.

## 3. Rebuilding the full physical finite-seed certificates

### Ground matrices and complete residuals

The ground trial basis is the g-independent vacuum/pair-orbit space B together with the q=4 vectors L=A_42 B. The previously independently rebuilt geometry contractions F=L*L, S=L*A_44L, V=(A_44L)*(A_44L), W=(A_64L)*(A_64L) are reused only after equality with their sealed independent results.

Fresh exact assembly gives G=<basis,basis>, A=<basis,H'basis> and B=<H'basis,H'basis>. The full H' image has q=0,2,4,6; W enters B and is not truncated. Every selected index and every new integer G, d A, d^2 B entry agrees. The exact coefficient-vector norm, Rayleigh quotient and full residual variance agree with the new records. The local two-rung relative-form matrices are also rebuilt directly from four physical spin-half exchanges and found strictly positive by rational inertia.

The base ground search dimensions are 11,29,29. Each patch retains one ground level. A residual filter uses a two-vector plane and an augmented-space upper dimension 12,30,30; it is not a new certified residual for the filtered vector. No MPS representation or bond dimension is used.

For .085 the complete original ground variances are approximately .0002967106944063562, .0029355219018837044 and .022351917349995726. Exact fractions, q=6 contributions and all endpoints are in results/physical_review.json. Small trial residuals alone are never used to assert spectral completeness.

### Translated spin-one band and full-space counting

All Fourier G/A/B symbols are rebuilt in exact Q(sqrt(2)), including every momentum and positive Gram norm. Their exact theta and residual variance, rational outward enclosures and rank-one Temple endpoints agree. There are N momentum directions, each with spin multiplicity three. A conjugate momentum pair is not counted an additional time.

The independently accepted quadratic-boson theorem gives D=3N oscillator modes, alpha=1-2g, v=(3g^2/4) sum_e w_e^2, delta<=sqrt(1-4g), and

    a_q=-v/(alpha+delta)+q delta,
    d_q=binom(3N+q-1,q).

Every edge multiplicity, directed square-root inequality, bin endpoint, multiplicity and first ordered index is rebuilt. In particular the first omitted index is 2+3N, and sum_(q=0)^N d_q=binom(4N,N)>=4^N. The oscillator multiplicities are never replaced by physical triplet-shell multiplicities binom(N,q)3^q.

In all six patches the ground Rayleigh rho<a_1 identifies a unique global even ground, while every one of the 3N odd trial Ritz values lies below a_2. Global min-max allows at most 1+3N levels below a_2. Thus the even sector has exactly one such level, every represented odd momentum/spin sector has exactly one, and no omitted sector has a level below the cutoff. This closes the missing-state issue before using Temple/pencil estimates or removing low levels from the trace tail.

The retained complete band dimensions are 49,97,193. The physical spin counts are 32,64,128 and complete Hilbert dimensions are 2^32,2^64,2^128. These are different from ground search dimensions and sparse support sizes.

### Pencil lower and filtered upper endpoints

For a=a_2 and a proposed ground lower endpoint l, the physical form

    B-(a+l)A+a l G = W_trial* (H'-a)(H'-l) W_trial

has a saved rational strictly negative direction. Since the even sector has exactly one eigenvalue below a, this proves that eigenvalue exceeds l. Every negative quadratic form is recomputed; five independent rational Schur-inertias per patch also verify G, A-aG, (H'-a)^2 moments, the endpoint pencil and the bracket's upper pencil, for 30 inertia tests overall.

The residual filter independently reconstructs its q=0,2,4,6 masses, checks their sum equals the complete variance, verifies the tridiagonal upper-bound positive pivots and directed cross-term roots, and checks the exact improvement inequality delta_gain*(R-rho+delta_gain)<=variance. The achieved upper Rayleigh bound agrees and is below the unfiltered rho. No higher moments or filtered-state residual are claimed.

Each combined patch is compared against the original full-band patch byte-structurally except for its declared ground endpoints, floor clipping, width and provenance metadata. All triplet endpoints and tail counts are preserved. The .09 physical inputs pass these same gates even though their selected scalar paths fail.

## 4. Directed physical heat traces and repeated-order bases

The scalar audit directly bounds Z'=Tr exp(-beta H'), retaining all 1+3N low-band terms and every positive q>=2 oscillator-tail term. It does not reuse the producer's normalized trace arithmetic. Independent 512-bit dyadic lower/upper exponentials use a range-reduced Taylor sum, individually directed terms, a geometric remainder and directed repeated squaring.

At beta_initial=177/20 the saved J1,J2,C0 witnesses are each no greater than independent direct-physical-trace lower bounds. Energy-shift cancellation is exact: the (16,32,64)-rung shapes and doubled inverse temperatures carry equal total shift in each ratio. The initial correlated cycle is replayed with exact 16-decimal downward endpoints.

For a ladder based at v, any order of the three commuting coordinate doublings obeys

    p_1^4 p_2^2 p_3 = Z(D_x D_y D_t v) / Z(v)^8.

This is the preserved same-base joint product K. The audit explicitly checks formal partition-function exponents for both txy and xyt at every repeated-cycle base. Rotating one purity step doubles the first direction's base and moves that axis to the back; three steps double all three coordinates and restore txy order. The ledger is in results/basepoint_ledger.json.

At additional cycle j the txy ladder and transported canonical ladder both have base

    n=m=8*2^j, tau=2*(177/20)*2^j.

Canonical lower components are (a sqrt(b), a^2 b sqrt(c), a^4 b^2 c). Every square root is rounded downward by an integer square-root enclosure, followed by downward component rounding. Each raw recursive step and rounding precision is independently replayed. K is recomputed from the current raw ladder and is not carried from a different base. It can exceed the product of the separately weakened canonical components without contradiction.

The eight-cycle selected canonical defect is about 4.13570232665195e-57. Its exact rational u satisfies 0<u<=1/500. The accepted small-defect theorem gives gap >= log(1/(32u))/tau. The proposed rational .027887084487 is accepted without trusting a floating logarithm, by checking the independent strict witness

    exp_upper(tau*.027887084487) * 32u < 1.

All five saved additional-cycle candidates, j=4,5,6,7,8, pass. Their all-size gaps are respectively .019519229939, .023775916983, .026073433601, .027276152074, .027887084487.

## 5. Every pre-asymptotic integer size, including odd sizes

Joint-aware two-dimensional signed-transfer interpolation uses the separately accepted joint lemma at each common even base. Its inner one-dimensional product bound uses K; its outer call has K=0 because no outer joint identity has been established. Both inverse-purity margins, the complete monotone quotient sqrt(2B-1)/B, every directed root and all gap exponential witnesses are independently checked.

The eight required finite windows are:

| Every integer L in | Inverse temperature | Gap lower bound |
|---|---:|---:|
| [8,16] | 177/10 | .050955347995 |
| [16,32] | 177/5 | .037912948253 |
| [32,64] | 354/5 | .031688698317 |
| [64,128] | 708/5 | .029074541844 |
| [128,256] | 1416/5 | .028183345658 |
| [256,512] | 2832/5 | .028108782146 |
| [512,1024] | 5664/5 | .028239866326 |
| [1024,2048] | 11328/5 | .028359368437 |

These bounds cover odd as well as even target L. The even-base purity assumption is not incorrectly extended to odd bases. The interval cursor check verifies no early or intermediate size window is missing.

The independently reconstructed short-size comparison covers every L=2,...,7 uniformly for 0<=g<=.1. The weighted edge-square sums are [16,18,32,50,72,98]. With alpha>=4/5, delta>=delta_lower<=sqrt(3/5), and v<=147/200, it gives

    gap >= delta_lower-(147/200)/(4/5+delta_lower)
         = .30781046655374045... .

The product-singlet Rayleigh upper bound is zero for H'. Uniformity uses monotonicity of this comparison expression, not assumed monotonicity of the physical gap in g.

The small-defect theorem supplies all L>=2048. The minimum of that asymptotic lower bound, six short sizes, and the eight required windows is exactly .027887084487.

A ninth diagnostic window [2048,4096] is also recomputed, but is unnecessary because the asymptotic theorem already starts at 2048. Its fixed 40-decimal interpolation precision produces the smaller bound .019931065555. It must not be included as a required bottleneck, nor used to hide an earlier missing interval. The complete earlier coverage is checked explicitly.

## 6. Reproduction and qualifications

Run bash REPRODUCE.sh. It performs the complete physical, polynomial and scalar replay, then the adversarial tests. Runtime output is under logs/ and machine-readable results under results/. Replays update timing bytes; preserve a sealed copy when comparing the final manifest.

One CPU, one numerical-library thread and a 1 GiB address-space cap are enforced. Resource use and elapsed time appear in results/SUMMARY.json. The adversarial suite checks denominator misnormalization, a forged interpolation checkpoint, the limits of finite fitting alone, incorrect oscillator counts/index/root direction, missing q=6 leakage, wrong beta/base labels, a missing early window, cross-base K reuse, and an inflated final gap. No producer file is mutated by these tests.

The .09 exact selected failures are checked for txy, xty and xyt. The saved finite grid is not rerun here; no all-beta statement is accepted. Nonselected .085 scan paths are preserved for provenance but are outside the accepted selected-five-candidate result. The strongest selected result, its physical input package and every required finite-size bridge are independently accepted.
