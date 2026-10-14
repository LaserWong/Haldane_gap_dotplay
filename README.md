# Spectral-gap bounds for spin chains and square bilayers

Updated 2026-10-14 16:00 EDT (America/New_York, UTC−4) / 2026-10-14 20:00 UTC.

The current task is a budgeted model-to-gap workflow. It starts with partial low-energy calculations, checks what can be certified, and reports the next calculation and its resource requirements. Ground-state multiplicity is unknown by default. The [workflow](gap_workflow/README.md), [input schema](gap_workflow/INPUT.md), and [current status](CURRENT_STATUS.json) describe the implementation. Earlier results and their recovery limitations remain recorded below.

## Latest progress

- An executable workflow now accepts finite spin models on graphs or rectangular lattices, including mixed spins and real transverse spin products. Numerical candidates are checked with rational inertia or weighted pencils. Exhaustive symmetry-sector coverage can certify the full finite space while storing one block at a time.
- Ground multiplicity is inferred when exact distinct-root counts or verified symmetry arguments permit it. Otherwise, the output gives a low-energy cluster's rank, width, and separation from the remaining spectrum. A split cluster is never reported as an exactly degenerate ground space. An adversarial splitting of 10^-100 is resolved by exact arithmetic.
- The periodic quantum Ising chain with Pauli normalization, J=1 and h=3/2, gives a rational bootstrap bound 0.484734263212 from n=16 and beta=8. The reviewed transfer theorem and analytic finite-size bridge extend it to all integer L>=2. The seed calculation uses single-particle mode enclosures and no many-body eigenpairs. The separately known analytic bound is 1, so this validates the bootstrap implementation rather than improving the model's known gap.
- Graph-state and pinned classical-Ising families have registered uniform-gap routes. Ferromagnetic Ising demonstrates failure of the unique-ground thermal criterion despite a positive excitation gap. A ferromagnetic Heisenberg-chain control has a proved zero uniform gap from its magnon branch.
- Physical seed size, Hilbert dimension, sector dimension, and trial rank are tracked separately. Pilot-based resource and seed forecasts are heuristic. No universal minimum-size estimator or arbitrary-model gap decision procedure is claimed.
- The current source passes 157 tests. Independent audits cover rational certificates, near-degenerate clusters, model construction, and quantum-Ising trace enclosures. These are code and mathematical reviews, not proof-assistant verification. See the [low-band review](gap_workflow/audit/LOW_BAND_REVIEW.md) and [quantum-Ising review](gap_workflow/audit/QUANTUM_ISING_CERTIFICATE_REVIEW.md).

The main open step is a spatial bootstrap that accepts an initially unknown ground rank or an isolated low band. The [unknown-multiplicity analysis](gap_workflow/theory/UNKNOWN_MULTIPLICITY_BOOTSTRAP.md) proves finite-matrix criteria and explains why a thermal plateau alone is insufficient. Exact polynomial methods still require the complete finite operator or exhaustive blocks. Generic finite-size certificates do not automatically imply a uniform thermodynamic gap. Missing historical late-stage proof dependencies remain a separate recovery task.

## Research question and main results

Can information from a small set of low-energy trial states establish a positive spectral gap at every system size, including genuinely two-dimensional systems? This project studies that question for periodic spin chains and square bilayers. The method combines certified low-energy information with bounds on the omitted spectrum, then propagates heat-trace inequalities through temperature and spatial scales. Finite-size bridges cover the sizes below the asymptotic recurrence.

| Model | Result | Scope and available evidence |
| --- | --- | --- |
| Uniform spin-1 Heisenberg chain | gap≥0.0248 | Every integer L≥2. The full-size proof survives in the Stage22 baseline. |
| Ordinary spin-1/2 square bilayer | gap≥0.004499695659 on [0,0.108], and gap≥0.000586405978 on [0,0.10825] | Every integer square side L≥2. Continuous-interval certificates survive in the baseline. |
| Ordinary bilayer, later history | gap≥0.004499695659 on [0,0.118], and gap≥0.005 on [0.108,0.118] | Recorded as independently accepted at Stage33. The recovered overview PDF confirms 166 and 80 interval pieces. The complete certificate dependencies have not been reconstructed. |
| Ordinary bilayer, stronger local bounds | gap≥0.01 on [0.108,0.115], and at the isolated point g=0.116 | Recorded in the later history. The isolated point does not extend the interval bound. |
| Alternating spin-1 chain | gap≥0.051807500 at g=0.225 | Every integer number of two-site cells M≥2. At g=0.25, only 2≤M≤16 is covered, with gap≥0.01. |
| Near-uniform alternating spin-1 chain | Four closed intervals around g=1 with bounds 0.020, 0.015, 0.010, and 0.005 | Every M≥2, with physical length 2M. Exact rational endpoints appear below. |
| Fully frustrated bilayer | Family-uniform gap min(1,4−12J), for 0≤J<1/3 | All periodic rectangles with both sides at least 2. This analytic result gives 0.4 at J=0.3. |
| Perturbed fully frustrated bilayer | gap>0.000768515509 for 0≤ε≤0.00855 at J=0.3 | Every square L≥2, with direct bonds J+ε and crossed bonds J. |
| Spin-1 square lattice with large single-ion anisotropy | gap≥0.086452285325 at D=1 and g=0.01 | Every square L≥2. An independent certificate survives. |
| AKLT reference model | gap≥1/10 for periodic L≥5, with a unique ground state for L≥3 | Normalization H=ΣP₂. The proof uses a local-projector criterion. |

Unless stated otherwise, each bound applies above a unique ground state in the full finite-volume Hilbert space. It does not establish infinite-volume ground-state uniqueness or locate a critical coupling.

At g=0.12, the recovered handoff records acceptance of the complete H³ calculation and Ritz calculation for a fixed preparation. The gap bootstrap remained `SOURCE_ONLY/NOTRUN`, with controls, entry checks, and resource admission unfinished. There is no positive gap certificate at this coupling. Spin-2 work has established finite heat-trace and error-control results, but no new all-size positive gap bound.

## Models and normalization

### Spin-1 chains

The uniform chain has periodic Hamiltonian

$$
H_L=\sum_{i=1}^{L}\mathbf S_i\cdot\mathbf S_{i+1},
$$

with $\mathbf S_{L+1}=\mathbf S_1$, unit antiferromagnetic bilinear exchange, S²=2, and Hilbert-space dimension 3^L. There is no biquadratic term, magnetic field, or single-ion anisotropy. The periodic convention counts parallel bonds at L=2, where the exact gap is 2. The exact L=3 gap is 1.

The alternating chain contains M two-site cells and 2M physical spins,

$$
H_M=\sum_{j=1}^{M}\left(\mathbf S_{2j-1}\cdot\mathbf S_{2j}
+g\,\mathbf S_{2j}\cdot\mathbf S_{2j+1}\right).
$$

Here $\mathbf S_{2M+1}=\mathbf S_1$. Its Hilbert-space dimension is 9^M. The energy shift is H′=H+2M I. A shifted isolated dimer has energies 0, 1, and 3, with multiplicities 1, 3, and 5. The quintet therefore carries energy 3. At g=0, the singlet-product ground state is unique and the gap is 1. The uniform chain is recovered at g=1. Intervals extending above g=1 keep the first bond coefficient fixed at 1 and retain the required energy and temperature rescaling.

The strongest near-uniform certificates use the full H² variance bounds and give

| Closed interval in g | Gap lower bound |
| --- | --- |
| [4999249/5000751,5000751/4999249] | 0.020 |
| [9997911/10002089,10002089/9997911] | 0.015 |
| [399901/400099,400099/399901] | 0.010 |
| [399891/400109,400109/399891] | 0.005 |

Each row covers every M≥2. These alternating-chain statements concern even physical lengths. The uniform-chain certificate separately covers odd lengths as well.

### Ordinary spin-1/2 square bilayer

Each layer is a periodic L×L square lattice, with S=σ/2 and S²=3/4. The Hamiltonian is

$$
H_L=\sum_{\mathbf r}\mathbf S_{\mathbf r,1}\cdot\mathbf S_{\mathbf r,2}
+g\sum_{\mathbf r}\sum_{\mu=x,y}\sum_{a=1}^{2}
\mathbf S_{\mathbf r,a}\cdot\mathbf S_{\mathbf r+\mathbf e_\mu,a}.
$$

Here $\mathbf r$ runs over the periodic square lattice, $a$ labels the layer, and $\mathbf e_x,\mathbf e_y$ are the positive lattice unit vectors.

Rung exchange is 1, and both layers have nearest-neighbor exchange g. There are no crossed interlayer bonds or magnetic fields. The system contains 2L² spins, its Hilbert-space dimension is 2^(2L²), and H′=H+3L² I/4. The positive-direction bond sum gives parallel double edges at L=2 and counts each undirected edge once for L≥3. Rectangular seeds use the same convention in each direction.

The all-size results cover every integer square side L≥2, including odd L. They do not assert uniformity over arbitrary aspect ratios. At g>0, the rung-singlet product is a reference state rather than an assumed exact ground state.

### Fully frustrated bilayer

Let $\mathbf T_{\mathbf r}=\mathbf S_{\mathbf r,1}+\mathbf S_{\mathbf r,2}$ and $\mathbf D_{\mathbf r}=\mathbf S_{\mathbf r,1}-\mathbf S_{\mathbf r,2}$, and let $Q$ count rung triplets.
The shifted Hamiltonian is

$$
H'=Q+J\sum_{\langle\mathbf r,\mathbf s\rangle}
\mathbf T_{\mathbf r}\cdot\mathbf T_{\mathbf s},
$$

where the sum follows the same periodic bond-counting convention as the ordinary bilayer.

Each neighboring rung pair has two direct and two crossed bonds. Changing the direct exchange to J+ε while retaining crossed exchange J gives the interaction

$$
(J+\varepsilon/2)\mathbf T_{\mathbf r}\cdot\mathbf T_{\mathbf s}
+(\varepsilon/2)\mathbf D_{\mathbf r}\cdot\mathbf D_{\mathbf s}.
$$

The unperturbed singlet ground space is one-dimensional with zero residual. Excited sectors still have nontrivial structure. For rectangles with both sides at least 3, the analytic bound is gap≥1−5J/2 for 0≤J<2/5, and the actual gap is 1 for 0≤J≤0.3. Including side length 2 changes the uniform range to J<1/3 and the optimal family infimum to min(1,4−12J).

At J=0.3, the three-purity bootstrap also gives the weaker bounds 0.033085166891 for squares L≥2 and 0.132295274293 for L≥4. These remain useful checks of the method. Under the ε perturbation, the trial-state preparations have linear dimensions 23, 93, and 377, even when only one state contributes to a heat trace.

### Large-D and AKLT models

The spin-1 large-D square-lattice Hamiltonian, with D=1, is

$$
H=\sum_i(S_i^z)^2+g\sum_{\langle i,j\rangle}\mathbf S_i\cdot\mathbf S_j.
$$

It has U(1) and spin-reversal structure rather than full SU(2) symmetry. The AKLT reference uses H=ΣP₂, where P₂ projects a neighboring spin pair onto total spin 2. Its gap bound therefore has a different normalization from the Heisenberg-chain result.

Further conventions are given in [Models and normalization](research_20261010/MODELS_AND_NORMALIZATION.md).

## How low-energy calculations reach all sizes

A retained low-energy state contributes a controlled term to a heat trace. The omitted states require both a count and a spectral-tail bound. Together, these bounds supply the heat-trace or purity inequalities used to enlarge temperature and system size. Every successful certificate also includes finite integer windows and a bridge to the smaller systems.

For the ordinary bilayer, the principal seeds contain 4×4, 8×4, and 8×8 rungs. Their 32, 64, and 128 spins span spaces of dimensions 2^32, 2^64, and 2^128. Full diagonalization of the largest seed is unnecessary in some correlated heat-trace ratios. When that seed enters only the numerator, a Rayleigh upper bound from one normalized vector supplies the required lower bound on its heat trace. The two denominator seeds still require conservative treatment of all omitted states. Other filtered constructions require higher moments.

The two-dimensional argument controls temperature and both spatial directions. Rectangular seeds, the order of the operations, and square symmetry affect whether the recurrence starts. The project includes audits of the general d-dimensional extension, the two-dimensional constant K=26, finite-integer interpolation, a common defect domain, and direction exchange or joint ratios. These ingredients explain why a one-dimensional length cannot simply be squared to obtain a two-dimensional certificate.

The size of a trial representation should be kept distinct from the physical Hilbert space. Early bilayer numerator searches used 29 dimensions, increasing to at most 30 after filtering. At g=0.09 and 0.10, the largest numerator search used 43 dimensions and retained one state. The smaller denominator seeds retained 49 and 97 contributions, consisting of one even ground contribution and 3N odd levels. These need not be the lowest 49 or 97 levels in global energy order. Their total search dimensions were 59/125 at g=0.09 and 59/139 at g=0.10. Later preparations used 16/58/57 dimensions. A final two-dimensional filtering plane or three-dimensional denominator does not remove the cost or role of those preparations.

For the uniform chain, an MPS bond dimension of 26, a norm-transfer dimension of 676, local-improvement bounds of 52 or 156 on the MPS bond dimension, and the physical dimension 3^L describe different objects. Successful tail initializations include n=30 with gap≥0.0179, n=32 with gap≥0.0245, and n=34 with gap≥0.0248. Finite-size bridges extend the last bound down to L=2. No minimal-seed theorem has been established.

A comparison of fixed ansatz spaces gives a more limited lower bound on their required flexibility. At g=0.03, a specified six-dimensional space has residual-square lower bound greater than 1.77756×10^-4, while a saved eleven-dimensional construction gives approximately 5.31537×10^-7. This comparison applies to the specified spaces and Rayleigh range. It does not impose an eleven-dimensional minimum on every possible ansatz. The full excitation-shell dimension $\sum_{j=0}^{q}\binom{M}{j}[(2s+1)^2-1]^j$ provides a cost estimate, while sufficiency is determined by the retained levels, full residuals, omitted-spectrum bounds, heat traces, and finite and infinite size windows.

The fully frustrated model at J=0.3 supplies a nonperturbative example with an exact one-state ground space. The perturbed model uses certified nonzero residuals and spectral tails through ε=0.00855. AKLT supplies an exact entangled MPS with bond dimension 2 and control of the 3^L−1 omitted states, although the common thermal-transfer sufficient condition has not passed there. Its successful certificate instead uses the local-projector criterion.

## Results, recovery, and reproduction

The [complete progress record](docs/PROGRESS.md) preserves all previously reported bounds, rational endpoints, finite-size results, unsuccessful searches, and resource exceptions. It also separates the available Stage22 certificates from the later recovered history. Bounds obtained from different constructions can vary nonmonotonically with g without implying the same behavior for the physical gap.

The uniform-chain [all-size proof](research_20261010/uniform_gap_0248_all_sizes_review/PROOF.md) dates to Stage19 and survives in the Stage22 baseline. The later bilayer extension rests on recovered records and a byte-verified Stage33 PDF. Its exact inputs, full proofs, interval data, and review receipts are not yet all available.

On 2026-10-14, bounded reruns checked the archived inputs, a 625-dimensional integer-moment benchmark, and the alternating-chain certificate at g=1/20, reproducing gap≥0.116303868802. These reruns did not reprove every transfer assumption or reproduce other models or later stages. The [replay instructions](research_20261014/readme_audit/replay/README.md) and [scope record](research_20261014/readme_audit/replay/AUDIT_SCOPE.json) specify the checks and exclusions.

Useful starting points are

- [Project rules](AGENTS.md) and [Stage22 overview](research_20261010/overview_stage22/README.md)
- [Heat-trace proof](heat_trace/PROOF.md) and [integer-size bridge](audit/APPENDIX_A_BRIDGE.md)
- [One- to two-dimensional bootstrap](research_20261010/BOOTSTRAP_1D_TO_2D.md), whose older g=0.10 value is superseded by 0.055807148827
- [Fully frustrated analytic proof](two_d_theory/NONPERTURBATIVE_MODELS.md)
- [Recovery index](recovery_20261012/README.md) and [known object paths](recovery_20261012/KNOWN_BLOB_PATHS.json)
- [Baseline audit](research_20261014/readme_audit/baseline_audit.md) and [recovered-history audit](research_20261014/readme_audit/recovered_audit.md)

The original archive entry points are `python verify_archive.py` and `python heat_trace/replay_appendix_a.py`. Individual review directories also contain `REPRODUCE.sh` or audit scripts. Run them in a working copy because some rewrite timing or result JSON. Historical environments recorded Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0. Some exact C++ routes require GMP and a compiler. These records do not imply that new software was installed for the present checks.

Recover the missing Stage32/33 proofs and post38 H³/Ritz outputs before attempting a bounded regression. Any new g=0.12 run also needs controls, entry checks, and an explicit resource budget. See the [next research steps](docs/PROGRESS.md#next-research-steps). This documentation work has produced no new gap certificate.
