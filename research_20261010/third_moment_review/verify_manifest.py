from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
m=json.loads((P/'MANIFEST_SHA256.json').read_text())
for name,h in m.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
print('PASS review manifest',len(m),'files')
