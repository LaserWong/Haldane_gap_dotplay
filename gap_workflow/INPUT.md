# Input contract

The CLI accepts one JSON object with model, budget, and optional solver, certificate, bootstrap keys. Unknown top-level and budget keys are rejected. Input files are limited to 1 MB.

## Minimal example

    {
      "model": {
        "name": "spin-half dimer",
        "spin": 0.5,
        "geometry": {"type": "graph", "n_sites": 2, "edges": [[0, 1]]},
        "terms": [{"type": "heisenberg", "J": "1"}]
      },
      "budget": {
        "max_dimension": 16,
        "memory_mb": 512,
        "wall_seconds": 20,
        "trial_rank": 3,
        "exact_max_dimension": 16
      }
    }

Couplings and exact certificate proposals should use rational strings such as "1/3". JSON decimal coefficient lexemes are preserved as exact decimal strings in the normalized input snapshot. Spin values are checked as exact half-integers before conversion. Numerical solver budgets are converted to floating point where applicable. Rational strings remain preferred for fractions such as one third.

The minimal input intentionally omits the optional certificate: neither exact ground energy nor ground multiplicity is required.

## Model

Specify spin (uniform positive integer or half-integer) or a spins list, geometry, and terms. A lattice geometry uses type=lattice, shape (positive integer lengths), periodic (boolean or one boolean per axis), and optionally bond_convention=positive_direction_multigraph. A graph uses type=graph, n_sites, and edges. Sites are indexed from zero. Preserve parallel-edge multiplicity and the supplied periodic length-two convention.

Supported term families are heisenberg (J), xxz (Jxy, Jz), onsite_d (D), and field_z (h). Consult [model.py](gapflow/model.py) for explicit site selection. The normalization is hbar=1, S squared=s(s+1), with no hidden energy shift. Geometry records the supplied finite model. Arbitrary graph input alone does not prove locality or family-wide geometric hypotheses.

## Budget

Defaults: max_dimension=4096, memory_mb=512, wall_seconds=30, trial_rank=6, exact_max_dimension=32, max_iterations=1000, tolerance=1e-9.

All values must be positive and finite. Dimension, memory, iteration and rank settings must be integers. memory_mb must be at least 128. exact_max_dimension cannot exceed 128. trial_rank is clamped to working_dimension minus one for partial eigsh. It does not change physical size. A dimension-one sector cannot establish an excitation gap. wall_seconds bounds the entire child process, including imports, model construction, iterative computation, and exact checks.

## Solver and certificate

Optional solver: {"total_m2": 0} selects twice the total magnetization. Omitting it uses the full Hilbert space. A selected-sector result is never relabeled a full-model gap.

Optional certificate: {"ground_energy": "-3/4", "gap_lower_bound": "1"}. Both are exact rational proposals, not trusted assertions. The certifier checks the proposed ground energy and the complete interval to the gap threshold. Without these proposals, the workflow first tries rational guesses from Ritz data and, when needed and admitted by the exact budget, a bottom-cluster certificate with unknown multiplicity. Explicit proposals select the proposal-verification path; a failed explicit proposal does not trigger the automatic low-cluster fallback. Failure means no certificate was obtained, not that the model is gapless.

There is no required g or ground_multiplicity input. Exact inertia certifies the bottom cluster rank, width, and separation from its complement. Rank alone is not ground multiplicity. The CLI uses exact distinct-root Sturm counts for working dimensions at most 16 when SymPy is already available, or exhaustive conserved-Sz sectors with a rank-two Kramers argument when applicable. These checks can establish exact degeneracy without a rational ground-energy input. Kramers only guarantees even multiplicity; a rank-four cluster need not be one ground energy.

A separated cluster with unresolved internal equality returns certified_low_energy_cluster (exit code 2). Its low_band_rank, low_band_width_upper, and gap_above_cluster_lower describe the cluster; true_ground_multiplicity and true_ground_gap_lower remain null. Numerical closeness does not establish degeneracy. Even arbitrarily small nonzero internal splitting prevents treating the full cluster as the ground space. Root-count or resource limits can also leave multiplicity unresolved. An all-space cluster cannot establish an excitation gap. The callable low_band functions default to infer_multiplicity=False; the CLI requests inference when supported.

Optional bootstrap is passed to the conditional scalar bootstrap adapter. Its output remains conditional and does not promote a finite matrix certificate into a uniform model theorem.

## Failure and resume

Use results.json status and diagnostics, not the shell exit code alone. Resource failure means the selected run exceeded its admitted resources. Unsupported criteria mean theorem or adapter work is missing. An unproved tail means omitted states have not been ruled out.

A matching --resume verifies the input fingerprint and saved artifact hashes and reuses a terminal result. Changed input, modified artifacts, and interrupted runs are not silently accepted. Choose a fresh output directory to rerun. No routine deletes existing results.

## Exact graph-state family benchmark

A separate supported analytic input is:

    {"model":{"family":"graph_state_projector","shape":[2,2,2],"h":"1","target_gap":"1/2"},"budget":{"wall_seconds":10,"memory_mb":256}}

shape must contain 1 to 6 even integer lengths at least 2. h must be positive rational. target_gap defaults to h/2. Optional max_power (1..100, default 24) bounds the rational thermal-parameter search. No solver, certificate, or scalar-bootstrap override is accepted with this backend. Successful runs use status certified_uniform_family, restricted to this proved projector family. The certificate also records the already-known analytic gap h. The selected seed is sufficient, without a claim of minimality.

## Pinned ferromagnetic Ising family

The analytic classical backend accepts

    {"model":{"family":"pinned_ferromagnetic_ising","shape":[2,2],"J":"10","h":"1","target_gap":"1/2"},"budget":{"wall_seconds":10,"memory_mb":256}}

The Hamiltonian is H=J/2 sum_edges (1-Z_i Z_j)+h/2 sum_i (1-Z_i), where Z_i has eigenvalues +/-1. Periodic directions use the positive-direction multigraph convention. The nonempty shape list contains even integers at least 2 and defaults to [2]. Exact rational parameters obey J>=0 and h>0, with both defaulting to 1. There is no weak-coupling restriction. target_gap defaults to h/2. max_power is an integer from 1 to 100, with default 24, and bounds the rational thermal-parameter search.

No solver, certificate, or scalar-bootstrap override is accepted. The backend allocates no Hilbert basis and computes no numerical eigenpairs. It uses the unique known ground state and a complete counted spectral comparison. Successful runs return certified_uniform_family for this specified family. The analytic physical gap is at least h and need not equal h when J>0. An unsuccessful bounded seed search returns insufficient_evidence for the requested bootstrap target.

## Gapless ferromagnetic Heisenberg family

Use model={"family":"ferromagnetic_heisenberg_chain","J":"1"}. The alias ferromagnetic_spin_half_heisenberg_cycle selects the same backend. The only model fields are family, J, and optional name. J is a positive exact rational string or integer and defaults to 1. No solver, certificate, or scalar-bootstrap override is accepted.

The proved family is H_L=J sum_i (1/4-S_i dot S_(i+1)) for spin one-half, every integer L>=2, and periodic positive-direction bonds. Length two has two bonds. The ground space has dimension L+1. An explicit excited state has energy J*(1-cos(2*pi/L)) <= 2*pi^2*J/L^2, which tends to zero. The backend returns certified_gapless_family with exit code 0. This certifies a zero uniform gap while preserving a positive excitation gap for each finite ring. It is an analytic result for this named family, not a general gaplessness test for arbitrary Hamiltonians.

## Generalized exact coordinates and spin products

The exact backend uses a positive diagonal metric W when physical spin matrix elements contain radicals. It constructs the rational pencil A - tW directly from the model. A numerical physical vector q becomes W^(-1/2)q before explicit rationalization. The proof then recomputes vAv/vWv exactly. This supports arbitrary integer and half-integer spins within the exact dimension budget.

A real spin product is specified by {"type":"spin_product","coefficient":"-1","factors":[{"site":0,"operator":"x"}]}. Factors must use distinct sites and x or z operators. Such a term can break total-magnetization conservation. An incompatible total_m2 selection is rejected.

## Automatic Ising method obstruction

Full-space, uniform spin-half models whose only nonzero interactions have Jxy=0 and Jz<0 on a connected graph are diagnosed before basis allocation. The adapter uses H=-sum J_ij Sz_i Sz_j with J_ij=-Jz, computes the exact minimum-cut gap, and proves thermal purity at most 1/2 from the twofold ground degeneracy. This is a method-specific obstruction to near-one purity, not physical gaplessness. A disconnected graph or a restricted sector follows the ordinary finite-model path instead.

## Exhaustive symmetry-sector certificates

For a full-model run that conserves total Sz, the resource plan records every sector dimension and exact_required_block_dimension. If the full matrix exceeds exact_max_dimension but every sector fits, the workflow checks exact inertia in every sector sequentially. A full-model claim requires complete coverage summing to the full Hilbert dimension. A single sector never suffices. Selected-sector input remains selected-sector scope.

The numerical partial-spectrum stage still obeys max_dimension for its working basis. The partition reduces the exact-matrix block size, not the Hilbert dimension or physical seed. No budget is automatically increased. For example, the cube requires exact_max_dimension at least 70. A cap of 32 reports that requirement and retains candidate-only evidence.

## Source and environment provenance

Results and checkpoints record SHA-256 hashes of all gapflow Python sources, NumPy/SciPy versions, Python version and platform. Resume refuses a changed solver or environment. The parent rechecks provenance after computation and refuses to accept a certificate if code or dependencies changed during the run. Preserve that run and start fresh after the implementation is stable.

## Paramagnetic quantum Ising family

Use model={"family":"quantum_ising_chain","J":"1","h":"3/2","n":16,"beta":"8","digits":50}. J and h are required exact rational parameters with h>J>=0. This is H_L=-J sum_i Z_i Z_(i+1)-h sum_i X_i with Pauli eigenvalues +/-1, periodic positive-direction multigraph bonds, and a doubled bond at L=2. Optional bond_convention must be positive_direction_multigraph; optional name is descriptive. No solver, certificate, or scalar-bootstrap override is accepted.

Optional n is a dyadic integer from 2 through 64 and denotes seed sizes n and 2n, not trial rank. Optional beta is positive rational. digits is an integer from 20 through 100, default 50. With n omitted, the search visits [2,4,8,16,32,64]; with beta omitted, it visits [1,2,4,8,16] at each n. It stops at the first positive scalar replay within that order and the hard process budget. No global minimality is claimed. No many-body basis or eigenpairs are computed.

Exact rational partition enclosures feed the thermal bootstrap. A separately reviewed analytic bound 2(h-J) covers every integer L>=2, including sizes outside the scalar replay's accepted scope; the physical bound reported is the minimum of the bootstrap bound and this bridge. Ground multiplicity one is derived, not supplied. Successful reviewed composition returns certified_uniform_family, restricted to this named paramagnetic family. No passing seed returns insufficient_evidence; changed or missing pinned review sources return proof_source_mismatch. Neither result proves physical gaplessness. The example with n=16, beta=8 certifies 0.484734263212; default bounded search may return a different sufficient seed and lower bound.
