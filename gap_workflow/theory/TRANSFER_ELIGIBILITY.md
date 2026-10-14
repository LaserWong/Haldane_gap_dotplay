# Machine-checkable eligibility for exact thermal transfers

## Conclusion

Two finite structural checks can make the current model-to-seed workflow automatic on useful subclasses.
A positive-semidefinite realignment test certifies the identical-factor quantum interaction structure used in the project's exact history construction.
A separate classical diagonal test gives explicit symmetric column transfers without requiring positive-semidefinite realignment.
Neither test is necessary for every possible selfadjoint-transfer representation.
Failure means that the chosen structural test did not establish eligibility.
It does not prove absence of a transfer or absence of a physical gap.

The reviewed bootstrap and interpolation remain analytic dependencies.
This note makes their model-specific hypotheses checkable, rather than replacing the proofs with a numerical flag.

## 1. The model family must be specified first

The current model.py represents a finite graph and expanded site-labelled terms.
A finite matrix alone does not define how those terms extend to all larger boxes.
Automatic thermodynamic eligibility therefore needs a verified family template in addition to finite matrices.

For an initial implementation, require one identical finite-dimensional cell per site of a rectangular lattice, homogeneous onsite term v, and one homogeneous nearest-neighbor bond h_i per spatial direction.
All directions are periodic and use the positive-direction multigraph convention.
Every side length in the transfer theorem is at least two.
Verify these requirements against the expanded terms rather than inferring them from a model name.
For seed generation, expand the same template at every staircase box and compare its exact term dictionary to the finite input.

Homogeneous global Heisenberg, XXZ, onsite_d, and field_z declarations can supply such templates.
A site-specific spin_product list must be checked for exact translational repetition and support before being admitted.
Inhomogeneous fields, mixed spins without an explicit repeated cell, long-range products, arbitrary graphs, and open boundaries require separate family constructions.
Anisotropic directional couplings are allowed when the family template preserves the direction labels.
The current flattened edge list does not itself preserve enough metadata to infer all such templates without reconstruction.

Length-two periodic directions retain both directed adjacency terms in this convention.
A simple-graph seed at length two generally does not equal the square of the same transfer used at lengths three and higher.
Do not silently change the convention.
The graph-state example is a special case whose edge-independent spectrum has a separate scalar-transfer proof.

## 2. Quantum identical-factor test by exact realignment

Work in any real local coefficient basis with positive real metric G.
Check that v is G-selfadjoint and h_i is G⊗G-selfadjoint.
These conditions say that the represented physical operators are Hermitian.
For a q-dimensional cell, let h denote the q² by q² coefficient matrix of one bond, with rows (a,c) and columns (b,d).
Define its realignment by

\[
R_{(a,b),(c,d)}=-h_{(a,c),(b,d)}.
\tag{1}
\]

This is a q² by q² matrix.
The following two statements are equivalent in the chosen real structure.

1. R is real symmetric and positive semidefinite.
2. There are real q by q matrices A_α and nonnegative scalars c_α such that −h = Σ_α c_α A_α⊗A_α.

Indeed, vectorizing each A_α gives R = Σ_α c_α vec(A_α)vec(A_α)ᵀ.
Conversely, any positive-semidefinite factorization of R gives the required operator decomposition by reshaping its factor vectors.
For rational R, an exact pivoted LDLᵀ factorization can produce rational factor vectors and nonnegative rational weights.
No square root is required in the witness.
An exact rational quadratic form with a negative value provides a checkable rejection of this particular test.
Floating-point positive eigenvalues or a tolerance-clipped negative eigenvalue do not certify positive semidefiniteness.

Use the coefficient matrix h in Eq. (1), not the symmetric energy-form matrix (G⊗G)h.
Realigning the latter generally tests a different tensor.
The rational spin basis in RATIONAL_SPIN_PENCIL.md is therefore suitable, provided its metric checks are retained.
A real change to an orthonormal basis transforms each A_α by the same real similarity and preserves the existence of the identical-factor decomposition.
The onsite operator then becomes real symmetric in that orthonormal basis.

For each direction, this witness meets the hypotheses of the project's continuous-time history construction.
Grouping a transverse column into one cell preserves real selfadjointness of its onsite Hamiltonian.
Each crossing bond contributes the same A_α at both ends.
Finite local norms give a finite history measure and a bounded real symmetric kernel, hence a selfadjoint Hilbert–Schmidt transfer.
The exact Dyson expansion gives Z = Tr X_i^L_i for every integer L_i ≥ 2.
This establishes all required directions and widths from finite local witnesses.
There is no Trotter approximation or numerical truncation in the implication.
The analytic construction is the one in the existing two_d_theory/THEORY.md, Section 2.1.

### Examples and exclusions

A ferromagnetic Ising bond h = −J Sz⊗Sz with J ≥ 0 passes with A = Sz and c = J.
Any real symmetric onsite term is permitted, including −ΓSx and a longitudinal field.
Consequently a homogeneous transverse-field Ising family is eligible even though its onsite and bond terms do not commute.
Eligibility alone does not establish a gap at every Γ or every field.
The seed still has to pass.

A real symmetric coupling matrix C on a real operator basis gives a witness whenever

\[
-h=\sum_{\mu,\nu}C_{\mu\nu}A_\mu\otimes A_\nu,
\qquad C\ge0.
\]

The full realignment test avoids requiring a guessed small operator basis.
It also handles linearly dependent operators because the reconstructed tensor, rather than a redundant coefficient parametrization, is tested.

In the ordinary Sz basis, antiferromagnetic Heisenberg interactions generally fail this PSD test.
For half-spin, their Sx and Sz channels already give negative realignment directions.
The model being a real Hermitian matrix is not enough.
For an integer spin, the project's time-reversal real structure provides another route in which spin components are imaginary antisymmetric and antiferromagnetic Heisenberg bonds admit the needed real identical-factor decomposition.
To automate that route, supply an exact algebraic basis-change witness and verify the transformed onsite and bond tensors.
A single half-odd-integer spin has time-reversal square −1, so the same one-cell construction cannot simply be copied.
Repeated cells, bilayers, or exchange-symmetric history constructions may work, but require their own checked witnesses.

A failed realignment test in one real structure does not exclude an admissible complex change of basis or an altogether different transfer construction.

## 3. Classical diagonal route

Suppose all terms are diagonal in one common local product basis and the family template is nearest-neighbor as in Section 1.
Let v(a) be the onsite energy and w_i(a,b) the direction-i bond energy.
Require w_i(a,b) = w_i(b,a) exactly.
There is no sign restriction on these energy tables.

For a fixed transverse periodic box, let a and b denote entire column configurations.
Let V(a) contain all onsite and transverse-bond energies within one column, including their periodic multiplicities.
Let W_i(a,b) be the sum of crossing-bond energies in direction i.
Then

\[
T_i(a,b)=\exp\left[-\beta\left(\tfrac12V(a)+W_i(a,b)
+\tfrac12V(b)\right)\right]
\tag{2}
\]

is a finite real symmetric matrix.
Multiplying its entries around the periodic direction counts each column energy once and each crossing bond once, giving

\[
Z(L_1,\ldots,L_d,\beta)=\operatorname{Tr}T_i^{L_i}
\]

for every L_i ≥ 2.
At L_i = 2 the product contains both crossing terms, as required by the multigraph convention.
The entries are positive, but T_i need not be positive semidefinite.
The bootstrap only needs selfadjointness and even seed powers, so this is sufficient.
The same construction works in every spatial direction.

This route includes both ferromagnetic and antiferromagnetic diagonal interactions and arbitrary homogeneous real onsite potentials.
It is strictly more permissive than the identical-factor PSD test for some classical models.
A nonsymmetric bond table is not covered unless a separately checked gauge or reversibility transformation symmetrizes the transfer.
The first implementation can safely return an unresolved structural obligation in that case.

For model.py, XXZ terms with Jxy = 0, onsite_d, field_z, and nearest-neighbor z-only spin_product terms are a directly detectable subclass.
Check the assembled tables exactly after combining terms, since individually non-diagonal terms could cancel.
Conversely, accepting any model with at least one diagonal term would be unsound.

## 4. An automatic unique-ground baseline with exact seeds

A pinned ferromagnetic Ising family supplies a complete baseline in arbitrary dimension.
Write σ_i ∈ {−1,+1} and

\[
H=\sum_{\langle i,j\rangle}\frac{J_{ij}}2(1-\sigma_i\sigma_j)
+\frac b2\sum_i(1-\sigma_i),
\qquad J_{ij}\ge0,\quad b>0.
\tag{3}
\]

Take homogeneous directional J values for the family template.
The all-plus state has energy zero and is the unique ground state.
Every configuration with k flipped spins has energy at least bk.
Thus, at q = exp(−βb), the exact counted upper envelope is

\[
1\le Z(\beta)\le(1+q)^N.
\tag{4}
\]

The bound includes every spin configuration by its flip count and does not require diagonalization or enumeration.
For an even seed box of volume V, the largest staircase base volume is V′ = 2^d V.
Every staircase numerator is at least one and every denominator is bounded by Eq. (4), so a common purity bound is

\[
P_i\ge(1+q)^{-2V'},
\qquad 1-P_i\le2V'q.
\tag{5}
\]

The last step follows from convexity of (1+q)^−m for m > 0, or its tangent bound at zero.
At rational q, this gives exact rational seed inputs.
For every fixed even seed box and every desired target 0 < γ < b, taking q sufficiently small admits the conservative bootstrap and establishes its lower bound γ.
Indeed K_du ≤ 2K_dV′q and the certified gap approaches b from below as q tends to zero.
The explicit integer-power target check used for the graph-state example applies with h replaced by b.

Equation (3) already proves a gap of at least b directly, so this baseline validates automatic structure checking, counted tails, energy shifts, and seed replay.
It is not a new Ising gap theorem.
Zero-field ferromagnetic Ising instead has at least two ground states and cannot pass a near-one Gibbs-purity uniqueness criterion, despite valid transfers.
Antiferromagnetic classical models also pass structural eligibility but may fail seed contraction because of degeneracy or low-energy behavior.

To express Eq. (3) through the current spin-1/2 parser, use σ = 2Sz.
The exchange coefficient is Jz = −2J with Jxy = 0, and field_z has coefficient −b because the parser defines that term as +hSz.
The omitted scalar is (Σ_edges J + Nb)/2, with every edge counted using the actual multigraph convention.
Restore this exact scalar or carry it in trace bookkeeping.
For a homogeneous periodic family it is extensive and cancels from the spatial ratios, but silently mixing shifted and unshifted traces is unsafe.

## 5. Certificate contract

A structural certificate should store the family template, local dimension and metric, onsite and per-direction bond tensors, exact checksums or canonical rational entries, boundary convention, and the selected proof route.
For the quantum route, include the realignment factorization and reconstructed identical-factor identity.
For the classical route, include simultaneous diagonal tables and exact swap symmetry of every bond table.
For an algebraic basis change, include its exact invertibility, metric transformation, and transformed tensor identities.

The verifier should distinguish a passed finite structural witness from an externally asserted theorem assumption.
A seed certificate must additionally establish heat-trace intervals, omitted-state coverage, recurrence admission, and geometric scope.
Neither a structural pass nor a small finite-volume gap alone can replace these steps.

An initial safe classifier can return one of the following outcomes.

- ELIGIBLE_CLASSICAL_SYMMETRIC_TABLES
- ELIGIBLE_REAL_IDENTICAL_FACTOR_WITNESS
- CONDITIONAL_EXTERNAL_TRANSFER_PROOF
- FAMILY_TEMPLATE_REQUIRED
- STRUCTURE_TEST_INCONCLUSIVE

The last outcome must not be reported as a proof that no transfer exists.

## Sources and checks

The exact history-kernel implication and the all-integer scope were checked against the existing project notes two_d_theory/THEORY.md and two_d_theory/GENERAL_DIMENSION.md.
The historical general_dimension_review/CONSTANT_IMPROVEMENTS.md changes constants but does not enlarge the structural hypothesis class.
The realignment equivalence and classical column-transfer construction are derived explicitly above.
They do not rely on an unverified citation or on a numerical tensor-network analogy.

The accompanying independent script checks rational realignment witnesses and failures, as well as exact classical transfer identities at β = log 2 for lengths two through five and transverse widths one and two.
Its test energies make the transfer entries rational, so these checks use exact arithmetic.

## Implemented local checker

The function bond_realignment_certificate in gapflow/transfer_eligibility.py now verifies rational coefficient matrices with an optional positive diagonal local metric.
It checks physical metric selfadjointness, exact symmetry and inertia of the realignment, and reconstructs a rational nonnegative identical-factor witness whenever the test passes.
An optional onsite matrix is checked in the same real metric.
The output deliberately leaves spatial_transfer_family_certified false because it has not inspected the global family template or all spatial directions.
A diagonal swap-symmetric bond is also reported as a candidate for the separate classical route even when its realignment has negative inertia.

For homogeneous quantum transverse-field Ising interactions −J_i Z⊗Z and onsite −hX, the local witness passes for every J_i ≥ 0 and real h.
Together with the verified family, onsite, directional, and periodic-convention conditions in Section 1, the existing exact history theorem establishes the spatial transfers in both one and two dimensions, and likewise in any fixed dimension.
No commutation of onsite and bond terms is assumed.
This is a precise affirmative eligibility statement, not a gap claim at every parameter value.
The current local function does not yet discharge the global conditions automatically.

Five focused tests passed for ferromagnetic ZZ with a transverse onsite X, antiferromagnetic ZZ rejected by this route but marked classical, a nonorthonormal spin-one metric, multi-factor and zero-bond witnesses, and malformed or unsupported inputs.
The test file is tests/test_transfer_eligibility.py.
