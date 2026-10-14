# What each counterexample shows

The workflow records the failed assumption and the scope of the conclusion. A failed test does not by itself identify a gapless model.

| Case | Cause | What follows | Appropriate next step |
| --- | --- | --- | --- |
| Zero-field ferromagnetic Ising | Two equal ground-state Gibbs weights | Thermal purity is at most 1/2 at every temperature | Use a ground-space-aware argument or an independent cut certificate |
| A zero-residual trial vector misses the ground state | Residuals measure invariance, not completeness | A perfect eigenvector can still be an excited state | Certify the complement or cover all symmetry sectors |
| One magnetization sector appears gapped | Other sectors were omitted | Only a sector gap has been established | Sum verified inertia counts over a complete sector partition |
| Multiplying purity by the ground degeneracy and retaining the old recurrence | Excited multiplicities need not scale with the ground multiplicity | The old quadratic constant can fail | Use the derived degeneracy-dependent temporal inequality |
| Dividing an Ising-cycle partition function into identical spin-flip sectors | A sector trace need not remain a spatial transfer trace | The putative spatial purity can exceed one | Prove the sector transfer representation separately |
| Original global-width Hoeffding seed at excluded couplings | The lower-bound construction loses too much to volume and interaction width | No temperature or larger seed rescues that construction | Improve the complete-tail estimate or use another seed construction |
| Small physical size gives an insufficient scalar seed | Finite-size curvature and thermal tails compete | Failure at the tested size does not establish failure at larger sizes | Collect comparable seed defects and propose an explicitly heuristic next size |
| Code rounds a model coefficient before exact verification | The exact checker receives a different Hamiltonian | Exact arithmetic can certify the wrong input | Preserve decimal lexemes and independently reconstruct the Hamiltonian |
| Forecast rounds a certified defect onto its threshold | Floating-point comparison changes the acceptance decision | A falsely sufficient seed can be reported | Compare acceptance thresholds exactly and reserve floats for forecasting |
| A scalar Hamiltonian is assigned a positive excitation gap | There is no excited eigenspace | The ordinary gap question is undefined for that supplied space | Return NO_EXCITED_SPACE with the multiplicity |
| Source changes during a calculation | Result provenance no longer identifies one executable version | The result cannot be accepted under the earlier source fingerprint | Preserve artifacts and rerun a stable version |

## Degeneracy and physical U(1)

The zero-field Ising model commutes with total Sz. Its obstruction is therefore not absence of U(1). On a connected positive-weight graph, ferromagnetic alignment gives exactly two ground configurations related by global spin flip. The zero-temperature Gibbs state mixes them equally.

A longitudinal field keeps total-Sz conservation while selecting a unique ground state. A graph-state projector Hamiltonian provides a complementary control with a unique ground state and valid thermal seeds despite not commuting with total Sz. These comparisons isolate ground multiplicity from the particular continuous symmetry.

The excitation gap is measured above the entire ground eigenspace. This distinction matters when the ground multiplicity is larger than one. The first two eigenvalues counted with multiplicity can coincide even when that excitation gap is positive.

Exact examples and inequalities are in [the degenerate-purity analysis](../theory/DEGENERATE_PURITY.md). The [Ising cut analysis](../theory/ISING_OBSTRUCTION.md) identifies the relevant gap, and the [Hoeffding analysis](../theory/HOEFFDING_SEED_LIMITS.md) proves a different, construction-specific failure. Regression tests retain the small counterexamples so subsequent workflow changes cannot silently restore invalid shortcuts.
