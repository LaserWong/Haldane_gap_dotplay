# Accepted partial physical reproduction; full campaign stopped

## Final scope

ACCEPTED physical inputs: all16 identity/π-seam traces atβ49/4, integer lengths4 through11. Every aggregate W exactly reproduces the official printed integer, and every independent rational trace enclosure lies inside its published center±30·10^-6 with margin greater than13·10^-6. Full L12I and L12P remain uncomputed and unaccepted. Consequently the18-input premises of the .0046 and .0214 all-L≥36 scalar certificates are not fully discharged; those gap claims remain conditional.

All990 saved batches pass identity/hash/coverage validation. Of these,962 cover the16 complete cases. Partial L12I has16 valid batches,256 representative columns, weighted multiplicity11172; partial L12P has12 valid batches,192 columns, weighted multiplicity8256. Each full L12 seam requires733 batches and11595 representatives. Partial columns are valid retained evidence, but are not full trace certificates or gap proofs.

The independent reviewer rebuilt every sparse physical matrix digest and all orbit metadata for lengths4–12 and both seams using fresh physical bond rules. No heat matrix powers or columns were launched by the reviewer. Every complete-case batch identity, source/kernel/coefficients/wrapper pin, matrix/orbit digest, exact ordered representative slice, nonnegative integer norm, weighted sum and final certificate binding was checked. Partial L12 batches receive the same checks. PROOF.md gives the physical approximation/error argument and explicitly limits acceptance to the completed16 inputs.

## Immutable evidence

snapshot/campaign contains a byte-checked copy of the terminal ledger, all18 case metadata files,990 saved batches,16 full certificates, completion objects and diagnostic logs. SNAPSHOT_SHA256.json binds every copied file; copies were checked against the original bytes during capture. check_completed.py and check_partial_outcome.py read this immutable snapshot, not the live campaign path. Thus a future separately authorized continuation cannot change this historical result. Source packages and earlier reviews remain unchanged.

## Terminal accounting

The supervisor reached BUDGET_RESERVATION_EXHAUSTED with no ACTIVE or RESERVED attempts. Exact ledger charges are:

- supervisor overhead:122CPU seconds;
- successfully completed attempt charges:1445CPU seconds;
- two failed L12 attempts, each retaining its full7320 reservation:14640CPU seconds;
- total:16207CPU seconds;
- unallocated capacity under21600:5393CPU seconds.

5393 cannot accommodate another maximal7320 reservation, so the supervisor correctly stopped. These are conservative ledger charges, not measured physical CPU consumption. In particular the two failed attempts did not each necessarily consume7320 seconds. Both retained charges are preserved; no refund, reset, ledger replacement, alternate campaign path or restart is authorized by this review.

Every successful attempt's stored completion identity and terminal wait4 accounting was checked, including its charge ceil(terminal whole-tree CPU)+2 capped by reservation. Every attempt's reservation was recomputed from its action and possible process count. The two failures have wait status9 and retain their entire reservations. The terminal ledger contains61 attempts and no unresolved live attempt.

## Cause and previous test limitation

Both failed L12 logs end with the frozen runner's assertion on a compute child return−9. The runner computes remaining=int(120−used)−1 and launches the next batch with min(120,remaining) as its hard CPU limit, provided only that remaining≥1.

Completed L12I batches consumed116.495635 childCPU seconds before the failure, so the next child allowance was at most2 seconds even before adding the Python parent's CPU. L12P consumed114.881077, leaving at most4. Recent successful batches took approximately6.8–9.0 seconds for I and8.5–9.9 for P. This code/timing evidence strongly supports a batch killed at the per-invocation allowance boundary. The log records SIGKILL, not a kernel-level cause diagnostic, so the review does not claim a recorded OS diagnosis that is absent. No integer mismatch or thermal error-bound failure was observed.

The safety gate worked as designed after failure: descendants were stopped and the conservative reservations were retained. The campaign nevertheless failed its completion objective due to the interaction between the runner's small remaining allowance and batch duration. The previous15 independent scheduling fixtures exercised failure accounting, crashes, cleanup, limits and resume identity; they did not run a sequence of successful batches approaching this allowance boundary. Their engineering acceptance should not be read as prior testing of that missing integration scenario.

Any repair must add a scaled, short, nonthermal regression reproducing this boundary, and must demonstrate graceful yield before starting a batch whose fixed authorized allowance is unavailable. It must distinguish an actual per-batch resource failure from an artificial shrinking invocation allowance. All old16207 charges and5393 remaining capacity must survive an explicitly authorized transition. A terminal-state change or new budget needs root's decision and a separate independent gate. The user campaign wallstop remains2026-10-11T06:00:00Z; research hardstop2026-10-14T00:00:00Z.

## Reproduction and limits

Run check_matrices.py, check_completed.py and check_partial_outcome.py in a disposable review copy. The first rebuilds only sparse matrix digests; the other two perform scalar/hash/coverage checks. Reviewer-generated geometry caches have embedded hashes; remove those caches in the disposable copy if a fresh reconstruction is desired. No producer/upstream scientific code is executed, no thermal job is started and no original campaign file is changed. Final artifacts contain no statement of full18-input acceptance or unconditional promotion of the second-initialization gap results.
