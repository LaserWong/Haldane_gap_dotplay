# Hostile search v2: only cases with positive bound; includes adversarial local search over weights.
import sys; sys.path.insert(0,'.')
from ff import *
rng=np.random.default_rng(int(sys.argv[1]))
def hyp(c,m):
    n=len(c)+1
    q=lambda x: sum(c[j]*c[j+x] for j in range(len(c)-x)) if 0<=x<len(c) else 0.0
    a=1/q(1); beta=a*q(0)-1
    worst=min([1-a*(q(e)+q(m-e)) for e in range(2,m//2+1)] or [1.0])
    return worst, a*sum(c)**2/(n-1), beta
def bnd(c,m,eps_n):
    w,Fp,b=hyp(c,m)
    return (Fp*eps_n-b) if w>=-1e-12 else -np.inf
def eig(H):
    if H.shape[0]<=2500: w=np.linalg.eigvalsh(H.toarray())
    else: w=sla.eigsh(H,k=6,which='SA',tol=1e-10,return_eigenvectors=False)
    return w[w>1e-8].min()
def models():
    for qd in ():
        v=np.zeros(4); v[1]=1; v[2]=-qd; v/=np.linalg.norm(v); yield f'xxzq{qd}',2,np.outer(v,v),None
    for r in range(4):
        for (d,rk) in ((2,1),(2,2),(3,3),(3,5),(3,7)):
            X=rng.normal(size=(d*d,rk)); Q,_=np.linalg.qr(X); yield f'rand{d}r{rk}#{r}',d,Q@Q.T,None
cnt=0;cntin=0;minrel=np.inf
for name,d,h,ms in models():
    for n in range(3,9):
        cap=200000 if ms is not None else 2500
        dig=lambda L: sector_basis(d,L,ms,0 if (2*ms[0])%2==0 else 0.5) if ms is not None else None
        if d**n>40*cap: break
        en=eig(build(h,d,n,chain(n),digs=dig(n)))
        for m in range(n,2*n+1):
            if d**m>40*cap: break
            D=dig(m)
            if D is not None and len(D)>cap: break
            if D is None and d**m>cap: break
            em=eig(build(h,d,m,ring(m),digs=D))
            # random + adversarial weights
            best=None
            for t in range(400):
                c=np.exp(rng.normal(size=n-1)*rng.uniform(0,2))
                b=bnd(list(c),m,en)
                if b>-np.inf and (best is None or b>best[0]): best=(b,c)
            if best is None: continue
            b,c=best
            for it in range(300):  # hill-climb to maximize the bound (worst case for the lemma)
                c2=c*np.exp(rng.normal(size=n-1)*0.05); b2=bnd(list(c2),m,en)
                if b2>b: b,c=b2,c2
            cnt+=1; cntin+= (m<2*n)
            if b>0: minrel=min(minrel,(em-b)/em)
            flag='COUNTEREXAMPLE' if em<b-1e-9 else ''
            print(f'{name:12s} n={n} m={m} eps_n={en:.5f} eps_m={em:.5f} maxbound={b:.5f} slack={em-b:.2e} {flag}',flush=True)
print('cases',cnt,'with n<=m<2n',cntin,'min relative slack (bound>0)',minrel)
