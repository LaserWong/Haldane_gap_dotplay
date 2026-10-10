# Paused checkpoint

Paused at the user's explicit request on 2026-10-10, approximately16:26 UTC. No numerical process from this worker remains active. Do not resume calculations until the user authorizes resumption.

## Complete and saved

- `README.md`: proof of the one-Ritz-state, no-missed-state, exact tail method; method comparison; primary references.
- `analytic_dimer_baseline_replay.json`: successful independent scalar rerun of the uploaded analytic dimer baseline.
- `ground_tail.py`: full-sector single-vector Ritz proposal and exact integer verification.
- `dimer_subspace.py`: exact sparse-support verification, including leaked states; full excitation-shell or selected Krylov-support proposals.
- `local_relative_bound.py`: exact local16x16/81x81 inertia and affine dimer spectral comparison.
- `bilayer_seed.py`, `chain_sparse_seed.py`, `fully_frustrated.py`: executable certified input construction and scalar replay.
- `dimension_counts.py/json`: exact full-shell and total-Sz=0 dimensions.
- `method_comparison.json`: quantitative difference between complete dimer-bin tails and the crude full-dimension-times-cutoff tail. Display values here are diagnostics; underlying certificate endpoints are rational elsewhere.
- Saved `*_ground.json`, `*_trial.npz`, `*_ritz.npz`, seed JSON, and logs contain both accepted and rejected proposals. Nothing in the uploaded original was edited.

## Independent audit status

1. Spin1 alternating chain g=1/20, n=2 was independently rebuilt and exact residuals/replay verified by the audit worker. At beta10 the all-cell-count gap is0.116303868802, with the separately verified short-size bridge.
2. Halfspin columnar matrices and all halfspin and spin1 local dimer kernels were independently checked by the numerics worker. The small bilayer sparse trials were expanded into the entire physical-spin basis; exact Rayleigh and entire residual-squared agreed as identical Fractions.
3. Halfspin ordinary bilayer g=1/100 was independently audited, including both transfer operators, by the audit worker. Certificate beta20 gives0.072950533962 for all integer square side L>=4, before any separately established small-size bridge.
4. Relative-form bilayer g=1/50 and spin1 bilayer g=1/200 are implemented exact-arithmetic successes. Independent audit was requested; consult the sibling audit files for its final status rather than assuming it finished.
5. Longer-chain g=.1,.125,.15, selected-depth3/4 trials, and the fully-frustrated perturbation extension are completed calculations but were NOT independently audited at pause. Treat their scope as provisional until reviewed.

## Quantitative coupling/depth results

The chain has unit strong bonds and weak Heisenberg coupling g, with two physical spin1 sites per cell. These are sufficient successes, not a claim of the maximal physical g.

- g=.05, n=2 cells, full-sector one-vector trial: max sector1107/fullD6561; beta10 gap0.116303868802; all M>=2 after the audited bridge.
- g=.1, n=2: tested temperatures fail, despite ground energy intervals near machine-vector exactness. Changing n is essential here.
- g=.1, n=4, selected support depth2: max trial453/reached5205/fullD43,046,721; beta24 gives0.118954972866 for M>=8. The same exact local form bound supplies a short-M bridge at least0.377320166292 for2<=M<=7.
- g=.125, n=4, depth3: max trial5205/reached43294; beta28 gives0.068202652189 for M>=8. The local bound is positive and larger than this gap through M=7, so a short-M bridge is available, pending audit.
- g=.15, n=4, depth3: max trial5205/reached43294; beta56 gives0.014789588586 for M>=32; beta64 gives0.011704389912 for M>=16. No all-small-M bridge has been completed.
- g=.15, depth4: max trial43294/reached245870; runtime15.52s, peak326.5MiB; ground width6.13e-6, versus2.98e-4 at depth3. The best tested gap improves only modestly to0.017013326349. This isolates the completeness/tail and spatial-curvature bottleneck after residual error is made much smaller. Consult its JSON for exact final length.

The ordinary halfspin bilayer g=.03 remains unaccepted with these ground-only dimer-bin bounds. The seed-size worker has a stronger all-beta/all-local-parameter obstruction for this *certificate family*, not a physical gaplessness claim. Improving ground digits alone does not remove that obstruction.

## New nonperturbative reference extension, unaudited

`fully_frustrated.py` uses unit rungs, all four inter-rung spin exchanges J=.3, and additional straight-leg coupling epsilon=.005. Thus straight exchanges are J+epsilon and crossed exchanges J.

The fully-frustrated baseline commutes with every rung-triplet occupation. For each occupied set A, an exact weighted-star inequality gives

 f(A)=|A|-J[active edge weight + half the sum of maximal incident active weights].

The occupancy sector has exact dimension3^|A|. Enumerating at most2^16 subsets produces complete reference bins without diagonalizing their spin Hamiltonians. Adding the exact local epsilon comparison shifts each bin by -4a|A|-2Nb. The vacuum remains the unique lowest reference bin for the recorded parameters, which is checked before Temple/tail use.

At epsilon=.005 the largest32spin patch uses377 trial configurations and21345 reached configurations. Beta32 is accepted by the correlated three-purity recursion. The full record is `ff_seed_J3d10_eps1d200_depth0.json`. This extension and its occupancy-star proof require independent audit before presenting them as a final theorem.

## Pending work, do not start while paused

- Independently audit every new local PSD, occupancy-star count, sparse residual, and multistep scalar input.
- Close the small-size bridge for g=.15 chain, if a claim covering all sizes is desired.
- Build the coupling-versus-depth/size frontier with certified sufficient and necessary bounds; avoid calling the largest tested g a maximum.
- Explore a certified entire low band (ground plus all one-triplet states) to overcome the ordinary-bilayer .03 tail obstruction. No multilevel code has yet been run.
- The parent proposed a safe multilevel lemma using a certified global(k+1)-st eigenvalue, a residual/operator-angle bound, and a complement compression. The derivation should be independently checked before implementation; algebraic orthonormalization can be avoided using exact rational Gram matrices and small generalized-inertia tests.
- Further compress q<=2 SU2-singlet trials to vacuum plus one singlet per unordered rung pair, potentially six translation/point-group basis vectors on4x4. No six-dimensional certificate has been implemented here.
- Nonperturbative uniform spin1 Heisenberg results were independently replayed elsewhere from the user's archive with a bond-dimension26 MPS plus separate trace certification. This is an archive reproduction, not a new result of this directory.
