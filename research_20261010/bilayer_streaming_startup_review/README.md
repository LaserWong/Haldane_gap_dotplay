# Independent streaming-startup review

Sealed 2026-10-11 01:11 EDT / 05:11 UTC.

## Result

PASS for the streaming-startup correction and the bounded staged-launch gate of proposed job `845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e`, conditional on fresh root launch authority and the new durable 220-second control precharge. No physical work was performed here. The predecessor's actual failed startup is retained, with all 220 seconds carried forward. This does not certify complete moments or a spectral gap.

The producer source seal is `88aa9e771ab91a958d43a339a9bbd96e627240f2ca82cdc0d4234ddf0908fbee`. The final 26-pin map is `227f433eb8a01923d217b7dc2d407e257bd1f7a438845432269364702da44be5`. All sealed producer files and copied evidence were verified. See `correction/CHECKS.json` and the raw guarded run.

## Independent executable evidence

The actual `outer.run`, `production_supervisor.launch`, and `physical_session.run` each reached the actual shared verifier with the complete final 26-pin map under a real 64 MiB soft / 128 MiB hard address-space limit, imposed before interpreter imports. The 30,894,944-byte pinned Python executable was included. All 1,605 hash reads were bounded to 65,536 bytes. VmPeak was 40,042,496 bytes. A corrupted Python-binary digest was rejected. The `python3` selected by the launch environment resolves to the same pinned executable.

The test-only adaptations were CPU 7, a hard/soft CPU limit of 6 for the bounded child, an exact two-token outer-source change for those CPU assertions, memory-only fixture authority, a reviewer-owned outer lock, and an exception immediately after each successful full-map verification. `os.fork` was replaced with a hard refusal. Actual final source paths and pins were used, and actual memory-limit checks were unchanged. There was no worker, real authority, active production ledger, or store created. This is a full-pin startup cutpoint test, not a replay of the entire new production lifetime.

## Source and accounting review

`SOURCE_DIFF.txt` records the complete old/new source comparison. The engine change is the two bounded digest helpers plus the equivalent synthetic-output digest substitution. Physical receipts, normalized payloads, startup pin loops, and the outer source-marker digest now use streaming SHA-256. The supervisor/observer implementation remains byte-identical. Small normalized payload reads and `/proc` command-line reads remain whole-buffer operations, but the arbitrary-size pinned binaries no longer do. Scheduling, all 24 numerical accumulators, final normalization, accepted m012 controls, retry rules, and stage-token logic are unchanged.

The pinned predecessor and verbatim carry ledger retain the failed job's 120+100=220 control charge. The successor outer requires those first two records and a fresh reservation ID. The global authority remains 21,600 CPU seconds, comprising 16,800 scheduled workers, 3,600 named-retry reserve, 1,200 controls. Old 220 + new 220 +30 ordinary sessions*(20+3)=1,130 controls, leaving 70. This arithmetic is a reservation forecast, not permission to expand it or automatically retry. The sole proposed launch recipe retains the external GNU timeout 28,800-second wall bound plus KILL after 5, deadline reserve, five-process 256 MiB sampled combined RSS accounting, and single-use launch markers.

Initial authority remains at most 100 committed chunks. Any 100→400 or 400→2945 continuation requires a new root-approved token bound to the exact job/checkpoint/cap. The first 100 chunks contain no q6 chunks. Later runtime projection requires the separate 400 stage. A complete 2945-chunk final audit, exact accepted 57D m0/m1/m2 equality, all 24 signed accumulators and sector normalization are still required before full moments can be accepted. Sampled RSS is not an instantaneous cgroup limit.

## Preserved failures and budgets

The original predecessor `db32...` failed before any worker because `Path.read_bytes()` allocated the 30.9 MB Python binary under 64 MiB AS. Its 220 charge is preserved in `failed_predecessor` and the successor carry files. The previous watchdog-gate PASS remains a historical scoped result. This actual failure exposed its missing final-map/actual-limit composition test.

Our first independent streaming attempt failed a review-harness delta assertion, which forgot the equivalent synthetic-output hash substitution. It verified the final map/carry under AS 64 but never reached the three cutpoints. Its complete 10-second reservation is retained unchanged in `BUDGET_LEDGER.json` and `FAILED_DELTA_ASSERTION.json`. The parent approved one separate 8-second correction after all source hash substitutions were reviewed. That correction passed with a 6-second child +2-second parent reservation, charged 8/8. Child wait4 CPU .278862, guard self CPU .046794, no descendants after cleanup. Both ledgers are no-refund and do not reset any older review budget. Metadata preparation/sealing uses the remaining parent allowance. No further numerical execution was made.

## Scope of launch acceptance

The narrow startup allocation defect is independently repaired for the actual final 26 pins and actual AS 64 cap. Prior sealed control, numerical, watchdog, stage-token, exact-controls, recovery, and integration findings continue to apply to unchanged code. Fresh authority, retained 220 plus new 220 precharge, and the initial 100 stop are mandatory. An unforeseen failure still stops for a new decision. This review does not authorize a launch itself.
