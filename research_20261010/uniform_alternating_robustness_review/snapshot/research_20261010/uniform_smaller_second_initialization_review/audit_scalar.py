#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(60,60));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_smaller_second_initialization';ROOT=R.parent;B=10**140;H={}
def rd(p):
 b=p.read_bytes();H[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(rd(p))
def seal(p,h):
 assert hashlib.sha256(rd(p/'MANIFEST_SHA256.json')).hexdigest()==h
 for f,v in js(p/'MANIFEST_SHA256.json').items():assert hashlib.sha256(rd(p/f)).hexdigest()==v
 return h
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return -down(-x)
@lru_cache(None)
def power(x,r):
 r=F(r);assert x>=0 and r>0;p,q=r.numerator,r.denominator;z=x**p;scaled=z.numerator*B**q//z.denominator
 if q==1:k=scaled
 elif q==2:k=math.isqrt(scaled)
 else:
  lo=0;hi=1<<((scaled.bit_length()+q-1)//q)
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**q<=scaled:lo=mid
   else:hi=mid
  k=lo
 l,u=F(k,B),F(k+1,B);assert l**q<=z<=u**q;return l,u
@lru_cache(None)
def exp_upper(x):
 assert x>=0;k=0
 while x>F(1,8):x/=2;k+=1
 term=total=F(1)
 for j in range(1,161):term*=x/j;total+=term
 upper=up(total+(term*x/161)/(1-x/162))
 for j in range(k):upper=up(upper*upper)
 return upper
@lru_cache(None)
def pack(m,h,r):
 assert m>=0 and h>0 and r>=1;q=m//h
 return up(q*power(h,r)[1]+power(m-q*h,r)[1])
def bernstein(poly,a,b):
 d=len(poly)-1
 co=[sum(poly[j]*math.comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,d+1)) for k in range(d+1)]
 row=[sum(co[k]*F(math.comb(i,k),math.comb(d,k)) for k in range(i+1)) for i in range(d+1)];pending=[(row,0)];leaves=depth=0
 while pending:
  row,level=pending.pop()
  if min(row)>=0:leaves+=1;depth=max(depth,level);continue
  assert row[0]>=0 and row[-1]>=0 and level<30
  tri=[row]
  while len(tri[-1])>1:tri.append([(a+b)/2 for a,b in zip(tri[-1][:-1],tri[-1][1:])])
  pending.extend([([v[0] for v in tri],level+1),([v[-1] for v in tri[::-1]],level+1)])
 return leaves,depth
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
def ints(p):return {k:int(v) for k,v in (l.split('=') for l in rd(p).decode().splitlines())}
producer_hash=(P/'PRODUCER_MANIFEST_SHA256.txt').read_text().strip();seal(A,producer_hash)
seals={A.name:producer_hash}
for name,h in [('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94'),('uniform_second_moment_review','dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de'),('uniform_second_moment_optimization','dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85')]:seals[name]=seal(R/name,h)
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(A/'long_certificate.json');cert=js(A/'certificate.json');M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
# Reconstruct every advertised signed long-moment majorant, not its floating proposals.
majorants={}
for key,v in L.items():
 s=key[0];n=int(key[1:]);q=list(map(F,v['coeff']));assert len(q)==9 and n>=12 and n%2==0
 a=-F(C['filters'][s+'-']['cap']);b=F(C['filters'][s+'+']['cap']);poly=q+[F(0)]*(n-3-len(q));poly[-1]-=1
 leaves,depth=bernstein(poly,a,b);bound=sum(c*(u if c>=0 else l) for c,(l,u) in zip(q,M[s]));assert bound==F(v['bound']) and (leaves,depth)==(v['bernstein_leaf_count'],v['bernstein_max_depth'])
 majorants[key]={'bound':str(bound),'leaves':leaves,'depth':depth}
U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
ours=ints(P/'anchors.out');prod=ints(A/'anchors.out');prod.update(ints(A/'anchor60.out'));assert ours==prod and set(ours)=={f'{t}_{n}' for t in ('H0','N0') for n in (60,64,68)}
assert (P/'d26_blocks.txt').read_bytes()==rd(ROOT/'audit/mps/mps_blocks.txt');assert js(P/'independent_d26.json')['D']==26
rows=[]
assert {r['n'] for r in cert['rows']}=={30,32,34}
for row in cert['rows']:
 n=row['n'];gap=F(row['gap']);assert row['status']=='PASS_PRODUCER' and row['all_integer_L_at_least']==n and row['unique_ground_state'] and row['anchor_length']==2*n
 norm=ours[f'N0_{2*n}'];energy=ours[f'H0_{2*n}'];assert norm>0;ray=F(energy,norm)+2*n*F(700741,500000);assert ray==F(row['shifted_Rayleigh'])<0
 ell=F(row['ell']);force=1-pack(mj,ell**12,F(2*n,12))-3*sector('N',2*n);assert 0<F(row['forcing_margin'])<=force
 assert ell>max(F(C['filters']['J-']['cap']),V) and 0<mj-ell**12<ell**12
 tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',2*n)+3*sector('N',2*n)
 S=(1+tail/ell**n)**-2;T=Q**-2;assert tail<=F(row['tail']) and Q<=F(row['Q']);assert 0<F(row['S'])<=S<=1 and 0<F(row['T'])<=T<=1
 states=row['states'];windows=row['windows'];assert len(states)==len(windows);prev=None;margins=[]
 for j,(st,w) in enumerate(zip(states,windows)):
  size=n*2**j;beta=F(49,4)*2**j;s,t=F(st['S']),F(st['T']);assert st['n']==size and F(st['beta'])==beta and 0<s<=1 and 0<t<=1
  if prev is None:assert s==F(row['S']) and t==F(row['T'])
  else:assert s<=G(prev[0]**2*prev[1]) and t<=G(prev[1]**2*s)
  K=s*s*t;assert K>F(1,2);root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=(1-rho)*min(s*power(d,F(1,2))[0],d)
  lower=F(w['purity']);assert F(1,2)<lower<=own and (w['from'],w['to'])==(size,2*size)
  margin=lower-exp_upper(beta*gap)*(1-lower);assert 0<F(w['margin'])<=margin;margins.append(str(margin));prev=s,t
 asym=row['asymptotic'];u=max(1-s,1-t);assert asym['from']==size and F(asym['beta'])==beta and F(asym['defect'])==u<=F(1,100)
 margin=1-5*u*exp_upper(beta*gap);assert 0<F(asym['margin'])<=margin
 rows.append({'n':n,'gap':str(gap),'all_integer_L_at_least':n,'unique_ground_state':True,'anchor_length':2*n,'anchor_shifted_total_Rayleigh':str(ray),'positive_leader_lower':str(ell),'forcing_margin':str(force),'S_seed':row['S'],'T_2n_seed':row['T'],'window_count':len(states),'window_margins':margins,'asymptotic_from':size,'asymptotic_beta':str(beta),'asymptotic_margin':str(margin)})
# Domain conditions for inherited small-defect continuation.
e=F(1,100);assert (3-3*e+e*e)**2/(2*(1-e)**6)<=5 and (2+5*e)**2/(2*(1-2*e-5*e*e)**2)<=5
out={'status':'ACCEPTED exact scalar chains with freshly rebuilt physical anchors and locally reproduced thermal inputs','rows':rows,'all_signed_majorants':majorants,'seals':seals,'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'CPU_affinity':4},'no_minimum_claim':True}
(P/'scalar_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'SCALAR_INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({'status':out['status'],'rows':[{k:r[k] for k in ('n','gap','asymptotic_from')} for r in rows],'resources':out['resources']},indent=2))
