"""Exact symbolic partition-function cancellation and basepoint audit.
Monomials are integer exponents of formal Z(v), not sampled partition values.
"""
from collections import defaultdict
from itertools import permutations
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
axes='xyt'
def doubled(v,i):
 w=list(v);w[axes.index(i)]+=1;return tuple(w)
def edge(v,i):
 return {doubled(v,i):1,v:-2}
def product(*factors):
 out=defaultdict(int)
 for mon,power in factors:
  for v,e in mon.items():out[v]+=power*e
 return {v:e for v,e in out.items() if e}
def staircase(v,order):
 points=[v];q=[]
 for i in order:q.append(edge(points[-1],i));points.append(doubled(points[-1],i))
 return points,q
rows=[];swaps=0;rotations=0
for order in permutations(axes):
 base=(0,0,0);points,q=staircase(base,order);end=points[-1]
 assert product((q[0],4),(q[1],2),(q[2],1))=={end:1,base:-8}
 assert product((q[1],4),(q[2],2))=={end:2,points[1]:-8}
 assert q[2]=={end:1,points[2]:-2}
 for pos in range(2):
  v=points[pos];i,j=order[pos:pos+2]
  a,b=edge(v,i),edge(doubled(v,i),j)
  c,e=edge(v,j),edge(doubled(v,j),i)
  assert product((e,1),(c,2))==product((b,1),(a,2));swaps+=1
  changed=list(order);changed[pos],changed[pos+1]=changed[pos+1],changed[pos]
  other,_=staircase(base,changed)
  assert points[:pos+1]==other[:pos+1] and points[pos+2:]==other[pos+2:]
 current_order=order;current_base=base
 for step in range(3):
  old_points,old_q=staircase(current_base,current_order)
  new_base=doubled(current_base,current_order[0]);new_order=current_order[1:]+current_order[:1]
  new_points,new_q=staircase(new_base,new_order)
  assert new_q[:2]==old_q[1:]
  assert new_q[2]==edge(old_points[-1],current_order[0])
  current_base,current_order=new_base,new_order;rotations+=1
 assert current_base==(1,1,1) and current_order==order
 rows.append(dict(order=''.join(order),initial_staircase_bases=[dict(zip(axes,p)) for p in points[:-1]],post_cycle_base=dict(zip(axes,current_base)),post_cycle_staircase_bases=[dict(zip(axes,p)) for p in staircase(current_base,order)[0][:-1]],all_cancellation_identities_equal=True))
# Prove the txy lower-only dependency graph in actual coordinates.
base=(0,0,0);points,q=staircase(base,'txy');largest=points[-1]
ratios=[product((q[0],4),(q[1],2),(q[2],1)),product((q[1],4),(q[2],2)),q[2]]
assert all(mon[largest]>0 for mon in ratios)
assert {v for mon in ratios for v,e in mon.items() if e<0}==set(points[:3])
assert all(not(v==largest and e<0) for mon in ratios for v,e in mon.items())
def physical(v):return [4*2**v[0],4*2**v[1],f'{2**v[2]} beta']
dataflow=[dict(name=name,monomial=[dict(basepoint=physical(v),exponent=e) for v,e in mon.items()]) for name,mon in zip(['J1','J2','C0'],ratios)]
result=dict(largest_numerator_only=True,ratio_dataflow=dataflow,status='PASS exact formal-monomial identities',interpretation='Coordinates count powers of two relative to (4,4,beta); the time coordinate is inverse temperature, not a spatial length',orders=rows,adjacent_swaps_checked=swaps,sequential_rotations_checked=rotations)
(HERE/'results/path_ledger.json').write_text(json.dumps(result,indent=2)+'\n')
print('PATH LEDGER PASS',len(rows),'orders,',swaps,'swaps,',rotations,'rotations')
