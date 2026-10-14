# A bounded plan for the full residual contraction

## Inputs and order

Start with the 8×4-rung denominator (N=32, 64 spins, 14 pair-orbit columns). Consider N=64 only after a measured N=32 gate. The prior verified geometry contains 73,206 active fixed-origin q6 supports at N=32 and 992,424 at N=64. Full fixed-origin q4 support counts are 4,495 and 39,711. The ratios are 13.56 and 8.83 respectively. These are support counts, not full Hilbert dimensions.

The M matching coefficients are evaluated on demand as exact integers, using

    M_p=2(w2 w3 e_j1+w1 w3 e_j2+w1 w2 e_j3).

No q6 cache is needed. Each matching coefficient vector has at most three initial nonzero orbit positions, before coincident positions are combined. The 15×15 matching Gram is precomputed once.

## q4 contribution D=CM

For each q4 target support S, enumerate geometric edges e disjoint from S. Evaluate M on T=S∪e, contract its two e endpoints using coefficient 3 if already paired and coefficient 1 with partner reconnection otherwise, then accumulate the resulting three q4 matching coefficient vectors. Multiply each contribution by w_e. Finally contract D(S)*D(S) with the 3×3 matching metric.

Use all q4 target supports containing the origin. Restricting to supports on which L or R is nonzero is not justified. Rescale the final accumulated matrix by N/4 with exact divisibility verification. Upper bounds on elementary matching evaluations are 4,495×64×15=4,315,200 for N=32 and 39,711×128×15=76,245,120 for N=64. Empty-edge exclusion reduces these counts. This approach streams D and requires no q4 image cache.

## q6 contribution M*K M

Stream active q6 bra supports containing the origin. For each support, accumulate the local pull action of K on M as follows.

1. Empty-empty diagonal weight can be computed from total Σ_e w_e² minus edges touching the occupied set. Multiply by 3.
2. Apply the negative singlet projector on occupied internal edges with its exact recoupling rule.
3. Enumerate ordered wedges that can move one occupied outer endpoint to one empty outer endpoint. Pull M from the support with that endpoint exchanged. The center is either empty (plain hop) or occupied (negative singlet reconnection). Use w_ij w_ik.
4. Contract the resulting matching coefficients with the bra M and its matching Gram.

Each occupied endpoint has at most Δ(Δ−1)=12 oriented nontrivial wedge paths when geometric degree Δ≤4. Thus there are at most 72 wedge moves per six-site support. A loose source-matching bound is 73,206×72×15=79,062,480 at N=32 and 992,424×72×15=1,071,817,920 at N=64, before exploiting empty/occupied exclusions, vanishing M sources, repeated target supports or sparse coefficient vectors. These are matching visits, not elapsed-time estimates. A dense n×n outer product for every matching visit would waste work. Accumulate local coefficient vectors first and use sparse outer products or precomputed metric transforms.

Multiply the final q6 matrix by N/6 with exact divisibility verification. The fixed-origin identity is valid because the full contraction density is translation invariant, and incidence counting gives q T=N T_origin even with nontrivial stabilizers. Every ordered wedge contribution to a bra support must be included before this rescaling.

## Arithmetic and memory

Use int64 matching coefficients, checked signed int128 matrix accumulation, and arbitrary precision for subsequent rational trial contractions. Do not contract 56-bit trial coefficients in int128. W8 can be assembled as a geometry matrix first, then contracted in Python arbitrary precision.

For N≤64 and |M_matching,column|≤24, physical amplitudes are bounded by 15×24=360. The weighted edge sum is 2N≤128 and Σ_e w_e²≤4N≤256. A conservative absolute physical row sum bound for K is 3Σ_e w_e²+3Σ_i(Σ_j w_ij)²≤768+3072=3840. Therefore |(KM)_physical|≤1,382,400. The bilinear bound C(64,6)×3^6×360×1,382,400 and the q4 norm bound C(64,4)×3^4×(3×128×360)² are both far below 2^80. They certify ample final signed-int128 headroom. Implementation must still check each addition and independently bound its chosen intermediate matching representation. Cancellation is not a reason to skip overflow checks.

Streaming q4 and q6 coefficients consumes small fixed working memory. A fixed-origin active-support mask list requires under 8 MB at N=64 if stored compactly. Generating candidates before deduplication needs a separate measured budget. Existing q4 R cache is unnecessary for W8 alone. Full residual assembly may choose one. Its prior N=64 allocation was about 107 MB. Keep the complete task below 1 GB and one CPU.

## Timing tests and stopping conditions

1. Implement local matching operators in a new C++ file, without modifying accepted producer code.
2. Reproduce all small physical q8 matrices here, including every cross entry and the negative-commutator fixture. Cross-check full-support versus origin rescaling on 4×2.
3. On CPU6/BLAS1 with a 1 GB limit, benchmark a deterministic stratified sample of N=32 q4 and active q6 supports. Record counts, actual seconds, maximum RSS, integer checks and extrapolation uncertainty. This sample is not a geometry certificate.
4. Run the complete N=32 contraction only after the root approves its measured budget. Verify symmetry and positive semidefiniteness of W8 by exact rational elimination and check trial scalar nonnegativity. Independently recompute before use as a physical denominator input.
5. Consider N=64 only if its measured cost fits the remaining budget and it serves a needed denominator/certificate. Do not extrapolate 13.56× support count as a guaranteed runtime, and do not run it simply because it is available.

The completed work consists of the local reduction and independent small-system tests. The remaining q4/q6 residual blocks require separate assessment. W8 alone does not complete a new denominator certificate.
