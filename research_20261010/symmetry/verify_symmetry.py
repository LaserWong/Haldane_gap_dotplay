"""Reproducible exact checks; independent physical spin action on the 2x2 patch."""
import sys,json,itertools,time,gzip
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from symmetric_ground import Model,OUT,gram,matrices,linear_combination
from analytic_q2 import analytic_matrices,bilinear

def expand_physical(vec,N):
    # Physical bit pair labels dd,ud,du,uu; changing every singlet's phase
    # multiplies all even-triplet trial sectors by the same overall phase.
    local=[[(1,-1),(2,1)],[(0,1)],[(1,1),(2,1)],[(3,1)]]
    out=defaultdict(int)
    for st,c in vec.items():
        partial={0:c}
        for i in range(N):
            nxt={}
            for s,a in partial.items():
                for digit,b in local[(st>>(2*i))&3]:nxt[s|(digit<<(2*i))]=a*b
            partial=nxt
        for s,a in partial.items():out[s]+=a
    return {s:a for s,a in out.items() if a}

def physical_T(model,vec):
    """T=4q(H+3N/4) directly using physical spin exchanges, no dimer kernels."""
    out=defaultdict(int);p=model.g.numerator;q=model.g.denominator
    bonds=[(2*i,2*i+1,q) for i in range(model.N)]
    for ai,aj,m in model.edges:
        for layer in (0,1):bonds.append((ai+layer,aj+layer,p*m))
    for st,c in vec.items():
        out[st]+=3*model.N*q*c
        for i,j,coup in bonds:
            opposite=((st>>i)^(st>>j))&1
            out[st]+=(-1 if opposite else 1)*coup*c
            if opposite:out[st^(1<<i)^(1<<j)]+=2*coup*c
    return {st:c for st,c in out.items() if c}

def dot(a,b):return sum(x*b.get(s,0) for s,x in a.items())

def pair_vec(N,i,j):
    return {(a<<(2*i))|(b<<(2*j)):c for a,b,c in ((1,3,-2),(2,2,1),(3,1,-2))}

def tensor_disjoint(a,b):
    out=defaultdict(int)
    for s,c in a.items():
        for t,d in b.items():assert not s&t;out[s|t]+=c*d
    return dict(out)

def verify():
    start=time.monotonic();checks=[]
    m4=Model(2,2,'3/100')
    pairings=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
    vs=[tensor_disjoint(pair_vec(4,*a),pair_vec(4,*b)) for a,b in pairings]
    P=gram(m4,vs)
    assert P==[[16*(9 if i==j else 3) for j in range(3)] for i in range(3)]
    checks.append('Exact four-triplet three-pairing Gram is 2^N times diag9/off3, including signs.')
    for g in ['1/100','1/50','3/100']:
        m=Model(2,2,g);bs,orbits=m.q2_basis();G,K,J,applied=matrices(m,bs)
        phys=[expand_physical(b,m.N) for b in bs];Tp=[physical_T(m,b) for b in phys]
        for i in range(len(bs)):
            assert Tp[i]==expand_physical(applied[i],m.N)
            for j in range(len(bs)):
                assert dot(phys[i],phys[j])==G[i][j]
                assert dot(phys[i],Tp[j])==K[i][j]
                assert dot(Tp[i],Tp[j])==J[i][j]
        checks.append(f'Independent full physical-spin T action and G/K/J exactly match on2x2 g={g}.')
    for g in ['1/100','1/50','3/100']:
        for nx,ny in [(2,2),(4,2),(4,4)]:
            r=json.loads((OUT/(f'symmetry_{nx}x{ny}_g{g}_block0.json'.replace('/','d'))).read_text())
            m=Model(nx,ny,g);G,K,J,orbits,cost=analytic_matrices(m)
            for key,A in [('gram',G),('shifted_hamiltonian_numerator',K),('shifted_H2_numerator',J)]:
                assert [[x*2**m.N for x in row] for row in A]==[[int(x) for x in row] for row in r[key]],key
            baseline=Path(__file__).resolve().parents[2]/'low_energy'/(f'bilayer_s1d2_{nx}x{ny}_g{g}_k{g}_q2_ground.json'.replace('/','d'))
            old=json.loads(baseline.read_text())
            assert abs(F(old['exact_rayleigh'])-F(r['exact_rayleigh']))<F(1,10**20)
            assert abs(F(old['exact_residual_squared'])-F(r['exact_residual_squared']))<F(1,10**13)
            checks.append(f'Analytic/explicit integer G/K/J identical, old Sz0 Ritz minimum agreement<1e-20 on{nx}x{ny} g={g}.')
    rec=dict(status='passed',checks=checks,total_seconds=time.monotonic()-start,independence='Physical-spin action is independent of dimer kernels; analytic vs explicit and baseline comparisons share portions of construction and are cross-checks, not a separate worker audit.')
    (OUT/'verification.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))

if __name__=='__main__':verify()
