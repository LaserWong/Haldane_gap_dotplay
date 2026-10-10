# Temperature-first spin-one chain candidates

Updated 2026-10-10 14:42 EDT / 18:42 UTC. **Awaiting independent audit.**

Using only previously saved physical trials, a time-first cycle and exact adjacent-swap conversion give all-integer M>=2 candidates:

- g=.1615: gap >= .039815121561
- g=.1625: gap >= .037716426713
- g=.175: gap >= .006791087005

The largest n=8 input is strictly Rayleigh-only. Its residual, ground isolation, full tail, and ground lower endpoint are not consumed. The old space-first obstructions remain true in their stated scope. g=.2 fails this bounded scan only; no all-temperature exclusion is claimed.

Read `PROOF.md`, `summary.json`, and the three successful `candidate_*.json` files. All short sizes and dyadic finite windows are included. The M7 short bridge reuses a fixed saved vector and evaluates its energy affinely in g; no new many-body eigensolve was run.

Run `REPRODUCE.sh` for the bounded diagnostic and exact producer. Freeze/provenance files seal the independent-review handoff. Do not promote these candidates without that review. Next action: independent physical/scalar/bridge audit; no additional coupling scan before review.
