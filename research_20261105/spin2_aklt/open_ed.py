"""NUMERICAL (float64): OPEN spin-2 chains with h = P3+P4 (a projector). Local gap eps_n of H_n=sum_{i<n-1} h_{i,i+1}.
Knabe: Delta_inf >= ((n-1)/(n-2))(eps_n - 1/(n-1)) [needs eps_n>1/(n-1)], applies to periodic chains m>n.
Gosset-Mozgunov: Delta_m >= (5/6)((n^2+n)/(n^2-4))(eps_n - 6/(n^2+n)) for m>2n>4 (periodic)."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, sys, json, time
from ed import bond, sector, d
def ham_open(L,states,h):
    dim=len(states); digits=np.zeros((dim,L),dtype=np.int64); x=states.copy()
    for s in range(L-1,-1,-1): digits[:,s]=x%d; x//=d
    pw=d**np.arange(L-1,-1,-1); rows=[];cols=[];vals=[]
    nz=[(p,q,h[p,q]) for p in range(25) for q in range(25) if abs(h[p,q])>1e-13]
    for i in range(L-1):
        j=i+1; ab=digits[:,i]*d+digits[:,j]
        for p,q,v in nz:
            ok=np.nonzero(ab==q)[0]
            if len(ok)==0: continue
            a2,b2=divmod(p,d); a1,b1=divmod(q,d)
            new=states[ok]+(a2-a1)*pw[i]+(b2-b1)*pw[j]
            pos=np.searchsorted(states,new); rows.append(pos); cols.append(ok); vals.append(np.full(len(ok),v))
    return sp.csr_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(dim,dim))
h=bond('P34',0)
for n in [int(a) for a in sys.argv[1:]]:
    t=time.time(); st=sector(n,0); H=ham_open(n,st,h)
    if len(st)<=3000: ev=np.linalg.eigvalsh(H.toarray())[:12]
    else: ev=np.sort(sla.eigsh(H,k=10,which='SA',tol=1e-12)[0])
    nzero=int(np.sum(np.abs(ev)<1e-8)); eps=float(ev[nzero])
    kn=(n-1)/(n-2)*(eps-1/(n-1)) if n>2 else None
    gm=(5/6)*((n*n+n)/(n*n-4))*(eps-6/(n*n+n)) if n>2 else None
    print(json.dumps(dict(n=n,dimSz0=len(st),zero_modes_Sz0=nzero,eps=eps,knabe=kn,gosset_mozgunov=gm,levels=[round(float(e),10) for e in ev],sec=round(time.time()-t,1))),flush=True)
