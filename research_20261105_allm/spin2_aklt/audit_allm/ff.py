# Independent builder (auditor-written). Spin-S operators, bond = projector onto pair spin >= Jmin
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, itertools
def spin_ops(S):
    d=int(2*S+1); ms=np.array([S-k for k in range(d)])
    Sz=np.diag(ms); Sp=np.zeros((d,d))
    for k in range(1,d):
        m=ms[k]; Sp[k-1,k]=np.sqrt(S*(S+1)-m*(m+1))
    return Sz,Sp,Sp.T,ms
def proj_bond(S,Js):
    Sz,Sp,Sm,ms=spin_ops(S); d=len(ms); I=np.eye(d)
    SS=np.kron(Sz,Sz)+0.5*(np.kron(Sp,Sm)+np.kron(Sm,Sp))
    w,v=np.linalg.eigh(SS)
    J=np.round((-1+np.sqrt(1+4*(2*w+2*S*(S+1))))/2).astype(int)
    P=sum(np.outer(v[:,i],v[:,i]) for i in range(len(w)) if J[i] in Js)
    return P,ms
def sector_basis(d,L,ms,Mtot):
    digs=np.array(list(itertools.product(range(d),repeat=L)))
    sel=np.isclose(ms[digs].sum(1),Mtot) if Mtot is not None else np.ones(len(digs),bool)
    return digs[sel]
def build(h,d,L,bonds,weights=None,digs=None):
    if digs is None: digs=np.array(list(itertools.product(range(d),repeat=L)))
    pw=d**np.arange(L-1,-1,-1); idx=digs@pw; order=np.argsort(idx); assert np.all(order==np.arange(len(idx)))
    N=len(digs); R=[];C=[];V=[]
    nz=[(p,q,h[p,q]) for p in range(d*d) for q in range(d*d) if abs(h[p,q])>1e-14]
    for b,(i,j) in enumerate(bonds):
        w=1.0 if weights is None else weights[b]
        pair=digs[:,i]*d+digs[:,j]
        for p,q,v in nz:
            ok=np.nonzero(pair==q)[0]
            if len(ok)==0: continue
            nd=digs[ok].copy(); nd[:,i]=p//d; nd[:,j]=p%d
            tgt=np.searchsorted(idx,nd@pw)
            assert np.all(idx[tgt]==nd@pw)
            R.append(tgt);C.append(ok);V.append(np.full(len(ok),w*v))
    return sp.csr_matrix((np.concatenate(V),(np.concatenate(R),np.concatenate(C))),shape=(N,N))
def ring(L): return [(i,(i+1)%L) for i in range(L)]
def chain(L): return [(i,i+1) for i in range(L-1)]
def gapnz(H,k=None,tol=1e-9):
    N=H.shape[0]
    if N<=3000:
        w=np.linalg.eigvalsh(H.toarray())
    else:
        w=np.sort(sla.eigsh(H,k=k or 12,which='SA',tol=1e-10,return_eigenvectors=False))
    nz=w[w>tol]; return (nz.min() if len(nz) else np.inf), int((w<=tol).sum()), w
