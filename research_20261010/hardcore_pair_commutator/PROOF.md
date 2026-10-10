# Exact hard-core pair commutator and the missing q8 norm

2026-10-10. Analytic derivation and independent exact-integer small-fixture verification. No production 8×4 or 8×8 contraction was run. All new files are confined to this directory; prior project artifacts are unchanged.

## Model and operator conventions

Ordinary periodic spin-1/2 bilayer, rung exchange one, straight intralayer exchange g, no crossed bonds. Let N be the rung count, Q the triplet count, H′=H+3N/4=Q+(g/2)A, A=2V. The orthonormal local basis is (s,t−,t0,t+), identified with (0,1,2,3). The physical Hilbert dimension is 4^N=2^(2N).

Write b_ia=|s><a|_i, h_i=|s><s|_i, X_i^{ca}=|c><a|_i. Then exactly

    b_ia b†_ic=δ_ac h_i,
    b†_ic b_ia=X_i^{ca},
    [b_ia,b†_ic]=δ_ac h_i−X_i^{ca}.

Different rungs commute. These are hard-core Hubbard operators, not canonical bosons. Set bar(a)=4−a and s_1=s_3=−1, s_2=+1. The real symmetric spin-singlet metric is J_ab=s_a δ_b,bar(a), so J²=I and sum_ab J_ab²=3.

    P†_ij=Σ_ab J_ab b†_ia b†_jb,
    |Ω_ij>=−|t−t+>+|t0t0>−|t+t−>,
    C†=Σ_{unordered distinct endpoint edges e={i,j}} w_ij P†_ij,
    C=(C†)*.

C† is precisely the q→q+2 block of A, with no factor g, 1/2 or sqrt(3). The independent test constructs A directly from the two physical layer spin exchanges and verifies this block exactly. Each repeated periodic edge is aggregated in w_ij before any product. Thus length-two directions have w=2. There are no self-loops in the considered geometries (side lengths at least two).

## Complete local commutator

Disjoint edges commute. For identical endpoint pairs,

    [P_ij,P†_ij]=3 h_i h_j−|Ω_ij><Ω_ij|.                 (1)

Proof: P_ij P†_ij=3 h_i h_j; P†_ij P_ij=|Ω><Ω|. In particular the negative term is a rank-one operator of eigenvalue 3, not a unit-normalized projector.

For distinct outer endpoints j≠k sharing center i,

    [P_ij,P†_ik]
      =Σ_abcd J_ab J_cd(δ_ac h_i−X_i^{ca}) b_jb b†_kd
      =h_i Σ_b b†_kb b_jb
       −Σ_ac s_a s_c X_i^{ca} b_j,bar(a) b†_k,bar(c). (2)

This is the full spin-index identity; it includes both the empty-center hop and the occupied-center spin-changing term. Equation (2) follows by commuting the outer-rung operators and inserting the single-rung commutator. Its adjoint is the same expression with j,k exchanged. Reversing an edge's written endpoints changes no sign because J is symmetric.

For real bilayer weights the global operator is

    K=[C,C†]
      =Σ_{edges {i,j}} w_ij² (3h_i h_j−|Ω_ij><Ω_ij|)
       +Σ_i Σ_{j,k∈neighbors(i), j≠k}
          w_ij w_ik [P_ij,P†_ik].                    (3)

The wedge sum is ORDERED. Equivalently sum unordered outer pairs and include O_ijk+O_ikj; expectations of real states then have a factor 2. Do not multiply the ordered sum by another two. Aggregating parallel edges yields w² for identical endpoints and w_e w_f for distinct incident edges, including all cross terms between original parallel bond occurrences. If nonphysical complex edge amplitudes were used, these products would instead be conjugate(w_e) w_f with the corresponding orientation of annihilation/creation edges.

## Matching implementation without physical spin enumeration

A matching is a product of unnormalized Ω tensors, with inner product 3 per closed loop in the union. The following rules are exact, as checked independently on all 15 six-site matchings:

- Annihilating sites i,j already paired together gives 3 times the remaining matching.
- If i,j have distinct partners u,v, annihilation joins u,v and has coefficient +1.
- The negative same-edge term annihilates the pair then recreates Ω_ij. Its coefficient is −3 in the first case, −1 in the second.
- An ordered wedge with empty center i hops an occupied outer endpoint j to an empty k, preserving its matching partner, with coefficient +1.
- An ordered wedge with occupied center i, occupied j and empty k annihilates Ω_ij and recreates Ω_ik. It has coefficient −3 or −1 under the two cases above.
- All other occupation patterns vanish. Positive diagonal same-edge contribution is 3 on empty-empty endpoints.

The minus signs of individual spherical components cancel in the matching reconnection because J²=I. They do not cancel the overall negative occupied-center term.

## Exact q8 Gram without constructing q8

For any q6 vectors m_a,m_b, adjointness gives

    <C†m_a,C†m_b>=<Cm_a,Cm_b>+<m_a,Km_b>.             (4)

This follows from CC†=C†C+K; it is valid with arbitrary coherent column combinations. K preserves q, so (4) involves only a q4 norm and q6 local contractions. It is not an assumption that the q8 component vanishes, and K is not generally positive.

For the existing basis, L=A42 B_pair, M=A64 L=C†L. Thus the missing matrix is

    W8=(A86 M)* (A86 M)=(CM)* (CM)+M* K M.

For a trial coefficient vector c, its q8 contribution to the FULL H′ residual squared is (g/2)² c*W8 c divided by the full trial norm. The trial itself has no q8 component, so subtracting its Rayleigh quotient changes nothing in this sector. This result alone does not provide other q4/q6 image norms needed for the complete residual. No denominator lower endpoint or g=.10 gap is certified here.

## Independent tests

verify.py imports no existing producer or reviewer modules. All amplitudes, Gram entries and comparisons are Python exact integers. SymPy is used only to construct the orthonormal physical-rung transform and local physical spin operator exactly.

- Every basis state on the support of identical, overlapping and disjoint edges: 16+64+256=336 tests.
- Every basis state of a four-rung graph with nonuniform signed integer edge weights, testing the complete global commutator: 256 tests. These detect missing w², wedge orientation and duplicate-factor errors.
- All 15 six-site matchings and local contractions: 465 recoupling tests.
- Physical periodic 2×2, 3×2, 4×2 fixtures, constructing B,L,M directly with spin-derived A, then comparing every cross entry of the explicitly enumerated q8 Gram against (4).
- The 3×2 fixture is saturated at q6 and checks exact cancellation to zero, despite a nonzero CM norm.
- The 4×2 fixture has genuine q6→q8 leakage. For pair-orbit ordering given by sorted unsigned displacement and coefficients c_i=(−1)^i(i+1),

      ||C†M_c||² = 3,898,368,
      ||CM_c||²  =18,705,408,
      <M_c,K M_c>=−14,807,040.

  The negative commutator is essential. The full 5×5 q8 Gram is stored in TEST_RESULTS.json and includes nonzero off-diagonal entries. Physical Hilbert dimension here is 4^8=65,536; the five columns are trial vectors, not five retained spectral levels.

These are independently replayable certificates for the local identities and small fixtures, not a formal proof-assistant verification or a large-seed execution result.
