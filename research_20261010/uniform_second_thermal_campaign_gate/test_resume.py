"""Fault-injection fixtures only: no new physical heat columns executed."""
from pathlib import Path
import importlib.util,json,copy,hashlib
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gate',P/'campaign.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
pilot=P.parent/'uniform_second_thermal_pilot'
# Rebuild small matrix/orbit metadata using kernel list/matrix modes only.
case={'parameters':{'n':4,'twist':'I','beta':'49/4','shift':'700741/500000','cutoff':280,'Q':2**55,'mode':'full_nonnegative_M','batch_size':16},'pins':g.pins(),'sectors':[g.sector_metadata(4,'I',m,0) for m in range(5)]}
records={}
for sec,start,count,name in g.batches(case):
 old=json.loads((pilot/f'L4_I_M{sec["M"]}_start0_count100000.json').read_text());rr=old['records'][start:start+count];ident=g.identity(case,sec,start,count);payload={'identity':ident,'records':rr,'weighted_norm':sum(r['multiplicity']*r['norm_squared'] for r in rr),'resources':{'test_fixture':'existing independently computed pilot records, rebound ONLY for validator unit tests; not campaign evidence'}};wrapped=g.wrapped(payload);g.verify_batch(wrapped,ident,sec['representatives'][start:start+count]);records[name]=payload
names=list(records);sample=records[names[0]];ident=sample['identity'];expected=case['sectors'][0]['representatives'];tests=[]
def reject(label,o):
 try:g.verify_batch(o,ident,expected)
 except (AssertionError,KeyError,TypeError,ValueError):tests.append(label);return
 raise AssertionError('fault accepted: '+label)
o=g.wrapped(copy.deepcopy(sample));o['sha256']='0'*64;reject('corrupt payload digest',o)
for key in ['matrix_sha256','orbit_sha256','case_sha256']:
 z=copy.deepcopy(sample);z['identity'][key]='0'*64;reject('stale '+key,g.wrapped(z))
z=copy.deepcopy(sample);z['identity']['pins']['kernel']='0'*64;reject('stale binary',g.wrapped(z))
z=copy.deepcopy(sample);z['identity']['pins']['coefficients.txt']='0'*64;reject('stale coefficients',g.wrapped(z))
z=copy.deepcopy(sample);z['identity']['parameters']['twist']='P';reject('wrong physical seam',g.wrapped(z))
z=copy.deepcopy(sample);z['records']=z['records'][:-1];reject('missing record',g.wrapped(z))
z=copy.deepcopy(sample);z['records'].append(z['records'][0]);reject('duplicate record',g.wrapped(z))
z=copy.deepcopy(sample);z['records'][0]['multiplicity']+=1;reject('wrong orbit weight',g.wrapped(z))
z=copy.deepcopy(sample);z['records'][0]['code']+=1;reject('wrong orbit code',g.wrapped(z))
z=copy.deepcopy(sample);z['records'][0]['norm_squared']=-1;reject('negative norm',g.wrapped(z))
z=copy.deepcopy(sample);z['weighted_norm']+=1;reject('wrong aggregate',g.wrapped(z))
z=copy.deepcopy(sample);z['records'][0]['norm_squared']=2**128;reject('overflow-sized norm',g.wrapped(z))
# Complete set validated idempotently without executing a thermal kernel.
for _ in range(2):
 for sec,start,count,name in g.batches(case):g.verify_batch(g.wrapped(records[name]),g.identity(case,sec,start,count),sec['representatives'][start:start+count])
# Full-certificate routine rejects a missing batch before reading reference totals.
try:g.finalize(case,Path('/unused'),{})
except AssertionError:tests.append('missing batch/hole')
else:raise AssertionError('missing batch accepted')
out={'status':'PASS validator tests only, no campaign computation','faults_rejected':tests,'idempotent_valid_passes':2,'valid_fixture_batches':len(records),'source_sha256':g.sha((P/'campaign.py').read_bytes()),'kernel_sha256':g.sha((P/'kernel').read_bytes())};(P/'resume_tests.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
