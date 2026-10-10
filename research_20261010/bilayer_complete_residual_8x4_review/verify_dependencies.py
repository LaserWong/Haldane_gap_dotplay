from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;P=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'hardcore_pair_commutator':('MANIFEST_SHA256.json','88409894783492f26c96efff2a1ea964db99d77c5b12fd3fe42ff35a84f86020'),'bilayer_commutator_feasibility':('FROZEN_MANIFEST.json','e74663721dcf3194a15dda2850de5e19e2b06fc9a9fcd3da16401e1b8526c10a'),'third_moment_review':('MANIFEST_SHA256.json',None),'bilayer_g010_diagnostics_review':('MANIFEST_SHA256.json',None)}
out={}
for name,(seal,digest) in expected.items():
 p=P/name/seal
 if digest:assert sha(p)==digest
 rec=json.loads(p.read_text());entries=rec.get('files',rec)
 for rel,h in entries.items():assert sha(p.parent/rel)==h,(name,rel)
 out[name]={'seal':seal,'sha256':sha(p),'files_checked':len(entries)}
(R/'DEPENDENCIES.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
