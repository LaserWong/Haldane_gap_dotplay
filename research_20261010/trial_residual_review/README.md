# Fixed-space residual and budget review

Updated 2026-10-10 14:19 America/New_York (EDT) / 18:19 UTC.

**PASS.** Four discrete ordinary-bilayer 4×4 fixed-6D residual obstructions and their 11D constructive comparisons are independently verified. The proof is uniform over each saved Rayleigh interval. Full q4 leakage is freshly rebuilt, and complete 11D moments match hash-verified independently audited geometry.

The residual-to-width and entropy/startup formulas are valid. Separate independent arithmetic reproduces all 18 scoped entropy-rank tests, three startup eighth-power inequalities, and the 13-step target replay.

- `REVIEW.md` gives the proof, independence boundary, endpoint checks, and dimension limitations.
- `results/residual_review.json` contains exact obstruction and wider-interval witnesses.
- `results/budget_review.json` contains exact independent entropy/startup bounds.
- `audit_residual.py` and `audit_budgets.py` import no producer code.
- `snapshot/` freezes the inputs used by the checks.
- `REPRODUCE.sh` reruns both tests with local-only writes.

This establishes an accuracy floor inside a specified ansatz. It is not a universal minimum linear dimension, a continuous coupling theorem, or a complete-band/gap proof by residuals alone.

No computation remains running. The next meaningful extension would separately specify and test intermediate 7–10 dimensional enlargements or a parameter-uniform obstruction. Neither has been asserted here.
