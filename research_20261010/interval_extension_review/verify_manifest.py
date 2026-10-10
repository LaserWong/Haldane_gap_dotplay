#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST_SHA256.json').read_text())
for rel,h in m.items():assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==h,rel
print('PASS',len(m),'sealed review files')
