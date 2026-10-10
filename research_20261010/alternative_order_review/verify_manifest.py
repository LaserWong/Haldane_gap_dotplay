from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'MANIFEST_SHA256.json').read_text())
for name,h in m.items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
print('PASS',len(m),'sealed alternative-order review files')
