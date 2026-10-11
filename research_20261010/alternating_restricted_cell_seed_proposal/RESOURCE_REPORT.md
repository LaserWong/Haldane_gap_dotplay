# Resource audit: NOT ACCEPTED

Authorized scientific allowance: at most30 cumulative CPU seconds and256 MiB. No physical computation or external write was authorized for this task.

## Actual launches

The immutable historical launch entries are retained in RESOURCE_LEDGER.json. Actual CPU is wait4 user+system; each launch also receives a conservative .05-second supervisor-overhead reserve.

| Launch | Requested/configured RLIMIT_CPU | Actual child CPU seconds | Charge including reserve | Peak RSS KiB | Outcome |
|---|---:|---:|---:|---:|---|
|NumPy/SciPy candidate search|6|7.328676|7.378676|58052|SIGKILL; no candidate output|
|Pure-Python candidate search|3|.082053|.132053|9216|Completed|
|Baseline exact checker|9|4.790784|4.840784|12032|Completed|
|Strengthened exact checker|8|6.174575|6.224575|12032|Completed|
|Exact diagnostic checker|3|1.230385|1.280385|12544|Completed|
|Final combined replay|8|10.791353|10.841353|13620|Completed despite configured8-second cap|
|TOTAL||30.397826|30.697826||NOT ACCEPTED|

The scientific budget was exceeded by .397826 actual CPU seconds; including supervisor reserves the excess is .697826. It is not rounded to30, and the failed first launch is not discarded. Scientific computation stopped immediately after this result was observed. Later work consisted solely of reading sources and writing documentation; no further candidate searches, rational checks, physical calculations, contractions, solver runs or thermal jobs were started.

## What the supervisor did and did not prove

run_limited.py forked one child, set one-CPU affinity, called setrlimit(RLIMIT_AS,256 MiB) and setrlimit(RLIMIT_CPU,(cap,cap)), then exec'd Python. It waited with blocking wait4 and appended actual user/system time, wall time, maximum RSS and exit status. It checked remaining aggregate budget before launch using earlier charges.

It did NOT actively poll child CPU or externally terminate on an observed threshold. It did NOT verify the effective limit after exec, did not record a post-exec getrlimit result and did not verify a process-group/descendant CPU monitor. The present scripts launch no scientific subprocesses themselves, but generic descendant enforcement was not established. The final run did record hashes of all Python sources immediately before execution.

The available evidence shows that the final process completed normally with actual CPU10.791353 although the wrapper requested an8-second hard limit. The cause is not established. No claim about runtime virtualization, scheduler behavior, kernel semantics or later limit changes is justified. Likewise the first SIGKILL cannot be attributed uniquely to a particular cause from this ledger alone; it happened before a candidate result was emitted.

The first five entries predate per-launch source hashing. Their source versions are retained as search.py, search_pure.py, verify_baseline.py, verify.py and diagnose.py, but hashes were not contemporaneously recorded for those launches. The final combined replay pins their current source bytes before running verify.py and diagnose.py. This does not repair the earlier provenance or resource-enforcement gap.

Peak observed RSS was58052 KiB, below256 MiB. The256-MiB address-space setting was requested in the wrapper; post-exec enforcement was not independently observed. Resource claims distinguish measured memory from configured limits.

## Future gate

This wrapper must not be reused as an accepted production resource guard. Any additional computation needs a freshly verified external guard, aggregate reserve policy with stop margin, observed post-exec limits and evidence that active CPU observation/termination works. No budget expansion, retrospective authorization or automatic retry is implied here.
