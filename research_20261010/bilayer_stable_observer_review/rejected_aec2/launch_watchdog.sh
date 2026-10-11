#!/bin/sh
# Sole proposed recipe. IDs must already be durably reserved by root.
set -eu
[ "$#" -eq 2 ]
case "$1:$2" in *[!0-9:]*|:*) exit 2;; esac
[ "$1" != "$2" ]
JOB=/workspace/shared/haldane_active/research_20261010/bilayer_full_m4_production_run_stable
NOW=$(/usr/bin/date -u +%s)
[ $((1791936000-NOW)) -ge 115205 ]
# Single-use markers prevent reuse even if Python never reaches its startup.
mkdir "$JOB/OUTER_LAUNCH_USED_$1"
mkdir "$JOB/WATCHDOG_LAUNCH_USED_$2"
export BILAYER_OUTER_RESERVATION_ID="$1" BILAYER_WATCHDOG_RESERVATION_ID="$2"
exec /usr/bin/taskset -c 6 /usr/bin/prlimit --cpu=100:100 --as=67108864:134217728 -- /usr/bin/timeout --signal=TERM --kill-after=5s 28800s /bin/sh /workspace/shared/haldane_active/research_20261010/bilayer_stable_observer_revision/launch.sh
