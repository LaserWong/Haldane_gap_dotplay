# Read-only clarification of resource records

2026-10-11 01:58 UTC. No numerical computation was rerun to prepare this clarification. The original algebra manifest and every sealed file remain unchanged.

The 33.13448-second number is the exact saved floating-point difference

(after.ru_utime+after.ru_stime)−(before.ru_utime+before.ru_stime)

from resource.getrusage(resource.RUSAGE_CHILDREN), sampled immediately before and after the ONE subprocess.run in a fresh invocation of finish_ldl.py. It is reported child user+system CPU time, not elapsed wall time and not an un-subtracted lifetime total across the earlier producer invocation. The child program exact_ldl.cpp itself makes no fork/exec/subprocess calls. Raw before/after counters were not separately retained, so their absolute values cannot now be reconstructed. The discrepancy with the configured 25-second hard limit remains unexplained by the saved evidence.

The retained execution outcomes are listed below.
- Compilation returned exit0. No measured compiler CPU retained. Configured compiler CPU cap 5.
- The initial produce.py run returned exit1 after a TimeoutExpired exception from the first LDL subprocess. Its saved checkpoint reports 5.991080623 parent CPU seconds BEFORE the final input serialization/wait/error path.
- The initial LDL run had a 15-second wall timeout and a configured CPU hard cap of 10. Six complete JSON matrix records were flushed before the timeout. Its actual CPU and final child wait status were not retained. Python subprocess.run performs termination on timeout, but the saved evidence does not contain a direct child exit-code field, so no numerical signal code is claimed.
- finish_ldl.py returned exit0. Its child returncode==0 is explicitly asserted before the completed results/resource JSON are written. The remaining child reported 33.13448 CPU seconds despite configured hard cap 25. The finisher's own terminating soft CPU cap was 3. Its actual CPU was not retained.
- Subsequent serialization only read completed outputs and wrote the final result, summary and seals. It launched no LDL, optimization or physical computation.

The recorded CPU subtotal is 39.125560623 seconds (5.991080623+33.13448). It is a LOWER BOUND on the total attempted computation, since it excludes compiler CPU, the first LDL child, late producer CPU, finisher CPU and bookkeeping. There is no verified total CPU upper bound in the saved measurements, and therefore no verified statement that the requested 60 CPU-second total was respected. Summing nominal limits would not repair this. Enforcement is precisely what is in question, and the initial parent limit 45 was not an aggregate-child limit.

Scientific jobs were affined to CPU 3, and tool timestamps place their broad execution envelope between approximately 01:51:47 and 01:54:59 UTC. That is only a coarse wall-clock envelope. It does not provide a useful proof of the 60 CPU-second requirement and is not substituted for process accounting. No budget refund, reset, additional numerical work or resource expansion follows from this clarification.

The mathematical outputs remain separately reviewable. Six first-pass LDL jobs and three resumed jobs are fully recorded, along with exact rational witnesses and complete matrices. The supervising researcher was informed immediately after the anomalous resource report was read. Physical full-row review subsequently passed under its own separately authorized audit. This clarification does not change the status of that independent review or promote the endpoint optimization without its audit.
