# Review of fixed-space residuals and budgets

Updated 2026-10-10 14:19 America/New_York (EDT) / 18:19 UTC.

**PASS.** The review independently verifies four discrete ordinary-bilayer 4×4 residual obstructions in the fixed 6D space and their constructive 11D comparisons. Each proof holds uniformly over its saved Rayleigh interval. The full q4 leakage was rebuilt afresh, and the complete 11D moments agree with hash-verified, independently audited geometry.

The residual-to-width and entropy/startup formulas are valid. Separate independent arithmetic reproduces all 18 scoped entropy-rank tests, the three startup eighth-power inequalities, and the 13-step target replay.

- `REVIEW.md` gives the proof, independence boundary, endpoint checks, and dimension limitations.
- `results/residual_review.json` contains exact obstruction and wider-interval witnesses.
- `results/budget_review.json` contains exact independent entropy/startup bounds.
- `audit_residual.py` and `audit_budgets.py` import no producer code.
- `snapshot/` freezes the inputs used by the checks.
- `REPRODUCE.sh` reruns both tests with local-only writes.

These results establish an accuracy floor within the specified ansatz. They do not establish a universal minimum linear dimension, a continuous-coupling theorem, or a complete-band/gap proof from residuals alone.

No computation remains running. A meaningful extension would require a separate specification and test of intermediate 7–10 dimensional enlargements or a parameter-uniform obstruction. Neither extension is claimed here.
