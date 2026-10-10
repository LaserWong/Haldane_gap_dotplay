"""Create an immutable review snapshot and check its sealed provenance."""
from pathlib import Path
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SRC=ROOT/'low_band/tail_comparison';DEST=HERE/'snapshot'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
prior={}
for name in ['large_seed_review','temple_variant_review','alternative_order_review','bosonic_tail_review','quadratic_boson_review']:
 p=ROOT/name;m=load(p/'MANIFEST_SHA256.json')
 for k,h in m.items():assert sha(p/k)==h,(name,k)
 for k,h in load(p/'INPUT_SHA256.json').items():assert sha(p/'snapshot'/k)==h,(name,k)
 prior[name]=dict(manifest_sha256=sha(p/'MANIFEST_SHA256.json'),files=m)
print('All five sealed prior reviews and frozen inputs verified')
files={p for p in SRC.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
for variant in ['original','jacobi','quadratic']:
 assert (SRC/variant/'summary.json').exists()
 for p in (SRC/variant).glob('temple_*.json'):
  for name,h in load(p)['source_sha256'].items():
   q=ROOT/name;assert sha(q)==h;files.add(q)
 # Already frozen physical, Fourier and tail bytes must match the sealed audit.
 for p in (SRC/variant).glob('temple_*.json'):
  for name,h in load(p)['source_sha256'].items():
   base=Path(name).name
   if 'frontier_g006/' in name:review='alternative_order_review';key=base
   elif 'large_seed_moments/' in name or 'translation_band/' in name:review='large_seed_review';key='research_20261010/'+name
   elif 'bosonic_tail/' in name:review='bosonic_tail_review';key=base
   elif 'quadratic_boson/' in name:review='quadratic_boson_review';key=base
   else:raise AssertionError(name)
   assert load(ROOT/review/'INPUT_SHA256.json')[key]==h,(review,key)
short=ROOT/'low_band/frontier_g006/all_size_bridges.json';files.add(short)
assert sha(short)==load(ROOT/'alternative_order_review/INPUT_SHA256.json')['all_size_bridges.json']
for side in range(2,8):
 p=ROOT/f'low_band/frontier_g006/small_sizes/number_bins_{side}x{side}_g3d50.json';files.add(p)
 assert sha(p)==load(ROOT/'alternative_order_review/INPUT_SHA256.json')[f'small_sizes/{p.name}']
manifest={}
for p in sorted(files):
 name=str(p.relative_to(ROOT));q=DEST/name;q.parent.mkdir(parents=True,exist_ok=True)
 data=p.read_bytes();h=hashlib.sha256(data).hexdigest()
 if q.exists():assert sha(q)==h,('Snapshot exists with different bytes',name)
 else:q.write_bytes(data)
 assert sha(p)==h and sha(q)==h;manifest[name]=h
(HERE/'INPUT_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
(HERE/'PRIOR_REVIEW_SHA256.json').write_text(json.dumps(prior,indent=2)+'\n')
print('Snapshot inputs',len(manifest),'bytes',sum((DEST/k).stat().st_size for k in manifest))
