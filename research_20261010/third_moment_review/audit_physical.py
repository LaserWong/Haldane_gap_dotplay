"""Exact spin-kernel, invariant-tensor, stabilizer, and sparse model regressions."""
from audit_matrices import *
import sympy as S

def local():
 T=S.Matrix([[0,1,0,0],[-1/S.sqrt(2),0,1/S.sqrt(2),0],[1/S.sqrt(2),0,1/S.sqrt(2),0],[0,0,0,1]])
 assert T.T*T==S.eye(4);U=S.kronecker_product(T,T);V=S.zeros(16)
 for c in range(16):
  for i,j in ((0,2),(1,3)):
   a=(c>>(3-i))&1;b=(c>>(3-j))&1;V[c,c]+=S.Rational((2*a-1)*(2*b-1),4)
   if a!=b:V[c^(1<<(3-i))^(1<<(3-j)),c]+=S.Rational(1,2)
 A=(2*U.T*V*U).applyfunc(S.simplify);assert A==A.T and all(x.is_Integer for x in A)
 A=[[int(x) for x in row] for row in A.tolist()];saved=load(P/'physical_local_A.json');assert A==saved['A_orthonormal_spherical_triplet_basis']
 assert all(not A[i][j] or abs((i//4!=0)+(i%4!=0)-(j//4!=0)-(j%4!=0)) in (0,2) for i in range(16) for j in range(16))
 return A

def clean(v):return {s:c for s,c in v.items() if c}
def dotv(a,b):return sum(x*b.get(s,0) for s,x in a.items())
def plus(*vectors):
 out=defaultdict(int)
 for v,f in vectors:
  for s,c in v.items():out[s]+=f*c
 return clean(out)
def q(s):return sum(bool((s>>(2*i))&3) for i in range((s.bit_length()+1)//2))
def act(v,A,edges,target=None):
 out=defaultdict(int)
 for s,c in v.items():
  for (i,j),w in edges.items():
   a=(s>>(2*i))&3;b=(s>>(2*j))&3
   for xy in range(16):
    z=A[xy][4*a+b]
    if z:
     x,y=divmod(xy,4);r=s^((a^x)<<(2*i))^((b^y)<<(2*j))
     if target is None or q(r)==target:out[r]+=c*w*z
 return clean(out)
def h(v,A,edges,den=200,gn=9):
 out=act(v,A,edges);out={s:gn*x for s,x in out.items()}
 for s,c in v.items():out[s]=out.get(s,0)+den*q(s)*c
 return clean(out)
def pairings(rem):
 if not rem:yield [];return
 a=rem[0]
 for j,b in enumerate(rem[1:],1):
  for p in pairings(rem[1:j]+rem[j+1:]):yield [(a,b)]+p
def pairvector(p):
 out={0:1}
 for i,j in p:
  out={s|(a<<(2*i))|(b<<(2*j)):c*z for s,c in out.items() for a,b,z in ((1,3,-1),(2,2,1),(3,1,-1))}
 return out

def match_tests(A):
 rows=[]
 for nq in (4,6):
  pp=list(pairings(list(range(nq))));vv=[pairvector(p) for p in pp];grams=[];bonds=0
  for p,v in zip(pp,vv):
   partners={i:j for a,b in p for i,j in ((a,b),(b,a))};grow=[]
   for r,w in zip(pp,vv):
    conn={i:set() for i in range(nq)}
    for a,b in p+r:conn[a].add(b);conn[b].add(a)
    seen=set();loops=0
    for i in range(nq):
     if i in seen:continue
     loops+=1;pending=[i]
     while pending:
      x=pending.pop()
      if x in seen:continue
      seen.add(x);pending.extend(conn[x]-seen)
    assert dotv(v,w)==3**loops;grow.append(3**loops)
   grams.append(grow)
   for i,j in itertools.combinations(range(nq),2):
    actual=act(v,A,{(i,j):1},nq)
    if partners[i]==j:expected=plus((v,-2))
    else:
     k,l=partners[i],partners[j];rest=[e for e in p if not (i in e or j in e)]
     expected=plus((pairvector(rest+[(i,l),(j,k)]),1),(pairvector(rest+[(i,j),(k,l)]),-1))
    assert actual==expected;(bonds:=bonds+1)
  rows.append(dict(q=nq,matching_count=len(pp),all_matching_grams=grams,local_recoupling_tests=bonds))
 save('matching_tensor_review.json',rows)

def translation(nx,ny,dx,dy,s):return tuple(sorted((((i//ny+dx)%nx)*ny+(i%ny+dy)%ny) for i in s))
def support_tests():
 rows=[]
 for nx,ny in ((2,2),(4,2),(4,4)):
  N=nx*ny;e,orbs,ids=graph(nx,ny)
  expected=f'{N} {len(orbs)}\n{len(e)}\n'+''.join(f'{i} {j} {w}\n' for (i,j),w in sorted(e.items()))+' '.join(str(ids[i,j]) for i,j in itertools.combinations(range(N),2))+'\n'
  assert expected==(SNAP/'prior_geometry'/f'geometry_{nx}x{ny}.txt').read_text()
  for nq in (4,6):
   if nq>N:continue
   grouped=defaultdict(list)
   for s in itertools.combinations(range(N),nq):
    key=min(translation(nx,ny,dx,dy,s) for dx,dy in itertools.product(range(nx),range(ny)))
    grouped[key].append(s)
   stabilizers=Counter()
   for rep,orbit in grouped.items():
    fixed=sum(0 in s for s in orbit);assert len(orbit)*nq==N*fixed
    stabilizer=sum(translation(nx,ny,dx,dy,rep)==rep for dx,dy in itertools.product(range(nx),range(ny)))
    assert stabilizer*len(orbit)==N;stabilizers[stabilizer]+=1
   # Number of active q6 sets also follows N/q even in repeated patterns.
   if nq==6:
    active=lambda s:any(e.get(tuple(sorted(a)),0) and e.get(tuple(sorted(b)),0) and len(set(a+b))==4 for a,b in itertools.combinations(itertools.combinations(s,2),2))
    allact=sum(active(s) for orbit in grouped.values() for s in orbit);origin=sum(active(s) for orbit in grouped.values() for s in orbit if 0 in s)
    assert allact*nq==N*origin
   rows.append(dict(shape=[nx,ny],q=nq,translation_orbits=len(grouped),stabilizer_multiplicities=dict(stabilizers),every_orbit_incidence_exact=True))
 save('stabilizer_review.json',rows)

def physical(A):
 rows=[]
 for nx,ny in ((2,2),(4,2)):
  edges,orbits,_=graph(nx,ny);N=nx*ny;B=[{0:1}]
  for orb in orbits:B.append(plus(*[(pairvector([p]),1) for p in orb]))
  L=[act(b,A,edges,4) for b in B[1:]];R=[act(v,A,edges,4) for v in L];M=[act(v,A,edges,6) for v in L];U=[plus((r,1),(m,1)) for r,m in zip(R,M)]
  geo={k:[[dotv(a,b) for b in right] for a in left] for k,left,right in [('F',L,L),('S',L,R),('V',R,R),('W',M,M),('X',R,[act(r,A,edges,4) for r in R]),('Y',[act(r,A,edges,6) for r in R],M),('Z',M,[act(m,A,edges,6) for m in M])]}
  saved=load(OUT/'results'/f'geometry_{nx}x{ny}.json');assert all(geo[k]==saved[k] for k in geo)
  vectors=B+L+U;images=[h(v,A,edges) for v in vectors]
  gg=[[dotv(a,b) for b in vectors] for a in vectors];aa=[[F(dotv(a,hb),200) for hb in images] for a in vectors]
  r=rebuild(nx,ny,F(9,100),geo);assert gg==r['G'].tolist() and aa==r['A'].tolist()
  coeff=[7]+[(-1)**i*(i+1) for i in range(len(orbits))]+[-(-1)**i*(i+2) for i in range(len(orbits))]
  psi=plus(*zip(B+L,coeff));hp=h(psi,A,edges);h2p=h(hp,A,edges);norm=dotv(psi,psi)
  mom=[dotv(psi,hp),dotv(hp,hp),dotv(hp,h2p)]
  assert F(mom[2],200**3)==bil(coeff,r['H30'])
  p=load(P/f'physical_{nx}x{ny}.json')['fixture'];assert p['norm']==norm and [p[f'H{k}_numerator'] for k in (1,2,3)]==mom
  leaking=sum(x*x for s,x in h2p.items() if q(s)==8);assert leaking>0 if N==8 else leaking==0
  hp_cut={s:x for s,x in h2p.items() if q(s)<=6};assert dotv(hp,h2p)==dotv(hp,hp_cut)
  assert dotv(h2p,h2p)-dotv(hp_cut,hp_cut)==leaking
  rows.append(dict(shape=[nx,ny],all_F_S_V_W_X_Y_Z_exact=True,full_enlarged_G_and_A_exact=True,physical_H1_H2_H3_exact=True,unrestricted_H2psi_q8_norm_squared=leaking,H3_orthogonality_exact=True,H4_projection_norm_identity_exact=True,H4_projection_strictly_wrong=(leaking>0),physical_H3_numerator=str(mom[2])))
 save('sparse_physical_review.json',rows)
if __name__=='__main__':
 t=time.monotonic();A=local();match_tests(A);support_tests();physical(A);print('PASS spin kernel, matching recouplings, every stabilizer orbit, sparse physical moments; seconds',time.monotonic()-t,flush=True)
