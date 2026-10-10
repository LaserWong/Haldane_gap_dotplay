from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for rel,digest in manifest.items():
 p=root/rel
 assert p.is_file(),f'Missing: {rel}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,f'Changed: {rel}'
print(f'PASS: {len(manifest)} file hashes')
