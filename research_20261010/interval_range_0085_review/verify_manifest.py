#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
for rel,h in json.loads((p/'MANIFEST_SHA256.json').read_text()).items():
    assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==h,rel
print('PASS sealed independent review manifest')
