# Coupling, seed size, and trial support in the spin-1 chain

Updated 2026-10-10 13:38 EDT / 17:38 UTC.

## Verification status and main finding

These files contain **new exact-arithmetic candidate certificates** awaiting independent review. The independent review concerns the new physical inputs, cancelled recursion, finite windows and obstruction certificates. Existing independently audited results through g=0.15 remain in `../chain_audit/CHAIN_CERTIFICATE_PROOF.md` and are unchanged.

The first new pass finds all-integer-size candidates:

| Weak g | Support depth | Largest linear trial dimension | Initial beta | Eventual regime | Proposed all-M≥2 gap |
|---|---:|---:|---:|---:|---:|
| 4/25 = 0.16 | 4 | 43,294 | 80 | M≥64 | 0.004358246531 |
| 161/1000 = 0.161 | 4 | 43,294 | 86 | M≥128 | 0.001952374069 |
| 129/800 = 0.16125 | 4 | 43,294 | 88 | M≥256 | 0.001075806295 |

Each row retains one vector on each seed patch. The largest full residual support is 245,870. The full Hilbert space on eight dimers has dimension 9^8=43,046,721. These are three sufficient points, not a proof of acceptance at every coupling between them, a maximal method threshold, or a physical phase boundary. The completed depth-five test at g=0.1615 uses 245,870 trial coordinates and 939,326 full-residual coordinates. It improves the ground enclosure enough to establish the stronger method obstruction below, rather than producing another accepted seed.

A rigorous **method obstruction at g=323/2000=0.1615** excludes every inverse temperature and every local comparison parameter in the declared ground-only-numerator, independent-dimer-bin tail family, even allowing zero residual-width penalties and arbitrarily sharp ground refinement inside the saved intervals. It also excludes the first-step-cancelled version. This exclusion is pending independent audit. Additional all-beta obstructions at g=13/80=0.1625 and g=7/40=0.175 have also been saved. Neither is a statement about the true physical gap.

## Model and exact whole-space inputs

The Hamiltonian and boundary multiplicities are exactly those of the independently audited chain:

H_M(g) = sum_i S_(i,R)·S_(i+1,L) + g sum_i S_(i,L)·S_(i,R), spin one,

with unit strong bonds, M two-spin cells, periodic boundary conditions and all integers M≥2. Both distinct strong bonds are retained at M=2. The full dimension is 9^M. This is never the trial dimension or an MPS bond dimension.

The existing producer `low_energy/dimer_subspace.py` is imported without source edits, and its output directory is overridden explicitly. It constructs a rational orthogonal dimer basis, proposes a single Ritz vector in a selected Krylov-support coordinate space, rounds it to a dyadic integer vector, and includes **every state reached by H** in the exact metric residual. New `_trial.npz` files contain the full integer vector and its coordinate basis. New `_ground.json` files contain exact rational Rayleigh quotients, residual squares, interval endpoints, local comparisons and graph multiplicities.

A certified local inequality gV+a(h_i+h_j)+bI ≥ 0 gives

H_M ≥ -2M + alpha sum_i h_i - M b, alpha=1−2a>0.

The reference polynomial (1+3x+5x^3)^M counts every eigenvalue with multiplicity. Its full count is 9^M, so min–max gives every ordered physical eigenvalue a lower bound and, in particular, lambda_1 ≥ c_M = -2M+alpha−M b. Where rho<c_M, the whole-space ground interval is

L_M = rho − R²/(c_M−rho) ≤ E_0(M) ≤ U_M = rho.

It is the full-spectrum comparison, together with rho<c_M, that certifies unique ground-state isolation. A small residual alone does not establish completeness.

For beta>0, the exact majorant Q_M^+ bounds exp(beta U_M) Z_M(beta):

Q_M^+ = exp(beta(U_M−L_M)) + exp(-beta(-2M−Mb−U_M))[(1+3 exp(-alpha beta)+5 exp(-3 alpha beta))^M−1].

All exponentials are enclosed by rational outward arithmetic. Saved twelve-decimal lower endpoints and integer vectors are the proof inputs. Floating values are displays or proposals only.

## Why cancelling the first ratio matters

Let S=Z_(2n)(beta)/Z_n(beta)^2 and T=Z_(2n)(2beta)/Z_(2n)(beta)^2. Their exact product is

J=S²T=Z_(2n)(2beta)/Z_n(beta)^4.

Rather than multiply separately bounded S and T, bound this cancelled expression directly:

J ≥ exp(-2 beta(U_(2n)−2U_n))/(Q_n^+)^4,
T ≥ 1/(Q_(2n)^+)².

With G(x)=1−(1−x)²/(2x²), the first doubled-scale inputs are S_1≥G(J_lower), T_1≥G(T_lower² S_1). The existing exact sequential recursion resumes at 2n,2beta. This requires no new trace, no extra eigenstate and no new physical approximation. It simply avoids double-counting the common intermediate heat-trace error. `correlated_frontier.py` saves every accepted and rejected temperature.

## All-size bridges

The finite-window lemma in `../root_review/finite_window_2d.py` is used only through its one-dimensional function. Given S(n,beta)≥S and T(2n,beta)≥T with P=S²T>1/2, define

w=(1+sqrt(2P−1))/2, r=(1−w)/w, D=T/(1+r²), I=(1−r) min(S sqrt(D),D).

Then every integer n≤M≤2n has thermal purity at least I. If I>1/2, its gap is at least log(I/(1−I))/beta. Square roots and emitted gap values are checked with exact outward enclosures. This includes odd M and does not assume a positive transfer spectrum.

The three accepted rows start this interpolation at n=8 after the cancelled first step. Every intermediate window is explicitly recorded in `*_correlated_bridges.json`, and every window gap exceeds that row's eventual gap.

- g=0.16: windows 8–16,16–32,32–64 have gaps 0.004786281211,0.004941728136,0.005042826756. A separately optimized local comparison gives 0.006304485945 throughout 2≤M≤7.
- g=0.161: local comparison handles 2≤M≤6. A separate M=7 depth-two vector uses only 365 trial coordinates and 3,683 reached coordinates. Its exact upper ground pivot combined with the ordered second-level bound closes M=7. Four windows cover 8 through 128.
- g=0.16125: the same small-size strategy applies. Window gaps through M=256 are 0.001283948378,0.001095353433,0.001126137799,0.001202344641,0.001232945173, all larger than 0.001075806295.

## Separating the three limitations

### Residual precision / trial-support demand

At g=0.16, depth 3 has largest trial dimension 5,205, full reached support 43,294, exact residual-square display 6.27817886018e-5 and ground-interval width 0.000820728317409. No tested cancelled seed at beta32,34,…,160 accepts.

Depth 4 increases the trial dimension to 43,294 and the reached support to 245,870. Its residual-square display 1.49237762468e-6 and interval width 0.0000195060398861 permit 14 of those temperatures to accept. This is an observed sufficient demand within this coordinate-support family, not a lower bound on every possible ansatz.

`depth3_residual_counterfactual.json` deliberately sets each depth-three interval width to zero while keeping its current Rayleigh pivot and tail comparison. Fourteen temperatures would then accept. This counterfactual is not asserted to enclose a physical energy. It diagnoses the residual penalty as material at this depth.

At g=0.1615, going from depth 4 to depth 5 increases the trial support 43,294→245,870 and reduces the ground width 2.37194706236e-5→2.37048574793e-7. The beta80…104 grid at quarter-unit steps still has no acceptance. More importantly, the tighter **actual** interval now permits an all-beta/all-a obstruction even after setting the residual-width penalty to zero, so further ground refinement cannot rescue this specified recipe at that coupling.

### Complete-tail / ground-isolation failure

At g=0.175,n=4,depth 4, the N=8 ground width is 0.000731547742095 but the comparison cutoff is only 0.00511519467310 above the Rayleigh pivot. The 24 first-reference-excitation states therefore decay far too slowly in the tail bound. Every tested uncorrelated beta16…160 fails, and the all-beta proof below rules out both declared recipes after any further ground refinement inside the saved intervals.

At g=0.2,n=4,depth 4, the N=8 exact residual square is only 1.47202542039e-5, yet rho=-16.2240143800 is above c=-16.3318396199. Whole-space isolation fails. The saved record is explicitly `rejected_whole_space_isolation_exact_residual_only`. Its coarse ground interval is valid by comparison plus variational bounds, but no Temple or gap claim is made.

### Finite-geometry curvature / increasing seed size

At g=0.175, a larger n=6 seed was actually tested at depth 3. The N=12 trial has 14,863 coordinates, reached support 187,930, full dimension 9^12=282,429,536,481 and residual-square 0.000587250798985. Its rho=-24.2556013775 is above c=-24.4345711919, so its current complete-bin comparison fails isolation before thermal bootstrapping. Merely increasing seed size makes this extensive comparison penalty worse. The observed failure is not an all-depth impossibility theorem for n=6.

The all-beta obstructions also isolate a competing finite-size curvature. Positive kappa=L_(2n)−2U_n makes the optimistic cancelled spatial argument at most exp(-2 beta kappa). Cooling improves a positive spectral tail cutoff, but eventually destroys this ground-only spatial lower bound at fixed small n.

## All-beta, all-local-parameter obstruction

For any exact local test vector u in the rational dimer metric, write v=<gV>_u and h=<h_i+h_j>_u. The variational inequality gives

lambda_min(gV+a(h_i+h_j)) ≤ v+a h

for every real a. Therefore the best possible second-bin shift in the local-comparison family obeys

1−2a−Nb(a) ≤ 1+Nv+(Nh−2)a.

`local_ceiling.py` constructs two dyadic test vectors whose slopes have opposite signs. The minimum of their affine bounds has a global maximum at the exact rational intersection. This gives an upper bound C_N on the cutoff for **all a**, not just a sampled grid. The saved vectors, metric norm, h and gV expectations make the bound independently replayable.

Allow arbitrary sharpened ground pivots inside the existing intervals and remove their width penalties. Then delta_N^max=-2N+C_N−L_N implies the recipe majorant is still at least

Q_N^+ ≥ 1+3N exp(-beta delta_N^max).

This is a lower bound on the recipe's upper majorant, not a lower bound on the physical partition function. Combining it with kappa=L_(2n)−2U_n gives optimistic upper envelopes for the recipe's J_lower and T_lower. Enclose these on each beta interval and propagate **upward** through the monotone G updates. Entry into S²T≤1/2 proves permanent failure: G(x)−x=(1−x)(2x−1)(x+1)/(2x²)≤0 there, so the recursion cannot escape to its small-defect region.

For g=0.1625, `chain_sparse_s1_g13d80_n4_depth4_obstruction.json` excludes [0,64],[64,80],[80,88],[88,96],[96,112],[112,128],[128,256]. The curvature bound excludes every beta≥256. Thus all positive beta and all valid local a are covered, even if the ground energies are subsequently sharpened to arbitrary precision inside the current certified intervals.

For g=0.175, an even shorter certificate splits at beta128. The optimistic thermal lower-bound ceiling is 0.006560076526 for beta≤128, forcing immediate failure. For beta≥128 the optimistic cancelled spatial argument is≤0.493807629117<1/2. `local_ceiling_g7d40_N8.json` contains every exact fraction.

For g=0.1615, the depth-four optimistic envelope was unresolved near beta92.27, so its grid rejection was not treated as an exclusion. The completed depth-five enclosure resolves this: `chain_sparse_s1_g323d2000_n4_depth5_obstruction.json` contains 33 exact excluded intervals covering[0,256], with the curvature tail excluding beta≥256. Its optimistic cutoff gaps are at most 0.333462044010 (N=4) and 0.0692604333044 (N=8), and kappa≥0.00249603963999. This is the strongest method obstruction in the present pass. The sufficient point 0.16125 and excluded point 0.1615 are separated by 0.00025, but no monotonicity theorem or unique critical coupling is inferred.

## Reproduction and recoverability

Run from the repository root with PYTHONDONTWRITEBYTECODE=1 and OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1.

1. `python research_20261010/chain_frontier/run_frontier.py --g 4/25 --n 4 --depth 4`
2. `python research_20261010/chain_frontier/correlated_frontier.py research_20261010/chain_frontier/chain_sparse_s1_g4d25_n4_depth4.json`
3. `python research_20261010/chain_frontier/bridge_frontier.py research_20261010/chain_frontier/chain_sparse_s1_g161d1000_n4_depth4_correlated.json`
4. `python research_20261010/chain_frontier/exclude_beta.py research_20261010/chain_frontier/chain_sparse_s1_g13d80_n4_depth4.json`
5. `python research_20261010/chain_frontier/local_ceiling.py --record research_20261010/chain_frontier/chain_sparse_s1_g7d40_n4_depth4.json`

The sparse runner checkpoints each ground record and each temperature. Rejected Temple conditions preserve exact vectors and residuals using the existing producer's exception-frame data, clearly labeled as rejected, rather than modifying or weakening that assertion. Saved valid ground records are reused on rerun. The first g=0.2 attempt aborted at the original assertion before saving. Its one recorded recovery rerun only captured that already-computed diagnostic under the explicit rejected schema.

`RESOURCE_PLAN.md` gives preflight estimates and enforced caps. All files in this task are new under this directory. Repository-wide status and publication are handled separately. No remote push was performed. This workspace is an exported tree without a local `.git` directory. The recorded source commit is 6be889a30f642bde77fb89af75b3a7379615bed1 from CURRENT_STATUS. A final `verify_archive.py` replay passed all 1,149 baseline hashes.
