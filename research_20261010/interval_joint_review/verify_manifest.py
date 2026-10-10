#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
m=json.loads((H/'MANIFEST_SHA256.json').read_text())
for rel,expected in m.items():
    got=hashlib.sha256((H/rel).read_bytes()).hexdigest()
    if got!=expected:raise SystemExit('SHA256 mismatch: '+rel)
print('PASS finished independent review manifest:',len(m),'files')
