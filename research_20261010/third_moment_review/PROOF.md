# Exact third moment, enlarged numerator, and all-integer certificate

Independent review, 2026-10-10. This is an analytic proof with independently replayed exact-arithmetic certificates, not a formal proof-assistant verification.

## 1. Model and normalization

The model is the ordinary spin-1/2 periodic square bilayer. Rung exchange is one, every straight intralayer bond in either layer has exchange g, and there are no crossed bonds. Both positive-direction periodic bonds survive in a length-two direction. If N=nx ny, the physical Hilbert space has dimension 4^N=2^(2N), and

H′ = H + 3N/4 = Q + t A,    t=g/2.

An orthonormal rung basis consists of the singlet and three spherical triplets. The independent audit constructs the 16-by-16 inter-rung operator directly from the two physical spin-layer exchanges and conjugates by the orthonormal rung transform. Its A=2V entries are integral and symmetric; a nonzero matrix element changes total triplet number by 0 or ±2. Different occupied-site supports, in particular different q sectors, are orthogonal.

The original rational-dimer convention has a common Gram factor 2^N. The stored matrices remove that factor. Our direct orthonormal physical tests reproduce the reduced matrices without this factor, so ratios and moment normalizations agree. No Euclidean norm is assigned to an unnormalized rational dimer vector.

B comprises the vacuum and every translation/point-symmetry orbit sum of two-triplet spin singlets. The pair orbits are classified by periodic unsigned displacements, with x/y exchange only for square shapes. For each occupied pair, its spin-zero subspace is one-dimensional. Thus B exhausts the q≤2, spin-zero spatial-invariant subspace. This is why projecting any relevant Hamiltonian image to q≤2 loses no physical component. H′ preserves spin zero, even parity, and the spatial symmetries.

Write n for the number of pair orbits, and distinguish the following maps:

L=A42 B_pair, R=A44 L, M=A64 L, U=R+M.

L and R have q=4; M has q=6. The same column index labels the original pair orbit throughout.

## 2. Exact invariant-tensor contraction

A matching of 2k triplet sites is the product of k unnormalized spin-zero pair tensors. In spherical coordinates a pair has coefficients −1,+1,−1 on (t−,t+), (t0,t0), (t+,t−). Contracting two matchings gives 3 to the number of closed loops in their union. This includes all signs and spin multiplicities; it is not a count of only classical occupations.

The independent physical tests enumerate every q=4 and q=6 matching and verify every overlap: 3 matchings at q=4 and 15 at q=6. They also test every occupied bond on every matching against the spin-derived local operator. On an occupied pair already matched to each other, A gives −2 times that matching. On sites i,j with distinct partners k,l, it gives the matching (i,l)(j,k) minus (i,j)(k,l), retaining all other pairs. Across an occupied/empty bond it hops the occupied label with coefficient equal to the bond multiplicity. A vacuum bond creates the pair tensor with the same multiplicity.

Consequently, on a six-site matching with paired edges e1,e2,e3, multiplicities w1,w2,w3 and pair-orbit labels j1,j2,j3, the M coefficient is

2(w2 w3 e_j1 + w1 w3 e_j2 + w1 w2 e_j3).

The factor two is the two orders of the two pair creations. Parallel bonds enter through their integer multiplicities before products or contractions are taken. Repeating the same occupied endpoints does not create another pair. Every nonzero M support contains two disjoint geometric edges. Conversely, the audited coefficients are nonnegative, so such a support has a nonzero coefficient. Skipping a support on which every M coefficient vanishes is exact whenever M is one of the two contracted factors.

Define the existing matrices

F=L*L, S=L*R, V=R*R, W=M*M,

and the new matrices

X=R* A44 R, Y=(A64 R)*M=R* A46 M, Z=M* A66 M.

X and Z are symmetric. Y need not be. All old F/S/V/W entries match the previously accepted physical geometry exactly.

The new auditor does not import or execute producer code. It caches the q=4 R coefficients, but independently contracts X and Z using precomputed local bond bilinear forms, rather than producing and then contracting the producer's second images. It enumerates every q=6 subset containing the origin and evaluates whether M is zero; it does not reuse the producer's reachable-edge-mask construction. At 8×8 this examines all C(63,5)=7,028,847 origin supports, of which 992,424 contribute. All seven resulting matrices agree entry-for-entry. Independent full-support and origin calculations also agree on 2×2, 4×2, and 4×4.

### Fixed-origin factor and stabilizers

For any matrix-entry contraction density f(S) invariant under all N translations, let T=Σ_|S|=q f(S) and T_i=Σ_(S contains i) f(S). Translations biject supports and preserve their edge multiplicities, orbit labels, pairing metrics and operator action, so every T_i is equal. Double-counting the incidences (i,S) gives

N T_0 = Σ_i T_i = q T,

hence T=(N/q)T_0. This does not assume that a support has N distinct translates. Periodic repetitions and nontrivial stabilizers are already counted correctly. In a single translation orbit O, q|O|=N·#{S in O:0∈S}; no additional stabilizer divisor is allowed.

The audit explicitly checks every translation orbit of q=4 and q=6 subsets on the small fixtures, including stabilizers of size two and four. It independently checks that both generating translations preserve every weighted edge and every pair-orbit index on all five geometries. The final integer divisibility by q is checked before every N/q rescaling.

### Integer safety

For the fixed limits N≤64, n≤14, q≤6 and weighted degree four, conservative component bounds are |L|≤4, |R|≤256, |A44R|≤16384, |M|≤24, |A64R|≤9216 and |A66M|≤9216. For example a q=4 site set has at most 16 weighted outgoing hops and total internal edge weight at most eight; each local matching action has at most two signed outputs. These deliberately loose bounds put every producer int32 temporary safely within range. The auditor uses int64 coefficients, and both implementations use checked int128 matrix accumulation. Even the crude number-of-supports times matching-count times coefficient bounds stay many orders below the signed int128 limit, including the final multiplication by N. Trial coefficient contractions use arbitrary-precision Python integers and rational fractions.

## 3. Enlarged Gram and Hamiltonian matrices

Let D=B*B=diag(1,3|O1|,…,3|On|), let C be the exact coordinates of P_(q≤2)H′B in B, and put E=[0;I_n], F_e=EF, S_e=ES. Direct graph action independently reconstructs C; D C is symmetric. In the ordered family (B,L,U), the exact matrices are

G = [[D,0,0], [0,F,S], [0,S*,V+W]],

A = [[D C,t F_e,t S_e],
     [t F_e*,4F+tS,4S+t(V+W)],
     [t S_e*,4S*+t(V+W),4V+6W+t(X+Y+Y*+Z)]].

All entries are real, and S=S*. The U/U Gram is V+W because R⊥M. The U/U number contribution is 4V+6W. The L/U interaction contains both V and W: <L,A R>=V and <L,A M>=W. Omitting W from either block discards a physical contribution.

The full H′ image of (B,L) is represented in the enlarged family by

T_old = [[C,t D^−1 F_e], [t E*,4I], [0,tI]].

Here the q≤2 component is exact by the exhaustion argument in §1. Thus G_old, A_old and J_old are respectively the leading Gram block, the leading Hamiltonian block, and T_old* G T_old. The old original-trial third-moment matrix is T_old* A T_old. This independently rebuilds every original G/A/J entry at g=9/100 and the separate third-moment result.

For t>0, H′B gives every L modulo B, and H′L gives every U modulo B+L. Therefore

span(B,H′B,H′²B)=span(B,L,U).

The restriction t>0 matters: at g=0, Q leaves B invariant and the original block Krylov span is only B. A dedicated regression checks this degenerate case rather than extrapolating the positive-coupling rank.

Exact rational Schur elimination gives all positive pivots at g=.09, with ranks 16,43,43 for 4×4,8×4,8×8. No floating rank tolerance is used. The saved integer coefficients are substituted directly into G and A and have positive norm. Their quotients are the exact accepted upper endpoints; the float eigensolver is only a coefficient proposal mechanism.

Using B0=B, B1=H′B, B2=H′²B in these coordinates, all applicable B_i*G B_j and B_i*A B_j reproduce the previously stored integer base moments M0 through M4 after multiplying by the recorded integer Hamiltonian denominator. B2*A B2 independently reproduces the new base M5. There is no M6 claim.

## 4. Original-trial H³ and the rational two-vector state

Let ψ=Bb+Lc, with reduced squared norm nψ. Put a equal to its H′ image's B coordinates and u=4c+t b_pair. Then

H′ψ = B a + L u + tR c + tM c.

Thus μ3=<H′ψ,H′H′ψ>/nψ is exactly the expectation obtained from T_old* A T_old. Decomposing by q gives all q=0,2,4,6 number terms, number-preserving interactions, and both neighboring-sector cross terms. The sum of new terms is t³ c*(X+Y+Y*+Z)c; no term is silently discarded.

For a normalized original ψ with ρ=μ1, v=μ2−ρ² and r=(H′−ρ)ψ, one has

<ψ,r>=0, <r,r>=v, <ψ,H′r>=v,

z=<r,H′r>=μ3−2ρμ2+ρ³.

The exact two-vector Gram and Hamiltonian matrices are diag(1,v) and [[ρ,v],[v,z]]. Write C=z/v−ρ. Every saved rational gain δ>0 satisfies δ(C+δ)≤v, and α=δ/v. Direct evaluation of φ=(ψ−αr)/sqrt(1+α²v) yields energy at most ρ−δ. The audit checks the exact quotient, denominator, discriminant-grid direction, fallback gain and slack. No floating eigenvalue is accepted as a bound.

### Why q≥8 is irrelevant here, and why it matters for a residual

H′ changes q by at most two, so H′ψ has support q≤6. Its next image can have q=8, but that component is orthogonal to the bra H′ψ. Therefore <H′ψ,H′H′ψ> is exactly unchanged by discarding q≥8 from the second factor. Similarly U has q≤6, so <U,H′U> needs only the q≤6 compression. This is support orthogonality, not an approximation, a smallness assumption, or a claim that A86M vanishes.

The unrestricted 4×2 physical test explicitly produces a nonzero q=8 component of H′²ψ. With the test's integer Hamiltonian scaling, its squared norm is 76,187,381,760. It changes the fourth moment <H′²ψ,H′²ψ>, but does not change the third moment. Thus neither the two-vector Rayleigh bound nor the enlarged G/A data certify the new state's full residual or a denominator spectral lower endpoint.

## 5. Thermal use and the separate g=.09 certificate

For any normalized trial state φ and β>0, spectral Jensen gives

Tr exp(−βH′) ≥ <φ,exp(−βH′)φ> ≥ exp(−β<φ,H′φ>).

Consequently one accepted Rayleigh upper bound supplies one rigorous numerator contribution. A 43-dimensional search is not 43 retained levels. No residual, low-energy count, or lower energy bound is needed for this numerator.

The scalar audit is separate from the physical audit. It checks that the 4×4 and 8×4 denominator input files are byte-identical to the g=.09 records physically accepted by `bilayer_polynomial_frontier_review`. Their ground search ranks remain 11 and 29, their full physical dimensions are 2^32 and 2^64, and their retained low-band dimensions remain 49 and 97. Their low-energy intervals, full omitted-state tails and uniqueness/count hypotheses are unchanged. The newly verified 16- and 43-dimensional smaller-geometry Rayleigh trials are not used to alter these denominators. In the 8×8 input only the ground upper endpoint is replaced and the old excited numerator terms are removed. The audit uses only exp(−2β E_upper) from this input; it never uses an incomplete 8×8 denominator after that removal.

Write U16(β), U16(2β), U32(2β) for the complete denominator trace upper bounds, and l64(2β) for that single numerator lower term. The three lower ratio witnesses are independently rebuilt as

J1=l64(2β)/U16(β)^8,
J2=l64(2β)^2/U16(2β)^8,
C0=l64(2β)/U32(2β)^2.

All physical energy shifts cancel because their extensive volumes and inverse temperatures match. The audit uses 512-bit outward integer/rational exponential enclosures from an unchanged hash-pinned independent implementation. Every saved downward ratio is checked against these enclosures.

The joint-product and order-transport inequalities are the already independently accepted analytic lemmas in `joint_ratio_review`. The exact scalar functions used here come unchanged from the accepted independent polynomial-frontier auditor, not from producer modules. For each update the current raw ladder, canonical ladder, joint bound, base geometry and inverse temperature are all recomputed. The two ladders' weighted partition-function monomials agree exactly at the same physical base; no factor from a different basepoint or temperature is substituted. Square roots are lower bounded on an explicitly checked rational grid.

Every finite window is reconstructed using the accepted joint-aware interpolation theorem, and its positive gap is checked with a directed exponential inequality. The two variants cover:

- Two-vector: β_initial=89/10, windows [8,16], [16,32], …, [1024,2048], followed by the all-integer small-defect theorem from L=2048 at β=22784/5.
- Enlarged numerator: β_initial=35/4, windows [8,16], [16,32], [32,64], [64,128], followed by that theorem from L=128 at β=280.

The final same-base defects satisfy 0<u≤1/500. The saved asymptotic gap d is accepted by the strict inequality exp(β_terminal d)·32u<1, with upward rounding of both u and the exponential. The theorem's domain constants are checked explicitly. An additional terminal finite window is verified but is not required in the final minimum.

For L=2,…,7, the inherited quadratic comparison is independently rechecked uniformly for 0≤g≤.10, including the period-two square sum 16 and all edge-square sums [16,18,32,50,72,98]. With α=4/5, a rational δ≤sqrt(3/5), and v=147/200, its positive gap lower bound is δ−v/(α+δ)>0. The singlet product has H′ expectation zero. This establishes the short-size gap and uniqueness without assuming monotonicity of the physical gap in g.

Taking the minimum over the short sizes, every required finite window, and the asymptotic tail gives, for every integer square side L≥2 at g=.09,

- two-vector numerator: gap ≥ 0.001111944974;
- enlarged numerator: gap ≥ 0.027330086079.

Each finite volume has a unique ground state. These are sufficient lower certificates at one coupling, not the actual gap, an optimal coupling frontier, a new continuous-coupling interval, an arbitrary-aspect-ratio claim, or infinite-volume uniqueness. The g=.10 files in the producer's scalar seal remain unaudited bounded floating diagnostics here; their failures do not exclude other temperatures or methods.
