#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
/usr/bin/python3 verify.py
if [ -f MANIFEST_SHA256.json ]; then /usr/bin/python3 - <<'PY'
import json,hashlib
for f,h in json.load(open('MANIFEST_SHA256.json')).items():assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
PY
fi
check=$(mktemp -d "$PWD/check.XXXXXX")
cp checkpoint.py chunk_kernel.cpp base_kernel.inc init_kernel.inc fixture_coefficients.txt independent.py independent_interrupt.py interrupt_probe.cpp "$check/"
/usr/bin/python3 measure.py "$check/compile.json" 512 40 g++ -O2 -std=c++17 "$check/chunk_kernel.cpp" -lgmpxx -lgmp -o "$check/chunk_kernel"
/usr/bin/python3 measure.py "$check/probe_compile.json" 512 20 g++ -O2 -std=c++17 "$check/interrupt_probe.cpp" -o "$check/interrupt_probe"
export RESEARCH_ROOT="$(dirname "$PWD")"
/usr/bin/python3 measure.py "$check/runtime.json" 100 30 /usr/bin/python3 "$check/independent.py"
/usr/bin/python3 measure.py "$check/interrupt_runtime.json" 100 30 /usr/bin/python3 "$check/independent_interrupt.py"
/usr/bin/python3 - "$check" <<'PY'
import json,sys
from pathlib import Path
c=Path(sys.argv[1])
for f in ['result.json','interrupt_result.json']:
 a=json.load(open(f));b=json.load(open(c/f))
 a.pop('observed_kernel_cpu_seconds',None);b.pop('observed_kernel_cpu_seconds',None)
 assert a==b,f
print('PASS corrected gate clean replay')
PY
