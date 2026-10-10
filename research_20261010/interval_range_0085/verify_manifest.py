"""Check immutable handoff and all directly used external files."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent

def main():
 for name,digest in json.loads((HERE/'INPUT_SHA256.json').read_text()).items():
  assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('input changed',name)
 path=HERE/'FROZEN_MANIFEST.json'
 if path.exists():
  for name,digest in json.loads(path.read_text())['files'].items():
   assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,('frozen output changed',name)
 for row in json.loads((HERE/'INHERITED_REVIEWS.json').read_text()):
  folder=HERE.parent/row['folder'];manifest=folder/row['manifest'];assert hashlib.sha256(manifest.read_bytes()).hexdigest()==row['sha256']
  raw=json.loads(manifest.read_text());files=raw.get('files',raw);assert len(files)==row['file_count']
  for name,digest in files.items():assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest,('inherited file changed',row['folder'],name)
 print('PASS interval extension and inherited review manifests')
if __name__=='__main__':main()
