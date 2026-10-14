# Read-only finding on frozen 22-field hardening

2026-10-11 03:30 UTC. Source manifest c26c513f7e29e4dd23e83b1ad9ca367ece96c3b26e8347f926429606e160f5e5. No new review numerical run, compilation, support sweep or cache construction has been performed. The separately authorized 90-CPU-second review budget is preserved for the forthcoming 24-field/control package, following the parent's latest instruction.

The package provides useful producer component evidence covering deterministic chunk addressing, exact 22-field serialization, full generic 4×2 sector recombination, interrupted numerical chunk plus separately charged rerun, staged atomic commit/recovery checks, duplicate/corruption/coverage rejection, and a repaired numeric-/proc process observer. These are not independent replay results in this review.

At this historical checkpoint, full production remained blocked for the following reasons.

1. adopt_chunks.py does not verify receipt output_sha256 before adopting its result/accumulator/chunk/target files. The final controller records digests, but the adoption path does not enforce them. In particular, values 15–21 are not checked against the saved result moments during adoption.
2. A controller killed after fork can leave its setsid worker running. A restarted controller may reacquire the released lock. Stale running reservations/worker identities are not reconciled before a new launch. No parent-death lifetime guarantee is implemented.
3. The dispatch controller hardcodes a 120/90 component-test ledger. It does not implement the proposed 21600-second allocation, remaining-reservation forecast, research-deadline admission, or a complete production scheduler/finalization contract.
4. The numerical worker still uses CAP−2 internally. Thus a 3-second allowance has only a 1-second soft computation window, rather than the proportional policy proposed in the design.

The complete schema remains 22 accumulators at fixed g=11/100. Variable-g weighted bilinears are absent and excluded. The parent has directed the producer to repair these control gaps and add a versioned 24-field extension in a new package. Neither the prior sealed whole-moment review nor its exhausted 90/90 ledger is modified.
