# Independent review of whole-spectrum-tail recombinations

Updated 10 October 2026, 14:40 America/New_York (EDT) / 18:40 UTC.

## Verdict and exact scope

**PASS:** all 36 full-band patches and all 35 successful recombinations pass independent exact arithmetic and analytic review. The strongest certified gaps are

| g | Exact lower bound | Initial beta | First asymptotic square side |
|---|---:|---:|---:|
| 0.03 | 0.318085460990 | 259/20 | 8 |
| 0.04 | 0.235117964607 | 47/4 | 8 |
| 0.05 | 0.171822115684 | 199/20 | 16 |
| 0.06 | 0.103487228301 | 203/20 | 16 |

Each bound holds for **every integer square side L >= 2**, with a unique finite-volume ground state. The Hamiltonian is the ordinary spin-1/2 square bilayer, with unit vertical rung exchange, equal positive straight intralayer exchange g in both directions and both layers, and no crossed exchange. Positive-direction periodic bonds retain their multiplicities, including parallel bonds at side two. The four g values are discrete certified points; this review does not certify an interpolating global-gap curve or a continuous-g global lower bound.

These are sufficient lower bounds, not estimates of the actual physical gap, an optimum over temperatures or geometries, or a claim of the maximum provable coupling. No arbitrary-aspect-ratio theorem or uniqueness of all infinite-volume ground states is asserted. The review is not proof-assistant verification.

## 1. Frozen provenance and independent work

The producer freeze is `low_band/tail_comparison/FROZEN_MANIFEST_1834.json`, SHA-256

`ca267779b17e27a109cfc964c3ca6aaf6a5be9ba8cbc84b368e0c3fc0fc082dd`.

Every one of its 56 entries was checked. This review freezes 124 input files, including the three complete recombination families, their ground/Fourier/tail sources, and the short-size bridge sources. `INPUT_SHA256.json` checks their bytes. Existing original and Jacobi outputs were not changed while completing the quadratic family.

All files in the sealed manifests of `large_seed_review`, `temple_variant_review`, `alternative_order_review`, `bosonic_tail_review`, and `quadratic_boson_review`, and all of those reviews' frozen inputs, were independently hash-checked before and after replay. `PRIOR_REVIEW_SHA256.json` records the manifests and entries. Every reused ground-moment, complete translated-band, and tail source matches its prior accepted frozen byte hash. No physical trial state is regenerated or silently substituted.

The previous independent physical reviews already reconstructed complete ground moments and full translated H-images, orthogonality, momentum/spin sector labels, and their residuals. This review reuses those accepted facts by exact hash. It independently re-contracts every stored ground G/K/J quadratic form, rechecks every full-spectrum bin and counting index, recomputes every new Temple endpoint, and rebuilds all trace enclosures, order/basepoint identities, transport, recurrence, and finite-size bridges. Its arithmetic modules execute no producer module or previous review module.

The extracted working directory has no local Git metadata. A local file write does not imply a commit or external publication.

## 2. Two distinct full-spectrum counting constructions

Let N be the number of rungs and K_phys = H + 3N/4. The physical Hilbert dimension is 4^N. For the physical-number comparisons, the shell multiplicities are

m_q = C(N,q) 3^q,  q = 0,...,N.

The preserving-block lower diagonal is (1-2g)q. The original squared off-block bound is

(3g²/4) E_empty,upper(q) E_occupied,upper(q+2).

The bosonic-Jacobi variant takes the minimum of that bound and

(floor(q/2)+1) v + 4g² floor((q+1)²/4),

where v = (3g²/4) sum_e w_e² and w_e is the combined multiplicity of an unordered graph edge. Both entries are bounds on the same physical off-block operator, so this minimum is legitimate. Every graph count, diagonal, off-diagonal square, positive rational LDL pivot in both parity chains, monotonicized bin endpoint, multiplicity and first ordered index is recomputed. These multiplicities sum exactly to 4^N.

The separate quadratic-boson comparison uses D = 3N oscillator modes. Write alpha = 1-2g, delta = sqrt(1-4g), and E_b = -v/(alpha+delta). The sealed theorem gives, in increasing ordered-index convention,

lambda_j(K_phys) >= lambda_j(E_b + delta Q_ref),  1 <= j <= 4^N.

A rational lower root delta_l gives E_l = -v/(alpha+delta_l) and lower endpoints E_l+q delta_l. Every squared root witness and endpoint is rechecked. These reference shells have multiplicities

d_q = C(3N+q-1,q).

Their positive finite sum through q=N contains C(4N,N) reference levels, at least 4^N. It safely overcounts the physical ordered spectrum in a heat-trace upper bound. It is not an assertion that the transformed physical subspace has oscillator number at most N.

**The two multiplicity sequences are never pointwise merged at a common q.** Their first two shells agree, with total 1+3N, but their higher ordered-index breakpoints differ. All three tails are evaluated separately with their own multiplicities.

## 3. Complete low-band identification and endpoint replay

For each of the three tail variants, call its first three ordered-bin lower endpoints a0,a1,a2. They bound lambda_1, lambda_2, and lambda_(2+3N), respectively. The re-contracted singlet trial has exact mean rho and full variance r², with rho < a1. Therefore the unique full ground state belongs to its represented singlet sector.

The accepted translated triplet modes supply N orthogonal momentum sectors, each with spin multiplicity three. Every mode Ritz upper endpoint is below a2. Together with the singlet trial, they supply 1+3N orthogonal states below a2. The full-space ordered count allows at most 1+3N such eigenvalues. Thus these states account for the complete low band, each represented invariant sector contains exactly one level below a2, and every omitted level is at least a2.

Within a represented sector, if theta < a2 is the exact mean and r² >= 0 the complete variance, the rank-one Temple lower endpoint is

theta - r²/(a2-theta).

The ground endpoint is recomputed as an exact fraction. Every triplet endpoint is recomputed independently in Q(sqrt(2)). Each stored 14-decimal rational lower endpoint lies below its exact endpoint and less than one grid cell away, and satisfies the exact Temple margin. No small residual alone is used as a substitute for the complete low-band count.

The patches have 16, 32, and 64 rungs, hence 32, 64, and 128 physical spins. Their complete Hilbert dimensions are 2^32, 2^64, and 2^128. The respective ground search dimensions are 11, 29, and 29, and complete retained band dimensions are 49, 97, and 193. These are different quantities. No MPS bond dimension enters, and the maximum physical spectrum is not diagonalized.

## 4. Independent exact heat bounds and a conservative-rounding nuance

Let u0 be the ground Rayleigh upper endpoint. The retained complete band gives a lower and upper enclosure of Tr exp[-beta(K_phys-u0)]. The upper enclosure adds every positive tail term from q=2 through N, using m_q for either physical-number variant and d_q for the quadratic reference. No positive term is dropped and no interval cancellation is used.

The independent exponential routine first reduces |x| to at most 1/16, encloses the reduced argument on a 384-bit dyadic grid, and evaluates 80 Taylor terms using directed integer lower/upper recurrences. A geometric bound controls all remaining positive terms. Directed repeated squaring, and directed reciprocal bounds for a negative argument, give a rigorous enclosure. This is independent of the producer's 256-bit, degree-70 routine. All physical energy shifts E00+u0 are restored explicitly in partition-function ratios; no assumed extensivity of u0 is used.

For the original and Jacobi families, all saved 16-decimal ratios equal the independent lower-rounded values. Four quadratic x–y–time C0 ratios are **3 or 4 units of 10^-16 smaller** than the independent certified values. Their very large positive oscillator multiplicities amplify the producer's conservative dyadic tail floor enough to affect these final decimal cells. This is a loss of sharpness, not an invalid bound. The review verifies each saved ratio is positive and no greater than its independently certified lower bound, then replays the subsequent certificate using that valid saved witness. All other ratios agree at the saved precision. The best time–x–y certificates are unaffected by this equality nuance.

`results/accepted_certificates.json` stores every independent trace enclosure, ratio witness, rounding difference, transported triple, and accepted final bound. Rational gap acceptance is checked by a direct upper exponential inequality, not a floating logarithm.

## 5. All three orders and correct canonical transport

Put v=(4,4,beta), and let D_x,D_y,D_t double the indicated direction. For the staircase order (i,j,k), let v1=D_i v, v2=D_jD_i v, and v3=D_kD_jD_i v. Exact cancellation gives

J1 = Z(v3)/Z(v)^8,
J2 = Z(v3)^2/Z(v1)^8,
C0 = Z(v3)/Z(v2)^2.

The order-dependent v1 and v2 are retained. `results/path_ledger.json` verifies the formal partition-function monomials and required adjacent-swap identities.

With G(z)=1-(1-z)^2/(2z²), the first cycle supplies conservative lower witnesses

a=G(J1), b=G(J2 a), c=G(C0^4 a² b),

with directed rounding. These belong to the selected ordered staircase at the common post-cycle base (8,8,2beta). They are not automatically canonical merely because the base is square.

For adjacent edges a=P_i(w), b=P_j(D_i w), the swapped edges c=P_j(w), e=P_i(D_j w) satisfy e c²=b a². Since each relevant purity is in (0,1], lower witnesses transform as (a,b) -> (a sqrt(b),a²b). The endpoint after the pair is unchanged, so later edge basepoints remain valid. Consequently:

- x–y–time: (A,B,C)=(a,b,c)
- x–time–y: (A,B,C)=(a,b sqrt(c),b²c)
- time–x–y: (A,B,C)=(a sqrt(b),a²b sqrt(c),a^4 b² c)

Every square root is certified with integer-square-root inequalities and transported values are rounded down to 18 decimal places. Only this canonical x–y–time triple is passed to the canonical recurrence. Time is never relabeled as a spatial coordinate.

## 6. Exact recursion and complete integer-size coverage

The review independently reproduces every three-step defect update and every doubled spatial/temperature basepoint. At the accepted square side n, the maximum common defect u satisfies 0<u<=1/500. The inherited all-integer interpolation theorem gives the asymptotic bound through

exp(beta_accepted d) 32u < 1.

This strict inequality is independently checked at the stored rational d. Acceptance onsets among all 35 certificates are 8, 16, 32, and 64.

For every pre-acceptance dyadic window [n,2n]^2, the two successive signed-transfer interpolation steps are recomputed exactly. The dominant-weight witnesses, tail ratios, spatial bound, intermediate thermal bound and final lower thermal purity agree with the stored rational data. Every proposed window gap d is independently verified by

exp(beta d)(1-C) < C,

where C>1/2 is its certified thermal purity. The final all-L gap is the minimum of the asymptotic certificate and every required finite-window and short-size bridge.

For L=2,...,7, the singlet-product trial has K_phys-energy zero. The rechecked g=.06 number-compression cutoff a1 is positive, giving lambda_2(K_phys)>=a1 and gap>=a1. Its smallest value, at L=7, is 0.583853380272. It exceeds every accepted all-L target.

These same short-size cutoffs apply uniformly to 0<=g<=.06: in the sector-norm comparison, x_q=||psi_q|| is nonnegative; decreasing g increases each lower diagonal and decreases the magnitude of each negative off-diagonal term evaluated on x. The entire comparison is therefore bounded below by the fixed g=.06 quadratic expression on these nonnegative norm vectors. This is a comparison-form argument, **not physical spectral-gap monotonicity in g**, nor an assertion of ordinary matrix Loewner monotonicity for entrywise off-diagonal changes.

Short sizes, every required finite window, and the asymptotic theorem cover all integer L>=2 without omissions. The positive gap and purity bounds also establish finite-volume ground-state uniqueness.

## 7. Same-order comparison and isolated tail gain

Each entry below is an accepted all-L lower bound. The initial beta is optimized only over the producer's bounded proposal grid beta=5,...,30 in steps .05; exact acceptance does not assert grid or global optimality.

| g | Initial order | Original physical tail | Bosonic Jacobi | Quadratic reference |
|---|---|---:|---:|---:|
| .03 | x–y–time | .282017228092 | .284244946351 | .285486569967 |
| .03 | x–time–y | .310415608077 | .310698713746 | .310892154512 |
| .03 | time–x–y | .317881464188 | .317999803724 | .318085460990 |
| .04 | x–y–time | .180632156388 | .186732573140 | .189781926241 |
| .04 | x–time–y | .224253737992 | .225121319141 | .225681371002 |
| .04 | time–x–y | .234445519760 | .234841332964 | .235117964607 |
| .05 | x–y–time | .104475599844 | .120219321470 | .126764478428 |
| .05 | x–time–y | .160779055429 | .161353905979 | .161489014324 |
| .05 | time–x–y | .170554842579 | .171296530205 | .171822115684 |
| .06 | x–y–time | No accepted grid proposal | .037080019126 | .049167163415 |
| .06 | x–time–y | .082067113439 | .087632864832 | .090419443895 |
| .06 | time–x–y | .099555868340 | .101960334497 | .103487228301 |

The missing original .06 x–y–time entry is also independently reproduced as a floating grid diagnostic. It is not an all-beta exclusion or a physical gaplessness claim.

For the best time–x–y order, **all three variants use the same beta at each g**, so their differences isolate the tail/end-point improvement without any change in physical trial moments, seed geometry, order, or temperature:

| g | Common beta | Jacobi minus original | Quadratic minus original | Quadratic minus Jacobi |
|---|---:|---:|---:|---:|
| .03 | 259/20 | .000118339536 | .000203996802 | .000085657266 |
| .04 | 47/4 | .000395813204 | .000672444847 | .000276631643 |
| .05 | 199/20 | .000741687626 | .001267273105 | .000525585479 |
| .06 | 203/20 | .002404466157 | .003931359961 | .001526893804 |

Thus most of the improvement over the older published x–y–time results at .03–.05 comes from the valid order change and canonical transport. The tail improvement is the smaller positive like-for-like difference in this last table. The stronger cutoff also sharpens the Temple lower endpoints, so “tail improvement” includes both its counting bound and its induced endpoint improvement.

## 8. Reproduction and limits

Run `bash REPRODUCE.sh` from any directory. The script first verifies the sealed package, then repeats the independent recombination audit and the separately labeled floating grid diagnostic. It writes only review results and a new replay log, and does not alter producer inputs, the five prior reviews, or any remote state.

All substantive computation is pinned to one available CPU; numerical-library thread counts are one; address space is limited to 1.5 GiB. The audit uses only Python standard-library exact integer/rational arithmetic. Runtime and actual maximum RSS are recorded in `logs/audit.log`.

- `REVIEW_STATUS.json`: accepted model, scope, strongest four bounds and qualifications
- `results/patch_review.json`: 36 complete-band/tail checks and dimensions
- `results/accepted_certificates.json`: all 35 exact trace/transport/recurrence/bridge certificates
- `results/small_sizes.json`: shared L=2,...,7 comparisons and their coupling scope
- `results/path_ledger.json`: exact order/basepoint algebra
- `results/same_order_comparison.json`: all three tail families at all three orders
- `results/fixed_order_fixed_beta_gains.json`: clean same-order, same-beta differences
- `results/grid_no_success_diagnostic.json`: limited floating diagnostic, not an exclusion theorem
- `INPUT_SHA256.json`, `PRIOR_REVIEW_SHA256.json`, `snapshot/`: frozen provenance
- `MANIFEST_SHA256.json`: completed independent review package
