#!/usr/bin/env python3
"""Strict campaign runner; creation does not authorize campaign execution."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import argparse,json,hashlib,subprocess,resource,os,time,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def wrapped(o):return {'payload':o,'sha256':sha(canonical(o))}
def unpack(o):
 assert set(o)=={'payload','sha256'} and o['sha256']==sha(canonical(o['payload'])),'corrupt output digest'
 return o['payload']
def save(path,o):
 raw=json.dumps(wrapped(o),indent=2)+'\n';tmp=path.with_suffix('.tmp')
 with open(tmp,'x') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def limits(cpu,seconds=120):
 def go():
  os.sched_setaffinity(0,{cpu});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(seconds,seconds))
 return go
def pins():
 v=[98**j*(factorial(280)//factorial(j)) for j in range(281)];Q=2**55;co=[Q*x//sum(v) for x in v];raw=(P/'coefficients.txt').read_bytes();assert raw==''.join(str(x)+'\n' for x in co).encode();assert max(i for i,x in enumerate(co) if x)==191
 return {f:sha((P/f).read_bytes()) for f in ['kernel.cpp','kernel','coefficients.txt','campaign.py']}
def command(n,t,m,start,count,mode):return [str(P/'kernel'),str(n),t,'full',str(m),str(start),str(count),str(P/'coefficients.txt'),mode]
def sector_metadata(n,t,m,cpu):
 r=subprocess.run(command(n,t,m,0,0,'list'),capture_output=True,text=True,check=True,preexec_fn=limits(cpu),timeout=120)
 lines=r.stdout.splitlines();meta=lines[0].split();assert meta[:5]==['META',str(n),t,'full',str(m)] and int(meta[-1])==191
 d,num=int(meta[5]),int(meta[6]);reps=[list(map(int,l.split())) for l in lines[1:]];assert len(reps)==num and len({c for c,w in reps})==num and reps==sorted(reps);assert all(w>0 for c,w in reps)
 h=hashlib.sha256();process=subprocess.Popen(command(n,t,m,0,0,'matrix'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=limits(cpu))
 header=process.stdout.readline();h.update(header);fields=header.decode().split();assert fields[:5]==['MATRIX',str(n),t,str(m),str(d)]
 while True:
  chunk=process.stdout.read(1<<16)
  if not chunk:break
  h.update(chunk)
 err=process.stderr.read();assert process.wait(timeout=120)==0,err
 return {'M':m,'dimension':d,'nnz':int(fields[5]),'representatives':reps,'orbit_sha256':sha(canonical(reps)),'matrix_sha256':h.hexdigest()}
def loadcase(path,n,t,batch,sourcepins):
 obj=unpack(json.loads(path.read_text()));assert obj['parameters']=={'n':n,'twist':t,'beta':'49/4','shift':'700741/500000','cutoff':280,'Q':2**55,'mode':'full_nonnegative_M','batch_size':batch};assert obj['pins']==sourcepins
 assert [s['M'] for s in obj['sectors']]==list(range(n+1));codes=[];mass=0
 for s in obj['sectors']:
  rr=s['representatives'];assert s['orbit_sha256']==sha(canonical(rr));assert rr==sorted(rr);assert len(rr)==len({c for c,w in rr}) and all(w>0 for c,w in rr)
  codes.extend(c for c,w in rr);mass+=sum(w for c,w in rr)
 assert len(codes)==len(set(codes)) and mass==3**n
 return obj

def identity(case,s,start,count):
 return {'case_sha256':sha(canonical(case)),'parameters':case['parameters'],'pins':case['pins'],'M':s['M'],'start':start,'count':count,'matrix_sha256':s['matrix_sha256'],'orbit_sha256':s['orbit_sha256']}
def verify_batch(obj,ident,expected):
 p=unpack(obj);assert set(p)=={'identity','records','weighted_norm','resources'} and p['identity']==ident
 rr=p['records'];assert len(rr)==ident['count']==len(expected)
 assert [(r['code'],r['multiplicity']) for r in rr]==[tuple(x) for x in expected]
 n=ident['parameters']['n'];d=isqrt(3**n)+1;E=281*(d+1)+1;cap=(2**55+E)**2
 for r in rr:
  assert set(r)=={'code','multiplicity','norm_squared'};assert type(r['norm_squared']) is int and 0<=r['norm_squared']<=cap
 assert p['weighted_norm']==sum(r['multiplicity']*r['norm_squared'] for r in rr)
 return p

def batches(case):
 size=case['parameters']['batch_size']
 for s in case['sectors']:
  for start in range(0,len(s['representatives']),size):
   count=min(size,len(s['representatives'])-start);yield s,start,count,f"M{s['M']:02d}_start{start:06d}_count{count:04d}.json"
def finalize(case,folder,records):
 expected={name for *_,name in batches(case)};assert set(records)==expected,'missing batch or hole'
 allcodes=[];mass=0;W=0
 for name,p in records.items():
  W+=p['weighted_norm'];allcodes.extend(r['code'] for r in p['records']);mass+=sum(r['multiplicity'] for r in p['records'])
 n=case['parameters']['n'];t=case['parameters']['twist'];assert len(allcodes)==len(set(allcodes)) and mass==3**n
 x=F(49,4)*n*(F(3,2)-F(700741,500000));ss=sum((x**j/F(factorial(j)) for j in range(101)),F(0));tt=x**100/factorial(100);d=isqrt(3**n)+1;E=d*(281*(d+1)+1);r=isqrt(W);Q=2**55;lo=ss*max(0,r-E)**2/Q**2;hi=(ss+tt)*(r+1+E)**2/Q**2
 # Reference totals are read ONLY after complete independent physical aggregation.
 import ast
 src=ROOT/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py';tree=ast.parse(src.read_text());rows=next(ast.literal_eval(a.value) for a in tree.body if isinstance(a,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='B' for z in a.targets));ref={(nn,'I' if j%2==0 else 'P'):(c,w) for j,(nn,c,w) in enumerate(rows)};center,printed=ref[n,t];assert F(center-30,10**6)<lo<=hi<F(center+30,10**6)
 out={'case_sha256':sha(canonical(case)),'W':str(W),'published_W_equal':W==printed,'published_source_sha256':sha(src.read_bytes()),'lower':str(lo),'upper':str(hi),'multiplicity_sum':mass,'representatives':len(allcodes),'complete_batches':len(records),'batch_payload_sha256':{name:sha(canonical(p)) for name,p in records.items()},'status':'PRODUCER complete independently aggregated physical thermal case; review required'}
 path=folder/'certificate.json'
 if path.exists():assert unpack(json.loads(path.read_text()))==out
 else:save(path,out)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--action',choices=['prepare','validate','run'],required=True);ap.add_argument('--length',type=int,required=True);ap.add_argument('--twist',choices=['I','P'],required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--batch-size',type=int,default=16);ap.add_argument('--max-new-batches',type=int,default=1);ap.add_argument('--cpu',type=int,default=0);ap.add_argument('--cpu-budget',type=float,default=120);args=ap.parse_args();assert 4<=args.length<=12 and 1<=args.batch_size<=32 and 0<=args.max_new_batches and 0<args.cpu_budget<=21600
 os.sched_setaffinity(0,{args.cpu});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));sourcepins=pins();n,t=args.length,args.twist;folder=args.output.resolve();assert folder!=P and P not in folder.parents,'runtime output must be outside frozen source package';folder.mkdir(parents=True,exist_ok=True)
 lock=folder/'.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  meta=folder/'case.json'
  if not meta.exists():
   assert args.action=='prepare' and not list(folder.glob('*.json'))
   sectors=[sector_metadata(n,t,m,args.cpu) for m in range(n+1)]
   case={'parameters':{'n':n,'twist':t,'beta':'49/4','shift':'700741/500000','cutoff':280,'Q':2**55,'mode':'full_nonnegative_M','batch_size':args.batch_size},'pins':sourcepins,'sectors':sectors};save(meta,case)
  case=loadcase(meta,n,t,args.batch_size,sourcepins)
  # Rebuild physical matrix/orbit identities on every entry; checksums alone are insufficient.
  for sector in case['sectors']:
   assert sector_metadata(n,t,sector['M'],args.cpu)==sector,'geometry metadata changed'
  expected={name for *_,name in batches(case)};unknown={f.name for f in folder.glob('*.json')}-expected-{'case.json','certificate.json'};assert not unknown,unknown;assert not list(folder.glob('*.tmp')),'incomplete atomic write present; inspect before resume'
  records={};new=0;startusage=resource.getrusage(resource.RUSAGE_CHILDREN);startcpu=time.process_time()
  for s,start,count,name in batches(case):
   path=folder/name;ident=identity(case,s,start,count);rr=s['representatives'][start:start+count]
   if path.exists():records[name]=verify_batch(json.loads(path.read_text()),ident,rr);continue
   if args.action!='run' or new>=args.max_new_batches:continue
   usage=resource.getrusage(resource.RUSAGE_CHILDREN);used=time.process_time()-startcpu+usage.ru_utime+usage.ru_stime-startusage.ru_utime-startusage.ru_stime
   remaining=int(args.cpu_budget-used)-1
   if remaining<1:break
   b=resource.getrusage(resource.RUSAGE_CHILDREN);wall=time.monotonic();r=subprocess.run(command(n,t,s['M'],start,count,'compute'),capture_output=True,text=True,preexec_fn=limits(args.cpu,min(120,remaining)),timeout=min(125,remaining+5));a=resource.getrusage(resource.RUSAGE_CHILDREN);assert r.returncode==0,(r.returncode,r.stderr)
   rows=[dict(zip(('code','multiplicity','norm_squared'),map(int,line.split()))) for line in r.stdout.splitlines()];payload={'identity':ident,'records':rows,'weighted_norm':sum(z['multiplicity']*z['norm_squared'] for z in rows),'resources':{'cpu_seconds':a.ru_utime+a.ru_stime-b.ru_utime-b.ru_stime,'wall_seconds':time.monotonic()-wall,'child_maxrss_kib':a.ru_maxrss,'diagnostic':r.stderr}}
   verify_batch(wrapped(payload),ident,rr);save(path,payload);records[name]=payload;new+=1;print('checkpoint',name,flush=True)
  if len(records)==len(expected):print(json.dumps(finalize(case,folder,records),indent=2))
  else:print(json.dumps({'status':'INCOMPLETE, no thermal certificate','valid_batches':len(records),'expected_batches':len(expected),'new_batches':new}))
 finally:lock.unlink()
if __name__=='__main__':main()
