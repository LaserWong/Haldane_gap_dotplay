# Independent H², variance and Gibbs-effect review

2026-10-11 04:52 UTC / 2026-10-11 00:52 America/New_York (EDT).

## Accepted result and scope

For the fixed periodic D26 trial of the unit-exchange spin-one uniform Heisenberg chain, the new exact total-energy variances are independently accepted:

- physical L64: σ² ≈ .0004964120744254386;
- physical L32: σ² ≈ .0002629779063020885.

At β0 = 49/4, the variance-refined fidelity argument independently certifies the actual uniform Gibbs effect bounds

    κ64 = Tr(ρ0,64 B64²)/96² ≤ 119/1000 = .119,
    κ32 = Tr(ρ0,32 B32²)/48² ≤ 969/10000 = .0969.

The corresponding finer outward bounds are approximately .11893272968811675 and .09685318612605492. Exact fractions are in scalar_results.json. This is not a new all-size alternating interval certificate. Use of these bounds in such an interval requires a separate composition review.

The physical Hilbert dimensions remain 3^64 and 3^32, MPS bond dimension26 and retained linear trial dimension1. No thermal trace, eigensolver or full physical Hilbert vector was recomputed. This is a new separately authorized review gate, with its own resource ledger. Earlier B² and interval seals, including all Stage21 evidence, remain unchanged.

Producer manifests:

- H²64: a6552c8c5de014a0ffc603e98e96b5e65752892a3752fab6a107d97722898e50;
- H²32: 5e6bb98a58c8b4f72a3199061bf23488749e11b80fe7177080c86760c0839dd0;
- inherited independent B²/local review: 8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee.

## 1. Independent positive-convolution reconstruction

Let T be the one-site double transfer, O = E_h, U = E_(h²), V = E_(h01 h12 + h12 h01), and N_L = Tr(T^L). The complete eleven charge-difference sectors have dimensions1,8,32,80,136,162,136,80,32,8,1. Every local insertion entry and both full physical H² fixtures at L4/L6 were independently verified in the inherited review; that seal is checked rather than modified or rerun.

Expanding H_L² as a sum over ordered bond pairs gives, for the lengths considered,

    H2_L = L [Tr(U T^(L−2)) + Tr(V T^(L−3))
      + Σ_(r=2)^(L−2) Tr(O T^(r−2) O T^(L−r−2))].

Both adjacent orders occur in V with positive sign. Every disjoint displacement, including the periodic closing configurations, occurs once per initial bond. This is distinct from the negative adjacent term and alternating disjoint sum for B².

For K+ = [[T,O],[0,T]], its upper-right block R_n satisfies

    R_n = Σ_(j=0)^(n−1) T^j O T^(n−1−j).

The reviewer uses its own matrix primitives and a left-to-right recurrence, not the producer's right-to-left binary kernel:

    P_(2a) = P_a²,
    R_(2a) = P_a R_a + R_a P_a,
    R_(2a+1) = P_(2a) O + R_(2a) T.

With n = L−3 and Pnext = T^(L−2), each sector contributes

    N = Tr(Pnext T²), H = L Tr(Pnext O),
    H2 = L[Tr(Pnext U) + Tr(P_n V) + Tr(R_n O)].

A single parameterized reviewer executable supports exactly L32 and L64 with separate length-dependent hard guards. It retains the unchanged dimension162 and avoids unrestricted numeric source substitution. Fresh exact GMP contractions reproduce every sector's norm, total H, H², same-bond, adjacent and positive-disjoint integers:22 checkpoints and132 fields in total. The old B² checkpoints independently agree on norm/H/same/adjacent; final N/H agree with the previously accepted exact anchors.

## 2. Exact total variance

For the normalized trial,

    σ² = H2/N − (H/N)² = (H2·N−H²)/N².

The full integer subtraction is performed exactly and is nonnegative at both lengths. H/N is already total energy, H2/N is its second moment, and no extra factor L is applied. These are total variances, not per-site quantities or standard deviations. They are invariant under adding the scalar shift aL, a = 700741/500000. The checker also verifies H2 ≥ 0 and H2 ≤ (2L)²N.

## 3. Separately improved finite thermal premises

At each physical length, load the original accepted shifted partition-function upper bound Q_L and the exact shifted trial mean μ_L = H/N + aL. The scalar checker verifies μ_L exactly against the relevant accepted certificate. The variational inequality E0′ ≤ μ_L gives a new ground Gibbs weight lower bound

    p0 = exp(−β0 E0′)/Z_L ≥ exp(−β0 μ_L)/Q_L ≥ w_L.

This step uses the actual Gibbs state and the variational numerator; it is separate from the earlier purity-only weight bound. The resulting lower weights are approximately .9176574240821238 at64 and .9387875477507066 at32. Both exceed1/2, which excludes ground degeneracy.

The reviewer independently checks lower_exp(−β0 E_lo) > Q_L at

    E_lo,64 = −702409/100000000,
    E_lo,32 = −627681/100000000.

Because exp(−β0 E0′) ≤ Z_L ≤ Q_L, these are rigorous lower energy bounds. It separately checks

    w_L > upper_exp(β0 δ_L)(1−w_L)

at δ64 = 19681/100000 = .19681 and δ32 = 1783/8000 = .222875. Since p1 ≤ 1−p0, this proves the required finite-volume spectral gaps. Neither stronger value is substituted without verification into an older purity certificate, and neither is asserted as an all-size gap.

The energy-only infidelity bound is ε0 = (μ−E_lo)/δ. Its verified values are approximately .0356425286 and .0231359780, both strictly below1/2. Thus the ground overlap F is already known to exceed1/2 before any variance inversion.

## 4. Pairwise variance and branch selection

Write the normalized trial's spectral probabilities as p_i, with p0 = F. The exact variance identity is

    σ² = Σ_(i<j) p_i p_j(E_i−E_j)².

All terms are nonnegative. Retaining only the ground/excited pairs and using E_i−E0 ≥ δ gives

    σ² ≥ F(1−F)δ².

There is no missing factor2: the expression is the i<j version of one half the ordered-pair sum. Let ε = 1−F. The prior energy-only bound places ε in[0,1/2), where ε(1−ε) is increasing. When4σ² ≤ δ², this selects the small root and gives

    ε ≤ [1−sqrt(1−4σ²/δ²)]/2.

The reviewer verifies the discriminant, takes the minimum with ε0 and brackets the root independently. The resulting infidelity upper bounds are approximately .012984463954072514 at64 and .005322482587375599 at32. Each variance also lies strictly below δ²ε0(1−ε0), proving a strict improvement over the energy-only bound.

As an additional exact consistency check, the producer's saved variance-infidelity endpoint e is tested by0 ≤ e ≤1/2 and e(1−e) ≥ σ²/δ². The large-overlap branch is therefore verified rather than assumed from a small residual or variance.

## 5. From fidelity to the actual Gibbs effect

The trial B² effects q64 and q32 are inherited as exact fractions from the accepted independent B² review. For A = B_L²/(3L/2)²,0 ≤ A ≤ I, trial expectation q and ground expectation α, Cauchy–Schwarz applied separately to sqrt(A) and sqrt(I−A) gives

    sqrt(F) ≤ sqrt(qα) + sqrt((1−q)(1−α)).

On the verified branch f ≤ F with f > q, inversion yields

    α ≤ f q + (1−f)(1−q) + 2 sqrt[f q(1−f)(1−q)].

The reviewer uses this single-root expression, independently of the producer's square of a sum of two roots. Excited-state effect expectations are bounded by1, hence

    κ_L ≤ 1−w_L+w_L α.

All endpoint directions are checked. The independent bounds give κ64 < .119 and κ32 < .0969 and agree with the producer's more coarsely argument-rounded bounds within10^−35. These remain Gibbs bounds, not just trial-state expectation values.

## 6. Independent arithmetic and preserved producer failure

The independent scalar implementation encloses exponential arguments on a192-bit dyadic grid, uses512-bit directed fixed-point Taylor recurrences, a positive geometric tail, and outward squaring/reciprocals. Term-by-term rounding prevents large exact Rayleigh denominators from growing through the Taylor expansion. Integer square roots bracket the exact variance and effect fractions. Thus the exact variance is never replaced by floating cancellation or a rounded display.

The producer's first64 scalar-only attempt hit its one-second limit before producing an accepted result. Its failure and conservative3-second charge are preserved; the authorized corrected producer used dyadic argument rounding. This review never reruns that failed source and has no failed attempt or retry of its own. Both physical producer runs and their final scalar proofs are frozen and independently checked.

## 7. Separate resource ledger

The approved review split was14 CPU seconds for64,11 for32 and5 for scalar checks/sealing, with a separate30-second compilation allowance. Actual observations:

- Reviewer compilation:4.260730 child plus .250349611 launcher CPU seconds; peak159040 KiB. One compilation serves both lengths.
- Physical64:8.705217 child plus .292431468 launcher seconds; peak29644 KiB.
- Physical32:5.607410 child plus .281775827 launcher seconds; peak20116 KiB.
- Joint scalar: .132122 child plus .153348410 launcher seconds; peak11008 KiB.

Before sealing, scientific review total is15.172304705 CPU seconds; compilation total is4.511079611 seconds. Charging the final seal its full one-second hard reserve gives16.172304705 < 30 for the separate new review gate. Older review ledgers are neither reset nor charged again.

All numerical runs are CPU5/256 MiB, with explicit child/parent reservations, verified post-exec CPU/address-space/affinity/signal controls, parent-death SIGKILL, active aggregate CPU polling, external90-second whole-session watchdog, independent wait4 and complete tree cleanup. Compilation uses512 MiB and10+1 CPU reservations. Every attempt is exclusive, all exits are zero, no guard fired, no descendants remained and no automatic or unexpected retry occurred.

The exact outputs, source/binary, full input pins, guard logs, mathematical proof and new seal form the review deliverable. No wider interval is accepted by this package alone.
