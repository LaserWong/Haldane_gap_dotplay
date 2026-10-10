#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import hashlib,json,shutil,tempfile,subprocess,os,resource
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='independent_bilayer_physical_') as td:
 t=Path(td)
 for name in ('audit.py','run_independent.py','independent_residual.cpp','independent_residual','INPUT_SHA256.json','ENGINE_PROVENANCE.json'):shutil.copy2(p/name,t/name)
 shutil.copytree(p/'snapshot',t/'snapshot')
 def caps():
  os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 subprocess.run(['g++','-std=c++17','-O3','-UNDEBUG',str(t/'independent_residual.cpp'),'-lgmpxx','-lgmp','-o',str(t/'rebuilt_engine')],check=True,preexec_fn=caps,timeout=55)
 subprocess.run(['python',str(t/'run_independent.py'),str(t/'rebuilt_engine')],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['python',str(t/'audit.py')],check=True,stdout=subprocess.DEVNULL)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in(a,b):
  for k in('independent_contraction','assembly_seconds','assembly_peak_rss_kib'):x.pop(k)
 assert a==b
print('PASS seals, independently rebuilt checker, full support replay and assembly')
PY
