#!/usr/bin/env python3
"""Independent read-only campaign validator; no subprocesses or thermal kernels."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
from itertools import product
import json,hashlib,ast,os,resource,time,sys
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));start=time.process_time();sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];RUN=__import__('snapshot_reader').campaign(P);G=P.with_name('uniform_second_thermal_campaign_gate');S=P.with_name('uniform_second_thermal_supervisor');hashes={}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def rd(p):
 b=p.read_bytes();hashes[str(p.relative_to(ROOT))]=sha(b);return b
def js(p):return json.loads(rd(p))
def unwrap(p):
 o=js(p);assert set(o)=={'payload','sha256'} and sha(canonical(o['payload']))==o['sha256'];return o['payload']
for path,want in [(G,'4a282841f56100a6ea99d20d9ce63a79309afe0d1ecdec12f39dee4f94013b68'),(S,'4c631ec44671a0fd7c85ff88754ae1c426b92d215595ee47715b832e87367c3f'),(P.with_name('uniform_second_thermal_extension_gate'),'c97bbaba6236265d86770be29c7bc9a35e9c28d1bb1de0cf1e16f5f029ae83fd')]:
 mf=js(path/'MANIFEST_SHA256.json');assert sha((path/'MANIFEST_SHA256.json').read_bytes())==want
 for f,h in mf.items():assert sha(rd(path/f))==h
pins={f:sha(rd(G/f)) for f in ['kernel.cpp','kernel','coefficients.txt','campaign.py']}
refpath=ROOT/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py';tree=ast.parse(rd(refpath).decode());tab=next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in x.targets));refs={(n,'I' if j%2==0 else 'P'):(c,W) for j,(n,c,W) in enumerate(tab)}

def code(w):
 z=0
 for d in w:z=3*z+d+1
 return z
def geometry(n):
 cache=P/f'orbits_L{n}.json'
 # Cache is reviewer-generated output, checked against its embedded digest.
 if cache.exists():
  o=json.loads(cache.read_text());assert sha(canonical(o['payload']))==o['sha256'];return o['payload']
 seen=set();sectors={str(m):{'dimension':0,'representatives':[]} for m in range(n+1)}
 for w in product((-1,0,1),repeat=n):
  m=sum(w)
  if m<0:continue
  sectors[str(m)]['dimension']+=1;c=code(w)
  if c in seen:continue
  orb=set()
  for x in (w,w[::-1]):
   for j in range(n):
    v=x[j:]+x[:j];orb.add(code(v))
    if m==0:orb.add(code(tuple(-a for a in v)))
  assert c==min(orb);seen.update(orb);sectors[str(m)]['representatives'].append([c,len(orb)*(2 if m else 1)])
 assert sum(sum(mu for c,mu in s['representatives']) for s in sectors.values())==3**n
 cache.write_text(json.dumps({'payload':sectors,'sha256':sha(canonical(sectors))},indent=2)+'\n');return sectors
results=[];pending=[]
for n in range(4,13):
 geo=None
 for t in ('I','P'):
  folder=RUN/'cases'/f'L{n}_{t}';certpath=folder/'certificate.json'
  if not certpath.exists():pending.append(f'L{n}_{t}');continue
  cert=unwrap(certpath);case=unwrap(folder/'case.json');casehash=sha(canonical(case));assert cert['case_sha256']==casehash
  params={'n':n,'twist':t,'beta':'49/4','shift':'700741/500000','cutoff':280,'Q':2**55,'mode':'full_nonnegative_M','batch_size':16};assert case['parameters']==params and case['pins']==pins
  assert [s['M'] for s in case['sectors']]==list(range(n+1))
  if geo is None:geo=geometry(n)
  mat=js(P/f'matrix_L{n}.json');assert mat['sha256']==sha(canonical(mat['payload']));mat={x['M']:x for x in mat['payload']}
  expectednames=set();allcodes=set();mass=W=count=0;payloadhashes={};dn=isqrt(3**n)+1;E=281*(dn+1)+1;normcap=(2**55+E)**2
  for sec in case['sectors']:
   m=sec['M'];assert sec['dimension']==geo[str(m)]['dimension'] and sec['representatives']==geo[str(m)]['representatives'];rr=sec['representatives'];assert sec['orbit_sha256']==sha(canonical(rr))
   assert sec['matrix_sha256']==mat[m][t+'_matrix_sha256'] and sec['nnz']==mat[m]['nnz']
   for starti in range(0,len(rr),16):
    sl=rr[starti:starti+16];num=len(sl);name=f'M{m:02d}_start{starti:06d}_count{num:04d}.json';expectednames.add(name);payload=unwrap(folder/name)
    ident={'case_sha256':casehash,'parameters':params,'pins':pins,'M':m,'start':starti,'count':num,'matrix_sha256':sec['matrix_sha256'],'orbit_sha256':sec['orbit_sha256']}
    assert payload['identity']==ident and set(payload)=={'identity','records','weighted_norm','resources'}
    rows=payload['records'];assert len(rows)==num and [(r['code'],r['multiplicity']) for r in rows]==[tuple(x) for x in sl]
    for r in rows:
     assert set(r)=={'code','multiplicity','norm_squared'} and type(r['norm_squared']) is int and 0<=r['norm_squared']<=normcap
     assert r['code'] not in allcodes;allcodes.add(r['code']);mass+=r['multiplicity'];count+=1
    subtotal=sum(r['multiplicity']*r['norm_squared'] for r in rows);assert subtotal==payload['weighted_norm'];W+=subtotal;payloadhashes[name]=sha(canonical(payload))
  actual={p.name for p in folder.glob('M*.json')};assert actual==expectednames
  assert mass==3**n and cert['multiplicity_sum']==mass and cert['representatives']==count and cert['complete_batches']==len(expectednames) and cert['batch_payload_sha256']==payloadhashes
  center,printed=refs[n,t];assert W==int(cert['W'])==printed and cert['published_W_equal'] is True and cert['published_source_sha256']==sha(refpath.read_bytes())
  x=F(49,4)*n*(F(3,2)-F(700741,500000));term=summ=F(1)
  for k in range(1,101):term*=x/k;summ+=term
  q=isqrt(W);assert q*q<=W<(q+1)**2;err=dn*E;lo=summ*max(0,q-err)**2/2**110;hi=(summ+term)*(q+1+err)**2/2**110
  assert lo==F(cert['lower']) and hi==F(cert['upper']);marginlo=lo-F(center-30,10**6);marginhi=F(center+30,10**6)-hi;assert min(marginlo,marginhi)>F(13,10**6)
  results.append({'case':f'L{n}_{t}','W':str(W),'exact_published_match':True,'representatives':count,'batches':len(expectednames),'multiplicity':mass,'case_sha256':casehash,'certificate_file_sha256':sha(certpath.read_bytes()),'lower':str(lo),'upper':str(hi),'margin_lower':str(marginlo),'margin_upper':str(marginhi),'independent_orbit_coverage':True});print(f'L{n}_{t}: PASS W/identity/coverage/enclosures',flush=True)
ledger=unwrap(RUN/'ledger.json');assert ledger['limit']==43200 and ledger['deadline']==1791698400 and sum(a['charge'] for a in ledger['attempts'])<=43200
old=unwrap(P.with_name('uniform_second_thermal_partial_review')/'snapshot/campaign/ledger.json');assert ledger['attempts'][:61]==old['attempts'] and ledger['bindings']==old['bindings'] and len(ledger['extensions'])==1
event=ledger['extensions'][0];assert (event['old_limit'],event['new_limit'],event['additional_budget'],event['retained_charge'],event['original_attempt_count'],event['deadline'])==(21600,43200,21600,16207,61,1791698400)
assert event['original_terminal_sha256']=='9a6b8fe6944c06544247c07b04344e2258784cbfc722f902b3cc2b979d57f288' and event['authorization_id']=='root-20261011-cap-extension-21600-to-43200'
for filename,h in event['new_bindings'].items():assert sha(rd(Path(filename)))==h
assert ledger['active_extension_bindings']==event['new_bindings']
out={'status':'COMPLETE all18 independently validated physical outputs' if not pending else 'PARTIAL independent read-only validation','completed':len(results),'pending':pending,'cases':results,'live_ledger_observation':{'terminal_state':ledger['terminal_state'],'charged_CPU_seconds':sum(a['charge'] for a in ledger['attempts']),'attempts':len(ledger['attempts'])},'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'no_thermal_jobs_launched':True}
(P/'progress_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','completed','pending','live_ledger_observation','CPU_seconds','RSS_KiB']},indent=2))
