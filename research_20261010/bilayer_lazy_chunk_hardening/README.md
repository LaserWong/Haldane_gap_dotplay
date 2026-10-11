# Lazy-chunk checkpoint hardening gate

2026-10-11 03:29UTC / 2026-10-10 23:29EDT. Producer handoff for independent hardening review. No full production, full8×4 support sweep or complete cache was performed. Schema remains exactly22 scalar components; variable-g weighted extension is excluded.

## Results

- Six complete physical fixtures (localized, symmetrized and generic on4×2/5×2) pass under the new controller. Every15 signed term and m0–m4 remain exact.
- Four independently computed sector chunks cover the complete generic4×2 fixture. Their22 exact integer accumulators sum to the uninterrupted physical fixture result.
- A numerical q6 chunk was deliberately killed after it wrote completed target progress. Its incomplete scalar output was not committed. A separately reserved rerun of the same range matches the uninterrupted chunk in all22 components. Both3-second reservations remain charged; root explicitly authorized this planned interruption/resume pair.
- Three separate-process checkpoint crashes (before write, partial write, after atomic rename) recover exact22 values. Duplicate identical commits count once. Conflicting duplicates, valid-JSON scalar corruption, truncation, missing/overlapping coverage, malformed integers, wrong job/sector size, wrong pinned inputs and lowered budget charges are rejected.
- Numeric/proc observer detected and killed/reaped both processes in the descendant self-test. Busy-child watchdog stopped at2.505598 wait4 CPU seconds. Injected accounting failure killed/reaped the child rather than skipping observation.
- New dispersed schedule sample covers128 q6+32q4 targets, including the first and final sequence chunks, with no repeated target ranks. It does not cover the full lattice. All existing source/term computations execute in these samples.

Resource ledger:85/120 CPU seconds conservatively charged, soft admission stop90. This includes10 seconds reserved for controller/metadata. Final SUMMARY.json gives actual child wait4, controller timings, metadata timings, wall and RSS. Child work includes intentionally stopped tests. Compilation was separately capped512MiB and CPU6; compile CPU was not collected by wait4. Earlier seals remain unchanged.

## Files

- whole.cpp / whole_original.cpp / build_source.py: numeric kernel changes limited to dumping all22 accumulators and deterministic chunk generation; inherited source snapshots are referenced read-only in ../bilayer_whole_m4_pipeline. The numerical executable is unchanged across every run in this gate.
- controller.py: final atomic writer, pinned-input verifier, no-refund budget validator, single-controller lock, numeric/proc watchdog/subreaper, checkpoint commit and complete-coverage finalizer.
- controller_initial.py, controller_interruption.py, controller_recovery.py, controller_budget_validated.py: earlier controller revisions retained to match per-attempt hashes. These are evidence, not production entry points.
- reviewer_guard_reference.py: read-only snapshot of independently repaired guard, retained for provenance; itsCPU7 settings are not used by ourCPU6 controller.
- PINNED_INPUTS.json: externally initialized final input/executable/source/controller identities. Runtime verifies, never silently refreshes it. Changing inputs requires a new explicit initialized job.
- BUDGET_LEDGER.json, runs/*/receipt.json: reservations before launch, all failures retained, actualwait4/controller/wall/RSS. Final successful final_bound_q0 additionally binds every worker output digest before receipt commit.
- CHECKPOINT_TESTS.json, RECOVERY_PROCESS_TESTS.json, ADOPTION.json, adopted/, checkpoints/: exact serialization/recovery/mutation evidence.
- SUMMARY.json: startup/body/controller sample costs.

Use a fresh copy/output directory for review; set PYTHONDONTWRITEBYTECODE=1. Do not execute against this frozen ledger. Guard invocation is `controller.py NAME CAP chunk KIND NX Q BEGIN COUNT`; fixture invocation is `controller.py NAME CAP fixture KIND NX`. Standalone executable arguments are documented by whole.cpp. The cap is the perattempt allowance, not extra authority. This gate's controller hardcodes120/90 and cannot serve as a21600-second launcher without separately reviewed allocation configuration.

## Provenance limits and remaining admission work

The first numerical receipts bound executable/input hashes but not worker-output hashes. Their output content was subsequently adopted into prepared SHA256 journals with exact physical comparisons. This is not retroactive evidence of an exit-time output hash. Final controller adds immediate output digests and final_bound_q0 exercises that path. Independent review should require it for every production chunk.

The complete physical/sampling executable hash is identical throughout. Controller revisions add fault injection, checksum journals, stale-temp tolerance, pinned verification, budget-schema checks and final output digests. Core observer/group-kill logic is shared across revisions; independent reviewer should replay the final controller, not assume earlier self-tests certify every later line.

The controller times reported in earlier receipts start after initial hash/setup work and omit interpreter startup/final receipt overhead. The final version starts its clock earlier, but still reports before final receipt writes. Ten reserved controller seconds cover this gate; measured controller values are not claimed as an exhaustive process-levelwait4 total. Metadata childwait4 and process CPU are separately recorded. Production admission retains explicit overhead reserve and requires independent controller accounting review.

Checkpoint fault tests use deliberate process exit at specified transaction boundaries, not a simulated filesystem/power-loss failure. fsync/atomic rename rely on the actual filesystem's guarantees. No hardware power-failure claim is made. Complete small geometry normalization tests are inherited from the physical fixtures; no full8×4 normalized moment is claimed. The adopted sample is explicitly rejected by the complete-coverage finalizer.

This is an implemented/tested checkpoint API and bounded dispatch driver, not an automatically running full production scheduler. Input job initialization and the production allocation configuration must be reviewed before launch. No variable-g extra fields have been added. Independent review must decide whether any control gaps require another bounded fix before requesting production authority.
