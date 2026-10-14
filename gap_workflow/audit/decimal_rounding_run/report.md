# Gap workflow report

Status: certified_finite_size

Exact finite-size gap lower bound 1 in the full space. No uniform-family conclusion.

Reason: No general geometric bootstrap adapter is registered. Finite-size certification alone is insufficient.

This run concerns one finite Hamiltonian and its stated sector, if any. A floating-point Ritz calculation does not certify spectral completeness. No general uniform-family bootstrap adapter is implemented. Failure does not establish gaplessness or impossibility.

## Diagnostics

{
  "bootstrap": {
    "admission_requires": [
      "Hamiltonian normalization and local interaction hypotheses",
      "boundary and patch geometry",
      "proved overlap constants and finite-size threshold",
      "certified seed bounds at every required size",
      "independently checked theorem hypotheses"
    ],
    "forecast_is_not_proof": true,
    "minimal_seed_physical_size": null,
    "minimal_trial_dimension": null,
    "reason": "No general geometric bootstrap adapter is registered. Finite-size certification alone is insufficient.",
    "status": "criterion_unsupported",
    "uniform_family_claim": false
  },
  "full_hilbert_dimension": 2,
  "geometric_seed_failure": "not evaluated: general bootstrap adapter unavailable",
  "minimal_seed_size": "unknown: requires an applicable geometric criterion and certified multi-size data",
  "physical_seed_sites": 1,
  "requested_trial_rank": 6,
  "tail_completeness": "exact full-working-matrix inertia certificate",
  "time_forecast": "uncalibrated; no guaranteed completion-time estimate",
  "trial_approximation": "converged numerical candidate",
  "working_dimension": 2
}
