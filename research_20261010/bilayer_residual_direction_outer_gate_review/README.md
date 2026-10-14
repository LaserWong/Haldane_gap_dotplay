# Review of the single permitted production launcher

The fixed 46-call production launcher passed independent review.
Its reservation is 350 seconds across the calls plus 10 seconds for the persistent driver, with an effective address-space split of 8 + 32 + 60 MiB.
The review checked the exact small-system replay, charges for failed preflight checks, cascading termination, inherited locks, and refusal to restart.

This result verifies the launch controls.
It does not supply a complete 8×4 calculation or authorize a production run.
Any failure stops the campaign, and a restart or a run in another directory requires a new decision.
`PROOF.md` explains the interpreter, signal, cost, and memory conditions.

Run `./REPRODUCE.sh` only for the bounded small tests.
