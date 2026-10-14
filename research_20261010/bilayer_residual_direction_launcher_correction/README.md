# Separately sealed parent-death and lock correction

2026-10-10 21:32 EDT / 2026-10-11 01:32 UTC. Producer correction PASS, independent acceptance pending. Design/small-fixture authorization only. No 8×4 work and no production launch.

## Correction

The prior sealed production gate remains unchanged. `checkpoint.py` now arms Linux PR_SET_PDEATHSIG(SIGKILL) in the child pre-exec function, then verifies its parent PID still equals the PID captured before fork. A parent death between fork and prctl therefore either triggers the installed signal or fails the explicit identity check and immediately kills the child. The child does not proceed with limits or exec until this guard succeeds.

The campaign's flock descriptor is retained in the kernel using subprocess `pass_fds`. Thus an abrupt supervisor death cannot release exclusive ownership while that child remains alive, even during parent-death signal delivery. The descriptor closes on kernel exit. Direct library `run_chunk` calls also acquire and pass the campaign lock when the caller did not provide one. The scientific kernel never forks or spawns descendants. This guard is deliberately scoped to the actual single-kernel topology.

PR_SET_PDEATHSIG persists across the ordinary non-setuid kernel exec. No setuid binary, capability transition, detached process, shell launch or descendant worker is used. Timeout handling still kills/waits for the direct child, and all interrupted attempts retain their prior CPU charge. An orphaned reserved entry is not successful coverage.

## Real adversarial tests

`test_interruption.py` uses a separately identified test-only single-process executable, `interrupt_probe`, in an isolated launcher directory. The probe writes its PID and waits before exec, allowing a deterministic supervisor kill. It then delegates, on a successful restart, to the unchanged real 4×2 kernel. This test probe is NEVER the production scientific kernel.

For both supervisor SIGKILL and SIGXCPU, tests establish the following.
1. The child is running and actually holds the campaign lock inode through an inherited descriptor.
2. A competing CLI restart is rejected by the lock and cannot launch a second child.
3. Killing the supervisor terminates the child. The inherited lock is released only after child death.
4. A subsequent restart executes a real 4×2 one-support chunk successfully.
5. The first reserved attempt remains charged. Charges progress 3→5 rather than being refunded/reset.

A direct fork test additionally invokes the exact production guard with a mismatched expected parent identity and verifies termination by SIGKILL, exercising the fork/prctl race-check branch. `interruption_tests.json` records the results. The separately repeated complete 4×2 gate test still matches all physical rows/scalars and all 11 prior rejection tests.

## Scientific compatibility and source binding

The kernel source, include files and executable are byte-identical to the preceding production gate. The executable SHA256 is 1ca45020313a43902c62e72220554e561b2766c77403af63a488bc1bbb0c8667. `compatibility.json` verifies exact equality of the normalized scientific rows, coupling-polynomial rows and scalars between the old and corrected complete 4×2 checkpoints.

The wrapper change intentionally gives NEW configuration hashes. Old checkpoints are not silently rebound or overwritten and must not be resumed under the changed launcher. No 8×4 production checkpoint exists, so no production progress is discarded. Any future migration of a genuine campaign would require a separately reviewed explicit compatibility bridge. None is claimed here.

## Resource accounting qualification

All resource limits remain unchanged at CPU 3, supervisor 32 MiB+kernel 68 MiB, supervisor 1 CPU second per CLI invocation, child hard cap=specified chunk cap−1. The proposed successful schedule remains 350 charged seconds within a proposed 360-second campaign (44 chunks plus initialization/assembly).

Importantly, the internal state ledger charges successful/reserved work, initialization and assembly attempts. Rejected preflight calls, lock failures and already-complete output rereads also consume up to 1 supervisor CPU second but do NOT currently increment that state ledger. Therefore the 350 calculation is a bound for the stated successful invocation schedule, NOT a ledger-only bound for arbitrary repeated CLI commands. Before any full-run authorization, the parent/driver must record every EXTRA invocation and subtract 1 second per extra invocation from the remaining 10-second allowance, including rejected calls and rereads. A retry already charged as a chunk includes its supervisor second and must not be double-counted. Stop before launching an invocation if that combined accounting would exceed 360. Do not claim that the state ledger alone enforces arbitrary whole-campaign usage.

The adversarial tests deliberately include rejected invocations and are fixture tests, not a production campaign. Compilation of the small test probe used the same separately allowed 512 MiB/40 CPU-second cap. No 8×4 support computation or enlarged numerical cap was used.

## Current evidence

Only `fixture_checkpoint`, `adversarial_launcher`, `interrupt_SIGKILL` and `interrupt_SIGXCPU` are current test directories. Suffix `_first` directories preserve development evidence and are not the current gate. The manifest seals the corrected source, unchanged kernel, test source/results, current fixture state, adversarial state and compatibility report. Independent review must accept this correction before a root production-budget decision.
