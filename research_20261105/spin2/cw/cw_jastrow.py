"""Collatz-Wielandt (CW) lower bound on spin-1 Heisenberg e0 with translation-invariant
k-site Jastrow positive test vectors  log v(x) = sum_i theta(x_i..x_{i+k-1}).
Marshall-rotated bond: h = SzSz - (1/2)(S+S- + S-S+); all off-diagonal elements = -1 (spin-1).
Local bond energy e_b depends on 2k sites -> edge of de Bruijn graph on (2k-1)-site states.
Certified bound mu = min over edges of [e(edge) + phi(src) - phi(dst)]  (min-mean-cycle dual).
max_{theta,phi} mu is a CONVEX program (constraints: affine - sum exp(affine) >= mu).
Float solve with cvxpy/Clarabel; certification separately in cw_certify.py with arb."""
import numpy as np, itertools, scipy.sparse as sp, cvxpy as cp, json, sys, time
SP=[1,0,-1]  # local states index 0,1,2 -> m=+1,0,-1
def flips(a,b):
    """off-diagonal partners of (m_a,m_b) under S+S- + S-S+ : list of (a',b'), each coefficient (1/2)*2=1"""
    out=[]
    ma,mb=SP[a],SP[b]
    for da in (+1,-1):
        na,nb=ma+da,mb-da
        if abs(na)<=1 and abs(nb)<=1: out.append((SP.index(na),SP.index(nb)))
    return out
def build(k):
    W=2*k                     # edge = 2k sites x_0..x_{2k-1}; bond between sites k-1,k
    nwin=3**k
    def widx(t): 
        r=0
        for c in t: r=3*r+c
        return r
    rows=[];  # for each (edge, flip) a sparse row in theta
    zz=[];src=[];dst=[];fl_edge=[];data=[];ri=[];ci=[]
    nf=0
    for e,x in enumerate(itertools.product(range(3),repeat=W)):
        zz.append(SP[x[k-1]]*SP[x[k]])
        s=0
        for c in x[:-1]: s=3*s+c
        t=0
        for c in x[1:]: t=3*t+c
        src.append(s);dst.append(t)
        for (a2,b2) in flips(x[k-1],x[k]):
            y=list(x);y[k-1]=a2;y[k]=b2
            # windows starting at j=0..k (those containing site k-1 or k)
            for j in range(0,k+1):
                ri+= [nf,nf]; ci+=[widx(y[j:j+k]),widx(x[j:j+k])]; data+=[1.0,-1.0]
            fl_edge.append(e); nf+=1
    A=sp.csr_matrix((data,(ri,ci)),shape=(nf,nwin))
    A.sum_duplicates()
    F=sp.csr_matrix((np.ones(nf),(np.array(fl_edge),np.arange(nf))),shape=(3**W,nf))
    return dict(zz=np.array(zz,float),src=np.array(src),dst=np.array(dst),A=A,F=F,nwin=nwin,nstate=3**(W-1))
def solve(k,verbose=False):
    B=build(k); E=len(B['zz'])
    th=cp.Variable(B['nwin']); ph=cp.Variable(B['nstate']); mu=cp.Variable()
    Ssrc=sp.csr_matrix((np.ones(E),(np.arange(E),B['src'])),shape=(E,B['nstate']))
    Sdst=sp.csr_matrix((np.ones(E),(np.arange(E),B['dst'])),shape=(E,B['nstate']))
    expr=B['zz']+ (Ssrc-Sdst)@ph - B['F']@cp.exp(B['A']@th)
    cons=[expr>=mu, th[0]==0, ph[0]==0, cp.abs(th)<=15]
    pr=cp.Problem(cp.Maximize(mu),cons)
    t0=time.time(); 
    try: pr.solve(solver=cp.CLARABEL,verbose=verbose,max_iter=400,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,static_regularization_constant=1e-7)
    except Exception as ex:
        print('clarabel failed',ex,flush=True); pr.solve(solver=cp.SCS,verbose=verbose,eps=1e-9,max_iters=200000)
    return dict(k=k,mu_float=float(mu.value),status=pr.status,sec=time.time()-t0,theta=th.value.tolist(),phi=ph.value.tolist())
if __name__=='__main__':
    k=int(sys.argv[1]); r=solve(k)
    print(k,r['status'],r['mu_float'],r['sec'],flush=True)
    json.dump(r,open(f'jastrow_k{k}.json','w'))
