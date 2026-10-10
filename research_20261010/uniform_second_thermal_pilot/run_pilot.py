#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import ast,json,subprocess,resource,os,time,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
v=[98**j*(factorial(280)//factorial(j)) for j in range(281)];Q=2**55;co=[Q*x//sum(v) for x in v];assert max(j for j,x in enumerate(co) if x)==191 and sum(co)<=Q
(P/'coefficients.txt').write_text(''.join(str(x)+'\n' for x in co))
assert 76*2*Q<2**63-1 and 76*2*Q//32+Q<2**63-1
src=ROOT/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'
tree=ast.parse(src.read_text());table=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets));expected={(n,'I' if j%2==0 else 'P'):(c,w) for j,(n,c,w) in enumerate(table)}
def limits():
 os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
def run(n,t,m,count):
 name=f'L{n}_{t}_M{m}_start0_count{count}';path=P/(name+'.json')
 if path.exists():return json.loads(path.read_text())
 b=resource.getrusage(resource.RUSAGE_CHILDREN);st=time.monotonic()
 r=subprocess.run([str(P/'stream_second'),str(n),t,'full',str(m),'0',str(count),str(P/'coefficients.txt'),'compute'],capture_output=True,text=True,preexec_fn=limits,timeout=110)
 a=resource.getrusage(resource.RUSAGE_CHILDREN);assert r.returncode==0,(r.returncode,r.stderr)
 out={'n':n,'twist':t,'magnetization':m,'start':0,'requested_count':count,'records':[dict(zip(('code','multiplicity','norm_squared'),map(int,l.split()))) for l in r.stdout.splitlines()],'diagnostic':r.stderr,'cpu_seconds':a.ru_utime+a.ru_stime-b.ru_utime-b.ru_stime,'wall_seconds':time.monotonic()-st,'maxrss_kib':a.ru_maxrss,'source_sha256':hashlib.sha256((P/'stream_second.cpp').read_bytes()).hexdigest(),'coefficients_sha256':hashlib.sha256((P/'coefficients.txt').read_bytes()).hexdigest()}
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(out,indent=2)+'\n');tmp.replace(path);return out
full=[]
for n in (4,6):
 for t in ('I','P'):
  chunks=[run(n,t,m,100000) for m in range(n+1)];records=[r for c in chunks for r in c['records']];assert sum(x['multiplicity'] for x in records)==3**n
  W=sum(x['multiplicity']*x['norm_squared'] for x in records);center,old=expected[n,t];assert W==old
  x=F(49,4)*n*(F(3,2)-F(700741,500000));ss=sum((x**j/F(factorial(j)) for j in range(101)),F(0));tt=x**100/factorial(100);d=isqrt(3**n)+1;err=d*(281*(d+1)+1);r=isqrt(W);lo=ss*max(0,r-err)**2/Q**2;hi=(ss+tt)*(r+1+err)**2/Q**2;assert F(center-30,10**6)<lo<=hi<F(center+30,10**6)
  full.append({'n':n,'twist':t,'W':str(W),'matches_published_W':True,'lower':str(lo),'upper':str(hi),'representatives':len(records),'cpu_seconds':sum(c['cpu_seconds'] for c in chunks)});print(n,t,'PASS',flush=True)
pilot=run(12,'I',0,4)
result={'status':'PRODUCER independent physical pilot; four small cases complete, L12 partial only','full_small_cases':full,'L12_batch':pilot,'coefficient_data':{'mean':98,'cutoff':280,'Q':Q,'effective_steps':192},'resource_limits':{'cpu_per_child':120,'address_space_mib':256,'cpu_affinity':0}}
(P/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'small_cpu':sum(c['cpu_seconds'] for c in full),'L12_batch_cpu':pilot['cpu_seconds'],'L12_maxrss_kib':pilot['maxrss_kib'],'L12_diagnostic':pilot['diagnostic']},indent=2))
