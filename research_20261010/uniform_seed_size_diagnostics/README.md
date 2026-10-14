# Uniform spin-one seed-size diagnostics

Exact producer checks, awaiting independent review.

For the fixed archived D26 one-Rayleigh numerator at length 2n, the specified
G-based thermal-first recipe fails at every beta for n=6,8,10,12. The n=6/8
checks explicitly include the newly accepted joint-aware conversion and every
legal fixed time-first delay. For n=10/12 the first G already fails because four
orthogonal rational denominator vectors give global J caps 3/25 and 19/100.
Two vectors alone give the sufficient obstruction J<3/10 at both sizes.

This excludes a fixed certification recipe, not the physical Haldane gap or
all seeds/MPS/bootstrap methods. No n>=14 support or full spectral
diagonalization was performed.

- PROOF.md: model, exact scopes, joint-aware replay, hot/box/cold proof.
- uniform_seed_size_diagnostics.json: exact all-beta rational witnesses.
- exact_trial_data.json: physical actions, energies, orthogonality and support counts.
- trial_n*_sz*.json.gz: all proposed integer coefficients. Derived vectors are exact symmetry constructions.
- mps_lengths.out: exact archived-block contractions at 12,16,20,24.
- REPRODUCE.sh: exact replay without an eigensolver.
- INPUT_MANIFEST_SHA256.json: frozen inherited source hashes.
- MANIFEST_SHA256.json: this producer package seal.
- next_size_cost_estimate.json: analytic n=14 resource estimate only.

Replay writes only this directory and updates timing metadata. Preserve the
sealed package before rerunning if exact original bytes matter. No root files,
frozen inputs or remote repository were changed.
