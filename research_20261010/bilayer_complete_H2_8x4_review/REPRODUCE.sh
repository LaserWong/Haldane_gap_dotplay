#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import json,hashlib,shutil,tempfile,subprocess,resource,os
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='complete_H2_8x4_') as td:
 t=Path(td)
 for n in ('audit.py','build_independent_matrix.py','run_full.py','independent_residual','independent_residual.cpp','fixture4x4.json','benchmark.json'):shutil.copy2(p/n,t/n)
 shutil.copytree(p/'snapshot',t/'snapshot');shutil.copytree(p/'polarization',t/'polarization')
 subprocess.run(['python',str(t/'build_independent_matrix.py')],check=True)
 assert (t/'independent_matrix.cpp').read_bytes()==(p/'independent_matrix.cpp').read_bytes()
 def limits():
  os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(40,40));resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
 subprocess.run(['g++','-O3','-UNDEBUG',str(t/'independent_matrix.cpp'),'-o',str(t/'independent_matrix')],preexec_fn=limits,check=True,timeout=60)
 subprocess.run(['python',str(t/'run_full.py')],check=True)
 subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib','independent_run_resources'):x.pop(k)
 assert a==b
print('PASS sealed complete8x4 matrix with fresh rebuilt independent support pass')
PY
