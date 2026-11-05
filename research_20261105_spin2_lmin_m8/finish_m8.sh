#!/usr/bin/env bash
set -euo pipefail
cd /workspace/runs/spin2_lmin
CERT=cert
STATUS=finish_m8.status
echo "waiting $(date -Iseconds)" > "$STATUS"
need=(P_L8_sz3_q5 P_L8_sz3_q7 P_L8_sz4_q2 P_L8_sz4_q4 P_L8_sz4_q6 P_L8_sz4_q8)
while true; do
  miss=0
  for k in "${need[@]}"; do
    [[ -f "$CERT/enc/${k}.json" ]] || miss=$((miss+1))
  done
  # also require full 162
  n=$(ls "$CERT/enc/"*_L8_*.json 2>/dev/null | wc -l)
  echo "miss_tail=$miss L8_enc=$n $(date -Iseconds)" >> "$STATUS"
  if [[ $miss -eq 0 && $n -ge 162 ]]; then break; fi
  # relaunch any dead missing
  for k in "${need[@]}"; do
    f="$CERT/enc/${k}.json"
    [[ -f "$f" ]] && continue
    tw=${k%%_*}; rest=${k#*_}; L=${rest:1:1}; # fragile; use python
  done
  python3 - <<'PY'
import subprocess
from pathlib import Path
miss=['P_L8_sz3_q5','P_L8_sz3_q7','P_L8_sz4_q2','P_L8_sz4_q4','P_L8_sz4_q6','P_L8_sz4_q8']
D=Path('cert')
for key in miss:
  if (D/'enc'/f'{key}.json').exists():
    continue
  parts=key.split('_'); tw=parts[0]; L=int(parts[1][1:]); sz=int(parts[2][2:]); q=int(parts[3][1:])
  r=subprocess.run(['pgrep','-af',f'run2.py one {tw} {L} {sz} {q}'],capture_output=True,text=True)
  if any('run2.py one' in ln for ln in r.stdout.splitlines()):
    continue
  log=open(D/'run_L8.log','a')
  subprocess.Popen(['/usr/bin/python3','-u',str(D/'run2.py'),'one',tw,str(L),str(sz),str(q)],
                   cwd=str(D), stdout=log, stderr=log, start_new_session=True)
  print('relaunched',key, flush=True)
PY
  sleep 30
done
echo "L8 complete $(date -Iseconds)" >> "$STATUS"
cd cert
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /usr/bin/python3 -u assemble2.py 8 > assemble_L8.log 2>&1
echo "assembled $(date -Iseconds)" >> ../"$STATUS"
cd ..
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /usr/bin/python3 -u fit_cert.py > fit_cert.log 2>&1
echo "fit $(date -Iseconds)" >> "$STATUS"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /usr/bin/python3 -u check_cert.py > check_cert.log 2>&1
echo "check $(date -Iseconds) exit=$?" >> "$STATUS"
python3 - <<'PY' >> "$STATUS"
import json
from pathlib import Path
enc=json.loads(Path('cert/enclosures.json').read_text())
print('enclosure_keys',sorted(enc))
for k in ['Z8','P8']:
  if k in enc: print(k,'rel_radius',enc[k]['rel_radius'],'modes',enc[k]['blocks_by_mode'],'mom',enc[k]['moments_contain_exact'])
if Path('check_cert_result.json').exists():
  r=json.loads(Path('check_cert_result.json').read_text())
  print('accepted',r.get('accepted'),'S',r.get('S'))
PY
echo DONE >> "$STATUS"
