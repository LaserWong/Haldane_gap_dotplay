# Extend the spin-one chain without large state expansion

Updated 2026-10-10 15:19 America/New_York / 19:19 UTC.

Exact candidates at g=.175, .18, .181, and .182 are in `candidate_g*.json`; numerical results and resource measurements are in `summary.json`. External independent review is still required.

| g | All-integer M≥2 gap candidate |
|---|---:|
| .175 | .026579108896 |
| .18 | .013222512347 |
| .181 | .009728769181 |
| .182 | .005940278341 |

The improvement retains the joint partition-function ratio after changing direction order and repeats temperature-first cycles. Largest support stays 43,294; only a two-dimensional combination of two saved vectors is optimized. New complete residuals are restricted to M=4, with reached support 1,107. Largest residual-direction filtering is quantitatively negligible for this route.

Read `PROOF.md`, then `verification.json`. Run `REPRODUCE.sh` to replay. Frozen prior files were not altered. No Git metadata is present in this extracted tree and no remote change was made.
