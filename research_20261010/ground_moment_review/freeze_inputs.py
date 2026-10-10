"""Freeze producer bytes only after its manifest is finalized; seal dependencies."""
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SRC=ROOT/'low_band/ground_moment_pencil';DEST=HERE/'snapshot'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
assert len(sys.argv)==3,'manifest basename and expected SHA-256 required'
manifest=SRC/sys.argv[1];assert sha(manifest)==sys.argv[2]
prior={}
for name in ['large_seed_review','alternative_order_review','tail_comparison_review','quadratic_boson_review','bilayer_frontier_review']:
 p=ROOT/name;m=load(p/'MANIFEST_SHA256.json')
 for k,h in m.items():assert sha(p/k)==h,(name,k)
 for k,h in load(p/'INPUT_SHA256.json').items():assert sha(p/'snapshot'/k)==h,(name,k)
 prior[name]=dict(manifest_sha256=sha(p/'MANIFEST_SHA256.json'),files=m)
print('PASS all prior review seals',flush=True)
manifest_files=load(manifest);manifest_files=manifest_files.get('files',manifest_files)
files={manifest}
for name,h in manifest_files.items():
 p=SRC/name;assert sha(p)==h,(name,'producer manifest');files.add(p)
external={}
for p in sorted(files):
 if p.suffix=='.json' and (p.name.startswith('ground_') and p.name!='ground_summary.json' or p.name.startswith('scalar_') and p.name!='scalar_summary.json'):
  for name,h in load(p)['source_sha256'].items():
   q=ROOT/name;assert sha(q)==h,(name,'new source map');files.add(q);external[name]=h
for name,h in list(external.items()):
 if name.startswith('low_band/ground_moment_pencil/'):continue
 review='bilayer_frontier_review' if 'frontier_g007_g010/' in name else 'tail_comparison_review'
 sealed=load(ROOT/review/'INPUT_SHA256.json');assert sealed[name]==h,(review,name,'previously accepted input')
 if Path(name).name.startswith('temple_'):
  for nested,hh in load(ROOT/name)['source_sha256'].items():
   q=ROOT/nested;assert sha(q)==hh and sealed[nested]==hh;files.add(q)
for side in range(2,8):
 name=f'low_band/frontier_g006/small_sizes/number_bins_{side}x{side}_g3d50.json'
 p=ROOT/name;assert sha(p)==load(ROOT/'tail_comparison_review/INPUT_SHA256.json')[name];files.add(p)
name='low_band/frontier_g007_g010/short_sizes/quadratic_bins_7x7_g1d10.json'
p=ROOT/name;assert sha(p)==load(ROOT/'bilayer_frontier_review/INPUT_SHA256.json')[name];files.add(p)
inputs={}
for p in sorted(files):
 name=str(p.relative_to(ROOT));q=DEST/name;q.parent.mkdir(parents=True,exist_ok=True)
 data=p.read_bytes();h=hashlib.sha256(data).hexdigest()
 if q.exists():assert sha(q)==h,('Existing snapshot differs',name)
 else:q.write_bytes(data)
 assert sha(p)==h and sha(q)==h;inputs[name]=h
(HERE/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
(HERE/'PRIOR_REVIEW_SHA256.json').write_text(json.dumps(prior,indent=2)+'\n')
(HERE/'PRODUCER_FREEZE.json').write_text(json.dumps(dict(path=str(manifest.relative_to(ROOT)),sha256=sys.argv[2],files=manifest_files),indent=2)+'\n')
print('PASS snapshot',len(inputs),'files',flush=True)
