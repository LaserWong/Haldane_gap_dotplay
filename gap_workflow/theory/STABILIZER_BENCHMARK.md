# Exact graph-state benchmark for the seed workflow

## Model and exact spectrum

Let G be a finite simple graph with N vertices and h > 0.
Define commuting graph-state stabilizers and their Hamiltonian by

\[
K_i=X_i\prod_{j\sim i}Z_j,
\qquad H_G=\frac h2\sum_i(I-K_i).
\]

Let U be the product of controlled-Z gates over the edges of G.
The gates commute, U is unitary, and U X_i U* = K_i.
Consequently

\[
H_G=U\left[\frac h2\sum_i(I-X_i)\right]U^*.
\]

The ground state U|+⟩^⊗N is unique.
The energy hk has exact multiplicity binomial(N,k), and the gap is exactly h for every N ≥ 1.
On bounded-degree lattice graphs the stabilizer terms have bounded support, although they are generally not two-site interactions.
They commute with one another.
Thus this is a nonperturbative interacting-spin benchmark in its physical basis, but not a generic noncommuting Hamiltonian benchmark.

## Heat trace and transfer admissibility

Set q = exp(−βh), so 0 < q < 1.
The exact heat trace and its excited contribution are

\[
Z_G(\beta)=(1+q)^N,
\qquad Z_G(\beta)-1=\sum_{k=1}^N\binom Nk q^k.
\]

Every omitted state is accounted for by this polynomial.
No explicit enumeration or numerical diagonalization of those states is needed.
The retained ground-space rank is one, while the number of numerically computed eigenpairs is zero.
The code's compatibility field trial_rank has this analytic retained-rank meaning.
It does not describe a one-dimensional numerical trial solve.

For a periodic rectangular simple-graph family with side lengths L_1,…,L_d, let V_i = ∏_{j≠i}L_j.
In direction i, the positive scalar operator

\[
X_i=[(1+q)^{V_i}]
\]

is real selfadjoint and Hilbert–Schmidt.
For every integer L_i ≥ 2, Tr X_i^{L_i} = (1+q)^{V_iL_i} = Z_G(β).
This establishes the exact spatial-transfer hypothesis directly, including odd side lengths.
It does not rely on the bond-history construction used for the Heisenberg examples.
The graph family is explicitly simple, including length-two directions.
Changing a different model's periodic multiedge convention is not authorized by this example.

## Exact staircase seed

For even seed lengths n_i ≥ 2, let V = ∏_i n_i.
Every spatial staircase ratio is exactly one.
After all d spatial coordinates have doubled, the volume is V′ = 2^d V.
The temporal ratio is

\[
T=\left(\frac{1+q^2}{(1+q)^2}\right)^{V'}
 =\left(1-\frac{2q}{(1+q)^2}\right)^{V'}.
\]

Bernoulli's inequality gives the rational defect bound

\[
1-T\le u=\min\left\{1,\frac{2V'q}{(1+q)^2}\right\}.
\]

For rational q, all inputs and the general-dimensional admission test are exact rational computations.
Use the conservative constants K_d and the admissible defect threshold from THEORY.md.
A rational target γ > 0 can be checked without evaluating a logarithm.
If γ/h = p/r in lowest terms, the bootstrap bound reaches γ exactly when

\[
(K_du)^r\le q^p,
\]

provided the seed is admitted.
This equivalence follows from β = log(1/q)/h and the monotonicity of the logarithm.
The published numerical target should refer to this rational inequality, not floating-point log rounding.

The seed controls the common-scale boxes of the bootstrap theorem.
The exact unitary spectrum independently covers all smaller finite graphs and all aspect ratios, so it supplies the finite-size bridge without extra numerical assumptions.
The exact gap h is already known from the unitary conjugation.
A successful bootstrap target such as h/2 tests certificate assembly and recurrence logic, rather than proving a new physical gap theorem.
The first successful q in a finite decimal grid is a grid-search result, not an optimal inverse temperature or a globally minimal seed.

## Independent checks and limits

The analytic derivation above proves the model-specific statements at every finite size.
The independent script check_stabilizer_independent.py separately constructs Hamiltonian matrices and the diagonal controlled-Z transformation for a single vertex, a two-vertex periodic simple graph, cycles of lengths three and eight, and periodic simple rectangles of sizes 2×2 and 2×3.
Every binary-matrix conjugation check passed.
Floating-point diagonalization matched the expected binomial spectrum with maximum absolute error below 1.3×10^−14.
The recorded output is stabilizer_independent_checks.json.
These finite diagnostics check implementation conventions and do not replace the analytic all-size proof.

The parent implementation also maintains its own test suite.
This note does not claim that finite tests establish the general transfer theorem or certify any unrelated input Hamiltonian.
