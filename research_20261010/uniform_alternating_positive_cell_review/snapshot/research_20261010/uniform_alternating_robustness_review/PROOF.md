# Independent review: a closed near-uniform alternating-chain neighborhood

2026-10-11 03:19 UTC / 2026-10-10 23:19 America/New_York (EDT).

## Verdict and exact model

**ACCEPTED.** For every integer M >= 2, let

    H_M(g) = sum_(j=1)^M [S_(2j-1) · S_(2j) + g S_(2j) · S_(2j+1)],
    S_(2M+1) = S_1,       S_j^2 = 2.

There are L = 2M physical spin-one sites and Hilbert-space dimension 3^(2M) = 9^M. The coefficient on the designated first family of bonds is exactly one, even for g > 1. In these units:

- On the entire closed interval [19999/20001, 20001/19999], the ground state is unique and the gap is at least 3/200 = .015 for every integer M >= 2.
- On the entire closed interval [12499/12501, 12501/12499], the ground state is unique and the gap is at least 1/200 = .005 for every integer M >= 2.

The second interval contains the first. The endpoints and gaps are rational, not decimal approximations. No phase label, actual-gap estimate, maximal-neighborhood statement, or optimality result is asserted.

The frozen producer manifest is 836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd. This review supplies an independently reconstructed physical cell kernel, analytic comparison and all-size composition, plus independently implemented directed scalar checks. It imports no producer code. Existing accepted physical thermal and MPS evidence is inherited, with its exact source members and claimed quantities checked; it is not physically recomputed here.

## 1. Even-ring normalization and finite trace comparison

Write h_j = S_j · S_(j+1), H_0,L = sum_j h_j and

    B_L = sum_(j odd) h_j - sum_(j even) h_j,
    c = (1+g)/2,       eta = (1-g)/(1+g).

Then H_M(g) = c(H_0,L + eta B_L), with c = 1/(1+eta). If |eta| <= r < 1, then

    (1-r)/(1+r) <= g <= (1+r)/(1-r),
    1/(1+r) <= c <= 1/(1-r).

The two-spin spin-one bond eigenvalues are -2, -1 and 1. Consequently ||h_j + I/2|| = 3/2. Equal numbers of positive and negative bonds cancel the scalar parts of B_L, giving

    ||B_L|| <= 3L/2.

This is a triangle-inequality bound and makes no commutativity assumption. At M = 2 there are four distinct physical bonds, with two coefficients one and two coefficients g. There is no M = 1 claim.

Set a = 700741/500000 and retain the accepted shift per physical site:

    Z_eta,L(beta) = Tr exp[-beta(H_0,L + eta B_L + aL I)],
    Z_g,M(tau) = Tr exp[-tau(H_M(g) + c a L I)].

For tau = beta/c, these traces are equal. The shift is linear in M, so it cancels in all spatial and thermal purity ratios and does not change the gap. In particular, the fixed normalized temperature beta_0 = 49/4 corresponds to the actual physical inverse temperature tau_0 = (49/4)(1+eta).

One-site translation U of an even, **untwisted** ring fixes H_0,L and sends B_L to -B_L. Thus the uniform Gibbs state rho_0 has Tr(rho_0 B_L) = 0. The Gibbs variational principle gives Z_eta,L >= Z_0,L. Alternatively, the trace exponential is a convex function of eta and is even under eta -> -eta, so its minimum is at zero. Convexity is valid for noncommuting matrices: the second derivative has a Duhamel integral whose spectral-basis terms are positive coefficients times squared matrix elements.

Golden–Thompson has the required upper direction:

    Z_eta,L(beta) / Z_0,L(beta)
        <= Tr[rho_0 exp(-beta eta B_L)].

For a self-adjoint operator B with spectrum in [-b,b], scalar convexity and functional calculus give

    exp(t B) <= cosh(tb) I + [sinh(tb)/b] B.

Taking its expectation in rho_0 removes the linear term. Finally, cosh(x) <= exp(x^2/2), since log cosh(x) has derivative tanh(x) <= x for x >= 0 and both sides are even. Therefore

    1 <= Z_eta,L(beta)/Z_0,L(beta)
      <= cosh(3 beta eta L/2)
      <= exp[9 beta^2 r^2 L^2 / 8].                         (1)

The use of the spectral measure is legitimate even when rho_0 and B do not commute: Tr(rho_0 P_lambda) are nonnegative probabilities with the stated mean. Neither the lower bound nor translation symmetry is assigned to a twisted trace. The I/P seam data enter only the previously accepted **uniform** seed derivation.

## 2. A direct physical cell-history kernel

The product of two self-adjoint operators need not be self-adjoint. Such a product argument would not prove the needed hypothesis and is not used.

Group the g bonds into cells C_j = (2j, 2j+1), with periodic indices. The unit bonds connect the right spin of C_j to the left spin of C_(j+1). The cell Hamiltonian, including the shift, is

    v = g S_L · S_R + 2 c a I.

This is the same v in every cell. It is Hermitian, is invariant under the cell swap F and under cell time reversal Theta_1 tensor Theta_1. For spin one one can use the real Cartesian time-reversal basis. Equivalently, the square of cell time reversal is +1, so there is a basis in which it acts as complex conjugation. In that basis:

- v is real symmetric;
- each spin component is purely imaginary and Hermitian;
- C_L^alpha = i S_L^alpha and C_R^alpha = i S_R^alpha are real skew-symmetric matrices of norm one;
- F is a real orthogonal swap, F v F = v and F C_L^alpha F = C_R^alpha.

On an intercell bond,

    -S_R · S_L = sum_alpha C_R^alpha tensor C_L^alpha.

Expand the exponential by Duhamel around sum_j v_j. For each bond, a history is a finite ordered list 0 < t_1 < ... < t_k < tau of component labels alpha in {1,2,3}. Counting labels and integrating the simplex gives positive measure mass

    sum_(k>=0) (3 tau)^k/k! = exp(3 tau).

For a cell with left history xi and right history zeta, merge the events in time order, place exp(-Delta t v) between consecutive insertions, and trace the resulting local product. Call this real-valued kernel k(xi,zeta). The products remain in chronological order. Conjugating the entire product by F exchanges all left and right insertions and fixes every exponential, so

    k(xi,zeta) = k(zeta,xi).

This argument does not reverse a noncommuting product. Time coincidences have zero product measure unless there are no events, which causes no ambiguity. Since each insertion has norm at most one,

    |k(xi,zeta)| <= 9 exp(tau ||v||).

The kernel is bounded on a finite measure space and therefore defines a real self-adjoint Hilbert–Schmidt operator X_g,tau. For every fixed finite M, absolute convergence of the finite-dimensional Duhamel series permits regrouping by bond and cell. Its cyclic integral is the physical trace, hence

    Z_g,M(tau) = Tr X_g,tau^M                 for every integer M >= 2.    (2)

For M = 2 the two intercell bonds are distinct physical bonds. The same operator X_g,tau works for all M. As a Hilbert–Schmidt self-adjoint operator, it is compact, has a real l^2 eigenvalue sequence, and its powers M >= 2 are trace class. The cyclic integral equals the corresponding absolutely convergent eigenvalue-power sum.

This construction works for each finite g and tau in the claimed intervals. Its proof never uses width(v) <= .03. That old width condition controlled an analytic **dimer seed**, not boundedness, symmetry or existence of this kernel. We also do not claim a nonnegative spectrum, an entrywise-positive kernel, or a separate unproved reflection-positivity theorem.

## 3. Reusing the exact uniform seed

The accepted uniform seed has physical n = 32 and anchor length 64, at beta_0 = 49/4. The full physically accepted inputs are the eighteen uniform thermal traces at lengths 4 through 12, at identity and pi seams, with the shift a. Their signed-moment and support argument supplies the exact rational endpoints

    Z_0,64(beta_0)/Z_0,32(beta_0)^2 >= s_0,
    Z_0,64(2 beta_0)/Z_0,64(beta_0)^2 >= t_0,

where the displayed values are s_0 approximately .9301225504257616 and t_0 approximately .8419036295805096. The exact values in results and snapshot, not these displays, are used.

The independently accepted seed reviewer gives precisely the same s_0 and t_0 as the source producer. This review verifies both equalities, the consumed certificate's membership in its sealed manifest, and its beta/length labels. It also recomputes from the accepted integers

    R_64 = H0_64/N0_64 + 64a < 0,

where N0_64 > 0 and H0_64 is already the **total** periodic energy numerator. The negative value is approximately -9.283946501609371e-6. It is not multiplied by 64 again.

The fixed periodic MPS amplitude is Tr(A_s1 ... A_s64), using the same tensor at every site. Cyclicity proves U psi = psi exactly, hence its staggered expectation vanishes. Its shifted alternating Rayleigh value is c R_64, and at tau_0 = beta_0/c the variational exponential numerator is unchanged. This provides a separate consistency check on the unchanged numerator; no new tensor contraction is needed for the perturbation step.

The trial span is one-dimensional, its MPS bond dimension is 26, the norm transfer has dimension 676, and the physical anchor space has dimension 3^64. The physical history transfer need not have finite rank.

Let A_32 = 9(beta_0 r 32)^2/8. Applying (1) to the actual **untwisted** ratios, at normalized lengths 32 and 64 and required temperatures beta_0 or 2 beta_0, gives

    S_g(16,tau_0) >= s_0 exp(-2 A_32),
    T_g(32,tau_0) >= t_0 exp(-8 A_32).                         (3)

For the second line A_64 = 4 A_32 and the denominator is squared. The physical 32-site seed is cell n = 16, while its 64-site thermal endpoint is cell 2n = 32. No twisted perturbation or alternative sector identification is introduced. Bounds (1) are used only at these fixed finite input sizes. Subsequent growing volumes use (2), not an extensive perturbation estimate.

## 4. Canonical recurrence and all integer windows

Define physical ratios

    S(n,tau) = Z_(2n)(tau)/Z_n(tau)^2,
    T(m,tau) = Z_m(2tau)/Z_m(tau)^2.

For even n, the normalized eigenvalues of X_tau^n are a probability sequence, so S(n,tau) <= 1. Physical Gibbs states likewise have T <= 1.

For a probability sequence with purity P, normalizing its squares yields purity at least

    G(P) = 1 - (1-P)^2/(2 P^2).

Indeed, P^2 - sum_i p_i^4 = 2 sum_(i<j) p_i^2 p_j^2 <= (1-P)^2/2. Since G is increasing on (0,1], lower endpoints may be used.

The exact identity

    S(n,2tau) T(n,tau)^2 = S(n,tau)^2 T(2n,tau)

and T(n,tau) <= 1 first give the spatial argument S^2 T. Spatial squaring then gives S_new = G(S^2 T) at (2n,2tau). Next,

    T(4n,tau) >= S(2n,2tau) T(2n,tau)^2,

because S(2n,tau) <= 1. Thermal squaring gives T_new = G(T^2 S_new), at thermal endpoint 4n and temperature 2tau. Thus the legal sequential update is

    S_new = G(S^2 T),       T_new = G(T^2 S_new),
    n_new = 2n,            tau_new = 2tau.                    (4)

The second update uses the **new** spatial bound. All arguments, endpoints and cell/temperature labels are independently checked.

For a finite integer window, let K = S^2 T > 1/2 and

    w = (1+sqrt(2K-1))/2,       rho = (1-w)/w,
    d = T/(1+rho^2),
    C = (1-rho) min(S sqrt(d), d).                            (5)

Then T(M,tau) >= C for every integer n <= M <= 2n, including odd M. Here is the signed-spectrum justification. The n-th powers of eigenvalues of Y = X_(2tau) form a probability distribution with purity at least K. Its largest weight is unique and at least w > 1/2. The corresponding eigenvalue mu_0 is the unique largest-modulus eigenvalue. It must be positive: compactness and the l^n summability imply that all other relative M-th powers tend to zero, while a negative mu_0 would make sufficiently large odd traces negative. Equation (2) gives strictly positive physical traces also for odd cell lengths, excluding that possibility.

The relative n-th absolute tail is at most rho. Therefore the relative 2n-th tail is at most rho^2 and the relative M-th tail for M >= n is at most rho^(M/n) <= rho. For t = M/(2n) in [1/2,1],

    Z_M(2tau) >= [Z_(2n)(2tau)/(1+rho^2)]^t (1-rho).

Absolute-spectrum Holder interpolation at the even endpoints n and 2n gives

    0 < Z_M(tau) <= Z_n(tau)^(2-2t) Z_(2n)(tau)^(2t-1).

Dividing and canceling yields T(M,tau) >= (1-rho) S^(2-2t) d^t. The logarithm is affine in t, so its minimum is exactly the lesser endpoint factor in (5). This proves (5) without transfer-spectrum positivity, odd-power substitution or monotonicity of physical purity in size.

All factors in (5) increase with S and T; a downward square-root approximation reduces the bound safely. If C > 1/2, the largest Gibbs weight is at least C, so it is unique and the ratio of the next weight to it is at most (1-C)/C. Hence the strict directed test

    C - exp(tau_upper D)(1-C) > 0                            (6)

proves a unique ground state and gap at least D. At round j,

    tau = 2^j beta_0(1+eta) <= 2^j beta_0(1+r) = tau_upper.

This correctly tests the gap in the designated unit-exchange physical Hamiltonian, not in a differently normalized one.

## 5. Small-defect closure, with constants checked analytically

When S,T >= 1-u with u <= 1/100, the two updates in (4) obey u_new <= 5u^2. For the first update, 1-K <= 3u-3u^2+u^3 and K >= (1-u)^3; for the second, its defect argument is at most 2u+5u^2. Substitution into 1-G and bounding the coefficients at u = 1/100 proves both estimates. The independent checker verifies the exact rational endpoint inequalities.

The all-integer window then has purity at least 1-4u. One explicit elementary derivation from (5) is as follows. Since K >= (1-u)^3,

    sqrt(2K-1) >= 1 - 16u/5,

because the squared difference is u[2/5 - (106/25)u - 2u^2] >= 0 in the stated range. Thus rho <= (8u/5)/(1-8u/5) <= 5u/3. Since d >= (1-u)/(1+rho^2), sqrt(d) >= d, and S >= 1-u,

    C >= (1-5u/3)(1-u)^2/(1+25u^2/9) >= 1-4u.

After putting the last inequality over its positive denominator, the numerator difference is u/3 + 14u^2/9 + 85u^3/9 >= 0. Also 4u/(1-4u) <= 5u. Thus a terminal state satisfying

    5u exp(tau_upper D) < 1                                  (7)

proves the target gap throughout that state’s window.

Under arbitrary further exact updates, u_j <= (5u)^(2^j)/5 and tau_upper,j = 2^j tau_upper. Accordingly 5u_j exp(tau_upper,j D) remains strictly less than one. Every larger integer cell size lies in a dyadic window, which proves the same gap for all sizes beyond the terminal base. Rounded arithmetic is used only to enter this region, not iterated indefinitely with a finite rounding floor.

The independently validated windows are:

- r = 1/20000: [16,32], [32,64], [64,128], [128,256], and the overlapping terminal window [256,512]. The asymptotic tail begins at cell 256, normalized beta 196, with u approximately .006616387512382841. The exact terminal margin is positive, displayed as .3741351579972647.
- r = 1/12500: the same initial four windows, then [256,512] and overlapping terminal [512,1024]. The asymptotic tail begins at cell 512, normalized beta 392, with u approximately .003177757460539276. The terminal margin is displayed as .8871826138901137.

Exact fractions and all eleven window margins are in results.json. These intervals cover every integer cell size M >= 16, not only powers of two or even M.

## 6. Fixed finite bridge M = 2,...,15

Only for these fourteen finite sizes, the accepted uniform gap delta_0 = 31/1250 and Weyl's inequality give

    gap(H_0,L + eta B_L) >= delta_0 - 2|eta| ||B_L||
                         >= delta_0 - 3Lr.

The right side is positive for L <= 30 in both proposed neighborhoods. Multiplication by c and use of its positive lower bound give

    gap(H_M(g)) >= (31/1250 - 90r)/(1+r).                     (8)

At r = 1/20000 this is 406/20001, approximately .02029898505, strictly exceeding .015. At r = 1/12500 it is 220/12501, approximately .01759859211, strictly exceeding .005. Weyl is applied to ordered eigenvalues including multiplicity, so positivity also proves uniqueness of the perturbed ground state.

Besides checking the accepted uniform theorem and its exact range, the independent checker retrieves its actual accepted purity endpoints for each needed **even physical length 4,6,...,30** and rechecks the .0248 gap inequality at beta 49/4. It does not infer a stronger finite gap from an earlier weaker theorem. It does not need the historical physical length-25 result or change its preserved CPU-limit exception.

The finite set 2 <= M <= 15 and the cell bootstrap M >= 16 meet without a hole. No extensive Weyl loss is extrapolated to infinite size.

## 7. Independent arithmetic, provenance and limitations

The scalar implementation uses a 300-bit binary directed grid, a 96-term positive Taylor expansion after reduction to argument <= 1/4, an explicit first-omitted-term geometric remainder, reciprocal interval inversion, repeated squaring and exact integer square roots. This differs from the producer's 60-decimal/100-term/1/16 implementation. Every saved endpoint, recurrence, coordinate, finite-window margin and terminal margin is checked conservatively. There are no floating acceptance tests or imported producer modules.

The review freezes 34 consumed files, totalling 1,262,900 bytes. It verifies all frozen bytes, every producer input hash, all five manifest digests, and the 19 corresponding manifest members available in the snapshot, including the actual source n32 certificate and accepted s_0/t_0 results. It does **not** claim to rehash or rerun the entire physical dependency tree. Source proofs and implementations were inspected to establish what is inherited, and the new mathematical steps above were reconstructed independently.

Principal accepted source pins:

- uniform_smaller_second_initialization: fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84.
- uniform_smaller_second_initialization_review: 54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f.
- uniform_gap_0248_all_sizes_review: 5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf.
- uniform_second_thermal_full_review: 792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94.

The direct cell construction was cross-checked against original/Haldane_extensions/REPORT.md section 3.2, audit/AUDIT_REPORT.md, and the accepted chain/integer-window proofs. The sharper interpolation is also pinned from research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md. SNAPSHOT_SHA256.json provides exact per-file pins.

Eighteen adversarial corruptions are rejected, covering inflated seed values, Gaussian-length error, omitted c rescaling, cell/physical confusion, missing/odd windows, false terminal data, inflated purity or updates, threshold misuse, finite-bridge holes and losses, and a wrong g interval. These tests supplement the analytic proof and do not replace it.

The single accepted independent scalar run used .047441373 process CPU seconds, .051736311 monotonic wall seconds and 11,796 KiB peak RSS. Hard process limits were 30 CPU seconds and 256 MiB address space, with one-CPU affinity. No physical contraction, eigensolver or heat campaign was launched. The active directory is an extracted working tree, not a Git checkout. No root documentation, producer file, earlier seal or remote state was modified.

This is a mathematical exact-arithmetic audit, not a proof-assistant formalization. It inherits the already accepted physical thermal/MPS computations, keeps their provenance and historical exceptions, and adds no new physical-input claim. Run `python audit.py` in a disposable copy of this review folder; it reads only the included snapshot and rewrites local results. No network access is needed.
