# Exact large-seed block-Krylov moments through fourth order

Updated 2026-10-10 13:52 America/New_York / 17:52 UTC.

## Scope and normalization

This is the ordinary spin-1/2 square bilayer with unit vertical exchange and equal positive intralayer exchange g, on the periodic rung rectangle nx×ny. Length-two directions have parallel edges. Put N=nx ny, E00=−3N/4, t=g/2, and

H′=H−E00=Q+t A,    A=Σ_{ij} m_ij (T_i·T_j+D_i·D_j).

All inner products here remove the common factor 2^N from the rational local dimer basis used in `../symmetry/PROOF.md`. The vacuum norm is one. A singlet pair tensor |ij⟩ has norm squared 3, with rational magnetic coefficients (−2,1,−2). A product of disjoint pairs is represented by its matching, not by its physical magnetic configurations.

The original invariant basis B consists of vacuum and pair-orbit sums. Its dimension d is 6 on 4×4 and 15 on 8×4 and 8×8. Its Gram D is diagonal, with entries 1 and three times each pair-orbit size.

## Pairing algebra and its independent check

On an occupied pair of vertices, T_i·T_j acts as permutation minus contraction. If i,j are matched, the result is −2 times the original matching. If they belong to distinct pairs (i,k),(j,l), the result replaces those pairs by (i,l),(j,k), minus the replacement (i,j),(k,l).

The D_i·D_j rules are:

* Both sites empty: create the pair (i,j).
* One occupied: move that matching endpoint to the empty site.
* Both occupied and paired together: delete that pair with coefficient 3.
* Both occupied in different pairs (i,k),(j,l): delete i,j and join (k,l), with coefficient 1.

These rules, including every sign, were checked against both the rational dimer kernel and independently implemented physical-spin exchange on all 76 matchings with q=0,2,4,6 on the six-rung 3×2 periodic patch. The physical Hilbert space for this check has dimension 4^6=4096. The Hamiltonian includes parallel edges in the length-two direction. These finite checks supplement the tensor identities, rather than supplying an extrapolation assumption.

On a fixed four-vertex occupation set the three matching tensors have Gram diag(9), off-diagonal 3. For vectors of their coefficients x_p,y_p,

⟨x,y⟩ = 6 Σ_p x_p y_p + 3 (Σ_p x_p)(Σ_p y_p).

On a fixed six-vertex set the 15 matching tensors have Gram 3^c, where c is the number of connected loops in the union of the two matchings (a common pair counts as one loop). All 225 entries were checked in the physical rational basis. Distinct occupation sets are orthogonal. No occupation sector above q=6 can be reached by H from the trial space below.

## A coupling-independent form of the one-block trial space

Let L=A_42 B, omitting the zero column corresponding to vacuum. L has only q=4 support. If its input is a pair-coefficient array c, its coefficient on the matching (ij)(kl) is

L_(ij|kl)=m_ij c_kl+m_kl c_ij.

Thus span(B,L)=span(B,H′B) for every g≠0. This choice removes the small-g scaling and q≤2 component from the new Krylov columns. It is the same trial space as the previous explicit block1 calculation, with a different basis.

Write R=A_44 L and W=A_64 L. We compute four coupling-independent integer matrices:

F=L*L,    S=L*R,    V=R*R,    W6=W*W.

Here the asterisk denotes the physical inner product, with factor 2^N removed. S is symmetric. R is calculated by the occupied-edge permutation/contraction action and by pulling L from all configurations differing by one graph hop. Only four-vertex occupation sets and three matchings per set are required.

For a six-vertex matching (ij)(kl)(mn), W has coefficient

2 [m_ij m_kl c_mn + m_ij m_mn c_kl + m_kl m_mn c_ij].

The factor 2 counts the two possible creation orders of the graph pairs. This is the q6 part of A²B. It is the parent formula for H′²B with t² factored out. A nonzero coefficient requires two disjoint graph edges. The code generates unions of two disjoint graph edges and one arbitrary disjoint pair, deduplicates their six-vertex masks, and contracts only those sets. It never expands the 15 matching tensors into magnetic configurations.

## Complete exact block matrices

Let C denote the q≤2 coefficient matrix of H′B in the basis B. Let I be the d×(d−1) matrix with zero vacuum row and identity in its remaining rows, E=IF, and Fbar=IFIᵀ. The matrices in the basis (B,L) are

G = diag(D,F),

K = [[D C, t E], [t Eᵀ, 4F+tS]],

J_BB = Cᵀ D C+t² Fbar,

J_BL = t Cᵀ E+t I(4F+tS),

J_LL = 16F+8tS+t²(V+W6+Eᵀ D⁻¹ E).

J is the full ⟨H′trial,H′trial⟩, not a square of the compressed Hamiltonian. Its q6 term is W6. The q≤2 part of A L equals B D⁻¹E, by self-adjointness and invariance; its coefficients are exact integers in every geometry checked. The q4 part of H′L is 4L+tR.

For g=p/q, exported K and J multiply the displayed matrices by den=4q and den² respectively, so their entries are integers. With T=den H′ and

X = [[C_T], [2p Iᵀ]],    C_T=den C,

the original B-basis integer moments are

M0=D, M1=D C_T, M2=J_BB, M3=Xᵀ K X, M4=Xᵀ J X.

The last two formulas use integer-scaled K,J. All five matrices are exported in each coupling file. An exact Gram-LDL selection removes dependent trial columns before solving; 2×2 has dimension 4, 4×2 and 4×4 have dimension 11, and 8×4 and 8×8 have dimension 29.

## Ground intervals and limits of their claim

Floating generalized eigensolving proposes a 48-bit integer coefficient vector v. The norm, Rayleigh quotient, and complete residual squared are recomputed with exact rational arithmetic:

n=vᵀGv,    e=(vᵀKv)/(den n),

ρ=E00+e,    r²=(vᵀJv)/(den² n)−e².

Where the existing independently certified all-sector threshold a for λ1(H) satisfies ρ<a, Temple gives ρ−r²/(a−ρ)≤E0≤ρ. Otherwise the files retain exact moments, ρ, and r² but set the Temple lower endpoint and width to null. This failure of an old threshold is not a physical gaplessness claim and does not invalidate the trial moments. The parallel complete-band work can use its stronger number-sector cutoff and Schur bounds.

A small trial residual does not exclude missed low eigenstates. Spectral completeness always comes from an external all-sector comparison. The new seed files remain candidates pending independent-worker review and their incorporation into the complete trace/transfer calculation.

## Cost and integer safety

For N=64 there are 635,376 four-vertex sets. The code visits 478,176 sets with nonzero L or R. Two disjoint graph edges plus an arbitrary pair generate 13,706,880 six-set masks (before deduplication); 10,585,856 distinct sets remain, compared with C(64,6)=74,974,368 total six-sets. Reserved mask storage is 109,655,040 bytes. The rest is small fixed-size arrays and recursion state. The measured resource replay is saved separately and imposes a 1.5 GiB address-space cap and one CPU thread.

All graph degrees including multiplicity are four, and each edge multiplicity is at most two. In one q4 matching row each L coefficient is ≤4 in absolute value. The hopping and TT terms give the loose bound |R coefficient|≤256. A V entry is therefore at most C(64,4)×2,949,120 < 1.9×10^12 in absolute value. A W coefficient is at most 24; bounding all 15² Gram entries by 27 gives the loose whole-sum bound C(64,6)×15²×27×24² < 2.7×10^14. The remaining F and S contractions are smaller. These deliberately loose bounds are far below signed 64-bit maximum. Input is restricted to N≤64 and at most 20 pair orbits; supported exported geometries obey the graph assumptions. Subsequent matrix assembly and certificate arithmetic use unbounded Python integers and rational fractions.

## Verification coverage

`verify_moments.py` checks the pairing rules against independent physical spins and all q6 Gram entries, then transforms the new basis back to B+primitive(TB). Every saved G/K/J entry matches exactly on 2×2,4×2,4×4 for g=.01,.02,.03, including the saved 11-vector 4×4 block. Consequently these comparisons cover the full moments needed for one Krylov block, including the complete leaked q6 norm. The capped 8×8 repeat checks F/S/V/W entry-for-entry against the first run. Independent audit status must be taken from the parent review; these internal tests alone do not claim that review is complete.
