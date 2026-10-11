# Independent acceptance of eight positive-cell robustness certificates

2026-10-11 03:37 UTC / 2026-10-10 23:37 America/New_York (EDT).

## Verdict, model and main nested conclusions

**ACCEPTED.** The Hamiltonian is

    H_M(g) = sum_(j=1)^M [S_(2j-1) · S_(2j) + g S_(2j) · S_(2j+1)],
    S_(2M+1) = S_1,       S_j^2 = 2,

on 2M physical spin-one sites, for every integer M >= 2. The designated first bond family has coefficient exactly one, also when g > 1. The full Hilbert dimension is 3^(2M) = 9^M. All gaps below are in that fixed exchange unit, and each statement includes a unique periodic finite-volume ground state.

The four main, fully closed nested neighborhoods are:

| Exact closed g interval | Gap lower bound | Physical seed / cell seed |
|---|---:|---:|
| [19999/20001, 20001/19999] | 1/50 = .02 | 32 / 16 |
| [99993/100007, 100007/99993] | 3/200 = .015 | 32 / 16 |
| [199983/200017, 200017/199983] | 1/100 = .01 | 32 / 16 |
| [99991/100009, 100009/99991] | 1/200 = .005 | 32 / 16 |

All four hold for **every integer cell count M >= 2**, not only even cells or dyadic lengths. The widest interval is approximately [.9998200161985421, 1.0001800162014581]; its exact fractions define the statement.

Four additional rows independently validate odd cell initializations:

| Physical / cell seed | Eta radius r | Exact closed g interval | Gap |
|---|---:|---|---:|
| 34 / 17 | 69/1000000 | [999931/1000069, 1000069/999931] | .015 |
| 34 / 17 | 89/1000000 | [999911/1000089, 1000089/999911] | .005 |
| 30 / 15 | 1/25000 | [24999/25001, 25001/24999] | .015 |
| 30 / 15 | 7/100000 | [99993/100007, 100007/99993] | .005 |

These also cover every M >= 2, but are dominated as interval/gap summaries by the main rows. They document successful use of the genuine own-length physical60 and68 anchors with odd cell starts15 and17.

The previously accepted .015 and .005 neighborhoods, their files and seals, remain unchanged and valid. These conclusions concern alternating even-physical-length chains. They do not relabel the existing uniform all-physical-integer-length .0248 theorem as a stronger theorem. No optimal radius, actual-gap value, minimal initialization, or phase label is claimed.

Frozen producer manifest: ea050102bb50eea1a287e7e674de0f43aa091a4fcd17a3d8279870f5e26ab529.

## 1. What is independently checked and what is inherited

The producer script and analytic notes were inspected. This review imports no producer module and executes no producer scientific code. It uses independently implemented, higher-precision directed arithmetic to verify all eight exact records, all intermediate states and every stated inequality.

The physical uniform seeds at n30, n32 and n34 were already independently accepted in uniform_smaller_second_initialization_review, manifest 54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. Their accepted physical evidence consists of eighteen uniform I/P thermal inputs at beta_0 = 49/4, lengths4 through12, and their own physical60/64/68 MPS anchors. The thermal-input review manifest is 792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94. No thermal calculation, contraction, new trial state, moment construction or physical matrix is recomputed here.

For each n in {30,32,34}, this checker verifies:

- the producer source certificate is an exact member of its sealed manifest;
- its S and T endpoints exactly equal the independently accepted review endpoints;
- beta_0 is exactly49/4 and the own physical anchor length is2n;
- the accepted integer norm N0_(2n) is positive;
- R_(2n) = H0_(2n)/N0_(2n) + 2n(700741/500000) equals every stored Rayleigh value and is strictly negative.

H0 is already the total periodic energy numerator. Multiplication by an additional2n is neither done nor allowed. Each trial span has dimension one and MPS bond dimension26; the norm-transfer dimension676 is distinct from the physical dimensions3^60,3^64,3^68.

All source proofs and their exact scope remain inherited evidence. Matching source bytes does not itself prove the physics; the new analytic composition below is independently justified, while the earlier physical audits supply the fixed input premises.

## 2. Fixed finite perturbation transport and physical units

Let L = 2M, h_j = S_j · S_(j+1), H_0,L = sum_j h_j and

    B_L = sum_(j odd) h_j - sum_(j even) h_j,
    eta = (1-g)/(1+g),       c = (1+g)/2 = 1/(1+eta).

Then H_M(g) = c(H_0,L + eta B_L). For |eta| <= r < 1,

    g in [(1-r)/(1+r), (1+r)/(1-r)],
    1/(1+r) <= c <= 1/(1-r).

The local h spectrum is {-2,-1,1}; centering it by I/2 gives norm3/2. Its alternating constants cancel, so ||B_L|| <= 3L/2.

For the untwisted uniform even ring, one-site translation fixes H_0,L and reverses B_L. Thus the uniform Gibbs expectation of B_L is zero. The Gibbs variational lower bound and Golden–Thompson upper bound, followed by the spectral chord bound for exp(-beta eta B_L), give

    1 <= Z_eta,L(beta)/Z_0,L(beta)
      <= cosh(3 beta eta L/2)
      <= exp[(9/8)(beta L r)^2].                              (1)

The scalar shift a = 700741/500000 per physical site is common to these normalized traces. In physical units the shifted Hamiltonian is H_M(g) + c a L I, and actual inverse temperature is tau = beta/c = beta(1+eta). Therefore

    Z_g,M(beta/c) = Z_eta,2M(beta).

The shift cancels in S and T and does not change the gap. No translation identity is applied to a pi-seam trace; those traces are used only inside the already accepted uniform seed.

For physical seed n with accepted endpoints s_0,t_0, let m = n/2 be the cell seed and A_n = (9/8)(beta_0 n r)^2. Applying (1) only at fixed physical lengths n and2n yields

    S_g(m,beta_0/c) >= s_0 exp(-2A_n),
    T_g(2m,beta_0/c) >= t_0 exp(-8A_n).                       (2)

The factor8 includes A_(2n) = 4A_n and the squared denominator. All source length/temperature labels and both exact losses are checked separately for each row. The periodic MPS is exactly translation invariant by cyclicity of its trace amplitudes, so its staggered expectation also vanishes; its physical shifted Rayleigh is c R_(2n), consistent with the unchanged variational numerator at beta_0/c.

The L^2 perturbation loss is used only at these finite inputs. No growing-volume perturbation loss is subtracted from an infinite-volume gap.

## 3. Positive physical cell transfer and the improved window

The independent structural review, manifest abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872, is fully pinned and retained. Its actual factorization is as follows.

In a single-site Cartesian spin-one basis, C^alpha = i S^alpha is real and -S·S = sum_alpha C^alpha tensor C^alpha. A raw history measure mu_J on ordered component-labeled events has mass exp(3J tau) for J >= 0. The single-site merged chronological trace k(x,u) is real, symmetric in its two input histories, and bounded by3. Define A_g:L²(mu_g)->L²(mu_1) with kernel k. It is Hilbert–Schmidt. Its correct adjoint uses the two distinct measures and complex conjugation, giving

    K_g(x,y) = integral k(x,u) k(u,y) d mu_g(u) = (A_g A_g*)(x,y).

Thus K_g is positive trace class. Absolute convergence of the full finite-volume Dyson expansion permits grouping g bonds into two-spin cells, so the same operator obeys

    Z_g,M(tau) = Tr X_g,tau^M                       for every integer M >= 2,

where X is K multiplied by the positive scalar accounting for the cell shift. This is not an unsupported product-of-self-adjoint-transfers argument. It applies at all finite positive g in these neighborhoods, and the structural theorem includes g=0. It does not assert the same positivity for an arbitrary symmetric cell perturbation.

For any integer base m >= 2, X_tau^m is positive trace class. Define

    S(m,tau) = Z_(2m)(tau)/Z_m(tau)^2,
    T(M,tau) = Z_M(2tau)/Z_M(tau)^2.

Both are purities in (0,1]. No even-cell restriction remains.

For m <= M <= 2m, write p = M/m in [1,2]. Nonnegative-spectrum norm monotonicity gives

    Z_M(2tau) >= Z_(2m)(2tau)^(p/2),

while Holder interpolation gives

    Z_M(tau) <= Z_m(tau)^(2-p) Z_(2m)(tau)^(p-1).

The spectra are countable and all powers here are summable; these inequalities follow from their finite-sequence forms by monotone limits. Division and exact cancellation yield

    T(M,tau) >= S(m,tau)^(2-p) T(2m,tau)^(p/2).

The logarithm is affine in p, so certified lower endpoints s,t supply

    T(M,tau) >= C = min(s sqrt(t), t).                        (3)

There is no inverse-purity gate s²t > 1/2 in this interpolation, no signed tail to subtract and no dominant-eigenvalue construction. The arithmetic checker uses an independent lower square-root enclosure to bound (3). It does not infer parity eligibility from scalar success alone.

A purity lower bound C > 1/2 proves uniqueness of the largest Gibbs weight and bounds its next-to-largest ratio by (1-C)/C. The directed test

    C - upper_exp[beta_j(1+r)D](1-C) > 0                     (4)

therefore proves the gap D in physical units on every cell integer in that window. Here beta_j = 2^j beta_0 and the actual tau_j = beta_j(1+eta) is at most beta_j(1+r).

## 4. Sequential recurrence, late closure and complete windows

For a probability sequence, normalizing its squares gives purity at least

    G(z) = 1 - (1-z)^2/(2z²),

an increasing function on (0,1]. Exact trace identities and S,T <= 1 imply the sequential update

    S_new = G(S² T),       T_new = G(T² S_new),
    (m,tau) -> (2m,2tau).                                  (5)

The thermal update must use the new S. Every input and accepted output is checked in (0,1]. In addition to checking conservative inequality directions, the reviewer reproduces the producer's exact120-decimal grid recurrence: its stored K is precisely floor_120(S²T), its next S is floor_120(G(K)), and its next T is floor_120(G(floor_120(T² S_new))). No positivity or legal-domain check is omitted at odd starts.

Once u = max(1-S,1-T) <= .01, both updated defects are at most5u². Indeed, the first pre-squaring defect is at most3u; the coefficient9/[2(1-3u)²] is below5 at u=.01. The second pre-squaring defect is at most2u+5u² <=3u. These rational domain inequalities are independently rechecked.

The positive window gives C >= (1-u)^(3/2) >= 1-3u/2, hence a next-to-largest Gibbs ratio at most2u. At all subsequent exact updates,

    u_j <= (5u)^(2^j)/5,       tau_j = 2^j tau.

Therefore the conservative terminal test

    5u upper_exp[beta_j(1+r)D] < 1                           (6)

proves the same gap at every larger cell size through the successive dyadic windows. Finite-precision iteration is used only to reach a successful terminal state. It is not iterated indefinitely through a rounding floor.

The independently checked closure data are:

| Physical / cell seed | Radius | Gap | Number of windows | Tail begins at cell | Normalized terminal beta | Terminal margin, display |
|---|---:|---:|---:|---:|---:|---:|
| 32 / 16 | 1/20000 | .02 | 9 | 4096 | 3136 | .3150123701 |
| 32 / 16 | 7/100000 | .015 | 8 | 2048 | 1568 | .2104613542 |
| 32 / 16 | 17/200000 | .01 | 11 | 16384 | 12544 | .5743910556 |
| 32 / 16 | 9/100000 | .005 | 7 | 1024 | 784 | .6824822822 |
| 34 / 17 | 69/1000000 | .015 | 9 | 4352 | 3136 | .0707896126 |
| 34 / 17 | 89/1000000 | .005 | 8 | 2176 | 1568 | .1462357361 |
| 30 / 15 | 1/25000 | .015 | 11 | 15360 | 12544 | .00866684945 |
| 30 / 15 | 7/100000 | .005 | 7 | 960 | 784 | .6241500994 |

Each row has consecutive windows [m2^j,m2^(j+1)] from its own initial m through the listed terminal base, with the terminal window also checked. Every exponent, coordinate, physical length and margin is stored in results.json. In total, all70 windows pass.

The most precision-sensitive accepted row is physical30/cell15, r=1/25000 and D=.015. Its terminal defect is approximately3.77686303836e-83 at normalized beta12544. It cannot be verified using a defect floor1e-60. The final120-decimal source endpoints remain strictly below1 and pass the directed terminal inequality. The reviewer uses a600-bit binary grid, approximately180 decimal digits, and checks the entire path without replacing tiny defects by zero or relying on displayed floats. Its terminal margin is still above .00866.

## 5. Finite bridges and exact interval endpoints

The accepted uniform theorem supplies delta_0 = 31/1250 at the finite even physical lengths needed below the cell seed. For every such fixed length L,

    gap(H_0,L + eta B_L) >= delta_0 - 2|eta| ||B_L||
                         >= delta_0 - 3Lr.

The bracket remains positive. Scaling by c and using c >= 1/(1+r) gives, for physical seed n,

    gap(H_M(g)) >= [31/1250 - 3(n-2)r]/(1+r),
    2 <= M <= n/2 - 1.                                    (7)

The exact bridge lower bounds are recorded per row, with displayed values:

- n32 main rows: .02029898505, .01849870509, .01714854237 and .01669849714.
- n34 rows: .01817474594 and .01625455334.
- n30 rows: .02143914243 and .01891867569.

All exceed their targets strictly. The .02 row has the smallest bridge slack, approximately .00029898505, which is checked as an exact rational difference. These bridges cover cells2..15,2..16,2..14 for starts16,17,15 respectively, without a missing final short cell.

The checker does not merely trust the all-size gap label: it retrieves the actual accepted uniform purity endpoint for every even physical length4,6,...,32 and rechecks its .0248 gap inequality at beta49/4. It preserves each endpoint's accepted source construction, including the physical24 parity/MPS48 numerator. No nonexistent own24 anchor is inserted. Historical physical25 resource exceptions are unchanged and are not needed for this even-size bridge.

Every row separately verifies the exact endpoint conversion g_lower=(1-r)/(1+r), g_upper=(1+r)/(1-r). All claims include equality at both ends. The finite bridge joins the first cell window exactly; (6) covers the remainder. Positive ordered gaps include ground-state uniqueness throughout the interval. Weyl is never applied with unbounded volume.

## 6. Directed arithmetic, adversarial checks and provenance

The independent exponential enclosure uses a600-bit binary outward grid,112 positive Taylor terms after reduction to argument at most1/4, a first-omitted-term geometric remainder, and outward repeated squaring. This differs from the source's120-decimal grid,100 terms and1/16 reduction. Negative exponentials are bounded by reciprocal intervals. Roots use exact integer square brackets. All decisions are rational; floats appear only as labeled displays.

The reviewer verifies every saved lower seed, every source endpoint, exact recurrence grid value, window purity and positive margin. The precision is sufficient to distinguish the final120-digit endpoints and the late1e-83 defect from zero. Twenty-two adversarial corruptions are rejected, including wrong odd-cell starts, physical/cell or anchor confusion, omitted c scaling, missing windows, illegal/inflated updates, false late defects, rounding the last purity to one, substituting a60-digit floor, and finite-bridge holes or omitted perturbation loss.

The frozen snapshot contains198 files,10,577,706 bytes. All snapshot bytes and all182 producer-consumed input hashes are checked. Eight complete source/producer manifests and their183 member entries are verified, including all prior interval and structural review members. This is a complete member check for these selected packages; it is not a fresh physical recomputation or a re-audit of every underlying scientific dependency.

The preliminary60-digit mixed-result certificate and logs remain sealed as diagnostics. Their failed rows are not promoted, erased or interpreted as no-go theorems. The final n34/.015 radius is69/1000000; the wider earlier n34 proposal7/100000 is not silently certified. The same radius7/100000 is independently certified with the separate n32 seed. Numerical equality of radius does not permit substituting a different seed's proof.

The one accepted independent scalar run used .568265435 process CPU seconds, .570589311 monotonic wall seconds and15,300 KiB peak RSS, with hard limits30 CPU seconds/256 MiB and one-CPU affinity. No physical contraction, thermal campaign or eigensolver was run. Producer historical measurements and the conservative4-CPU-second preliminary charge are preserved as reported provenance; the independent timing measures this review's own run.

No root documentation, existing accepted file, producer record, earlier seal or remote state was changed. Reproduce with `python audit.py` in a disposable copy of this review folder: it needs only the included snapshot and writes local results. This is an exact-arithmetic mathematical certificate, not formal proof-assistant verification.
