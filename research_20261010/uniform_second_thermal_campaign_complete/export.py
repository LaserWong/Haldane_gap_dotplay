#!/usr/bin/env python3
"""Read-only validation/export of terminal physical thermal campaign."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json,hashlib,ast,os,resource,time,importlib.util,shutil
P=Path(__file__).resolve().parent;ROOT=P.parents[1];R=P.parent;STATE=R/'uniform_second_thermal_campaign_run';os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));start=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 obj=json.loads(p.read_text());assert obj['sha256']==hashlib.sha256(json.dumps(obj['payload'],sort_keys=True,separators=(',',':')).encode()).hexdigest();return obj['payload']
ledger=read(STATE/'ledger.json');assert ledger['terminal_state']=='ALL_CASES_COMPLETE_PRODUCER_REVIEW_REQUIRED' and ledger['limit']==43200
assert not any(a['status'] in ('ACTIVE','RESERVED') for a in ledger['attempts']);assert not any(a['status'] in ('UNKNOWN_CHARGED','DEADLINE_CHARGED') for a in ledger['attempts'][61:]);old=read(R/'uniform_second_thermal_campaign_partial_outcome/terminal_ledger_snapshot.json');assert ledger['attempts'][:61]==old['attempts'] and sum(a['charge'] for a in old['attempts'])==16207;assert sum(a['charge'] for a in ledger['attempts'])==27543
spec=importlib.util.spec_from_file_location('accepted_runner',R/'uniform_second_thermal_campaign_gate/campaign.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);pins=g.pins()
source=ROOT/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py';tree=ast.parse(source.read_text());data=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets));published={(n,'I' if j%2==0 else 'P'):(c,w) for j,(n,c,w) in enumerate(data)}
results=[];batch_count=0
for n in range(4,13):
 for twist in ('I','P'):
  folder=STATE/'cases'/f'L{n}_{twist}';case=g.loadcase(folder/'case.json',n,twist,16,pins);saved=read(folder/'certificate.json');assert saved['case_sha256']==g.sha(g.canonical(case));W=0;mass=0;codes=[];cpu=0;maxrss=0;names=set()
  for sec,first,count,name in g.batches(case):
   f=folder/name;payload=g.verify_batch(json.loads(f.read_text()),g.identity(case,sec,first,count),sec['representatives'][first:first+count]);assert saved['batch_payload_sha256'][name]==g.sha(g.canonical(payload));names.add(name);W+=payload['weighted_norm'];mass+=sum(r['multiplicity'] for r in payload['records']);codes.extend(r['code'] for r in payload['records']);cpu+=payload['resources']['cpu_seconds'];maxrss=max(maxrss,payload['resources']['child_maxrss_kib'])
  assert names=={f.name for f in folder.glob('M*.json')};assert len(codes)==len(set(codes)) and mass==3**n and W==int(saved['W']);assert len(names)==saved['complete_batches'];batch_count+=len(names)
  x=F(49,4)*n*(F(3,2)-F(700741,500000));ss=sum((x**j/F(factorial(j)) for j in range(101)),F(0));tt=x**100/factorial(100);d=isqrt(3**n)+1;E=d*(281*(d+1)+1);r=isqrt(W);lo=ss*max(0,r-E)**2/(2**110);hi=(ss+tt)*(r+1+E)**2/(2**110);center,printed=published[n,twist];assert lo==F(saved['lower']) and hi==F(saved['upper']);assert F(center-30,10**6)<lo<=hi<F(center+30,10**6);assert W==printed
  target=P/'certificates'/f'L{n}_{twist}';target.mkdir(parents=True,exist_ok=True);shutil.copyfile(folder/'certificate.json',target/'certificate.json');results.append({'n':n,'twist':twist,'beta':'49/4','shift':'700741/500000','W':str(W),'lower':str(lo),'upper':str(hi),'published_center':str(F(center,10**6)),'published_error':'3/100000','published_W_equal':True,'lower_margin':str(lo-F(center-30,10**6)),'upper_margin':str(F(center+30,10**6)-hi),'physical_dimension':3**n,'representatives':len(codes),'batches':len(names),'successful_batch_child_cpu_seconds':cpu,'max_recorded_child_rss_kib':maxrss,'case_metadata_sha256':sha(folder/'case.json'),'certificate_sha256':sha(folder/'certificate.json')});print(n,twist,'PASS',flush=True)
assert batch_count==2428
shutil.copyfile(STATE/'ledger.json',P/'terminal_ledger.json');shutil.copyfile(R/'uniform_second_thermal_extension_stdout.log',P/'terminal_stdout.log')
statehashes={str(f.relative_to(STATE)):sha(f) for f in sorted(STATE.rglob('*')) if f.is_file()};(P/'CAMPAIGN_STATE_SHA256.json').write_text(json.dumps(statehashes,indent=2)+'\n')
out={'status':'PRODUCER COMPLETE all18 physical thermal inputs independently recomputed; final independent review pending','model':'uniform periodic spin1 Heisenberg, bilinear coefficient1; n4..12 including odd lengths, identity/pi seams','thermal_inputs':results,'total_batches':batch_count,'terminal_state':ledger['terminal_state'],'ledger':{'old_limit':21600,'old_charges_retained':16207,'old_attempts_preserved':61,'new_limit':43200,'total_charged':27543,'remaining':15657,'unknown_old_attempts_full_charge':14640,'new_failures':0,'active_attempts':0,'wallstop_utc':'2026-10-11T06:00:00Z'},'scope':'This supplies the physical18 beta49/4 thermal inputs. It does not itself promote any conditional gap theorem; independent final audit and linkage remain required.','export_validation_resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'address_space_limit_mib':256,'cpu_limit_seconds':120}}
(P/'thermal_inputs.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'total_batches':batch_count,'ledger':out['ledger'],'resources':out['export_validation_resources']},indent=2))
