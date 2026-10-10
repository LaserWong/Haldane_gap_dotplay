"""Independent rational audit of a fixed-ansatz residual obstruction.

Imports no producer or previous-review arithmetic. Rebuilds the q2 action and
its entire q4 leakage directly from graph pairings. Only S,V,W geometry for the
11D comparison is inherited from the hash-verified independent large-seed audit.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
if hasattr(os, 'sched_setaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from collections import Counter
from math import isqrt
import hashlib, json, time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
RESEARCH = ROOT / 'research_20261010'
READ_HASHES = {}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read(rel):
    """Create a read-only-input snapshot on first run and prohibit drift later."""
    p = ROOT / rel
    raw = p.read_bytes()
    snapshot = OUT / 'snapshot' / rel
    if snapshot.exists():
        assert snapshot.read_bytes() == raw, ('changed input', rel)
    else:
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(raw)
    READ_HASHES[str(rel)] = digest(raw)
    return json.loads(raw)

def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)):
        return [serial(v) for v in x]
    return x

def zeros(n,m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]

def transpose(a):
    return [list(row) for row in zip(*a)]

def mm(a,b):
    bt=transpose(b)
    return [[sum((u*v for u,v in zip(row,col)),F(0)) for col in bt] for row in a]

def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]

def scale(a,t):
    return [[t*x for x in row] for row in a]

def block(a,b,c,d):
    return [r+s for r,s in zip(a,b)]+[r+s for r,s in zip(c,d)]

def qform(a,v):
    return sum((v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),F(0))

def determinant(a):
    """Bareiss determinant with row swaps, entirely rational."""
    a=[row[:] for row in a]
    old=F(1)
    sign=1
    for k in range(len(a)-1):
        if a[k][k]==0:
            pivot=next((i for i in range(k+1,len(a)) if a[i][k]),None)
            if pivot is None:
                return F(0)
            a[k],a[pivot]=a[pivot],a[k]
            sign=-sign
        p=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                a[i][j]=(p*a[i][j]-a[i][k]*a[k][j])/old
        old=p
    return sign*a[-1][-1]

def leading_minors(a):
    return [determinant([row[:n] for row in a[:n]]) for n in range(1,len(a)+1)]

def positive(a):
    assert a==transpose(a)
    # Sylvester's criterion, independent of the producer's LDL routine.
    return all(x>0 for x in leading_minors(a))

def graph_pair_geometry():
    n=4
    edges=Counter()
    for x in range(n):
        for y in range(n):
            s=x*n+y
            edges[tuple(sorted((s,((x+1)%n)*n+y)))]+=1
            edges[tuple(sorted((s,x*n+(y+1)%n)))]+=1
    pairs=list(combinations(range(n*n),2))
    # Construct orbits by explicit translations and the D4 point-group action.
    pending=set(pairs)
    orbits=[]
    while pending:
        i,j=min(pending)
        images=set()
        for swap in (False,True):
            for sx in (-1,1):
                for sy in (-1,1):
                    for tx in range(n):
                        for ty in range(n):
                            image=[]
                            for site in (i,j):
                                x,y=divmod(site,n)
                                if swap:
                                    x,y=y,x
                                image.append(((sx*x+tx)%n)*n+(sy*y+ty)%n)
                            images.add(tuple(sorted(image)))
        assert images<=pending
        orbits.append(sorted(images))
        pending-=images
    assert len(orbits)==5
    ids={pair:k for k,orbit in enumerate(orbits) for pair in orbit}
    D=zeros(6)
    D[0][0]=1
    for k,orbit in enumerate(orbits,1):
        D[k][k]=3*len(orbit)
    # L=A42 Bpair. On each four-set its three pairings have Gram 6I+3ee^T.
    leakage=zeros(5)
    for a,b,c,d in combinations(range(16),4):
        pairing=[((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]
        amps=zeros(3,5)
        for row,(p,q) in enumerate(pairing):
            amps[row][ids[q]]+=edges[p]
            amps[row][ids[p]]+=edges[q]
        sums=[sum(amps[r][i] for r in range(3)) for i in range(5)]
        for i in range(5):
            for j in range(5):
                leakage[i][j]+=6*sum(amps[r][i]*amps[r][j] for r in range(3))+3*sums[i]*sums[j]
    return edges,orbits,ids,D,leakage

def matrices(g,geom,edges,orbits,ids,D,Lgram):
    t=g/2
    C=zeros(6)
    for col in range(6):
        pair_coeff={pair:F(int(col>0 and ids[pair]==col-1)) for pair in ids}
        vacuum=F(col==0)
        C[0][col]=3*t*sum(edges[p]*v for p,v in pair_coeff.items())
        images={}
        for i,j in ids:
            pair=(i,j)
            value=t*edges[pair]*vacuum+(2-2*t*edges[pair])*pair_coeff[pair]
            for k in range(16):
                if k not in (i,j):
                    value+=t*(edges[tuple(sorted((i,k)))]*pair_coeff[tuple(sorted((k,j)))]+
                              edges[tuple(sorted((j,k)))]*pair_coeff[tuple(sorted((k,i)))])
            images[pair]=value
        for row,orbit in enumerate(orbits,1):
            assert len({images[p] for p in orbit})==1
            C[row][col]=images[orbit[0]]
    E=[([F(0)]*5)]+Lgram
    S,V,W=[[[F(x) for x in row] for row in geom[k]] for k in ('S','V','W')]
    # Orthogonal components of H'B and H'L.
    BB=mm(mm(transpose(C),D),C)
    for i in range(5):
        for j in range(5):
            BB[i+1][j+1]+=t*t*Lgram[i][j]
    BL=scale(mm(transpose(C),E),t)
    q4part=add(scale(Lgram,4),scale(S,t))
    for i in range(5):
        for j in range(5):
            BL[i+1][j]+=t*q4part[i][j]
    DinvE=[[E[i][j]/D[i][i] for j in range(5)] for i in range(6)]
    LL=add(add(scale(Lgram,16),scale(S,8*t)),scale(add(add(V,W),mm(transpose(E),DinvE)),t*t))
    G=block(D,zeros(6,5),zeros(5,6),Lgram)
    A=block(mm(D,C),scale(E,t),scale(transpose(E),t),q4part)
    B=block(BB,BL,transpose(BL),LL)
    assert G==transpose(G) and A==transpose(A) and B==transpose(B)
    return G,A,B

def center_matrix(A,B,G,c):
    return add(add(B,scale(A,-2*c)),scale(G,c*c))

def uniform_certificate(A,B,G,lo,hi,gamma=None):
    assert lo<=hi
    c=(lo+hi)/2
    h=(hi-lo)/2
    Q=center_matrix(A,B,G,c)
    if gamma is None:
        a,b=F(0),F(1,5)
        for _ in range(36):
            m=(a+b)/2
            if positive(add(Q,scale(G,-m))):
                a=m
            else:
                b=m
        gamma=a
    P=add(Q,scale(G,-gamma))
    minors=leading_minors(P)
    assert gamma>0 and all(x>0 for x in minors)
    denom=10**15
    alpha=F(isqrt(gamma.numerator*denom**2//gamma.denominator),denom)
    assert alpha*alpha<=gamma<(alpha+F(1,denom))**2
    assert alpha>h
    return dict(interval=[lo,hi],midpoint=c,halfwidth=h,generalized_squared_singular_lower=gamma,
                positive_leading_minors=minors,sqrt_lower=alpha,residual_squared_lower=(alpha-h)**2)

def main():
    start=time.monotonic()
    review=read('research_20261010/large_seed_review/MANIFEST_SHA256.json')
    geom_path='research_20261010/large_seed_review/results/geometry_4x4.json'
    geom=read(geom_path)
    assert READ_HASHES[geom_path]==review['results/geometry_4x4.json']
    old_review=read('research_20261010/large_seed_review/results/ground_replay.json')
    assert READ_HASHES['research_20261010/large_seed_review/results/ground_replay.json']==review['results/ground_replay.json']
    proposal=read('research_20261010/trial_size_criteria/residual_obstructions.json')
    edges,orbits,ids,D,Lgram=graph_pair_geometry()
    assert Lgram==[[F(v) for v in row] for row in geom['F']]
    rows=[]
    for prop in proposal['results']:
        tag=prop['g']
        g=F(tag.replace('d','/'))
        rel=f'research_20261010/large_seed_moments/block1_4x4_g{tag}.json'
        rec=read(rel)
        assert READ_HASHES[rel]==proposal['input_sha256'][rel]
        inherited='snapshot/'+rel
        assert review[inherited]==READ_HASHES[rel]
        assert any(x['shape']=='4x4' and x['g']==str(g) and x['Temple_available'] for x in old_review)
        GG,AA,BB=matrices(g,geom,edges,orbits,ids,D,Lgram)
        assert positive(GG)
        den=F(rec['integer_matrix_denominator'])
        assert GG==[[F(v) for v in row] for row in rec['gram']]
        assert AA==[[F(v)/den for v in row] for row in rec['shifted_hamiltonian_numerator']]
        assert BB==[[F(v)/den**2 for v in row] for row in rec['shifted_H2_numerator']]
        G,A,B=([row[:6] for row in m[:6]] for m in (GG,AA,BB))
        assert positive(G)
        # Directly identify the omitted-q4 norm. The obstruction keeps this term.
        compressed=mm(mm(A,[[F(int(i==j))/G[i][i] for j in range(6)] for i in range(6)]),A)
        leak=add(B,scale(compressed,-1))
        expected=zeros(6)
        for i in range(5):
            for j in range(5):
                expected[i+1][j+1]=(g/2)**2*Lgram[i][j]
        assert leak==expected and any(v for row in leak for v in row)
        lo,hi=map(F,prop['shifted_Rayleigh_interval'])
        gamma=F(prop['matrix_lower_bound'])
        cert=uniform_certificate(A,B,G,lo,hi,gamma)
        # Independently verify saved LDL pivots using determinant ratios.
        minors=cert['positive_leading_minors']
        piv=[minors[0]]+[minors[i]/minors[i-1] for i in range(1,6)]
        assert piv==list(map(F,prop['exact_positive_LDL_pivots']))
        alpha=F(prop['sqrt_lower'])
        h=(hi-lo)/2
        target=F(prop['residual_squared_target'])
        assert alpha**2<=gamma and alpha>h
        assert (alpha-h)**2==F(prop['uniform_residual_squared_lower'])>target
        v=list(map(F,rec['coefficients']))
        norm=qform(GG,v)
        rho=qform(AA,v)/norm
        rs=qform(BB,v)/norm-rho**2
        assert F(rec['E00'])==-12 and rho==F(rec['exact_rayleigh'])+12
        assert rs==F(rec['exact_residual_squared'])==F(prop['block1_residual_squared'])
        assert lo<=rho<=hi and 0<rs<target
        assert len(v)==11 and rec['trial_subspace_dimension']==11
        assert rec['selected_basis_indices']==list(range(11))
        old_a=F(rec['second_eigenvalue_lower'])+12
        assert old_a>rho
        temple=rho-rs/(old_a-rho)
        assert temple==F(rec['ground_lower'])+12
        wider=uniform_certificate(A,B,G,temple,rho+F(1,1000))
        assert temple<=lo and hi==rho+F(1,1000)
        assert wider['residual_squared_lower']>target
        rows.append(dict(g=g,shape=[4,4],full_hilbert_dimension=4**16,
                         fixed_ansatz_dimension=6,enlarged_ansatz_dimension=11,
                         producer_interval=cert,
                         producer_residual_squared_floor=F(prop['uniform_residual_squared_lower']),
                         audited_Temple_interval=wider,target=target,
                         eleven_dimensional_vector_residual_squared=rs,
                         eleven_dimensional_vector_shifted_rayleigh=rho,
                         complete_q4_leakage_independently_rebuilt=True,
                         eleven_dimensional_matrices_match_audited_geometry=True))
        print('PASS',g,'producer floor',float(F(prop['uniform_residual_squared_lower'])),
              'wider interval floor',float(wider['residual_squared_lower']),
              'target',float(target),'11D residual',float(rs),flush=True)
    result=dict(status='PASS fixed-space residual floor and 11D constructive comparison',
                scope='Four discrete g values, periodic 4x4 ordinary bilayer, unit rung coupling. No arbitrary minimum-dimension or coupling-interval claim.',
                pair_orbit_sizes=[len(x) for x in orbits],results=rows,
                input_sha256=READ_HASHES,seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/'results/residual_review.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    for rel,sha in READ_HASHES.items():
        assert digest((ROOT/rel).read_bytes())==sha
    print('seconds',result['seconds'],'peak RSS KiB',result['peak_rss_kib'],flush=True)

if __name__=='__main__':
    main()
