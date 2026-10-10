"""Copy only immutable, hash-checked inputs used by this independent review."""
from pathlib import Path
import json,hashlib,shutil
OUT=Path(__file__).resolve().parent;RES=OUT.parent;SNAP=OUT/'snapshot';PROD=RES/'low_band/third_moment_exact'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
manifest=json.loads((PROD/'PHYSICAL_MANIFEST.json').read_text())
for p,h in manifest['files'].items():
 assert sha(PROD/p)==h,p
 copy(PROD/p,SNAP/'producer'/p)
copy(PROD/'PHYSICAL_MANIFEST.json',SNAP/'producer/PHYSICAL_MANIFEST.json')
prior={}
for name in ('large_seed_review','variational_filter_review','ground_moment_review'):
 p=RES/name/'MANIFEST_SHA256.json';data=json.loads(p.read_text());entries=data.get('files',data)
 for rel,h in entries.items():assert sha(p.parent/rel)==h,(name,rel)
 prior[name]={'manifest_sha256':sha(p),'entries_checked':len(entries)}
 copy(p,SNAP/'prior_reviews'/name/'MANIFEST_SHA256.json')
 copy(RES/name/'REVIEW.md',SNAP/'prior_reviews'/name/'REVIEW.md')
for shape in ('2x2','4x2','4x4','8x4','8x8'):
 for ext in ('json','txt'):copy(RES/'large_seed_review/results'/f'geometry_{shape}.{ext}',SNAP/'prior_geometry'/f'geometry_{shape}.{ext}')
for name in ('FROZEN_MANIFEST_1920.json','INPUT_PROVENANCE.json'):
 copy(RES/'low_band/frontier_g009'/name,SNAP/'original'/name)
frozen=json.loads((RES/'low_band/frontier_g009/FROZEN_MANIFEST_1920.json').read_text());print('frontier manifest keys',list(frozen)[:6])
for shape in ('4x4','8x4','8x8'):
 name=f'block1_{shape}_g9d100.json';p=RES/'low_band/frontier_g009'/name
 copy(p,SNAP/'original'/name)
 for family in ('filtered','enlarged'):
  rec=json.loads((PROD/f'{family}_{shape}_g9d100.json').read_text());assert rec['source_sha256'][f'low_band/frontier_g009/{name}']==sha(p)
(OUT/'PRIOR_REVIEW_SHA256.json').write_text(json.dumps(prior,indent=2)+'\n')
inputs={str(p.relative_to(SNAP)):sha(p) for p in sorted(SNAP.rglob('*')) if p.is_file()}
(OUT/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print('frozen input snapshot',len(inputs),'files; producer seal',sha(PROD/'PHYSICAL_MANIFEST.json'))
