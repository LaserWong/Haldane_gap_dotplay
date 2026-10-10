"""Diagnostics and exact replay for q2 larger seed ladder; no accepted claim by scan."""
import sys,math,json
from fractions import Fraction as F
from pathlib import Path
from symmetric_ground import ROOT,OUT
from local_relative_bound import trace,exp_bounds,down
sys.path.insert(0,str(ROOT/'two_d_theory'))
from three_purity_certificate import replay

def floats(r,beta,zero_width=False):
 alpha=float(F(r['relative_form_bound']['alpha']));B=float(F(r['relative_form_bound']['B']))
 mean=float(F(r['ground_upper'])-F(r['E00']));width=float(F(r['ground_upper'])-F(r['ground_lower']))
 # Stable binomial tail from log1p/expm1.
 tail=math.exp(beta*(B+mean))*math.expm1(r['N_dimers']*math.log1p(3*math.exp(-beta*alpha)))
 return math.exp(beta*(0 if zero_width else width))+tail

def seed(rs,beta):
 qs=[trace(r,F(beta))[1] for r in rs]
 c1=F(rs[1]['ground_upper'])-2*F(rs[0]['ground_upper']);c2=F(rs[2]['ground_upper'])-2*F(rs[1]['ground_upper'])
 A=down(exp_bounds(-F(beta)*c1)[0]/qs[0]**2,digits=15)
 B=down(exp_bounds(-F(beta)*c2)[0]/qs[1]**2,digits=15)
 C=down(1/qs[2]**2,digits=15)
 return dict(beta=beta,A=str(A),B=str(B),C=str(C),A_display=float(A),B_display=float(B),C_display=float(C),bootstrap=replay(A,B,C,n=4,m=4,beta=F(beta),rounds=32,digits=18))

out=[]
for g in ['1/100','1/50','3/100']:
 rs=[json.loads((OUT/(f'analytic_{nx}x{ny}_g{g}.json'.replace('/','d'))).read_text()) for nx,ny in [(4,4),(8,4),(8,8)]]
 curves=[];ideal=[]
 for beta in range(1,201):
  qs=[floats(r,beta) for r in rs]
  c1=float(F(rs[1]['ground_upper'])-2*F(rs[0]['ground_upper']));c2=float(F(rs[2]['ground_upper'])-2*F(rs[1]['ground_upper']))
  A=math.exp(-beta*c1)/qs[0]**2;B=math.exp(-beta*c2)/qs[1]**2;C=1/qs[2]**2
  curves.append((min(A,B,C),beta,A,B,C))
  qi=[floats(r,beta,True) for r in rs];ideal.append((min(math.exp(-beta*c1)/qi[0]**2,math.exp(-beta*c2)/qi[1]**2,1/qi[2]**2),beta))
 best=max(curves);tested=[seed(rs,b) for b in sorted(set([best[1]-1,best[1],best[1]+1])) if b>=1]
 row=dict(coupling=g,best_min_purity_float=best[0],best_beta=best[1],best_ABC_float=best[2:],zero_width_diagnostic_best=max(ideal),exact_tests=tested)
 out.append(row);print(json.dumps(row),flush=True)
(OUT/'larger_seed_diagnostics.json').write_text(json.dumps(out,indent=2))
