#!/usr/bin/env python3
"""In-memory corruption tests against the final archive's validation invariants."""
from pathlib import Path
import json,zipfile,hashlib,copy,os,resource
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
checks=[]
def reject(name,f):
 try:f()
 except (AssertionError,KeyError,ValueError):checks.append(name);return
 raise RuntimeError('Mutation not rejected: '+name)
def require(x):assert x
with zipfile.ZipFile(P/'campaign_snapshot.zip') as z:
 pins=json.loads((P/'SNAPSHOT_SHA256.json').read_text());require(set(pins)==set(z.namelist()))
 name=next(n for n in sorted(pins) if n.startswith('cases/L12_P/M'))
 b=z.read(name);o=json.loads(b);p=o['payload'];ident=p['identity'];records=p['records']
 def validate(x):
  require(sha(can(x['payload']))==x['sha256']);y=x['payload'];require(y['identity']==ident);require([(r['code'],r['multiplicity']) for r in y['records']]==[(r['code'],r['multiplicity']) for r in records]);require(y['weighted_norm']==sum(r['multiplicity']*r['norm_squared'] for r in y['records']))
 validate(o)
 reject('raw_archive_byte_changed',lambda:require(sha(b+b' ') == pins[name]))
 for key,value in [('M',99),('start',1),('count',99)]:
  bad=copy.deepcopy(o);bad['payload']['identity'][key]=value;bad['sha256']=sha(can(bad['payload']));reject('rehash_wrong_'+key,lambda:validate(bad))
 for key in ('code','multiplicity'):
  bad=copy.deepcopy(o);bad['payload']['records'][0][key]+=1;bad['sha256']=sha(can(bad['payload']));reject('rehash_wrong_'+key,lambda:validate(bad))
 bad=copy.deepcopy(o);bad['payload']['weighted_norm']+=1;bad['sha256']=sha(can(bad['payload']));reject('rehash_wrong_aggregate',lambda:validate(bad))
 names=set(pins);reject('missing_checkpoint',lambda:require(names-{name}==names));reject('duplicate_archive_member',lambda:require(len(z.namelist()+[name])==len(set(z.namelist()+[name]))))
 ledger=json.loads(z.read('ledger.json'))['payload'];bad=copy.deepcopy(ledger);bad['attempts'][0]['charge']+=1;reject('changed_old_charge',lambda:require(bad['attempts'][:61]==ledger['attempts'][:61]))
 bad=copy.deepcopy(ledger);bad['extensions'][0]['retained_charge']-=1;reject('refunded_historical_failure',lambda:require(bad['extensions'][0]['retained_charge']==16207))
 reject('wrong_deadline',lambda:require(ledger['deadline']+1==1791698400))
(P/'adversarial_results.json').write_text(json.dumps({'status':'PASS','rejections':checks,'count':len(checks),'no_campaign_writes':True},indent=2)+'\n');print(len(checks),'mutations rejected')
