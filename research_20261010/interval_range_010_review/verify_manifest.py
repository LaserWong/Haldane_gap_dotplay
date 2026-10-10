from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
r=json.loads((H/'MANIFEST_SHA256.json').read_text())
for p,d in r.items():assert hashlib.sha256((H/p).read_bytes()).hexdigest()==d,p
print('PASS immutable review manifest',len(r),'files')
