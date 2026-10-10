# Conservative campaign supervisor: producer launch gate

2026-10-10 23:37 UTC. No campaign launched. This package preserves the frozen thermal pilot and strict runner. Independent review/root approval required.

## Fixed campaign bounds

Campaign cap21600 aggregate CPU seconds. User research deadline2026-10-14T00:00:00Z, campaign wallstop2026-10-11T06:00:00Z; earliest applies. Unix values are asserted against UTC conversions. At most two worker trees, on CPUs0 and1. A worker tree comprises one64MiB watchdog, one96MiB runner and at most one96MiB kernel child, aggregate address-space soft ceilings256MiB. The supervisor is a separate bookkeeping process capped at256MiB and120CPU seconds, conservatively charged122CPU seconds per invocation. Typical actual supervisor memory is small; it is not silently counted as one of the two worker trees.

The existing runner sequentially waits each metadata/compute child. hooks/sitecustomize.py is a private task-only PYTHONPATH hook, never installed system-wide. It clamps all runner/child address limits to96MiB and adds parent-death signals and fixed absolute-deadline alarms to each subprocess. The watchdog itself has64MiB soft address limit; its child can lower hard/soft limits to96MiB before exec. This division enforces the sum of the three process address ceilings at256MiB. CPU affinity is inherited; no extra compute cores or threaded libraries exist.

## Reserve before launch

Every possible process is hard limited to120CPU seconds. Reserve122 per process to cover Linux second/tick enforcement granularity. At prepare, the frozen runner can make at most4(n+1) sequential metadata children: list+matrix once to create metadata, once to revalidate. At run/validate it makes2(n+1) metadata children plus at most max_new_batches compute children. Add runner+watchdog as two more possible processes. Therefore reserve122*(children+2) BEFORE launching the attempt. For max_new_batches32,n12, run reservation7320, prepare6588. Two maximal run reservations14640 fit below21600. A reservation reduces spendable budget immediately and cannot be reused while the attempt is active.

The ledger uses an exclusive flock and atomic JSON replacement with file and directory fsync. It binds supervisor/hook and frozen runner/source/binary/coefficient hashes, fixed budget/deadline, attempt IDs, parameters, reservation, actual charge and status. A second launch is rejected. Changed bindings/limit/deadline are rejected. Terminal budget/deadline/completion states cannot automatically restart. A crash in RUNNING may be resumed under the same ledger: interrupted attempts retain their full reservation and never receive speculative refunds. No automatic budget reset or new ledger is created by the program.

The child is initially blocked on a pipe. Parent durably records its pid/starttime/boot identity before releasing execution. A crash after reservation but before activation remains fully charged and starts no unrecorded work. If the pipe closes the blocked child exits. Kernel metadata/setup costs are included in the process-count reservation, not ignored as non-compute work. Failed/killed attempts retain the full worst-case charge.

## Lifetime safety and cleanup

Each worker watchdog is its own process-group leader. It has an absolute wall alarm and parent-death SIGTERM handler that kills the entire group. Runner has parent-death SIGKILL and its own deadline alarm. Each child gets the same independent parent-death/deadline protection through the private hook. Thus killing the watchdog cannot strand a runner/kernel; killing the supervisor triggers cascade cleanup, even if the main ledger code cannot run.

On every guardian reap, successful or failed, supervisor sends SIGKILL to any residual group and waits until /proc contains no non-zombie member before reusing the slot. Exited zombies cannot compute; the direct guardian is reaped by wait4. Cleanup failure raises and launches no replacement. Exceptions in a guardian also kill its whole group. At the campaign wallstop the supervisor kills active groups, marks their reservations fully charged, persists terminal state, and exits. The per-process independent alarms cover supervisor/watchdog crashes near the deadline.

## Safe refunds and accounting

A successful normal frozen-runner return implies every child was waited; this follows from the inspected sequential subprocess.run/Popen.wait calls. The guardian waits the runner with wait4. It durably records a completion object, but this alone never authorizes a refund. The supervisor then waits the normally exited guardian with wait4, obtaining cumulative CPU for guardian plus the descendants each level waited. A controlled fixture deliberately burns.2CPU seconds in a grandchild and verifies inclusion in terminal usage. Only this completed terminal tree measurement authorizes a refund to ceil(measured CPU)+2 seconds, never above the reserved amount. The result's own intermediate usage is cross-checked but not used instead of the terminal measurement. A crash before ledger commit, missing result, failed exit, inconsistent identity or unknown state retains full original charge. Supervisor's own122 seconds are never refunded, covering ledger writes and restart overhead.

All attempts are counted, including repeats and setup. Reservations can conservatively exhaust capacity before21600 seconds are physically used; this is safe and reported. Typical overhead is now rounded fees plus measured setup, not120 seconds per successful watchdog. The6CPU-hour cap is never relaxed. Parent-death/crash cases may consume the budget conservatively; root review is required to decide next work.

## Checkpoints, resume and completion

The frozen strict runner validates complete case/source/binary/coefficient/matrix/orbit identity and batch integrity before reuse. It regenerates physical matrix/orbit metadata on each invocation; duplicate/hole/partial/stale records fail. Only complete independent aggregation precedes published-total comparison. Supervisor never substitutes its ledger for these checks. On a fresh supervisor invocation, an existing final certificate requires a successful validate action in THAT invocation. A historical success plus file existence is insufficient. Cases reach completed only after current-invocation normal run/validate success.

A process crash can leave runner.lock/.tmp files. Resume stops for manual inspection rather than removing them or trusting incomplete data. This may block progress safely; automatic lock deletion is deliberately absent.

## Tests, resource estimate and scope

Scheduling fixtures test crash-after-reserve, during-child, before-commit, failed metadata, budget exhaustion, duplicate campaign, third-worker rejection, deadline group kill, watchdog kill, supervisor crash, normal durable refund and identity change. They execute trivial Python processes, never thermal jobs. Metadata-only integration runs the frozen L4I prepare action under lifetime/memory hooks, verifies no heat batch or thermal certificate is created, and measures~.47CPU seconds. Full test CPU remains under120 seconds,256MiB CPU0.

The kernel estimate remains7906CPU seconds from the measured L12 batch; metadata regeneration/setup and fees add cost. With nominal120-compute-second throttles, around70–100 successful work attempts plus18 preparations would add at most a few hundred seconds in rounded accounting fees, plus measured metadata CPU. Expected2–3CPU hours is an estimate;6CPU-hour reservation cap remains binding. Near budget exhaustion a maximal7320 reservation may no longer fit; no overcommit occurs. Two simultaneous maximal reservations fit initially, but scheduling may serialize as spend accumulates. No full campaign is authorized by this file.
