# Append-only campaign extension and bounded-invocation repair

2026-10-11 00:12 UTC. Design-only producer gate. No production ledger change, restart or thermal job has occurred. Root explicitly authorized DESIGN of +21600CPU seconds, preserving16207 charged and all old history, for new total43200. Launch still requires independent review and root's fresh instruction.

## 1. Why this fixes the actual boundary

The old runner remains frozen and byte-identical. Its generic remaining-budget rule is not claimed repaired. Instead the new supervisor confines it to a proved-safe domain: max_new_batches8, internal compute-phase allowance600CPU seconds, fixed35-second cap per compute child. Metadata children get5 seconds. Runner and watchdog each get35 seconds. Linux enforcement slack of2CPU seconds is charged per possible process.

Even if every one of eight children consumes its full37-second charged allowance, and all runner overhead consumes37 seconds, total used in the compute phase is at most333. (Metadata occurs before the runner's phase counter starts, but is separately reserved.) Therefore the legacy remaining=int(600-used)-1 is at least266, always exceeding its requested120 cap. The legacy min(120,remaining) can NEVER shorten a child within an allowed invocation. The private hook instead gives that child its full fixed35 seconds. After at most eight complete checkpoints the frozen runner returns normally. Unprocessed work is left for the next invocation. This is a deterministic checkpoint-preserving stop before the insufficient-allowance regime, not a claim about typical timing.

The code asserts INTERNAL_ALLOWANCE>BATCHES*(CPU_CAP+2)+(CPU_CAP+2)+120+2. No CLI can override those fixed production constants. A truly slow >35-second compute batch may still fail safely; it is not intentionally starved by a shrinking invocation budget. Current measured successful batches took6.8–11.6 seconds. Five-second metadata caps exceed observed per-child setup by a substantial factor, though neither timing claim is a mathematical guarantee of successful completion.

A scaled nonthermal runtime fixture deliberately recreates the old failure: budget7, three2.2CPU-second batches, requested child cap3. The caps become3,3,1; the third child is killed. Under the bounded configuration (budget30,max3,cap3), all three complete with full caps and checkpoints. The larger workload compared with the reviewer's independent1.3-second fixture avoids dependence on exact RLIMIT_CPU tick granularity. No thermal arithmetic was executed in these tests.

## 2. Reservations now match this whole-process domain

For n12, each run invocation has at most26 metadata children, eight compute children, one runner and one watchdog. Reserve26*(5+2)+(8+2)*(35+2)=552CPU seconds. Prepare reserves52*7+2*37=438; validate reserves26*7+2*37=256. Both setup and compute are included. Every default cap is enforced by the reviewed process-tree structure plus the new private CPU hook. Parent wait4 refunds only after normal terminal whole-tree completion, rounded up plus2. Unknown/failed attempts retain their full552-or-smaller reservation. Two maximal run reservations1104 fit comfortably within the extended remaining26993.

Supervisor itself retains the separate120CPU-second hard cap and122 charged reserve. At most two worker trees use CPUs0 and1. Each has64MiB watchdog+96MiB runner+96MiB single child, total256MiB address ceilings. The private hook is never installed system-wide. It changes resource/lifetime policy only, not the physical matrix, coefficients, floor/norm arithmetic or output identity.

## 3. Append-only authorization transition

The ONLY production state path is /workspace/shared/haldane_active/research_20261010/uniform_second_thermal_campaign_run. No alternative/copied production ledger is allowed. On explicit launch, the extension constructor acquires the same exclusive lock and requires the exact frozen original terminal-file SHA256, original limit21600, deadline06:00UTC, BUDGET_RESERVATION_EXHAUSTED state, no active/reserved attempts, and total old charge16207.

BEFORE changing the active ledger, it saves byte-identical old terminal content to history/original_terminal_<SHA256>.json, with fsync. It then appends one extension event recording authorizationID root-20261011-cap-extension-21600-to-43200, old21600 limit, +21600 amount, new43200 cap, retained16207 charge, original terminal state/hash, original attempt count/digest, original bindings digest, new supervisory bindings, unchanged deadline and timestamp. Original attempts and original bindings are retained unchanged; only new attempts are subsequently appended. New active limit43200 and EXTENSION_READY/RUNNING state reflect this explicit authorization, not a reset/refund.

Resume checks EXACTLY one event and all fixed event fields, original terminal hash equal to the source-pinned constant, byte-identical historical attempt prefix, original bindings, and current extension source/hook pins. Changing an event plus recomputing its outer JSON checksum is insufficient. Duplicate extension, changed old charges, changed hashes/limits/deadline and post-deadline extension are rejected. The deadline is checked before the first extension write. Existing final certificates require current-invocation validation through the frozen runner; historical success plus existence is not trusted.

Fixture copies of the old ledger exist ONLY under this design-test package to test prefix equality. They are not alternative campaigns, cannot be used by the production CLI's exact-path assertion, and launched no thermal process. The actual production ledger was verified byte-for-byte unchanged after all tests.

## 4. Checkpoint provenance and lifetime

Frozen campaign.py, kernel.cpp, compiled kernel and coefficients are unchanged. Existing case/batch wrapper/source/binary/matrix/orbit pins therefore remain valid; no data are relabeled as generated by new arithmetic. The new supervisor/hook are separate extension bindings. All28 existing partialL12 checkpoints pass the original strict validator under their original identities. Completed16 cases remain independently reviewed under the partial-review seal.

The previously reviewed watchdog process-group, parent-death and absolute-deadline propagation remains. Hooks additionally distinguish child mode list/matrix (5CPU seconds) from compute (35); unexpected child command modes fail. Group cleanup completes before slot reuse. Unknown/completion accounting, exclusive flock, fixed user/campaign deadlines, exact successful wait4 refunds and no automatic restart after terminal state are preserved. Campaign wallstop remains2026-10-11T06:00:00Z, earlier than user2026-10-14T00:00:00Z.

## 5. Tests and expected resources

Tests verify exact old16207 charge retention, original terminal bytes and attempt/binding prefix, new43200 limit, duplicate extension rejection, refund mutation rejection,12 altered-event/deadline cases, unchanged old checkpoint pins, scaled old-boundary failure, repaired bounded completion, and metadata-only integration of the actual frozen runner under new hooks. These consumed about14CPU seconds, under120CPU/256MiB, CPU0. No new thermal columns or production-state mutation occurred.

The remaining measured kernel+batch-setup estimate is8621CPU seconds. With at most eight batches per invocation,1438 remaining batches need about180 invocations; repeated metadata revalidation (roughly7–9CPU seconds each from prior full preparation timings) adds around1260–1620 seconds, plus parent bookkeeping/rounded fees. Planning estimate about10000–11500 additionalCPU seconds, not a guarantee. This fits26993 extended remaining with substantial failure headroom. No unknown old attempt receives a refund. The6:00 wallstop and aggregate43200 cap remain hard stops.
