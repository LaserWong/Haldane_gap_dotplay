from pathlib import Path
import hashlib,json
out=Path(__file__).resolve().parent
m=json.loads((out/'INPUT_SHA256.json').read_text())
for p,h in m.items():assert hashlib.sha256((out/'snapshot'/p).read_bytes()).hexdigest()==h,p
print('PASS',len(m),'frozen input hashes')
