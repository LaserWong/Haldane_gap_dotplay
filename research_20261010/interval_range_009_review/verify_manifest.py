from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent
r=json.loads((O/'MANIFEST_SHA256.json').read_text())
for f,h in r.items():assert hashlib.sha256((O/f).read_bytes()).hexdigest()==h,f
print('PASS immutable review manifest',len(r),'files')
