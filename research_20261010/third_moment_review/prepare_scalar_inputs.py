from pathlib import Path
import json,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parent;S=O/'snapshot';P=R/'low_band/third_moment_exact'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
f=P/'scalar_candidates/SCALAR_MANIFEST.json';m=json.loads(f.read_text());copy(f,S/'producer/scalar_candidates/SCALAR_MANIFEST.json')
for name,h in m['files_relative_to_third_moment_exact'].items():
 assert sha(P/name)==h,name;copy(P/name,S/'producer'/name)
prior=json.loads((O/'PRIOR_REVIEW_SHA256.json').read_text())
for name,manifest in [('bilayer_polynomial_frontier_review','MANIFEST_SHA256.json'),('combined_ground_review','MANIFEST_SHA256.json'),('joint_ratio_review','LEMMA_REVIEW_MANIFEST.json')]:
 p=R/name/manifest;entries=json.loads(p.read_text());entries=entries.get('files',entries)
 for rel,h in entries.items():assert sha(p.parent/rel)==h,(name,rel)
 prior[name]={'manifest_sha256':sha(p),'manifest_filename':manifest,'entries_checked':len(entries)}
 copy(p,S/'prior_reviews'/name/manifest)
for path in ('bilayer_polynomial_frontier_review/audit.py','bilayer_polynomial_frontier_review/PROOF.md','bilayer_polynomial_frontier_review/PHYSICAL_ACCEPTANCE.json','bilayer_polynomial_frontier_review/results/physical_review.json','combined_ground_review/independent_math.py','joint_ratio_review/GENERAL_LEMMA.md','joint_ratio_review/LEMMA_ACCEPTANCE.json'):
 copy(R/path,S/'prior_reviews'/path)
# Denominator inputs must be the exact physically accepted .09 records.
accepted=json.loads((R/'bilayer_polynomial_frontier_review/MANIFEST_SHA256.json').read_text())
for shape in ('4x4','8x4','8x8'):
 name=f'combined_patch_{shape}_g9d100.json';h=sha(S/'producer/scalar_candidates'/f'denominator_snapshot_{name}')
 assert h==accepted[f'snapshot/low_band/frontier_g009/{name}']
(O/'PRIOR_REVIEW_SHA256.json').write_text(json.dumps(prior,indent=2)+'\n')
(O/'INPUT_SHA256.json').write_text(json.dumps({str(p.relative_to(S)):sha(p) for p in sorted(S.rglob('*')) if p.is_file()},indent=2)+'\n')
print('scalar inputs frozen; existing physically accepted denominators match byte-for-byte')
