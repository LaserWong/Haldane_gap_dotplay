# Independent review of the 63-commit failure

Sealed 2026-10-11 01:18 EDT /05:18 UTC.

## Result

The partial receipts and no-refund accounting passed review. Production failed its gate pending a reviewed observer repair. No full m4 or gap is established. The prior streaming startup review remains valid for its exact pin-verification cutpoints. This actual lifecycle failure is now separately preserved.

The immutable producer failure manifest is `552153e60e66c147e6384cca5f6b878e6a7cfac271cc35d4e0d66a0ed2e17b73` at `bilayer_full_m4_production_run_streaming/FAILED_OBSERVER_MANIFEST_SHA256.json`. All 650 listed files were independently hashed and copied to `evidence/`. The proposed job is `845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e`. All 26 pinned inputs were reverified. Source copies retain the precise stopped observer.

## Coverage and consistency

Exactly 63 commits, IDs 0–62, cover vacuum 1, q2 all 496 targets, q4 first 864 scheduled targets, q6 zero. Each complete record was independently checked through raw file hashes, worker receipt, normalized canonical payload, attempt digest, and commit receipt binding. All 24 canonical signed accumulator strings and exact 15-term/moment assembly agree. Target schedules are disjoint and their modular strides are coprime to the sector sizes. The raw partial sector totals match the producer failure summary.

The calculation retains signed commutator terms without assuming each term is positive. These partial totals do not satisfy a complete-coverage 57D m0/m1/m2 gate. Sector-normalized full moments must still wait for the entire 2945-chunk coverage. There is no CHECKPOINT_READY100, continuation token, or FULL_MOMENTS marker.

Attempt 63 remains raw `reserved`, not completed or adopted. Its 3-second charge is retained with all 63 earlier reservations, giving 192 worker seconds. Control records total 463, including the original failed 220. The total charge is 655. Watchdog/session control rows can remain labelled reserved after the enclosing kill. That does not authorize reuse or a refund. A fresh process scan found no matching production processes. Both existing locks could be exclusively acquired and released. The review did not reconcile or modify producer records.

Completed native-worker wait4 CPU totals 10.835780 seconds. Native setup totals 1.061749 and body 9.429620, with the remainder including process overhead. Outer wait4 tree CPU 13.279291 plus self .667257 seconds, wall 14.233770, reported combined peak RSS 59,031,552. This covers the observed prefix only, with no q6 runtime projection. The independent audit used .455473 child CPU + .085018 guard CPU. Its entire 5-second reservation is charged. No physical worker was run by this review.

## Static observer defect

The observer reads argv and then CPU/address-space/affinity as separate `/proc` records. After fork, a controller initially inherits the supervisor argv but subsequently sets CPU20/20 before exec. A worker likewise inherits the controller argv while changing to a 3- or 6-second CPU cap and 128 MiB address space. The old role inference can therefore compare a valid transitional process against the wrong role. If an inherited tuple happens to pass, the PID is cached permanently and its later exec identity/limits are not revalidated. The recorded duplicate supervisor roles are consistent with this defect.

The exact tuple that triggered `post_exec_limit_mismatch` was not persisted, so the specific 63-commit failure cannot be conclusively attributed to that race. A repair must establish stable process identity/role, explicitly bound transitions, revalidate changed identities, retain mismatch diagnostics, and test genuine bad CPU/address-space/affinity rather than merely widening allowed tuples.

## Successor accounting

A separate design authorization proposed repartitioning the same 21,600 total into 16,800 for standard workers, 1,600 for controls and 3,200 for retries in a clean generation. The prior 463 control and all 192 retired worker reservations must carry forward, with 192 deducted from retries. Ordinary clean-generation control forecast is 463+220+30*23=1,373, leaving 227. Retry remainder 3,008. The proposed partition fits the total budget. The failed source still has the old 1,200/3,600 partition and cannot implement the new proposal unchanged. New source/pins, independent observer review, and separate root launch authority are required. No old output is implicitly adopted into the clean job.
