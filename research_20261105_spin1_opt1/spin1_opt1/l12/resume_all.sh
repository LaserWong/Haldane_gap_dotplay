#!/bin/bash
# Resume exact_chunked re-cert of the 54 float L=12 blocks. Skips enc/*.json already present.
# Safe to re-run. Parallelism P (default 3) for ~16GB box with m~6k complex eigensolves.
set -u
cd "$(dirname "$0")"
P=${1:-3}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p logs enc work
need=()
while read -r K; do
  [ -f "enc/$K.json" ] || need+=("$K")
done < blocks.txt
echo "[$(date -Is)] resume_all: ${#need[@]} blocks remaining, P=$P" | tee -a logs/resume_all.log
if [ ${#need[@]} -eq 0 ]; then echo "nothing to do"; exit 0; fi
printf '%s\n' "${need[@]}" | xargs -P "$P" -n 1 ./job.sh
# report
done_n=$(ls enc/*.json 2>/dev/null | wc -l)
fail=()
while read -r K; do [ -f "enc/$K.json" ] || fail+=("$K"); done < blocks.txt
echo "[$(date -Is)] resume_all done: enc=$done_n/54 fail=${#fail[@]}: ${fail[*]-}" | tee -a logs/resume_all.log
[ ${#fail[@]} -eq 0 ]
