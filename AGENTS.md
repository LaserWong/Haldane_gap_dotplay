# Haldane project instructions

These instructions apply when opening the repository, starting a new session, or returning after a restart.
They do not schedule work or guarantee that an execution environment will load this file automatically.

## Starting or resuming work

1. Read this file, then read the update time, current status, progress, and next tasks at the top of `README.md`.
2. Check the branch, commit, and existing changes. Preserve uncommitted work and use the current files rather than recollections of an earlier session.
3. Restore the specific release or checkpoint identified in the README. Check the ZIP SHA-256 and the archive manifest, then read the relevant `PAUSE` or `PAUSED` records. Report missing files, conflicting versions, and failed checksums without silently substituting other material.
4. Follow the user's latest instructions. While research is paused, perform only the reading, organization, or publication that the user explicitly requests. A restart, an opened repository, or a restored connection does not lift a pause.
5. If work is active and remains within the authorized goal, deadline, and actions, continue with the highest-priority unfinished task. Avoid repeating verified calculations. Clarify any uncertainty about authorization or status before proceeding.

## Research and verification

- Distinguish analytic proofs, exact-arithmetic certificates, independent checks, floating-point benchmarks, and unverified candidates.
- Preserve the Hamiltonian, parameters, boundary conditions, size range, and normalization for every result. Report the ordinary bilayer and the fully frustrated bilayer separately.
- Distinguish the full Hilbert-space dimension, the linear trial-space dimension, and the MPS bond dimension.
- A small trial-state residual does not by itself certify the full spectral tail or exclude omitted low-energy states.
- Check existing runs, logs, and checkpoints before repeating a costly calculation. Establish the environment, resource budget, and recovery method before starting a long run.

## Recording results and unfinished work

After substantial progress, a blocker, completion, or a pause, update the time, current task, and progress at the top of `README.md`.
Give both UTC and America/New_York local time, with the correct daylight-saving offset.
Record the relevant code commit, data or release, file hashes, completed checks, unresolved questions, and next executable step.
Save the code, data, dependencies, reproduction commands, and checkpoints needed to recover the work.
Identify commands that take substantial time or change remote state.
Do not include passwords, tokens, other credentials, or unrelated private information.

Repository changes, release publication, and other external actions must remain within the user's authorization.
These instructions grant no additional permissions and do not replace required confirmation.

## Resumption on October 14, 2026

The user explicitly resumed this project on 2026-10-14 at 17:36:22 UTC, or 13:36:22 EDT in New York.
Earlier pause and deadline records remain historical records.
This resumption and any later user instructions determine the current scope.

The README must report the scientific results, parameter and size ranges, evidence, unfinished questions, and next tasks.
Recovery instructions alone are insufficient.
Use only repository-relative links or plain-text commit hashes in the README.
Do not add external links or present missing paths as working evidence links.
Preserve raw code, data, and numerical certificates. Documentation may be rewritten in place under the user’s instructions.

Distinguish historical independent checks, evidence that can currently be reproduced, and calculations newly rerun during the current work.
Recovering files or replaying an existing certificate does not establish a new gap theorem.
The resumption does not automatically restart previously disabled scheduled tasks.

## Writing

Follow `WRITING.md` for new or revised project documentation.

## Documentation

Maintain project documentation in English under `WRITING.md`. Update existing documents in place rather than adding duplicate reading editions. Keep raw code, data, and numerical certificates unchanged. Historical documentation hashes record historical versions and do not prohibit authorized prose edits. The root README uses repository-relative links only.
