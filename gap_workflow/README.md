# Budgeted spectral-gap workflow

This local workflow accepts a finite spin model and a resource budget. It plans the calculation, computes low-energy candidates, attempts exact certification, and reports the supported gap statement. Ground-state energy and multiplicity need not be supplied: unknown multiplicity is the default starting point, and exact degeneracy must be established rather than inferred from numerical closeness. The implementation described here was reviewed on 2026-10-14.

## Run

Use Python with NumPy and SciPy already available. Exact distinct-root multiplicity inference additionally uses an already-installed SymPy; its absence does not authorize installation or a degeneracy assumption.

    python -m gapflow examples/dimer.json --output results/dimer
    python -m gapflow examples/dimer.json --output results/dimer --resume

Use a fresh output directory for each changed input. [INPUT.md](INPUT.md) defines the schema. Exit code 0 means a certified gap or gapless-family result. Code 2 also covers a certified low-energy cluster whose true ground multiplicity remains unresolved, as well as invalid input, insufficient evidence, resource limits, and worker failures. Read the saved `results.json` for the specific outcome.

## Implemented CLI paths

| Path | Computation | Result |
|---|---|---|
| Finite spin models | Matrix-free partial eigsh followed by rational-matrix or weighted-pencil inertia, Rayleigh bounds, and optional exact multiplicity inference | Certified finite-size gap when justified; otherwise a separated low cluster or unresolved result |
| Paramagnetic quantum Ising chain | Exact rational parity-partition enclosures, thermal bootstrap, and an analytic all-size bridge | Uniform gap lower bound for the specified periodic family with h>J≥0 |
| Graph-state projector family | Analytic rank-one ground space, binomial spectral tail, rational thermal seed and bootstrap | Exact family gap h and a verified bootstrap target such as h/2 |
| Pinned ferromagnetic classical Ising family | Exact counted spectral comparison, rational thermal seed and bootstrap | Uniform gap lower bound at least h and a verified bootstrap target, with J≥0 and h>0 |
| Connected ferromagnetic spin-half Ising | Exact weighted minimum cut before Hilbert-basis allocation | Positive finite gap and a rigorous obstruction to near-one thermal purity |
| Periodic ferromagnetic spin-half Heisenberg family | Analytic ground-space characterization and explicit excited magnon | Zero uniform gap despite a positive gap for every finite ring |
| User-supplied scalar bootstrap data | Exact seed-label validation and conservative scalar inequalities | Conditional inequality replay |

The [model examples](examples/README.md) include Heisenberg chains, mixed spins, XXZ models, and transverse-field spin products. Local real x/z products are supported. Incompatible magnetization-sector requests are rejected. Exact weighted pencils extend rational certification to arbitrary integer and half-integer spins without rounding the Hamiltonian. For total-Sz-conserving models, exhaustive sector coverage can certify the full model while storing one exact block at a time. The 81-state large-D square needs blocks of size 19, and the 256-state cube needs size 70. The [certificate reference](docs/PARTIAL_SPECTRUM_CERTIFICATION.md) describes both routes.

The Ising example illustrates a method-specific obstruction.

    python -m gapflow examples/ising_obstruction.json --output results/ising

Its two-dimensional ground space forces thermal purity at most 1/2 despite a positive excitation gap. Increasing seed size, beta, or trial rank cannot satisfy a near-one purity requirement. A ground-space-aware criterion is needed to proceed beyond this obstruction. See the [Ising analysis](theory/ISING_OBSTRUCTION.md).

For the positive family benchmark, use model={"family":"graph_state_projector","shape":[2,2,2],"h":"1","target_gap":"1/2"}. The [stabilizer benchmark](theory/STABILIZER_BENCHMARK.md) supplies the proof and finite-size bridge.

The [pinned-Ising strong-coupling example](examples/pinned_ising_strong_coupling.json) uses J=10, h=1, and target_gap=1/2. Its counted comparison has no weak-coupling restriction. The analytic bound h is a lower bound, not a claim that the physical gap equals h. The [classical-seed backend](gapflow/classical_seed.py) supplies this CLI route.

The [gapless control](examples/ferromagnetic_heisenberg_gapless.json) invokes a separate analytic family proof. Its excited magnon energy approaches zero as the ring length grows, while each finite ring has a positive gap above its L+1-dimensional ground space. This is a proved zero uniform gap, rather than a conclusion drawn from failed certification. See [GAPLESS_CONTROL.md](theory/GAPLESS_CONTROL.md).

## Unknown ground multiplicity and near-degenerate levels

    python -m gapflow examples/unknown_degeneracy_chain.json --output results/unknown_multiplicity

This input supplies neither a ground energy nor a ground multiplicity. The ordinary path first tries exact certificates from numerical proposals; if these fail and no explicit certificate was supplied, it attempts an exactly counted bottom cluster within the admitted dimensions. Numerical tolerances propose brackets only. They never prove equality of energies.

Exact squarefree characteristic-polynomial Sturm counts can show that the cluster contains exactly one distinct energy, even when that energy is irrational. Its exact rank then gives the ground multiplicity. For conserved total Sz, exhaustive sector coverage plus Kramers symmetry also establishes a rank-two bottom cluster as one exact doublet. Kramers symmetry alone does not identify a rank-four cluster as a fourfold ground space. The CLI limits distinct-root inference to dimension 16; sector-based Kramers inference can operate beyond that limit when every block fits the budget.

If exact equality is not established, status `certified_low_energy_cluster` records `low_band_rank`, `low_band_width_upper`, and `gap_above_cluster_lower`. The ground multiplicity and `true_ground_gap_lower` remain unknown. Separation above a near-degenerate cluster is not the excitation gap above the true ground space: unequal internal levels can have a much smaller gap. A cluster filling the whole space has no complementary excitation gap. Selected-sector results remain restricted to that sector; generic full-space results remain finite-size statements.

## Quantum Ising family benchmark

    python -m gapflow examples/quantum_ising_interval.json --output results/quantum_ising

The registered `quantum_ising_chain` route treats H_L=-J sum Z_i Z_(i+1)-h sum X_i, with Pauli eigenvalues ±1, h>J≥0, and periodic positive-direction bonds (two bonds at L=2). It derives the unique ground state from the paramagnetic proof; no multiplicity is requested from the user. Exact thermal seed enclosures and scalar bootstrap are composed with a separately proved all-integer-L≥2 bridge. The independently reviewed J=1, h=3/2, n=16, beta=8 example certifies a uniform lower bound 0.484734263212. This statement applies to this named family, not arbitrary noncommuting models.

The backend encloses single-particle modes and complete parity-partition formulas without computing many-body eigenpairs. The largest seed contains 2n physical sites; this is distinct from trial rank or an exact-matrix dimension. Omitted n and beta trigger a bounded grid search; a first passing seed is not a globally minimal seed. Reviewed proof-source hashes must match before a physical certificate is accepted. [INPUT.md](INPUT.md) specifies the grid and restrictions.

## Callable research modules

These modules are available through Python functions rather than additional CLI model families.

- [degenerate.py](gapflow/degenerate.py) evaluates finite-spectrum temporal defects and supplies the exact uniform ferromagnetic Ising-cycle certificate. The [degenerate-purity analysis](theory/DEGENERATE_PURITY.md) states its scope and the unresolved general spatial criterion.
- [seed_obstruction.py](gapflow/seed_obstruction.py) checks the model-specific global-width Hoeffding obstruction described in [HOEFFDING_SEED_LIMITS.md](theory/HOEFFDING_SEED_LIMITS.md).
- [forecast.py](gapflow/forecast.py) proposes physical seed sizes from measured pilot data. Its forecasts are heuristic, as detailed in [RESOURCE_ESTIMATION.md](docs/RESOURCE_ESTIMATION.md).

The [transfer-eligibility analysis](theory/TRANSFER_ELIGIBILITY.md) gives structural conditions and their mathematical justification. It is not a registered generic model-to-seed CLI adapter.

## Pipeline and evidence

The ordinary spin-model path runs validation → dimensions and memory planning → partial spectrum → exact certificate → validation → bootstrap admission → report/checkpoint.

Physical seed size, full Hilbert dimension, selected-sector dimension, trial rank, and MPS bond dimension are separate quantities. Ritz residuals provide numerical evidence without establishing completeness. Exact inertia covers the complete admitted working matrix. A selected-sector certificate concerns that sector. The graph-state and pinned-Ising routes establish uniform-family results for their specified families. Generic finite-size certificates and conditional scalar checks retain their narrower scope.

Validation replays exact arithmetic and separately checks the matrix-free numerical representation against the rational construction. Ising graphs up to 12 nodes also receive an exhaustive cut check. Exact replay uses the same arithmetic implementation, rather than a second independent verifier.

## Resources and unsuccessful runs

The workflow checks dimensions and estimated memory before allocating a basis. A fresh subprocess enforces wall time, one BLAS thread, and POSIX CPU/address-space limits. The default exact-matrix cap is 32, with a hard configurable ceiling of 128. Analytical graph backends do not allocate Hilbert-space matrices. Larger budgets require explicit input.

Diagnostics distinguish trial approximation, unresolved spectral tail, geometric criterion, and resource limits. [FAILURE_MODES.md](docs/FAILURE_MODES.md) explains each counterexample and the next appropriate calculation. Multi-size studies use measured pilot data for heuristic threshold forecasts. A passing size is sufficient, without a claim of minimality. Timing remains unknown without calibration. [INPUT.md](INPUT.md) and the [resource discussion](docs/RESOURCE_ESTIMATION.md) specify the assumptions.

## Historical model matching

Generic model runs save `catalog.json` and include `historical_catalog` in their results. The [historical catalog](workflow_docs/HISTORICAL_CATALOG.md) matches the exact periodic spin-one Heisenberg-chain convention to the recorded all-size bound 31/1250=0.0248. It reports available and missing evidence without replacing the fresh finite-size result or claiming a new independent replay.

## Unknown-rank verification and gap definitions

The callable [invariant-witness verifier](docs/INVARIANT_WITNESS_VERIFIER.md) checks exact rational invariance and a small annihilating polynomial, then matches its inferred multiplicity against full-pencil inertia. It avoids the full characteristic polynomial when a suitable witness exists. The CLI does not yet discover or consume these witnesses.

The [ordered-Ising control](theory/ORDERED_ISING_GAP_DEFINITIONS.md) proves that a unique finite-volume ground state can have a first gap tending to zero while the lowest two states remain uniformly separated from all higher states. Reports must distinguish the exact-ground-space gap from low-band separation. Four-eigenpair calculations for L=4 through 12 are saved in [the benchmark](benchmarks/ordered_ising_low_band.json), with floating evidence separated from the analytic proof.

The second milestone passes 175 tests and a fresh 14-example run. The [test log](audit/full_suite_milestone2_20261014_2010.log), [invariant-witness review](audit/INVARIANT_WITNESS_REVIEW.md), and [ordered-Ising review](audit/ORDERED_ISING_GAP_REVIEW.md) record the checks.

## Saved work

Each run saves its normalized input, model, resource plan, candidates, certificate, validation, bootstrap decision, worker log, `results.json`, `report.md`, and `checkpoint.json` as stages become available. Exact decimal coefficient lexemes are preserved. Terminal resume verifies input, artifact hashes, solver source, and dependency versions before reusing results. A code or environment change during execution preserves artifacts but prevents acceptance. Interrupted artifacts remain available for inspection. Rerun in a fresh directory.

## Agent trigger

> Read AGENTS.md and INPUT.md. Run examples/dimer.json within its budget, inspect every stage, and report the strongest justified gap statement. If the target is not certified, diagnose the failed step and propose the smallest evidence-backed next calculation. Preserve results and do not publish remotely.

[AGENTS.md](AGENTS.md) assigns model, resource, spectrum, certificate, bootstrap, review, and reporting responsibilities. The broader [research protocol](workflow_docs/AGENTS_WORKFLOW.md) and [adapter contracts](workflow_docs/BOOTSTRAP_ADAPTERS.md) distinguish implemented components from the additional proof work needed for new model families. The CLI performs no installation, remote publication, or scheduled background work.
