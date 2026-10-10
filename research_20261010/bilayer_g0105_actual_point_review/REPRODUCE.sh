#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY2'
from pathlib import Path
import hashlib,json,shutil,tempfile,subprocess
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items(): assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='actual_g0105_') as td:
 t=Path(td)
 for n in ('audit.py','budget_math.py','physical_library.py','independent_point_math.py','INPUT_SHA256.json','PROVENANCE.json'):shutil.copy2(p/n,t/n)
 shutil.copytree(p/'snapshot',t/'snapshot')
 subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib'):x.pop(k)
 assert a==b
print('PASS sealed actual point and clean independent replay')
PY2
