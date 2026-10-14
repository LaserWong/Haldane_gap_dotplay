# Incremental control first-seal review

Source manifest 1bad844f7945081ddae5a86a2167ef40e2510ef49434678d422c588023ed6a1d. The production review failed. Committed startup validates the payload against its envelope and the attempt against its receipt, but does not bind the payload digest to attempt.output_sha256. This was reported before the frozen handoff and remains unresolved in this source. No source was modified.

A separate component check passed. An independent 2945-record synthetic benchmark ran from zero commits with only the CPU affinity changed from 6→7. Cold generation used 5.590519133 CPU seconds, the full benchmark 6.553844269, controller wait4 6.745495 and the supervisor .429194. A full restart used .432679314 CPU seconds. It read 2945 attempts and 2945 commits once, with no historical raw-output reads or adoptions. A restart with one uncommitted record read and adopted exactly 1 output. All 24 exact signed accumulators match the closed-form synthetic arithmetic. Synthetic records are not physical moments and cannot enter the physical namespace.

The external review used 7.187328 child-tree CPU seconds and .158266 parent CPU seconds against a conservative reservation of 18+2=20 seconds. The whole-tree peak was 60,010,496 bytes on CPU7 with a 256 MiB cap. All descendants were reaped. The parent hold message arrived after this already-launched call completed. No later test ran under this source. Review ledger after benchmark was 45/90. The original 25 numerical24 reservations and this 20 remain charged.

The physical 32/64/160 MiB partition and dispatcher were not run under this first seal. Production is blocked. A later correction must be separately pinned and reviewed. This finding remains in the frozen record.
