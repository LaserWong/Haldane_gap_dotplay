#!/usr/bin/env python3
"""Fresh exact physical-basis audit; no producer modules imported."""
import itertools as it,json,collections as co,resource,time,os
from pathlib import Path
import sympy as s
START=time.time(); ROOT=Path(__file__).resolve().parent

def add(v,k,c):
 v[k]+=c
 if not v[k]:del v[k]
def inner(v,w):return sum(c*w.get(k,0) for k,c in v.items())
def combine(vs):
 out=co.defaultdict(int)
 for v,c in vs:
  for k,a in v.items():add(out,k,a*c)
 return out
# Physical rung transform independently assembled from ket labels (up=0, down=1).
r=s.sqrt(2); U=s.Matrix.hstack(s.Matrix([0,1/r,-1/r,0]),s.Matrix([0,0,0,1]),s.Matrix([0,1/r,1/r,0]),s.Matrix([1,0,0,0]))
z=s.diag(s.Rational(1,2),-s.Rational(1,2)); p=s.Matrix([[0,1],[0,0]]);m=p.T; I=s.eye(2)
def emb(a,i):return s.kronecker_product(*[a if j==i else I for j in range(4)])
h=sum((2*emb(z,i)*emb(z,j)+emb(p,i)*emb(m,j)+emb(m,i)*emb(p,j) for i,j in [(0,2),(1,3)]),s.zeros(16))
local=s.kronecker_product(U,U).T*h*s.kronecker_product(U,U)
assert all(x.is_Integer for x in local)
trans=[[(divmod(a,4),int(local[a,b])) for a in range(16) if local[a,b]] for b in range(16)]
sg=[0,-1,1,-1]
def graph(x,y):
 e=co.Counter()
 for a,b in it.product(range(x),range(y)):
  for c,d in [((a+1)%x,b),(a,(b+1)%y)]:e[tuple(sorted([a*y+b,c*y+d]))]+=1
 return dict(e)
def action(v,edges,mode):
 out=co.defaultdict(int)
 for st,c in v.items():
  for (i,j),w in edges.items():
   for (a,b),h in trans[4*st[i]+st[j]]:
    dq=bool(a)+bool(b)-bool(st[i])-bool(st[j])
    if mode is not None and dq!=mode:continue
    dst=st[:i]+(a,)+st[i+1:j]+(b,)+st[j+1:];add(out,dst,c*w*h)
 return out

def comm(v,edges):
 out=co.defaultdict(int);adj=co.defaultdict(dict)
 for (i,j),w in edges.items():adj[i][j]=w;adj[j][i]=w
 for st,c in v.items():
  for (i,j),w in edges.items():
   if st[i]==st[j]==0:add(out,st,3*w*w*c)
   if st[i] and st[i]+st[j]==4:
    for a in [1,2,3]:
     t=list(st);t[i]=a;t[j]=4-a;add(out,tuple(t),-w*w*c*sg[st[i]]*sg[a])
  for i,nn in adj.items():
   for j,k in it.permutations(nn,2):
    if st[k] or not st[j]:continue
    w=nn[j]*nn[k]
    if not st[i]:
     t=list(st);t[j]=0;t[k]=st[j];add(out,tuple(t),w*c)
    elif st[i]+st[j]==4:
     for a in [1,2,3]:
      t=list(st);t[i]=a;t[j]=0;t[k]=4-a;add(out,tuple(t),-w*c*sg[st[i]]*sg[a])
 return out

def q(v,n):return {st:c for st,c in v.items() if sum(bool(x) for x in st)==n}
# Local complete basis matrix identity, weighted signs and parallel-edge square factors.
weighted={(0,1):2,(0,2):-3,(1,2):1,(2,3):4,(0,3):2}
for n,ed in [(2,{(0,1):3}),(3,{(0,1):2,(0,2):-3}),(4,weighted)]:
 for st in it.product(range(4),repeat=n):
  v={st:1};rhs=combine([(action(action(v,ed,2),ed,-2),1),(action(action(v,ed,-2),ed,2),-1)])
  assert rhs==comm(v,ed)

def fixture(nx,ny):
 n=nx*ny;ed=graph(nx,ny);orbits=co.defaultdict(list)
 for i,j in it.combinations(range(n),2):
  xi,yi=divmod(i,ny);xj,yj=divmod(j,ny);key=(min((xi-xj)%nx,(xj-xi)%nx),min((yi-yj)%ny,(yj-yi)%ny))
  if nx==ny:key=tuple(sorted(key))
  orbits[key].append((i,j))
 B=[]
 for orb in sorted(orbits):
  v=co.defaultdict(int)
  for i,j in orbits[orb]:
   for a in [1,2,3]:
    st=[0]*n;st[i]=a;st[j]=4-a;add(v,tuple(st),sg[a])
  B.append(v)
 L=[action(b,ed,2) for b in B];R=[action(l,ed,0) for l in L];M=[action(l,ed,2) for l in L]
 down=[action(m,ed,-2) for m in M];up=[action(m,ed,2) for m in M];km=[comm(m,ed) for m in M]
 grams=[[inner(u,v) for v in up] for u in up]
 assert grams==[[inner(a,b)+inner(c,d) for b,d in zip(down,km)] for a,c in zip(down,M)]
 c=[(-1)**i*(i+1) for i in range(len(B))]
 mm=combine(zip(M,c));rr=combine(zip(R,c));ll=combine(zip(L,c));bb=combine(zip(B,c))
 # A nontrivial full enlarged vector, whose H image has interference in each sector.
 psi=combine([({(0,)*n:1},17),(bb,-2),(ll,3),(rr,5),(mm,5)])
 # Integer 20 H'=20Q+A at g=1/10.
 hpsi=combine([({st:20*sum(bool(x) for x in st)*v for st,v in psi.items()},1),(action(psi,ed,None),1)])
 sectors={str(k):inner(q(hpsi,k),q(hpsi,k)) for k in [0,2,4,6,8]}
 assert sum(sectors.values())==inner(hpsi,hpsi)
 q8ident=25*(inner(action(mm,ed,-2),action(mm,ed,-2))+inner(mm,comm(mm,ed)))
 assert q8ident==sectors['8']
 # Full/fixed-origin identity checked in every nonvacuum bra sector.
 for k in [2,4,6,8]:
  v=q(hpsi,k);fixed=sum(a*a for st,a in v.items() if st[0]);assert n*fixed==k*inner(v,v)
 tt=combine([(action(rr,ed,2),1),(action(mm,ed,0),1)])
 extra={st:a for st,a in tt.items() if st not in mm};extra_norm=inner(extra,extra)
 return dict(shape=[nx,ny],q8_gram=grams,coherent_Cdag_norm=inner(action(mm,ed,2),action(mm,ed,2)),coherent_C_norm=inner(action(mm,ed,-2),action(mm,ed,-2)),coherent_commutator=inner(mm,comm(mm,ed)),full_image_sector_norms=sectors,T_norm_on_M_zero_physical_states=extra_norm,translation_check=True)
result=dict(status='PASS',fixtures=[fixture(2,2),fixture(3,2),fixture(4,2)],seconds=time.time()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(ROOT/'local_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
