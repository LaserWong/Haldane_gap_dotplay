# Trial-size criteria and minimal-seed diagnostics

Updated 2026-10-10 14:16 America/New_York / 18:16 UTC.

## Results

* A practical sufficient test links certified band separation, the **full
  residual matrix**, Boltzmann-weighted eigenvalue widths, omitted-bin entropy,
  and the exact bootstrap startup. It distinguishes search dimension d,
  retained physical band rank k, sparse configuration support, and geometry.
* At g=.03,beta=9.09, the 13/25/49-state band certificates meet explicit
  posterior trace-error budgets. The largest ground search uses 11 vectors,
  not 49 and not 20,081. The latter is its expanded configuration support.
* Exact full-second-moment witnesses show that the **fixed six-vector q2
  search space** cannot achieve stated residual targets at g=.02/.03/.04/.05,
  while the saved 11-vector space does. This is not a universal lower bound
  on dimension.
* A new all-beta calculation excludes the **specified canonical
  2x2 -> 4x2 -> 4x4 recurrence**, even with exact physical traces, at g=.04 and
  .05. The separate
  `small_seed_exclusion_review/` has now independently passed all six physical
  inputs and the full scalar deduction, including all 640 parameter boxes.
  Every interval has an upper iterate that becomes nonpositive; it is not a
  conclusion from failure to reach a sufficient basin. Other orders and
  methods are not excluded.
* The independently audited FF continuum illustrates genuinely small spaces:
  one product direction through epsilon=.00475, and one retained ground
  vector from the current 23/93/377-dimensional searches through epsilon=.00855,
  at the nonperturbative crossed reference J=.3. All omitted states remain
  controlled. The uniform square gap through .00855 is >.000768515509.

## Files

- `PROOF.md`: complete new criteria, explicit ansatz scopes, proofs and examples
- `criteria.py`, `all_beta_exclusions.json`: self-contained rigorous exponentials,
  trace intervals and all-temperature upper-recurrence obstruction; six input hashes
- `examples.py`, `examples.json`: .02 successful ground-only replay, .03/.04/.05
  band budgets, 12 larger-ground moment contractions, all six FF interval pieces
- `entropy_rank.py`, `entropy_rank.json`: exact minimum ranks for a specified
  coarse-bin tail-majorant tolerance, explicitly not universal minima
- `residual_obstruction.py`, `residual_obstructions.json`: exact 6x6 positive
  LDL witnesses excluding small residuals in a fixed q2 search space
- `REPRODUCE.sh`: one-CPU, one-GB replay; no remote writes
- `MANIFEST_SHA256.json`: hashes for this directory's stable deliverables

Baseline files are immutable. Original generated JSON status fields record
generation-time review status; `small_seed_exclusion_review/` independently
accepts the complete Section 6 result. Other source review scopes are preserved.
No full many-body diagonalization or fresh trial-vector eigensolver was used.
The new residual lower witnesses require only small exact PSD tests.
