# Proposed full57D fixed-witness m0–m4 launch contract

SOURCE-ONLY. No production launch, test of this wrapper, or production authority is included. This successor preserves the prior e43899b7f3ba4f6baf8627832c711d2b03b56ae3a5ce45b385ab3ad94134b7e4 source unchanged. Component review and bounded integration are separate from this unreviewed outer delta.

## Identity and controls
Stable job directory: research_20261010/bilayer_full_m4_production_run. Its PINNED_INPUTS.json binds the final64/64/128 source revision427344..., numerical24 executable/source, pencil consumer, three Brauer diagram files, geometry, fixed57-component witness, accepted-m012 control file, this outer guard and launch shell. Job ID is SHA256 of engine.raw({kind:'PHYSICAL-FIXED-WITNESS24',schema:'bilayer-moment24-v1',identity:pin_map}). No test adapters, synthetic records or mock controls enter that map. EXPECTED_M012 comes from the accepted full57D review874c87..., not the43D compression. Independent verification pending.

## Cumulative reservations
Hard job envelope21600 CPU seconds =16800 standard worker reservations +1200 fully prepaid control pool +3600 specifically authorized retry reserve. Workers: q0 one3-second; q2 eight3-second; q4 281 three-second; q6 2655 six-second =2945 chunks. No refund after any failure/interruption. The attempted reservation is archived idempotently and a matching explicit retry receipt is required before replacement.

Before executing launch.sh, root must atomically create/verify the reviewed CONTROL_SESSIONS ledger and reserve120 from its1200 pool: controller_cap100, supervisor_cap20, charged120, state reserved, with an explicit unique reservation ID in authority. The100 is the persistent outer's own CPU cap;20 covers one failed pre-inner-reservation child startup. On successful inner launches their startup is included in their3-second supervisor self cap. An unexpected child failure stops the outer; no second uncharged startup is attempted. Every outer restart needs a NEW120 reservation, never reuses its old ID. No ledger/authority has been initialized by this proposal.

One standard inner session reserves20 controller +3 supervisor seconds. Thirty100-chunk sessions cost690 control seconds; with outer120 this leaves390 of1200 for early graceful sessions, finalization and specifically approved recovery. Inner admission checks enough remaining controller slots. The entire1200 pool remains included in the21600 forecast even when actual use is lower.

## Resource bootstrap and runtime
Only launch.sh is proposed; bare production_supervisor.py is not an authorized launch recipe. It sets CPU6 and initial OS CPU99soft/100hard plus AS64MiBsoft/128hard before Python import or pin hashing. Hard ceilings permit descendants to set their own reviewed caps; no inherited-low-hard-limit trap. Outer precharge must already be durable before exec.

Production inner virtual profile is supervisor64 +controller64 +native128 MiB =256 MiB soft caps. The additional persistent outer has64 MiB soft AS, hence FOUR-process virtual cap sum320 MiB. The outer continuously includes all four resident sets in a256 MiB aggregate RSS ceiling. This distinction is explicit. Inner three-process RSS guard remains redundant. Outer samples actual /proc limits and CPU affinity after recognized exec; short processes can exit between polls, so per-process sampling is not asserted complete. Before-exec setters remain the source-level guarantee inherited through exec. Native128 was measured with accepted64-q6 control; observed VmPeak38,637,568 bytes.

Outer observes numeric /proc process trees from child startup, fail-closes missing accounting, tracks wait4 tree CPU separately from own CPU, watches cumulative current-run actual CPU21600 in addition to no-refund ledger admissions, kills known groups/PIDs and reaps via subreaper. Cleanup does not require a fresh process inventory. Persistent own CPU stops at98 seconds, preserving the100 limit. Post-exec observations are serialized in its final receipt.

## Coverage and checkpoint cadence
2945 disjoint chunks cover q0=1, q2=496 full supports, q4=4495 anchored supports and q6=169911 anchored supports. Modular schedules are multipliers1/127/1024/65536, respectively, coprime to sector domain sizes; independent canonical rank proof applies. The origin-normalization factors are1,1,8,16/3 with stabilizers already accounted for. No second factor32 division.

Every worker reserves before fork, starts cold lazy caches, emits24 exact signed scalar fields, verifies all output digests/rank ranges, and atomically commits once. Each session performs one startup reconciliation then incremental commits. Source coefficients/GMP and all15 terms remain unchanged. No full q6 cache is built.

First stage dispatches at most100 chunks, then the persistent outer writes CHECKPOINT_READY_100.json with exact state hash and waits with NO active worker. In current ordered plan these are vacuum, all eight q2 chunks and91 q4 chunks; the first stage does not yet sample q6. Root must inspect committed/attempt/output hashes, coverage, ledger/no-refund charges, resource receipts and startup/profile observations before writing exactly matching CONTINUE_AFTER_100.json with explicit_root_approval=true and max_completed_chunks=400. The token binds job ID and checkpoint SHA256. Restart reconstructs this bounded token chain. The next pause is at or before400 committed chunks, including at most110 q6 chunks if sessions complete fully. A separate matching CONTINUE_AFTER_400.json with max_completed_chunks=2945 is required for the remainder. An early graceful session can cause a pause below the cap rather than rounding permission upward. No token can authorize a higher cap than its explicit field. Root should monitor each session receipt and stop on any failure or unsupported cost change; no automatic numerical retry.

## Cost, wall and final acceptance
Measured complete cold pipeline projection1507.736555 CPU, with historical conservative10x setup/chunk/control envelope17649.86555. This is a projection, not a promise.21600 includes every reserved failure, setup and control cost; no automatic expansion.

Absolute deadline2026-10-14 00:00UTC, with at least86400 seconds independent-review reserve. Inner admission uses actual remaining worker/retry allowances plus10 seconds per possible worker, controller/session overhead and that reserve. Outer additionally uses a conservative upper bound for the ORIGINAL complete plan before each session, never a zero forecast; this may refuse a late continuation even if inner remaining-work estimate would fit. Each session wall≤2260, outer2280. Root must not weaken a deadline refusal without a new reviewed decision.

After complete coverage, assemble24 fields with exact rational sector factors. Full m0,m1,m2 must equal accepted controls exactly before FULL_MOMENTS is written. Version24 pencil denominators are22*g_den and its square; G denominator1. Only then separately review m3/m4 and pencils. No new spectral-gap or all-size claim follows automatically.

Remaining admission conditions: independent accepted-control verification, independent outer delta/startup/fault review, final hash/job-ID confirmation, root explicit production approval, durable120 outer precharge and exact authority document. No production numerical work is authorized by this file.

Reviewer tightening: inner supervisor pre-exec CPU soft3/hard20 caps startup at its nominal3 while allowing the forked controller20. Outer own hard100 plus one failed-startup contingency20 cannot exceed its120 prepaid allocation.

The only allowed token transitions are100→400 and400→2945. A100 token cannot skip directly to2945 even if its JSON field is larger.
