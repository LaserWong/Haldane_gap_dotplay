#!/usr/bin/env python3
"""Build from pinned immutable reviews; never consume active working trees."""
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from stage21 import build_stage21
assert not (HERE/'MANIFEST_SHA256.json').exists()
old=ROOT/(R+'overview_stage20')
assert sha(old/'MANIFEST_SHA256.json')=='de1e346d56f73dc638dba23e97845b8767ed9c6d3b85fe2f609642551e28b853'
manifest_check(R+'overview_stage20/MANIFEST_SHA256.json')
data=json.loads((old/'overview_data.json').read_text())
data['preserved_stage20_files']={R+'overview_stage20/'+p:sha(old/p) for p in json.loads((old/'MANIFEST_SHA256.json').read_text())}
data['preserved_stage20_files'][R+'overview_stage20/MANIFEST_SHA256.json']=sha(old/'MANIFEST_SHA256.json')
data['sources'][R+'overview_stage20/overview_data.json']=sha(old/'overview_data.json')
build_stage21(data)
data.update(snapshot_label='stage21',schema_version=18,generated_utc=datetime.now(timezone.utc).isoformat(),claim_selection='Preserve all Stage20 scientific records and CSVs; add final independent B2 physical-observable, second-moment all-size intervals, and explicitly limited sealed engineering findings. Producer-only failure remains unaccepted.')
(HERE/'overview_data.json').write_text(json.dumps(data,indent=2)+'\n')
(HERE/'ACCEPTED_REVIEW_SEALS.json').write_text(json.dumps({s['manifest']:s['sha256'] for s in data['review_seals']},indent=2)+'\n')
(HERE/'review_acceptance_snapshot.json').write_text(json.dumps(data['review_seals'],indent=2)+'\n')
for p in old.glob('*.csv'):(HERE/p.name).write_bytes(p.read_bytes())
for key in ['stage21_observables','stage21_first_intervals','stage21_finite_intervals','stage21_engineering_scope','stage21_component_scope','stage21_unaccepted_findings']:csv_write(key+'.csv',data[key])
print('PASS Stage21 preparation',len(data['claims']),len(data['review_seals']),len(data['stage21_dependencies']))
