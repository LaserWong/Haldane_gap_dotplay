# Gap workflow report

Status: candidate_only

Floating-point finite-size candidates only; no certified gap.

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
  "failure_class": "tail_completeness_or_exact_certificate_unresolved",
  "full_hilbert_dimension": 2,
  "geometric_seed_failure": "not evaluated: general bootstrap adapter unavailable",
  "minimal_seed_size": "unknown: requires an applicable geometric criterion and certified multi-size data",
  "next_experiments": [
    "Fix a proved geometry-specific bootstrap threshold before forecasting a sufficient physical seed size.",
    "For each explicitly specified larger model, run resource planning before allocating a basis.",
    "Compare increasing trial ranks at fixed physical size to separate trial error from geometric seed failure.",
    "Calibrate matvec time on an admitted small pilot; time extrapolation remains heuristic.",
    "Call a passing size sufficient, never minimal unless all smaller admissible sizes are excluded."
  ],
  "physical_seed_sites": 1,
  "requested_trial_rank": 6,
  "tail_completeness": "not yet certified",
  "time_forecast": "uncalibrated; no guaranteed completion-time estimate",
  "trial_approximation": "converged numerical candidate",
  "working_dimension": 2
}
