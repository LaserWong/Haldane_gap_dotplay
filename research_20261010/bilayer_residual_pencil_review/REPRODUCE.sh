#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='residual_pencil_fixture_') as td:
 t=Path(td)
 for n in ('audit.py','polarize.py','independent_residual','independent_residual.cpp'):shutil.copy2(p/n,t/n)
 shutil.copytree(p/'snapshot',t/'snapshot');(t/'polarization').mkdir()
 subprocess.run(['python',str(t/'polarize.py')],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib','independent_run_resources'):x.pop(k)
 assert a==b
print('PASS sealed complete4x4 fixture and15 fresh independent support polarizations')
PY
