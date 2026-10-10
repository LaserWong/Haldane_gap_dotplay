"""Floating proposals only. No diagnostic is a certificate or exclusion."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json,math,resource
from fractions import Fraction as Q
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));HERE=Path(__file__).resolve().parent
f=lambda x:float(Q(x))
def G(p):return 1-(1-p)**2/(2*p*p) if 0<p<=1 else -1

def trace(s,b):
 a=f(s['relative_form_bound']['alpha']);B=f(s['relative_form_bound']['B']);rho=f(s['exact_rayleigh']);lo=f(s['ground_lower'])
 return math.exp(b*(rho-lo))+math.exp(-b*(-8-B-rho))*math.expm1(4*math.log1p(3*math.exp(-a*b)+5*math.exp(-3*a*b)))
def interpolate(S,T,beta,P=None):
 p=S*S*T if P is None else P
 if p<=.5:return -1
 w=(1+math.sqrt(2*p-1))/2;r=(1-w)/w;D=T/(1+r*r);I=(1-r)*min(S*math.sqrt(D),D)
 return math.log(I/(1-I))/beta if .5<I<1 else -1

def run(s,rho8,beta):
 shift=rho8-f(s['exact_rayleigh'])*2;L=math.exp(-2*beta*shift);J=L/trace(s,beta)**4;C=L/trace(s,2*beta)**2
 a=G(J);b=G(C*C*a) if a>0 else -1
 if b<=0:return None
 best=None;lim=100;nn=8;be=2*beta
 for tsteps in range(8):
  S=a*math.sqrt(b);T=a*a*b
  if S<=0 or T<=0:break
  # Try conversion here followed by any further canonical rounds.
  SS,TT=S,T;PP=a*a*b;mm=nn;bb=be;ww=lim
  for csteps in range(8):
   u=max(1-SS,1-TT)
   if 1e-15<u<=.01:
    asym=math.log(1/(5*u))/bb;gap=min(asym,ww)
    cand=dict(beta=beta,time_steps=tsteps,canonical_steps=csteps,from_M=mm,all_M_ge8_gap=gap,asymptotic_gap=asym,finite_window_min=ww,time_pair_at_conversion=[a,b])
    if best is None or gap>best['all_M_ge8_gap']:best=cand
   wgap=interpolate(SS,TT,bb,PP)
   if wgap<=0:break
   ww=min(ww,wgap)
   SS=G(PP);TT=G(TT*TT*SS) if SS>0 else -1;PP=SS*SS*TT
   if SS<=0 or TT<=0:break
   mm*=2;bb*=2
  wgap=interpolate(S,T,be,a*a*b)
  if wgap<=0:break
  lim=min(lim,wgap)
  a=G(a*a*b);b=G(b*b*a) if a>0 else -1
  if a<=0 or b<=0:break
  nn*=2;be*=2
 return best

def main():
 out=[]
 for rec in json.loads((HERE/'inputs.json').read_text()):
  rows=[r for k in range(40,1601) if (r:=run(rec['small'],f(rec['large']['exact_rayleigh']),k/20))]
  best=max(rows,key=lambda x:x['all_M_ge8_gap']) if rows else None
  out.append(dict(g=rec['g'],number_passes=len(rows),best=best));print(out[-1],flush=True)
 (HERE/'float_orders.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
