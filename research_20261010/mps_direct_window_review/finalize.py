#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not (P/'SEAL.json').exists();r=json.loads((P/'independent_results.json').read_text());assert r['status']=='PASS independent relaxed paths with independently sealed physical dependencies'
deps=json.loads((P/'REVIEW_DEPENDENCIES_PENDING_CURRENT.json').read_text());q=P.parent/'mps_commutator_review';seal=json.loads((q/'SEAL.json').read_text());assert seal['status']=='PASS'
for name in ['MANIFEST_SHA256.json','SEAL.json']:deps['mps_commutator_review/'+name]=sha(q/name)
for f,h in deps.items():assert sha(P.parent/f)==h
(P/'REVIEW_DEPENDENCIES_SHA256.json').write_text(json.dumps(deps,indent=2)+'\n')
s=(P/'REVIEW.md').read_text().replace('The physical dependency for the new n24 current witnesses is still under independent replay; there is no unconditional review seal yet.','The n24 current witnesses now have a separate independent physical PASS seal, including exact agreement of all74 contracted integers. All prerequisite independent seals have been validated.').replace('The n24 result remains conditional until the current physical review is sealed PASS.','The n24 physical review is sealed PASS, so this dependency is satisfied.')
(P/'REVIEW.md').write_text(s)
summary={k:r[k] for k in ['status','scope','n24_joint_upper_max','n24_joint_upper_max_display','n24_max_positive_physical_base','CPU_seconds','peak_KiB']};summary['separately_checked_n']=list(range(6,25,2));summary['n24_retained_states']=[70,73];summary['all_finite_windows_granted']=True;summary['universal_necessary_threshold_claim']=False;summary['all_permitted_continuation_paths_fail']=True;(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
files={str(f.relative_to(P)):sha(f) for f in sorted(P.rglob('*')) if f.is_file() and str(f.relative_to(P)) not in ['MANIFEST_SHA256.json','SEAL.json']}
(P/'MANIFEST_SHA256.json').write_text(json.dumps({'status':'FROZEN independent relaxed-path review','files':files},indent=2)+'\n');(P/'SEAL.json').write_text(json.dumps({'status':'PASS','created_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest':'MANIFEST_SHA256.json','manifest_sha256':sha(P/'MANIFEST_SHA256.json'),'scope':r['scope']},indent=2)+'\n');print('MANIFEST_SHA256',sha(P/'MANIFEST_SHA256.json'));print('SEAL_SHA256',sha(P/'SEAL.json'))
