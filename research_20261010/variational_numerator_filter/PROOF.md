# Optional variational heat-trace numerator filter

Updated 2026-10-10 15:00 America/New_York (EDT, UTC−4) / 19:00 UTC.

Status: exact producer candidates and exact producer tests pass; independent audit pending. This note proves a new variational upper-energy endpoint. It does not certify a complete thermal ratio, scalar recursion, all-size bridge, or new physical gap by itself.

## 1. Model, input, and normalization

The model is the ordinary spin-1/2 square bilayer: unit vertical exchange, equal positive straight intralayer exchange g in both directions, no crossed exchanges, periodic nx×ny rungs, and one edge in each positive direction. Directions of length two therefore have parallel edges. Let N=nx ny, E00=−3N/4, and H′=H−E00. The physical Hilbert-space dimension is 4^N.

The existing one-block ground trial basis has a q=0 vacuum, spatial orbit sums B of q=2 spin-singlet pairs, and L=A42 B at q=4, with H′=Q+(g/2)A. The basis dimensions are 11,29,29 for 4×4,8×4,8×8. All its vectors have total spin zero, even triplet parity, and zero momentum. Those statements and the complete geometry moments are inherited from the independent `large_seed_review/REVIEW.md`.

The stored matrices G, K, J mean exactly

Gij=⟨vi,vj⟩/2^N,
Kij=den ⟨vi,H′vj⟩/2^N,
Jij=den² ⟨H′vi,H′vj⟩/2^N.

J contains the complete q=6 leakage. It is not the square of the projected first moment. The common factor 2^N cancels from all quotients. For a nonzero stored integer coefficient vector c, n=cᵀGc>0 and the normalized physical vector ψ=(Σ ci vi)/sqrt(2^N n) has

ρ=cᵀKc/(den n),
σ²=cᵀJc/(den² n)−ρ².

Only those three matrices and the existing integer coefficients are used by the basic variant. The sharper variant also reads the already available geometric contractions F,S,V,W; it does not compute new Hamiltonian moments or expand a production physical vector. In particular, the saved M3/M4 fields in source files are not accessed by the consumer.

## 2. A residual direction without constructing a residual

Define r=(H′−ρ)ψ. Self-adjointness and the exact definition of ρ give ⟨ψ,r⟩=0 and ||r||²=σ². A local exchange changes triplet number by 0 or ±2. Hence ψ is supported at q=0,2,4 and r at q=0,2,4,6. The full r, not a projected residual, is meant here.

Suppose an exact upper bound R satisfies ⟨r,H′r⟩≤R σ². The global compressed upper bound below is sufficient; a state-specific expectation bound is also sufficient. Write C=R−ρ and assume C>0. For t≥0 the physical vector

φ(t)=(ψ−t r)/sqrt(1+t²σ²)

is normalized. The identities ⟨ψ,H′r⟩=σ² and ⟨r,H′r⟩−ρσ²≤Cσ² give

⟨φ(t),H′φ(t)⟩ ≤ ρ + σ²(−2t+C t²)/(1+t²σ²).

For σ²>0, choose a rational δ>0 such that δ(C+δ)≤σ² and set t=δ/σ². Substitution proves the upper endpoint

⟨φ(t),H′φ(t)⟩≤ρ−δ<ρ.

The best endpoint allowed by this two-dimensional comparison has δ*=(sqrt(C²+4σ²)−C)/2. We enclose this from below by an exact integer-square-root operation and verify δ(C+δ)≤σ² with fractions. No floating eigensolver enters acceptance. As a safe fallback for an arbitrarily tiny nonzero variance, δ0=σ² C/(C²+σ²)>0 obeys the same quadratic inequality. For σ²=0 the original endpoint ρ is retained.

The filtered vector is still spin zero and even parity, so it remains orthogonal to every spin-one/odd-parity trial used in the existing lower-trace family. Its residual is not computed or bounded. No eigenvalue lower endpoint or Temple bound for φ is asserted.

## 3. Exact local upper bound in orthonormal coordinates

Use the normalized singlet and three normalized triplets on each rung. The single inter-rung operator is

V=S(i,0)·S(j,0)+S(i,1)·S(j,1).

Its number-preserving part has the following occupancy blocks:

- qlocal=0: zero
- qlocal=1: hopping blocks with eigenvalues ±1/2
- qlocal=2: (1/2)Ti·Tj, with eigenvalues −1,−1/2,+1/2

Thus Vpres≤(Qi+Qj)/2. Each graph vertex has weighted degree four, including parallel-edge multiplicity. Summing gives Pq H′ Pq≤(1+2g)q Pq.

The producer test independently constructs the four-spin exchange in the standard orthonormal computational basis, transforms with normalized singlet/triplet columns, and verifies the full 16×16 rational inequality by exact inertia. It also verifies all local number changes, orthonormality, and the normalized pair-creation coefficients (+1/2,−1/2,−1/2). These checks avoid treating the unnormalized rational production dimer coordinates as Euclidean coordinates.

## 4. Upper Jacobi comparison on even q≤6

The independently reviewed bosonic pair bound supplies

||P(q+2) H′ Pq||² ≤ bq=(floor(q/2)+1)v+κ² floor((q+1)²/4),

v=(3g²/4)Σe we², κ²=4g².

Here we is the combined multiplicity of an unordered edge; multiplicities must be combined before squaring. This is the hard-core orthogonal compression of a bosonic creation operator, as proved in `bosonic_tail_review/PROOF.md`. Its normalization agrees with the local physical kernel above.

For xq=||Pq u|| and u supported on q=0,2,4,6, Cauchy–Schwarz gives

⟨u,H′u⟩≤Σq(1+2g)q xq²+2Σq=0,2,4 sqrt(bq)xq x(q+2).

Therefore the maximum eigenvalue of the four-by-four Jacobi matrix with diagonal (1+2g)q and positive off-diagonal sqrt(bq) bounds the compression from above. If R I−Jplus has positive rational LDL pivots

p0=R−d0,
pj=R−dj−b(previous q)/p(j−1),

then R is a strict upper bound. Only off-diagonal squares occur, so no irrational arithmetic is needed. Rational binary search finds such an R; the saved pivots themselves are the certificate. For N<6, truncate the even chain at the largest available q.

The expectation ⟨r,H′r⟩ only involves the compression to r's support. H′r could have q=8 components, but these are orthogonal to r and do not affect the expectation. The proof never discards an overlapping component.

## 5. Sharper q-resolved expectation from existing geometry

Let D be the diagonal Gram matrix of B, and write coefficients as cB,cL, reinserting zero coefficients for any unselected basis columns. The full residual in q≤2 lies in B because B contains the full spatially invariant spin-singlet q≤2 subspace. Thus its coordinate vector there is

u=D⁻¹ K(B,all)c/den−ρ cB.

Consequently w0=D00 u0²/n and w2=Σi≥1 Dii ui²/n are exactly ||P0r||² and ||P2r||².

Using the previously reviewed definitions F=L*L, S=L*A44L, V=(A44L)*(A44L), W=(A64L)*(A64L), all with 2^N removed, put

h=(g/2)cB,pairs+(4−ρ)cL.

Then the two remaining squared norms are exactly

w4=[hᵀFh+g hᵀS cL+(g²/4)cLᵀV cL]/n,
w6=(g²/4)cLᵀW cL/n.

Each candidate explicitly verifies wq≥0 and w0+w2+w4+w6=σ² with exact fractions. This last identity checks all sectors and the common normalization; it does not assume that leakage vanishes.

The direct scalar upper estimate is

⟨r,H′r⟩ ≤ Σq(1+2g)q wq + 2Σq=0,2,4 sqrt(bq wq w(q+2)).

Each square root is rounded upward on a rational grid and its squared upper endpoint is checked against the exact radicand. Divide the resulting expression by σ² to obtain a state-specific R. The smaller of this R and the global R is used. It need not bound H′ on every vector: an upper expectation for this particular r is exactly what Section 2 requires.

## 6. Thermal use and limitations

For β>0 and the normalized filtered vector, scalar Jensen applied to its spectral measure gives

Tr exp(−βH′)≥⟨φ,exp(−βH′)φ⟩≥exp(−β⟨φ,H′φ⟩)≥exp(−β(ρ−δ)).

This contribution can be added to expectations from an orthonormal spin-one trial family, because the filtered ground vector remains orthogonal by exact symmetry. Equivalently, the variational principle gives E0(H′)≤ρ−δ. Any proposed trace ratio greater than one must be rejected and investigated, never clipped to one.

The original minimal first-moment-only route is unchanged. This is an optional improvement whose input contract explicitly requires existing full second moments. It retains one implicit filtered trial state. The filter plane span{ψ,r} has dimension at most two; adjoining r to the original trial space would have dimension at most 12,30,30 and q≤6 support. Thus the new filtered vector need not lie in the original 11/29/29-dimensional q≤4 space, even though no new vector is stored or expanded. It neither increases the counted retained spectral band nor supplies a residual certificate for that filtered state.

All saved coupling points from 0.03 through 0.10 are discrete candidates. No coupling-interval statement follows from the list. These files alone do not improve a global gap: numerator replacements, denominator enclosures, complete tails, recursion and finite-size bridges must still be recombined and independently checked.

## 7. Executable verification

`REPRODUCE.sh` rebuilds all 21 candidates and runs exact producer tests. Tests include the normalized four-spin upper inequality and support selection rule; actual filtered Rayleigh quotients on three tiny 2×2 physical fixtures with doubled edges; exact orthogonality and normalization; zero variance and a variance of 10^−60; and byte-independent recomputation of each saved candidate dictionary.

The tiny physical vectors are test fixtures only. Production candidates use no new physical vector, no new geometric contraction, and no H³/H⁴ input. Runs are pinned to one CPU, with BLAS/OpenMP thread counts one and a 1 GiB address-space cap. No upstream file or remote repository is changed. The active workspace is an extracted tree without Git metadata; its source revision and source hashes remain those recorded in the existing root checkpoint.
