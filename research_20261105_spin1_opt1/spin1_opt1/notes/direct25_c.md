## (c) Seals / direct-25 (from existing direct25/ logs; no repo seal fights)
audit_HEAD.log: AssertionError on MANIFEST_SHA256 — .md files edited after sealing (known).
replays_HEAD_sealedmd.log: with 253 .md restored to sealed blobs at HEAD a99fa21:
  direct25/n24/gap0248 audits exit 0; results.json match except CPU/RSS; INPUT_SHA256 identical.
rerun.log: limited_run.py L=25 under RLIMIT_CPU 15s / AS 100MiB: exit 0, cpu_seconds=2.5792
  stdout == sealed anchor25.out (sha 8d2fbffd...); prior "26s vs 15s cap" anomaly NOT reproduced.
Verdict: seals fail only due to post-seal .md edits; mathematics of direct-25 replays clean under sealed sources.
