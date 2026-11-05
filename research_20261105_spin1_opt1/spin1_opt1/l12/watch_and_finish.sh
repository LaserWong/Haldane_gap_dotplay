#!/bin/bash
cd "$(dirname "$0")"
LOG=logs/watch.log
echo "[$(date -Is)] watch start; waiting for prior xargs/jobs" | tee -a "$LOG"
# Wait until no job.sh / chunked.py / xargs for this dir
while pgrep -af 'spin1_opt1/l12.*(job\.sh|chunked\.py|xargs)' >/dev/null 2>&1 || pgrep -af './job.sh' >/dev/null 2>&1; do
  # more precise: count our job.sh
  n=$(pgrep -af '/workspace/haldane_chat_bundle/runs/spin1_opt1/l12/job.sh|/workspace/haldane_chat_bundle/runs/spin1_opt1/l12/chunked.py|xargs -P 3 -n 1 \./job.sh' 2>/dev/null | grep -v watch_and_finish | grep -v resume_all | wc -l)
  # fallback simpler
  if ! pgrep -f 'chunked.py' >/dev/null 2>&1 && ! pgrep -f 'xargs -P .* ./job.sh' >/dev/null 2>&1; then
    # check for stray job.sh in our dir
    if ! pgrep -f 'spin1_opt1/l12/job.sh' >/dev/null 2>&1; then
      break
    fi
  fi
  done_n=$(ls enc/*.json 2>/dev/null | wc -l)
  echo "[$(date -Is)] waiting... enc=$done_n/54 chunked=$(pgrep -c -f chunked.py || true)" >> "$LOG"
  sleep 30
done
echo "[$(date -Is)] prior jobs quiet; launching resume_all" | tee -a "$LOG"
# retry loop until 54 or 3 consecutive no-progress rounds
prev=-1; stall=0
for round in 1 2 3 4 5 6 7 8; do
  done_n=$(ls enc/*.json 2>/dev/null | wc -l)
  echo "[$(date -Is)] round $round enc=$done_n/54" | tee -a "$LOG"
  [ "$done_n" -ge 54 ] && break
  if [ "$done_n" -eq "$prev" ]; then stall=$((stall+1)); else stall=0; fi
  prev=$done_n
  [ "$stall" -ge 3 ] && { echo "STALLED" | tee -a "$LOG"; break; }
  ./resume_all.sh 3 >> logs/resume_all.log 2>&1
done
done_n=$(ls enc/*.json 2>/dev/null | wc -l)
echo "[$(date -Is)] final enc=$done_n/54" | tee -a "$LOG"
if [ "$done_n" -ge 54 ]; then
  echo "assembling..." | tee -a "$LOG"
  cd /workspace/haldane_chat_bundle/runs/spin1_opt1
  timeout 120 python3 assemble12.py 12 > l12/logs/assemble12.log 2>&1
  echo "assemble rc=$?" | tee -a l12/logs/watch.log
fi
