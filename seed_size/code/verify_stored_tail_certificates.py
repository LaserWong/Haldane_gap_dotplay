"""Verify saved optimized half-spin bilayer seeds WITHOUT floating minimization."""
from fractions import Fraction as Q
from pathlib import Path
import json
from certified_core import exp_bounds,up,down,G
from axis_order_search import ordered_replay,OUT

def verify(row):
 best=row['best_grid_gap']
 if best is None:return None
 ns=best['thermal_tail_nodes'];assert len(ns)==4
 qs=[];Us=[];betas=[]
 for node in ns:
  p=node['parameters'];a,b,alpha,B=map(Q,[p['a'],p['b_upper'],p['alpha'],p['B_upper']])
  g=Q(node['g']);N=node['N_dimers'];beta=Q(node['beta']);lo=Q(node['ground_lower']);U=Q(node['ground_upper']);E00=Q(node['E00'])
  assert g/2<=a<Q(1,4) and b>=0
  assert b+a-g/2>=0 and (b+a-g/2)**2>=a*a-a*g+g*g
  assert alpha==1-4*a and B==2*N*b
  tail=up(exp_bounds(beta*(B+U-E00))[1]*((1+3*exp_bounds(-beta*alpha)[1])**N-1))
  q=up(exp_bounds(beta*(U-lo))[1]+tail)
  assert Q(p['tail_upper'])>=tail and Q(p['upper_Q'])>=q
  qs.append(Q(p['upper_Q']));Us.append(U);betas.append(beta)
 def ratio(co):
  x=-sum((k*beta*U for k,beta,U in zip(co,betas,Us)),Q(0))
  val=exp_bounds(x)[0]
  for k,q in zip(co,qs):
   if k<0:val/=q**(-k)
  return down(val)
 J1=ratio([-8,0,0,1]);J2=ratio([0,-8,0,2]);C=ratio([0,0,-2,1])
 A1=down(G(J1));B1=down(G(J2*A1));C1=down(G(C**4*A1*A1*B1))
 assert list(map(str,[A1,B1,C1]))==best['correlated_first_step']
 actual=ordered_replay([A1,B1,C1],row['order'],4,2*Q(best['beta_initial']))
 assert actual['accepted']
 for k in ['gap_lower','n','m','beta','u_canonical','canonical_purities']:
  assert actual[k]==best[k],(k,actual[k],best[k])
 return {'g':row['g'],'order':row['order'],'gap_lower':actual['gap_lower'],'L0':actual['n'],'passed':True}

def main():
 rows=json.loads((OUT/'optimized_bilayer_tail_results.json').read_text());results=[]
 for row in rows:
  r=verify(row)
  if r:results.append(r);print('REPLAY',r['g'],r['order'],'PASS',flush=True)
 (OUT/'stored_tail_replay_validation.json').write_text(json.dumps({'passed':all(r['passed'] for r in results),'uses_float_optimizer':False,'records':results},indent=2))
if __name__=='__main__':main()
