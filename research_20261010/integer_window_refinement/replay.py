"""Length-resolved signed-transfer lemma tests and saved-input scalar replay.
No Hamiltonian construction, physical eigensolver, or predecessor writes.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json, math, time, resource, hashlib, random
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
available=os.sched_getaffinity(0); os.sched_setaffinity(0,{7 if 7 in available else min(available)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parent/'chain_frontier_rank195/expanded_inputs.json'
B=128; SCALE=1<<B

def down(x):return F(x.numerator*SCALE//x.denominator,SCALE)
def up(x):return -down(-x)
def nthfloor(x,n):
 lo=0;hi=1<<((x.bit_length()+n-1)//n)
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**n<=x:lo=mid
  else:hi=mid
 return hi if hi**n<=x else lo

def powerbox(x,m,n):
 assert x>=0
 v=x**m;z=v.numerator*SCALE**n//v.denominator;k=nthfloor(z,n)
 return F(k,SCALE),F(k+1,SCALE)
@lru_cache(maxsize=2048)
def expbox(x):
 if x<0:
  lo,hi=expbox(-x);return down(1/hi),up(1/lo)
 k=0
 while x>F(1,16):x/=2;k+=1
 term=v=F(1)
 for j in range(1,65):term=term*x/j;v+=term
 nxt=term*x/65;lo=down(v);hi=up(v+nxt/(1-x/66))
 for _ in range(k):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi

def G(x):return down(1-(1-x)**2/(2*x*x))
def wlower(b):return (1+powerbox(2*b-1,1,2)[0])/2

def lower(a,b,M,n):
 assert b>F(1,2) and n%2==0 and n<=M<=2*n
 w=wlower(b);factor=powerbox(w,M,n)[0]
 if M%2:factor-=powerbox(1-w,M,n)[1]
 return down(powerbox(a,M,n)[0]*factor)

def trace(s,beta):
 info=s['expanded_band'];rho=F(s['exact_rayleigh']);lo=F(s['ground_lower']);alpha=F(info['alpha']);bb=F(info['B'])
 out=expbox(beta*(rho-lo))[1]
 out+=sum(row['multiplicity']*expbox(beta*(rho+8-F(row['lower'])))[1] for row in info['comparison_endpoints'][1:])
 out+=sum(mult*expbox(beta*(rho+8-alpha*e+bb))[1] for e,mult in info['complete_reference_bins'] if e>=info['omitted_reference_excitation'])
 return up(out)

def toys():
 # Two-state positive-entry symmetric classical transfers with signed eigenvalues.
 # Z_M(beta)=(u+v)^M+(u-v)^M; Z_M(2beta)=(u²+v²)^M+(u²-v²)^M.
 checks=0;signed=0;minimum_margin=1.0
 for u in range(1,9):
  for v in range(1,9):
   for n in [2,4,8]:
    X=[F(u+v),F(u-v)];Y=[F(u*u+v*v),F(u*u-v*v)]
    zx=lambda M:sum(x**M for x in X)
    zy=lambda M:sum(x**M for x in Y)
    a=zy(n)/zx(n)**2;b=zy(2*n)/zy(n)**2
    if b<=F(1,2):continue
    for M in range(n,2*n+1):
     exact=zy(M)/zx(M)**2;lb=lower(a,b,M,n)
     assert exact>=lb,(u,v,n,M)
     checks+=1;signed+=(u<v);minimum_margin=min(minimum_margin,float(exact-lb))
 return dict(exact_rational_inequalities=checks,negative_subleading_spectrum_checks=signed,minimum_margin=minimum_margin)

def main():
 start=time.monotonic();toy=toys();rec=json.loads(SOURCE.read_text())[0];assert rec['g']=='1/4';s=rec['small'];delta=F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']);beta=F(942,125)
 L=expbox(-2*beta*delta)[0];J=down(L/trace(s,beta)**4);C=down(L/trace(s,2*beta)**2);a=G(J);b=G(down(C*C*a));P=down(a*a*b)
 assert b>F(1,2)
 uniform=down(a*a*powerbox(2*b-1,1,2)[0]);initial=down(J*powerbox(2*C-1,1,2)[0]);lc=s['relative_form_bound']['local_certificate'];short=[1-2*F(lc['a'])-M*F(lc['b']) for M in [2,3]]
 assert min(short)>F(1,100)
 assert expbox(2*beta/F(100))[1]<uniform/(1-uniform)
 assert expbox(beta/F(100))[1]<initial/(1-initial)
 rows=[]
 for M in range(8,17):
  lb=lower(a,b,M,8)
  if M==8:lb=max(lb,a)
  if M==16:lb=max(lb,P)
  assert lb>F(1,2)
  # A shared safely small rational gap, verified without logarithms.
  gap=F(1,100)
  assert expbox(2*beta*gap)[1]<lb/(1-lb)
  rows.append(dict(M=M,purity_lower=str(lb),purity_display=float(lb),gap_lower=str(gap)))
 nexta=G(P);nextarg=down(b*b*nexta);nextb=G(nextarg)
 out=dict(status='EXACT_FIRST_INTEGER_WINDOW_PASS_NOT_ALL_SIZE',g='1/4',initial_beta=str(beta),window_beta=str(2*beta),a=str(a),b=str(b),P=str(P),display=dict(a=float(a),b=float(b),P=float(P)),rows=rows,uniform_window_lower=str(uniform),uniform_window_display=float(uniform),initial_M4_M8_lower=str(initial),initial_window_display=float(initial),short_M2_M3=list(map(str,short)),finite_scope='Every integer 2<=M<=16 has gap >=1/100 from inherited inputs and the new lemma; this is not all-size.',next_time_cycle=dict(a=str(nexta),b_argument=str(nextarg),b=str(nextb),display=[float(nexta),float(nextarg),float(nextb)]),toys=toy,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
