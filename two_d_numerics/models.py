"""Transparent finite Heisenberg graphs. Energies use strong J=1.
Basis: site 0 is the least-significant base-(2s+1) digit; digit a means m=a-s.
Parallel periodic lattice bonds are retained explicitly, never deduplicated.
"""
from dataclasses import dataclass, asdict
from collections import Counter
from functools import lru_cache
import json, hashlib
import numpy as np
import scipy.sparse as sp
import scipy.linalg as la
from scipy.sparse.linalg import eigsh

@dataclass(frozen=True)
class Edge:
    i: int
    j: int
    coupling: float
    kind: str

@dataclass(frozen=True)
class Model:
    spin: float
    nsites: int
    edges: tuple
    label: str
    geometry: dict
    single_ion: float = 0.
    def metadata(self):
        return {**asdict(self), 'dimension': self.dimension, 'edge_counts':dict(Counter(e.kind for e in self.edges)), 'total_coupling':sum(e.coupling for e in self.edges)}
    @property
    def dimension(self): return int(2*self.spin+1)**self.nsites
    @property
    def fingerprint(self): return hashlib.sha256(json.dumps(self.metadata(),sort_keys=True).encode()).hexdigest()[:20]
    def validate(self):
        assert self.spin>0 and int(2*self.spin)==2*self.spin
        assert self.nsites>0
        assert all(0<=e.i<self.nsites and 0<=e.j<self.nsites and e.i!=e.j and np.isfinite(e.coupling) for e in self.edges)
        assert self.dimension<=10**8, 'Explicit basis ID resource guard exceeded'
        return self

def square(spin,nx,ny,jx=1.,jy=1.,periodic_x=False,periodic_y=False,periodic_convention='multigraph'):
    """Site=x*ny+y. A length-two periodic axis has two parallel lattice bonds
    in multigraph convention, one in simple. Only multigraph matches transfer.
    """
    assert nx>=1 and ny>=1 and periodic_convention in ('multigraph','simple')
    edges=[]
    for x in range(nx):
        for y in range(ny):
            i=x*ny+y
            for axis,n,a,J,pbc in [('x',nx,x,jx,periodic_x),('y',ny,y,jy,periodic_y)]:
                if n<2 or (a==n-1 and not pbc): continue
                if pbc and n==2 and periodic_convention=='simple' and a==1: continue
                j=((x+1)%nx)*ny+y if axis=='x' else x*ny+(y+1)%ny
                edges.append(Edge(i,j,float(J),axis))
    return Model(spin,nx*ny,tuple(edges),f'square_s{spin:g}_{nx}x{ny}',dict(family='square',nx=nx,ny=ny,periodic_x=periodic_x,periodic_y=periodic_y,periodic_convention=periodic_convention)).validate()

def columnar(spin,n,width,g,k,periodic_x=True,periodic_y=False):
    """Site=2*(x*width+y)+a, a=L:0,R:1. Strong R(x,y)-L(x+1,y);
    intracell g; vertical k on both legs. n=2 strong bonds are distinct pairs.
    Width=2 periodic retains the two lattice bonds per leg.
    """
    assert n>=2 and width>=1
    site=lambda x,y,a:2*(x*width+y)+a
    edges=[]
    for x in range(n):
        for y in range(width):
            edges.append(Edge(site(x,y,0),site(x,y,1),float(g),'intracell'))
            if x<n-1 or periodic_x:edges.append(Edge(site(x,y,1),site((x+1)%n,y,0),1.,'strong'))
            if width>1 and (y<width-1 or periodic_y):
                for a in [0,1]:edges.append(Edge(site(x,y,a),site(x,(y+1)%width,a),float(k),'transverse'))
    return Model(spin,2*n*width,tuple(edges),f'columnar_s{spin:g}_n{n}_w{width}_g{g:g}_k{k:g}',dict(family='columnar',n=n,width=width,g=g,k=k,periodic_x=periodic_x,periodic_y=periodic_y)).validate()

def large_d_square(nx,ny,gx,gy,D=1.,periodic_x=True,periodic_y=True):
    base=square(1.,nx,ny,gx,gy,periodic_x,periodic_y)
    return Model(base.spin,base.nsites,base.edges,f'largeD_{nx}x{ny}_gx{gx:g}_gy{gy:g}_D{D:g}',{**base.geometry,'family':'large_d','D':D,'gx':gx,'gy':gy},D).validate()

def bilayer(spin,nx,ny,gx,gy,periodic_x=False,periodic_y=False):
    """Strong interlayer dimers at every square-base vertex; weak in-layer bonds."""
    base=square(spin,nx,ny,gx,gy,periodic_x,periodic_y)
    edges=[Edge(2*i,2*i+1,1.,'rung') for i in range(nx*ny)]
    edges += [Edge(2*e.i+a,2*e.j+a,e.coupling,'inlayer_'+e.kind) for e in base.edges for a in [0,1]]
    return Model(spin,2*nx*ny,tuple(edges),f'bilayer_s{spin:g}_{nx}x{ny}_gx{gx:g}_gy{gy:g}',dict(family='bilayer',nx=nx,ny=ny,gx=gx,gy=gy,periodic_x=periodic_x,periodic_y=periodic_y)).validate()

@lru_cache(maxsize=24)
def basis(spin,nsites,twice_m):
    d=int(2*spin+1);qnum=twice_m+int(2*spin)*nsites
    if qnum%2:return np.empty(0,np.int64),np.empty((0,nsites),np.int8)
    q=qnum//2
    if q<0 or q>(d-1)*nsites:return np.empty(0,np.int64),np.empty((0,nsites),np.int8)
    counts=[1]
    for _ in range(nsites): counts=np.convolve(counts,np.ones(d,dtype=np.int64)).tolist()
    assert counts[q]<=300000, 'Sector resource guard exceeded before basis allocation'
    rows=[]
    def rec(left,total,prefix):
        if left==0:
            if total==0:rows.append(prefix)
            return
        for a in range(max(0,total-(left-1)*(d-1)),min(d-1,total)+1):rec(left-1,total-a,prefix+[a])
    rec(nsites,q,[])
    digits=np.asarray(rows,dtype=np.int8);pw=d**np.arange(nsites,dtype=np.int64)
    ids=digits@pw;order=np.argsort(ids)
    return ids[order],digits[order]

def hamiltonian(model,twice_m=0):
    ids,digits=basis(model.spin,model.nsites,twice_m)
    n=len(ids);d=int(2*model.spin+1);s=model.spin
    assert n<=300000, 'Sparse-sector resource guard exceeded'
    pw=d**np.arange(model.nsites,dtype=np.int64);m=digits.astype(float)-s
    diag=model.single_ion*np.sum(m*m,axis=1);rr=[];cc=[];vv=[]
    for edge in model.edges:
        i,j,J=edge.i,edge.j,edge.coupling
        if J==0:continue
        diag+=J*m[:,i]*m[:,j]
        for sign in [1,-1]:
            mask=((digits[:,i]<d-1)&(digits[:,j]>0)) if sign==1 else ((digits[:,i]>0)&(digits[:,j]<d-1))
            cols=np.flatnonzero(mask);dest=ids[cols]+sign*(pw[i]-pw[j]);rows=np.searchsorted(ids,dest)
            assert np.all(ids[rows]==dest)
            mi,mj=m[cols,i],m[cols,j]
            value=J*.5*np.sqrt((s*(s+1)-mi*(mi+sign))*(s*(s+1)-mj*(mj-sign)))
            rr.append(rows);cc.append(cols);vv.append(value)
    rr.append(np.arange(n));cc.append(np.arange(n));vv.append(diag)
    H=sp.coo_matrix((np.concatenate(vv),(np.concatenate(rr),np.concatenate(cc))),shape=(n,n)).tocsr()
    H.sum_duplicates();H.eliminate_zeros()
    assert np.max(np.abs((H-H.T).data),initial=0.)<1e-12
    return H

def raising(spin,nsites,twice_m):
    """S_total^+ between adjacent magnetization sectors."""
    ids,dig=basis(spin,nsites,twice_m);dest,_=basis(spin,nsites,twice_m+2)
    d=int(2*spin+1);pw=d**np.arange(nsites,dtype=np.int64);rr=[];cc=[];vv=[]
    for i in range(nsites):
        cols=np.flatnonzero(dig[:,i]<d-1);m=dig[cols,i]-spin;rows=np.searchsorted(dest,ids[cols]+pw[i])
        rr.extend(rows);cc.extend(cols);vv.extend(np.sqrt(spin*(spin+1)-m*(m+1)))
    return sp.coo_matrix((vv,(rr,cc)),shape=(len(dest),len(ids))).tocsr()

def independent_dense(model):
    """Independent tensor-product construction, hard limited to tiny references."""
    assert model.dimension<=1000, 'Full-Hilbert dense reference guard exceeded'
    s=model.spin;d=int(2*s+1);m=np.arange(d)-s
    plus=np.diag(np.sqrt(s*(s+1)-m[:-1]*(m[:-1]+1)),-1)
    ops=[(plus+plus.T)/2,(plus-plus.T)/(2j),np.diag(m)];local=[]
    for i in range(model.nsites):
        row=[]
        for op in ops:
            mat=np.ones((1,1))
            for j in reversed(range(model.nsites)):mat=np.kron(mat,op if j==i else np.eye(d))
            row.append(mat)
        local.append(row)
    H=np.zeros((model.dimension,model.dimension),complex)
    for i in range(model.nsites):H+=model.single_ion*(local[i][2]@local[i][2])
    for e in model.edges:
        for a in range(3):H+=e.coupling*(local[e.i][a]@local[e.j][a])
    assert np.max(abs(H.imag))<1e-13
    return H.real

def full_spectrum(model,max_block=2000):
    es=[];sectors=[];parity=int(2*model.spin*model.nsites)%2
    for m2 in range(parity,int(2*model.spin*model.nsites)+1,2):
        H=hamiltonian(model,m2)
        assert H.shape[0]<=max_block, 'Full-sector ED guard exceeded'
        e=la.eigvalsh(H.toarray(),check_finite=False);mult=1 if m2==0 else 2
        es.extend([e]*mult);sectors.append((m2,H.shape[0],mult))
    out=np.sort(np.concatenate(es));assert len(out)==model.dimension
    return out,sectors

def low_sector(model,twice_m,k=24,dense_cut=1200):
    H=hamiltonian(model,twice_m)
    if H.shape[0]<=dense_cut or k>=H.shape[0]-1:
        e,v=la.eigh(H.toarray(),check_finite=False,subset_by_index=[0,min(k,H.shape[0])-1]);method='dense_subset'
    else:
        rng=np.random.default_rng(90137+twice_m)
        e,v=eigsh(H,k=k,which='SA',tol=2e-12,maxiter=20000,ncv=min(H.shape[0],max(4*k+1,80)),v0=rng.normal(size=H.shape[0]))
        order=np.argsort(e);e=e[order];v=v[:,order];method='eigsh'
    residual=np.linalg.norm(H@v-v*e[None,:],axis=0)
    return dict(twice_m=twice_m,dimension=H.shape[0],eigenvalues=e.tolist(),residuals=residual.tolist(),orthogonality_error=float(np.max(abs(v.T@v-np.eye(len(e))))),method=method,certified=False)
