# Complete the finite prefix: every integer length L >= 2

2026-10-10 22:44 EDT / 2026-10-11 02:44 UTC. Exact producer certificate; independent finite-prefix review pending.

## Result and what changed

For the uniform periodic spin-one Heisenberg chain with unit bilinear exchange and the usual periodic bond convention, every integer length L >= 2 has a unique ground state and gap at least 23/10000 = .0023, subject to independent review of this new finite prefix.

This combines three separately identified parts:

1. L = 2,3: elementary total-spin algebra, with gaps 2 and 1.
2. Every L = 4,...,23: a fresh own-length D26 MPS Rayleigh numerator and an exact certified thermal-trace upper bound, all evaluated at beta0 = 49/4.
3. Every L >= 24: the previously frozen direct25/parity24/coverage26/bootstrap30 chain.

All twenty finite direct tests pass. There are no unfilled integer lengths. The canonical bootstrap initialization remains 30. This is a completion of finite-size coverage, not a new bootstrap initialization at 2 and not a minimum-seed theorem. The stronger nested bounds .0179 for L >= 28, .0245 for L >= 32 and .0248 for L >= 34 remain intact.

The weakest purity among the twenty new direct tests is approximately .8604973284 at L = 17, still well above 1/2. The comparatively small common gap .0023 is inherited from the existing coverage chain, not optimized over the new finite prefix.

## Hamiltonian and the two analytic lengths

The normalization is explicitly pinned in audit/APPENDIX_A_BRIDGE.md:

    H_L = sum over j of S_j dot S_(j+1), with periodic indices,
    S_j squared = 2, and L = 2 counting both periodic bonds.

At L = 2, H_2 = 2 S_1 dot S_2 = S_total squared - 4. Total spin j = 0,1,2 gives energies -4,-2,2. The singlet occurs once, so the ground state is unique and the gap is 2.

At L = 3, each pair occurs once and H_3 = (S_total squared - 6)/2. Total spins 0,1,2,3 have energies -3,-2,0,3. The total singlet occurs exactly once: only the intermediate j12 = 1 from coupling the first two spin-one sites can couple with the third spin one to total zero, and j12 = 1 itself occurs once. Thus the gap is 1 and the ground state is unique. These finite algebraic facts do not require the transfer identity below its original length-4 domain.

## Own-length trial numerators

For each L = 4,...,23 the batch contracts the unchanged physical D26 tensors via the already audited norm transfer T and two-site Heisenberg insertion O:

    N0_L = Tr(T^L) > 0,
    H0_L = L Tr(T^(L-2) O),
    R_L = H0_L/N0_L + aL, a = 700741/500000.

H0_L/N0_L is total energy. Every output is its own length's exact integer pair; no nearby even-length quotient is reused at an odd size. The physical Hilbert dimension is 3^L, MPS bond dimension is 26, and only one trial state is retained for each numerator. No ED, thermal matrix rebuild, tensor optimization, rank assumption or larger bond dimension is used.

For the normalized physical trial, Jensen gives

    Z_L(2 beta0) >= exp(-2 beta0 R_L).

Several odd-length shifted Rayleigh energies are positive. Their signs do not invalidate Jensen and are never silently replaced by a negative-anchor assumption. Exact Rayleigh fractions and positive norms appear in certificate.json.

## Exact denominators at physical lengths 4,...,12

The nine untwisted identity-seam upper bounds are read directly from the fully reviewed18-input provenance mapping in uniform_second_thermal_full_review/provenance_results.json. Each selected case is explicitly Lk_I, never the pi-twisted P value. The final-review manifest is checked against 792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94.

These are the exact refined outward rational intervals mapped to the independently reproduced physical integer totals/error analysis. The code verifies all nine lengths are present and the review declares all18 totals/endpoints matched. It does not infer a physical untwisted trace from a pi seam or from a falsely unsigned odd sector.

## Longer signed moments and lengths 13,...,23

The accepted self-adjoint history-transfer spectrum has J and N multiplicity-space sectors with full physical trace J + 3N. Its signed moments 4,...,12 and four signed support caps are inherited unchanged from the independently reviewed second-moment optimization.

This package adds rational polynomial majorants at k = 13,14,15,17,19,21,23 for both sectors. For each sector interval, certify_long.py proves

    p(x) - x^(k-4) >= 0

by exact Bernstein coefficients and recursively bisected exact de Casteljau intervals. Multiplication by x^4 and summation gives an upper bound on the signed kth moment. Coefficient signs select the correct lower or upper input moment endpoint. The target power is odd for the odd k cases, and its sign is retained throughout. In particular, the proved N upper bounds at 13,15,17,19,21,23 are negative; they are valid signed traces, not impossible negative absolute masses.

Floating LP and scalar minimization propose coefficients only. Every accepted polynomial has an exact whole-interval certificate; a sampled grid is not used as a proof. The previously sealed even-length majorants cover 16,18,20,22 and24. Twelfth-moment packing remains a valid fallback. At odd lengths, Cauchy–Schwarz gives the optional independent upper bound Z_L <= sqrt(Z_(L-1) Z_(L+1)); the final code compares safe bounds rather than assuming either is always sharper. All accepted odd lengths in this batch select the new signed-polynomial upper bound, which retains substantial cancellation.

The transfer identity is used only at lengths at least4. No finite transfer rank, unit-weight count inferred from a relaxation, or realization of a moment optimizer is assumed.

## Exact purity and gap checks

Let Q_L be the selected strictly positive upper trace. The checker computes

    C_L = lower_exp(-2 beta0 R_L) / Q_L squared,

with exact rational outward rounding. Integer-root bisection and explicitly bounded Taylor remainders provide directed powers/exponentials. It checks C_L <= 1 as a consistency test and, for each L = 4,...,23,

    C_L > 1/2,
    C_L - upper_exp(beta0 * .0023) (1-C_L) > 0.

These inequalities imply a unique largest Gibbs weight, hence unique physical ground state, and the claimed gap. Each exact fraction, trace method and positive margin is saved. All twenty entries pass; failed_bound_lengths is empty.

The predecessor direct25 producer manifest is abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa. Its mathematical independent review is a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9. That review separately recorded an unresolved resource-accounting anomaly in its own25 contraction. This new batch does not overwrite or cure that historical anomaly, and mathematical acceptance must not be described as resource clearance for that different run.

## Resource controls and observed measurements

The small-power C++ engine shares exact powers T,T^2,T^4,T^8,T^16 across all twenty requested lengths. Since max(L-2) = 21, no higher powers are needed. Matrix multiplication and insertion rules are unchanged; the source restricts accepted lengths to4..23. Truncating unnecessary powers is not truncating the state or spectrum.

This batch had a separate authorized30CPU-second/100MiB limit. Before launch, a self-test verified:

- hard and soft CPU limits both30, and address-space limits both104857600 bytes;
- one process on CPU5, no BLAS or worker threads;
- SIGXCPU default and unblocked;
- verified Linux parent-death SIGKILL;
- a separate process group/session;
- external30-second wall watchdog with process-group cleanup;
- independent wait4 user/system CPU and peak RSS collection, distinct from the program's own clock.

The C++ program rechecks setrlimit/getrlimit and logs the exact limits before any contraction. The launcher has no automatic retry. Build work is separate, under the authorized CPU2/512MiB/30CPU-second allowance. The guarded build had an unusually long observed wall wait; no duplicate build or bypassed physical launcher was started.

Observed physical batch results, all successful:

- external monotonic wall:6.824680186 seconds;
- wait4 user CPU:6.705690 seconds;
- wait4 system CPU:.077379 seconds;
- wait4 total CPU:6.783069 seconds;
- program CPU timer:6.775790 seconds;
- wait4 peak RSS:14772KiB; program peak RSS:14644KiB;
- exit0; wall watchdog did not fire.

These independent measurements are mutually consistent and below the authorized limits. They are recorded in guard_resources.json and anchors.log without equating the two timer definitions. The guard-only self-test did no physical contraction.

Cached LP proposals used.936CPU seconds; exact signed majorants3.145CPU seconds; final scalar/analytic composition5.037CPU seconds and about11MiB. Each cached stage is CPU2 with a30CPU-second/256MiB hard cap. No new thermal job or remote change was made.

## Reproduction and status

Preserve this package and all predecessor seals. In a disposable copy, run search.py only if regenerating proposals is desired, then certify_long.py and certify.py. Fresh physical reproduction requires separately compiling contract_small.cpp under the build allowance and using run_guarded.py; it deliberately refuses automatic repetition once guard_resources.json exists. A reviewer should use a fresh output directory or independently implemented engine and preserve its own guard/accounting logs rather than deleting the original run record.

INPUT_SHA256.json pins consumed physical inputs, signed moments, trial blocks and predecessor coverage. MANIFEST_SHA256.json and SEAL.json freeze this package. Independent reconstruction of the new own-length trials, odd signed majorants, finite gap inequalities and analytic L2/L3 normalization remains the next acceptance step.
