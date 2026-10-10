"""Verify frozen review bytes and optionally all live prerequisite review seals."""
import json,hashlib,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;R=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def check(base,entries):
 for n,h in entries.items():assert sha(base/n)==h,(str(base),n)
if (HERE/'MANIFEST_SHA256.json').exists():check(HERE,load(HERE/'MANIFEST_SHA256.json'))
check(HERE/'snapshot',load(HERE/'INPUT_SHA256.json'))
if '--live' in sys.argv:
 for name,rec in load(HERE/'PRIOR_REVIEW_SHA256.json').items():
  assert sha(R/name/'MANIFEST_SHA256.json')==rec['manifest_sha256'];check(R/name,rec['files'])
 for name in ['low_band/combined_ground_bounds/FROZEN_MANIFEST_1906.json','low_band/ground_moment_pencil/ENDPOINT_MANIFEST_SHA256.json','variational_numerator_filter/FROZEN_MANIFEST.json']:
  path=R/name;assert sha(path)==sha(HERE/'snapshot/research_20261010'/name);d=load(path);check(path.parent,d.get('files',d))
print('PASS all requested immutable seals')
