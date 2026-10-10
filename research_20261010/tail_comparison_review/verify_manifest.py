from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
for name,h in json.loads((HERE/'MANIFEST_SHA256.json').read_text()).items():
 assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
print('REVIEW MANIFEST PASS')
