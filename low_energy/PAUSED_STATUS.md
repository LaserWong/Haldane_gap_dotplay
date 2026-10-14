# Results at the October 10 pause

This record describes the October 10, 2026 pause.
The project resumed on October 14, 2026, at 17:36:22 UTC.
The current repository README and AGENTS.md determine the authorized work.
The completed checks and pending tasks below retain their status at the earlier pause.

Paused at the user's explicit request on 2026-10-10, approximately 16:26 UTC. No numerical process remained active in this calculation at the pause. The pause required a new user instruction before calculations could resume.

## Completed work

- `README.md`: proof of the single-Ritz-state method with spectral completeness and an exact tail bound, a method comparison, and primary references.
- `analytic_dimer_baseline_replay.json`: successful independent scalar rerun of the uploaded analytic dimer baseline.
- `ground_tail.py`: full-sector single-vector Ritz proposal and exact integer verification.
- `dimer_subspace.py`: exact sparse-support verification, including states outside the trial space, with full excitation-shell or selected Krylov-support proposals.
- `local_relative_bound.py`: exact local 16x16/81x81 inertia and affine dimer spectral comparison.
- `bilayer_seed.py`, `chain_sparse_seed.py`, `fully_frustrated.py`: executable certified input construction and scalar replay.
- `dimension_counts.py/json`: exact full-shell and total-Sz=0 dimensions.
- `method_comparison.json`: quantitative difference between complete dimer-bin tails and the crude full-dimension-times-cutoff tail. Display values here are diagnostics. Underlying certificate endpoints are rational elsewhere.
- Saved `*_ground.json`, `*_trial.npz`, `*_ritz.npz`, seed JSON, and logs contain both accepted and rejected proposals. Nothing in the uploaded original was edited.

## Independent audit status

1. Spin-1 alternating chain g=1/20, n=2 was independently rebuilt and exact residuals/replay verified by the independent audit. At beta = 10, the gap bound for all cell counts is 0.116303868802, with the separately verified short-size bridge.
2. Spin-1/2 columnar matrices and all spin-1/2 and spin-1 local dimer kernels were checked independently. The small bilayer sparse trials were expanded into the entire physical-spin basis. Exact Rayleigh and entire residual-squared agreed as identical Fractions.
3. Spin-1/2 ordinary bilayer g=1/100 was independently audited together with both transfer operators. Certificate beta = 20 gives 0.072950533962 for all integer square side L>=4, before any separately established small-size bridge.
4. Relative-form bilayer g=1/50 and spin-1 bilayer g=1/200 are implemented exact-arithmetic successes. Independent audit was requested. Consult the sibling audit files for its final status rather than assuming it finished.
5. Longer-chain g=.1,.125,.15, selected-depth 3/4 trials, and the fully-frustrated perturbation extension are completed calculations but were not independently audited at pause. Treat their scope as provisional until reviewed.

## Quantitative coupling/depth results

The chain has unit strong bonds and weak Heisenberg coupling g, with two physical spin-1 sites per cell. These certificates establish sufficient coupling ranges. They do not determine the largest coupling with a physical gap.

- g=.05, n=2 cells, full-sector one-vector trial: The largest sector has dimension 1107 and the full space has dimension 6561. At beta = 10, the gap bound is 0.116303868802 for all M>=2 after the audited short-size argument.
- g=.1, n=2: tested temperatures fail, despite ground energy intervals near machine-vector exactness. Changing n is essential here.
- g=.1, n=4, selected support depth 2: The largest trial space has dimension 453, its Hamiltonian image reaches 5205 configurations, and the full space has dimension 43,046,721. At beta = 24, the calculation gives 0.118954972866 for M>=8. The same exact local form bound supplies a short-M bridge at least 0.377320166292 for 2<=M<=7.
- g=.125, n=4, depth 3: The largest trial space has dimension 5205 and its Hamiltonian image reaches 43294 configurations. At beta = 28, the calculation gives 0.068202652189 for M>=8. The local bound is positive and larger than this gap through M=7, so a short-M bridge is available, pending audit.
- g=.15, n=4, depth 3: The largest trial space has dimension 5205 and its Hamiltonian image reaches 43294 configurations. At beta = 56, the calculation gives 0.014789588586 for M>=32. At beta = 64, the calculation gives 0.011704389912 for M>=16. No all-small-M bridge has been completed.
- g=.15, depth 4: The largest trial space has dimension 43294 and its Hamiltonian image reaches 245870 configurations. The run took 15.52 s with peak memory 326.5 MiB. The ground-energy interval has width 6.13e-6, compared with 2.98e-4 at depth 3. The best tested gap improves only modestly to 0.017013326349. This isolates the completeness/tail and spatial-curvature bottleneck after residual error is made much smaller. Consult its JSON for exact final length.

The ordinary spin-1/2 bilayer g=.03 remains unaccepted with these ground-only dimer-bin bounds. The seed-size analysis establishes a stronger all-beta/all-local-parameter obstruction for this *certificate family*, not a physical gaplessness claim. Improving ground digits alone does not remove that obstruction.

## New nonperturbative reference extension, unaudited

`fully_frustrated.py` uses unit rungs, all four inter-rung spin exchanges J=.3, and additional straight-leg coupling epsilon=.005. Thus straight exchanges are J+epsilon and crossed exchanges J.

The fully-frustrated baseline commutes with every rung-triplet occupation. For each occupied set A, an exact weighted-star inequality gives

f(A)=|A|-J[active edge weight + half the sum of maximal incident active weights].

The occupancy sector has exact dimension 3^|A|. Enumerating at most 2^16 subsets produces complete reference bins without diagonalizing their spin Hamiltonians. Adding the exact local epsilon comparison shifts each bin by -4a|A|-2Nb. The vacuum remains the unique lowest reference bin for the recorded parameters, which is checked before Temple/tail use.

At epsilon=.005 the largest 32-spin patch uses 377 trial configurations and 21345 reached configurations. The seed at beta = 32 is accepted by the correlated three-purity recursion. The full record is `ff_seed_J3d10_eps1d200_depth0.json`. This extension and its occupancy-star proof require independent audit before presenting them as a final theorem.

## Work pending at the pause

- Independently audit every new local PSD, occupancy-star count, sparse residual, and multistep scalar input.
- Close the small-size bridge for g=.15 chain, if a claim covering all sizes is desired.
- Build the coupling-versus-depth/size frontier with certified sufficient and necessary bounds. Avoid calling the largest tested g a maximum.
- Explore a certified entire low band (ground plus all one-triplet states) to overcome the ordinary-bilayer .03 tail obstruction. No multilevel code has yet been run.
- A proposed multilevel lemma uses a certified global(k+1)-st eigenvalue, a residual/operator-angle bound, and a complement compression. The derivation should be independently checked before implementation. Algebraic orthonormalization can be avoided using exact rational Gram matrices and small generalized-inertia tests.
- Further compress q<=2 SU2-singlet trials to vacuum plus one singlet per unordered rung pair, potentially six translation/point-group basis vectors on 4x4. No six-dimensional certificate has been implemented here.
- Nonperturbative uniform spin-1 Heisenberg results were independently replayed elsewhere from the user's archive with a bond-dimension 26 MPS plus separate trace certification. This is an archive reproduction, not a new result of this directory.
