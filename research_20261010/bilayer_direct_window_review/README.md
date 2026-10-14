# Independent 2D direct-window review

Updated 2026-10-10 18:29 EDT / 22:29 UTC.

The review establishes that the ordinary spin-1/2 periodic bilayer at g=0.10 has gap >=0.055807148827 and a unique ground state for every integer square side L>=2, with unit rung coupling and the established side-two multiedge convention.

The new direct time-first window lemma is proved independently in PROOF.md. All nine producer exact paths pass independent arithmetic, including every early box, odd sides, the L2..7 bridge and asymptotic closure. The strongest path begins at beta=187/20, reaches the common base 8 at beta=187/10, and enters the asymptotic theorem at base 1024 and beta=11968/5. Inputs are hash-matched to the accepted complete-residual review. The point result does not extend coupling coverage or establish an interval improvement.

The frozen producer proof's fraction typo and resource-measurement typo are retained with the explicit erratum. The certificate JSON is correct. See ACCEPTANCE.json, audit.json and snapshot/PRODUCER_PROSE_ERRATUM.json.

`REPRODUCE.sh` verifies the seals and runs the independent scalar audit in a fresh temporary directory. Each batch uses CPU4, at most 600 CPU seconds, and 700 MiB. It performs no physical contraction, imports no producer code, and makes no repository-root changes or remote publication.
