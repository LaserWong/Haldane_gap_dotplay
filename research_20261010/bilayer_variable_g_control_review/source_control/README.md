# Incremental metadata and control revision

2026-10-11 04:15 UTC / 2026-10-11 00:15 EDT. This gate ran metadata tests only. It did not execute a physical contraction, full cache or production job. All old seals, especially the 24-field numerical package, remain unchanged. This package is not independently approved production software.

## Synthetic benchmark

All 2945 synthetic chunk records were generated and exactly assembled after a bounded continuation. A near-full restart reads 2945 attempt records and 2945 committed records once, but reads zero historical raw outputs and performs zero historical adoptions. A restart with one completed-uncommitted receipt reads/adopts exactly that one output. Ordinary incremental commits read only their newly completed output. The restart avoids the 4.3-million-adoption loop.

The complete continuation used 3.393483 wait4 CPU seconds and 4.341713 wall seconds. Combined supervisor/controller RSS peaked at 59,801,600 bytes. Startup reconciliation used .369046918 CPU seconds with one uncommitted receipt and .365011474 with all receipts committed. Generation used 2.413078401 CPU seconds, including initial recovery and the remaining 1005 chunks. The continuation resumed 1940 completed records. Of these, 1939 were already committed and one additional receipt was adopted at startup. Exact signed 24-field synthetic sums match the closed-form generator.

The controller-CPU, combined-memory and supervisor-CPU fault tests each stopped and reaped their child and verified the inherited lock. The controller fault test used .185992 child CPU seconds. The memory fault test observed 85,065,728 combined bytes against an 80 MiB threshold. The supervisor fault test used .171240 supervisor CPU seconds. These deliberate fault thresholds are below the production limits. They test process control without a physical state.

## Resource and failure history

The original metadata gate retains a conservative charge of 27/30 CPU seconds. Its soft limit was explicitly raised from 25→27. The charge includes five prepaid supervisor seconds and child reservations of 12 for the failed attempt, 5 for the corrected benchmark, 2 for the controller fault test, 2 for the memory fault test and 1 for the supervisor fault test.

- The 12-second attempt failed before engine execution because the supervisor lowered its hard CPU limit before fork. Its child could not raise the inherited hard limit. The child used .087201 CPU seconds. The full 12 remains charged, with the source and receipt preserved.
- The 5-second benchmark reached 1939 committed records and one further completed receipt, then correctly stopped at its external controller CPU threshold. The run used 4.911592 CPU seconds. The full 5 remains charged.
- A separate 10-second continuation was authorized, with 8 for the worker and 2 for supervisor and metadata work. It remains fully charged at 10/10. The benchmark child used 3.393483 CPU seconds and the supervisor .321123. Both earlier failures remain charged.
- A later metadata-validation script hit its own 1-second CPU limit and exited 137 without a final receipt. No retry was made. FAILED_FINAL_VALIDATION.json explicitly marks it incomplete. It must not be counted as passing. The complete 2945 benchmark result is separate and valid. The 1-second control charge belongs to the continuation's 2-second metadata/supervisor reserve, not a new/refunded worker allocation.

The completed gates provide no remaining allowance for producer tests. Independent review uses a separate allocation.

## Implementation

engine.IncrementalJob performs one startup reconciliation and maintains pending/completed dictionaries and pending-reservation totals in memory. It persists independent constant-size attempt/commit files plus a small state record. Ordinary commits do not reload earlier receipts or outputs. Complete-but-uncommitted outputs alone are verified/adopted at startup. This same generic store is used by physical_session.py. Synthetic generation is explicitly rejected for physical schema/kind.

ControlBudget enforces a fixed prepaid 1200, positive integral controller/supervisor reservations, exact sum and unique sequential session IDs. Every session reserves both controller and supervisor allowances before fork and never refunds, including crashes. The shared session_supervisor externally measures controller-own CPU, supervisor-own CPU and combined live tree RSS, applies kernel CPU/AS limits, inherits the lock, sets parent-death SIGKILL and reaps descendants. Controller-own CPU is separate from wait4 tree CPU, which can include numerical workers. Missing self-CPU measurements remain unknown, with the full reservation charged.

physical_session.py is a persistent physical dispatcher using the same store. It verifies mandatory pins and strict per-worker digests/schema/ranges/moment assemblies, normalizes the new record format by sector, and checks accepted m0–m2 before any FULL_MOMENTS.json. It includes stale→abandoned recovery and explicit receipt-specific retry authority. Retry archival is idempotent across the archive-before-unlink crash window. Archived/current duplicate charge is reconciled once.

production_supervisor.py is the only proposed new physical entrypoint. It requires explicit production authority, pins, accepted controls and an initialized controller budget. The production authority was absent at this stage. It dispatches at most 100 chunks per session and uses a worker-aware wall limit (2·6+10)·count+60, not a multiple of controller CPU. Shared supervision requests a graceful stop at a completed chunk boundary before controller/supervisor CPU or session-wall exhaustion, with hard termination still active. The physical remaining-work forecast includes per-worker 10-second margins, retry-worker margins, controller/session overhead and a 24-hour independent-review reserve before the absolute 2026-10-14 deadline.

## Production memory topology

For the approved single numerical-worker topology, proposed soft address-space allocations are supervisor 32 MiB, controller 64 MiB, worker 160 MiB, totaling 256 MiB. The controller hard ceiling allows only the child worker's 160 MiB limit to be raised. Approved parent code retains its 64 MiB soft limit. The supervisor hard ceiling is likewise chosen before child initialization, avoiding the inheritance bug. Combined RSS is independently sampled. Excess memory use or extra descendants terminate the session. The metadata tests used the shared default profile and a lower 80 MiB combined-memory fault threshold. The 32/64/160 physical profile has not run physical work. The physical profile still requires independent checks of allocation headroom and process topology.

## Synthetic evidence and publication scope

Synthetic schema=`synthetic-metadata24-v1`, kind=`SYNTHETIC-NONPHYSICAL-NOT-ADOPTABLE`. Every record carries that job identity. These records cannot be adopted by the physical 24-field validator. Their signed values are a deterministic arithmetic sequence, not quantum-state data or moments.

The generated data directory under runs/full_metadata_fixed/data is scratch replay material and deliberately excluded from the final package manifest, avoiding publication of thousands of redundant synthetic files. The retained generator, benchmark result, resource receipts, resume frontier, closed-form final 24 sums and representative valid/corrupt records are sealed. The raw data remains on disk for independent review. It was not deleted. The failed final inventory script left the complete inventory hash unverified.

## Remaining checks

The final physical adapter and memory/deadline-profile changes are source-level implementations, not executed physical-production evidence. The standalone final-validation script is incomplete. Independent review should test retry crash idempotence, stale recovery, mandatory pins, the new-format accepted-control finalizer, and controller/session boundary behavior, then verify the near-full benchmark in a fresh isolated directory. Use PYTHONDONTWRITEBYTECODE=1 and separate ledgers. Frozen evidence must remain unchanged. The synthetic benchmark does not validate the full physical calculation.

Actual accepted 57D m0/m1/m2 control values, a production authority file and a production job directory have not been created. Production remains blocked pending independent gate acceptance and an explicit resource decision. The existing 24-field full-calculation projection and 21600-second proposal are empirical planning estimates. They establish neither guaranteed performance nor a new spectral result.
