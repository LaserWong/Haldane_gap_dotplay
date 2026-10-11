# Revised memory profile and bounded cleanup

Source-only freeze before the separately authorized30-second integration retry. Prior receipt overlay bb79db2442c9f34cb9cdd877551fda639bb0328602a2b1a25884d0e19b1f6a8c remains immutable.

Changes: physical worker hard AS128 MiB; production supervisor soft AS64 MiB, controller64 MiB, native128 MiB (sum256). Controller hard AS128 permits authorized native128 soft/hard after fork. Combined RSS guard remains256 MiB. Test outer watchdog is an additional process, included in256 MiB aggregate RSS but not the three-process virtual partition.

Supervisor accounting exceptions use a constant reason. Orphan cleanup no longer allocates a fresh /proc inventory: known PIDs/groups are killed, subreaper wait4 reaps all children, and fixed-PID kill(0) checks known survivors. Unobserved workers have parent-death signals. Fail-closed accounting remains in normal polling. This is a targeted fallback, not proof that all Python operations can succeed under arbitrary process-wide allocation failure.

Memory-profile prerequisite bbdd4d9ff02de958dd7e1944d5b0505fce5e88b8b697643e1be0927356e3fc9d reproduced all24 accepted64-q6 fields under AS128. Original failed30 gate remains charged. No production launch or complete production acceptance is authorized.
