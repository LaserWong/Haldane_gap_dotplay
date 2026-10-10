#!/usr/bin/env python3
import sys; sys.dont_write_bytecode=True
from common import *
p=HERE/'MANIFEST_SHA256.json'
if not p.exists():raise SystemExit('Not frozen: MANIFEST_SHA256.json is absent')
d=json.loads(p.read_text())
for name,h in d.items():assert sha(HERE/name)==h,name
print(f'PASS: {len(d)} frozen stage14 files match SHA-256.')
