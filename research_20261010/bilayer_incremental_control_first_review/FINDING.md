# Incremental control first-seal review

Source manifest1bad844f7945081ddae5a86a2167ef40e2510ef49434678d422c588023ed6a1d. Production gateFAIL: committed startup validates payload against its envelope and attempt against receipt but does not bind payload digest to attempt.output_sha256. This was reported before the frozen handoff and remains unresolved in this source. No source was modified.

Component PASS: an independently fresh2945-record synthetic benchmark from zero commits, with CPU-affinity-only adaptation6→7, completed. Cold generation5.590519133CPU, full benchmark6.553844269CPU, controllerwait4 6.745495CPU, supervisor.429194CPU. Full restart .432679314CPU reads2945 attempts+2945 commits once, zero historical raw outputs/adoptions; one-uncommitted restart reads/adopts exactly1. Exact signed24 accumulators match closed-form synthetic arithmetic. Synthetic records are not physical moments and cannot enter the physical namespace.

External review child-tree7.187328CPU, external parent.158266CPU; conservative reservation18+2=20 seconds. Whole-tree peak60,010,496 bytes, CPU7,256MiB cap, all descendants reaped. The parent hold message arrived after this already-launched call completed; no later test ran under this source. Review ledger after benchmark45/90. The original25 numerical24 reservations and this20 remain charged.

Physical32/64/160MiB partition and dispatcher were not run under this first seal. Production is blocked. A later correction must be separately pinned and reviewed; this finding stays immutable.
