#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import json,hashlib,shutil,tempfile,subprocess
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='short_bridge_review_') as td:
 t=Path(td)
 for name in ('audit.py','DEPENDENCIES.json'):shutil.copy2(p/name,t/name)
 shutil.copytree(p/'snapshot',t/'snapshot')
 subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib'):x.pop(k)
 assert a==b
print('PASS seal and fresh independent physical short-bridge replay')
PY
