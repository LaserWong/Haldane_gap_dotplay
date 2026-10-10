"""Independent all-beta arithmetic verification of the g=.03 method-family ceiling."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
from verify_bilayer import ground,bounded_exp
BASE=Path(__file__).resolve().parents[2];OUT=BASE/'audit/independent'
SCALE=1<<128
def up(x):return Q(-((-x.numerator*SCALE)//x.denominator),SCALE)
def G(x):return 1-(1-x)**2/(2*x*x)
def vertices(order):
 v=[2,2,Q(1)];out=[tuple(v)]
 for axis in order:v['xyt'.index(axis)]*=2;out.append(tuple(v))
 return out

def envelope(records,deltas,order,l,h):
 vs=vertices(order);idx=[{4:0,8:1,16:2}[x*y] for x,y,t in vs]
 rec=[records[i] for i in idx];dd=[deltas[i] for i in idx];qfloor=[]
 for r,d,(x,y,t) in zip(rec,dd,vs):
  beta=h if d>=0 else l
  qfloor.append(1+3*r['N_dimers']*bounded_exp(-t*beta*d)[0])
 def ratio(coeff):
  rate=-sum(k*v[2]*Q(r['ground_lower'] if k>0 else r['ground_upper']) for k,v,r in zip(coeff,vs,rec))
  bb=h if rate>=0 else l
  ans=bounded_exp(bb*rate)[1]
  for k,q in zip(coeff,qfloor):
   if k<0:ans/=q**(-k)
  return min(Q(1),up(ans))
 J1,J2,C=[ratio(c) for c in [[-8,0,0,1],[0,-8,0,2],[0,0,-2,1]]]
 if J1<=Q(1,2):return None
 A=up(G(J1))
 if A<=0:return None
 B=up(G(J2*A))
 if B<=0:return None
 CC=up(G(C**4*A*A*B))
 if CC<=0:return None
 return [A,B,CC]

def excluded(p):
 if p is None:return True,0
 for j in range(100):
  if p[0]**4*p[1]**2*p[2]<=Q(1,2):return True,j
  for _ in range(3):
   x=p[0]**4*p[1]**2*p[2]
   if x<=0:return True,j
   a=up(G(x))
   if a<=0:return True,j
   p=p[1:]+[min(Q(1),a)]
 return False,100

def main():
 path=BASE/'seed_size/results/bilayer_majorant_ceiling.json';data=json.loads(path.read_text());rows=[r for r in data if r['g']=='3/100']
 records=[json.loads(Path(p).read_text()) for p in rows[0]['sources']]
 gc=[ground(r,*shape,Q(3,100)) for r,shape in zip(records,[(2,2),(4,2),(4,4)])]
 print('GROUND-INTERVAL INPUTS VERIFIED',gc,flush=True)
 checks=[]
 for row in rows:
  assert row['majorant_family_excluded'] and not row['unresolved_intervals']
  ds=list(map(Q,row['delta_best_upper']));g=Q(3,100)
  for r,delta in zip(records,ds):
   # Rearranged radical comparison avoids reusing any sqrt routine.
   needed=(1-2*g+Q(r['E00'])-Q(r['ground_lower'])-delta)/(2*g)
   assert needed<=0 or needed*needed<=3*(r['N_dimers']-1)
  curvature=2*Q(records[2]['ground_lower'])-8*Q(records[0]['ground_upper'])
  assert curvature==Q(row['corner_curvature']) and curvature>0
  tail=Q(row['beta_tail_start']);assert bounded_exp(-tail*curvature)[1]<=Q(1,2)
  intervals=sorted((Q(a),Q(b)) for a,b in row['excluded_intervals']);end=Q(0);certified=[]
  for l,h in intervals:
   assert l==end and l<h;end=h
   ok,rounds=excluded(envelope(records,ds,row['order'],l,h));assert ok
   certified.append({'beta_lo':str(l),'beta_hi':str(h),'upper_map_exclusion_rounds':rounds})
  assert end==tail
  checks.append({'order':row['order'],'intervals':certified,'tail_from':str(tail),'all_beta_covered':True})
 out={'status':'PASS independent source-ground audit, radical envelope, interval coverage and optimistic-map failure','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'ground_input_checks':gc,'all_beta_checks':checks,'scope':'Only the declared ground-only numerator/independent-dimer-bin majorant family, with arbitrary refined pivots inside these intervals, all admissible local a, and xyt/xty/txy staircase orders; not a physical phase boundary.'}
 (OUT/'majorant_g003_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
