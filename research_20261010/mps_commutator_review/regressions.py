#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
for name in ['tiny','fused','physical','scalar']:
 q=P/'inputs'/name;filename={'tiny':'MANIFEST_SHA256.json','fused':'INPUT_MANIFEST_SHA256.json','physical':'PHYSICAL_MANIFEST_SHA256.json','scalar':'SCALAR_MANIFEST_SHA256.json'}[name];m=json.loads((q/filename).read_text())
 for f,h in m.get('files',m).items():assert sha(q/f)==h,(name,f)
 checks['frozen_'+name]=sha(q/filename)
for sub in ['mps_excited_seed_review','mps_excited_seed_review/longitudinal_extension','mps_excited_seed_review/momentum_extension']:
 q=P.parent/sub;m=json.loads((q/'MANIFEST_SHA256.json').read_text())
 for f,h in m.get('files',m).items():assert sha(q/f)==h,(sub,f)
 checks['prior_'+sub]=sha(q/'MANIFEST_SHA256.json')
for f,h in json.loads((P/'REPLAY_INPUT_MANIFEST_SHA256.json').read_text()).items():
 if isinstance(h,str) and len(h)==64:assert sha(P/f)==h,f
state=json.loads((P/'independent_n24_checkpoint.json').read_text());assert state['status']=='complete' and len(state['completed'])==37 and len(state['exact'])==74
for f,h in state['input_sha256'].items():assert sha(P/f)==h,f
expected={k:int(v) for k,v in (s.split('=') for s in (P/'inputs/physical/n24_exact.out').read_text().splitlines())};actual={k:int(v) for k,v in (s.split('=') for s in (P/'independent_n24.out').read_text().splitlines())};assert actual==expected=={k:int(v) for k,v in state['exact'].items()}
assert state['total_recorded_CPU_seconds']<2400 and max(x['peak_child_KiB'] for x in state['attempts'])<700*1024
for n in [4,6]:
 data={k:int(v) for k,v in (s.split('=') for s in (P/f'independent_n{n}.out').read_text().splitlines())};ref={k:int(v) for k,v in (s.split('=') for s in (P/f'inputs/fused/fixtures_n{n}.out').read_text().splitlines())};assert data==ref
for f in ['independent_tiny.json','independent_cells.json','independent_fsum.json','independent_assembly.json','independent_scalar.json']:assert json.loads((P/f).read_text())['status'].startswith('PASS')
s=json.loads((P/'independent_scalar.json').read_text());assert all(r['all_beta_excluded'] and len(r['boxes'])==318 for r in s['rows'])
out={'status':'PASS all physical, arithmetic, scalar and immutability regressions','checks':checks,'exact_n24_pairs':37,'exact_n24_integers':74,'recorded_replay_CPU_seconds':state['total_recorded_CPU_seconds'],'peak_child_KiB':max(x['peak_child_KiB'] for x in state['attempts'])};(P/'regressions.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
