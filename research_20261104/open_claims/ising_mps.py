# Claim A3: finite-temperature (purification) MPS as fuzzy input, periodic TFI H=-J sum ZZ - h sum X, J=1, h=5,
# seed n=2, beta=1/2.  Claimed all-size lower bounds chi=6,9,16: 1.492020, 1.714857, 1.931304; ideal 1.973380.
# Pipeline (own implementation; the chat's code is not in the bundle/repo):
#   Y ~ exp(-beta' H/2) from a purification MPS (L sites, local dim 4 = phys x ancilla, open-chain MPS,
#   periodic bond applied as a full two-site gate on the dense tensor), Trotter steps with per-step SVD truncation to chi.
#   eta = ||Y - exp(-beta' H/2)||_F  : RIGOROUS (arb ball arithmetic, exact matrix exponential enclosure).
#   max(0,||Y||-eta)^2 <= Z <= (||Y||+eta)^2   (triangle inequality, since Z = ||exp(-beta'H/2)||_F^2) : RIGOROUS.
#   s=Z4(b)-/Z2(b)+^2, t=Z4(2b)-/Z4(b)+^2, then the win.py window recursion (W windows) in arb with lower-endpoint
#   propagation (every map used is monotone)  : RIGOROUS given eta.
import sys, itertools, json, numpy as np, flint
from flint import arb, arb_mat
flint.ctx.prec=600
J=1.0; h=5.0
X=np.array([[0,1],[1,0.]]); Z=np.diag([1.,-1]); I2=np.eye(2)
def op(L,ops):
    M=np.array([[1.]])
    for k in range(L): M=np.kron(M,ops.get(k,I2))
    return M
def bonds(L): return [(0,1),(1,0)] if L==2 else [(i,(i+1)%L) for i in range(L)]
def Hdense(L):
    H=np.zeros((2**L,)*2)
    for (i,j) in bonds(L): H-=J*op(L,{i:Z,j:Z}) if i!=j else 0
    for i in range(L): H-=h*op(L,{i:X})
    return H
def Hexact(L):  # exact integer matrix (J=1,h=5 integers) for arb
    return [[int(round(x)) for x in row] for row in Hdense(L)]
def expm_sym(M,t):
    w,V=np.linalg.eigh(M); return (V*np.exp(t*w))@V.T
def bond_h(L,i,j):
    hb=-J*np.kron(Z,Z) - (h/2)*(np.kron(X,I2)+np.kron(I2,X))   # field split over the 2 bonds of each site
    return hb
def run_mps(L,tau_total,chi,steps=32,order=2):
    # state psi[s1..sL, a1..aL] as operator Y[s,a]; start Y=I; each gate acts on physical legs only
    Y=np.eye(2**L).reshape([2]*(2*L))
    dt=tau_total/steps
    gates=[(i,j,expm_sym(bond_h(L,i,j),-dt)) for (i,j) in bonds(L)]
    if order==2:
        half=[(i,j,expm_sym(bond_h(L,i,j),-dt/2)) for (i,j) in bonds(L)]
        seq=half[:-1]+[gates[-1]]+half[:-1][::-1]
    else: seq=gates
    def apply(Y,i,j,G):
        G4=G.reshape(2,2,2,2); Y=np.tensordot(G4,Y,axes=([2,3],[i,j])); 
        return np.moveaxis(Y,[0,1],[i,j])
    def truncate(Y):
        # bring to site-grouped order (s1 a1)(s2 a2)... and compress left-to-right to bond dim chi
        T=np.transpose(Y,[x for k in range(L) for x in (k,L+k)]).reshape([4]*L)
        cores=[];rest=T.reshape(1,-1);r=1
        for k in range(L-1):
            rest=rest.reshape(r*4,-1);U,S,Vt=np.linalg.svd(rest,full_matrices=False)
            kk=min(chi,len(S));cores.append(U[:,:kk].reshape(r,4,kk));rest=S[:kk,None]*Vt[:kk];r=kk
        cores.append(rest.reshape(r,4,1))
        T=cores[0]
        for c in cores[1:]: T=np.tensordot(T,c,axes=([-1],[0]))
        T=T.reshape([2]*(2*L))
        return np.transpose(T,[2*k for k in range(L)]+[2*k+1 for k in range(L)])
    for _ in range(steps):
        for (i,j,G) in seq: Y=apply(Y,i,j,G)
        Y=truncate(Y)
    return Y.reshape(2**L,2**L)
def Zbounds(L,beta,chi,steps,order):
    Y=run_mps(L,float(beta.mid())/2,chi,steps,order)
    Ex=(arb_mat(Hexact(L))*arb(-beta)/2).exp()
    Ya=arb_mat([[arb(float(x)) for x in row] for row in Y])   # float64 -> exact arb
    D=Ya-Ex; n=2**L
    eta=sum((D[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt()
    nY=sum((Ya[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt()
    eta_up=(eta.mid()+eta.rad()) if True else None; eta_up=arb(eta.upper()); nYlo=arb(nY.lower()); nYhi=arb(nY.upper())
    lo=nYlo-eta_up; lo=arb((lo*lo).lower()) if lo>0 else arb(0); hi=arb(((nYhi+eta_up)**2).upper())
    Zex=Ex.trace() if False else sum((Ex[i,k]**2 for i in range(n) for k in range(n)),arb(0))
    assert lo<=Zex.upper() and hi>=Zex.lower()
    return lo,hi,float(eta.upper()),Zex
def G(x): return 1-(1-x)**2/(2*x*x)
def ok(s,t,beta,d,W):
    for j in range(W):
        K=arb((s*s*t).lower())
        if not K>arb(0.5): return False
        r=arb(((2*K-1).sqrt()).lower()); rho=arb(((1-r)/(1+r)).upper()); dd=arb((t/(1+rho*rho)).lower())
        a1=arb((s*dd.sqrt()).lower()); own=arb(((1-rho)*(a1 if a1<dd else dd if dd<a1 else arb(min(a1.lower(),dd.lower())))).lower())
        if not (own-(beta*d).exp()*(1-own))>0: return False
        if j==W-1:
            u=1-s if s<t else 1-t; u=arb(max((1-s).upper(),(1-t).upper()))
            return bool(u<=arb(1)/100 and 5*u*(beta*d).exp()<1)
        s=arb(G(s*s*t).lower()); t=arb(G(t*t*s).lower()); beta=beta*2
def best(s,t,beta,W):
    if not ok(s,t,beta,arb(0),W): return None
    lo,hi=0.0,10.0
    for _ in range(40):
        m=(lo+hi)/2
        if ok(s,t,beta,arb(m),W): lo=m
        else: hi=m
    return lo
if __name__=='__main__':
    beta=arb(1)/2; W=int(sys.argv[1]) if len(sys.argv)>1 else 8
    out={}
    # ideal (exact Z, enclosed): sanity vs 1.973380
    def Zex(L,b): return sum(((arb_mat(Hexact(L))*(-b)).exp()[i,i] for i in range(2**L)),arb(0))
    A,B,D=Zex(2,beta),Zex(4,beta),Zex(4,2*beta)
    sI=arb((B/A**2).lower()); tI=arb((D/B**2).lower())
    print('ideal (exact traces, enclosed): s',sI.str(10),'t',tI.str(10),'gap',best(sI,tI,beta,W),flush=True); out['ideal']=best(sI,tI,beta,W)
    for order in (2,1):
      for steps in (32,):
        for chi in (4,6,9,16):
            Alo,Ahi,e1,_=Zbounds(2,beta,chi,steps,order); Blo,Bhi,e2,_=Zbounds(4,beta,chi,steps,order); Dlo,Dhi,e3,_=Zbounds(4,2*beta,chi,steps,order)
            s=arb((Blo/Ahi**2).lower()); t=arb((Dlo/Bhi**2).lower()); g=best(s,t,beta,W)
            print(f'order={order} steps={steps} chi={chi}: eta(Z2b,Z4b,Z4_2b)=({e1:.3e},{e2:.3e},{e3:.3e}) s={s.str(8)} t={t.str(8)} gap={g}',flush=True)
            out[f'o{order}_s{steps}_chi{chi}']={'eta':[e1,e2,e3],'s':s.str(12),'t':t.str(12),'gap':g}
    json.dump(out,open(f'ising_mps_W{W}.json','w'),indent=1)
