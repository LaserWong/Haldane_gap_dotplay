# Model input examples

Each JSON file is a CLI request containing a schema-version-1 `model` and execution `budget`. Use `python -m gapflow examples/dimer.json --output /tmp/dimer-example-run` from the project root. The dimer also supplies an exact certificate target; the other requests default to bounded numerical candidate calculations. These finite-size inputs do not assert thermodynamic gaps or supply a bootstrap theorem.

- `ising_obstruction.json`: connected ferromagnetic four-site Ising ring with two ground states and a positive finite excitation gap; illustrates why an unmodified one-ground-state heat-trace criterion fails.
- `tfim_spin_product.json`: open three-site transverse-field Ising model using real spin-product terms.
- `dimer.json`: two spin-1/2 sites, exchange 1, exact ground energy −3/4 and finite-size gap 1.
- `chain_spin_half.json`: four spin-1/2 sites, open boundaries, Heisenberg exchange 1, Hilbert dimension 16.
- `chain_spin_one_periodic.json`: three spin-1 sites, periodic positive-direction bonds, exchange 1, dimension 27.
- `square_large_d.json`: open 2×2 spin-1 square, exchange 1/100 and single-ion anisotropy 1, dimension 81.
- `cube_xxz.json`: open 2×2×2 spin-1/2 cube, transverse exchange 1 and longitudinal exchange 3/2, dimension 256.
- `graph_mixed_spin.json`: explicit triangle with spins (1/2, 1, 1/2), anisotropy and field, dimension 12. Its ordinary normalized exchange matrix has radicals; the rational generalized-pencil backend supports it exactly.

## Schema and normalization

Required fields are `geometry`, either uniform `spin` or site-specific `spins`, and a `terms` list. Optional fields are `schema_version` (1), `name`, and `description`. Unknown model, geometry, or term keys fail explicitly.

A lattice geometry has `type: "lattice"`, a nonempty positive-integer `shape`, optional `periodic` (one boolean or one per axis), and optional `bond_convention`. Shape may have any finite spatial dimension. Site ordering is row-major; the final coordinate changes fastest. The default `positive_direction_multigraph` adds a forward bond at each site and direction, including the periodic wrap bond. In a periodic direction of length two this counts two parallel bonds, matching the historical project normalization. The alternative `simple_graph` counts each undirected pair once. Periodic length-one axes fail rather than silently create self-interactions.

A graph geometry has `type: "graph"`, `n_sites`, `edges`, and optional `positions` with one finite coordinate vector per site. Edges are zero-based distinct-site pairs. Repeated pairs represent repeated interaction bonds. Coordinates are descriptive and never create additional interactions.

Supported terms:

- `heisenberg`: coefficient `J`, representing J(Sx_i Sx_j + Sy_i Sy_j + Sz_i Sz_j).
- `xxz`: coefficients `Jxy` and `Jz`, representing Jxy(Sx_i Sx_j + Sy_i Sy_j) + Jz Sz_i Sz_j.
- `onsite_d`: coefficient `D`, representing D Sz_i².
- `spin_product`: rational `coefficient` and `factors: [{"site": i, "operator": "x"}, ...]`, with distinct sites and real spin operators x or z. The term is the coefficient times their tensor product. Empty factors mean an explicit constant identity term. Spin operators are not Pauli matrices: on spin 1/2, X = 2Sx and Z = 2Sz.
- `field_z`: coefficient `h`, representing **+h Sz_i**, not the alternative negative-field convention.

For exchange, optional `sites: [i,j]` selects one pair; omitted `sites` applies the term to every geometry edge. For onsite terms, optional `sites: [i,...]` selects sites; omission applies it to all sites. All listed terms add, including duplicates. An empty term list is the zero Hamiltonian. No energy shift is inserted. Spins use hbar=1 and S²=s(s+1).

Real multi-site x/z products include transverse fields, transverse-field Ising models, and graph-state X-times-neighbor-Z terms. General complex y products, repeated-site noncommuting factors, biquadratic interactions, arbitrary local matrices, and non-Hermitian coefficients are not supported and fail explicitly rather than being omitted. Graph geometry is general; the supported interaction vocabulary is deliberately restricted.

## Exact and numerical representations

Integer, decimal, and rational-string coefficients such as `"1/100"` are accepted. Rational strings are recommended for certificate provenance. `Model.from_json` preserves decimal lexemes using Python Decimal. `Model.from_dict` interprets a Python float's decimal spelling as the intended exact coefficient; a caller requiring lexical provenance should load JSON with Decimal or use rational strings.

The numerical Hamiltonian uses float64. The separate `exact_hamiltonian` path constructs Fraction entries directly from the retained input coefficients. It supports uniform spin-1/2 and uniform spin-1 exchange, spin-1/2 x factors, and arbitrary-spin diagonal-only models. Normalized higher-spin x factors may have radicals and are rejected by this direct matrix path. The normalized rational-matrix backend explicitly rejects other exchange representations. The separate `exact_pencil` backend supports arbitrary mixed integer/half-integer spins using a rational generalized eigenproblem A v = E W v. Its divided-power basis has positive diagonal norm W = product binom(2s,p), and A = W Htilde is symmetric rational. Exact inertia of A − t W counts the physical eigenvalues below t by congruence; no radicals or floating rationalization are needed. Numerical eigenvalues and residuals remain numerical diagnostics.

`total_m2` means twice total Sz, an integer. Models with a nonzero x-product term conservatively report `preserves_total_sz: false` and reject magnetization-sector selection. A sum that happens to restore the symmetry is still rejected unless expressed in the supported exchange form. Sector dimensions are computed by exact integer dynamic programming. A sector certificate alone is not a full-space certificate: omitted sectors need independent lower bounds. A basis is only enumerated after dimension checks; extreme sectors are generated by pruning rather than scanning the full product space.

## Resource estimates and seed studies

`plan_resources` distinguishes full Hilbert dimension, selected sector dimension, linear trial rank, and optional MPS bond dimension. No MPS solver is supplied. Matrix-free means no Hamiltonian entries are retained, but the present backend still stores explicit Python basis tuples and a lookup dictionary. It is not a constant-storage bitstring kernel.

Memory estimates list assumptions and include basis, vector, trial-block, dense eigensolve, sparse construction, and iterative workspaces. They are advisory, not process-memory enforcement. Timing requires local calibration and is explicitly heuristic. Sparse runtime is left unestimated unless separately measured. Missing memory or timing evidence produces null admission, not an assertion that a run fits.

`sweep_resources` evaluates a supplied sequence of finite model sizes without enumerating bases. `summarize_seed_evidence` may identify the smallest **verified sufficient tested** seed but never invents a global minimum from failed partial-spectrum bounds. A failed certificate can reflect a weak tail bound, incomplete sectors, or a trial space that misses states. It does not prove that the model is gapless or that the tested physical size is inherently too small.
