# Memory limits and bounded cleanup

This source revision was frozen before the separately authorized 30-second integration retry. Receipt overlay `bb79db2442c9f34cb9cdd877551fda639bb0328602a2b1a25884d0e19b1f6a8c` remains unchanged.

The physical worker has a hard address-space limit of 128 MiB. The production supervisor, controller, and native worker have soft limits of 64, 64, and 128 MiB, respectively, for a total of 256 MiB. The controller's hard limit of 128 MiB permits the authorized native worker's 128 MiB soft and hard limits after fork. Combined RSS remains limited to 256 MiB. The additional test watchdog counts toward aggregate RSS, but is outside the three-process virtual-address partition.

Accounting exceptions in the supervisor now use a constant reason string. Orphan cleanup kills known PIDs and process groups without allocating a new `/proc` inventory. The subreaper uses `wait4` to reap children and fixed-PID `kill(0)` checks to identify surviving known processes. Unobserved workers have parent-death signals. Normal polling still fails closed when accounting is unavailable. This fallback does not guarantee that every Python operation can survive arbitrary process-wide allocation failure.

Memory-profile prerequisite `bbdd4d9ff02de958dd7e1944d5b0505fce5e88b8b697643e1be0927356e3fc9d` reproduced all 24 accepted 64-q6 fields under a 128 MiB address-space limit. The failed original 30-second test remains charged. This source revision authorizes neither production execution nor acceptance of a complete production run.
