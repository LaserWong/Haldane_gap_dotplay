"""Exact comparisons to saved physical-support block matrices and independent spin action."""
import json,math,time,itertools
import numpy as np
from collections import defaultdict
from fractions import Fraction as F
from large_seed_moments import ROOT,OUT,geometry,matrices
from symmetric_ground import Model,gram,primitive,independent_indices
from verify_symmetry import pair_vec,tensor_disjoint,expand_physical,physical_T

def pairing_vector(N,matching):
    v={0:1}
    for a,b in matching:v=tensor_disjoint(v,pair_vec(N,a,b))
    return v

def canonical(mat):return tuple(sorted(tuple(sorted(pair)) for pair in mat))

def symbolic_T(model,matching):
    """All occupation sectors, independent matching rules for Q+g/2(TT+DD)."""
    matching=canonical(matching);partner={a:b for pair in matching for a,b in [pair,pair[::-1]]};out=defaultdict(int)
    out[matching]+=2*len(matching)*model.den
    for ai,bi,mul in model.edges:
        a,b=ai//2,bi//2;h=2*model.g.numerator*mul
        if a not in partner and b not in partner:out[canonical(matching+((a,b),))]+=h
        elif a in partner and b in partner:
            c,e=partner[a],partner[b]
            if c==b:
                out[matching]-=2*h
                out[canonical([pair for pair in matching if pair!=tuple(sorted((a,b)))])]+=3*h
            else:
                rest=[pair for pair in matching if a not in pair and b not in pair]
                out[canonical(rest+[(a,e),(b,c)])]+=h
                out[canonical(rest+[(a,b),(c,e)])]-=h
                out[canonical(rest+[(c,e)])]+=h
        else:
            if b in partner:a,b=b,a
            out[canonical([(b if i==a else i,b if j==a else j) for i,j in matching])]+=h
    vec=defaultdict(int)
    for mat,coef in out.items():
        for st,c in pairing_vector(model.N,mat).items():vec[st]+=coef*c
    return {st:c for st,c in vec.items() if c}

def matchings(vertices):
    if not vertices:yield ();return
    first,*others=vertices
    for second in others:
        for rem in matchings([x for x in others if x!=second]):yield ((first,second),)+rem

def verify():
    start=time.monotonic();checks=[]
    # Every q0/q2/q4/q6 matching on six rungs; physical 12-spin Hilbert is 4096.
    m=Model(3,2,'3/100');count=0
    for q in [0,2,4,6]:
        for occupied in itertools.combinations(range(m.N),q):
            for mat in matchings(occupied):
                v=pairing_vector(m.N,mat);sym=symbolic_T(m,mat)
                assert sym==m.apply(v),(q,mat,'rational dimer action')
                assert expand_physical(sym,m.N)==physical_T(m,expand_physical(v,m.N)),(q,mat,'physical spin action')
                count+=1
    checks.append(f'Independent direct physical-spin T action exactly matches symbolic TT/DD matching rules on all {count} matchings for 3x2, including q0/q2/q4/q6 and length-two parallel edges.')
    mats=list(matchings(tuple(range(6))));vs=[pairing_vector(6,mat) for mat in mats]
    for i,a in enumerate(mats):
        for j,b in enumerate(mats):
            edges=a+b;remaining=set(range(6));loops=0
            while remaining:
                reached={next(iter(remaining))};change=True
                while change:
                    new=reached|{y for pair in edges for x,y in [pair,pair[::-1]] if x in reached};change=new!=reached;reached=new
                remaining-=reached;loops+=1
            assert m.inner(vs[i],vs[j])==2**6*3**loops
    checks.append('All 225 six-triplet pairing Gram entries exactly equal 2**6 times 3**union_loops in the physical rational basis.')
    for nx,ny in [(2,2),(4,2),(4,4)]:
        geom=geometry(nx,ny)
        for g in ['1/100','1/50','3/100']:
            model,G,K,J,mom=matrices(nx,ny,g,geom);bs,_=model.q2_basis();d=len(bs);n=d-1
            applied=[model.apply(b) for b in bs];prims=[primitive(a) for a in applied]
            explicit=bs+prims;sel=independent_indices(gram(model,explicit));D=[]
            # Columns expressing the saved B+primitive(TB) basis in (B,L).
            C=np.zeros((2*d-1,2*d),dtype=object);C[:d,:d]=np.eye(d,dtype=object)
            for i,a in enumerate(applied):
                divisor=math.gcd(*a.values()) if a else 1
                for j,b in enumerate(bs):C[j,d+i]=F(model.inner(b,a),2**model.N*int(mom[0][j,j])*divisor)
                if i:C[d+i-1,d+i]=F(2*model.g.numerator,divisor)
            C=C[:,sel]
            saved=json.loads((ROOT/'research_20261010'/'symmetry'/(f'symmetry_{nx}x{ny}_g{g}_block1.json'.replace('/','d'))).read_text())
            for key,A in [('gram',G),('shifted_hamiltonian_numerator',K),('shifted_H2_numerator',J)]:
                transformed=(C.T@A@C)*2**model.N
                assert transformed.tolist()==[[int(x) for x in row] for row in saved[key]],(nx,ny,g,key)
            checks.append(f'All saved block1 G/K/J entries exactly match after explicit integer-basis transformation on {nx}x{ny}, g={g}; dimension {len(sel)}.')
    rec=dict(status='passed',checks=checks,total_seconds=time.monotonic()-start,independence='Matching rules checked against independent physical-spin action; saved large block matrix comparisons share local conventions, independent worker review pending.')
    (OUT/'verification.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2),flush=True)

if __name__=='__main__':verify()
