# A persistent driver with a whole-campaign resource bound

2026-10-10 21:38 EDT / 2026-10-11 01:38 UTC. The producer's small tests passed. Independent review and explicit launch approval remained pending. No 8×4 support computation or full run occurred. The earlier fixture, production checks, and parent-death correction remain unchanged.

## Fixed launch sequence and CPU budget

`outer_driver` is the only proposed production entry point. Its `production_authorized` argument is a mode name, not permission. Launch only after explicit root authorization of this exact gate. It creates a new campaign directory and refuses any existing directory. It never retries, restarts, resumes, repairs a failed invocation, or issues an extra read/assembly command. Any failed child invocation stops the entire campaign. A killed driver leaves its existing directory, so automatic restart is rejected.

The one fixed 8×4 plan contains 46 invocations, allocated as follows.
- Initialization: 1 supervisor CPU second.
- Two q4 chunks, each at most 4096 supports: 6 CPU seconds each, including supervisor 1 and kernel 5.
- Forty-two q6 chunks, each at most 4096 supports: 8 CPU seconds each, including supervisor 1 and kernel 7.
- Assembly: 1 supervisor CPU second.

These reserve 350 seconds. The persistent C++ driver reserves 10 more for all its own work, including planning, hashing-independent coordination, ledger writes, wait/reaping, failed/preflight handling and bookkeeping. Total whole-campaign allowance is 360 CPU seconds. There is no unallocated retry allowance in this sole-path design. Independent compilation and review/fixture tests are separate, explicitly scoped tasks and do not count as a production campaign. They must not silently consume or enlarge its budget.

Every CLI call is durably precharged to `outer_ledger.jsonl` before fork, regardless of outcome. Lock failures, preflight rejection and interpreter/exec failure therefore remain charged. The driver issues no additional CLI calls after failure, nor any post-completion reread. If somebody manually invokes the inner wrapper or a second driver, that is outside this sole authorized path and is not covered by this campaign claim. The parent must not do so without a new budget decision.

The driver's terminating CPU soft limit is 10 seconds. Each supervisor's 1-second terminating soft limit is installed before Python exec, so interpreter startup and preflight work are covered. SIGXCPU is explicitly restored to its terminating default before any launches. Scientific kernels retain their hard 5/7-second caps. Larger inherited hard ceilings exist solely so a child can set its own smaller effective limit. No code raises the driver's or supervisor's effective soft limit. Each invocation is accounted at its whole reserved cap, never refunded based on observed time.

## A 100 MiB address-space budget

Effective address-space limits are 8 MiB driver +32 MiB system-Python supervisor +60 MiB scientific kernel =100 MiB. The driver has no subprocess other than the one supervisor. That supervisor has only one single-process numerical kernel. No shell, grandchildren of the kernel, worker pool or simultaneous support jobs are created.

The scientific kernel is byte-identical to the reviewed gate. Its stricter 60 MiB allowance is a safety limit, not an observed 8×4 measurement in this stage. The earlier 8×4 sample measured approximately 47 MiB resident memory. If its address space does not fit 60 MiB, the invocation fails and the driver stops. Do not expand memory or switch to another launch route automatically.

`/usr/bin/python3` is pinned. Its resolved path, version and SHA256 are in `interpreter_identity.json`. The interpreter digest is included in each checkpoint's source binding, together with the outer executable/source, inner wrapper, exact kernel, include files, geometry and coefficients. The wrapper rejects a different interpreter path. Streamed 16 KiB hashing avoids whole-file temporary allocations under 32 MiB. The larger default Codex Python is not the supported production interpreter.

## Death propagation and campaign ownership

Before supervisor exec, the driver installs PR_SET_PDEATHSIG(SIGKILL) plus a parent-PID race check. The inner launcher independently does the same for its kernel. Driver death therefore kills the supervisor, which kills the numerical kernel. The driver's campaign flock is inherited by the supervisor and explicitly passed onward to the kernel. The kernel also retains the inner checkpoint flock. The wrapper validates the inherited outer descriptor against the campaign lock's device/inode before passing it. Campaign ownership remains held until the full active chain exits, including signal-delivery races.

State/range hashing, charged interrupted attempts, exact completeness and separate q4/q6 normalization are unchanged from the reviewed launcher correction. A scientifically complete checkpoint still requires both full support ranges and exact N/4,N/6 divisions before sector addition. No partial row can be assembled as complete.

## Small tests

`fixture_campaign` runs the actual persistent driver, pinned interpreter and real kernel through six calls on 4×2. Four chunks use q4 ranges 0–17 and 17–35, q6 ranges 0–10 and 10–21. Every normalized G,H200,H200² entry equals the independently verified full physical fixture. This tests the real source/interpreter binding and 32+60 MiB child split, not an imported wrapper bypass.

`test_outer.py` additionally verifies the following behavior.
- A deliberately invalid coefficient file causes the first init invocation to fail. Its entire 1-second call remains charged and no later call starts.
- Killing the driver while a bounded test-only delay probe runs causes both supervisor and kernel-process death.
- The active kernel actually holds the outer campaign lock inode.
- A restart against the killed campaign is rejected without changing its ledger. Interrupted inner reservations remain charged.

The delay probe is a single-process test artifact copied from the previous correction. It is not the production scientific kernel. Test source and the resulting output/ledgers are sealed. `outer_tests.json` records the current final results. Directories with suffixes such as `_first` or `_pre_*` are preserved development runs, not the current evidence.

## Reproduction and pending action

Compile `outer_driver.cpp` separately with g++ -O2 -std=c++17 under the existing 512-MiB/40-CPU-second compiler cap. Recompiling changes the executable binding, so tests must use a fresh campaign. A small replay uses the following command.

outer_driver fixture PACKAGE_ABSOLUTE_PATH new_FIXTURE_DIRECTORY GEOMETRY_4X2_ABSOLUTE_PATH FIXTURE_COEFFICIENTS_ABSOLUTE_PATH

The proposed production invocation has the identical shape, but mode `production_authorized`, the reviewed 8×4 geometry and the saved .11 coefficients. Production execution is not yet authorized. First obtain independent acceptance of this outer gate and root approval of one 360-CPU-second/100-MiB campaign. On any failure, stop and report its charged ledger, completed ranges and blocker. No automatic restart or extra resources are permitted.
