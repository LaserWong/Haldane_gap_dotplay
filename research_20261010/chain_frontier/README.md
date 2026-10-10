# Chain frontier continuation

Start with [FRONTIER_REPORT.md](FRONTIER_REPORT.md). New candidates and method obstructions are exact producer outputs and require separate independent audit before promotion.

- `run_frontier.py`: isolated, resource-bounded use of existing sparse producer; saves rejected isolation diagnostics.
- `correlated_frontier.py`: exact cancelled first update and accepted/rejected temperature scan.
- `bridge_frontier.py`: every-integer-size finite-window bridge plus small sizes.
- `local_ceiling.py`, `exclude_beta.py`: exact test-vector envelopes for all local comparison parameters and all temperatures.
- `RESOURCE_PLAN.md`: preflight estimates, runtime/RAM constraints and scope.
- `*_ground.json` and `*_trial.npz`: exact local matrices, integer trial vectors, full residuals and energy intervals.
- `*_correlated.json`, `*_bridges.json`, `*_obstruction.json`: executable candidate acceptance or exclusion records, with full rational endpoints.
- `depth3_residual_counterfactual.json`: deliberately optimistic diagnostic, not a physical certificate.

Only one vector per physical patch is retained. Linear trial dimension, entire residual-support dimension and full Hilbert dimension are separate quantities. No full-space diagonalization is performed.
