# Bosonic comparison for number-changing rung couplings

2026-10-10 14:20 America/New_York / 18:20 UTC. This lemma bounds number-changing rung interactions through a bosonic embedding. Internal exact checks are complete. Independent review is required before the bound enters a released gap certificate.

## Pair creation as a hard-core compression

Use an orthonormal singlet/triplet basis on each spin-1/2 rung. Embed the physical
basis into the bosonic Fock space of three modes per rung. A singlet is the vacuum,
and each triplet is one boson of the corresponding color. Physical states have
at most one boson per rung. Let P be this hard-core projection, and Q the total
boson number, equal to the triplet count on the physical subspace.

For a weighted rung edge i,j of multiplicity w_ij, the q-to-q+2 piece of the
ordinary bilayer exchange is

    (g w_ij/2) (t_i,0^dagger t_j,0^dagger
                -t_i,+^dagger t_j,-^dagger -t_i,-^dagger t_j,+^dagger).

These coefficients follow from the physical two-rung matrix already used in the
local number-sector audit. Write J for the symmetric orthogonal 3x3 color matrix
with J_00=1 and J_+-=J_-+=-1. If A is the weighted adjacency matrix of the rung
graph, define K=(g/2) A tensor J. This is a real symmetric matrix. The unrestricted
bosonic pair creation operator is

    B = (1/2) sum_(u,v) K_uv a_u^dagger a_v^dagger.

There are no graph loops. The factor 1/2 cancels the two orientations of each
edge. The exact physical creation operator is C_+=PBP restricted to the
hard-core Hilbert space. Consequently its q-to-q+2 operator norm is no larger
than that of B on the entire q-particle sector. This is an orthogonal physical
embedding. No unnormalized coordinate norm is being substituted.

## A number-resolved bound for arbitrary bosonic pair creation

Let K be any finite complex symmetric matrix, and let B be as above. Set

    kappa^2 >= ||K||^2,
    v = (1/2) Tr(K* K) = ||B vacuum||^2.

The canonical bosonic commutation relations give

    [B*,B] = a* K K* a + v I.

For completeness this can be verified by expanding
[a_u a_v,a_r* a_s*]. Moving both annihilators to the right leaves the four
single contractions, which sum to a*KK*a, and the two double contractions,
which sum to Tr(K*K)/2. On the q-particle sector,

    0 <= a*KK*a <= kappa^2 q I.

Let A_q=||B|_(Q=q)||^2, and set A_-1=A_-2=0. Since B* lowers number by two,

    A_q = ||B*B|_q||
        <= ||BB*|_q|| + kappa^2 q + v
         = A_(q-2) + kappa^2 q + v.

The equality of the two nonzero squared singular-value norms identifies
||BB*|_q|| with A_(q-2). The cases q=0,1 have B*|_q=0. Iterating the inequality
therefore gives the exact formula

    A_q <= (floor(q/2)+1) v + kappa^2 floor((q+1)^2/4).

For even q=2s this is (s+1)v+kappa^2 s(s+1). For odd q=2s+1 it is
(s+1)v+kappa^2(s+1)^2. The bound is sharp for a single bosonic mode.

## Specialization to periodic square bilayers

The weighted adjacency has constant degree four, hence ||A||=4 and one may take
kappa^2=4g^2. Since J*J=I_3,

    v = (3g^2/4) sum_(unordered edges e) w_e^2.

For a simple torus with both sides at least three, there are 2N edges and thus
v=3Ng^2/2. Length-two periodic parallel edges are combined into w_e=2 before
squaring. They must not be counted as separate orthogonal pair-creation images.
The implementation computes the weighted graph explicitly.

Combine this bosonic upper bound with the previous safe occupancy bound by
setting

    t_q^2 = min{ (3g^2/4) Eempty_upper(q) Eocc_upper(q+2),
                 (floor(q/2)+1) v + 4g^2 floor((q+1)^2/4) }.

Both entries upper-bound the same physical squared norm, so their minimum does
too. The diagonal block inequality H'_qq >= (1-2g)q and every subsequent
Jacobi-chain/LDL/min-max count are unchanged. Both parity chains of each
compression Q>=q must still be checked. This is a whole-space tail bound, not
an assumption that total triplet number is conserved.

On N=64 at g=.06, for example, v=.3456 and the new q=2 bound is .72. The old
occupancy expression at q=2 is 1.3392. No many-body diagonalization or new trial
moment is needed to exploit this improvement.
