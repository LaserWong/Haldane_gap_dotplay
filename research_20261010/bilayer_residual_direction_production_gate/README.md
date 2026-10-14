# Implementation and small tests of the q6 residual launcher

2026-10-10 21:27 EDT / 2026-10-11 01:27 UTC. Producer gate PASS. Independent review and explicit full-run authorization remain required. No 8×4 supports were evaluated in this stage. The earlier sealed fixture package is unchanged.

## Separate-sector normalization

`chunk_kernel.cpp` accepts exactly one q4 or q6 phase and one contiguous half-open range of lexicographically enumerated fixed-origin supports. It emits raw integer sums, range boundaries, total support count, processed counts, and partial=true. q4 and q6 sums are never combined in a raw chunk. All inherited scalar overflow assertions, coefficient bounds, generic cache behavior and GMP bilinears remain active. `BOUND_ERRATUM.md` in the preceding fixture package supplies the applicable conservative bounds.

`checkpoint.py assemble` first demands contiguous, nonoverlapping, complete coverage of BOTH phases. It sums integer values separately, multiplies every q4 component by N and checks divisibility by 4, and every q6 component by N and checks divisibility by 6. Only after those exact divisions does it add sector contributions. Thus all mixed H² contributions, including J(T,L), J(T,R), J(T,M) and self, receive the correct separate weights. No sample rescaling or rounded division is allowed.

The kernel returns the new G,H200,H200² row in order [vacuum,B,L,R,M,T], with H200=200Q+11A. The wrapper additionally extracts exact integer coupling-polynomial rows, using q(T)=6:

Arow=(H200row−1200Grow)/11,
A²row=(H200²row−1440000Grow−2200(6+q_j)Arow)/121.

Both divisions are checked. The polynomial convention is H(g)=Q+gA/2, so H²(g)=Q²+g(QA+AQ)/2+g²A²/4. This supplies all new rows. Accepted old 57×57 blocks still need merging after a successful authorized 8×4 pass. No optimization or spectral claim is included.

## Checkpoint safety

- State binds hashes of the wrapper source, kernel source, include files, executable, geometry and coefficient file, plus shape, dimensions, support totals, CPU budget, affinity and memory allowance.
- All bindings are rechecked before a chunk and again after it returns, before accepting output.
- One requested chunk is run per invocation. There is no automatic full-pass loop or authorization implied by a command-line flag.
- The wrapper holds an exclusive file lock. Every attempt is reserved and charged BEFORE launch. Timeout/failure/interruption never refunds it. An abandoned reserved entry is not coverage. A retry begins at the last successfully committed boundary and receives a new charge.
- State/output writes use temporary files, fsync, atomic rename and directory fsync. Completed output hashes are recorded. Uncommitted output after a crash cannot masquerade as coverage.
- Assembly first proves coverage, then reserves its CPU allowance before arithmetic. Its final row is hash-bound to state. A completed-row reread verifies that hash.
- Changing source, inputs or binary requires a new separately approved state. No silent resume migration exists. Do not recompile midway and then reuse a state whose executable hash changed.

## Resources and proposed production plan

Compilation is separate: CPU 3,512 MiB,40 CPU-second cap. The kernel allocates the same full 40.78 MB scalar cache and 6.04 MB family cache as the sampled fixture, populating scalar entries lazily for each chunk. The supervisor's address soft limit is 32 MiB and each child kernel's hard address limit is 68 MiB, totaling 100 MiB for the two active numerical processes. This tighter kernel allowance has passed 4×2 tests but has not been exercised on 8×4 in this stage. Earlier sample resident memory was about 47 MiB.

CLI supervisor invocations have 1 CPU-second soft limit with the default terminating SIGXCPU action. A chunk's requested cap includes this 1 second. Its child has a hard CPU cap of cap−1. Initialization and each assembly attempt charge 1 additional second. All caps remain charged regardless of actual use. An external supervisor imposing another tighter hard cap must still allow the requested child's cap.

If independently accepted and separately authorized for 360 CPU seconds total, the proposed schedule is:
- Two q4 chunks of at most 4096 supports, total-cap 6 each (child 5+supervisor 1):12 seconds charged.
- Forty-two q6 chunks of at most 4096 supports, total-cap 8 each (child 7+supervisor 1):336 seconds charged.
- Initialization 1 and successful assembly 1: total 350 charged, leaving 10 for at most one 8-second retry and one assembly retry.

This is a HARD BUDGET PLAN, not a guarantee of scientific completion. Linear sampling previously estimated 134–158 CPU seconds for an unchunked pass. Repeated lazy-cache rebuilds and support variability add uncertain cost. A chunk exceeding its cap fails visibly and retains its charge. No larger retry, alternate state, budget reset or production run is authorized here. A failure that makes remaining completion impossible needs a project decision.

## Tests and reproduction

`gate_tests.json` records the current final tests. Four 4×2 chunks (q4 ranges 0–17 and 17–35, and q6 ranges 0–10 and 10–21), with on-disk state reload between each, exactly reproduce all 22 new G,H200,H200² entries and scalar terms against the prior full 4^8 physical fixture. This exercises the fractional 8/6 normalization, not just integer scaling. Eleven deliberate rejection tests cover incomplete phase/assembly, duplicate coverage, changed source/binary, changed coefficients, output hash mismatch, reservation≠completion, completed-phase rerun, and charged failed attempts exhausting budget. Actual total child CPU is recorded. It is under 0.1 seconds for the final test. No full 4×4 or 8×4 computation is part of the gate.

To reproduce, copy the sealed package to a fresh review directory, compile `chunk_kernel.cpp -O2 -std=c++17 -lgmpxx -lgmp`, retain access to the two prior input packages, and run `test_gate.py` after selecting a new fixture checkpoint directory in a reviewer copy. The test refuses to overwrite existing state. The source/binary binding necessarily changes after independent recompilation, so old checkpoints must not be resumed with that new executable. Earlier development directories named `fixture_checkpoint_*` are historical attempts, not the final accepted checkpoint. Only `fixture_checkpoint` is current and included as evidence.

Next: independent gate review, then explicit project decision on 360 CPU/100 MiB. The project maintainer must not treat this implementation or its suggested commands as authorization to launch.
