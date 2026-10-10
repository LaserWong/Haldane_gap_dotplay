#!/usr/bin/env python3
"""All-r interval exclusion for a precisely specified canonical cooled recipe."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**24;START=time.process_time();os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));hashes={}
def read(p):
 raw=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest();return raw
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x,q):
 assert x>=0
 if q==1:return down(x),up(x)
 lo=0;hi=B
 while F(hi,B)**q<x:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if F(mid,B)**q<=x:lo=mid
  else:hi=mid
 return F(lo,B),F(hi,B)
def power(x,q):
 q=F(q);return root(x**q.numerator,q.denominator)
def expi(x):
 if x<0:
  lo,hi=expi(-x);return down(1/hi),up(1/lo)
 count=0
 while x>F(1,16):x/=2;count+=1
 term=sm=F(1)
 for k in range(1,41):term=term*x/k;sm+=term
 nxt=term*x/41;lo=down(sm);hi=up(sm+nxt/(1-x/42))
 for _ in range(count):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi

def logi(x):
 assert x>0
 if x<1:
  a,b=logi(1/x);return -b,-a
 shift=0
 while x>=2:x/=2;shift+=1
 def unit(z):
  v=(z-1)/(z+1);sm=2*sum((v**(2*j+1)/F(2*j+1) for j in range(80)),F(0));tail=2*v**161/(161*(1-v*v));return down(sm),up(sm+tail)
 a,b=unit(x)
 if shift:
  c,d=unit(F(2));a+=shift*c;b+=shift*d
 return down(a),up(b)

def val(x):return {'exact':str(x),'display':float(x)}
old=P.parent/'uniform_transfer_moment_assessment';mf=json.loads(read(old/'MANIFEST_SHA256.json'));raw=read(old/'results.json');assert hashlib.sha256(raw).hexdigest()==mf['results.json'];data=json.loads(raw)
moms={s:{int(j):tuple(F(v['exact']) for v in iv) for j,iv in d['moment_intervals'].items()} for s,d in data['hankel_caps'].items()};caps={s:F(d['x_cap']['exact']) for s,d in data['hankel_caps'].items()};nodes={}
for s,h in caps.items():
 a,b,c=[sum(moms[s][j],F(0))/2 for j in (3,4,5)];raw=(h*b-c)/(h*a-b);nodes[s]=F((raw*10**10).__floor__(),10**10);assert 0<nodes[s]<h
BCACHE={}
def bounds(L):
 if L in BCACHE:return BCACHE[L]
 out=[]
 for s,h in caps.items():
  t=nodes[s];k=L//2-3;cc=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;bb=k*t**(k-1)-2*cc*t;aa=t**k-k*t**k+cc*t*t
  hermite=sum(c*moms[s][j][1 if c>=0 else 0] for c,j in zip((aa,bb,cc),(3,4,5)))
  M=moms[s][5][1];h5=h**5;q=M//h5;packed=q*h**(L//2)+power(M-q*h5,F(L,10))[1]
  out.append(min(up(hermite),up(packed)))
 a,b,c=out;BCACHE[L]=(a+2*b+3*c,a+2*b);return BCACHE[L]
anchor_dir=P.parent/'uniform_moment_optimality_assessment';mf=json.loads(read(anchor_dir/'MANIFEST_SHA256.json'));raw=read(anchor_dir/'anchors.out');assert hashlib.sha256(raw).hexdigest()==mf['anchors.out'];ints={k:int(v) for line in raw.decode().splitlines() for k,v in [line.split('=')]};R={n:F(ints[f'H0_{2*n}'],ints[f'N0_{2*n}'])+2*n*F(700741,500000) for n in (48,50)};assert all(r<0 for r in R.values())
G=lambda z:1-(1-z)**2/(2*z*z)
def fail_replay(s,t):
 hist=[]
 for j in range(32):
  if min(s,t)>=F(99,100):return None
  z=s*s*t;s=up(G(z));hist.append({'kind':'spatial','argument_upper':str(z),'output_upper':str(s)})
  if s<=0:return {'round':j+1,'kind':'spatial','history':hist}
  z=t*t*s;t=up(G(z));hist.append({'kind':'thermal','argument_upper':str(z),'output_upper':str(t)})
  if t<=0:return {'round':j+1,'kind':'thermal','history':hist}
 return None

allrows=[];total_boxes=0
selected_n=[int(s) for s in sys.argv[1].split(',')] if len(sys.argv)>1 else [48,50]
selected_ell=int(sys.argv[2]) if len(sys.argv)>2 else None
for n in selected_n:
 vhi=expi(-F(21,2)*R[n])[1];Q=bounds(2*n)[0];base=Q/vhi-1;assert 0<base<1;logbase=logi(base)[0];thermal_cache={}
 def Tup(r):
  if r not in thermal_cache:thermal_cache[r]=up(1/(1+expi(r*logbase)[0])**2)
  return thermal_cache[r]
 for ell in ([selected_ell] if selected_ell else range(10,n+1,2)):
  if ell>n:continue
  start=time.process_time();q=F(n,ell);p=2*q;z,e=bounds(ell);assert z>=e>1;logz=logi(z)[0];loge=logi(e)[0];tcoef=-F(21,2)*R[n]/p
  # D/t*=exp(r*(log z - tcoef)); r>=16 gives D/t*>=4.
  cold_log_lower=logz-tcoef;assert cold_log_lower>0 and expi(16*cold_log_lower)[0]>4
  assert G(F(1,16)**2)<0
  Dcache={};tcache={}
  def optimistic(a,b):
   if a not in Dcache:Dcache[a]=(expi(a*logz)[0],expi(a*loge)[0])
   if b not in tcache:tcache[b]=expi(b*tcoef)[1]
   D,E=Dcache[a];t=tcache[b];tau=(D+11*E)/12;tau0=(D+3*E)/4
   assert t<tau<=tau0<=D
   tails=[]
   for x,y in [(F(0),F(0)),(tau-t,F(0)),(tau-t,tau0-tau),(F(0),tau0-t)]:
    zz=D-t-x-y;assert min(x,y,zz)>=0
    tails.append(down(power(x,q)[0]+2*power(y/2,q)[0]+3*power(zz/3,q)[0]))
   tail=max(tails);den=power(t,q)[1];S=up(1/(1+tail/den)**2)
   return S,Tup(b)
  stack=[(F(1),F(16),0)];leaves=[];seen=0
  while stack:
   a,b,depth=stack.pop();S,T=optimistic(a,b);failure=fail_replay(S,T);seen+=1
   if failure:
    leaves.append({'r_lower':str(a),'r_upper':str(b),'S_upper':str(S),'T_upper':str(T),'failure':failure})
   else:
    assert depth<24,('unresolved box',n,ell,a,b,S,T)
    mid=(a+b)/2;stack.append((mid,b,depth+1));stack.append((a,mid,depth+1))
   if seen%50==0:
    (P/'CHECKPOINT.json').write_text(json.dumps({'status':'RUNNING','n':n,'ell':ell,'checked_boxes':seen,'pending_boxes':len(stack),'completed_parameter_families':len(allrows),'cpu_seconds':time.process_time()-START},indent=2)+'\n')
  leaves.sort(key=lambda v:F(v['r_lower']));assert F(leaves[0]['r_lower'])==1 and F(leaves[-1]['r_upper'])==16 and all(a['r_upper']==b['r_lower'] for a,b in zip(leaves,leaves[1:]));total_boxes+=len(leaves)
  rec={'n':n,'ell':ell,'anchor_shifted_R':str(R[n]),'z':str(z),'e':str(e),'Q':str(Q),'cold_from':'16','cold_D_over_t_lower':str(expi(16*cold_log_lower)[0]),'cold_S_upper':'1/16','closed_interval_leaves':leaves,'visited_boxes':seen,'cpu_seconds':time.process_time()-start};allrows.append(rec)
  (P/'partial_results.json').write_text(json.dumps({'status':'PARTIAL','families':allrows},indent=2)+'\n');print(json.dumps({'n':n,'ell':ell,'leaves':len(leaves),'max_failure_round':max(v['failure']['round'] for v in leaves),'cpu':rec['cpu_seconds']}),flush=True)
out={'status':'PASS all-r recipe-specific canonical startup exclusions','recipe':'Fixed accepted Hermite/packing envelope; even ell10..n; r>=1; exact one-MPS anchor; standard total-power leading forcing and arbitrary iteration of direct-sector-power tail forcing, then canonical sequential G; bridges granted free. No adaptive direction changes or other moment inequalities.','families':allrows,'selected_n':selected_n,'selected_ell':selected_ell,'leaf_count':total_boxes,'cpu_seconds':time.process_time()-START,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'anchor_review_status':'Independent supplement required/externally tracked; producer inputs hash-verified here'}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');(P/'CHECKPOINT.json').write_text(json.dumps({'status':'COMPLETE','leaf_count':total_boxes,'cpu_seconds':time.process_time()-START},indent=2)+'\n')
print(json.dumps({'status':out['status'],'families':len(allrows),'leaf_count':total_boxes,'cpu_seconds':out['cpu_seconds'],'maxrss_kib':out['maxrss_kib']}),flush=True)
