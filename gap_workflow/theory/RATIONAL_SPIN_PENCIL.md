# Exact rational spin pencils

## Basis and metric

Let s be a nonnegative integer or half-integer and set n = 2s.
Fix a normalized lowest-weight vector |−s⟩ and define

\[
e_p=\frac{(S^+)^p}{p!}|-s\rangle,
\qquad p=0,\ldots,n.
\]

The vectors are orthogonal but generally not normalized.
Their squared norms and spin actions are

\[
w_p=\langle e_p,e_p\rangle=\binom np,
\quad S^ze_p=(p-s)e_p,
\quad S^+e_p=(p+1)e_{p+1},
\quad S^-e_p=(n-p+1)e_{p-1}.
\tag{1}
\]

Out-of-range vectors are zero.
In particular, the raising action vanishes at p = n and the lowering action vanishes at p = 0.
The coefficient n−p+1 belongs to the input column p for S−, not to the output row.

To check Eq. (1), the standard normalized raising product has squared amplitude n!p!/(n−p)!.
Dividing by (p!)² gives binomial(n,p).
The commutator identity S−(S+)^p|−s⟩ = p(n−p+1)(S+)^(p−1)|−s⟩ gives the lowering coefficient.
Equivalently, weighted adjointness requires

\[
w_{p+1}(p+1)=w_p(n-p).
\]

Thus, in coefficient coordinates, S− = W^−1(S+)ᵀW with W = diag(w_0,…,w_n).
All entries of S± and Sz are rational.
The physical inner product of coefficient vectors x,y is x*Wy.

## Tensor products and rationality

For several spins, use the tensor-product basis and positive diagonal metric W = ⊗_i W_i.
The Heisenberg interaction has the rational representation

\[
\mathbf S_i\cdot\mathbf S_j
=S_i^zS_j^z+\tfrac12(S_i^+S_j^-+S_i^-S_j^+).
\]

The same construction gives rational matrices for XXZ interactions with rational J_xy,J_z, rational x- and z-directed fields, and real-rational onsite terms such as D(Sz)².
Here Sx = (S+ + S−)/2 and Sy = (S+ − S−)/(2i).
Real-rational coefficients alone do not ensure a real matrix when an odd number of Sy factors appears.
A y-directed field, for example, is imaginary in this basis.
Such models have Gaussian-rational entries and require the Hermitian extension below, or an independently justified real change of basis.
A parser must not silently discard their imaginary parts.

Let Htilde denote the coefficient matrix of a physically Hermitian Hamiltonian in this basis.
Metric Hermiticity is

\[
\widetilde H^*W=W\widetilde H.
\]

Consequently A = W Htilde is Hermitian, and it is real symmetric when the matrix entries are real.
The normalized physical Hamiltonian is

\[
H_{\mathrm{orth}}=W^{1/2}\widetilde H W^{-1/2}.
\]

Square roots appear only in this explanatory change of coordinates.
They need not be evaluated by the exact certificate backend.

## Inertia and spectral counts

For any rational test energy E,

\[
A-EW
=W^{1/2}(H_{\mathrm{orth}}-EI)W^{1/2}.
\tag{2}
\]

Sylvester's law of inertia therefore gives exactly the same numbers of negative, zero, and positive eigenvalues on both sides.
An exact rational symmetric-indefinite factorization of A−EW counts eigenvalues of the physical Hamiltonian below, equal to, and above E, with full multiplicity.
The factorization must handle zero pivots, permutations, and two-dimensional pivots correctly.
A positive-definite-only Cholesky procedure is not a general inertia algorithm.

The eigenvalues of A alone are generally not the physical energies.
The relevant generalized eigenproblem is A x = E W x.
Using Htilde directly in a Euclidean symmetric eigensolver is also invalid unless W is the identity or the solver has explicitly performed the metric conversion.

For a Gaussian-rational Hermitian pencil M = A−EW = B+iC, B is rational symmetric and C is rational skew-symmetric.
Its realification

\[
\mathcal R(M)=\begin{pmatrix}B&-C\\C&B\end{pmatrix}
\]

is rational symmetric and has each eigenvalue of M twice.
Thus each of its three inertia counts must be divided by two to recover physical multiplicities.
This doubles the matrix dimension and is a separate supported backend, not an implicit consequence of real-only code.

## Rayleigh quotients and full residuals

For any nonzero rational coefficient vector x, the exact generalized Rayleigh quotient and residual variance are

\[
\rho=\frac{x^*Ax}{x^*Wx},
\qquad
\sigma^2=\frac{[(\widetilde H-\rho I)x]^*W
[(\widetilde H-\rho I)x]}{x^*Wx}.
\tag{3}
\]

A rational vector gives rational values in the real-rational case.
Gaussian-rational vectors also give real rational values for a Gaussian-rational Hermitian model.
The residual must include every output basis vector reached by Htilde, including those outside the trial support.
A residual compressed back into the trial space is insufficient.

For a trial basis matrix V, the projected pencil is (V*AV,V*WV).
Verify that V has full column rank and that its Gram matrix is positive definite.
The generalized Ritz values obey the usual min-max bounds because this pencil represents the physical compression in the correct inner product.
An exact Rayleigh quotient or residual does not itself prove omitted-state coverage.
Combine it with the counted-inertia, complement, or reference-Hamiltonian bounds in THEORY.md.

## Independent check

The accompanying check_rational_spin_independent.py uses exact symbolic arithmetic for spins 1/2, 1, 3/2, and 2.
It checks the Lie commutators, the Casimir identity, weighted adjointness, the normalized ladder coefficients, and positivity of the metric.
It then constructs a mixed-spin 1 and 3/2 XXZ Hamiltonian with rational x/z fields and single-ion anisotropy.
It checks metric Hermiticity, the symmetric pencil, and Eq. (2) exactly.
A y-field example checks the Gaussian-rational extension and its realification.
All checks in this script are exact symbolic identities.
No floating-point spectral diagnostic is used.
These finite checks guard coefficient and implementation conventions.
The derivation establishes the representation for every finite collection of integer and half-integer spins.
