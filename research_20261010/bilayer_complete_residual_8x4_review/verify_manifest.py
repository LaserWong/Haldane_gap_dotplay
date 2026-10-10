from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
for f,h in json.loads((R/'MANIFEST_SHA256.json').read_text())['files'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
print('Review manifest intact')
