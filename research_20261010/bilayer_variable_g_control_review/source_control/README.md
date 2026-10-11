# Incremental metadata/control revision — review handoff

2026-10-11 04:15UTC / 2026-10-11 00:15EDT. No physical contraction, full cache or production job was executed in this gate. All old seals, especially the24-field numerical package, remain unchanged. This package is not independently approved production software.

## Useful result

All2945 synthetic chunk records were generated and exactly assembled after a bounded continuation. A near-full restart reads2945 attempt records and2945 committed records once, but reads zero historical raw outputs and performs zero historical adoptions. A restart with one completed-uncommitted receipt reads/adopts exactly that one output. Ordinary incremental commits read only their newly completed output. There is no4.3-million-adoption loop.

The complete continuation used3.393483wait4 CPU seconds and4.341713wall seconds, combined supervisor/controller RSS peak59,801,600bytes. Startup reconciliation with one uncommitted receipt was.369046918CPU seconds; a fully committed restart was.365011474. Continuation generation CPU2.413078401 includes initial recovery and the remaining1005 chunks. It resumed1940 completed records:1939 had been committed before the stop, and one additional completed receipt was adopted during startup. Exact signed24-field synthetic sums match the closed-form generator.

Controller-CPU, combined-memory and supervisor-CPU fault tests all stop and reap their child, with inherited lock verified. Controller fault:.185992childCPU. Memory fault:85,065,728observed combined bytes against80MiB test threshold. Supervisor fault:.171240supervisorCPU. These are deliberate test thresholds below the production profile; no physical state is involved.

## Resource and failure history

The original metadata gate is27/30 CPU seconds conservatively charged, with its soft limit explicitly raised25→27 by root. It includes five prepaid supervisor seconds and these child reservations: failed12, corrected benchmark5, controller fault2, memory fault2, supervisor fault1.

- The12-second attempt failed before engine execution because the supervisor lowered its hard CPU limit beforefork; its child could not raise the inherited hard limit. ActualchildCPU.087201. Full12 remains charged, source/receipt preserved.
- The5-second benchmark reached1939 committed records and one further completed receipt, then correctly stopped at its external controllerCPU threshold. ActualCPU4.911592. Full5 remains charged.
- Root separately authorized a10-second continuation:8worker+2supervisor/metadata reserve. It is fully charged10/10; actual benchmark child3.393483, supervisor.321123. Both earlier failures remain charged.
- A later metadata-validation script hit its own1-second CPU limit and exited137 without a final receipt. No retry was made. FAILED_FINAL_VALIDATION.json explicitly marks it incomplete; it must not be counted as passing. The complete2945 benchmark result is separate and valid. The1-second control charge belongs to the continuation's2-second metadata/supervisor reserve, not a new/refunded worker allocation.

No further producer test is authorized by these completed gates. Independent review has its own allocation.

## What was changed

engine.IncrementalJob performs one startup reconciliation and maintains pending/completed dictionaries and pending-reservation totals in memory. It persists independent constant-size attempt/commit files plus a small state record. It never reloads every prior receipt/output on each ordinary commit. Complete-but-uncommitted outputs alone are verified/adopted at startup. This same generic store is used by physical_session.py; synthetic generation is explicitly rejected for physical schema/kind.

ControlBudget enforces fixed prepaid1200, positive integral controller/supervisor reservations, exact sum and unique sequential session IDs. Every session reserves both controller and supervisor allowances beforefork and never refunds, including crashes. The shared session_supervisor externally measures controller-own CPU, supervisor-own CPU and combined live tree RSS, applies kernelCPU/AS limits, inherits the lock, sets parent-death SIGKILL and reaps descendants. Controller-own CPU is separate from wait4 treeCPU, which can include numerical workers. An unavailable self-CPU receipt stays unknown rather than being fabricated; its full reservation remains charged.

physical_session.py is a persistent physical dispatcher using the same store. It verifies mandatory pins and strict per-worker digests/schema/ranges/moment assemblies, normalizes the new record format by sector, and checks accepted m0–m2 before any FULL_MOMENTS.json. It includes stale→abandoned recovery and explicit receipt-specific retry authority. Retry archival is idempotent across the archive-before-unlink crash window; archived/current duplicate charge is reconciled once.

production_supervisor.py is the only proposed new physical entrypoint. It requires absent explicit production authority, pins, accepted controls and initialized controller budget. It dispatches at most100 chunks per session and uses a worker-aware wall limit(2·6+10)·count+60, not a multiple of controllerCPU. Shared supervision requests a graceful stop at a completed chunk boundary before controller/supervisorCPU or session-wall exhaustion, with hard termination still active. The physical remaining-work forecast includes per-worker10-second margins, retry-worker margins, controller/session overhead and a24-hour independent-review reserve before the absolute2026-10-14 deadline.

## Production memory topology

For the approved single numerical-worker topology, proposed soft address-space allocations are supervisor32MiB, controller64MiB, worker160MiB, totaling256MiB. The controller hard ceiling allows only the child worker's160MiB limit to be raised; approved parent code retains its64MiB soft limit. The supervisor hard ceiling is likewise chosen before child initialization, avoiding the inheritance bug. Combined RSS is independently sampled and excess or extra descendants terminates the session. The metadata tests used the shared default profile and a lower80MiB combined-memory fault threshold; the32/64/160 physical profile has not run physical work. Independent review must assess it, including allocation headroom and topology assumptions.

## Synthetic evidence and publication scope

Synthetic schema=`synthetic-metadata24-v1`, kind=`SYNTHETIC-NONPHYSICAL-NOT-ADOPTABLE`; every record carries that job identity. These records cannot be adopted by the physical24-field validator. Their signed values are a deterministic arithmetic sequence, not quantum-state data or moments.

The generated data directory under runs/full_metadata_fixed/data is scratch replay material and deliberately excluded from the final package manifest, avoiding publication of thousands of redundant synthetic files. The retained generator, benchmark result, resource receipts, resume frontier, closed-form final24 sums and representative valid/corrupt records are sealed. The raw data remains on disk for independent review; it was not deleted. The failed final inventory script did not establish a complete inventory hash, and no such hash is claimed.

## Remaining review obligations

The final physical adapter and memory/deadline-profile changes are source-level implementations, not executed physical-production evidence. The standalone final-validation script is incomplete. Independent review should test retry crash idempotence, stale recovery, mandatory pins, the new-format accepted-control finalizer, and controller/session boundary behavior, then verify the near-full benchmark in a fresh isolated directory. Use PYTHONDONTWRITEBYTECODE=1 and separate ledgers. Do not modify frozen evidence or treat the synthetic benchmark as a full physical pass.

Actual accepted57D m0/m1/m2 control values, a production authority file and a production job directory have not been created. Production remains blocked pending independent gate acceptance and an explicit resource decision. The existing24-field whole-body projection and21600-second proposal are still empirical planning figures, not a guarantee or a new spectral/gap claim.
