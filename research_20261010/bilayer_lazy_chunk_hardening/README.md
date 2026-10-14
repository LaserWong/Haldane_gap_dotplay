# Checkpoint recovery for lazily generated chunks

The controller reproduced the physical fixtures and recovered exact chunk accumulators after deliberately interrupted writes and calculations. The producer submitted these results for independent review on 2026-10-11 at 03:29 UTC / 2026-10-10 at 23:29 EDT. The tests cover the 22-component scalar schema only. No full production run, complete 8×4 support sweep, complete cache, or variable-g weighted extension was performed.

## Results

- Six complete physical fixtures (localized, symmetrized and generic on 4×2/5×2) pass under the new controller. All 15 signed terms and m0–m4 remain exact.
- Four independently computed sector chunks cover the complete generic 4×2 fixture. Their 22 exact integer accumulators sum to the uninterrupted physical fixture result.
- A numerical q6 chunk was deliberately killed after it wrote completed target progress. Its incomplete scalar output was not committed. A separately reserved rerun of the same range matches the uninterrupted chunk in all 22 components. Both 3-second reservations remain charged. The root agent explicitly authorized this planned interruption/resume pair.
- Three separate-process checkpoint crashes (before write, partial write, after atomic rename) recover all 22 exact values. Duplicate identical commits count once. Conflicting duplicates, valid-JSON scalar corruption, truncation, missing/overlapping coverage, malformed integers, wrong job/sector size, wrong pinned inputs and lowered budget charges are rejected.
- The numeric/proc observer detected and killed/reaped both processes in the descendant self-test. The busy-child watchdog stopped at 2.505598 wait4 CPU seconds. Injected accounting failure killed/reaped the child rather than skipping observation.
- The new dispersed schedule sample covers 128 q6 and 32 q4 targets, including the first and final sequence chunks, with no repeated target ranks. It does not cover the full lattice. All existing source/term computations execute in these samples.

The ledger conservatively charges 85/120 CPU seconds, with new admissions stopping at 90. This includes a 10-second reservation for controller and metadata work. Final SUMMARY.json gives actual child wait4, controller timings, metadata timings, wall and RSS. Child work includes intentionally stopped tests. Compilation was separately capped at 512 MiB on CPU6. Compile CPU was not collected by wait4. Earlier seals remain unchanged.

## Files

- whole.cpp / whole_original.cpp / build_source.py: numeric kernel changes limited to dumping all 22 accumulators and generating chunks deterministically. Inherited source snapshots are referenced read-only in ../bilayer_whole_m4_pipeline. The numerical executable is unchanged across every run in this gate.
- controller.py: final atomic writer, pinned-input verifier, no-refund budget validator, single-controller lock, numeric/proc watchdog/subreaper, checkpoint commit and complete-coverage finalizer.
- controller_initial.py, controller_interruption.py, controller_recovery.py, controller_budget_validated.py: earlier controller revisions retained to match per-attempt hashes. These are evidence, not production entry points.
- reviewer_guard_reference.py: read-only snapshot of independently repaired guard, retained for provenance. Its CPU7 settings are not used by the CPU6 controller.
- PINNED_INPUTS.json: externally initialized final input/executable/source/controller identities. Runtime verifies, never silently refreshes it. Changing inputs requires a new explicit initialized job.
- BUDGET_LEDGER.json, runs/*/receipt.json: reservations before launch, all failures retained, actual wait4/controller/wall/RSS. Final successful final_bound_q0 additionally binds every worker output digest before receipt commit.
- CHECKPOINT_TESTS.json, RECOVERY_PROCESS_TESTS.json, ADOPTION.json, adopted/, checkpoints/: exact serialization/recovery/mutation evidence.
- SUMMARY.json: startup/body/controller sample costs.

Use a fresh copy/output directory for review and set PYTHONDONTWRITEBYTECODE=1. Do not execute against this frozen ledger. Guard invocation is `controller.py NAME CAP chunk KIND NX Q BEGIN COUNT`. The fixture invocation is `controller.py NAME CAP fixture KIND NX`. Standalone executable arguments are documented by whole.cpp. The cap is the per-attempt allowance, not extra authority. This gate's controller hardcodes 120/90 and cannot serve as a 21600-second launcher without separately reviewed allocation configuration.

## What remains to be checked

The first numerical receipts bound executable/input hashes but not worker-output hashes. Their output content was subsequently adopted into prepared SHA256 journals with exact physical comparisons. This is not retroactive evidence of an exit-time output hash. The final controller adds immediate output digests and final_bound_q0 exercises that path. Independent review should require it for every production chunk.

The complete physical/sampling executable hash is identical throughout. Controller revisions add fault injection, checksum journals, stale-temp tolerance, pinned verification, budget-schema checks and final output digests. Core observer/group-kill logic is shared across revisions. An independent reviewer should replay the final controller, not assume earlier self-tests certify every later line.

The controller times reported in earlier receipts start after initial hash/setup work and omit interpreter startup/final receipt overhead. The final version starts its clock earlier, but still reports before final receipt writes. Ten reserved controller seconds cover this test. Measured controller values are not claimed as an exhaustive process-level wait4 total. Metadata child wait4 and process CPU are separately recorded. Production admission retains explicit overhead reserve and requires independent controller accounting review.

Checkpoint fault tests use deliberate process exit at specified transaction boundaries, not a simulated filesystem/power-loss failure. fsync/atomic rename rely on the actual filesystem's guarantees. No hardware power-failure claim is made. Complete small geometry normalization tests are inherited from the physical fixtures. No full 8×4 normalized moment is claimed. The adopted sample is explicitly rejected by the complete-coverage finalizer.

This is an implemented/tested checkpoint API and bounded dispatch driver, not an automatically running full production scheduler. Input job initialization and the production allocation configuration must be reviewed before launch. No variable-g extra fields have been added. Independent review must decide whether any control gaps require another bounded fix before requesting production authority.
