import os,resource,math,json,time
from pathlib import Path
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
HERE=Path(__file__).resolve().parent;RES=HERE.parent
start=time.process_time();source=json.loads((RES/'bilayer_split_pencil_scalar/result.json').read_text())['results'][0]
K=9
coords=[(x,y,t) for x in range(K) for y in range(K) for t in range(K)]
def inc(v,i):w=list(v);w[i]+=1;return tuple(w)
def mirror(v):return (v[1],v[0],v[2])
def G(p):return 1-(1-p)**2/(2*p*p) if p>1e-100 else 0

def closure(raw):
 E={(v,i):0. for v in coords for i in range(3)}
 E[((0,0,0),2)]=raw[0];E[((0,0,1),0)]=raw[1];E[((1,0,1),1)]=raw[2]
 ops=0
 for it in range(180):
  change=0.
  def up(key,value):
   nonlocal change,ops
   if value>E[key]:change=max(change,value-E[key]);E[key]=value;ops+=1
  for v in coords:
   for i in range(3):
    p=E[v,i];up((mirror(v),1-i if i<2 else 2),p)
    if v[i]+1<K:up((inc(v,i),i),max(p,G(p)))
   for i,j in [(0,1),(0,2),(1,2)]:
    if v[i]+1>=K or v[j]+1>=K:continue
    ka=(v,i);kb=(inc(v,i),j);kc=(v,j);kd=(inc(v,j),i)
    a,b,c,d=E[ka],E[kb],E[kc],E[kd]
    up(kd,b*a*a);up(kc,a*math.sqrt(b));up(kb,d*c*c);up(ka,c*math.sqrt(d))
  if change<1e-14:break
 rows=[]
 for j in range(K-2):
  v=(j,j,j);a=E[v,2];b=E[(j,j,j+1),0];c=E[(j+1,j,j+1),1]
  can=[E[v,0],E[(j+1,j,j),1],E[(j+1,j+1,j),2]]
  s=b*b*math.sqrt(max(0,2*c-1));old=(a**4*(2*b*math.sqrt(c)-1)*math.sqrt(2*s-1)) if s>.5 else 0
  better=(a**4*(2*b-1)*math.sqrt(2*s-1)) if s>.5 else 0
  rows.append(dict(cycle=j,raw=[a,b,c],canonical=can,defect=max(1-x for x in can),old_window=old,symmetry_window=better))
 mixed=[]
 for j in range(K-2):
  for t in range(K-2):
   v=(j,j,t);a=E[v,2];b=E[(j,j,t+1),0];c=E[(j+1,j,t+1),1];can=[E[v,0],E[(j+1,j,t),1],E[(j+1,j+1,t),2]]
   ss=b*b*math.sqrt(max(0,2*c-1));val=a**4*(2*b-1)*math.sqrt(2*ss-1) if ss>.5 else 0
   mixed.append(dict(spatial_cycle=j,temperature_cycle=t,raw=[a,b,c],window=val,defect=max(1-x for x in can)))
 return dict(iterations=it+1,updates=ops,states=rows,mixed_indices=mixed)

def plain(raw):
 out=[]
 for j in range(10):
  a,b,c=raw;s=b*b*math.sqrt(max(0,2*c-1));v=a**4*(2*b-1)*math.sqrt(2*s-1) if s>.5 else 0
  out.append(dict(cycle=j,raw=raw,symmetry_window=v))
  if j==9:break
  raw=raw[:]
  for _ in range(3):
   z=raw[0]**4*raw[1]**2*raw[2];p=G(z)
   if p<=0:return out
   raw=raw[1:]+[p]
 return out
out=[]
for test in source['tests']:
 raw=test['diagnostic']['states'][0]['raw'] if test['diagnostic'].get('states') else None
 if raw is None:continue
 row=dict(beta=test['beta'],plain=plain(raw),closure=closure(raw));out.append(row)
 (HERE/'pilot_results.json').write_text(json.dumps(dict(status='floating_bounded_cached_pilot_only',source='bilayer_split_pencil_scalar/result.json',results=out,cpu_seconds=time.process_time()-start),indent=2)+'\n')
 print(test['beta'],[(r['cycle'],round(r['symmetry_window'],5),round(r['defect'],5)) for r in row['closure']['states']],flush=True)
print('CPU',time.process_time()-start)
