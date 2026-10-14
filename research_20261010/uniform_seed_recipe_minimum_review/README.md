# All-cooling exclusions for the n48 and n50 recipes

2026-10-10 19:10 EDT / 23:10 UTC. The independent review accepts exclusions only for n48 and n50 within the fixed-node Hermite/packing and fixed-MPS canonical-G recipe.

The result covers all 41 permitted even bases and every real cooling ratio r≥1. The 332 closed boxes end in genuinely nonpositive updates, and analytic cold rays cover r≥16. The maximum terminal round is 7. No timeout is counted as an exclusion.

The review also covers ideal unrounded fixed-envelope evaluation, so the conclusion is independent of arithmetic precision within this recipe. It is neither a physical gap obstruction nor a minimum-seed theorem, even within the specified family. No n<48 claim is made.

See `REVIEW.md` and `CLAIM_VERDICTS.json`. In a disposable copy, run `python independent_check.py > replay.log` and `python adversarial.py > adversarial.log`. The checks use CPU5, a 700 MiB limit, and approximately 4.19 CPU seconds. No producer, root, remote, or earlier sealed files are changed.
