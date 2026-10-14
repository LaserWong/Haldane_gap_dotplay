# Bounded native-memory test

The 64-q6 target batch completed under a 128 MiB native address-space limit and reproduced all 24 aggregate fields exactly.
The test used CPU 6 and did not construct the full support or cache.
Its authorized 8 CPU seconds were charged in full, giving 8/8 used.
The native process used .511223 CPU seconds as measured by wait4.
The sampled maximum VmPeak and VmSize were 38,637,568 bytes, and sampled native RSS was 20,398,080 bytes.
These samples do not certify VmPeak at final exit.
Successful execution under the hard address-space limit does establish that this batch fits within 128 MiB.

The observer's VmPeak of 38,637,568 bytes explains why the earlier 32 MiB limit was insufficient.
The observer and outer process each had a 64 MiB soft address-space limit, while the native process had 128 MiB.
Their combined limits were 256 MiB while the native process was active.
The hard limits allowed children to set their authorized larger soft limits.
The sampled resident peak across the outer process, observer, and native process was 42,930,176 bytes, with an external 256 MiB guard.
Tree-wide wait4 CPU time was .627859 seconds, outer-process CPU time was .101444 seconds, and elapsed time was .666316 seconds.

A planned MemoryError test killed and reaped a known sleeping child through its fixed PID and wait4, without enumerating /proc again.
That child's .000216 CPU seconds were included in the three-second observer reservation, consisting of two seconds for the observer and one for the fault test.
This verifies the limited fallback path, rather than the complete production supervisor.

The proposed next test repeats the four-singleton, two-session integration with limits of 64 MiB for the supervisor, 64 MiB for the controller, and 128 MiB for the native process.
It retains the cleanup fallback for known PIDs and process groups.
The outer observer must remain within the 256 MiB aggregate resident limit.
Its additional virtual address space requires separate accounting for virtual limits and total resident memory.
This proposal grants no retry or production-run authority.
The earlier failed 30-second integration remains fully charged.
