# Independent review: small-seed canonical exclusion at g=.04 and .05

This audit writes only `small_seed_exclusion_review`. Producer files and prior independent-review results are not changed. Final acceptance and numerical summaries are recorded in README.md after both replays finish.

## Precisely what is being excluded

The physical model is the ordinary spin-1/2 square bilayer, with unit antiferromagnetic rung exchange and equal straight in-layer exchange g=1/25 or 1/20 in both directions. There are no crossed exchanges. All patches have periodic positive-direction edge multisets, retaining parallel bonds when a side has length two. A patch with N rungs has 2N spins, dimension 4^N, and shifted Hamiltonian H'=H+3N/4.

Write Z4, Z8 and Z16 for the unnormalized physical partition functions on 2×2, 4×2 and 4×4. The exact canonical x→y→temperature starting data are

- J1=Z16(2β)/Z4(β)^8
- J2=Z16(2β)^2/Z8(β)^8
- C=Z16(2β)/Z16(β)^2.

The specified recurrence is G(x)=1−(1−x)^2/(2x²), followed by

A1=G(J1), B1=G(J2 A1), C1=G(C^4 A1² B1),

and successive cyclic updates G(A^4 B² C) in the ordered sliding triple. An update is usable only when all prior lower bounds are positive. The even-patch transfer-purity identities give the physical J1,J2,C≤1. On 0<x≤1, G is increasing since G'(x)=(1−x)/x³≥0.

For every β≥0, the independently checked data produce an upper enclosure of one of these recurrence outputs that is nonpositive. If the exact recurrence remained positive up to that output, monotonicity would make its output no larger than that enclosure, a contradiction. Consequently even exact physical partition functions cannot keep this particular small-seed canonical lower-bound recurrence positive indefinitely at either specified coupling. This is stronger than a failed sufficient-basin test or a finite floating temperature scan.

This excludes neither other spatial seeds, another order or recurrence, improved bootstrap inequalities, nor another proof method. It does not imply physical gaplessness, a phase boundary, failure of the actual thermal purities to be positive, or a no-go for all low-band certificates.

## Physical inputs: independent reconstruction

The six final `frontier/*_symmetric_number_low_band.json` files are audited coupling by coupling. No producer code is imported. The physical-spin local kernel and rational symmetric-inertia elimination come from the prior independently reviewed `low_band_review/independent_review.py`; their exact source hashes are recorded. Using that kernel, every current excited trial is reapplied to the Hamiltonian, with independent combinatorial checking of its basis, all reached configurations, the full weighted Gram matrices G/A/B, and the direct full residual matrix E. Leakage outside the trial support is retained.

Each current symmetry ground basis is independently applied to the same physical Hamiltonian. Every compressed G, H and H² entry is reconstructed from the sparse integer vectors, and positive definiteness of the full trial Gram matrix is checked. For its supplied integer coefficient vector, the exact Rayleigh quotient and full residual are reconstructed and compared with the final scalar ground block. On each 2×2 patch, all these moments are also rebuilt directly in the computational-spin basis, using the exact integer physical Hamiltonian. Ground trial dimensions, expanded configuration supports, reached supports and full Hilbert dimensions are separately reported; none is an MPS bond dimension.

The excited blocks have odd triplet parity with M=0 and M=1, each rank N. Exact spin flip supplies the orthogonal M=−1 partner of the latter. The ground block has even parity/M=0 and rank one. The total retained rank is therefore 1+3N, namely 13, 25 and 49.

The g=.05 4×4 M=1 accepted block is independently reconstructed from its final trial file. The retained rejected ARPACK proposal is checked to differ and to have a highest Ritz value above the counted cutoff. The accepted block has full exact rank 16 and every Ritz value below the cutoff. This audits the degeneracy repair from its exact mathematical output, without relying on a LOBPCG convergence claim or rerunning a numerical eigensolver.

## Complete-band count and omitted spectral tail

The local number-preserving inequality v_pres≥−(n_i+n_j)/2 and the three pair-creation amplitudes of normalized absolute square 1/4 are checked from the physical-spin-derived 16×16 kernel. Number changes are only 0 and ±2. The periodic rung multigraph is four-regular with multiplicities, so the number-q diagonal block is bounded below by d_q=(1−2g)q.

Independent occupancy dynamic programming rebuilds E_occ(q) and E_empty(q), with E_empty(q)=2N−4q+E_occ(q). Absolute row/column sums give squared pair-creation norm at most t_q²=(3g²/4)E_empty(q)E_occ(q+2). The compression to number≥q is bounded below by the minimum of both parity Jacobi chains, with diagonal d_j and off-diagonals −sqrt(t_j²). Every rational endpoint is verified by recomputing every strictly positive LDL pivot. The monotone envelope is independently checked.

The high-number subspace has codimension sum_{j<q} binom(N,j)3^j. Min-max therefore gives the global ordered-bin lower endpoints with these multiplicities. This is whole-Hilbert counting, not a claim that interacting eigenstates have fixed triplet number. Bin multiplicities sum exactly to 4^N. The q=2 bin gives λ_(2+3N)≥a; all 1+3N trial Ritz values are strictly below a, leaving no room for an omitted low mode in any magnetization/parity sector.

Let L0 be the q=0 global lower bound, r the largest trial Ritz upper endpoint, and ε the maximum normalized residual-squared bound across the orthogonal blocks. The prior independent principal-angle argument gives the orthogonal-complement lower bound

b=a−(a−L0) ε/(a−r)²,

with ε/(a−r)²<1 and r<b, both checked exactly here. For every saved lower eigenvalue endpoint t<b, the rational pencil

(b−t)(A−den·t·G)·eden−den·E

is independently checked by symmetric elimination to have at most the permitted number of negative eigenvalues. Each upper endpoint is independently checked by the Ritz min-max bound. These results provide certified intervals for the complete retained band. The q≥2 ordered bins bound every remaining eigenvalue.

## Heat-trace normalization and directions

For each patch let s be its retained ground upper endpoint in H' units and E=−3N/4+s in physical units. The shifted partition trace is Z(β)=exp(−βE)T(β). Each retained interval [l_i,u_i] contributes exp[−β(u_i−s)] to a lower bound and exp[−β(l_i−s)] to an upper bound. Exact multiplicities are retained. The upper trace includes the complete q≥2 bin sum; the lower trace may omit those positive terms. At β=0 the upper trace multiplicity is exactly 4^N and the lower trace multiplicity is exactly 1+3N.

The resulting canonical upper inputs use an upper Z16 numerator and lower Z4, Z8 or Z16 denominators. The physical energy-shift factors are exp[β(8E4−2E16)] and exp[β(8E8−4E16)]; the rung constants cancel exactly. No normalized-versus-unnormalized trace factors are dropped.

For a closed interval [β_l,β_h], each exponential upper bound is taken at the endpoint selected by the sign of its shifted energy. Retained upper gaps u_i−s are checked nonnegative, so the lower denominator is valid at β_h throughout the interval. All arithmetic, including exponential truncation, range reduction and rounding, uses rational enclosures. The independent replay uses the previously reviewed 256-bit/70-term routine, separate from the producer's 160-bit/40-term implementation. Every independently computed upper input is no larger than the producer's saved upper input, and the saved coarser inputs are separately propagated with independent directed arithmetic.

## Exhaustive inverse-temperature partition

1. Hot range 0≤β≤4. Physical thermal purity C(β)=Z(2β)/Z(β)² is nondecreasing because d log C/dβ=2(〈H〉_β−〈H〉_2β)≥0, with d〈H〉_β/dβ=−Var_β(H)≤0. Hence C(β)≤C(4). If the first two recurrence outputs are positive, they are at most one, and C1≤G(C(4)^4)<0. Otherwise failure already occurred. The hot argument gives failure by update three for both couplings.

2. Middle range 4≤β≤20. Exactly 320 consecutive closed rational boxes [4+k/20,4+(k+1)/20], k=0,…,319, cover the whole interval. Each box has an independently certified nonpositive recurrence upper output, with no sampling inference. All shared endpoints are covered twice and there are no gaps.

3. Cold range β≥20. Rebase the 4×4 upper trace on its ground lower endpoint E16_low. Every resulting retained/tail lower gap is nonnegative. If U_rel(40) is its relative trace upper bound at 40, then for β≥20, the numerator is bounded by exp(−2βE16_low)U_rel(40). Keeping only the ground term in each denominator yields

J1≤exp(−20 d1)U_rel(40), J2≤exp(−20 d2)U_rel(40)²,

where d1=2E16_low−8E4_upper>0 and d2=4E16_low−8E8_upper>0. Both slope signs and all relative gaps are checked exactly. Together with C≤1, these uniform upper inputs already force a nonpositive recurrence output.

The three closed ranges cover every β≥0. The case β=∞ is a limit, not a separately evaluated Gibbs state; all finite nonnegative inverse temperatures are covered uniformly, including the entire unbounded cold ray.

## Resource and provenance policy

The audit scripts pin numerical execution to one CPU, set each BLAS backend to one thread, and impose a 1 GiB process address-space limit. No remote write is performed. Input SHA-256 hashes are verified again at completion and are not used as a substitute for the physical, analytic or exact-arithmetic checks. The two runnable audit programs and their result files allow independent resumption and reproduction.
