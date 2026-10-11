# Independent structural theorem: a positive alternating spin-one cell transfer

2026-10-11 03:26 UTC / 2026-10-10 23:26 America/New_York (EDT).

## Verdict and scope

**ACCEPTED analytic lemma.** For the homogeneous periodic spin-one chain

    H_M(g) = sum_(j=1)^M [S_(2j-1) · S_(2j) + g S_(2j) · S_(2j+1)],

at every finite inverse temperature tau > 0 and every finite g >= 0, grouping each g bond into a two-spin cell gives a **positive trace-class** history transfer K_g,tau. With any real constant cell shift q,

    Tr exp[-tau(H_M(g) + q M I)] = Tr K_g,tau^M,       every integer M >= 2.

The positivity follows from a factorization A A*, between explicitly different history-measure Hilbert spaces. It does not follow merely from multiplying self-adjoint operators. This is stronger than the real self-adjoint Hilbert–Schmidt property used in the frozen earlier review.

Consequences:

1. Canonical cell seed lengths may be odd, including physical n30 -> cell15 and physical n34 -> cell17.
2. The spatial/thermal sequential purity recursion remains valid without an even-cell restriction.
3. Every integer window n <= M <= 2n has the stronger lower bound

       T(M,tau) >= min(S(n,tau) sqrt(T(2n,tau)), T(2n,tau)).       (A)

   This removes both the signed-tail loss and the inverse-purity threshold K > 1/2 from the **interpolation lemma**. Positive purity endpoints and legal recurrence domains are still required for a numerical bootstrap.

This note changes no frozen review or numerical conclusion. New interval or gap candidates require separate directed arithmetic verification.

## 1. Single-site reality and the common chronological kernel

For integer spin one there is an orthonormal Cartesian basis in which single-site time reversal is complex conjugation. Every spin component S^alpha is purely imaginary and Hermitian. Put

    C^alpha = i S^alpha.

These are real skew-symmetric matrices with operator norm one. Therefore

    -S · S = sum_(alpha=1)^3 C^alpha tensor C^alpha.

The two factors at the endpoints of a bond have the **same** sign, matrices and component labels. No endpoint transpose or additional complex conjugation is inserted.

A history x is a finite time-ordered sequence ((t_1,alpha_1),...,(t_k,alpha_k)), with 0 < t_1 < ... < t_k < tau. Include the empty history. Given two histories x and u with no coincident event times, merge their events chronologically and define

    k(x,u) = Tr_site [C^(alpha_last) ... C^(alpha_first)].

For two empty histories this is Tr I = 3. The trace is real and |k(x,u)| <= 3. Both boundary histories use the same local C matrices, so merely exchanging the two labeled input lists leaves their merged matrix sequence unchanged:

    k(x,u) = k(u,x).                                          (1)

There is no reversal of matrix order. The equality does not require the matrices to commute. Equal-time collisions between two independently integrated nonempty histories have zero measure. One may define the kernel arbitrarily and symmetrically on this null set; such choices do not change the integral operators or finite-volume traces.

The single-site reality premise is specific to integer spin. Cell time reversal squaring to +1 alone would not establish this single-site real factorization for half-odd-integer spins. No such extension is claimed here.

## 2. Raw history measures, including g = 0

For a nonnegative coupling a, define the **unnormalized** positive history measure mu_a by

    integral f(x) d mu_a(x)
      = sum_(k>=0) a^k sum_(alpha_1,...,alpha_k)
          integral_(0<t_1<...<t_k<tau) f(x) dt_1...dt_k.

Its total mass is exp(3a tau). In particular mu_0 is a unit point mass on the empty history. Thus no division by g or assumption g > 0 is needed. If normalized Poisson measures were used instead, their missing exponential masses would have to be restored; this proof always uses the raw measures above.

Let

    H_1 = L^2(history space, mu_1),
    H_g = L^2(history space, mu_g).

These Hilbert spaces carry different measures. They are not silently identified. For g > 1 the density g^k relative to mu_1 need not be bounded; no bounded multiplication or similarity assertion involving that density is used.

Define A_g : H_g -> H_1 by

    (A_g f)(x) = integral k(x,u) f(u) d mu_g(u).

The bound on k and the finite measures show

    ||A_g||_HS^2
       = integral integral |k(x,u)|^2 d mu_1(x) d mu_g(u)
       <= 9 exp[3tau(1+g)] < infinity.                        (2)

It is therefore a bounded Hilbert–Schmidt operator. Its actual Hilbert-space adjoint is

    (A_g* h)(u) = integral conjugate(k(y,u)) h(y) d mu_1(y).

Because k is real and satisfies (1), conjugate(k(y,u)) = k(u,y). Hence A_g A_g* is an operator on H_1 with kernel

    K_g(x,y) = integral k(x,u) k(u,y) d mu_g(u).                (3)

For any h in H_1, <h,A_g A_g* h> = ||A_g* h||^2 >= 0. This proves positivity with the correct measures and adjoint, rather than a noncommuting product shortcut. The product of two Hilbert–Schmidt operators is trace class, and

    Tr(A_g A_g*) = ||A_g||_HS^2 < infinity.

Its eigenvalues are nonnegative and summable. Multiplication by exp(-tau q) accounts for a real scalar cell shift and preserves all these properties.

## 3. Identification with the physical cell kernel

Choose cell j to contain physical sites (2j,2j+1). Its internal bond has coupling g and its two external bonds have coupling one. Consider the local two-spin chronological kernel with prescribed external histories x and y, using the intra-cell propagator exp(-Delta t g S_L · S_R) between external events.

Expand each intra-cell propagator in its Duhamel/Dyson series. Every internal event contributes g sum_alpha C_L^alpha tensor C_R^alpha. Combining the internal events over the time intervals separated by prescribed external events gives exactly the history measure mu_g. For each resulting history u, chronological ordering separately at the left and right spin gives k(x,u) and k(u,y). Tracing the two-spin tensor product multiplies these scalar traces. Consequently the physical cell kernel is exactly (3).

This regrouping is absolutely convergent. For fixed external histories, each C insertion has norm at most one. The sum of absolute traces of internal histories is bounded by 9 exp(3g tau). For a finite periodic chain, summing all histories is bounded by

    3^(2M) exp[3tau M(1+g)]

before the optional finite scalar shift. Thus Fubini/Tonelli on absolute values and termwise regrouping are justified. There is no time- or volume-limit exchange.

Equivalently, expand all 2M physical bonds at once. Integrate the M unit-bond histories with mu_1, then integrate the M internal-bond histories with mu_g. The resulting cyclic product of cell kernels is exactly the full finite-dimensional partition function. For M >= 2, bounded kernels on these finite measure spaces and the trace-class factorization give the usual cyclic-integral trace identity

    Z_M(tau) = Tr K_g,tau^M.

The same K_g,tau works for every M. At M = 2 the two unit bonds and the two internal g bonds are distinct physical bonds. No separate convention at M = 1 is needed for the theorem.

Checks at the endpoints of the structural argument:

- At g = 0, H_g is one-dimensional, A_g A_g* has rank at most one, and the representation reduces to independent unit-coupling dimers.
- At g = 1, the measures agree and k is a real symmetric single-site kernel; the cell kernel is its square. At general g the valid expression is A_g A_g* between the two measures, not an unjustified product of same-space self-adjoint transfers.

## 4. Positive transfer purities at every integer base

For a positive trace-class K_tau and any integer n >= 1,

    rho_sp = K_tau^n / Tr K_tau^n

is a genuine positive trace-one operator. Its purity is

    S(n,tau) = Z_(2n)(tau)/Z_n(tau)^2 <= 1.

For our physical application we only need n >= 2. Evenness is unnecessary. Physical thermal purity remains

    T(M,tau) = Z_M(2tau)/Z_M(tau)^2 <= 1.

The exact identities behind the previous sequential update do not change:

    S(n,2tau) T(n,tau)^2 = S(n,tau)^2 T(2n,tau),
    T(4n,tau) >= S(2n,2tau) T(2n,tau)^2.

Purity squaring gives the increasing function

    G(z) = 1 - (1-z)^2/(2z^2),

and hence lower endpoints may be updated sequentially as

    S_new = G(S^2 T),       T_new = G(T^2 S_new),
    (n,tau) -> (2n,2tau).

All inputs must lie in their legal positive domains, and a nonpositive lower output cannot be treated as a useful positive endpoint. The positivity theorem does not make an unsuccessful scalar recurrence automatically successful.

## 5. Stronger interpolation with no signed-tail construction

Fix any integer n >= 2 and integer n <= M <= 2n. Write t = M/(2n), so 1/2 <= t <= 1. Let lambda_i >= 0 be eigenvalues of K_tau and mu_i >= 0 those of K_(2tau). These operators may act on different history spaces; no identification between their eigenvectors is made.

For the numerator, nonnegative-sequence l^p norm monotonicity gives

    Z_M(2tau) = sum_i mu_i^M
       >= (sum_i mu_i^(2n))^(M/(2n))
       = Z_(2n)(2tau)^t.                                    (4)

For a direct proof, put a_i = mu_i^M and r = 2n/M >= 1; then sum_i a_i^r <= (sum_i a_i)^r. Finite-subfamily limits justify the countable sequence. All relevant sums are finite because the operators are positive trace class.

For the denominator, Holder interpolation gives

    Z_M(tau) <= Z_n(tau)^(2-2t) Z_(2n)(tau)^(2t-1).            (5)

Dividing (4) by the square of (5) and canceling trace factors yields

    T(M,tau) >= S(n,tau)^(2-2t) T(2n,tau)^t.                  (6)

The logarithm of the right side is affine in t, so its minimum on [1/2,1] is the smaller endpoint value. This proves (A). If only certified lower endpoints s <= S and v <= T are available, monotonicity of the nonnegative exponents proves the safe uniform bound

    T(M,tau) >= C_pos := min(s sqrt(v), v).                   (7)

Use a downward square-root enclosure. A strict directed inequality

    C_pos - upper_exp(tau_upper D)(1-C_pos) > 0

then proves uniqueness and gap at least D for every integer M in the window, just as in the accepted earlier proof.

No leading-atom construction, inverse-purity threshold, signed-tail subtraction, parity restriction, or assumption of physical purity monotonicity in volume is present. For a signed transfer, (4) need not hold: eigenvalues 2 and -1 give Z_3 = 7 and Z_4 = 17, but 7^4 < 17^3. This illustrates the precise role of the newly established positivity.

## 6. Consequences and remaining certification requirements

All three accepted uniform physical initializations may now be used as cell seeds: n30 -> cell15 with own physical60 anchor; n32 -> cell16 with own physical64 anchor; n34 -> cell17 with own physical68 anchor. The untwisted staggered Gaussian comparison still concerns **even physical lengths**, which all three provide. Odd cell count does not mean odd physical ring length. A stronger uniform-chain conclusion obtained through these two-site cells would cover even physical lengths only; it must not be relabeled as a stronger all-physical-length theorem without a separate odd-physical-length argument. The existing all-integer-physical-length .0248 theorem remains unchanged.

For near-uniform couplings, retain c = (1+g)/2 and tau = beta/c. Each particular trial uses its own accepted physical anchor, and the Gaussian losses use that actual physical seed length. Finite bridges must reach exactly to cell n-1, and no source endpoint or temperature may be relabeled.

The improved window estimate can enlarge the proved gap or help a perturbed seed that previously failed an early signed window. It does not by itself prove that a larger perturbation interval reaches the small-defect basin. The existing small-defect continuation remains a valid sufficient closure once its directed conditions are met. No stronger numerical interval is certified by this structural note alone.

## 7. Independence, checks and preservation

The mathematical proof above was independently reconstructed after the producer proposed the factorization. The sharper interpolation in section 5 was proposed by the producer and independently verified here. The predecessor source is original/Haldane_extensions/REPORT.md section 3.2, which constructs the self-adjoint cell history kernel; positivity here uses the additional factorization available for the specific spin-one internal Heisenberg bond. It is not asserted for arbitrary exchange-invariant cell operators v.

The companion exact scalar checks exercise the positive-spectrum norm inequalities and the combined window formula, plus signed-spectrum and noncommuting-product counterexamples. They perform no spin matrix construction, physical contraction, eigensolver or heat calculation. They are consistency checks of the analytic inequalities, not replacements for the proof.

All files are new in uniform_alternating_positive_cell_review. The frozen numerical interval review, producer package, prior source seals, root documents and remote state are unchanged. This is an analytic/exact-arithmetic mathematical review, not a formal proof-assistant certificate.
