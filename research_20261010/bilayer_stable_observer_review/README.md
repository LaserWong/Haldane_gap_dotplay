# Independent stable-observer and checksum review

Sealed 2026-10-11 01:35 EDT / 05:35 UTC.

## Review result

The review accepts the repaired observer, unchanged scientific validator, retained accounting, and bounded staged-launch checks for proposed job `c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01`. This remains conditional on new root launch authority, the durable fresh 220 control reservation in addition to all prior charges, and the initial 100-chunk limit. No physical worker was launched by this review. No complete moments or gap are claimed.

The accepted source seal is `6b810258d0d4f593d6d19308b5d19690dedde8d69ac721e9554b6dff66cc9d5a`, `bilayer_stable_observer_checksum_fix`. The exact 28-entry pin map is `4c9c17ece2714710b83c8f4e975b027dc057da3a51bb9d44671ba869b124f6da`. Source snapshots, pin membership, controls, predecessor, retired-worker accounting and raw test receipts are included.

## Independently checked source and science

The actual verify_output, worker, stop_after_chunk, required_pins and finalize_physical functions are byte-identical to accepted streaming source 88aa9e.... The dispatcher run AST becomes exactly the accepted AST when named resource budgets are mapped back to their old constants. The coverage plan, native executable, numerical source, pencil consumer, session supervisor and production supervisor remain identical. New resource constants are CONTROL_POOL=1600, RETRY_POOL=3200, and RETIRED_WORKER_RESERVATIONS=192.

The first observer candidate aec2ba0... was rejected by static inspection because an unscoped budget substitution had changed the scientific m3 coefficient 193600 to 193200. That seal and finding are preserved under rejected_aec2 and REJECTED_AEC2_FINDING.json. The correct coefficient 1600*121=193600 is restored. A previously accepted physical chunk 9 with nonzero n8=21577012503156359948438856 passed the actual new validator. A separately copied, hash-consistent result changed only to the wrong 193200 m3 assembly was rejected. Its signed-term ordering remained unchanged. This was metadata validation of existing physical evidence, not a new numerical fixture.

## Deterministic observer tests

The helper is byte-identical to the producer-tested helper, with only its required affinity value adapted from CPU6 to reviewer CPU7. Three real fork/exec fixtures use /usr/bin/sleep, never the scientific kernel. Pipe barriers make the parent sample before limits change, after limits change with inherited argv, and after exec. Both inherited-parent stages defer, the correct stable runtime passes, and genuine bad CPU and address-space limits are rejected with full persisted before/after identities and observed tuples. A separately injected wrong affinity is rejected without executing on another CPU. A constructed read straddling exec defers. The same PID/starttime/image is rechecked after a genuine post-exec CPU-limit change and rejected, demonstrating that a previous pass cannot permanently exempt the process. Unexpected stable image and exited-during-observation cases are also checked. All test children are killed and wait4-reaped.

Static outer review confirms topology-derived roles and per-poll calls to the helper without the old PID-only cache. The source persists mismatch diagnostics before raising. Resource enforcement continues through deferred transitions. Sampling is supplemental and cannot guarantee observing every short-lived worker. The actual cause of the prior 63-commit failure remains unproven because that older code did not save its failing tuple.

## Final pins and address-space startup

All 28 pin keys were independently matched to the prior 26 map with path substitutions plus exactly limit_observer.py and RETIRED_WORKER_CHARGES.json. Every digest was checked, including the 30,894,944-byte Python executable. All three actual entrypoints reached their actual full-map verifier under real 64 MiB soft/128 MiB hard AS imposed before imports. VmPeak was 44,306,432 bytes. Test-only outer adaptations were CPU7 and a 4-second CPU cap, a reviewer-owned lock and memory-only fixture authority. Each entry stopped immediately after successful verification. os.fork was forbidden for this phase. No real production authority, ledger or store was created.

## Global budget, stages and remaining limits

The global CPU ceiling remains 21,600 seconds, allocated as 16,800 for standard workers, 1,600 for controls, and 3,200 for retries. Pinned carry preserves 463 controls, including the original 220 failure, and 192 retired worker reservations consisting of 189 completed plus 3 in-flight. Old numerical accumulators are not rebound to the clean generation. The retired 192 consumes retry allowance, leaving 3,008. Initial worker forecast is exactly 21,600. A reviewer-only reservation/restart fixture preserved the charge as 195 after a 3-second abandoned reservation, without doubling or refunding the 192. New-control forecast 463+220+30*23=1,373 leaves 227. A fixture ControlBudget accepted exactly the carried first 5 records plus new IDs 5/6. Full source still refuses unbudgeted automatic retries or expansion.

Only the pinned watchdog recipe is accepted. It uses CPU6 and an external GNU timeout of 28,800 seconds, sending TERM followed by KILL after 5 seconds. Startup reserves 28,805 seconds plus 24 hours before the deadline. Source CPU/AS inheritance, five-process sampled combined RSS of 256 MiB cap, pre-exec shell limits and durable single-use markers retain the earlier reviewed contract. Virtual soft limits sum to 384 MiB, separately from sampled RSS. This is not an instantaneous cgroup bound. Tokens remain exactly 100→400→2945, bound to job and checkpoint, with no worker while paused. The first 100 has no q6 coverage. A separately approved 400 stage is needed for representative q6 cost evidence.

The heavier per-poll observer and retained full identity records have not completed a full production lifetime. Stage checkpoints must inspect actual CPU/memory, complete-work/deadline forecasts, idle state and digests before later authority. All 2945 chunks, exact sector normalization, all 24 signed accumulators and accepted 57D m0/m1/m2 equality remain final acceptance gates. Component tests do not establish full scientific output.

## Review reservations and failures

The first 8-second review gate stopped before any test fork on a reviewer count assertion that expected 27 pins rather than the actual 28. The correct map hash and source manifest matched. This was a harness error. That complete 8-second reservation is retained unchanged, including .111976 child CPU and .087659 guard CPU. Parent separately approved a 6-second correction after the full map/keyset and assertions were inspected. The corrected 4-child+2-parent gate passed, fully charged 6/6. Its wait4 tree CPU was 1.105272, guard CPU .222168, and observed combined RSS 30,257,152, no descendants after cleanup. Metadata preparation/sealing uses the remaining parent allowance. All earlier sealed review budgets and production failure charges remain unchanged.
