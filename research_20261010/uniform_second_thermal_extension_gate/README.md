# Proposed append-only budget extension

The design preserves the original 16207 charge and every attempt, then appends an authorized +21600 event. This gives a total cap of 43200 and a remaining allowance of 26993. It retains the sole state path, CPUs 0/1, two 256 MiB process trees, and the 06:00 UTC wall stop. No production ledger has been changed and no thermal run restarted.

The bounded repair leaves the frozen arithmetic runner, kernel, and old checkpoint pins unchanged. Invocations contain at most eight batches under an internal allowance of 600, with fixed caps of 35 seconds for computation and 5 for metadata. These limits make the shrinking-cap boundary unreachable. A full n12 invocation reserves 552 CPU seconds. Unknown attempts remain fully charged, and terminal wait4 refunds stay conservative.

Scaled runtime regression and append-only history, event, and identity tests pass, as does metadata-only integration with the frozen runner. `PROOF.md` and `tests.json` contain the checks. A fresh independent review and explicit launch instruction are still required.
