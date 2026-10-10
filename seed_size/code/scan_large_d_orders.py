"""Correlation/order optimization for the SINGLE-LAYER spin-one large-D square."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from math import exp,log,log1p,expm1
import json,sys
from axis_order_search import ordered_bilayer,ROOT,OUT
from certified_core import up,exp_bounds
sys.path.insert(0,str(ROOT/'two_d_numerics'))
from large_d_certificates import choices

@lru_cache(maxsize=None)
def opts(g,N):return choices(g,N)

@lru_cache(maxsize=None)
def q_cached(g,N,elo,ehi,beta):
 beta=Q(beta);elo=Q(elo);ehi=Q(ehi)
 def score(p):
  a,b,c,B=p
  return float(beta*(B+ehi))+log(expm1(N*log1p(2*exp(-float(beta*c)))))
 a,b,c,B=min(opts(g,N),key=score)
 # Every choice has an exact rational two-site PSD certificate; floating selection affects efficiency only.
 tail=up(exp_bounds(beta*(B+ehi))[1]*((1+2*exp_bounds(-beta*c)[1])**N-1))
 return up(exp_bounds(beta*(ehi-elo))[1]+tail)

def qfunc(rec,beta):return q_cached(rec['g'],rec['N'],rec['ground_lower'],rec['ground_upper'],Q(beta))

def main():
 out=[]
 for g in ['1d100','3d200','1d50','1d40']:
  path=ROOT/'two_d_numerics'/'results'/f'largeD_g{g}_q2_certificate.json'
  if not path.exists():continue
  data=json.loads(path.read_text());recs=data['ground_certificates']
  for order in ['xyt','xty','txy']:
   rows=[ordered_bilayer(recs,Q(k,2),order,qfunc=qfunc) for k in range(10,61)]
   ok=[r for r in rows if r['accepted']]
   best=max(ok,key=lambda r:Q(r['gap_lower'])) if ok else None
   out.append({'model_id':'single_layer_spin_one_large_D_square','hamiltonian':'sum_i (Sz_i)^2 + g sum_square_edges S_i dot S_j; periodic length2 multibonds','D':'1','g':g.replace('d','/'),'order':order,'source':str(path),'best_grid_gap':best})
   print('SINGLE-LAYER LARGE-D',g,order,'beta',best['beta_initial'] if best else None,'gap',float(Q(best['gap_lower'])) if best else None,'L0',best['n'] if best else None,flush=True)
 (OUT/'single_layer_large_D_order_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
