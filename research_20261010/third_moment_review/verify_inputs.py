from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent;S=O/'snapshot'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((O/'INPUT_SHA256.json').read_text())
for p,h in inputs.items():assert sha(S/p)==h,p
P=S/'producer'
for name,key in [('PHYSICAL_MANIFEST.json','files'),('scalar_candidates/SCALAR_MANIFEST.json','files_relative_to_third_moment_exact')]:
 for p,h in json.loads((P/name).read_text())[key].items():assert sha(P/p)==h,p
prior=json.loads((O/'PRIOR_REVIEW_SHA256.json').read_text())
for name,r in prior.items():assert sha(S/'prior_reviews'/name/r.get('manifest_filename','MANIFEST_SHA256.json'))==r['manifest_sha256']
print('PASS',len(inputs),'frozen snapshot hashes and both producer seals')
