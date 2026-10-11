#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(60,60));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_n28_second_initialization';ROOT=R.parent;B=10**140;H={}
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
seals={}
for name,h in [('uniform_n28_second_initialization','66c710bfc302c3f6a220a3162d933add710bfe51aef6fbcf1e256d6725430b55'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94')]:seals[name]=seal(R/name,h)
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(R/'uniform_smaller_second_initialization/long_certificate.json');core=js(R/'uniform_smaller_second_initialization_review/scalar_results.json');cert=js(A/'certificate.json')
assert F(L['N28']['bound'])==F(core['all_signed_majorants']['N28']['bound'])
M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()};U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);p=pack(m,h,F(n,12));return min(p,F(L[f'{s}{n}']['bound'])) if f'{s}{n}' in L else p
ours=ints(P/'anchors.out');prod=ints(A/'anchor56.out');assert {k:v for k,v in ours.items() if k.endswith('_56')}==prod
assert rd(P/'d26_blocks.txt')==rd(ROOT/'audit/mps/mps_blocks.txt');rebuild=js(P/'independent_d26.json');assert rebuild['D']==26 and rebuild['status']=='PASS'
old=ints(R/'mps_excited_seed_witnesses/ground_lengths.out');assert all(ours[k]==old[k] for k in ('H0_48','N0_48'))
N,H0=ours['N0_56'],ours['H0_56'];assert N>0;ray=F(H0,N)+56*F(700741,500000);assert ray<0
r=cert['n28_gap_0179_test'];assert ray==F(r['anchor_shifted_Rayleigh']);ell=F(r['ell']);force=1-pack(mj,ell**12,F(56,12))-3*sector('N',56);assert 0<F(r['forcing_margin'])<=force and ell>max(V,F(C['filters']['J-']['cap'])) and 0<mj-ell**12<ell**12
Q=sector('J',56)+3*sector('N',56);tail=power(mj-ell**12,F(28,12))[1]+3*sector('N',28);s0=(1+tail/ell**28)**-2;t0=Q**-2;assert 0<F(r['S'])<=s0<1 and 0<F(r['T'])<=t0<1
w=cert['direct_window'];assert w==r['windows'][0] and (w['from'],w['to'])==(28,56)
s,t=F(r['S']),F(r['T']);K=s*s*t;assert K>F(1,2);root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=(1-rho)*min(s*power(d,F(1,2))[0],d);cc=F(w['purity']);margin=cc-exp_upper(F(49,4)*F(179,10000))*(1-cc);assert F(1,2)<cc<=own and 0<F(w['margin'])<=margin
core30=next(x for x in core['rows'] if x['n']==30);assert core30['gap']=='179/10000' and core30['all_integer_L_at_least']==30;assert 28<=30<=56
assert cert['combined_claim']=={'gap':'179/10000','all_integer_L_at_least':28,'unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':28,'union':['28..56 direct window','30..infinity inherited smaller initialization']}
# Reproduce literal failed arithmetic at the producer's grid; this is not a
# physical upper bound or an impossibility statement.
BB=10**100
def dn(x):return F(x.numerator*BB//x.denominator,BB)
def sqlo(x):return F(math.isqrt(x.numerator*BB**2//x.denominator),BB)
def window(s,t):
 k=dn(s*s*t);assert k>F(1,2);rr=sqlo(2*k-1);rho=(1-rr)/(1+rr);dd=dn(t/(1+rho*rho));return dn((1-rho)*min(s*sqlo(dd),dd))
diagnostics=[]
for key in ['n28_zero_gap_continuation_test','n28_gap_0179_test']:
 z=cert[key];assert z['status']=='FAIL_window' and F(z['S'])==F(r['S']) and F(z['T'])==F(r['T']);s,t=F(z['S']),F(z['T'])
 for j,st in enumerate(z['states']):
  assert F(st['S'])==s and F(st['T'])==t and st['n']==28*2**j and F(st['beta'])==F(49,4)*2**j
  assert window(s,t)==F(z['windows'][j]['purity']);k=dn(s*s*t);s=dn(G(k));t=dn(G(dn(t*t*s)))
 assert z['round']==len(z['states']) and window(s,t)==F(z['purity'])
 if F(z['gap'])==0:assert F(z['purity'])<F(1,2)
 else:assert F(z['purity'])-exp_upper(F(49,4)*2**z['round']*F(z['gap']))*(1-F(z['purity']))<0
 diagnostics.append({'gap':z['gap'],'failed_round':z['round'],'literal_lower_purity':z['purity'],'scope':'failure of these particular lower bounds only'})
pilot=js(A/'cooling_pilot.json');assert pilot['tested_n']==28
out={'status':'ACCEPTED finite-window bridge and composition; no n28 bootstrap startup','gap':'179/10000','direct_integer_window':[28,56],'all_integer_L_at_least':28,'unique_ground_state':True,'bootstrap_initialization':30,'anchor56_shifted_total_Rayleigh':str(ray),'purity_lower':str(cc),'strict_gap_margin':str(margin),'literal_failed_continuations':diagnostics,'floating_pilot_scope':'proposal-only bounded scan; no all-temperature exclusion or minimum theorem','seals':seals,'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all_integer_L_at_least','bootstrap_initialization','resources']},indent=2))
