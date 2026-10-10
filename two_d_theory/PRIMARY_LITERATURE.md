# 二维能隙方法的原始文献核验

Checked 2026-10-10. These are primary papers, not summaries or reviews. The mathematical statements below are deliberately limited to the hypotheses actually checked. The three-purity theorem in THEORY.md is an independent derivation here. No priority claim is made for it.

## Gosset–Mozgunov, local finite-size thresholds

David Gosset and Evgeny Mozgunov, “Local gap threshold for frustration-free spin systems,” Journal of Mathematical Physics 57, 091901 (2016), DOI https://doi.org/10.1063/1.4962337. Primary preprint https://arxiv.org/abs/1512.00088 and https://arxiv.org/pdf/1512.00088.

The checked preprint's Theorem 5 gives, for its translation-invariant nearest-neighbor frustration-free square-lattice projector Hamiltonian, even n>2 and periodic size m>2(n+2),

ε_m^T ≥ (3/4)(ε_n^P−8/n²).

P_n is the specifically designed patch graph in the paper. The patch cannot be replaced silently by an arbitrary rectangular restriction, because the proof balances different classes of overlapping bonds. The anisotropic version uses the minimum over the two rotated patches. The familiar one-dimensional threshold 6/[n(n+1)] belongs to its chain theorem and is not the two-dimensional formula.

For the current project, this is a strong option when a model is frustration-free and the required patch's positive gap can be rigorously bounded. It does not directly apply to the frustrated Heisenberg bilayer or large-D square model. Unlike purity approaching one, it permits a degenerate zero-energy ground space.

## Lemm–Mozgunov, boundaries and rhomboidal patches

Marius Lemm and Evgeny Mozgunov, “Spectral gaps of frustration-free spin systems with boundary,” primary paper https://arxiv.org/abs/1801.08915 and https://arxiv.org/pdf/1801.08915.

Theorem 3.5 is explicitly an effectively one-dimensional strip statement whose constants depend on the transverse size. It must not be promoted to width-uniform two-dimensional control. Theorem 3.10 is a distinct two-dimensional criterion. For finite-range frustration-free interactions and its rhomboidal geometries, it compares the large-region gap with the minimum of patch gaps at both side parameters in [n/2,n], minus C₂n^(−3/2). The constants and the boundary intersections are part of the theorem, not dispensable implementation details.

This separation closely illustrates the logical distinction addressed by the present work. Merely blocking a column produces a strip theorem. Simultaneous control of two directions needs additional data or a distinct argument.

## Anshu, optimal inverse-square local threshold

Anurag Anshu, “Improved local spectral gap thresholds for lattices of finite dimension,” Physical Review B 101, 165104 (2020), DOI https://doi.org/10.1103/PhysRevB.101.165104. Primary paper https://arxiv.org/abs/1909.01516 and https://arxiv.org/pdf/1909.01516.

For frustration-free local projector systems, the paper proves a local-gap threshold of order 1/min_i(t_i)² in any fixed dimension. Its argument uses detectability and coarse graining, then iterates a dimension-independent type of strip reduction. Translation invariance is unnecessary, and the local input is a minimum over positioned rectangles, not an average. The formal theorem includes lower and upper restrictions on patch side lengths, interaction overlap and coloring constants, and a global-gap branch condition. Therefore the asymptotic O(t^−2) statement by itself is not an executable small-patch certificate.

For this project, it motivates testing certified FF patch gaps, but it cannot replace the non-FF thermal argument without changing hypotheses. Its geometric iterative mechanism is conceptually comparable to controlling both transfer directions, although its operators and inputs are different.

## Rai et al., local positive-operator SDP hierarchy

Kshiti Sneh Rai, Ilya Kull, Patrick Emonts, Jordi Tura, Norbert Schuch, and Flavio Baccari, “A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems,” Quantum 10, 2065 (2026), DOI https://doi.org/10.22331/q-2026-04-13-2065. Primary text https://arxiv.org/html/2411.03680v3.

The hierarchy searches for geometrically local positive decompositions certifying H²−δH≥0 when the frustration-free Hamiltonian has ground energy zero. The presented construction and numerical benchmarks are one-dimensional. The paper explains extension to higher-dimensional lattices. Its inclusion proofs show how established finite-size certificates enter the feasible set. It does not mean any finite-size numerical SDP value is already rigorous. A usable numerical certificate requires a verified local identity and certified positive semidefiniteness, as discussed in its certifiable formulation appendix.

A practical two-dimensional implementation must explicitly enumerate local support, translated cancellations and the positive discarded terms. For the present frustrated models, their unknown extensive ground energy prevents simply substituting H into the zero-energy FF formula.

## Rao, a non-FF finite-qubit hierarchy and a uniform XY example

Sujit Rao, “A convergent hierarchy of spectral gap certificates for qubit Hamiltonians,” https://arxiv.org/html/2510.08427v2, version dated 2026-10-02. This was checked as a preprint, without asserting journal publication.

The hierarchy bounds λ₀+λ₁ through an exterior-square representation and combines that with an upper bound on λ₀. It does not assume frustration freeness. Finite-n convergence alone is not a generic width-uniform thermodynamic theorem. However, the paper also derives a model-specific bound 2h−dJ for the transverse-field XY Hamiltonian on an arbitrary d-regular graph,

H=−hΣ_i Z_i−(J/2)Σ_(ij)(X_iX_j+Y_iY_j),

when the stated bound is nonnegative. Thus square-lattice strong-field examples already have relevant non-FF analytic/SDP alternatives. The present bilayer result should not be advertised as the first non-FF two-dimensional gap certificate.

The paper's size estimates also make clear that finite-level polynomial dependence on the number of qubits can still carry a substantial variable and constraint count. It is a distinct computational route from sparse low-energy heat-trace inputs.

## Additional dimensional-extension reference

Marius Lemm, “Finite-size criteria for spectral gaps in D-dimensional quantum spin systems,” https://arxiv.org/abs/1902.07141 and https://arxiv.org/pdf/1902.07141. The checked Theorem 3.1 is stated for D≥3. For its nearest-neighbor FF setting it has threshold 1/n+2/n², bounded by 3/n, on an open box. It is useful methodological context but should not be cited as a directly stated D=2 theorem without explaining the reduction or separately checking the proof.

## Decision rule for the current models

The contrast is about hypotheses, not a universal ranking of methods. FF projector models admit local positive-gap, martingale and local SDP approaches. The present non-FF bilayer and large-D examples instead admit two exact selfadjoint thermal transfers. Sparse certified low-energy data can improve their finite thermal seeds. A proposed new model should first be checked for each structure, then the cheapest applicable certificate should be tried. Numerical failure of one sufficient criterion does not establish gaplessness.
