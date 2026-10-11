#!/usr/bin/env python3
"""Independent bounded exact tests: no physical many-rung vector is constructed."""
import collections, fractions, itertools, json, resource, time
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
start=time.process_time()
import sympy as S
F=fractions.Fraction
I=S.I; h=S.Rational(1,2)
sx=S.Matrix([[0,h],[h,0]]); sy=S.Matrix([[0,-I*h],[I*h,0]]); sz=S.diag(h,-h)
identity=S.eye(2)
spin1=[S.kronecker_product(a,identity) for a in (sx,sy,sz)]
spin2=[S.kronecker_product(identity,a) for a in (sx,sy,sz)]
r=S.sqrt(2)
U=S.Matrix.hstack(S.Matrix([0,1,-1,0])/r,S.Matrix([-1,0,0,1])/r,S.Matrix([I,0,0,I])/r,S.Matrix([0,1,1,0])/r)
assert S.simplify(U.H*U)==S.eye(4)
D=[S.simplify(U.H*(a-b)*U) for a,b in zip(spin1,spin2)]
T=[S.simplify(U.H*(a+b)*U) for a,b in zip(spin1,spin2)]
for a,d in enumerate(D,1):
    expected=S.zeros(4); expected[0,a]=expected[a,0]=1
    assert d==expected
A=sum((S.kronecker_product(d,d)+S.kronecker_product(t,t) for d,t in zip(D,T)),S.zeros(16))
s1=[S.simplify(U.H*a*U) for a in spin1]; s2=[S.simplify(U.H*a*U) for a in spin2]
V=sum((S.kronecker_product(a,a)+S.kronecker_product(b,b) for a,b in zip(s1,s2)),S.zeros(16))
assert A==2*V
vac=S.zeros(16,1); vac[0]=1
omega=S.zeros(16,1)
for a in range(1,4):omega[4*a+a]=1
assert A*vac==omega and (omega.H*omega)[0]==3
for a in range(1,4):
    v=S.zeros(16,1); v[a]=1
    w=S.zeros(16,1); w[4*a]=1
    assert A*v==w
TT=sum((S.kronecker_product(t,t) for t in T),S.zeros(16))
assert TT*omega==-2*omega
vertices=list(itertools.product(range(8),range(4)))
edges={tuple(sorted((u,((u[0]+dx)%8,(u[1]+dy)%4)))) for u in vertices for dx,dy in ((1,0),(0,1))}
adj={u:set() for u in vertices}
for u,v in edges:adj[u].add(v);adj[v].add(u)
assert len(edges)==64 and all(len(v)==4 for v in adj.values())
assert all((sum(u)-sum(v))%2 for u,v in edges)
counts=collections.Counter(); sumsq=0; records=[]
for u,v in itertools.combinations(vertices,2):
    n=len(adj[u]&adj[v])
    if n:
        assert (sum(u)-sum(v))%2==0
        counts[n]+=1;sumsq+=n*n;records.append([list(u),list(v),n])
assert counts=={1:32,2:80} and sumsq==352
# Direct q=2 image of z*Cdag vacuum under hopping: integer coefficient before g*z.
hop=collections.Counter()
for u,v in edges:
    for old,partner in ((u,v),(v,u)):
        for new in adj[old]-{partner}:
            hop[tuple(sorted((new,partner)))]+=1
assert all(hop[tuple((tuple(u),tuple(v)))]==2*n for u,v,n in records)
assert sum(3*c*c for c in hop.values())==4224 # multiplying (g*z/2)^2 gives 1056*g²*z²
# For all q=4 supports of two NN pairs, removing a NN pair leaves opposite sublattices.
q4_removals=0
for e,f in itertools.combinations(edges,2):
    occupied=set(e)|set(f)
    if len(occupied)!=4:continue
    for a,b in itertools.combinations(occupied,2):
        if tuple(sorted((a,b))) in edges:
            residual=occupied-{a,b};x,y=residual
            assert (sum(x)-sum(y))%2
            q4_removals+=1
z=-F(11,400);g=F(11,100)
num=3*sumsq*g*g*z*z
norm_upper=(1+48*z*z)**16
floor=num/norm_upper
out={'status':'PASS','geometry':[8,4],'vertices':32,'edges':64,'common_neighbor_pair_counts':dict(counts),'sum_n_squared':sumsq,'variance_numerator_coefficient':1056,'q4_annihilation_occupation_checks':q4_removals,'g':str(g),'z':str(z),'norm_upper_exact':str(norm_upper),'variance_floor_exact':str(floor),'variance_floor_decimal':float(floor),'same_sublattice_pairs':records,'cpu_seconds':time.process_time()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Exact local 16-dimensional algebra and geometry only; no full 8x4 state or eigensolver.'}
print(json.dumps(out,indent=2))
