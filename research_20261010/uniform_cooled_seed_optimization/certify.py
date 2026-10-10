#!/usr/bin/env python3
"""Exact scalar cooled-sector candidates; no physical eigensolver."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**24;tstart=time.process_time()
allowed=os.sched_getaffinity(0);os.sched_setaffinity(0,{next((c for c in (0,5) if c in allowed),min(allowed))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
hashes={}
def read(p):
 p=Path(p);data=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(data).hexdigest();return data

def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def roots(x,q):
 assert x>=0
 if q==1:return down(x),up(x)
 lo=0;hi=B
 while F(hi,B)**q<x:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if F(mid,B)**q<=x:lo=mid
  else:hi=mid
 l,u=F(lo,B),F(hi,B);assert l**q<=x<=u**q;return l,u

def power(x,r):
 r=F(r);return roots(x**r.numerator,r.denominator)
def expi(x):
 if x<0:
  l,u=expi(-x);return down(1/u),up(1/l)
 k=0
 while x>F(1,16):x/=2;k+=1
 term=s=F(1)
 for j in range(1,50):term=term*x/j;s+=term
 nxt=term*x/50;l=down(s);u=up(s+nxt/(1-x/51))
 for _ in range(k):l=down(l*l);u=up(u*u)
 return l,u

def val(x):return {'exact':str(x),'display':float(x)}
old=P.parent/'uniform_transfer_moment_assessment';manifest=json.loads(read(old/'MANIFEST_SHA256.json'));raw=read(old/'results.json');assert hashlib.sha256(raw).hexdigest()==manifest['results.json'];d=json.loads(raw)
caps={s:F(v['x_cap']['exact']) for s,v in d['hankel_caps'].items()};m5={s:F(v['moment_intervals']['5'][1]['exact']) for s,v in d['hankel_caps'].items()}
def sector(s,L):
 x=caps[s];h=x**5;M=m5[s];q=M//h;return up(q*x**(L//2)+power(M-q*h,F(L,10))[1])
def bounds(L):
 a,b,c=[sector(s,L) for s in ['trivial','complex','vector']];return a+2*b+3*c,a+2*b

def ints(path):return {k:int(v) for l in read(path).decode().splitlines() for k,v in [l.split('=')]}
new=ints(P/'new_lengths.out');benchmark=ints(P/'benchmark48.out');arch=ints(ROOT/'research_20261010/mps_excited_seed_witnesses/ground_lengths.out');assert benchmark['H0_48']==arch['H0_48'] and benchmark['N0_48']==arch['N0_48']
for L in (104,108,112,120):
 assert new[f'N0_{L}']>0 and F(new[f'H0_{L}'],new[f'N0_{L}'])+L*F(700741,500000)<0
oldmps=ints(ROOT/'audit/mps/contraction.out');assert new['H0_120']==120*oldmps['U120'] and new['N0_120']==oldmps['V120']
read(ROOT/'audit/mps/mps_blocks.txt');read(P/'contract_ground.cpp')
G=lambda z:1-(1-z)**2/(2*z*z)

def candidate(n,l,r,gap,mode):
 assert l%2==0 and n%2==0 and n>=l
 R=F(new[f'H0_{2*n}'],new[f'N0_{2*n}'])+2*n*F(700741,500000);assert R<0
 z,p=bounds(l);D=power(z,r)[1];E=power(p,r)[1];tau=(D+11*E)/12;tau0=(D+3*E)/4
 assert D>=tau0>=tau>0
 q=F(n,l);pp=2*q
 def tail(t,exponent):
  assert t<tau
  vs=[]
  for x,y in [(F(0),F(0)),(tau-t,F(0)),(tau-t,tau0-tau),(F(0),tau0-t)]:
   zz=D-t-x-y;assert min(x,y,zz)>=0
   # repeated two/three-copy sectors: y^p/2^(p-1)=2*(y/2)^p.
   vs.append(up(power(x,exponent)[1]+2*power(y/2,exponent)[1]+3*power(zz/3,exponent)[1]))
  return max(vs)
 # Initial largest-weight t bound uses 1<Z_(2n)<=t^(pp-1)*D.
 t=F(4,5)
 assert D*power(t,pp-1)[1]<1 and 2*t>D
 hist=[{'t_lower':val(t),'proof':'D*t^(p-1)<1; unique unit-multiplicity leading atom in trivial sector'}]
 for _ in range(16):
  rem=tail(t,F(2))**2 if mode=='original_squared_tail' else tail(t,pp)
  assert rem<1
  proposed=power(1-rem,1/pp)[0]
  # Exact outward lower root, rounded down one extra grid unit for a strict contradiction.
  proposed=down(proposed)-F(1,B)
  if proposed<=t:break
  bound=power(proposed,pp)[1]+rem
  assert bound<1
  t=proposed;hist.append({'t_lower':val(t),'contradiction_upper':val(bound)})
 # Original route requires n=2l and p=4. General route uses direct sector convexity at q,p.
 if mode=='original_squared_tail':assert q==2
 tail_n=tail(t,q);S=down(1/(1+tail_n/power(t,q)[0])**2)
 Q=bounds(2*n)[0];assert Q>1
 T=down(1/(1+power(Q-1,r)[1])**2)
 beta=F(21,2)*r;states=[];windows=[];sn,tn=S,T;nn=n;bt=beta
 for j in range(32):
  state={'round':j,'n':nn,'beta':val(bt),'S':val(sn),'T':val(tn)};states.append(state)
  # Every early integer window is independently checked with the signed-spectrum lemma.
  pure=sn*sn*tn;assert pure>F(1,2)
  w=(1+roots(2*pure-1,2)[0])/2;rr=(1-w)/w;di=tn/(1+rr*rr)
  C=down((1-rr)*min(sn*roots(di,2)[0],di));assert C>F(1,2)
  e=expi(bt*gap)[1];margin=C-e*(1-C);assert margin>0
  windows.append({'from':nn,'to':2*nn,'beta':val(bt),'thermal_purity_lower':val(C),'gap':val(gap),'exponential_margin':val(margin)})
  u=max(1-sn,1-tn)
  if u<=F(1,100):
   margin=1-5*u*e;assert margin>0
   asym={'from':nn,'beta':val(bt),'common_defect':val(u),'gap':val(gap),'exponential_margin':val(margin)};break
  sn=down(G(sn*sn*tn));assert sn>0
  tn=down(G(tn*tn*sn));assert tn>0
  nn*=2;bt*=2
 else:raise AssertionError('No asymptotic entry')
 return {'status':'PRODUCER exact scalar and all-integer bridges PASS; independent review pending','seed_n':n,'base_moment_length':l,'cooling_ratio':val(r),'beta':val(beta),'mode':mode,'anchor_length':2*n,'anchor_shifted_Rayleigh':val(R),'D':val(D),'E':val(E),'tau':val(tau),'tau0':val(tau0),'dominant_mass_steps':hist,'Z_anchor_beta0_upper':val(Q),'S_seed':val(S),'T_seed':val(T),'states':states,'finite_integer_windows':windows,'asymptotic':asym,'claimed_scope':f'all integer periodic L >= {n}','gap':val(gap),'below_seed':'Not certified here; no minimum-seed claim'}
rows=[candidate(60,30,F(5,2),F(102,10000),'original_squared_tail'),candidate(56,28,F(58,25),F(68,10000),'original_squared_tail'),candidate(54,28,F(113,50),F(25,10000),'direct_sector_power')]
result={'status':'PASS producer candidates; independent review required','rows':rows,'resources':{'cpu_seconds':time.process_time()-tstart,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'address_space_limit':700*1024**2}}
(P/'certificates.json').write_text(json.dumps(result,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({'rows':[{'n':x['seed_n'],'beta':x['beta']['display'],'gap':x['gap']['display'],'S':x['S_seed']['display'],'T':x['T_seed']['display'],'asymptotic_from':x['asymptotic']['from']} for x in rows],'resources':result['resources']},indent=2))
