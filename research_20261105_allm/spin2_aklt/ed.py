"""NUMERICAL (float64, NOT rigorous): periodic spin-2 chains with bond h = poly(x), x = S_i.S_{i+1}.
Models: 'KHH' alpha: h = x + alpha*(2/9 x^2 + 1/63 x^3 + 10/7)  [Katsura-Hirano-Hatsugai family; alpha=1 is 10(P3/7+P4)]
        'P34': h = P3+P4.
Sz-sector sparse Lanczos. Output: lowest levels in Sz=0 and Sz=1 sectors."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, sys, json, time
from fractions import Fraction as F
S=2; d=5; m=np.arange(d)-S
def spin_mats():
    Sz=np.diag(m.astype(float)); Sp=np.zeros((d,d))
    for i in range(d-1): Sp[i+1,i]=np.sqrt(S*(S+1)-m[i]*(m[i]+1))
    return Sz,Sp,Sp.T
def bond(model, alpha):
    Sz,Sp,Sm=spin_mats(); x=np.kron(Sz,Sz)+0.5*(np.kron(Sp,Sm)+np.kron(Sm,Sp))
    I=np.eye(25)
    if model=='KHH':
        return x+alpha*(2/9*x@x+1/63*x@x@x+10/7*I)
    if model=='P34':
        c=[1,17/35,1/180,-1/45,-1/420]; return sum(ck*np.linalg.matrix_power(x,k) for k,ck in enumerate(c))
    if model=='LAM':  # AKLT10 + lam*(Heis - AKLT10) == KHH with alpha=1-lam
        return bond('KHH',1-alpha)
def sector(L,M):
    states=np.array([0],dtype=np.int64); tot=np.array([0])
    for site in range(L):
        states=(states[:,None]*d+np.arange(d)[None,:]).ravel(); tot=(tot[:,None]+m[None,:]).ravel()
        keep=np.abs(tot-M)<=S*(L-site-1); states,tot=states[keep],tot[keep]
    return states
def ham(L,states,h):
    dim=len(states); digits=np.zeros((dim,L),dtype=np.int64); x=states.copy()
    for s in range(L-1,-1,-1): digits[:,s]=x%d; x//=d
    pw=d**np.arange(L-1,-1,-1); rows=[];cols=[];vals=[]
    nz=[(p,q,h[p,q]) for p in range(25) for q in range(25) if abs(h[p,q])>1e-13]
    for i in range(L):
        j=(i+1)%L; ab=digits[:,i]*d+digits[:,j]
        for p,q,v in nz:   # <p|h|q>: state with pair q -> pair p
            ok=np.nonzero(ab==q)[0]
            if len(ok)==0: continue
            a2,b2=divmod(p,d); a1,b1=divmod(q,d)
            new=states[ok]+(a2-a1)*pw[i]+(b2-b1)*pw[j]
            pos=np.searchsorted(states,new); rows.append(pos); cols.append(ok); vals.append(np.full(len(ok),v))
    return sp.csr_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(dim,dim))
def low(L,M,h,k):
    st=sector(L,M); H=ham(L,st,h)
    if len(st)<=2000: ev=np.linalg.eigvalsh(H.toarray())[:k]
    else: ev=np.sort(sla.eigsh(H,k=k,which='SA',tol=1e-11)[0])
    return ev.tolist(), len(st)
if __name__=='__main__':
    model=sys.argv[1]; alpha=float(sys.argv[2]); Ls=[int(v) for v in sys.argv[3:]]
    h=bond(model,alpha); out={}
    for L in Ls:
        t=time.time(); e0,d0=low(L,0,h,6); e1,d1=low(L,1,h,3)
        E0=e0[0]; Esz0_2=[e for e in e0[1:]]; gap=min(e0[1],e1[0])-E0
        out[L]=dict(E0=E0,E0_per_site=E0/L,gap=gap,triplet_gap=e1[0]-E0,Sz0=e0,Sz1=e1,dims=[d0,d1],sec=time.time()-t)
        print(model,alpha,L,json.dumps(out[L]),flush=True)
    json.dump(out,open(f'ed_{model}_{alpha:g}_{Ls[0]}-{Ls[-1]}.json','w'),indent=1)
