#!/usr/bin/env python3
"""Independent exact-integer hard-core commutator tests; no producer imports."""
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import json, time, resource, argparse
import sympy as sy
OUT=Path(__file__).resolve().parent
SGN={1:-1,2:1,3:-1}
def clean(v): return {s:c for s,c in v.items() if c}
def plus(*terms):
 d=defaultdict(int)
 for v,w in terms:
  for s,c in v.items():d[s]+=w*c
 return clean(d)
def dot(a,b): return sum(x*b.get(s,0) for s,x in a.items())
def pair(v,i,j,create):
 d=defaultdict(int)
 for s,c in v.items():
  if create:
   if s[i] or s[j]:continue
   for a in (1,2,3):
    t=list(s);t[i]=a;t[j]=4-a;d[tuple(t)]+=SGN[a]*c
  elif s[i] and s[j]==4-s[i]:
   t=list(s);t[i]=t[j]=0;d[tuple(t)]+=SGN[s[i]]*c
 return clean(d)
def C(v,edges,create):return plus(*[(pair(v,i,j,create),w) for (i,j),w in edges.items()])
def edge_comm(v,i,j):
 # 3 h_i h_j - |Omega_ij><Omega_ij|, expanded directly.
 d=defaultdict(int)
 for s,c in v.items():
  if not s[i] and not s[j]:d[s]+=3*c
  elif s[i] and s[j]==4-s[i]:
   for a in (1,2,3):
    t=list(s);t[i]=a;t[j]=4-a;d[tuple(t)]-=SGN[s[i]]*SGN[a]*c
 return clean(d)
def wedge(v,i,j,k):
 # [P_ij,P^dagger_ik]: j is annihilation-side outer endpoint.
 d=defaultdict(int)
 for s,c in v.items():
  if not s[k] and s[j]:
   if not s[i]:
    t=list(s);t[k]=t[j];t[j]=0;d[tuple(t)]+=c
   elif s[j]==4-s[i]:
    for a in (1,2,3):
     t=list(s);t[i]=a;t[j]=0;t[k]=4-a
     d[tuple(t)]-=SGN[s[i]]*SGN[a]*c
 return clean(d)
def K(v,edges):
 adj=defaultdict(list);terms=[]
 for (i,j),w in edges.items():
  terms.append((edge_comm(v,i,j),w*w));adj[i].append((j,w));adj[j].append((i,w))
 for i,ns in adj.items():
  for j,w in ns:
   for k,z in ns:
    if j!=k:terms.append((wedge(v,i,j,k),w*z))
 return plus(*terms)
def spin_A():
 # Build both layer exchanges in the physical up/down basis, then conjugate.
 r=sy.sqrt(2);T=sy.Matrix([[0,1,0,0],[-1/r,0,1/r,0],[1/r,0,1/r,0],[0,0,0,1]])
 assert T.T*T==sy.eye(4)
 V=sy.zeros(16)
 for c in range(16):
  for i,j in ((0,2),(1,3)):
   a=(c>>(3-i))&1;b=(c>>(3-j))&1
   V[c,c]+=sy.Rational((2*a-1)*(2*b-1),4)
   if a!=b:V[c^(1<<(3-i))^(1<<(3-j)),c]+=sy.Rational(1,2)
 U=sy.kronecker_product(T,T);A=(2*U.T*V*U).applyfunc(sy.simplify)
 assert A==A.T and all(x.is_Integer for x in A)
 return [[int(x) for x in row] for row in A.tolist()]
def physical(v,edges,A,target):
 d=defaultdict(int)
 for s,c in v.items():
  for (i,j),w in edges.items():
   old=4*s[i]+s[j]
   for ab in range(16):
    if A[ab][old]:
     a,b=divmod(ab,4);t=list(s);t[i]=a;t[j]=b
     if sum(x!=0 for x in t)==target:d[tuple(t)]+=w*c*A[ab][old]
 return clean(d)
def graph(nx,ny):
 e=defaultdict(int)
 for x,y in product(range(nx),range(ny)):
  i=x*ny+y
  for a,b in (((x+1)%nx,y),(x,(y+1)%ny)):
   j=a*ny+b;assert i!=j;e[tuple(sorted((i,j)))]+=1
 return dict(e)
def pair_orbits(nx,ny):
 out=defaultdict(list)
 for i,j in combinations(range(nx*ny),2):
  x,y=divmod(i,ny);a,b=divmod(j,ny)
  dx=min((x-a)%nx,(a-x)%nx);dy=min((y-b)%ny,(b-y)%ny)
  key=tuple(sorted((dx,dy))) if nx==ny else (dx,dy)
  out[key].append((i,j))
 return [out[k] for k in sorted(out)]
def local_tests(A):
 count=0
 for s in product(range(4),repeat=2):
  v={s:1};assert physical(v,{(0,1):1},A,sum(bool(x) for x in s)+2)==pair(v,0,1,True)
 for n,e,f,kind in [(2,(0,1),(0,1),'same'),(3,(0,1),(0,2),'wedge'),(4,(0,1),(2,3),'disjoint')]:
  for s in product(range(4),repeat=n):
   v={s:1};actual=plus((pair(pair(v,*f,True),*e,False),1),(pair(pair(v,*e,False),*f,True),-1))
   expected=edge_comm(v,*e) if kind=='same' else wedge(v,0,1,2) if kind=='wedge' else {}
   assert actual==expected;(count:=count+1)
 # Nonuniform, signed edge weights test cross weights and ordered wedge factors.
 edges={(0,1):2,(0,2):-3,(1,2):1,(2,3):4,(0,3):2}
 for s in product(range(4),repeat=4):
  v={s:1};assert K(v,edges)==plus((C(C(v,edges,True),edges,False),1),(C(C(v,edges,False),edges,True),-1))
 return dict(exhaustive_pair_commutator_basis_tests=count,weighted_graph_basis_tests=256,physical_pair_block_exact=True)
def fixture(nx,ny,A):
 n=nx*ny;edges=graph(nx,ny);vac={(0,)*n:1}
 B=[plus(*[(pair(vac,i,j,True),1) for i,j in orb]) for orb in pair_orbits(nx,ny)]
 L=[physical(b,edges,A,4) for b in B];M=[physical(l,edges,A,6) for l in L]
 assert all(m==C(l,edges,True) for m,l in zip(M,L))
 up=[C(m,edges,True) for m in M];down=[C(m,edges,False) for m in M];km=[K(m,edges) for m in M]
 assert all(u==physical(m,edges,A,8) for u,m in zip(up,M))
 rhs=[[dot(a,b)+dot(m,k) for b,k in zip(down,km)] for a,m in zip(down,M)]
 lhs=[[dot(a,b) for b in up] for a in up]
 assert lhs==rhs and lhs==list(map(list,zip(*lhs)))
 if n==8:assert sum(lhs[i][i] for i in range(len(M)))>0
 # An arbitrary coherent combination tests cross terms (including negative coefficients).
 co=[(-1)**i*(i+1) for i in range(len(M))];v=plus(*zip(M,co));u=C(v,edges,True);d=C(v,edges,False);kv=K(v,edges)
 assert dot(u,u)==dot(d,d)+dot(v,kv)
 return dict(shape=[nx,ny],rungs=n,spins=2*n,physical_Hilbert_dimension=4**n,pair_orbits=len(M),edge_weights=sorted(set(edges.values())),q6_support_states=[len(m) for m in M],q8_gram=lhs,coherent_q8_norm=dot(u,u),coherent_q4_norm=dot(d,d),coherent_commutator=dot(v,kv),all_cross_entries_exact=True)
def matching(p,n):
 v={(0,)*n:1}
 for i,j in p:v=pair(v,i,j,True)
 return v
def matchings(xs):
 if not xs:yield [];return
 i=xs[0]
 for k,j in enumerate(xs[1:],1):
  for rest in matchings(xs[1:k]+xs[k+1:]):yield [(i,j)]+rest
def recoupling_tests():
 count=0
 for p in matchings(list(range(6))):
  partners={i:j for a,b in p for i,j in ((a,b),(b,a))};v=matching(p,7)
  for i,j in combinations(range(6),2):
   rem=[e for e in p if i not in e and j not in e]
   if partners[i]==j:coef=3
   else:coef=1;rem.append((partners[i],partners[j]))
   expected=matching(rem+[(i,6)],7)
   assert wedge(v,i,j,6)==plus((expected,-coef))
   assert edge_comm(v,i,j)==plus((matching(rem+[(i,j)],7),-coef))
   count+=2
 # Empty-center wedge is a plain hop with positive coefficient.
 for p in matchings(list(range(6))):
  v=matching(p,8);expected=matching([(6 if a==0 else a,6 if b==0 else b) for a,b in p],8)
  assert wedge(v,7,0,6)==expected;count+=1
 return dict(exact_matching_recoupling_tests=count)
if __name__=='__main__':
 start=time.monotonic();A=spin_A();result={'local':local_tests(A),'matching':recoupling_tests(),'fixtures':[fixture(2,2,A),fixture(3,2,A),fixture(4,2,A)]}
 result.update(status='PASS',seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
