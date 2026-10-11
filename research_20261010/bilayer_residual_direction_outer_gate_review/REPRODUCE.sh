#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
/usr/bin/python3 verify.py
if [ -f MANIFEST_SHA256.json ]; then /usr/bin/python3 - <<'PY'
import hashlib,json
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
PY
fi
check=$(mktemp -d "$PWD/check.XXXXXX")
cp checkpoint.py outer_driver.cpp chunk_kernel.cpp base_kernel.inc init_kernel.inc fixture_coefficients.txt interrupt_probe.cpp independent.py "$check/"
for item in kernel driver probe; do
 case "$item" in kernel) source=chunk_kernel; libs='-lgmpxx -lgmp';; driver) source=outer_driver; libs='';; probe) source=interrupt_probe; libs='';; esac
 /usr/bin/python3 measure.py "$check/compile_$item.json" 512 40 g++ -O2 -std=c++17 "$check/$source.cpp" $libs -o "$check/$source"
done
export RESEARCH_ROOT="$(dirname "$PWD")"
/usr/bin/python3 measure.py "$check/runtime.json" 100 30 /usr/bin/python3 "$check/independent.py"
cmp result.json "$check/result.json"
echo 'PASS clean sole-path outer gate replay'
