# Independent append-only extension and boundary repair gate

## Verdict

PASS for the frozen extension design and bounded fixture configuration. This gate does not itself activate the extension or authorize a thermal run. A final root launch decision is still required.

Producer uniform_second_thermal_extension_gate manifestc97bbaba6236265d86770be29c7bc9a35e9c28d1bb1de0cf1e16f5f029ae83fd was fully verified before executing exact copies of its supervisor/hook in this review directory. Production ledger bytes remain unchanged. Scientific campaign.py, kernel source/binary and coefficients remain frozen at the earlier strict-runner manifest4a282841f56100a6ea99d20d9ce63a79309afe0d1ecdec12f39dee4f94013b68. Existing physical checkpoints retain their exact original identities.

The approved design allocation extends the cumulative CPU cap from21600 to43200 seconds, retaining all16207 already charged. It grants26993 additional spendable seconds before new overhead/work, not a refund. The sole state path remains /workspace/shared/haldane_active/research_20261010/uniform_second_thermal_campaign_run. No alternative path, copied production ledger, reset or second campaign instance is permitted. At most two CPU0/1 worker trees retain256MiB per-tree address-space ceilings, plus separately charged bookkeeping. The wallstop remains2026-10-11T06:00:00Z, earlier than research hardstop2026-10-14T00:00:00Z.

## Actual boundary regression and repair mechanism

The earlier partial run failed after16/12 L12 batches because the generic runner launched another full batch with its shrinking invocation remainder. Independent boundary_regression.py demonstrates the same mechanism using only short CPU-consuming Python children: with a5-second invocation allowance and1.3CPU-second work per batch, child caps are4,2,1 and the third exits−9. A separate fixed2-second-allowance variant finishes two batches and yields before the third. These are actual process-limit tests, not only a scalar timing simulation. Total waited-childCPU was6.45 seconds; no heat command was executed.

The production repair intentionally leaves the generic runner unchanged. It restricts its configuration to at most8 new batches per invocation and internal allowance600. The private hook enforces a fixed35CPU-second cap for each compute child and5 seconds for list/matrix metadata children; runner and watchdog each get35. Reserve two additional seconds per possible process for Linux enforcement granularity.

For every prefix of any allowed invocation, compute children consume at most8·37=296 chargedCPU seconds and runner overhead at most37. The counter used by the legacy shrinking rule starts after metadata, so its used amount is at most333. Thus int(600−used)−1 is at least266 (our independent inequality uses the even more conservative lower bound265), always greater than120. The legacy min(120,remaining) cannot shorten a batch request. The hook then applies the same full35-second compute cap to every batch. After at most8 checkpoints, the frozen runner returns normally, leaving the next work for another invocation. This is deterministic yielding before the unsafe region; the generic runner is not claimed safe under arbitrary configurations.

The code asserts the configuration inequality and supplies fixed8/600 arguments internally; the production CLI cannot override them. Our independent checks cover every prefix0..8, not only observed timings. A genuinely slow compute batch exceeding35 seconds or metadata child exceeding5 can still fail safely. This gate guarantees avoidance of the previous artificial short-allowance failure, not universal completion under any host conditions.

## Correct whole-process reservations

Prepare creates at most4(n+1) metadata children. Run/validate creates2(n+1), plus at most8 compute children for run. The reservation is metadata_count·7+(compute_count+2)·37, including runner and watchdog. At n12 this gives438 for prepare,552 for run and256 for validate. Two maximal run reservations need1104, well below the26993 extended remaining capacity. Every dimension4..12/action combination is checked independently.

Live hook fixtures reproduce the frozen runner's original preexec resource requests. They verify5CPU seconds for list/matrix,35 for compute,96MiB child address limits and one-core affinity. All actual frozen-runner child creation sites supply these preexec callbacks; the hook clamps their calls and adds lifetime protection. The hook must not be generalized to arbitrary new subprocess creation without review.

Successful terminal whole-tree wait4 measurements permit only the existing conservative ceil(CPU)+2 refunds. Unknown failures retain their complete new552-or-smaller reservation. All old7320 failed charges remain unchanged. The separate supervisor still gets120CPU hard limit and122 charged seconds. Parent-death signals, absolute-deadline alarms, group cleanup before slot reuse and the two-worker cap retain the previously independently tested implementation. AST comparison shows guardian, launch and drain definitions unchanged from the accepted supervisor; the changes are reservation, ledger-extension logic and production arguments in main, plus mode-specific resource clamping in the private hook.

## Append-only extension integrity

Activation requires the exact original terminal ledger file SHA2569a6b8fe6944c06544247c07b04344e2258784cbfc722f902b3cc2b979d57f288, old limit21600, terminal BUDGET_RESERVATION_EXHAUSTED, unchanged deadline, no active/reserved work and16207 total charge. The constructor rejects any production state path other than the sole authorized one. Deadline validity is checked before extension writes.

The old terminal bytes are first preserved in history with fsync. Exactly one authorization event records21600 old limit,+21600 extension,43200 new limit,16207 retained charge, source-pinned original terminal hash, original61-attempt prefix/digest, original bindings/digest, unchanged deadline and new supervisor/hook bindings. Original attempts and original scientific bindings remain byte-equivalent as data. Only subsequent new attempts are appended. The authorized terminal-to-EXTENSION_READY/RUNNING transition is explicit; it is not an automatic reset.

Resume pins the historical hash to the source constant, requires one event and exact authorization/limit/deadline fields, verifies the original historical bytes and attempt/binding prefix, and checks active extension source pins. Our tests reject altered authorization, old/new/additional limits, retained charge, deadline, original hash/count/binding digest, extra events, retroactive refunds and historical binding rewrites, even when operating on otherwise coherent fixture objects. Duplicate activation is rejected. New552 reservation is shown to append after the preserved61 original attempts without changing them.

The changed resource policy is bound at supervisor/hook level; no scientific wrapper migration occurs. All prior case/batch hashes remain truthful and valid. Current-invocation run/validate is still required before a historical final certificate is considered complete. A new terminal failure/deadline/exhaustion still requires another explicit root decision; this gate creates no recurring extension authority.

## Independent tests and limits

Nineteen extension/runtime tests pass in extension_test_results.json. They ran exact copied inspected code only against the review's immutable terminal-copy fixture and trivial process trees, underCPU5/256MiB. The actual production ledger was read before and after and stayed byte-identical. The terminal fixture is not an alternative campaign: no thermal command can be dispatched by the test harness, and the production canonical-path constructor is bypassed explicitly only for testing the extension method on the copy.

Two preliminary harness mismatches are retained transparently: a30-second inherited hard cap prevented the tested guardian from installing its intended35-second cap; then a dummy subprocess lacked the frozen runner's preexec resource setter, so a clamping hook had no request to clamp. The final harness allows the intended guardian setting while bounding its trivial group with a15-second wall alarm, and supplies the same resource callback as the actual frozen runner. Neither event changed production state or represented a physical arithmetic failure. Final extension tests used about.07 selfCPU+.23 childCPU seconds; all independent review fixtures, including the6.45CPU-second boundary reproduction and preliminary attempts, stayed below30CPU seconds and256MiB.

The16-input partial physical acceptance remains unchanged, and both L12 full traces remain absent at this gate. Conditional scalar gaps are not promoted by a resource extension. The remaining-work estimate is planning evidence only; final physical output review is still required after any separately authorized resumed campaign.
