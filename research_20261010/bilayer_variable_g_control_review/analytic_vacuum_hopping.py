"""Independent q0 derivation with scalar singlet contractions on local edge pairs.
Only supports that are unions of two graph edges are used; no full sector/support cache.
"""
from itertools import combinations
from pathlib import Path

def vacuum24(root):
 z=list(map(int,(Path(root)/'geometry_8x4.txt').read_text().split()));n,d,ne=z[:3];assert (n,d,ne)==(32,14,64);edge={}
 for k in range(ne):
  a,b,w=z[3+3*k:6+3*k];edge[tuple(sorted((a,b)))]=w
 orb={};offset=3+3*ne
 for k,p in enumerate(combinations(range(n),2)):orb[p]=z[offset+k]
 w=list(map(int,(Path(root)/'witness57.txt').read_text().split()));a=w[0];cb,cl,cr,cm=[w[1+j*d:1+(j+1)*d] for j in range(4)];assert a==2**48
 Cpsi2=3*sum(x*cb[orb[p]] for p,x in edge.items());CDpsi2=-6*sum(x*x*cb[orb[p]] for p,x in edge.items());CCdpsi0=3*a*sum(x*x for x in edge.values())
 # D has both T·T and hopping |t,0>↔|0,t> with coefficient1.
 CDpsi2+=3*sum(wt*edge.get(tuple(sorted((x,y))),0)*cb[orb[tuple(sorted((other,y)))]] for (u,v),wt in edge.items() for x,other in [(u,v),(v,u)] for y in range(n) if y not in (u,v))
 supports={tuple(sorted(set(p)|set(q))) for p,q in combinations(edge,2) if len(set(p)|set(q))==4}
 total=0
 def canon(pairs):return tuple(sorted(tuple(sorted(p)) for p in pairs))
 for s in supports:
  i,j,k,l=s;pm=[canon([(i,j),(k,l)]),canon([(i,k),(j,l)]),canon([(i,l),(j,k)])]
  v=[2*edge.get(p[0],0)*edge.get(p[1],0) for p in pm]
  ll=[edge.get(p[0],0)*cl[orb[p[1]]]+edge.get(p[1],0)*cl[orb[p[0]]] for p in pm]
  lr=[edge.get(p[0],0)*cr[orb[p[1]]]+edge.get(p[1],0)*cr[orb[p[0]]] for p in pm];dl=[0]*3
  for idx,pairing in enumerate(pm):
   mate={u:v for p in pairing for u,v in [p,p[::-1]]}
   for x,y in combinations(s,2):
    wt=edge.get((x,y),0)
    if not wt:continue
    if mate[x]==y:dl[idx]-=2*wt*lr[idx]
    else:
     crossed=canon([(x,mate[y]),(y,mate[x])]);contracted=canon([(x,y),(mate[x],mate[y])])
     dl[pm.index(crossed)]+=wt*lr[idx];dl[pm.index(contracted)]-=wt*lr[idx]
  psi4=[x+y for x,y in zip(ll,dl)]
  total+=sum(v[p]*psi4[q]*(9 if p==q else 3) for p in range(3) for q in range(3))
  # Hermitian hopping acts on the dual Cd²|0>, avoiding a full psi4 image.
  for idx,pairing in enumerate(pm):
   if not v[idx]:continue
   for x in s:
    for y in range(n):
     if y in s:continue
     wt=edge.get(tuple(sorted((x,y))),0)
     if not wt:continue
     moved=canon([tuple(y if z==x else z for z in pair) for pair in pairing])
     aa,bb,cc,dd=sorted(y if z==x else z for z in s)
     newpm=[canon([(aa,bb),(cc,dd)]),canon([(aa,cc),(bb,dd)]),canon([(aa,dd),(bb,cc)])]
     pi=newpm.index(moved)
     for q,pairs in enumerate(newpm):
      lvalue=edge.get(pairs[0],0)*cr[orb[pairs[1]]]+edge.get(pairs[1],0)*cr[orb[pairs[0]]]
      total+=v[idx]*wt*lvalue*(9 if pi==q else 3)
 chi=11*Cpsi2;z0=11*(400*Cpsi2+11*CDpsi2+11*CCdpsi0+11*total)
 return list(map(str,[0]*15+[a*a,a*chi,chi*chi,2*chi*z0,z0*z0,0,0,0,0]))
