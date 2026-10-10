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
 print('PASS interval extension manifests')
if __name__=='__main__':main()
