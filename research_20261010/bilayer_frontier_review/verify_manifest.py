from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
entries=json.loads((p/'MANIFEST_SHA256.json').read_text())
for name,h in entries.items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
print('PASS',len(entries),'sealed review files')
