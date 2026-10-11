#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python - <<'PY'
from pathlib import Path
import hashlib,json,shutil,tempfile,subprocess
p=Path.cwd()
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
with tempfile.TemporaryDirectory(prefix='split21_fixture_') as td:
 t=Path(td)
 for n in ('audit.py','build_split.py','run_fixture.py'):shutil.copy2(p/n,t/n)
 shutil.copytree(p/'snapshot',t/'snapshot');subprocess.run(['python',str(t/'build_split.py')],check=True);assert (t/'independent_split.cpp').read_bytes()==(p/'independent_split.cpp').read_bytes()
 subprocess.run(['python',str(t/'run_fixture.py')],check=True);subprocess.run(['python',str(t/'audit.py')],check=True)
 a=json.loads((p/'audit.json').read_text());b=json.loads((t/'audit.json').read_text())
 for x in (a,b):
  for k in ('seconds','peak_rss_kib'):x.pop(k)
 assert a==b
print('PASS21D split fixture fresh independent rebuilt physical replay')
PY
