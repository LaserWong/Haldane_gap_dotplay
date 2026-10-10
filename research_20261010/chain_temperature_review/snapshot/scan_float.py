"""Bounded float diagnostic; never an accepted certificate."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json,math,resource
from pathlib import Path
from fractions import Fraction as F
resource.setrlimit(resource.RLIMIT_AS,(1500*1024**2,1500*1024**2))
OUT=Path(__file__).resolve().parent;BASE=OUT.parent/'chain_frontier'
def f(x):return float(F(x))
def G(x):return 1-(1-x)**2/(2*x*x) if x>0 else -1

def q(r,b):
 a=f(r['relative_form_bound']['alpha']);B=f(r['relative_form_bound']['B']);N=r['N_dimers'];u=f(r.get('ground_upper',r['exact_rayleigh']));l=f(r['ground_lower'])
 tail=math.exp(-b*(f(r['E00'])-B-u))*math.expm1(N*math.log1p(3*math.exp(-a*b)+5*math.exp(-3*a*b)))
 return math.exp(b*(u-l))+tail

def replay(S,T,n,b):
 for i in range(20):
  u=max(1-S,1-T)
  if u<=.01:return {'gap':math.log(1/(5*u))/b,'n':n,'beta':b,'S':S,'T':T}
  if S*S*T<=.5:return None
  S=G(S*S*T)
  if S<=0:return None
  T=G(T*T*S)
  if T<=0:return None
  n*=2;b*=2
 return None

def run(r,b):
 small,big=r['ground_certificates'];shift=f(big.get('ground_upper',big['exact_rayleigh']))-2*f(small['ground_upper'])
 q1=q(small,b);q2=q(small,2*b)
 J=math.exp(-2*b*shift)/q1**4;C=math.exp(-2*b*shift)/q2**2
 a=G(J)
 if a<=0:return None
 bb=G(C*C*a)
 if bb<=0:return None
 S=a*math.sqrt(bb);T=a*a*bb
 boot=replay(S,T,8,2*b)
 if boot:return dict(beta=b,J=J,C=C,a=a,b=bb,S=S,T=T,bootstrap=boot)

out={}
for g in ['323d2000','13d80','7d40','1d5']:
 p=BASE/f'chain_sparse_s1_g{g}_n4_depth4.json';r=json.loads(p.read_text());rows=[x for ib in range(4,641) if (x:=run(r,ib/4))]
 best=max(rows,key=lambda x:x['bootstrap']['gap']) if rows else None
 out[g]={'source':str(p),'accepted_float_count':len(rows),'best':best}
 print(g,len(rows),best,flush=True)
(OUT/'float_scan.json').write_text(json.dumps(out,indent=2)+'\n')
