#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import hashlib,json,shutil,tempfile,subprocess,os,resource
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='full57_split_review_') as td:
 t=Path(td)
 for n in ('audit.py','run.py','independent_split.cpp'):shutil.copy2(p/n,t/n)
 shutil.copytree(p/'snapshot',t/'snapshot')
 def compile_limits():
  os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(40,40));resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
 subprocess.run(['g++','-O3','-UNDEBUG',str(t/'independent_split.cpp'),'-o',str(t/'independent_split')],preexec_fn=compile_limits,check=True,timeout=55)
 subprocess.run(['python',str(t/'run.py')],check=True);subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib','run_resources'):x.pop(k)
 assert a==b
print('PASS complete57D split matrix fresh independent physical replay')
PY
