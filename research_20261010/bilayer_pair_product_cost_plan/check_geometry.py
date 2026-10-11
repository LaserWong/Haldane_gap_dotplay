"""Geometry-only exact checks: no physical state or support contraction."""
from fractions import Fraction
from collections import Counter
import json

def check(L,W):
 pts=[(x,y) for x in range(L) for y in range(W)]
 edge=Counter()
 for u in pts:
  for v in [((u[0]+1)%L,u[1]),(u[0],(u[1]+1)%W)]:
   edge[tuple(sorted((u,v)))]+=1
 adj={u:{} for u in pts}
 for (u,v),w in edge.items():adj[u][v]=w;adj[v][u]=w
 counts=Counter()
 for i,u in enumerate(pts):
  for v in pts[i+1:]:
   if (sum(u)-sum(v))%2==0:
    n=sum(w*adj[v].get(k,0) for k,w in adj[u].items())
    counts[n]+=1
 assert all(sum(a.values())==4 for a in adj.values())
 return dict(shape=[L,W],rungs=L*W,edges=len(edge),weighted_edges=sum(edge.values()),same_sublattice_common_neighbor_histogram=dict(sorted(counts.items())),residual_coefficient=3*sum(n*n*c for n,c in counts.items()))
r=[check(8,4),check(4,2),check(2,2)]
assert r[0]['residual_coefficient']==1056
assert r[1]['residual_coefficient']==432
g=Fraction(11,100);z=-g/4
Z=(1+48*z*z)**16
v=1056*g*g*z*z/Z
T=[1,1]
for n in range(2,33):T.append(T[-1]+(n-1)*T[-2])
print(json.dumps(dict(scope='geometry-only; no physical contraction',geometries=r,g=str(g),z=str(z),norm_upper=str(Z),norm_upper_display=float(Z),variance_lower=str(v),variance_lower_display=float(v),partial_pairing_bounds={str(n):T[n] for n in [8,10,16,18,20,32]}),indent=2))
