# Gap workflow report

Status: certified_finite_size

Exact finite-size gap lower bound 5247173023625625600484265145630437118717390625273393991661/12758626649727536241481881626987035086852223198815120638278 in the full space. No uniform-family conclusion.

Reason: No general geometric bootstrap adapter is registered. Finite-size certification alone is insufficient.

Scope: the specified finite Hamiltonian and selected sector, if any. Numerical candidates alone do not certify spectral completeness.

## Diagnostics

{
  "all_sector_coverage_required": true,
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
  "exact_backend": "complete Sz-sector partition",
  "exact_required_block_dimension": 70,
  "full_hilbert_dimension": 256,
  "geometric_seed_failure": "not evaluated: general bootstrap adapter unavailable",
  "ground_multiplicity": 1,
  "ground_multiplicity_assumption": null,
  "ground_multiplicity_source": "inferred by exact certificate",
  "minimal_seed_size": "unknown: requires an applicable geometric criterion and certified multi-size data",
  "next_experiments": [
    "Fix a proved geometry-specific bootstrap threshold before forecasting a sufficient physical seed size.",
    "For each explicitly specified larger model, run resource planning before allocating a basis.",
    "Compare increasing trial ranks at fixed physical size to separate trial error from geometric seed failure.",
    "Calibrate matvec time on an admitted small pilot; time extrapolation remains heuristic.",
    "Call a passing size sufficient, never minimal unless all smaller admissible sizes are excluded."
  ],
  "physical_seed_sites": 8,
  "requested_trial_rank": 6,
  "tail_completeness": "exact full-working-matrix inertia certificate",
  "time_forecast": "uncalibrated; no guaranteed completion-time estimate",
  "trial_approximation": "converged numerical candidate",
  "working_dimension": 256
}
