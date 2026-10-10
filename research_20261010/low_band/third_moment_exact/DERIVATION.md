# Exact additional numerator contraction

2026-10-10 17:06 EDT / 21:06 UTC. Producer derivation and checks, independent review pending.

## Model, convention, and support

The model is the ordinary spin-1/2 square bilayer with periodic rung graph,
including multiplicity-two edges when a direction has length two. Strong
rung coupling is one. Write H′=H+3N/4=Q+tA, t=g/2. The input B comprises the
vacuum and all singlet pair-orbit sums. Its pairing vectors have reduced
inner product 3 per closed loop; the common factor 2^N in the older rational
dimer convention is removed. L=A42 B_pair, R=A44 L, and M=A64 L have q=4,4,6.

The matching action of A in a fixed occupied sector has two contributions.
An occupied/empty graph edge hops the occupied label. For an occupied edge
(i,j), the spin-one interaction is permutation minus singlet contraction.
On a matching where i,j are paired it gives −2 times the same matching.
Otherwise, with partners k,l, it gives matching (i,l)(j,k) minus (i,j)(k,l),
with all other pairs unchanged. This is the same local rule for q=4 and q=6.
It is verified against the local matrix obtained by conjugating both physical
spin-layer bonds with the orthonormal singlet/triplet change of basis.

For a six-site matching with pair multiplicities m1,m2,m3 and orbit labels
j1,j2,j3, the M coefficient is

    2(m2 m3 e_j1 + m1 m3 e_j2 + m1 m2 e_j3).

The factor two counts the two orders of the two creation operations.
Consequently only six-site sets containing two disjoint graph edges can
contribute when M occurs as bra or ket.

## New geometry

Existing F=L*L, S=L*R, V=R*R, W=M*M are retained exactly. Compute

    X=R* A44 R,    Y=R* A46 M=(A64 R)*M,    Z=M* A66 M.
    T=X+Y+Yᵀ+Z.

X and Z must be symmetric; Y need not be. The exact new reusable data can
be reduced to the one symmetric n×n matrix T (n=14 on 8×8); X/Y/Z are kept
separately for independent checks. No q≥8 sector participates in these
expectations. In particular no vector A86 M is constructed or claimed zero.

For every translation-invariant entry density f on q-site subsets,

    Σ_all S f(S) = (N/q) Σ_S containing site 0 f(S).

This follows by summing over all N translations: each q-site subset contains
the origin after exactly q translations, with multiplicity, even for subsets
with stabilizers. The coefficient/matching metric contraction is invariant,
not just the count of sites. Both generating translations preserve every
graph multiplicity and every pair-orbit label in all five geometry inputs;
verify_fixtures.py checks this. Full and fixed-origin contractions coincide
entry by entry on 2×2, 4×2, 4×4. The final N/q rescaling checks divisibility.

The implementation caches all q4 R matching coefficients, remapping the
matching labels when a hopped source is sorted. At q6 it streams the sorted
fixed-origin support list, evaluating M, A66 M, and A64 R locally. It stores
no physical 8×8 state dictionary and no q6 amplitude cache.

## Third moment of the original B+L trial

Let ψ=Bb+Lc, with reduced norm nψ. Set a to the exact B coordinates of H′ψ,
which are obtained from the first rows of the original K matrix divided by
the B Gram diagonal and the integer Hamiltonian denominator. Set

    u=4c+t b_pair.
    H′ψ=B a + (L u+tR c) + tM c.

With H_B=B*H′B, the exact unnormalized third moment is

    a*H_B a + 2t a_pair*(F u+t S c)
    +4(u*F u+2t u*S c+t² c*V c)
    +t u*S u+2t² u*V c
    +6t² c*W c+2t² u*W c+t³ c*T c.

Divide by nψ to get μ3. Let ρ=μ1 and v=μ2−ρ². Then r=(H′−ρ)ψ satisfies

    ⟨r,H′r⟩/nψ = μ3−2ρμ2+ρ³.
    R_res=(μ3−2ρμ2+ρ³)/v.

The exact rational two-vector pencil in normalized-original coordinates is

    Gram = diag(1,v),   H = [[ρ,v],[v,v R_res]].

The saved filter selects an explicit rational coefficient for ψ−s r. Its
Rayleigh upper endpoint is verified by exact Fraction arithmetic using the
existing optimize_filter implementation. This is a variational upper bound,
not a filtered residual bound and not a physical lower spectral endpoint.

## Full enlarged numerator search

For t>0, span(B,H′B,H′²B)=span(B,L,U), where U=R+M. With F_e=[0;F]
and S_e=[0;S], the exact matrices are

    G = [[G_B,0,0], [0,F,S], [0,S,V+W]],

    H = [[H_B,tF_e,tS_e],
         [tF_eᵀ,4F+tS,4S+t(V+W)],
         [tS_eᵀ,4S+t(V+W),4V+6W+tT]].

Exact Gram LDL selects independent columns; ranks are 16,43,43 on
4×4,8×4,8×8. A floating generalized eigensolver only proposes coefficients.
Those coefficients are rounded to integers at 56-bit scale, and their
Rayleigh quotient is recomputed as an exact rational number. The saved
G/K/coefficients are sufficient to replay that upper bound without trusting
the eigensolver. The original T=den H′ base moments M0..M4 are reconstructed
as all applicable block-Hankel products, and the new integer M5 is exported.
The separate sector formula for the original trial's H′³ agrees exactly
with the enlarged matrix construction.

This enlarges a search space; exactly one trial state is retained in the
largest-seed numerator. It supplies no residual of that state, no base M6,
and no change to denominator ground lower bounds or omitted-state counts.

## Integer safety

Pair multiplicities are at most two. A coarse component bound for L is four;
for R it is below 500, for M below 24, for A44R below 100,000, for A64R
below 50,000, and for A66M below 50,000. These bounds follow by counting at
most 4q directed occupied hops and q(q−1)/2 occupied-edge actions, each
having at most two signed outputs per matching. Thus the int32 coefficient
temporaries are safe for the fixed input limits N≤64, d≤14, q≤6. Geometry
matrix accumulation uses checked signed 128-bit addition. Subsequent trial
arithmetic uses Python arbitrary-precision integers and Fraction; large
rounded trial coefficients are never accumulated in 128-bit C++ scalars.
