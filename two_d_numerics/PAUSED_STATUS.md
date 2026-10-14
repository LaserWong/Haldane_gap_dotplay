# Results at the October 10 pause

This record describes the October 10, 2026 pause.
The project resumed on October 14, 2026, at 17:36:22 UTC.
The current repository README and AGENTS.md determine the authorized work.
The completed checks and pending tasks below retain their status at the earlier pause.

Checkpoint: 2026-10-10 16:25 UTC. At that time, further research, parameter sweeps, and monitoring required an explicit resumption.

## Completed work

### Independent validation

- Seven graph/basis/reference tests pass (`results/test_models.log`). They check periodic multiedge conventions, independent full tensor matrices against symmetry-block matrices and spectra, SU(2) ladders where applicable, dimer limits, sparse low levels and the spin-1 single-ion reference.
- `results/certificate_crosschecks.json`: the low-energy calculation's spin-1/2 and spin-1 dimer kernels agree with independent rational Clebsch-Gordan transformations exactly. Its bilayer 8-/16-spin trial artifacts reproduce exactly the same rational Rayleigh quotients and complete full-spin-basis residual squared.
- `results/largeD_independent_checks.json`: the new large-D 2x2/4x2 ground proposals reproduce exactly the same Rayleigh quotient and complete residual in an independent full physical-Sz basis. Full small-system spectra lie inside their certified ground intervals.
- The separate independent audit has passed the full large-D g=.01 certificate, including the all-integer L>=2 bridge. Audit record: `../audit/independent/largeD_g001_audit.json`. The implementation crosschecks above are additional independent evidence.

### Independently audited exact-rational interacting certificate

`results/largeD_g1d100_q2_certificate.json` is the independently audited spin-1 D=1, g=.01 three-purity certificate at base size 2. At beta=12 it gives A>=.9898383806359963, B>=.9790341376100279, C>=.9928327376166918, and the three-purity replay returns gap .086452285325. The successful independent audit includes the physical inputs, transfer/interpolation premises and bridge to all integer square sides L>=2. Largest physical dimension: 3^16=43,046,721. Trial support: 241 product configurations. Complete Hamiltonian-action support: 8,321. The ground, residual, comparison and thermal arithmetic are exact-rational. The completed audit is recorded at `../audit/independent/largeD_g001_audit.json`.

### Order-one, exactly structured nonperturbative reference

`fully_frustrated.py` and `results/fully_frustrated_checks.json` independently benchmark the fully frustrated bilayer with rung coupling 1 and all four interrung couplings J=.3. The shifted Hamiltonian is Q+J sum T_i·T_j, with conserved rung-triplet number operators.

- 2x2: unique singlet-product ground, exactly zero residual, gap .4.
- 4x2: unique singlet-product ground, gap .8. Complete reference spectrum obtained by rung-occupation and Sz blocks. Physical dimension 65,536, largest dense block 1,107.
- 2x2 at J=1/3: ground degeneracy 2. At J=.35 the product is an excited eigenstate.
- Small spin-1 star and occupied-plaquette matrices agree with analytic inequalities used in the analytic proof.
- The analytic conclusion is as follows. for all periodic rectangles of side at least 2, the unique-product phase covers 0<=J<1/3 and the uniform infimum gap is min(1,4-12J). This uses triplet-count bounds and is saturated by the 2x2/isolated-triplet states. The theory directory contains the written proof and exact three-purity certificates.
- Ground representation dimension 1 is distinct from the full excited Hilbert-space dimension. Excited interactions are noncommuting.

### Robustness diagnostics only

`frustrated_robustness.py` and `results/frustrated_robustness_diagnostics.json` use the convention: straight J+epsilon, cross J, J=.3. This equals (J+epsilon/2) T_i·T_j+(epsilon/2) D_i·D_j. It is not the symmetric J±epsilon convention.

For epsilon=.005,.01,.02 respectively:

- 2x2 gaps: .369984020939, .340040407779, .281030177572.
- 4x2 gaps: .789973866547, .779851413466, .759030103134.
- 4x2 product-overlap squared: .999442449338, .997720751654, .990492834451.
- Exact reference-vector Rayleigh quotient is zero. Residual squared is 12 epsilon^2 on 2x2 and 18 epsilon^2 on 4x2. Both formulas match the independent physical matrices.

These finite-spectrum values and overlaps are floating-point diagnostics. The low-energy calculations were being extended to include rigorous robustness certificates when work was paused.

### Negative/limitation results retained

- `results/purity_scans.json` includes successful and unsuccessful fixed-width scans. Small finite gaps in isotropic controls do not establish a thermodynamic gap.
- Larger spin-1 large-D base-size-4 tests at g=.02 did not produce an accepted seed on the tested temperatures. The two-bond trial extension reached 34,881 trial configurations and 3,224,129 full-action configurations on 8x8 (64 spin-1 sites), peak process RSS 765,800 KiB, about 75 seconds. The thermal comparison and residual width remain too loose. This is not a failed physical-gap result.
- The simpler 64-site two-excitation trial used 4,033 configurations but produced wider ground intervals. Both outputs are kept as honest complexity/accuracy comparisons.

## Tasks recorded for a later resumption

1. Preserve the completed large-D successful audit record (`../audit/independent/largeD_g001_audit.json`) with the certificate and source. Reconcile any subsequent user-requested revisions against it.
2. Reconcile the low-energy calculation's robustness certificate artifacts with the independent spectra above. Keep straight/cross conventions explicit.
3. If additional robustness representation compression is wanted, an unimplemented idea is to restrict two-triplet support to total-spin singlets and translation/point-group orbit sums. On a 4x4 torus, vacuum plus five pair-separation classes would give six variational basis vectors, while raw support and complete residual support remain larger. This idea has not yet been implemented or validated.
4. The pause did not authorize an automatic restart of the former four-day schedule or new calculations.

All source is local to this directory. Uploaded original files were not edited.
