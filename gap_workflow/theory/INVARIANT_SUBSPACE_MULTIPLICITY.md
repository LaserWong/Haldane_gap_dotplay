# Ground multiplicity from an exact invariant-subspace witness

This note gives a sufficient finite-matrix criterion for inferring ground multiplicity without a full characteristic polynomial. A standalone verifier is implemented in gapflow/invariant_witness.py. Automatic witness discovery and CLI integration remain open. The existing low-band, exact-inertia, Sturm and Kramers implementations remain unchanged.

## Setting and sufficient criterion

Let A be an n by n real symmetric rational matrix and let W be a positive-definite rational metric. The physical energies are the generalized eigenvalues of A−λW. Equivalently, they are the eigenvalues of the Hermitian matrix W^(−1/2) A W^(−1/2). The existing model builder uses a positive diagonal W.

Choose rational numbers a < b < t. Exact full-matrix inertia, or the sum over every verified invariant symmetry sector, must establish

- No eigenvalue lies below a.
- Exactly r eigenvalues lie below b, and none equals b.
- Exactly r eigenvalues lie below t, with 1 ≤ r < n.

These conditions certify an isolated bottom cluster in [a,b), but do not by themselves establish degeneracy.

An additional witness consists of rational matrices V ∈ Q^(n×k) and T ∈ Q^(k×k), and a squarefree rational polynomial p. Verify the following exact statements.

1. V has full column rank and AV = WVT.
2. With G = VᵀWV and C = VᵀAV, the restricted pencil C−λG has exactly r eigenvalues in [a,b). This can be checked by its exact inertia at a and b, including endpoint nullities. Under the full-space conditions above it suffices to verify that C−bG has r negative eigenvalues and no zero eigenvalues.
3. p(T) = 0, and an exact Sturm count establishes that p has exactly one distinct real root in [a,b].

An annihilating polynomial suffices. It need not be the minimal polynomial or characteristic polynomial. Checking a proposed p is enough, provided its squarefree property and the stated root count are verified.

Then the true ground energy is the unique root of p in this bracket, its multiplicity is exactly r, and the gap above the ground eigenspace obeys

Δ ≥ t−b > 0.

The count r is obtained from exact inertia. It is not supplied as an assumed ground degeneracy. A root at a is permitted. The upper endpoint b must not be an eigenvalue in this formulation. Excited eigenvalues exactly at t are permitted.

## Proof

Positive definiteness of W and full rank of V imply G > 0. Multiplying AV = WVT by Vᵀ gives C = GT. Since C is symmetric, T is self-adjoint in the G metric and has a real, diagonalizable spectrum. The image of V is an invariant subspace of W^(−1)A, and its generalized energies are genuine full-space energies.

Every restricted energy is a root of p because p(T) = 0. The restricted inertia establishes r energies in the bottom bracket. The root count forces all r of these energies to coincide. The independent full-space inertia establishes that precisely r energies occur in the bracket and none lies below it. Thus the witness exhausts the bottom cluster and establishes its exact multiplicity. The next full-space energy is at least t, while the ground is below b, giving the stated gap bound.

The full-space or complement-completeness step is indispensable. An invariant subspace can omit lower states just as a numerical trial space can. Exact invariance alone does not identify the global ground.

## Proper-subspace example with an irrational ground

Set W = I₆ and define

B = [[−1, 1], [1, 1]],

A = diag(B, B, 3, 4).

Take V to be the first four columns of I₆. This is a proper four-dimensional invariant subspace of the six-dimensional physical space. Its exact restricted matrix is T = diag(B,B), with G = I₄. Direct multiplication verifies AV = VT and

T² − 2I₄ = 0.

Use p(x) = x²−2 and the bracket and cutoff

a = −2, b = −1, t = 1.

The squarefree polynomial p has exactly one root in [−2,−1], namely −sqrt(2). Full inertia at a, b and t is respectively

(negative, zero, positive) = (0,0,6), (2,0,4), (2,0,4).

Restricted inertia at b has two negative eigenvalues and no zero eigenvalues. The criterion therefore infers a ground multiplicity of two and certifies Δ ≥ 2. No ground energy or multiplicity was assumed. Neither a six-dimensional characteristic polynomial nor a full eigenspectrum is needed for this witness check.

The displayed block identities and inertia values are an explicit mathematical example in this note. They are not a claim that a new invariant-witness software path or regression test has been implemented.

## Cost and limitations

For diagonal W, verifying AV = WVT requires approximately O(nnz(A)k + nk²) rational operations. Forming G and C and checking full rank or positive definiteness cost roughly O(nk² + k³). Straightforward verification of a degree-d annihilator costs O(dk³), followed by a univariate exact root count whose cost depends on d and coefficient bit sizes. Sparse structure can reduce these costs. These are arithmetic-operation estimates, not hard runtime or memory guarantees.

The existing full-space inertia or structural complement certificate is still required. This method removes the need for a full characteristic polynomial when a small suitable witness is available. It does not remove the cost of spectral completeness.

Finding such a witness can be substantially harder than verifying it. A rounded floating Ritz basis generally has a nonzero exact invariance residual and is therefore not acceptable. Its entries must not be treated as an exact invariant basis merely because the floating residual is small. A separately proved interval method could address approximate invariance, but that is outside this criterion and the proposed verifier.

Rational invariant subspaces containing an irrational eigenvalue must also accommodate the appropriate algebraic conjugates. If the ground energy has irreducible degree d and the witness contains its entire multiplicity-r eigenspace, it can require at least rd rational dimensions. Thus a two-state bottom cluster need not admit a two-dimensional rational invariant witness. For a generic problem the necessary witness can grow to the full space.

The standalone verifier accepts exact rational witnesses, reports their dimension and polynomial evidence, and checks full-pencil completeness. Automatic construction of useful small witnesses remains a separate task. All conclusions remain finite-model statements, with no thermodynamic extrapolation.
