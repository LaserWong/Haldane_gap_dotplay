from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check_hashes():
 for p,h in json.loads((HERE/'INPUT_SHA256.json').read_text()).items():assert sha(HERE/'snapshot'/p)==h,p
 for name,rec in json.loads((HERE/'PRIOR_REVIEW_SHA256.json').read_text()).items():
  prior=ROOT/name;assert sha(prior/'MANIFEST_SHA256.json')==rec['manifest_sha256'],name
  for p,h in rec['files'].items():assert sha(prior/p)==h,(name,p)
 freeze=json.loads((HERE/'PRODUCER_FREEZE.json').read_text());m=HERE/'snapshot'/freeze['path'];assert sha(m)==freeze['sha256']
 for p,h in freeze['files'].items():assert sha(m.parent/p)==h,p
 print('PASS frozen inputs and prior independent seals',flush=True)
if __name__=='__main__':check_hashes()
