# Independent proof of the bosonic triplet-number tail bound

Updated 2026-10-10 14:26 America/New_York (EDT) / 18:26 UTC.

## Scope and verdict

The proposed pair-creation estimate is valid for every finite complex symmetric matrix K and every nonnegative integer particle number q. Its application to the ordinary spin-1/2 periodic square bilayer is valid with the stated normalization and period-two parallel-edge convention. The revised whole-space Jacobi comparison follows by an orthogonal compression and min-max. Numerical acceptance of the frozen files is reported separately in `results/summary.json` and `results/bin_replay.json`.

The physical model has N=nx ny rungs, nx,ny at least two, vertical coupling one, positive straight intralayer coupling g on both layers, and no crossed exchanges. Each positive-direction periodic graph edge is counted, so a direction of length two has parallel bonds. Set H′=H+3N/4. Energies below refer to H′. The physical Hilbert dimension is 4^N. No global spectral-gap improvement is claimed by this review, which checks the new whole-space tail inputs only.

## 1. Pair creation on finite bosonic number sectors

Let F_q be the q-particle sector of the bosonic Fock space over C^d. For a finite complex symmetric matrix K=K^T, define

B = (1/2) Σ_(i,j) K_ij a_i† a_j†,

v = (1/2) Tr(K K†),

κ² ≥ ||K||².

Here † denotes the Hilbert-space adjoint. Symmetry of K is essential to the displayed commutator with that K. If one begins with a nonsymmetric coefficient matrix, B depends only on its symmetric part and that part must replace K throughout. No reality assumption or sign assumption on K is needed.

All identities below may first be evaluated on finite-particle vectors. Their restrictions to F_q are finite-dimensional identities, so this proof never takes the operator norm of B on the entire Fock space.

Normal ordering gives

[a_i a_j, a_k† a_l†]
= δ_jk a_l† a_i + δ_ik a_l† a_j
+ δ_jl a_k† a_i + δ_il a_k† a_j
+ δ_jk δ_il + δ_ik δ_jl.

Multiplying by conjugate(K_ij) K_kl /4 and summing, the four single contractions give dΓ(KK†)=Σ_(u,v) (KK†)_uv a_u† a_v. The double contractions give vI. Thus

[B†,B] = dΓ(KK†) + vI.

In particular v=||B|vacuum⟩||². The matrix in the number-preserving term is KK†, which cannot generally be replaced entrywise by K†K. The independently implemented complex test uses a symmetric nonnormal K for which these two matrices differ.

Since 0≤KK†≤κ²I, its second quantization satisfies

0≤dΓ(KK†)|_(F_q)≤q κ² I_(F_q).

Let B_q:F_q→F_(q+2) be the restriction of B, and define A_q=||B_q||². Set A_−2=A_−1=0. On F_q,

B_q† B_q = B_(q−2) B_(q−2)† + dΓ(KK†)|_(F_q) + vI,

where the first term vanishes at q=0,1. The nonzero singular values of B_(q−2) and its adjoint agree, so its squared norm is A_(q−2), with no shift of the source index. Consequently

A_q ≤ A_(q−2) + q κ² + v.

Iteration separately on the two parities gives, for every s≥0,

A_(2s) ≤ (s+1)v + κ² s(s+1),

A_(2s+1) ≤ (s+1)v + κ²(s+1)².

Equivalently,

||B_q||² ≤ (floor(q/2)+1)v + κ² floor((q+1)²/4).

The q=0 value is exactly v. The q=1 value is exactly v+||K||². For one mode and κ²=|K|², equality holds for every q because the exact norm is |K|²(q+1)(q+2)/4. The bound is therefore sharp as a general statement in terms of v and κ² alone.

## 2. Orthogonal physical embedding and normalization

Choose on each rung the orthonormal singlet and the three orthonormal triplets. Let the singlet correspond to the bosonic vacuum at that rung and each triplet correspond to one boson of its color. The tensor product defines an isometry from the entire physical Hilbert space into the Fock space of d=3N modes. Its image consists of states with at most one boson per rung, including across different colors. Let P be the orthogonal projection onto this image. The triplet-count operator Q equals the total bosonic number under this isometry.

For one unit straight inter-rung exchange V=S_(i,0)·S_(j,0)+S_(i,1)·S_(j,1), direct evaluation in that orthonormal basis gives its number-raising part

V_+|s_i s_j⟩ = (|t_i,0 t_j,0⟩ − |t_i,+ t_j,−⟩ − |t_i,− t_j,+⟩)/2.

There are no other local q-to-q+2 matrix elements. This identity is independently rebuilt from the four physical spin-1/2 computational basis in `audit_bosonic_tail.py`, with the normalized singlet and t0 columns containing 1/sqrt(2). It is not inferred from an unweighted norm in the production code's unnormalized dimer coordinates.

Let w_ij be the combined multiplicity of each unordered graph edge and A its symmetric weighted adjacency. Let J be the symmetric orthogonal color matrix with J_00=1 and J_+−=J_−+=−1. With K=(g/2) A⊗J, the operator B above is

B = Σ_(unordered edges i,j) (g w_ij/2) Σ_(a,b) J_ab a_(i,a)† a_(j,b)†.

The factor 1/2 in the ordered matrix sum defining B cancels the two graph orientations. The three color terms remain exactly the three physical amplitudes. Thus the full physical creation operator is C_+=PBP on ran(P). Since P and Q commute, orthogonal compression gives

||C_+|_(Q=q)|| ≤ ||B_q||.

Bosonic creation may produce more than one boson at a rung. Those output components are removed by P and can only increase the unrestricted norm. This is the correct direction of the comparison.

Every weighted graph degree is four, including sides of length two. Hence A has constant-vector eigenvalue four and ||A||≤4 by the row-sum bound. Therefore ||A||=4, ||J||=1, and one may take κ²=4g². Since Tr(A²)=2Σ_e w_e² and Tr(JJ†)=3,

v = (3g²/4) Σ_e w_e².

Parallel bonds must be combined before squaring. Their creation images are the same vector, not orthogonal vectors. For both sides at least three, all edges have weight one and v=3Ng²/2. On 2×2 there are four edges of weight two, so v=12g². On 3×2 there are six edges of weight one and three of weight two, so v=27g²/2. All of these vacuum norms are checked exactly.

## 3. Safe diagonal and off-diagonal Jacobi inputs

The exact local preserving block satisfies V_pres≥−(Q_i+Q_j)/2. This follows directly from its three occupancy blocks and is independently checked by rational inertia of the full normalized 16×16 matrix. Summing over weighted degree four gives

H′_(q,q) ≥ (1−2g)q I.

The previous occupancy norm bound is compatible with the same orthonormal representation. Each column of the absolute creation matrix has weighted sum at most (3g/2) E_empty,upper(q). Each row has weighted sum at most (g/2) E_occ,upper(q+2). The latter may overcount occupied edges whose colors are not coupled by J, which is safe. The row-column norm bound therefore gives

||C_+|_(Q=q)||² ≤ (3g²/4) E_empty,upper(q) E_occ,upper(q+2).

The two independent upper bounds may be combined pointwise as

t_q² = min{(3g²/4) E_empty,upper(q) E_occ,upper(q+2),
            (floor(q/2)+1)v + 4g² floor((q+1)²/4)}.

For a vector ψ=Σ_j ψ_j in the compression Q≥q, put x_j=||ψ_j||. Cauchy-Schwarz and the off-diagonal norm bound imply

⟨ψ,H′ψ⟩ ≥ Σ_(j≥q) (1−2g)j x_j² − 2Σ_(j≥q) t_j x_j x_(j+2).

The scalar comparison separates into both parity chains starting at q and q+1. The lowest lower endpoint from those two chains bounds the entire compression. Off-diagonal entries are −t_j. A proposed endpoint ℓ is rigorously below a chain spectrum when the exact rational pivots

p_0=d_(j0)−ℓ,

p_r=d_(jr)−ℓ−t_(j_(r−1))²/p_(r−1)

are all positive. Only t_j² enters this test, so irrational square roots do not enter acceptance.

The graph uppercounts in the frozen files use the previously reviewed isoperimetric and bipartite estimates, independently reconstructed here. If h=min(q,N−q), then e(q)≤2q−min(ceil(2sqrt(h)),nx,ny). For the simple even-sided shapes in these files, e(q)≤min(2q,floor(q²/4)) and the complementary identity e(q)=4q−2N+e(N−q) supply two further upper bounds. Their minimum is again an upper bound. The empty-edge upper count is 2N−4q+e_upper(q). None of these saved arrays is asserted to be the exact occupancy maximum.

## 4. Whole-space spectral counting

The physical q-particle shell has dimension m_q=C(N,q)3^q. The compression Q≥q has codimension D_q=Σ_(j<q) m_j in the full 4^N-dimensional Hilbert space. Courant-Fischer therefore gives

λ_(D_q+1)(H′) ≥ a_q,

where a_q is any lower bound of that compression. This is a lower bound on the next full-space ordered eigenvalue, not a claim that Q is conserved by H′. Since ordered eigenvalues are nondecreasing, a_q can safely be replaced by max_(j≤q) a_j.

Assigning the resulting a_q to m_q consecutive ordered indices yields a complete lower spectral sequence. Its multiplicities sum to 4^N. In particular D_2=1+3N and

λ_(2+3N)(H′) ≥ a_2.

Any full low-band or heat-trace calculation using these bins must separately establish its retained-band eigenvalue enclosures and replay its trace, scalar recurrence, and finite-size bridges. Acceptance of the new tail inputs alone does not certify a new gap.

## 5. Independent executable checks

The acceptance script imports no producer module. It preserves and checks all 18 producer files plus the 18:23 manifest, whose SHA-256 is `4bc8db06b3695b37f01dd12b63eb15476853b5dfe5d5bd772897e6d32d81a08e`.

The Fock tests use factorial Gram metrics for unnormalized monomials and the exact corresponding adjoints. Hermitian positivity for complex matrices is checked through an exact rational realification. They include a complex single mode, a complex symmetric nonnormal matrix, three identity modes, and the producer's real symmetric example. Physical tests reconstruct the orthonormal four-spin exchange independently and verify exact equality with hard-core compressed creation, the exact vacuum norm, and rational positivity of the proposed norm bound minus C†C.

All frozen Jacobi diagonals, both off-diagonal bounds, their minima, both parity chains, every saved LDL pivot, every shell multiplicity, every first ordered index, and monotonicization are recomputed with exact integers and fractions. Floating eigensolvers are used only for labeled diagnostic norm values and the old occupancy-only a2 comparison. They do not enter acceptance.

Reproduce with `bash REPRODUCE.sh`. Computation is pinned to one available CPU, BLAS and OpenMP threads are one, and the address-space limit is 1.5 GiB. Review outputs remain in this directory. No producer file or remote state is changed.
