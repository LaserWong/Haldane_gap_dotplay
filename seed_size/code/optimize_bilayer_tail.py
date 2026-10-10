"""Optimize the rigorous half-spin bilayer thermal tail over local form a.

The exact 16x16 local eigenvalue formula is in root_review/BILAYER_LOCAL_ANALYTIC.md.
Floating minimization proposes a rational a; a dyadic square-root upper bound
and exact rational exp enclosures certify the chosen local/thermal bound.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from math import exp,log,log1p,expm1,sqrt,isqrt
import json
from scipy.optimize import minimize_scalar
from certified_core import down,up,exp_bounds
from axis_order_search import ordered_bilayer,ROOT,OUT,nodes,record_for

def sqrt_bounds(x,bits=128):
 x=Q(x);scale=1<<bits;k=isqrt(x.numerator*scale*scale//x.denominator)
 lo=Q(k,scale);return lo,lo if lo*lo==x else Q(k+1,scale)

@lru_cache(maxsize=10000)
def local_for_beta(g,N,beta):
 g,beta=Q(g),Q(beta)
 def score(a):
  b=sqrt(a*a-a*float(g)+float(g*g))-a+float(g)/2
  t=N*log1p(3*exp(-float(beta)*(1-4*a)))
  return float(beta)*2*N*b+log(expm1(t))
 opt=minimize_scalar(score,bounds=(float(g)/2,.249999),method='bounded',options={'xatol':1e-12})
 a=Q(round(opt.x*10**10),10**10);a=max(a,g/2);assert a<Q(1,4)
 b=up(sqrt_bounds(a*a-a*g+g*g)[1]-a+g/2)
 alpha=1-4*a;B=2*N*b
 return a,b,alpha,B

@lru_cache(maxsize=20000)
def q_cached(g,N,elo,U,E00,beta):
 g,N,elo,U,E00,beta=Q(g),int(N),Q(elo),Q(U),Q(E00),Q(beta)
 a,b,alpha,B=local_for_beta(g,N,beta)
 tail=up(exp_bounds(beta*(B+U-E00))[1]*((1+3*exp_bounds(-beta*alpha)[1])**N-1))
 upper=up(exp_bounds(beta*(U-elo))[1]+tail)
 return upper,{'a':str(a),'b_upper':str(b),'alpha':str(alpha),'B_upper':str(B),
               'tail_upper':str(tail),'upper_Q':str(upper),'local_proof':'Exact half-spin 16x16 spectrum; a>=g/2 and rational sqrt upper'}

def g_for(rec):return rec['relative_form_bound']['local_certificate']['coupling'] if 'relative_form_bound' in rec else rec['weak_bonds'][0][-1]
def qfunc(rec,beta):return q_cached(g_for(rec),rec['N_dimers'],rec['ground_lower'],rec['ground_upper'],rec['E00'],Q(beta))[0]

def main():
 cases=[('1/100',f'bilayer_s1d2_{{x}}x{{y}}_g1d100_k1d100_q2_ground.json'),
        ('1/50',f'bilayer_s1d2_{{x}}x{{y}}_g1d50_k1d50_q2_ground.json'),
        ('3/100',f'bilayer_s1d2_{{x}}x{{y}}_g3d100_depth2_ground.json')]
 out=[]
 for g,template in cases:
  paths=[ROOT/'low_energy'/template.format(x=x,y=y) for x,y in [(2,2),(4,2),(4,4)]]
  records=[json.loads(p.read_text()) for p in paths]
  for order in ['xyt','xty','txy']:
   rows=[ordered_bilayer(records,Q(k,4),order,qfunc=qfunc) for k in range(24,121)]
   ok=[r for r in rows if r['accepted']]
   best=max(ok,key=lambda r:Q(r['gap_lower'])) if ok else None
   if best:
    beta=Q(best['beta_initial']);best['thermal_tail_nodes']=[]
    for i,v in enumerate(nodes(order,beta)):
     r=record_for(records,v);par=q_cached(g_for(r),r['N_dimers'],r['ground_lower'],r['ground_upper'],r['E00'],v[2])[1]
     best['thermal_tail_nodes'].append({'node_index':i,'nx':v[0],'ny':v[1],'beta':str(v[2]),'N_dimers':r['N_dimers'],'g':g_for(r),'ground_lower':r['ground_lower'],'ground_upper':r['ground_upper'],'E00':r['E00'],'parameters':par})
    best['ground_certificate_records']=records
   out.append({'model_id':'square_af_bilayer_spin_half_unit_rung','g':g,'order':order,'best_grid_gap':best,'sources':list(map(str,paths))})
   print('OPT-A BILAYER',g,order,'beta',best['beta_initial'] if best else None,'gap',float(Q(best['gap_lower'])) if best else None,'L0',best['n'] if best else None,flush=True)
 (OUT/'optimized_bilayer_tail_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
