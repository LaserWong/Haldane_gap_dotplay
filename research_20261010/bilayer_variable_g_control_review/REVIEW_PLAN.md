# Authorized independent hardening review

New90 CPU-second ledger, CPU7,256MiB runtime; compilation512MiB only if necessary. The completed whole-m4 fixture-review ledger is untouched. No full8×4 support/cache or production. Planned documented fault injection/resume pairs are authorized; unexpected failures stop for a new decision.

Read-only/source review starts before producer freeze. Numerical and checkpoint work uses only a new copied sandbox after source identity is frozen. Review the exact numerical kernel delta, schedule permutation/rank endpoints, all22 component conservation, receipt hashes, commit/range exactly-once semantics, reservations and failed attempts, observer/kill/reaping, controller-death recovery, and cost/admission. Variable-g bilinears are excluded unless actually present in the frozen schema.

The outer review guard permits intentional nested test processes, but caps their aggregate CPU/RSS, pins inherited affinity toCPU7, uses a subreaper, and kills tracked descendants as well as the root process group. Every outer attempt is separately reserved before launch and never refunded.
