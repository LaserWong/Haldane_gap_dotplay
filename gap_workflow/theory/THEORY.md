# Certified low-energy seeds for local spin Hamiltonians

## Result and scope

A model-input workflow can certify finite-volume heat traces without diagonalizing the full Hamiltonian when it controls the omitted states by an independent inequality.
For a restricted class of models, these finite certificates can feed the exact selfadjoint-transfer bootstrap already developed in Haldane_gap_dotplay.
Locality alone does not supply that transfer structure.
An unsuccessful certificate is inconclusive about the physical gap.

This note gives general finite-matrix bounds and a conditional arbitrary-dimensional bootstrap.
It is an analytic workflow specification, not a new numerical gap certificate for the uniform spin-1 Heisenberg chain or for a generic two-dimensional antiferromagnet.
Its conservative bootstrap constants are those of the existing general-dimensional proof.
The sharper constants in the historical review are optional and are not silently substituted.

## 1. Model, spectrum, and the meaning of a gap

Specify a finite graph or periodic lattice box Λ, the local Hilbert dimensions q_x, and Hermitian interaction terms h_X.
The input Hamiltonian is

\[
H_\Lambda=\sum_{X\subseteq\Lambda}h_X,
\qquad D_\Lambda=\prod_{x\in\Lambda}q_x.
\]

For a thermodynamic statement, specify a consistent family of boxes, interactions, boundary conditions, and normalization.
Finite interaction range and uniformly bounded local terms are standard locality assumptions, but neither is sufficient for the bootstrap below.
A periodic direction of length two must retain the two periodic adjacency terms when the transfer identity uses that convention.
Changing these to one simple-graph edge changes the seed Hamiltonian.

Write the ordered eigenvalues, including multiplicities, as

\[
E_0\le E_1\le\cdots\le E_{D-1}.
\]

The ground-space dimension is g = dim ker(H − E_0 I).
The gap above that space is Δ = E_g − E_0 when g < D.
For g = D there are no excited states, and the output should say so rather than report a measured finite gap.
A uniqueness certificate has g = 1 and Δ = E_1 − E_0.
A symmetry-sector gap is not the full-system gap unless all remaining sectors have been bounded.
For nearly degenerate finite-volume bands, distinguish the splitting within the band from the gap above the band.
This note's purity bootstrap certifies unique finite-volume ground states, not a degenerate ground band.

Use four distinct size measures.
The number of physical sites is |Λ|.
The full Hilbert dimension is D.
The linear trial-space dimension is r.
An MPS bond dimension is χ and is not interchangeable with r.
A single MPS is one trial vector even when its representation uses a large χ.

## 2. Counted eigenvalue enclosures and omitted states

Fix β > 0.
Suppose that, for j = 0,…,r−1, certified ordered eigenvalue intervals satisfy l_j ≤ E_j ≤ u_j.
Suppose also that a full-space argument gives E_j ≥ a for every j ≥ r.
Then

\[
\sum_{j<r}e^{-\beta u_j}
\le Z(\beta)=\operatorname{Tr}e^{-\beta H}
\le\sum_{j<r}e^{-\beta l_j}+(D-r)e^{-\beta a}.
\tag{1}
\]

The proof applies the monotonicity of the scalar exponential to each eigenvalue and counts every omitted state.
No assumption about noncommuting operator exponentials is needed.
If distinct certified bins have counts c_b and lower endpoints a_b, replace the last term by Σ_b c_b exp(−β a_b).
The counts must exhaust the complement and include multiplicities.
Overlapping bins cannot count the same eigenvalue twice when being used as exact spectral coverage.
A deliberately overcounted upper envelope is valid if its domination of the actual tail is proved.

Ritz values θ_j from an r-dimensional orthonormal trial subspace satisfy E_j ≤ θ_j by min-max.
Thus Σ_j exp(−β θ_j) is always a lower bound on Z.
Ritz values do not automatically supply the l_j or the omitted-state threshold a in Eq. (1).
A residual norm proves proximity to some eigenvalue, not its ordered index or the absence of other states.
Even an exact eigenvector with residual zero may be an excited state.

An exact or verified inertia calculation for H − aI counts eigenvalues below a.
A symmetry decomposition is valid only when the invariant blocks and their dimensions form a complete decomposition of the physical Hilbert space.
A tested sector is not a certificate for omitted sectors.
Floating-point eigenvalues, pivot signs, and approximate quantum numbers are proposals until rounding and counting errors are bounded.

## 3. A general trial-space and complement certificate

Let P be an orthogonal rank-r projector, Q = I − P, and write H in the corresponding decomposition as

\[
H=\begin{pmatrix}A&B^*\\B&C\end{pmatrix}.
\]

Assume certified bounds C ≥ cI_Q and ||B|| ≤ η.
For every t > 0, the quadratic-form inequality

\[
2\operatorname{Re}\langle y,Bx\rangle
\ge-t\|x\|^2-\eta^2t^{-1}\|y\|^2
\]

gives

\[
H\ge (A-tI_P)\oplus(c-\eta^2/t)I_Q.
\tag{2}
\]

Ordered eigenvalue monotonicity, followed by scalar exponentiation and summation, gives

\[
\operatorname{Tr}_P e^{-\beta A}
\le Z(\beta)
\le e^{\beta t}\operatorname{Tr}_P e^{-\beta A}
 +(D-r)e^{-\beta(c-\eta^2/t)}.
\tag{3}
\]

For the upper bound use certified lower endpoints of the eigenvalues of A, and for the lower bound use their certified upper endpoints.
Equation (3) does not require P to be an invariant subspace or to contain the lowest r exact eigenvectors.
It bounds the whole trace directly.
When η = 0, the block decomposition is exact and t can be removed.
For r = D, use the full-space trace enclosure without a complement term.

The full leaked vector QHP must be included in η.
A residual computed after projecting H back into P cannot bound this leakage.
For a nonorthonormal basis, verify its positive Gram matrix and use the corresponding metric consistently before applying these formulas.
A Gershgorin, local-form, sum-of-squares, or verified inertia argument can supply c, but its correctness must cover all of Q.
A weak c is a legitimate failed bound, not permission to omit the complement.

Equation (2) also supplies finite-gap certificates without a thermodynamic bootstrap.
Let μ_0 ≤ μ_1 ≤ ⋯ be the sorted eigenvalues of its right-hand side.
If the lowest Ritz value obeys θ_0 < μ_1, then E_1 ≥ μ_1 > θ_0 ≥ E_0.
The finite ground state is unique and Δ ≥ μ_1 − θ_0.
Numerical implementation must compare a certified lower endpoint for μ_1 with a certified upper endpoint for θ_0.

## 4. Comparison Hamiltonians and one-vector seeds

A structured alternative starts from a reference excitation operator K ≥ 0 with exactly known ordered eigenvalues κ_j and a computable heat trace.
Suppose the full-space form inequality

\[
H\ge a_0 I+\alpha K,\qquad \alpha>0
\tag{4}
\]

has been proved.
Then E_j ≥ a_0 + ακ_j for every ordered index j.
A tensor-product reference can encode all D eigenvalues through a small generating polynomial, without enumerating them.
This is the key omitted-state mechanism in the existing dimer certificates.
The comparison is allowed to be loose and need not share eigenvectors with H.

Assume κ_0 = 0 is simple and κ_1 > 0.
Let a = a_0 + ακ_1, and let a normalized trial vector have exact Rayleigh quotient ρ and variance σ² = ||(H−ρ)ψ||².
If ρ < a, min-max proves that precisely one eigenvalue lies below a.
The Temple enclosure is

\[
\rho-\frac{\sigma^2}{a-\rho}\le E_0\le\rho.
\tag{5}
\]

Indeed, every eigenvalue λ satisfies (λ−E_0)(λ−a) ≥ 0.
Taking the expectation gives σ² + (ρ−E_0)(ρ−a) ≥ 0.
The strict denominator condition is essential.

Let e_- and e_+ be the endpoints in Eq. (5), with e_+ = ρ.
The shifted trace obeys

\[
1\le e^{\beta e_+}Z(\beta)
\le e^{\beta(e_+-e_-)}
 +e^{\beta(e_+-a_0)}
 \left[\operatorname{Tr}e^{-\alpha\beta K}-1\right].
\tag{6}
\]

This is a one-vector spectral seed even when the variational solver used many basis vectors.
Its validity comes from Eq. (4) across the entire Hilbert space, not from the number or quality of computed Ritz states.
A reference with degenerate κ_0 needs a block or counted-level treatment and cannot use the unique-ground argument unchanged.

## 5. Temperature, tail tolerance, and sufficient retained dimension

For Eq. (1), an absolute tail target ε_Z is met whenever

\[
(D-r)e^{-\beta a}\le\varepsilon_Z.
\tag{7}
\]

The absolute target changes under an energy shift.
A shift-invariant sufficient target relative to a known ground-energy upper bound e_+ is

\[
(D-r)e^{-\beta(a-e_+)}\le\varepsilon.
\tag{8}
\]

If a > e_+ and r < D, it suffices that

\[
\beta\ge\frac{\log[(D-r)/\varepsilon]}{a-e_+}.
\tag{9}
\]

This is a sufficient temperature for this particular tail estimate.
It is not an optimal inverse temperature for a spatial-purity seed.
Increasing β can make a spatial ratio worse through its finite-size ground-energy mismatch.
The workflow must optimize all staircase ratios together.
It must also include uncertainty in retained energies, whose multiplicative trace effect grows as exp(β times the energy uncertainty).

For an exact invariant spectral truncation at fixed β, retaining the lowest r eigenvectors maximizes retained Boltzmann weight among rank-r orthogonal projectors.
This follows from the variational characterization of the sum of the largest r eigenvalues of exp(−βH).
The smallest r attaining a specified trace tolerance therefore depends on the entire low-energy density of states and the target tolerance.
At β = 0, retaining a fraction 1−ε of the trace requires r ≥ (1−ε)D.
At β tending to infinity, relative trace capture requires accounting for the ground-state multiplicity, with the precise required fraction depending on ε.
Neither observation implies that a variational trial space must have this spectral-truncation rank when a separate analytic tail bound is available.

A successful dimension r is an upper bound on the resources needed by that certificate construction.
To claim a minimum, specify the model, volume, β, tolerance, admissible basis family, tail method, and objective, and exclude all smaller admissible candidates.
A failure of one basis or one moment order does not establish any such minimum.
There is no model-independent universally sufficient small r inferred merely from locality.
The finite universal fallback r = D exists, so claims of absolute nonexistence of a finite seed dimension would be false.

## 6. From heat traces to physical and spatial purities

For one finite Hamiltonian define the Gibbs purity

\[
T(\beta)=\frac{Z(2\beta)}{Z(\beta)^2}.
\]

Certified positive trace intervals Z^- ≤ Z ≤ Z^+ yield

\[
T\ge\frac{Z^-(2\beta)}{[Z^+(\beta)]^2}.
\tag{10}
\]

The largest Gibbs probability p_0 obeys p_0 ≥ T because Σ_j p_j² ≤ p_0 Σ_j p_j.
If a certified lower bound p for T exceeds 1/2, the ground state is unique and

\[
e^{-\beta\Delta}=p_1/p_0
\le(1-p)/p,
\qquad
\Delta\ge\beta^{-1}\log\frac{p}{1-p}.
\tag{11}
\]

If the ground multiplicity is g ≥ 2, T ≤ p_0 ≤ 1/g at every β and T tends to 1/g as β tends to infinity.
Thus the near-one purity criterion cannot certify a degenerate ground space.
A symmetry-resolved purity only certifies its selected sector.
It does not bound inter-sector splittings.
A general degenerate-band extension needs a new bootstrap theorem, not a rescaling of T by g.

For spatial doubling D_i of a box v, the candidate ratio is P_i(v) = Z(D_i v)/Z(v)².
The same interval division gives a rigorous lower bound on this scalar ratio.
Its interpretation as a purity, and in particular P_i ≤ 1, needs an exact transfer theorem.
It is not a generic consequence of the Hamiltonian being local.

If shifted traces Q_v = exp(β_v e_v) Z_v are stored, reconstruct

\[
\log P_i(v)=\log Q_{D_i v}-2\log Q_v
-\beta_{D_i v}e_{D_i v}+2\beta_v e_v.
\tag{12}
\]

For spatial doubling β remains fixed.
For temporal doubling β doubles and the physical volume is unchanged.
Independently resetting every patch's ground energy to zero and discarding the shift terms generally corrupts spatial ratios.
Use log intervals and simplify common trace factors before interval arithmetic when this preserves the dependencies exactly.

## 7. Conditional heat-trace bootstrap in spatial dimension d

Assume d ≥ 1 and exact positive physical partition functions Z(L_1,…,L_d,β).
For each direction i, every fixed choice of the other integer lengths at least two, and every β > 0, require a real selfadjoint Hilbert–Schmidt transfer X_i with

\[
Z(L_1,\ldots,L_d,\beta)=\operatorname{Tr}X_i^{L_i}
\quad\text{for every integer }L_i\ge2.
\tag{13}
\]

The operator may depend on the transverse box and β but must not depend on its power L_i.
These assumptions must remain valid at all scales used by the proof.
An approximate Trotter identity, an uncontrolled tensor-network truncation, or a general nonselfadjoint transfer matrix does not meet Eq. (13).
Finite blocking can organize finite-range terms but does not automatically prove the required real selfadjoint transfer structure.
A sufficient construction for certain identical-factor real interactions is recorded in the existing two-dimensional theory.
In a common real cell basis, the onsite term must be real symmetric and each intercell bond must admit −h = Σ_α c_α A_α ⊗ A_α with real A_α and c_α ≥ 0, while h itself is Hermitian.
The exact continuous-time history expansion then produces a real symmetric Hilbert–Schmidt transfer kernel.
Apply and verify this structure independently in every direction, including after grouping a transverse column into a cell.
Real antisymmetric factors are permitted, so this sufficient condition is not a requirement that every A_α be a positive operator.
More general exchange-symmetric constructions need their own proof.

Let k = d+1, with the last coordinate β.
Let D_i double coordinate i and P_i(v) = Z(D_i v)/Z(v)².
Take even seed lengths n_i ≥ 2 and β_* > 0.
In the standard order of spatial coordinates followed by β, define

\[
Q_j=P_j(D_{j-1}\cdots D_1v),\qquad j=1,\ldots,k.
\tag{14}
\]

Each Q_j lies in (0,1].
The spatial powers are even, while the temporal ratio is the physical Gibbs purity.
The seed uses a staircase of k+1 distinct partition functions rather than all corners of the doubling cube.
Different coordinate orderings generally require different finite boxes.

Commuting coordinate doublings give the exact exchange identity

\[
P_i(D_jv)P_j(v)^2=P_j(D_iv)P_i(v)^2.
\tag{15}
\]

For a nonnegative normalized spectrum with purity defect u, squaring its eigenvalues and renormalizing gives a new defect at most

\[
f(u)=\frac{u^2}{2(1-u)^2}.
\tag{16}
\]

One direct proof writes the original purity as p = Σ_i w_i².
Then the new defect is 2Σ_{i<j}w_i²w_j²/p², bounded by 2(Σ_{i<j}w_iw_j)²/p² = (1−p)²/(2p²).

Moving the first edge through the remaining staircase bounds its pre-squaring purity from below by

\[
\prod_{j=1}^k Q_j^{2^{k-j}}
=\frac{Z(D_k\cdots D_1v)}{Z(v)^{2^k}}.
\tag{17}
\]

Square that edge and move it to the end of the queue.
Repeat sequentially for the remaining edges.
Later updates use already updated entries, not the old staircase in parallel.
A full cycle doubles every spatial length and β.

Define

\[
c_d=2^{d+1}-1,\qquad F_d=4\,8^{d-1},
\qquad K_d=\max\{c_d^2,2F_d\},
\]

and

\[
u_{\mathrm{adm}}(d)=
\min\left\{\frac1{4K_d},\frac1{100\,8^{d-1}}\right\}.
\tag{18}
\]

If all seed defects are at most 0 < u_* ≤ u_adm(d), each sequential update stays within the common bound and a full cycle obeys

\[
u_{j+1}\le K_du_j^2,
\qquad u_j\le\frac{(K_du_*)^{2^j}}{K_d}.
\tag{19}
\]

Indeed, the product in Eq. (17) loses at most c_du, and f(c_du) ≤ c_d²u² on this domain.
The contraction is in the common linear scale, not the volume.

The existing all-integer interpolation lemma under Eq. (13) gives

\[
T(L_1,\ldots,L_d,\beta_j)\ge1-F_du_j
\]

whenever 2^j n_i ≤ L_i ≤ 2^{j+1} n_i for every i, including odd integer lengths.
Its proof uses the unique dominant absolute eigenvalue of each transfer and interpolation of its absolute spectral powers.
Positivity of partition functions at arbitrarily large odd powers fixes the dominant eigenvalue's positive sign.
The full interpolation derivation is in the existing GENERAL_DIMENSION.md and its one-dimensional lemma in THEORY.md.
This is an inherited analytic dependency, not a new independently formalized theorem in this workflow.

Combining this bound with Eq. (11), F_du_j/(1−F_du_j) ≤ K_du_j, and β_j = 2^jβ_* gives

\[
\boxed{\displaystyle
\Delta_{L_1,\ldots,L_d}\ge
\frac{\log[1/(K_du_*)]}{\beta_*}.}
\tag{20}
\]

Every covered finite volume has a unique ground state.
Equal n_i cover all sufficiently large integer hypercubes.
Unequal n_i cover common-scale boxes, not arbitrary aspect ratios.
Smaller sizes need a separate finite-size bridge.
Open boundaries need a separate theorem.
A finite-volume family statement should not be relabeled as uniqueness of every infinite-volume state.
An infinite-volume GNS conclusion needs the corresponding local-limit argument and its boundary assumptions stated explicitly.

If certified seeds enter the admissible region only after m preliminary recurrence cycles, use the new seed scale 2^m n_i and β = 2^mβ_* in Eq. (20).
The numerical gap and size coverage must both reflect this change.
Failure to enter this sufficient region after a finite search proves only that this run has not certified the theorem.

## 8. Model-input workflow and proof obligations

1. Parse the exact local operators, lattice, parameters, boundary convention, and requested conclusion. Reject inconsistent Hermiticity, dimensions, or boundary multiplicities.
2. Separate a finite-volume target from a thermodynamic family target. Record whether uniqueness, a ground-space gap, or a band gap is intended.
3. Select a structural theorem only after its assumptions are verified. Use the heat-trace bootstrap only with Eq. (13). Frustration-free finite-size criteria are an alternative route with different assumptions and thresholds.
4. Choose seed boxes and a β search domain, and estimate D, r, leakage support, memory, and exact-arithmetic costs before calculation.
5. Generate low-energy trial vectors by an allowed solver. Store them as proposals until exact or interval Rayleigh, leakage, and complement checks pass.
6. Construct a complete tail certificate by counted inertia, a complement bound, or a reference comparison. Return an explicit unresolved-complement result if none succeeds.
7. Build outward trace intervals, with all energy shifts and degeneracies recorded. Evaluate the staircase in logarithmic form where necessary.
8. Replay the recurrence with conservative arithmetic and its exact sequential order. Return the theorem assumptions, admitted seed, gap bound, and covered sizes only on acceptance.
9. Check uncovered short sizes separately when the requested conclusion includes them. Preserve failed candidates and the reason for failure.
10. Report analytic assumptions, exact certificates, interval certificates, floating-point diagnostics, and conjectures as separate evidence classes.

A certificate verifier must reject missing evidence rather than treat a user-supplied Boolean such as transfer_verified as a mathematical proof.
A Boolean can record an external proof obligation but cannot discharge it.
For a new model, the theorem report remains conditional until the referenced structural proof has been checked.

## 9. Why the workflow cannot always decide or minimize

For a fixed finite Hermitian matrix with exact rational or algebraic entries, exhaustive exact spectral methods are a finite fallback.
Computational cost and input precision remain practical constraints.
This finite problem must not be confused with deciding a uniform gap for an infinite family.

Cubitt, Pérez-García, and Wolf proved undecidability of the spectral-gap problem for a specified class of translationally invariant nearest-neighbor models on a two-dimensional square lattice with fixed finite local dimension.
Bausch, Cubitt, Lucia, and Pérez-García established a one-dimensional undecidability result for their corresponding model class.
These primary results exclude an always-terminating algorithm that correctly decides every input in those classes.
They do not say that every physically interesting subclass is undecidable or that finite matrices cannot be solved.

Therefore a general assistant must allow unsupported, inconclusive, resource-limited, and conditionally certified outcomes.
It cannot promise a decisive theorem for every local spin model.
Undecidability does not by itself prove that every chosen certificate language lacks a computable optimum on every restricted subclass.
A universal minimum-seed promise is nevertheless unjustified without a defined certificate family, a complete success criterion, and termination guarantees.
For the present workflow, accepted seed dimensions and sizes are sufficient examples.
Optimality claims require explicit lower-bound or exclusion proofs within a stated search class.

## Sources and provenance

The following current local project notes were read on 14 October 2026.
They distinguish historical independent reviews from the new analytic organization in this note.
Paths below are relative to the shared working directory, not remote publication claims.

- haldane_english_20261014/publish_inplace/low_energy/README.md gives the existing full-space reference comparison, Temple interval, and dimer-tail mechanism.
- haldane_english_20261014/publish_inplace/two_d_theory/THEORY.md gives the exact transfer hypotheses, the one-dimensional interpolation lemma, and the specialized two-dimensional theorem.
- haldane_english_20261014/publish_inplace/two_d_theory/GENERAL_DIMENSION.md gives the conservative d-dimensional recurrence and interpolation constants used here.
- haldane_english_20261014/publish_inplace/research_20261010/general_dimension_review/CONSTANT_IMPROVEMENTS.md records sharper sufficient constants and their distinct review status.
- haldane_english_20261014/publish_inplace/seed_size/proofs/DERIVATIONS.md distinguishes method-specific seed exclusions from statements about the physical gap.

Primary external records verified through their author or journal records on 14 October 2026 follow.
The finite-matrix inequalities in Sections 2–6 are proved directly above rather than attributed to an unchecked numerical package.

- Toby Cubitt, David Pérez-García, and Michael M. Wolf, Undecidability of the Spectral Gap, full version, arXiv 1502.04573.
- Johannes Bausch, Toby Cubitt, Angelo Lucia, and David Pérez-García, Undecidability of the Spectral Gap in One Dimension, arXiv 1810.01858, Physical Review X 10, 031038, 2020.
- Marius Lemm, Finite-size criteria for spectral gaps in D-dimensional quantum spin systems, arXiv 1902.07141. This provides an alternative frustration-free route, not a replacement for the hypotheses of Eq. (13).
- David Gosset and Evgeny Mozgunov, Local gap threshold for frustration-free spin systems, arXiv 1512.00088. Its improved finite-size thresholds apply to the specified frustration-free models, not arbitrary frustrated Hamiltonians.

No new physical-model numerics, remote writes, or proof-assistant formalization were performed for this note.
