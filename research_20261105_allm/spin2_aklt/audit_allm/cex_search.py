# Hostile counterexample search for GM' (m >= n, any positive weights meeting the stated hypothesis).
import sys; sys.path.insert(0,'.')
from ff import *
from fractions import Fraction as Fr
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
def hyp(c,m):
    n=len(c)+1
    q=lambda x: sum(c[j]*c[j+x] for j in range(len(c)-x)) if 0<=x<len(c) else 0.0
    a=1/q(1); beta=a*q(0)-1
    worst=min([1-a*(q(e)+q(m-e)) for e in range(2,m//2+1)] or [1.0])
    S=sum(c); Fp=a*S*S/(n-1)
    return worst, Fp, beta
def models():
    # q-deformed XXZ ferro projector on qubits
    for qd in (1.0,0.5,0.2):
        v=np.zeros(4); v[1]=1; v[2]=-qd; v/=np.linalg.norm(v); yield f'xxz q={qd}',2,np.outer(v,v)
    P,_=proj_bond(1,[2]); yield 'AKLT S=1',3,P
    P,_=proj_bond(1,[1,2]); yield 'S=1 P1+P2',3,P
    for r in range(3):
        for (d,rk) in ((2,1),(2,2),(3,2),(3,4)):
            X=rng.normal(size=(d*d,rk))+1j*rng.normal(size=(d*d,rk)); Q,_=np.linalg.qr(X)
            yield f'rand d={d} rk={rk} #{r}',d,(Q@Q.conj().T)
rows=[]; worst_slack=np.inf
maxdim=int(sys.argv[2]) if len(sys.argv)>2 else 4100
for name,d,h in models():
    for n in range(3,8):
        if d**n>maxdim: break
        eps_n,_,_=gapnz(sp.csr_matrix(build(h.real if np.isrealobj(h) else h,d,n,chain(n)).toarray()) if False else None) if False else (None,None,None)
        Hn=sum_build=None
        # dense open chain
        def dense(L,bonds,w=None):
            N=d**L; H=np.zeros((N,N),complex)
            for b,(i,j) in enumerate(bonds):
                ww=1 if w is None else w[b]
                # embed h on sites i,j
                T=h.reshape(d,d,d,d)
                psi=np.eye(N).reshape([d]*L+[N])
                out=np.tensordot(T,psi,axes=([2,3],[i,j]))
                out=np.moveaxis(out,[0,1],[i,j]).reshape(N,N)
                H+=ww*out
            return H
        wn=np.linalg.eigvalsh(dense(n,chain(n))); eps_n=wn[wn>1e-9].min()
        for m in range(n,2*n+2):
            if d**m>maxdim: break
            wm=np.linalg.eigvalsh(dense(m,ring(m))); nzm=wm[wm>1e-9]; em=nzm.min()
            for t in range(60):
                kind=t%3
                if kind==0: c=rng.uniform(0.05,1,n-1)
                elif kind==1: c=np.ones(n-1); c[rng.integers(n-1)]=rng.uniform(0.01,3)
                else: c=np.exp(rng.normal(size=n-1)*1.5)
                wst,Fp,beta=hyp(list(c),m)
                if wst< -1e-12: continue
                bound=Fp*eps_n-beta
                slack=em-bound
                rows.append((name,n,m,slack))
                if slack<worst_slack: worst_slack=slack; print('new min slack %.3e'%slack,name,'n',n,'m',m,'eps_n %.4f eps_m %.4f bound %.4f'%(eps_n,em,bound),np.round(c,3),flush=True)
                if slack< -1e-9: print('COUNTEREXAMPLE',name,n,m,c,flush=True)
pos=[r for r in rows]
print('tested',len(rows),'(model,n,m,weights) cases; min slack',worst_slack, 'n<=m<2n cases',sum(1 for r in rows if r[2]<2*r[1]))
