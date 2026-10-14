# Extending the spin-1 chain certificate with fixed support

Updated October 10, 2026, at 15:19 America/New_York / 19:19 UTC.

Exact candidate certificates at g = .175, .18, .181, and .182 are saved in `candidate_g*.json`.
Their numerical results and resource measurements are in `summary.json`.
Independent review remains required.

| g | Candidate gap for every integer M ≥ 2 |
|---|---:|
| .175 | .026579108896 |
| .18 | .013222512347 |
| .181 | .009728769181 |
| .182 | .005940278341 |

The improvement retains the joint partition-function ratio after changing the update order and applies repeated temperature-first cycles.
The largest support remains 43,294 configurations.
Only a two-dimensional combination of two saved vectors is optimized.
New complete residual calculations are restricted to M = 4, where the Hamiltonian image reaches 1,107 configurations.
Residual-direction filtering at the largest size has a negligible effect on this calculation.

`PROOF.md` gives the argument and `verification.json` records the checks.
Run `REPRODUCE.sh` to replay the calculation.
The frozen earlier files remain unchanged.
The extracted tree contains no Git metadata, and no remote change was made.
