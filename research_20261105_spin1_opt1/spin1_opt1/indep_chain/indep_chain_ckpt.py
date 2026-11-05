# Independent exact-rational re-derivation of the n=34 scalar chain (a_uniform/improve.py logic, written
# separately from the repo audit_scalar.py), extended to W windows with a configurable rounding grid B=10^DIGITS.
# Only change vs improve.py: B from env DIGITS (directed rounding unchanged; finer grid is still sound).
# usage: DIGITS=d python3 indep_chain.py MODE(Z1|FULL) W GAP [ELL]
# Independent re-run of the n=34 tail certificate (audit_scalar.py logic) with optional use of the
# full anchor Rayleigh value: Z_68(b) >= exp(-b R68) instead of Z_68(b) > 1. Reads repo data only.
import sys,json,math
from fractions import Fraction as F
from functools import lru_cache
sys.set_int_max_str_digits(0)
ROOT='/workspace/repos/Haldane_gap_dotplay/research_20261010/'
import os
B=10**int(os.environ.get('DIGITS','600'))
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return -down(-x)
@lru_cache(None)
def power(x,r):
 r=F(r);p,q=r.numerator,r.denominator;z=x**p;scaled=z.numerator*B**q//z.denominator
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
def exp_lower(x):  # x>=0 small: truncated Taylor is a lower bound
 term=total=F(1)
 for j in range(1,40):term*=x/j;total+=term
 return down(total)
def pack(m,h,r):
 q=m//h;return up(q*power(h,r)[1]+power(m-q*h,r)[1])
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
js=lambda p:json.load(open(ROOT+p))
C=js('uniform_second_moment_optimization/certificate.json');L=js('uniform_smaller_second_initialization/long_certificate.json')
cert=js('uniform_smaller_second_initialization/certificate.json')
M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
ints=lambda p:{k:int(v) for k,v in (l.split('=') for l in open(ROOT+p).read().splitlines())}
A=ints('uniform_smaller_second_initialization_review/anchors.out')
n=34;b0=F(49,4)
row=[r for r in cert['rows'] if r['n']==n][0]
R=F(A['H0_68'],A['N0_68'])+68*F(700741,500000);assert R==F(row['shifted_Rayleigh'])
print('R68 =',float(R))
def seed(full,ell=None):
 Z1=exp_lower(-b0*R) if full else F(1); Z2=exp_lower(-2*b0*R) if full else F(1)
 N2=3*sector('N',2*n)
 if ell is None:
  # largest ell (10^-10 grid) with pack(mj,ell^12,68/12)+N2 < Z1 and 0<mj-ell^12<ell^12
  lo,hi=F(9*10**9,10**10),F(10**10,10**10)
  for _ in range(40):
   mid=down((lo+hi)/2); 
   if pack(mj,mid**12,F(2*n,12))+N2<Z1: lo=mid
   else: hi=mid
  ell=F(math.floor(lo*10**10),10**10)
 assert pack(mj,ell**12,F(2*n,12))+N2<Z1 and 0<mj-ell**12<ell**12 and ell>max(F(C['filters']['J-']['cap']),V)
 tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',2*n)+3*sector('N',2*n)
 return ell,(1+tail/ell**n)**-2, Z2/Q**2
def chain(S,T,gap,extra=10,W=None):
 W=W or WMAX
 s,t=down(S),down(T);size=n;beta=b0;best=None
 for j in range(W):
  K=s*s*t
  if not K>F(1,2):return False,f'K<=1/2 at {size}',None
  root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=(1-rho)*min(s*power(d,F(1,2))[0],d)
  if own-exp_upper(beta*gap)*(1-own)<=0:return False,f'window {size}-{2*size} fails',None
  u=max(1-s,1-t)
  if u<=F(1,100):
   fac=5*u*exp_upper(beta*gap)
   if j+1==W or (FREE and (best is None or fac<best[2])):best=(fac<1,f'asym from L={size} beta={beta} u={float(u):.6g} windows={j+1}',fac)
  s=down(G(s*s*t));t=down(G(t*t*s));size*=2;beta*=2
 return best

import time,os,json
t0=time.process_time()
mode,W,g=sys.argv[1],int(sys.argv[2]),F(sys.argv[3]);full=(mode=='FULL')
gap=g;WMAX=W;FREE=False
ck=f'ckpt_{mode}_W{W}_{str(g).replace("/","_")}_d{str(B).count("0")}.json'
# Resumable copy of chain(): identical per-window logic; exact state (j,s,t) saved after each window.
if os.path.exists(ck):
 c=json.load(open(ck));j0=c['j'];s,t=F(c['s']),F(c['t']);print('resume at window',j0,flush=True)
else:
 # seed lower bounds (S,T) are valid on any grid; computed on the coarser grid SEED_DIGITS (default 600) and
 # stored exactly; a 10^-600-grid rational is also a 10^-DIGITS-grid rational, so the chain continues soundly.
 sd_=int(os.environ.get('SEED_DIGITS','600'));Bfull=B;B=10**sd_;power.cache_clear();exp_upper.cache_clear()
 ell,S,T=seed(full,None);s,t=down(S),down(T);B=Bfull;power.cache_clear();exp_upper.cache_clear()
 assert s>0 and t>0 and (s*Bfull).denominator==1 and (t*Bfull).denominator==1
 print(mode,'W',W,'digits',str(B).count('0'),'seed_digits',sd_,'ell',ell,'S',float(S),'T',float(T),flush=True)
 j0=0
size=n*2**j0;beta=b0*2**j0;res=None
for j in range(j0,W):
 K=s*s*t
 if not K>F(1,2):res=(False,f'K<=1/2 at {size}');break
 root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=(1-rho)*min(s*power(d,F(1,2))[0],d)
 if own-exp_upper(beta*gap)*(1-own)<=0:res=(False,f'window {size}-{2*size} fails');break
 print('window',j,size,'ok cpu %.0f'%(time.process_time()-t0),flush=True)
 u=max(1-s,1-t)
 if j+1==W:
  assert u<=F(1,100);fac=5*u*exp_upper(beta*gap);res=(fac<1,f'asym from L={size} beta={beta} windows={j+1} u>0:{u>0}',float(fac));break
 s=down(G(s*s*t));t=down(G(t*t*s));size*=2;beta*=2
 json.dump({'j':j+1,'s':str(s),'t':str(t)},open(ck+'.tmp','w'));os.replace(ck+'.tmp',ck)
 if time.process_time()-t0>400:print('checkpoint; rerun to resume',flush=True);sys.exit(3)
if res:print('gap',g,'ACCEPTED' if res[0] else 'REJECTED',res[1:],'cpu %.1fs'%(time.process_time()-t0),flush=True)
