"""Read-only producer checks, then copy consumed bytes to this review only."""
import json,hashlib,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent;SNAP=HERE/'snapshot'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def copy(p):
 t=SNAP/p.relative_to(ROOT);t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,t)
def check_manifest(p):
 d=load(p);entries=d.get('files',d)
 for name,h in entries.items():
  assert isinstance(h,str) and len(h)==64,(str(p),name)
  assert sha(p.parent/name)==h,(str(p),name,'hash mismatch')
 return dict(manifest_sha256=sha(p),files=entries)

def main():
 combined=R/'low_band/combined_ground_bounds';manifest=combined/'FROZEN_MANIFEST_1906.json'
 assert sha(manifest)=='452848690e6303fb768b1d48e90b3635a52e46c8f4c8c620f8906d956f0aa2bd'
 seal=check_manifest(manifest)
 for n in seal['files']:copy(combined/n)
 copy(manifest);reviews={}
 for review in ['large_seed_review','alternative_order_review','bosonic_tail_review','quadratic_boson_review','tail_comparison_review','bilayer_frontier_review','variational_filter_review','ground_moment_review']:
  p=R/review/'MANIFEST_SHA256.json'
  if not p.exists():raise RuntimeError('Review is not yet sealed: '+review)
  reviews[review]=check_manifest(p);copy(p)
  for f in ['REVIEW_STATUS.json','REVIEW.md','PROOF.md','README.md','INPUT_SHA256.json']:
   if (p.parent/f).exists():copy(p.parent/f)
  s=load(p.parent/'REVIEW_STATUS.json');assert 'pass' in s['status'].lower(),(review,s)
 for directory,manifestname in [('low_band/ground_moment_pencil','ENDPOINT_MANIFEST_SHA256.json'),('variational_numerator_filter','FROZEN_MANIFEST.json')]:
  p=R/directory/manifestname;d=check_manifest(p);copy(p)
  for n in d['files']:copy(p.parent/n)
 paths=set()
 for variant in ['combined','filter_only']:
  for p in (combined/variant).glob('patch_*.json'):
   d=load(p)
   for k in ['source_sha256','recombination_source_sha256']:
    for n,h in d[k].items():assert sha(R/n)==h;paths.add(R/n)
   filtered=load(R/next(n for n in d['recombination_source_sha256'] if 'filtered_' in n))
   for prefix in ['source','geometry_source']:
    q=ROOT/filtered[prefix];assert sha(q)==filtered[prefix+'_sha256'];paths.add(q)
 for item in load(combined/'comparison.json')['results']:
  for v in item['variants'].values():
   p=ROOT/v['source'];assert sha(p)==v['sha256'];paths.add(p)
 for p in paths:copy(p)
 for n in ['low_band/frontier_g006/all_size_bridges.json','low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json','low_band/frontier_g007_g010/short_sizes/quadratic_bins_7x7_g1d10.json','root_review/FINITE_WINDOW_INTERPOLATION.md','root_review/INTERPOLATION_DOMAIN.md']:
  copy(R/n)
 for p in (R/'low_band/frontier_g006/small_sizes').glob('*.json'):copy(p)
 for n in ['two_d_theory/THEORY.md','two_d_theory/three_purity_certificate.py']:copy(ROOT/n)
 deps=load(combined/'DEPENDENCIES.json')['code_sha256']
 for n,h in deps.items():assert sha(ROOT/n)==h
 save(HERE/'PRIOR_REVIEW_SHA256.json',reviews)
 save(HERE/'INPUT_SHA256.json',{str(p.relative_to(SNAP)):sha(p) for p in sorted(SNAP.rglob('*')) if p.is_file()})
 print('INPUTS FROZEN',len(list(SNAP.rglob('*'))),'entries; all eight prior seals PASS')
if __name__=='__main__':main()
