#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from stage22 import build_stage22
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage21')
assert sha(old/'MANIFEST_SHA256.json')=='36e427dd2105465d40adf8b3d8c36cd76bff079b31a995bef1efa9837d847da4'
manifest_check(R+'overview_stage21/MANIFEST_SHA256.json')
data=json.loads((old/'overview_data.json').read_text())
data['preserved_stage21_files']={R+'overview_stage21/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
data['preserved_stage21_files'][R+'overview_stage21/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
data['sources'][R+'overview_stage21/overview_data.json']=sha(old/'overview_data.json')
build_stage22(data)
data.update(snapshot_label='stage22',schema_version=19,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='Preserve all Stage21 data and CSV bytes. Add final independent H2/variance and refined all-size interval evidence, bounded launch/streaming reviews, and the immutable failed original startup. Only immutable independently reviewed partial checkpoints and terminal failures are included; live runtime paths and pending repairs remain excluded.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in data['review_seals']},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(data['review_seals'],indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
for key in ['stage22_observables','stage22_refined_intervals','stage22_engineering_scope','stage22_failed_jobs','stage22_failure_summary','stage22_checkpoint100','stage22_terminal100']:csv_write(key+'.csv',data[key])
print('PASS Stage22 preparation',len(data['claims']),len(data['review_seals']),len(data['stage22_dependencies']))
