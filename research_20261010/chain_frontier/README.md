# Alternating-chain candidates and obstructions

[FRONTIER_REPORT.md](FRONTIER_REPORT.md) describes the new candidates and method-specific obstructions. These exact producer outputs still require independent review before acceptance.

- `run_frontier.py`: isolated, resource-bounded use of the existing sparse producer that saves rejected isolation diagnostics.
- `correlated_frontier.py`: exact cancelled first update and accepted/rejected temperature scan.
- `bridge_frontier.py`: every-integer-size finite-window bridge plus small sizes.
- `local_ceiling.py`, `exclude_beta.py`: exact test-vector envelopes for all local comparison parameters and all temperatures.
- `RESOURCE_PLAN.md`: preflight estimates, runtime/RAM constraints and scope.
- `*_ground.json` and `*_trial.npz`: exact local matrices, integer trial vectors, full residuals and energy intervals.
- `*_correlated.json`, `*_bridges.json`, `*_obstruction.json`: executable candidate acceptance or exclusion records, with full rational endpoints.
- `depth3_residual_counterfactual.json`: deliberately optimistic diagnostic, not a physical certificate.

Each physical patch retains one vector. Its linear trial dimension, full residual-support size and full Hilbert dimension measure different objects. The calculation does not diagonalize the full space.
