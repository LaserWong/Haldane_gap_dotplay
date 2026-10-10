# Independent review: shell tails, correlated seed, and all-integer bridge

Updated 2026-10-10 13:36 America/New_York / 17:36 UTC.

## Exact checks completed

All three g=3/100 shell-tail certificates and updated low bands pass independent exact checks. All four original x→y→temperature correlated successes and all three refined successes reproduce exactly, including the refined beta=911/100 certificate with lower gap 0.004333053946 for every integer square side L≥256 under the previously audited transfer theorem. The physical model, edge multiplicities, and energy shift are those documented in REVIEW.md.

The parent’s strengthened finite-window interpolation is independently proved below. Independent rational endpoint checks pass all four original and all three refined all-integer bridges. An initial provenance mismatch was resolved by regenerating the bridge after the input checkpoint was complete; the source hashes now match. The final result is a unique ground state and gap at least 0.004333053946 for every integer square side L≥2. The complete exact endpoint evidence is in finite_window_results.json.

## 1. Number-preserving and pair-creation bounds

For one rung pair, write v=S_i,0·S_j,0+S_i,1·S_j,1. Its triplet-number-preserving part has

v_pres ≥ −(n_i+n_j)/2.

This is checked independently as a rational 16×16 PSD matrix using the physical-spin-derived local kernel. Its three singlet-pair creation amplitudes have normalized absolute square 1/4. There are no other changes of triplet number besides 0 and ±2.

On the four-regular periodic rung multigraph, the diagonal block at total triplet count q is at least d_q=(1−2g)q. Let E_empty(q) and E_occ(q) be the maximum weighted empty and occupied edge counts among q-site occupied subsets. The independent audit computes them by subset dynamic programming, rather than the producer’s edge scan over masks. It checks both

E_empty(q)=2N−4q+E_occ(q)

and the complementary-subset construction directly.

The creation block H_(q+2,q) has maximum absolute column sum at most (3g/2)E_empty(q), since each empty edge offers three spin assignments. Its maximum absolute row sum is at most (g/2)E_occ(q+2), since each compatible occupied pair offers at most one reverse transition. The Schur row/column bound therefore gives

||H_(q+2,q)||² ≤ t_q² = (3g²/4) E_empty(q) E_occ(q+2).

Parallel edges are counted with their weights; combining repeated transitions cannot invalidate these absolute-sum bounds.

## 2. Both parity chains and global ordered bins

For the compression to total triplet count at least q, split by number parity. The quadratic form of either block is bounded below by a scalar Jacobi matrix with diagonal d_j and off-diagonal −sqrt(t_j²), using the norms of the corresponding vector components. Both chains starting at q and q+1 must be included. The implementation does include both.

For each chain and proposed endpoint a, positive rational LDL pivots certify Jacobi−aI≻0. The audit recomputes every pivot independently and compares it with the saved rational value. The minimum of the two chain bounds gives a lower bound on the entire high-number compression.

Its codimension is sum_(j<q) C(N,j)3^j. The max-min principle yields the global ordered-bin inequality

λ_(1+sum_(j<q) C(N,j)3^j)(H') ≥ a_q.

Increasing a later bin to the preceding certified bound is also valid by ordered eigenvalue monotonicity. This explains the producer’s monotone-envelope step. The bins are whole-Hilbert-space bounds, not claims that interacting eigenvectors retain a fixed triplet number.

The q=0 and q=2 bins replace L0 and a in the already reviewed principal-angle theorem. The audit confirms that G/A/B/E and the trial spaces are unchanged, recomputes the improved complement b, and independently verifies every new Schur endpoint.

The upper heat-trace tail is the positive sum over q≥2 of C(N,q)3^q exp[−beta(a_q−shift)]. It has the correct direction for beta≥0.

## 3. Correlated first bootstrap cycle

For canonical finite traces,

A=Z8(beta)/Z4(beta)^2,
B=Z16(beta)/Z8(beta)^2,
C=Z16(2beta)/Z16(beta)^2.

Before interval substitution, cancel the common factors exactly:

J1=A^4 B^2 C=Z16(2beta)/Z4(beta)^8,
J2=B^4 C^2=Z16(2beta)^2/Z8(beta)^8.

The purity-squaring map G(x)=1−(1−x)^2/(2x^2) is increasing on (0,1]. Every argument accepted in the reviewed certificates is checked to lie in this interval. Consequently the first complete x→y→temperature cycle can use

A1≥G(J1), B1≥G(J2 A1), C1≥G(C^4 A1^2 B1).

This improves the certified interval arithmetic while preserving the same valid canonical recurrence. It does not assume independence of correlated trace estimates. After this cycle the base geometry is 4×4 and the inverse temperature is 2beta.

`correlated_audit.py` and `refined_correlated_audit.py` independently recompute every exponential enclosure, cancellation ratio, downward-rounded first purity, upward-rounded recurrence defect, final scale, and logarithmic gap endpoint. Only the xyt order is used; the other axis orders are not promoted.

The strongest reviewed refined result is beta_initial=911/100, six further complete cycles, final base side 256, and gap 2166526973/500000000000 = 0.004333053946. This is an exact-rational lower bound, not an ED estimate.

## 4. Sharper finite-window interpolation

Let S and T be lower bounds on S(n,beta) and T(2n,beta), with even n≥2, and let p=S²T>1/2. The identity S(n,2beta)=S(n,beta)² T(2n,beta)/T(n,beta)² and T(n,beta)≤1 imply S(n,2beta)≥p.

For the normalized spectrum of X_(2beta)^n, the dominant weight obeys

w≥[1+sqrt(2p−1)]/2.

Indeed the purity is at most w²+(1−w)², and purity>1/2 first ensures w>1/2. Uniqueness of the dominant absolute eigenvalue, together with positivity of every sufficiently large odd physical trace, forces its sign to be positive. Set r=(1−w)/w<1 and D=T/(1+r²).

For t=L/(2n) in [1/2,1], the signed numerator has the lower bound from the positive dominant eigenvalue and absolute tail, while Hölder gives the upper bound on the denominator. Combining them yields

T(L,beta) ≥ (1−r) S^(2−2t) D^t.

The logarithm of the last two factors is affine in t, so its minimum occurs at an endpoint. Therefore

I(S,T)=(1−r) min(S sqrt(D),D)

is a valid simultaneous lower bound for every integer n≤L≤2n, including odd L.

For the 2D spatial interpolation, inverse purity at B>1/2 gives a dominant y-transfer weight w_B≥[1+sqrt(2B−1)]/2. For s=W/m in [1,2],

S_x(n,W) ≥ (A w_B)^s−[A(1−w_B)]^s.

The derivative divided by (A w_B)^s decreases with s. Hence there is at most one interior stationary point, a maximum; monotone and constant limiting cases cause no problem. The endpoint values are A(2w_B−1) and A²(2w_B−1), so the lower bound is A²sqrt(2B−1).

Apply the 1D result first transversely, then longitudinally:

T(L,W) ≥ I(A²sqrt(2B−1), I(B,C)).

Both inverse-purity preconditions must be checked. The root implementation checks them and every accepted window passes.

The independent endpoint audit does not import the root script. It validates each recorded square-root-dependent bound by exact rational squaring and verifies each gap using a separate rational Taylor exponential enclosure. It also checks all source hashes, geometry, temperatures, recurrence states, window coverage, and the minimum with the asymptotic gap.

## 5. Side lengths two and three

There are 4N straight spin-half bonds at coupling g, each bounded below by −3g/4. Thus lambda2(H')≥1−3gN. The singlet product has expectation zero, so lambda1(H')≤0. Hence Delta≥1−3gN. At g=.03, the lower bound for L=2,3 is at least .19. This elementary full-space estimate covers the sizes below the first canonical 4×4 window.

## Reproduction

Run after the original review:

    python research_20261010/low_band_review/number_tail_audit.py
    python research_20261010/low_band_review/correlated_audit.py
    python research_20261010/low_band_review/refined_correlated_audit.py
    python research_20261010/low_band_review/finite_window_audit.py

Evidence: number_results.json, correlated_results.json, refined_correlated_results.json, finite_window_results.json. Floating 2×2 shell diagnostics are explicitly segregated inside number_results.json and do not supply any rigorous acceptance condition.
