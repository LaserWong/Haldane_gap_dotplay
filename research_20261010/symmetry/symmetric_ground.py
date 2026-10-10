"""Exact rational SU(2)/space-symmetry ground trials for ordinary halfspin bilayers.

State digits agree with low_energy/dimer_subspace.py. Sparse dictionaries contain
integer coefficients in the unnormalized rational dimer eigenbasis. T=4q(H-E00)
for coupling g=p/q. All H-applied configurations are retained for residuals.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import sys,math,json,itertools,time,resource,argparse
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sy

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'low_energy'))
from dimer_subspace import dimer_local,bilayer_bonds
from local_relative_bound import optimize_bound
OUT=Path(__file__).resolve().parent

class Model:
    def __init__(self,nx,ny,g):
        self.nx,self.ny,self.N,self.g=nx,ny,nx*ny,F(g)
        self.E00=-F(3*self.N,4)
        self.den=4*self.g.denominator
        self.lowmask=sum(1<<(2*i) for i in range(self.N))
        labels,weights,kernels=dimer_local(F(1,2))
        self.localweights=weights
        self.transitions=[]
        for c in range(16):
            acc=defaultdict(F)
            for layer in (0,1):
                for p,q,v in kernels[layer,layer][c]:acc[p,q]+=v*4
            self.transitions.append([(p,q,int(v)) for (p,q),v in acc.items() if v])
            assert all(v.denominator==1 for v in acc.values())
        edges=defaultdict(int)
        for i,aa,j,bb,g1 in bilayer_bonds(nx,ny,F(1),F(1)):
            if aa==0:edges[tuple(sorted((i,j)))]+=1
        self.edges=[(2*i,2*j,m) for (i,j),m in edges.items()]
    def weight(self,st):
        return 1<<(self.N-(st&self.lowmask).bit_count())
    def q(self,st):
        return ((st|(st>>1))&self.lowmask).bit_count()
    def apply(self,vec):
        """Return exact T vec; no support truncation."""
        out=defaultdict(int);p=self.g.numerator
        for st,c in vec.items():
            n=self.q(st)
            if n:out[st]+=self.den*n*c
            for i,j,m in self.edges:
                a=(st>>i)&3;b=(st>>j)&3
                for x,y,k in self.transitions[a*4+b]:
                    st1=st^((a^x)<<i)^((b^y)<<j)
                    out[st1]+=c*p*m*k
        return {st:c for st,c in out.items() if c}
    def inner(self,a,b):
        if len(a)>len(b):a,b=b,a
        return sum(c*b.get(st,0)*self.weight(st) for st,c in a.items())
    def group(self):
        """Translations, coordinate reflections, and x/y exchange only if square."""
        maps=set()
        for tx in range(self.nx):
            for ty in range(self.ny):
                for sx,sy1 in itertools.product((-1,1),repeat=2):
                    for swap in range(2 if self.nx==self.ny else 1):
                        perm=[]
                        for i in range(self.N):
                            x,y=divmod(i,self.ny)
                            if swap:x,y=y,x
                            perm.append(((sx*x+tx)%self.nx)*self.ny+(sy1*y+ty)%self.ny)
                        maps.add(tuple(perm))
        return sorted(maps)
    def q2_basis(self):
        remain=set(itertools.combinations(range(self.N),2));group=self.group();orbits=[]
        while remain:
            pair=min(remain)
            orb=sorted({tuple(sorted((perm[pair[0]],perm[pair[1]]))) for perm in group})
            assert set(orb)<=remain
            remain.difference_update(orb);orbits.append(orb)
        basis=[{0:1}]
        for orb in orbits:
            vec={}
            for i,j in orb:
                for a,b,c in ((1,3,-2),(2,2,1),(3,1,-2)):
                    vec[(a<<(2*i))|(b<<(2*j))]=c
            basis.append(vec)
        return basis,orbits

def primitive(v):
    d=math.gcd(*v.values()) if v else 1
    if d>1:return {s:c//d for s,c in v.items()}
    return v

def gram(model,vs,ws=None):
    if ws is None:ws=vs
    return [[model.inner(v,w) for w in ws] for v in vs]

def independent_indices(G):
    """Select independent vectors using exact positive-semidefinite Gram LDL."""
    selected=[];L=[];D=[]
    for i in range(len(G)):
        row=[]
        for j,idx in enumerate(selected):
            v=F(G[i][idx])-sum(row[k]*L[j][k]*D[k] for k in range(j))
            row.append(v/D[j])
        pivot=F(G[i][i])-sum(row[k]*row[k]*D[k] for k in range(len(D)))
        assert pivot>=0
        if pivot:
            selected.append(i);L.append(row+[F(1)]);D.append(pivot)
    return selected

def linear_combination(vectors,coefficients):
    out=defaultdict(int)
    for vec,c in zip(vectors,coefficients):
        for st,b in vec.items():out[st]+=int(c)*b
    return {st:c for st,c in out.items() if c}

def matrices(model,basis,applied=None):
    if applied is None:applied=[model.apply(v) for v in basis]
    G=gram(model,basis);K=gram(model,basis,applied);J=gram(model,applied)
    assert K==list(map(list,zip(*K)))
    return G,K,J,applied

def exact_certificate(model,basis,orbits,depth,bits=48,save=True,bound=None):
    start=time.monotonic();G,K,J,applied=matrices(model,basis);built=time.monotonic()
    normscales=np.sqrt(np.array([G[i][i] for i in range(len(G))],dtype=float))
    GG=np.array(G,dtype=float)/normscales[:,None]/normscales[None,:]
    KK=np.array(K,dtype=float)/normscales[:,None]/normscales[None,:]/model.den
    vals,vecs=la.eigh(KK,GG,check_finite=True)
    raw=vecs[:,0]/normscales
    # Max-coefficient normalization controls integer size for nonorthogonal bases.
    raw/=max(abs(raw));ints=[int(round(float(x)*2**bits)) for x in raw]
    v=linear_combination(basis,ints);Tv=linear_combination(applied,ints)
    norm=model.inner(v,v);vTv=model.inner(v,Tv);TvTv=model.inner(Tv,Tv)
    ray=F(vTv,model.den*norm)+model.E00
    r2=F(TvTv,model.den**2*norm)-F(vTv,model.den*norm)**2
    assert r2>=0
    if bound is None:bound=optimize_bound(F(1,2),model.g,'bilayer',model.N)
    a=model.E00+F(bound['second_shift_lower']);assert ray<a
    lo=ray-r2/(a-ray)
    full=4**model.N
    rec=dict(status='exact_rational_symmetry_compressed_ground_certificate',s='1/2',nx=model.nx,ny=model.ny,N_dimers=model.N,physical_sites=2*model.N,
        coupling=str(model.g),full_dimension=full,Sz0_full_dimension=math.comb(2*model.N,model.N),
        q2_Sz0_dimension=1+model.N+3*math.comb(model.N,2),q2_singlet_dimension=1+math.comb(model.N,2),
        trial_subspace_dimension=len(basis),q2_space_invariant_dimension=1+len(orbits),retained_states=1,
        pair_orbit_sizes=[len(x) for x in orbits],spatial_group_order=len(model.group()),block_krylov_depth=depth,
        trial_expanded_support_dimension=len(set().union(*(b.keys() for b in basis))),
        reached_support_dimension=len(set().union(*(b.keys() for b in basis+applied))),
        actual_trial_support_dimension=len(v),actual_H_applied_support_dimension=len(Tv),
        trial_max_excited_dimers=max(model.q(st) for b in basis for st in b),
        E00=str(model.E00),second_eigenvalue_lower=str(a),ground_lower=str(lo),ground_upper=str(ray),exact_rayleigh=str(ray),exact_residual_squared=str(r2),
        ground_lower_display=float(lo),ground_upper_display=float(ray),ground_width_display=float(ray-lo),exact_residual_squared_display=float(r2),
        shifted_ritz_energy_display=float(vals[0]),
        integer_matrix_denominator=model.den,relative_form_bound=bound,
        weak_bonds=[[i,aa,j,bb,str(g)] for i,aa,j,bb,g in bilayer_bonds(model.nx,model.ny,model.g,model.g)],
        bits=bits,coefficients=[str(c) for c in ints],gram=[[str(x) for x in row] for row in G],
        shifted_hamiltonian_numerator=[[str(x) for x in row] for row in K],shifted_H2_numerator=[[str(x) for x in row] for row in J],
        build_seconds=built-start,total_seconds=time.monotonic()-start,peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        proof='Exact rational Rayleigh and full leaked residual, plus independently certified all-sector relative-form bound and Temple. Symmetry compression makes no independent spectral-completeness claim.')
    if save:
        tag=f'symmetry_{model.nx}x{model.ny}_g{model.g}_block{depth}'.replace('/','d')
        (OUT/(tag+'.json')).write_text(json.dumps(rec,indent=2))
        # Exact sparse bases use decimal strings, supporting >64-bit Krylov coefficients.
        import gzip
        with gzip.open(OUT/(tag+'_basis.json.gz'),'wt') as f:json.dump([[[str(st),str(c)] for st,c in sorted(b.items())] for b in basis],f)
    print(json.dumps({k:rec[k] for k in ['nx','ny','coupling','block_krylov_depth','trial_subspace_dimension','trial_expanded_support_dimension','reached_support_dimension','ground_upper_display','ground_width_display','exact_residual_squared_display','build_seconds','total_seconds','peak_process_rss_kib']}),flush=True)
    return rec,applied

def run(nx,ny,g,depths):
    start=time.monotonic();model=Model(nx,ny,g);basis,orbits=model.q2_basis();bound=optimize_bound(F(1,2),model.g,'bilayer',model.N)
    recs=[]
    for depth in range(depths+1):
        rec,applied=exact_certificate(model,basis,orbits,depth,bound=bound);recs.append(rec)
        if depth==depths:break
        candidates=basis+[primitive(v) for v in applied]
        G=gram(model,candidates);inds=independent_indices(G);basis=[candidates[i] for i in inds]
        print('NEXT',depth+1,len(basis),len(set().union(*(b.keys() for b in basis))),flush=True)
    return recs

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nx',type=int,default=4);p.add_argument('--ny',type=int,default=4);p.add_argument('--g',default='1/100');p.add_argument('--depths',type=int,default=0)
    a=p.parse_args();run(a.nx,a.ny,a.g,a.depths)
