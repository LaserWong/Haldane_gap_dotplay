# Gap workflow report

Status: certified_finite_size

Exact Ising gap above the two-dimensional ground space is 4. Near-one thermal-purity bootstrap is obstructed.

Reason: Change to a ground-space-aware criterion; increasing seed size, beta or trial rank cannot remove this obstruction

Scope: the specified finite Hamiltonian and selected sector, if any. Numerical candidates alone do not certify spectral completeness.

## Diagnostics

{
  "U1_symmetry_present": true,
  "cause": "degenerate_Gibbs_ground_state_mixture",
  "failed_assumption": "unique_ground_state",
  "failure_class": "rigorous_method_specific_obstruction",
  "full_hilbert_dimension": 16,
  "general_gap_proof_impossible": false,
  "ground_degeneracy": 2,
  "larger_seed_remedy": false,
  "lower_temperature_remedy": false,
  "minimum_seed_for_near_one_purity": "none within this degenerate family: purity never exceeds 1/2",
  "physical_seed_sites": 4,
  "trial_rank_remedy": false
}
