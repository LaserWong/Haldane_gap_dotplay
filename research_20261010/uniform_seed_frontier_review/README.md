# Independent review of the n = 52 uniform-chain seed

Recorded October 10, 2026, at 18:36 EDT / 22:36 UTC.
The independent review passed.

The unit-coupling uniform spin-1 Heisenberg chain has a unique ground state and gap>=19/5000=0.0038 for every integer periodic L>=52.
No claim is made below 52 or about a minimum seed size.

`REVIEW.md` distinguishes the exact Hermite-majorant proof and scalar certificate from the inherited nine thermal certificates, MPS104 anchor, and thermal-transfer assumptions.
All early signed-integer windows and the asymptotic coverage passed review.

Reproduce the checks in a disposable copy with the following commands.

    python independent_check.py > replay.log
    python adversarial.py > adversarial.log

The recorded replay used CPU 5 with a 700 MiB limit and took about 2.7 CPU seconds.
It performed no new contraction and changed neither the generating files, repository root, nor remote repository.
`CLAIM_VERDICTS.json`, `scalar_results.json`, `INPUT_SHA256.json`, `MANIFEST_SHA256.json`, and `SEAL.json` give the exact scope and provenance.
